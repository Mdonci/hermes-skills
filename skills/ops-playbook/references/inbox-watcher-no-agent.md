# Inbox Watcher — no_agent Conversion Reference

## The Problem

Job `0b1ab4567548` ("Inbox Watcher") was configured as an LLM-driven cron with `skill: ops-playbook`, firing a full AI model call every 1 minute.

**Token burn:** ~6,300 tokens × 1/min × 1,440 min/day = **~9M tokens/day**

The task itself — polling a directory for new files and creating request envelopes — is pure Python with zero reasoning required.

## The Fix

### 1. Write the wrapper script

```bash
#!/bin/bash
# /root/.hermes/scripts/inbox_watcher.sh

mkdir -p ~/solo-company-os/01_inbox

cd /root/solo-company-os && PYTHONPATH=/root/solo-company-os python3 -m ai-os.autonomy.inbox_watcher 2>&1
```

Key lesson: the inbox_watcher.py uses relative imports (`from .request_envelope import ...`), so it must be run as a module (`python3 -m ai-os.autonomy.inbox_watcher`) from the correct directory, with correct PYTHONPATH. Running it directly as a script fails with `ImportError: attempted relative import with no known parent package`.

### 2. Test standalone before updating the cron

```bash
bash /root/.hermes/scripts/inbox_watcher.sh && echo "---DONE---"
```

### 3. Update the cron job

```python
cronjob(
    action="update",
    job_id="0b1ab4567548",
    no_agent=True,
    script="inbox_watcher.sh",
    skills=[],
    prompt=""
)
```

### 4. Verify with a manual trigger

```python
cronjob(action="run", job_id="0b1ab4567548")
```

## Source Files

- `/root/solo-company-os/ai-os/autonomy/inbox_watcher.py` — InboxWatcher class, polls `~/solo-company-os/01_inbox` every 5s
- `/root/solo-company-os/ai-os/autonomy/request_envelope.py` — creates YAML envelope + copies to handoffs dir
- `/root/.hermes/scripts/inbox_watcher.sh` — wrapper script

## Key Imports Gotcha

```python
# This FAILS (relative import, no parent package)
from .request_envelope import create_request_envelope

# This WORKS (run as module from correct dir)
cd /root/solo-company-os && PYTHONPATH=/root/solo-company-os python3 -m ai-os.autonomy.inbox_watcher
```

The `--once` flag doesn't exist in the script (it always runs once via `run_once()` when used as a module). The polling loop is handled by the cron schedule (every 1m), not by the script itself.