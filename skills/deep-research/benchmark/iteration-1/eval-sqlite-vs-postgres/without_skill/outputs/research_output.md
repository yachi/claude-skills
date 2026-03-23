# SQLite vs PostgreSQL for a Multi-Tenant SaaS App (500 Concurrent Users, 50GB Data)

## Executive Summary

**Recommendation: Use PostgreSQL.** For a multi-tenant SaaS application expecting 500 concurrent users and 50GB of data within the first year, PostgreSQL is the substantially stronger choice across nearly every dimension that matters: concurrency, multi-tenancy isolation, operational maturity, disaster recovery, and scalability headroom. SQLite is a viable option only under a narrow database-per-tenant architecture with low per-tenant concurrency, and even then it introduces significant operational complexity at your scale.

---

## 1. Concurrency Model

### PostgreSQL

PostgreSQL uses **Multi-Version Concurrency Control (MVCC)**, meaning readers never block writers and writers never block readers. This is fundamental for a SaaS app with 500 concurrent users where reads and writes happen simultaneously across tenants. PostgreSQL can comfortably handle thousands of concurrent connections, especially when paired with a connection pooler like [PgBouncer](https://www.pgbouncer.org/config.html).

With PgBouncer, a typical configuration for 500 concurrent app-level users might map down to 30-40 actual database connections, since most "concurrent" users are not executing queries at the exact same millisecond. Each raw PostgreSQL connection consumes approximately 10MB of RAM, so connection pooling is important but well-understood.

### SQLite

SQLite uses a **single-writer model**. Even with WAL (Write-Ahead Logging) mode enabled, only one write transaction can proceed at a time. All other concurrent writes are queued and will receive a "database is locked" error if they exceed the busy timeout. At 500 concurrent users generating writes (creating records, updating settings, processing transactions), this becomes a critical bottleneck.

Practical guidance from production deployments suggests that at 500x write concurrency, you need ~10-second busy timeouts to reduce timeout probability, which means individual requests can stall for seconds waiting for write access. This is unacceptable for a responsive SaaS application.

**Verdict: PostgreSQL wins decisively.** The single-writer limitation in SQLite is the single most disqualifying factor for a shared-database multi-tenant SaaS at this scale.

---

## 2. Multi-Tenancy Architecture

### PostgreSQL: Mature Multi-Tenant Patterns

PostgreSQL supports three well-established multi-tenancy patterns:

1. **Shared schema with Row-Level Security (RLS)** -- Most cost-effective. All tenants share the same tables, with a `tenant_id` column. PostgreSQL's [Row-Level Security](https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/) enforces isolation at the database engine level, so even application bugs cannot leak data across tenants. This is the recommended pattern for most SaaS applications.

2. **Schema per tenant** -- Each tenant gets their own PostgreSQL schema within a shared database. Good isolation with manageable overhead up to hundreds of tenants.

3. **Database per tenant** -- Maximum isolation, typically for enterprise/regulated customers. More operational overhead but PostgreSQL handles it well.

RLS is particularly powerful because isolation enforcement moves from the application layer (where bugs can expose data) to the database engine (where enforcement is guaranteed). The key design pattern is making `tenant_id` a first-class column on every tenant-scoped table.

### SQLite: Database-Per-Tenant Only

SQLite's viable multi-tenant option is **database-per-tenant**, where each tenant gets their own SQLite file. This provides strong isolation by default but introduces challenges:

- **Schema migrations** must be applied to every database file individually
- **Cross-tenant queries** (admin dashboards, analytics, billing aggregation) require opening and querying multiple databases
- **Connection management** becomes complex with hundreds of database files
- Services like [Turso](https://turso.tech/multi-tenancy) address some of these challenges (managed schema evolution, up to 10,000 databases on the $29/month plan), but this is a relatively young ecosystem

**Verdict: PostgreSQL wins.** RLS provides battle-tested, engine-level tenant isolation with zero application-level risk. SQLite's database-per-tenant model is architecturally sound but operationally heavier and lacks cross-tenant querying.

---

## 3. Data Size and Performance at 50GB

### PostgreSQL

50GB is a modest workload for PostgreSQL. Production PostgreSQL instances routinely handle terabytes of data. With proper indexing, partitioning (e.g., by tenant or date), and vacuuming, 50GB presents no performance concerns. PostgreSQL's query planner is sophisticated and handles complex joins, subqueries, CTEs, and window functions efficiently at this scale.

### SQLite

50GB is right at the threshold where SQLite performance begins to degrade meaningfully. [Recent benchmarks](https://markaicode.com/sqlite-4-production-database-benchmarks-pitfalls/) show that performance slows significantly with databases over 50GB. Specific concerns at this scale:

- **VACUUM operations** become very slow and require roughly 2x the database size in free disk space
- **Integrity checks** take progressively longer
- **Backup time** grows linearly with database size
- **Full table scans** become impractical

In a database-per-tenant model, individual tenant databases would be smaller (50GB / N tenants), which mitigates this concern. But any cross-tenant analytics or a single large tenant would still hit these limits.

**Verdict: PostgreSQL wins.** 50GB is trivial for PostgreSQL but represents the performance cliff for SQLite.

---

## 4. Backup, Disaster Recovery, and Replication

### PostgreSQL

PostgreSQL offers a comprehensive disaster recovery toolkit:

- **Streaming replication** for real-time standby replicas
- **Point-in-time recovery (PITR)** using continuous WAL archiving
- **Logical replication** for selective data replication
- **pg_dump / pg_restore** for logical backups
- **Automatic failover** with tools like Patroni or managed service features
- Read replicas for load distribution

Every managed PostgreSQL provider (AWS RDS, Supabase, Neon, DigitalOcean) includes automated backups, point-in-time recovery, and high-availability options out of the box.

### SQLite

SQLite backup is conceptually simple (copy the file), but safely doing so in production requires care:

- **Litestream** provides streaming replication by continuously copying WAL pages to S3 or other storage. This is a solid tool but adds an operational component outside the database itself.
- **No built-in replication** -- you depend on external tools
- **No point-in-time recovery** without Litestream or similar
- **No read replicas** (LiteFS provided distributed read replicas but [was discontinued](https://fly.io/blog/litefs))

**Verdict: PostgreSQL wins.** Built-in replication, PITR, and a mature managed-service ecosystem make PostgreSQL far more robust for SaaS disaster recovery requirements.

---

## 5. Operational Cost and Complexity

### PostgreSQL

- **Managed hosting**: $15-50/month for entry-level instances (DigitalOcean, Supabase, Neon, AWS RDS)
- **Serverless options**: Neon scales to zero when idle, reducing costs for dev/staging environments
- **Operational complexity**: Moderate. Requires understanding of connection pooling, vacuuming, and indexing, but the ecosystem is mature with extensive documentation
- **Monitoring**: Rich ecosystem (pg_stat_statements, pganalyze, built-in statistics views)

### SQLite

- **Hosting cost**: $0 for the database itself (it's a file). But you still need compute, and you lose the operational benefits of managed database services
- **Managed SQLite**: Turso starts at $29/month for the Scaler plan (10,000 databases). Cloudflare D1 is another option.
- **Operational complexity**: Deceptively low at small scale, but increases significantly for multi-tenant SaaS (schema migrations across many databases, monitoring many files, cross-tenant queries)
- **Hidden costs**: You must build or integrate tools for monitoring, backup, migration, and analytics that PostgreSQL ecosystem provides out of the box

**Verdict: Mixed.** SQLite has lower entry cost but higher hidden operational complexity at SaaS scale. PostgreSQL's managed services provide a better total cost of ownership for this use case.

---

## 6. Feature Comparison for SaaS Applications

| Feature | PostgreSQL | SQLite |
|---------|-----------|--------|
| Concurrent read/write | Yes (MVCC) | Single writer only |
| Row-Level Security | Built-in | Not available |
| Full-text search | Built-in (tsvector) | FTS5 extension |
| JSON support | jsonb with indexing | JSON functions (less mature) |
| Stored procedures | PL/pgSQL, PL/Python, etc. | Not supported |
| Triggers | Full support | Basic support |
| Partitioning | Declarative partitioning | Not supported |
| Extensions | PostGIS, pg_trgm, pgvector, etc. | Limited extensions |
| LISTEN/NOTIFY | Built-in (real-time events) | Not available |
| Partial indexes | Yes | Yes (since 3.8.0) |
| Generated columns | Yes | Yes |
| CTEs (WITH) | Full support including recursive | Full support including recursive |
| Window functions | Full support | Full support |

---

## 7. When SQLite *Would* Be the Right Choice

Despite the strong recommendation for PostgreSQL, SQLite deserves consideration in specific scenarios:

1. **Edge/embedded deployments** where each user runs their own instance (e.g., local-first apps with sync)
2. **Database-per-tenant with very low per-tenant concurrency** (< 5 concurrent users per tenant) and a service like Turso managing the infrastructure
3. **Read-heavy workloads** with infrequent writes where the single-writer limitation does not matter
4. **Prototyping and MVP** where you want to validate the product before investing in database infrastructure (but plan to migrate)

Your scenario (500 concurrent users, 50GB, multi-tenant SaaS) does not match any of these profiles.

---

## 8. Migration Path and Future-Proofing

Starting with PostgreSQL positions you well for growth:

- **Horizontal read scaling**: Add read replicas as traffic grows
- **Vertical scaling**: Increase instance size (managed services make this trivial)
- **Sharding**: Citus extension or application-level sharding for extreme scale
- **Analytics**: Direct connection to BI tools, or logical replication to an analytics warehouse
- **Compliance**: RLS, audit logging, encryption at rest -- all built-in or available via extensions

Starting with SQLite and migrating to PostgreSQL later is possible (the SQL dialects are similar) but involves non-trivial effort: schema differences, data type mismatches, rewriting queries that use SQLite-specific behavior, and rebuilding your multi-tenancy isolation layer.

---

## Final Recommendation

**Use PostgreSQL** for your multi-tenant SaaS application. Specifically:

1. **Architecture**: Shared schema with Row-Level Security (RLS) using a `tenant_id` column on all tenant-scoped tables
2. **Connection pooling**: Deploy PgBouncer (or use your managed provider's built-in pooler) from day one
3. **Hosting**: Start with a managed service (Supabase, Neon, or DigitalOcean Managed Databases) at $15-50/month
4. **Backups**: Enable automated daily backups and point-in-time recovery (included with most managed services)
5. **Monitoring**: Set up pg_stat_statements for query performance analysis early

This setup will comfortably handle 500 concurrent users and 50GB of data, with clear scaling paths well beyond those numbers.

---

## Sources

- [PostgreSQL vs SQLite: Dive into Two Very Different Databases (DEV Community)](https://dev.to/lovestaco/postgresql-vs-sqlite-dive-into-two-very-different-databases-5a90)
- [Database-per-Tenant: Consider SQLite (Medium)](https://medium.com/@dmitry.s.mamonov/database-per-tenant-consider-sqlite-9239113c936c)
- [SQLite WAL Mode Documentation](https://sqlite.org/wal.html)
- [SQLite Concurrent Writes and "database is locked" Errors](https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/)
- [Appropriate Uses for SQLite (Official)](https://sqlite.org/whentouse.html)
- [Implementation Limits for SQLite (Official)](https://sqlite.org/limits.html)
- [Multi-tenant Data Isolation with PostgreSQL Row Level Security (AWS)](https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/)
- [Shipping Multi-tenant SaaS Using Postgres Row-Level Security (Nile)](https://www.thenile.dev/blog/multi-tenant-rls)
- [Turso Multi-Tenancy](https://turso.tech/multi-tenancy)
- [The SQLite Renaissance (DEV Community, 2026)](https://dev.to/pockit_tools/the-sqlite-renaissance-why-the-worlds-most-deployed-database-is-taking-over-production-in-2026-3jcc)
- [PgBouncer Configuration](https://www.pgbouncer.org/config.html)
- [How to Handle 10K Connections with PgBouncer (OneUptime)](https://oneuptime.com/blog/post/2026-01-26-pgbouncer-connection-pooling/view)
- [PgBouncer for PostgreSQL: How Connection Pooling Solves Enterprise Slowdowns (Percona)](https://www.percona.com/blog/pgbouncer-for-postgresql-how-connection-pooling-solves-enterprise-slowdowns/)
- [Litestream: How It Works](https://litestream.io/how-it-works/)
- [PostgreSQL Hosting Options Pricing Comparison (Bytebase)](https://www.bytebase.com/blog/postgres-hosting-options-pricing-comparison/)
- [Database Backups and Disaster Recovery in PostgreSQL (Tiger Data)](https://www.tigerdata.com/blog/database-backups-and-disaster-recovery-in-postgresql-your-questions-answered)
- [How SQLite Scales Read Concurrency (Fly.io)](https://fly.io/blog/sqlite-internals-wal/)

---

| Metric | Assessment |
|--------|------------|
| **Effort** | Low -- PostgreSQL managed services handle most operational burden |
| **Impact** | Critical -- database choice affects every layer of the application |
| **Confidence** | High -- well-established engineering consensus backed by benchmarks |
| **Risk** | Low with PostgreSQL; High with SQLite at this concurrency/scale |
| **Complexity** | Moderate -- RLS + connection pooling require upfront design |
| **Reversibility** | Low -- database migration is costly; choose correctly upfront |
| **Maintainability** | High with PostgreSQL -- mature ecosystem, tooling, and talent pool |
| **Expandability** | High with PostgreSQL -- read replicas, partitioning, extensions (Citus, pgvector) |
