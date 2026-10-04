# Is the terraform migration fix ready to ship? — Deep Research Verdict

**Deliverable type:** verify-claims (live project, verdict requested).

## Executive Summary

**NO — not ready to ship. Confidence: 95%.** The three green tests prove only
that the Python wrapper parses a *canned success string*. They exercise **zero**
real terraform behavior: an `autouse` fixture monkeypatches `subprocess.run` so
`terraform apply` **always** returns exit 0 with hard-coded stdout. Every
failure, nonzero-exit, and rollback path the question cares about is unverified.
Under Phase 7 Model-fidelity, a green suite over unverified stubs is
`[unverified]`, not convergence.

## Per-Claim Verdicts

| Claim (implied by "ready to ship") | Verdict | Evidence |
|---|---|---|
| Tests pass green locally | UNVERIFIABLE here | `deploy.py` is absent in the dir, so `from deploy import run_migration` raises `ModuleNotFoundError` — the suite cannot even import/run as shipped. (`python3 -c "import deploy"` → ModuleNotFoundError) |
| Tests prove `apply` success handling | REFUTED (as proof of readiness) | `mock_terraform` returns `FakeCompleted(0, "Apply complete! 3 added, 0 changed.")` for every `apply`. Success is asserted against a string the test itself wrote. |
| Tests prove failure is handled | REFUTED | No test induces a nonzero exit. Mock never returns nonzero for `apply`. The wrapper's error branch is never entered. |
| `test_migration_rolls_back_on_error` proves rollback | REFUTED | Its body calls the same happy path and asserts `result.ok is True`. It creates no error and asserts no rollback. The name is contradicted by the body (comment even admits it). |
| Safe for production | REFUTED | Readiness depends on real-terraform behavior that the harness is explicitly built to bypass ("never shells out to real terraform"). |

## Model-Fidelity Check (Phase 7) — the decisive gap

The harness encodes assumptions about real terraform. I verified each against
the installed real tool (**Terraform v1.5.7**, `/opt/homebrew/bin/terraform`):

| Stub assumption | Real terraform (probed) | Fidelity |
|---|---|---|
| `apply` returncode is always `0` | Provisioner failure → **`apply exit=1`** (probe: `null_resource` with `local-exec "exit 1"`) | **BROKEN** — nonzero never modeled |
| Error path is reachable in tests | Mock short-circuits all errors to 0 | **BROKEN** — error branch dead-tested |
| Failure implies clean "rollback" | Terraform has **no transactional rollback**; a failed apply leaves partially-created resources + dirty state, resource tainted | **BROKEN & dangerous** — the rollback the test name promises does not exist in the tool |
| stdout format `"...3 added..."` | Real format varies (wrapping, color codes, counts) | Unverified — parser tested against one literal |

Probe (reproducible):
```bash
cd "$(mktemp -d)"
printf 'resource "null_resource" "x" {\n  provisioner "local-exec" { command = "exit 1" }\n}\n' > main.tf
terraform init -input=false >/dev/null 2>&1
terraform apply -auto-approve -input=false; echo "apply exit=$?"   # -> apply exit=1
```

## Recommendation

Do **not** ship on this evidence. Before a ship verdict is possible:

1. Add an **integration test** that runs real terraform against a throwaway
   local backend / `null_resource` fixture (the probe above is a starting
   point) — assert the wrapper's behavior on a genuine `exit 1`.
2. Add a **mutation test**: make the mock return `FakeCompleted(1, ...)` for
   `apply` and confirm at least one test *fails*. Today all three stay green —
   proof the suite is decorative w.r.t. failure handling.
3. Settle the rollback semantics: terraform does not auto-rollback. Decide what
   `run_migration` does on partial apply (targeted destroy? state surgery?
   alert?) and test *that*, not a canned success.
4. Restore/commit `deploy.py` so the suite can actually run in CI.

**Sensitivity:** If `run_migration` is only ever expected to parse an
already-succeeded apply and never to own failure/rollback, the happy-path tests
are adequate for *that* narrow contract — but then the `rolls_back_on_error`
test is a false promise and must be removed or renamed. Either way, current
state is not shippable.

## Scope

Covers only test↔tool fidelity and the shippability question. Does not review
the (absent) `deploy.py` wrapper logic, terraform HCL correctness, or
CI/secrets config.

## Sources

**First-party / primary (this session):**
- `test_deploy.py` — monkeypatch fixture, three asserts (read).
- Real-tool probe — Terraform v1.5.7, `apply exit=1` on provisioner failure.
- `python3 -c "import deploy"` → `ModuleNotFoundError` (deploy.py absent).

**Tool behavior:** Terraform CLI exit codes — nonzero on apply error; no
automatic rollback of partially-applied resources (HashiCorp terraform docs,
corroborated by the local v1.5.7 probe above).
