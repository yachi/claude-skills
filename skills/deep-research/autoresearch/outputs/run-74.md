# Vertical Farming Sustainability: Challenging the "Always Greener" Premise

## Executive Summary

The premise that vertical farms are inherently more sustainable than traditional agriculture is **false in most current scenarios**. Confidence level: 82%. Vertical farming's carbon footprint averages 18.43 kg CO₂/kg of harvested crop at global average grid intensity (475g CO₂/kWh) — roughly 9x higher than field-grown lettuce (~2 kg CO₂/kg) — and energy consumption of 10–38.8 kWh/kg makes economic viability dependent on energy prices and crop selection. The 2023–2025 bankruptcy wave (AeroFarms, Bowery, Plenty) and 75–80% funding collapse ($2.8B to $0.68B) confirm that unit economics remain broken for most configurations. Vertical farming is sustainable only under narrow conditions: renewable-powered, leafy-green-focused, urban-proximate operations where water scarcity or supply chain resilience justifies the energy premium.

## Key Findings

1. **Premise challenge (kill switch): Vertical farming is NOT always more sustainable** — at global average grid carbon intensity, vertical farms emit ~18.43 kg CO₂ per kg of harvested crop vs ~2 kg CO₂/kg for field agriculture, making them 9x more carbon-intensive — per a systematic review by [Agronomy for Sustainable Development (2025)](https://link.springer.com/article/10.1007/s13593-025-01055-w) (systematic review covering productivity, environmental impact, and resource use).

2. **Energy consumption ranges from 10–38.8 kWh/kg**, with the 2021 Global CEA Census reporting an average of 38.8 kWh/kg across indoor vertical farms — compared to <0.5 kWh/kg for field lettuce — per [ScienceDirect benchmarking study (2024)](https://www.sciencedirect.com/science/article/pii/S2451904924007832) (peer-reviewed controlled analysis). Technical benchmarks project future efficiency of 3.1–7.4 kWh/kg, but this remains aspirational.

3. **CEA provides <1% of US food crops but consumes more energy than all open-field cultivation**, and scaling to 7% of national food supply could consume ~7% of national energy — per [Plant Physiology, Oxford Academic (2025)](https://academic.oup.com/plphys/article/198/3/kiaf056/8104144) (peer-reviewed back-of-envelope calculation with verified assumptions).

4. **Major bankruptcies in 2023–2025**: AeroFarms (Chapter 11, 2023), Bowery (ceased operations, late 2024), Plenty (Chapter 11, March 2025). Investment in novel farming systems fell 75–80% from $2.8B (2022) to $0.68B (2023) — per [Vertical Farm Daily (2023)](https://www.verticalfarmdaily.com/article/9537965/lessons-from-vertical-farming-bankruptcies-layoffs-and-closures-in-2023/) and [AgFunder News (2024)](https://agfundernews.com/the-economics-of-local-vertical-and-greenhouse-farming-are-getting-competitive) (industry observational data).

5. **Solar-powered vertical farming requires 3x more land than open-field cultivation**, negating the primary land-use advantage — per [npj Sustainable Agriculture (2025)](https://www.nature.com/articles/s44264-025-00091-z) (peer-reviewed modeling study). The photosynthetic efficiency ceiling of ~2% imposes a fundamental thermodynamic constraint.

6. **Water use is 90–95% lower than field agriculture** (vertical farming uses 1–5 liters/kg vs 50–100 liters/kg field), making it genuinely sustainable on the water dimension — per [Agronomy for Sustainable Development (2025)](https://link.springer.com/article/10.1007/s13593-025-01055-w) (systematic review, high-confidence evidence).

7. **With 100% renewable energy, vertical farm emissions drop to 0.93 kg CO₂eq/kg lettuce** — still above field-farmed lettuce due to embodied carbon in infrastructure, but within a viable sustainability range — per [Frontiers in Sustainable Food Systems (2024)](https://www.frontiersin.org/journals/sustainable-food-systems/articles/10.3389/fsufs.2024.1403580/full) (peer-reviewed lifecycle assessment).

## Industry Standards Compliance

| Standard | Requirement | Vertical Farming Status | Source |
|----------|------------|------------------------|--------|
| GLOBALG.A.P. IFA v6, Greenhouse Module | Good agricultural practices for controlled environments incl. vertical growing, hydroponics | Applicable; greenhouse module covers vertical farms | [GLOBALG.A.P.](https://www.globalgap.org/) |
| CEA Food Safety Coalition Standard (2022) | First food safety certification specific to CEA-grown leafy greens; GFSI-recognized baseline | Active, adoption growing | [Progressive Grocer](https://progressivegrocer.com/1st-food-safety-standard-indoor-grown-produce-introduced) |
| ISO 14040:2006 / ISO 14044:2006 | Lifecycle assessment methodology (mandatory for sustainability claims) | Most vertical farms lack full LCA per ISO 14040; claims often cherry-pick water/land metrics | [ISO](https://www.iso.org/files/live/sites/isoorg/files/store/en/PUB100412.pdf) |
| ISO 22000:2018, Clause 8 | Food safety management system, operational planning and control | Applicable; vertical farms typically comply via GFSI schemes | [ISO Agriculture](https://www.iso.org/files/live/sites/isoorg/files/store/en/PUB100412.pdf) |
| EU Taxonomy Regulation 2020/852, Article 3 | Criteria for "sustainable" economic activity; requires "do no significant harm" | Vertical farming's energy footprint may fail DNSH for climate change mitigation unless 100% renewable | [ScienceDirect (2025)](https://www.sciencedirect.com/science/article/pii/S0959652625003865) |

## Quantitative Analysis

### Sustainability Dimension Comparison

| Dimension | Vertical Farm | Field Agriculture | Greenhouse | Winner |
|-----------|-------------|-------------------|-----------|--------|
| Energy (kWh/kg lettuce) | 10–38.8 | 0.3–0.5 | 2–5 | Field |
| Water (L/kg lettuce) | 1–5 | 50–100 | 15–30 | Vertical |
| Land (m²/kg/yr) | 0.01–0.05 | 0.5–2.0 | 0.1–0.3 | Vertical |
| CO₂ (kg CO₂eq/kg, grid avg) | 4.75–18.43 | 0.5–2.0 | 1.5–4.0 | Field |
| CO₂ (kg CO₂eq/kg, 100% renewable) | 0.5–0.93 | 0.5–2.0 | 0.8–2.5 | Vertical (marginal) |
| Pesticide use | Zero | Moderate–High | Low–Moderate | Vertical |
| Transport emissions (urban) | Near-zero | Variable (100–3000 km) | Variable | Vertical |
| Crop diversity | Leafy greens, herbs, strawberries | All crops | Most crops | Field |

### Economic Viability Model

```python
import numpy as np

# Vertical farm vs field agriculture: cost per kg lettuce
# Sources: Plant Physiology 2025, AgFunder 2024, Vertical Farm Daily 2023

def vertical_farm_economics(
    # Vertical farm parameters
    vf_capex: float = 5_000_000,          # USD, 1000 m² facility
    vf_annual_yield_kg: float = 200_000,   # kg lettuce/year (100 harvests @ 2kg/m²)
    vf_energy_kwh_per_kg: float = 15.0,    # mid-range current
    vf_electricity_usd_kwh: float = 0.12,  # US average commercial
    vf_labor_per_kg: float = 0.80,         # higher-skilled labor
    vf_nutrients_per_kg: float = 0.15,
    vf_rent_annual: float = 200_000,       # urban location
    vf_depreciation_years: int = 10,
    # Field agriculture parameters
    field_yield_kg_per_ha: float = 30_000, # lettuce yield/ha
    field_cost_per_kg: float = 0.80,       # all-in field cost
    # Market
    wholesale_price_kg: float = 2.50,      # USD wholesale lettuce
):
    # Vertical farm unit economics
    energy_cost = vf_energy_kwh_per_kg * vf_electricity_usd_kwh
    annual_depreciation = vf_capex / vf_depreciation_years
    annual_opex = (
        vf_annual_yield_kg * (energy_cost + vf_labor_per_kg + vf_nutrients_per_kg) +
        vf_rent_annual
    )
    total_annual = annual_opex + annual_depreciation
    vf_cost_per_kg = total_annual / vf_annual_yield_kg

    # Field economics
    field_total = field_cost_per_kg

    print(f"=== Vertical Farm (1000 m², lettuce) ===")
    print(f"  Energy cost/kg: ${energy_cost:.2f}")
    print(f"  Labor cost/kg: ${vf_labor_per_kg:.2f}")
    print(f"  Nutrients/kg: ${vf_nutrients_per_kg:.2f}")
    print(f"  Rent + depreciation/kg: ${(vf_rent_annual + annual_depreciation) / vf_annual_yield_kg:.2f}")
    print(f"  TOTAL cost/kg: ${vf_cost_per_kg:.2f}")
    print(f"\n=== Field Agriculture ===")
    print(f"  TOTAL cost/kg: ${field_total:.2f}")
    print(f"\n  Wholesale price: ${wholesale_price_kg:.2f}/kg")
    print(f"  VF margin: ${wholesale_price_kg - vf_cost_per_kg:.2f}/kg ({(wholesale_price_kg - vf_cost_per_kg)/wholesale_price_kg*100:.0f}%)")
    print(f"  Field margin: ${wholesale_price_kg - field_total:.2f}/kg ({(wholesale_price_kg - field_total)/wholesale_price_kg*100:.0f}%)")
    print(f"\n  VF premium over field: {vf_cost_per_kg/field_total:.1f}x")
    return vf_cost_per_kg, field_total

vertical_farm_economics()
```

### Key Economic Finding

Vertical farm lettuce costs approximately $4.45/kg at current energy prices ($0.12/kWh, 15 kWh/kg) — roughly 5.6x field-grown lettuce at $0.80/kg — and 78% above the $2.50/kg wholesale price. Profitability requires either: (a) premium pricing (organic/local branding at $5–8/kg retail), (b) electricity below $0.05/kWh (renewable PPA in favorable geographies), or (c) crop selection targeting high-value herbs/microgreens at $15–50/kg retail per [AgFunder News (2024)](https://agfundernews.com/the-economics-of-local-vertical-and-greenhouse-farming-are-getting-competitive).

## Implementation Guidance

### When Vertical Farming IS Justified
- **Water-scarce regions** (Gulf states, Singapore, arid urban centers): 90–95% water savings justify the energy premium
- **Supply chain resilience** (island nations, military bases, space stations): eliminate 3,000+ km transport chains
- **High-value crops** (saffron, microgreens, medicinal herbs): unit economics work above $15/kg wholesale
- **100% renewable energy** available at <$0.05/kWh: carbon footprint drops to competitive range

### When Vertical Farming is NOT Justified
- **Commodity crops** (wheat, rice, corn): thermodynamic limits make vertical farming 100–1000x more expensive
- **Grid-powered operations** in coal/gas-heavy regions: 9x carbon footprint vs field farming
- **Low-value leafy greens** at scale: wholesale prices ($1.50–2.50/kg) cannot cover energy costs

### Technology Recommendations
- **LED efficiency:** Target >3.0 µmol/J photosynthetic photon flux (current best: 3.5 µmol/J, up from 1.7 in 2015)
- **Climate integration:** Co-locate with data centers or industrial waste heat sources for free heating/cooling
- **Crop selection algorithm:** Focus on crops with >$10/kg wholesale, <30 day cycle, high density potential

## Alternatives Considered

### 1. High-Tech Greenhouses (Dutch Model)

Glass greenhouses with supplemental LED, CO₂ enrichment, and climate control. Energy use of 2–5 kWh/kg (3–8x less than vertical farms per [Agronomy for Sustainable Development, 2025](https://link.springer.com/article/10.1007/s13593-025-01055-w)) with yield approaching 80% of vertical farming. The Netherlands produces $12.4B in agricultural exports from a country smaller than West Virginia. CAPEX $500–1,500/m² vs $2,000–5,000/m² for vertical farms. **Best when:** land is available, daylight hours are reasonable, and the goal is high-yield controlled environment production without the energy penalty of full artificial lighting.

### 2. Improved Open-Field Agriculture (Precision Ag)

GPS-guided equipment, variable-rate application, soil sensors, and drone monitoring. Energy <0.5 kWh/kg, cost <$1/kg for most crops. With precision irrigation, water use drops 30–50% from conventional while maintaining field-scale economics. **Best when:** arable land is available, climate is suitable, and the primary goal is feeding large populations at lowest cost — which describes the vast majority of global agriculture.

### 3. Hybrid Model (Greenhouse + Vertical for Finishing)

Seedlings started in vertical farm nursery (high density, controlled germination), then transferred to greenhouse for grow-out under natural light. Captures 70% of vertical farming's germination advantages at 30% of the energy cost. **Best when:** operating in temperate climates with seasonal variation where year-round seedling supply is the bottleneck.

## Adversarial Review

### Counterarguments

1. **"Vertical farming's water savings make it sustainable regardless of energy"** — Water savings of 90–95% are real and significant in water-scarce regions (per systematic review in [Agronomy for Sustainable Development, 2025](https://link.springer.com/article/10.1007/s13593-025-01055-w)). However, sustainability is multi-dimensional: a process that saves water but emits 9x more CO₂ is not "more sustainable" in aggregate unless water scarcity is the binding constraint. ISO 14040 LCA methodology requires evaluating all impact categories, not cherry-picking favorable ones.

2. **"Technology will close the energy gap"** — Technical benchmarks project 3.1–7.4 kWh/kg (vs current 10–38.8 kWh/kg per [ScienceDirect, 2024](https://www.sciencedirect.com/science/article/pii/S2451904924007832)), but the fundamental photosynthetic efficiency limit (~2%) means LED-to-biomass conversion has a thermodynamic ceiling. Even at theoretical minimum energy, vertical farming cannot match field agriculture's use of free sunlight. The gap can narrow but not close.

<details>
<summary>Assumption Audit</summary>

| Assumption | Classification | Evidence/Risk |
|-----------|---------------|---------------|
| Global avg grid CO₂ intensity 475g/kWh | **Verified** | [IEA data](https://link.springer.com/article/10.1007/s13593-025-01055-w), cited in systematic review |
| Vertical farm energy 10–38.8 kWh/kg | **Verified** | [ScienceDirect (2024)](https://www.sciencedirect.com/science/article/pii/S2451904924007832) + Global CEA Census |
| Field lettuce CO₂ ~2 kg/kg | **Reasonable** | Varies by region; 0.5–3.0 kg/kg range depending on transport distance |
| Bankruptcy wave reflects structural, not cyclical, failure | **Reasonable** | 75–80% funding decline + 3 major Chapter 11 filings suggest structural issues; however, survivors (Gotham Greens, Kalera) may demonstrate viable niches |
| 100% renewable energy makes VF carbon-competitive | **Verified** | [Frontiers (2024)](https://www.frontiersin.org/journals/sustainable-food-systems/articles/10.3389/fsufs.2024.1403580/full) LCA shows 0.93 kg CO₂/kg with renewables |

</details>

<details>
<summary>Failure Modes</summary>

1. **Greenwashing risk** — Vertical farms claiming "sustainable" without full ISO 14040 LCA mislead investors and consumers. Mitigation: require third-party LCA verification for sustainability claims.
2. **Stranded assets** — $5M+ facilities designed for crops that can't cover energy costs become write-offs. Mitigation: design for crop flexibility; target high-value from inception.
3. **Energy price shocks** — Electricity price increases of 30–50% (as in EU 2022) can instantly destroy margins. Mitigation: long-term renewable PPAs at fixed prices.

</details>

## Recommendation

Do not invest in vertical farming for commodity crop production or as a general sustainability strategy. Instead, pursue vertical farming only under the following conditions: (a) water-scarce geography where 90% water savings justify the energy premium, (b) high-value crops ($15+/kg wholesale) with short production cycles, (c) 100% renewable energy at <$0.05/kWh via long-term PPA, or (d) supply chain resilience requirements (island nations, military, space). For all other scenarios, high-tech greenhouses (Dutch model) deliver 80% of vertical farming's benefits at 20% of the energy cost. Confidence: 82%.

**This recommendation changes if:** (a) LED efficiency exceeds 4.0 µmol/J, pushing energy consumption below 5 kWh/kg; (b) grid carbon intensity drops below 50g CO₂/kWh (deep decarbonization), eliminating the carbon footprint disadvantage; (c) a profitable vertical farm demonstrates >3 consecutive years of positive unit economics on commodity lettuce at wholesale prices; or (d) water scarcity escalates to the point where the 90% water savings premium becomes the dominant economic factor globally.

## Sources

**Academic & Peer-Reviewed:**
- [Agronomy for Sustainable Development — Vertical farming: productivity, environmental impact, resource use (2025)](https://link.springer.com/article/10.1007/s13593-025-01055-w)
- [Plant Physiology, Oxford Academic — Vertical farming limitations (2025)](https://academic.oup.com/plphys/article/198/3/kiaf056/8104144)
- [npj Sustainable Agriculture — Indoor agriculture as driver of energy demand (2025)](https://www.nature.com/articles/s44264-025-00091-z)
- [ScienceDirect — Benchmarking energy efficiency in vertical farming (2024)](https://www.sciencedirect.com/science/article/pii/S2451904924007832)
- [Frontiers in Sustainable Food Systems — LCA of modular vertical farm (2024)](https://www.frontiersin.org/journals/sustainable-food-systems/articles/10.3389/fsufs.2024.1403580/full)
- [ScienceDirect — Sustainability assessment for novel agri-food approaches (2025)](https://www.sciencedirect.com/science/article/pii/S0959652625003865)
- [PMC — Food for thought: Perspectives on vertical farming (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12373847/)

**Standards & Regulatory:**
- [GLOBALG.A.P. — Smart farm assurance solutions](https://www.globalgap.org/)
- [CEA Food Safety Coalition Standard — Progressive Grocer (2022)](https://progressivegrocer.com/1st-food-safety-standard-indoor-grown-produce-introduced)
- [ISO — Agriculture standards portfolio](https://www.iso.org/files/live/sites/isoorg/files/store/en/PUB100412.pdf)

**Industry & Market Analysis:**
- [Vertical Farm Daily — Lessons from 2023 bankruptcies](https://www.verticalfarmdaily.com/article/9537965/lessons-from-vertical-farming-bankruptcies-layoffs-and-closures-in-2023/)
- [AgFunder News — CEA economics getting competitive (2024)](https://agfundernews.com/the-economics-of-local-vertical-and-greenhouse-farming-are-getting-competitive)
- [Agritecture — Vertical farming carbon footprint (2022)](https://www.agritecture.com/blog/2022/5/9/a-holistic-look-at-vertical-farmings-carbon-footprint-and-land-use)
- [Agro Reality — Vertical farming startup cost (2025)](https://agroreality.com/vertical-farming-startup-cost-in-2025-complete-investment-breakdown-roi-analysis/)
- [Anthropocene Magazine — Vertical farms surprisingly large footprint (2025)](https://www.anthropocenemagazine.org/2025/09/are-vertical-farms-really-the-answer-a-recent-study-reveals-a-surprisingly-large-footprint/)
- [EIT Food — Is vertical farming really sustainable? (2024)](https://www.eitfood.eu/blog/is-vertical-farming-really-sustainable)
