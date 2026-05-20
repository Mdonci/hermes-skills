---
name: marketing-research-pipeline
title: Marketing Research Pipeline
description: Full deep research + creative execution system. 6-phase research engine then 8-phase creative engine. Each phase has an approval gate.
domain: marketing
---

# Marketing Research Pipeline

## System Architecture

```
RESEARCH ENGINE (6 Phases)
Phase 1: Awareness Research  ──→  awareness_doc.md
Phase 2: Competitor Research ──→  competitor_doc.md (include US + European)
Phase 3: Avatar Research     ──→  avatar_doc.md
Phase 4: Master Research Doc ──→  master_doc.md (synthesizes 1-3)
Phase 5: Mass Desire Extract ──→  desires_doc.md
Phase 6: Desire Validation   ──→  validated_desires_doc.md

CREATIVE ENGINE (8 Phases) — DtS System
Phase 7:  Killer Hooks       ──→  hooks.md (10 hooks × ALL 5 awareness levels = 50 hooks)
Phase 8:  Desire Test Copy   ──→  desire_test_ads.md
Phase 9:  Marketing Angles   ──→  angles.md
Phase 10: Angle Test Copy    ──→  10-angle-test-copy/ (20 files: 5 angles × 4 awareness levels)
Phase 11: Advertorial (PAS)  ──→  advertorial_pas.md
Phase 12: Advertorial (Auth) ──→  advertorial_authority.md
Phase 13: Awareness Test Copy──→  awareness_test_ads.md
Phase 14: Testing Rules Doc  ──→  testing_strategy.md

Approval gate between EVERY phase
```

## Trigger
When David says: "Run deep research on [product]", "Run the pipeline for [product]", etc. — load this skill and begin.

## Prompt File Locations
- Research: `~/.hermes/research/prompts/research/`
- Creatives: `~/.hermes/research/prompts/creatives/`
- DtS system: `~/.hermes/research/prompts/dts/`
- Output: `~/.hermes/research/output/[product-name-slug]/`

## Delegation Failure Fallback Strategy

**Problem:** `delegate_task` can fail when the configured provider is unavailable (e.g., `openai-codex` not set up, provider credentials missing, or `AUXILIARY_VISION_PROVIDER` env var conflicts). The error looks like: `Cannot resolve delegation provider 'openai-codex': No Codex credentials stored.`

**Fallback — Do research directly, don't stall:**
1. If delegation fails 2+ consecutive times with provider errors, **pivot immediately to direct execution** using your own browser + web_search tools
2. Research multiple targets simultaneously by rotating between sites with `browser_navigate`
3. Use multi-query `mcp_minimax_web_search` (or other search tools) in parallel to cover: brand research, competitor analysis, niche advertising policies, marketing best practices
4. Compile findings manually into the standard pipeline document structure
5. Use `write_file` to save output to `~/.hermes/research/output/[product]/`
6. Continue to produce the deliverable at full quality — do not let delegation issues degrade output depth

**After fallback completes:**
- Note the delegation failure in the deliverable so the user knows there was a config issue
- Consider fixing the config (check `~/.hermes/config.yaml` delegation.provider setting, verify provider credentials, check for env var conflicts)

**Browser blocking fallback (Shopify/Cloudflare sites):**
When researching competitors on Shopify sites protected by Cloudflare, the browser may redirect to Google or fail silently. Detect this by checking the page title/snapshot. If it shows "Google" or lacks the expected brand content, switch to curl:

```bash
curl -sL -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" https://competitor.com/ | grep -oP '<h[1-6][^>]*>.*?</h[1-6]>' | head -30
```

Extract key signals from the HTML:
- `<h1>-<h6>` tags for brand messaging and product names
- `<meta name="description">` for positioning
- Navigation links (`<a>` tags) for product categories, pricing pages, subscription models
- Footer links for legal pages, terms, privacy — often reveal subscription terms

Cross-reference with web_search for additional context (brand history, funding, marketing strategy mentions).

## Model Configuration
- **Default model: deepseek-v4-pro** (set in config.yaml model.default)
- Research phases: use [Researcher] prefix → deepseek-v4-pro
- Creative phases: use [Copywriter] prefix → deepseek-v4-pro
- Agent priority: Copywriter > Researcher for creative work. If Copywriter routing fails (model unavailable), use [Researcher] as fallback — do not let model routing issues stall the pipeline

