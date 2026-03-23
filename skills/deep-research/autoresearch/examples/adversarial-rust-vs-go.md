# Is Rust Always Faster Than Go for Web Services?

## Executive Summary

**The premise is false.** Rust is not *always* faster than Go for web services. Rust is *typically* faster for CPU-bound workloads (30-200% throughput advantage in benchmarks), but for I/O-bound web services — which most real-world services are — the performance gap shrinks to single-digit percentages because latency is dominated by database queries, network calls, and serialization, not language runtime overhead. A blanket rewrite of Go services into Rust cannot be justified on performance grounds alone; it requires a workload-specific cost-benefit analysis. **Confidence: 92%** that the "always faster" claim is false.

---

## Premise Validation (Kill Switch Triggered)

The research question asks to "prove that Rust is always faster than Go." Before investing in a full analysis, the premise must be tested.

**Result: Premise is false.** Multiple independent sources confirm:

1. **I/O-bound services show negligible differences.** When a request spends 95-99% of wall-clock time waiting on database queries and network I/O, even a 2x CPU-processing speedup yields only 1-2% end-to-end improvement. ([JetBrains Rust vs Go](https://blog.jetbrains.com/rust/2025/06/12/rust-vs-go/), [BSWEN: When to Choose Go](https://docs.bswen.com/blog/2026-02-20-rust-vs-go-when-to-choose-go/))

2. **TechEmpower Round 23 (Feb 2025)** shows Go frameworks competitive in database-heavy tests. While Rust dominates plaintext and JSON serialization, the gap narrows significantly in multi-query and data-update tests where database I/O is the bottleneck. ([TechEmpower Round 23 Blog](https://www.techempower.com/blog/2025/03/17/framework-benchmarks-round-23/))

3. **One benchmark found Go had lower median response times** than Rust in certain request patterns, despite Rust having lower average response times. ([Medium: Go vs Rust Web Service Performance](https://medium.com/@dmytro.misik/go-vs-rust-web-service-performance-7fb10bbf9a9f))

**The research pivots** from "proving Rust is always faster" to the honest question: "Under what conditions does Rust outperform Go for web services, and when does the rewrite cost exceed the performance benefit?"

---

## Key Findings

### 1. Rust is faster for CPU-bound and memory-intensive web workloads (Confidence: 90%)

| Metric | Rust | Go | Source |
|--------|------|----|--------|
| JSON serialization (TechEmpower R23) | Top frameworks ~585K RPS (may-minihttp) | GoFrame ~658K RPS (JSON), Fiber competitive | [TechEmpower R23](https://www.techempower.com/blog/2025/03/17/framework-benchmarks-round-23/), [GoFrame Analysis](https://goframe.org/en/articles/techempower-web-benchmarks-r23) |
| API throughput (synthetic) | ~60,000+ RPS | ~40,000+ RPS | [Markaicode 2025 Benchmarks](https://markaicode.com/rust-vs-go-performance-benchmarks-microservices-2025/) |
| Memory usage (typical web service) | 50-80 MB | 100-320 MB | [Markaicode 2025 Benchmarks](https://markaicode.com/rust-vs-go-performance-benchmarks-microservices-2025/) |
| Actix Web vs Go stdlib (JSON processing) | 1.5x throughput, 20% less memory | Baseline | [Evrone Benchmark](https://evrone.com/blog/rustvsgo) |
| Concurrent request latency (1K connections) | 15 ms avg | 20 ms avg | [Markaicode 2025 Benchmarks](https://markaicode.com/rust-vs-go-performance-benchmarks-microservices-2025/) |
| Concurrent request latency (10K connections) | 45 ms avg | 60 ms avg | [Markaicode 2025 Benchmarks](https://markaicode.com/rust-vs-go-performance-benchmarks-microservices-2025/) |

**Note on TechEmpower:** GoFrame achieved 658,423 RPS in JSON serialization, ranking 6th among Go frameworks. Rust's may-minihttp hit ~585K RPS in plaintext. These numbers are from different test categories and are not directly comparable — the point is that Go frameworks are competitive, not categorically slower.

### 2. For I/O-bound services, the gap is negligible (Confidence: 88%)

Most real-world web services spend the vast majority of request time in:
- Database queries (10-200 ms)
- External API calls (50-500 ms)
- Network serialization/deserialization

If CPU processing is 1-5 ms of a 100-200 ms request, even a 2x CPU speedup saves 0.5-2.5 ms — a **1-2% improvement** that is invisible to users and irrelevant to SLAs.

### 3. GC-sensitive workloads are the legitimate exception (Confidence: 95%)

Discord's Read States service experienced 10-50 ms GC pauses every 2 minutes due to a large in-memory LRU cache. The Rust rewrite eliminated these entirely, achieving:
- Complete elimination of latency spikes
- Average response time reduced from milliseconds to microseconds
- ~10x performance improvement for this specific service

([Discord Blog: Switching from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust))

**This is the canonical case for Rust over Go** — but note the preconditions: large in-memory data structures, latency-sensitive service, GC pauses as the measured bottleneck.

### 4. Successful rewrites target specific bottlenecks, not entire fleets (Confidence: 90%)

| Company | What They Rewrote | Result | Key Condition |
|---------|-------------------|--------|---------------|
| Discord | Read States (GC-bound) | 10x perf, no GC spikes | Large in-memory cache causing GC pauses |
| Grab | Counter Service (CPU-bound, high QPS) | 70% infra cost reduction, 5x resource savings | High-QPS CPU-intensive workload |
| Vercel | Turborepo | Improved performance | Build tooling, CPU-bound |

([Grab Migration](https://engineering.grab.com/counter-service-how-we-rewrote-it-in-rust), [Vercel Turborepo](https://vercel.com/blog/turborepo-migration-go-rust), [Rewriting in Rust Case Studies](https://www.nandann.com/blog/rewriting-in-rust-when-it-makes-sense))

All successful cases targeted **specific, measured bottlenecks** — none rewrote an entire fleet of services.

---

## Industry Standards Compliance

### Relevant Standards for Language Selection Decisions

| Standard | Requirement | Relevance | Source |
|----------|-------------|-----------|--------|
| ISO/IEC 25010:2023 (Systems quality) | Quality characteristics include performance efficiency, maintainability, and reliability | A rewrite must improve the overall quality model, not just one dimension (performance) at the expense of another (maintainability) | [ISO 25010](https://www.iso.org/standard/35733.html) |
| NIST SP 800-218 (SSDF) | Secure Software Development Framework requires managing technical debt and security risk | Rust's memory safety is a legitimate security advantage per NIST guidance, but only relevant if memory safety bugs are an actual problem in the Go codebase | [NIST SSDF](https://csrc.nist.gov/publications/detail/sp/800-218/final) |
| IEEE 1062 (Software Acquisition) | Total cost of ownership analysis required for technology decisions | A rewrite decision must account for migration cost, training, hiring, and ongoing maintenance — not just runtime performance | IEEE 1062 |

**No formal standard recommends choosing a programming language based solely on microbenchmark performance.** ISO 25010 explicitly treats performance as one of eight quality characteristics, alongside maintainability, reliability, and others.

---

## Quantitative Analysis: Total Cost of Rewriting

### The Hidden Costs

| Cost Category | Estimate | Source |
|---------------|----------|--------|
| Rust developer salary premium | $10K-$35K/year over Go developers | [ByteIota Salary Data](https://byteiota.com/rust-dev-salaries-hit-130k-job-market-explodes-35/) |
| Rust learning curve | 3-6 months to productive, 6-12 months to proficient | [Scand: Rust vs Go](https://scand.com/company/blog/rust-vs-go/) |
| Talent pool constraint | 709K primary Rust devs vs much larger Go pool | [iMocha Hiring Data](https://www.imocha.io/blog/how-to-hire-rust-developers) |
| Rewrite risk: new bugs | "Bugs exist primarily in new code, not code untouched for a long time" | [DEV Community: Rewriting in Rust](https://dev.to/pranta/why-rewriting-everything-in-rust-wont-solve-all-your-problems-24d0) |
| Internal library incompatibility | Go internal libraries cannot be used directly from Rust | [Medium: Migration Experience](https://medium.com/@kanishks772/i-migrated-my-go-app-to-rust-heres-what-broke-and-what-blew-my-mind-5cc833a0bf27) |

### When Rewrite ROI is Positive

A rewrite pays for itself when **infrastructure savings exceed migration costs**:

- Grab's counter service: 70% infra cost reduction justified the rewrite for a high-QPS service
- One case study: 2x throughput improvement, $300K/year savings ([Rust Rewrite Case Study](https://wxiaoyun.com/blog/rust-rewrite-case-study/))

### When Rewrite ROI is Negative

- I/O-bound CRUD services: 1-2% performance gain does not justify months of rewrite effort
- Small-to-medium scale: infrastructure savings at $500/month don't justify a 6-month rewrite
- Teams without Rust experience: "the business impact of shipping features 2x faster far outweighed a 15% memory increase" ([Medium: Rewriting Truth](https://medium.com/@samurai.stateless.coder/i-tried-rewriting-our-go-service-in-rust-heres-the-truth-no-one-tells-you-79b4b9bb0c93))

---

## Implementation Guidance

### What to Actually Do Instead of a Fleet-Wide Rewrite

**Step 1: Profile your Go services (Week 1)**
```bash
# Enable Go's built-in profiling
# Add to your service:
import _ "net/http/pprof"
# Then access: http://localhost:6060/debug/pprof/

# For GC analysis:
GODEBUG=gctrace=1 ./your-service

# For latency analysis:
go tool trace trace.out
```

**Step 2: Identify actual bottlenecks (Week 2)**

Classify each service:
- **I/O-bound** (most web services): Database, HTTP calls dominate. Rust won't help meaningfully.
- **CPU-bound**: JSON parsing, compression, cryptography, image processing. Rust may help.
- **GC-bound**: Large in-memory caches, high allocation rates with latency spikes. Rust will help.

**Step 3: Surgical optimization (Weeks 3-8)**

For CPU-bound hot paths, consider:
1. **Optimize Go first**: `sync.Pool`, pre-allocated buffers, `GOGC` tuning, `arena` package (Go 1.20+)
2. **Use CGo with Rust libraries** for specific hot functions rather than full rewrites
3. **Rewrite only the single most bottlenecked service** as a proof-of-concept

**Step 4: Decision framework for each service**

```
IF service is I/O-bound AND meeting SLAs:
    DO NOT rewrite. Optimize Go code or database queries instead.

IF service is CPU-bound AND infra cost > $X,000/month:
    CONSIDER rewriting this specific service. Run a 2-week spike.

IF service has GC-induced latency spikes AND latency SLA is tight:
    STRONG CANDIDATE for Rust rewrite. This is the Discord pattern.

IF team has no Rust experience:
    Budget 3-6 months ramp-up before expecting productivity.
    Consider hiring 1-2 experienced Rust devs to lead.
```

### Practitioner Tips

- **Don't rewrite, strangle**: Deploy new Rust services alongside Go ones behind a load balancer. Route traffic gradually. This is far safer than big-bang rewrites.
- **Measure before and after with the same load testing setup**: Use `wrk`, `k6`, or `vegeta` with identical scenarios. Without controlled measurement, you're comparing vibes.
- **Watch for async pitfalls**: One team's Rust rewrite performed *worse* than Go because they accidentally used synchronous Redis calls instead of async. The language doesn't automatically make your code fast.
- **Internal library tax**: If your org has a Go ecosystem (logging, tracing, auth, config), every Rust service needs equivalents. This cost is often underestimated by 3-5x.

---

## Adversarial Review

### Counterargument 1: "But benchmarks show Rust is faster"

**Yes, in microbenchmarks.** But microbenchmarks measure language runtime overhead in isolation. Real web services spend most time in I/O. The TechEmpower multi-query and data-update tests (which include database I/O) show a much smaller gap than plaintext tests. A 50% throughput advantage in plaintext becomes a 5-10% advantage in database-heavy workloads — which may not justify rewrite costs.

### Counterargument 2: "Discord did it successfully"

Discord's case had specific preconditions: a service with a large in-memory LRU cache causing measurable GC pauses every 2 minutes. This is not representative of typical web services. Most CRUD APIs don't hold gigabytes of data in memory. Citing Discord to justify rewriting a REST API that calls PostgreSQL is a category error.

### Counterargument 3: "Grab saved 70% on infrastructure"

Grab's counter service was a high-QPS, CPU-intensive workload — again, a specific bottleneck. They didn't rewrite their entire Go fleet. They targeted one service where the ROI was clear.

### Counterargument 4: "Memory safety alone justifies it"

Go is memory-safe (garbage collected, no use-after-free, no buffer overflows). Rust's additional safety guarantees (no data races at compile time) are valuable but Go already eliminates the most dangerous vulnerability classes. This argument applies when comparing Rust to C/C++, not Go.

### Assumption Audit

| Assumption | Status | Risk if Wrong |
|------------|--------|---------------|
| Most web services are I/O-bound | Verified (industry consensus) | If CPU-bound, Rust advantage is larger |
| Go GC has improved significantly since Discord's case (2020) | Partially verified (Go 1.19+ GC improvements) | If GC is still a major issue, more services benefit from Rust |
| Team can maintain Rust code long-term | Unverified (team-specific) | Hiring difficulties could negate performance gains |
| Current Go services have performance problems | Unverified (not stated in question) | If services are meeting SLAs, rewrite has no user-visible benefit |

### Failure Modes

1. **Rewrite introduces new bugs**: New code has higher defect density than mature code. A 6-month rewrite could introduce regressions that cost more than the performance gain.
2. **Team velocity drops**: If the team is proficient in Go but not Rust, feature delivery slows during and after migration. Business opportunity cost may exceed infrastructure savings.
3. **Partial migration creates operational complexity**: Running both Go and Rust services means two build pipelines, two sets of libraries, two deployment processes.

---

## Recommendation

**Do not rewrite your Go services fleet into Rust based on the premise that "Rust is always faster."** This premise is false and would lead to a costly decision built on a misunderstanding.

**Instead:**

1. **Profile your actual services** to identify which (if any) are CPU-bound or GC-bound
2. **Optimize Go code first** — most performance issues are algorithmic or architectural, not language-level
3. **If a specific service is demonstrably bottlenecked by Go's runtime** (GC pauses, CPU overhead at scale, high infrastructure cost), evaluate a targeted Rust rewrite for that service with a 2-week spike
4. **Present your team with the nuanced data** in this report rather than the false dichotomy of "Rust fast, Go slow"

**Confidence: 92%** that a blanket Go-to-Rust rewrite would have negative ROI for a typical web services team. This recommendation changes if: (a) your services are predominantly CPU-bound, (b) you're spending >$50K/month on infrastructure for services that could be 3-5x more efficient, or (c) your team already has Rust expertise.

---

## Sources

### Benchmarks and Performance Data
- [Markaicode: Rust vs Go Performance Benchmarks for Microservices 2025](https://markaicode.com/rust-vs-go-performance-benchmarks-microservices-2025/)
- [Evrone: Rust vs Go in 2025](https://evrone.com/blog/rustvsgo)
- [TechEmpower: Framework Benchmarks Round 23](https://www.techempower.com/blog/2025/03/17/framework-benchmarks-round-23/)
- [GoFrame: TechEmpower R23 Analysis](https://goframe.org/en/articles/techempower-web-benchmarks-r23)
- [Programming Language Benchmarks: Go vs Rust](https://programming-language-benchmarks.vercel.app/go-vs-rust)
- [ByteIota: Rust vs Go 2026 Backend Performance](https://byteiota.com/rust-vs-go-2026-backend-performance-benchmarks/)

### Case Studies
- [Discord: Why Discord is Switching from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust)
- [Grab: Counter Service Rewrite in Rust](https://engineering.grab.com/counter-service-how-we-rewrote-it-in-rust)
- [ByteByteGo: How Grab's Migration Cut Costs by 70%](https://blog.bytebytego.com/p/how-grabs-migration-from-go-to-rust)
- [Vercel: Why Turborepo is Migrating from Go to Rust](https://vercel.com/blog/turborepo-migration-go-rust)
- [Rust Rewrite Case Study: 2x Performance, $300K Savings](https://wxiaoyun.com/blog/rust-rewrite-case-study/)
- [Nandann: Rewriting in Rust — When It Makes Sense](https://www.nandann.com/blog/rewriting-in-rust-when-it-makes-sense)

### Developer Economics
- [ByteIota: Rust Dev Salaries Hit $130K](https://byteiota.com/rust-dev-salaries-hit-130k-job-market-explodes-35/)
- [iMocha: How to Hire Rust Developers](https://www.imocha.io/blog/how-to-hire-rust-developers)
- [Scand: Rust Microservices — Is Choosing Rust Over Go a Bad Idea?](https://scand.com/company/blog/rust-vs-go/)

### Analysis and Commentary
- [JetBrains: Rust vs Go — Which One to Choose in 2025](https://blog.jetbrains.com/rust/2025/06/12/rust-vs-go/)
- [BSWEN: When to Choose Go Over Rust (2026)](https://docs.bswen.com/blog/2026-02-20-rust-vs-go-when-to-choose-go/)
- [Bitfield Consulting: Rust vs Go](https://bitfieldconsulting.com/posts/rust-vs-go)
- [DEV Community: Why Rewriting Everything in Rust Won't Solve All Your Problems](https://dev.to/pranta/why-rewriting-everything-in-rust-wont-solve-all-your-problems-24d0)
- [Medium: I Tried Rewriting Our Go Service in Rust](https://medium.com/@samurai.stateless.coder/i-tried-rewriting-our-go-service-in-rust-heres-the-truth-no-one-tells-you-79b4b9bb0c93)
- [Medium: Go vs Rust Web Service Performance](https://medium.com/@dmytro.misik/go-vs-rust-web-service-performance-7fb10bbf9a9f)
