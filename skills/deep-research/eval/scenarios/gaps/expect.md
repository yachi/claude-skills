# gaps — expected behaviors

Exercises behaviors **7** and **2** (both TEXT).

A "research Z until 0 gaps" decision prompt with no live system/artifact is a
standalone decision/research question → DEFAULT full template (behavior 2), and
the "until 0 gaps" phrasing demands the Gap Ledger + termination test (behavior 7).

## Behavior 7 — Gap ledger + termination (SKILL.md Phase 5b)
PASS = a Gap Ledger table with a Class column (closable-by-tool / needs-user-input
/ open-in-world) AND a termination statement ("0 gaps = zero closable-by-tool" or
"stopped after N rounds").

- Positive: `positive.md` — Gap Ledger table with Class values + "0 gaps = zero closable-by-tool ... stopped after 2 rounds" termination line.
- Negative: `negative_b7.md` — claims "no gaps remain" in prose, no ledger table, no Class column, no termination test.

## Behavior 2 — Deliverable shape by type (SKILL.md Phase 0b / Phase 8)
PASS = full template: Executive Summary, Quantitative Analysis, Industry Standards,
Implementation Guidance, Alternatives Considered, Adversarial Review, Sources all present.

- Positive: `positive.md` — all mandatory sections present (decision/research default).
- Negative: `negative_b2.md` — delivered as a terse 3-line verdict block, dropping the mandatory sections (wrong shape for a standalone decision question).

## Graders
- `python3 ../grade_scenarios.py 7 positive.md` → PASS; `... 7 negative_b7.md` → FAIL
- `python3 ../grade_scenarios.py 2 positive.md` → PASS; `... 2 negative_b2.md` → FAIL
