---
name: email-strategy-production-system
description: "Proven multi-agent pipeline for producing premium, copywriter-ready email marketing strategies. Based on Qlean.hu project — PASS 96/100. Chain: Research → ResearchQA → MarketingStrategist → Copywriter → EmailMarketingExpert → DART (stitch) → QualityTester ×3."
version: 1.2.0
tags:
  - email-marketing
  - multi-agent
  - pipeline
  - strategy
  - premium
  - template
  - copywriting
  - visual-briefs
  - translation
---

# Email Strategy Production System

A templated multi-agent pipeline for producing premium, copywriter-ready email marketing strategies. Designed to be brand-agnostic — swap the target and competitors for any client.

## Pipeline Overview

```
D.A.R.T. (triage + brief)
  │
  ├─ 3× Researcher (parallel) ────────────── deepseek-v4-pro
  │    1. Client/Brand research
  │    2. Competitor deep-dive (3+ competitors)
  │    3. Channel/policy constraints and market landscape
  │
  ├→ ResearchQA (gate) ───────────────────── deepseek-v4-pro
  │    Validates evidence and source quality
  │    FAIL → retry delta back to Researcher
  │    PASS → proceed
  │
  ├→ MarketingStrategist ─────────────────── deepseek-v4-pro
  │    Strategic backbone:
  │    - Buyer psychology & belief ladder
  │    - Offer ladder & pricing logic
  │    - Reorder/replenishment architecture
  │    - Retention & loyalty design
  │    - Compliance & copy filters
  │
  ├→ Copywriter (flow briefs) ────────────── claude-sonnet-4-6
  │    Email-by-email flow briefs:
  │    - Welcome series (7+ emails)
  │    - Browse/cart abandonment
  │    - Post-purchase (first-time + repeat)
  │    - Replenishment / reorder
  │    - Winback / lapsed
  │    - Referral / review
  │    - Seasonal campaigns
  │    - Newsletter / editorial
  │    Each email: timing, subject direction, copy direction,
  │    proof type, CTA type, emotional job
  │
  │  └─> OUTPUT: Section 02 of master strategy document
  │
  │→ Copyworker (full body copy) ────────── claude-sonnet-4-6 / claude-opus-4-7
  │    PHASE 4b (AFTER strategy is approved):
  │    Takes Section 02 flow briefs and writes FULL body copy
  │    for EVERY email. No skeletons. No placeholders.
  │    EACH email includes:
  │    - Full body copy in English (for Hungarian → translate later)
  │    - Visual brief (colors, layout, photography direction)
  │    - Designer instructions (dimensions, fonts, mobile breakpoints)
  │    - Copywriting notes (psychological job, compliance traps)
  │
  │    Uses template at: templates/email-copy-package-header.md
  │
  ├→ EmailMarketingExpert ────────────────── deepseek-v4-pro
  │    Segmentation & operations:
  │    - Lifecycle map (Anonymous → Lapsed)
  │    - Risk scoring & segment definitions
  │    - Seasonal calendar
  │    - Testing roadmap (P0–P3)
  │    - Infrastructure roadmap
  │
## ═══════════════════════════════════════════════
## MANDATORY GATE: Writing Quality Verification
## ═══════════════════════════════════════════════
## 
## After EVERY copy production phase (both Flow Briefs
## and Full Body Copy), D.A.R.T. MUST run:
##
##   python3 /root/.hermes/scripts/humanize-verify.py <output-file.md>
##
## If FAIL (exit 10): Do NOT deliver. Either auto-fix with
## --fix for surface issues, or send back to Copyworker
## with the exact violations listed.
##
## See writing-quality skill → "MANDATORY ENFORCEMENT GATE"
## for full protocol.
##
## The verify script catches 30+ pattern categories across
## 6 severity tiers. This is the ONLY reliable way to know
## if a subagent actually applied the writing-quality audit.
## Subagents lie about compliance. The script doesn't.
## ═══════════════════════════════════════════════
  │
  └→ QualityTester ×3 (iterative gate) ──── claude-opus-4-7
       1st pass: deep structural check
       2nd pass: verify all fixes
       3rd pass: final approval
       PASS ≥ 90 → deliver
       Otherwise → back to D.A.R.T. for patches

### Mandatory Instruction: Hard Writing Quality Enforcement for Copyworker Subagents

> **⚠️ EXPERIENCE FROM LATTICE GLAMPING (May 2026): David rejected the first landing page copy because the copywriter used staccato fragments (\"Three minutes. One person. Zero tools.\"), em dashes, and disconnected sentences. The same pattern appeared in the first email copies. This is now a **hard enforcement rule**, not just a quality aspiration.**

When delegating copy body production to a Copyworker subagent, **include this exact instruction at the top of the context:**

```
CRITICAL: You MUST apply the writing-quality / humanize skill on your own output. Read the skill at ~/.hermes/skills/writing-quality/SKILL.md and enforce ALL of these rules:
- NO em dashes (—). Use periods, commas, or sentence breaks.
- NO staccato fragments. Connect sentences with "because," "so," "and," "which."
- NO staccato list patterns like "X. Y. Z." — write connected prose.
- NO Tier 1 AI vocabulary: no "delve," "tapestry," "beacon," "cutting-edge," "seamless," "game-changer," "leverage," "robust," "comprehensive," "paradigm," "testament."
- NO exclamation marks. Zero. None.
- NO rhetorical questions. If you know the answer, just say it.
- NO "it's not X, it's Y" pattern. State everything as a direct positive claim.
- NO "your wife." Use "your partner."
- Vary sentence and paragraph lengths. Some short. Some long. The rhythm should change.
- Pass the read-aloud test. Read each email aloud in your head. If it sounds like TTS or a spec sheet, rewrite it.
```

**After the subagent completes, independent verification is mandatory even if the subagent claims compliance.** Run:

```bash
# Quick scan for residual violations
grep -c '—' output-file.md                    # Should be 0 in body copy
grep -c '!' output-file.md                    # Should be 0
grep -cin 'your wife' output-file.md          # Should be 0
grep -cin 'delve\|tapestry\|beacon' output-file.md  # Should be 0
grep -in 'game-changer\|seamless\|cutting-edge\|leverage\|robust' output-file.md  # Should only appear in "words to avoid" lists
```

If violations are found in the body copy (not in metadata/headers/avoid-lists), **patch them directly** — do not re-delegate. The patch tool is faster and the subagent's self-reported "clean" output cannot be trusted.

**Real example from Lattice Glamping Track A:** The first copyworker pass had body copy written as staccato fragments. The subagent claimed the voice rules were enforced but the file contained disconnected sentences. Direct patch fixed the issue in seconds.

### Mandatory Step Between Stitch and QA: Cross-Section Reconciliation

> **⚠️ CRITICAL: This is not optional.** Three subagents writing different sections of the same strategy document WILL produce internally consistent but mutually contradictory work. This happened in the Lattice Glamping project (May 19, 2026): 6 load-bearing contradictions across 3 sections (tier structure, price anchor, campaign length, list size, revenue target, send count) that caused a FAIL 62/100 on first QA.

**After stitching all sections into the master document BUT BEFORE sending to QualityTester:**

1. **Run a cross-section consistency scan.** Check these specific parameters across all sections:
   - Tier names and prices (do all sections use the same offer ladder?)
   - Price anchor (same currency, same number throughout?)
   - Campaign length (same start and end dates?)
   - List size targets (same floor/target/stretch numbers?)
   - Revenue goals (same conservative/target/ambitious figures?)
   - Send counts (do the flow briefs match the phase plan's total?)
   - Welcome series length (do strategic and operational sections agree on email count?)
   - Flow names and timing (do all sections reference the same triggers and send windows?)
   - KPI targets (do all sections agree on open/CTR/conversion benchmarks?)
   - Downstream document numbering (do all sections agree on what Section 04, 05, etc. contain?)

2. **Create a reconciliation appendix** appended to the master document. For each contradiction:
   - State the authoritative decision
   - Explain what changed and why
   - Make the override explicit: "Where this appendix and any body text conflict, this appendix wins"
   - Be specific enough that an operator can execute without editorial guesswork

3. **Update the QA brief** to tell the QualityTester that the reconciliation appendix exists and to focus on:
   a) Whether the appendix resolves ALL contradictions
   b) Whether the decisions are clear and unambiguous
   c) Whether the document is now executable by a single operator

4. **Re-QA after the appendix is appended.** The initial QA (before appendix) will almost certainly FAIL on cross-section consistency. This is expected. The re-QA (after appendix) should PASS if the resolutions are complete.

**Real example from Lattice Glamping project:**
- Initial QA (no appendix): FAIL 62/100 — 6 critical contradictions across 3 sections
- 11-rule reconciliation appendix created
- Re-QA (with appendix): PASS 94/100

**The appendix is not a permanent fix** — the individual section files should be updated in the next editorial pass to match the reconciliation decisions. But for time-sensitive delivery (campaign deadlines), the appendix allows immediate execution while deferring the full rewrite.
```

