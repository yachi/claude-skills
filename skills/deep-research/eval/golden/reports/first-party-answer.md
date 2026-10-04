# checkout-service 503s under load — Root Cause & Fix

**Deliverable:** diagnosis of a live service. Evidence is first-party: the service's own
`config.yaml` and `app.log` (503 burst, 2026-10-03T14:22Z). No web needed — the records answer it.

## Executive summary (confidence: 95%)

The 503s are **DB connection-pool exhaustion**, not a payments outage. Each `/checkout`
holds one of only **5** DB connections for the **entire ~8s payments upstream call**, while
up to **64 worker threads** accept requests concurrently. Once all 5 connections are in use,
the other ~59 in-flight requests wait on the pool, hit the **2000 ms** `acquire_timeout_ms`,
and are returned as `503 db_pool_acquire_timeout`. It is intermittent because it only fires
when concurrent in-flight checkouts exceed 5 for longer than 2s — i.e. under load.

**One line:** 64 worker threads contend for a 5-connection DB pool while each request pins a
connection across an ~8s payments call, so waiters exceed the 2s acquire timeout and get 503s.

## Evidence (from app.log / config.yaml)

| Signal | Value | Source |
|---|---|---|
| Worker threads (max in-flight) | 64 | config.yaml `concurrency.worker_threads` |
| DB pool ceiling | 5 | config.yaml `database.pool.max_connections` |
| Pool acquire timeout | 2000 ms | config.yaml `database.pool.acquire_timeout_ms` |
| Payments call timeout | 8000 ms | config.yaml `upstream.payments.timeout_ms` |
| Connection hold time (observed) | 8100 ms | app.log L15 `db.pool released ... held_ms=8100` |
| Pool exhausted, waiters queued | in_use=5, waiters=59 | app.log L9 `db.pool exhausted max=5 ... waiters=59` |
| 503 reason | `db_pool_acquire_timeout` | app.log L10–L13 |

**Transition timeline (the 503 burst):**
- `14:22:01–02` — conns 1→5 acquired (a1…a5); request a1 enters the payments call.
- `14:22:02` — pool exhausted: `in_use=5, waiters=59`.
- `14:22:04` (+2s) — a6, a7 hit the 2s acquire timeout → `status=503`.
- `14:22:10` — a1's payments call returns after `duration_ms=7980`; connection released
  after `held_ms=8100`; a8 immediately acquires the freed slot.

The connection is held for the whole payments round-trip (acquire at request start,
release only after the 8s upstream response). That is the mechanism.

## Why it's intermittent (quantified)

With a connection pinned for the full ~8s request, steady-state throughput is bounded by
`pool_size / hold_time = 5 / 8.1s ≈ 0.62 checkout/s`. Any arrival rate above that grows the
waiter queue; a waiter older than 2s becomes a 503. Below ~0.6 req/s the pool rarely
saturates and no 503s appear — hence "intermittent under load."

## Root cause

Two compounding design faults, not a payments fault:
1. **Connection held across an external call.** A DB connection is acquired for the request's
   full lifetime, including the ~8s payments HTTP call during which the connection does no DB
   work — it is idle but reserved. This is the primary fault.
2. **Gross concurrency/pool mismatch.** 64 accepted-concurrent requests against a 5-connection
   pool guarantees 59 waiters the instant load arrives.

## Fix

**Primary (root cause) — stop holding the connection across the payments call.** Restructure
`/checkout` to: acquire conn → do pre-payment DB work → **release** → call payments →
**re-acquire** → do post-payment DB work → release. The connection is only held during actual
DB work (tens of ms), collapsing hold time from ~8s to near-zero and removing the bottleneck.
This is the real fix; the knobs below are mitigations.

**Mitigations (deploy now, cheap):**
- **Raise `max_connections`** toward the real concurrency. To sustain 64 in-flight requests
  each holding a conn ~8s you need ~64 connections — verify Postgres `max_connections` and any
  PgBouncer limits can take it (guard the DB, don't just move the exhaustion downstream).
- **Cap `worker_threads` to the pool size** (e.g. 5–10) so load sheds as backpressure/queueing
  rather than as a 5:64 thundering herd. Lower ceiling + bounded queue beats 59 instant 503s.
- **Trim `upstream.payments.timeout_ms`** (8s is very long for a sync checkout path) and add a
  retry/circuit-breaker so a slow payments provider can't pin the pool.

**Recommended sequence:** (1) ship the config mitigation now — raise pool to match concurrency
(validated against DB limits) and/or lower worker_threads — to stop the bleeding; (2) land the
connection-release refactor to fix it structurally; (3) add a pool-saturation alert
(`db.pool exhausted` / waiters > 0) so this is caught before users see 503s.

## Decisive verification

Reproduce under load and watch `db.pool exhausted` + `held_ms`. After the refactor,
`held_ms` per request should drop from ~8000 to ≤~100 and `waiters` should stay ~0 at the same
arrival rate. If raising the pool instead, confirm Postgres accepts the new connection count
(`SHOW max_connections;`) before rollout.

## Scope / caveats

- Single 19-line log window (one burst) and one config file; no metrics history or DB-side
  stats were available. The mechanism is unambiguous from this window, but the *sustained*
  arrival rate and the DB's own connection ceiling are not in these files — verify both before
  sizing the pool.
- Assumes the log's own root-cause annotation (L17–L19) reflects the real code path; the
  acquire→payments→release ordering is inferred from the timestamps and `held_ms`, which is
  consistent with holding the connection across the upstream call.
