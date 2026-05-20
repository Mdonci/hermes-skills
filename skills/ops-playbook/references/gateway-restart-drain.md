## Gateway Restart Drain — Why `systemctl restart` Hangs

**Observed:** 2026-05-14 during LegalCounsel delegation fix. After modifying config.yaml, agent_profiles.yaml, and delegate_tool.py, attempted `systemctl restart hermes-gateway` — command hung for 60s+, then timed out. `systemctl is-active` reported `deactivating` for 10+ minutes. Active Discord session was the blocker.

**Root cause:** The gateway drains active connections before shutdown (`restart_drain_timeout` in config.yaml). An active session keeps the drain from completing. `systemctl stop`, `systemctl restart`, and `SIGUSR1` all trigger the drain — none complete while connected.

**Symptoms:**
```
systemctl is-active hermes-gateway → deactivating (stuck for minutes)
systemctl stop hermes-gateway → hangs, eventually times out
SIGUSR1 → triggers ExecReload drain, same hang
```

**Workaround:** End the active session (user sends `/new` or disconnects). Gateway restarts on its own once all sessions drain. For urgent restarts, the only reliable path is to disconnect first.

**What does NOT work:**
- `kill -9` → orphans workers, leaves port in use, unclean restart
- Multiple stop attempts → all queue behind the drain
- `systemctl kill -s SIGKILL` → same as kill -9, unclean

**Lesson:** When making config/code changes that need gateway restart, plan for restart between sessions. Apply changes, notify user, session ends → systemd cycles.
