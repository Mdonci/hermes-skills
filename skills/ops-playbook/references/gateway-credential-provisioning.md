# Gateway Credential Provisioning — Three-Path Architecture

## Overview

The Hermes gateway has three independent credential paths. Understanding all
three is essential when adding or troubleshooting API keys for subagent delegation.

## The Three Paths

| Path | File | Loaded By | Best For |
|---|---|---|---|
| **Systemd Environment** | `/etc/systemd/system/hermes-gateway.service` | systemd (always, on start) | Critical API keys that delegation subagents need |
| **Encrypted vault** | `/root/.vault/secrets.txt.enc` | `load_vault_env.py` (sourced in ExecStart) | Keys that should be encrypted at rest |
| **`.env` file** | `/root/.hermes/.env` | NOT loaded by gateway | Only useful for manual CLI sessions |

### Path 1: Systemd Environment Directives (Most Reliable)

The gateway service file has explicit `Environment=` directives for critical keys:

```
Environment="MINIMAX_API_KEY=sk-cp-..."
Environment="DEEPSEEK_API_KEY=sk-..."    # added 2026-05-10
```

**Pros:** Always loaded, survives restarts, no decryption step.
**Cons:** Keys visible in plaintext in service file; requires `daemon-reload` after edit.

**Commands to modify:**
```bash
# Add a new key (insert after existing one)
sed -i '/Environment="MINIMAX_API_KEY=/a\Environment="NEW_KEY=value"' /etc/systemd/system/hermes-gateway.service
sudo systemctl daemon-reload && sudo systemctl restart hermes-gateway
```

**On restart, the `--replace` flag means the old process exits, then the new one starts.**
Restart can appear to hang for 30-60s. Check: `sudo systemctl is-active hermes-gateway`.

### Path 2: Encrypted Vault

`/root/.vault/secrets.txt.enc` is an OpenSSL AES-256-CBC encrypted file.
Decrypted by `load_vault_env.py` which maps vault key names to env var names.

**Current KEY_MAP** (from `/root/.hermes/scripts/load_vault_env.py`):
```python
KEY_MAP = {
    "minimax_api_key": "MINIMAX_API_KEY",
    "serpapi_key": "SERPAPI_KEY",
    "github_token": "GITHUB_TOKEN",
    "notion_api_key": "NOTION_API_KEY",
    "sherif_discord_webhook_url": "SHERIF_DISCORD_WEBHOOK_URL",
}
```

**DeepSeek was intentionally removed** from the vault on 2026-05-05 (Dman killed
all DeepSeek usage at that time). The KEY_MAP and vault both lack it.

To add a key to the vault:
1. Decrypt: `openssl enc -aes-256-cbc -pbkdf2 -d -in /root/.vault/secrets.txt.enc -pass pass:DmanVault2026!`
2. Add the key=value line
3. Re-encrypt: `openssl enc -aes-256-cbc -pbkdf2 -salt -in <plaintext> -out /root/.vault/secrets.txt.enc -pass pass:DmanVault2026!`
4. Add the mapping to KEY_MAP in `load_vault_env.py`
5. Restart the gateway

### Path 3: `.env` File (Not Loaded by Gateway)

`/root/.hermes/.env` contains `DEEPSEEK_API_KEY` and `MINIMAX_API_KEY` in plaintext.
This file is **not sourced** by the gateway service. It may be sourced by shell
profiles or manual CLI usage.

**Do not rely on `.env` for delegation subagents.** The gateway process does not
read it. The only reason it appears to work is that the main CLI agent (this
Hermes session) may have it in its environment via shell sourcing.

## Pitfalls

### New provider needs two independent changes

When adding a new model provider for delegation subagents:
1. **Config change** — model + provider in `config.yaml` delegation section
2. **Credential change** — API key in the gateway service Environment directives
   (or vault + load_vault_env.py if you prefer encryption)

Changing only the config without the credential path → subagent cannot authenticate.
The error may be silent (subagent returns empty or times out).

### Vault is not auto-synced with .env

The `.env` file and the encrypted vault are independent. Adding a key to `.env`
does not add it to the vault, and vice versa. The gateway only reads the vault
(and systemd Environment). If a key is only in `.env`, the gateway never sees it.

### `load_vault_env.py` KeyMaps must be updated

Adding a key to the vault file is insufficient — the `KEY_MAP` dict in
`load_vault_env.py` must also have the mapping from vault key name to env var name.
If the mapping is missing, the key is decrypted but not exported.

## Related

- `references/deepseek-credential-provisioning.md` in `coder-delegation-enforcement` skill — full discovery trace for the DeepSeek credential path (2026-05-10 session)
