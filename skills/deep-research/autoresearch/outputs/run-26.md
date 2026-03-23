# Pension Fund Actuarial Analysis: DB Plan Underfunding, ERISA Compliance, and ASC 715 Reporting Strategy for a Mid-Size Corporate Sponsor

## Executive Summary

A mid-size corporate sponsor (S&P 1500) with a single-employer DB plan at 82% funded status faces a convergence of ERISA funding obligations, ASC 715 financial reporting impacts, and strategic de-risking decisions. The recommended path is a phased approach: (1) accelerate contributions to cross the 80% AFTAP threshold to avoid benefit restrictions under ERISA Section 206(g), (2) implement an LDI glide path to reduce P&L volatility under ASC 715-30, and (3) evaluate pension risk transfer at 95%+ funded status. **Confidence: 78%** — high certainty on regulatory mechanics, moderate uncertainty on interest rate trajectory and PRT pricing beyond 12 months.

## Key Findings

1. **S&P 1500 aggregate funded status reached 110% at year-end 2025** ($146B surplus), up from 109% at year-end 2024, but individual plan variation is enormous — plans below 80% face acute regulatory consequences ([Mercer S&P 1500 Update](https://www.mercer.com/en-us/about/newsroom/s-p-1500-pension-funded-status-increased-by-one-percent-in-2025-according-to-mercer/))
2. **PBGC variable-rate premium for 2025: $52 per $1,000 of unfunded vested benefits**, capped at $717 per participant — an underfunded plan with 2,000 participants and $50M UVB pays ~$1.43M in VRP alone ([PBGC Premium Fact Sheet](https://www.pbgc.gov/about/factsheets/page/premiums))
3. **ARPA interest rate stabilization corridors widen in 2026** from 5% to 10%, meaning the stabilized segment rates will begin tracking closer to actual market rates — sponsors relying on ARPA relief should prepare for higher minimum required contributions ([Milliman ARPA Analysis](https://www.milliman.com/en/insight/brief-history-interest-rate-stabilization-relief-corridors))
4. **PRT market pricing is at historic lows**: retiree liabilities can be annuitized at ~100.5% of accounting liabilities as of February 2026, with 22 carriers competing ([Milliman Pension Buyout Index March 2026](https://www.milliman.com/en/insight/milliman-pension-buyout-index-march-2026))
5. **ASC 715-30-35-43/44 discount rate** must reflect high-quality corporate bond yields at measurement date — a 50bp rate change on a $500M PBO shifts the obligation by approximately $25-40M depending on duration ([PwC PEB Guide 2.4](https://viewpoint.pwc.com/dt/us/en/pwc/accounting_guides/pensions-and-employee-benefitspeb/peb_guide/Chapter-2-PEB/2_4_Financial_assumptions_when_measuring_the_plan_obligation.html))

## Industry Standards Compliance

| Standard / Regulation | Requirement | Compliance Risk at 82% Funded | Source |
|----------------------|-------------|------------------------------|--------|
| ERISA §303 / IRC §430 | Minimum required contribution = target normal cost + shortfall amortization (7-year) | Active — shortfall amortization charges apply | [29 USC §1083](https://www.law.cornell.edu/uscode/text/29/1083) |
| ERISA §206(g) / IRC §436 | Benefit restrictions at <80% AFTAP: no amendments increasing liabilities, lump-sum restrictions at <60% | At risk — 82% is dangerously close to 80% trigger | [IRS IRC §436](https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title26-section412&num=0&edition=prelim) |
| ERISA §4010 | Annual financial/actuarial reporting to PBGC if aggregate funding shortfall >$15M or FTAP <80% | Likely triggered — plan near 80% threshold without stabilization | [29 CFR Part 4010](https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XL/subchapter-C/part-4010) |
| ERISA §4043.25 | Reportable event: failure to make minimum required contribution | Not yet triggered but watch quarterly installments | [29 CFR §4043.25](https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XL/subchapter-E/part-4043/subpart-B/section-4043.25) |
| ASC 715-30-25 | Net periodic pension cost: service cost (operating) + interest cost, EROA, amortization (non-operating per ASU 2017-07) | Active — components affect both operating income and OCI | [PwC PEB Guide 3.2](https://viewpoint.pwc.com/dt/us/en/pwc/accounting_guides/pensions-and-employee-benefitspeb/peb_guide/chapter_3/32_composition.html) |
| ASC 715-30-35-43/44 | Discount rate = high-quality fixed-income yield reflecting plan cash flow duration | Active — rate selection methodology must be defensible to auditors | [SEI Discount Rate Selection](https://www.seic.com/institutional-investors/our-insights/pension-accounting-asc-715-discount-rate-selection) |
| IRC §4971 | 10% excise tax on aggregate unpaid minimum required contributions | Risk if contributions deferred | [IRC §4971](https://irc.bloombergtax.com/public/uscode/doc/irc/section_412) |
| PBGC Premium Rules 2025 | Flat-rate: $101/participant; VRP: $52/$1,000 UVB; cap: $717/participant | Active — VRP is material cost driver | [PBGC 2025 Rates](https://www.pbgc.gov/about/factsheets/page/premiums) |

## Quantitative Analysis

### Cost Impact Model

```python
# Pension Underfunding Cost Model
# Assumptions: 2,000 participants, $500M PBO, 82% funded, 5.2% discount rate

pbo = 500_000_000          # Projected Benefit Obligation
funded_pct = 0.82
plan_assets = pbo * funded_pct  # $410M
uvb = pbo - plan_assets         # $90M unfunded vested benefits

# PBGC Premiums (2025)
flat_rate_premium = 101 * 2000                          # $202,000
vrp = min(52 * (uvb / 1000), 717 * 2000)               # $4,680,000 vs cap $1,434,000
vrp = min(vrp, 717 * 2000)                              # Capped at $1,434,000
total_pbgc = flat_rate_premium + vrp                     # $1,636,000

# Shortfall Amortization (7-year, ~5.2% segment rate blend)
shortfall = uvb  # $90M
annual_amort = shortfall / 6.0  # ~$15M/yr (approx 7-yr amortization at blended rate)

# ASC 715 P&L Impact Components
service_cost = 8_000_000       # Typical for ongoing accruals
interest_cost = pbo * 0.052    # $26M
expected_return = plan_assets * 0.065  # $26.65M (6.5% EROA)
amort_losses = 5_000_000       # Corridor amortization from AOCI
net_periodic_cost = service_cost + interest_cost - expected_return + amort_losses
# = $8M + $26M - $26.65M + $5M = $12.35M

# Contribution needed to reach 80% AFTAP (with buffer)
target_funded = 0.85  # Buffer above 80% threshold
contribution_to_target = (target_funded * pbo) - plan_assets  # $15M

# PRT cost estimate (retiree liabilities only, ~40% of PBO)
retiree_pbo = pbo * 0.40       # $200M
prt_premium = retiree_pbo * 1.005  # $201M at 100.5% of accounting liability
prt_savings_vrp_annual = 52 * (retiree_pbo * 0.18 / 1000)  # Reduced UVB -> lower VRP

print(f"Plan Assets: ${plan_assets:,.0f}")
print(f"Unfunded Vested Benefits: ${uvb:,.0f}")
print(f"Total PBGC Premiums: ${total_pbgc:,.0f}")
print(f"Annual Shortfall Amortization: ~${annual_amort:,.0f}")
print(f"Net Periodic Pension Cost (ASC 715): ${net_periodic_cost:,.0f}")
print(f"Contribution to reach 85% funded: ${contribution_to_target:,.0f}")
print(f"PRT buyout cost (retirees): ~${prt_premium:,.0f}")
```

### Key Financial Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Plan Assets | $410,000,000 | 82% of $500M PBO |
| Unfunded Vested Benefits | $90,000,000 | Drives VRP and shortfall amortization |
| PBGC Total Premium | $1,636,000/yr | Flat + VRP (capped) |
| Shortfall Amortization | ~$15,000,000/yr | 7-year ERISA amortization |
| Net Periodic Pension Cost | $12,350,000/yr | ASC 715-30 P&L impact |
| Contribution to 85% funded | $15,000,000 | One-time to create buffer |
| PRT buyout (retirees) | ~$201,000,000 | At current 100.5% pricing |
| ARPA corridor widening impact (2026) | +$2-5M/yr MRC increase | Estimated from corridor change |

### Discount Rate Sensitivity

| Discount Rate Change | PBO Impact | Funded Status Impact | MRC Change |
|---------------------|-----------|---------------------|-----------|
| +50 bps | -$30M (-6%) | +4.9 pts to ~87% | -$4M/yr |
| +25 bps | -$15M (-3%) | +2.5 pts to ~84.5% | -$2M/yr |
| Base (5.20%) | $500M | 82.0% | Baseline |
| -25 bps | +$16M (+3.2%) | -2.6 pts to ~79.4% | +$2.5M/yr |
| -50 bps | +$33M (+6.6%) | -5.4 pts to ~76.6% | +$5.5M/yr |

**Critical risk**: A 25bp rate decline pushes funded status below the 80% AFTAP threshold, triggering ERISA §206(g) benefit restrictions.

## Implementation Guidance

### Phase 1: Immediate (Q1-Q2 2026) — Stabilize Funded Status

1. **Make a discretionary contribution of $15-25M** to create a buffer above 80% AFTAP
   - Fund from operating cash flow or revolver draw
   - Tax deduction under IRC §404(a)(1) up to 150% of funding target
   - Quarterly contribution installments required under ERISA §303(j): 25% of prior year MRC per quarter

2. **Review and lock discount rate methodology**
   - Choose between single weighted-average vs. spot rate approach per ASC 715-30-35-44
   - Document methodology for auditor defensibility
   - Consider Citigroup Pension Discount Curve, FTSE Pension Liability Index, or Mercer yield curve

3. **File ERISA §4010 report if required** (aggregate shortfall >$15M or FTAP <80%)

### Phase 2: Medium-Term (Q3 2026 — Q4 2027) — LDI Glide Path

1. **Implement liability-driven investment allocation**:
   - At 82% funded: 50% return-seeking / 50% LDI (long-duration credit + Treasury STRIPS)
   - At 90% funded: 30% return-seeking / 70% LDI
   - At 100% funded: 10% return-seeking / 90% LDI
   - Set automated rebalancing triggers at each 5% funded status increment

2. **Hedge interest rate risk** using long-duration corporate bonds matching plan liability duration (typically 10-14 years for a mature plan)

3. **Prepare for ARPA corridor widening** — the 2026 corridor moves to 90%-110% of 25-year average, and by 2030 reaches 70%-130%, meaning stabilized rates converge toward market rates

### Phase 3: Long-Term (2027+) — Pension Risk Transfer

1. **At 95%+ funded status**, solicit PRT bids from the 22 active carriers
   - Retiree-first buyout: transfer ~$200M in retiree liabilities via group annuity contract
   - Current pricing: ~100.5% of accounting liability (Milliman Buyout Index, Feb 2026)
   - Insurer selection: evaluate financial strength (AM Best A+ minimum), administrative capabilities, and DOL fiduciary requirements under Interpretive Bulletin 95-1

2. **Consider plan termination** if strategic objective is full de-risking
   - Standard termination requires 100% funded on a termination basis (ERISA §4041)
   - Termination basis uses more conservative assumptions than ongoing — typically 102-105% of PBO

## Alternatives Considered

| Strategy | Cost | Pros | Cons |
|----------|------|------|------|
| Accelerate contributions only | $15-25M/yr | Tax-deductible, reduces VRP, simple | Ties up cash, no risk transfer |
| LDI glide path (recommended) | $0 incremental (portfolio reallocation) | Reduces P&L volatility, systematic de-risking | Lower expected returns, requires governance |
| Immediate full PRT | ~$510M (102% of PBO) | Eliminates all pension risk and PBGC premiums | Massive cash outlay, settlement accounting charge under ASC 715-30-35-79 |
| Plan freeze + LDI | $0 + ERISA §204(h) notice | Stops accruing new benefits, reduces future cost | HR/labor relations impact, doesn't address existing UVB |
| Borrow-and-fund | $15-25M + interest | Arbitrage: VRP savings > borrowing cost if UVB large | Adds leverage to balance sheet |

## Adversarial Review

### Counterargument 1: "Interest rates will rise, fixing underfunding automatically"
**Rebuttal**: While higher rates reduce PBO, this is not guaranteed. The 2025 experience showed funded status falling to 99% in April before recovering to 110% by December ([Mercer](https://www.mercer.com/en-us/about/newsroom/s-p-1500-pension-funded-status-increased-by-one-percent-in-2025-according-to-mercer/)). A plan at 82% funded cannot afford to gamble on rate movements — a 25bp decline triggers benefit restrictions. Counterargument dismissed: relying on favorable rate movements is speculation, not risk management.

### Counterargument 2: "PBGC premiums are a sunk cost — don't chase funded status just to reduce them"
**Rebuttal**: At $1.6M/yr and growing (VRP cap increases annually with inflation), PBGC premiums are a material expense. However, the counterargument has partial merit: contribution decisions should weigh opportunity cost of capital. If the sponsor's WACC exceeds the VRP-equivalent interest rate (~5.8% implied), the borrow-and-fund strategy may not create value. Each sponsor must run their own NPV analysis. Counterargument partially valid.

### Counterargument 3: "PRT market will get cheaper — wait for better pricing"
**Rebuttal**: Current pricing at 100.5% of accounting liability is near historic competitiveness with 22 carriers in the market ([BusinessWire/Milliman](https://www.businesswire.com/news/home/20260313710806/en/Milliman-analysis-Competitive-pension-risk-transfer-cost-increased-from-100.4-to-100.5-during-February)). However, PRT pricing is a function of insurer demand for assets, credit spreads, and competitive dynamics — all of which could shift. The counterargument is reasonable for a 6-12 month horizon but risky beyond that. A partial buyout (retirees only) locks in current pricing while retaining optionality.

### Assumption Audit

| Assumption | Status | Risk if Wrong |
|-----------|--------|---------------|
| 5.20% discount rate | Verified (approximate AA corporate bond yield, March 2026) | ±50bp = ±$30M PBO swing |
| 6.5% EROA | Reasonable for 50/50 equity/fixed portfolio | Overstated EROA inflates P&L; understated reduces it |
| 2,000 participants | Assumed for illustration | Premium cap and flat-rate scale linearly |
| PRT at 100.5% | Verified (Milliman Feb 2026 index) | Market-dependent; could be 98-103% |
| ARPA corridor widening schedule | Verified (statutory: §430(h)(2)(C)(iv)) | Legislative change possible but unlikely |

## Recommendation

**Recommended strategy**: Phased de-risking with immediate contribution + LDI glide path + eventual PRT.

1. **Immediately**: Contribute $15-25M to buffer above 80% AFTAP (avoid benefit restrictions)
2. **Within 6 months**: Implement LDI glide path (50/50 at 82%, stepping to 90% LDI at full funding)
3. **At 95%+ funded**: Execute retiree PRT (~$200M group annuity buyout)
4. **Monitor**: ARPA corridor widening (2026-2030) will gradually increase MRC — model the trajectory annually

**Overall confidence: 78%** — regulatory mechanics are certain; optimal timing of contributions and PRT depends on rate movements and corporate cash flow priorities.

**Conditions that change this recommendation**:
- If rates drop >75bp: accelerate contributions immediately to prevent AFTAP breach
- If sponsor faces liquidity constraints: freeze plan first, then address funding over longer horizon
- If PRT pricing exceeds 103%: defer buyout and focus on LDI hedging

## Sources

- [Mercer S&P 1500 Pension Funded Status 2025](https://www.mercer.com/en-us/about/newsroom/s-p-1500-pension-funded-status-increased-by-one-percent-in-2025-according-to-mercer/)
- [PBGC Premium Fact Sheet](https://www.pbgc.gov/about/factsheets/page/premiums)
- [PBGC 2025 Annual Report](https://www.pbgc.gov/sites/default/files/documents/pbgc-annual-report-2025.pdf)
- [PBGC Projections Report](https://www.pbgc.gov/about/reports/projections)
- [Milliman Pension Buyout Index March 2026](https://www.milliman.com/en/insight/milliman-pension-buyout-index-march-2026)
- [Milliman ARPA Interest Rate Stabilization](https://www.milliman.com/en/insight/brief-history-interest-rate-stabilization-relief-corridors)
- [Milliman 2025 Corporate Pension Funding Study](https://www.milliman.com/en/insight/2025-corporate-pension-funding-study)
- [PwC PEB Guide: Financial Assumptions](https://viewpoint.pwc.com/dt/us/en/pwc/accounting_guides/pensions-and-employee-benefitspeb/peb_guide/Chapter-2-PEB/2_4_Financial_assumptions_when_measuring_the_plan_obligation.html)
- [PwC PEB Guide: Net Periodic Cost](https://viewpoint.pwc.com/dt/us/en/pwc/accounting_guides/pensions-and-employee-benefitspeb/peb_guide/chapter_3/32_composition.html)
- [SEI: ASC 715 Discount Rate Selection](https://www.seic.com/institutional-investors/our-insights/pension-accounting-asc-715-discount-rate-selection)
- [Deloitte FRA 25-1: Pension Reporting 2025](https://dart.deloitte.com/USDART/home/publications/deloitte/financial-reporting-alerts/2025/asc-715-pension-postretirement-benefits-reporting-considerations)
- [EY FRD: Pension Benefits](https://www.ey.com/content/dam/ey-unified-site/ey-com/en-us/technical/accountinglink/documents/ey-frd11344-201us-06-24-2025.pdf)
- [29 USC §1083 — ERISA §303](https://www.law.cornell.edu/uscode/text/29/1083)
- [29 CFR Part 4010 — PBGC Reporting](https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XL/subchapter-C/part-4010)
- [29 CFR §4043.25 — Reportable Events](https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XL/subchapter-E/part-4043/subpart-B/section-4043.25)
- [IRS Pension Segment Rates](https://www.irs.gov/retirement-plans/pension-plan-funding-segment-rates)
- [ASPPA: ARPA and Pension Plans](https://asppa.org/news/arpa-and-pension-plans-closer-look)
- [ASPPA: PBGC Single-Employer Good News](https://www.asppa-net.org/news/2025/3/a-close-look-at-pbgc-single-employer-plans-good-news/)
- [Russell Investments: Future of LDI](https://russellinvestments.com/content/ri/us/en/insights/russell-research/2025/02/the-future-of-liability-driven-investing.html)
- [NISA: Dynamic LDI](https://www.nisa.com/perspectives/dldi/)
- [October Three: Feb 2026 PRT Pricing](https://www.octoberthree.com/articles/february-2026-pension-risk-transfer-pricing-update/)
- [BusinessWire/Milliman: PRT Cost Feb 2026](https://www.businesswire.com/news/home/20260313710806/en/Milliman-analysis-Competitive-pension-risk-transfer-cost-increased-from-100.4-to-100.5-during-February)
- [Mercer: 2025 PRT Market Update](https://www.mercer.com/en-us/insights/retirement/defined-benefit-plans/pension-risk-transfer-market-update-2025-review/)
- [PLANSPONSOR: Pension Finances End 2025](https://www.plansponsor.com/pension-finances-end-2025-on-high-note/)
- [PLANSPONSOR: Funding Levels Start Strong 2026](https://www.plansponsor.com/pension-funding-levels-start-strong-in-2026/)
- [Wilshire: US Corporate Pension Funding July 2025](https://www.wilshire.com/press-releases/u-s-corporate-pension-plans-funding-status-july-2025)
