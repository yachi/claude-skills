# Should I Use SQLite or PostgreSQL for a Multi-Tenant SaaS App (500 Concurrent Users, 50GB Year-1 Data)?

## Executive Summary

**Use PostgreSQL.** For a multi-tenant SaaS application expecting 500 concurrent users and 50GB of data within the first year, PostgreSQL is the clear choice. SQLite's single-writer architecture creates a fundamental bottleneck at 500 concurrent users with any meaningful write workload, its lack of built-in authentication/authorization makes multi-tenant security fragile, and it lacks native row-level security, replication, and compliance tooling that SaaS applications require. PostgreSQL handles all of these natively. The only scenario where SQLite would be viable is a database-per-tenant architecture on an edge platform (e.g., Turso/D1) with a predominantly read-heavy workload -- but even then, the operational complexity and ecosystem immaturity add risk that PostgreSQL avoids entirely.

**Overall confidence: 92%**

---

## Research Decomposition (Phase 1)

| Sub-Question | Evidence Type Required | Primary Sources |
|---|---|---|
| 1. Concurrency at 500 users | Benchmarks, architecture docs | SQLite official docs, PostgreSQL MVCC docs, production case studies |
| 2. Multi-tenancy patterns | Architecture patterns, security frameworks | OWASP, AWS best practices, Turso docs |
| 3. Performance at 50GB scale | Benchmarks, implementation limits | SQLite limits page, PostgreSQL docs, phiresky benchmarks |
| 4. Operational characteristics | Official docs, operational guides | Backup/replication docs, HA guides |
| 5. Security & compliance | Standards bodies, official docs | OWASP, NIST, SOC2/GDPR frameworks |
| 6. Total cost of ownership | Cloud pricing, hosting benchmarks | AWS RDS pricing, Neon/Supabase pricing, Turso pricing |
| 7. Ecosystem & tooling | Package registries, framework docs | ORM docs, migration tool docs |
| 8. Growth trajectory | Scaling case studies, architecture limits | Production case studies, official limits |

---

## Key Findings

### 1. Concurrency: PostgreSQL Wins Decisively (Confidence: 95%)

