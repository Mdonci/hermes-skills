# Discord 503 API Outage — 2026-05-08

## Symptom
Dman reports "can't send messages on Discord." Gateway was receiving messages fine but could not send responses. Log shows:

```
ERROR gateway.platforms.discord: [Discord] Failed to send Discord message: 503 Service Unavailable (error code: 0): upstream connect error or disconnect/reset before headers. reset reason: overflow
```

Same 503 on both primary send and fallback send attempt.

## Diagnosis

**All REST API calls to Discord returned 503, not just send:**
```
curl -s -o /dev/null -w "%{http_code}" "https://discord.com/api/v10/gateway"  → 200 (gateway URL fine)
curl -s -o /dev/null -w "%{http_code}" "https://discord.com/api/v10/users/@me" → 503
curl -s -o /dev/null -w "%{http_code}" "https://discord.com/api/v10/channels/<ID>/messages?limit=1" → 503
curl -s -o /dev/null -w "%{http_code}" "https://discord.com/api/v10/users/@me/channels" → 503
```

**Gateway was still receiving messages** — confirmed by `inbound message:` log entries. The bot's WebSocket connection (inbound direction) was working fine. Only the REST API (outbound send) was affected.

## Root Cause
Discord global API infrastructure outage — all REST endpoints were returning 503 while the WebSocket gateway remained partially operational.

## Key Diagnostic Pattern

```
# Test Discord API health — 3 calls, all must return 200 for bot to send
curl -s -o /dev/null -w "%{http_code}" "https://discord.com/api/v10/gateway"                  # → 200 means API reachable
curl -s -o /dev/null -w "%{http_code}" "https://discord.com/api/v10/users/@me"               # → 200 means token valid
curl -s -o /dev/null -w "%{http_code}" "https://discord.com/api/v10/channels/<CHANNEL_ID>"   # → channel accessible

# If gateway=200 but users/@me=503 → Discord is having an infrastructure outage
# If users/@me=401 → token is wrong or revoked
# If channel=404 → bot lost access to that specific channel
```

## Resolution
Wait for Discord to recover. The bot will resume sending once the API is back. No bot or config changes needed.

## Differentiation from Other Discord Failures

| Pattern | Meaning | Action |
|---------|---------|--------|
| `gateway` → 503, others → 503 | Discord global outage | Wait |
| `gateway` → 200, `users/@me` → 401 | Token invalid/revoked | Check `.env` / config.yaml |
| `gateway` → 200, `users/@me` → 200, `channels` → 404 | Bot lost access to channel | Re-invite or use different channel |
| `gateway` → 200, `users/@me` → 200, `channels` → 503 | Discord partial outage | Wait |
| Bot receives but cannot send | Either 503 outage OR channel access lost | Check `users/@me` first |