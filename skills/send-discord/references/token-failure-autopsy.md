# Token Failure Autopsy — 2026-05-10

## What happened

During the daily skill registry sync cron job (2026-05-10), the final step (send Discord notification) appeared to fail for **all 17 bot tokens** in the vault — but this was later discovered to be a false negative from concurrent curl testing (see CORRECTION below). Only Researcher was actually dead.

## Validation log

### Attempt 1: send-discord CLI with "Dallas"
- Bot: `Dallas`
- Channel: `general` (1499264203708694540)
- Result: `401: Unauthorized`

### Attempt 2: send-discord CLI with "PaulBlart"
- Bot: `PaulBlart`
- Channel: `general` (1499264203708694540)
- Result: `401: Unauthorized`

### Attempt 3: Direct curl POST to channel
- Bot: `Dallas` token
- Endpoint: `POST /channels/1499264203708694540/messages`
- Result: `401: Unauthorized`

### Attempt 4: Direct curl GET /users/@me (identity check)
- Bot: `PaulBlart` token
- Endpoint: `GET /users/@me`
- Result: `401: Unauthorized`
- Significance: If the token were valid but lacked channel permissions, this endpoint would succeed. A 401 here means the token itself is rejected by Discord.

### All 17 tokens in vault (all failed)

| Bot Name | Status |
|----------|--------|
| Researcher | 401 |
| MarketingStrategist | 401 |
| ContentStrategist | 401 |
| Copywriter | 401 |
| EmailMarketingExpert | 401 |
| DataAnalyst | 401 |
| MediaMonitor | 401 |
| CustomerSupportSpecialist | 401 |
| ProjectManager | 401 |
| Coder | 401 |
| LegalCounsel | 401 |
| PersonalAssistant | 401 |
| QualityTester | 401 |
| ResearchQA | 401 |
| Dallas | 401 |
| PaulBlart | 401 |
| ops | 401 |

## Diagnosis

All 17 tokens failing simultaneously with 401 (not 403 Forbidden) points to a systemic cause:

1. **Discord application bot token reset** — A user regenerated the bot tokens in Discord Developer Portal
2. **Bot removed from server** — If the bot was kicked from the Solo Company OS server, all tokens for that bot would 401. But 17 different bots all failing suggests the Discord application itself was affected
3. **OAuth2 token expiry** — Bot tokens don't expire unless explicitly revoked, so this is likely a manual regeneration event

## Recovery needed

1. Regenerate at least one bot token in Discord Developer Portal
2. Update `/root/.vault/bot-tokens.txt.enc` with the new token
3. Validate with `curl -H "Authorization: Bot $TOKEN" https://discord.com/api/v10/users/@me`
5. If the bot was removed from the server, re-invite via OAuth2 URL generator

---

## CORRECTION (2026-05-15)

The "all 17 tokens 401" conclusion was produced by a concurrent shell loop that generated
**false negatives** from Discord rate-limiting. Retested sequentially: only **Researcher**
(app `1500590749157298236`) is actually dead. See `references/token-status-2026-05-15.md`
for the full sequential audit.
