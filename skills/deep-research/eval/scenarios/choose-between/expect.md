# choose-between — expected behaviors

Exercises behavior **9** (TEXT).

The user frames it as "migrate from Mocha to Jest", but `package.json` shows the
project does not use Mocha at all — the actual incumbent test runner is **ava**
(`"ava": "5.3.1"`, `"test": "ava"`). A compliant report enumerates the real
incumbent (ava) in the candidate set, not just the two options the user named.
The sub-question "does Vitest support native ESM" is a version-scope question:
state the version and check both the pinned version and the latest release.

## Behavior 9 — Candidate space + version scope (SKILL.md Phase 1 + Phase 5)
PASS = Alternatives enumerate the unnamed incumbent (ava) AND the version
sub-question states a version and checks pinned AND latest.

- Positive fixture: `positive.md` — candidate set includes ava (the status quo); Vitest ESM answer states the pinned version in package.json's toolchain and the latest Vitest release.
- Negative fixture: `negative_b9.md` — compares only Mocha vs Jest (the two named options), never mentions ava; answers ESM without version scope.

## Graders
- `python3 ../grade_scenarios.py 9 positive.md --incumbent ava` → PASS
- `python3 ../grade_scenarios.py 9 negative_b9.md --incumbent ava` → FAIL
