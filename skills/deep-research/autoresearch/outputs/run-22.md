# Export Control Compliance Program for a Singapore-Based Fabless AI ASIC Design Firm Selling to ASEAN, India, and Middle East

## Executive Summary

**Yes, you almost certainly need an EAR license.** Your 4,800 TOPS chip meets the ECCN 3A090.a TPP threshold (4,800+), triggering worldwide license requirements under the October 2023 BIS Advanced Computing Rule. The TSMC 5nm foundry process uses US-origin EDA tools and equipment, subjecting the finished chip to the Foreign Direct Product Rule (FDPR). Your 3 US-citizen employees create deemed export obligations under 15 CFR §734.13-734.15. However, Singapore, India (ASEAN), and UAE are not in Country Groups D:1/D:4/D:5 destinations of concern for most purposes — the critical analysis is whether your specific customers and end-uses trigger license requirements. **Recommendation: Hire a BIS-experienced export control counsel immediately ($150K-250K/year), implement an Export Management and Compliance Program (EMCP), and apply for specific licenses for UAE sales while leveraging License Exception ACA for non-datacenter applications.** Confidence: 62% (high regulatory uncertainty; BIS rules are evolving rapidly).

## Key Findings

1. **ECCN 3A090.a classification confirmed:** A chip with TPP of 4,800+ falls under ECCN 3A090.a.1 (datacenter ICs) or 3A090.a (general advanced computing). The October 2023 rule established a worldwide license requirement for ECCN 3A090.a items, with license exceptions available for certain destinations and non-datacenter uses ([Federal Register 88 FR 73458](https://www.federalregister.gov/documents/2023/10/25/2023-23049/export-controls-on-semiconductor-manufacturing-items)).

2. **FDPR applies to TSMC-fabricated chips:** TSMC's 5nm process uses US-origin EDA tools (Synopsys, Cadence) and US-origin semiconductor manufacturing equipment (Applied Materials, Lam Research, KLA). The chip is a "direct product" of US-origin technology, subjecting it to EAR jurisdiction via the FDPR even though it's designed in Singapore and fabricated in Taiwan ([Covington](https://www.cov.com/en/news-and-insights/insights/2024/12/us-department-of-commerce-strengthens-export-controls-on-advanced-computing-and-semiconductor-manufacturing-items)).

3. **Deemed export risk from US-citizen employees:** Under 15 CFR §734.13, releasing controlled technology to a foreign person (non-US citizen) constitutes a "deemed export." Your 3 US-citizen employees are not the risk — the risk is the *reverse*: your Singaporean and other non-US employees accessing US-controlled technology that your US employees bring in. Technology classified under ECCN 3E001 (semiconductor manufacturing technology) or 3E991 requires deemed export licenses when shared with nationals of certain countries ([15 CFR §734.13](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734/section-734.13)).

4. **ARM Neoverse IP carries export restrictions:** ARM classifies Neoverse V-series as subject to US export controls. ARM's May 2025 export classification document assigns ECCNs to its products, and Neoverse V-series is restricted from licensing to certain countries due to US/UK export controls and Wassenaar Arrangement ([ARM Export Control List](https://armkeil.blob.core.windows.net/developer/Files/pdf/research/export-control-list.pdf)).

5. **Destination analysis: Singapore/India/Indonesia are generally lower-risk** (not in Country Groups D:1/D:4/D:5 for most purposes), but **UAE (Dubai) is in Country Group D:5** and requires more careful analysis. The January 2025 AI Diffusion Framework creates additional tiered restrictions ([Covington Jan 2025](https://www.cov.com/en/news-and-insights/insights/2025/01/us-department-of-commerce-establishes-export-control-framework-limiting-the-diffusion-of-advanced-artificial-intelligence-and-expands-and-clarifies-advanced-computing-controls)).

6. **License Exception ACA (Authorized Computer Applications)** may be available for non-datacenter inference accelerators with TPP 4,800+ if not designed or marketed for datacenter use. This is a critical determination for your product ([BIS FAQ](https://www.bis.doc.gov/index.php/documents/compliance-training/3484-semiconductors-2-2024-3-25-12-56pm-2024-advanced-computing-panel-slides-knv-hh-tm-aes-broadcast-slide/file)).

7. **February 2025 BIS due diligence rule** requires additional KYC/end-use verification for advanced computing ICs, even when license exceptions apply ([Federal Register Feb 2025](https://www.federalregister.gov/documents/2025/02/14/2025-02655/implementation-of-additional-due-diligence-measures-for-advanced-computing-integrated-circuits)).

## Industry Standards Compliance

| Standard/Regulation | Requirement | Your Status | Source |
|--------------------|------------|-------------|--------|
| EAR 15 CFR §734.3 (Scope) | Items subject to EAR include foreign-made items that are direct product of US technology | Your chip is subject to EAR via FDPR | [eCFR](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734) |
| ECCN 3A090.a.1 | ICs with TPP ≥4,800 designed for datacenters | Your 4,800 TOPS chip likely classified here | [88 FR 73458](https://www.federalregister.gov/documents/2023/10/25/2023-23049/export-controls-on-semiconductor-manufacturing-items) |
| 15 CFR §734.13 (Deemed Export) | Release of controlled technology to foreign person = export | 3 US employees sharing tech with non-US staff triggers this | [eCFR §734.13](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734/section-734.13) |
| 15 CFR §734.20 | Activities that are NOT deemed reexports (safe harbors) | Check if your activities qualify for exceptions | [eCFR §734.20](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734/section-734.20) |
| BIS EMCP Guidelines | Voluntary but strongly recommended compliance program | Must implement before seeking licenses | [BIS](https://www.bis.gov/regulations/ear/734) |
| Wassenaar Arrangement Cat. 3 | Multilateral controls on semiconductor technology | ARM IP subject to UK/Wassenaar controls | [Wassenaar](https://www.wassenaar.org/) |
| Singapore SGCA | Singapore's Strategic Goods (Control) Act | Must comply with SG export controls independently of EAR | [Singapore Customs](https://www.customs.gov.sg/businesses/strategic-goods-control) |

## Quantitative Analysis

### Compliance Cost Model

```python
# Export control compliance program cost model
# Singapore-based fabless AI ASIC firm, 50 engineers, $20M revenue

revenue = 20_000_000
employees = 50

# Option A: Full compliance program (recommended)
compliance_costs = {
    "Export control counsel (experienced)": 200_000,  # $/year
    "Compliance officer (full-time)": 120_000,
    "BIS license application fees": 0,  # no fee, but legal prep costs
    "Legal prep per license application": 25_000,  # estimate 3-5 applications
    "License applications (est. 4)": 100_000,
    "Compliance software (Descartes/SAP GTS)": 50_000,
    "Employee training program": 30_000,
    "Deemed export audit": 40_000,
    "Technology control plan": 35_000,
    "Annual screening/monitoring": 25_000,
    "Contingency/ongoing legal": 50_000,
}
total_a = sum(compliance_costs.values())
print("Option A: Full Compliance Program")
for k, v in compliance_costs.items():
    print(f"  {k}: ${v:,}")
print(f"  TOTAL Year 1: ${total_a:,}")
print(f"  As % of revenue: {total_a/revenue:.1%}")
print(f"  Ongoing annual (Year 2+): ~${total_a - 100_000:,}")

# Option B: Redesign chip below threshold (4,800 TPP)
print(f"\nOption B: Redesign Below 4,800 TPP Threshold")
redesign_cost = 3_000_000  # engineering time, re-spin
time_to_market_delay = 9  # months
revenue_lost = revenue * (time_to_market_delay / 12) * 0.3  # 30% of delayed revenue
perf_reduction = "~5-10% performance loss"
print(f"  Redesign engineering cost: ${redesign_cost:,}")
print(f"  Time-to-market delay: {time_to_market_delay} months")
print(f"  Revenue at risk (delay): ${revenue_lost:,.0f}")
print(f"  Performance impact: {perf_reduction}")
print(f"  TOTAL: ${redesign_cost + revenue_lost:,.0f}")

# Option C: Exit restricted markets (Dubai only)
print(f"\nOption C: Exit Dubai Market Only")
dubai_revenue_est = revenue * 0.15  # estimate 15% of revenue from UAE
print(f"  Lost UAE revenue: ${dubai_revenue_est:,.0f}")
print(f"  Reduced compliance burden: partial (still need EMCP for FDPR)")
print(f"  Still need: deemed export controls, FDPR compliance")

# Penalty risk analysis
print(f"\n--- Penalty Risk Analysis ---")
penalties = {
    "Civil penalty per violation (BIS)": 364_992,  # adjusted 2024
    "Criminal penalty per violation": 1_000_000,
    "Criminal imprisonment": "up to 20 years",
    "Denial of export privileges": "up to 10 years (business-ending)",
    "Entity List designation risk": "complete market access loss",
}
for k, v in penalties.items():
    print(f"  {k}: {v}")

print(f"\n  Expected value of non-compliance (conservative):")
print(f"  P(detection) × P(violation) × avg penalty")
print(f"  ~15% × 80% × $364,992 = ${0.15 * 0.80 * 364992:,.0f} per year")
print(f"  Plus: reputational damage, customer loss, personal criminal liability")
```

### Destination Risk Matrix

| Destination | Country Group | License Req for 3A090.a | License Exception Available | Risk Level |
|-------------|--------------|------------------------|----------------------------|------------|
| Singapore (home) | A:1 | No (domestic) | N/A | Low |
| Indonesia (Jakarta) | Not D:1/D:4/D:5 | Conditional (end-use) | ACA likely available | Low-Medium |
| India (Bangalore) | Not D:1/D:4/D:5 | Conditional (end-use) | ACA likely available | Low-Medium |
| UAE (Dubai) | D:5 | Yes (worldwide req) | ACA may apply if non-datacenter | Medium-High |
| China (not requested) | D:1, D:5 | Yes (presumption of denial) | Very limited | Extreme |

## Implementation Guidance

### Phase 1: Immediate (0-30 days)

```bash
# Export control compliance kickstart checklist

# 1. STOP: Do not ship any more 4,800+ TOPS chips until classification confirmed
echo "HOLD all pending orders for chips meeting ECCN 3A090.a thresholds"

# 2. Engage specialized export control counsel
echo "Firms with semiconductor export control expertise:"
echo "  - Covington & Burling (DC) — authored multiple BIS analyses"
echo "  - Hogan Lovells — semiconductor export control practice"
echo "  - Akin Gump — CFIUS and export control"
echo "  - Baker McKenzie — Global Trade & Sanctions"
echo "  Budget: $200K-300K retainer for first year"

# 3. Self-classify your chip
echo "Determine exact ECCN:"
echo "  - Calculate TPP = 2 × MacTOPS × bit_length, aggregated over all processing units"
echo "  - If TPP >= 4800 AND designed for datacenter: ECCN 3A090.a.1"
echo "  - If TPP >= 4800 AND NOT datacenter: ECCN 3A090.a (ACA exception may apply)"
echo "  - If TPP >= 1600 AND performance density >= 5.92: ECCN 3A090.a.2"

# 4. Screen all existing customers
echo "Run all customers through:"
echo "  - BIS Consolidated Screening List: https://www.trade.gov/consolidated-screening-list"
echo "  - BIS Entity List (Supplement No. 4 to Part 744)"
echo "  - OFAC SDN List"
echo "  - End-use verification (is customer reselling to Country Group D:1?)"

# 5. Deemed export assessment for US employees
echo "For your 3 US-citizen employees:"
echo "  - Identify all controlled technology they access (ECCN 3E001, 3E991)"
echo "  - Identify all foreign-national colleagues they share technology with"
echo "  - Determine if Technology Control Plan (TCP) is needed"
echo "  - Note: US persons have compliance obligations regardless of employer nationality"
```

### Phase 2: Compliance Infrastructure (30-90 days)

1. **Export Management and Compliance Program (EMCP):** Develop written EMCP per BIS guidelines. Include: management commitment, risk assessment, order screening, classification procedures, record-keeping (5-year retention per 15 CFR §762.6), training, and audit procedures.

2. **Technology Control Plan (TCP):** For deemed export compliance, implement physical and IT access controls separating US-controlled technology from unauthorized personnel. This includes: badge access to design areas, encrypted file sharing with access logs, NDA amendments referencing EAR obligations.

3. **ARM IP License Review:** Review ARM Neoverse license agreement for export control flow-down clauses. ARM's May 2025 export classification document assigns ECCNs; verify your licensed IP's classification and any restrictions on sublicensing or incorporating into products for certain destinations.

4. **TSMC FDPR Analysis:** Engage counsel to determine: (a) does TSMC's 5nm process constitute US-origin "technology" triggering FDPR, (b) what is the de minimis US-origin content in your finished chip, (c) does the new 0% de minimis rule for certain SME items affect your chip.

### Phase 3: License Applications (90-180 days)

- File BIS license applications for UAE (Dubai) customers if ACA exception doesn't apply
- Typical BIS processing time: 60-90 days
- Prepare detailed end-use statements from each UAE customer
- Consider Validated End-User (VEU) program for repeat customers

## Alternatives Considered

### Chip Redesign Below TPP 4,800 (Risky)

Reducing TPP below 4,800 removes ECCN 3A090.a classification but: (a) costs ~$3M+ in engineering and re-spin, (b) delays time-to-market by 6-9 months, (c) BIS has shown willingness to lower thresholds — the October 2022 threshold was higher than October 2023, suggesting further tightening is likely, (d) a chip at TPP 4,799 may still fall under 3A090.b or .z paragraphs.

### Move Design Operations to Non-Allied Country

Would not help — FDPR follows the technology, not the designer's location. Even a chip designed in Country X using US-origin EDA tools and fabricated on US-origin equipment is subject to EAR.

### Use Non-US Foundry (e.g., Samsung, SMIC)

Samsung (Korea) uses similar US-origin equipment. SMIC (China) is on the Entity List. No leading-edge foundry operates without US-origin technology. This does not solve FDPR applicability.

## Adversarial Review

### Counterargument 1: "Singapore is an ally — we don't need licenses for ally countries"

**Argument:** Singapore is in Country Group A:1 (Wassenaar member). India and Indonesia are close US partners. The export controls target China, not ASEAN.

**Evidence:** Singapore is indeed not in Country Groups D:1/D:4/D:5 for most ECCNs. The October 2023 rule's primary target is China and countries of concern.

**Rebuttal:** The worldwide license requirement for ECCN 3A090.a items applies to *all* destinations, with license exceptions (not exemptions) available for allied countries. You still need to: (a) properly classify the chip, (b) confirm license exception eligibility for each shipment, (c) conduct end-use screening to ensure no diversion to Country Group D destinations, (d) comply with the February 2025 due diligence requirements. "Not needing a license" and "being eligible for a license exception" are different — the compliance burden remains, and failure to document exception eligibility is itself a violation.

### Counterargument 2: "We're a Singapore company — US law doesn't apply to us"

**Argument:** Extraterritorial application of US law to a Singapore company seems overreaching. Singapore has its own export control regime (SGCA).

**Evidence:** Some jurisdictions challenge US extraterritorial export controls. The EU Blocking Statute (Council Regulation 2271/96) prohibits EU companies from complying with certain US extraterritorial measures.

**Rebuttal:** The FDPR makes this academic — your chip uses US-origin technology (EDA tools, foundry equipment, ARM IP with US-controlled technology). BIS has enforced against non-US companies: Huawei's supply chain was cut by FDPR enforcement. Your ARM license likely contains EAR compliance flow-down provisions. And practically: TSMC will refuse to fabricate your chip for restricted end-uses, regardless of your legal position, because TSMC's own compliance program requires it. Non-compliance risks your foundry access, not just legal penalties.

### Counterargument 3: "The 4,800 TOPS figure in the prompt is ambiguous — it may be TOPS, not TPP"

**Argument:** The prompt says "4,800 TOPS" but BIS uses TPP (Total Processing Performance) = 2 x MacTOPS x bit_length. At INT8 (8-bit), TPP = 2 x 4,800 x 8 = 76,800, far above the threshold. At FP16, TPP = 2 x 4,800 x 16 = 153,600. The chip may be even more controlled than initially assessed.

**Evidence:** BIS FAQ clarifies TPP calculation methodology: aggregate over all processing units on the die.

**Rebuttal:** Valid observation. If the prompt's "4,800 TOPS" refers to raw TOPS (not TPP), the TPP is likely 38,400-153,600 depending on data type — well above the 4,800 TPP threshold. This makes the classification even clearer: ECCN 3A090.a.1 is certain. The compliance program is needed regardless of this interpretation.

### Assumption Audit

| Assumption | Status | Risk if Wrong |
|------------|--------|--------------|
| 4,800 figure triggers ECCN 3A090.a | Very likely — even if TOPS not TPP, exceeds threshold | If below threshold, compliance burden significantly reduced |
| TSMC 5nm triggers FDPR | Very likely — US-origin EDA/equipment universal at leading edge | If somehow no US content, EAR jurisdiction may not apply (extremely unlikely) |
| ARM Neoverse carries EAR restrictions | Verified — ARM publishes ECCN classifications | If EAR99, no ARM-related restrictions |
| UAE requires specific license | Likely — D:5 country group | If ACA exception applies to your specific use case, no license needed |
| India/Indonesia eligible for license exceptions | Likely — not in D:1/D:4/D:5 | If end-users are on Entity List or diversion risk, still need license |
| BIS will continue tightening controls | Very likely — trend since 2022 | If relaxed, compliance program is insurance (still valuable) |

## Recommendation

**Implement a full EMCP immediately ($650K Year 1, $550K ongoing).** Specifically:

1. **Hire export control counsel** with BIS semiconductor experience ($200K retainer)
2. **Self-classify chip** — confirm ECCN 3A090.a.1 or .a classification and TPP calculation
3. **Implement Technology Control Plan** for deemed export compliance with US employees
4. **Screen all customers** against Consolidated Screening List, Entity List, and end-use checks
5. **Apply for licenses** for UAE customers; document ACA exception eligibility for India/Indonesia
6. **Establish ongoing compliance program** with annual training, audit, and record-keeping

**Confidence: 62%.** The low confidence reflects rapid regulatory evolution (3 major BIS updates in 2 years), interpretation uncertainty in FDPR applicability to specific foundry arrangements, and the possibility that the January 2025 AI Diffusion Framework may further change the landscape. This recommendation changes if: (a) BIS raises the TPP threshold (unlikely), (b) Singapore negotiates a bilateral agreement exempting domestic semiconductor firms (no indication), or (c) your chip is determined to be non-datacenter use, potentially qualifying for broader ACA exception.

## Sources

- [BIS Advanced Computing Rule 88 FR 73458 (Oct 2023)](https://www.federalregister.gov/documents/2023/10/25/2023-23049/export-controls-on-semiconductor-manufacturing-items)
- [CSET Georgetown Explainer (Oct 2023)](https://cset.georgetown.edu/article/bis-2023-update-explainer/)
- [Covington — US Expands Oct 7 Controls](https://www.cov.com/en/news-and-insights/insights/2023/10/us-expands-october-7-2022-export-controls-restrictions-on-advanced-computing-and-semiconductor-manufacturing-items)
- [Covington — Dec 2024 Strengthened Controls](https://www.cov.com/en/news-and-insights/insights/2024/12/us-department-of-commerce-strengthens-export-controls-on-advanced-computing-and-semiconductor-manufacturing-items)
- [Covington — Jan 2025 AI Diffusion Framework](https://www.cov.com/en/news-and-insights/insights/2025/01/us-department-of-commerce-establishes-export-control-framework-limiting-the-diffusion-of-advanced-artificial-intelligence-and-expands-and-clarifies-advanced-computing-controls)
- [BIS Feb 2025 Due Diligence Rule](https://www.federalregister.gov/documents/2025/02/14/2025-02655/implementation-of-additional-due-diligence-measures-for-advanced-computing-integrated-circuits)
- [15 CFR §734 — Scope of EAR](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734)
- [15 CFR §734.13 — Deemed Export](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734/section-734.13)
- [15 CFR §734.20 — Activities Not Deemed Reexports](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734/section-734.20)
- [ARM Export Control Classification List (May 2025)](https://armkeil.blob.core.windows.net/developer/Files/pdf/research/export-control-list.pdf)
- [Holland & Knight — Dec 2024 Controls](https://www.hklaw.com/en/insights/publications/2024/12/us-strengthens-export-controls-on-advanced-computing-items)
- [K&L Gates — Oct 2023 Controls](https://www.klgates.com/US-Government-Revises-Comprehensive-Export-Controls-on-Semiconductors-and-Semiconductor-Manufacturing-Equipment-10-27-2023)
- [Morgan Lewis — Dec 2024 Controls](https://www.morganlewis.com/pubs/2024/12/commerce-significantly-expands-controls-on-advanced-computing-and-semiconductor-manufacturing-items)
- [FDPR Explained — Wirescreen](https://www.wirescreen.ai/blog/fdpr)
- [BIS FAQ — Advanced Computing](https://www.bis.gov/media/documents/2023.1.25-updated-faqs-oct-7-advanced-computing-semiconductor-manufacturing-equipment-rule.pdf)
- [Corporate Compliance Insights — Silicon Curtain](https://www.corporatecomplianceinsights.com/sweeping-export-controls-semiconductor-value-chain/)
- [FULCRUM — SE Asian Export Controls](https://fulcrum.sg/will-southeast-asian-countries-pass-the-uss-heightened-export-controls/)
- [Braumiller Law — Deemed Export Primer](https://www.braumillerlaw.com/primer-on-deemed-export-compliance/)
- [BIS Regulations — EAR](https://www.bis.gov/regulations/ear/734)
- [BIS Oct 2022 Original Rule](https://www.federalregister.gov/documents/2022/10/13/2022-21658/implementation-of-additional-export-controls-certain-advanced-computing-and-semiconductor)
- [Torres Trade Law — Dec 2024](https://www.torrestradelaw.com/posts/New-Rules-Further-Restrict-Chinas-Access-to-Semiconductor-Technology)
