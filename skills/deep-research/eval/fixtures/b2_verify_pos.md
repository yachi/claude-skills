# Verify: claims about our Postgres connection-pool config

Deliverable type: **verify** — per-claim verdict block.

| Claim | Verdict | Strongest source (URL + date) | What would change it |
|-------|---------|-------------------------------|----------------------|
| `max_connections=100` is set in prod | CONFIRMED | repo `postgresql.conf` line 64, read 2026-10-04 | a later override in `conf.d/` |
| PgBouncer runs in transaction mode | CONFIRMED | `pgbouncer.ini` `pool_mode=transaction`, 2026-10-04 | a deploy changing the ini |
| The pool never exhausts under load | PARTIAL | Grafana `pg_stat_activity` 30-day series shows 2 spikes to 98/100 | a longer window or a load test |
| Idle-in-transaction leaks exist | REFUTED | `idle_in_transaction_session_timeout=30s` set; 0 events in log | removing the timeout |
| The 2026-09 outage was pool exhaustion | UNVERIFIABLE | incident log lacks connection metrics for that hour | recovering the metrics backfill |

Confidence in the CONFIRMED verdicts: 90%. Scope: this verifies configuration
and 30-day behavior only; it does not predict behavior under a 10x traffic event.
