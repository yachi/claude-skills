---
name: deep-research
description: "Deep Research (/deep-research or /dr) — exhaustive, evidence-based investigation of any topic. Use when the user invokes /deep-research, /dr, asks for deep research, says 'research this thoroughly', wants expert-level analysis on any subject (technical, business, scientific, regulatory, financial, medical, legal, etc.), needs quantitative comparison of alternatives, or wants a decision backed by hard data and industry standards. Also trigger when the user says things like 'I need to be 100% sure', 'prove it', 'give me the data', 'what does the industry standard say', 'I want to be confident about this', or any request where superficial answers would be dangerous. If in doubt whether to use this skill, use it — shallow research is the bigger risk."
---

# /dr — Deep Research

You are now in Deep Research mode. The standard: ICD 203 analytic tradecraft (9/9 standards), GRADE evidence hierarchy, NIST reproducibility. Every claim survives cross-examination by the foremost domain expert. No hand-waving. No unverified assertions. If you can't prove it, you don't say it.

## Core Principles

1. **Evidence over reasoning** — Your internal knowledge is a starting hypothesis, never a conclusion. Every factual claim must be verified through tool use (first-party data, WebSearch, WebFetch, Bash, code execution, MCP tools) against authoritative sources.

2. **Quantitative over qualitative** — Replace adjectives with numbers. "Faster" becomes "47% lower p99 latency (benchmarked)." "More popular" becomes "3.2M weekly downloads vs 180K." "More secure" becomes "0 CVEs in 3 years vs 12 (4 critical)."

3. **Standards over opinions** — Every domain has authoritative standards bodies, best practices, and regulatory frameworks. Find them. Cite them. Compare the subject against them.

4. **Adversarial rigor** — Before presenting conclusions, actively try to disprove them. The strongest argument is one that has survived its best counterargument.

## Research Protocol

### Phase 0: Clarify (if needed)

If the query is ambiguous or underspecified, ask 1-2 clarifying questions before committing to research. Skip if the question is already clear and specific.

### Phase 0b: Decide the deliverable

Before researching, state in one line what the user will **do** with the output: decide / build / consume / learn / verify / diagnose. This sets the report shape (see Phase 8) and prevents the #1 failure mode — delivering a 3,000-word report when the user wanted an artifact, an action, or a short verdict in their own language. When the type is genuinely unclear, default to the full research report. Never silently substitute a different deliverable than the user asked for.

**Gate on a live system/artifact.** The verify/diagnose/build/consume shapes apply ONLY when you are operating inside a live project — local code, data, a device, or an artifact to produce. A standalone research question delivered as text, with no local system to diagnose and nothing to build, ALWAYS uses the DEFAULT full template — even when phrased as "is X safe", "verify Y", or "I need a definitive answer". Phrasing alone never selects an adaptive shape; the presence of a live system or artifact does.

### Phase 1: Decompose

Break the research question into orthogonal sub-questions. For each, identify what needs to be answered, what evidence would be conclusive (benchmark data, standards compliance, expert consensus, regulatory text, academic study), and where that evidence is most likely found. Write the decomposition out so the user can see your research plan.

**Candidate space (choose-between questions):** Enumerate the FULL candidate set — including the incumbent/status-quo and the previously chosen option — then filter by hard constraints, then compare. Never limit alternatives to only the options the user named by hand; the unnamed incumbent is often the right answer.

**Premise validation (two falsifiable premises, kill switch):**
- **(a) Factual premise** — the claim the question rests on. Attack it first with the cheapest first-party check (see Phase 1.5, next), not a web search. If it fails, pivot immediately and tell the user. A fast evidence-based pivot beats a thorough analysis built on a false premise.
- **(b) Intent premise** — the approach/architecture/scope the user expects. If evidence points toward an approach the user did **not** ask for (different architecture, different scope, a different question), STOP and ask in one line before investing rounds.

The kill switch applies to the *research* premise, NEVER to explicit user constraints (named tools, URLs, formats, versions). If a user-named tool cannot do part of the job, use it for the part it can and surface the limit as a decision — do not substitute silently.

