---
name: self-diagnosis
description: "Daily automated health checks for Dman's infrastructure — VPS, Hermes cron, wikis, rclone backup, MySQL. Alerts to Discord channel 1499264203708694540 only when issues are found (alerts channel 1499508390294978691 is dead). Trigger: cron daily 16:00 UTC (8 AM PST)."
version: 1.4.0
author: Hermes Agent
license: MIT
triggers:
  - "daily cron health check"
  - "manual self-check"
  - "post-incident verification"
---

# Self-Diagnosis

Daily automated health checks for Dman's infrastructure. Sends Discord alerts only when issues found.

## Discord Alerting — Use Hermes send_message Tool, NOT Webhooks

**Important:** Do NOT try to create Discord webhooks via API. The bot lacks `MANAGE_WEBHOOKS` permission. Use Hermes's native `send_message` tool directly:

```
send_message(target="discord:1499264203708694540", message="🚨 Alert | <category> | <description>")
```

**⚠ Channel `1499508390294978691` (alerts) is dead (10003 Unknown Channel).** Always use `1499264203708694540` (general) for Discord delivery in cron jobs and alert targets.

Alert format: `🚨 Alert | <category> | <description>`

**Categories:**
- `VPS` — VPS health issues (disk, memory, CPU, connectivity)
- `CRON` — Hermes cron job failures or misconfigurations
- `GIT` — Wiki git repository issues (uncommitted changes, unpulled commits, detached HEAD)
- `RCLONE` — Google Drive sync issues
- `MYSQL` — Database connection or data issues

---

## Credentials

**All credentials are in the encrypted vault at `/root/.vault/secrets.pass.age`** (GPG AES256, passphrase: `DmanVault2026!`). For manual/interactive sessions, decrypt before running diagnostics.

**To get MySQL credentials from vault:**
```bash
echo "DmanVault2026!" | gpg --batch --yes --passphrase-fd 0 -d /root/.vault/secrets.pass.age 2>/dev/null | jq -r '.wordpress_db_user'   # → wp_user
echo "DmanVault2026!" | gpg --batch --yes --passphrase-fd 0 -d /root/.vault/secrets.pass.age 2>/dev/null | jq -r '.wordpress_db_password'  # → N3wW0rdPr3ss!2026
```

For automated cron jobs that cannot decrypt interactively, fallback credentials are:
- MySQL: `wp_user` / `N3wW0rdPr3ss!2026` (still functional but less secure — vault is primary)

---

## Diagnostics

### 1. VPS Health
- [ ] `ssh -i /root/.ssh/hermes_dman_vps -p 22 root@217.156.65.87 "echo ok"` — alert if fails
- [ ] Disk: `df -h /` — alert if > 90% used
- [ ] Memory: `free -m` — alert if > 90% used
- [ ] Load: `uptime`

### 2. Hermes Cron Status
- [ ] `hermes cron list` — check all jobs exist
- [ ] Check `/var/log/cron.log` for failures

### 3. Wiki Git Status
**Wikis do NOT live on AlexHost VPS.** The paths `~/peptide-wiki`, `~/ai-wiki`, etc. on 217.156.65.87 do not exist. Wikis are either on the Ionos local machine (check `/root/*-wiki/` locally) or have been retired. If wikis are found locally, run git checks locally (no SSH needed). If no wikis exist anywhere, skip this section and note it in the report.

When wikis exist locally on Ionos (not via SSH):
- [ ] `git status --porcelain` in each wiki dir — alert if uncommitted changes
- [ ] `git rev-parse --abbrev-ref HEAD` — alert if detached HEAD
- [ ] `git fetch --dry-run` — alert if remote fetch fails

**If wikis exist on a different VPS in the future**, SSH there first and check `~/peptide-wiki`, `~/ai-wiki`, `~/marketing-wiki`, `~/career-wiki`, `~/meta-wiki`.

### 4. Google Drive Rclone Sync
- [ ] `rclone version` — alert if not installed
- [ ] `REMOTE=$(rclone listremotes 2>/dev/null | grep -E ':$' | head -1 | tr -d ':')` — discover first available remote (avoids hardcoding `gdrive:` vs `driv:` mismatch)
- [ ] `rclone lsd "${REMOTE}:aeternabiolab-backups"` — verify Drive folder accessible using discovered remote name

