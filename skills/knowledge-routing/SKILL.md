---
name: knowledge-routing
description: "Route user queries to the correct wiki, system, or VPS based on intent keywords. Synthesizes answers from multiple routed sources."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [routing, multi-wiki, intent, dispatch]
    category: meta
    related_skills: [llm-wiki, hermes-agent]
---

# Knowledge Routing

Route user queries to the correct wiki, system, or VPS based on intent detection.
Handles single-source and multi-source (multi-part) queries.

## Wikis & Systems

| Wiki / System | Path | Location | Notes |
|---|---|---|---|
| peptide-wiki | `/root/peptide-wiki` | **LOCAL** | Agent host (not VPS) |
| ai-wiki | `/root/ai-wiki` | **LOCAL** | Agent host (not VPS) |
| marketing-wiki | `/root/marketing-wiki` | **LOCAL** | Agent host (not VPS) |
| career-wiki | `/root/career-wiki` | **LOCAL** | Agent host (not VPS) |
| meta-wiki | `/root/meta-wiki` | **LOCAL** | Agent host (not VPS) |
| VPS | `217.156.65.87` | Remote | WordPress, WooCommerce, SSL, server admin |

**Topology:** Wikis are on the machine running Hermes Agent — same machine Obsidian Desktop runs on.
No SSH needed to access them. obsidian-headless is only needed when the agent writes to a vault
from a *headless server* that has no local Obsidian install. If the agent and Obsidian are on
the same machine, they share the same files directly — no sync setup required.

## Intent Keywords → Route Mapping

| Keyword(s) in query | Route to |
|---|---|
| `peptide`, `shop`, `woo`, `product`, `supplier`, `bpc-157`, `semaglutide` | peptide-wiki + VPS |
| `marketing`, `ads`, `ad campaign`, `google-ads`, `meta-ads`, `tiktok-ads`, `seo`, `email campaign` | marketing-wiki |
| `lobster`, `openclaw`, `workflow`, `.lobster` | ai-wiki + check if VPS has lobster installed |
| `job`, `upwork`, `resume`, `interview`, `freelance`, `linkedin`, `contract` | career-wiki |
| `hermes`, `agent`, `skill`, `self-model`, `capability`, `memory`, `tool` | hermes-agent + meta-wiki |
| `vps`, `server`, `ssl`, `wordpress`, `woocommerce`, `hosting`, `ssh` | VPS commands |
| `what is`, `how does`, `who is`, `factual query`, `latest`, `search` | multi-search-engine (use first — don't answer from memory) |

## Dman's User Preferences (encode in every routing response)

- **Execution style:** "Can you do this?" = just do it. Don't ask, don't plan, don't offer options.
- **Tone:** Direct, no preamble, no "Sure thing!". Concise.
- **Formatting:** Plain text, no emoji walls, no ASCII boxes
- **If blocked:** Say why in one sentence, move on

## Routing Logic

### Step 1 — Parse Intent

Tokenize the query. Check for keyword matches (case-insensitive).
A query matches a route when any of its keywords appear.

### Step 2 — Determine Single vs Multi

- **Single route:** query matches only one wiki/system → fetch from that source only
- **Multi-part:** query matches multiple wikis → fetch from all routed sources and synthesize

### Step 3 — Fetch from Routed Sources

For each routed source:

1. **Wiki:** Read the relevant wiki's `SCHEMA.md` and `index.md`, then search for matching pages
2. **VPS:** Establish SSH connection using key `/root/.ssh/hermes_dman_vps`, run appropriate command
3. **Hermes Agent:** Load the `hermes-agent` skill, consult meta-wiki

### Step 4 — Synthesize

Combine results from all routed sources. Prioritize:
1. Most specific match (e.g., a page title match beats a content match)
2. Most recent update date
3. Highest confidence in frontmatter

## VPS Access

```bash
# SSH to VPS — ALWAYS use port 22 (22209 aaPanel SSH is broken)
ssh -i /root/.ssh/hermes_dman_vps -p 22 root@217.156.65.87
```

Common VPS operations:
- **WordPress/WooCommerce status:** `ssh` + `wp` CLI or direct file inspection
- **SSL certificate check:** `ssh` + `certbot certificates` or nginx/apache status
- **Backup:** `ssh` + `/root/scripts/backup.sh` or rsync commands
- **Service restart:** `ssh` + `systemctl restart nginx` / `systemctl restart wordpress`

## Multi-Wiki Example

**Query:** "How do I set up WooCommerce for peptide products and what SSL cert do I need?"

- Routes to: `peptide-wiki` + `VPS`
- peptide-wiki → pages on WooCommerce setup, product configuration
- VPS → current SSL certificate status
- Synthesize: Combined answer covering both shop setup and SSL requirements

## Session Context
## Session Context

Before routing, call `session_search` to check for relevant recent context.

```bash
# Check for recent context
session_search "<topic keywords>"
```

**⚠️ session_search false positives:** `session_search` matches any session containing the query string — including JSON tool schemas embedded in session files, not just actual tool invocations. A match on `delegate_task` in a session JSON is likely the tool's parameter schema, not a real delegation call. Always cross-check with log files (`bot-launcher.log`, agent logs) for operational truth. See `references/session-investigation.md` for the full investigation pattern.

## Pitfalls

- **Wikis are LOCAL — never SSH to check them.**
  at `/root/*-wiki`. Git operations (push/pull) are done locally. Only SSH to the VPS for
  server-side tasks (WordPress, cron, nginx, etc.).
- **obsidian-headless is rarely needed.** If the agent and Obsidian desktop run on the same
  machine, they share the vault files directly. obsidian-headless is only needed when the agent
  runs on a headless server and Obsidian runs elsewhere — in that case the wikis should live
  on the server and sync via Obsidian Sync.
- **VPS SSH: always use `-p 22`** — port 22209 (aaPanel) resets at key exchange. Use standard OpenSSH on port 22.
- **rclone OAuth tokens expire** — if `rclone about gdrive:` returns 401 or empty, the OAuth token has expired. Re-auth with `ssh -p 22 root@217.156.65.87 'rclone config reconnect gdrive:'` (device code flow). Current `gdrive:` remote uses an OAuth app tied to the original Google account — do NOT reconfigure it without checking which account it belongs to.

## Response Format

When synthesizing from multiple sources:

```
Based on [[wiki/page]] and VPS:
- [Point from wiki]
- [Point from VPS]
- [Combined synthesis]
```
