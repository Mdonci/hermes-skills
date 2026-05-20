---
name: writing-quality
description: "Comprehensive writing quality system — audit and rewrite content to remove AI writing patterns ('AI-isms'). Merges avoid-ai-writing (v3.3.1 by Conor Bronsdon) + humanizer (v2.5.1 by Siqi Chen/blader). 109-entry 3-tier word table, 36+ pattern categories, context profiles, severity tiers, detect mode, voice calibration, second-pass audit, and personality/soul guidance."
version: 1.0.0
license: MIT
authors: [Conor Bronsdon, Siqi Chen (blader)]
metadata:
  hermes:
    tags: [writing, editing, voice, quality, ai-isms, humanize, style]
    category: creative
    homepage: https://github.com/conorbronsdon/avoid-ai-writing
    source_humanizer: https://github.com/blader/humanizer
    source_avoid_ai_writing: https://github.com/conorbronsdon/avoid-ai-writing
related_skills:
  - brand-voice-system
  - email-strategy-production-system
---

# Writing Quality — Audit & Rewrite

You are editing content to remove AI writing patterns ("AI-isms") that make text sound machine-generated. This skill merges two industry-validated systems: **avoid-ai-writing** (109-entry 3-tier word replacement, 36 patterns, context profiles) and **humanizer** (voice calibration, personality/soul, 29 patterns from Wikipedia's Signs of AI Writing).

## Two Core Principles

1. **Remove AI tells** — structured audit with 3-tier vocabulary, 36+ pattern categories, context profiles
2. **Add human voice** — don't just strip AI-isms, inject personality, rhythm, and actual opinions

## Modes

**`rewrite`** (default) — Flag AI-isms and rewrite the text to fix them.

**`detect`** — Flag AI-isms only. No rewriting. Use when:
- The writer wants to decide what to fix themselves
- The flagged patterns might be intentional
- You're auditing text you don't want altered
- You want a quick scan

Trigger detect mode when the user says "detect," "flag only," "audit only," "just flag," "scan," or similar. Default to rewrite mode.

---

## Process (6 Steps)

When given text to humanize:
1. **Audit** — scan for all patterns below, cite specific text
2. **Draft rewrite** — rewrite with all AI-isms removed
3. **AI audit** — ask yourself: "What about this draft still sounds AI-generated?" Answer briefly with remaining tells
4. **Final rewrite** — revise one more time
5. **Show diff summary** — list what changed and why
6. **Second-pass audit** — re-read the final version, catch any surviving tells

---

## What to Remove or Fix

### Formatting
- **Em dashes (— and --)**: Replace with commas, periods, parentheses, or two sentences. Target: zero. Hard max: 1 per 1,000 words.
- **Bold overuse**: One bolded phrase per major section at most. Restructure to lead with the important bit instead.
- **Emoji in headers**: Remove entirely. Exception: social posts may use 1-2 emoji sparingly at line end.
- **Excessive bullet lists**: Convert to prose. Bullets only for genuine list content (comparisons, steps, params).
- **Curly quotation marks** ("..."): Replace with straight quotes ("...").
- **Title case in headings: HARD BAN**: Only sentence case allowed. "Key Benefits And Features" → "Key benefits and features". Title case is one of the strongest single AI tells in section headers. The verify script flags ANY heading with more than one capitalized word.
- **Horizontal dividers (--- or ***): HARD BAN**: Zero in body text. AI uses them as structural scaffolding. Human-written content uses section breaks or transitions instead of mechanical dividers. The verify script flags them as critical.

### Sentence Structure
- **"It's not X — it's Y"**: Rewrite as direct positive statement. Max one per piece. Also flag the period-separated variant: "The Lattice suite is not a tent. It is a portable room." → "The Lattice suite is a portable room." The pattern is the same whether joined by em dash or split by period.
- **Hollow intensifiers**: Cut `genuine`, `real` (as "a real improvement"), `truly`, `quite frankly`, `to be honest`, `let's be clear`.
- **Vague endorsement**: Cut `worth reading`, `worth a look`, `worth checking out`, `worth your time`. Say *why*.
- **Hedging**: Cut `perhaps`, `could potentially`, `it's important to note that`.
- **Missing bridge sentences**: Each paragraph should connect to the last.
### Compulsive hármas felsorolás (Rule of Three) — HARD ENFORCEMENT

AI overuses comma-separated triples: "their face, their emotion, their environment." "a focused expression, a frustrated pout, or a little hand reaching." This is the Hungarian term for it because it's the single most common AI tell in copy — three parallel items listed in a row.

**Rules:**
- **Max 1 per piece.** If the text has 2+ triads, it's blocked.
- **Variants to catch:** X, Y, and Z / X, Y, or Z / X, Y, Z (no conjunction) / for X, for Y, and for Z (repeated preposition)
- **Do NOT catch:** actual lists of 3 discrete things where each item could stand alone (product names, feature lists in tables, step-by-step instructions where each step is substantial)

**Fix:** Use two items instead of three. Or four. Or one full sentence. Vary the groupings. If you catch yourself listing a third item, ask: "Does this need three? Or is two tighter?"
- **Passive voice & subjectless fragments**: "No configuration file needed" → "You do not need a config file." "The results are preserved automatically" → "The system preserves the results."
- **Fragmented headers**: If a heading is followed by a one-line paragraph that just restates it, cut the restatement.

### Hyphenated Word Pair Overuse
Common pairs that AI hyphenates with perfect consistency (humans rarely do):

`third-party`, `cross-functional`, `client-facing`, `data-driven`, `decision-making`, `well-known`, `high-quality`, `real-time`, `long-term`, `end-to-end`

Fix: Remove the hyphen. "Cross functional team," "data driven decisions," "high quality output." Only keep hyphens for genuine compound modifiers where meaning changes (e.g., "re-cover" vs "recover").

### Persuasive Authority Tropes
Phrases that pretend to cut through noise to a deeper truth, but usually just restate an ordinary point:

`The real question is`, `at its core`, `in reality`, `what really matters`, `fundamentally`, `the deeper issue`, `the heart of the matter`

Fix: If the sentence after the phrase is a routine point, cut the phrase. If it genuinely reveals something non-obvious, lead with the revelation.

### Signposting and Announcements
AI announces what it's about to do instead of doing it:

`Here's what you need to know`, `now let's look at`, `without further ado`

Also flag these common variants (caught in production):
- **Email preview/recap** — "I will tell you the full story in my next email", "This is the email where I answer the question", "The next email covers the pricing", "Next email I am going to walk through", "Over the next two emails I will cover"
- **"Here is what" constructions** — "Here is what you can expect", "Here is what that actually means", "Here is what you get:", "Here is the breakdown"
- **"Let me" constructions (non-question)** — "Let me explain how", "Let me walk you through" (these are AI reasoning chain artifacts)

The rule: if a sentence can be deleted without losing information, it is signposting. Delete it. Just present the information.

(Note: "Let's dive in," "let's explore" are covered under Let's constructions below.)

### Words and Phrases to Replace

**TIER 1 — Always flag** (appear 5-20x more in AI text). Replace on sight.

| Replace | With |
|---|---|
| delve / delve into | explore, dig into, look at |
| landscape (metaphor) | field, space, industry, world |
| tapestry | (describe the actual complexity) |
| realm | area, field, domain |
| paradigm | model, approach, framework |
| embark | start, begin |
| beacon | (rewrite entirely) |
| testament to | shows, proves, demonstrates |
| robust | strong, reliable, solid |
| comprehensive | thorough, complete, full |
| cutting-edge | latest, newest, advanced |
| leverage (verb) | use |
| pivotal | important, key, critical |
| underscores | highlights, shows |
| meticulous / meticulously | careful, detailed, precise |
| seamless / seamlessly | smooth, easy, without friction |
| game-changer / game-changing | describe what specifically changed |
| hit differently / hits different | (say what changed, or cut) |
| utilize | use |
| watershed moment | turning point, shift |
| marking a pivotal moment | (state what happened) |
| the future looks bright | (cut — say something specific) |
| only time will tell | (cut) |
| nestled | is located, sits, is in |
| vibrant | (describe what makes it active, or cut) |
| thriving | growing, active (or cite a number) |
| despite challenges… continues to thrive | (name challenge + response) |
| showcasing | showing, demonstrating (or cut) |
| deep dive / dive into | look at, examine, explore |
| unpack / unpacking | explain, break down, walk through |
| bustling | busy, active (or cite why) |
| intricate / intricacies | complex, detailed |
| complexities | (name the actual complexities) |
| ever-evolving | changing, growing |
| enduring | lasting, long-running |
| daunting | hard, difficult, challenging |
| holistic / holistically | complete, full, whole |
| actionable | practical, useful, concrete |
| impactful | effective, significant |
| learnings | lessons, findings, takeaways |
| thought leader / thought leadership | expert, authority |
| best practices | what works, proven methods |
| at its core | (cut — just state it) |
| synergy / synergies | (describe the actual combined effect) |
| interplay | relationship, connection, interaction |
| in order to | to |
| due to the fact that | because |
| serves as | is |
| features (verb) | has, includes |
| boasts | has |
| presents (inflated) | is, shows, gives |
| commence | start, begin |
| ascertain | find out, determine, learn |
| endeavor | effort, attempt, try |
| keen (as intensifier) | interested, eager (or cut) |
| symphony (metaphor) | (describe actual coordination) |
| embrace (metaphor) | adopt, accept, use, switch to |

**TIER 2 — Flag when 2+ appear in the same paragraph.** Individually fine, cluster is AI signal.

| Replace | With |
|---|---|
| harness | use, take advantage of |
| navigate | work through, handle, deal with |
| foster | encourage, support, build |
| elevate | improve, raise, strengthen |
| unleash | release, enable, unlock |
| streamline | simplify, speed up |
| empower | enable, let, allow |
| bolster | support, strengthen |
| spearhead | lead, drive, run |
| resonate with | connect with, appeal to |
| revolutionize | change, transform |
| facilitate | enable, help, allow, run |
| underpin | support, form basis of |
| nuanced | specific, subtle, detailed |
| crucial | important, key, necessary |
| multifaceted | (describe the actual facets) |
| ecosystem (metaphor) | system, community, network, market |
| myriad | many, numerous |
| plethora | many, a lot of |
| encompass | include, cover, span |
| catalyze | start, trigger, accelerate |
| reimagine | rethink, redesign, rebuild |
| galvanize | motivate, rally, push |
| augment | add to, expand, supplement |
| cultivate | build, develop, grow |
| illuminate | clarify, explain, show |
| elucidate | explain, clarify, spell out |
| juxtapose | compare, contrast |
| paradigm-shifting | (describe what shifted) |
| transformative | (describe what changed) |
| cornerstone | foundation, basis, key part |
| paramount | most important, top priority |
| poised (to) | ready, set, about to |
| burgeoning | growing, emerging |
| nascent | new, early-stage, emerging |
| quintessential | typical, classic, defining |
| overarching | main, central, broad |

**TIER 3 — Flag only at high density (~3%+ of total words).** Normal words AI overuses.

| Word | What to do |
|---|---|
| significant / significantly | Replace some with specifics |
| innovative / innovation | Describe what's actually new |
| effective / effectively | Say how or cite a metric |
| dynamic / dynamics | Name the actual forces |
| scalable / scalability | Describe what scales |
| compelling | Say why it compels |
| unprecedented | Name the precedent it breaks |
| exceptional / exceptionally | Cite what makes it an exception |
| remarkable / remarkably | Say what's worth remarking on |
| sophisticated | Describe the sophistication |
| instrumental | Say what role it played |
| world-class / best-in-class | Cite a benchmark |

### Template Phrases (Avoid)
- "a [adjective] step towards [adjective] AI infrastructure" → be specific
- "Whether you're [X] or [Y]" → false-breadth. Pick your actual audience.
- "I recently had the pleasure of [verb]-ing" → just say what happened.
- "It is important to note that" → (just state it)
- "In terms of" → (rewrite)
- "The reality is that" → (cut or state the claim)

### Transition Phrases
- "Moreover" / "Furthermore" / "Additionally" → restructure or use "and"/"also"
- "In today's [X]" / "In an era where" → cut or state specific context
- "It's worth noting that" / "Notably" → just state the fact
- "Here's what's interesting" / "Here's what caught my eye" → let content signal its own importance
- "In conclusion" / "In summary" → your conclusion should be obvious
- "When it comes to" → talk about the thing directly
- "That said" / "That being said" → cut or use "but"/"yet"
- "At the end of the day" → cut

### Structural Issues
- **Uniform paragraph length**: Vary deliberately. Some 1-2 sentence paragraphs, some longer.
- **Formulaic openings**: Lead with the news, not "In the rapidly evolving world of..."
- **Suspiciously clean grammar**: Keep natural disfluency, fragments starting with "And"/"But", comma splices for effect.

### Significance Inflation
- "marking a pivotal moment in the evolution of..." → state what happened. If the sentence still works after deleting the inflation, delete it.

### Copula Avoidance
- Default to "is"/"has" instead of "serves as," "features," "boasts," "presents."

### Synonym Cycling
- AI rotates synonyms to avoid repeating: "developers… engineers… practitioners… builders." Human writers repeat the clearest word.

### Vague Attributions
- "Experts believe," "Studies show" without sources → cite the specific source or drop the attribution.

### Generic Conclusions
- "The future looks bright," "Only time will tell," "One thing is certain" → cut. If needed, make it specific.

### Chatbot Artifacts
- "I hope this helps!", "Certainly!", "Great question!", "Feel free to reach out" → remove entirely.

### "Let's" Constructions
- "Let's explore," "Let's break this down," "Let's examine" → just start with the point.

### Notability Name-Dropping
- "cited in NYT, BBC, Financial Times" → one specific reference with context beats four name-drops.

### Superficial -ing Analyses
- Strings: "symbolizing… reflecting… showcasing…" → replace with specific facts or cut.

### Promotional Language
- "nestled within the breathtaking foothills" → plain description: "is in the Gonder region."

### Formulaic Challenges
- "Despite challenges, continues to thrive" → name the actual challenge and response.

### False Ranges
- "from the Big Bang to dark matter" → list the actual topics or pick one.

### Inline-Header Lists
- "**Performance:** Performance improved by..." → strip bold header, write the point directly.

### Title Case Headings
- "Strategic Negotiations And Key Partnerships" → "Strategic negotiations and key partnerships." Sentence case for subheadings.

## Wikipedia Signs of AI Writing — Additional Patterns

These patterns come from Wikipedia's "Signs of AI Writing" (https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). They overlap with the rules above but add specific detection language for newer GPT-era patterns.

### Negative Parallelisms (GPT-4/4o/5)

LLMs reframe a subject by telling you what it ISN'T before telling you what it IS. This creates a "clearing up a misconception" structure that AI overuses dramatically.

**"Not just X, but also Y":**
- "Self-Portrait ... constitutes not only a work of self-representation, but a visual document of her obsessions"
- "This isn't just sourcing — it's framing"

**"Not X, but Y":**
- "It's not a mirror but a portal"
- "The Lattice suite is not a tent. It is a portable room with..." (period-separated variant)
- "This isn't about X, it's about Y"
- "Not a career, not a body of work, not sustained relevance — just an algorithmic moment"

**Fix:** If the positive statement stands on its own, delete the negative framing and lead with the positive. Max one per piece, and only if it genuinely resolves a common misconception rather than creating a rhetorical contrast.

### Overattribution / Notability Name-Dropping (GPT-4o/5)

LLMs prove notability by stating that the subject has been covered, rather than showing what the coverage said:

- "has been featured in/cited in/profiled in [list of media outlets]"
- "independent coverage across multiple [type] outlets"
- "maintains an active social media presence" (particularly idiopathic to AI)
- "a strong digital presence"

**Fix:** If a source matters, use it with context: "In a 2024 NYT interview, she argued..." One specific reference with substance beats four name-drops. Cut "maintains an active social media presence" entirely.

### Superficial -ing Analyses (GPT-4)

Strings of present participles pretending to be analysis:
- ", highlighting the importance of..." (or "its importance")
- ", underscoring the significance..."
- ", emphasizing the need for..."
- ", reflecting the broader trend..."
- ", symbolizing the commitment to..."
- ", showcasing the potential of..."

**Fix:** These clauses can almost always be deleted without losing information. Replace with a specific fact or cut entirely. If the sentence would read the same without the -ing clause, it's padding.

### Formulaic Challenges Conclusion (GPT-4/4o)

At the end of a section or article, AI writes:
- "Despite [positive trait], [subject] faces several challenges..."
- "Despite these challenges, [subject] continues to thrive..."
- "The future of [subject] lies in its ability to adapt..."

This is a zero-statement pattern. Name the actual challenge and the actual response, or delete the sentence entirely.

### Canned Emphasis on Significance / Legacy (GPT-4)

LLMs inflate routine events into history-making ones:
- "marking a pivotal moment in the evolution of..."
- "represents a significant shift toward..."
- "setting the stage for future..."
- "a key turning point in..."
- "left an indelible mark on..."
- "deeply rooted in the history of..."
- "this [etymology/population data] highlights the enduring legacy of..."

**Fix:** If the sentence still works after deleting the inflation clause, delete it. State what happened and let the reader judge significance.

### Copula Avoidance (GPT-4/4o)

LLMs replace "is" with inflated verbs:
- "serves as" → just "is"
- "boasts/features/offers" → just "has"
- "marks/represents" → just "is"
- "refers to" in lead sentences → just "is"

Studies show a 10%+ decrease in "is" and "are" usage in academic writing after 2023 when LLMs became widespread.

**Fix:** Default to "is" or "has" unless a more specific verb genuinely adds meaning.

### Inline-Header Vertical Lists (GPT-4)

AI produces lists formatted as: `**Header:** Description text`

This is a strong structural tell because LLMs default to this format for any expository list. Humans use prose or table formats.

**Fix:** If each item's bold header can be merged into the descriptive text, do so. If the list genuinely needs headers, use paragraphs instead.

### Title Case in Section Headings (GPT-4/4o)

AI capitalizes every word in section headings: "Strategic Negotiations And Key Partnerships" instead of "Strategic negotiations and key partnerships."

**Fix:** Sentence case for subheadings. Title case only for the piece's main title, if at all.

### Generic Challenges and Future Prospects Sections

AI articles include a rigid "Challenges" section beginning with "Despite its [positive], [subject] faces challenges..." and ending with a vaguely positive assessment or speculation.

Note: This is about the rigid formula, not the mere mention of challenges.

### False Ranges

AI creates false breadth by pairing unrelated extremes: "from the Big Bang to dark matter," "from ancient civilizations to modern startups."

**Fix:** List the actual topics or pick the one that matters.

### "As of [Month Year]" / "While specific details are limited"

These are model limitations leaking into published prose. NEVER publish a sentence that admits the writer didn't look something up.

### Novelty Inflation
- "He introduced a term I hadn't heard before" → describe what they *did with* the concept. If unsure whether it's novel, assume it isn't.

### Emotional Flatline
- "What surprised me most," "I was fascinated to discover" → the writing should earn the emotion. If a thing is genuinely surprising, the reader should feel it.

### False Concession Structure
- "While X is impressive, Y is a challenge" → either make both halves specific or pick a side.

### Rhetorical Question Openers
- "So why should you care?" / "What's next?" → if you know the answer, just say it.

### Parenthetical Hedging
- "(and, increasingly, Z)" / "(or, more precisely, Y)" → give it its own sentence or cut.

### Numbered List Inflation
- "Three key takeaways" / "Five things to know" → only use when content genuinely has that many items.

### Reasoning Chain Artifacts
- "Let me think step by step," "Breaking this down," "Here's my thought process" → state the conclusion, then evidence.

### Sycophantic Tone
- "Great question!", "Excellent point!", "You're absolutely right!" → conversational rewards, not writing. Remove.

### Acknowledgment Loops
- "You're asking about," "To answer your question" → AI restates the prompt. Just answer.

### Confidence Calibration Phrases
- "Interestingly," "Surprisingly," "Notably," "Certainly," "Undoubtedly" → one per 2,000 words is fine. More is AI stacking.

### Excessive Structure
- More than 3 headings in under 300 words = AI looking organized. Merge sections.
- 8+ bullets in under 200 words = should be a paragraph.

---

## Rhythm and Uniformity

**Structure is the #1 detection signal.** Pangram's classifier, trained on 28M human documents, weights structural regularity higher than vocabulary. Fixing every Tier 1 word but leaving rhythm untouched still reads as AI.

- **Sentence length uniformity**: Most sentences 15-25 words = robotic. Mix short (3-8 words) with long (20+). Fragments and questions break monotony.
- **Excessive staccato rhythm**: The opposite problem is equally bad — every sentence being 3-8 words with no connective tissue. "It is 4am. You are awake. The ground is hard. Your back hurts. You have to pee." reads like a ticker tape, not human writing. Human writing uses compound sentences, subordinate clauses, and connecting phrases. A 30-word sentence followed by a 6-word sentence is more natural than ten 6-word sentences in a row.

- **Staccato fragment lists (HIGH SEVERITY — David rejection pattern):** AI-written product copy frequently falls into a pattern of listing attributes as independent fragments: "Three minutes. One person. Zero tools." or "Laser-welded aluminum frame. Full 2.1m stand-up interior. Blackout bedroom." This is the same staccato problem but specific to product/feature descriptions where the writer reached for a "scanable" format instead of connected prose.
  
  **David's explicit rejection:** "Three minutes. One person. Then your car drives away." and "Laser-welded aluminum frame. Full 2.1m stand-up interior. Blackout bedroom. Folds to the size of a golf bag. No poles. No pump. No partner required. No storage lot." — he called these unreadable and demanded they be replaced with connected sentences.
  
  **How to fix:** Connect the fragments with compound structures, subordinate clauses, and linking words (because, so, and, which, that):
  - ❌ "Three minutes. One person. Then your car drives away."
  - ✅ "It takes about three minutes and one person can do it from start to finish, then your car can drive away because the suite stands by itself."
  
  **⚠️ Pitfall: don't fix staccato by adding em dashes.** When you connect short fragments, your first instinct may be to use em dashes as dramatic connective tissue (e.g. replacing "Short sentence. Another short sentence." with "Short sentence — another short sentence."). The humanize-verify script bans em dashes entirely — zero tolerated. Fix staccato with commas + conjunctions (`and`, `but`, `because`, `so`, `which`), colons for list-like connections, or parentheses for asides. The em-dash shortcut will get your file failed at the verification gate and require a costly second pass where you have to replace every em dash with context-appropriate alternatives. See `references/subagent-audit-verification.md` for the full em-dash-as-crutch case study.

**Real example from Lattice Glamping landing page copy (May 2026):** The Copywriter subagent wrote staccato fragments ("Three minutes. One person. Zero tools." / "Laser-welded aluminum frame. Full 2.1m stand-up interior. Blackout bedroom."). When instructed to fix them, the writer added em dashes as connective tissue ("A rigid glamping suite on your hitch. Deploys alone in three minutes. Your car free to leave."). David rejected this as "an instant fail" and demanded connected sentences. The fix that passed: "A rigid glamping suite mounted to your hitch that deploys in three minutes, lets your car drive away, and fits in the hallway closet when you get home."
  - ❌ "Laser-welded aluminum frame. Full 2.1m stand-up interior. Blackout bedroom. No poles. No pump. No partner required."
  - ✅ "The result is a laser-welded aluminum frame on a hitch receiver that gives you 2.1 meters of standing room, a real bed off the ground instead of on it, blackout panels so you can actually sleep past sunrise, and a fold-down footprint roughly the size of a golf bag for when it is parked between trips."
  
  **The rule:** If you can replace 3+ consecutive period-separated short phrases with a single compound sentence using "and", "which", "that", "because", or "so", do it. The only exception is deliberately punchy copy for short-form social posts (LinkedIn, TikTok captions) where the audience expects staccato scanning.
- **Paragraph length uniformity**: Vary deliberately. Some one-sentence. Some longer.
- **Vocabulary repetition vs. synonym cycling**: Repeat when the word is right. Force variation = thesaurus abuse.
- **Read-aloud test**: If it sounds like TTS, it's too uniform.
- **Missing first-person perspective**: AI is relentlessly neutral. If appropriate, use "I think," "in my experience."
- **Over-polishing**: Sanding away every irregularity pushes text *toward* AI profiles. Keep natural disfluency.

### When to Rewrite vs. Patch
If 5+ vocabulary flags across multiple categories, 3+ pattern categories triggered, AND uniform sentence/paragraph length → advise full rewrite. State the core point in one sentence, rebuild from there.

---

## Personality & Soul

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop.

### Signs of Soulless Writing
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

### How to Add Voice
- **Have opinions.** Don't just report facts — react to them. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.
- **Vary your rhythm.** Short punchy sentences. Then longer ones. Mix it up.
- **Acknowledge complexity.** "This is impressive but also kind of unsettling" beats "This is impressive."
- **Use "I" when it fits.** First person signals a real person thinking.
- **Let some mess in.** Tangents, asides, and half-formed thoughts are human.
- **Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

---

## Voice Calibration (Optional)

If a writing sample is provided for voice matching:

1. **Read the sample.** Note:
   - Sentence length patterns (short and punchy? Long and flowing? Mixed?)
   - Word choice level (casual? academic? somewhere between?)
   - How they start paragraphs (jump right in? Set context first?)
   - Punctuation habits (dashes? parenthetical asides? semicolons?)
   - Recurring phrases or verbal tics
   - How they handle transitions

2. **Match their voice.** Don't just remove AI patterns — replace them with patterns from the sample. If they write short sentences, don't produce long ones. If they use "stuff" and "things," don't upgrade to "elements" and "components."

3. **No sample provided** → fall back to default (natural, varied, opinionated voice).

---

## Severity Tiers

| Tier | What | Examples |
|------|------|----------|
| **P0** — Credibility killers (fix now) | Cutoff disclaimers, chatbot artifacts, vague attributions, significance inflation | "As of my last update," "I hope this helps!", "Experts believe" |
| **P1** — Obvious AI smell (fix before publish) | Word-list violations, template phrases, "let's" openers, synonym cycling, formulaic openings, bold overuse, em dashes, **hármas felsorolás (rule of three)** | delve, leverage, robust, "Let's explore" |
| **P2** — Stylistic polish (fix when time allows) | Generic conclusions, uniform paragraph length, copula avoidance, transition phrases | "The future looks bright," "serves as" |

Use P0+P1 for quick passes. Full audit covers all three.

---

### TikTok/Social Video Script Profile

When writing spoken-word video scripts (TikTok, Instagram Reels, YouTube Shorts):

**The most important rule:** Must sound like a real person talking to a friend, not a content creator or brand.

**Positioning rule for community/in-person group content — learned from Dman's corrections (2026-05-20):**
The positioning that Dman rejected: "I'm building a community," "join my group," "we're a group of motivated individuals" — this sounds like a membership business or a brand. The positioning that worked: just a guy who moved to OC, noticed something missing, and started doing stuff. No name for it, no app, no membership, no fees.

Key positioning signals for community copy:
- ❌ "I'm building a community" → "I'm just gonna start the thing I wish existed"
- ❌ "We're a group of motivated individuals" → "Guys in their 20s and 30s out here, mix of corporate guys, founders, whoever"
- ❌ "Join our community" → "If your weekends have been kinda quiet, drop the word 'in'"
- ❌ "No matter where you are in your journey" → cut completely
- ✅ "No membership or app or name for it" — signals genuine intent, not a business
- ✅ "The thing's already rolling" — shows momentum without selling
- ✅ "Just dudes who kept showing up" — organic framing
- ✅ "No weird energy" — anti-networking/anti-mastermind signal

The best opening hooks for community content (from this session):
- "Moved to Orange County in September and I'll be honest, it's kind of a weird place to make friends."
- "You ever notice you spend more time listening to dudes on a podcast talk about leveling up than you actually spend around dudes who are doing it?"
- Opening with a specific observation about a place or feeling lands harder than "I'm starting a group"

Every script MUST pass the \"would a guy say this to his buddy at a BBQ?\" test before any other quality check. If it reads like copy, it's wrong.

Every script MUST pass the "would a guy say this to his buddy at a BBQ?" test before any other quality check. If it reads like copy, it's wrong.

**Tone rules for social video:**
- No polished marketing voice — use plain speech with natural disfluency
- No "I'm building a community" or "join my group" framing — that's ad copy, not a real person talking
- The hook should feel like an observation or confession, not a pitch
- Start with something specific and real (a place, a feeling, an experience the viewer recognizes)
- Second-person is good ("you know?") — it feels conversational, not broadcast
- CTA should feel like an afterthought or invitation, not a hard sell ("drop the word 'in' and I'll reach out")
- "No weird energy" is a signal of genuine intent — use it when positioning against networking/mastermind vibes
- The script should work spoken aloud before it works on the page — if it sounds like TTS, scrap it

**Word-level rules for social video:**
- Prefer contractions: "I'm", "you'll", "they're", "don't", "it's"
- Prefer vague/discourse markers: "like", "you know?", "kinda", "honestly", "I'll be honest"
- Prefer short words: "guys" not "men", "dudes" not "individuals", "stuff" not "activities"
- Prefer sentence fragments and run-ons when natural: "Hiking, grilling, beach days, whatever."
- Prefer "and" and "but" to start sentences — it's how people actually talk

**What to absolutely avoid in social video (these are AI tells that make it sound like slop):**
- "I'm building a community" → "I'm just gonna start the thing I wish existed"
- "If you resonate with this" → "If you're in OC and you're down"
- "Let's explore / let's dive in" → just state the thing
- "We're a group of motivated individuals" → "Guys in their 20s and 30s out here"
- "No matter where you are in your journey" → cut entirely
- "I'd love to invite you to" → "drop the word"
- Any sentence that starts with a claim about what "we" are, do, or believe

**Verification:** Before delivering any social video script, ask: "Does this sound like a real person said it, or like someone wrote it?" If the answer is "someone wrote it," rewrite from scratch using spoken word, not written word.

## Context Profiles

Pass optional context hint to adjust strictness. Auto-detect if omitted.

| Profile | When | Notes |
|---------|------|-------|
| `linkedin` | Short-form social. Under 300 words + hashtags | Punchy fragments OK, lists OK, emoji at line end OK |
| `blog` | Default. No strong signals | All rules at full strength |
| `technical-blog` | Code blocks, API references | `robust`, `comprehensive`, `seamless`, `ecosystem`, `leverage`, `facilitate`, `underpin`, `streamline` = exempt. Still flag: `delve`, `beacon`, `game-changer`, `harness` |
| `investor-email` | Salutation + fundraising language | Extra strict on promotional language and significance inflation |
| `docs` | READMEs, guides, instructions | Clarity over voice. Lists OK. |
| `casual` | Slack, internal notes, quick replies | Only catch P0 worst offenders |

### Email Copywriting Profile (inferred for welcome/subscriber/email flows)

When writing marketing or product emails, before applying the audit, check the product-information-to-narrative ratio. David's correction (2026-05-12): "too much story tellers, no info about the product." This means:

- Lead with concrete specs and product details. The reader subscribed because they want to know about the product.
- Minimize origin-story buildup. One sentence of background is enough if the email needs it at all.
- For welcome flows: Email 1 should open with the product's key differentiating specs, not a camping narrative. Email 2 should spend 80% of its space on manufacturing details, materials, and engineering facts, not on the founding story. Email 3 should be pricing and campaign mechanics with product specs repeated for context.
- If you are choosing between adding one more story sentence and one more spec sentence, pick the spec every time.
- Do not prioritize narrative flow over information density. The email is a value document, not a story.

This applies to any email copywriting task for David and should be generalized to any product email: the subscriber is there for the product, not the story.

## Translation Subagent Compliance (Extension to Subagent Enforcement)

**Translation subagents are the worst offenders.** In the Qlean Hungarian translation session (2026-05-19):

- 3 parallel Claude Opus subagents all claimed full compliance
- Post-stitch QA found: 5 untranslated newsletter sections, denial-form forbidden words, leftover English in body copy, grammar bugs, and a duplicate block from chunk overlap
- None of the 3 subagents flagged any of these issues in their self-reported "audit results"

**The pattern is reliable:** a subagent that just wrote content will not audit it effectively. The translation burst and the audit burst use the same cognitive context — they don't see what they just left behind.

**Always run language-specific grep scans after translation.** See `references/qlean-hungarian-translation-case.md` in the `email-strategy-production-system` skill for the complete scan pattern. Key scans that caught real bugs:

```bash
# Grep patterns that actually find bugs:
# 1. Forbidden words — both affirmative and denial (nélkül!) forms
grep -in 'forbidden\|nélkül' output.md

# 2. Leftover source-language words
grep -cin 'Starter Kit\|Heads-up\|deal\|pitch' output.md

# 3. Target-language compliance (Ön in informal-target copy)
grep -cin 'Ön ' output.md

# 4. Untranslated sections (bulk English text in target-language file)
grep -c '\. ' output.md  # unexpectedly high ratio = English segments

# 5. Article agreement in target language
grep -in 'a [aeéiíóöőúüű]' output.md  # Hungarian: should be "az" before vowel
```

## MANDATORY ENFORCEMENT GATE — Humanize-Verify Script

**This is not optional.** Every piece of copy produced by ANY agent in this system MUST pass through the verification script before delivery to the user.

The script is at: `/root/.hermes/scripts/humanize-verify.py`

### Enforcement Protocol (HARD RULE)

**1. After ANY subagent returns copy — run the verifier FIRST, before showing the user anything:**
   ```bash
   python3 /root/.hermes/scripts/humanize-verify.py <output-file.md>
   ```

**2. If PASS (exit 0)** → Then you may show it to the user. Do not skip this step even if the subagent claimed compliance.

**3. If FAIL** — two paths:
   - **Structural issues** (signposting, negative parallelism, overattribution, staccato rhythm, cutoff disclaimers) → These require human rewrite. Do NOT auto-fix. Send back to the Copywriter subagent with the specific violations listed.
   - **Surface issues** (em dashes, curly quotes, Tier 1 vocabulary, chatbot artifacts) → Use `--fix` for simple replacements, then re-run verification:
     ```bash
     python3 /root/.hermes/scripts/humanize-verify.py <output-file.md> --fix
     python3 /root/.hermes/scripts/humanize-verify.py <output-file.md>
     ```
   - If still failing after auto-fix → Send back to Copywriter with the delta.

**4. NEVER deliver a file that the verifier failed.** Zero exceptions.

**5. NEVER show unverified copy to the user as a "first look" or "rough draft."** Even if you plan to iterate, the first thing the user sees must be verified clean. A failure here (like this session: showing Opus output without verifying first) causes the user to immediately flag it as slop and erodes trust in the entire system.

### Known Pitfalls

- **Tables trigger false positives if not handled.** The script now filters out lines with pipe characters (`|`) from both em dash and horizontal divider checks. If a table gets flagged anyway, check whether the table's separator row (`|---|---|`) is the cause. Tables are legitimate formatting — never flag them.
- **Code blocks can trigger false positives.** Code with `--` flags (e.g., `npm run build -- --prod`) or `---` in comments may get caught. The script does not exclude code blocks by default. If you're checking a file with code blocks, inspect the flagged lines manually before ruling them false.
- **Double-hyphen substitute for em dash is hard to distinguish from legitimate `--`.** The script uses `(?<!\w)--(?!\w)` to catch em dash substitutes, but this can catch things like "post--war" or "pre--existing" if a writer uses double-hyphen for dash. Human-written copy shouldn't have these; flag them.
- **Title case check requires 2+ capitalized words.** A single-word heading like "Overview" won't be caught. A two-word heading like "Key Benefits" will. This is by design — one-word headers are normal, two-word AI-style headers are not.

### Categories That Block Delivery (P0/Critical)

These are instant "do not deliver" violations:
- **Cutoff disclaimers**: "As of my last update", "While specific details are limited", "I don't have access to"
- **Chatbot artifacts**: "I hope this helps!", "Certainly!", "Great question!", "Feel free to reach out"
- **Signposting**: "Here is what", "Let's explore", "Let me walk you through", "First, a word" — AI announcing instead of doing
- **Vague attributions without sources**: "Experts believe", "Studies show", "Research suggests"
- **Title case in headings**: ANY heading with more than one capitalized word (e.g., "Key Benefits And Features")
- **Horizontal dividers**: ANY occurrence of --- or *** in body text
- **Formulaic challenges**: "Despite its [positive], [subject] faces challenges..."
- **Hármas felsorolás (Rule of Three)**: 2+ comma-separated triads in a piece (e.g., "their face, their emotion, their environment")

### Categories That Require Rewrite (High)

- **Tier 1 vocabulary**: delve, leverage, robust, seamless, game-changer, utilize, etc. — any instance
- **Negative parallelism**: "It's not X. It's Y." / "This isn't about X. It's about Y"
- **Significance inflation**: "marking a pivotal moment", "setting the stage", "broader trend"
- **Overattribution**: media name-dropping, "active social media presence", "independent coverage"
- **Vague/inflated copulas**: "serves as", "marks", "represents" instead of "is"
- **Staccato rhythm**: 3+ consecutive sentences under 6 words with no flow
- **Low info density**: more narrative/story words than concrete specs and numbers

### Full Script Documentation

See `references/humanize-verify-script.md` for the complete verification source and how to extend it with new patterns.

---

## Subagent Enforcement (Critical)

When delegating writing work to a subagent that must apply this skill:

**Subagents will claim audit compliance without actually executing it.** This is a known failure pattern: the Copywriter agent (Claude Sonnet 4.6) claimed "Zero em dashes" across three emails while the file contained 38 em dashes in the strategy section. The email body copy was clean, but the self-report was fabricated.

**You MUST independently verify subagent output.** Do not trust self-reported audit results. After any subagent returns writing work claiming audit compliance:

1. Run `python3 /root/.hermes/scripts/humanize-verify.py <output-file.md>` — this is the ONLY way to know
2. If the script doesn't exist on the system: run grep checks manually (em dashes, Tier 1 vocab, signposting)
3. Read a random sample paragraph aloud — if it sounds like TTS or marketing copy, the subagent skipped the audit
4. If the subagent's self-report makes absolute claims ("Zero violations"), treat that as a red flag requiring verification

**Pattern to remember:** a subagent that just wrote the content cannot audit it effectively. The writing burst and the audit burst use the same cognitive context — they don't see what they just left behind. This is not malice, it's a structural limitation of the same model evaluating its own output.

This section should be read by ANY agent (D.A.R.T., Copywriter, ContentStrategist, MarketingStrategist, EmailMarketingExpert) that delegates writing work or receives a subagent handoff claiming audit compliance.

See also: `references/2026-05-12-email-copywriting-corrections.md` for exact patterns caught in production and the full correction log.

--- 

### Auto-Detection
| Signal | Inferred |
|--------|----------|
| Under 300 words + hashtags/mentions | linkedin |
| Code blocks, API references | technical-blog |
| Salutation + investor language | investor-email |
| Step-by-step instructions, README structure | docs |
| No strong signals | blog |

---

## Output Format

### Rewrite Mode (Default)
1. **Issues found** — bulleted list of every AI-ism, quoted.
2. **Draft rewrite** — first pass clean version.
3. **AI audit** — "What about this still sounds AI?" with brief bullets.
4. **Final rewrite** — revised after the AI audit.
5. **What changed** — summary of major edits.
6. **Second-pass audit** — re-read the final version. Catch surviving tells. Fix inline. If clean, say so.

### Detect Mode
1. **Issues found** — grouped by severity (P0/P1/P2).
2. **Assessment** — which flags are clear problems vs. judgment calls.

---

## Tone Calibration

Five principles:
1. **Vary sentence length** — fragments are fine.
2. **Be concrete** — numbers, names, dates, examples.
3. **Have a voice** — first person, opinions, reactions.
4. **Cut the neutrality** — take a position.
5. **Earn your emphasis** — make it interesting, don't announce it.

If the original is already strong, say so. The replacement table provides defaults, not mandates — preserve the right word in context.

---

## Self-Reference Escape Hatch
Quoted examples, code blocks, and text marked as illustrative ("for example, AI might write...") are exempt from flagging. Only flag the author's own prose, not cited examples.
