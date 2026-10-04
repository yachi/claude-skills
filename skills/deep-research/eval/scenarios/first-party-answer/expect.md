# first-party-answer — expected behaviors

Exercises behaviors **1** and **8** (both TRACE, graded on the tool-call transcript).

## Behavior 1 — First-party evidence first (SKILL.md Phase 1.5)
The root cause (64 worker threads contending for a 5-connection pool; 8s payment
calls hold connections; waiters hit the 2s acquire timeout → 503) is already
inside `config.yaml` + `app.log`. A compliant run reads those local files
(Read/Grep/Bash) BEFORE any WebSearch/WebFetch.

- PASS assertion: a local Read/Grep/Bash-on-repo call occurs before the first web call.
- Positive fixture: `positive.jsonl` — reads config.yaml and greps app.log, then (optionally) searches the web for pool-sizing guidance.
- Negative fixture: `negative_b1.jsonl` — WebSearch("checkout 503 causes") fires first, before any local read.

## Behavior 8 — Durable output path (SKILL.md Phase 8 'Durable output path')
The prompt asks for the write-up to be kept.

- PASS assertion: the report Write targets a path NOT under /tmp or scratch.
- Positive fixture: `positive.jsonl` — Write to `./checkout-503-root-cause.md` (project dir).
- Negative fixture: `negative_b8.jsonl` — Write only to `/tmp/report.md`.

## Graders
- `python3 ../grade_scenarios.py 1 positive.jsonl` → PASS; `... 1 negative_b1.jsonl` → FAIL
- `python3 ../grade_scenarios.py 8 positive.jsonl` → PASS; `... 8 negative_b8.jsonl` → FAIL
