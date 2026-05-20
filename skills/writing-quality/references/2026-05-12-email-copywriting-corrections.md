# Email Copywriting Corrections — 2026-05-12

## Session Summary

David requested a 3-email welcome subscriber flow for Lattice Glamping (Indiegogo waitlist). The copy went through correction cycles, revealing specific patterns the writing-quality audit should catch.

## Exact Pattern Corrections

### Signposting/Announcements (flagged and removed)

These are all variants of "AI telling what it will do instead of doing it":

```
"I will tell you the full story in my next email."
→ (cut entirely, just write the story)

"But for now I just want you to know:"
→ (cut)

"Instead, here is what you can expect:"
→ (cut, just present the information)

"This is not a normal welcome email because this is not a normal product and you are not a normal subscriber."
→ (cut, "It's not X because it's not Y" variant)

"I want to honor that by not burying you in"
→ (pretentious, cut)

"Here is the breakdown:"
→ (cut)

"Here is what that actually means."
→ (cut)

"Next email I am going to walk through exactly how the campaign will work."
→ "The campaign works with early-bird tiers..."

"The next email covers the campaign pricing..."
→ "The campaign pricing... are in the next email"

"This is the email where I answer the question you have been wondering since you subscribed"
→ (cut, just answer)

"First, a word about how crowdfunding works."
→ (cut, just explain)

"What I can tell you: the early-bird tier will be..."
→ (cut "What I can tell you", state directly)

"What I can tell you is this:"
→ (same pattern, used TWICE in email 3)

"Here is what you get:"
→ (cut, just list the specs)

"Over the next two emails I will cover how the campaign works..."
→ (cut, present the information directly)
```

### "It's not X — it's Y" pattern variant

The skill flags em-dash variants. But it also appears as two sentences separated by a period:

```
"The Lattice suite is not a tent. It is a portable room with..."
→ "The Lattice suite is a portable room with..."
```

Same reframing pattern. Flag it regardless of punctuation.

### Staccato Rhythm (David: "too short sentences, no real flow")

The original copy had mostly 3-8 word sentences in sequence. Every sentence was a standalone island with no connective tissue:

```
"It is 4am. You are awake. The ground is hard. Your back hurts. You have to pee."
```

Fix: Use compound sentences with commas, conjunctions, and subordinate clauses to create natural flow between ideas. A 30-word flowing sentence followed by a 6-word punch is more natural than ten 6-word sentences.

### Product-Information-First (David: "too much story tellers, no info about the product")

The welcome emails led with camping pain narrative and origin story before getting to product specs. David's correction: lead with specs, minimize story.

Wrong priority: pain narrative > founder story > product specs > campaign info
Right priority: product specs > manufacturing details > pricing/campaign > (minimal story)

## Verification Pattern

After any subagent returns email copy claiming "writing-quality audit applied":

1. grep for em dashes (—) — should be 0 in email body
2. grep for signposting patterns: "here is what", "i will tell", "i am going to", "this is the email", "in my next", "the next email", "over the next", "first, a word", "what i can tell", "here is the breakdown"
3. grep for "It is not" / "This is not" followed by "It is" / "This is" patterns
4. Read a random paragraph aloud — if every sentence is 3-8 words with no flow, flag it
5. Check product-info-to-story ratio — is there more concrete spec copy than narrative?

Do not deliver unverified subagent output to David. Always run these checks first.
