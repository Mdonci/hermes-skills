# Product Spec Card — Canonical Reference

**Purpose:** Before running any pipeline phase, write a canonical product spec card to `~/.hermes/research/output/[product]/product-spec-card.md`. Every subagent task context must reference this file path rather than inline specs. This prevents subagents from hallucinating different specs across documents.

**Required fields:**

## Product Spec Card Template

```markdown
# Product: [Product Name]
Client: [Company Name]
Launch: [Date/Platform — e.g., "Indiegogo July 1, 2026"]

## Core Specifications
| Field | Value | Source |
|-------|-------|--------|
| Weight | [e.g., 45-50 kg / 99-110 lbs] | [USP doc, website] |
| Package size (folded) | [W×H×D in cm/in] | |
| Interior floor | [W×D in m/ft] | |
| Peak height | [e.g., 2.1m / 6.9ft] | |
| Setup time | [e.g., 3 min] | |
| Setup crew | [e.g., 1 person] | |
| Tools required | [e.g., Zero / None] | |
| Frame material | [e.g., Premium aluminum, laser-welded] | |
| Fabric | [e.g., UV & waterproof polycotton] | |
| Wind resistance | [e.g., 100 km/h] | |
| Key features | [e.g., Blackout bedroom, LED lighting, adjustable legs, modular expansion] | |

## Pricing
| Tier | Price (EUR) | Price (USD approx) |
|------|-------------|---------------------|
| Super Early Bird | €X,XXX | $X,XXX |
| Regular Early Bird | €X,XXX | $X,XXX |
| Indiegogo Special | €X,XXX | $X,XXX |
| Retail MSRP | €X,XXX | $X,XXX |

## Company Context
- HQ: [City, Country]
- Founded: [Year]
- Prior business: [B2B/B2G segments]
- Launch market: [e.g., US via Indiegogo]
- Website: [URL]
- Social: [Instagram, Facebook, LinkedIn, etc.]

## Product Category & Substitutes
- Direct category: [e.g., Hitch-mounted foldable glamping unit]
- Adjacent categories: [e.g., Rooftop tents, pop-up campers, inflatable hitch tents, teardrop trailers, RVs]
```

## Usage in Subagent Context

When delegating a task, include this exact snippet in the `context` parameter:

```
## PRODUCT SPECS (canonical — do not modify)
See /root/.hermes/research/output/[product]/product-spec-card.md
Key values: [WEIGHT X kg], [PRICE $X SEB / $X retail], [SETUP X min], [HEIGHT X m]
```

This gives subagents the critical numbers (weight, price, setup, height) inline while pointing to the full spec card for reference.
