# Google Drive rclone Reference

## Current Setup (VPS: 217.156.65.87)

### `gdrive:` — WordPress Site Backups (IN USE, DO NOT TOUCH)
- **Account:** Unknown (current OAuth app — not `mnakovics.david@gmail.com`)
- **Path:** `gdrive:aeternabiolab-backups/`
  - `db/` — WordPress SQL dumps (`wordpress_YYYYMMDD_HHMMSS.sql.gz`)
  - `files/` — WordPress file archives (`wordpress_files_YYYYMMDD_HHMMSS.tar.gz`)
- **Used by:** `/usr/local/bin/wordpress-backup.sh` (cron: `0 3 * * *`)
- **Token status:** Working as of 2026-05-01 03:00 UTC (sync completed successfully)
- **Token expiry:** Current token expires ~16:32 UTC on 2026-05-01. If `rclone about gdrive:` starts returning 401, reconnect with:
  ```
  rclone config reconnect gdrive:
  ```

### `dman-drive:` — Wikis / Personal Backup (TO BE SET UP)
- **Account:** `mnakovics.david@gmail.com`
- **Status:** NOT YET CONFIGURED
- **Next step:** Run `ssh -p 22 root@217.156.65.87 'rclone config'` → add new remote named `dman-drive` → device code OAuth flow → authorize `mnakovics.david@gmail.com`

## Reconnecting / Re-authenticating rclone

If rclone returns 401 or "token expired":

```bash
# On VPS
ssh -i /root/.ssh/hermes_dman_vps -p 22 root@217.156.65.87

# Reconnect existing remote
rclone config reconnect gdrive:

# For new remote (device code flow — no browser needed on server)
rclone config create dman-drive drive
# Then follow prompts for OAuth / device code flow
```

## Verifying Which Account a Remote Belongs To

```bash
rclone about gdrive:        # Shows used/total — confirms remote is alive
rclone listremotes          # Shows all configured remotes
rclone config show gdrive   # Shows client_id — use to identify OAuth app
```

**Current `gdrive:` OAuth client:** `606609600823-mets45of16qsns8g35q02e1bnni2ecn7.apps.googleusercontent.com` (NOT tied to `mnakovics.david@gmail.com`)