**Multi-perspective framing:** Consider each sub-question from at least 2 stakeholder viewpoints. When a question spans 3+ domains (e.g., regulatory + technical + financial), structure the analysis with explicitly labeled domain perspectives (e.g., "### Regulatory Analysis", "### Technical Assessment", "### Financial Perspective"). Each perspective must contribute unique findings; the synthesis then analyzes how constraints across domains interact — tensions, compounding effects, cross-cutting requirements.

### Phase 1.5: First-party evidence first

**Before any web search, exhaust the evidence the system under study already holds.** List its own data stores: repo code and config, databases and tables, time-series and `*_hourly`/`*_daily` stats, audit/change/update logs, metrics stores, the device's own history. Read the code you will recommend changing — do not trust a subagent's summary of it.

- **For a regression**, pull the longest available series for the failing object AND a healthy peer, find the hour behaviour changed, then correlate that hour with change/update/reboot logs. A capture taken entirely after the transition cannot see the transition.
- **A snapshot is not history.** One capture, one query, one `conntrack` dump never supports a claim containing "never" / "always" / "since" / "the entire time."
- **If you cannot reach the system**, ask for the specific command output in the **first** turn — not after round 1.

This phase comes before Phase 2 on purpose: the answer is often already in the system's own records, and web evidence can't overturn first-party data you never looked at.

### Phase 2: Multi-Source Investigation

For each sub-question, research from multiple independent source types. Triangulation — a claim supported by three independent source types — is far more credible than one source, however authoritative. Use WebSearch and WebFetch aggressively; search multiple phrasings per sub-question. When a claim appears in a secondary source, trace it to the primary source.

**Source hierarchy by domain:**

| Domain | Primary Sources | Secondary Sources |
|--------|----------------|-------------------|
| System under study | Its own code, config, DB, logs, time-series, device history | — |
| Technology | Official docs, RFCs, source code, benchmarks you run | GitHub issues, conference talks, reputable blogs |
| Security | NVD/CVE databases, vendor advisories, NIST/OWASP | Security research papers, pentesting reports |
| Business/Finance | SEC filings, annual reports, GAAP/IFRS standards | Industry analyst reports, earnings calls |
| Science/Medicine | Peer-reviewed journals, FDA/EMA, WHO | Systematic reviews, preprints (flagged as such) |
| Legal/Regulatory/Engineering | Statutory text, regulatory guidance, case law, ISO/IEC/IEEE standards | Legal commentary, compliance frameworks, industry handbooks |

**Raw primary data for numbers:** For prices, versions, limits, and quotas, fetch the raw primary source (API JSON, source file, registry) via Bash — not a summarizing fetcher that may paraphrase. Check variant/tier qualifiers (quantization, region, plan) against the user's constraints. Reconcile any figure that differs across sources before using it.

**Fetch fallback ladder:** On encoded/FlateDecode PDF bytes, save the file and run `pdftotext`/Read-pages instead of reading the stream. On 403 / Cloudflare / credit exhaustion, try exactly one alternate tool (Firecrawl → WebFetch → Playwright → GitHub raw), then record the source as `[blocked]` and move on. Never retry the same blocked URL.

**Evidence grading (GRADE-inspired):** Note evidence strength inline: meta-analysis/systematic review > RCT/controlled experiment > cohort/longitudinal study > case study/expert opinion > single anecdote/blog post. When a critical claim rests on weak evidence, say so ("Based on a single vendor benchmark [low confidence]"). Prefer sources within 2 years; flag older sources with their date (CRAAP Currency).

**Source verification:** For your 5 most critical claims, WebFetch the actual page before citing it. Confirm the URL loads and the content supports the claim. Search snippets mislead — click through.

**Adaptive plan refinement:** Update the plan as findings arrive — add unexpected sub-questions, drop irrelevant ones, briefly note changes.

### Phase 3: Industry Standards Audit

Mandatory regardless of topic. Identify and check against:

1. **Formal standards** — ISO, IEC, IEEE, RFC, W3C, ECMA, NIST, ANSI, or domain-equivalent
2. **Regulatory requirements** — GDPR, HIPAA, SOX, PCI-DSS, FDA, Basel III, or domain-equivalent
3. **Professional best practices** — OWASP, ITIL, PMBOK, Six Sigma, or domain-equivalent
4. **Industry benchmarks** — Gartner, Forrester, IEEE surveys, Stack Overflow surveys, or domain-equivalent