### 5. MySQL Database
- [ ] `mysql -u wp_user -p'N3wW0rdPr3ss!2026' -e 'SELECT 1' wordpress` — alert if fails
- [ ] `mysql -u wp_user -p'N3wW0rdPr3ss!2026' -e 'SELECT COUNT(*) FROM wp_users' wordpress` — verify WP users table

### 6. Site Monitoring + Screenshots (Aeterna)
The site monitoring system is fully operational on the AlexHost VPS. It runs 3× daily and produces screenshots:
- **Schedule** (UTC): `0 16,0,8 * * *` → 8 AM PST / 4 PM PST / midnight PST
- **Backup** (files + DB): `0 11 * * *` → 3 AM PST
- **Screenshot dir**: `/backups/wordpress/screenshots/`
- **Latest screenshot**: `aeternabiolab.com_YYYYMMDD_HHMM.png`
- [ ] `ls -lh /backups/wordpress/screenshots/*.png | tail -3` — verify recent screenshots exist
- [ ] `cat /var/log/site-monitor.json | tail -1 | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['status'], d['http_code'], d['page_title'])"` — verify last check was OK
- [ ] `cat /var/log/site-monitor-cron.log | tail -5` — check for errors
- **Screenshot tool**: Playwright in `/opt/playwright-venv/bin/python` (NOT wkhtmltoimage — it hangs on Ubuntu 24.04 server)

### 7. Site Monitoring — Greta's Bakies (Hostinger)
Greta's Bakies runs on a Hostinger VPS at `89.116.192.34:65002`. HTTP checks run on Hostinger itself; screenshots are taken from the Ionos VPS (which has Playwright). Alert flags are written to `~/backups/logs/` on Hostinger.
- **Hostinger SSH**: `ssh -i /root/.ssh/hermes_hostinger -p 65002 u237753535@89.116.192.34`
- **Script**: `~/bin/site-monitor-gretas.py` (runs via wrapper `~/bin/site-monitor-wrapper-gretas.sh`)
- **Screenshot dir on Hostinger**: `~/backups/screenshots/`
- **Log dir**: `~/backups/logs/`
- [ ] `ssh ... "python3 ~/bin/site-monitor-gretas.py gretasbakies.com"` — verify HTTP check runs OK
- [ ] `ssh ... "cat ~/backups/logs/site-monitor-gretas.flag"` — verify last check shows OK
- [ ] `ssh ... "ls -lh ~/backups/screenshots/*.png | tail -3"` — verify recent screenshots (from Ionos)
- [ ] `cat ~/backups/logs/alert-gretas.flag 2>/dev/null` — check for pending alerts on Ionos side

### 8. Discord Gateway Health
Discord bot connectivity issues (gateway timeouts, silent failures, crash recovery) can be diagnosed in isolation from Hermes gateway.

**Session Log (2026-05-06):** `references/discord-gateway-timeout-2026-05-06.md` — hangs at `discord connect timed out after 30s` despite token and raw WebSocket working fine.
**Session Log (2026-05-08):** `references/discord-delivery-failure-2026-05-08.md` — delivery failure 10003 Unknown Channel, deadlock when trying to alert about Discord being unreachable.

**Gateway crash recovery procedure (2026-05-18):** The gateway can crash from provider API drops (Anthropic disconnect → reconnect attempt → exit code 1). When this happens, also check for competing old bot services:

```bash
# 1. Check gateway state
sudo systemctl status hermes-gateway

# 2. Kill old solo-company-os bot services (compete for same Discord tokens)
sudo systemctl list-units --all 2>/dev/null | grep 'solo-company-os' | awk '{print $1}' | while read svc; do
  sudo systemctl stop "$svc" 2>/dev/null
  sudo systemctl disable "$svc" 2>/dev/null
done

# 3. Kill stale sco_bot processes
ps aux | grep '[s]co_bot' | awk '{print $2}' | xargs -r kill -9 2>/dev/null

# 4. Restart gateway
sudo systemctl restart hermes-gateway

# 5. Verify
sudo systemctl is-active hermes-gateway
ps aux | grep -c '[s]co_bot'  # should be 0
```