### Model Quality Tradeoffs (Creative Work)
- **deepseek-v4-pro** — Reliable, no routing issues. Handles 1,200+ word copy in 2-3 minutes via delegation. Output is structurally solid but can lack emotional texture and tends toward formulaic patterns in longer creative pieces.
- **claude-sonnet-4-6 (direct Anthropic API)** — Superior creative output: tighter storytelling, more emotional resonance, fewer repetitive patterns. Direct API path confirmed working (2026-05-18 fix). Hits 600s timeout on 4+ full document refactors — split into 2-doc batches for Mac+Narrative OS separately.
- **claude-opus-4-7** — Premium reasoning. Best for QualityTester gates where 600K+ token context is needed. **Do NOT use for strategy writing or copywriting per David's preference.** Opus is limited to QA/review gates only.
- **Rule of thumb:** When speed and reliability matter, use deepseek-v4-pro. When creative quality is make-or-break and task fits under ~2 docs per call, prefer claude-sonnet-4-6. Opus = QA only.

## Prompt Rules (Set in Stone)
All prompt templates at `~/.hermes/research/prompts/*/` are canon. Do NOT modify them. Only fill placeholders (e.g. [PRODUCT NAME], [NICHE], [INSERT MASS DESIRE]). The user has validated these across hundreds of executions — they are the system's DNA.

## Critical Execution Rules

### Phase 1-6 (Research Engine)
- Run 5-8 parallel web searches per phase for multi-query depth
- Use delegate_task with tasks array for parallelizable work (e.g. batch competitors)
- Use [Researcher] prefix for deepseek-v4-pro model override
- Two-pass pattern: broad sweep → identify gaps → deep follow-up on most promising threads
- Verify every phase against its embedded deliverable checklist before presenting
- Present to David for approval before proceeding to next phase

### New Client Bootstrap (CRITICAL — first run for a client)
When running the pipeline for a **brand-new client** with no prior research:

1. **Write the product spec card first.** Before any delegation, write the product spec card to `~/.hermes/research/output/[product]/product-spec-card.md` using the canonical template at `references/product-spec-card.md`. This becomes the source of truth for all subagents.
2. **Do your own web research first.** Run 5-10 parallel web searches yourself before delegating. The standard pipeline prompts assume prior research outputs exist. On first run, you are the initial researcher — D.A.R.T. must supply the seed context that subagents can then enrich.
3. **Feed findings into subagent context.** Package your initial web findings as structured context in the `delegate_task()` call. Subagents get your seed data + web search tools to extend it. Do NOT delegate a "blank canvas" and expect the subagent to do all the discovery from zero.
4. **Cross-check specs in every subagent output.** Subagents will invent plausible-but-wrong specs for your own product (wrong weight, wrong price, wrong dimensions) even when you provide correct data in context. After each subagent returns, grep for your product's spec values in the output to confirm they match.
5. **Run QA gate before presenting to David.** QualityTester will catch cross-document inconsistencies, but you should also spot-check before routing to QT.

### Phase 2 — Competitor Research (CRITICAL)
- Must find BOTH US-native AND European competitors
- US competitors are the PRIMARY threat — research them first
- European competitors are secondary (most lack US distribution)
- Search for US competitors specifically: pop-up camper brands, rooftop tent brands, teardrop manufacturers, glamping unit sellers
- Minimum 5 US competitors + any European ones David provides

### Phase 7 — Killer Hooks (CRITICAL RULE)
**Generate 10 hooks for EVERY awareness level (50 hooks total), not just the dominant one.**

Each hook must:
- Be 6-25 words
- Use personal first-person or specific scenario format
- Ground in verbatim quotes from Phase 3 Avatar Research
- Connect to Phase 1 awareness distribution data
- Reference Phase 2 competitor pricing where relevant
- Avoid marketing speak completely

