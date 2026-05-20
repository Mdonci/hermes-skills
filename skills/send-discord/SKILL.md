---
name: send-discord
description: "Send Discord messages as any bot from the Solo Company OS vault. Usage: send-discord <channel_name_or_id> <message> [bot_name]. Channel map: /root/.discord-channels. Bot tokens: /root/.vault/bot-tokens.txt.enc."
version: 1.0.0
---

# send-discord

Send a Discord message from any bot in the Solo Company OS using the vault-encrypted bot tokens.

## Location
`/root/send-discord`

## Usage

```bash
send-discord <channel_id_or_name> <message> [bot_name]
```

**Examples:**
```bash
send-discord general "Hello world" Researcher
send-discord 1499264203708694540 "Hello" Researcher
send-discord alerts "Alert message" PaulBlart
send-discord security "Security notice" QualityTester
```

## Known IDs (Solo Company OS server)

| Channel | ID | Status |
|---------|-----|--------|
| general | 1499264203708694540 | ✅ Working (2026-05-18) — D.A.R.T. bot token valid, REST 200, WebSocket connects |
| alerts | 1499508390294978691 | ✅ Working (2026-05-18) — direct Discord API POST with Dallas bot returned HTTP 200 |
| weather | 1499918035119640626 | 🔴 untested |
| legal | 1500391922156699749 | 🔴 untested |
| security | 1501295603227951194 | 🔴 untested |
| clickup | 1501317305718804611 | 🔴 untested |

**Current status (2026-05-18):** Alerts channel `1499508390294978691` is live — a direct Discord API POST succeeded with the Dallas bot token (HTTP 200). Current token checks: Researcher = HTTP 401, Dallas = HTTP 200, PaulBlart = HTTP 200, QualityTester = HTTP 200, Coder = HTTP 200. The earlier blanket-401 claim was at least partly a false positive from concurrent testing, but the Researcher token is currently invalid for API use.

## Known Bots (from `/root/.vault/bot-tokens.txt.enc`)

Researcher, MarketingStrategist, ContentStrategist, Copywriter, EmailMarketingExpert, DataAnalyst, MediaMonitor, CustomerSupportSpecialist, ProjectManager, Coder, LegalCounsel, PersonalAssistant, QualityTester, ResearchQA, Dallas, PaulBlart

## Files

- `/root/send-discord` — the CLI script (executable)
- `/root/.discord-channels` — channel name → ID mapping
- `/root/.vault/bot-tokens.txt.enc` — encrypted bot tokens (AES-256-CBC, passphrase: DmanVault2026!)
- `references/vault-and-api.md` — Discord vault decryption, API patterns, token extraction, and auth troubleshooting

## Important: Prefer Built-In send_message Tool

**Always use `send_message` tool first** before trying the CLI. The `send_message` tool (platform: `discord`, target: `discord:#channel-name`) bypasses the vault token entirely and handles auth internally. It was failing in this session with a 401 when called from Python/curl with the decrypted vault token, even though the token was correct.

CLI workflow → use when `send_message` is unavailable or for cross-bot routing that requires a specific bot's token.

**Known CLI pitfall (2026-05-18):** `/root/send-discord` does not trim trailing whitespace from decrypted tokens. On this system that caused false `401 Unauthorized` responses even when the raw token was valid. If the CLI returns 401, retry with a direct `curl`/Python POST that strips token whitespace before use.

**Vault decryption (if needed directly):**
```bash
openssl enc -aes-256-cbc -pbkdf2 -d -salt -pass pass:DmanVault2026! -in /root/.vault/bot-tokens.txt.enc 2>/dev/null | grep "^BotName:" | cut -d: -f2
```
Note: `-pbkdf2` flag is required. Without it, OpenSSL uses a deprecated KDF and decryption fails with "bad decrypt".


## Failure Modes

### All tokens return 401 (total outage)

Observed 2026-05-10: all 17 bot tokens in the vault returned `401: Unauthorized` when attempting to send to the `general` channel (1499264203708694540). The `/users/@me` endpoint also returned 401, confirming the tokens have been invalidated by Discord — not a server-side permission issue.

**Likely cause:** Discord token rotation event, bot re-authorization required, or the application was reset in Discord Developer Portal.

**Resolution path:**
1. Go to https://discord.com/developers/applications
2. Regenerate the bot token for at least one bot (e.g. "ops" or "Dallas")
3. Update the vault: decrypt `/root/.vault/bot-tokens.txt.enc`, replace the old token, re-encrypt
4. Validate: `curl -H "Authorization: Bot $NEW_TOKEN" https://discord.com/api/v10/users/@me` should return bot user info
5. Test a message: `curl -H "Authorization: Bot $NEW_TOKEN" -H "Content-Type: application/json" -d '{"content":"test"}' https://discord.com/api/v10/channels/1499264203708694540/messages`

### Pitfall: send_message tool not available in all contexts

The `send_message` tool (platform: `discord`) is Hermes Agent's preferred delivery path and bypasses vault tokens. However, **`send_message` is NOT available in all agent runtimes** — it may be absent from cron job sessions, certain profile configurations, or when the tool capability is not registered. Always have the CLI fallback ready.

### Pitfall: Concurrent token testing yields false 401s

When testing multiple tokens in a shell loop, concurrent or back-to-back curl calls to Discord's `/users/@me` can produce false 401s — even for valid tokens. This is likely Discord rate-limiting or connection-reuse interference.

**Wrong (false negatives):**
```bash
# while-read loop with curls inside — generates false 401s
openssl ... | while IFS=: read -r name token; do
  curl -s -H "Authorization: Bot $token" https://discord.com/api/v10/users/@me &
done
```

**Right (reliable):**
```bash
# Sequential calls with connect-timeout, one at a time
for name in Researcher MarketingStrategist Coder; do
  token=$(openssl ... | grep "^${name}:" | cut -d: -f2- | tr -d '[:space:]')
  code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 \
    -H "Authorization: Bot ${token}" https://discord.com/api/v10/users/@me)
  echo "$name: HTTP $code"
done
```

Always test tokens individually with `--connect-timeout 10`. If you get a blanket 401 from a loop, retest sequentially before concluding tokens are dead.

A channel can exist and accept messages (`200 OK`) while no bot can authenticate to it. Always validate at the token level before assuming a channel is usable. Test with `/users/@me` to confirm the token itself is valid.

```bash
echo "channel_name: CHANNEL_ID" >> /root/.discord-channels
```

## Adding a new bot

The bot token must already be in `/root/.vault/bot-tokens.txt.enc` as `BotName:TOKEN`.