**⚠ Old solo-company-os bot services:** These are 14 system-level services (`solo-company-os-<agent-name>.service`) from the pre-Hermes era. They compete for the same Discord bot tokens as the main gateway, causing connection conflicts. They should be stopped and disabled permanently — they are NOT needed now that the Hermes gateway handles all Discord traffic.

**Quick connectivity test (bypasses Hermes):**
```python
import asyncio, httpx, websockets, json

TOKEN = "BOT_TOKEN_HERE"  # Get from config.yaml discord.token

async def test_discord():
    async with httpx.AsyncClient() as client:
        # Test 1: Token validity via REST
        r = await client.get(
            'https://discord.com/api/v10/users/@me',
            headers={'Authorization': f'Bot {TOKEN}'},
            timeout=5.0
        )
        print(f"REST API: {r.status_code} — {r.json().get('username', r.text[:100])}")

        # Test 2: WebSocket gateway reachability
        gateway_url = (await client.get(
            'https://discord.com/api/v10/gateway',
            headers={'Authorization': f'Bot {TOKEN}'},
            timeout=5.0
        )).json()['url'] + '/?v=10&encoding=json'

        async with websockets.connect(gateway_url, open_timeout=5) as ws:
            hello = await asyncio.wait_for(ws.recv(), timeout=5)
            print(f"WebSocket: connected — {hello[:80]}...")

asyncio.run(test_discord())
```

If REST returns 200 and WebSocket connects with a HELLO frame → token and network are fine. The issue is in Hermes gateway's connection handling.

**Additional checks:**
- `rm -f /root/.hermes/gateway.lock` — stale lock file can prevent reconnection
- `ps aux | grep sco_bot` — kill stale solo-company-os bot subprocesses that may be holding the gateway connection
- `sudo systemctl status hermes-gateway-ops 2>&1 | head -5` — check for zombie ops service competing for same bot token
- Check `config.yaml` has `discord.token` set — missing token causes silent gateway failure

**Known failure modes:**
- **All bot tokens return 401 (total outage)** — ⚠️ REVISED 2026-05-15. The May 10 claim of "all 17 bots 401" was a false negative from concurrent curl testing. Retested sequentially: only **Researcher** (app `1500590749157298236`) is actually dead; 16/17 tokens are valid. See `send-discord` skill → `references/token-status-2026-05-15.md` for the full sequential audit. When diagnosing token failures, ALWAYS test tokens one-by-one with `--connect-timeout 10` — concurrent loop testing produces false 401s from Discord rate-limiting.
- **503 Service Unavailable (global Discord API outage)** — ALL REST endpoints return 503, not just specific channels. Discord's gateway URL (`/api/v10/gateway`) still returns 200, but channel/user endpoints return 503. This is a transient infrastructure outage, NOT a bot misconfiguration. Test with: `curl -s -o /dev/null -w "%{http_code}" "https://discord.com/api/v10/users/@me" -H "Authorization: Bot $TOKEN"`. If gateway returns 200 but users/@me returns 503 → Discord is down, bot is fine. Wait and retry. Session log: `references/discord-503-outage-2026-05-08.md`
- **10003 Unknown Channel** — Bot lost access to a specific channel (deleted, removed from server, or permissions revoked). Gateway still functions, other channels still work. The cron deliver="origin" path still captures output. Check `hermes cron list` for ⚠ Delivery failed flags — visible even when Discord delivery is down.
  - **⚠ Primary alerts channel `1499508390294978691` is dead (10003).** It was retired/deleted. The bot has been re-added to server but the channel ID is gone.
  - **Confirmed working channel: `1499264203708694540`** (general). All cron jobs that need Discord delivery should use this channel ID.
  - **Deadlock scenario:** If self-diagnosis tries to alert about Discord being unreachable to the dead channel, it deadlocks. Always use deliver="origin" for self-diagnosis output so it reaches the cron log even when Discord is down.
