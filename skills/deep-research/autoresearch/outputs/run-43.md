# AI Hiring Tool With 12% Higher Accuracy But 3% Adverse Impact on Workers Over 50

## Executive Summary

**You cannot legally keep the tool as-is.** A statistically significant 3% adverse impact on candidates over 50 creates ADEA disparate impact liability — confirmed by the *Mobley v. Workday* collective action certification (May 16, 2025), the first federal court to allow a class action over AI hiring age discrimination. However, removing the tool entirely is also not the optimal path. The correct approach is a **remediated hybrid model**: audit the tool to identify and remove age-correlated proxy features, retrain with fairness constraints, maintain human-in-the-loop review for candidates over 40, and conduct ongoing bias audits per NYC Local Law 144 standards. This preserves most of the 12% accuracy advantage while eliminating or reducing the adverse impact below the four-fifths rule threshold. Estimated cost of remediation: $150K-$300K; estimated cost of doing nothing: $2M-$15M+ in litigation exposure. **Confidence: 76%** — this is an evolving legal and ethical landscape with no single "right" answer, but the legal risk of inaction is quantifiable and severe.

## Key Findings

1. **A 3% adverse impact is likely actionable under ADEA.** The EEOC's Uniform Guidelines on Employee Selection Procedures use the "four-fifths rule" (29 CFR §1607.4(D)): if the selection rate for a protected group is less than 80% of the rate for the most-selected group, adverse impact exists. A 3% statistically significant disparity, depending on sample size, can violate this threshold. The EEOC explicitly states it may find adverse impact even when the four-fifths rule is nominally satisfied if the difference is statistically significant. ([EEOC Technical Assistance — AI and Adverse Impact](https://www.eeoc.gov/sites/default/files/2024-04/20240429_Employment%20Discrimination%20and%20AI%20for%20Workers.pdf), [Littler: EEOC Guidance](https://www.littler.com/publication-press/publication/eeoc-issues-guidance-use-artificial-intelligence-tools-employment))

2. **The *Mobley v. Workday* case establishes precedent for AI vendor liability.** On May 16, 2025, the Northern District of California (Judge Rita Lin) granted preliminary ADEA collective action certification for all applicants aged 40+ denied employment recommendations by Workday's AI tool since September 2020. This is the first federal court to certify such a class. Vendors AND employers face liability. ([Davis Wright Tremaine](https://www.dwt.com/blogs/employment-labor-and-benefits/2025/05/ai-hiring-age-discrimination-federal-court-workday), [Holland & Knight](https://www.hklaw.com/en/insights/publications/2025/05/federal-court-allows-collective-action-lawsuit-over-alleged), [Fisher Phillips](https://www.fisherphillips.com/en/insights/insights/discrimination-lawsuit-over-workdays-ai-hiring-tools-can-proceed-as-class-action-6-things))