### Phase 4c: Translation (post-QA)

**IMPORTANT — Translation is Phase 4c, NOT Phase 4b.** Full body copy must be written AND QA-approved FIRST, then translated. Never translate strategy flow briefs — only the production-ready copy file.

**Model:** claude-opus-4-7 only. Opus preserves tone, psychological triggers, and idiomatic flow across language gaps better than Sonnet at this volume. Sonnet produces more literal, less natural translations.

**Pipeline:**

```
D.A.R.T. (split copy file into ~400-500 line chunks at flow boundaries)
  │
  ├─ chunk1 ── delegate_task (parallel, claude-opus-4-7)
  ├─ chunk2 ── delegate_task (parallel, claude-opus-4-7)
  └─ chunk3 ── delegate_task (parallel, claude-opus-4-7)
  │
  └→ D.A.R.T. (VERIFY all chunks completed — check all -hu.md exist)
  │
  └→ D.A.R.T. (stitch chunks into one file, clean up overlap artifacts)
  │
  └→ D.A.R.T. (run grep QA scan — forbidden words, leftover English,
  │            duplicate headers, title case in body, "Ön", "előfizetés")
  │
  └→ D.A.R.T. (fix found issues with patch, not re-delegation)
  │
  └→ delegate_task (final QualityTester audit — flow, tone, compliance)
```

