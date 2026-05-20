# Discord API Health Check — Quick Reference

## Three-curl diagnostic

```bash
TOKEN="Bot $(grep discord.token ~/.hermes/config.yaml | awk '{print $2}')"
curl -s -o /dev/null -w "gateway: %{http_code}\n" "https://discord.com/api/v10/gateway"
curl -s -o /dev/null -w "users/@me: %{http_code}\n" "https://discord.com/api/v10/users/@me" -H "Authorization: Bot $TOKEN"
curl -s -o /dev/null -w "channel: %{http_code}\n" "https://discord.com/api/v10/channels/1499264203708694540" -H "Authorization: Bot $TOKEN"
```

## Result table

| gateway | users/@me | channel | Meaning | Action |
|---------|-----------|---------|---------|--------|
| 200 | 503 | 503 | Discord global API outage | Bot is fine — wait |
| 200 | 401 | — | Token invalid/revoked | Check `.env` / config.yaml |
| 200 | 200 | 404 | Bot lost channel access | Re-invite bot OR use different channel (`1499264203708694540`) |
| 200 | 200 | 200 | Both OK | Issue is permissions, rate limit, or code-side |
| 200 | 200 | 503 | Discord partial outage | Wait |

## Key distinction — 503 vs 404

- **503** = Discord infrastructure problem (global or channel-level API unavailable)
- **404** = Bot has lost access to a channel it could previously reach (removed from server, permissions revoked, channel deleted)

## From this session (2026-05-08)

Discord returned 503 on all REST endpoints during a global API outage. The gateway's WebSocket connection still received inbound messages, but outbound sends (REST API) all failed. Resolution: Discord self-recovered. No config or token changes needed.

## Related

- `self-diagnosis` skill → `references/discord-503-outage-2026-05-08.md` — full reproduction
- `ops-playbook` SKILL.md — Discord API Health Check section (top-level)