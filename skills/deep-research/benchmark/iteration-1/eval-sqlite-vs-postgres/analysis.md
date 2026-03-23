# Comparative Analysis: With-Skill vs Without-Skill Research Output

**Evaluation:** SQLite vs PostgreSQL for Multi-Tenant SaaS (500 concurrent users, 50GB Year-1 data)

---

## 1. Basic Metrics

| Metric | With Skill | Without Skill |
|--------|-----------|---------------|
| Total word count | 4,144 | 1,830 |
| Grading pass rate | 8/8 (100%) | 6/8 (75%) |
| Failed criteria | None | Industry standards by section; Methodology |

---

## 2. Source URLs

### With Skill: 30 unique URLs

**Official documentation (7):**
1. https://sqlite.org/whentouse.html
2. https://sqlite.org/limits.html
3. https://www.sqlite.org/src/doc/begin-concurrent/doc/begin_concurrent.md
4. https://www.postgresql.org/docs/current/mvcc.html
5. https://www.postgresql.org/docs/current/mvcc-intro.html
6. https://www.postgresql.org/docs/current/app-pgbasebackup.html
7. https://www.pgbouncer.org/config.html

**Security & compliance standards (4):**
8. https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html
9. https://owasp.org/www-project-cloud-tenant-isolation/
10. https://www.enterprisedb.com/postgresql-compliance-gdpr-soc-2-data-privacy-security
11. https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final

**Multi-tenancy architecture (5):**
12. https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/
13. https://www.crunchydata.com/blog/row-level-security-for-tenants-in-postgres
14. https://turso.tech/multi-tenancy
15. https://learn.microsoft.com/en-us/azure/azure-sql/database/saas-tenancy-app-design-patterns
16. https://www.bytebase.com/blog/multi-tenant-database-architecture-patterns-explained/

**Benchmarks & performance (5):**
17. https://phiresky.github.io/blog/2020/sqlite-performance-tuning/
18. https://andersmurphy.com/2025/12/02/100000-tps-over-a-billion-rows-the-unreasonable-effectiveness-of-sqlite.html
19. https://blog.skypilot.co/abusing-sqlite-to-handle-concurrency/
20. https://fly.io/blog/sqlite-internals-wal/
21. https://github.com/dev-family/sqlite-bench

**Hosting & pricing (3):**
22. https://aws.amazon.com/rds/postgresql/pricing/
23. https://neon.com/pricing
24. https://www.bytebase.com/blog/postgres-hosting-options-pricing-comparison/

**Production case studies & industry (5):**
25. https://www.sitepoint.com/sqlite-edge-production-readiness-2026/
26. https://dev.to/pockit_tools/the-sqlite-renaissance-why-the-worlds-most-deployed-database-is-taking-over-production-in-2026-3jcc
27. https://www.percona.com/blog/pgbouncer-for-postgresql-how-connection-pooling-solves-enterprise-slowdowns/
28. https://devcenter.heroku.com/articles/postgresql-concurrency
29. https://www.simplyblock.io/blog/underated-postgres-multi-tenancy-with-row-level-security/
30. https://gdpr-info.eu/art-25-gdpr/

### Without Skill: 17 unique URLs

1. https://dev.to/lovestaco/postgresql-vs-sqlite-dive-into-two-very-different-databases-5a90
2. https://medium.com/@dmitry.s.mamonov/database-per-tenant-consider-sqlite-9239113c936c
3. https://sqlite.org/wal.html
4. https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/
5. https://sqlite.org/whentouse.html
6. https://sqlite.org/limits.html
7. https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/
8. https://www.thenile.dev/blog/multi-tenant-rls
9. https://turso.tech/multi-tenancy
10. https://dev.to/pockit_tools/the-sqlite-renaissance-why-the-worlds-most-deployed-database-is-taking-over-production-in-2026-3jcc
11. https://www.pgbouncer.org/config.html
12. https://oneuptime.com/blog/post/2026-01-26-pgbouncer-connection-pooling/view
13. https://www.percona.com/blog/pgbouncer-for-postgresql-how-connection-pooling-solves-enterprise-slowdowns/
14. https://litestream.io/how-it-works/
15. https://www.bytebase.com/blog/postgres-hosting-options-pricing-comparison/
16. https://www.tigerdata.com/blog/database-backups-and-disaster-recovery-in-postgresql-your-questions-answered
17. https://fly.io/blog/sqlite-internals-wal/

**Source quality difference:** The with-skill output has 76% more sources (30 vs 17). Critically, it includes **authoritative standards body sources** (OWASP, NIST, GDPR legislation, PCI-DSS, ISO 27001) that the without-skill output entirely lacks. The without-skill output leans more on blog posts (DEV Community, Medium) and vendor content.

---

## 3. Concrete Quantitative Data Points

### With Skill -- Top 10 (many more present)

