# Discord Delivery Failure — 2026-05-08 (Channel Dead — May 2026)

## Symptom
Two Hermes cron jobs show `⚠ Delivery failed` with:
```
Discord API error 10003: Unknown Channel
```

Affected jobs:
- `3f9a14490161` Daily Self-Diagnosis
- `519a263ad63d` Daily Config Snapshot

## Root Cause — CONFIRMED DEAD CHANNEL
**Channel `1499508390294978691` (alerts) was deleted or the bot was removed from the server.** The 10003 is not recoverable — the channel ID no longer exists. The bot still has access to the server and other channels work fine.

## Confirmed Working Channel
- `1499264203708694540` (general) — bot has full access here
- All cron jobs that need Discord delivery should target `1499264203708694540`

## Diagnosis Path
1. `hermes cron list` — shows ⚠ Delivery failed flags (visible even if Discord unreachable)
2. Confirmed gateway is running but channel returns 404
3. Gateway logs confirm: `discord.errors.NotFound: 404 Not Found (error code: 10003): Unknown Channel`

## Deadlock
Self-diagnosis cannot send alert to channel it can't reach. The cron deliver="origin" still captures output. The delivery="discord" path fails silently.

## Resolution
1. All cron jobs → use `discord:1499264203708694540` for Discord delivery
2. Do NOT try to re-authorize channel `1499508390294978691` — it no longer exists
3. The alerts channel may need to be recreated in Discord and the new ID added to skills

## Prevention
When Discord delivery fails, the diagnostic output still reaches the cron log (origin deliver). Always check `hermes cron list` output for ⚠ flags — these are visible even when Discord delivery is down.