#### Chunk rules
- Split at FLOW boundaries (not mid-flow) using a Python script to find `# FLOW` line numbers
- Overlap chunks by ~2 lines at boundaries so no content is lost
- Each chunk delegate_task with `toolsets=["file"]` only — they don't need web
- Launch all chunks as `tasks` array in one `delegate_task` call for true parallelism

#### Translation rules (instruct each chunk subagent)
- Translate ONLY: subject lines, preview text, email body, CTA labels, blockquote testimonials, SMS text, inline examples
- KEEP IN ENGLISH: section headings, Visual Brief, Designer Instructions, Copywriting notes, Trigger descriptions, flow metadata, headers like "## Email 1.1 — Welcome + Discount Delivery"
- Preserve ALL markdown (bold, italics, blockquotes, links, horizontal rules)
- Preserve ALL merge tags ({{product_name}}, {{first_aroma}}, etc.) exactly as-is
- Preserve discount codes, pricing (Ft), shipping partners (GLS), payment methods (utánvét), phone numbers
- Sentence case only in target language — NO title case
- Warm, direct tone appropriate to the brand

#### Post-stitch cleanup pattern
After stitching, ALWAYS run these grep scans (the stitch WILL create overlaps):

```bash
# 1. Check for duplicate email headers
grep -c '## Email 11.1' output-file.md   # should be 1

# 2. Check all flow headers exist
grep '^# FLOW ' output-file.md | wc -l   # should match original count

# 3. Check forbidden words in customer-facing copy (exclude English notes sections)
grep -in 'forbidden_word' output-file.md

# 4. Check leftover English artifacts
grep -cin 'Starter Kit' output-file.md   # should be 0 in body copy
grep -cin 'deal' output-file.md
grep -cin 'Heads-up' output-file.md

# 5. Check target-language compliance
grep -cin 'Ön ' output-file.md           # should be 0 in body (if informal)
grep -cin 'előfizetés' output-file.md     # should be 0 in body (if "Klub" rule)
```

