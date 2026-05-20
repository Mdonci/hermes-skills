# humanize-verify.py — Reference

The mandatory enforcement gate for all copy output.

**Location:** `/root/.hermes/scripts/humanize-verify.py` (v2.1)

## Usage

```bash
# Basic scan (exit 0 = PASS, exit 10 = FAIL)
python3 /root/.hermes/scripts/humanize-verify.py <filepath>

# Auto-fix surface issues (em dashes, Tier 1 words, curly quotes)
python3 /root/.hermes/scripts/humanize-verify.py <filepath> --fix

# After fix, run plain scan again to confirm
python3 /root/.hermes/scripts/humanize-verify.py <filepath>
```

## What It Checks

### Critical (P0) — Blocks Delivery
| Category | Examples | Auto-fix? |
|----------|----------|-----------|
| Cutoff disclaimers | "As of my last update", "While specific details", "I don't have access" | No |
| Chatbot artifacts | "I hope this helps", "Certainly!", "Great question", "Feel free to reach out" | No |
| Signposting | "Here is what", "Let's explore", "Let me walk", "First, a word", "In my next email" | No |
| Vague attributions | "Experts believe", "Studies show", "Research suggests", "Industry leaders agree" | No |
| **Title case headings** | "Key Benefits And Features" — only sentence case allowed | No |
| **Horizontal dividers** | --- or *** in body text | No |
| Formulaic challenges | "Despite these challenges", "Despite its [adj]", "Challenges and Future" | No |
| AI defense signals | "Concrete evidence", "concrete examples", "in the absence of" | No |
| **Hármas felsorolás** | "their face, their emotion, their environment" — 2+ triads = blocked | No |

### High (P1) — Requires Rewrite
| Category | Examples | Auto-fix? |
|----------|----------|-----------|
| Tier 1 vocabulary | delve, leverage, robust, seamless, game-changer, utilize, serves as | Partial |
| Em dashes | — (U+2014) and -- | Yes |
| Negative parallelism | "It's not X. It's Y", "Not only... but", "This isn't about X. It's about Y" | No |
| Significance inflation | "marking a pivotal moment", "setting the stage", "broader trend" | No |
| Overattribution | "featured in [media list]", "active social media presence", "independent coverage" | No |
| Staccato rhythm | 3+ consecutive short sentences | No |
| Low info density | More narrative words than concrete specs/numbers | No |
| Vague/inflated copulas | "serves as", "marks", "represents" instead of "is" | No |

### Medium (P2) — Polish Before Ship
| Category | Examples | Auto-fix? |
|----------|----------|-----------|
| Transition overuse | "Moreover", "Furthermore", "Additionally", "In terms of" | No |
| Hedging | "perhaps", "notably", "interestingly", "surprisingly", "importantly" | No |
| Superficial -ing | ", highlighting", ", underscoring", ", reflecting", ", showcasing" | No |
| Uniform paragraphs | All paragraphs within 35% of mean length | No |
| Bold overuse | More than 1 bold phrase per section | No |
| Title case headers | "Strategic Negotiations And Key" instead of sentence case | No |
| Copula avoidance | 3+ instances of "serves as"/"marks"/"represents" | No |
| Curly quotes | "smart quotes" instead of "straight quotes" | Yes |

## Extending the Script

Add new patterns by editing the lists at the top of the file:

```python
# Add Tier 1 words
TIER1_WORDS.append('new_word_to_flag')

# Add signposting patterns (regex, description)
SIGNPOST_PATTERNS.append((r'my new pattern', 'Description of pattern'))

# Add significance inflation
SIGNIFICANCE_PATTERNS.append((r'pattern regex', 'Description'))
```

## Enforcement in D.A.R.T. Workflows

After ANY copy subagent returns work, D.A.R.T. MUST run:

```python
from hermes_tools import terminal
result = terminal(f"python3 /root/.hermes/scripts/humanize-verify.py {filepath}")
if "PASS" in result['output']:
    # Deliver to user
else:
    if result['exit_code'] == 10:
        # First try auto-fix for surface issues
        terminal(f"python3 /root/.hermes/scripts/humanize-verify.py {filepath} --fix")
        result2 = terminal(f"python3 /root/.hermes/scripts/humanize-verify.py {filepath}")
        if "PASS" not in result2['output']:
            # Still failing — send back to Copyworker with delta
            pass
```

## Known False Positive Rate

The script errs on the side of false positives. Some Tier 1 words are legitimate in specific contexts (e.g., "robust" in technical writing). The script flags them so D.A.R.T. can make the judgment call — the script's output is a gate, not a final editorial decision. D.A.R.T. can override and pass a file that flagged a false positive if the context warrants it.

However: signposting, cutoff disclaimers, and chatbot artifacts are NEVER false positives. They are always correct flags.

## Exemptions for Legitimate Formatting

The following are explicitly exempt from being flagged to avoid breaking legitimate markdown:

| Check | Exemption | Why |
|-------|-----------|-----|
| Em dashes (`--`) | Lines containing `\|` (pipe characters) | Markdown table separator rows contain `----------` which would otherwise be parsed as `--` em dash pairs |
| Em dashes (`--`) | Lines that are pure `---` (3+ hyphens) | These are horizontal dividers caught by a separate check |
| Horizontal dividers | Lines containing `\|` (pipe characters) | Table separator rows like `\|-------\|-------\|` contain consecutive `-` but are valid table formatting |

**Lesson from production (2026-05-19):** Dman reported the script "broke table formatting." The original regex `^---$` was matching `|---|` table rows because the pipe wasn't accounted for. The fix was to add pipe-line filtering to both the em dash counter and the horizontal divider checker. If you add new formatting checks, always test against a file that contains markdown tables, code blocks, and blockquotes — AI-writing detectors commonly false-positive on these.