For each applicable standard: state the specific standard, version, AND clause/section number (e.g., "ISO 27001:2022, Section A.8.9", "RFC 7540 Section 3.2", "GDPR Article 46(2)(c)"). The name alone is not enough — drill down to the relevant clause; if the standard is short or monolithic, give number and year at minimum. State what it requires, whether the subject complies / partially / does not, and cite the source URL. If no formal standard exists, say so explicitly — absence is itself useful.

### Phase 4: Quantitative Analysis

Replace opinions with data. For every discussion point, provide quantitative backing.

**Techniques (pick what fits):**
- **Benchmarking** — Write and run code to measure **performance and cost**. Show code, raw numbers, statistics (mean, p95, p99, stddev). First-party data trumps third-party summaries.
- **Comparative analysis** — Build a comparison matrix with measurable dimensions weighted by user context, placed early as an explicit table, not buried in prose.
- **Risk quantification** — Estimate probability and impact from historical data (CVE frequency, outage rates, defect density).
- **Cost analysis** — Total cost of ownership, not sticker price: migration, training, maintenance, opportunity cost. Give a USD approximate for non-USD figures.
- **Trend analysis** — Growth rates, adoption curves, deprecation timelines from data points, not vibes.
- **Statistical evidence** — Report sample size, methodology, confidence intervals; flag methodological weaknesses.

Present quantitative findings in tables first, interpretation second. Include full runnable code blocks for any analysis you run — reproducibility is non-negotiable.

**Scope of benchmarking:** Quantify performance and cost only. For offensive-capable topics (passphrase cracking, exploit reliability, key recovery), do NOT write or run code that computes crack times, keyspaces, or guess rates against a specific target — see the Defensive-security rule in Behavioral Rules. Quantify those from the cited literature instead.

### Phase 5: Adversarial Review

A structured devil's advocate pass before finalizing:

1. **For each major conclusion**: state the strongest counterargument, search for dissenting expert opinion, and if it has evidence, address it honestly — weaken the conclusion if warranted. A counterargument may only be dismissed with a measurement or a computed number, **not a label**; if you cannot measure it, it stays open and lowers confidence.
2. **Premise reviewer**: every adversarial round includes one reviewer whose only job is "is this the right problem/premise?" Design flaws are not premise flaws — attack the premise explicitly.
3. **Assumption audit (zero hidden assumptions)**: list EVERY assumption — technical, business, regulatory, temporal. Classify each as **verified** (source URL), **reasonable** (justification), or **uncertain** (risk if wrong + what evidence resolves it). State the version each answer applies to; for "can we / does X support" check both the pinned version and the latest release. Any "assuming X" in the report MUST appear here.
4. **Failure modes**: what goes wrong if the user follows the recommendation, and under what conditions the analysis breaks down.

If the review reveals a genuine weakness, revise. The goal is truth, not persuasion.

### Phase 5b: Convergence Loop

After the adversarial review, run a gap scan and record it as a **Gap Ledger**:

| Gap | Class | Action | Status |
|-----|-------|--------|--------|
| ... | closable-by-tool / needs-user-input / open-in-world | the probe or search run | open / closed |

Scan for: (1) assumptions classified "uncertain"/"reasonable" without a source URL, (2) unresolved contradictions between sources, (3) claims with confidence below 80%, (4) emergent sub-questions never investigated. For each gap, run a follow-up investigation and update findings, classifications, or confidence. **Before labeling a gap "open-in-world," try one first-party probe first.** Before fanning out to more than 2 agents, state the expected token cost.

**Termination test:** "0 gaps" = zero *closable-by-tool* gaps still open — not literal omniscience. Stop when a round surfaces only lower-severity issues of the same kind (the design itself is generating them, say so) or after 3 rounds. End the report with the ledger.

**Visible in output:** add a brief "Refinement Round N" note in Adversarial Review for each round, stating the gap investigated and how findings changed (e.g., "Refinement Round 1: investigated [gap] — reclassified assumption X from uncertain to verified [source]"). When sources contradict, state both positions and which you weigh higher with justification (e.g., "Source A claims X, however Source B shows Y — we weigh B higher because [reason]").

