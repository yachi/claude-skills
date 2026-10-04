# Does our deploy gate correctly block on a failing smoke test?

## Key Findings

1. The smoke-test gate passes 42/42 in CI. However, those tests run against a
   **mock** of the `deployctl` binary, not the real tool.

## Model-fidelity check

The test harness replaces `deployctl` with a stub. That stub encodes three
assumptions about the real tool:
- **Exit codes:** the stub returns 0 on success and 1 on failure. Verified
  against the real tool via a one-line probe (`deployctl --version; echo $?`)
  which confirmed exit 0, and the man page documents exit 1 on any failed
  health check.
- **Sync vs async:** the stub blocks until completion; the real `deployctl`
  also blocks (confirmed against the real tool in a container).
- **Error propagation on partial rollout:** the stub assumes a partial failure
  returns 1. This is NOT confirmed against the real tool — the 8 tests that
  depend on partial-rollout behavior are therefore `[unverified]` until probed
  against a staging deploy.

So 34/42 tests are trustworthy; the 8 partial-rollout tests are `[unverified]`,
not convergence. Confidence in the gate: 70%.
