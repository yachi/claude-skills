# claude-skills — project notes

Reference for working in this repo. It documents repo-specific facts a fresh session
cannot infer. (An A/B test on 2026-10-04 found these rules did NOT change a capable
agent's one-shot decisions — generic process discipline is already covered by the
global CLAUDE.md and general competence. So treat this as a fast on-ramp and a
checklist, not a behavior fix.)

## Layout
- `skills/deep-research/` — the main skill. `SKILL.md` is the prompt; `eval/` is its test harness; `autoresearch/` is the self-improvement loop.
- `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` — the plugin manifests.

## Shipping a skill change
- A `SKILL.md` edit reaches NO installed session until the version is bumped in BOTH `.claude-plugin/plugin.json` AND `.claude-plugin/marketplace.json`. Installed sessions load the pinned cached version under `~/.claude/plugins/cache/`, not the repo.
- After the user updates the plugin, confirm the cache copy matches the repo (`diff` them).

## Evaluating a skill change
- `eval/grade.py` grades a research REPORT, not `SKILL.md`. Running it on the instruction file is a category error (it scores ~22-24 because the skill is not a report).
- The only regression test is the skill executed on a prompt, then graded. Scores are high-variance: use N≥3 runs per version, and do not trust a per-eval delta or a total delta under ~3 from a single run.
- New behavioral rules in a skill need their own eval. Sequence: build harness → run the skill live → fix graders against REAL output → THEN commit. A grader proven only on hand-authored fixtures is unverified against real inputs.
- Authoritative graders: `eval/grade_v11.py` (TEXT behaviors B2,B3,B4,B6,B7,B9), `eval/grade_trace.py` (TRACE behaviors B1,B5,B8). `eval/scenarios/grade_scenarios.py` is a thin dispatcher over those two — do not re-implement grading logic elsewhere.
- Self-test: `python3 eval/selftest_v11.py` (graders discriminate) and `python3 eval/golden/scorecard.py` (all 9 behaviors pass on real captured output).
- When a grader disagrees with a report, read the artifact yourself and fix the grader or the skill — never the golden/report. `eval/golden/` is an external oracle; never regenerate it from the graders.

## Git
- Conventional Commits. Do not add a `Co-Authored-By: Claude` line. The main thread commits after reviewing diffs; the user pushes.