Each awareness level requires different emotional framing:
- **Stage 1 — Unaware (35%):** Must first expose the problem they don't know exists. Make them aware of the pain.
- **Stage 2 — Problem-Aware (30%):** Agitate the known pain, hint at a solution. Dominant stage.
- **Stage 3 — Solution-Aware (22%):** Reframe the category. Challenge existing product comparisons. Reposition.
- **Stage 4 — Product-Aware (10%):** Build conviction. Address objections head-on ("is it just a fancy tent?").
- **Stage 5 — Most-Aware (3%):** Create urgency and FOMO. Offer-based. Price anchoring.

### Phase 8 — Desire Testing Ad Copy (CRITICAL RULE)
**Generate ad copy for ALL 5 mass desires × ALL 5 awareness levels = 25 copies total.** Each copy is 1,200-1,400 words following the Prompt #8 Personal Discovery Story format. Use [Copywriter] prefix for delegation (deepseek-v4-pro or claude-sonnet-4.6 via minimax). Each copy must use a different hook from Phase 7 matched to the correct awareness level. Ground every copy in the Master Research Doc (Phase 4) and Avatar Research verbatim quotes (Phase 3).

**CRITICAL RULE — First pass writes at FULL LENGTH (1,200-1,400 words). Do NOT write stubs.**
The backfill pattern (write 200 words → David says "these are short" → expand later) wastes a full delegation round. If delegation timeouts make full-length output unreliable, write fewer copies per batch (1-2 per delegate_task) or write directly. Every copy must hit 1,200+ words on its first appearance.

**Pre-presentation verification checklist (before showing David):**
1. `wc -w` on ALL 25 output files — verify every file is 1,200+ words
2. If ANY file is under 1,200 words, expand it before presenting — do NOT present with known deficits
3. David will catch short copies immediately and will require rework. Proactive expansion saves a full delegation cycle.

**PITFALL — Delegation timeout on large creative tasks:**
Subagents have a 600s hard timeout. A single 1,200-1,400 word ad copy typically takes 2-3 minutes for deepseek-v4-pro. Running 3+ copies in one delegation will likely time out. Strategy: batch 2-3 copies max per delegation task, or write copies directly if delegation is flaky. Files written by subagents survive timeouts — they remain on disk.

**Which awareness levels run short:**
In practice, copies for Time Reclamation and Physical Comfort land at full length (~1,200+ words). Relationship Harmony, Spontaneous Adventure, and Freedom from Clutter tend to come back at 200-500 word stubs — especially at Product-Aware and Most-Aware levels. Expect to expand these and batch them early.

**Copywriter routing:** The Copywriter agent routes via agent_profiles.yaml → allowed_models. If claude-sonnet-4.6 times out, switch to [Researcher] prefix which uses deepseek-v4-pro directly. Always verify model in result metadata (`results[i].model`).

**RECOVERY — Short copy expansion (applies to Phase 8 AND Phase 10):**
When subagent-produced copies come back under 1,200 words (common with inline writing), expand them via delegate_task in batches of 3:

```python
delegate_task(tasks=[
    {"goal": "Expand this ad copy from ~200 words to 1,200-1,400 words...",
     "context": "...stub content + angle structure + format requirements + output path",
     "toolsets": ["file"]},
    # ... 2 more similar tasks
])
```

Each subagent needs:
- The **stub content** — the existing short copy to expand
- The **angle structure** — story arc, target audience, emotional arc
- The **awareness-level framing** — what the reader knows at this stage
- **Format requirements** — 1,200-1,400 words, first person, conversational, 5th grade level
- The **exact output path** — subagents write directly via `write_file`

Subagents take 130-215 seconds each and produce full-length copies. Batch 3 per invocation (respects max_concurrent_children default). Verify with `wc -w` after each batch.

**Pro tip for Most-Aware copies:** Most-Aware (waitlist stage, 3% of market) naturally runs shorter. The hook should create urgency (discount closing, summer running out, cost of waiting). The story arc should frame the reader's hesitation as the true cost — every trip without Lattice is a trip they'll regret.

### Phase 9 — Marketing Angles

Generate 5 distinct marketing angles, each targeting a different persona segment from Phase 3 Avatar Research. Save as `09-marketing-angles.md`. Each angle must have:
- **Angle Name** — memorable, ownable (e.g., "The Weekend That Almost Didn't Happen", "The Body Remembers")
- **Target Audience** — specific demographic/psychographic with pain point
- **Story Arc** — 7-10 beat narrative (setup → crisis → discovery → transformation)
- **Unique Problem Mechanism** — the true root cause driving the frustration
- **Unique Solution Mechanism** — how the product solves THAT specific root
- **Key Emotional Moment** — the single scene that captures the transformation
- **Research Grounding** — verbatim quote from Phase 3

