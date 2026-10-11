# Is the terraform migration fix ready to ship?

## Verdict

**NOT ready to ship `[unverified]`.** Confidence 80%. The three green tests do
not exercise real terraform, so "all green" is not evidence that the migration
applies in production.

## Model-fidelity check

`test_deploy.py` uses a pytest fixture (`mock_terraform`) that **monkeypatches
`subprocess.run`** with a `FakeCompleted` stub. The stub encodes assumptions
about the real external CLI that the suite never validates:

| Stub assumption | What it hard-codes | Real-world risk if wrong |
|---|---|---|
| `terraform apply` exit code | always `0` (hard-coded `returncode=0`) | real apply can exit non-zero on provider errors, lock contention, drift |
| apply stdout | canned `"Apply complete! 3 added"` | real output varies; parsing may break |
| error / rollback path | also returns the mock's `ok=True` | the rollback branch is never actually taken |
| sync execution | `subprocess.run` returns immediately | real apply is long-running; timeouts untested |

Because every passing assertion rides on these unverified stubs, the ship
verdict over this suite is `[unverified]`. To convert it, run the suite against
real terraform in a sandbox (`terraform apply` on a throwaway workspace, one-line
probe of the actual exit code) before counting the green run as evidence.

## What would change the verdict

Re-run with real terraform (or at least a recorded real exit code) and confirm
the rollback path triggers on a genuine non-zero exit. If that passes, the
verdict moves to CONFIRMED.
