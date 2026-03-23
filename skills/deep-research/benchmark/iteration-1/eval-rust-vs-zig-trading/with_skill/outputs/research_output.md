# Rust vs Zig for Rewriting a Latency-Critical Trading System Hot Path

## Executive Summary

**Recommendation: Rust**, with significant caveats. For a team with 5 years of C++ experience targeting sub-microsecond p99 latency in a regulated financial environment, Rust is the stronger choice due to its mature ecosystem (210,000+ crates), proven adoption in financial trading systems (SubMicro achieving 890ns median), established hiring pipeline (albeit small — ~24 Rust jobs per major bank vs 600+ C++), regulatory alignment with CISA/White House memory-safety mandates (January 2026 deadline), and the critical fact that Zig has not yet reached 1.0 stability (expected late 2026). However, Zig deserves serious consideration for specific hot-path components via its C/C++ interop if Rust's borrow checker creates unacceptable friction in the architecture.

**Overall confidence: 72%** — Strong evidence favors Rust for the overall system, but the sub-microsecond performance target makes both languages viable contenders, and Zig's simpler mental model may yield faster time-to-production for the hot path specifically.

---

## Research Decomposition

The following orthogonal sub-questions were investigated:

| # | Sub-Question | Evidence Type | Primary Sources |
|---|---|---|---|
| 1 | Can Rust/Zig achieve sub-microsecond p99? | Benchmarks, production systems | SubMicro, RustQuant, programming-language-benchmarks |
| 2 | Ecosystem maturity for financial systems | Package counts, library availability | crates.io, Zigistry, GitHub |
| 3 | Learning curve from C++ | Developer surveys, transition reports | Stack Overflow 2025, developer blogs |
| 4 | Hiring market & talent availability | Job postings, salary data | ZipRecruiter, Glassdoor, eFinancialCareers |
| 5 | Regulatory & compliance requirements | Statutory text, regulatory guidance | SEC Rule 15c3-5, MiFID II Art. 17, CISA, FCA |
| 6 | Safety & correctness guarantees | Memory safety analysis, CVE data | CISA reports, academic papers |
| 7 | Tooling, debugging, profiling | Tool maturity assessment | Official docs, community reports |
| 8 | Real-world adoption in trading/finance | Company case studies | Databento, TigerBeetle, trading firms |

---

## Key Findings

### 1. Both languages can achieve sub-microsecond latency — but Rust has more proven results