- **discord.py hangs at gateway connection but raw WebSocket succeeds** → possible IPv6 routing issue. Discord's gateway may prefer IPv6; if the path is broken for IPv6, discord.py fails whereas raw `websockets` library handles it gracefully. Force IPv4: add `Environment="GATEWAY_IPV4=1"` to systemd service, or disable IPv6 system-wide (`net.ipv6.conf.all.disable_ipv6 = 1` in sysctl).
- **Delivery failure `10003: Unknown Channel`** → deadlock situation. See `references/discord-delivery-failure-2026-05-08.md`.

### 9. Docker Containers
Docker containers run locally on the Ionos VPS. The container-updater cron job (`0c62984d8fa9`, every 6h) handles pulling and restarting; self-diagnosis should verify container health and flag any that are not running.
- **Container updater script**: `/root/.hermes/scripts/container-updater.sh`
- **Running containers** (expected): `hindsight`, `mcp-warden-gateway`, `mcp-warden-controller`, `mcp-warden-agents`, `mcp-warden-secret-broker`, `mcp-warden-obsidian`, `qdrant`
- [ ] `docker ps --format "{{.Names}}\t{{.Status}}" | sort` — list all containers and their status
- [ ] Alert if any expected container is not `Up` (running)
- [ ] Alert if container-updater failed to pull an image (check last run output at `~/.hermes/cron/output/0c62984d8fa9/`)
- **Note:** `mcp-warden-*` images may fail to pull if they are private or require Docker Hub authentication. If pull fails consistently, a `docker login` may be needed on the VPS.

---

## Cron Setup

The cron job (`3f9a14490161`) runs daily at **16:00 UTC** (not 08:00 UTC — schedule is `0 16 * * *`). Update via:
```
hermes cron edit 3f9a14490161 --prompt "..."
```

---

## Pitfalls

- **Do NOT use port 22209 for SSH to the VPS** — aaPanel's SSH daemon on 22209 resets connections at key exchange (kex algorithm mismatch with OpenSSH 9+). Always use `-p 22` explicitly. This was discovered by debugging "Connection reset by peer" on port 22209 while port 22 worked fine.
- **Wikis are NOT on AlexHost VPS** — `~/peptide-wiki`, `~/ai-wiki`, `~/marketing-wiki`, `~/career-wiki`, `~/meta-wiki` do NOT exist on 217.156.65.87. Wikis may be on Ionos local at `/root/*-wiki/` or may be retired. Check locally first. This pitfall was discovered when `cd /root/peptide-wiki` returned "No such file or directory" despite the skill stating they were on the VPS.
- **WordPress users table is `wp_users`** — NOT `wp_user`. The correct check is `SELECT COUNT(*) FROM wp_users`. WordPress table names use `wp_` prefix.
- **WordPress plugin path is deprecated** — `/var/www/html/wp-content/plugins/peptide-research-data/` is no longer in use. Do NOT include it in diagnostics.
- **Alert only when broken** — never send "all OK" messages to Discord. Suppress all output on success.
- **Do not use webhook curl for Discord** — bot lacks `MANAGE_WEBHOOKS` permission. Always use `send_message` tool for Discord alerts.
- **Always SSH on port 22** — port 22209 (aaPanel) resets at kex exchange. See `vps-management` pitfall #27.

---

## Related Skills

- `vps-management` — SSH port 22209 kex issue documented as pitfall #27; MySQL `wp_users` table as pitfall #28; Ionos disk size discrepancy (116G reported vs 120G actual)
- `self-improvement` — if a diagnosis finds a recurring issue, trigger self-improvement workflow
- `knowledge-routing` — uses wiki paths from this skill for routing decisions
- **Daily Briefing** (`/root/.hermes/pipelines/examples/daily_briefing.py`) — complementary to self-diagnosis. Self-diagnosis alerts only on problems. The daily briefing sends a bulletpointed emoji status report to Discord every morning regardless (VPS ping + disk, website visual check, Drive storage). Cron job: `779090870481` at 13:30 UTC. Key prefs: Ionos disk total 120 GB (df reports 116G — use hardcoded); AlexHost disk total 40 GB (df reports 38G — use hardcoded); screenshots NOT attached (website check still runs, text confirms title/business name only); Storage section uses `X/Y GB (Z%)` format for all lines; Google Drive label is `(Aelab)`. Update the briefing pipeline at `/root/.hermes/pipelines/examples/daily_briefing.py` directly.
