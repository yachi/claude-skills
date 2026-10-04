#!/usr/bin/env python3
"""Discrimination self-test for grade_v11.py (TEXT: 2,3,4,6,7,9) and
grade_trace.py (TRACE: 1,5,8).

For every v1.1.0 behavior it runs the behavior's grader on a POSITIVE fixture
(must emit `B<n> PASS`) and a NEGATIVE fixture (must emit `B<n> FAIL`). A
behavior is "discriminating" only when both hold. Exit 0 iff every behavior
discriminates. Run:  python3 eval/selftest_v11.py
"""

import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, 'fixtures')

# (behavior, grader, extra args, positive fixture, negative fixture)
CASES = [
    # TRACE — grade_trace.py
    ('B1', 'grade_trace.py', [], 'b1_pos.jsonl', 'b1_neg.jsonl'),
    ('B5', 'grade_trace.py', [], 'b5_pos.jsonl', 'b5_neg.jsonl'),
    ('B8', 'grade_trace.py', [], 'b8_pos.jsonl', 'b8_neg.jsonl'),
    # TEXT — grade_v11.py ; B2 is tested in all four deliverable shapes
    ('B2', 'grade_v11.py', ['--type', 'default'],  'full_report_pos.md', 'b2_default_neg.md'),
    ('B2', 'grade_v11.py', ['--type', 'verify'],   'b2_verify_pos.md',   'b2_verify_neg.md'),
    ('B2', 'grade_v11.py', ['--type', 'diagnose'], 'b2_diagnose_pos.md', 'b2_diagnose_neg.md'),
    ('B2', 'grade_v11.py', ['--type', 'build'],    'b2_build_pos.md',    'b2_build_neg.md'),
    ('B3', 'grade_v11.py', [], 'full_report_pos.md', 'b3_neg.md'),
    ('B4', 'grade_v11.py', [], 'b4_pos.md', 'b4_neg.md'),
    ('B6', 'grade_v11.py', [], 'b6_pos.md', 'b6_neg.md'),
    ('B7', 'grade_v11.py', [], 'full_report_pos.md', 'b7_neg.md'),
    ('B9', 'grade_v11.py', [], 'full_report_pos.md', 'b9_neg.md'),
]

def line_for(behavior, grader, extra, fixture):
    out = subprocess.run(
        [sys.executable, os.path.join(HERE, grader), os.path.join(FIX, fixture)] + extra,
        capture_output=True, text=True).stdout
    for ln in out.splitlines():
        if ln.startswith(behavior + ' '):
            return ln
    return f'{behavior} <no line>'

def main():
    all_ok = True
    label = {'--type default': 'default', '--type verify': 'verify',
             '--type diagnose': 'diagnose', '--type build': 'build'}
    print(f'{"behavior":10} {"shape":9} {"positive->PASS":16} {"negative->FAIL":16} verdict')
    print('-' * 78)
    for behavior, grader, extra, pos, neg in CASES:
        shape = label.get(' '.join(extra), '-')
        pos_line = line_for(behavior, grader, extra, pos)
        neg_line = line_for(behavior, grader, extra, neg)
        pos_ok = pos_line.startswith(f'{behavior} PASS')
        neg_ok = neg_line.startswith(f'{behavior} FAIL')
        ok = pos_ok and neg_ok
        all_ok &= ok
        print(f'{behavior:10} {shape:9} {"PASS" if pos_ok else "**"+pos_line.split("—")[0].strip():16} '
              f'{"FAIL" if neg_ok else "**"+neg_line.split("—")[0].strip():16} '
              f'{"DISCRIMINATES" if ok else "NOT DISCRIMINATING"}')
    print('-' * 78)
    covered = sorted({c[0] for c in CASES})
    print(f'behaviors covered: {", ".join(covered)}  ({len(covered)} of 9)')
    print('RESULT:', 'ALL BEHAVIORS DISCRIMINATE' if all_ok else 'FAILURE — see ** rows')
    sys.exit(0 if all_ok else 1)

if __name__ == '__main__':
    main()