**Pitfalls:**
- ❌ Subagents may miss chunks if a delegate_task times out — always verify all expected `-hu.md` files exist
- ❌ Chunk boundaries at the SAME flow (e.g. middle of Flow 7) will produce duplicated content upon stitch — always split at flow boundaries
- ❌ Subagents don't catch their own compliance errors. The QA audit pattern from writing-quality skill is mandatory — never trust subagent self-reports
- ❌ Parallel sessions can be killed independently. Verify ALL expected output files before declaring done

### Post-stitch fix pattern

After QA finds issues, **patch directly**, don't re-delegate. The patch tool is faster and more precise:

```python
# Direct fix pattern — faster than re-delegating
patch(old_string="Heads-up.", new_string="Előre is szólok.", path="file.md")
patch(old_string="a aromát", new_string="az aromát", path="file.md")
patch(old_string="Starter Kit", new_string="Kezdőcsomag", path="file.md")
```

For bulk section removal (e.g. removing a duplicated block), use a Python script reading/writing lines by index.

## Two-Phase Copy Production

This pipeline has **two distinct copy phases** that should NOT be confused:

| Phase | Agent | Output | When |
|-------|-------|--------|------|
| **Flow Briefs** | Copywriter (strategy) | Subject direction, copy direction, proof type, timing per email — high level | During initial strategy creation (Section 02) |
| **Full Body Copy** | Copyworker (production) | Complete email text, visual briefs, designer instructions | AFTER strategy is approved and QA-passed |

**Do not attempt both phases in the same delegation.** The copy production phase depends on a QA-approved strategy document to write against.

## Copy Production Phase — Detailed Brief

When David says "write the email copies", delegate to Copyworker with:

1. **Load the strategy document** — the `-master.md` file from the output directory
2. **Include this exact requirement:** "Write every email in FULL body copy. No skeletons. No placeholders. No 'see above.' Each email must be complete and ready for a graphic designer to build."
3. **Require per-email output structure** (see template at `templates/email-copy-package-header.md`):
   - Subject line + preview text
   - Full body copy (English — Hungarian can be translated later)
   - Type: plain text vs. designed
   - Visual brief (hex codes, photography style, layout)
   - Designer instructions (dimensions, fonts, mobile requirements)
   - Copywriting notes (psychological job, compliance traps)
4. **Include a Creative Brief** at the top: brand voice, visual identity palette, photography style, do's/don'ts cheat sheet
5. **Specify the model** — use claude-opus-4-7 for full body copy (produces more specific, editorial-grade text than Sonnet for this volume of work)

### Common QA Failures in Copy Production
- Forbidden terms appearing in customer-facing body copy (even by accident — QA checker must scan the ENTIRE file)
- "Vapor", "switch", "inhaler" — these slip past compliance easily
- Missing SMS copy for Payment Failed flow (strategy says 3 emails + 1 SMS)
- Visual briefs not specific enough for a designer to execute (hex codes, exact dimensions, fonts)
- Body copy that reads like a template with placeholders — must be complete

### Translation-specific QA failures (from Qlean case)
- Denial-form forbidden words ("X nélkül" / "Y nélkül") pass subagent review but violate the brief. QA must check positive AND negative forms.
- Adjacent vocabulary (e.g. "pára" = ~"vapor") is easily missed. Scan with a word-root approach, not exact-match.
- Leftover English in what should be 100% translated body copy ("deal", "sales-pitch", "Starter Kit", "Heads-up.")
- Grammar bugs preserved from the original English that read wrong in the target language ("a aromát" → "az aromát")
- Untranslated newsletter/editorial sections — these are easy to miss because the QA doesn't read them as "body copy"

## Model Assignment (Why This Works)

