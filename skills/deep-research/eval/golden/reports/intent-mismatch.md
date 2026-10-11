# Fast full-text search for the internal-notes app — Algolia vs. on-prem options

## Executive Summary

**Algolia is a non-starter for this app and cannot be recommended.** Algolia is a SaaS-only product — it has no on-premises or self-hosted deployment; all indexing and query processing happen on Algolia's cloud infrastructure. That directly violates the README's non-negotiable constraints (fully on-premises, no third-party SaaS may process/index/store app data, no outbound connections from the data tier). Any Algolia integration would ship regulated patient data to an external service, which compliance has ruled out.

The right move is to pivot to a **self-hosted** search engine running on hardware you own. The strongest default is **PostgreSQL full-text search** if the app already runs on Postgres (zero new infrastructure, index stays inside the DB and inside the datacenter). If you need typo tolerance / instant search-as-you-type UX or expect a large corpus, self-host **Meilisearch** or **Typesense**; reach for **OpenSearch** only if you also need log-scale analytics. **Overall confidence: 95%** (the constraint conflict is unambiguous; the ranking among on-prem options depends on your existing stack, which I had to assume).

> **Intent note (why I did not just "confirm Algolia"):** You asked me to confirm Algolia is the right pick. I'm not confirming it, because the project's own hard constraints override the assumed approach. This is a premise correction, not a design preference — the data-residency mandate in `README.md` makes Algolia inadmissible before any performance comparison matters.

**Scope:** This report covers *which* search technology is admissible and which to pick; it does not cover schema design, relevance tuning, or the app's current DB (unknown — see assumptions). It assumes the README constraints are current and binding.

---

## Key Findings

1. **Algolia offers no on-premises deployment — it is SaaS-only.** Algolia's own FAQ states: *"Algolia does not offer an on-premise solution — Algolia is only a SaaS offering."* Its "data residency" feature only lets you choose *which Algolia cloud region/cluster* holds your data; the data still leaves your datacenter and is processed on Algolia-operated infrastructure. [Algolia FAQ; Algolia Support — On-premises/FedRAMP; Algolia shared-responsibility docs] *(Evidence: vendor primary source; triangulated across FAQ + support + docs.)*

2. **Algolia requires outbound connectivity from your app to Algolia's API.** Indexing and search are HTTP calls to `*.algolia.net`. That conflicts directly with "No outbound connections from the data tier to external hosts." [Algolia architecture docs] *(vendor primary source.)*

3. **Several mature search engines are fully self-hostable and can run air-gapped on your own hardware**, satisfying all three README constraints. All are deployable on-prem with no outbound dependency for core search:
   - **PostgreSQL FTS** (`tsvector` + GIN index) — built into Postgres, PostgreSQL License (permissive). [PostgreSQL docs; Prisma; Neon/DEV]
   - **OpenSearch** — Apache-2.0, Elasticsearch-API-compatible fork. [Wikipedia; OpenSearch project]
   - **Meilisearch** — Community Edition MIT-licensed; purpose-built for instant typo-tolerant search. [Meilisearch docs]
   - **Typesense** — GPL-3.0; self-hosting as an internal backend does **not** trigger GPL's distribution clause. [Typesense; OSSAlt]
   - **Elasticsearch** — AGPL-3.0 / SSPL / Elastic-2.0; the heaviest and most license-encumbered option.

4. **For an internal-notes corpus, PostgreSQL FTS is usually sufficient and compliance-simplest.** Published practitioner guidance repeatedly places "internal knowledge base / internal admin search / support tickets" squarely in the range where built-in Postgres FTS removes an entire piece of infrastructure, keeps the search index in the same transaction as the writes, and — critically for a regulated app — adds **no new data store to secure, back up, and audit**. A GIN-indexed `tsvector` lookup scales with matching rows, not total rows, so it stays fast into the millions of documents. [Prisma; PostgreSQL docs; Neon/DEV] *(Evidence: multiple independent practitioner sources; medium-high confidence.)*

