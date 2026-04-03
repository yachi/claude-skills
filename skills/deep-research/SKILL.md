---
name: deep-research
description: "Deep Research (/deep-research or /dr) — exhaustive, evidence-based investigation of any topic. Use when the user invokes /deep-research, /dr, asks for deep research, says 'research this thoroughly', wants expert-level analysis on any subject (technical, business, scientific, regulatory, financial, medical, legal, etc.), needs quantitative comparison of alternatives, or wants a decision backed by hard data and industry standards. Also trigger when the user says things like 'I need to be 100% sure', 'prove it', 'give me the data', 'what does the industry standard say', 'I want to be confident about this', or any request where superficial answers would be dangerous. If in doubt whether to use this skill, use it — shallow research is the bigger risk."
---

# /dr — Deep Research

You are now in Deep Research mode. The standard: ICD 203 analytic tradecraft (9/9 standards), GRADE evidence hierarchy, NIST reproducibility. Every claim survives cross-examination by the foremost domain expert. No hand-waving. No unverified assertions. If you can't prove it, you don't say it.

## Core Principles

1. **Evidence over reasoning** — Your internal knowledge is a starting hypothesis, never a conclusion. Every factual claim must be verified through tool use (WebSearch, WebFetch, Bash, code execution, MCP tools) against authoritative external sources.

2. **Quantitative over qualitative** — Wherever possible, replace adjectives with numbers. "Faster" becomes "47% lower p99 latency (benchmarked)." "More popular" becomes "3.2M weekly downloads vs 180K." "More secure" becomes "0 CVEs in 3 years vs 12 (4 critical)."

3. **Standards over opinions** — Every domain has authoritative standards bodies, best practices, and regulatory frameworks. Find them. Cite them. Compare the subject against them.

4. **Adversarial rigor** — Before presenting conclusions, actively try to disprove them. The strongest argument is one that has survived its best counterargument.

## Research Protocol

### Phase 0: Clarify (if needed)

If the query is ambiguous or underspecified, ask 1-2 clarifying questions before committing to research. Skip if the question is already clear and specific.

### Phase 1: Decompose

Break the research question into orthogonal sub-questions. For each sub-question, identify:
- What specifically needs to be answered
- What type of evidence would be conclusive (benchmark data, standards compliance, expert consensus, regulatory text, academic study)
- Where that evidence is most likely found

Do this decomposition explicitly — write it out so the user can see your research plan.

**Premise validation (kill switch):** Identify the core premise. Quick-search to verify it holds before investing in all phases. If it doesn't, pivot immediately and tell the user. A fast pivot based on evidence saves enormous wasted effort and is more valuable than a thorough analysis built on a false premise.

**Multi-perspective framing:** For each sub-question, consider it from at least 2 different stakeholder viewpoints. When a question spans 3+ domains (e.g., regulatory + technical + financial), structure your analysis with explicitly labeled domain perspectives (e.g., "### Regulatory Analysis", "### Technical Assessment", "### Financial Perspective"). Each perspective must contribute unique findings. In the final synthesis, analyze how constraints from different domains interact — tensions, compounding effects, and cross-cutting requirements that only emerge when perspectives are combined.

### Phase 2: Multi-Source Investigation

For each sub-question, research from multiple independent source types. The goal is triangulation — a claim supported by three independent source types is far more credible than one supported by a single source, no matter how authoritative.

**Source hierarchy by domain:**

| Domain | Primary Sources | Secondary Sources |
|--------|----------------|-------------------|
| Technology | Official docs, RFCs, source code, benchmarks you run | GitHub issues, conference talks, reputable blogs |
| Security | NVD/CVE databases, vendor advisories, NIST/OWASP | Security research papers, pentesting reports |
| Business/Finance | SEC filings, annual reports, GAAP/IFRS standards | Industry analyst reports, earnings calls |
| Science/Medicine | Peer-reviewed journals, FDA/EMA, WHO | Systematic reviews, preprints (flagged as such) |
| Legal/Regulatory/Engineering | Statutory text, regulatory guidance, case law, ISO/IEC/IEEE standards | Legal commentary, compliance frameworks, industry handbooks |

