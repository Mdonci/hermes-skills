# Claude Model Routing — Copywriter Agent (Lattice Glamping Session)

## Status: Claude NOT accessible via direct Anthropic API

The `ANTHROPIC_API_KEY` in `/root/.hermes/.env` authenticates to `api.anthropic.com` but returns HTTP 404 ("not_found_error") for ALL model names — including legacy models like `claude-2` and `claude-instant-1`. The key was added 2026-05-11.

### What was tried
- `claude-sonnet-4-20250514` → 404
- `claude-sonnet-4` → 404
- `claude-3-5-sonnet-20241022` → 404
- `claude-3-haiku-20240307` → 404
- `claude-2` → 404
- All at `api.anthropic.com/v1/messages`

### What works
Claude through the **MiniMax proxy** (`api.minimax.io/anthropic`) using the `MINIMAX_API_KEY` (sk-cp-... token plan key). The Hermes config already maps `claude-sonnet-4.6` → provider `minimax`. This route is stable for short outputs but times out on long-form (>800 word) subagent tasks.

### Key storage
- `ANTHROPIC_API_KEY`: `/root/.hermes/.env` (plaintext)
- Vault backup: `/root/.vault/anthropic_api_key.enc` (AES-256-CBC, passphrase: DmanVault2026!)
- For Copywriter: provider must be `minimax`, NOT `anthropic` (direct Anthropic provider doesn't work)

### If David asks about Claude
The key exists but needs to be re-provisioned or have billing added. At this time all Claude access goes through the MiniMax proxy at `api.minimax.io/anthropic`.
