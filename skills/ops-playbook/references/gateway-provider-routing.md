# Gateway Provider Routing — Why Discord Uses the Wrong Provider

**Session:** 2026-05-10
**Symptom:** Discord bot stopped responding. `hermes config set model deepseek-v4-flash --provider deepseek` had been run, but all gateway requests still hit `Provider: minimax` with `HTTP 429: weekly usage limit reached for Token Plan Starter (15000/15000 used)`.

## Root Cause

The gateway had **both** `MINIMAX_API_KEY` and `DEEPSEEK_API_KEY` set in the systemd environment (`/etc/systemd/system/hermes-gateway.service`). Even though `config.yaml` said:

```yaml
model:
  default: deepseek-v4-flash
  provider: deepseek
```

...the gateway's runtime resolution still had access to MiniMax credentials, creating a fallback path. When the `deepseek` provider was used and hit a transient `RemoteProtocolError`, the fallback mechanism switched to `minimax`, which then hit the exhausted MiniMax Token Plan (15K/week Starter limit).

## Diagnostic Sequence

### 1. Check the gateway process environment

What credentials does the gateway actually have access to?

```bash
sudo systemctl status hermes-gateway --no-pager | head -30
cat /proc/<PID>/environ 2>/dev/null | tr '\0' '\n' | grep -iE "deepseek|minimax|api_key|base_url"
# Or read the systemd unit directly:
cat /etc/systemd/system/hermes-gateway.service | grep Environment
```

### 2. Check what provider the gateway logs show

```bash
sudo journalctl -u hermes-gateway --no-pager --since "30 min ago" | grep -E "🔌 Provider|provider=|model="
```

The log format is:
```
🔌 Provider: <provider>  Model: <model>
```

- `Provider: deepseek` + `Model: deepseek-v4-flash` → using DeepSeek API directly (correct)
- `Provider: minimax` + `Model: deepseek/deepseek-v4-flash` → routing DeepSeek through MiniMax (wrong — exhausting MiniMax tokens)
- `Provider: minimax` + `Model: deepseek-v4-flash` → also routing through MiniMax

### 3. Check what the runtime resolver computes

Test what `resolve_runtime_provider()` returns in the current shell:

```bash
python3 -c "
import os
from hermes_cli.runtime_provider import resolve_runtime_provider
result = resolve_runtime_provider()
print('Provider:', result.get('provider'))
print('Base URL:', result.get('base_url'))
print('API Key (first 20):', result.get('api_key', '')[:20] + '...' if result.get('api_key') else 'EMPTY')
print('Source:', result.get('source'))
"
```

If this returns `deepseek` with a valid key but the gateway is using `minimax`, the gateway has a stale or overridden resolution path.

### 4. Test the DeepSeek API key directly

```bash
curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "https://api.deepseek.com/v1/chat/completions" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"hello"}],"max_tokens":5}'
```

Expected: HTTP 200 with a valid completion. HTTP 401/403 means the key is invalid/expired.

### 5. Check the model_assignments.json

For subagent/bot routing (NOT main gateway), check:

```bash
cat /root/.hermes/model_assignments.json
```

The main gateway does NOT use `model_assignments.json` — it uses `config.yaml`'s `model.provider` and `_resolve_runtime_agent_kwargs()`. The `model_assignments.json` is used by the HermesModelManager (Node.js) for per-agent model overrides in subprocess delegation.

### 6. Check the .env file

```bash
cat /root/.hermes/.env | grep -iE "deepseek|minimax|provider|model"
```

The `.env` file can override env vars. If both `DEEPSEEK_API_KEY` and `MINIMAX_API_KEY` are set, the gateway has a fallback path.

## The Fallback Chain

When the gateway resolves provider credentials, the fallback chain works like this:

1. `_resolve_runtime_agent_kwargs()` → calls `resolve_runtime_provider(requested=os.getenv("HERMES_INFERENCE_PROVIDER"))`
2. If `HERMES_INFERENCE_PROVIDER` is not set, reads `config.yaml` → `model.provider`
3. Calls `resolve_provider(normalized)` which checks `PROVIDER_REGISTRY` for the provider
4. For API-key providers (like `deepseek`), reads the provider's configured env var (`DEEPSEEK_API_KEY`)
5. Gets the base URL from `pconfig.inference_base_url` (for deepseek: `https://api.deepseek.com/v1`)
6. Returns `{provider, api_key, base_url, api_mode, ...}`

**The fallback to minimax happens when:** the primary provider (deepseek) returns a `RemoteProtocolError` or `AuthError`, and the `fallback_providers:` list in config.yaml is consulted. If `MINIMAX_API_KEY` env var is set, the minimax provider has valid credentials and gets selected as fallback.

## Fix

Remove the competing provider's API key from the gateway's environment to prevent fallback:

```bash
# Edit the systemd unit
sudo sed -i '/MINIMAX_API_KEY/d' /etc/systemd/system/hermes-gateway.service
sudo sed -i '/MINIMAX_BASE_URL/d' /etc/systemd/system/hermes-gateway.service
sudo systemctl daemon-reload
sudo systemctl restart hermes-gateway
```

Or remove the key from `/root/.hermes/.env` and `load_vault_env.py` KEY_MAP.

After restart, verify:
```bash
sudo journalctl -u hermes-gateway --no-pager --since "1 min ago" | grep "🔌 Provider"
# Should show: Provider: deepseek  Model: deepseek-v4-flash
```

## Key Distinctions

| Concern | Config file | Runtime source | Used by |
|---------|------------|----------------|---------|
| Main model | `config.yaml` → `model.provider` | `resolve_runtime_provider()` | Main gateway (Discord, Telegram, Slack sessions) |
| Subagent model | `model_assignments.json` | `HermesModelManager` (Node.js) | `delegate_task` subagents |
| Fallback | `fallback_providers:` in config | `_try_resolve_fallback_provider()` | Gateway when primary auth fails |
| Vault env vars | `load_vault_env.py` KEY_MAP | `os.environ` | Both — all gateway processes inherit |
