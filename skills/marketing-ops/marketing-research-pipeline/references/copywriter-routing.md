# Copywriter Model Routing Configuration

## How Copywriter Agent Routes (as of 2026-05-11)

The Copywriter agent resolves its model through TWO config layers:

### Layer 1: agent_profiles.yaml
File: `/root/.hermes/router/agent_profiles.yaml`
```yaml
copywriter:
  display_name: CopyWriter
  preferred_class: conversational
  default_profile: premium
  allowed_models:
    - deepseek-v4-pro    # works reliably
    - claude-sonnet-4.6  # requires minimax provider
  excluded_models: []
  fallback_chain:
    - deepseek-v4-pro
```

### Layer 2: model_catalog.yaml  
File: `/root/.hermes/router/model_catalog.yaml`
```yaml
claude-sonnet-4.6:
  provider: minimax      # NOT anthropic — goes through MiniMax proxy
  # ...
```

### Layer 3: model_assignments.json
File: `/root/.hermes/model_assignments.json`
```json
{
  "defaultModel": "deepseek-v4-pro",
  "agentAssignments": {
    "Copywriter": "deepseek-v4-pro",
    ...
  }
}
```

## Verified Working Combinations

| Prefix | Model | Status | Notes |
|--------|-------|--------|-------|
| `[Copywriter]` | deepseek-v4-pro | ✅ Works | Most reliable, no special config needed |
| `[Copywriter]` | claude-sonnet-4.6 | ⚠️ Provider must be minimax | Routes via api.minimax.io/anthropic proxy |
| `[Researcher]` | deepseek-v4-pro | ✅ Works | Good fallback when Copywriter route fails |

## Common Failure Mode
If `[Copywriter]` delegation returns 404 or times out:
1. Check `allowed_models` in agent_profiles.yaml — first model is preferred
2. Check `provider` in model_catalog.yaml for that model — must match a configured provider
3. If claude-sonnet-4.6 is first and failing, reorder to put deepseek-v4-pro first
4. After any config change: `sudo systemctl restart hermes-gateway`
5. Fall back to `[Researcher]` prefix — verified working path

## Timeout Reality
- deepseek-v4-pro 1,200-1,400 word copy generation: ~2-3 minutes
- 600s hard timeout on delegation
- Batch 2-3 copies max per delegation task
- Files persist on timeout — check on disk