Angles must be distinct enough that "they could be 5 different people at a support group, each with a completely different story about the same problem."

### Phase 10 — Angle Testing Ad Copy (CRITICAL RULE)

**Generate ad copy for ALL 5 angles × 4 awareness levels = 20 copies total.** Awareness levels used: Problem-Aware, Solution-Aware, Product-Aware, Most-Aware. (Unaware is not tested at the angle stage.)

**CRITICAL RULE — Full length on first pass, then verify and expand before presenting.**
Do NOT show David Phase 10 until every single copy passes a `wc -w` check at 1,200+ words. The most common failure mode: Product-Aware and Most-Aware copies come back at 200-300 word stubs because the model runs out of steam on awareness levels that assume more reader knowledge. These MUST be expanded before you present.**

**File naming convention:**
```
10-angle-test-copy/
  angle1-product-aware.md
  angle1-most-aware.md
  angle1-problem-aware.md
  angle1-solution-aware.md
  angle2-... (20 files total)
```

**Production workflow — write all 20 in a first pass, then expand shorts:**

1. **First pass** — Write all angles × awareness combinations. Batch by angle (1 angle × 4 awarenesses) or by awareness level (5 angles × 1 awareness). Use [Copywriter] or [Researcher] prefix. Each subagent gets: angle structure + awareness-level framing + format requirements + output path.

2. **Verify word counts** — `for f in .../10-angle-test-copy/*.md; do wc -w "$f"; done`

3. **Batched expansion via delegation (CRITICAL STEP):**
   Product-Aware and Most-Aware copies frequently come back as 200-300 word stubs. Expand them 3-at-a-time via delegate_task:
   
   Each subagent context must include:
   - The **stub content** — existing short copy verbatim
   - The **angle structure** — from Phase 9 (story arc, target, emotional moment)
   - The **awareness-level framing** — what the reader knows at this stage
   - **Format requirements** — 1,200-1,400 words, first person, conversational, 5th grade reading level, short paragraphs, specific details
   - The **exact output path** — subagent uses `write_file` to overwrite the file
   
   Subagents take 130-215 seconds each. Batch 3 per delegate_task call (respects max_concurrent_children=3 default). Run batch 1 (angles 1-3), then batch 2 (angles 4-5 + 1 more), etc., until all 10 short copies are expanded.

4. **Final verification** — Re-run `wc -w` on all 20 files. Every copy must hit 1,200+ words.

**PITFALL — Do not proceed to Phase 11 with short copies.**
A stub (under 500 words) is not a valid angle test copy. Reject and expand before the user reviews Phase 10.

**Pre-presentation verification checklist (before showing David):**
1. `wc -w` on ALL output files in the phase — verify minimum word counts
2. Spot-read 2-3 copies to confirm story arc, hook, and closing are complete
3. If ANY file is under 1,200 words, expand it before presenting — do not present with known deficits
4. David will catch short copies immediately and will ask for rework. Proactive expansion saves a round-trip.

### Phase 11 — Advertorial (PAS) — Nightmare Personal Story

**Prompt file:** `creatives/11_-_creating_nightmare_personal_story_advertorial.md` (Lines 1-143 — the PAS/Nightmare Personal Story framework)

**Purpose:** Convert winning angle into a longer-form landing page that reads like an article but sells the product. Used to scale spend past FB-native ad limits.

**Target length:** 900-1,200 words

**Framework:** RMBC + PAS (Problem-Agitate-Solution)
- **Lead** — Statistics/urgency, promise of solution, tease discovery story, brief credibility, qualify audience
- **Background Story** — Customer narrator ("I was just like you"), traditional solutions failing, trigger/crisis moment, search for truth
- **UMP (Unique Mechanism of Problem)** — Counterintuitive explanation of root cause, scientific/logical backing
- **Product Buildup + Reveal** — Customer discovered product through research, testing/results story, proof it works
- **Close** — Product details/differentiators, social proof/testimonials, urgency/scarcity, guarantee, price justification, multiple CTAs, two-choice close

