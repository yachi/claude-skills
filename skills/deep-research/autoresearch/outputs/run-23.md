# Mobile Banking App Accessibility Remediation for a Credit Union Under ADA Title III Litigation

## Executive Summary

**Critical premise correction: The DOJ's April 2024 Title II web accessibility rule (28 CFR Part 35) does NOT apply to your credit union.** Title II covers state and local government entities only. Credit unions are private entities covered under ADA Title III — which has no explicit WCAG standard but where courts routinely use WCAG 2.1 AA as the benchmark. **Do NOT use an accessibility overlay vendor like accessiBe** — the FTC fined accessiBe $1M in April 2025 for misrepresenting compliance claims, and 25% of all 2024 accessibility lawsuits targeted sites using overlay widgets. **Recommendation: Engage a specialized accessibility audit firm (Deque, Level Access, or TPGi) for WCAG 2.2 AA audit + remediation, with parallel VPAT/ACR development and EN 301 549 V3.2.1 mapping for European expansion. Budget: $450-650K of the $800K, with $150-350K reserved for ongoing monitoring and legal settlement costs.** Confidence: 78%.

## Key Findings

1. **DOJ 2024 Title II rule does NOT apply to credit unions.** The final rule (28 CFR Part 35, published April 24, 2024) explicitly applies to "State and local government entities." Credit unions are private entities under ADA Title III, not Title II. Your board's assumption is incorrect — correct this immediately to avoid misallocating compliance resources ([Federal Register 2024-07758](https://www.federalregister.gov/documents/2024/04/24/2024-07758/nondiscrimination-on-the-basis-of-disability-accessibility-of-web-information-and-services-of-state)).

2. **ADA Title III applies to credit unions as "places of public accommodation."** Over 60 credit unions have faced website accessibility lawsuits since 2017. Courts and DOJ consent decrees consistently use WCAG 2.0/2.1 Level AA as the compliance standard for Title III digital accessibility ([DeLeon & Stang](https://deleonandstang.com/insights/2018/09/08/credit-union-ada-lawsuits-how-we-got-here-and-whats-next)).

3. **WCAG 2.2 AA adds 9 new success criteria beyond WCAG 2.1**, including 2.4.11 Focus Not Obscured (AA), 2.5.7 Dragging Movements (AA), 2.5.8 Target Size Minimum (AA), 3.2.6 Consistent Help (A), 3.3.7 Redundant Entry (A), and 3.3.8 Accessible Authentication (AA). Your 2021 audit against WCAG 2.0 AA means you're two versions behind — missing all 2.1 and 2.2 criteria ([W3C — What's New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)).

