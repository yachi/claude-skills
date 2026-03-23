# Comparative Analysis: SCADA-to-IoT Research Quality

**Eval:** scada-to-iot-chemical-plant (eval_id: 4)
**Date:** 2026-03-21

---

## 1. Top-Line Metrics

| Metric | WITH SKILL | WITHOUT SKILL |
|--------|-----------|---------------|
| Word count | 4,470 | 2,328 |
| Grading pass rate | **8/8 (100%)** | **6/8 (75%)** |
| Failed criteria | None | No specific standard clause citations; No confidence level |
| Unique source URLs | ~35 | ~19 |
| Comparison tables | 7 | 2 |
| Explicit confidence level | Yes (82%) | No |
| Counterarguments section | Yes (4 with rebuttals) | No (has "Red Flags" but not adversarial) |
| Methodology section | Yes (8 sub-questions) | No |
| Assumption audit | Yes (7 assumptions tabled) | No |
| Failure modes enumerated | Yes (5) | No |

---

## 2. Unique Source URLs

### WITH SKILL (~35 unique domains/URLs)

Key sources by category:

**Siemens Lifecycle (5)**
- support.industry.siemens.com (discontinuation notice, migration guide, S7-400H EOL)
- eichler-service.com (S7-300 type discontinuation)
- industrialmonitordirect.com (lifecycle analysis)

**IEC Standards & Safety (9)**
- webstore.iec.ch (IEC 61511-1:2016)
- icheme.org (IEC 61511 Ed 2 paper)
- methodfs.com (SIS modification lifecycle)
- exida.com (x2: SIS/BPCS separation, proven-in-use)
- arcweb.com (x2: separation/integration, DCS market)
- intertek.com (IEC 61508 proven-in-use)
- tuvsud.com (IEC 61508)

**Cybersecurity (6)**
- isa.org (IEC 62443 series, TR84.00.09-2024)
- pmc.ncbi.nlm.nih.gov (IIoT mapped to IEC 62443)
- technologyreview.com (TRITON malware)
- ic3.gov (FBI PIN on TRITON)
- en.wikipedia.org (Triton malware)

**Downtime & Migration (6)**
- innovapptive.com ($20B downtime challenge)
- accruent.com (unplanned downtime costs)
- chemicalprocessing.com (hot cutover case study -- Emerald Kalama)
- researchgate.net (pre-migration stress testing)
- avidsolutionsinc.com (DCS migration roadmap)
- control.com (cost per DCS point)

**IoT & OPC UA (4)**
- opcconnect.opcfoundation.org (x2: Dec 2025, Mar 2026 compliance corners)
- isa.org/intech (IIoT in safety applications)
- analog.com (functional safety + Industry 4.0)

**Regulatory (3)**
- osha.gov (29 CFR 1910.119)
- epa.gov (x2: RMP Safer Communities rule, RMP overview)

**Industry Architecture (2)**
- profibus.com (NAMUR NOA)
- arcweb.com (Siemens dual DCS strategy)

### WITHOUT SKILL (~19 unique URLs)

- industrialmonitordirect.com, indmallautomation.com, support.industry.siemens.com, manufacturingtomorrow.com, pteinc.com, elisity.com, isa.org (x2), en.wikipedia.org (x2), emersonautomationexperts.com, prelectronics.com, cse-icon.com, powergearx.com, zscaler.com, dragos.com, trips-group.com, pattiengineering.com, dpstele.com, flowfuse.com

**Notable gaps in without-skill:** No OPC Foundation sources, no OSHA/EPA regulatory URLs, no FBI/TRITON primary source, no IEC webstore link, no exida or intertek for functional safety, no ResearchGate academic sources, no Chemical Processing case study.

---

## 3. Concrete Quantitative Data Points (Top 5 Each)

### WITH SKILL

