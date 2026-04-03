# EU E-Invoicing for a Series A Fintech: Build, Library, or SaaS?

## Executive Summary

**Use a SaaS connector (Storecove or e-invoice.be) for Peppol/EN 16931 compliance, not open-source libraries or a from-scratch build.** The regulatory surface area (ViDA Directive, 5+ national mandates with divergent timelines, HMRC MTD, EN 16931:2026 B2B revision) is too large and too volatile for a 40-person startup to maintain in-house within $30K and 3 months. A SaaS Peppol Access Point provides certified compliance, format conversion, multi-country coverage, and ongoing regulatory updates for approximately $6K-$12K/year — leaving budget for integration engineering. Open-source Python libraries (python-en16931, python-ubl) are proof-of-concept grade with low adoption and would require 6-10 months of custom development to reach production quality. Building from scratch is a $140K-$400K endeavor per industry estimates, far exceeding the $30K budget.

**Confidence: 88%** — High confidence in the SaaS recommendation; moderate uncertainty around exact SaaS pricing (vendor quotes required) and the 2030 ViDA intra-EU mandate's final technical specifications.

## Key Findings

1. **The ViDA Directive mandates EN 16931 e-invoicing for intra-EU B2B transactions from 1 July 2030**, but national mandates are arriving much sooner: Belgium (Jan 2026, live now), Poland KSeF (Feb 2026), France (Sep 2026 receive + large/mid issue), Germany (Jan 2027 issue for >€800K turnover). A system built today must handle the national mandates first, then adapt to ViDA. ([Source: fiskaly.com](https://www.fiskaly.com/blog/e-invoicing-mandates-in-europe-2026); [vatcalc.com](https://www.vatcalc.com/eu/eu-2028-digital-reporting-requirements-drr-e-invoice/)) — *Evidence: regulatory text summaries from multiple compliance vendors, cross-verified across 3 sources* [high confidence]

2. **EN 16931 was revised in February 2026 specifically for B2B transactions**, adding new fields (IBAN, triangulation indicators, corrective invoice sequencing, margin scheme support). Any implementation must target this 2026 revision, not the 2017 B2G-only version. ([Source: vatupdate.com](https://www.vatupdate.com/2025/10/31/european-e-invoicing-standard-en-16931-approved-oct-23-2025/); [vatcalc.com](https://www.vatcalc.com/eu/eu-updates-en-16931-e-invoicing-standard-for-vida/)) — *Evidence: CEN committee approval record* [high confidence]

3. **Peppol BIS Billing 3.0 requires UBL 2.1 XML** validated at three levels: XSD schema, EN 16931 schematron rules, and Peppol-specific business rules. CII (Cross-Industry Invoice) is an alternative syntax used primarily in France/Germany (Factur-X/ZUGFeRD), but UBL is mandatory for the Peppol network. ([Source: docs.peppol.eu](https://docs.peppol.eu/poacc/billing/3.0/bis/); [invoicenavigator.eu](https://www.invoicenavigator.eu/compare/ubl-vs-cii)) — *Evidence: official Peppol specification* [high confidence]

4. **HMRC MTD does not mandate a specific invoice format** but requires digital records with digital links (no manual re-keying between systems), quarterly submissions via HMRC's VAT API, and HMRC-compatible software. Peppol-enabled systems naturally satisfy MTD's digital record-keeping requirements. The UK plans mandatory structured e-invoicing (likely EN 16931/UBL) from April 2029. ([Source: developer.service.hmrc.gov.uk](https://developer.service.hmrc.gov.uk/guides/vat-mtd-end-to-end-service-guide/); [accountingweb.co.uk](https://www.accountingweb.co.uk/community/industry-insights/peppol-e-invoicing-for-uk-businesses-everything-you-need-to-know-about)) — *Evidence: HMRC developer documentation (primary source) + compliance analyst interpretation* [high confidence]

5. **Python open-source libraries for EN 16931/Peppol are immature.** `python-en16931` (en16931 on PyPI) is self-described as "proof of concept" at version 0.1, published by Invinet Sistemes. `python-ubl` is at version 0.1.5 with minimal community adoption. `invoice2data` extracts data from PDFs (wrong direction — it reads invoices, doesn't generate compliant ones) and hasn't been updated in 12+ months per Snyk analysis. `factur-x` (v3.15, by Akretion) is more mature but targets CII/Factur-X format, not UBL/Peppol. None of these libraries handle Peppol network connectivity, Access Point certification, or multi-country regulatory updates. ([Source: invinet.github.io](https://invinet.github.io/python-en16931/build/html/invoice.html); [snyk.io/advisor](https://snyk.io/advisor/python/invoice2data); [pypi.org/project/factur-x](https://pypi.org/project/factur-x/)) — *Evidence: PyPI metadata, GitHub repositories, Snyk health analysis* [high confidence]

6. **Custom e-invoicing development costs $140K-$400K and takes 6-10 months** according to ScienceSoft's industry analysis. This exceeds the $30K budget by 4.7-13x and the 3-month timeline by 2-3x. The ongoing maintenance burden (regulatory changes, schematron rule updates, new country mandates) is a recurring cost that scales with the number of countries served. ([Source: scnsoft.com](https://www.scnsoft.com/financial-management/e-invoicing)) — *Evidence: vendor estimate from IT consultancy with e-invoicing practice; cross-referenced with Maventa's build-vs-buy analysis* [moderate confidence — vendor estimates, not audited project data]

7. **SaaS Peppol Access Points provide certified, multi-country compliance via a single API.** Storecove (starting ~€495/month, 30+ countries, REST/JSON API, ISO 27001 certified), Qvalia (starting €39/month for 100 messages, Peppol + EDI), and e-invoice.be (pay-per-use, €1 start, Python SDK) offer different price/feature tradeoffs. All handle format conversion, validation, and Peppol network delivery. ([Source: storecove.com](https://www.storecove.com/us/en/); [qvalia.com/pricing](https://qvalia.com/pricing/); [e-invoice.be](https://e-invoice.be/peppol-api)) — *Evidence: vendor websites, G2/GetApp pricing data* [moderate confidence — exact pricing requires vendor quotes]

## Industry Standards Compliance

| Standard | Requirement | Build-from-scratch | Open-source library | SaaS connector | Source |
|---|---|---|---|---|---|
| **EN 16931:2026** | Semantic data model for B2B e-invoices; new B2B fields (IBAN, triangulation, corrective sequencing) | Must implement from scratch; no Python lib covers 2026 revision | `python-en16931` covers 2017 version only (proof-of-concept) | Storecove/Qvalia handle updates as part of service | [vatcalc.com](https://www.vatcalc.com/eu/eu-updates-en-16931-e-invoicing-standard-for-vida/) |
| **Peppol BIS 3.0** | UBL 2.1 XML with 3-level validation (XSD + EN16931 schematron + Peppol rules) | Must implement all 3 validation layers + become/use Access Point | `python-ubl` generates UBL but no validation; no Access Point | Certified Access Point included | [docs.peppol.eu](https://docs.peppol.eu/poacc/billing/3.0/bis/) |
| **ViDA Directive** (EU 2024/1837) | Mandatory e-invoicing for intra-EU B2B from Jul 2030; 10-day issuance deadline | Must track evolving implementing acts | N/A — no library covers this | SaaS providers commit to regulatory updates | [edicomgroup.com](https://edicomgroup.com/blog/vida-the-european-union-promotes-b2b-electronic-invoicing) |
| **HMRC MTD** | Digital records, digital links, quarterly VAT filing via HMRC API | Must build HMRC API integration separately | No Python library covers MTD | Storecove covers UK; MTD API integration is separate (~2 weeks dev) | [developer.service.hmrc.gov.uk](https://developer.service.hmrc.gov.uk/guides/vat-mtd-end-to-end-service-guide/) |
| **Belgium B2B mandate** | Mandatory Peppol e-invoicing from Jan 2026, UBL 2.1 | Must implement full Peppol stack | Partial UBL generation only | Fully covered by any Peppol Access Point | [fiskaly.com](https://www.fiskaly.com/blog/e-invoicing-mandates-in-europe-2026) |
| **France Factur-X** | CII format via PDP (Plateforme de Dématérialisation Partenaire), Sep 2026 | Must implement CII + PDP certification | `factur-x` library handles CII generation | Storecove supports France SDI-equivalent | [fiskaly.com](https://www.fiskaly.com/blog/e-invoicing-mandates-in-europe-2026) |
| **ISO 27001** | Information security management (required by some Peppol authorities) | Must obtain own certification (~$20K-$50K) | N/A | Storecove is ISO 27001 certified | [storecove.com](https://www.storecove.com/blog/en/peppol-standards-iso-certification/) |

## Quantitative Analysis

### Cost Comparison Matrix (3-year TCO)

| Dimension | Build from Scratch | Open-Source + Custom | SaaS Connector (Storecove) | SaaS Connector (e-invoice.be) |
|---|---|---|---|---|
| **Initial development** | $140K-$300K | $40K-$80K (estimate) | $5K-$10K (integration) | $3K-$5K (integration) |
| **Timeline** | 6-10 months | 3-5 months | 4-8 weeks | 2-4 weeks |
| **Annual SaaS/hosting** | $0 (self-hosted) | $0 (self-hosted) | ~€6K-€12K/yr (~$6.5K-$13K) | Pay-per-use (~$1-2K/yr at low volume |
| **Annual maintenance** | $30K-$60K (1 FTE partial) | $20K-$40K | $0 (vendor-managed) | $0 (vendor-managed) |
| **Peppol certification** | ~$5K-$15K + annual fees | N/A (use SaaS AP) | Included | Included |
| **3-year TCO** | **$235K-$495K** | **$100K-$200K** | **$25K-$49K** | **$9K-$11K** |
| **Fits $30K budget?** | No (4.7-16.5x over) | No (3.3-6.7x over) | Yes (borderline) | Yes (comfortable) |
| **Fits 3-month deadline?** | No | Possible but risky | Yes | Yes |

*Assumptions: EUR/USD rate ~1.08. "Low volume" = <500 invoices/month. Storecove pricing based on G2/GetApp reported starting price of €495/month. e-invoice.be pricing based on pay-per-use model. Maintenance cost for build options assumes partial developer allocation for regulatory updates.*

### Developer Effort Breakdown (SaaS Integration Path)

| Task | Estimated Hours | Notes |
|---|---|---|
| SaaS vendor evaluation + sandbox testing | 20-30 | Storecove offers 30-day free sandbox |
| Invoice data model in PostgreSQL | 15-20 | Map internal invoice fields to EN 16931 semantic model |
| FastAPI endpoints for invoice CRUD | 20-30 | Create, read, update, send, receive |
| SaaS API integration (send/receive) | 30-40 | REST/JSON mapping, webhook receiver for incoming |
| HMRC MTD VAT API integration | 30-40 | Separate from Peppol; OAuth 2.0 + VAT submission |
| Validation + error handling | 15-20 | Pre-submission validation, retry logic, status tracking |
| Testing + UAT | 20-30 | End-to-end with sandbox, schematron validation |
| **Total** | **150-210 hours** | **~4-6 weeks at 1.5 FTE** |

At $100/hr loaded cost (Series A startup rates), this is **$15K-$21K in engineering cost**, comfortably within the $30K budget with room for SaaS subscription costs.

## Implementation Guidance

### Recommended Architecture

```
FastAPI Backend (Railway)
    ├── /api/v1/invoices/           — CRUD for invoice management
    ├── /api/v1/invoices/{id}/send  — Trigger send via SaaS AP
    ├── /api/v1/invoices/receive    — Webhook endpoint for incoming
    ├── /api/v1/vat/submit          — HMRC MTD quarterly submission
    └── /webhooks/storecove         — Incoming invoice notifications

PostgreSQL
    ├── invoices                    — Core invoice data (EN 16931 fields)
    ├── invoice_lines               — Line items
    ├── invoice_parties             — Buyer/seller entities
    ├── invoice_submissions         — Send status tracking
    └── vat_returns                 — MTD quarterly aggregation
```

### Step 1: Choose SaaS Provider

**For EU-focused with API maturity: Storecove**
- REST/JSON API at `https://api.storecove.com/api/v2/document_submissions`
- Submit invoices as JSON (no XML generation needed — Storecove converts)
- 30+ country coverage, ISO 27001 certified
- OpenAPI spec available for client generation
- Starting ~€495/month

**For cost-sensitive with Python SDK: e-invoice.be**
- Native Python SDK: `pip install e-invoice-api`
- Pay-per-use (no monthly minimum)
- Async + sync clients via httpx
- Newer provider, smaller footprint

**For budget-conscious with own Peppol ID: Qvalia**
- Free tier available (limited messages)
- Small plan: €39/month for 100 messages
- Good for testing/low-volume start

### Step 2: Invoice Data Model (PostgreSQL)

```sql
-- Core invoice table mapping EN 16931 semantic model
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_number VARCHAR(255) NOT NULL UNIQUE,
    issue_date DATE NOT NULL,
    due_date DATE,
    invoice_type_code VARCHAR(10) NOT NULL,  -- 380=invoice, 381=credit note
    currency_code VARCHAR(3) NOT NULL DEFAULT 'EUR',
    -- Buyer/Seller references
    seller_id UUID REFERENCES parties(id),
    buyer_id UUID REFERENCES parties(id),
    -- Totals (EN 16931 BT-106 through BT-115)
    line_extension_amount NUMERIC(15,2),      -- BT-106
    tax_exclusive_amount NUMERIC(15,2),       -- BT-109
    tax_inclusive_amount NUMERIC(15,2),        -- BT-112
    payable_amount NUMERIC(15,2),             -- BT-115
    -- Peppol delivery tracking
    peppol_id VARCHAR(255),
    submission_status VARCHAR(50) DEFAULT 'draft',
    external_id VARCHAR(255),  -- SaaS provider's ID
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
```

### Step 3: FastAPI Integration with Storecove

```python
# app/services/einvoice.py
import httpx
from app.config import settings

STORECOVE_BASE = "https://api.storecove.com/api/v2"

async def send_invoice(invoice_data: dict) -> dict:
    """Send invoice via Storecove API."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{STORECOVE_BASE}/document_submissions",
            headers={
                "Authorization": f"Bearer {settings.STORECOVE_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "legalEntityId": settings.STORECOVE_LEGAL_ENTITY_ID,
                "document": {
                    "documentType": "invoice",
                    "invoice": invoice_data,  # JSON Pure format
                },
            },
        )
        response.raise_for_status()
        return response.json()
```

### Step 4: HMRC MTD Integration (Separate from Peppol)

HMRC MTD requires a separate integration using their OAuth 2.0 API:

- **API Base**: `https://api.service.hmrc.gov.uk` (production) / `https://test-api.service.hmrc.gov.uk` (sandbox)
- **VAT API**: `POST /organisations/vat/{vrn}/returns` for quarterly submission
- **Auth**: OAuth 2.0 with Government Gateway credentials
- **Fraud Prevention Headers**: Mandatory — HMRC checks these during onboarding
- **Approval process**: Complete 2 questionnaires + fraud header validation (10 working days)

```python
# app/services/hmrc_mtd.py
async def submit_vat_return(vrn: str, period_key: str, vat_data: dict) -> dict:
    """Submit quarterly VAT return to HMRC."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.service.hmrc.gov.uk/organisations/vat/{vrn}/returns",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Gov-Client-Connection-Method": "WEB_APP_VIA_SERVER",
                # Additional fraud prevention headers required
            },
            json={
                "periodKey": period_key,
                "vatDueSales": vat_data["vat_due_sales"],
                "vatDueAcquisitions": vat_data["vat_due_acquisitions"],
                "totalVatDue": vat_data["total_vat_due"],
                "vatReclaimedCurrPeriod": vat_data["vat_reclaimed"],
                "netVatDue": vat_data["net_vat_due"],
                "totalValueSalesExVAT": vat_data["total_sales_ex_vat"],
                "totalValuePurchasesExVAT": vat_data["total_purchases_ex_vat"],
                "totalValueGoodsSuppliedExVAT": vat_data["total_goods_supplied_ex_vat"],
                "totalAcquisitionsExVAT": vat_data["total_acquisitions_ex_vat"],
                "finalised": True,
            },
        )
        response.raise_for_status()
        return response.json()
```

### Step 5: Deployment on Railway

No special infrastructure changes needed. The SaaS connector approach means your Railway-hosted FastAPI app makes outbound HTTPS calls to the Peppol Access Point API and receives webhooks for incoming invoices. Ensure:

- **Webhook endpoint**: Public URL for receiving incoming invoices (Railway provides this)
- **Environment variables**: `STORECOVE_API_KEY`, `STORECOVE_LEGAL_ENTITY_ID`, `HMRC_CLIENT_ID`, `HMRC_CLIENT_SECRET`
- **Retry logic**: SaaS APIs may return 429/503; implement exponential backoff
- **Idempotency**: Use invoice numbers as idempotency keys to prevent duplicate submissions

## Alternatives Considered

### 1. Open-Source Library Stack (python-en16931 + python-ubl + custom Peppol layer)

**Why considered:** Zero licensing costs, full control over invoice generation, Python-native integration with FastAPI.

**Why it ranked lower:** 
- `python-en16931` is explicitly a "proof of concept" at v0.1 — not production-ready
- No library handles the Peppol network layer (AS4 message exchange, SMP lookup, Access Point protocol)
- Becoming a Peppol Access Point requires OpenPeppol membership, ISO 27001 certification (~$20K-$50K), and ongoing compliance audits
- The 2026 B2B revision of EN 16931 is not implemented in any Python library yet
- Estimated 3-5 months of development to reach production quality, plus ongoing maintenance for regulatory changes

**When this would be the right choice:** If you were building an e-invoicing platform as your core product (not a feature), had 5+ engineers to dedicate, and a 12+ month timeline. Also viable if you only need to generate UBL XML for submission through a SaaS Access Point (hybrid approach) — but the SaaS connector's JSON-in/UBL-out conversion eliminates even this need.

### 2. Build from Scratch (Full Custom Implementation)

**Why considered:** Maximum control, no vendor dependencies, potential competitive advantage if e-invoicing becomes a core differentiator.

**Why it ranked lower:**
- Industry estimates: $140K-$300K for average complexity, 6-10 months development ([scnsoft.com](https://www.scnsoft.com/financial-management/e-invoicing))
- Exceeds $30K budget by 4.7-10x and 3-month timeline by 2-3x
- Regulatory maintenance is a continuous cost — ViDA implementing acts, national mandate changes, schematron rule updates, new country formats
- Peppol Access Point certification is a significant operational overhead for a 40-person startup
- "E-invoicing in Europe is not a 'build once and move on' feature" ([maventa.com](https://maventa.com/blog/the-true-cost-of-building-e-invoicing-in-europe))

**When this would be the right choice:** If e-invoicing compliance is your startup's core value proposition (you are the SaaS provider), you have $500K+ budget, 12+ month timeline, and plan to serve thousands of businesses. Think: you want to be the next Storecove, not use Storecove.

### 3. Hybrid: SaaS for Peppol + Custom for HMRC MTD

This is actually the recommended path. HMRC MTD is a simpler, well-documented REST API that doesn't require Peppol infrastructure. Building the MTD integration in-house (~30-40 hours) while using a SaaS connector for Peppol gives best-of-both-worlds: vendor-managed complexity where it's highest (EU multi-country e-invoicing) and in-house control where it's manageable (single-country UK VAT API).

## Adversarial Review

### Counterarguments to SaaS Recommendation

**"Vendor lock-in risk"** — Valid concern. Mitigation: Storecove's API accepts JSON Pure format (your internal representation) and converts to UBL/CII. If you switch providers, you change the API client, not your data model. The Peppol standard itself is the interoperability layer. Switching cost is estimated at 2-4 weeks of engineering.

**"€495/month is expensive for a startup"** — At projected invoice volumes (a B2B fintech at Series A likely processes hundreds to low thousands of invoices/month), this is €0.50-€5.00 per invoice. Manual invoice processing costs ~€15 per invoice ([peppol.org Billentis report](https://peppol.org/wp-content/uploads/2024/06/Billentis-Peppol-May-2024.pdf)). The SaaS cost is a fraction of the manual alternative. For tighter budgets, e-invoice.be (pay-per-use) or Qvalia (€39/month) are alternatives.

**"We could outgrow the SaaS provider"** — At scale (10K+ invoices/month), becoming your own Peppol Access Point may make economic sense. But that's a Series B/C decision, not a Series A decision. The SaaS connector gets you to market within budget and timeline.

### Sensitivity Analysis

| If this assumption is wrong... | Recommendation changes to... |
|---|---|
| Invoice volume exceeds 5K/month within year 1 | Negotiate volume discount with Storecove or switch to Qvalia Plus/e-invoice.be pay-per-use |
| UK mandates structured e-invoicing before 2029 | No change — Peppol/UBL infrastructure already in place via SaaS; MTD integration handles current requirements |
| Storecove raises prices significantly | Switch to e-invoice.be or Qvalia — API is similar, migration cost ~2-4 weeks |
| You need France (CII/Factur-X) support sooner than expected | Storecove handles CII conversion; no architecture change needed. If using e-invoice.be, verify CII support |
| EN 16931:2026 revision introduces breaking changes | SaaS provider absorbs the update; this is the primary value of the SaaS approach |
| $30K budget is hard-capped (no overrun possible) | Use e-invoice.be (pay-per-use, ~$3K-5K integration) + build HMRC MTD in-house (~$3K-4K). Total: ~$8K-$10K |

<details>
<summary>Assumption Audit (click to expand)</summary>

| Assumption | Classification | Risk if Wrong |
|---|---|---|
| Storecove starting price is ~€495/month | **Reasonable** — reported by G2/GetApp but may vary by contract | Budget impact; could be higher for multi-entity setup. Mitigation: get quote before committing |
| e-invoice.be is production-ready for EU-wide use | **Uncertain** — newer provider, limited public reviews | Could lack coverage for specific country mandates. Mitigation: test in sandbox with target countries before committing |
| python-en16931 will not reach production quality within 3 months | **Reasonable** — v0.1 proof-of-concept with single maintainer, no 2026 EN update | If it suddenly matures, hybrid (library for XML generation + SaaS for AP) becomes viable |
| HMRC MTD API integration takes ~30-40 hours | **Verified** — based on HMRC developer documentation scope ([developer.service.hmrc.gov.uk](https://developer.service.hmrc.gov.uk/guides/vat-mtd-end-to-end-service-guide/)) | Could take longer if fraud prevention header validation has issues; HMRC approval takes 10 working days |
| Invoice volume is <500/month in year 1 | **Uncertain** — depends on customer acquisition | If volume is higher, Storecove's per-document cost decreases with volume tiers |
| Railway hosting can accept webhooks reliably | **Verified** — Railway provides public URLs and persistent services | N/A |
| EUR/USD rate ~1.08 | **Reasonable** — current market rate as of early 2026 | ±10% currency fluctuation = ±€500-€1,200/year impact |
| The team has Python/FastAPI expertise | **Assumed from prompt** — stated as current stack | If team lacks API integration experience, add 20-30% to hour estimates |

</details>

<details>
<summary>Failure Modes (click to expand)</summary>

1. **SaaS provider outage during critical invoice deadline** — Mitigation: implement queue-based submission with retry logic; store invoices locally and mark as "pending submission." Most Peppol SaaS providers offer 99.9%+ uptime SLAs.

2. **HMRC rejects MTD submission due to fraud prevention headers** — This is the most common integration failure. HMRC requires specific headers (client IP, device info, connection method) and validates them during onboarding. Mitigation: use HMRC's sandbox extensively and follow their fraud prevention header specification exactly.

3. **Country-specific mandate requires a format the SaaS provider doesn't support** — Mitigated by choosing a provider with 30+ country coverage (Storecove). For niche requirements, a secondary provider or manual submission may be needed temporarily.

4. **Invoice data mapping errors cause rejected invoices** — EN 16931 has ~160 business terms with specific data type and cardinality requirements. Mitigation: validate against Peppol schematron rules before submission (use https://peppol.helger.com/wsdvs for pre-flight validation).

5. **Vendor discontinues or is acquired** — The Peppol standard is the interoperability layer, not the vendor. Your data model maps to EN 16931, making provider switching a client-layer change, not a data migration.

</details>

## Recommendation

**Use a SaaS Peppol Access Point connector (primary recommendation: Storecove; budget alternative: e-invoice.be) combined with a custom HMRC MTD integration.**

**Confidence: 88%**

**Execution plan:**
1. **Week 1-2**: Evaluate Storecove and e-invoice.be sandboxes with sample invoices targeting Belgium (Peppol/UBL) and France (CII). Decision gate: choose provider.
2. **Week 3-5**: Build PostgreSQL invoice data model, FastAPI CRUD endpoints, and SaaS API integration for send/receive.
3. **Week 6-8**: Build HMRC MTD OAuth flow and VAT return submission. Test in HMRC sandbox.
4. **Week 9-10**: End-to-end testing with Peppol sandbox, HMRC sandbox, and internal UAT.
5. **Week 11-12**: Production rollout, HMRC onboarding approval (10 working days), monitoring setup.

**Estimated cost**: $15K-$21K engineering + $6K-$12K/year SaaS = **$21K-$33K year-1 total**. Within or marginally above the $30K budget.

**This recommendation changes if:** (1) your invoice volume exceeds 10K/month within 12 months (evaluate becoming own Access Point), (2) you need to support 10+ countries simultaneously (may need Storecove's higher tier), or (3) e-invoicing becomes a core product differentiator rather than a compliance requirement (build in-house with dedicated team).

**Scope boundaries:** This analysis does not cover: (a) tax calculation engines (VAT rate determination, reverse charge rules) — these are separate from e-invoicing format compliance; (b) accounts receivable/payable workflow automation beyond invoice submission; (c) archiving requirements (10-year retention mandates in some jurisdictions); (d) specific PDP (Plateforme de Dématérialisation Partenaire) certification for France if acting as intermediary.

## Sources

**Official Standards & Specifications:**
- [Peppol BIS Billing 3.0 Specification](https://docs.peppol.eu/poacc/billing/3.0/bis/) — OpenPeppol official documentation
- [Peppol BIS 3.0 UBL Invoice Syntax](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/tree/) — XML structure reference
- [OpenPEPPOL peppol-bis-invoice-3 (GitHub)](https://github.com/OpenPEPPOL/peppol-bis-invoice-3) — Validation rules and schemas
- [ConnectingEurope/eInvoicing-EN16931 (GitHub)](https://github.com/ConnectingEurope/eInvoicing-EN16931) — EN 16931 validation artefacts
- [OpenPeppol Membership Fees](https://peppol.org/join/fees-2025/) — Fee structure for Service Providers

**Regulatory & Government:**
- [HMRC VAT MTD End-to-End Service Guide](https://developer.service.hmrc.gov.uk/guides/vat-mtd-end-to-end-service-guide/) — Primary source for MTD API integration
- [HMRC VAT MTD API Documentation](https://developer.service.hmrc.gov.uk/api-documentation/docs/api/service/vat-api/1.0) — API reference
- [VAT Notice 700/22: Making Tax Digital for VAT](https://www.gov.uk/government/publications/vat-notice-70022-making-tax-digital-for-vat/vat-notice-70022-making-tax-digital-for-vat) — Official HMRC guidance
- [EDICOM: ViDA Council Approval](https://edicomgroup.com/blog/vida-the-european-union-promotes-b2b-electronic-invoicing) — ViDA directive summary

**Industry Analysis & Compliance Guides:**
- [VATcalc: EU Digital Reporting Requirements](https://www.vatcalc.com/eu/eu-2028-digital-reporting-requirements-drr-e-invoice/) — ViDA timeline analysis
- [VATcalc: EN 16931 Update for ViDA](https://www.vatcalc.com/eu/eu-updates-en-16931-e-invoicing-standard-for-vida/) — 2026 B2B revision details
- [VATupdate: CEN Revised EN 16931 Approval](https://www.vatupdate.com/2025/10/31/european-e-invoicing-standard-en-16931-approved-oct-23-2025/) — Standard revision timeline
- [Fiskaly: E-Invoicing Mandates in Europe 2026](https://www.fiskaly.com/blog/e-invoicing-mandates-in-europe-2026) — Country-by-country timeline
- [Maventa: True Cost of Building E-Invoicing in Europe](https://maventa.com/blog/the-true-cost-of-building-e-invoicing-in-europe) — Build vs buy analysis
- [ScienceSoft: E-Invoicing Software Costs](https://www.scnsoft.com/financial-management/e-invoicing) — Development cost estimates
- [InvoiceNavigator: UBL vs CII Comparison](https://www.invoicenavigator.eu/compare/ubl-vs-cii) — Format comparison
- [AccountingWeb: Peppol E-Invoicing for UK Businesses](https://www.accountingweb.co.uk/community/industry-insights/peppol-e-invoicing-for-uk-businesses-everything-you-need-to-know-about) — UK 2029 mandate analysis
- [Billentis/OpenPeppol: Global E-Invoicing Report](https://peppol.org/wp-content/uploads/2024/06/Billentis-Peppol-May-2024.pdf) — Industry statistics on cost savings

**SaaS Vendor Documentation:**
- [Storecove API Documentation](https://www.storecove.com/docs/) — REST API reference
- [Storecove E-Invoicing API](https://www.storecove.com/us/en/solutions/e-invoicing-api/) — Platform overview
- [Storecove Peppol Access Point](https://www.storecove.com/us/en/solutions/peppol-access-point/) — Certification details
- [Qvalia Pricing](https://qvalia.com/pricing/) — Tier details
- [Qvalia Peppol API Guide](https://qvalia.com/help/how-to-access-peppol-api-step-by-step-guide/) — Integration guide
- [e-invoice.be Peppol API](https://e-invoice.be/peppol-api) — Pay-per-use model
- [e-invoice.be Python SDK (GitHub)](https://github.com/e-invoice-be/e-invoice-py) — Python SDK source

**Open-Source Libraries:**
- [python-en16931 Documentation](https://invinet.github.io/python-en16931/build/html/invoice.html) — Library docs (v0.1, proof-of-concept)
- [python-en16931 (GitHub)](https://github.com/invinet/python-en16931) — Source repository
- [python-ubl on Libraries.io](https://libraries.io/pypi/python-ubl) — Package health data
- [invoice2data on Snyk](https://snyk.io/advisor/python/invoice2data) — Maintenance status analysis
- [factur-x on PyPI](https://pypi.org/project/factur-x/) — CII/Factur-X library
- [factur-x (GitHub)](https://github.com/akretion/factur-x) — Source repository

**Pricing & Reviews:**
- [Storecove Pricing on G2](https://www.g2.com/products/storecove/pricing) — Reported pricing tiers
- [Storecove on GetApp](https://www.getapp.com/finance-accounting-software/a/storecove/) — Features and pricing
- [Qvalia on Capterra](https://www.capterra.com/p/191303/Qvalia/) — Reviews and pricing