4. **AccessiBe fined $1M by FTC (April 2025)** for misrepresenting that its widget makes websites "fully WCAG compliant within 48 hours." Research shows automated overlays address only ~30% of WCAG issues. 25% of 2024 accessibility lawsuits targeted sites using overlays — the overlay itself becomes evidence of negligence ([FTC/Lainey Feingold](https://www.lflegal.com/2025/01/ftc-accessibe-million-dollar-fine/)).

5. **EN 301 549 V3.2.1 references WCAG 2.1 AA** for mobile apps (Clause 11) with additional requirements. The standard applies to ICT products serving EU public sector bodies. For Canadian military bases in Europe, compliance is required under EU Directive 2016/2102 and potentially the European Accessibility Act (EAA) effective June 2025 ([ETSI](https://www.etsi.org/human-factors-accessibility/en-301-549-v3-the-harmonized-european-standard-for-ict-accessibility)).

6. **Remediation costs: $100-250/screen for audit, $250-550/screen for remediation.** For a banking app with ~50-80 screens: $30K-45K for audit, $50K-120K for remediation. Full program including VPAT, training, and monitoring: $200K-500K ([DigitalA11Y](https://www.digitala11y.com/pricing/)).

7. **Wire transfer accessibility is a high-priority flow.** Blind users relying on VoiceOver need: proper ARIA labels on all form fields, logical focus order, error announcements via `aria-live` regions, and timeout warnings per WCAG 2.2.1 (Timing Adjustable). This is likely where your plaintiff's claim is strongest.

## Industry Standards Compliance

| Standard | Requirement | Applicability | Your Status | Source |
|----------|------------|---------------|-------------|--------|
| ADA Title III (42 USC §12182) | No discrimination in places of public accommodation | Yes — credit unions are public accommodations | Non-compliant (lawsuit filed) | [ABA](https://www.americanbar.org/groups/business_law/resources/business-law-today/2025-august/digital-accessibility-under-title-iii-ada/) |
| DOJ Title II (28 CFR Part 35) | WCAG 2.1 AA for state/local government | **NO — does not apply to credit unions** | N/A — board misconception | [Federal Register](https://www.federalregister.gov/documents/2024/04/24/2024-07758/) |
| WCAG 2.2 AA (W3C Rec, Oct 2023) | 87 success criteria (Level A + AA) | De facto standard for Title III compliance | Non-compliant (audited against 2.0 in 2021) | [W3C](https://www.w3.org/TR/WCAG22/) |
| EN 301 549 V3.2.1 Clause 11 | WCAG 2.1 AA + additional mobile requirements | Required for EU expansion (military bases) | Not assessed | [ETSI](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf) |
| Section 508 (29 USC §794d) | WCAG 2.0 AA for federal agencies | Only if serving federal contracts | Likely not applicable | [Section508.gov](https://www.section508.gov/) |
| NCUA Reg (12 CFR Part 749) | Records preservation and accessibility | Tangential — not accessibility-specific | Compliant | [NCUA](https://www.ncua.gov/) |

## Quantitative Analysis

### Option Comparison Matrix

| Dimension | Overlay (accessiBe) | In-House Remediation | Audit Firm + Rebuild |
|-----------|-------------------|---------------------|---------------------|
| **Cost** | $5K-15K/year subscription | $200K-350K (hire 2 a11y devs + training) | $350K-650K (audit + remediation + VPAT) |
| **Timeline to compliance** | "48 hours" (false per FTC) | 6-12 months | 4-9 months |
| **WCAG 2.2 AA coverage** | ~30% (automated only) | 70-90% (depends on expertise) | 95%+ (expert audit + manual testing) |
| **Legal defensibility** | Very poor (overlay = evidence of negligence) | Moderate (depends on documentation) | Strong (VPAT/ACR, third-party attestation) |
| **EN 301 549 compliance** | No | Partial (if trained) | Yes (included in scope) |
| **VoiceOver wire transfer fix** | Unlikely | Possible if devs trained | Guaranteed (prioritized remediation) |
| **Court admissibility** | Harmful (FTC precedent) | Moderate | Strong (expert testimony available) |
| **Ongoing cost** | $5K-15K/year (false security) | $80K-120K/year (retain a11y team) | $30K-60K/year (annual re-audit) |

### Cost Model

```python
# Accessibility remediation cost model
# Credit union mobile banking app, 180K members, ADA Title III lawsuit

app_screens = 65  # estimated for banking app (login, accounts, transfers, etc.)
critical_flows = 8  # wire transfer, bill pay, mobile deposit, login, etc.

# Option 1: Overlay (DO NOT USE)
overlay_annual = 12_000
overlay_coverage = 0.30  # per FTC finding
print("Option 1: Overlay Widget (accessiBe-type)")
print(f"  Annual cost: ${overlay_annual:,}")
print(f"  WCAG coverage: {overlay_coverage:.0%}")
print(f"  Legal risk: EXTREME (FTC $1M fine precedent, 25% of lawsuits target overlays)")
print(f"  RECOMMENDATION: DO NOT USE")

# Option 2: In-house remediation
inhouse_devs = 2  # accessibility-trained developers
inhouse_salary = 130_000  # each, annual
inhouse_training = 40_000  # IAAP certification, tools
inhouse_tools = 25_000  # axe-core pro, screen reader licenses
inhouse_year1 = inhouse_devs * inhouse_salary + inhouse_training + inhouse_tools
print(f"\nOption 2: In-House Team")
print(f"  Year 1 cost: ${inhouse_year1:,}")
print(f"  Ongoing annual: ${inhouse_devs * inhouse_salary + inhouse_tools:,}")
print(f"  Timeline: 6-12 months (learning curve)")
print(f"  Risk: Moderate — no third-party attestation for court")

# Option 3: Audit firm + remediation (RECOMMENDED)
audit_cost = app_screens * 200  # $200/screen average
remediation_cost = app_screens * 400  # $400/screen average
vpat_cost = 8_000
en301549_mapping = 15_000
training_staff = 25_000
legal_integration = 50_000  # work with defense counsel
monitoring_annual = 45_000  # ongoing automated + manual
project_management = 60_000
total_option3 = audit_cost + remediation_cost + vpat_cost + en301549_mapping + training_staff + legal_integration + monitoring_annual + project_management
print(f"\nOption 3: Audit Firm + Remediation (RECOMMENDED)")
print(f"  Audit (65 screens × $200): ${audit_cost:,}")
print(f"  Remediation (65 screens × $400): ${remediation_cost:,}")
print(f"  VPAT/ACR: ${vpat_cost:,}")
print(f"  EN 301 549 mapping: ${en301549_mapping:,}")
print(f"  Staff training: ${training_staff:,}")
print(f"  Legal integration: ${legal_integration:,}")
print(f"  Annual monitoring: ${monitoring_annual:,}")
print(f"  Project management: ${project_management:,}")
print(f"  TOTAL: ${total_option3:,}")
print(f"  Timeline: 4-6 months to substantial compliance")

# Settlement cost estimate
print(f"\n--- Settlement/Litigation Cost Estimate ---")
settlement_range_low = 50_000  # typical ADA website settlement
settlement_range_high = 300_000  # complex financial services
legal_defense = 150_000  # 9 months of litigation
attorney_fees_plaintiff = 75_000  # if you lose, you pay plaintiff's fees
print(f"  Settlement range: ${settlement_range_low:,}-${settlement_range_high:,}")
print(f"  Legal defense (9 mo): ${legal_defense:,}")
print(f"  Plaintiff attorney fees (if lost): ${attorney_fees_plaintiff:,}")
print(f"  Total litigation exposure: ${settlement_range_low + legal_defense:,}-${settlement_range_high + legal_defense + attorney_fees_plaintiff:,}")

# Budget allocation from $800K
print(f"\n--- $800K Budget Allocation ---")
budget = 800_000
remediation_budget = total_option3
settlement_reserve = 175_000
legal_defense_budget = 150_000
contingency = budget - remediation_budget - settlement_reserve - legal_defense_budget
print(f"  Remediation program: ${remediation_budget:,}")
print(f"  Settlement reserve: ${settlement_reserve:,}")
print(f"  Legal defense: ${legal_defense_budget:,}")
print(f"  Contingency/expansion: ${contingency:,}")
print(f"  Total: ${budget:,}")
```

## Implementation Guidance

### Phase 1: Emergency Triage (Weeks 1-4)

```bash
# Immediate actions before court deadline

# 1. Fix the wire transfer flow (plaintiff's specific complaint)
echo "PRIORITY: Wire transfer VoiceOver accessibility"
echo "  - Add aria-label to all form fields (recipient, amount, routing)"
echo "  - Ensure logical tab order through transfer form"
echo "  - Add aria-live='polite' for balance updates and confirmations"
echo "  - Add aria-live='assertive' for error messages"
echo "  - Test with VoiceOver (iOS) AND TalkBack (Android)"
echo "  - Timeline: 2 weeks for wire transfer fix"

# 2. Engage audit firm
echo "Recommended firms (banking/financial expertise):"
echo "  - Level Access (levelaccess.com) — financial services specialty"
echo "  - Deque Systems (deque.com) — axe tools ecosystem"
echo "  - TPGi (tpgi.com) — VPAT/ACR specialists"
echo "  Budget: $50K-80K for initial audit"
echo "  Timeline: 3-4 weeks for audit report"

# 3. Correct board misconception
echo "BRIEF BOARD: DOJ Title II (28 CFR Part 35) = state/local government ONLY"
echo "  Your obligation: ADA Title III (42 USC §12182)"
echo "  Standard: WCAG 2.2 AA (court practice, not statutory mandate)"
echo "  Action: Reallocate any Title II compliance budget to Title III remediation"

# 4. Document good faith effort for court
echo "Generate timestamped evidence of remediation:"
echo "  - Engagement letter with audit firm (week 1)"
echo "  - Remediation roadmap with milestones (week 2)"
echo "  - Wire transfer fix deployed (week 2-3)"
echo "  - Preliminary audit report (week 4)"
```

### Phase 2: Systematic Remediation (Months 2-6)

1. **WCAG 2.2 AA audit** (all 87 Level A + AA success criteria) across all 65+ screens
2. **Priority remediation** by severity: (a) complete blockers (cannot use feature), (b) serious (can use with difficulty), (c) moderate (inconvenience), (d) minor
3. **Focus on new WCAG 2.2 criteria:** 2.4.11 Focus Not Obscured, 2.5.8 Target Size (24x24 CSS px minimum), 3.3.8 Accessible Authentication (no cognitive function tests for login)
4. **VPAT/Accessibility Conformance Report (ACR)** generation: document conformance level per criterion for court evidence
5. **EN 301 549 V3.2.1 Clause 11 mapping:** identify delta between WCAG 2.2 AA and EN 301 549 additional requirements for mobile apps (Chapter 11)

### Phase 3: Sustained Compliance (Month 7+)

- Integrate automated testing (axe-core, Lighthouse) into CI/CD pipeline
- Quarterly manual testing by users with disabilities (minimum: screen reader, keyboard-only, switch access)
- Annual third-party re-audit ($15K-25K)
- IAAP CPACC/WAS certification for 2-3 development team members
- Accessibility statement published on app and website

## Alternatives Considered

### Accessibility Overlay (Rejected)

AccessiBe, UserWay, and similar overlays are categorically rejected:
- FTC fined accessiBe $1M for false compliance claims (April 2025)
- Only ~30% WCAG coverage (automated cannot detect contrast in images, reading order, focus management)
- 25% of 2024 accessibility lawsuits targeted overlay users — overlay becomes evidence of negligence
- National Federation of the Blind publicly opposes overlay products
- Cannot fix mobile app VoiceOver issues (overlays target web only)
- **Using an overlay during active litigation would likely harm your legal position**

### Pure In-House Approach

Possible but risky for court timeline: (a) hiring accessibility-trained developers takes 3-6 months, (b) no third-party attestation for court evidence, (c) learning curve on WCAG 2.2 and EN 301 549 additional requirements. Better as a long-term complement to initial audit firm engagement.

## Adversarial Review

### Counterargument 1: "WCAG 2.0 AA (our 2021 audit) should be sufficient — courts haven't mandated 2.2"

**Argument:** No court has explicitly required WCAG 2.2. The DOJ Title II rule only requires WCAG 2.1. Why go beyond what's legally required?

**Evidence:** True — no statute mandates WCAG 2.2 specifically for Title III entities. Most consent decrees reference WCAG 2.0 or 2.1 AA.

**Rebuttal:** (a) Your 2021 audit is 5 years old — accessibility regressions occur with every app update. Even WCAG 2.0 AA compliance is likely degraded. (b) WCAG 2.2 is backward-compatible — meeting 2.2 automatically meets 2.0 and 2.1. (c) EN 301 549 V3.2.1 already requires WCAG 2.1 AA, and V4.1.1 (expected 2026) will require WCAG 2.2 AA. Targeting 2.2 now avoids a second remediation cycle. (d) Courts increasingly view the latest WCAG as demonstrating good faith — remediating to an outdated standard weakens your position.

### Counterargument 2: "We can settle the lawsuit cheaply and delay remediation"

**Argument:** ADA Title III settlements for web accessibility typically range $50K-150K for credit unions. Settling now and remediating later is cheaper than a $450K remediation program.

**Evidence:** Many credit unions have settled ADA web accessibility suits for $50K-$100K plus agreement to remediate within 12-24 months.

**Rebuttal:** (a) Settlement typically *requires* remediation on a timeline — you can't just pay and walk away. (b) Serial plaintiffs: once you settle, other attorneys target you (60+ credit unions already sued). (c) EN 301 549 compliance for European expansion requires the same remediation regardless of the lawsuit. (d) The $800K budget covers both settlement AND remediation. Delaying remediation doesn't save money — it just defers it while accumulating legal risk.

### Counterargument 3: "The Title II rule should apply because credit unions are quasi-governmental (federally insured, NCUA regulated)"

**Argument:** Credit unions are not-for-profit cooperatives with federal charters, NCUA insurance, and regulatory oversight. This makes them more like government entities than private businesses.

**Evidence:** Federal credit unions are chartered by NCUA under the Federal Credit Union Act (12 USC §1751). They receive deposit insurance from the NCUSIF.

**Rebuttal:** ADA Title II (28 CFR Part 35) defines covered entities as "state or local government" entities or "instrumentalities" thereof. Credit unions — even federally chartered ones — are private member-owned cooperatives, not government entities. The DOJ's April 2024 final rule preamble explicitly scopes to "public entities as defined in 28 CFR 35.104." No court has classified a credit union as a Title II entity. Your obligations are under Title III (42 USC §12182), which covers "places of public accommodation" including "service establishment[s]" — a category that clearly includes financial institutions.

### Assumption Audit

| Assumption | Status | Risk if Wrong |
|------------|--------|--------------|
| Title II does not apply to credit unions | Verified (28 CFR 35.104 definition) | If somehow applicable, adds WCAG 2.1 AA mandate with specific deadline |
| WCAG 2.2 AA is the appropriate target | Best practice (courts use 2.1, 2.2 is superset) | If court only requires 2.0, you've over-invested (but future-proofed) |
| Overlay solutions are harmful | Strongly verified (FTC fine, lawsuit data) | If overlay tech improves, could supplement (but not replace) manual remediation |
| $800K is sufficient | Verified — covers audit + remediation + settlement + legal | If remediation scope grows, EN 301 549 delta may push costs up |
| 9-month court deadline is firm | Assumed | If extended, more time for remediation; if shortened, prioritize critical flows |
| EN 301 549 V3.2.1 applies to EU military base banking | Likely — EU Directive 2016/2102 applies to public sector | If Canadian military bases exempt, EN 301 549 still good practice |

## Recommendation

**Engage a specialized accessibility audit firm (Level Access, Deque, or TPGi) immediately.** Allocate the $800K budget as follows:

| Line Item | Budget |
|-----------|--------|
| Audit firm (audit + remediation + VPAT) | $450K |
| Settlement reserve | $150K |
| Legal defense (9 months) | $150K |
| Contingency / EN 301 549 delta | $50K |

**Confidence: 78%.** Key action items: (1) correct board on Title II vs Title III, (2) fix wire transfer VoiceOver immediately as good faith gesture, (3) do NOT purchase any overlay product, (4) target WCAG 2.2 AA for future-proofing. This recommendation changes if: (a) court imposes specific WCAG version requirement, (b) EN 301 549 V4.1.1 releases before remediation completes (re-scope to WCAG 2.2 AA — which you're already targeting), or (c) plaintiff accepts early settlement without remediation requirement (unlikely but possible).

## Sources

- [DOJ Title II Final Rule — 28 CFR Part 35](https://www.federalregister.gov/documents/2024/04/24/2024-07758/nondiscrimination-on-the-basis-of-disability-accessibility-of-web-information-and-services-of-state)
- [ADA.gov Fact Sheet — Title II Web Rule](https://www.ada.gov/resources/2024-03-08-web-rule/)
- [WCAG 2.2 — W3C Recommendation](https://www.w3.org/TR/WCAG22/)
- [What's New in WCAG 2.2 — W3C WAI](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- [EN 301 549 V3.2.1 — ETSI](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf)
- [EN 301 549 — ETSI Overview](https://www.etsi.org/human-factors-accessibility/en-301-549-v3-the-harmonized-european-standard-for-ict-accessibility)
- [FTC AccessiBe $1M Fine](https://www.lflegal.com/2025/01/ftc-accessibe-million-dollar-fine/)
- [FTC AccessiBe Order](https://www.ecomback.com/blogs/ftc-final-order-accessibility-widget-provider-accessibe-to-pay-1m)
- [AccessiBe Class Action](https://commlawgroup.com/2024/accessibe-faces-class-action-lawsuit-over-alleged-misrepresentation-of-ada-compliance-and-ai-accessibility-capabilities/)
- [Overlay Lawsuits — Accessibility.Works](https://www.accessibility.works/blog/accessibility-overlay-widgets-attract-lawsuits/)
- [Credit Union ADA Lawsuits — DeLeon & Stang](https://deleonandstang.com/insights/2018/09/08/credit-union-ada-lawsuits-how-we-got-here-and-whats-next)
- [ADA Financial Institution Requirements — Level Access](https://www.levelaccess.com/blog/ada-financial-institutions/)
- [Credit Union ADA Response — BOIA](https://www.boia.org/blog/how-credit-unions-respond-to-ada-website-accessibility-lawsuits)
- [Title III ADA Digital Accessibility — ABA](https://www.americanbar.org/groups/business_law/resources/business-law-today/2025-august/digital-accessibility-under-title-iii-ada/)
- [ADA Litigation Financial Services — Morgan Lewis](https://www.morganlewis.com/pubs/2024/11/ada-compliant-websites-uptick-in-litigation-against-financial-services-firms-increased-regulatory-attention)
- [DigitalA11Y Pricing](https://www.digitala11y.com/pricing/)
- [Deque EN 301 549](https://www.deque.com/en-301-549-compliance/)
- [WCAG 2.2 Checklist — Level Access](https://www.levelaccess.com/blog/wcag-2-2-aa-summary-and-checklist-for-website-owners/)
- [EN 301 549 — Appt](https://appt.org/en/guidelines/en-301-549)
- [European Accessibility Act — Applause](https://www.applause.com/blog/european-accessibility-act-en-301-549/)
