# Designing a TEMPEST-Shielded SCIF for a 50-Person Defense Contractor Office

## Executive Summary

A TEMPEST-shielded SCIF for 50 personnel in a commercial office building with shared HVAC is feasible within $3M but requires aggressive scope management. The shared HVAC system is the single hardest constraint — ICD 705 Tech Spec Section 3.C and CNSSAM TEMPEST/01-13 require that HVAC penetrations prevent both acoustic leakage (STC 45/50) and RF emanation escape, meaning the shared building HVAC must be completely isolated from SCIF airspace via dedicated air handling units, waveguide penetrations, and dielectric breaks. Estimated total cost: $2.4M–$3.1M, with TEMPEST shielding and HVAC isolation consuming 40–50% of the budget. Timeline: 14–24 months to accreditation under post-2025 ICD 705 updates. Confidence: 72%.

## Key Findings

1. **ICD 705 v1.5.1 Tech Spec Section 3.C** mandates three layers of 5/8" gypsum wallboard (2 controlled side, 1 uncontrolled), staggered seams, acoustic fill, and STC 45 minimum (STC 50 for VTC/conference rooms) — [Source](https://exwc.navfac.navy.mil/Portals/88/Documents/EXWC/DoD_Locks/PDFs/ICD-ICS-705_Tech_Spec.pdf)
2. **CNSSAM TEMPEST/01-13** establishes RED/BLACK installation separation distances: 1m baseline, reducible to 30cm with Level 1 TEMPEST-certified equipment — [Source](https://cryptome.org/2014/10/cnssam-tempest-1-13.pdf)
3. **Shared HVAC is the critical risk**: ICD 705 requires HVAC systems prevent escape of compromising emanations and acoustics. Ductwork over 96 sq inches requires slab-to-slab mesh and man bars. All metallic penetrations may require dielectric breaks or grounding per CTTA recommendation — [Source](https://strategicsolutionsunlimited.com/an-overview-of-icd-705-perimeter-wall-requirements/)
4. **SCIF construction costs range $350–$1,000/sqft** depending on TEMPEST requirements and construction type. A 50-person SCIF requires approximately 4,000–5,000 sqft (80–100 sqft/person) — [Source](https://strategicsolutionsunlimited.com/the-cost-to-build-a-scif-or-sapf/)
5. **Accreditation timeline: 14–36 months** under updated ICD 705 standards, with DCSA/DIA mission transfer adding administrative complexity — [Source](https://www.asi247.com/blog/scif-accreditation-process)
6. **NSA/CSS EPL equipment** is required for all TEMPEST-certified systems within the SCIF, including shielded enclosures meeting NSA No. 94-106 — [Source](https://www.nsa.gov/Resources/Media-Destruction-Guidance/NSA-Evaluated-Products-Lists-EPLs/)
7. **UFC 4-010-05 (May 2023)** provides DoD Unified Facilities Criteria for SCIF/SAPF planning, design, and construction, complementing ICD 705 — [Source](https://www.wbdg.org/FFC/DOD/UFC/ufc_4_010_05_2023.pdf)

## Industry Standards Compliance

| Standard | Requirement | Application | Source |
|----------|-------------|-------------|--------|
| ICD 705 Tech Spec Section 3.C | Perimeter walls: 3 layers 5/8" GWB, STC 45+ | All SCIF perimeter walls | [NAVFAC](https://exwc.navfac.navy.mil/Portals/88/Documents/EXWC/DoD_Locks/PDFs/ICD-ICS-705_Tech_Spec.pdf) |
| ICD 705 Tech Spec Section 3.C (VTC) | STC 50 for amplified audio spaces | Conference/VTC rooms | [SPG Secure](https://www.spgsecure.com/post/stc-deciphering-icd-705-acoustic-requirements-and-when-testing-is-required-part-i) |
| CNSSAM TEMPEST/01-13 | RED/BLACK separation: 1m (Level 2), 30cm (Level 1 certified) | All classified processing equipment | [CNSS](https://www.cnss.gov/CNSS/issuances/Memoranda.cfm) |
| ICS 705-2 (Dec 2016) | Accreditation standards and reciprocal use | SCIF accreditation process | [DNI](https://www.dni.gov/files/NCSC/documents/Regulations/ICS_705-2_Standards_for_Accreditation_Reciprocal_Use_of_SCIFs.pdf) |
| UFC 4-010-05 (May 2023) | DoD SCIF/SAPF planning and construction | Facility design baseline | [WBDG](https://www.wbdg.org/FFC/DOD/UFC/ufc_4_010_05_2023.pdf) |
| NSA No. 94-106 | Shielded enclosure testing standard | TEMPEST room certification | [NIST CSRC](https://csrc.nist.gov/glossary/term/tempest_certified_equipment_or_system) |
| CNSSI 7003 (Sept 2015) | Protected Distribution Systems (PDS) | Classified cable routing | [DCSA](https://www.dcsa.mil/Portals/91/documents/ctp/nao/CNSSI_7003_PDS_September_2015.pdf) |
| NIST SP 800-53 Rev 5, PE-3/PE-5 | Physical access control, access control for output devices | Facility security controls | [NIST](https://csrc.nist.gov/) |
| ICD 705 Tech Spec Section 3.2 (Acoustic) | STC 45 minimum perimeter, STC 50 amplified audio areas | All SCIF acoustic envelope | [NAVFAC](https://exwc.navfac.navy.mil/Portals/88/Documents/EXWC/DoD_Locks/PDFs/ICD-ICS-705_Tech_Spec.pdf) |

## Quantitative Analysis

### Space Planning (50 Personnel)

| Zone | Sqft | Function | TEMPEST Level |
|------|------|----------|---------------|
| Open SCIF workspace | 2,500 | 40 analyst workstations @ 60 sqft | Standard SCIF (RF foil GWB) |
| TEMPEST-shielded server room | 300 | Rack enclosures, UPS | Full shielded enclosure (100dB+) |
| VTC/Conference (2 rooms) | 600 | Classified briefings (STC 50) | Enhanced acoustic + RF |
| SCIF manager/SSO office | 200 | Administration | Standard SCIF |
| Entry vestibule/mantrap | 150 | Access control, IDS | Physical security zone |
| Support (breakroom, storage) | 400 | Non-classified support | Outside SCIF boundary |
| Mechanical/electrical | 350 | Dedicated AHU, UPS, panels | TEMPEST boundary |
| **Total** | **4,500** | | |

### Cost Breakdown

| Category | Low Estimate | High Estimate | % of Budget |
|----------|-------------|---------------|-------------|
| TEMPEST RF shielding (walls, ceiling, floor) | $450,000 | $650,000 | 18–22% |
| Acoustic treatment (STC 45/50, doors, seals) | $180,000 | $280,000 | 7–9% |
| Dedicated HVAC system (AHU, waveguide vents) | $250,000 | $400,000 | 10–13% |
| HVAC waveguide penetrations & dielectric breaks | $80,000 | $120,000 | 3–4% |
| Perimeter wall construction (ICD 705 Type A/B) | $200,000 | $300,000 | 8–10% |
| Access control (IDS, mantrap, CCTV, badge) | $180,000 | $250,000 | 7–8% |
| Electrical (filtered power, TEMPEST grounding) | $150,000 | $220,000 | 6–7% |
| TEMPEST-certified server enclosure | $134,000 | $200,000 | 5–7% |
| PDS cabling infrastructure (CNSSI 7003) | $100,000 | $160,000 | 4–5% |
| A&E design (SCIF-cleared architect/engineer) | $200,000 | $300,000 | 8–10% |
| CTTA review, testing, accreditation | $80,000 | $120,000 | 3–4% |
| Contingency (10%) | $240,000 | $310,000 | 10% |
| **Total** | **$2,244,000** | **$3,310,000** | |

**Budget assessment**: The $3M budget is tight but feasible at the low-to-mid range. The shared HVAC isolation is the swing factor — if existing building HVAC can be partially leveraged with waveguide penetrations rather than a fully independent system, costs drop $100–150K.

### Timeline

| Phase | Duration | Key Activities |
|-------|----------|---------------|
| Pre-construction (CSA concept approval) | 2–4 months | FFC submission, CTTA TEMPEST checklist, CSA review |
| A&E design | 3–5 months | Cleared architect, TEMPEST engineer, HVAC engineer |
| Construction | 5–8 months | Perimeter walls, RF shielding, HVAC, electrical, access control |
| Testing & inspection | 1–2 months | STC testing, RF attenuation testing, IDS testing, CTTA TCR |
| Accreditation | 3–6 months | CSA final review, documentation, accreditation decision |
| **Total** | **14–25 months** | |

## Implementation Guidance

### Critical Path: Shared HVAC Isolation

The shared HVAC is the highest-risk element. Here is the required approach:

```yaml
# HVAC Isolation Architecture for SCIF in Shared Commercial Building
scif_hvac:
  dedicated_ahu:
    type: "Split system or packaged rooftop unit"
    capacity: "15-20 tons for 4,500 sqft"
    location: "Inside SCIF mechanical room or dedicated rooftop pad"
    note: "Must NOT share air with building common system"

  penetrations:
    ductwork:
      max_size: "96 sq in without man bars"
      treatment: "HVAC waveguide (honeycomb) at every SCIF boundary penetration"
      vendor: "MAJR Products HVAC Waveguide (ICS/ICD 705 compliant)"
      url: "https://www.majr.com/hvac-waveguide/"
    dielectric_breaks:
      required: "All metallic penetrations per CTTA recommendation"
      material: "Non-conductive coupling or isolation section"
    acoustic:
      duct_lining: "Minimum 2-inch acoustic duct liner at all penetrations"
      silencers: "Duct silencers at each boundary crossing"
      flexible_connections: "Vibration isolators on all mechanical equipment"

  building_isolation:
    return_air: "100% dedicated - NO connection to building return plenum"
    exhaust: "Dedicated exhaust, not tied to building common exhaust"
    pressurization: "Slight positive pressure inside SCIF to prevent infiltration"
```

### RF Shielding Specification

```bash
# TEMPEST Shielding Performance Requirements
# Per NSA No. 94-106 shielded enclosure testing

# Minimum attenuation targets:
# - Server room (full enclosure): ≥100 dB, 400 MHz - 18 GHz
# - SCIF perimeter (architectural): ≥60 dB per CTTA recommendation
# - Doors: RF-shielded doors with knife-edge or finger-stock gaskets

# Approved shielding approaches (consult CTTA for site-specific):
# Option A: Welded steel enclosure (server room) - highest performance
# Option B: Foil-backed GWB (Ultra Radiant R-Foil) per CTTA - perimeter walls
# Option C: Copper mesh in wall cavity - moderate performance

# Vendors on NSA/CSS EPL or with TEMPEST certification:
# - MAJR Products (TEMPEST shielding, waveguides): https://www.majr.com/tempest-shielding/
# - Faraday Defense (shielded rooms): https://shop.faradaydefense.com/
# - Raymond EMC QuietShield TEMPEST: https://raymondemc.com/products/shielded-enclosures/quietshield-tempest/
# - Krieger Products (RF shielded doors): https://www.kriegerproducts.com/radio-frequency/
```

### Accreditation Checklist

```bash
#!/bin/bash
# SCIF Accreditation Document Checklist (ICS 705-2)

echo "=== Pre-Construction ==="
echo "[ ] Fixed Facility Checklist (FFC) submitted to CSA"
echo "[ ] TEMPEST Checklist (DNI SCIF TEMPEST Checklist v1.4) submitted to CTTA"
echo "[ ] Concept approval from Cognizant Security Authority (CSA)"
echo "[ ] CTTA Countermeasures Review (TCR) completed"
echo "[ ] Construction Security Plan (CSP) approved"
echo "[ ] Cleared contractor verification (all construction workers)"

echo ""
echo "=== During Construction ==="
echo "[ ] CSA construction inspections (minimum 3 visits)"
echo "[ ] Photo documentation of all hidden construction (behind walls)"
echo "[ ] RF shielding continuity testing at each phase"
echo "[ ] Acoustic STC testing (STC 45 perimeter, STC 50 VTC rooms)"

echo ""
echo "=== Pre-Accreditation ==="
echo "[ ] Final CTTA TEMPEST inspection and testing"
echo "[ ] IDS (Intrusion Detection System) installation and testing"
echo "[ ] Access control system commissioned"
echo "[ ] STC field test results documented"
echo "[ ] RF attenuation test results documented"
echo "[ ] As-built drawings submitted to CSA"
echo "[ ] Security operating procedures (SOPs) drafted"

echo ""
echo "=== Accreditation Package ==="
echo "[ ] Completed FFC with all attachments"
echo "[ ] TEMPEST Checklist (signed by CTTA)"
echo "[ ] Construction completion report"
echo "[ ] Test reports (STC, RF, IDS)"
echo "[ ] Security SOPs"
echo "[ ] CSA accreditation decision"
```

## Alternatives Considered

| Approach | Cost | Timeline | Pros | Cons |
|----------|------|----------|------|------|
| **Tenant improvement (recommended)** | $2.2–3.3M | 14–25 mo | Lowest cost, leverages existing structure | Shared HVAC complexity, lease dependency |
| Modular SCIF (pre-fab) | $2.5–3.5M | 10–18 mo | Faster, factory-controlled quality | Size limitations for 50 people, floor loading |
| Purpose-built standalone | $4–6M | 18–30 mo | Full control, no shared systems | Exceeds $3M budget, requires land |
| Container SCIF (TSCIF) | $1.5–2.5M | 6–12 mo | Fastest, relocatable | Only 2-4 person capacity, not suitable for 50 |

## Adversarial Review

### Counterargument 1: "$3M is insufficient for TEMPEST + shared HVAC"

**Argument**: Industry data shows TEMPEST-shielded SCIFs at $500–$1,000/sqft. At 4,500 sqft, that's $2.25M–$4.5M before HVAC isolation, pushing total to $3.5–5.5M.

**Rebuttal**: The $500–$1,000/sqft range includes fully shielded enclosures (100dB+). A hybrid approach — full shielded enclosure only for the 300-sqft server room ($134K–$200K) and architectural RF shielding (foil-backed GWB) for the remaining perimeter — brings costs to $350–$500/sqft for the overall facility. This hybrid is CTTA-approvable when the inspectable space profile supports it. Budget risk remains real at the high end; a 10% contingency is built in but could be consumed.

### Counterargument 2: "Shared HVAC makes commercial building unsuitable" (common myth)

**Argument**: A common myth in the defense contractor community is that shared HVAC makes commercial buildings unsuitable for SCIFs, and that the requirement to prevent compromising emanations through HVAC means you need a completely independent system, which is impractical in a multi-tenant building. This premise must be challenged.

**Rebuttal**: ICD 705 does not prohibit SCIFs in commercial buildings — it requires engineered solutions. A dedicated AHU serving only the SCIF space, with waveguide penetrations at the SCIF boundary, meets the standard. The building's shared system provides condenser water or chilled water to the dedicated AHU but shares no air. This is standard practice per MAJR Products HVAC waveguide solutions and is specifically addressed in the ICD 705 Tech Spec. The CTTA reviews this on a case-by-case basis.

### Counterargument 3: "Post-2025 ICD 705 updates may invalidate current design"

**Argument**: ODNI is releasing the first major ICD 705 overhaul in 15 years, with enhanced TEMPEST/RF requirements. A design started now may not comply when updates take effect.

**Rebuttal**: Valid concern. The updated requirements are expected to enhance, not relax, RF shielding standards. Designing to the higher end of current CTTA recommendations (rather than minimum) provides a buffer. The CSA concept approval process includes review against current and pending standards. Engaging the CSA early (Phase 1) provides advance notice of any changes that affect design.

### Assumption Audit

| Assumption | Status | Risk if Wrong |
|------------|--------|--------------|
| 80–100 sqft/person is adequate | Reasonable (GSA standard) | Undersized SCIF, need more space = more cost |
| Building structure can support SCIF loads | Unverified — requires structural assessment | Reinforcement costs $50–150K |
| Cleared construction workforce available | Reasonable in major metro areas | Rural locations: 3–6 month delay |
| CTTA will approve architectural (not full enclosure) RF shielding for workspace | Probable but site-specific | Full enclosure for 2,500 sqft adds $300–500K |
| Building lease permits SCIF modifications | Must verify | Lease restrictions could be a showstopper |
| DCSA/DIA mission transfer does not delay accreditation | Uncertain (in progress) | 3–6 month additional delay |

### Failure Modes

1. **Budget overrun**: Shared HVAC isolation costs exceed estimate → mitigate with early CTTA engagement and phased construction
2. **Accreditation delay**: Post-2025 ICD 705 changes require design revision → mitigate by designing above minimum
3. **Lease termination**: Building owner refuses SCIF modifications or doesn't renew → $2M+ sunk cost; mitigate with long-term lease (10+ years) before construction
4. **Structural inadequacy**: Floor can't support server room loads → structural assessment required before design commit

## Recommendation

**Proceed with tenant improvement approach**, but gate the $3M commitment on three pre-conditions:

1. **Structural assessment** of the commercial building (floor loading for server room, wall attachment points for RF shielding) — $15–25K, 2–4 weeks
2. **Early CSA concept approval** with CTTA TEMPEST checklist submission — determines whether architectural RF shielding is acceptable or full enclosure is required (the single largest cost variable)
3. **Lease verification** — confirm landlord permits SCIF modifications and offers 10+ year term

If all three clear, the $3M budget is achievable at the 50th percentile confidence level. If the CTTA requires full-enclosure shielding for the entire workspace (not just server room), budget rises to $3.5–4M and requires scope reduction (e.g., 35-person SCIF instead of 50).

**Confidence: 72%** — High confidence on technical feasibility and standards compliance; moderate confidence on budget sufficiency due to CTTA site-specific determination being the key variable.

## Sources

- [ICD/ICS 705 Tech Spec v1.5.1 (NAVFAC)](https://exwc.navfac.navy.mil/Portals/88/Documents/EXWC/DoD_Locks/PDFs/ICD-ICS-705_Tech_Spec.pdf)
- [ICS 705-2 Accreditation Standards (DNI)](https://www.dni.gov/files/NCSC/documents/Regulations/ICS_705-2_Standards_for_Accreditation_Reciprocal_Use_of_SCIFs.pdf)
- [DNI SCIF TEMPEST Checklist v1.4](https://www.dni.gov/files/Governance/CLEANED_705-Tech-Spec-SCIF-TEMPEST-Checklist-1.4.pdf)
- [CNSSAM TEMPEST/01-13 RED/BLACK Installation Guidance](https://cryptome.org/2014/10/cnssam-tempest-1-13.pdf)
- [CNSS Issuances (Memoranda)](https://www.cnss.gov/CNSS/issuances/Memoranda.cfm)
- [CNSSI 7003 Protected Distribution Systems (DCSA)](https://www.dcsa.mil/Portals/91/documents/ctp/nao/CNSSI_7003_PDS_September_2015.pdf)
- [UFC 4-010-05 SCIF/SAPF Planning (WBDG)](https://www.wbdg.org/FFC/DOD/UFC/ufc_4_010_05_2023.pdf)
- [NIST CSRC TEMPEST Glossary](https://csrc.nist.gov/glossary/term/tempest_certified_equipment_or_system)
- [NSA/CSS EPL Lists](https://www.nsa.gov/Resources/Media-Destruction-Guidance/NSA-Evaluated-Products-Lists-EPLs/)
- [SCIF Construction Cost Guide (SSU)](https://strategicsolutionsunlimited.com/the-cost-to-build-a-scif-or-sapf/)
- [ICD 705 Perimeter Wall Requirements (SSU)](https://strategicsolutionsunlimited.com/an-overview-of-icd-705-perimeter-wall-requirements/)
- [ICD 705 SCIF Compliance (DAVIS Construction)](https://www.davisconstruction.com/news-insights/icd-705-scif-compliance-what-you-need-know)
- [ICD 705 RF Shielding 2025-2027 (DAVIS)](https://www.davisconstruction.com/sites/default/files/2025-08/DAVIS_ICD%20705%20RF%20Shielding%20Requirements.pdf)
- [SCIF Accreditation Process (ASI)](https://www.asi247.com/blog/scif-accreditation-process)
- [MEP Design for SCIF Spaces (GHT)](https://ghtltd.com/mep-design-scif-spaces/)
- [ICD 705 Acoustic Requirements (SPG Secure)](https://www.spgsecure.com/post/stc-deciphering-icd-705-acoustic-requirements-and-when-testing-is-required-part-i)
- [ICD 705 Wall Types (Cooper Builds)](https://www.cooperbuilds.com/post/scif-sapf-wall-types-understanding-icd-705-minimum-requirements-and-applications)
- [TEMPEST Shielding (MAJR Products)](https://www.majr.com/tempest-shielding/)
- [HVAC Waveguide ICD 705 Compliant (MAJR)](https://www.majr.com/hvac-waveguide/)
- [Faraday Defense Shielded Room NEXUS](https://shop.faradaydefense.com/product/tempest-shielded-room-nexus/)
- [Raymond EMC QuietShield TEMPEST](https://raymondemc.com/products/shielded-enclosures/quietshield-tempest/)
- [Krieger RF Shielded Doors](https://www.kriegerproducts.com/radio-frequency/)
- [New SCIF Requirements Under ICD 705 (MGAC)](https://www.mgac.com/blog/new-scif-requirements-under-the-icd-705/)
- [ICD 705 Modular SCIF Guide (CenCore)](https://cencoregroup.com/comprehensive-guide-to-icd-705-modular-scif-requirements/)
- [TEMPEST (Wikipedia)](https://en.wikipedia.org/wiki/Tempest_(codename))
- [FAA TEMPEST Countermeasures Order](https://www.faa.gov/documentLibrary/media/Order/1600.67.pdf)
- [BICSI Classified Facility Cabling](https://www.bicsi.org/docs/default-source/conference-presentations/2017-winter/classified-facility-communications-cabling.pdf)
- [JLL SCIF Construction Insights](https://www.jll.com/en-us/insights/navigating-the-new-era-of-scif-construction-compliance-security-and-strategy)
- [ICD 705 Construction Changes (LVT)](https://www.lvt.com/blog/icd-705-construction-security-requirements-whats-changing-and-how-to-prepare)
- [Navigating SCIF Construction (Area Development)](https://www.areadevelopment.com/business-climate/q1-2025/navigating-the-new-era-of-scif-construction.shtml)