1. **$100,000/hour** average unplanned downtime in chemical industry (sourced: Innovapptive, Accruent)
2. **10^6 to 10^8+ operating hours** across >=100 installed units required for IEC 61508 proven-in-use (sourced: Intertek, exida)
3. **>900,000 synthetic transactions** in pre-migration stress testing reduces post-cutover defects >98% (sourced: ResearchGate)
4. **$690K-$1,335K** total for S7-1500F migration vs **$1,500K-$3,400K** for full IoT replacement (detailed 15-line-item budget)
5. **5-year risk-adjusted TCO:** $1,160K-$2,025K (hybrid) vs $3,060K-$5,950K (IoT) -- includes probabilistic risk premiums (5%/20% migration failure, 0.1%/1% safety incident)

Additional notable: Downtime sensitivity table showing IoT best-case at $7.7M-$18.8M, worst-case at $35.6M+; 1,750 I/O points in Emerald Kalama case study; OPC UA Safety Cert Lab not operational until 2026.

### WITHOUT SKILL

1. **$150-$400 per I/O point** for PLC/DCS hardware
2. **$4M-$10M+** for full rip-and-replace of SIL-2 chemical plant
3. **$200K-$500K** for SIL verification and safety lifecycle
4. **30-48%** reduction in unplanned downtime from predictive maintenance
5. **40%** of industrial sites have at least one direct connection to a public network

**Key difference:** With-skill provides budget breakdowns at line-item granularity (15 categories for S7-1500F, 9 for IoT replacement) plus risk-adjusted TCO with explicit probability estimates. Without-skill provides rougher ranges without itemization or risk quantification.

---

## 4. Industrial Safety Standards Cited with Section Numbers

### WITH SKILL

| Standard | Specific Sections Referenced |
|----------|----------------------------|
| IEC 61511:2016 | Clause 11.4 (proven-in-use), Clause 11.2.4 (SIS/BPCS independence), MOC requirements |
| IEC 61508-2 | Clause 7.4.10 (proven-in-use definition) |
| IEC 61508-1 | Clause 7.6.2.7 (independence requirements -- different CPUs, OSes, chipsets, power) |
| IEC 61508-6 | Annex D (chi-square confidence intervals for proven-in-use) |
| IEC 62443 | SL 1-4 security levels defined; zone/conduit model referenced |
| ISA TR84.00.09:2024 | Cybersecurity as common-mode failure for SIS |
| NAMUR NE 131/NOA | Second channel architecture |
| IEC 61131-3 | PLC programming standard (5 languages) |
| OSHA 29 CFR 1910.119 | PSM MOC for control system changes |
| EPA 40 CFR Part 68 | RMP requirements; 2024 Safer Communities rule noted |

### WITHOUT SKILL

| Standard | Specific Sections Referenced |
|----------|----------------------------|
| IEC 61511 | Named, no clause numbers |
| IEC 61508 | Named indirectly via SIL discussion, no clause numbers |
| IEC 62443 | Named, zones/conduits mentioned, SL-2/SL-3 target stated, no part/section |
| ISA-95 | Purdue model referenced |

**Verdict:** The with-skill output cites 6 specific clause/annex numbers across 4 parts of IEC 61508/61511. The without-skill output cites zero clause numbers. This is the difference between "we read the standard" and "we know the standard exists."

---

## 5. Structural Features

### Comparison Tables

**WITH SKILL (7 tables):**
1. Cost per I/O point benchmarks (DCS/SCADA/PLC)
2. S7-1500F migration budget (15 line items)
3. IoT replacement cost breakdown (9 items)
4. Risk-adjusted 5-year TCO comparison
5. Downtime sensitivity analysis (4 scenarios)
6. Industry Standards Compliance Matrix (8 standards x 3 columns)
7. Cybersecurity attack surface comparison (6 dimensions)

**WITHOUT SKILL (2 tables):**
1. SCADA vs IoT technical requirements (6 rows)
2. Summary recommendation (7 rows)

### Confidence Level

- **WITH:** 82% stated in executive summary and recommendation. Risk probabilities given for 3 failure modes per option.
- **WITHOUT:** None stated anywhere.

### Counterarguments / Adversarial Review

- **WITH:** Dedicated "Adversarial Review" section with 4 named counterarguments, each with argument/rebuttal structure, plus an assumption audit table (7 assumptions with risk-if-wrong) and 5 enumerated failure modes.
- **WITHOUT:** "Red Flags to Watch For" section (6 bullets) serves a similar purpose but is unidirectional warning rather than structured adversarial engagement. No assumption audit.

