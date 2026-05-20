# Discord Gateway Connectivity — Session Debug Log

**Date:** 2026-05-06
**Token tested:** ops bot (D.A.R.T. / `hermes-gateway-ops` service)
**Symptom:** Gateway times out (`discord connect timed out after 30s`) but raw WebSocket test succeeds in <2s

---

## Key Findings

- **Token + network are fine.** REST API returns 200, raw WebSocket connects instantly.
- **The issue is in discord.py's connection handshake**, not the token or the network path.
- **Both the regular `hermes-gateway` and the ops service (`hermes-gateway-ops`) exhibit the same hang.**
- Raw WebSocket test uses `websockets.connect()` directly — succeeds. Discord `Bot` client hangs at connection.

---

## IPv6 Hypothesis

Discord's gateway may prefer IPv6 routing on the server. If the VPS has an IPv6 address but the path to `gateway.discord.gg` is broken over IPv6, discord.py may try IPv6 first, timeout, then fail to fall back to IPv4. The raw `websockets` library may handle this differently than discord.py.

**Test command:**
```bash
curl -v --connect-timeout 5 https://gateway.discord.gg/ 2>&1 | grep -E 'Trying|Connected|IPv'
```

**Fix if IPv6 is the issue:** Disable IPv6 on the server or force IPv4 in the gateway startup environment:
```bash
# In the systemd service file, add:
Environment="DISCORD_DISABLE_IPV6=1"
# Or in /etc/sysctl.conf:
net.ipv6.conf.all.disable_ipv6 = 1
```

---

## Gateway vs Ops Service

Both services run the same discord.py `Bot` client:
- `hermes-gateway` — primary gateway
- `hermes-gateway-ops` — ops service (separate systemd unit, separate config)

Both hang at the same point. This suggests a server-side network issue affecting discord.py specifically, not a token or configuration error.

---

## Diagnostic Checklist (Before Blaming discord.py)

1. `curl -v --connect-timeout 5 https://gateway.discord.gg/ 2>&1 | grep -E 'Trying|Connected|IPv'` — check which IP family is used
2. Raw WebSocket test (see SKILL.md Section 8) — verify token and network are working
3. If raw WS works but discord.py doesn't → network/firewall issue specific to discord.py's connection mechanism
4. Check if the VPS has a stale gateway lock: `rm -f /root/.hermes/gateway.lock`
5. Kill stale solo-company-os bot subprocesses: `ps aux | grep sco_bot | grep -v grep | awk '{print $2}' | xargs kill -9`
6. Check for competing service: `sudo systemctl status hermes-gateway-ops`

---

## Related

- `self-diagnosis` SKILL.md Section 8 — Discord Gateway Health
- `hermes-gateway-ops` systemd service — check when debugging ops bot connectivity
