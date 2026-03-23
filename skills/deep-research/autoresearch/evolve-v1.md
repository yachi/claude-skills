---
description: "One iteration of /dr auto-evolution: generate a harder test case, run skill, grade (8 evals), simplify skill, re-grade, keep winner. Use with /loop for continuous improvement."
---

# /dr Auto-Evolve — Single Iteration

You are an autonomous skill optimizer for the `/dr` deep research skill.

## Read State

1. Read the log at `autoresearch/log.md` to determine run number and current champion score.
2. Read the current skill at `skill/SKILL.md`.
3. Read the program at `autoresearch/program.md` for the eval suite.

## Step 1: Generate a Hard Test Prompt

Do NOT reuse previous prompts. Generate a NEW prompt that is harder than what's been tested. Draw from these difficulty escalation strategies:

- **Cross-domain**: Combine 2-3 unrelated domains (e.g., ML + regulatory + supply chain)
- **Flawed premise**: Embed a popular misconception the skill must catch
- **Adversarial framing**: Ask to "prove" something that's nuanced or false
- **Ambiguous constraints**: Give conflicting requirements that force tradeoff analysis
- **Niche domain**: Pick domains far from tech (agriculture, maritime law, pharmaceutical manufacturing)
- **Time-sensitive**: Reference evolving regulations or recent events the skill must verify

Write the prompt to the log before running.

## Step 2: Run the Skill

Spawn a subagent (opus model) that:
1. Reads `skill/SKILL.md`
2. Follows the skill to research the test prompt
3. Saves output to `autoresearch/outputs/run-{N}.md`

## Step 3: Grade (16 binary evals)

Grade using `python3 autoresearch/grade.py <output.md>` (add `--flawed-premise` if the prompt has one). If Bash is denied, grade manually against these 16 criteria:

**Tier 0 (structural):** E1: 15+ URLs, E2: confidence %, E3: comparison table, E4: standard by clause, E5: code block, E6: premise challenge, E7: cost figures, E8: counterargument
**Tier 1 (verifiable):** E9: URLs use legit TLDs, E10: 3+ specific clause citations, E11: numbers have inline sources
**Tier 2 (quality):** E12: code is executable (has imports/language tag), E13: recommendation has change conditions, E14: word count 1500-5000
**Tier 3 (rigor):** E15: no [unverified] in key findings, E16: sources section is organized by category

## Step 4: Simplify (if score = 16/16)

If the skill already passes 8/8, try to make it SHORTER without losing score:
1. Read the current SKILL.md and count lines
2. Identify the most verbose section (longest paragraph or most redundant instruction)
3. Make ONE simplification: compress, merge, or remove redundant text
4. Re-run the SAME test prompt with the simplified skill
5. Re-grade. If still 8/8 AND line count decreased: keep the simplification. Otherwise: revert.

This prevents the skill from growing bloated over time — the Karpathy principle of "keep it small."

## Step 5: Mutate (if score < 8/8)

If any eval failed:
1. Identify which eval(s) failed
2. Make ONE targeted mutation to the skill addressing the failure
3. Do NOT re-run yet — the next iteration will test the mutation

## Step 6: Log

Append to `autoresearch/log.md`:

```
## Run {N} — {date} evolve
- **Test prompt:** {the generated prompt}
- **Score:** {X}/8 (E1:{0|1} ... E8:{0|1})
- **Action:** {simplify | mutate | none}
- **Change:** {what was changed, or "none — champion holds"}
- **Skill lines:** {line count before → after}
- **Result:** {kept | reverted | mutation pending}
- **Tokens:** {from agent result} | **Duration:** {from agent result}
```

## Step 7: Report

Output a one-line summary: "Run {N}: {score}/8. Skill: {lines} lines. Action: {what happened}."
