# Should We Adopt Rust for Our New Internal CLI Tool (vs. Go)?

**Deliverable type:** Decision (general technology choice, no existing codebase).
**Scope:** This analysis covers a *new internal CLI tool* where Go is the default. It does NOT cover web services, embedded/real-time systems, WASM targets, or rewriting an existing codebase — those shift the calculus and are called out where relevant.

## Executive Summary

**Recommendation: Stay with Go for the internal CLI tool. Confidence: 82%.** For the overwhelming majority of internal CLIs, both languages are "fast enough," and the dominant cost is engineering time, not CPU cycles. Go's 5–10x faster compile times, days-not-months onboarding, and 3–7x larger hiring pool make it the lower-total-cost choice for a tool whose bottleneck is almost never raw compute. **Adopt Rust only if a specific, named driver applies** (see Recommendation): the tool is CPU/memory-bound on large data in tight loops, it is correctness/security-critical and long-lived, or your team already has Rust fluency and an established Rust toolchain. Absent one of those, choosing Rust here optimizes a dimension that does not bind.

## Key Findings

1. **For typical CLI workloads, both languages are "fast enough"; the bottleneck is elsewhere.** Trivial-program startup is ~1–5 ms for both (Go ~1.8 ms vs Rust ~2.5 ms in one microbenchmark) — negligible for a CLI invoked interactively. Rust's real advantage appears only in CPU-bound tight loops: processing a million-line log file, a Rust tool might take ~0.8 s where Go takes ~3 s (≈2–5x). [Evidence: practitioner benchmarks + aggregated comparisons — moderate confidence; vendor/blog benchmarks, not peer-reviewed] ([unixy.io](https://unixy.io/blog/rust-vs-go-cli-tools/), [besterry.com](https://besterry.com/posts/rust-vs-go-for-cli-tools/))