**Format rules:**
- Customer testimonial format — narrator is a CUSTOMER who discovered the product, NOT the company owner (explicit: "not affiliated")
- 5th grade reading level — sentences under 15 words, 1-3 sentence paragraphs
- **Bold** key statistics, shocking revelations, solution benefits, urgency/scarcity, guarantee terms, CTAs
- Opening hook: 6-12 words, punchy, cuts to core pain/fear
- Subheadlines as standalone story beats (facts, not questions)
- Multiple CTAs throughout (minimum 3)
- Two-choice close (before/after or option A/B)
- Reference example: Google Drive 1Tac Roadside Safety Advertorial + Cat Dehydration Advertorial (URLs in prompt file)

**Mass desires to target:** Prevention of Crisis, Peace of Mind, Understanding

**Delegation pattern:**
```python
delegate_task(tasks=[
    {"context": """## Phase 11(a) Framework
[Full framework text from prompt file — see references/advertorial-pattern.md for exact structure]

### Angle: [Name]
**Target:** [audience]
**Story Arc:** [beats]
**Core Pain:** [one-line]

**UMP (Unique Mechanism of Problem):** [the hidden root cause]
**UMS (Unique Mechanism of Solution):** [how product fixes UMP]

### Format Requirements
- 900-1,200 words
- Customer testimonial, NOT company owner
- RMBC structure + PAS flow
- 5th grade reading level
- **Bold** key elements
- Opening hook 6-12 words
- Multiple CTAs (≥3)
- Two-choice close

### Output
Write to: /root/.hermes/research/output/[product]/11-advertorials/angleX-pas-advertorial.md""",
     "goal": "...", "toolsets": ["file"]},
    # ... 2 more similar tasks
])
```

**IMPORTANT — Develop ALL angles at professional grade.**
When David says "proceed with Phase 11" (or any creative phase after angles are defined), the expected output is ALL 5 angles at full professional length. Do NOT ask which angle to use. Do NOT pick one. Execute exhaustive coverage — batch 3 per delegate_task call, then 2, until all 5 are produced.

**Batch strategy:** 3 per call (max_concurrent_children=3 × default). Two calls covers 5 angles. Verify with `wc -w` afterward.

**PITFALL — One prompt file serves two phases:**
The file `11_-_creating_nightmare_personal_story_advertorial.md` contains BOTH the PAS framework (lines 1-143, used for Phase 11) AND the Authority Revelation framework (lines 146-299, used for Phase 12). Do NOT confuse them. Phase 11 uses the customer testimonial format with RMBC + PAS. Phase 12 uses the expert/whistleblower format with UMP + UMS.

**PITFALL — Don't ask which angle to use for advertorials unless the user gave no direction:**
If David says "proceed with Phase 11" without specifying an angle, execute ALL angles at professional grade. The user expects exhaustive coverage, not a single cherry-picked angle. Batch all 5.

### Phase 12 — Advertorial (Auth) — Authority Revelation

**Prompt file:** Same as Phase 11 — `creatives/11_-_creating_nightmare_personal_story_advertorial.md` (Lines 146-299 — the Authority Revelation framework)

**Target length:** 1,200-1,500 words

**Framework:** Authority Revelation (whistleblower/expert exposes hidden truth)
- **Opening Hook Sequence** — Stark contrast format ("[Target] should have [succeeded]. They [failed] instead."), 3-4 escalating "If you..." statements, reveal widespread problem with specific percentage, contrast obvious vs. hidden
- **Authority Establishment** — Expert credentials (15+ years, specific degrees, published work, case count), breaking point where conventional wisdom failed
- **UMP Discovery** — The REAL hidden root cause nobody knows about, counterintuitive but immediately makes sense, includes scientific/biological/behavioral explanation, shows why all traditional approaches fail
- **Systematic Debunking** — Test each common solution, show how each fails because it doesn't address the UMP, consistent structure per solution
- **UMS Reveal (Professional Secret)** — How the solution specifically addresses the UMP, why this works when others don't, single company making it available
- **Proof Sequence** — Immediate changes (hours/days), formal trial with specific numbers, "X out of Y showed improvement" format, expert's personal experience
- **3 Testimonial Quotes** — Specific results from fictional customers
- **Urgency & Close** — Professional community discovering solution, supply/demand imbalance, risk reversal guarantee (90-day typical), clear CTA with discount percentage

