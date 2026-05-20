# Discord Vault & API Patterns

## Bot Token Vault

**Location:** `/root/.vault/bot-tokens.txt.enc`
**Format:** OpenSSL AES-256-CBC with salted PBKDF2
**Passphrase:** `DmanVault2026!`

### Decrypting tokens

**Correct command (requires `-pbkdf2` flag):**
```bash
openssl enc -aes-256-cbc -pbkdf2 -d -salt -pass pass:DmanVault2026! -in /root/.vault/bot-tokens.txt.enc 2>/dev/null
```

**Common mistake — omitting `-pbkdf2`:**
```bash
# WRONG — uses deprecated KDF, causes "bad decrypt"
openssl enc -aes-256-cbc -d -salt -pass pass:DmanVault2026! -in /root/.vault/bot-tokens.txt.enc
```

**Python Fernet attempt — not compatible:**
The vault uses OpenSSL's salted format, not Fernet. Python `cryptography.fernet` will throw `InvalidToken`. Use OpenSSL via subprocess or shell.

### Extracting a specific bot's token
```bash
openssl enc -aes-256-cbc -pbkdf2 -d -salt -pass pass:DmanVault2026! -in /root/.vault/bot-tokens.txt.enc 2>/dev/null | grep "^Dallas:" | cut -d: -f2
```

## Discord API Calls

**API base:** `https://discord.com/api/v10`

**Headers for bot messages:**
```
Authorization: Bot <TOKEN>
Content-Type: application/json
```

**Send message endpoint:**
```
POST https://discord.com/api/v10/channels/{channel_id}/messages
```

## Why send_message Tool Often Works Better

The `send_message` tool (Hermes built-in) routes through the gateway's active Discord session and does NOT need vault token decryption. It was returning 401 Unauthorized when tokens were used directly via curl, even with correct decryption — possibly due to:
- Gateway token caching
- Active connection using a different bot session
- Rate limiting or token rotation

**Use `send_message` first** for all Discord sends. Only fall back to CLI/curl with vault tokens when `send_message` is unavailable.

## Known Bot Tokens (decrypted)

| Bot | Token prefix |
|-----|-------------|
| Researcher | MTUwMDU5... |
| Dallas | MTUwMTIy... |
| PaulBlart | (in vault) |

## Known Channel IDs

| Channel | ID |
|---------|-----|
| general | 1499264203708694540 |
| weather | 1499918035119640626 |
| security | 1501295603227951194 |
