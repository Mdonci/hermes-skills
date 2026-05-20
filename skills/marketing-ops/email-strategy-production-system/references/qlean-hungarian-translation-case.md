# Qlean Hungarian Translation — Case Study (actual run, 2026-05-19)

## Summary

Successfully translated 1,902 lines of English email copy (13 flows, 50+ emails) to Hungarian. All 3 parallel chunks completed on claude-opus-4-7. Post-stitch QA found and fixed ~15 issues.

## Source file

`/root/.hermes/research/output/qlean-email-copies-complete.md` — 1,902 lines, 91 KB.
English body copy with Creative Brief, Visual Briefs, Designer Instructions, and Copywriting notes.

## Chunking

Split at flow boundaries using a Python script:

| Chunk | Lines | Flows | Size |
|-------|-------|-------|------|
| chunk1 | 1-962 | Creative Brief + Flows 1-5 (Welcome, Browse Abandon, Cart Abandon, Post-Purchase, First Reorder) | 962 lines, 47 KB |
| chunk2 | 958-1500 | Flows 6-10 (Ongoing Replenishment, Klub Convert, Klub Retention, Payment Failed, Winback) | 542 lines, 25 KB |
| chunk3 | 1462-1902 | Flows 11-13 (Review+Referral, Seasonal Campaigns, Newsletter/Editorial) | 440 lines, 19 KB |

Split points overlap by ~2 lines to avoid losing content at boundaries.

## Parallel translation

All 3 chunks delegated as a single `delegate_task(tasks=[...])` call on claude-opus-4-7, each with `toolsets=["file"]`.

- chunk1: completed in 402s, 5 API calls, 23K output tokens
- chunk2: completed in 221s, 4 API calls, 13K output tokens
- chunk3: completed in 178s, 4 API calls, 10K output tokens
- **Total wall time: 403s** (parallel — ran concurrently)

## Stitch

Simple Python concatenation: `c1 + '\n' + c2 + '\n' + c3` → 1,946 lines initially (later cleaned to 1,907 after removing duplicate block).

## QA findings

### Found by grep+patch (D.A.R.T.)

Quick grep scan caught:
- **Forbidden words in body copy (denial form):** "Nikotin nélkül. Dohánykivonat nélkül. Diacetil nélkül. Égés nélkül. Kátrány nélkül." — the brief explicitly bans these even in negative form
- **Adjacent vocabulary:** "pára" is one root from forbidden "párologtatás" — replaced with "levegő"
- **Leftover English:** "deal" → "ajánlat", "sales-pitch" → "eladás", "Heads-up." → "Előre is szólok"
- **Untranslated brand term:** "Starter Kit" → "Kezdőcsomag" (3 instances)
- **Grammar:** "a aromát" → "az aromát" (article agreement before vowel)
- **Untranslated newsletter sections:** Example Issues #2 and #3 had 5 sections still in English

### Found by QualityTester audit (claude-opus-4-7)

Deep scan found an additional ~8 minor calques/stiff phrasings plus confirmed the same issues. Also flagged:
- **Duplicate block from chunk overlap:** Email 11.1 appeared twice (once from chunk2 end, once from chunk3 start), plus an empty 11.2 header. Removed 38 lines.
- **Em dash density:** 375 em dashes across the file (carried over from English original — brand voice choice, not a bug)
- Sentence rhythm and "te" pronoun usage verified clean

### Fix pattern

All fixes done with `patch(old_string, new_string)` — no re-delegation. One bulk removal with a Python line-range script.

## Translation rules used (proven working)

Each chunk received identical instructions:

```
Translate ONLY customer-facing copy:
- Subject lines + preview text
- Email body (text between **Body:** and next element)
- CTA labels
- Blockquote testimonials
- SMS text
- Inline examples

Do NOT translate:
- Section headings ("## Email 1.1 — Welcome + Discount Delivery")
- Visual Brief, Designer Instructions, Copywriting notes
- Flow trigger descriptions
- The Creative Brief
- Hex codes, dimensions, font names
- English examples inside instructions
- Merge tags ({{product_name}})

Hungarian-specific conventions:
- Informal "te" throughout — NEVER "Ön"
- "Klub" stays as "Klub" — never "előfizetés"
- Sentence case only — NO title case
- Forbidden words not even in denial form
- Keep: Ft prices (with Hungarian spacing: 16 990 Ft), GLS, utánvét, phone numbers, discount codes
```

## Output file

`/root/.hermes/research/output/qlean-email-copy-hungarian.md` — 1,907 lines, 88 KB.

## What to do differently next time

1. **Reduced chunk size:** Using `tasks` array in a single `delegate_task`, max 3 parallel. For 1900 lines, 3 chunks of ~630 lines each would be safer (fewer timeouts).
2. **Verify ALL chunk files exist before stitch.** Parallel sessions can be interrupted.
3. **Run the grep scan FIRST** — before delegating the heavy QualityTester audit. The grep catches things the subagent won't report.
4. **Fix with patch, not re-delegation.** 15 issues fixed in ~60 seconds total with grep+patch. Re-delegating would take 3+ minutes and introduce new errors.
5. **Don't split mid-flow.** Chunk boundaries should be at flow boundaries (find `# FLOW` line numbers). Overlap by 2 lines max.
6. **Add a "denial form" check to QA grep** — the naive scan only catches affirmative forbidden words. Add `nélkül` to the pattern.
