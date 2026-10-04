# Diagnosis: checkout p99 latency regression

Deliverable type: **diagnose** — transition timeline, ranked hypotheses, next test.

## Transition timeline
- 2026-09-30 14:00 — p99 steady at 45ms (30-day baseline).
- 2026-09-30 14:12 — p99 jumped to 310ms within one sample window; the hour it
  changed. A healthy peer service (`payments`) did NOT regress in the same hour.
- 2026-09-30 14:10 — deploy `checkout@3.4.0` rolled out (change log correlates).

## Ranked hypotheses
1. **Hypothesis 1 (most likely, 70%):** `checkout@3.4.0` added a synchronous
   call to the tax service inside the request path — timeline aligns to the deploy.
2. **Hypothesis 2 (20%):** connection-pool contention from a new N+1 query.
3. **Hypothesis 3 (10%):** downstream tax-service degradation independent of us
   — weakened because the peer sharing that dependency did not regress.

## Next decisive test
Roll `checkout` back to 3.3.9 on one canary pod and compare p99 for 10 minutes;
if it returns to 45ms, Hypothesis 1 is confirmed. Confidence: 75%.
