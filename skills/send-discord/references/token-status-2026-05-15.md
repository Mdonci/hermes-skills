# Token Status — 2026-05-15 (CORRECTION to May 10 autopsy)

## What changed

The May 10 autopsy reported all 17 tokens as 401. That conclusion was produced by a
concurrent shell loop that generated **false negatives** from Discord rate-limiting or
connection-reuse interference (see pitfall in SKILL.md).

When retested sequentially on 2026-05-15, only **1 of 17 tokens is dead**.

## Current status (sequential testing, 2026-05-15)

```
DEAD  Researcher             HTTP 401  app 1500590749157298236
OK    MarketingStrategist    HTTP 200  app 1500591918319403018
OK    ContentStrategist      HTTP 200  app 1500593341933551758
OK    Copywriter             HTTP 200  app 1500594110619193526
OK    EmailMarketingExpert   HTTP 200  app 1500594955952066771
OK    DataAnalyst            HTTP 200  app 1500597257316073544
OK    MediaMonitor           HTTP 200  app 1500597679217184978
OK    CustomerSupport        HTTP 200  app 1500598073699864688
OK    ProjectManager         HTTP 200  app 1500598436800630794
OK    Coder                  HTTP 200  app 1500598830410891364
OK    LegalCounsel           HTTP 200  app 1500599260671119411
OK    PersonalAssistant      HTTP 200  app 1500600445679304714
OK    QualityTester          HTTP 200  app 1500606921328296006
OK    ResearchQA             HTTP 200  app 1500703340114350170
OK    Dallas                 HTTP 200  app 1501227880078774482
OK    PaulBlart              HTTP 200  app 1501295063718826094
OK    ops (D.A.R.T.)         HTTP 200  app 1499264869801791518
```

16 of 17 tokens are valid. Researcher is the only broken one.

## Researcher bot details

- App ID: `1500590749157298236`
- Token prefix: `REDACTED_DISCORD_TOKEN_PREFIX`
- Hardcoded in: `/tmp/sco_bot_researcher.py`
- Service: `solo-company-os-researcher.service` (crash loop since May 9)
- Fix: regenerate token at https://discord.com/developers/applications/1500590749157298236

## System services status

- `hermes-gateway` → active (main D.A.R.T., works fine)
- 14 individual agent services → "active running" (but may be idle without coordinator)
- `solo-company-os-researcher` → activating/auto-restart (crash loop, exit code 1)
- `solo-company-os-bots` → failed (restart limit hit May 9, exit code 1)

## Diagnostic commands proven in this session

```bash
# 1. Check gateway status
systemctl is-active hermes-gateway
tail -30 /root/.hermes/logs/gateway.log | grep -iE 'discord|error|401|503'

# 2. Check agent services
systemctl list-units 'solo-company-os-*' --no-legend

# 3. Test individual token (RELIABLE method)
TOKEN=$(openssl enc -aes-256-cbc -pbkdf2 -d -salt -pass pass:DmanVault2026! \
  -in /root/.vault/bot-tokens.txt.enc 2>/dev/null | grep "^BotName:" | cut -d: -f2- | tr -d '[:space:]')
curl -s -w "\nHTTP %{http_code}\n" --connect-timeout 10 \
  -H "Authorization: Bot ${TOKEN}" https://discord.com/api/v10/users/@me

# 4. Decode app ID from token
echo "$TOKEN" | cut -d. -f1 | base64 -d

# 5. Check service error logs
journalctl -u solo-company-os-researcher --no-pager -n 20
```