### Methodology

- **WITH:** "Research Decomposition" section listing 8 orthogonal sub-questions that structure the entire analysis.
- **WITHOUT:** Topical organization without stated methodology.

---

## 6. Quality of Recommendation

### WITH SKILL

- **4-phase plan** with specific month ranges, budget bands per phase, and deliverables
- Phase 0: FEED + I/O survey + PHA + SIL verification + IEC 62443 assessment + OSHA PSM MOC (Months 1-3, $100K-$150K)
- Phase 1: Safety system migration with hot cutover at annual turnaround (Months 4-12, $300K-$500K)
- Phase 2: SCADA/HMI modernization (Months 10-18, $200K-$400K)
- Phase 3: IoT overlay via NOA second channel (Months 16-24, $150K-$350K)
- Total: $750K-$1,400K with $600K-$1,250K contingency remaining
- **5 explicit conditions** that change the recommendation (I/O count >3K, safety incident, corporate mandate, OPC UA Safety maturity, insurer mandate)
- **3-layer architecture** defined (Safety & Control / SCADA-HMI / IIoT Monitoring)

### WITHOUT SKILL

- **3-phase plan** with year-level granularity and budget bands
- Phase 1: IoT monitoring overlay without touching controls (Year 1, $800K-$1M)
- Phase 2: Migration planning and engineering (Year 2, $400K-$600K)
- Phase 3: Incremental control migration (Year 3+, $600K+/phase)
- Notes $2M-$4M additional needed beyond initial budget
- Summary table with 7 aspects
- No conditions for recommendation change
- No contingency calculation

**Key difference in phasing logic:** The with-skill version migrates the safety/control layer first (Phase 1) and adds IoT last (Phase 3). The without-skill version adds IoT monitoring first (Phase 1) and defers control migration to later phases. The with-skill sequencing is more defensible for a plant with aging safety hardware -- you address the highest-risk element first while the S7-400 is still well-supported.

---

## 7. Grading Results Comparison

| Criterion | WITH | WITHOUT |
|-----------|------|---------|
| >=5 unique verifiable URLs | PASS | PASS |
| >=5 concrete quantitative data points | PASS | PASS |
| IEC 61508/61511 by specific section | **PASS** | **FAIL** |
| Structured cost breakdown / TCO table | PASS | PASS |
| Explicit confidence level | **PASS** | **FAIL** |
| Migration risks (safety case + downtime) | PASS | PASS |
| Clear actionable recommendation | PASS | PASS |
| Methodology + avoids vendor marketing | PASS | PASS |

---

## 8. Verdict

### Which output survives cross-examination by a functional safety engineer or plant manager?

**The with-skill output wins decisively.** Here is why, in the language a functional safety engineer would use:

1. **Standards literacy.** A TUV-certified functional safety engineer will immediately test whether the analyst has actually read the standards. Citing "IEC 61511 Clause 11.4" and "IEC 61508-2 Clause 7.4.10" versus just saying "IEC 61511" is the difference between a competent assessment and a Wikipedia-level summary. The with-skill output demonstrates clause-level familiarity; the without-skill output would fail this test.

2. **Quantified risk.** A plant manager making a $2M capital decision needs to see risk-adjusted numbers, not just ranges. The with-skill output provides probabilistic risk premiums (5% x $2M = $100K for migration failure) and downtime sensitivity analysis showing that even the best-case IoT replacement ($7.7M-$18.8M in downtime cost) exceeds the entire budget. This is the kind of analysis that gets approved at a capital review board.

3. **Adversarial robustness.** The with-skill output anticipates 4 specific objections that management or vendors will raise and provides sourced rebuttals. In a capital approval meeting, the question "but isn't this just kicking the can down the road?" will absolutely be asked. Having a pre-structured answer with evidence (S7-1500 supports OPC UA/MQTT natively, PCS neo designed for 20+ year lifecycle) prevents the recommendation from being derailed.