2. **Go compiles 5–10x faster, which directly drives iteration speed.** Medium Go projects compile in 2–10 s with sub-second incremental builds; equivalent Rust projects take 30–120 s, and large dependency trees reach 5–10 min on clean builds. For a tool under active development, this is felt dozens of times per day. [Evidence: multiple independent practitioner reports — moderate-high confidence] ([rustify.rs](https://rustify.rs/articles/rust-vs-go-2026), [unixy.io](https://unixy.io/blog/rust-vs-go-cli-tools/))

3. **Onboarding cost strongly favors Go.** Go: a mid-level Python/Java developer ships productive code within ~1 week; Rust requires internalizing ownership/borrowing/lifetimes — weeks to 2–3 months even for experienced engineers. For an *internal* tool likely maintained by rotating/non-specialist engineers, this is the single largest hidden cost. [Moderate-high confidence] ([rustify.rs](https://rustify.rs/articles/rust-vs-go-2026), [unixy.io](https://unixy.io/blog/rust-vs-go-cli-tools/))

4. **Hiring pool is 3–7x larger for Go; Rust costs ~10–20% more per head.** Go reportedly has 5–7x more open positions than Rust (and ~3–4x larger by other counts); Rust median comp runs ~$145K–$185K vs Go ~$135K–$175K (US, ~10–20% premium). Rust postings grew ~35% YoY but from a much smaller base. [Evidence: recruiting-market blog aggregations — low-moderate confidence; figures vary by source and are not from a single authoritative dataset] ([rustify.rs](https://rustify.rs/articles/rust-vs-go-backend-2026), [haystackapp.io](https://haystackapp.io/compare/go-vs-rust))

5. **Both have mature, battle-tested CLI ecosystems.** Go's Cobra powers Kubernetes, Docker, Hugo, and the GitHub CLI (used across 170k+ projects); Rust's `clap` is used by 240k+ repositories. Flags, subcommands, config, shell completions, and colored output are first-class in both. Ecosystem maturity is **not** a differentiator here. [High confidence] ([cobra.dev](https://cobra.dev/), search aggregation)

6. **Rust wins decisively on memory safety — but a CLI rarely needs it.** ~70% of CVEs at Microsoft, Google, Apple, and in the Linux kernel are memory-safety bugs; Android's memory-safety vulnerabilities fell from 76% (2019) to ~24% (2024) as it shifted new code to memory-safe languages (Rust/Java/Kotlin). CISA/NSA name Rust explicitly as a memory-safe systems language. **However, Go is also memory-safe** (garbage-collected), so this argument does not distinguish Rust from Go — it distinguishes both from C/C++. [High confidence] ([Google/The Register](https://www.theregister.com/software/2024/09/25/googles_rust_belts_bugs_out_of_android_in_safe_coding_push/948796), [CISA/NSA via The Register](https://www.theregister.com/software/2025/06/27/cisa_nsa_repeat_call_for_memory_safe_programming_languages/1192628))

7. **Binaries: Rust is smaller, both are statically linked and dependency-free.** Minimal stripped Rust binaries ~300 KB–2 MB; equivalent Go ~2 MB (Go embeds its runtime/GC). For real CLIs with dependencies both land in the 5–15 MB range. Both cross-compile to a single static binary — a major shared advantage over interpreted alternatives. [High confidence] ([unixy.io](https://unixy.io/blog/rust-vs-go-cli-tools/))

8. **Developer sentiment favors Rust, but that is not a cost/throughput metric.** Rust was the *most-admired* language in the 2024 Stack Overflow survey (~83%), far above Go. Admiration predicts retention/morale, not delivery speed for an internal tool. Usage: Go 13.5% / Rust 12.6% of all respondents (2024). [High confidence for usage; sentiment via InfoWorld] ([SO Survey 2024](https://survey.stackoverflow.co/2024/technology), [InfoWorld](https://www.infoworld.com/article/2338638/rust-most-admired-language-stack-overflow-survey-says.html))

## Industry Standards Compliance

| Standard / Guidance | Requirement | Go status | Rust status | Source |
|---|---|---|---|---|
| CISA/NSA "Memory Safe Languages" (June 2025) | Prefer memory-safe languages for new code | **Compliant** (GC memory-safe) | **Compliant** (named explicitly) | [The Register](https://www.theregister.com/software/2025/06/27/cisa_nsa_repeat_call_for_memory_safe_programming_languages/1192628) |
| NIST SSDF (SP 800-218) secure-by-design | Reduce vulnerability classes at the language level | Compliant | Compliant | derived from CISA guidance (above) |
| ISO/IEC 5055 (code quality / reliability) | Avoid memory/resource weaknesses | Both satisfy memory-safety class; Rust adds compile-time data-race prevention | — | [unverified] — not fetched this session |

No CLI-specific formal standard (ISO/IEEE/RFC) governs language choice for an internal command-line tool; language selection is an engineering/economic decision, not a compliance one. Absence of a binding standard is itself a finding: **this is a cost/fit decision, not a regulatory one.**

## Quantitative Analysis

| Dimension | Go | Rust | Edge | Matters for internal CLI? |
|---|---|---|---|---|
| Startup (trivial) | ~1.8 ms | ~2.5 ms | Go (marginal) | No |
| CPU-bound throughput | baseline | 2–5x faster | **Rust** | Only on large-data tight loops |
| Clean compile (medium) | 2–10 s | 30–120 s | **Go (5–10x)** | Yes (iteration) |
| Incremental compile | <1 s | seconds–minutes | **Go** | Yes |
| Onboarding to productive | ~1 week | 2–12 weeks | **Go** | Strongly yes |
| Binary size (minimal) | ~2 MB | ~0.3–2 MB | Rust | Marginal |
| Static single-binary dist | Yes | Yes | Tie | Yes (both win) |
| Memory safety | Yes (GC) | Yes (compile-time) | Tie for safety; Rust no-GC | Rarely |
| Hiring pool (open roles) | 3–7x larger | smaller | **Go** | Yes |
| Comp premium | baseline | +10–20% | Go (cheaper) | Yes |
| Ecosystem (CLI libs) | Cobra/Viper | clap | Tie | No |

**Weighted scoring (weights reflect an *internal CLI* context: iteration + maintainability dominate, raw perf is discounted).** Weights sum to 100. Scores 1–5 (5 best).

| Criterion | Weight | Go score | Rust score | Go wtd | Rust wtd |
|---|---|---|---|---|---|
| Maintainability / onboarding | 30 | 5 | 2 | 150 | 60 |
| Iteration speed (compile) | 20 | 5 | 2 | 100 | 40 |
| Hiring / staffing | 15 | 5 | 3 | 75 | 45 |
| Runtime performance | 10 | 3 | 5 | 30 | 50 |
| Memory safety / correctness | 10 | 4 | 5 | 40 | 50 |
| Ecosystem / libraries | 10 | 5 | 5 | 50 | 50 |
| Distribution (single binary) | 5 | 5 | 5 | 25 | 25 |
| **Total** | **100** | | | **470** | **320** |

Arithmetic check: Go = 150+100+75+30+40+50+25 = **470**; Rust = 60+40+45+50+50+50+25 = **320**. Go leads by 47% under internal-CLI weights. **Sensitivity:** if "runtime performance" is reweighted to 40 (and maintainability dropped to 15 — i.e., a performance-critical data-processing CLI), Rust = 60·(15/30)+40+45+200/10·... recomputed below.

Re-run with perf-dominant weights (Maintainability 15, Iteration 10, Hiring 10, Performance 40, Safety 15, Ecosystem 5, Distribution 5): Go = 5·15+5·10+5·10+3·40+4·15+5·5+5·5 = 75+50+50+120+60+25+25 = **405**; Rust = 2·15+2·10+3·10+5·40+5·15+5·5+5·5 = 30+20+30+200+75+25+25 = **405**. **They tie exactly when performance is weighted at 40%** — confirming the decision hinges entirely on whether this CLI is performance-critical.

## Implementation Guidance

**If you proceed with Go (recommended default):**
- Scaffold: `go mod init <tool>` then `go get github.com/spf13/cobra-cli@latest` → `cobra-cli init`. Add `spf13/viper` for config/env binding.
- Build static, stripped, cross-platform: `CGO_ENABLED=0 go build -ldflags="-s -w" -o bin/tool` ; cross-compile with `GOOS=linux GOARCH=arm64 go build ...`.
- Distribute via [GoReleaser](https://goreleaser.com/) for multi-arch binaries, checksums, and Homebrew/Scoop taps.
- Test: `go test ./...`; lint: `golangci-lint run`.

**If a Rust driver applies:**
- Scaffold: `cargo new tool` ; add `clap = { version = "4", features = ["derive"] }`.
- Fast dev loop: `cargo install cargo-watch` + `sccache` to blunt compile-time pain; use `cargo build` (debug) for iteration, `--release` only for ship.
- Size/perf: `[profile.release] panic = "abort"; lto = true; strip = true`.
- Distribute via [cargo-dist](https://opensource.axo.dev/cargo-dist/) for cross-platform installers.

**Monday-morning test:** write the tool's hottest realistic workload (e.g., parse your largest real input file) as a 30-line prototype in *both* languages, time it, and measure your own compile loop. If Go's runtime is acceptable on your real data, the decision is made.

## Alternatives Considered

### 1. Adopt Rust now
*Why considered:* Best-in-class performance, no GC pauses, compile-time data-race safety, highest developer admiration (83%), smallest binaries. *Why it ranked lower (score 320 vs 470):* For an internal CLI, its wins (raw throughput, no-GC determinism) rarely bind, while its costs (5–10x compile times, 2–12 week onboarding, scarcer/pricier hiring) are paid continuously. *When it WOULD be right:* the CLI is CPU/memory-bound on large inputs in tight loops; it is long-lived and correctness/security-critical (e.g., crypto, parsers exposed to untrusted input); or your team already writes Rust daily and has a toolchain/CI story.

### 2. Keep Go (recommended)
*Why considered:* Incumbent default; fast iteration; trivial onboarding; mature CLI ecosystem (Cobra); single static binary; memory-safe. *Why it ranks first:* lowest total cost of ownership for a tool whose bottleneck is engineering time, not CPU. *When it would be wrong:* performance becomes the binding constraint, or GC pause determinism matters.

### 3. A higher-level language (Python/TypeScript via Bun or Node)
*Why considered:* Fastest prototyping, largest hiring pool, richest libraries for glue tasks. *Why it ranked lower:* loses the single-static-binary distribution advantage (needs a runtime or bundling), slower runtime, and weaker for long-lived performance-sensitive tooling. *When it would be right:* throwaway scripts, or a CLI that is mostly orchestration glue with no distribution constraints. Out of the user's framing (Go-vs-Rust) but worth a one-line kill: viable only if distribution-as-single-binary is not required.

## Adversarial Review

**Counterargument to "stay with Go": "Rust is the industry's future; adopting now builds durable capability and avoids a later rewrite."**
Partially valid for a *platform* bet, but weak for a *single internal CLI*. The language of one internal tool is cheaply reversible (rewrites of small CLIs are days–weeks); you don't need to pre-commit the whole org via a utility. If the goal is org-wide Rust capability, make that decision explicitly on its own merits, not smuggled in through a CLI. [Counter stands; lowers confidence in a blanket "never Rust" to ~82%, not higher.]

**Counterargument: "Rust's borrow checker prevents whole bug classes Go allows (data races)."**
True and measurable — Rust prevents data races at compile time; Go does not (Go has `-race` detection at runtime only). But a typical internal CLI is short-lived, single-invocation, and rarely has complex shared-memory concurrency, so the exposure is small. Valid but low weight for this deliverable.

**Premise check (is this the right problem?):** The question frames language as the decision. The real binding variable is *"is this CLI performance-critical on large data?"* If yes → Rust is defensible; if no → the question nearly answers itself (Go). The premise is sound but under-specified: the decision cannot be fully closed without the tool's expected workload. This is the one gap I cannot close with tools (needs-user-input).

**Assumption audit:**
- *Verified:* Go and Rust both produce single static binaries; both memory-safe; Cobra/clap mature; SO 2024 usage Go 13.5%/Rust 12.6% ([SO](https://survey.stackoverflow.co/2024/technology)); Android 76%→24% ([Register](https://www.theregister.com/software/2024/09/25/googles_rust_belts_bugs_out_of_android_in_safe_coding_push/948796)).
- *Reasonable (justified, not primary-sourced):* compile-time ratios (5–10x) and onboarding times — consistent across ≥3 independent practitioner sources but no controlled study; salary/hiring multiples — recruiting-blog aggregations, directionally consistent but imprecise.
- *Uncertain (resolve before finalizing):* the tool's actual workload profile (CPU-bound vs IO/glue); team's current Rust familiarity; longevity/criticality of the tool. These flip the recommendation.

**Failure modes of the recommendation:** If the CLI later becomes a hot-path data processor run at scale (CI fan-out over GBs), Go's GC and lower throughput could bite — mitigation: prototype the hot path first (Implementation Guidance). If the org is strategically standardizing on Rust, choosing Go here creates an outlier to maintain.

**Refinement Round 1** — investigated "does Rust's compile-time penalty actually matter for a CLI, or is it a one-time cost?": reclassified from *uncertain* to *reasonable* — practitioner sources ([unixy.io](https://unixy.io/blog/rust-vs-go-cli-tools/)) confirm it is a *per-iteration* cost felt throughout development, not one-time, strengthening the Go case for actively-developed tools.

**Refinement Round 2** — investigated "is the memory-safety argument a Rust differentiator here?": reclassified the memory-safety finding from a pro-Rust point to a *non-differentiator* — Go is also memory-safe, so CISA/NSA guidance supports *both* equally over C/C++; it does not favor Rust vs Go. This removed a spurious Rust advantage and *increased* confidence in the Go default.

**Refinement Round 3** — gap scan surfaced only lower-severity issues of the same kind (exact compile-time seconds, precise salary deltas) — all source-of-the-same-class (imprecise blog aggregations); no new closable-by-tool gap. The remaining open gap (the tool's workload profile) is needs-user-input, not closable by tool. **Terminating per the Phase 5b rule (a round surfaced only same-kind lower-severity issues).**

### Gap Ledger

| Gap | Class | Action taken | Status |
|---|---|---|---|
| Exact SO 2024 admired % for Go | closable-by-tool | Fetched SO survey (usage confirmed; admired page not in excerpt); Rust 83% via InfoWorld | closed (usage); Go admired marked approximate |
| Compile-time ratio Go vs Rust | closable-by-tool | Triangulated 3 independent sources (5–10x) | closed |
| Is memory safety a Rust-vs-Go differentiator? | closable-by-tool | Confirmed Go is also memory-safe; reclassified as non-differentiator | closed |
| Salary/hiring multiples precision | closable-by-tool | Triangulated recruiting aggregations; flagged low-moderate confidence | closed (bounded; precision residual) |
| Android 76%→24% figure | closable-by-tool | Verified via The Register + Google Safe Coding announcement | closed |
| **The tool's actual workload (CPU-bound vs glue) + team Rust fluency + tool longevity** | **needs-user-input** | Cannot probe without the user; this is the single variable that flips the decision | **open (by nature)** |
| ISO/IEC 5055 clause detail | open-in-world | Not fetched this session | open (low severity) |

**Termination statement:** Zero *closable-by-tool* gaps remain open. The only open gaps are one **needs-user-input** (workload/team/longevity — which the user alone can supply) and one low-severity **open-in-world** item (ISO 5055 clause text). Convergence reached after 3 refinement rounds; Round 3 surfaced only same-class lower-severity issues. **Terminating per Phase 5b.**

## Recommendation

**Default to Go for the internal CLI tool. Confidence 82%.** Under internal-CLI weights, Go scores 470 vs Rust 320 (47% lead); the lead collapses to a tie only when runtime performance is weighted at ~40%.

**Switch to Rust if and only if** one of these is true — decide by answering them before writing code:
1. **Performance-critical:** the tool does heavy CPU/memory work on large inputs in tight loops (measured, not assumed — prototype the hot path first). *If this proves true, switch to Rust.*
2. **Correctness/security-critical and long-lived:** it parses untrusted input, handles crypto, or must run for years with minimal defects — Rust's compile-time guarantees earn their cost.
3. **Team already fluent in Rust** with an existing toolchain/CI — the onboarding and compile-time costs are already paid.

**Sensitivity:** If finding #1 (workload) proves CPU-bound at scale, the quantitative tie at 40% performance weight means Rust becomes defensible — re-run the weighted matrix with your real numbers. If none of the three triggers applies, Go is the lower-total-cost, faster-to-ship, easier-to-staff choice, and "we chose Go because this is an internal tool where iteration speed and maintainability dominate, and it is not performance-critical" is a fully defensible decision.

## Sources

**Official Documentation / Primary:**
- [Stack Overflow Developer Survey 2024 — Technology](https://survey.stackoverflow.co/2024/technology) (usage: Go 13.5%, Rust 12.6%)
- [Cobra — The CLI Framework Developers Love](https://cobra.dev/) (Go CLI ecosystem)

**Regulatory / Security Guidance:**
- [CISA/NSA repeat call for memory-safe languages (June 2025) — The Register](https://www.theregister.com/software/2025/06/27/cisa_nsa_repeat_call_for_memory_safe_programming_languages/1192628)
- [Google's Rust reduces Android memory-safety bugs 76%→24% — The Register](https://www.theregister.com/software/2024/09/25/googles_rust_belts_bugs_out_of_android_in_safe_coding_push/948796)

**Industry Analysis / Practitioner:**
- [Rust vs Go for CLI Tools: The Honest Comparison — unixy.io](https://unixy.io/blog/rust-vs-go-cli-tools/)
- [Rust vs Go for CLI Tools: A Practical Comparison — besterry.com](https://besterry.com/posts/rust-vs-go-for-cli-tools/)
- [Rust vs Go in 2026 — rustify.rs](https://rustify.rs/articles/rust-vs-go-2026)
- [Rust vs Go for Backend Engineers 2026: Jobs, Salary — rustify.rs](https://rustify.rs/articles/rust-vs-go-backend-2026)
- [Go vs Rust Developers — haystackapp.io](https://haystackapp.io/compare/go-vs-rust)
- [Rust most admired language, Stack Overflow survey — InfoWorld](https://www.infoworld.com/article/2338638/rust-most-admired-language-stack-overflow-survey-says.html)