**Key psychological elements:**
1. Authority as Whistleblower — Expert breaking ranks to help
2. Validation Pattern — "Your instincts were right all along"
3. David vs Goliath — Individual truth vs industry deception
4. Hidden Knowledge — Professional secrets made public
5. Preventable Tragedy — Suffering that didn't need to happen
6. Mechanism Discovery — "This changes everything we thought we knew"

**Authority figure requirements:**
- Must have BOTH specific credentials (degrees, years of experience, published work, number of cases/patients/clients treated) AND personal stake in exposing the truth
- Background must be directly connected to the problem domain (sleep researcher for sleep angle, relationship therapist for setup-argument angle, product designer for envy angle)
- Narration: first-person expert ("I discovered..."), NOT third-person about the expert

**Delegation pattern:** Same as Phase 11 — batch 3 per call, 2 calls covers 5 angles.

**Format rules:**
- Subheadlines as standalone story beats with specific numbers (not questions)
- Mixed paragraph lengths (1-4 sentences) for rhythm
- **Bold** key revelations, statistics, CTAs
- 3 testimonials in a block near the close
- Disclaimer at bottom
- 90-day guarantee, $X discount, free shipping or similar incentives

### Phase 13 — Awareness Test Copy

**Purpose:** Expand from one dominant awareness level to all levels. When a winning angle + desire is validated (Phase 10), rewrite ad copy for each awareness level targeting its unique psychological state.

**Output:** 5 short ad copies (~150-300 words each), one per awareness level.

**File naming convention:**
```
13-awareness-test-copy/
  01-unaware-ad.md
  02-problem-aware-ad.md
  03-solution-aware-ad.md
  04-product-aware-ad.md
  05-most-aware-ad.md
```