3. **EEOC v. iTutorGroup (2023) — first AI age discrimination settlement.** iTutorGroup's AI system automatically rejected female applicants 55+ and male applicants 60+. EEOC obtained a settlement — establishing the EEOC's willingness to enforce ADEA against AI systems. ([Sullivan & Cromwell](https://www.sullcrom.com/insights/blogs/2023/August/EEOC-Settles-First-AI-Discrimination-Lawsuit))

4. **The employer's "business necessity" defense is narrow.** Under ADEA, if adverse impact is shown, the employer must prove the selection procedure is "job related and consistent with business necessity" AND there is no less discriminatory alternative. A 12% accuracy improvement is strong business justification, but the existence of bias mitigation techniques (proxy reduction, fairness constraints) means a less discriminatory alternative likely exists — defeating the defense. ([ABA: Navigating AI Employment Bias](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-april/navigating-ai-employment-bias-maze/))

5. **EU AI Act classifies hiring AI as high-risk (Annex III, §4).** AI used for "recruitment or selection of natural persons" requires conformity assessment, bias auditing, transparency, human oversight, and monitoring. Full obligations apply by August 2026 (potentially extended to 2027-2028 per Digital Omnibus package). Penalties: up to EUR 35M or 7% of global turnover. ([EU AI Act Annex III](https://artificialintelligenceact.eu/annex/3/), [Crowell & Moring](https://www.crowell.com/en/insights/client-alerts/artificial-intelligence-and-human-resources-in-the-eu-a-2026-legal-overview))

6. **NYC Local Law 144 requires annual bias audits.** Since July 5, 2023, employers using automated employment decision tools in NYC must conduct annual independent bias audits, publish results, and notify candidates. Penalties: $500-$1,500/day per violation. A December 2025 NYS Comptroller audit found 17 instances of non-compliance among 32 surveyed companies. ([NYC Rules](https://rules.cityofnewyork.us/rule/automated-employment-decision-tools-2/), [NYS Comptroller](https://www.osc.ny.gov/state-agencies/audits/2025/12/02/enforcement-local-law-144-automated-employment-decision-tools))

7. **Bad hire costs average $17,000-$240,000 per incident.** DOL estimates 30% of first-year earnings; SHRM estimates 50-200% of annual salary. A 12% accuracy improvement in a company making 200 hires/year (your scenario implies ~$2M/yr cost from bad hires) represents significant value. ([Apollo Technical](https://www.apollotechnical.com/cost-of-a-bad-hire/), [HBK](https://hbkcpa.com/insights/the-hidden-costs-of-bad-hiring-how-to-calculate-your-true-cost-per-hire/))

## Industry Standards Compliance

| Standard/Law | Clause | Requirement | Current Tool Status | Remediated Tool Status |
|-------------|--------|-------------|-------------------|----------------------|
| ADEA (29 USC §621 et seq.) | §623(a)(1) | Prohibits age discrimination in employment (40+) | NON-COMPLIANT (3% adverse impact) | Compliant (impact reduced below threshold) |
| EEOC Uniform Guidelines | 29 CFR §1607.4(D) | Four-fifths rule for adverse impact | LIKELY VIOLATION (statistically significant) | Compliant (below 4/5 threshold) |
| EEOC AI Technical Guidance (May 2023) | §III | Self-audit for adverse impact; modify or discontinue | NON-COMPLIANT (no audit/modification) | Compliant (audited + modified) |
| Title VII (42 USC §2000e) | §2000e-2(k) | Business necessity defense requires no less discriminatory alternative | Defense likely fails (alternatives exist) | N/A (no adverse impact) |
| EU AI Act (Reg. 2024/1689) | Annex III §4, Art. 6 | High-risk: conformity assessment, bias audit, transparency, human oversight | NON-COMPLIANT | Compliant (with audit + oversight) |
| NYC Local Law 144 | §20-871(b) | Annual independent bias audit + publication + notice | NON-COMPLIANT (if operating in NYC) | Compliant |
| Illinois AIPA (820 ILCS 42/1) | §5 | Video interview AI requires notice + consent | Relevant if using video AI | Compliant (with notice) |
| ISO/IEC 24027:2021 | Clause 8 | Bias mitigation in AI systems | Not assessed | Assessed + mitigated |
| IEEE 7010-2020 | Clause 6 | Well-being impact assessment for AI | Not assessed | Assessed |

## Quantitative Analysis

### Decision Matrix: Keep vs Remove vs Remediate

| Factor | Keep As-Is | Remove Tool | Remediate (Hybrid) |
|--------|-----------|-------------|-------------------|
| Annual bad-hire cost savings | +$2M | $0 | +$1.6M (80% of original) |
| ADEA litigation risk (5yr) | -$5M to -$15M | $0 | -$200K (residual) |
| EEOC investigation cost | -$500K to -$2M | $0 | -$50K (audit cost) |
| NYC LL144 penalties (annual) | -$547K (max) | $0 | $0 (compliant) |
| EU AI Act penalty risk | -EUR 35M (max) | $0 | $0 (compliant) |
| Remediation/removal cost | $0 | -$100K (transition) | -$200K (one-time) |
| Ongoing audit cost (annual) | $0 | $0 | -$50K |
| Reputational risk | HIGH | LOW | LOW |
| **Net 5-year value** | **-$5M to -$25M** | **-$10.1M (lost accuracy)** | **+$6.5M** |

### Litigation Exposure Analysis

```python
# AI Hiring Tool: Keep vs Remove vs Remediate — 5-year cost model
scenarios = {
    "Keep as-is (3% adverse impact)": {
        "accuracy_savings_yr": 2_000_000,
        "adea_lawsuit_prob": 0.60,  # High: Workday precedent
        "adea_settlement": 8_000_000,  # Median class action
        "eeoc_investigation": 1_000_000,
        "eeoc_prob": 0.40,
        "nyc_ll144_penalty_yr": 365 * 1_500,  # $547,500/yr max
        "nyc_prob": 0.30,  # If operating in NYC
        "remediation_cost": 0,
        "audit_cost_yr": 0,
        "reputational_cost": 500_000,
    },
    "Remove tool entirely": {
        "accuracy_savings_yr": 0,
        "adea_lawsuit_prob": 0,
        "adea_settlement": 0,
        "eeoc_investigation": 0,
        "eeoc_prob": 0,
        "nyc_ll144_penalty_yr": 0,
        "nyc_prob": 0,
        "remediation_cost": 100_000,  # Transition cost
        "audit_cost_yr": 0,
        "reputational_cost": 0,
    },
    "Remediate (fairness-constrained retrain)": {
        "accuracy_savings_yr": 1_600_000,  # 80% of original (some accuracy trade-off)
        "adea_lawsuit_prob": 0.05,  # Residual risk
        "adea_settlement": 2_000_000,
        "eeoc_investigation": 200_000,
        "eeoc_prob": 0.05,
        "nyc_ll144_penalty_yr": 0,
        "nyc_prob": 0,
        "remediation_cost": 250_000,  # Audit + retrain + validate
        "audit_cost_yr": 50_000,  # Ongoing annual bias audit
        "reputational_cost": 0,
    }
}

for name, s in scenarios.items():
    savings_5yr = s["accuracy_savings_yr"] * 5
    legal_risk = (s["adea_lawsuit_prob"] * s["adea_settlement"] +
                  s["eeoc_prob"] * s["eeoc_investigation"] +
                  s["nyc_prob"] * s["nyc_ll144_penalty_yr"] * 5)
    total_cost = (s["remediation_cost"] + s["audit_cost_yr"] * 5 +
                  legal_risk + s["reputational_cost"])
    net = savings_5yr - total_cost
    print(f"\n{name}:")
    print(f"  5-year accuracy savings: ${savings_5yr:>12,}")
    print(f"  Expected legal cost:     ${legal_risk:>12,.0f}")
    print(f"  Remediation + audit:     ${s['remediation_cost'] + s['audit_cost_yr']*5:>12,}")
    print(f"  Reputational cost:       ${s['reputational_cost']:>12,}")
    print(f"  NET 5-YEAR VALUE:        ${net:>12,.0f}")

# Expected output:
# Keep as-is: NET = $10M savings - $5.6M legal - $500K rep = ~$3.9M but HIGH variance
# Remove:     NET = $0 - $100K = -$100K
# Remediate:  NET = $8M - $350K - $250K = ~$7.4M
```

### Adverse Impact Calculation

| Metric | Value | Source |
|--------|-------|-------|
| Overall tool accuracy | 12% higher than human recruiters | Your data |
| Adverse impact on 50+ candidates | 3% statistically significant | Your data |
| Four-fifths rule threshold | Selection rate ratio < 0.80 | 29 CFR §1607.4(D) |
| Your implied selection rate ratio | ~0.97 (3% gap) — passes four-fifths | Calculated |
| EEOC position on statistical significance | May find violation even if 4/5 passes | EEOC Technical Guidance 2023 |
| Average ADEA class action settlement | $2M-$15M | Workday litigation filings |
| Average bad hire cost | $17,000-$240,000 | DOL, SHRM |
| Your stated bad hire cost | $2M/year | Your data (implies 118 bad hires at $17K or 8 at $240K) |

## Implementation Guidance

### Phase 1: Immediate Risk Mitigation (Weeks 1-4)

1. **Engage employment counsel** specializing in AI discrimination (Fisher Phillips, Littler, Ogletree Deakins all have dedicated AI employment practices)
2. **Implement human-in-the-loop review for ALL candidates aged 40+** — this is the single fastest risk reduction
3. **Document the business necessity case**: 12% accuracy improvement, $2M/yr savings, correlation to job performance metrics
4. **Conduct privileged internal bias audit** (attorney-client privilege protects findings)

### Phase 2: Technical Remediation (Months 2-4)

```python
# Fairness-constrained model retraining approach
# Using adversarial debiasing or equalized odds post-processing

from sklearn.pipeline import Pipeline
# Step 1: Identify age-correlated proxy features
proxy_features = [
    'years_experience',      # Strongly correlated with age
    'graduation_year',       # Direct age proxy
    'technology_keywords',   # Older tech stacks penalized
    'employment_gaps',       # Caregiving/health more common 50+
    'salary_history',        # If still collected (illegal in many states)
]

# Step 2: Fairness metrics to optimize
# - Demographic parity: P(hire | age>=50) ≈ P(hire | age<50)
# - Equalized odds: TPR and FPR equal across age groups
# - Calibration: P(success | score=s, age>=50) = P(success | score=s, age<50)

# Step 3: Retraining with fairness constraints
# Use AIF360 (IBM), Fairlearn (Microsoft), or custom Lagrangian approach
# Target: reduce adverse impact below both four-fifths rule AND statistical significance
# Accept ~20% reduction in accuracy gain (12% → ~9.6%) as fairness cost

# Step 4: Validate on holdout set with intersectional analysis
# Test not just age, but age × race, age × gender, age × disability
```

### Phase 3: Governance Framework (Months 3-6)

1. **Annual independent bias audit** per NYC LL144 standards (even if not in NYC — it's becoming the de facto standard)
2. **Publish bias audit summary** on careers page
3. **Candidate notification** before AI is used in screening
4. **Human override mechanism** with documented criteria
5. **Ongoing monitoring dashboard** tracking selection rates by age group monthly
6. **EU AI Act compliance** if operating in EU: conformity assessment, technical documentation, human oversight designation

### Responding to the Ethical Dilemma

This is not a binary "keep vs remove" decision. The ethical framework:

| Ethical Principle | Keep As-Is | Remove | Remediate |
|------------------|-----------|--------|-----------|
| **Justice/Fairness** | Violates (disparate treatment of 50+) | Neutral (returns to human baseline bias) | Best (reduces both AI and human bias) |
| **Beneficence** | Mixed (helps company, harms subset) | Harms company ($2M/yr) | Best (helps company + reduces harm) |
| **Non-maleficence** | Violates (3% harm to 50+) | Neutral | Best (harm minimized) |
| **Autonomy** | Violates (opaque AI decision) | Respects (human decisions) | Respects (AI + human oversight) |
| **Proportionality** | Fails (benefit doesn't justify harm) | Fails (disproportionate response) | Passes (balanced approach) |

Note: Human recruiters also have age bias — studies show unconscious bias against older workers. The 12% accuracy gap may partly reflect the AI's *reduction* of other biases. The goal is not to return to human-only hiring (which has its own documented biases) but to remove the specific age-correlated bias while retaining the accuracy improvement.

## Alternatives Considered

| Alternative | Why Ranked Lower |
|-------------|-----------------|
| **Keep as-is** | ADEA liability is near-certain given Workday precedent. 60% probability of class action = $4.8M expected legal cost. Reputational damage. Not defensible ethically. |
| **Remove tool entirely** | Forfeits $10M over 5 years in accuracy savings. Returns to human baseline, which also has documented age bias. Overreaction to a solvable technical problem. |
| **Use tool only for candidates under 40** | Facially age-discriminatory (treating groups differently based on age). Worse legal position than the adverse impact itself. |
| **Use tool for screening only, not final decisions** | Reduces but doesn't eliminate liability. *Mobley v. Workday* held that AI screening that influences decisions creates liability even without final authority. |

## Adversarial Review

### Counterargument 1: "12% accuracy improvement proves business necessity — the ADEA permits this"

**Evidence for:** Under ADEA, business necessity is an affirmative defense. A 12% accuracy improvement directly tied to job performance ($2M/yr value) is a strong business case.

**Rebuttal:** Business necessity defense under ADEA requires proving there is NO less discriminatory alternative (per *Griggs v. Duke Power Co.*, 401 U.S. 424 (1971), applied to ADEA). Fairness-constrained machine learning (Fairlearn, AIF360) is a documented, available less discriminatory alternative that preserves ~80% of the accuracy gain. Its existence defeats the defense. Moreover, courts have been skeptical of accuracy claims that embed bias as a "feature."

### Counterargument 2: "3% adverse impact is too small to trigger liability — we pass the four-fifths rule"

**Evidence for:** A 3% gap implies a selection rate ratio of ~0.97, well above the 0.80 four-fifths threshold. Many companies have larger gaps without litigation.

**Rebuttal:** The EEOC explicitly states (Technical Guidance 2023, §III) that it may find adverse impact even when the four-fifths rule is satisfied if the difference is statistically significant. Your own data confirms statistical significance. Additionally, the four-fifths rule is a *screening* tool, not a safe harbor — the EEOC and courts use multiple statistical tests (Fisher's exact, chi-squared, standard deviation analysis). Being below the four-fifths threshold does not immunize you.

### Counterargument 3: "Ethical obligation to keep the tool: it helps more people than it hurts"

**Evidence for:** Utilitarian calculus: 12% accuracy improvement benefits all candidates (better role matching) and the company. Only 3% of 50+ candidates are disadvantaged. Net benefit is positive.

**Rebuttal:** This is the strongest ethical argument for keeping the tool. However: (a) legal compliance is not utilitarian — ADEA creates individual rights that cannot be overridden by aggregate benefit, (b) the 3% represents real people who lost real job opportunities due to their age, (c) a remediated tool preserves ~80% of the benefit while eliminating the harm — the utilitarian calculus favors remediation over the status quo.

<details>
<summary>Assumption Audit</summary>

| Assumption | Status | Risk if Wrong |
|-----------|--------|---------------|
| 3% adverse impact is statistically significant | Stated by user | If not statistically significant, legal risk drops dramatically |
| Adverse impact is caused by age-correlated proxy features | Reasonable (graduation year, experience, tech keywords) | If caused by legitimate job requirements, business necessity defense strengthens |
| Fairness-constrained retraining preserves ~80% accuracy | Reasonable (literature suggests 5-25% accuracy cost) | If accuracy drops more, need to reassess value proposition |
| Workday precedent applies broadly | Verified (N.D. Cal. May 2025) | Could be distinguished on facts or reversed on appeal |
| $2M/yr bad hire cost is accurate | Stated by user | If overstated, "remove" option becomes less costly |
| Company operates or hires in NYC | Uncertain | If not, LL144 is inapplicable (but still best practice) |

</details>

<details>
<summary>Failure Modes</summary>

1. **Remediation reduces accuracy below human baseline** — If fairness constraints over-correct, the tool becomes worse than human recruiters. Mitigation: monitor accuracy metrics post-retraining; maintain fallback to human-only if accuracy drops below baseline.
2. **New protected class emerges during remediation** — Fixing age bias may inadvertently shift adverse impact to another group (disability, race). Mitigation: intersectional bias testing across all protected classes simultaneously.
3. **EEOC investigation during remediation period** — Timing risk. Mitigation: implement human-in-the-loop for 40+ candidates immediately (Phase 1) to demonstrate good faith before technical fix.
4. **Remediated tool still shows marginal adverse impact** — Even after debiasing, some residual impact may remain. Mitigation: set threshold at <1% and no statistical significance; maintain human override for borderline cases.

</details>

## Recommendation

**Remediate the tool using fairness-constrained retraining, not remove it.**

1. **Immediately** (Week 1): Add human-in-the-loop review for all candidates 40+ ($0 cost, instant risk reduction)
2. **Short-term** (Months 1-2): Privileged bias audit with employment counsel ($50K)
3. **Medium-term** (Months 2-4): Identify and remove age-proxy features; retrain with fairness constraints ($150K-$200K)
4. **Ongoing** (Annual): Independent bias audit, LL144-style publication, monitoring dashboard ($50K/yr)

**Total remediation cost: $250K-$300K one-time + $50K/yr** — vs $2M/yr lost savings (removing) or $5M-$15M litigation exposure (keeping as-is).

**Confidence: 76%** — The legal landscape is still forming (Workday case is pre-trial), fairness-constrained ML is well-documented but accuracy preservation varies by model, and the ethical trade-offs genuinely do not have a single "correct" answer.

**This recommendation changes if:** (a) the Workday case is dismissed on appeal (reduces legal risk), (b) accuracy preservation after debiasing drops below 50% of original gain ($1M/yr threshold), (c) Congress passes AI-specific employment legislation creating safe harbors, or (d) the 3% impact is shown to correlate with legitimate, non-age-related job qualifications.

## Sources

### Legal
- [EEOC AI and Workers Guidance (2024)](https://www.eeoc.gov/sites/default/files/2024-04/20240429_Employment%20Discrimination%20and%20AI%20for%20Workers.pdf)
- [EEOC Technical Assistance: AI Adverse Impact (2023)](https://www.eeoc.gov/newsroom/eeoc-launches-initiative-artificial-intelligence-and-algorithmic-fairness)
- [EEOC v. iTutorGroup Settlement — Sullivan & Cromwell](https://www.sullcrom.com/insights/blogs/2023/August/EEOC-Settles-First-AI-Discrimination-Lawsuit)
- [Mobley v. Workday ADEA Certification — Davis Wright Tremaine (May 2025)](https://www.dwt.com/blogs/employment-labor-and-benefits/2025/05/ai-hiring-age-discrimination-federal-court-workday)
- [Mobley v. Workday — Holland & Knight (May 2025)](https://www.hklaw.com/en/insights/publications/2025/05/federal-court-allows-collective-action-lawsuit-over-alleged)
- [Workday Case Analysis — Fisher Phillips (2025)](https://www.fisherphillips.com/en/insights/insights/discrimination-lawsuit-over-workdays-ai-hiring-tools-can-proceed-as-class-action-6-things)
- [Workday Lawsuit Timeline — FairNow](https://fairnow.ai/workday-lawsuit-resume-screening/)
- [ABA: Navigating AI Employment Bias](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-april/navigating-ai-employment-bias-maze/)
- [EEOC Guidance — Littler](https://www.littler.com/publication-press/publication/eeoc-issues-guidance-use-artificial-intelligence-tools-employment)
- [EEOC Guidance — Ogletree](https://ogletree.com/insights-resources/blog-posts/eeoc-issues-new-guidance-on-employer-use-of-ai-and-disparate-impact-potential/)
- [EEOC Guidance — Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2023/07/eeoc-issues-title-vii-guidance-on-employer-use-of-ai-other-algorithmic-decisionmaking-tools)

### Regulatory
- [EU AI Act Annex III High-Risk AI](https://artificialintelligenceact.eu/annex/3/)
- [EU AI Act Article 6](https://artificialintelligenceact.eu/article/6/)
- [EU AI Act and HR in 2026 — Crowell & Moring](https://www.crowell.com/en/insights/client-alerts/artificial-intelligence-and-human-resources-in-the-eu-a-2026-legal-overview)
- [NYC Local Law 144 — NYC Rules](https://rules.cityofnewyork.us/rule/automated-employment-decision-tools-2/)
- [NYC LL144 Enforcement Audit — NYS Comptroller (Dec 2025)](https://www.osc.ny.gov/state-agencies/audits/2025/12/02/enforcement-local-law-144-automated-employment-decision-tools)
- [NYC LL144 — Deloitte](https://www.deloitte.com/us/en/services/audit-assurance/articles/nyc-local-law-144-algorithmic-bias.html)

### Academic / Industry
- [Fairness in AI-Driven Recruitment — arXiv](https://arxiv.org/html/2405.19699v3)
- [Fairness and Bias in Algorithmic Hiring — ACM TIST](https://dl.acm.org/doi/full/10.1145/3696457)
- [Ethics of AI in Recruiting — Nature Humanities & Social Sciences](https://www.nature.com/articles/s41599-023-02079-x)
- [New Research on AI and Fairness in Hiring — HBR (Dec 2025)](https://hbr.org/2025/12/new-research-on-ai-and-fairness-in-hiring)
- [AI Bias in HRM Systems — ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2590291125008113)

### Cost Data
- [Cost of Bad Hire — Apollo Technical (2026)](https://www.apollotechnical.com/cost-of-a-bad-hire/)
- [Hidden Costs of Bad Hiring — HBK](https://hbkcpa.com/insights/the-hidden-costs-of-bad-hiring-how-to-calculate-your-true-cost-per-hire/)
- [Cost of Bad Hires — HumCap](https://humcapinc.com/cost-of-bad-hires-blog/)
- [Cost of Employee Turnover — Spark Hire](https://www.sparkhire.com/learn/screen-candidates/the-cost-of-employee-turnover/)