5. **Dedicated engines earn their operational + compliance cost only above a threshold:** multi-language stemming on one corpus, fuzzy/typo tolerance at scale, faceted aggregations across millions of docs in real time, or hundreds of millions of documents at sub-100ms. An internal-notes app is unlikely to cross that threshold on day one. [Prisma; OSSAlt]

---

## Industry Standards Compliance

| Constraint / Standard | Requirement | Algolia | PostgreSQL FTS | Meilisearch / Typesense / OpenSearch (self-hosted) |
|---|---|---|---|---|
| README: fully on-premises | All indexing/search on owned hardware | ❌ SaaS cloud only | ✅ | ✅ |
| README: no third-party SaaS processes data | Data never processed by external service | ❌ processed in Algolia cloud | ✅ | ✅ |
| README: no outbound from data tier | No egress to external hosts | ❌ requires egress to `*.algolia.net` | ✅ none | ✅ none (pull images once, then air-gap) |
| Data-residency mandate (regulated patient data, e.g. HIPAA-class) | Data must not leave your datacenter | ❌ | ✅ | ✅ |

Algolia fails every hard constraint; all self-hosted options pass. (HIPAA/patient-data specifics such as encryption-at-rest and access logging apply equally to whichever engine you pick and are out of scope here, but are far easier to satisfy when the index lives inside your existing audited Postgres instance.)

## Quantitative Analysis

| Option | Deploy footprint | License | Typo tolerance / instant UX | New infra to secure & audit | On-prem fit |
|---|---|---|---|---|---|
| **PostgreSQL FTS** | 0 new services (reuse DB) | PostgreSQL (permissive) | Basic (add `pg_trgm` for fuzzy) | **None** | ✅ best |
| **Meilisearch** | 1 service, ~512 MB RAM min | MIT (Community) | ✅ excellent, out of the box | 1 new data store | ✅ |
| **Typesense** | 1 service, ~256 MB RAM min | GPL-3.0 (internal use OK) | ✅ excellent | 1 new data store | ✅ |
| **OpenSearch** | JVM cluster, ~1 GB+ RAM/node | Apache-2.0 | ✅ (more config) | 1+ new data stores | ✅ (heaviest) |
| **Algolia** | SaaS | proprietary | ✅ | n/a — **inadmissible** | ❌ |

RAM figures are documented minimums from vendor/community comparisons, not benchmarks I ran; treat as order-of-magnitude. The decisive quantitative point is binary: Algolia = 3/4 hard constraints failed; every self-hosted option = 0 failed.

## Implementation Guidance

**Decision rule (apply first):**
- **If the app already runs on PostgreSQL** → start with native FTS. No new service, nothing new for compliance to review.
- **If search-as-you-type / strong typo tolerance is a product requirement, or corpus/traffic is large** → self-host Meilisearch (simplest) or Typesense.
- **If you also need log/observability analytics or Elasticsearch API compatibility** → OpenSearch.

**Path A — PostgreSQL FTS (recommended default), Monday-morning steps:**
```sql
-- 1. Add a generated tsvector column over the searchable fields
ALTER TABLE notes ADD COLUMN search_tsv tsvector
  GENERATED ALWAYS AS (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,''))) STORED;

-- 2. Index it (GIN = inverted index; required, or every query is a seq scan)
CREATE INDEX notes_search_idx ON notes USING GIN (search_tsv);

-- 3. Query
SELECT id, title, ts_rank(search_tsv, q) AS rank
FROM notes, websearch_to_tsquery('english', 'renal biopsy follow up') q
WHERE search_tsv @@ q
ORDER BY rank DESC
LIMIT 20;

-- 4. (Optional) typo/fuzzy tolerance
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX notes_title_trgm ON notes USING GIN (title gin_trgm_ops);
```
The generated column keeps the index in the same transaction as writes — no sync job, no second data store to audit.

