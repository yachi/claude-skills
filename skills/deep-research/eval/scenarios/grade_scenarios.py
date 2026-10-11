#!/usr/bin/env python3
"""Scenario dispatcher for the 9 deep-research v1.1.0 behaviors.

ONE source of truth per behavior: this dispatches to the two authoritative graders
rather than re-implementing their logic (an earlier copy drifted and misgraded real
transcripts). TEXT behaviors (2,3,4,6,7,9) -> grade_v11.py on the report .md.
TRACE behaviors (1,5,8) -> grade_trace.py on the agent transcript (.jsonl/.output).

Usage: grade_scenarios.py <behavior 1-9> <path> [--incumbent NAME] [--type T] [--b9-mode M]
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # eval/
import grade_v11 as V            # noqa: E402
import grade_trace as T          # noqa: E402

TRACE = {1, 5, 8}


def run(n, path, dtype="default", b9_mode="both"):
    if n in TRACE:
        events = T._events(path)
        fn = {1: T.b1_first_party_first, 5: T.b5_intent_check, 8: T.b8_durable_output}[n]
        return fn(events)
    text = open(path).read()
    if n == 2:
        return V.b2_deliverable_shape(text, dtype)
    if n == 3:
        return V.b3_no_interim_headline(text)
    if n == 4:
        return V.b4_model_fidelity(text)
    if n == 6:
        return V.b6_defensive_security(text)
    if n == 7:
        return V.b7_gap_ledger(text)
    if n == 9:
        return V.b9_candidate_version(text, b9_mode)
    raise SystemExit(f"unknown behavior {n}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: grade_scenarios.py <behavior 1-9> <path> [--incumbent NAME] [--type T] [--b9-mode M]")
        sys.exit(2)
    n = int(sys.argv[1])
    target = sys.argv[2]
    dtype = "default"
    b9_mode = "both"
    argv = sys.argv[3:]
    for i, a in enumerate(argv):
        if a == "--type" and i + 1 < len(argv):
            dtype = argv[i + 1]
        elif a == "--b9-mode" and i + 1 < len(argv):
            b9_mode = argv[i + 1]
        # --incumbent accepted for back-compat; b9 no longer needs a name
    ok, detail = run(n, target, dtype=dtype, b9_mode=b9_mode)
    print(f"{'PASS' if ok else 'FAIL'} b{n} — {detail}  ({target})")
    sys.exit(0 if ok else 1)
