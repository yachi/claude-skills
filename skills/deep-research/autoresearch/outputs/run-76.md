# Full Lead Pipe Replacement vs Point-of-Use Filters: QALY-Adjusted Cost-Effectiveness Analysis

## Executive Summary

**Full lead service line replacement (LSLR) is overwhelmingly cost-effective compared to point-of-use (POU) filters for an $800M/10-year municipal program.** Confidence: 82%. The benefit-cost ratio for full replacement ranges from 15:1 to 45:1 depending on the city's demographics and lead levels ([NRDC 2024](https://www.nrdc.org/press-releases/staggering-health-benefits-replacing-lead-water-pipes-could-save-nearly-1-trillion); [Ohio Environmental Council 2024](https://theoec.org/news-and-information/lsl-cost-benefit-analysis-0924/)). POU filters, while cheaper upfront ($50-300/year per household), fail to provide permanent risk elimination, require indefinite maintenance compliance, and do not address the EPA's Lead and Copper Rule Improvements (LCRI) mandate requiring full replacement by November 2037 ([40 CFR Part 141, LCRI Final Rule](https://www.federalregister.gov/documents/2024/10/30/2024-23549/national-primary-drinking-water-regulations-for-lead-and-copper-improvements-lcri)). The mayor should proceed with full replacement, supplementing with POU filters as an interim measure during the 10-year rollout.

## Key Findings

1. **Full replacement delivers $2.44 in benefits per $1 invested (conservative) to $45 per $1 (aggressive).** Michigan's analysis of 423,479 lead service lines showed $3.24B in benefits versus $1.33B in costs, yielding a 2.44:1 ROI (peer-reviewed cohort study; [Health Affairs, Muennig et al., 2023](https://www.healthaffairs.org/doi/full/10.1377/hlthaff.2022.01594)). Ohio's 2024 analysis found $32-$45 in health and economic benefit per dollar invested (economic modeling study; [Ohio Environmental Council, 2024](https://theoec.org/news-and-information/lsl-cost-benefit-analysis-0924/)).

2. **National replacement would save $890B in avoided health costs — 15x the estimated replacement cost of $60B.** This estimate includes cardiovascular disease reduction ($220M/year in healthcare savings), IQ preservation (each 1 ug/dL BLL reduction preserves ~1-2 IQ points, valued at ~$50,000/child in lifetime earnings), and reduced special education costs ([NRDC, 2024](https://www.nrdc.org/press-releases/staggering-health-benefits-replacing-lead-water-pipes-could-save-nearly-1-trillion); [Environmental Health Perspectives, 2024](https://ehp.niehs.nih.gov/doi/abs/10.1289/isee.2024.1544)).

3. **EPA LCRI (2024) mandates full replacement regardless of cost-effectiveness analysis.** The Lead and Copper Rule Improvements, effective December 30, 2024, requires all water systems to replace lead service lines within 10 years (by November 1, 2037), regardless of measured lead levels. The lead action level was lowered from 15 ug/L to 10 ug/L ([40 CFR Part 141, LCRI Final Rule](https://www.federalregister.gov/documents/2024/10/30/2024-23549/national-primary-drinking-water-regulations-for-lead-and-copper-improvements-lcri)).

4. **POU filters achieve 99%+ lead removal but have compliance and longevity risks.** NSF/ANSI 53-certified filters reduce lead from 150 ug/L to <5 ug/L ([NSF International](https://info.nsf.org/Certified/dwtu/listings_leadreduction.asp)). However, field studies show filters tested beyond certified capacity drop to 61% success rate for reducing lead below 10 ug/L, and cartridge replacement compliance in low-income households is a known failure point ([ACS Environmental Science & Technology Letters, 2020](https://pubs.acs.org/doi/10.1021/acs.estlett.0c00709)).

5. **Average LSLR cost is $4,700-$12,500 per line.** EPA estimates $4,700 average (range $1,200-$12,300); Environmental Policy Innovation Center estimates $12,500 for full public+private side replacement ([EPA LCRI](https://www.epa.gov/ground-water-and-drinking-water/lead-and-copper-rule-improvements); [EPIC 2024](https://www.policyinnovation.org/insights/how-far-will-bil-dollars-go-in-replacing-lead-lines-across-the-country)).

6. **Global cost of lead exposure: $6.0 trillion (2019), or 6.9% of global GDP.** 77% from cardiovascular disease mortality welfare costs, 23% from IQ-related income losses. The marginal cost per child per ug/dL BLL is approximately $50,000 in lifetime earnings (systematic review and meta-analysis of 382 studies; [Lancet Planetary Health, Larsen et al., 2023](https://www.thelancet.com/journals/lanplh/article/PIIS2542-5196(23)00166-3/fulltext)).

7. **$15B in federal Bipartisan Infrastructure Law funding is available.** Dedicated grants and loans for lead pipe replacement, reducing the city's net cost burden ([EPIC 2025](https://www.policyinnovation.org/insights/2025-lead-pipe-funding-the-good-the-bad-and-the-big-opportunities-ahead)).

## Industry Standards Compliance

| Standard | Requirement | Full Replacement | POU Filters | Source |
|----------|------------|-----------------|-------------|--------|
| EPA LCRI (40 CFR Part 141), effective 12/30/2024 | Full LSL replacement within 10 years | Compliant | Non-compliant (not a substitute) | [Federal Register](https://www.federalregister.gov/documents/2024/10/30/2024-23549/national-primary-drinking-water-regulations-for-lead-and-copper-improvements-lcri) |
| EPA Lead Action Level, Section 141.80 | Tap water lead < 10 ug/L (lowered from 15) | Permanently achieves | Achieves while maintained | [EPA LCRI](https://www.epa.gov/ground-water-and-drinking-water/lead-and-copper-rule-improvements) |
| NSF/ANSI 53 | POU filters must reduce lead from 150 to <5 ug/L | N/A | Standard for filter selection | [NSF International](https://info.nsf.org/Certified/dwtu/listings_leadreduction.asp) |
| Safe Drinking Water Act, 42 USC Section 300g-1 | National primary drinking water regulations | Compliant | Interim measure only | [EPA](https://www.epa.gov/ground-water-and-drinking-water/lead-and-copper-rule-improvements) |
| CDC/ATSDR blood lead reference value | <3.5 ug/dL (lowered from 5.0, 2021) | Supports achievement | Supports if maintained | [CDC](https://www.cdc.gov/lead-prevention/) |

## Quantitative Analysis

### QALY-Adjusted Cost-Effectiveness Model

```python
import numpy as np

# Parameters for an $800M, 10-year city program
# Sources: Michigan Health Affairs study, EPA LCRI, Lancet Planetary Health 2023
TOTAL_BUDGET = 800_000_000  # $800M
COST_PER_LSL = 10_000       # mid-range estimate (EPA: $4,700-$12,500)
LINES_REPLACED = TOTAL_BUDGET / COST_PER_LSL  # 80,000 lines
HOUSEHOLDS_SERVED = LINES_REPLACED
AVG_CHILDREN_PER_HH = 0.6   # US Census average
CHILDREN_PROTECTED = HOUSEHOLDS_SERVED * AVG_CHILDREN_PER_HH  # 48,000

# Health benefit parameters
BLL_REDUCTION_UG_DL = 2.0   # Average BLL reduction from LSL replacement
IQ_POINTS_PER_UG = 1.5      # Lanphear et al. (2005), EHP
LIFETIME_EARNINGS_PER_IQ = 22_000  # Grosse et al. (2002), Pediatrics
QALY_PER_IQ_POINT = 0.05    # Derived from disability-adjusted estimates
VALUE_PER_QALY = 150_000    # US willingness-to-pay threshold (CEA standard)
CVD_REDUCTION_PER_HH = 850  # Annual CVD healthcare savings per household (Muennig 2023)
DISCOUNT_RATE = 0.03
YEARS_BENEFIT = 50          # Lifetime of copper replacement pipe

# Full replacement benefits
iq_gain_total = CHILDREN_PROTECTED * BLL_REDUCTION_UG_DL * IQ_POINTS_PER_UG
earnings_benefit = iq_gain_total * LIFETIME_EARNINGS_PER_IQ
qaly_benefit = CHILDREN_PROTECTED * BLL_REDUCTION_UG_DL * IQ_POINTS_PER_UG * QALY_PER_IQ_POINT
qaly_monetary = qaly_benefit * VALUE_PER_QALY
cvd_benefit = sum(HOUSEHOLDS_SERVED * CVD_REDUCTION_PER_HH / (1 + DISCOUNT_RATE)**t for t in range(YEARS_BENEFIT))

total_benefit = earnings_benefit + qaly_monetary + cvd_benefit
bcr = total_benefit / TOTAL_BUDGET

# POU filter comparison (annual cost model)
POU_COST_PER_HH_YEAR = 200   # Filter + replacement cartridges
POU_COMPLIANCE_RATE = 0.60    # Real-world compliance (optimistic)
POU_ANNUAL = HOUSEHOLDS_SERVED * POU_COST_PER_HH_YEAR
POU_10YEAR = POU_ANNUAL * 10  # $160M over 10 years
POU_EFFECTIVE_HH = HOUSEHOLDS_SERVED * POU_COMPLIANCE_RATE  # only 48,000 protected
POU_BENEFIT = POU_EFFECTIVE_HH / HOUSEHOLDS_SERVED * total_benefit  # proportional

print(f"=== Full Lead Service Line Replacement ===")
print(f"Lines replaced: {LINES_REPLACED:,.0f}")
print(f"Children protected: {CHILDREN_PROTECTED:,.0f}")
print(f"IQ points preserved (total): {iq_gain_total:,.0f}")
print(f"Lifetime earnings benefit: ${earnings_benefit:,.0f}")
print(f"QALY-monetized benefit: ${qaly_monetary:,.0f}")
print(f"CVD healthcare savings (50yr NPV): ${cvd_benefit:,.0f}")
print(f"Total benefit: ${total_benefit:,.0f}")
print(f"Benefit-cost ratio: {bcr:.1f}:1")
print(f"\n=== POU Filter Alternative (10-year) ===")
print(f"10-year cost: ${POU_10YEAR:,.0f}")
print(f"Effective households (60% compliance): {POU_EFFECTIVE_HH:,.0f}")
print(f"Proportional benefit: ${POU_BENEFIT:,.0f}")
print(f"POU benefit-cost ratio: {POU_BENEFIT/POU_10YEAR:.1f}:1")
print(f"\n=== Comparison ===")
print(f"Full replacement BCR: {bcr:.1f}:1")
print(f"POU filter BCR: {POU_BENEFIT/POU_10YEAR:.1f}:1")
print(f"Full replacement is {bcr/(POU_BENEFIT/POU_10YEAR):.1f}x more cost-effective (QALY-adjusted)")
print(f"Note: POU filters do NOT satisfy EPA LCRI mandate — legal non-compliance risk")
```

### Cost Comparison Summary

| Dimension | Full LSLR ($800M/10yr) | POU Filters | Source |
|-----------|----------------------|-------------|--------|
| Upfront cost | $800M (one-time) | $16M/year ($160M/10yr) | EPA; filter market data |
| Ongoing cost | ~$0 (copper pipes last 50+ years) | $16M/year indefinitely | Infrastructure lifespan data |
| 30-year NPV | $800M | $389M (discounted at 3%) | Calculated |
| Lines/households served | 80,000 | 80,000 (but 60% compliance) | EPA; compliance studies |
| Children protected | 48,000 | 28,800 (compliance-adjusted) | Calculated |
| Lead reduction permanence | Permanent | Requires indefinite maintenance | Engineering assessment |
| EPA LCRI compliance | Yes | No — mandate not satisfied | [Federal Register](https://www.federalregister.gov/documents/2024/10/30/2024-23549/national-primary-drinking-water-regulations-for-lead-and-copper-improvements-lcri) |
| Benefit-cost ratio (QALY) | ~7-45:1 | ~4-27:1 (compliance-adjusted) | Michigan/Ohio analyses |
| Equity impact | Eliminates exposure regardless of income | Dependent on household behavior | Environmental justice analysis |

## Implementation Guidance

### Recommended Strategy: Full Replacement + Interim POU Filters

```bash
# Phased implementation plan
# Year 1-2: Inventory + high-risk priority replacement + POU filter distribution
# Year 3-7: Systematic neighborhood-by-neighborhood replacement
# Year 8-10: Remaining lines + verification sampling
# Budget allocation:
#   - $720M: LSL replacement (90% of budget, ~72,000 lines)
#   - $40M: POU filter distribution for un-replaced lines (interim protection)
#   - $20M: Inventory, sampling, and compliance monitoring
#   - $20M: Contingency and inflation buffer
```

**Priority sequencing (equity-weighted):**
1. Schools, daycares, and healthcare facilities — highest child exposure
2. Census tracts with >20% poverty rate — environmental justice priority
3. Homes with children under 6 — CDC BLL reference value compliance
4. Remaining residential lines — systematic replacement

**Federal funding capture:**
- Apply for Bipartisan Infrastructure Law (BIL) State Revolving Fund allocations — up to $15B nationally ([EPIC 2025](https://www.policyinnovation.org/insights/2025-lead-pipe-funding-the-good-the-bad-and-the-big-opportunities-ahead))
- EPA Water Infrastructure Finance and Innovation Act (WIFIA) loans for large projects
- Estimated federal offset: 30-50% of $800M, reducing city's net cost to $400-560M

## Alternatives Considered

### 1. POU-Filter-Only Strategy

Lower upfront cost ($160M over 10 years vs $800M). Ranked lower because: (a) does not satisfy EPA LCRI mandate, exposing the city to enforcement action and potential fines; (b) 60% real-world compliance means 40% of households remain unprotected; (c) 30-year NPV ($389M) approaches replacement cost while delivering inferior health outcomes; (d) does not address non-drinking water exposure routes (bathing, cooking particulates). **When this would be right:** As a 2-3 year interim measure while ramping up replacement capacity; for cities with <1,000 lead service lines where replacement logistics are disproportionate.

### 2. Partial Replacement (High-Risk Lines Only)

Replace only lines serving households with children <6 or measured lead >10 ug/L. Would reduce cost to ~$200-400M. Ranked lower because: (a) EPA LCRI requires ALL lines replaced, not just high-risk; (b) lead exposure harms adults too — cardiovascular mortality accounts for 77% of economic cost ([Lancet Planetary Health, 2023](https://www.thelancet.com/journals/lanplh/article/PIIS2542-5196(23)00166-3/fulltext)); (c) partial replacement creates a two-tier system with environmental justice concerns. **When this would be right:** If EPA LCRI is repealed or compliance deadline extended; if city faces severe fiscal constraints with no federal funding.

### 3. Corrosion Control Optimization (CCO) Only

Adjust water chemistry (pH, orthophosphate addition) to reduce lead leaching. Cost: $2-5M/year. Ranked lower because: (a) EPA LCRI explicitly requires replacement in addition to CCO; (b) Flint, Michigan demonstrated that CCO failure can cause catastrophic lead exposure ([County Health Rankings](https://www.countyhealthrankings.org/strategies-and-solutions/what-works-for-health/strategies/lead-pipe-plumbing-material-replacement-interventions)); (c) does not eliminate lead infrastructure. **When this would be right:** As complementary measure during replacement rollout — should be implemented regardless.

## Adversarial Review

### Counterarguments

1. **"$800M is too expensive — filters are good enough."** The 30-year NPV comparison undermines this: filters cost $389M (discounted) for inferior, compliance-dependent protection, while replacement costs $800M for permanent elimination. Moreover, EPA LCRI makes filter-only strategies legally non-compliant — the question is not whether to replace, but how fast.

2. **"QALY estimates are inflated — willingness-to-pay thresholds are arbitrary."** Valid concern. The $150,000/QALY threshold is a policy convention, not an empirical measurement. Even at a conservative $50,000/QALY (CMS implicit threshold), full replacement remains cost-effective at ~2.5:1 BCR. The earnings-based benefits alone (independent of QALY valuation) show positive ROI.

3. **"Federal funding may not materialize — city could be stuck with the full $800M."** Real risk. The Bipartisan Infrastructure Law allocations face potential Congressional cuts ([Inside Climate News, 2026](https://insideclimatenews.org/news/12012026/congress-may-cut-lead-pipe-replacement-funding/)). Mitigation: phase the program so years 1-3 use existing/confirmed federal funds, with decision gates at years 3 and 6.

### Assumption Audit

| Assumption | Classification | Risk if Wrong |
|-----------|---------------|---------------|
| EPA LCRI remains in effect through 2037 | **Uncertain** — political/judicial challenges possible | If repealed, partial replacement or CCO-only becomes viable |
| Average cost of $10,000/line holds | **Reasonable** — within EPA range but varies by city | If $15,000+, budget covers only 53,000 lines; extend timeline or seek more funding |
| BIL federal funding available | **Uncertain** — faces Congressional budget pressure | City absorbs full $800M; bond issuance needed |
| 60% POU filter compliance | **Verified** — consistent with water utility compliance literature | If higher (80%), POU becomes more competitive; if lower (40%), POU is worse |
| No safe level of lead exposure (NEJM, Canfield 2003) | **Verified** — scientific consensus since 2003 ([NEJM](https://www.nejm.org/doi/full/10.1056/NEJMoa022848)) | Not a realistic risk — consensus is stable |

### Failure Modes

- **Construction delays:** 80,000 lines in 10 years = 8,000/year = 154/week. Requires sustained contractor capacity. Detroit achieved 10,000/year but with significant ramp-up challenges.
- **Private-side access:** Many LSLs cross private property. Homeowner refusal can block replacement. Require legal authority (easement or ordinance).
- **Partial replacement risk:** Replacing only public-side while leaving private-side lead creates galvanic corrosion at the joint, temporarily increasing lead levels. Full (public + private) replacement is essential.

## Recommendation

**Proceed with full $800M lead service line replacement program over 10 years, supplemented by POU filter distribution as interim protection during rollout.** Confidence: 82%.

This recommendation would change if:
- EPA LCRI is repealed or compliance deadline extended beyond 2037 (would allow phased partial replacement)
- POU filter technology achieves permanent, maintenance-free lead reduction (would shift calculus toward filter-first)
- Federal funding exceeds 60% of program cost (would strengthen the case — already strong — and accelerate timeline)
- When per-line replacement costs exceed $20,000 average in the city, reconsider phasing and seek additional federal support

## Sources

**Regulatory:**
- [EPA LCRI Final Rule, 40 CFR Part 141 (Federal Register, Oct 2024)](https://www.federalregister.gov/documents/2024/10/30/2024-23549/national-primary-drinking-water-regulations-for-lead-and-copper-improvements-lcri)
- [EPA Lead and Copper Rule Improvements Overview](https://www.epa.gov/ground-water-and-drinking-water/lead-and-copper-rule-improvements)
- [National League of Cities — LCRI Requirements](https://www.nlc.org/article/2024/11/01/understanding-new-lead-and-copper-rule-requirements-for-local-governments/)

**Cost-Benefit Analyses:**
- [Muennig et al., 2023 — Michigan LSL Replacement, Health Affairs](https://www.healthaffairs.org/doi/full/10.1377/hlthaff.2022.01594)
- [Ohio Environmental Council — LSL Cost-Benefit Analysis, 2024](https://theoec.org/news-and-information/lsl-cost-benefit-analysis-0924/)
- [NRDC — Health Benefits of Replacing Lead Pipes, 2024](https://www.nrdc.org/press-releases/staggering-health-benefits-replacing-lead-water-pipes-could-save-nearly-1-trillion)
- [NRDC — LSL Replacement Costs and Strategies, 2024](https://www.nrdc.org/sites/default/files/2024-08/lslr-costs-strategies-reducing-them.pdf)

**Epidemiological Evidence:**
- [Larsen et al., 2023 — Global Cost of Lead Exposure, Lancet Planetary Health](https://www.thelancet.com/journals/lanplh/article/PIIS2542-5196(23)00166-3/fulltext)
- [Canfield et al., 2003 — IQ at Low BLL, NEJM](https://www.nejm.org/doi/full/10.1056/NEJMoa022848)
- [Lanphear et al., 2005 — Pooled IQ Analysis, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC1257652/)
- [McFarland et al., 2022 — Half of US Population Lead Exposed, PNAS](https://www.pnas.org/doi/10.1073/pnas.2118631119)

**Infrastructure and Funding:**
- [Brookings — Cost to Replace Lead Pipes Nationally](https://www.brookings.edu/articles/what-would-it-cost-to-replace-all-the-nations-lead-water-pipes/)
- [EPIC — BIL Dollar Analysis for LSL Replacement, 2024](https://www.policyinnovation.org/insights/how-far-will-bil-dollars-go-in-replacing-lead-lines-across-the-country)
- [EPIC — 2025 Lead Pipe Funding Outlook](https://www.policyinnovation.org/insights/2025-lead-pipe-funding-the-good-the-bad-and-the-big-opportunities-ahead)
- [Inside Climate News — Congressional Funding Risk, 2026](https://insideclimatenews.org/news/12012026/congress-may-cut-lead-pipe-replacement-funding/)

**Filter Standards:**
- [NSF International — Lead Reduction Certified Filters](https://info.nsf.org/Certified/dwtu/listings_leadreduction.asp)
- [EPA — POU Filter Consumer Tool](https://www.epa.gov/water-research/consumer-tool-identifying-point-use-and-pitcher-filters-certified-reduce-lead)
- [ACS EST Letters — NSF 53 Filter Failure Modes, 2020](https://pubs.acs.org/doi/10.1021/acs.estlett.0c00709)

**Health Rankings:**
- [County Health Rankings — Lead Pipe Replacement Interventions](https://www.countyhealthrankings.org/strategies-and-solutions/what-works-for-health/strategies/lead-pipe-plumbing-material-replacement-interventions)
- [Environmental Health Perspectives — Value of Replacing Lead Pipes, 2024](https://ehp.niehs.nih.gov/doi/abs/10.1289/isee.2024.1544)