**Execution:**
- Use the **best-performing angle + desire** from Phases 8-10 (e.g., Angle 1 — The Weekend That Almost Didn't Happen + Time Reclamation)
- Each copy is a short Facebook/Instagram ad format, NOT a full advertorial
- Each copy must target the specific awareness level's psychology and language (see awareness distribution from Phase 1)
- Batch: 3 copies per delegate_task call, then 2. Each subagent needs:
  - Awareness-level psychology (who they are, what they say, what they need to hear)
  - The winning angle structure (story arc, UMP, UMS)
  - The product details
  - Format: 150-300 words, first-person or direct address, conversational, 5th grade reading level, catchy 6-12 word headline, single CTA
  - Output path

**Awareness psychology cheat sheet (from Lattice Glamping Phase 1 research):**

| Level | % | Psychology | Copy Goal |
|-------|---|------------|-----------|
| Unaware | 35% | Don't know the problem exists. Accept camping friction as normal. | Problem introduction — don't sell Lattice, sell the idea that there's a better way |
| Problem Aware | 30% | Know camping is broken. Say "I'd camp more if it weren't such a hassle." | Problem agitation + solution tease — validate and deepen the known pain |
| Solution Aware | 22% | Know solutions exist (tents, pop-ups, rooftop tents). Researching best option. | Differentiation — show why Lattice is different from everything they've researched |
| Product Aware | 10% | Know Lattice exists. On the fence about $3,800 and no reviews. | Price justification + social proof — reframe cost vs. cost of NOT buying |
| Most Aware | 3% | On waitlist or have it in cart. Need launch details. | Close the sale — shipping info, urgency, clear CTA |

**PITFALL — Don't re-introduce the product for Unaware copy.** Unaware doesn't know Lattice exists. The copy must first expose the problem. The product is the reveal, not the opener.

### Phase 14 — Testing Rules Doc

### Phase 8-14 (Creative Engine — DtS)
- Use delegate_task with [Copywriter] or [Researcher] prefix
- Ground every output in the Master Research Doc (Phase 4)
- Cross-reference Phase 3 verbatim quotes for authentic customer language
- Follow DtS system prompts exactly as written
- See `references/advertorial-pattern.md` for the session-specific delegation pattern that produced all 10 advertorials

### Deep Quality Strategies
- **Multi-query depth:** 5-8 separate web searches targeting different angles per phase
- **Parallel extraction:** Multiple subagents for competitive analysis, voice mining
- **Two-pass pattern:** Pass 1 broad sweep → Pass 2 deep follow-up on promising threads
- **Verbatim quote mining:** Extract actual quotes with platform names and dates. Minimum 20 quotes per Avatar Research phase.
- **Checklist enforcement:** Verify every phase output against prompt's deliverable checklist before presenting
- **Research grounding:** Every creative output must trace back to Phases 1-6 research data (not just general knowledge)

### Agent Routing Reference
Copywriter agent routes through agent_profiles.yaml allowed_models. For reliable routing:
- deepseek-v4-pro works via [Copywriter] or [Researcher] prefix
- claude-sonnet-4.6 requires provider: minimax in model_catalog.yaml (routes via MiniMax's Anthropic proxy)
- If Copywriter tasks time out, fall back to [Researcher] prefix immediately
- Verify actual model: check results[i].model in subagent return metadata

## Pipeline Completion — Full Export

At the end of Phase 13 (or Phase 14 if reached), David will likely ask for a full export of everything. Do NOT wait to be asked — offer it proactively.

**ZIP everything from the output directory:**
```bash
cd /root/.hermes/research
zip -r [product-slug]-full-pipeline.zip output/[product-slug]/
```

**Include prompts as a bonus:**
```bash
mkdir -p [product]-export/00-prompts
cp -r prompts/* [product]-export/00-prompts/
cp -r output/[product]/* [product]-export/
zip -r [product]-full-pipeline.zip [product]-export/
```

**Structure to aim for:**
```
product-full-pipeline.zip
├── 00-prompts/              (all original prompt templates — research, creatives, DtS)
├── 01-awareness-research.md
├── 02-competitor-research.md
├── ... (Phases 1-14 complete)
├── 11-advertorials/         (5 PAS)
├── 12-authority-advertorials/ (5 Authority)
└── 13-awareness-test-copy/  (5 ads)
```

**Send via Discord:** Use `send_message` with `MEDIA:/path/to/file.zip` in the message body. Target the thread where the conversation lives (not the home channel). If unsure, check the source of the user's messages to determine the correct thread ID.

## Non-Pipeline Deliverables

The standard pipeline produces ad copy, advertorials, and testing docs. But some tasks call for different output types — particularly when the client has restricted ad channels and needs an **owned-channel strategy** (email, SMS, community).

**When to produce a strategy document instead of ad copy:**
- User explicitly says "focus on email" or "focus on retention"
- Niche is restricted on Meta/Facebook/Instagram (vape alternatives, CBD, wellness with health claims)
- User asks for "strategy" not "copy"
- The core request is about LTV and retention, not acquisition

**Strategy document structure (email marketing focus):**
1. **Market & Competitive Landscape** — Primary research on brand + 2-3 key competitors
2. **Email Strategy Overview** — Core objective, metrics, platform recommendation
3. **Lead Capture Fixes** — Audit current capture points, add popups/quiz/lead magnets
4. **Welcome Sequence** — 5-7 email onboarding sequence (education → trust → offer → objection → urgency)
5. **Post-Purchase Flows** — Order confirmation, shipping, first-use guide, review request, reorder reminder, subscription offer, winback
6. **Subscription Model** — Name, pricing, benefits, implementation steps (critical for LTV)
7. **Content Newsletters** — Weekly cadence, content pillars, editorial calendar
8. **Referral & Loyalty** — Program structure, VIP tiers, points system
9. **Abandoned Cart** — Recovery sequence with discount escalation
10. **Technical Setup** — Platform choice, deliverability, GDPR compliance, segmentation plan

**Output format:** Save as `~/.hermes/research/output/[product]/email-marketing-strategy.md` and summarize the key findings in the user thread. The full doc is for reference — the user needs a condensed actionable summary first.

### QA Gate — Language Precision Note
When reviewing competitor or product specs flagged by QA, note the difference between "tested to X" (verified performance threshold) and "X rated" (marketing language). Prefer "tested to" in external-facing copy when the source research uses that framing. This avoids puffery claims.

### QA Gate — Internal Consistency Check (CRITICAL for new clients)

When running the QA gate on research deliverables (especially Phases 1-3 for a new client), check for **internal consistency across documents** as a first-class criterion:

1. **Self-spec alignment** — Do ALL documents use the same weight, price, dimensions, and setup time for your own product? A subagent may write "~250-400 lbs (est.)" while another has the correct "99-110 lbs." **Always grep for your product's specs in every output.**
2. **Pricing consistency** — Is the early-bird price in USD consistent across docs? Does one doc quote $3,000 SEB while another says $3,990?
3. **Competitor data alignment** — Do competitor prices/weights match across competitor profiles and the competitive matrix?
4. **Persona naming** — Do the avatar names and demographic details match between the Avatar Research doc (Phase 3) and the marketing angles (Phase 9)?

**Failure mode:** If Doc 02 uses estimated/placeholder specs for your own product while Docs 01 and 03 use real specs, the entire competitive landscape analysis is built on the wrong baseline. This must be caught before presenting to the user.

**Fix pattern:** When a document has wrong self-specs, use targeted `patch` commands to replace the specific values rather than rewriting the whole document. See the Lattice Glamping 2026-05-19 session for a successful 14-patch fix pattern.

### CopyWriter Timeout Recovery (2026-05-19)
When CopyWriter (claude-sonnet-4-6) times out processing 4 large strategy docs simultaneously:
1. **Check what wrote to disk** — `ls -la` and compare file sizes/timestamps to confirm partial writes
2. **Resume with smaller batches** — 2 docs per claude-sonnet-4-6 delegation (~400s) then 1 doc per remaining
3. **The original MarketingStrategist output is still valid** — CopyWriter polishes language but doesn't change strategy. If timeout leaves some docs unpolished, the underlying strategy is still correct
4. **Always verify with `wc -w`** after any subagent that processes multiple files — confirm all expected files exist

### Phase 8 — Proven Batching Pattern (New Client)

For a first-time Phase 8 execution (5 desires × 5 awareness levels = 25 copies, each 1,200-1,400 words), the following batching pattern reliably delivers all copies at full length without any expansion needed:

**Batch by desire group, not by awareness level.**
- Batch 1: Comfort × Unaware, Problem-Aware, Solution-Aware + Setup Pain × Problem-Aware, Solution-Aware = 5 copies
- Batch 2: Relationships × Unaware, Problem-Aware, Solution-Aware + Escape × Problem-Aware, Solution-Aware = 5 copies
- Batch 3: Freedom × Problem-Aware + Comfort × Product-Aware, Most-Aware + Setup Pain × Product-Aware + Escape × Most-Aware = 5 copies
- Batch 4: Setup Pain × Unaware, Most-Aware + Relationships × Product-Aware, Most-Aware + Escape × Unaware = 5 copies
- Batch 5: Freedom × Unaware, Solution-Aware, Product-Aware, Most-Aware + Escape × Product-Aware = 5 copies

**Key insight:** Each batch gets 5 copies at 1,200+ words. Claude Opus 4.7 handles this in 260-320 seconds per batch. No copies needed expansion. The trick is giving each copy its own hook, angle, awareness-level psychology, and output path — all in one context envelope.

**After all batches complete:**
1. Verify with `wc -w` on all 25 files
2. Clean old stub files from previous pipeline runs (they'll be in the same directory with different naming schemes)
3. Push to GitHub

## Common Failure Modes to Avoid
- Generating hooks for only 1 awareness level — must cover all 5
- Producing creative copy without grounding in Phase 3 verbatim quotes
- Presenting output without verifying against the deliverable checklist
- **Subagents hallucinating your own product's specs** — When delegating research tasks (Phases 1-3), subagents will NOT reliably read and use the product specs you provide in context. They frequently fabricate placeholder specs (wrong weight, wrong price, wrong dimensions). This creates internal consistency failures between documents. **Prevention: After every research subagent completes, verify your own product's specs in the output match what you provided.** Include a "self-spec cross-check" step in your pre-presentation QA. Use a known-good snippet file (e.g., `references/product-spec-card.md`) that subagents can reference rather than trying to remember from context.
- **Starting pipeline without a product spec card** — Never begin Phase 1 without first writing a canonical product spec card to a known path. This prevents the "each subagent invents different specs" failure. See `references/product-spec-card.md` for the standard format.
