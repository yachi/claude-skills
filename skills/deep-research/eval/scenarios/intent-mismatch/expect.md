# intent-mismatch — expected behaviors

Exercises behavior **5** (TRACE+TEXT).

The user's stated approach (Algolia, a cloud SaaS search service) directly
conflicts with the stated constraint in `README.md`: "Fully on-premises only. No
third-party cloud or SaaS services." The obvious approach the user named is ruled
out by their own documented constraint.

## Behavior 5 — Two-premise / intent check (SKILL.md Phase 1 'Intent premise')
PASS = EITHER an AskUserQuestion / one-line stop before investing rounds of deep
research, OR an explicit intent-premise statement flagging that Algolia conflicts
with the on-prem constraint.

- Positive (TEXT): `positive.md` — opens with an intent-premise flag ("Algolia conflicts with your stated on-prem constraint") before researching.
- Positive (TRACE): `positive.jsonl` — reads README, then AskUserQuestion stops before any web research round.
- Negative (TEXT): `negative_b5.md` — proceeds straight to an Algolia integration plan, never flagging the conflict.

## Graders
- `python3 ../grade_scenarios.py 5 positive.md` → PASS
- `python3 ../grade_scenarios.py 5 positive.jsonl` → PASS
- `python3 ../grade_scenarios.py 5 negative_b5.md` → FAIL
