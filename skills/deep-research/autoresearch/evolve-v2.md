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

Run `python3 grade.py outputs/run-{N}.md` or grade manually against the 35 evals. If score < 31/35: fix the structural issue first (old flow). If >= 31/35: proceed to judge.

## Step 4: LLM Judge (deep, 3-5 minutes)

Read `judge.md` instructions. Evaluate the output on 8 criteria (C1-C8, max 40):
- **C1 Accuracy**: Pick 3 claims, WebSearch to verify
- **C2 Recommendation**: Would you stake $1M on this?
- **C3 Completeness**: What's missing?
- **C4 Honesty**: Does it acknowledge what it doesn't know?
- **C5 Actionability**: Could someone start Monday morning?
- **C6 Contextual Specificity**: Is advice tailored to user's constraints, not generic?
- **C7 Citation Faithfulness**: Do sources actually say what the report claims?
- **C8 Logical Chain**: Can you trace claim → evidence → inference?

Save judge results to `outputs/run-{N}-judge.md`.

## Step 5: Targeted Mutation (if judge score < 36/40)

The judge tells you exactly what's wrong. Make ONE mutation to SKILL.md targeting the specific finding:

| Judge finding | Mutation target |
|--------------|-----------------|
| Hallucinated author/citation | Strengthen Phase 7 Verify academic citations check |
| Numbers don't match across sections | Strengthen Phase 7 numerical consistency |
| Missing important angle | Add to Phase 1 decomposition or Phase 6 practitioner check |
| Recommendation too vague | Strengthen Phase 8 recommendation template |
| Overclaimed confidence | Strengthen confidence calibration section |
| Code doesn't work | Strengthen Phase 6 executable code requirement |
| Generic advice not tailored to constraints | Strengthen Phase 6 to require naming specific artifacts |
| Source doesn't support claim it's cited for | Strengthen Phase 7 cross-reference check |
| Conclusion doesn't follow from evidence | Strengthen Phase 5 logical chain requirement |
| No sensitivity analysis | Strengthen Phase 5 assumption audit to require "what if wrong" |
| Missing scope boundaries | Add scope statement requirement to Phase 8 template |
| No sample sizes or precision indicators | Strengthen Phase 4 statistical evidence requirement |

## Step 6: Simplify (if judge score >= 36/40)

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
- **Regex:** {X}/35
- **Judge:** {X}/40 (C1:{} C2:{} C3:{} C4:{} C5:{} C6:{} C7:{} C8:{})
- **Fact-checks:** {verified}/{total}
- **Issues found:** {list from judge}
- **Action:** {mutation description | simplify | none}
- **Skill lines:** {before → after}
```

## Why This Is Better

The old flow ran 79 regex-passing outputs before we discovered a hallucinated co-author. The judge would have caught it on run 1. Regex tests form; the judge tests truth. Use both: regex as a fast gate, judge as the real quality check.

Tier 8 evals (E30-E35) and judge criteria C6-C8 were added after the paperclipai incident (2026-04-03), where a research output scored 29/29 on all existing evals but failed to name the specific config file (`~/.tool-versions`) the user needed to edit. Citation faithfulness (C7) was added based on FActScore/MiniCheck/CiteAudit literature showing that "confident wrong > uncertain correct" is the #1 practitioner eval complaint.
