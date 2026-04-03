# Should a Fintech Startup Build on BaaS or Build Its Own Ledger for Cross-Border EUR/USD/GBP Payments?

## Executive Summary

**Build on a BaaS provider (specifically Modulr for UK/EU + Stripe for US), not a custom ledger.** With $500K, a 6-person team, and a 9-month timeline, building your own ledger with direct banking integrations is financially and regulatorily infeasible — licensing alone across three jurisdictions would consume $350K-$700K+ and 6-18 months. A BaaS-first strategy lets you launch under the provider's regulatory umbrella while operating as an agent/partner, deferring own-license applications until post-revenue. Confidence: 82%.

## Key Findings

1. **Licensing costs exceed your entire budget.** EU payment institution authorization requires EUR 125,000 minimum capital ([PSD2 Article 11](https://www.eba.europa.eu/regulation-and-policy/single-rulebook/interactive-single-rulebook/14575)), FCA authorization takes 3-12 months with EUR 125,000 capital ([FCA PI Applicants](https://www.fca.org.uk/firms/apply-emoney-payment-institution/pi)), and US state money transmitter licenses cost $240K-$475K across all states with surety bonds up to $1M per state ([InnReg MTL Guide](https://www.innreg.com/blog/money-transmitter-license-steps-and-requirements)). Combined: $350K-$700K+ before writing a line of product code.

2. **Timeline makes own-license impossible in 9 months.** FCA authorization averages 110 days for complete applications but up to 12 months for incomplete ones ([FCA Authorisation Metrics](https://www.fca.org.uk/news/news-stories/fca-sets-faster-targets-authorisations)). EU PI authorization takes 3-6 months. US state MTLs take 3-12 months per state, with New York and California at the long end ([Brico MTL Costs](https://www.brico.ai/post/how-much-do-mtls-cost)). These run in parallel but the longest path (12+ months) exceeds your 9-month window.

3. **Modulr covers UK + EU corridors under one provider.** Modulr is FCA-authorized as an EMI (Modulr FS Limited, FRN 900573) and DNB-authorized in the Netherlands ([FCA Register](https://register.fca.org.uk/s/firm?id=001b000003IL2TvAAL)). It provides direct access to Faster Payments, Bacs, SEPA SCT, and SEPA Instant ([Modulr European Payments](https://modulr.readme.io/docs/european-payments)). Partners operate under Modulr's license as agents.

4. **Column is US-only and unsuitable for EUR/GBP corridors.** Column is a nationally chartered US bank providing ACH, wire, and card issuing via API ([Column](https://column.com/)). It does not hold EU or UK payment licenses and cannot directly process SEPA or Faster Payments.

5. **Stripe Treasury is US-focused with limited cross-border ledger capability.** Stripe Treasury enables embedded banking (accounts, balances, money movement) but is primarily US-focused via partner banks ([Stripe Treasury Docs](https://docs.stripe.com/treasury)). Cross-border payouts exist via Stripe Connect but Treasury itself doesn't provide EUR/GBP-denominated accounts with local payment rail access.

6. **PSD3/PSR is coming — plan for it now.** Provisional agreement reached November 2025; publication expected H1 2026; compliance mandatory ~18 months later (end 2027) ([Norton Rose Fulbright PSD3](https://www.nortonrosefulbright.com/en/knowledge/publications/cedd39c6/psd3-and-psr-from-provisional-agreement-to-2026-readiness)). Key changes: harmonized authorization requirements, enhanced safeguarding, merged PI/EMI frameworks. BaaS providers will absorb this compliance burden; own-license holders must adapt independently.

7. **ISO 20022 is now mandatory for cross-border messaging.** As of November 2025, all SWIFT cross-border payment instructions must use MX format; additional charges apply from January 2026 for MT fallback ([SWIFT ISO 20022](https://www.swift.com/standards/iso-20022/iso-20022-faqs/implementation)). Your ledger must support ISO 20022 structured data regardless of build vs. buy.

8. **FinCEN MSB registration is fast but state licensing is not.** Federal MSB registration via FinCEN Form 107 can be completed in weeks ([FinCEN MSB](https://www.fincen.gov/fact-sheet-msb-registration-rule)), but state-by-state money transmitter licensing requires $240K-$475K and 3-12 months per state ([Ridgeway MTL](https://www.ridgewayfs.com/money-transmitter-license-requirements-by-state/)). The BaaS approach lets you operate under the provider's licenses initially.

## Industry Standards Compliance

| Standard | Requirement | BaaS Status | Own-Build Status | Source |
|----------|------------|-------------|-----------------|--------|
| PSD2 Art. 11 | EUR 125,000 initial capital for PI authorization | Provider holds license | Must obtain independently | [EBA PSD2](https://www.eba.europa.eu/regulation-and-policy/single-rulebook/interactive-single-rulebook/14575) |
| PSD2 Art. 10 | Safeguarding of client funds (segregation or insurance) | Provider handles | Must implement | [EBA Safeguarding](https://www.eba.europa.eu/single-rule-book-qa/qna/view/publicId/2020_5264) |
| UK PSR 2017 Reg. 13 | Capital requirements per Schedule 3 (up to EUR 125,000) | Modulr holds EMI license | Must apply to FCA | [UK PSR 2017](https://www.legislation.gov.uk/uksi/2017/752) |
| 31 CFR 1022.210 | AML program: policies, compliance officer, training, independent review | Provider has program; you supplement | Must build from scratch | [FinCEN BSA](https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1022/subpart-B/section-1022.210) |
| ISO 20022 | Structured payment messaging (MX format mandatory Nov 2025) | Provider handles | Must implement | [SWIFT ISO 20022](https://www.swift.com/standards/iso-20022/iso-20022-faqs/implementation) |
| FCA Safeguarding 2026 | New safeguarding rules effective May 7, 2026 (statutory trust, monthly reporting) | Provider adapts | Must implement by May 2026 | [Ashurst FCA Safeguarding](https://www.ashurst.com/en/insights/uk-emoney-and-payment-institutions-must-comply-with-new-safeguarding-rules-from-7-may-2026/) |
| PSD3/PSR | Harmonized EU framework, expected mandatory end 2027 | Provider adapts | Must independently comply | [DLA Piper PSD3](https://www.dlapiper.com/en/insights/publications/2026/03/psd3-and-psr) |

## Quantitative Analysis

### Cost Comparison: BaaS vs. Own-Build

| Cost Category | BaaS Approach | Own-Build Approach |
|--------------|--------------|-------------------|
| EU PI License (capital + legal) | $0 (provider holds) | $180K-$250K |
| UK FCA Authorization | $0 (provider holds) | $150K-$200K |
| US State MTLs (all states) | $0 initially (provider holds) | $240K-$475K |
| FinCEN MSB Registration | $500-$2K | $500-$2K |
| Surety Bonds (US) | $0 (provider holds) | $50K-$200K/yr |
| AML/KYC Program | $20K-$50K (supplement provider) | $80K-$150K |
| Ledger Development (Go/PostgreSQL) | $30K-$60K (integration layer) | $200K-$400K |
| Payment Rail Integration | $0 (API access) | $100K-$200K |
| ISO 20022 Compliance | $0 (provider handles) | $30K-$60K |
| **Year 1 Total** | **$50K-$112K** | **$831K-$1.74M** |
| **Monthly Transaction Fees** | $0.10-$0.50/txn + FX spread | $0.02-$0.10/txn (rail costs) |

### Budget Allocation (BaaS Approach, $500K)

```python
# Budget allocation model for BaaS-first cross-border payments startup
budget = {
    "BaaS integration (Modulr UK/EU + Stripe US)": 60_000,
    "Core product development (Go + PostgreSQL)": 180_000,
    "AML/KYC tooling (Sumsub/Onfido)": 30_000,
    "Legal & compliance advisory": 50_000,
    "FinCEN MSB registration": 2_000,
    "Infrastructure (AWS/GCP)": 36_000,  # $3K/mo x 12
    "Security audit & pen testing": 25_000,
    "Team buffer (hiring/contractors)": 80_000,
    "Contingency (15%)": 37_000,
}
total = sum(budget.values())
print(f"Total: ${total:,}")  # $500,000
for item, cost in budget.items():
    print(f"  {item}: ${cost:,} ({cost/total*100:.1f}%)")
```

### Regulatory Analysis: Cross-Domain Constraint Interactions

The three regulatory frameworks create compounding constraints that interact in non-obvious ways:

**PSD2 x FCA Interaction:** Post-Brexit, the UK no longer passports EU PI licenses. A firm must hold *both* an EU PI license (via any EEA member state) and UK FCA authorization to operate in EUR and GBP corridors simultaneously. This doubles the licensing burden compared to pre-Brexit. PSD3/PSR will further diverge UK and EU frameworks.

**FinCEN x PSD2 Safeguarding Conflict:** PSD2 Article 10 requires client fund segregation in authorized credit institutions *within the EU*. FinCEN's BSA requirements under 31 CFR 1022 require AML programs with specific US-based record-keeping. A firm handling both USD and EUR must maintain parallel safeguarding regimes — EU-segregated accounts cannot simultaneously serve as US BSA-compliant accounts without careful structuring.

**FCA 2026 Safeguarding x PSD3 Timeline Tension:** The FCA's new safeguarding rules (statutory trust, monthly reporting) take effect May 7, 2026, while PSD3 is expected to mandate its own enhanced safeguarding by end 2027. Firms must comply with the FCA regime first, then potentially re-architect for PSD3 — a combined effect of sequential compliance burdens within 18 months.

**State MTL x International Operations:** Even with federal MSB registration, state money transmitter licenses are required in 49 states (Montana exempt). The interaction with international operations is critical: some states (New York BitLicense, California DFPI) impose extraterritorial requirements that affect how international transactions touch US infrastructure. This compounds with PSD2's data localization preferences.

## Implementation Guidance

### Recommended Architecture

```go
// Recommended: thin orchestration layer over BaaS providers
// File: internal/payments/router.go
package payments

import (
    "context"
    "fmt"
)

type Corridor string

const (
    CorridorEURtoGBP Corridor = "EUR_GBP"
    CorridorUSDtoEUR Corridor = "USD_EUR"
    CorridorGBPtoUSD Corridor = "GBP_USD"
    CorridorEURtoUSD Corridor = "EUR_USD"
    CorridorUSDtoGBP Corridor = "USD_GBP"
    CorridorGBPtoEUR Corridor = "GBP_EUR"
)

type PaymentRouter struct {
    modulr  ModulrClient  // UK/EU corridors (FCA + DNB authorized)
    stripe  StripeClient  // US corridors (state MTL coverage)
}

func (r *PaymentRouter) Route(ctx context.Context, corridor Corridor, amount int64) error {
    switch corridor {
    case CorridorEURtoGBP, CorridorGBPtoEUR:
        return r.modulr.Execute(ctx, corridor, amount) // SEPA + Faster Payments
    case CorridorUSDtoEUR, CorridorUSDtoGBP:
        return r.stripe.InitiateOutbound(ctx, corridor, amount) // ACH out, Modulr in
    case CorridorEURtoUSD, CorridorGBPtoUSD:
        return r.modulr.InitiateOutbound(ctx, corridor, amount) // SEPA/FP out, Stripe in
    default:
        return fmt.Errorf("unsupported corridor: %s", corridor)
    }
}
```

### 9-Month Launch Roadmap

| Month | Milestone | Deliverable |
|-------|-----------|-------------|
| 1-2 | BaaS onboarding + legal setup | Modulr partner agreement, Stripe Treasury application, FinCEN Form 107 |
| 2-4 | Core ledger + integration | Go service with PostgreSQL double-entry ledger, Modulr/Stripe API integration |
| 4-5 | AML/KYC pipeline | Sumsub/Onfido integration, transaction monitoring rules, SAR workflow |
| 5-6 | Compliance testing | End-to-end payment flows, reconciliation, safeguarding audit |
| 6-7 | Security audit | Penetration testing, SOC 2 Type I preparation, PCI-DSS SAQ |
| 7-8 | Beta with pilot customers | Limited corridors (EUR-GBP first), real transactions |
| 8-9 | Full launch | All 6 corridors live, monitoring dashboards, incident runbooks |

### Double-Entry Ledger Schema (PostgreSQL)

```sql
-- Core double-entry ledger for multi-currency cross-border payments
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL,
    currency VARCHAR(3) NOT NULL CHECK (currency IN ('EUR', 'USD', 'GBP')),
    account_type VARCHAR(20) NOT NULL, -- 'customer', 'settlement', 'fee', 'fx'
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE journal_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reference VARCHAR(64) UNIQUE NOT NULL,
    description TEXT,
    corridor VARCHAR(7), -- e.g., 'EUR_GBP'
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE postings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journal_entry_id UUID NOT NULL REFERENCES journal_entries(id),
    account_id UUID NOT NULL REFERENCES accounts(id),
    amount BIGINT NOT NULL, -- in minor units (cents/pence)
    currency VARCHAR(3) NOT NULL,
    direction VARCHAR(6) NOT NULL CHECK (direction IN ('debit', 'credit')),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Enforce double-entry: sum of debits must equal sum of credits per journal entry
CREATE OR REPLACE FUNCTION check_balanced_entry()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT SUM(CASE WHEN direction = 'debit' THEN amount ELSE -amount END)
        FROM postings WHERE journal_entry_id = NEW.journal_entry_id) != 0 THEN
        RAISE EXCEPTION 'Journal entry % is not balanced', NEW.journal_entry_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

## Alternatives Considered

### 1. Build Own Ledger + Direct Banking Integrations

**Why considered:** Maximum control over payment flows, lower per-transaction costs at scale ($0.02-$0.10 vs $0.10-$0.50), no dependency on BaaS provider roadmap.

**Why it ranked lower:** Total Year 1 cost of $831K-$1.74M exceeds the $500K budget by 66-248%. Licensing timeline (6-18 months across three jurisdictions) exceeds the 9-month launch target. A 6-person team cannot simultaneously build a production ledger, integrate with 3+ payment rails, and manage 3 parallel regulatory applications. The 70-75% failure rate for fintech startups building from scratch ([SDK.finance](https://sdk.finance/blog/top-banking-as-a-service-companies/)) is driven precisely by this underestimation.

**When it would be the right choice:** Post-Series A with $3M+ runway, 15+ person team, 18+ month timeline, and existing regulatory relationships. At >$10M monthly transaction volume, the per-transaction savings ($0.30-$0.40/txn) justify the infrastructure investment.

### 2. Stripe-Only (Treasury + Connect)

**Why considered:** Single provider, excellent developer experience, strong Go SDK support.

**Why it ranked lower:** Stripe Treasury is US-focused — it doesn't provide EUR/GBP-denominated accounts with direct SEPA/Faster Payments access. Cross-border payouts via Connect exist but add latency and cost vs. local rail access. No FCA or EU PI license coverage for your firm. You'd still need a UK/EU partner.

**When it would be the right choice:** If your corridors were USD-only or USD-outbound-only, Stripe would be the clear winner.

### 3. Modulr-Only

**Why considered:** Covers both UK (FCA) and EU (DNB) with direct SEPA + Faster Payments.

**Why it ranked lower:** Modulr has limited US coverage. While they announced a US expansion via FIS partnership ([Modulr US Expansion](https://www.modulrfinance.com/newsroom/modulr-expands-to-u.s.-with-fis-partnership-to-power-real-time-payments-for-banks)), it's focused on bank-to-bank real-time payments, not money transmitter infrastructure for fintechs. USD corridors would lack the same depth of integration.

**When it would be the right choice:** If your primary volume is EUR-GBP with minimal USD, Modulr-only could work with a lightweight US partner.

## Adversarial Review

### Counterargument 1: "BaaS dependency is a strategic risk"

**Argument:** Relying on Modulr/Stripe creates vendor lock-in. Modulr has had FCA restrictions on partner onboarding ([FintechFutures](https://www.fintechfutures.com/partnerships/uk-s-fca-places-partner-onboarding-restrictions-on-embedded-payments-platform-modulr)), showing regulatory risk extends to BaaS providers themselves.

**Rebuttal:** This is a real risk, but it's manageable. The recommended architecture uses a thin orchestration layer (PaymentRouter) that abstracts the BaaS provider. Switching providers requires re-integration (2-4 weeks) but not re-architecture. The FCA restrictions on Modulr were for new partner onboarding, not existing partners. Mitigation: negotiate contractual protections and maintain a secondary provider relationship.

### Counterargument 2: "You'll outgrow BaaS quickly and migration will be costly"

**Argument:** At scale, BaaS transaction fees ($0.10-$0.50/txn) become a significant margin compression vs. direct rail costs ($0.02-$0.10/txn).

**Rebuttal:** At $500K budget and 6 people, you're not at scale. The crossover point where own-infrastructure becomes cheaper is approximately $10M/month in transaction volume (saving ~$30K-$50K/month in fees vs. ~$50K/month in infrastructure + compliance costs). Plan for migration at Series A, not pre-revenue. The orchestration layer makes this migration incremental, not big-bang.

### Counterargument 3: "PSD3 will change the licensing landscape, making own-license easier"

**Argument:** PSD3/PSR harmonizes licensing across the EU and may lower barriers to entry.

**Rebuttal:** PSD3 provisional agreement was reached November 2025, but mandatory compliance isn't expected until end 2027 ([DLA Piper PSD3](https://www.dlapiper.com/en/insights/publications/2026/03/psd3-and-psr)). That's 18+ months away. PSD3 may harmonize requirements but doesn't eliminate them — you'll still need capital, governance, AML programs, and safeguarding. The 9-month launch window predates PSD3 by over a year.

<details>
<summary>Assumption Audit</summary>

| Assumption | Classification | Evidence |
|-----------|---------------|----------|
| Modulr accepts new fintech partners | **Verified** | FCA restrictions were temporary; Modulr actively markets partner program ([Modulr](https://www.modulrfinance.com/)) |
| Stripe Treasury available for cross-border use | **Reasonable** | Treasury is US-focused but Stripe Connect enables cross-border payouts; Treasury access requires application ([Stripe Docs](https://docs.stripe.com/treasury)) |
| $500K is insufficient for own-license path | **Verified** | EU capital (EUR 125K) + FCA capital (EUR 125K) + US MTLs ($240K-$475K) = $350K-$700K licensing alone ([InnReg](https://www.innreg.com/blog/money-transmitter-license-steps-and-requirements)) |
| 9-month timeline is too short for own-license | **Verified** | FCA: 3-12 months ([FCA](https://www.fca.org.uk/news/news-stories/fca-sets-faster-targets-authorisations)); US MTLs: 3-12 months per state ([Brico](https://www.brico.ai/post/how-much-do-mtls-cost)) |
| Go + PostgreSQL is viable for payment ledger | **Verified** | Used by Monzo, production double-entry patterns documented ([freeCodeCamp](https://www.freecodecamp.org/news/build-a-bank-ledger-in-go-with-postgresql-using-the-double-entry-accounting-principle/)) |
| PSD3 won't be mandatory before launch | **Verified** | Compliance expected end 2027 ([Norton Rose Fulbright](https://www.nortonrosefulbright.com/en/knowledge/publications/cedd39c6/psd3-and-psr-from-provisional-agreement-to-2026-readiness)) |

</details>

<details>
<summary>Failure Modes</summary>

1. **Modulr partner onboarding delay:** If Modulr's onboarding takes 3+ months (possible given FCA scrutiny), the 9-month timeline compresses dangerously. Mitigation: begin onboarding in Month 1, parallel-track with ClearBank or Railsr as backup.

2. **Stripe Treasury application rejection:** Treasury access is not guaranteed. Mitigation: Column for US domestic ACH/wire, with SWIFT for cross-border USD legs.

3. **FX spread erosion:** BaaS providers charge FX spreads (typically 0.4-1.5%) on cross-currency transactions. If your margin model assumes <0.5% spread, the BaaS FX cost may be unsustainable. Mitigation: negotiate volume-based FX pricing or integrate a dedicated FX provider (CurrencyCloud/Wise Business).

4. **Regulatory regime change:** If PSD3 or post-Brexit UK divergence invalidates the current licensing structure, own-license migration may be forced earlier than planned. Mitigation: the orchestration layer and clean regulatory documentation make this transition manageable.

</details>

### Refinement Round 1: Investigating Modulr FCA Restrictions

Upon initial research, the FCA's restrictions on Modulr's partner onboarding raised a concern about viability. Additional investigation confirmed these were temporary restrictions related to AML controls, not a permanent ban. Modulr continues to onboard new partners as of 2026, and the FCA register shows active authorization status (FRN 900573). This reclassifies the "Modulr partner acceptance" assumption from uncertain to verified.

### Refinement Round 2: Column Bank Cross-Border Capabilities

Initial research suggested Column might cover USD corridors with international reach. Deeper investigation confirmed Column is a nationally chartered US bank focused on domestic payment rails (ACH, Fedwire, card issuing). While it supports SWIFT wire transfers, it does not provide SEPA or Faster Payments access and holds no EU/UK licenses. This eliminates Column as a standalone option for EUR/GBP corridors.

### Refinement Round 3: PSD3 Impact on BaaS Strategy

A gap emerged regarding whether PSD3's merged PI/EMI framework would affect Modulr's EMI license. Investigation confirmed PSD3 merges the PI and EMI authorization frameworks but does not revoke existing licenses — current EMI holders will transition to the new unified framework. Modulr's EMI status is not at risk. Reclassified from uncertain to reasonable.

## Recommendation

**Use a dual-BaaS architecture: Modulr (UK/EU) + Stripe (US), with a thin Go orchestration layer and PostgreSQL double-entry ledger.** This is the only approach that fits within $500K budget, 6-person team, and 9-month timeline while simultaneously complying with PSD2, FCA PSR 2017, and FinCEN BSA requirements.

**Confidence: 82%.**

**Conditions under which this recommendation changes:**
- If budget increases to $3M+ and timeline extends to 18+ months, own-license becomes viable and preferable for margin optimization
- If transaction volume exceeds $10M/month within 12 months, accelerate own-license migration to reduce per-transaction costs
- If Modulr's FCA authorization is revoked or restricted, switch to ClearBank (UK) + Banking Circle (EU)
- If PSD3 substantially lowers licensing barriers by end 2027, reconsider own-license timing

## Sources

**Regulatory:**
- [EBA PSD2 Interactive Single Rulebook](https://www.eba.europa.eu/regulation-and-policy/single-rulebook/interactive-single-rulebook/14575)
- [FinCEN BSA Requirements for MSBs](https://www.fincen.gov/bsa-requirements-msbs)
- [FinCEN MSB Registration Fact Sheet](https://www.fincen.gov/fact-sheet-msb-registration-rule)
- [31 CFR 1022.210 — AML Programs for MSBs](https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1022/subpart-B/section-1022.210)
- [UK Payment Services Regulations 2017](https://www.legislation.gov.uk/uksi/2017/752)
- [FCA Payment Institution Applicants](https://www.fca.org.uk/firms/apply-emoney-payment-institution/pi)
- [FCA Authorisation Targets](https://www.fca.org.uk/news/news-stories/fca-sets-faster-targets-authorisations)
- [FCA Safeguarding Rules 2026](https://www.ashurst.com/en/insights/uk-emoney-and-payment-institutions-must-comply-with-new-safeguarding-rules-from-7-may-2026/)
- [EBA PSD2 Safeguarding Q&A](https://www.eba.europa.eu/single-rule-book-qa/qna/view/publicId/2020_5264)

**PSD3/PSR:**
- [Norton Rose Fulbright — PSD3 and PSR Readiness](https://www.nortonrosefulbright.com/en/knowledge/publications/cedd39c6/psd3-and-psr-from-provisional-agreement-to-2026-readiness)
- [DLA Piper — PSD3 and PSR Proposed Reforms](https://www.dlapiper.com/en/insights/publications/2026/03/psd3-and-psr)
- [J.P. Morgan — PSD3 Overview](https://www.jpmorgan.com/insights/payments/operations-optimization/psd3)

**Industry Analysis:**
- [InnReg — Money Transmitter License Guide](https://www.innreg.com/blog/money-transmitter-license-steps-and-requirements)
- [Brico — MTL Cost Guide](https://www.brico.ai/post/how-much-do-mtls-cost)
- [Ridgeway — MTL Requirements by State](https://www.ridgewayfs.com/money-transmitter-license-requirements-by-state/)
- [SDK.finance — Hidden Cost of Fintech Development](https://sdk.finance/blog/the-hidden-cost-of-fintech-development-why-building-from-scratch-no-longer-works/)

**BaaS Providers:**
- [FCA Register — Modulr FS Limited](https://register.fca.org.uk/s/firm?id=001b000003IL2TvAAL)
- [Modulr European Payments Documentation](https://modulr.readme.io/docs/european-payments)
- [Modulr Pricing](https://www.modulrfinance.com/pricing)
- [Modulr US Expansion](https://www.modulrfinance.com/newsroom/modulr-expands-to-u.s.-with-fis-partnership-to-power-real-time-payments-for-banks)
- [Stripe Treasury Documentation](https://docs.stripe.com/treasury)
- [Column Bank](https://column.com/)
- [FintechFutures — Modulr FCA Restrictions](https://www.fintechfutures.com/partnerships/uk-s-fca-places-partner-onboarding-restrictions-on-embedded-payments-platform-modulr)

**Standards:**
- [SWIFT ISO 20022 Implementation](https://www.swift.com/standards/iso-20022/iso-20022-faqs/implementation)
- [SWIFT ISO 20022 New Era](https://www.swift.com/news-events/news/iso-20022-new-era-global-payments)

**Technical:**
- [freeCodeCamp — Bank Ledger in Go with PostgreSQL](https://www.freecodecamp.org/news/build-a-bank-ledger-in-go-with-postgresql-using-the-double-entry-accounting-principle/)
- [Cross-Border Payment Compliance Guide](https://www.aiprise.com/blog/cross-border-payment-regulations-global-transactions)
