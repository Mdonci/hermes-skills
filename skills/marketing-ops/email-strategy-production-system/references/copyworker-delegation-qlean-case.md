# Copyworker Delegation — Qlean Case Study

Produced 2026-05-19. 50+ emails across 13 flows. QA: 88/100 → fixed → production-ready.

## What worked

### Delegation brief
The Copyworker brief must include:
1. **The strategy document** (read the full `-master.md` file)
2. **Explicit format structure** per email (see `templates/email-copy-package-header.md`)
3. **Model override** — explicitly request `claude-opus-4-7` (provider: anthropic) for this task. It auto-upgraded from Sonnet to Opus and the quality was visibly better
4. **Forbidden terms list** — include it in the context, not just the strategy doc reference. QA found "vapor" in a place the Copywriter thought was fine
5. **"Write EVERY email in full — no skeletons, no placeholders, no 'see above'"** — this was the key instruction that made the output production-ready

### Model behavior
- Claude Opus produced ~36K tokens of output in one call
- It auto-generated a Creative Brief section at the top that wasn't explicitly asked for — this was good
- It used specific, editorial-grade language (Tihany lavender, 1928 abbot, Calabrian bergamot co-op) — far better than templated copy
- It wrote visual briefs at designer-ready detail without being prompted for every field

### Output file structure
The output file (`qlean-email-copies-complete.md`) had this shape:
1. Creative Brief
   - Brand Voice
   - Visual Identity (hex palette table)
   - Photography Style
   - Do's and Don'ts (visual cheat sheet table)
2. Flow 1 — Welcome (Email 1.1 through 1.7)
3. Flow 2 — Browse Abandonment (Email 2.1, 2.2)
4. ...through Flow 13
5. Each email: Type → Subject → Preview → Body → CTA → Visual Brief → Designer Instructions → Copywriting Notes

## QA findings from this session

| Issue | Location | Fix |
|-------|----------|-----|
| "plant-based vapor mist" | Email 1.2 body copy | → "pure botanical mist that rises, lingers, and fades" |
| "made the switch" / "switched" | Email 1.1 body + Email 1.3 subject | → "started the ritual" / "brought one home" |
| Missing SMS for Payment Failed | Flow 9 | Added SMS between Email 9.2 and 9.3 |
| "nicotine" in denial form | Email 1.2 ingredient list | OK — "No nicotine" as ingredient statement is factual disclosure, not a health claim |

## Key insight for future runs
The Copyworker should be told to put "vapor" on the forbidden list even if the strategy doc doesn't list it. Aromatherapy brands naturally drift toward "vapor" language because steam/vapor is associated with essential oil diffusers. The compliance filter is tighter than the natural brand voice — always err toward compliance.

The second copy production phase (full body copy) should NOT repeat the strategy creation's agent pattern. It's a single-agent task (Copyworker + QA), not a multi-agent flow. The strategy is already done. The copyworker just needs the approved strategy file and the template.
