---
description: "V2 evolve loop: regex gate → LLM judge → targeted mutation → simplify. Catches substance errors, not just form."
---

# /dr Auto-Evolve V2

Two-layer eval: fast regex gate, then deep LLM judge. Mutations are driven by specific judge findings, not regex pattern failures.

## Read State

1. Read log at `autoresearch/log.md` for run number
2. Read skill at `skill/SKILL.md`

## Step 1: Generate Hard Prompt

Create a new test prompt. Rotate domains. Escalate difficulty. Never repeat.

## Step 2: Run the Skill

Research the prompt following SKILL.md. Use WebSearch, WebFetch, etc. Save to `outputs/run-{N}.md`.

## Step 3: Regex Gate (fast, 2 seconds)

Run `python3 grade.py outputs/run-{N}.md` or grade manually against the 23 evals. If score < 21/23: fix the structural issue first (old flow). If >= 21/23: proceed to judge.

## Step 4: LLM Judge (deep, 3-5 minutes)

Read `judge.md` instructions. Evaluate the output on 5 criteria (C1-C5, max 25):
- **C1 Accuracy**: Pick 3 claims, WebSearch to verify
- **C2 Recommendation**: Would you stake $1M on this?
- **C3 Completeness**: What's missing?
- **C4 Honesty**: Does it acknowledge what it doesn't know?
- **C5 Actionability**: Could someone start Monday morning?

Save judge results to `outputs/run-{N}-judge.md`.

## Step 5: Targeted Mutation (if judge score < 23/25)

The judge tells you exactly what's wrong. Make ONE mutation to SKILL.md targeting the specific finding:

| Judge finding | Mutation target |
|--------------|-----------------|
| Hallucinated author/citation | Strengthen Phase 7 Verify academic citations check |
| Numbers don't match across sections | Strengthen Phase 7 numerical consistency |
| Missing important angle | Add to Phase 1 decomposition or Phase 6 practitioner check |
| Recommendation too vague | Strengthen Phase 8 recommendation template |
| Overclaimed confidence | Strengthen confidence calibration section |
| Code doesn't work | Strengthen Phase 6 executable code requirement |

## Step 6: Simplify (if judge score >= 23/25)

If the output is publication-quality (23+/25), try to make the skill shorter:
1. Count lines
2. Find the most verbose instruction
3. Compress it
4. Re-run the SAME prompt
5. Re-judge. Keep only if judge score doesn't drop.

## Step 7: Log

```
## Run {N} — {date} evolve-v2
- **Prompt:** {prompt}
- **Regex:** {X}/23
- **Judge:** {X}/25 (C1:{} C2:{} C3:{} C4:{} C5:{})
- **Fact-checks:** {verified}/{total}
- **Issues found:** {list from judge}
- **Action:** {mutation description | simplify | none}
- **Skill lines:** {before → after}
```

## Why This Is Better

The old flow ran 79 regex-passing outputs before we discovered a hallucinated co-author. The judge would have caught it on run 1. Regex tests form; the judge tests truth. Use both: regex as a fast gate, judge as the real quality check.