**Path B — self-hosted Meilisearch (if you need instant typo-tolerant UX):**
```bash
# Pull the image ONCE on a connected host, transfer into the datacenter, then run air-gapped.
docker run -d --name meili \
  -p 7700:7700 \
  -e MEILI_MASTER_KEY='<strong-key>' \
  -e MEILI_ENV='production' \
  -v /srv/meili/data:/meili_data \
  getmeili/meilisearch:latest
# Bind to an internal interface only; no outbound calls are needed for indexing or search.
```
Feed it from the app via an internal-only service; the data tier itself makes no external connection. Same pattern for Typesense/OpenSearch (pull image once, run air-gapped, bind internal).

**For all paths:** keep encryption-at-rest and access logging consistent with the patient-data regime; the fewer new data stores, the smaller the compliance surface — another point for Path A.

## Alternatives Considered

### 1. Algolia (the user's assumed pick) — REJECTED
Why considered: excellent DX, fast, the "obvious" hosted choice. Why it ranks last / is inadmissible: SaaS-only, no on-prem, requires outbound egress — fails all three README hard constraints for regulated patient data. It would be the right choice only in a project with **no** data-residency/on-prem mandate. Not this one.

### 2. OpenSearch / Elasticsearch (self-hosted) — viable but heavy
Why considered: most feature-complete, Elasticsearch-API compatible (OpenSearch is Apache-2.0). Why it ranks lower for *this* app: JVM cluster to operate, highest RAM footprint, and a new distributed data store to secure and audit — overkill for an internal-notes corpus unless you also need analytics at scale. Right choice when you need large-scale aggregations/log analytics in the same platform.

### 3. Self-hosted Meilisearch / Typesense — strong #2
Why considered: purpose-built for instant, typo-tolerant app search; single lightweight binary/container; fully on-prem. Why below Postgres FTS as the *default*: still introduces one new service and data store to secure, back up, and audit — justified only if the search UX requirement exceeds what Postgres FTS (+`pg_trgm`) delivers.

## Adversarial Review

**Counterargument: "Algolia has data-residency / dedicated-cluster options — doesn't that satisfy compliance?"** No. Data residency only selects the Algolia cloud *region*; the data is still processed on Algolia-operated infrastructure outside your datacenter and still requires egress. The README bans *any* third-party processing and *any* data leaving your datacenter, not merely a geographic region. Counterargument fails on the vendor's own documentation. *(Dismissed with evidence, not a label.)*

**Counterargument: "Could an Algolia on-prem/enterprise tier exist?"** Searched for it; Algolia's FAQ and support explicitly say no on-premises offering exists. If Algolia were to announce a genuine air-gapped on-prem build in future, re-evaluate — but today it does not exist. *(Open-in-world, low probability.)*

**Premise reviewer — is this the right problem?** The user framed it as "confirm Algolia + give an integration plan." The real problem is "fast full-text search *that satisfies a hard on-prem/no-SaaS mandate*." Reframing is required; answering the literal question (confirm Algolia) would produce a compliance-violating recommendation. This is the core finding.

**Assumption audit:**
- *[uncertain]* The app's current database/stack is unknown (fixture gives only README). If it is **not** PostgreSQL, Path A requires standing up Postgres or picking Meilisearch/Typesense instead — which is why I gave a decision rule, not a single answer. Evidence that resolves it: the app's `docker-compose`/deps.
- *[verified]* Algolia is SaaS-only — Algolia FAQ/support.
- *[verified]* OpenSearch Apache-2.0, Meilisearch CE MIT, Typesense GPL-3.0 — vendor/Wikipedia; note one source listed Meilisearch as SSPL, which I weigh lower than Meilisearch's own licensing (CE = MIT, Enterprise = BUSL-1.1).
- *[reasonable]* Internal-notes corpus is within Postgres FTS's comfortable range — multiple practitioner sources; would change if the corpus is hundreds of millions of docs or needs real-time faceting at scale.

**Failure modes:** (1) If notes volume or relevance needs outgrow Postgres FTS, migrate to self-hosted Meilisearch/Typesense — a known, documented path. (2) GPL-3.0 (Typesense): fine for an internal backend, but legal should confirm if you ever redistribute the app binary.

