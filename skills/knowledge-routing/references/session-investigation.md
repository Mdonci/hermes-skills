# Session & Log Investigation Reference

Techniques for investigating Hermes Agent's own operational history — session transcripts, delegation logs, cron outputs, and agent process lifecycles.

---

## session_search False Positives for Tool Names

**Problem:** `session_search` matches any session containing the query string — including schema definitions embedded in session JSON, not just actual tool invocations.

**Symptom:** Searching for `delegate_task` returns every session that has the delegate_task tool schema in its tools array, even sessions where `delegate_task` was never called with real arguments. The `goal` field is empty (`{}`) because the schema defines the parameter shape, not the actual values.

**Correct verification:**
```python
# session_search says "delegate_task found" — verify whether it's a schema match or real call
python3 -c "
import json
with open('<session_file>') as f:
    data = json.load(f)
msgs = data.get('messages', [])
for msg in msgs:
    if isinstance(msg, dict) and msg.get('role') == 'assistant':
        args = str(msg.get('content', ''))
        if 'goal' in args and 'delegate' in args.lower():
            # This is a real invocation — content has goal+context
            print('REAL INVOCATION FOUND')
"
```

**Rule:** After `session_search` returns tool-name matches, always cross-check with actual log files for confirmation.

---

## Task Assignment / Delegation History

When asked "who did you assign X to" or "show delegation history":

1. **Check `bot-launcher.log`** (`/root/.hermes/logs/bot-launcher.log`) — shows process start/stop events with timestamps, not task assignments
2. **Check individual agent logs** (`/root/.hermes/logs/<agent>.log`) — per-agent request handling
3. **Check cron output** (`/root/.hermes/cron/output/`) — markdown transcripts of cron job runs
4. **session_search** — good for intent, but verify with logs (false positive risk)

**What bot-launcher.log shows:**
- Bot process lifecycle (start/stop/restart)
- No task-level detail — it's process management, not task routing

**What agent logs show:**
- Per-agent handling of requests
- Not cross-agent delegation visibility

**Actual cross-agent delegation** (D.A.R.T. → execution agents) lives in:
- The Solo Company OS Discord bot traffic itself
- D.A.R.T.'s own operational logs

---

## Cron Output Logs

Cron run transcripts are at `/root/.hermes/cron/output/<job_id>/`. Each is a markdown file with:
- Job metadata (ID, schedule, run time)
- Full prompt delivered to the cron agent
- Agent's response

Naming pattern: `YYYY-MM-DD_HH-MM-SS.md`

**Recent window query:**
```bash
find /root/.hermes/cron/output -name "*.md" -mmin -60 | sort
```

---

## Bot Process Logs

Bot logs at `/root/.hermes/logs/`:
- `gateway.log` — inbound messages
- `agent.log` — agent-level operations
- `bot-launcher.log` — process lifecycle (start/stop per agent)
- `bot-stdout.log` — captured stdout from agent subprocesses
- `<agent>.log` — per-agent operational logs

**Current bot roster** (14 agents + D.A.R.T.):
Researcher, MarketingStrategist, ContentStrategist, Copywriter, EmailMarketingExpert,
DataAnalyst, MediaMonitor, CustomerSupportSpecialist, ProjectManager, Coder,
LegalCounsel, PersonalAssistant, QualityTester, ResearchQA, PaulBlart