1. **SQLite 2,730 write req/sec** on a production Rails app (sequential throughput)
2. **SkyPilot 10-60s busy_timeout** needed at 500x concurrency
3. **PostgreSQL ~5-10MB RAM per connection** (2.5-5GB at 500 connections)
4. **SQLite 281 TB theoretical max** database size
5. **phiresky 100K SELECTs/sec** on multi-GB SQLite with tuning
6. **andersmurphy 100,000 TPS** over a billion rows in SQLite
7. **AWS RDS db.t3.medium ~$58/month**, db.t3.large ~$105/month, Multi-AZ ~$116/month
8. **Hetzner/DigitalOcean VPS ~$24-48/month** for SQLite hosting
9. **Write contention model:** 500 users x 1 write/min / 60 = 8.3 writes/sec, 4.2% utilization; burst of 200 writes = 1000ms queue
10. **Weighted decision matrix total:** PostgreSQL 8.45 vs SQLite 4.60 (84% higher)

### Without Skill -- Top 5

1. **PostgreSQL ~10MB RAM per connection**
2. **PgBouncer maps 500 users to 30-40 actual connections**
3. **~10-second busy timeouts** at 500x write concurrency in SQLite
4. **Turso $29/month** Scaler plan with 10,000 databases
5. **Managed PostgreSQL $15-50/month** entry-level

**Data density difference:** The with-skill output provides roughly 3x as many quantitative data points. It also builds a **write contention model from first principles** (showing assumptions, calculations, and burst scenarios) rather than stating results. The weighted decision matrix with explicit weights and scores is entirely absent from the without-skill output.

---

## 4. Industry Standards Cited with Section Numbers

### With Skill

| Standard | Sections Referenced |
|----------|-------------------|
| OWASP Multi-Tenant Security Cheat Sheet | Tenant isolation at data layer, independent encryption, ABAC over RBAC |
| SOC 2 Type II | Trust Services Criteria |
| GDPR | Art. 25, Art. 32 |
| PCI-DSS v4.0 | Req. 7, 8, 10 |
| NIST SP 800-53 Rev. 5 | AC family, AU family |
| ISO 27001:2022 | A.8.3, A.8.9 |

### Without Skill

**None.** No industry standard is cited by name with section numbers. The output mentions concepts like "Row-Level Security" and "compliance" generically but never ties them to specific regulatory frameworks.

**This is the single largest quality gap between the two outputs.** A database expert reviewing the without-skill output would immediately note the absence of compliance mapping, which is non-negotiable for SaaS serving business customers.

---

## 5. Structural Features

| Feature | With Skill | Without Skill |
|---------|-----------|---------------|
| Comparison tables | 8 tables (concurrency, risk, operations, security, ecosystem, growth, compliance, weighted matrix) | 1 table (feature comparison) + 1 metrics table |
| Confidence level | 92% overall + per-section: 95%, 90%, 85%, 93%, 92%, 80%, 90%, 88% | "High" (qualitative only, in metrics footer) |
| Counterarguments | 3 explicit counterarguments with evidence-for, rebuttal, and verdict | 1 implicit section ("When SQLite Would Be the Right Choice") |
| Methodology section | Yes -- Phase 1 "Research Decomposition" table with 8 sub-questions, evidence types, and sources | No |
| Assumption audit | Yes -- 6 assumptions with risk-if-wrong analysis | No |
| Failure mode analysis | Yes -- 4 scenarios (choose PG + low traffic, choose SQLite + high traffic, need to change from each) | No |
| Alternatives considered | 3 (Turso db-per-tenant, SQLite dev / PG prod, MySQL/MariaDB) with verdicts | Partially -- Section 7 mentions 4 scenarios where SQLite fits |
| Cost analysis | Detailed per-provider pricing tables for both PG and SQLite approaches, with hidden costs enumerated | Brief mentions ($15-50/month PG, $29/month Turso) |
| Growth trajectory | Year-by-year scaling table (Year 1-5) for both paths | Mentioned in prose (Section 8) but no structured projection |
| Conditions for changing recommendation | 4 explicit conditions | None |

---

## 6. Recommendation Quality

### With Skill

- **Specificity:** Names 3 provider options (Neon, Supabase, RDS) with rationale for each. Specifies RLS architecture with `tenant_id` column. Prescribes PgBouncer in transaction mode.
- **Conditions:** 4 explicit conditions under which the recommendation changes (read-only workload, data sovereignty, latency requirements, extreme budget constraint).
- **Growth milestones:** Year 1, 2, 3+ with specific actions and cost projections.
- **Caveats:** 8% uncertainty decomposed into two factors (read-heavy workload possibility, edge SQLite ecosystem maturation).
- **Actionable steps:** 4-step "Immediate Setup (Month 0-1)" plan.

### Without Skill

- **Specificity:** Names providers (Supabase, Neon, DigitalOcean) and prescribes RLS + PgBouncer. 5 numbered action items.
- **Conditions:** Section 7 lists when SQLite is appropriate, but no conditions that would change the primary recommendation.
- **Growth milestones:** Mentioned briefly in prose (read replicas, Citus) without timeline.
- **Caveats:** "High confidence" stated but no decomposition of uncertainty.
- **Actionable steps:** 5-step final recommendation (slightly more granular on monitoring).

