# DeepSeek API — Rate Limit Diagnostics

## The 429 "usage limit has been reached" Error

DeepSeek returns **two distinct error types** that look similar but have different root causes:

| HTTP Status | Error Message | Meaning |
|------------|---------------|---------|
| 429 | "The usage limit has been reached" | Rate limit exceeded (RPM or TPM) |
| 402 | "Insufficient balance" | Account has run out of credits |

**Critical distinction:** A 429 does NOT mean the account is out of money. If the account has $5+ balance and gets 429, it is a rate limit, not a billing issue.

### Known Rate Limits (Paid Tier)

- **RPM (Requests Per Minute):** ~60 requests/minute
- **TPM (Tokens Per Minute):** ~80,000 tokens/minute
- Limits are **per API key**, not per model

### Common Causes on This System

1. **Parallel requests from delegation/subagents** — `delegate_task` spawns multiple subagents simultaneously, each making its own API call to DeepSeek. If 3 subagents fire at once, each with a standard input (skills + memory + tools + user message ≈ 17,800 tokens), that's ~53,400 TPM in one burst — well over half the TPM limit.

2. **Auxiliary services hitting DeepSeek simultaneously** — The Hermes config uses DeepSeek for compression, web_extract, session_search, and approval. If any of these fire while a main agent is also making a DeepSeek call, the combined TPM can exceed the limit.

3. **Multiple gateway processes sharing the same key** — If the main gateway + researcher gateway + cron jobs are all using the same `DEEPSEEK_API_KEY`, they share the same rate limit bucket.

### Quick Diagnostic

```bash
# Check if the account actually has balance (should NOT return 402)
curl -s https://api.deepseek.com/user/balance \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY"

# Test a minimal API call
curl -s -w "\nHTTP %{http_code}" \
  https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"ping"}],"max_tokens":5}'
```

### Fixes

1. **Wait ~60 seconds** — rate limits reset per-minute window
2. **Switch model/provider** — use Claude (Anthropic) or GPT (OpenAI) which have higher rate limits
3. **Throttle parallelism** — reduce `delegation.max_concurrent_children` in config.yaml from 3 to 1
4. **Distribute load** — move auxiliary services (compression, web_extract) to a different provider so they don't compete with the main agent for DeepSeek's rate limit
