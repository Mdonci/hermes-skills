# Remote PHP Editing Workflow (Aeterna VPS)

When editing PHP on the Aeterna VPS (root@217.156.65.87, key /root/.ssh/hermes_dman_vps), use this battle-tested workflow to avoid the shell-quoting fiascos that inevitably happen with complex inline code.

## 1. Read the File

```bash
ssh -i /root/.ssh/hermes_dman_vps root@217.156.65.87 "cat /var/www/html/wp-content/themes/astra-child/target-file.php"
```

For specific lines:
```bash
ssh -i /root/.ssh/hermes_dman_vps root@217.156.65.87 "sed -n '50,80p' target-file.php"
```

**Always use `sed -n`** (not `head -N | tail -M`) for line ranges — it's simpler and doesn't miscount.

## 2. Write a Python Patch Script Locally

Use `write_file()` to create a Python script in `/tmp/` that:
- Reads the target file
- Uses `str.replace(old, new)` for precise changes
- Writes back to disk
- Prints diagnostic messages

**Never use raw shell heredocs** for complex PHP/HTML edits. The quoting goes wrong with `$`, `\`, `"`, `'`, and backticks. Write a Python script instead.

**Use repr() to debug pattern matching:**
```python
old = """some multi-line PHP string"""
if old not in content:
    print(f"NOT FOUND: looking for {repr(old[:100])}...")
    print(f"Actual content around that area: {repr(content[content.find('some'):content.find('some')+500])}")
    exit(1)
```

## 3. Upload via Base64 (NOT SCP)

```bash
B64=$(base64 -w0 /tmp/patch_script.py)
ssh -i /root/.ssh/hermes_dman_vps root@217.156.65.87 "echo '$B64' | base64 -d > /tmp/patch_script.py && python3 /tmp/patch_script.py"
```

**Don't use SCP** — it requires the file to exist locally and adds latency. Base64 piping through SSH is faster and more reliable.

**Don't use heredocs** — you'll hit quoting issues with `$`, backticks, `\n`, PHP code containing `'` and `"`.

## 4. Verify with PHP Lint

```bash
ssh -i /root/.ssh/hermes_dman_vps root@217.156.65.87 "php8.3 -l target-file.php"
```

**Always do this.** A `str.replace` that's slightly off can insert code in the wrong place and create parse errors. The error message tells you the exact line number.

**Common PHP parse errors from bad patches:**
- `Unclosed '{' on line X` — a `{` brace opens but no `}` closes it (usually from deleting the wrong lines or inserting code mid-block)
- `Cannot use [] for reading` — using short array syntax `$x[]` in a context where PHP expects different syntax
- `Unexpected 'function' (T_FUNCTION)` — missing `if ( ! function_exists() )` wrapper, or inserting code outside a function body

## 5. Clear All Caches

```bash
find /var/www/html/wp-content/cache -type f -delete 2>/dev/null
find /var/cache/nginx -type f -delete 2>/dev/null
systemctl restart php8.3-fpm 2>/dev/null
```

**Three layers:** WP Rocket (wp-content/cache), NGINX (var/cache/nginx), OPcache (PHP restart). All three must be cleared. Missing even one means the CMS, the proxy, or PHP may serve stale code.

## 6. Verify the Live Response

```bash
# From the VPS itself (external requests to Aeterna may be blocked)
ssh -i /root/.ssh/hermes_dman_vps root@217.156.65.87 "curl -sk -H 'Cache-Control: no-cache' https://aeternabiolab.com/cart/ | grep -c 'your-target-string'"
```

**Don't request from the DART VPS (74.208.34.157)** — the Aeterna site blocks it (returns 403).

## Pitfalls

### Shell-quoting PHP strings inside SSH commands
The most common failure mode. `$` in PHP code is interpreted by the shell as a variable reference. `\n` is interpreted as newline. Backticks exec subprocesses. Use the Python script + base64 pattern to bypass all shell quoting issues entirely.

### Heredocs inside SSH commands
Even with `<< 'EOF'` (single-quoted delimiter = no shell expansion), the content can contain characters that break parsing at the bash level (e.g., `$()` in JavaScript, backticks in PHP strings). Always use Python files.

### sed with complex replacement strings
`sed -i 's/old/new/'` breaks when old or new contains slashes, backslashes, or special characters. The `\|` delimiter trick helps but multiple escapes make it unreadable. Use Python `str.replace()` for anything non-trivial.

### Browser cache after CSS changes
After clearing server caches, the CLIENT still has the old CSS in browser cache. Users must hard refresh (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows, or clear site data on mobile). This is the most common cause of "the CSS isn't working" complaints when the response is confirmed correct from curl. Always ask the user to hard refresh before debugging further.

### `static $done` CSS guard
The `aeterna_cart_shortcodes_assets()` function has `static $done = false;` — the CSS `<style>` tag is only output ONCE per page load. If you change the CSS string in the PHP file and the function was already loaded, the old CSS persists until the PHP process restarts. Clearing OPcache (`systemctl restart php8.3-fpm`) fixes this. Don't waste time debugging CSS that's already correct in the file — restart PHP first.
