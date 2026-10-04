#!/usr/bin/env python3
"""Golden regression: assert all 9 v1.1.0 behaviors PASS on REAL /dr outputs.

These golden fixtures are actual deep-research runs on the eval/scenarios prompts
(captured 2026-10-04, skill v1.1.0), not hand-authored — so a grader change that
breaks on real report/transcript language is caught here, and the golden data is an
external oracle (never regenerate it from the graders). Exit non-zero on any FAIL.
"""
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
EVAL = os.path.dirname(HERE)
sys.path.insert(0, EVAL)
import grade_v11 as V          # type: ignore  # noqa: E402
import grade_trace as T        # type: ignore  # noqa: E402

R = os.path.join(HERE, "reports")
TR = os.path.join(HERE, "traces")

# (behavior, scenario, surface, path, grader)
CASES = [
    (1, "first-party-answer", "trace", f"{TR}/first-party-answer.jsonl", lambda p: T.b1_first_party_first(T._events(p))),
    (8, "first-party-answer", "trace", f"{TR}/first-party-answer.jsonl", lambda p: T.b8_durable_output(T._events(p))),
    (5, "intent-mismatch",    "trace", f"{TR}/intent-mismatch.jsonl",    lambda p: T.b5_intent_check(T._events(p))),
    (9, "choose-between",     "text",  f"{R}/choose-between.md",          lambda p: V.b9_candidate_version(open(p).read(), "both")),
    (6, "defensive-security", "text",  f"{R}/defensive-security.md",      lambda p: V.b6_defensive_security(open(p).read())),
    (7, "gaps",               "text",  f"{R}/gaps.md",                    lambda p: V.b7_gap_ledger(open(p).read())),
    (2, "gaps",               "text",  f"{R}/gaps.md",                    lambda p: V.b2_deliverable_shape(open(p).read(), "default")),
    (3, "stub-fidelity",      "text",  f"{R}/stub-fidelity.md",           lambda p: V.b3_no_interim_headline(open(p).read())),
    (4, "stub-fidelity",      "text",  f"{R}/stub-fidelity.md",           lambda p: V.b4_model_fidelity(open(p).read())),
]

if __name__ == "__main__":
    failed = 0
    print("behavior  scenario             surface  result")
    for n, scen, surf, path, fn in sorted(CASES):
        ok, detail = fn(path)
        if not ok:
            failed += 1
        print(f"  B{n:<6} {scen:<20} {surf:<7} {'PASS' if ok else 'FAIL'}  {detail[:70]}")
    print("-" * 60)
    print(f"{'ALL 9 BEHAVIORS PASS ON REAL OUTPUT' if failed == 0 else f'{failed} BEHAVIOR(S) FAILED'}")
    sys.exit(0 if failed == 0 else 1)