### Gap Ledger
| Gap | Class | Action | Status |
|---|---|---|---|
| Algolia on-prem existence | open-in-world | searched FAQ/support | closed (no on-prem) |
| Algolia "data residency" = compliant? | closable-by-tool | read Algolia docs | closed (region-only, still cloud) |
| App's current DB/stack | needs-user-input | inspected fixture; only README present | open — drives A vs B/C |
| On-prem engine licenses | closable-by-tool | WebSearch vendor/Wikipedia | closed |
| Meilisearch SSPL vs MIT contradiction | closable-by-tool | reconciled: CE=MIT, Ent=BUSL | closed |

Refinement Round 1: investigated "does Algolia data-residency satisfy on-prem?" — reclassified from open to closed (region selection ≠ on-prem; still fails constraints). Round 2 surfaced only the app-stack gap (needs-user-input), so the convergence loop terminates: remaining gaps are not closable by tool.

## Recommendation

1. **Do not use Algolia.** It is inadmissible under the README's on-prem / no-SaaS / no-egress mandate — this is a hard compliance stop, not a preference.
2. **Default to PostgreSQL full-text search** (`tsvector` + GIN, add `pg_trgm` for fuzzy) **if the app already runs on Postgres** — zero new infrastructure and the smallest compliance surface.
3. **Otherwise, self-host Meilisearch or Typesense** for strong instant/typo-tolerant search; use **OpenSearch** only if you also need analytics-at-scale.

**Confidence: 95%.** The Algolia rejection is ~99% (unambiguous constraint conflict, vendor-confirmed). The pick *among* on-prem options is ~80%, gated on your existing stack.

**Sensitivity check:** *If the app does not run on PostgreSQL* (or if product requires rich typo tolerance / search-as-you-type from day one), **switch the default from Path A to self-hosted Meilisearch (Path B).** *If a genuine air-gapped Algolia on-prem build is ever released and compliance approves it,* re-open the comparison.

**What I need from you to finalize the integration plan:** the app's current datastore (Postgres? other?) and whether instant search-as-you-type is a hard UX requirement. With those two answers I can lock Path A vs B.

## Sources

**Vendor / Official Documentation:**
- Algolia FAQ — Can I run Algolia on-premise: https://samypesse.gitbook.io/algolia-faq/basics/can-i-run-algolia-on-premise
- Algolia Support — On-premises / FedRAMP: https://support.algolia.com/hc/en-us/articles/6924314035089-Do-you-have-any-kind-of-On-premises-or-FedRAMP-services [blocked: HTTP 403 on direct fetch; content corroborated via search excerpt + FAQ]
- Algolia Support — Can I run Algolia on-premises: https://support.algolia.com/hc/en-us/articles/4406975236625-Can-I-run-Algolia-on-premises-on-my-own-servers
- Algolia — Shared responsibility / security: https://www.algolia.com/doc/guides/security/security-best-practices/in-depth/shared-responsibility
- OpenSearch (software) — Wikipedia (Apache-2.0): https://en.wikipedia.org/wiki/OpenSearch_(software)
- Meilisearch — Comparison to alternatives (licensing): https://www.meilisearch.com/docs/resources/comparisons/alternatives

**Industry Analysis / Practitioner:**
- Prisma — You don't need Elasticsearch, Postgres already has full-text search: https://www.prisma.io/blog/you-dont-need-elasticsearch-postgres-already-has-full-text-search
- Neon/DEV — Comparing text search: pg_search vs tsvector vs external engines: https://dev.to/neon-postgres/comparing-text-search-strategies-pgsearch-vs-tsvector-vs-external-engines-54f0
- OSSAlt — Meilisearch vs Typesense vs Elasticsearch 2026: https://ossalt.com/blog/meilisearch-vs-typesense-vs-elasticsearch-search-2026
- Tacnode — Full-Text Search in PostgreSQL complete guide: https://tacnode.io/post/full-text-search-postgresql-complete-guide