| Role | Model | Provider | Why |
|------|-------|----------|-----|
| Researcher | deepseek-v4-pro | deepseek | Large context window (128K), cost-efficient for heavy reading and evidence gathering |
| ResearchQA | deepseek-v4-pro | deepseek | Same — validation needs breadth, not creative polish |
| MarketingStrategist | deepseek-v4-pro | deepseek | Strong strategic reasoning, large context for synthesis |
| Copywriter (flow briefs) | claude-sonnet-4-6 | anthropic | Best-in-class persuasive copy |
| Copyworker (full body copy) | claude-opus-4-7 | anthropic | Better editorial quality for 50+ email production |
| Copyworker (translation) | claude-opus-4-7 | anthropic | Opus preserves tone across language gap; Sonnet produces literal translations |
| EmailMarketingExpert | deepseek-v4-pro | deepseek | Operational/systematic work — good fit for segmentation logic |
| D.A.R.T. | - | - | Orchestration, stitch, reconciliation, patch, deliver |
| QualityTester | claude-opus-4-7 | anthropic | Highest rigor for final gate |

## Delegation Pattern

### Phase 1-3: Strategy Creation
```python
# PHASE 1: Parallel Research (3 at once)
delegate_task(tasks=[
  {
    "goal": "Research [BRAND] thoroughly...",
    "context": "Website URL, product lines, pricing, target audience...",
    "toolsets": ["web", "browser"]
  },
  {
    "goal": "Research competitors [COMP1], [COMP2], [COMP3]...",
    "context": "Focus on email strategy, subscription models, retention...",
    "toolsets": ["web", "browser"]
  },
  {
    "goal": "Research ad policy constraints and channel alternatives...",
    "context": "...",
    "toolsets": ["web"]
  }
])

# PHASE 2: ResearchQA
delegate_task(goal="Validate research evidence...", context="...", toolsets=["file", "web"])

# PHASE 3: Strategic Backbone + Copy Briefs + Ops (sequential)
delegate_task(goal="Create email marketing strategic backbone...", context="...", toolsets=["file"])
delegate_task(goal="Write email-by-email copy briefs...", context="...", toolsets=["file"])
delegate_task(goal="Design email segmentation and operations plan...", context="...", toolsets=["file"])

# PHASE 4a: DART stitches sections into master file
# PHASE 4b: Full body copy production (only after strategy approved)
delegate_task(goal="Write FULL body copy for every email...", context="...include strategy file...", toolsets=["file"])

# PHASE 5: Iterative QA (QualityTester ×3)
delegate_task(goal="Quality-assess the full email strategy...", context="...", toolsets=["file"])
```

### Phase 4c: Translation (post-QA)
```python
# PHASE 4c: Split copy file at flow boundaries and translate
# First: determine chunk boundaries with a python script
# Then: parallel delegate each chunk
delegate_task(tasks=[
  {
    "goal": "Translate the customer-facing copy in /path/to/chunk1.md to Hungarian...",
    "context": "Full translation rules (see skill references/qlean-hungarian-translation-case.md)",
    "toolsets": ["file"]
  },
  {
    "goal": "Translate the customer-facing copy in /path/to/chunk2.md to Hungarian...",
    "context": "...",
    "toolsets": ["file"]
  },
  {
    "goal": "Translate the customer-facing copy in /path/to/chunk3.md to Hungarian...",
    "context": "...",
    "toolsets": ["file"]
  }
])

# After all chunks complete:
# 1. VERIFY all -hu.md files exist (parallel sessions may be interrupted independently)
# 2. Stitch into one file
# 3. Run grep QA
# 4. Patch fix issues
# 5. Delegate final audit to QualityTester
```

## Master Document Structure

```
├─ Section 01 — Strategic Backbone
│   ├─ Market Diagnosis
│   ├─ Buyer Psychology & Belief Ladder
│   ├─ Offer Ladder & Pricing Logic
│   ├─ Reorder / Replenishment Architecture
│   ├─ Retention & Loyalty (Klub/Club design)
│   ├─ Copy Filters & Compliance (forbidden terms)
│   └─ Timeline / Roadmap
│
├─ Section 02 — Lifecycle Flow Briefs
│   ├─ Welcome Series (7 emails / ~10 days)
│   ├─ Browse Abandonment
│   ├─ Cart Abandonment (3 emails / ~72h)
│   ├─ Post-Purchase First-Time (4 emails / ~9 days)
│   ├─ Post-Purchase Repeat (3 emails / ~14 days)
│   ├─ Replenishment / Reorder (3-6 emails, SKU-based)
│   ├─ Klub Conversion (4 emails / ~30 days)
│   ├─ Payment Failed (3 emails + 1 SMS / ~5 days)
│   ├─ Winback (4 emails / ~30 days)
│   ├─ Review & Referral (2 emails)
│   ├─ Seasonal Campaigns (3-email structure per event)
│   ├─ Active Member Retention
│   └─ Newsletter / Editorial (2-4/month)
│
├─ Section 03 — Segmentation & Operations
│   ├─ Lifecycle Map & Risk Scoring
│   ├─ Replenishment Windows by SKU
│   ├─ Seasonal Calendar
│   ├─ Lead Capture Forms & Signup Strategy
│   ├─ Flow Architecture & Taxonomy Crosswalk
│   ├─ Testing Roadmap (P0–P3, ~12 months)
│   ├─ Testing Log Format & Governance
│   ├─ KPIs & Deliverability
│   └─ Infrastructure Roadmap (5-year)
│
└─ Section 04 — Dos & Don'ts Cheat Sheet
```