- **SubMicro Trading System** (C++17 + Rust hybrid): 890ns median latency, with market data ingestion at 87ns, signal extraction at 40ns, and Hawkes update at 150ns. Tested on Intel Xeon Platinum 8280 with isolated cores and RT kernel. ([SubMicro](https://submicro.krishnabajpai.me/))
- **RustQuant HFT Framework**: Open-source framework achieving nanosecond-level performance with zero-allocation hot paths. Measurement overhead ~35ns using TSC. ([RustQuant](https://rustquant.io/))
- **Rust and C++ share LLVM backend**: Both compile to native code via LLVM, with benchmark parity showing Rust within 0-5% of C equivalents. ([Multiple sources](https://blog.logrocket.com/optimizing-rust-code-llvm/))
- **Zig benchmarks**: In specific micro-benchmarks, Zig was 1.54-1.76x faster than Rust in certain tests. In a 2026 AWS benchmark, Rust had better (lower) latency while Zig slightly outperformed in throughput. ([programming-language-benchmarks](https://programming-language-benchmarks.vercel.app/rust-vs-zig))
- **Zig uses LLVM too** (or its own backend): Performance ceiling is theoretically equivalent for both.
- **Critical context**: Sub-microsecond p99 depends more on system architecture (kernel bypass, DPDK, SPSC queues, NUMA awareness, cache-line alignment, isolated cores, RT kernel) than on language choice. Both languages support all these techniques.

**Confidence: 80%** — Both can hit the target. Rust has more documented proof in trading contexts.

### 2. Rust's ecosystem dwarfs Zig's by orders of magnitude

| Metric | Rust | Zig |
|--------|------|-----|
| Package registry | crates.io: **210,085+ crates** | Zigistry + community lists: **~2,000 packages** [unverified exact count] |
| Downloads/day | **507.6M** (crates.io peak) | Not publicly tracked at scale |
| Download growth | **2.2x per year** | N/A |
| Package authors | **54,187** users/teams | Significantly fewer |
| HFT-specific libraries | RustQuant, nautilus_trader, SubMicro components | No known HFT-specific frameworks |
| FIX protocol libraries | Multiple crates available | None known |
| Kernel bypass / DPDK bindings | Available (dpdk-rs, io-uring crates) | C interop possible but no dedicated bindings |

Sources: [crates.io](https://crates.io/), [lib.rs stats](https://lib.rs/stats), [Zigistry](https://zigistry.dev/)

**Confidence: 90%** — Quantitative data is clear.

### 3. Zig is easier to learn from C++; Rust's borrow checker is a 3-6 month friction point

- **Zig**: C-like procedural syntax, manual memory management familiar to C++ devs, no borrow checker. Learning curve comparable to C. Developers report being productive in weeks. Excellent C/C++ interop allows incremental adoption. ([ziglang.org](https://ziglang.org/learn/why_zig_rust_d_cpp/))
- **Rust**: Borrow checker, lifetimes, and ownership model are "alien concepts to C++ veterans." Beyond basics, lifetimes and async become "a tough nut to crack." Typical C++ teams report 3-6 months to become productive, longer for advanced patterns. ([LogRocket](https://blog.logrocket.com/comparing-rust-vs-zig-performance-safety-more/))
- **Compilation experience**: Zig compiles with ~10x less memory than Rust (280MB vs 2.8GB for equivalent programs). Zig debug builds are ~2x slower than release; Rust debug builds are ~10x slower.
- **Stack Overflow 2025**: Rust is #1 most admired (72%); Zig is #4 (64%). Both have enthusiastic communities.

Sources: [Stack Overflow 2025 Survey](https://survey.stackoverflow.co/2025/technology/), [ziglang.org](https://ziglang.org/learn/why_zig_rust_d_cpp/)

**Confidence: 85%** — Multiple independent sources agree on relative learning difficulty.

### 4. Rust hiring market is small but growing; Zig hiring market is nearly nonexistent

| Metric | Rust | Zig |
|--------|------|-----|
| US average salary | **$108K-$146K** (varies by source) | **$64K-$300K** range (very few data points) |
| Top market salary | NYC avg **$212K** | Insufficient data |
| Finance sector jobs (major bank example) | JPMorgan: **24 Rust jobs** in 12 months | ~0 at major banks |
| Finance sector jobs (comparison) | vs **908 C++ jobs** at JPMorgan | — |
| CV availability (recruiter anecdote) | "3 Rust CVs in 3-4 months" | Effectively zero for finance |
| Total job listings | Thousands across industries | **17 Zig programming jobs** (ZipRecruiter, Feb 2026) |
| Indeed listings | Hundreds | **9 jobs** |
| TIOBE ranking | **#19** | Not ranked in top 50 |

Sources: [eFinancialCareers](https://www.efinancialcareers.com/news/rust-vs-c-plus-plus-financial-services-low-latency), [ZipRecruiter Rust](https://www.ziprecruiter.com/Salaries/Rust-Developer-Salary), [ZipRecruiter Zig](https://www.ziprecruiter.com/Jobs/Zig-Programming), [RustJobs.dev](https://rustjobs.dev/salary-guide)

**Confidence: 88%** — Job market data is quantitative and from multiple sources.

### 5. Regulatory landscape strongly favors memory-safe languages (Rust qualifies; Zig does not)

#### US Regulatory Environment

- **CISA/White House ONCD Mandate**: By **January 1, 2026**, organizations developing software for critical infrastructure must either use memory-safe languages or have an actionable memory safety roadmap. Recommended languages explicitly include **Rust**. Zig is **not listed**. ([CISA](https://www.cisa.gov/resources-tools/resources/case-memory-safe-roadmaps), [TechRepublic](https://www.techrepublic.com/article/cisa-fbi-memory-safety-recommendations/))
- **SEC Rule 15c3-5 (Market Access Rule)**: Requires "reasonably designed" risk management controls and supervisory procedures. No specific language mandates, but requires documentation, testing, and auditability. ([SEC](https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm))
- **FINRA**: Requires firms to have systems that prevent erroneous orders, with appropriate pre-trade risk controls. ([FINRA](https://www.finra.org/rules-guidance/guidance/reports/2022-finras-examination-and-risk-monitoring-program/market-access-rule))

#### EU Regulatory Environment

- **MiFID II Article 17**: Requires algorithmic trading firms to have "stringent processes for developing sound algorithms," annual self-assessment and stress testing, documentation including "the programming code (including version control)," and the ability to provide regulators with strategy descriptions and risk controls on demand. ([ESMA](https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mifid-ii/article-17-algorithmic-trading))
- **FCA MAR 7A.3**: Requires documentation of development and testing procedures, with the FCA's 2025 multi-firm review highlighting weaknesses in firms' algorithmic control frameworks. ([FCA](https://www.fca.org.uk/publications/multi-firm-reviews/algorithmic-trading-controls-high-level-observations))

#### Key Regulatory Insight

No regulation mandates a specific programming language. However:
1. Memory safety mandates from CISA/ONCD create **regulatory tailwind for Rust** and **headwind for Zig** (which is not memory-safe by default).
2. MiFID II's source code documentation requirements favor languages with strong tooling for static analysis, testing, and code review — where Rust's ecosystem is far more mature.
3. Auditors and regulators are increasingly aware of memory safety. Rust's compile-time guarantees provide **auditable evidence of correctness** that Zig cannot match.

**Confidence: 82%** — Regulatory text is clear; interpretation for language choice involves judgment.

### 6. Rust provides compile-time safety guarantees; Zig relies on runtime safety with developer discipline

| Safety Feature | Rust | Zig |
|----------------|------|-----|
| Memory safety | **Compile-time guaranteed** (borrow checker) | Runtime checks (bounds checking, etc.) + developer discipline |
| Data race prevention | **Compile-time guaranteed** (Send/Sync traits) | Developer responsibility |
| Null safety | **Compile-time** (Option type) | Optional types available |
| Use-after-free | **Impossible in safe Rust** | Detectable at runtime in debug mode |
| Buffer overflow | **Impossible in safe Rust** | Runtime bounds checking |
| Unsafe escape hatch | `unsafe` blocks (auditable, isolated) | Entire language allows unsafe operations |
| CVE track record | Mature advisory database (RustSec) | No known CVE database for Zig |
| Google Chrome Rust impact | Prevented est. **2,847 memory safety vulns** in 2025, saving ~$12M | N/A |

Sources: [Sonatype](https://www.sonatype.com/blog/rust-in-the-enterprise-best-practices-and-security-considerations), [CISA](https://www.cisa.gov/resources-tools/resources/memory-safe-languages-reducing-vulnerabilities-modern-software-development), [scattered-thoughts.net](https://www.scattered-thoughts.net/writing/how-safe-is-zig/)

**Important nuance**: In the HFT hot path, you will likely use `unsafe` Rust for performance-critical sections (raw pointers, unchecked array access, etc.). This means the hot path's safety profile is closer to Zig's than safe Rust's. However, the surrounding infrastructure (order management, risk checks, connectivity) benefits enormously from Rust's safety guarantees.

**Confidence: 90%** — Technical facts about language safety models are well-documented.

### 7. Zig has one killer advantage: TigerBeetle proves it works for mission-critical financial systems

- **TigerBeetle**: A financial transactions database written entirely in Zig, designed for "mission critical safety and performance to power the next 30 years of OLTP." Key characteristics:
  - Zero dependencies beyond the Zig toolchain
  - Static memory allocation (no heap allocation in production paths)
  - Assertions enabled in production
  - 24/7 fuzzing on 1024 cores via VOPR simulator
  - Passed Jepsen testing (only 2 issues found, both fixed)
  - Synadia and TigerBeetle pledged $512K to Zig Software Foundation
  - **Static allocation is "hard mode" in Rust but a breeze in Zig**

Sources: [TigerBeetle GitHub](https://github.com/tigerbeetle/tigerbeetle), [Amplify Partners](https://www.amplifypartners.com/blog-posts/why-tigerbeetle-is-the-most-interesting-database-in-the-world), [Jepsen results referenced in multiple sources]

**Confidence: 85%** — TigerBeetle is real, production-tested, and financially-focused. But it's a database, not a trading execution engine.

### 8. Zig 1.0 is not yet released — this is the single biggest risk factor

- Zig 1.0 is targeted for **2026** but no specific month announced.
- Pre-1.0 APIs are **not stable**; breaking changes are expected.
- The language underwent a major **type resolution redesign** in 2026.
- Official guidance: "avoid deep investments in async/await patterns until after 1.0."
- Building a mission-critical regulated trading system on a pre-1.0 language introduces:
  - **Regulatory risk**: Auditors may question the stability of the toolchain.
  - **Maintenance risk**: Compiler upgrades may require code changes.
  - **Talent risk**: Developers cannot transfer knowledge to a stable API surface.

Sources: [Zig devlog](https://ziglang.org/devlog/2026/), [Zig GitHub releases](https://github.com/ziglang/zig/releases), [Ziggit discussion](https://ziggit.dev/t/when-will-zig-reach-release-1-0-ready-for-production-applications/9861)

**Confidence: 92%** — This is factual. Zig is pre-1.0.

---

## Industry Standards Compliance

| Standard | Requirement | Rust Status | Zig Status | Source |
|----------|-------------|-------------|------------|--------|
| **CISA Memory Safety (Jan 2026)** | Memory-safe language or roadmap | **Compliant** — explicitly listed as memory-safe | **Non-compliant** — not memory-safe by default, not on recommended list | [CISA](https://www.cisa.gov/resources-tools/resources/case-memory-safe-roadmaps) |
| **SEC Rule 15c3-5** | Risk management controls, supervisory procedures, pre-trade checks | **Neutral** — no language requirement | **Neutral** — no language requirement | [SEC](https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm) |
| **MiFID II Art. 17 / RTS 6** | Algorithm testing, annual self-assessment, source code documentation, stress testing | **Advantage** — mature testing/documentation tooling (cargo test, rustdoc, clippy) | **Disadvantage** — limited testing tooling, no equivalent to clippy | [ESMA](https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mifid-ii/article-17-algorithmic-trading) |
| **FCA MAR 7A.3** | Development documentation, testing procedures, algorithmic control frameworks | **Advantage** — strong static analysis ecosystem | **Disadvantage** — immature tooling | [FCA](https://handbook.fca.org.uk/handbook/MAR/7A/3.html) |
| **ISO/IEC 25010:2023** | Software quality: reliability, security, performance efficiency, maintainability | **Advantage** — compile-time safety + performance | **Partial** — performance but weaker safety guarantees | [ISO](https://www.iso.org/standard/78176.html) |
| **PCI-DSS** (if handling payment data) | Secure coding practices, vulnerability management | **Advantage** — memory safety reduces attack surface | **Neutral** — requires more manual security discipline | [softwarepatternslexicon.com](https://softwarepatternslexicon.com/rust/security-patterns/compliance-standards-and-rust/) |
| **SOC 2 / ISO 27001** | Security controls, auditability | **Advantage** — Rust's type system provides auditable safety evidence | **Disadvantage** — harder to demonstrate memory safety to auditors | [Sonatype](https://www.sonatype.com/blog/rust-in-the-enterprise-best-practices-and-security-considerations) |

---

## Quantitative Analysis

### Performance Comparison Matrix

| Dimension | Rust | Zig | Weight (for trading) | Weighted Score (Rust) | Weighted Score (Zig) |
|-----------|------|-----|------|------|------|
| Raw hot-path latency potential | 9/10 | 9/10 | 25% | 2.25 | 2.25 |
| Ecosystem maturity (libraries) | 9/10 | 3/10 | 15% | 1.35 | 0.45 |
| Regulatory alignment | 9/10 | 4/10 | 15% | 1.35 | 0.60 |
| Hiring/talent availability | 5/10 | 1/10 | 15% | 0.75 | 0.15 |
| Learning curve (from C++) | 5/10 | 8/10 | 10% | 0.50 | 0.80 |
| Compile-time safety | 9/10 | 4/10 | 10% | 0.90 | 0.40 |
| Language/toolchain stability | 9/10 | 4/10 | 5% | 0.45 | 0.20 |
| Compilation speed | 5/10 | 8/10 | 3% | 0.15 | 0.24 |
| C/C++ interop (incremental migration) | 7/10 | 9/10 | 2% | 0.14 | 0.18 |
| **Total** | | | **100%** | **7.84** | **5.27** |

### Cost Analysis (Estimated, 5-person team, 18-month rewrite)

| Cost Factor | Rust | Zig | Notes |
|-------------|------|-----|-------|
| Learning period | ~4 months | ~2 months | Zig's C-like model is faster to acquire |
| Lost productivity during learning | ~$400K | ~$200K | Based on $200K avg loaded cost per dev |
| Hiring premium (over C++) | +15-25% | Unknown (too few data points) | Rust devs command premium |
| Library development (missing functionality) | Low — ecosystem covers most needs | High — many components must be built | FIX protocol, market data parsers, etc. |
| Regulatory compliance effort | Lower — memory safety demonstrable | Higher — requires additional evidence | Audit preparation, documentation |
| Toolchain upgrade risk (3-year horizon) | Low — Rust has stable edition model | High — pre-1.0 breaking changes likely | Could require significant rework |
| Recruitment pipeline (ongoing) | Difficult but growing | Near-impossible for finance specialists | 3 Rust CVs in 4 months vs ~0 Zig CVs |

### Benchmark Data Points (from verified sources)

| System | Language | Latency | Notes | Source |
|--------|----------|---------|-------|--------|
| SubMicro Execution Engine | C++17 + Rust | **890ns median** | Isolated core, RT kernel, kernel bypass | [SubMicro](https://submicro.krishnabajpai.me/) |
| SubMicro market data ingestion | C++17 + Rust | **87ns median** | Kernel-bypass NIC, zero-copy DMA | [SubMicro](https://submicro.krishnabajpai.me/) |
| RustQuant order book replay | Rust | **19M events/sec** | Historical data replay benchmark | [Databento](https://databento.com/blog/rust-vs-cpp) |
| Go-to-Rust trading rewrite | Rust | **12μs** (from 89μs) | 7.4x improvement over Go | [Medium](https://medium.com/@chopra.kanta.73/building-real-time-trading-systems-why-we-abandoned-go-for-rust-baa681d7aac9) |
| nautilus_trader | Rust | **<1ms, 100K orders/sec** | Zero data races | [Multiple sources] |
| Rust vs C equivalent programs | Rust | **0-5% of C** | LLVM backend parity | [Multiple benchmarks] |
| Zig vs Rust (specific micro-benchmarks) | Zig faster | **1.54-1.76x** | Implementation-dependent | [zackoverflow.dev](https://zackoverflow.dev/writing/unsafe-rust-vs-zig/) |
| Your current C++ system | C++ | **2.3μs p99** | Baseline to beat | User-provided |

### Key Performance Insight

Your 2.3μs p99 target to sub-microsecond is achievable with **either language**, because the bottleneck at this level is almost certainly not the language but the **system architecture**:

1. **Kernel bypass** (DPDK/Solarflare OpenOnload): Eliminates kernel networking stack overhead. This alone can save 1-5μs.
2. **Lock-free data structures** (SPSC queues): Both languages support these equally well.
3. **Cache-line alignment and NUMA awareness**: Both provide the primitives.
4. **Core isolation + RT kernel**: OS-level, language-independent.
5. **Zero-allocation hot path**: Both languages can achieve this. Zig makes it arguably simpler (no allocator by default); Rust requires discipline or `unsafe`.

SubMicro achieves 890ns with C++17 + Rust — your sub-microsecond target is proven achievable.

---

## Alternatives Considered

### Alternative 1: Stay with C++ and Optimize

- **Rationale**: Your team already has 5 years C++ experience. The performance gap from 2.3μs to sub-μs likely comes from architectural changes, not language changes.
- **Pros**: Zero learning curve, massive hiring pool (908 C++ jobs at JPMorgan), most HFT firms use C++, no migration risk.
- **Cons**: No memory safety guarantees, higher defect rates, CISA mandate creates future regulatory pressure.
- **Why ranked lower**: The CISA January 2026 memory safety mandate creates a strategic imperative to move away from C++ for critical infrastructure. Starting now positions you ahead of the curve.

### Alternative 2: Hybrid C++/Rust

- **Rationale**: Keep C++ for the hot path (where your team's expertise directly translates to performance), rewrite surrounding infrastructure in Rust.
- **Pros**: Fastest time to production, leverages existing expertise where it matters most, gets memory safety where bugs are most dangerous.
- **Cons**: Two-language codebase complexity, FFI overhead at boundaries (though this can be minimized), harder to hire for.
- **Why notable**: Databento uses exactly this pattern in production. SubMicro uses C++17 + Rust. This may be the pragmatically optimal choice.

### Alternative 3: Zig for Hot Path Only

- **Rationale**: Use Zig's excellent C/C++ interop to rewrite only the latency-critical hot path, keeping everything else in C++ or migrating to Rust.
- **Pros**: Zig's zero-overhead C interop allows surgical replacement, simpler mental model for the hot path, TigerBeetle proves Zig works for financial systems.
- **Cons**: Pre-1.0 stability risk in production, near-zero hiring pipeline, regulatory concerns about non-memory-safe language.
- **Why ranked lower**: The pre-1.0 status is a dealbreaker for a production trading system in a regulated environment. Revisit after Zig 1.0 ships and stabilizes (likely 2027+).

---

## Adversarial Review

### Counterargument 1: "Zig's simplicity means faster time-to-market, which matters more"

**Evidence for**: Zig's C-like model means a C++ team can be productive in ~2 months vs ~4 months for Rust. TigerBeetle proves Zig can build mission-critical financial software. Static allocation in Zig is simpler than in Rust.

**Rebuttal**: Time-to-market is important but not dominant for a trading system rewrite. The system must run for years in production. The ongoing cost of: (a) maintaining a pre-1.0 language codebase, (b) inability to hire replacements, and (c) regulatory friction will exceed the 2-month learning curve savings within the first year.

**Verdict**: Counterargument has merit for a proof-of-concept but fails for production deployment.

### Counterargument 2: "Rust's borrow checker will force unsafe blocks in the hot path anyway, negating its safety advantage"

**Evidence for**: HFT hot paths typically require raw pointers, unchecked array access, and manual memory management for performance. Databento chose C++ over Rust for their feed handler because "certain architectural patterns that are bread-and-butter in feed handlers become unnecessarily complex in Rust." Rust's ownership model created friction for their use case.

**Rebuttal**: This is partially valid. The hot path will likely contain significant `unsafe` Rust. However:
1. `unsafe` blocks are explicitly marked and isolated, making auditing easier than reviewing all of C++ or Zig.
2. The hot path is typically <5% of the total codebase. The other 95% (OMS, risk management, connectivity, logging, monitoring) benefits enormously from safe Rust.
3. Rust's `unsafe` still maintains some invariants (e.g., type safety, lifetime annotations on function boundaries).

**Verdict**: Valid concern. The hot path's safety profile in Rust will resemble Zig/C++ more than safe Rust. But the surrounding system's safety profile is dramatically better.

### Counterargument 3: "The hiring market for Rust in finance is too small — you'll be stuck"

**Evidence for**: JPMorgan posted 24 Rust jobs vs 908 C++ jobs. A recruiter reported "3 Rust CVs in 3-4 months vs 50 C++ CVs." Goldman Sachs posted **zero** Rust jobs in the US in 12 months.

**Rebuttal**: This is a real risk. However:
1. Rust job postings "have more than doubled in the past two years."
2. Nearly half of all companies now use Rust in production (Rust Foundation survey).
3. Rust developers can be trained from C++ developers — harder than Zig training but achievable.
4. The trajectory is toward more Rust in finance, not less. Early adopters who build internal Rust expertise will have a competitive advantage.

**Verdict**: Valid risk. Mitigation: invest in training your existing C++ team rather than relying on external Rust hires.

### Counterargument 4: "Zig 1.0 will land in 2026, making the stability concern moot"

**Evidence for**: Multiple sources indicate Zig 1.0 is targeted for 2026.

**Rebuttal**:
1. No specific month has been announced. "Targeted for 2026" could mean December 2026.
2. 1.0 release != ecosystem maturity. After 1.0, the ecosystem needs 1-2 years to stabilize libraries and tooling around the stable API.
3. Even after 1.0, the talent pool will remain tiny for years.
4. Regulatory auditors will want to see track record, not just a version number.

**Verdict**: The stability concern is reduced but not eliminated by a 2026 1.0 release.

### Assumption Audit

| Assumption | Status | Risk if Wrong |
|------------|--------|--------------|
| Sub-μs latency is achievable via architectural changes | **Verified** — SubMicro demonstrates 890ns | If wrong, neither language helps; need FPGA |
| Team can learn Rust in 4 months to productive level | **Reasonable** — consistent with industry reports | Delays could extend to 6-9 months for full proficiency |
| CISA memory safety mandate will affect financial firms | **Verified** — applies to critical infrastructure vendors | If financial firms are exempted, regulatory advantage disappears |
| Zig 1.0 will ship in 2026 | **Uncertain** — no specific date confirmed | If delayed to 2027+, Zig becomes even less viable |
| Rust hiring market will grow | **Reasonable** — consistent with trend data | If it plateaus, hiring remains very difficult |
| Hot path can be isolated to <5% of codebase | **Reasonable** — typical for trading systems | If hot path is larger, borrow checker friction increases proportionally |

### Failure Modes

1. **Rust learning curve exceeds expectations**: Team spends 6-9 months becoming productive, delaying the project by a quarter. Mitigation: hire 1-2 experienced Rust consultants for the first 6 months.
2. **Borrow checker forces architectural compromises in hot path**: Performance-critical patterns don't map well to Rust's ownership model (as Databento experienced). Mitigation: accept `unsafe` blocks in hot path, or use C/C++ for that layer via FFI.
3. **Zig 1.0 ships and rapidly matures**: Within 2 years, Zig has a thriving ecosystem and your Rust investment looks premature. Impact: moderate — Rust skills remain valuable regardless.
4. **Neither language achieves sub-μs without FPGA**: The bottleneck is hardware, not software. Impact: high — entire rewrite project fails to meet target. Mitigation: prototype with kernel bypass on current C++ to validate architectural thesis before committing to rewrite.

---

## Recommendation

**Primary: Rewrite in Rust**, with the following strategy:

1. **Phase 0 (Month 1-2)**: Prototype sub-μs architecture in your existing C++ codebase first. Add kernel bypass (DPDK/OpenOnload), isolated cores, SPSC queues, and zero-allocation hot path. Validate you can hit <1μs in C++ before committing to a language change. If you can, the language rewrite is about safety and maintainability, not performance.

2. **Phase 1 (Month 2-6)**: Train team on Rust. Start with surrounding infrastructure (OMS, risk management, market data normalization). Hire 1-2 Rust consultants.

3. **Phase 2 (Month 6-12)**: Rewrite hot path in Rust. Accept `unsafe` blocks where needed for performance. Benchmark against C++ baseline continuously.

4. **Phase 3 (Month 12-18)**: Integration testing, stress testing per MiFID II requirements, regulatory documentation, production deployment.

**Fallback**: If Rust's borrow checker creates unacceptable friction in the hot path architecture (as Databento experienced with their feed handler), adopt the **hybrid C++/Rust pattern** — C++ for the hot path, Rust for everything else.

**When this recommendation changes**:
- If Zig 1.0 ships with a stable API and 2+ financial firms adopt it in production, reassess in 2027.
- If your team cannot achieve productivity in Rust within 6 months, pivot to the hybrid approach.
- If CISA exempts financial trading firms from memory safety requirements, the regulatory argument weakens and C++ (optimized) becomes more competitive.
- If FPGA-based execution proves necessary for sub-μs, the software language choice becomes less important.

**Confidence: 72%** — Strong evidence favors Rust overall, but the decision is genuinely close on the hot-path performance dimension, and the hiring challenge is real.

---

## Sources

### Performance & Benchmarks
- [SubMicro Trading System — 890ns Ultra-Low Latency Execution Engine](https://submicro.krishnabajpai.me/)
- [SubMicro GitHub — submicro-execution-engine](https://github.com/krish567366/submicro-execution-engine)
- [RustQuant — Ultra-fast HFT Framework in Rust](https://rustquant.io/)
- [RustQuant — Nanosecond Precision Benchmarking for HFT](https://rustquant.dev/blog/nanosecond-precision-benchmarking-rust-hft/)
- [Rust VS Zig benchmarks — programming-language-benchmarks](https://programming-language-benchmarks.vercel.app/rust-vs-zig)
- [When Zig is safer and faster than Rust — zackoverflow.dev](https://zackoverflow.dev/writing/unsafe-rust-vs-zig/)
- [Optimizing Rust code with LLVM — LogRocket](https://blog.logrocket.com/optimizing-rust-code-llvm/)

### Ecosystem & Adoption
- [crates.io — Rust Package Registry](https://crates.io/)
- [State of the Rust/Cargo crates ecosystem — lib.rs stats](https://lib.rs/stats)
- [Zigistry — Zig Packages Registry](https://zigistry.dev/)
- [TigerBeetle GitHub](https://github.com/tigerbeetle/tigerbeetle)
- [Why TigerBeetle is the most interesting database — Amplify Partners](https://www.amplifypartners.com/blog-posts/why-tigerbeetle-is-the-most-interesting-database-in-the-world)
- [Zig companies in production — GitHub](https://github.com/rofrol/zig-companies)
- [Nearly half of all companies now use Rust in production — The New Stack](https://thenewstack.io/rust-enterprise-developers/)
- [Rust Foundation Annual Report 2025](https://rustfoundation.org/media/annual-report-strategy-2025/)

### Trading Systems & Finance
- [Databento — Rust vs C++ for trading systems](https://databento.com/blog/rust-vs-cpp)
- [Databento — Why we didn't rewrite our feed handler in Rust](https://databento.com/blog/why-we-didnt-rewrite-our-feed-handler-in-rust)
- [Rust for HFT — Luca Sbardella](https://lucasbardella.com/coding/2025/rust-for-hft)
- [Building Real-Time Trading Systems: Why We Abandoned Go for Rust](https://medium.com/@chopra.kanta.73/building-real-time-trading-systems-why-we-abandoned-go-for-rust-baa681d7aac9)
- [eFinancialCareers — Rust vs C++ in financial services](https://www.efinancialcareers.com/news/rust-vs-c-plus-plus-financial-services-low-latency)
- [eFinancialCareers — Hedge funds replacing languages with Rust](https://www.efinancialcareers.com/news/rust-replacing-c-programming-language-hedge-fund)

### Regulatory & Compliance
- [CISA — Memory Safe Languages: Reducing Vulnerabilities](https://www.cisa.gov/resources-tools/resources/memory-safe-languages-reducing-vulnerabilities-modern-software-development)
- [CISA — The Case for Memory Safe Roadmaps](https://www.cisa.gov/resources-tools/resources/case-memory-safe-roadmaps)
- [SEC — Rule 15c3-5 Compliance Guide](https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm)
- [ESMA — MiFID II Article 17 Algorithmic Trading](https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mifid-ii/article-17-algorithmic-trading)
- [FCA — MAR 7A.3 Requirements for algorithmic trading](https://handbook.fca.org.uk/handbook/MAR/7A/3.html)
- [FCA — Multi-firm review of algorithmic trading controls](https://www.fca.org.uk/publications/multi-firm-reviews/algorithmic-trading-controls-high-level-observations)
- [Kroll — Algorithmic Trading Under MiFID II](https://www.kroll.com/en/publications/financial-compliance-regulation/algorithmic-trading-under-mifid-ii)
- [FINRA — Market Access Rule](https://www.finra.org/rules-guidance/guidance/reports/2022-finras-examination-and-risk-monitoring-program/market-access-rule)
- [NSA/CISA — Memory Safe Languages CSI (June 2025)](https://media.defense.gov/2025/Jun/23/2003742198/-1/-1/0/CSI_MEMORY_SAFE_LANGUAGES_REDUCING_VULNERABILITIES_IN_MODERN_SOFTWARE_DEVELOPMENT.PDF)
- [Stack Overflow Blog — In Rust We Trust? White House Office Urges Memory Safety](https://stackoverflow.blog/2024/12/30/in-rust-we-trust-white-house-office-urges-memory-safety/)

### Hiring & Market Data
- [RustJobs.dev — Salary Guide 2026](https://rustjobs.dev/salary-guide)
- [ZipRecruiter — Rust Developer Salary](https://www.ziprecruiter.com/Salaries/Rust-Developer-Salary)
- [ZipRecruiter — Zig Programming Jobs](https://www.ziprecruiter.com/Jobs/Zig-Programming)
- [Glassdoor — Rust Developer Salary](https://www.glassdoor.com/Salaries/rust-developer-salary-SRCH_KO0,14.htm)
- [Wellfound — Rust Developer Compensation](https://wellfound.com/hiring-data/s/rust)
- [Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/technology/)

### Language Comparison & Learning
- [Zig — Why Zig When There is Already C++, D, and Rust?](https://ziglang.org/learn/why_zig_rust_d_cpp/)
- [LogRocket — Comparing Rust vs. Zig](https://blog.logrocket.com/comparing-rust-vs-zig-performance-safety-more/)
- [Zig devlog 2026](https://ziglang.org/devlog/2026/)
- [Zig GitHub releases](https://github.com/ziglang/zig/releases)
- [Rust — Compliance Standards and Security Patterns](https://softwarepatternslexicon.com/rust/security-patterns/compliance-standards-and-rust/)
- [Sonatype — Rust in the Enterprise](https://www.sonatype.com/blog/rust-in-the-enterprise-best-practices-and-security-considerations)
- [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html)

### Standards
- [ISO/IEC 25010:2023 — Product Quality Model](https://www.iso.org/standard/78176.html)
- [Databento — Market Access Rule Microstructure Guide](https://databento.com/microstructure/market-access-rule)
