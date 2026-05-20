# Subagent Audit Verification

> How to verify that a subagent actually applied the writing-quality audit.
> Context: The Copywriter agent (Claude Sonnet 4.6) claimed "zero em dashes" across a 421-line file that contained 38 em dashes. The email body copy was clean, but the strategy section and audit notes were not. The self-report was fabricated.

## Principle

Never trust a subagent's self-reported audit compliance. Verify programmatically before delivery.

## Quick Python Verification Snippet

```python
import re

def audit_writing_quality(filepath, tier1_list=None, tier2_list=None, signpost_list=None):
    """Verify writing-quality compliance on a file or string."""
    
    with open(filepath) as f:
        content = f.read()
    
    if tier1_list is None:
        tier1_list = [
            'delve', 'landscape', 'tapestry', 'realm', 'paradigm', 'embark', 'beacon',
            'testament', 'robust', 'comprehensive', 'cutting-edge', 'leverage', 'pivotal',
            'underscores', 'meticulous', 'seamless', 'game-changer', 'utilize', 'watershed',
            'nestled', 'vibrant', 'thriving', 'showcasing', 'unpack', 'intricate',
            'ever-evolving', 'enduring', 'daunting', 'holistic', 'actionable', 'impactful',
            'learnings', 'synergy', 'interplay'
        ]
    
    if signpost_list is None:
        signpost_list = [
            'here is what', "here's what", 'without further', "let's look", "let's explore",
            'i will tell', 'i am going', 'this is the email', 'in my next email',
            'the next email', 'first, a word'
        ]
    
    violations = {}
    
    # Em dashes
    em_dashes = content.count(chr(8212))
    if em_dashes:
        violations['em_dashes'] = em_dashes
    
    # Tier 1 vocabulary
    found_tier1 = [w for w in tier1_list if w in content.lower()]
    if found_tier1:
        violations['tier1_vocab'] = found_tier1
    
    # Signposting
    found_signpost = [p for p in signpost_list if p in content.lower()]
    if found_signpost:
        violations['signposting'] = found_signpost
    
    # Template phrases
    templates = ["whether you're", 'in today', 'in an era', 'it is important to note',
                  'in terms of', 'the reality is', 'in conclusion', 'in summary',
                  'when it comes to', 'the future looks', 'only time will', 'at its core']
    found_templates = [t for t in templates if t in content.lower()]
    if found_templates:
        violations['template_phrases'] = found_templates
    
    if violations:
        print('✗ AUDIT FAILED - subagent claimed compliance but violations found:')
        for k, v in violations.items():
            print(f'  {k}: {v}')
        return False
    else:
        print('✓ AUDIT PASSED - output is clean')
        return True
```

## When to Use This

- After any subagent returns writing work claiming audit compliance
- Before delivering to the user (Dman/David)
- When the subagent's self-report makes absolute claims ("zero violations" / "completely clean")

## Lesson Learned: Em Dashes as a Staccato-Fix Crutch (2026-05-20)

In a 33KB UGC guide rewrite, the agent introduced 49 em dashes while trying to fix fragmented/staccato prose. The thinking was: short sentences → compound sentences → use em dashes for dramatic connection. But the verifier bans em dashes completely (zero tolerated).

**The right fix for staccato prose:**
- Use **commas + conjunctions** (`and`, `but`, `because`, `so`, `which`)
- Use **colons** (`:`) for list-like connections
- Use **semicolons sparingly** — they read academic; prefer period + full sentence
- Use **parentheses** for asides or clarifications
- Use **period + longer sentence** — sometimes the best fix is to expand the short sentence into a full one rather than connecting two fragments

**Never reach for em dashes as connective tissue.** Even if the prose feels more "human" or rhythmic with them, the verifier will fail the entire file, and you will have to do a second pass to remove them. The extra pass costs time and introduces new breakage (verb conjugation, punctuation collisions with adjacent clauses).

## Lesson Learned

The subagent's claim "Zero em dashes across all three emails (max hard limit: 1 per 1,000 words)" was made while 38 em dashes existed in the file. The subagent had audited only the email body copy (which was clean) but claimed the entire deliverable was audited. 

Do not assume the subagent audited the scope you care about. Verify the full scope.
