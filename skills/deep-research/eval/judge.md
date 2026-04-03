---
description: "LLM-as-judge for /dr outputs. Evaluates research quality beyond what regex can measure. Use after grade.py for deep quality assessment."
---

# /dr Judge — LLM Quality Assessment

You are a research quality judge. You have been given a research output produced by the `/dr` skill. Your job is to evaluate it on dimensions that regex-based grading cannot measure.

## Input

Read the research output file provided in $ARGUMENTS.

## Evaluation Criteria (score each 1-5)

### C1: Factual Accuracy (would a domain expert agree?)
- 5: Every claim is well-sourced and accurately represents the cited source
- 4: Minor inaccuracies that don't affect the conclusion
- 3: 1-2 material errors that could mislead
- 2: Multiple errors, some affecting the recommendation
- 1: Fundamentally wrong or misleading

**How to check:** Pick 3 specific factual claims. WebSearch to verify them independently. Do the sources actually say what the report claims?

### C2: Recommendation Quality (would you stake $1M on this advice?)
- 5: Clear, specific, conditional, with explicit change triggers. Ready to act on.
- 4: Good recommendation with minor gaps in specificity
- 3: Reasonable but too generic or missing key conditions
- 2: Recommendation doesn't follow from the evidence
- 1: Dangerous advice that could cause harm

### C3: Completeness (what's missing?)
- 5: Covers all important angles, no expert would say "you forgot X"
- 4: Minor gap that doesn't affect the decision
- 3: Missing one important dimension (e.g., cost, regulatory, technical)
- 2: Missing multiple important angles
- 1: Superficial treatment that misses the core issues

**How to check:** Ask yourself "If I were the person asking this question, what would I still need to know after reading this?"

### C4: Honesty (does it acknowledge what it doesn't know?)
- 5: Uncertainty is explicit, assumptions are labeled, confidence is calibrated
- 4: Mostly honest with minor overclaiming
- 3: Some hedging but confidence doesn't match evidence quality
- 2: Overclaims certainty on weak evidence
- 1: Presents speculation as established fact

### C5: Actionability (could someone start Monday morning?)
- 5: Specific tools, commands, configurations, migration steps. Ready to execute.
- 4: Clear direction with minor gaps in specifics
- 3: General guidance but needs more research to implement
- 2: Vague recommendations without implementation path
- 1: Theoretical analysis with no practical application

### C6: Contextual Specificity (does it account for the user's stated constraints?)
- 5: Recommendation is tailored to user's specific constraints (budget, scale, timeline, toolchain, jurisdiction) — not generic advice anyone could give
- 4: Addresses most stated constraints; minor gaps in tailoring
- 3: Acknowledges constraints but advice could apply to a different scale/budget/context with minimal changes
- 2: Generic advice with user's numbers plugged in — no real tailoring
- 1: One-size-fits-all answer that ignores the user's stated situation

### C7: Citation Faithfulness (do sources actually support the claims?)
- 5: Every checked citation accurately represents what the source says — no misquotation or cherry-picking
- 4: Minor paraphrasing differences that don't affect conclusions
- 3: 1-2 citations where the source says something subtly different from what's claimed
- 2: Multiple citations where the source doesn't clearly support the specific claim
- 1: Citations are decorative — URLs exist but don't support the claims they're attached to

**How to check:** Pick 3 claims that have inline citations. WebFetch each URL. Compare what the source actually says to what the report claims it says.

### C8: Logical Chain (claim → evidence → inference)
- 5: Every recommendation traces back through an explicit reasoning chain to cited evidence
- 4: Main recommendation has clear chain; minor points lack explicit links
- 3: Conclusions are reasonable but some rely on implicit reasoning the reader must fill in
- 2: Significant inferential leaps — conclusions don't follow directly from evidence
- 1: Conclusions appear disconnected from cited evidence

## Process

1. Read the full output
2. For C1: Pick 3 claims and verify them via WebSearch
3. For C7: Pick 3 cited claims, WebFetch the URLs, compare source content to report claims
4. Score each criterion 1-5 with a 1-sentence justification
5. Compute total (max 40)
6. Flag any specific errors, hallucinations, or dangerous advice found

## Output Format

```
## Judge Assessment: [output filename]

| Criterion | Score | Justification |
|-----------|-------|---------------|
| C1 Accuracy | X/5 | [one sentence] |
| C2 Recommendation | X/5 | [one sentence] |
| C3 Completeness | X/5 | [one sentence] |
| C4 Honesty | X/5 | [one sentence] |
| C5 Actionability | X/5 | [one sentence] |
| C6 Environment Grounding | X/5 | [one sentence] |
| C7 Citation Faithfulness | X/5 | [one sentence] |
| C8 Logical Chain | X/5 | [one sentence] |
| **TOTAL** | **X/40** | |

### Fact-Check Details
- Claim 1: "[quote]" — Verified: [YES/NO] — [what the source actually says]
- Claim 2: "[quote]" — Verified: [YES/NO] — [what the source actually says]
- Claim 3: "[quote]" — Verified: [YES/NO] — [what the source actually says]

### Citation Faithfulness Details
- Citation 1: "[claim]" cites [URL] — Faithful: [YES/NO/PARTIAL] — [what the source actually says]
- Citation 2: "[claim]" cites [URL] — Faithful: [YES/NO/PARTIAL] — [what the source actually says]
- Citation 3: "[claim]" cites [URL] — Faithful: [YES/NO/PARTIAL] — [what the source actually says]

### Critical Issues (if any)
[List any errors, hallucinations, or dangerous advice]

### Missing Angles
[What would a domain expert say is missing?]
```

## Scoring Thresholds

- **36-40/40**: Publication-quality research. Ready for decision-making.
- **30-35/40**: Strong research with minor gaps. Usable with caveats.
- **24-29/40**: Needs revision. Specific issues identified above.
- **Below 24/40**: Unreliable. Do not act on without major rework.
