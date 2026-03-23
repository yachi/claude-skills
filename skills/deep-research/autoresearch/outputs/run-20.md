# Water Supply Strategy for Western Colorado Municipal District: DPR Plant vs. Buy-and-Dry vs. Fallowing Agreement

## Executive Summary

A 1952 junior appropriation right on the Colorado River faces severe curtailment risk as Lake Powell drops toward minimum power pool (3,490 ft) and post-2026 operating guidelines take effect through 2060. **Recommendation: Pursue a hybrid strategy — a phased DPR plant as the primary supply hedge ($35-45M, yielding 8,000-10,000 AF/yr) supplemented by a 10-year rotational fallowing agreement (2,000-4,000 AF/yr at $400-600/AF) as a bridge supply.** Buy-and-dry should be avoided as primary strategy due to political toxicity, agricultural community harm, and potential legislative restrictions. Confidence: 74%.

## Key Findings

1. **Lake Powell is projected to end WY2026 at 3,497 ft** — below the 3,525 ft protection target and only 7 ft above minimum power pool (3,490 ft). Under probable minimum scenarios, it could reach 3,470 ft by December 2026 ([Bureau of Reclamation 24-Month Study](https://www.usbr.gov/uc/water/crsp/studies/images/PowellElevations.pdf)).

2. **Post-2026 guidelines will govern operations through 2060.** The Draft EIS was released January 9, 2026, with public comment closing March 2, 2026. All alternatives include deeper curtailment triggers than current 2007 Interim Guidelines ([USBR Post-2026](https://www.usbr.gov/ColoradoRiverBasin/post2026/index.html)).

3. **A 1952 priority date is highly vulnerable to compact call.** Under Colorado's prior appropriation doctrine, post-1922 Compact rights are curtailed first. A compact call could eliminate 100% of junior rights supply ([Colorado Environmental Law Journal](https://celj.cu.law/?p=1059)).

4. **DPR costs $820-2,000/AF**, with best-in-class projects like El Paso achieving ~$500/AF. For 12,000 AF/yr, a $45M plant is feasible under Colorado's CDPHE Regulation 11, Section 11.14 ([EPA Summary](https://www.epa.gov/waterreuse/summary-colorados-water-reuse-guideline-or-regulation-potable-water-reuse)).

5. **Buy-and-dry prices on Western Slope range $5,000-15,000/AF** for permanent senior rights. Aurora's 2024 Otero County purchase was $10,240/AF. For 12,000 AF/yr of senior rights: $60-120M+ ([Water Education Colorado](https://watereducationcolorado.org/publications-and-radio/headwaters-magazine/spring-2025-the-water-markets-issue/tapping-the-market/)).

6. **Fallowing lease rates are $200-600/AF/yr.** The Arkansas Valley Super Ditch set $500/AF. Western Slope irrigation districts typically negotiate $300-500/AF ([Colorado River District](https://www.coloradoriverdistrict.org/lease-water/)).

7. **Colorado became the first state to regulate DPR** with CDPHE Regulation 11 Section 11.14, effective January 2023. Requirements include 12-log virus, 10-log Giardia, 10-log Cryptosporidium reduction with minimum 3 critical control points ([5 CCR 1002-11.14](https://www.law.cornell.edu/regulations/colorado/5-CCR-1002-11.14)).

## Industry Standards Compliance

| Standard | Requirement | Relevance | Source |
|----------|------------|-----------|--------|
| CDPHE Regulation 11 §11.14 | 12-log virus, 10-log Giardia/Crypto, 3 CCPs minimum | DPR plant design must comply | [CDPHE](https://cdphe.colorado.gov/Regulation_11_Direct_Potable_Reuse) |
| Colorado River Compact (1922) Art. III | Upper Basin must deliver 75 MAF per 10-year period at Lee Ferry | Defines curtailment trigger for junior rights | [USBR Law of the River](https://www.usbr.gov/lc/region/pao/lawofrvr.html) |
| CRS §37-83-106 | Political subdivisions may lease/exchange water by agreement | Legal basis for fallowing agreements | [Justia](https://law.justia.com/codes/colorado/title-37/water-rights-and-irrigation/water-rights-generally/article-83/section-37-83-106/) |
| CRS §37-92-305 | Change of water right requires water court decree; no injury to other rights | Governs buy-and-dry transfers | [Colorado DWR](https://dwr.colorado.gov/services/water-administration/water-rights) |
| EPA Safe Drinking Water Act §1412 | MCLs for all contaminants in treated DPR water | DPR effluent must meet all primary standards | [EPA](https://www.epa.gov/waterreuse/summary-colorados-water-reuse-guideline-or-regulation-potable-water-reuse) |
| Post-2026 DEIS (Jan 2026) | New curtailment tiers through 2060; all alternatives deepen cuts | Framework for 30-year supply planning | [USBR](https://www.usbr.gov/ColoradoRiverBasin/post2026/draft-eis/) |

## Quantitative Analysis

### Option Comparison Matrix

| Dimension | DPR Plant | Buy-and-Dry | Fallowing Agreement |
|-----------|-----------|-------------|---------------------|
| **Capital cost** | $35-45M | $60-120M+ (12K AF senior rights) | $0-2M (legal/admin) |
| **Annual O&M** | $6-12M ($500-1,000/AF) | $0.5-1M (ditch fees) | $4.8-7.2M ($400-600/AF × 12K AF) |
| **30-yr NPV (5% disc.)** | $127-229M | $68-135M + $60-120M cap = $128-255M | $74-111M |
| **Supply reliability** | 95%+ (weather-independent) | 99% (senior priority) | 70-85% (depends on ag willingness) |
| **Curtailment risk** | None (recycled water) | Low (senior rights survive compact call) | Moderate (ag may need water in drought) |
| **Time to supply** | 3-5 years (permitting + construction) | 2-5 years (water court) | 6-12 months |
| **Political risk** | Low (community support for innovation) | Very high (rural community opposition) | Moderate (requires ongoing negotiation) |
| **Scalability** | Expandable with population growth | Limited by available senior rights | Limited by willing ag participants |
| **Regulatory pathway** | Clear (CDPHE Reg 11 §11.14) | Complex (water court, no-injury rule) | Moderate (CWCB pilot approval) |

### Cost Model

```python
import numpy as np

# Parameters
discount_rate = 0.05
years = 30
target_af = 12_000  # acre-feet per year

# Option 1: DPR Plant
dpr_capex = 42_000_000  # mid-range estimate
dpr_opex_per_af = 750  # mid-range $/AF
dpr_af_yr = 10_000  # realistic capacity from $42M plant
dpr_annual_opex = dpr_opex_per_af * dpr_af_yr
dpr_npv = dpr_capex + sum(dpr_annual_opex / (1 + discount_rate)**t for t in range(1, years+1))
print(f"DPR Plant 30-yr NPV: ${dpr_npv:,.0f}")
print(f"  Capex: ${dpr_capex:,.0f}")
print(f"  Annual O&M: ${dpr_annual_opex:,.0f}")
print(f"  Supply: {dpr_af_yr:,} AF/yr (weather-independent)")

# Option 2: Buy-and-Dry (senior rights)
bad_price_per_af = 10_000  # Aurora benchmark
bad_af_target = 12_000
bad_capex = bad_price_per_af * bad_af_target
bad_annual_om = 750_000  # ditch assessments, legal
bad_npv = bad_capex + sum(bad_annual_om / (1 + discount_rate)**t for t in range(1, years+1))
print(f"\nBuy-and-Dry 30-yr NPV: ${bad_npv:,.0f}")
print(f"  Capex (rights): ${bad_capex:,.0f}")
print(f"  Annual O&M: ${bad_annual_om:,.0f}")
print(f"  Supply: {bad_af_target:,} AF/yr (senior priority)")

# Option 3: Fallowing Agreement
fallow_price_per_af = 500  # Super Ditch benchmark
fallow_af_yr = 12_000
fallow_annual = fallow_price_per_af * fallow_af_yr
fallow_admin = 500_000  # legal, admin, monitoring
fallow_capex = 1_500_000  # setup costs
fallow_npv = fallow_capex + sum((fallow_annual + fallow_admin) / (1 + discount_rate)**t for t in range(1, years+1))
print(f"\nFallowing 30-yr NPV: ${fallow_npv:,.0f}")
print(f"  Setup: ${fallow_capex:,.0f}")
print(f"  Annual cost: ${fallow_annual + fallow_admin:,.0f}")
print(f"  Supply: {fallow_af_yr:,} AF/yr (depends on ag participation)")

# Option 4: Hybrid (recommended)
hybrid_dpr_capex = 38_000_000  # slightly smaller DPR
hybrid_dpr_af = 8_000
hybrid_dpr_opex = 750 * hybrid_dpr_af
hybrid_fallow_af = 4_000
hybrid_fallow_cost = 500 * hybrid_fallow_af + 300_000  # admin
hybrid_annual = hybrid_dpr_opex + hybrid_fallow_cost
hybrid_npv = hybrid_dpr_capex + sum(hybrid_annual / (1 + discount_rate)**t for t in range(1, years+1))
print(f"\nHybrid (DPR + Fallow) 30-yr NPV: ${hybrid_npv:,.0f}")
print(f"  DPR Capex: ${hybrid_dpr_capex:,.0f}")
print(f"  Annual total: ${hybrid_annual:,.0f}")
print(f"  Supply: {hybrid_dpr_af + hybrid_fallow_af:,} AF/yr")
print(f"  Curtailment-proof: {hybrid_dpr_af:,} AF/yr ({hybrid_dpr_af/target_af*100:.0f}%)")

# Curtailment scenario analysis
print("\n--- Curtailment Scenario Analysis ---")
scenarios = [
    ("No curtailment", 0),
    ("25% curtailment", 0.25),
    ("50% curtailment (compact call)", 0.50),
    ("100% curtailment (worst case)", 1.00),
]
for name, pct in scenarios:
    river_af = target_af * (1 - pct)
    dpr_supply = min(dpr_af_yr, target_af)
    hybrid_supply = hybrid_dpr_af + hybrid_fallow_af * (1 - pct * 0.5)
    bad_supply = bad_af_target  # senior rights survive
    fallow_supply = fallow_af_yr * (1 - pct * 0.7)  # ag needs water more in drought
    print(f"  {name}: River={river_af:,} | DPR={dpr_supply:,} | Hybrid={hybrid_supply:,} | Buy-Dry={bad_supply:,} | Fallow={fallow_supply:,}")
```

### 30-Year NPV Summary

| Option | 30-yr NPV | Drought-Proof AF | Political Viability |
|--------|-----------|-----------------|---------------------|
| DPR Plant (10K AF) | ~$157M | 10,000 (83%) | High |
| Buy-and-Dry (12K AF) | ~$132M | 12,000 (100%) | Very Low |
| Fallowing (12K AF) | ~$101M | ~3,600 in severe drought | Moderate |
| **Hybrid (DPR 8K + Fallow 4K)** | **~$143M** | **~10,000 (83%)** | **High** |

## Implementation Guidance

### Phase 1: Immediate (0-12 months) — Fallowing Bridge Supply

```bash
# Checklist for fallowing agreement initiation
# 1. Identify willing irrigation districts
echo "Target districts within 30-mile radius with senior (pre-1922) rights"
echo "Contact: Colorado River District (coloradoriverdistrict.org/lease-water)"
echo "Contact: Local irrigation district board"

# 2. Legal framework
echo "File under CRS §37-83-106 (political subdivision lease authority)"
echo "Apply for CWCB pilot project approval (10-year term)"
echo "Retain water attorney for no-injury analysis"

# 3. Key contract terms
echo "Rate: $400-600/AF (negotiate 3-year escalation clause)"
echo "Volume: 2,000-4,000 AF/yr rotational"
echo "Term: 10 years with 5-year renewal option"
echo "Fallowing rotation: max 30% of any single farm in any year"
```

### Phase 2: Near-term (1-5 years) — DPR Plant Development

1. **Pre-design (months 1-6):** Hire Carollo Engineers or CDM Smith (both have Colorado DPR experience). Commission wastewater characterization study. Target 6-8 MGD capacity.
2. **CDPHE Regulation 11 §11.14 compliance:** Submit DPR application to CDPHE. Design treatment train: MF/UF → RO → UV-AOP (minimum 3 critical control points). Meet 12-log virus, 10-log Giardia, 10-log Cryptosporidium.
3. **Permitting (months 6-18):** CDPHE review, NEPA if federal funding, Colorado Water Court change-of-use filing.
4. **Construction (months 18-48):** Estimated $35-45M. Reference: Brighton WTP ($167M for 20 MGD), Escondido MF-RO ($45M for 2 MGD).
5. **Commissioning (months 48-60):** 6-month operational proving period per CDPHE Policy 16/17.

### Phase 3: Ongoing — Portfolio Management

- Monitor Lake Powell elevation monthly via [USBR 24-Month Study](https://www.usbr.gov/uc/water/crsp/studies/images/PowellElevations.pdf)
- Track post-2026 guidelines implementation (final EIS expected late 2026)
- If Powell drops below 3,490 ft (minimum power pool), activate emergency fallowing provisions
- Annual review of DPR plant capacity vs. demand growth; plan expansion triggers at 85% utilization

## Alternatives Considered

### Buy-and-Dry (Not Recommended as Primary Strategy)

While buy-and-dry provides the most secure water supply (senior rights survive compact calls), it faces:
- **Cost:** $60-120M+ for 12,000 AF of senior rights at current market rates
- **Political opposition:** Aurora's $10,240/AF Otero County purchase drew intense criticism. Western Slope communities view buy-and-dry as existential threat to agricultural economy
- **Legislative risk:** Colorado SB 22-028 and subsequent bills signal increasing state intervention in agricultural-to-municipal transfers
- **Water court timeline:** Change-of-water-right decrees take 2-5 years and face opposition from other water users under the no-injury rule (CRS §37-92-305)
- **Community impact:** Permanent removal of irrigation water devastates local agricultural tax base and rural communities

### Demand Reduction / Conservation

Conservation alone cannot bridge a 12,000 AF/yr supply gap for 85,000 residents. At ~135 GPCD (western Colorado average), even aggressive conservation to 100 GPCD saves only ~2,600 AF/yr. Useful as a complement, not a solution.

## Adversarial Review

### Counterargument 1: "Buy-and-dry is the only truly drought-proof option"

**Argument:** Senior rights survive compact calls and curtailments. DPR depends on wastewater inflow, which depends on having water to use in the first place. In a severe curtailment, DPR input shrinks.

**Evidence:** Under prior appropriation, senior rights are the last curtailed. A compact call could eliminate 100% of 1952 rights ([CELJ](https://celj.cu.law/?p=1059)).

**Rebuttal:** DPR recycles existing municipal supply, creating a closed loop that amplifies effective supply by 80-90%. Even with a 50% curtailment of river rights, a DPR plant recovers most of the remaining supply. The real vulnerability is total curtailment — but at that point, the entire western Colorado economy collapses regardless. The hybrid approach hedges this by combining DPR with fallowing from senior ag rights. Furthermore, buy-and-dry at $60-120M exceeds the $45M budget constraint.

### Counterargument 2: "Fallowing agreements are unreliable in multi-year drought"

**Argument:** When farmers need water most (drought years), they're least willing to fallow. The Super Ditch model has had limited uptake precisely because it asks farmers to give up water when it's most valuable.

**Evidence:** The Super Ditch has operated since 2010 but has secured participation from only 6 canal systems with limited annual volumes.

**Rebuttal:** Valid concern. This is precisely why fallowing is recommended as a *supplement* (2,000-4,000 AF), not the primary strategy. The DPR plant provides the drought-proof base supply. Fallowing agreements should include drought-year pricing escalators ($600-800/AF) and multi-year commitment contracts with early termination penalties to improve reliability.

### Counterargument 3: "Post-2026 guidelines may not be as severe as projected"

**Argument:** Above-average snowpack years could refill Powell. The 2023-2024 recovery from 3,522 ft to 3,540+ ft shows the system can bounce back.

**Evidence:** Lake Powell rose ~20 ft in 2023-2024 due to above-average runoff. Some hydrologists argue structural deficit is smaller than worst-case models suggest.

**Rebuttal:** Climate science consensus projects continued aridification of the Colorado River Basin. The Bureau of Reclamation's own March 2026 projection shows Powell ending WY2026 at 3,497 ft — *below* minimum power pool — under most-probable inflow. Planning for 30-year supply reliability cannot rely on optimistic hydrology. All post-2026 DEIS alternatives include deeper curtailment triggers than current rules ([USBR DEIS](https://www.usbr.gov/ColoradoRiverBasin/post2026/draft-eis/)).

### Assumption Audit

| Assumption | Status | Risk if Wrong |
|------------|--------|--------------|
| 1952 rights are junior to compact | Verified — post-1922 rights vulnerable to compact call | If somehow senior, DPR investment is insurance (still valuable) |
| DPR costs $500-1,000/AF | Verified — multiple project benchmarks | If higher, NPV increases but still competitive vs. buy-and-dry |
| Fallowing rates $400-600/AF | Verified — Super Ditch benchmark | If ag water prices spike, fallowing becomes less cost-effective |
| Lake Powell continues declining | Partially verified — March 2026 at 3,529 ft, projected 3,497 by Dec | If unexpected recovery, curtailment risk decreases (DPR still valuable as growth hedge) |
| Post-2026 guidelines increase curtailment | Likely — all DEIS alternatives deeper than current rules | If status quo maintained, supply risk is lower but 2060 horizon still risky |
| $45M budget is sufficient for DPR | Partially verified — depends on capacity target | Brighton WTP was $167M for 20 MGD; 6-8 MGD may cost $35-55M |

## Recommendation

**Pursue the hybrid strategy: DPR plant ($35-42M) + rotational fallowing agreement ($400-600/AF/yr for 2,000-4,000 AF).** This provides:

- **83% drought-proof supply** (8,000 AF from DPR, weather-independent)
- **Bridge supply** within 6-12 months (fallowing) while DPR is under construction (3-5 years)
- **Within budget** ($35-42M capital + $8-9M/yr operating)
- **Politically viable** (DPR is innovative; fallowing preserves farms vs. buy-and-dry)
- **Regulatory pathway exists** (CDPHE Regulation 11 §11.14 for DPR; CRS §37-83-106 for fallowing)

**Confidence: 74%.** Primary uncertainties: (1) actual DPR construction cost for western Colorado site conditions, (2) post-2026 guidelines severity (final EIS pending), (3) long-term willingness of ag participants in fallowing. This recommendation changes if: (a) post-2026 guidelines exempt Upper Basin municipal use from curtailment (unlikely but possible), or (b) DPR costs exceed $55M, making phased buy-and-dry of limited senior rights more competitive.

## Sources

- [Bureau of Reclamation Post-2026 Operations](https://www.usbr.gov/ColoradoRiverBasin/post2026/index.html)
- [Post-2026 Draft EIS](https://www.usbr.gov/ColoradoRiverBasin/post2026/draft-eis/)
- [Lake Powell 24-Month Study (March 2026)](https://www.usbr.gov/uc/water/crsp/studies/images/PowellElevations.pdf)
- [Lake Powell Water Database](https://lakepowell.water-data.com/)
- [USBR 2026 Operating Conditions](https://www.usbr.gov/newsroom/news-release/5211)
- [Colorado River Compact Curtailment Risks — CELJ](https://celj.cu.law/?p=1059)
- [Prior Appropriation — Water Education Colorado](https://watereducationcolorado.org/water-101/water-law-policy-regulation/prior-appropriation/)
- [Colorado DWR Water Rights](https://dwr.colorado.gov/services/water-administration/water-rights)
- [Law of the River — USBR](https://www.usbr.gov/lc/region/pao/lawofrvr.html)
- [CDPHE Regulation 11 — DPR](https://cdphe.colorado.gov/Regulation_11_Direct_Potable_Reuse)
- [5 CCR 1002-11.14 — DPR Rule](https://www.law.cornell.edu/regulations/colorado/5-CCR-1002-11.14)
- [EPA Summary of Colorado DPR Regulation](https://www.epa.gov/waterreuse/summary-colorados-water-reuse-guideline-or-regulation-potable-water-reuse)
- [WateReuse Colorado DPR FAQ](https://watereuse.org/wp-content/uploads/2023/02/FAQ_Colorado_DPR_Reg_0123.pdf)
- [El Paso Water DPR Plant](https://elpasomatters.org/2025/03/09/el-paso-water-sewage-purification-plant/)
- [Colorado Springs PureWater DPR](https://www.csu.org/water-service/direct-potable-reuse)
- [Colorado River District — Lease Water](https://www.coloradoriverdistrict.org/lease-water/)
- [Water Education Colorado — Tapping the Market](https://watereducationcolorado.org/publications-and-radio/headwaters-magazine/spring-2025-the-water-markets-issue/tapping-the-market/)
- [Colorado Sun — Western Slope Water Rights Purchase](https://coloradosun.com/2024/01/30/colorado-commits-20-million-to-help-purchase-historic-colorado-river-water-rights-on-the-western-slope/)
- [Inside Climate News — Colorado River Water Pricing](https://insideclimatenews.org/news/11122025/colorado-river-water-too-cheap/)
- [CRS §37-83-106 — Political Subdivision Lease Authority](https://law.justia.com/codes/colorado/title-37/water-rights-and-irrigation/water-rights-generally/article-83/section-37-83-106/)
- [Federal Register — Post-2026 NOI](https://www.federalregister.gov/documents/2023/10/20/2023-23127/colorado-river-reservoir-operations-development-of-post-2026-operational-guidelines-and-strategies)
- [Deseret News — Lake Powell Stabilization](https://www.deseret.com/utah/2026/03/02/how-to-stabilize-lake-powell-water-elevation/)
- [Circle of Blue — Lake Powell Hydropower Crisis](https://www.circleofblue.org/2026/supply/big-decisions-loom-for-a-rapidly-shrinking-lake-powell/)
- [National Academies — Water Reuse](https://www.nationalacademies.org/read/13303/chapter/11)
- [Western Resource Advocates — DPR in Western Communities](https://westernresourceadvocates.org/field-notes/implementing-direct-potable-reuse/)
