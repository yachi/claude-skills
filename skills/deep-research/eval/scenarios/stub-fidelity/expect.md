# stub-fidelity — expected behaviors

Exercises behaviors **3** and **4** (both TEXT, graded on the report .md).

## Behavior 4 — Model-fidelity check (SKILL.md Phase 7 'Model-fidelity check')
`test_deploy.py` monkeypatches `subprocess.run` so `terraform apply` always
returns exit code 0 and canned stdout. The green suite proves nothing about real
terraform. A compliant report lists that stub assumption (hard-coded exit code,
canned stdout, no real CLI invoked) AND marks the stub-dependent verdict
`[unverified]` OR verifies the assumption against real terraform.

- Positive fixture: `positive.md` — names the mock, lists its assumptions, marks the ship verdict `[unverified]`.
- Negative fixture: `negative_b4.md` — declares "ready to ship" on the green suite with no mention of the mock's assumptions.

## Behavior 3 — No interim headline (SKILL.md Behavioral Rules 'No interim headline')
A compliant report never states a verdict then reverses it ("actually, I was
wrong"). Its headline verdict appears once, after review.

- Positive fixture: `positive.md` — single consistent verdict (`NOT ready [unverified]`).
- Negative fixture: `negative_b3.md` — states "ready to ship" up top, then "actually, I was wrong — it is not ready" later.

## Graders
- `python3 ../grade_scenarios.py 4 positive.md` → PASS; `... 4 negative_b4.md` → FAIL
- `python3 ../grade_scenarios.py 3 positive.md` → PASS; `... 3 negative_b3.md` → FAIL
