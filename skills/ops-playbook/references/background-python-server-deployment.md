# Background Python HTTP Server Deployment

Pattern for running a Python stdlib HTTP server as a persistent background process on Dman's VPS.

## The Pattern

```bash
terminal(background=true, command="cd /root/project && export PYTHONPATH=./src && exec python3 -u -c '
from mymodule import run_server
run_server(host="0.0.0.0", port=8080)
'")
```

## Key Details

| Element | Why |
|---|---|
| `background=true` | Hermes terminal tool requires this instead of `&` for long-lived processes |
| `exec python3` | Replaces the shell process with Python — avoids orphan processes |
| `-u` | Unbuffered stdout/stderr — ensures log visibility in process output |
| `export PYTHONPATH=...` | Set module search path before Python starts (can't be changed after) |

## Pitfalls

### Old server process blocks the port
When you commit code changes and start a new server, the OLD server process may still be running holding the port. Always kill old processes first:
```bash
pkill -f "my_server_module" || true
sleep 1
ss -tlnp | grep <PORT> || echo "Port free"
```

### Process stays running with old code
Python caches imported modules. Even after the source file is modified on disk, the running process has stale code in memory. You MUST restart the process to pick up changes.

### No output in process log
The Hermes background process capture reads stdout. If `-u` is omitted, Python buffers stdout and the process log may appear empty even though the server is running correctly. Always use `python3 -u`.

### ThreadingHTTPServer required for concurrent requests
The stdlib `HTTPServer` is single-threaded — one slow request blocks all others (including health checks). Use `ThreadingHTTPServer` from `http.server` (Python 3.7+) for any server that handles operations with >1s latency:
```python
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
server = ThreadingHTTPServer((host, port), MyHandler)
```

### Basic Auth / Security
The stdlib http.server has no built-in auth. For public endpoints, put nginx in front with `auth_basic`. See `ops-playbook/references/hermes-dashboard-nginx.md`.

## HCIS Server Example

Start script at `/root/.hermes/scripts/start_hcis.sh`:
```bash
#!/usr/bin/env bash
cd /root/solo-company-os/ai-os/knowledge_foundry
export PYTHONPATH=./src
exec python3 -u -c "
from hcis.hindsight_client import HttpHindsightClient
from hcis.web_server import run_server
client = HttpHindsightClient(base_url='http://localhost:8888')
run_server(host='0.0.0.0', port=8080, client=client)
"
```

Invoke via:
```python
terminal(background=true, command="bash /root/.hermes/scripts/start_hcis.sh")
```

## Verification

After starting:
1. Wait 2-3 seconds for Python startup
2. `ss -tlnp | grep <PORT>` — confirm process is listening
3. `curl -s --max-time 5 http://localhost:<PORT>/health` — confirm endpoint responds
4. Check concurrent request handling by hitting health while a slow endpoint runs
