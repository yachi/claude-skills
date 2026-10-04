# Roadmap — claude-skills

## deep-research skill

### P1 — Scenario eval tier for project-context behaviors (open)
The v1.1.0 revision (commit 57dd3da) added 9 behavioral rules, 7 of which only fire inside a live project (repo, logs, device, artifact). `eval/grade.py` and `autoresearch/` test only synthetic standalone-report prompts, so these 9 behaviors have **zero** eval coverage. The A/B that gated the commit (old 21/34, new 25/34) proved no regression on the old suite only — it did not verify any new behavior.

Build:
- **Fixtures**: a throwaway repo + fake time-series/logs (for first-party-first + snapshot-is-not-history), a verify-claims task set (for deliverable-shape + per-claim verdict blocks), a regression-with-healthy-peer dataset (for the Phase 1.5 regression drill), a stub-vs-real probe (for model-fidelity).
- **Graders**: structural/LLM-judge checks for — first-party evidence consulted before web search; deliverable shape matches type; no interim headline before Phase 5/7; gap ledger present with termination; version scope (pinned + latest); defensive-security framing (no crack-time/keyspace code); durable output path; no dead sources cited.
- **Wire into `autoresearch/program.md`**: add project-context prompts to the rotation so the champion loop can reward/regress the new rules.
- **Cheaper partial (do first)**: add report-text graders to `grade.py` for the patterns visible in output text — gap-ledger table, version scope, scope-of-benchmarking, dead-source — before the full fixture harness.

### P2 — GitHub repo settings
Tiers 1-2 done; only P7 (social preview) remains, low ROI. (See project memory.)
