# Discord API — Session Patterns

## Get channel ID by name (REST)

```bash
curl -s "https://discord.com/api/v10/guilds/<GUILD_ID>/channels" \
  -H "Authorization: Bot <BOT_TOKEN>" | python3 -c "
import json,sys
for c in sorted(json.load(sys.stdin), key=lambda x: x['id']):
    print(f'{c[\"id\"]:25} {c[\"type\"]:3}  #{c[\"name\"]}')"
```

## Send message — RIGHT way (jq approach)

```bash
MSG_JSON=$(jq -n --arg msg "$MESSAGE" '{"content": $msg}')
curl -X POST "https://discord.com/api/v10/channels/${CHANNEL_ID}/messages" \
  -H "Authorization: Bot ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$MSG_JSON"
```

## Vault token loading

```bash
BOT_TOKENS=$(openssl enc -aes-256-cbc -pbkdf2 -d \
  -in /root/.vault/bot-tokens.txt.enc \
  -pass pass:DmanVault2026!)

TOKEN=$(echo "$BOT_TOKENS" | grep "^${BOT_NAME}:" | cut -d: -f2- | tr -d ' ')
```

## Channel ID leading-space bug

`cut -d: -f2` on channel map file leaves a leading space. Must `tr -d ' '` or curl gets a 500.

## Known IDs (Solo Company OS server)

| Channel | ID |
|---------|-----|
| general | 1499264203708694540 |
| alerts | 1499508390294978691 |
| weather | 1499918035119640626 |
| legal | 1500391922156699749 |
| security | 1501295603227951194 |
| clickup | 1501317305718804611 |

GUILD_ID: `1499264202999595121`
D.A.R.T. bot ID: `1499264869801791518`