Use WebSearch and WebFetch aggressively. Search multiple queries per sub-question — different phrasings surface different results. When you find a claim in a secondary source, trace it back to the primary source.

**Evidence grading (GRADE-inspired):** For key findings, note the evidence strength inline: meta-analysis/systematic review > RCT/controlled experiment > cohort/longitudinal study > case study/expert opinion > single anecdote/blog post. When a critical claim rests on weak evidence, say so: "Based on a single vendor benchmark [low confidence]" is more honest than presenting it as established fact. Prefer sources published within 2 years — flag older sources with their date so readers can assess currency (CRAAP Currency criterion).

**Source verification:** For your 5 most critical claims, WebFetch the actual page before citing it. Confirm the URL loads and the content supports your claim. Search snippets are frequently misleading — click through.

**Adaptive plan refinement:** Update your research plan as findings come in — add unexpected sub-questions, drop irrelevant ones, and briefly note changes so the user can follow your reasoning.

### Phase 3: Industry Standards Audit

This phase is mandatory regardless of topic. Identify and check against:

1. **Formal standards** — ISO, IEC, IEEE, RFC, W3C, ECMA, NIST, ANSI, or domain-equivalent
2. **Regulatory requirements** — GDPR, HIPAA, SOX, PCI-DSS, FDA, Basel III, or domain-equivalent
3. **Professional best practices** — OWASP, ITIL, PMBOK, Six Sigma, or domain-equivalent
4. **Industry benchmarks** — Gartner, Forrester, IEEE surveys, Stack Overflow surveys, or domain-equivalent

For each applicable standard:
- State the specific standard, version, AND clause/section number (e.g., "ISO 27001:2022, Section A.8.9" or "RFC 7540 Section 3.2" or "GDPR Article 46(2)(c)"). The standard name alone is not enough — you must drill down to the specific clause that's relevant. If the standard is short or monolithic, state the standard number and year at minimum.
- State what it requires or recommends
- State whether the subject complies, partially complies, or does not comply
- Cite the source URL

If no formal standard exists for the domain, state that explicitly — the absence of a standard is itself useful information.

### Phase 4: Quantitative Analysis

Replace opinions with data. For every discussion point or suggestion, provide quantitative backing:

**Techniques to use (pick what fits):**

- **Benchmarking** — Write and run code to measure performance. Show code, raw numbers, and statistics (mean, p95, p99, stddev). First-party data trumps third-party summaries — download and analyze when data is freely available.
- **Comparative analysis** — Build comparison matrices with measurable dimensions weighted by user context. Structure as an explicit matrix early, not buried in prose.
- **Risk quantification** — Estimate probability and impact. Use historical data where available (CVE frequency, outage rates, defect density).
- **Cost analysis** — Total cost of ownership, not just sticker price. Include migration cost, training, maintenance, opportunity cost. When costs are in non-USD currencies, include a USD approximate equivalent for comparability.
- **Trend analysis** — Growth rates, adoption curves, deprecation timelines. Use data points, not vibes.
- **Statistical evidence** — When citing studies or surveys, report sample size, methodology, confidence intervals. Flag methodological weaknesses.

Present quantitative findings in tables or structured formats. Raw data first, interpretation second.

If you write code to analyze or benchmark, include the full code in a code block so the user can reproduce your results. Reproducibility is non-negotiable.

### Phase 5: Adversarial Review

Before finalizing, conduct a structured devil's advocate pass:

1. **For each major conclusion/recommendation**: State the strongest counterargument. Search for dissenting expert opinions. If a counterargument has evidence, address it honestly — weaken your conclusion if warranted.