Both recommendations are directionally correct and actionable. The with-skill version is materially richer in conditionality and planning horizon.

---

## 7. Verdict: Cross-Examination Survivability

### Which output better survives cross-examination by a database expert?

**The with-skill output, by a significant margin.**

A database expert cross-examining the without-skill output could challenge it on:

1. **"What compliance frameworks does this satisfy?"** -- The without-skill output has no answer. No OWASP, SOC 2, GDPR, PCI-DSS, or NIST citations. A SaaS selling to businesses will face this question from customers' security teams.

2. **"Show me the math on write contention."** -- The without-skill output asserts "10-second busy timeouts" but does not model the workload. The with-skill output builds a model from assumptions (1 write/user/min, 5ms per write, burst scenarios) and shows the arithmetic.

3. **"What if I told you SQLite handles this fine? Expensify processes $10B on SQLite."** -- The without-skill output concedes some SQLite use cases but does not engage with specific counterarguments. The with-skill output addresses this exact argument (Counterargument 2), acknowledges the evidence, and rebuts with operational complexity analysis.

4. **"What are your assumptions?"** -- The without-skill output has no assumption audit. The with-skill output lists 6 assumptions with risk-if-wrong analysis.

5. **"What happens if you're wrong?"** -- The without-skill output has no failure mode analysis. The with-skill output analyzes 4 failure scenarios and identifies the asymmetric risk (choosing SQLite + high traffic = much worse than choosing PostgreSQL + low traffic).

### What specific things does the with-skill version do that the baseline does not?

1. **Research decomposition** -- Explicitly breaks the question into 8 sub-questions with evidence types needed before starting research. This is a methodology disclosure that makes the analysis auditable.

2. **Per-section confidence levels** -- 8 calibrated percentages (80-95%) instead of a single "High." This lets the reader know where the analysis is strongest (concurrency at 95%) and weakest (TCO at 80%).

3. **Compliance mapping table** -- 6 standards with specific sections mapped to both databases' capabilities. This alone could save a team weeks of compliance research.

4. **Quantitative write contention model** -- First-principles calculation with explicit assumptions, average vs burst analysis, and the key insight that "SaaS must be designed for peak, not average."

5. **Weighted decision matrix** -- 8 dimensions with explicit weights summing to 1.0, scores for each, and a quantified result (PostgreSQL 84% higher). This makes value judgments transparent and debatable.

6. **Adversarial review with structured counterarguments** -- 3 steel-manned counterarguments with "evidence for," "rebuttal," and "conclusion" (noting whether each weakens the recommendation).

7. **Assumption audit** -- 6 assumptions with "risk if wrong" analysis.

8. **Failure mode analysis** -- Asymmetric risk identification.

9. **Conditions for changing recommendation** -- 4 explicit conditions with thresholds.

10. **Detailed TCO comparison** -- Per-provider pricing tables for both PostgreSQL and SQLite approaches, including hidden costs.

### What (if anything) does the baseline do better?

1. **Conciseness** -- At 1,830 words vs 4,144, the baseline is easier to scan for a time-pressed reader who just wants the answer. The recommendation section is tight and immediately actionable.

2. **Feature comparison table** -- The baseline's single feature comparison table (Section 6) is clean and covers practical SaaS features (LISTEN/NOTIFY, stored procedures, partial indexes) that the with-skill output does not tabulate in one place.

3. **Metrics footer** -- The baseline includes an effort/impact/confidence/risk/complexity/reversibility/maintainability/expandability assessment table, which is a useful executive summary format (though this appears to be a user-configured output format rather than a research quality indicator).

4. **LiteFS discontinuation** -- The baseline directly links to the Fly.io blog post announcing LiteFS discontinuation. The with-skill output mentions the sunset but its SitePoint link is a secondary source.

---

## 8. Summary Scorecard

| Dimension | With Skill | Without Skill | Delta |
|-----------|-----------|---------------|-------|
| Word count | 4,144 | 1,830 | +126% |
| Unique source URLs | 30 | 17 | +76% |
| Standards body sources | 6 (OWASP, SOC2, GDPR, PCI-DSS, NIST, ISO) | 0 | -- |
| Quantitative data points | ~20+ | ~5 | +300% |
| Comparison tables | 8 | 2 | +300% |
| Confidence granularity | 9 calibrated percentages | 1 qualitative label | -- |
| Counterarguments | 3 structured | 1 implicit | -- |
| Methodology disclosed | Yes | No | -- |
| Assumption audit | Yes (6 items) | No | -- |
| Failure mode analysis | Yes (4 scenarios) | No | -- |
| Grading pass rate | 100% (8/8) | 75% (6/8) | +25pp |

**Overall verdict:** The with-skill output is substantially more rigorous. It would survive expert cross-examination; the without-skill output would be adequate for an internal decision but vulnerable to challenge on compliance, methodology, and edge cases. The with-skill output's main cost is length -- it demands more reader time -- but for a consequential infrastructure decision, that tradeoff favors thoroughness.
