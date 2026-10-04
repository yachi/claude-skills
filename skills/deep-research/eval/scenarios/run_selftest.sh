#!/usr/bin/env bash
# Discrimination self-test: every covered behavior's POSITIVE fixture must PASS
# and NEGATIVE fixture must FAIL. Exits non-zero if any pair fails to discriminate.
set -u
cd "$(dirname "$0")"
G="python3 grade_scenarios.py"
fail=0

# check <behavior> <expect: pass|fail> <file> [--incumbent NAME...]
check() {
  local beh="$1" want="$2" file="$3"; shift 3
  local out rc
  out=$($G "$beh" "$file" "$@" 2>&1); rc=$?
  local got="pass"; [ $rc -ne 0 ] && got="fail"
  if [ "$got" = "$want" ]; then
    echo "  OK   [b$beh want=$want] $out"
  else
    echo "  XXXX [b$beh want=$want got=$got] $out"; fail=1
  fi
}

echo "== first-party-answer (b1 TRACE, b8 TRACE) =="
check 1 pass first-party-answer/positive.jsonl
check 1 fail first-party-answer/negative_b1.jsonl
check 8 pass first-party-answer/positive.jsonl
check 8 fail first-party-answer/negative_b8.jsonl

echo "== stub-fidelity (b4 TEXT, b3 TEXT) =="
check 4 pass stub-fidelity/positive.md
check 4 fail stub-fidelity/negative_b4.md
check 3 pass stub-fidelity/positive.md
check 3 fail stub-fidelity/negative_b3.md

echo "== intent-mismatch (b5 TRACE+TEXT) =="
check 5 pass intent-mismatch/positive.md
check 5 pass intent-mismatch/positive.jsonl
check 5 fail intent-mismatch/negative_b5.md

echo "== defensive-security (b6 TEXT) =="
check 6 pass defensive-security/positive.md
check 6 fail defensive-security/negative_b6.md

echo "== choose-between (b9 TEXT) =="
check 9 pass choose-between/positive.md --incumbent ava
check 9 fail choose-between/negative_b9.md --incumbent ava

echo "== gaps (b7 TEXT, b2 TEXT) =="
check 7 pass gaps/positive.md
check 7 fail gaps/negative_b7.md
check 2 pass gaps/positive.md
check 2 fail gaps/negative_b2.md

echo "------------------------------------------------------"
if [ $fail -eq 0 ]; then echo "ALL DISCRIMINATE: PASS"; else echo "DISCRIMINATION FAILURE"; fi
exit $fail