## QA Checklist (What QualityTester Checks)

- [ ] Flow count consistency (no "5 email" vs "7 email" contradictions)
- [ ] Timing consistency (all email send windows match)
- [ ] Timing correctness (replenishment windows make sense for the product)
- [ ] KPI window consistency
- [ ] Trigger consistency (automation triggers match flow descriptions)
- [ ] Forbidden terms are not used even in denial
- [ ] Offer ladder is consistent across all sections
- [ ] Dos/Don'ts section exists and is substantive
- [ ] Taxonomy crosswalk exists if multiple naming systems are used
- [ ] Pricing references match source material
- [ ] Subscription/retention architecture is clear
- [ ] Compliance section is present (for restricted niches)
- [ ] (Copy phase) Full body copy — no placeholders, every email complete
- [ ] (Copy phase) Visual briefs specific enough for a designer to execute
- [ ] (Copy phase) SMS included for Payment Failed flow
- [ ] (Copy phase) "vapor", "switch" (in cessation context), "inhaler", "puff" absent from body copy
- [ ] (Translation phase) All chunk output files exist — no gaps from interrupted sessions
- [ ] (Translation phase) No leftover English in body copy
- [ ] (Translation phase) Forbidden words absent even in denial form
- [ ] (Translation phase) Adjacent/root vocabulary scanned (e.g. "pára" → "párologtatás" root)
- [ ] (Translation phase) Target-language grammar verified (article agreement, etc.)
- [ ] (Translation phase) No duplicate email blocks from chunk-boundary overlap

## Output

### Strategy Document
- Single `.md` file at `/root/.hermes/research/output/[brand]-email-marketing-strategy-master.md`
- Commit to `/root/Personal` under `research/[brand]/[brand]-email-marketing-strategy-master.md`
- Deliver GitHub link to client

### Copy Production Package
- Single `.md` file at `/root/.hermes/research/output/[brand]-email-copies-complete.md`
- Includes Creative Brief + all email copies
- Commit to `/root/Personal` under `research/[brand]/[brand]-email-copies-complete.md`
- Deliver GitHub link — the graphic designer and copy translator both work from this file

### Translation
- Single `.md` file at `/root/.hermes/research/output/[brand]-email-copy-[language].md`
- Generated by chunking, parallel translation, stitch, QA, patch. Never a single-shot subagent task.

## Templates

| File | Purpose |
|------|---------|
| `templates/email-copy-package-header.md` | Creative brief structure + per-email output format for copy production phase |
| `templates/indiegogo-email-copy-package.md` | 5-track Indiegogo email copy template (Welcome/Launch/Mid/Last48h/Post) with per-email structure, AI image brief format, and writing quality rules |

## References

| File | Purpose |
|------|---------|
| `references/qlean-hungarian-translation-case.md` | Full case study: chunking, parallel translation, stitch, QA patterns, pitfall list |
| `references/copyworker-delegation-qlean-case.md` | Copy production delegation patterns from Qlean project |
| `references/lattice-cross-section-reconciliation-case.md` | Case study: 6 cross-section contradictions in parallel-subagent output, resolved via 11-rule reconciliation appendix (2026-05-19) |
| `references/lattice-cross-section-reconciliation-case.md` | Case study: 6 cross-section contradictions in parallel-subagent output, resolved via 11-rule reconciliation appendix (2026-05-19) |

