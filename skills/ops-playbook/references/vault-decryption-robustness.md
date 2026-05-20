# Vault Decryption Robustness Fix

## Problem

`load_vault_env.py` was crashing intermittently at gateway startup with:

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xbf in position 4: invalid start byte
```

This happened ~50% of the time — when OpenSSL produced corrupted binary output from the encrypted vault, Python's `subprocess.run(text=True)` tried to decode it as UTF-8 and crashed. The crash prevented systemd from starting the gateway, causing a 30-second retry loop that sometimes hit the same error again.

## Root Cause

Line 41 of `/root/.hermes/scripts/load_vault_env.py`:

```python
result = subprocess.run(
    ["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-d",
     "-in", VAULT_PATH, "-pass", f"pass:{vault_pass}"],
    capture_output=True, text=True, timeout=5,  # ← crashes on non-UTF-8 output
)
```

`text=True` tells `subprocess.run` to decode stdout as UTF-8. When OpenSSL produces binary garbage (corrupted vault file, wrong password, IPC glitch), the decode raises `UnicodeDecodeError` — and this propagates up through `decrypt_vault()`, `main()`, and kills the process substitution in the systemd ExecStart.

## Fix

Capture raw bytes, then attempt UTF-8 decode with `errors="replace"`:

```python
result = subprocess.run(
    ["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-d",
     "-in", VAULT_PATH, "-pass", f"pass:{vault_pass}"],
    capture_output=True, timeout=5,  # no text=True
)

if result.returncode != 0:
    return {}

# Decode with replacement for corrupted bytes — OpenSSL sometimes
# produces non-UTF-8 output when the vault file is damaged
try:
    stdout = result.stdout.decode("utf-8")
except UnicodeDecodeError:
    stdout = result.stdout.decode("utf-8", errors="replace")
```

The `errors="replace"` fallback inserts `�` (U+FFFD) for any undecodable bytes. Since the vault format is `key=value\n` lines, a corrupted line will typically fail to parse (no `=` sign) and be silently skipped in the key extraction loop. The script continues and exports whatever valid keys it extracted.

## Why This Pattern Isn't Just for the Vault

Any `subprocess.run(text=True)` against a process that can produce binary output is fragile. Alternative patterns:

1. **Capture bytes, decode with fallback** (used here) — safest for intermittent binary corruption
2. **Check exit code before decoding** — `returncode != 0` catch before `text=True` decode, but the decode can still fail mid-stream even with exit code 0
3. **`errors="replace"` in `text=True`** — not possible; `text=True` doesn't expose the `errors` parameter
4. **Use `communicate()` directly with Popen** — gives more control but more verbose

## Test

```bash
# Should print export lines or "# Vault not available" — never a traceback
python3 /root/.hermes/scripts/load_vault_env.py; echo "exit=$?"
```

## Affected Files

- `/root/.hermes/scripts/load_vault_env.py` — patched 2026-05-11