4. **Regulatory completeness.** The with-skill output covers OSHA PSM (29 CFR 1910.119) and EPA RMP (40 CFR Part 68) requirements. A chemical plant's EHS manager or legal counsel will immediately ask about regulatory compliance during any control system change. The without-skill output does not mention OSHA or EPA at all.

5. **TRITON/TRISIS precedent.** Citing the 2017 TRITON attack on a Saudi petrochemical plant's Schneider Triconex SIS, with both the MIT Technology Review analysis and the FBI Private Industry Notification, is precisely the kind of evidence that converts skeptics. It transforms "cybersecurity is a concern" into "a state-sponsored actor already built malware specifically designed to kill people by disabling safety systems in plants like yours."

### What specific things does the with-skill version do that the baseline does not?

1. **Research decomposition into 8 sub-questions** -- visible methodology that makes the analysis auditable
2. **Clause-level IEC 61508/61511 citations** (5 specific clause/annex references)
3. **Explicit 82% confidence level** with granular risk probabilities
4. **Line-item budget tables** (15 items for S7-1500F, 9 for IoT replacement)
5. **Risk-adjusted 5-year TCO** with probabilistic failure/downtime/safety premiums
6. **Downtime sensitivity analysis** (4 scenarios from 8-hour best to 336+ hour worst)
7. **Industry Standards Compliance Matrix** (8 standards x 3 columns)
8. **Cybersecurity attack surface comparison table** (6 dimensions)
9. **Adversarial review** with 4 counterargument/rebuttal pairs
10. **Assumption audit** (7 assumptions with risk-if-wrong)
11. **5 enumerated failure modes** with mitigations
12. **5 conditions that change the recommendation**
13. **OSHA PSM and EPA RMP regulatory coverage**
14. **TRITON/TRISIS case study** with FBI and MIT Technology Review sources
15. **OPC UA Safety certification timeline** (sourced from OPC Foundation compliance corners)
16. **Emerald Kalama Chemical hot cutover case study** (1,750 I/O points, sourced from Chemical Processing)
17. **Pre-migration stress testing research** (900K synthetic transactions, >98% defect reduction)

### What (if anything) does the baseline do better?

1. **Communication style for non-technical stakeholders.** The "honest pitch" analogy ("replacing the engine of a running car with a bicycle motor because the bicycle has GPS") is more memorable and persuasive for a management audience than anything in the with-skill output. The with-skill output is written for engineers; the without-skill output has a section explicitly for "What to Tell Your Management."

2. **Readability and conciseness.** At 2,328 words vs 4,470, the without-skill output is more likely to be read cover-to-cover by a busy plant manager. The with-skill output is dense and demands engagement.

3. **Spare parts stockpiling advice.** The without-skill output explicitly recommends stockpiling critical S7-400 components (CPUs, power supplies, communication processors) while prices are current. This is practical, actionable advice that the with-skill output omits.

4. **"Red Flags to Watch For" section.** While less rigorous than the adversarial review, this section is more actionable as a vendor-screening checklist. It is something an operations manager could hand to procurement.

5. **ISA-95/Purdue model reference.** The without-skill output explicitly references the Purdue/ISA-95 model for network segmentation, which is a practical framework that OT security teams use daily. The with-skill output focuses on IEC 62443 zones/conduits without naming Purdue.

---

## 9. Final Score

| Dimension | WITH SKILL | WITHOUT SKILL |
|-----------|-----------|---------------|
| Technical depth | 9/10 | 6/10 |
| Standards compliance rigor | 10/10 | 4/10 |
| Quantitative analysis | 9/10 | 5/10 |
| Source quality & breadth | 9/10 | 6/10 |
| Adversarial robustness | 9/10 | 3/10 |
| Actionability of recommendation | 9/10 | 7/10 |
| Management communication | 6/10 | 8/10 |
| Readability / conciseness | 6/10 | 8/10 |
| Regulatory coverage | 9/10 | 3/10 |
| **Overall (weighted toward cross-examination survival)** | **8.7/10** | **5.4/10** |

The with-skill output is the one you bring to a functional safety audit. The without-skill output is a decent briefing document. They are not in the same league for decision-quality analysis.