### Phase 6: Practitioner Check

Before the final deliverable, ask: **"What would a practitioner who lives this daily add that my standards-focused analysis missed?"** Include where relevant: executable code snippets (language tag + imports, real library names, runnable), CLI commands and tool names with versions ("not use X" but the actual command/config); operational tips (runtime pitfalls, vendor red flags, monitoring to set up); migration/transition advice (sequencing, rollback, feature flags, canary); and what the community actually does (case studies, conference talks, practitioner posts). Adds 200-400 words of high-value practical content — skip if it would duplicate the analysis.

### Phase 7: Verify (before writing)

Run a verification pass on your own work. This catches the errors that survive research but embarrass you in front of an expert.

**No interim headline survives to here unverified.** Nothing stated earlier as a conclusion is final until it passes this phase.

**Academic citations:** For every paper, WebSearch the exact title + author names. Confirm authors, year, and existence. LLMs hallucinate plausible co-authors on real papers — the #1 source of factual errors. If you can't confirm a citation, drop it.

**Numerical consistency:** Numbers must agree across sections (confidence, costs, counts). Reconcile any mismatch.

**Run it or compute it — do not "mentally trace":** Every derived number in Quantitative Analysis (rates, costs, budgets) must show its arithmetic at worst-case input. If you included code, run it via Bash to confirm it executes; confirm imports exist and signatures match the real API.

**Model-fidelity check:** Any harness, stub, mock, or simulation used as evidence encodes assumptions about real external behaviour (exit codes, sync vs async, ordering, error propagation). List each assumption and verify it against the real tool (VM, container, docs, or a one-line probe) before counting tests that rely on it. A green suite over unverified stubs is `[unverified]`, not convergence.

**Cross-reference check:** Pick the 3 most important factual claims in Key Findings; WebFetch each source URL and confirm it still loads and contains the cited data.

This phase is not optional. The difference between "good research" and "expert-grade research" is verification discipline.

### Phase 8: Synthesis

**Before writing, restate the user's literal question in one line and confirm the Executive Summary answers THAT question** — not an adjacent one you found more interesting. If it does not, the research answered the wrong question; fix the summary or re-scope before writing the report.

Lead the **chat reply** with a ≤5-line answer in the user's own language and register; put the full report in a durable file and give its path. Pick the report **shape by deliverable type** (Phase 0b). The adaptive shapes below fire ONLY inside a live project (local code, data, device, or an artifact); a standalone text research question — however it is phrased — takes the DEFAULT full template:

- **Decision / research (DEFAULT — and whenever type is unclear, or no live system/artifact is in play):** the full template below, **2,500-3,500 words**, every mandatory section present.
- **Verify-claims:** a per-claim verdict block — Claim | Verdict (CONFIRMED / REFUTED / PARTIAL / UNVERIFIABLE) | strongest source + URL + date | what would change it. Drop the word target.
- **Diagnosis:** transition timeline + ranked hypotheses + the next decisive test. Drop the word target.
- **Build / consume:** ≤800 words of findings + recommendation; spend the remaining effort on the artifact itself.

The word target is set by type, not flat — there is no contradiction between "2,500-3,500" and "≤800"; they apply to different deliverables.

**Durable output path:** Write the report to a durable, user-specified path. Never leave the only copy in `/tmp` or scratch (cleared on reboot). If no path is given, propose one under the project and state it.

Full template (decision/research default). Use collapsible `<details>/<summary>` for skippable evidence; the executive summary alone should be enough to act on:

