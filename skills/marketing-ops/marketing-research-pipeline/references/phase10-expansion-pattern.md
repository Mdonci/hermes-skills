# Phase 10 — Angle Test Copy Expansion Pattern

## Case Study: Lattice Premium Glamping Units (2026-05-12)

### The Problem
First pass wrote all 20 angle test copies. Problem-Aware and Solution-Aware hit full length (1,000-2,500 words). Product-Aware and Most-Aware came back as 200-300 word stubs — summarized story arcs without the visceral detail required.

### The Fix
10 copies needed expansion. All 10 were expanded in 4 batched delegate_task calls of 3 copies each.

### Batching Strategy

| Batch | Copies | Subagents | Wall Time | 
|-------|--------|-----------|-----------|
| 1 | Angles 1-3 Product-Aware | 3 | ~215s |
| 2 | Angles 4-5 Product-Aware + Angle 1 Most-Aware | 3 | ~200s |
| 3 | Angles 2-4 Most-Aware | 3 | ~216s |
| 4 | Angle 5 Most-Aware | 1 | ~206s |

**Total: 4 calls, ~11 min wall time.** Each subagent took 130-215 seconds.

### What Each Subagent Received

The exact context structure that worked:

```
## Current Short Copy

[full stub content verbatim — the ~200 word version]

## Angle Structure

**Angle Name:** [name]
**Target:** [audience description]
**Story Arc:**
- beat 1
- beat 2
- ...

## Awareness-Level Framing

[what the reader knows at this stage]
- Product-Aware: Reader knows Lattice exists. They're hesitating on the price. The copy must validate their fear while reframing the cost of NOT buying.
- Most-Aware: Reader is on the waitlist or has it in their cart. They know what it does. The copy must create urgency — every trip without it is a waste.

## Format Requirements
- 1,200-1,400 words minimum
- First person personal story (buyer talking to reader)
- Conversational tone, 5th grade reading level
- Short paragraphs (1-3 sentences), punchy sentences
- Specific details (dollar amounts, times, locations, physical sensations)
- Hook at top (preserve the original)
- Punchy closing that ties back to the hook
- OVERWRITE file: /path/to/output/angleX-awareness.md
```

### Results

| File | Before | After |
|------|--------|-------|
| angle1-product-aware | ~200w | 2,494w |
| angle2-product-aware | ~200w | 2,209w |
| angle3-product-aware | ~200w | 2,169w |
| angle4-product-aware | ~200w | 2,563w |
| angle5-product-aware | ~250w | 2,334w |
| angle1-most-aware | ~200w | 1,675w |
| angle2-most-aware | ~200w | 1,916w |
| angle3-most-aware | ~200w | 2,823w |
| angle4-most-aware | ~200w | 1,488w |
| angle5-most-aware | ~200w | 2,203w |

All copies exceeded 1,200-word minimum. Most-Aware copies naturally run shorter than Product-Aware (1,400-1,900 vs 2,100-2,500) — acceptable since the Most-Aware reader needs urgency, not elaborate storytelling.

### Key Learnings
1. **One angle structure file** (`09-marketing-angles.md`) served as the single source of truth for all 4 awareness-level expansions of that angle
2. **Stub content is not wasted** — it provides the hook and story beats that the subagent expands
3. **Each batch produces files independently** — subagents write directly to disk; verify with `wc -w` after each batch
4. **Three at a time is the sweet spot** — avoids 600s timeout while keeping wall time manageable
5. **Deepseek-v4-pro handles this well** — no routing issues, each subagent returns with the file written