**SQLite Architecture:**
- Single-writer model: only one write transaction can execute at any instant. All other writers queue behind a database-level lock.
- In WAL mode, concurrent readers are not blocked by writes, but **all writes are serialized**.
- SkyPilot encountered severe write contention at 500x concurrency, requiring busy_timeout values of 10-60 seconds to avoid "database is locked" errors. ([SkyPilot Blog](https://blog.skypilot.co/abusing-sqlite-to-handle-concurrency/))
- A production Rails app achieved ~2,730 write requests/second on SQLite -- but this is sequential throughput, not concurrent. Under 500 simultaneous write attempts, queueing latency dominates.
- The experimental `BEGIN CONCURRENT` feature (not yet in mainline SQLite) would allow partial write overlap, but conflict detection is at the **page level**, not row level, causing spurious aborts. ([SQLite BEGIN CONCURRENT docs](https://www.sqlite.org/src/doc/begin-concurrent/doc/begin_concurrent.md))

**PostgreSQL Architecture:**
- MVCC (Multi-Version Concurrency Control): readers never block writers, writers never block readers, and multiple writers operate concurrently with row-level conflict detection. ([PostgreSQL Concurrency Docs](https://www.postgresql.org/docs/current/mvcc.html))
- Each connection spawns a process consuming ~5-10MB RAM. At 500 connections, that is 2.5-5GB RAM -- manageable with connection pooling.
- PgBouncer in transaction mode can multiplex 500 application connections over 50-100 actual PostgreSQL connections, drastically reducing resource usage. ([PgBouncer Config](https://www.pgbouncer.org/config.html))
- PostgreSQL natively supports all four SQL isolation levels (READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE).

**Quantitative Comparison:**

| Metric | SQLite (WAL mode) | PostgreSQL (MVCC) |
|---|---|---|
| Concurrent readers | Unlimited | Unlimited |
| Concurrent writers | **1** (database-level lock) | **Hundreds+** (row-level locking) |
| Write latency under 500 concurrent writes | 10-60s busy_timeout needed | Milliseconds (normal row-level contention) |
| Isolation levels | SERIALIZABLE only (effective) | READ COMMITTED (default), all 4 supported |
| Connection overhead | Zero (embedded, in-process) | ~5-10MB per connection |
| Connection pooling needed? | No | Yes (PgBouncer recommended at 500+) |

### 2. Multi-Tenancy: PostgreSQL Has Native Support (Confidence: 90%)

**PostgreSQL Multi-Tenancy Patterns:**

Three established patterns, all production-proven:

1. **Shared database + Row-Level Security (RLS)**: Single database, `tenant_id` column on every table, PostgreSQL RLS policies enforce isolation at the database engine level. This is the most common pattern for SaaS. ([AWS Blog: Multi-tenant RLS](https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/))
2. **Schema-per-tenant**: Each tenant gets a separate PostgreSQL schema within the same database. Good isolation with moderate overhead.
3. **Database-per-tenant**: Complete isolation. Higher operational overhead but simplest security model.

PostgreSQL's RLS is battle-tested: policies are enforced at the engine level regardless of query origin, preventing tenant data leakage even from application bugs. ([Crunchy Data: RLS for Tenants](https://www.crunchydata.com/blog/row-level-security-for-tenants-in-postgres))

**SQLite Multi-Tenancy Patterns:**

1. **Database-per-tenant**: The primary viable pattern. Each tenant gets a separate `.db` file. Provides strong isolation but requires application-level routing, per-tenant backup management, and cross-tenant schema migration tooling. ([Turso: Database Per Tenant](https://turso.tech/multi-tenancy))
2. **Shared database with application-level filtering**: No RLS -- the application must add `WHERE tenant_id = ?` to every query. A single missed filter leaks data across tenants.

**Risk Assessment:**

| Risk | SQLite | PostgreSQL |
|---|---|---|
| Tenant data leakage from missed query filter | **HIGH** (no engine-level enforcement) | **LOW** (RLS enforces at engine level) |
| Schema migration across tenants | Complex (N databases) | Simple (1 database, RLS) or moderate (N schemas) |
| Cross-tenant reporting/analytics | Requires ATTACH or application-level aggregation | Native (same database) |
| Per-tenant backup granularity | Excellent (copy file) | Moderate (pg_dump with schema filter) |

### 3. Data Volume at 50GB: Both Capable, PostgreSQL More Comfortable (Confidence: 85%)

**SQLite:**
- Theoretical max: 281 TB (with default page size). 50GB is well within limits. ([SQLite Limits](https://sqlite.org/limits.html))
- Practical performance depends heavily on indexing and whether frequently-used indices fit in OS page cache.
- phiresky achieved 100K SELECTs/second on a multi-GB SQLite database with proper tuning (WAL mode, mmap, correct page size). ([phiresky Blog](https://phiresky.github.io/blog/2020/sqlite-performance-tuning/))
- A benchmark showed 100,000 TPS over a billion rows in SQLite with optimized configuration. ([andersmurphy Blog](https://andersmurphy.com/2025/12/02/100000-tps-over-a-billion-rows-the-unreasonable-effectiveness-of-sqlite.html))
- However: 50GB in a **single file** with concurrent access from a web server means the OS page cache must work hard, and write contention at this size amplifies the single-writer bottleneck.

**PostgreSQL:**
- 50GB is a modest database for PostgreSQL. Production PostgreSQL databases routinely handle hundreds of GB to TB.
- VACUUM, autovacuum, and table partitioning handle data lifecycle at this scale.
- Parallel query execution available for analytical queries across large tables.
- pg_stat_statements, EXPLAIN ANALYZE, and auto_explain provide deep performance introspection.

**In a database-per-tenant SQLite model:** If you have, say, 100 tenants, each database averages 500MB -- a size where SQLite excels. This is the strongest argument for SQLite. But the aggregate operational complexity of managing 100+ databases must be weighed against the simplicity of one PostgreSQL instance.

### 4. Operational Characteristics: PostgreSQL Far Superior (Confidence: 93%)

| Capability | SQLite | PostgreSQL |
|---|---|---|
| Backup | File copy (or Litestream for streaming) | pg_dump, pg_basebackup, pgBackRest, PITR via WAL archiving |
| Point-in-Time Recovery | Not native (Litestream provides approximate) | Native via WAL archiving (exact LSN recovery) |
| Replication | LiteFS (beta, deprioritized by Fly.io), Turso embedded replicas | Streaming replication (sync/async), logical replication, native |
| High Availability | Application-level only | Patroni, pg_auto_failover, cloud-managed HA (RDS Multi-AZ) |
| Monitoring | Application-level metrics only | pg_stat_activity, pg_stat_statements, pgBadger, cloud monitoring |
| Online schema changes | Not supported (must rebuild table) | ALTER TABLE with minimal locking, pg_repack for zero-downtime |
| Connection management | N/A (embedded) | PgBouncer, pgpool-II |

**Key concern:** LiteFS Cloud was sunset in October 2024, and Fly.io has deprioritized active development on LiteFS. For new projects, Turso or Cloudflare D1 are the recommended SQLite replication solutions, but both add vendor lock-in. ([SitePoint: SQLite Edge Production Ready](https://www.sitepoint.com/sqlite-edge-production-readiness-2026/))

### 5. Security & Compliance: PostgreSQL is Enterprise-Ready (Confidence: 92%)

| Security Feature | SQLite | PostgreSQL |
|---|---|---|
| Authentication | None (OS file permissions only) | SCRAM-SHA-256, Kerberos, LDAP, certificate-based |
| Authorization | None built-in | RBAC with GRANT/REVOKE, Row-Level Security |
| Encryption at rest | Requires SQLCipher (third-party) | Native tablespace encryption, cloud KMS integration |
| Encryption in transit | N/A (embedded, no network) | Native SSL/TLS |
| Audit logging | None built-in | pgAudit extension (session + object level) |
| SOC 2 readiness | Requires extensive external tooling | Native controls map to SOC 2 requirements ([EDB: PostgreSQL Compliance](https://www.enterprisedb.com/postgresql-compliance-gdpr-soc-2-data-privacy-security)) |
| GDPR support | Manual implementation required | RLS, audit logging, encryption support GDPR data handling |

**OWASP Multi-Tenant Security Cheat Sheet** recommends:
- Tenant isolation at the data layer (PostgreSQL RLS satisfies this; SQLite requires application-level enforcement)
- Independent encryption of tenant data (PostgreSQL supports per-tablespace encryption)
- Attribute-Based Access Control (ABAC) over RBAC for multi-tenant (PostgreSQL's policy system supports this pattern)

Source: [OWASP Multi-Tenant Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)

### 6. Total Cost of Ownership (Confidence: 80%)

**PostgreSQL (Managed):**

| Provider | Configuration | Est. Monthly Cost |
|---|---|---|
| AWS RDS (db.t3.medium) | 2 vCPU, 4GB RAM, 50GB gp3 | ~$58/month |
| AWS RDS (db.t3.large) | 2 vCPU, 8GB RAM, 50GB gp3 | ~$105/month |
| AWS RDS Multi-AZ (db.t3.medium) | HA with failover, 50GB | ~$116/month |
| Neon (Scale plan) | Autoscaling, 50GB storage | ~$70-150/month (usage-dependent) |
| Supabase (Pro) | 50GB, built-in auth/API | ~$25/month base + compute |
| DigitalOcean Managed | 2 vCPU, 4GB RAM, 50GB | ~$60/month |

Sources: [AWS RDS PostgreSQL Pricing](https://aws.amazon.com/rds/postgresql/pricing/), [Neon Pricing](https://neon.com/pricing), [Bytebase Hosting Comparison](https://www.bytebase.com/blog/postgres-hosting-options-pricing-comparison/)

**SQLite (Self-Managed on VPS):**

| Approach | Configuration | Est. Monthly Cost |
|---|---|---|
| Single VPS (Hetzner/DigitalOcean) | 4 vCPU, 8GB RAM, 80GB SSD | ~$24-48/month |
| VPS + Litestream backups to S3 | Above + S3 storage | ~$26-50/month |
| Turso (managed SQLite) | Scale plan, 50GB, replication | ~$50-200/month |

**Hidden costs for SQLite at this scale:**
- No managed HA -- engineer time to build and maintain failover: **significant**
- No managed monitoring -- must integrate custom solutions
- Schema migrations across N tenant databases: **custom tooling required**
- If you outgrow SQLite: migration to PostgreSQL costs engineering weeks

**Hidden costs for PostgreSQL:**
- Connection pooling setup (PgBouncer): ~1 hour one-time setup
- Managed services handle backups, HA, monitoring: **included in price**

**Net assessment:** SQLite has lower infrastructure cost ($24-50/month vs $58-150/month) but significantly higher operational/engineering cost. For a SaaS startup where engineer time is the most expensive resource, PostgreSQL's managed offerings provide better TCO.

### 7. Ecosystem & Tooling: PostgreSQL is More Mature (Confidence: 90%)

| Dimension | SQLite | PostgreSQL |
|---|---|---|
| ORM support | Supported by all major ORMs (SQLAlchemy, Prisma, Drizzle, Django ORM, ActiveRecord, GORM) | Supported by all major ORMs with deeper feature integration (RLS, JSONB, arrays, custom types) |
| Full-text search | FTS5 extension (functional but basic) | tsvector/tsquery (powerful, configurable) + pg_trgm |
| JSON support | JSON1 extension (basic) | JSONB with indexing, containment operators, JSON path queries |
| Extensions | Limited (loadable extensions, growing ecosystem) | Rich: PostGIS, pgvector, pg_cron, pgAudit, TimescaleDB, hundreds more |
| Hosting options | VPS + manual management, Turso, Cloudflare D1 | AWS RDS, Neon, Supabase, DigitalOcean, Render, Railway, Fly.io, Aiven, CrunchyBridge, self-hosted |
| Migration tools | Limited (app-level migrations, pgloader for SQLite->PG) | Alembic, Flyway, Liquibase, golang-migrate, prisma migrate, dbmate |
| Monitoring | None built-in | pg_stat_statements, pgBadger, pgHero, cloud-native monitoring |
| Vector/AI | sqlite-vec (early) | pgvector (mature, widely adopted) |

### 8. Growth Trajectory: PostgreSQL Scales Without Architecture Change (Confidence: 88%)

| Growth Milestone | SQLite Path | PostgreSQL Path |
|---|---|---|
| Year 1: 500 users, 50GB | Feasible with db-per-tenant, tight optimization | Comfortable, standard deployment |
| Year 2: 2,000 users, 200GB | **Strain**: write contention serious, need Turso/edge infra | Add read replicas, minor tuning |
| Year 3: 5,000 users, 500GB | **Migration required** or complex distributed SQLite | Vertical scaling or partitioning |
| Year 5: 20,000 users, 2TB | Not viable without full re-architecture | Add Citus for horizontal sharding, or Aurora |

The SQLite official documentation itself states: "If there are many client programs sending SQL to the same database over a network, then use a client/server database engine instead of SQLite." ([SQLite: Appropriate Uses](https://sqlite.org/whentouse.html))

---

## Industry Standards Compliance (Phase 3)

| Standard | Requirement | SQLite | PostgreSQL | Source |
|---|---|---|---|---|
| **OWASP Multi-Tenant Security** | Engine-level tenant data isolation | Does NOT comply (application-level only) | Complies (Row-Level Security) | [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html) |
| **SOC 2 Type II** (Trust Services Criteria) | Access controls, audit logging, encryption | Partial (requires extensive external tooling) | Complies (native RBAC, pgAudit, SSL/TLS, encryption) | [EDB Compliance Guide](https://www.enterprisedb.com/postgresql-compliance-gdpr-soc-2-data-privacy-security) |
| **GDPR** (Art. 25, 32) | Data protection by design, encryption, access control | Partial (SQLCipher for encryption, no native access control) | Complies (RLS, encryption, audit logging) | [GDPR Art. 25](https://gdpr-info.eu/art-25-gdpr/) |
| **PCI-DSS v4.0** (Req. 7, 8, 10) | Access control, authentication, audit trails | Does NOT comply natively | Complies (authentication, RBAC, pgAudit) | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/) |
| **NIST SP 800-53** (AC, AU families) | Access control, audit and accountability | Partial | Complies | [NIST SP 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) |
| **ISO 27001:2022** (A.8.3, A.8.9) | Access control to information, configuration management | Partial (requires external tooling) | Complies (native capabilities) | [ISO 27001:2022](https://www.iso.org/standard/27001) |

**Summary:** PostgreSQL meets or can be configured to meet all major compliance frameworks natively. SQLite requires significant external tooling and application-level controls to achieve partial compliance, and some requirements (engine-level access control) cannot be satisfied at all.

---

## Quantitative Analysis (Phase 4)

### Write Contention Model

For a SaaS app with 500 concurrent users, assuming a typical web application write pattern:

```
Assumptions:
- 500 concurrent users
- Average 1 write operation per user per minute (conservative for SaaS)
- Average write transaction duration: 5ms (SQLite), 2ms (PostgreSQL per-row)
- Read:write ratio: 10:1 (typical SaaS)

SQLite (single writer):
- Write operations per second: 500 users * 1 write/min / 60 = ~8.3 writes/sec
- Time per write: 5ms
- Write utilization: 8.3 * 0.005 = 4.2% of available write capacity
- At 4.2% utilization, queueing is minimal -- SQLite CAN handle this load
- BUT: Real-world writes come in bursts (page loads, form submissions, batch ops)
- Burst scenario (50 simultaneous writes): 50 * 5ms = 250ms queue time for last writer
- Peak scenario (200 simultaneous writes): 200 * 5ms = 1000ms (1 second) queue time

PostgreSQL (MVCC, multiple writers):
- Write operations per second: same 8.3 writes/sec
- All 8.3 writes execute concurrently (row-level locking)
- Burst scenario (50 simultaneous writes): ~2-5ms each (parallel execution)
- Peak scenario (200 simultaneous writes): ~2-10ms each (parallel, row-level contention only)
```

**Key insight:** At *average* load, SQLite can handle 500 users. At *peak/burst* load (which happens daily in any SaaS), PostgreSQL provides 10-100x lower write latency. SaaS applications must be designed for peak, not average.

### Cost-Benefit Decision Matrix

| Dimension | Weight | SQLite Score (1-10) | PostgreSQL Score (1-10) | SQLite Weighted | PostgreSQL Weighted |
|---|---|---|---|---|---|
| Write concurrency at 500 users | 0.20 | 4 | 9 | 0.80 | 1.80 |
| Multi-tenant security | 0.20 | 3 | 9 | 0.60 | 1.80 |
| Operational simplicity | 0.15 | 5 | 8 | 0.75 | 1.20 |
| Infrastructure cost | 0.10 | 9 | 6 | 0.90 | 0.60 |
| Compliance readiness | 0.10 | 3 | 9 | 0.30 | 0.90 |
| Growth scalability | 0.10 | 3 | 8 | 0.30 | 0.80 |
| Ecosystem/tooling | 0.10 | 6 | 9 | 0.60 | 0.90 |
| Data volume handling | 0.05 | 7 | 9 | 0.35 | 0.45 |
| **TOTAL** | **1.00** | | | **4.60** | **8.45** |

**PostgreSQL scores 84% higher than SQLite** in this weighted analysis for the specific requirements given.

---

## Alternatives Considered

### Alternative 1: SQLite with Database-Per-Tenant on Turso

**Architecture:** Each tenant gets a separate SQLite database hosted on Turso with embedded replicas at the edge.

**Strengths:**
- Eliminates the single-writer bottleneck (each tenant has its own writer)
- Edge replication provides low-latency reads globally
- Natural data isolation without RLS complexity
- Per-tenant backup is trivial (copy file)

**Weaknesses:**
- Turso is a relatively young platform (higher vendor risk)
- Cross-tenant queries (analytics, admin dashboards) require aggregation across N databases
- Schema migrations must be applied to each database individually
- No native RLS, audit logging, or compliance tooling
- LiteFS Cloud was sunset in Oct 2024; the SQLite replication ecosystem is still stabilizing

**Verdict:** Viable for read-heavy, privacy-focused SaaS with strict tenant isolation requirements and global edge deployment needs. Not recommended as the default choice for a general multi-tenant SaaS. Ranked lower due to ecosystem maturity risk.

### Alternative 2: SQLite for Development, PostgreSQL for Production

**Architecture:** Use SQLite locally for development speed, PostgreSQL in production.

**Strengths:**
- Fast local development (no database server to manage)
- Zero-config development environment

**Weaknesses:**
- Behavioral differences between SQLite and PostgreSQL (type affinity, date handling, string comparison) cause bugs that only appear in production
- ORM abstraction doesn't eliminate all differences
- Industry best practice is to develop against the same database you deploy to

**Verdict:** Not recommended. Use Docker/docker-compose to run PostgreSQL locally -- it takes 30 seconds to set up and eliminates an entire class of environment parity bugs.

### Alternative 3: MySQL/MariaDB

**Architecture:** Use MySQL as a middle ground.

**Strengths:**
- Strong concurrency (MVCC in InnoDB)
- Lower resource usage than PostgreSQL in some configurations
- Wide hosting availability

**Weaknesses:**
- No native Row-Level Security (application-level tenant isolation only)
- Weaker standards compliance than PostgreSQL (SQL standard conformance)
- Less rich extension ecosystem
- PostgreSQL has overtaken MySQL in developer preference (Stack Overflow 2024 survey: PostgreSQL #1 most admired database)

**Verdict:** Ranked below PostgreSQL for multi-tenant SaaS due to lack of RLS. Ranked above SQLite for concurrency but below PostgreSQL overall.

---

## Adversarial Review (Phase 5)

### Counterargument 1: "SQLite is fast enough -- the write bottleneck is overblown"

**The argument:** At 8.3 writes/second average, SQLite is at <5% write utilization. Most web apps are read-heavy (10:1 or higher). SQLite handles this fine.

**Evidence for:** A production Rails app on SQLite handled 2,730 write req/sec. The 37signals team (Basecamp/HEY) has championed SQLite for production use.

**Rebuttal:** Average load is not the design constraint -- **peak load is**. SaaS applications experience traffic bursts (marketing campaigns, onboarding cohorts, batch operations, cron jobs, webhook storms). A single long-running write transaction (report generation, data import) blocks ALL other writes. PostgreSQL's MVCC handles bursts gracefully; SQLite's single-writer creates cascading latency spikes. The SkyPilot team documented this exact failure mode at 500 concurrent operations.

**Conclusion:** The counterargument holds for low-write SaaS (content platforms, dashboards). It fails for typical SaaS with form submissions, real-time updates, or batch operations. **Partially weakens** the recommendation for read-heavy-only use cases.

### Counterargument 2: "Database-per-tenant SQLite solves all concurrency issues"

**The argument:** With N tenants each having their own database, each database only handles (500/N) concurrent users. With 100 tenants, that is 5 concurrent users per database -- trivial for SQLite.

**Evidence for:** Turso supports this pattern at scale. Expensify processes $10B in transactions on SQLite.

**Rebuttal:** This is architecturally valid but introduces **operational complexity** that must be weighed:
- Schema migrations across 100+ databases require custom tooling
- Cross-tenant analytics require aggregation infrastructure
- No managed HA/failover solution with the maturity of PostgreSQL equivalents
- Monitoring and alerting across N databases is harder than one
- Turso/D1 maturity risk: these platforms are 2-3 years old vs PostgreSQL's 28 years

**Conclusion:** Valid architecture for specific use cases (edge-first, privacy-focused). Does not change the general recommendation. **Does not weaken** the conclusion for the stated requirements.

### Counterargument 3: "PostgreSQL is overengineered for a startup -- start simple"

**The argument:** Startups should minimize infrastructure complexity. SQLite requires zero configuration. PostgreSQL requires a server, connection pooling, monitoring.

**Evidence for:** "SQLite for SaaS -- Why You Don't Need Postgres Yet" articles exist. YAGNI principle.

**Rebuttal:** Managed PostgreSQL (Neon, Supabase, RDS) requires zero server management. `docker run postgres` provides a local development instance in seconds. The "complexity" argument was valid in 2015; in 2026, managed PostgreSQL is as simple to deploy as any SaaS tool. Meanwhile, starting with SQLite and migrating to PostgreSQL later costs **engineering weeks** and carries data migration risk -- the opposite of simplicity.

**Conclusion:** The counterargument is outdated given modern managed PostgreSQL options. **Does not weaken** the recommendation.

### Assumption Audit

| Assumption | Status | Risk if Wrong |
|---|---|---|
| 500 concurrent users implies meaningful write concurrency | Reasonable -- SaaS apps involve form submissions, updates, notifications | If purely read-only (e.g., analytics dashboard), SQLite becomes more viable |
| Multi-tenant means shared infrastructure | Verified -- standard SaaS model | If dedicated infrastructure per customer (enterprise), architecture changes significantly |
| 50GB grows over time | Reasonable -- SaaS data typically grows | If data is ephemeral/pruned, SQLite's size limitation is less relevant |
| Compliance will eventually be required | Reasonable -- SaaS serving business customers will face SOC2/GDPR requests | If B2C-only with no compliance needs, this factor's weight decreases |
| Team has standard web development skills | Assumed | If team has deep SQLite expertise and no PostgreSQL experience, learning curve factor changes |
| Single-region deployment initially | Assumed | If multi-region from day 1, edge SQLite (Turso/D1) becomes more interesting |

### Failure Modes

1. **If you choose PostgreSQL and traffic is much lower than expected:** Minimal downside. You've slightly overspent on infrastructure (~$30-80/month more than SQLite VPS). PostgreSQL still works fine for 50 users.

2. **If you choose SQLite and traffic is higher than expected:** Significant downside. Write contention causes user-facing latency spikes. Migration to PostgreSQL under production load is stressful and risky. This is the asymmetric risk that drives the recommendation.

3. **If you choose PostgreSQL and need to change:** PostgreSQL-to-MySQL or PostgreSQL-to-CockroachDB migrations are well-documented. The ecosystem is mature.

4. **If you choose SQLite and need to change:** SQLite-to-PostgreSQL migration is a one-way door that costs engineering time. Data type differences (SQLite's type affinity vs PostgreSQL's strict typing) can surface data integrity issues during migration.

---

## Recommendation

**Use PostgreSQL** with a managed hosting provider. Specific guidance:

### Immediate Setup (Month 0-1)
1. **Choose a managed PostgreSQL provider:** Neon (serverless, scales to zero for cost savings), Supabase (if you want built-in auth/API), or AWS RDS (if you want maximum control and mature tooling)
2. **Implement RLS-based multi-tenancy:** `tenant_id` column on every tenant-scoped table, RLS policies enforcing isolation
3. **Use PgBouncer** in transaction mode if your connection count exceeds 100 (most managed providers include this)
4. **Use an ORM** that supports PostgreSQL natively (Prisma, Drizzle, SQLAlchemy, Django ORM, etc.)

### Growth Milestones
- **500 users, 50GB (Year 1):** Single PostgreSQL instance with RLS. Total cost: $50-150/month managed.
- **2,000 users, 200GB (Year 2):** Add read replica for analytics queries. Cost: ~$100-300/month.
- **5,000+ users, 500GB+ (Year 3+):** Consider table partitioning, Citus for horizontal sharding, or Aurora for managed scaling.

### Conditions Under Which This Recommendation Changes

- If the application is **read-only or read-95%+** (e.g., a content delivery platform), SQLite with Turso becomes viable.
- If **data sovereignty** requires per-tenant database files in specific geographic regions, SQLite database-per-tenant on edge infrastructure is worth evaluating.
- If **latency to a centralized database** is unacceptable (global users, <50ms requirement), edge SQLite with Turso embedded replicas provides a compelling architecture.
- If **budget is extremely constrained** (<$20/month for infrastructure) and the write load is genuinely minimal, SQLite on a single VPS is acceptable as a temporary measure with a documented migration plan.

**Confidence in recommendation: 92%**

The 8% uncertainty is allocated to: (a) the possibility that the workload is overwhelmingly read-heavy, which would make SQLite viable, and (b) the rapid maturation of the edge SQLite ecosystem (Turso, D1), which could close the operational gap faster than expected.

---

## Sources

### Official Documentation
- [SQLite: Appropriate Uses](https://sqlite.org/whentouse.html)
- [SQLite: Implementation Limits](https://sqlite.org/limits.html)
- [SQLite: BEGIN CONCURRENT (experimental)](https://www.sqlite.org/src/doc/begin-concurrent/doc/begin_concurrent.md)
- [PostgreSQL: Concurrency Control (MVCC)](https://www.postgresql.org/docs/current/mvcc.html)
- [PostgreSQL: MVCC Introduction](https://www.postgresql.org/docs/current/mvcc-intro.html)
- [PostgreSQL: pg_basebackup](https://www.postgresql.org/docs/current/app-pgbasebackup.html)
- [PgBouncer Configuration](https://www.pgbouncer.org/config.html)

### Security & Compliance Standards
- [OWASP Multi-Tenant Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)
- [OWASP Cloud Tenant Isolation Project](https://owasp.org/www-project-cloud-tenant-isolation/)
- [EDB: PostgreSQL Compliance (GDPR, SOC 2)](https://www.enterprisedb.com/postgresql-compliance-gdpr-soc-2-data-privacy-security)
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

### Multi-Tenancy Architecture
- [AWS: Multi-tenant data isolation with PostgreSQL RLS](https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/)
- [Crunchy Data: Row Level Security for Tenants in Postgres](https://www.crunchydata.com/blog/row-level-security-for-tenants-in-postgres)
- [Turso: Database Per Tenant](https://turso.tech/multi-tenancy)
- [Microsoft: Multi-Tenant SaaS Patterns](https://learn.microsoft.com/en-us/azure/azure-sql/database/saas-tenancy-app-design-patterns)
- [Bytebase: Multi-Tenant Database Architecture Patterns](https://www.bytebase.com/blog/multi-tenant-database-architecture-patterns-explained/)

### Benchmarks & Performance
- [phiresky: SQLite Performance Tuning (100K SELECTs/sec)](https://phiresky.github.io/blog/2020/sqlite-performance-tuning/)
- [andersmurphy: 100,000 TPS over a billion rows with SQLite](https://andersmurphy.com/2025/12/02/100000-tps-over-a-billion-rows-the-unreasonable-effectiveness-of-sqlite.html)
- [SkyPilot: SQLite Concurrency at 500x](https://blog.skypilot.co/abusing-sqlite-to-handle-concurrency/)
- [Fly.io: SQLite Internals WAL](https://fly.io/blog/sqlite-internals-wal/)
- [dev-family: PostgreSQL & SQLite Speed Test (GitHub)](https://github.com/dev-family/sqlite-bench)

### Hosting & Pricing
- [AWS RDS PostgreSQL Pricing](https://aws.amazon.com/rds/postgresql/pricing/)
- [Neon Pricing](https://neon.com/pricing)
- [Bytebase: PostgreSQL Hosting Options Pricing Comparison (2025)](https://www.bytebase.com/blog/postgres-hosting-options-pricing-comparison/)

### Production Case Studies & Industry Analysis
- [SitePoint: Is SQLite on the Edge Production Ready? (2026)](https://www.sitepoint.com/sqlite-edge-production-readiness-2026/)
- [DEV Community: The SQLite Renaissance (2026)](https://dev.to/pockit_tools/the-sqlite-renaissance-why-the-worlds-most-deployed-database-is-taking-over-production-in-2026-3jcc)
- [Percona: PgBouncer for PostgreSQL](https://www.percona.com/blog/pgbouncer-for-postgresql-how-connection-pooling-solves-enterprise-slowdowns/)
- [Heroku: PostgreSQL Concurrency](https://devcenter.heroku.com/articles/postgresql-concurrency)
- [Simplyblock: Row-Level Security for Multi-Tenancy](https://www.simplyblock.io/blog/underated-postgres-multi-tenancy-with-row-level-security/)
