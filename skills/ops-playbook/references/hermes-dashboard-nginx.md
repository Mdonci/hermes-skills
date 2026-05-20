# Hermes Dashboard — nginx SPA Proxy Cheatsheet

## The Problem

The Hermes dashboard is a Single Page App (SPA). The HTML at `/dashboard/` references JS/CSS/assets at **root paths**, not `/dashboard/assets/`:

```
/dashboard/          → HTML (references /assets/, /fonts/, /api/, /plugins/)
/assets/             → JS/CSS (NOT /dashboard/assets/)
/fonts/              → Font files
/api/                → Backend API calls
/plugins/            → Dashboard plugin bundles
```

If nginx only proxies `/dashboard/`, all those supporting paths 404 — white screen after login.

## All Required nginx Location Blocks

```nginx
server {
    listen 80;
    server_name 74.208.34.157;

    location /dashboard/ {
        proxy_pass http://127.0.0.1:9119/;
        proxy_set_header Host 127.0.0.1:9119;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        auth_basic "Hermes Dashboard";
        auth_basic_user_file /var/www/html/.htpasswd;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:9119/api/;
        proxy_set_header Host 127.0.0.1:9119;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /assets/ {
        proxy_pass http://127.0.0.1:9119/assets/;
        proxy_set_header Host 127.0.0.1:9119;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /fonts/ {
        proxy_pass http://127.0.0.1:9119/fonts/;
        proxy_set_header Host 127.0.0.1:9119;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /plugins/ {
        proxy_pass http://127.0.0.1:9119/plugins/;
        proxy_set_header Host 127.0.0.1:9119;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /dashboard-plugins/ {
        proxy_pass http://127.0.0.1:9119/dashboard-plugins/;
        proxy_set_header Host 127.0.0.1:9119;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        auth_basic "Hermes Dashboard";
        auth_basic_user_file /var/www/html/.htpasswd;
    }

    # ... other locations (webhooks, key, etc.)
}
```

**CRITICAL:** `proxy_set_header Host 127.0.0.1:9119` — the dashboard validates the Host header and rejects external origins with "Invalid Host header". Never use `$host` here.

## Why /plugins/ and /dashboard-plugins/ Are Easy to Miss

The plugin entries in `/api/dashboard/plugins` look like API metadata. But when the browser loads the Kanban plugin, it fetches `/dashboard-plugins/kanban/dist/index.js` — a static asset served by the dashboard's own file server, not an API call. If `/dashboard-plugins/` isn't proxied, you get:
- Dashboard page loads (200 on HTML)
- API calls work (200 on /api/status)
- Kanban tab shows "Could not load this plugin's script. Check the Network tab"

Additionally, the Hermes dashboard itself serves plugin bundles at `/plugins/<name>/dist/index.js` (used by some plugins). Both `/plugins/` and `/dashboard-plugins/` must be proxied.

**Always test plugin loading after any nginx change.**

## systemd Service — Port Conflict on Restart

**Symptom:** Dashboard was running (PID started manually). Systemd service starts but immediately crashes with:
```
ERROR: [Errno 98] error while attempting to bind on address ('127.0.0.1', 9119): address already in use
```
Service enters restart loop — hundreds of restarts logged.

**Root cause:** The old manual process is still holding port 9119. Systemd can't bind, crashes, schedules another restart in 5s, repeats forever.

**Fix — kill stale process first:**
```bash
# Find what's on port 9119
sudo fuser 9119/tcp

# Kill it
sudo kill <PID>

# Then start/restart the service
sudo systemctl restart hermes-dashboard
```

**Prevention:** Before starting the systemd service, always verify port 9119 is free:
```bash
sudo fuser 9119/tcp 2>/dev/null && echo "PORT IN USE" || echo "PORT FREE"
```

**Note:** `systemctl is-active hermes-dashboard` returns `activating` while in a restart loop — it only returns `active` when the process holds the port successfully.
```

## Quick Diagnostic Commands

```bash
# Is the service running?
sudo systemctl is-active hermes-dashboard

# What's on port 9119?
sudo fuser 9119/tcp

# What's nginx seeing?
sudo tail -20 /var/log/nginx/error.log | grep dashboard

# Can the dashboard reach itself locally?
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:9119/

# End-to-end from outside (with auth)?
curl -s -o /dev/null -w "%{http_code}" -u "mdavid9@gmail.com:T32EdiSON" http://74.208.34.157/dashboard/
curl -s -o /dev/null -w "%{http_code}" -u "mdavid9@gmail.com:T32EdiSON" http://74.208.34.157/api/status
curl -s -o /dev/null -w "%{http_code}" -u "mdavid9@gmail.com:T32EdiSON" http://74.208.34.157/plugins/kanban/dist/index.js
```

## Auth Credentials

- URL: `http://74.208.34.157/dashboard/`
- User: `mdavid9@gmail.com`
- Pass: `T32EdiSON`
- htpasswd file: `/var/www/html/.htpasswd`

## Live nginx Config

Full config at: `/etc/nginx/sites-available/hermes-webhook`
