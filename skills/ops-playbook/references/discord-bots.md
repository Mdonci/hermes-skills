# Discord Bot Reference

## Active Bots

| Bot | Profile | Service | Model | Client ID |
|-----|---------|---------|-------|-----------|
| D.A.R.T. | (global) | `hermes-gateway.service` (sudo) | MiniMax-M2.7 | `1499264869801791518` |
| Researcher | `researcher` | `hermes-gateway-researcher.service` | deepseek-v4-pro | `1500590749157298236` |

## Researcher Bot — Setup Summary (2026-05-06)

**Token:** `REDACTED_DISCORD_BOT_TOKEN`
**Client ID:** `1500590749157298236`
**Model:** deepseek-v4-pro (deepseek provider) — updated from MiniMax-M2.7 on 2026-05-06

### Profile structure
```
/root/.hermes/profiles/researcher/
├── config.yaml        # model: deepseek-v4-pro + discord platform config
├── .env               # MINIMAX_API_KEY + DEEPSEEK_API_KEY + GATEWAY_ALLOW_ALL_USERS=true
├── SOUL.md            # Researcher persona
├── skills/            # 794 skills (copied from global on 2026-05-06)
├── memories/
├── sessions/
├── plans/
├── workspace/
├── home/
├── logs/
│   ├── gateway.log
│   ├── agent.log
│   └── errors.log
└── cron/
```

### config.yaml
```yaml
model:
  default: deepseek-v4-pro
  provider: deepseek

fallback_providers: []
credential_pool_strategies: {}

platforms:
  discord:
    enabled: true
    token: REDACTED_DISCORD_BOT_TOKEN
    require_mention: true
    free_response_channels: ""
    allowed_channels: ""
    auto_thread: true
    reactions: true
    channel_prompts: {}

agent:
  max_turns: 90
  tool_use_enforcement: ""

terminal:
  backend: local
  cwd: ""
  timeout: 180

display:
  skin: default
  tool_progress: off

checkpoints:
  enabled: false
  max_snapshots: 50

compression:
  enabled: true
  threshold: 0.5
  target_ratio: 0.2
```

### .env
```
MINIMAX_API_KEY=sk-cp-aP1j6YKa7ZvpKtHn9iClthd3jO6P3BbLlkQzf5zbpAhLRWdzWNawPBSXjeQApwGJaIX3G3EnMV1jU-dwHIDt4bcgCCSIJw1MOz0xI0hbaNprYJnz2ITUDLE
DEEPSEEK_API_KEY=sk-ce3b7a8690e74b27b4bf5f825e1f25f7
GATEWAY_ALLOW_ALL_USERS=true
```

### systemd service: /etc/systemd/system/hermes-gateway-researcher.service
```ini
[Unit]
Description=Hermes Gateway - Researcher
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.hermes/profiles/researcher
Environment=HERMES_HOME=/root/.hermes/profiles/researcher
ExecStart=/usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Key commands
```bash
# Start/restart
sudo systemctl restart hermes-gateway-researcher.service

# Status
sudo systemctl status hermes-gateway-researcher.service

# Logs
journalctl -u hermes-gateway-researcher.service --no-pager -f

# Gateway logs
tail -f /root/.hermes/profiles/researcher/logs/gateway.log
```

### Invite URL
```
https://discord.com/api/oauth2/authorize?client_id=1500590749157298236&permissions=8&scope=bot%20applications.commands
```

## Adding a New Discord Bot Profile

1. Create profile directory: `mkdir -p /root/.hermes/profiles/<name>`
2. Create `config.yaml` with discord token and desired model
3. Create `.env` with API keys for the model provider + `GATEWAY_ALLOW_ALL_USERS=true`
4. Create service file: `/etc/systemd/system/hermes-gateway-<name>.service`
5. `sudo systemctl daemon-reload && sudo systemctl enable hermes-gateway-<name>.service && sudo systemctl start hermes-gateway-<name>.service`
6. Copy skills from global: `cp -r /root/.hermes/skills/* /root/.hermes/profiles/<name>/skills/`
7. Note: `hermes gateway install` (the CLI command) may not work reliably — manual systemd setup is more robust

## Discord Duplicate Messages from Subagent Status Pings

If you see multiple identical messages like:
```
⏳ Still working... (21 min elapsed — iteration 7/90, running: delegate_task)
```
This is a **built-in Hermes subagent status ping** — not a script notification. It comes from `delegate_task` with `max_iterations=90` and is delivered to Discord by the cron job's `deliver=` setting.

**Diagnosis:** `cronjob list` → find `deliver=discord:<channel_id>` → identify which job runs the subagent pipeline.

**Jobs delivering to Discord that use subagents:** `OC Companies Daily Career Check` (→ `1499264203708694540`), `Daily Briefing` (→ `1499508390294978691`).

**Prevention:** Check `ps aux | grep jobbot` before re-running manually. Verify no stuck processes after a job completes.

## Gateway Log Locations

- Global (DART): `/root/.hermes/logs/gateway.log`
- Profile-specific: `/root/.hermes/profiles/<name>/logs/gateway.log`