## Key Lessons from Lattice Glamping (May 2026)

16. **Cross-section consistency must be enforced by DART before QA, not discovered by QA.** Three subagents writing in parallel WILL contradict each other on load-bearing parameters. Run a cross-section scan after stitch and resolve via reconciliation appendix before sending to QualityTester.

17. **Writing quality enforcement must be instructed to subagents, not just applied as a gate after.** Subagents claim compliance with voice rules but produce staccato fragments, em dashes, and Tier 1 vocabulary. Include the humanize rules as mandatory context in every copy delegation, not just as a check DART runs afterward.

18. **Full body copy for a crowdfunding campaign maps naturally to 5 tracks:** Welcome/Nurture (6 emails), Launch Week (4-5), Mid-Campaign (5), Last 48 Hours (3), Post-Launch (3). Save this structure as a template for future campaigns.

19. **Landing page copy and email strategy must share the same brand voice rules and price anchors.** The Lattice landing page showed €2,790 — the email strategy initially referenced $3,000. These must be reconciled before any copy is written.

20. **For $3,000 crowdfunding products, a 6-email welcome/nurture series is appropriate** (not the 3-email default). High consideration = more trust-building before the ask.

21. **AI image generation briefs in email copy packages are expected by David.** Each email should include a text-to-image prompt, style reference, lighting notes, and aspect ratio so the designer can generate supporting visuals without a separate briefing call.

## Key Lessons from Qlean

1. **Premium model tier matters.** Copywriter on Claude Sonnet, QA on Claude Opus — the quality delta is visible. Cheaping out here produces generic output.
2. **Parallel research first.** Don't start strategy until all three research streams are done and QA-validated.
3. **DART must reconcile sections.** Subagents produce internally consistent work but contradict each other. DART is the patch layer.
4. **Skip the first QA result.** The first QT round almost always finds things. Plan for 2-3 rounds.
5. **Taxonomy crosswalk prevents downstream confusion.** If three sections use three different naming systems (A–O, Flows 1–13, F1–F18), add a mapping table.
6. **Contradictions hide in: flow counts, timings, KPI windows, triggers, forbidden terms.**
7. **A good Deploy/Deliver step is a GitHub commit.** The client reads Markdown best there.
8. **Copy production is a separate phase, not part of strategy creation.** Only write full body copy after the strategy is QA-approved. The copyworker needs the approved flow briefs to write against.
9. **Visual briefs + designer instructions are standard.** David expects every designed email to include hex codes, hero image descriptions, layout specs, font sizes, and mobile breakpoints. The designer should be able to build from the document without a separate briefing call.
10. **Prefer claude-opus-4-7 for bulk copy production.** For 50+ emails, Opus produces more specific, less templated copy than Sonnet. The QA delta is visible at this volume.
11. **Compliance trap to watch:** "vapor" is not on the obvious forbidden list but is often used affectionately in aromatherapy brands — it gets past the copywriter but the QA checker must catch it. "Vapor mist" was flagged in Qlean.
12. **Translation is Phase 4c, not 4b.** Full body copy must be written AND QA-approved FIRST, then translated in parallel chunks on claude-opus-4-7. Do not translate strategy flow briefs — only the production-ready copy file.
13. **Verify ALL chunk output files exist after parallel translation.** A single timeout or interruption leaves a gap. Check file existence programmatically before stitching.
14. **Don't trust subagent compliance self-reports on translation.** The translation subagent said "all checks passed" while leaving 5 untranslated newsletter sections, denial-form forbidden words, and leftover English in the body copy. Always run independent grep QA after stitch.
15. **Post-stitch fix with patch, not re-delegation.** Fixing 15 small issues across 1900 lines takes 15 seconds with grep+patch vs. 3+ minutes re-delegating a QA subagent who'll miss the same things.

## Related Skills

- `writing-quality` — writing quality audit and rewrite system (useful for copy QA)
- `brandformance-marketing` — Dman's broader marketing system (strategy layer)
- `marketing-research-pipeline` — deeper research engine (6-phase, for heavier research needs)
