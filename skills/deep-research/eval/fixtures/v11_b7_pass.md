# Research: should we adopt gRPC for the internal service mesh?

## Adversarial Review

### Gap Ledger

| Gap | Class | Action | Status |
|-----|-------|--------|--------|
| p99 latency vs REST unmeasured | closable-by-tool | ran local ghz benchmark | closed |
| Team gRPC experience unknown | needs-user-input | asked staffing lead | open |
| Future HTTP/3 mesh support | open-in-world | no vendor commitment yet | open |

**Termination:** 0 gaps = zero *closable-by-tool* gaps remain open after 2
refinement rounds. The two still-open gaps are needs-user-input and
open-in-world, which no tool can close, so we stopped after 2 rounds.
