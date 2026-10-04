#!/usr/bin/env bash
# Authoritative self-test for the 9 v1.1.0 behavior graders.
#   1. selftest_v11.py  — graders DISCRIMINATE (positive fixtures pass, negatives fail)
#   2. golden/scorecard.py — all 9 behaviors PASS on REAL captured /dr output
# grade_v11.py (TEXT) and grade_trace.py (TRACE) are the single source of truth;
# scenarios/grade_scenarios.py dispatches to them.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
EVAL="$(dirname "$HERE")"

echo "== discrimination =="
python3 "$EVAL/selftest_v11.py"
echo
echo "== golden regression (real /dr output) =="
python3 "$EVAL/golden/scorecard.py"