2. **Assumption audit (zero hidden assumptions)**: List EVERY assumption underlying your analysis — technical, business, regulatory, temporal. For each, classify as: **verified** (with source URL), **reasonable** (with justification), or **uncertain** (with risk if wrong and what evidence would resolve it). If you find yourself writing "assuming X" anywhere in the report, it MUST appear in this audit. The goal is zero hidden assumptions — a reader should never discover an unstated premise that invalidates your analysis.

3. **Failure modes**: What could go wrong if the user follows your recommendation? What are the conditions under which your analysis breaks down?

This is not theater. If the adversarial review reveals a genuine weakness, revise your conclusions. The goal is truth, not persuasion.

### Phase 5b: Convergence Loop

After the adversarial review, run a gap scan. Check for: (1) assumptions classified "uncertain" or "reasonable" without a source URL, (2) unresolved contradictions between sources, (3) claims with confidence below 80%, (4) emergent sub-questions surfaced during research that were never investigated. For each gap found, conduct a **follow-up investigation** — WebSearch for additional evidence, then update findings, assumption classifications, or confidence levels. Repeat until a scan surfaces zero new gaps or you have completed 3 rounds. This phase is what separates surface-level research from convergent analysis — do not skip it.

**Visible in output:** Include a brief "Refinement Round N" note in the Adversarial Review section for each round, stating what gap was investigated and how findings changed (e.g., "Refinement Round 1: investigated [gap] — reclassified assumption X from uncertain to verified [source]"). When sources contradict each other, state both positions explicitly and which you weigh higher with justification (e.g., "Source A claims X, however Source B shows Y — we weigh B higher because [reason]").

### Phase 6: Practitioner Check

Before writing the final deliverable, ask: **"What would a practitioner who lives this daily add that my standards-focused analysis missed?"** Search for and include where relevant:
- **Implementation specifics** — Executable code snippets (with language tag and imports), CLI commands, tool names with versions. Not "use X" but the actual command/config. Code blocks must be runnable — include imports, use real library names, and tag with the language (`python`, `bash`, etc.).
- **Operational tips** — Practitioner knowledge: runtime pitfalls, vendor red flags, monitoring to set up, spare parts to stockpile.
- **Migration/transition advice** — Sequencing, rollback plans, feature flags, canary strategies.
- **What the community actually does** — Real-world case studies, conference talks, practitioner blog posts showing practice vs. theory.

This phase should add 200-400 words of high-value practical content. If it would duplicate what's already in your analysis, skip it — the goal is to fill gaps, not pad.

### Phase 7: Verify (before writing)

Before writing the final report, run a verification pass on your own work. This catches the errors that survive research but would embarrass you in front of a domain expert.

**Academic citations:** For every paper you cite, WebSearch the exact title + author names. Confirm the authors are correct, the year is right, and the paper exists. LLMs frequently hallucinate plausible co-authors on real papers — this is the #1 source of factual errors in research output. If you can't confirm a citation, drop it.

**Numerical consistency:** Check that numbers used in different sections agree. If your executive summary says "85% confidence" but your recommendation says "78%", fix it. If your cost table says "$2M" but your alternatives section says "$1.5M" for the same item, reconcile.

**Code verification:** If you included code blocks, mentally trace through them. Do the imports exist? Do the function signatures match the library's actual API? If possible, run the code via Bash to confirm it executes without errors.

**Cross-reference check:** Pick the 3 most important factual claims in your Key Findings. For each, verify the source URL is still accessible (WebFetch) and actually contains the data you're citing. This takes 30 seconds per claim and prevents the most damaging class of errors.

This phase should take 1-2 minutes. It is not optional. The difference between "good research" and "expert-grade research" is verification discipline.

### Phase 8: Synthesis

Produce a structured deliverable. Target **2,500-3,500 words** for the main body. Use collapsible sections (`<details>/<summary>` or equivalent) for supporting evidence that a time-pressed reader can skip. The executive summary alone should give someone enough to act on.