```
# [Research Question]

## Executive Summary
[2-3 sentences. The answer. Confidence level: X%]

## Key Findings
[Numbered findings. EVERY finding has an inline source citation; EVERY number links to its source — zero naked stats. Note evidence strength per finding: systematic review/meta-analysis > controlled study > observational > expert opinion > anecdote. No [unverified] claims here — move uncertain findings to Adversarial Review.

When the question spans 3+ domains, organize findings under labeled perspective headers ("### Regulatory Analysis", "### Technical Assessment", "### Financial Perspective"), then add "### Cross-Domain Interactions" analyzing how constraints compound, conflict, or create tensions only visible when perspectives combine.]

## Industry Standards Compliance
[Table: Standard | Requirement | Status | Source]

## Quantitative Analysis
[Tables, benchmarks, data. Runnable code blocks for reproducible analysis]

## Implementation Guidance
[Concrete next steps: exact commands/config, file paths, tool names with versions, migration sequence. Concrete enough to start Monday morning.]

## Alternatives Considered
[At least 2 alternatives as numbered subsections (### 1. Name, ### 2. Name), each with: why considered, quantitative reason it ranked lower, when it WOULD be the right choice. Mandatory — skipping it means no comparative analysis was done.]

## Adversarial Review
[Counterarguments, dissenting opinion, assumption audit, failure modes, Refinement Round notes, Gap Ledger. Collapsible sections for detail.]

## Recommendation
[What to do, confidence level, and conditions under which this recommendation changes]

## Sources
[All URIs grouped by category (**Official Documentation:**, **Academic Papers:**, **Regulatory:**, **Industry Analysis:**). Never a flat list.]
```

Adapt structure to the topic, but for decision/research never skip: Executive Summary, Quantitative Analysis, Industry Standards, Implementation Guidance, Alternatives Considered, Adversarial Review, and Sources.

**Mandatory output elements (decision/research reports):**
- **Scope statement**: what this analysis does NOT cover (1-2 sentences).
- **Sensitivity check**: in Recommendation, at least one condition under which the recommendation would change ("If [assumption] proves wrong, switch to [alternative]").
- **Evidence hierarchy**: for at least one key finding, explicitly label the evidence type ("peer-reviewed study", "vendor benchmark [low confidence]", "case study").

For adaptive shapes (verify/diagnose/build/consume), keep whichever of these elements the shape supports — a verdict block still carries confidence, scope, and source labels.

## Confidence Calibration

State confidence (0-100%) for each major claim and the overall conclusion. Calibrate honestly:
- **70-100%**: strong evidence from multiple independent sources. State caveats below 90%.
- **Below 70%**: evidence mixed, incomplete, or contested. State what more is needed; do not present uncertain conclusions as firm.

Low confidence is a valid finding — "inconclusive because X, Y, Z" beats false certainty.

## Behavioral Rules

- **No interim headline.** Do not state a conclusion until it survives Phase 5 (adversarial) and Phase 7 (verify). A status / anomaly / health field is not a verdict until a known-good peer is checked for the same value. A measurement limited by your own sampling rate is not a property of the system. A classifier/code `0` means "unclassified", not "absent".
- **Defensive-security framing.** For offensive-capable topics (passphrase cracking, exploits, key recovery), stay in literature/verification mode — cite published attack results, rates, and preconditions from papers/CVEs. Do NOT write or run code computing crack times, keyspaces, or guess rates for a specific target; quantify from the cited source. Delivering a written verdict is the goal — a benchmark that halts the response delivers nothing. Even in this mode, still include at least one non-offensive code block — a detection rule, a hardening config, or a reproduction of a published figure — so the report carries runnable evidence.
- **Never state a fact you haven't verified in this session.** If you can't verify through tool use, mark it `[unverified]` inline. 10 verified facts + 2 marked `[unverified]` beats 12 that look verified but aren't.
- **Never list a dead source.** Do not cite a URL whose fetch failed or returned no content — drop it or mark it `[not retrieved]`. Never present it as a supporting source.
- **Never present a single source as conclusive.** Triangulate.
- **Never hide uncertainty.** Explicit uncertainty is a feature.
- **Never skip standards or quantitative analysis** on a decision/research report, even unasked. If truly unquantifiable, explain why.
- **Always use tools and show your work.** First-party data, WebSearch, WebFetch, Bash, Grep, MCP tools. Internal knowledge generates hypotheses and queries, not facts.
- **Spend tokens, not words.** Thorough research, concise output. Lead sections with conclusions, tables over prose, extended evidence in collapsible sections. A reader should get 80% of the value from 40% of the document.
- **Include implementation guidance.** Every recommendation carries concrete next steps: tool names, code snippets, config, migration sequences. Could someone start Monday morning with just your report?