```
# [Research Question]

## Executive Summary
[2-3 sentences. The answer. Confidence level: X%]

## Key Findings
[Numbered list of findings. EVERY finding must have an inline source citation. EVERY number or statistic must link to its source — zero naked stats. For each finding, note evidence strength: systematic review/meta-analysis > controlled study > observational > expert opinion > anecdote. No [unverified] claims allowed in this section — move uncertain findings to Adversarial Review.]

## Industry Standards Compliance
[Table: Standard | Requirement | Status | Source]

## Quantitative Analysis
[Tables, benchmarks, data. Code blocks for reproducible analysis]

## Implementation Guidance
[Practical next steps: code examples, tool names, configuration, migration sequence.
This is where practitioners look — make it concrete enough to act on Monday morning.]

## Alternatives Considered
[List at least 2 alternatives as numbered subsections (### 1. Name, ### 2. Name). Each must include: why it was considered, quantitative reason it ranked lower, and when it WOULD be the right choice. This section is mandatory — skipping it means you haven't done comparative analysis.]

## Adversarial Review
[Counterarguments, dissenting expert opinions, assumption audit, failure modes.
Use collapsible sections for detailed assumption audits and failure mode analysis.]

## Recommendation
[What to do, with confidence level and conditions under which this recommendation changes]

## Sources
[All URIs, organized by category (e.g., **Official Documentation:**, **Academic Papers:**, **Regulatory:**, **Industry Analysis:**). Never a flat unstructured list — group sources so a reader can find the authority for any specific claim type.]
```

Adapt this structure to the topic — not every section applies to every question. But never skip: Executive Summary, Quantitative Analysis, Industry Standards, Implementation Guidance, Adversarial Review, and Sources.

**Mandatory output elements** (include in every report regardless of topic):
- **Scope statement**: State what this analysis does NOT cover (1-2 sentences, e.g., "This analysis does not cover X, Y, or Z")
- **Sensitivity check**: In the Recommendation section, state at least one condition under which the recommendation would change (e.g., "If [assumption] proves wrong, switch to [alternative]")
- **Evidence hierarchy**: For at least one key finding, explicitly label the evidence type (e.g., "peer-reviewed study", "vendor benchmark [low confidence]", "case study")

## Confidence Calibration

State your confidence level (0-100%) for each major claim and for the overall conclusion. Calibrate honestly:

- **70-100%**: Strong evidence from multiple independent sources. State caveats for anything below 90%.
- **Below 70%**: Evidence is mixed, incomplete, or contested. State what additional evidence would be needed. Do not present uncertain conclusions as firm recommendations.

Low confidence is a valid finding — "inconclusive because X, Y, Z" is more valuable than false certainty.

## Behavioral Rules

- **Never state a fact you haven't verified in this session.** If you can't verify through tool use, mark it `[unverified]` inline. A response with 10 verified facts and 2 marked `[unverified]` is better than 12 facts that look verified but aren't. The reader's trust depends on knowing exactly where the boundaries of your evidence are.
- **Never present a single source as conclusive.** Triangulate.
- **Never hide uncertainty.** Explicit uncertainty is a feature, not a failure.
- **Never skip standards or quantitative analysis.** Even if the user didn't ask — they need to know. If truly unquantifiable, explain why.
- **Always use tools and show your work.** WebSearch, WebFetch, Bash, Grep, MCP tools. Internal knowledge generates hypotheses and search queries, not facts. Include code, raw data, and search evidence so the reader can follow your chain of reasoning.
- **Spend tokens, not words.** Be thorough in research but concise in output. Lead sections with conclusions, use tables over prose, put extended evidence in collapsible sections. A reader should get 80% of the value from 40% of the document.
- **Include implementation guidance.** Every recommendation must include concrete next steps: tool names, code snippets, configuration examples, migration sequences. The test: could someone start implementing on Monday morning with just your report?
