# GDPR Compliance: Data Handling Changes for US-to-EU Expansion

## Executive Summary

Expanding from the US to the EU with user PII stored in a single US-based AWS region triggers comprehensive obligations under the General Data Protection Regulation (GDPR). The changes span data residency and transfer mechanisms, architectural redesign for privacy-by-design, new organizational roles, documentation requirements, and user-facing rights infrastructure. This document covers each area in detail with actionable guidance.

---

## 1. Data Residency and Cross-Border Transfer

### The Core Problem

Storing EU residents' personal data exclusively in a US-based AWS region is not inherently illegal under GDPR, but it requires a valid **legal transfer mechanism** and creates ongoing compliance risk. You have three primary options, and the recommended approach combines multiple strategies.

### Option A: Migrate EU User Data to an EU AWS Region (Recommended)

AWS offers regions in **Ireland (eu-west-1), Frankfurt (eu-central-1), Paris (eu-west-3), Stockholm (eu-north-1), Milan (eu-south-1), and Spain (eu-south-2)**. Storing EU residents' data in an EU region eliminates the cross-border transfer issue entirely for data at rest.

**Action items:**
- Provision infrastructure in an EU AWS region (Frankfurt or Ireland are common choices).
- Implement data routing so that EU user data is created, processed, and stored in the EU region.
- Configure AWS service control policies to prevent accidental data replication to non-EU regions.
- Update your AWS GDPR Data Processing Addendum (DPA) to reflect the new region selection.

### Option B: EU-US Data Privacy Framework (DPF)

The [EU-US Data Privacy Framework](https://www.dataprivacyframework.gov/Program-Overview), established in July 2023, allows personal data to flow from the EU to self-certified US organizations. In September 2025, the European General Court confirmed the adequacy decision's validity, affirming that the US ensures an adequate level of protection for transfers to DPF-participating organizations.

**Action items:**
- Self-certify your organization with the US Department of Commerce via the DPF program.
- Implement the DPF Principles (notice, choice, accountability for onward transfer, security, data integrity, access, recourse/enforcement/liability).
- Re-certify annually.

**Risk:** The DPF could face future legal challenges (as happened with Safe Harbor and Privacy Shield). Always maintain a fallback.

### Option C: Standard Contractual Clauses (SCCs)

For any transfers not covered by the DPF (e.g., sub-processors not DPF-certified), use the [European Commission's Standard Contractual Clauses](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/eu-us-data-transfers_en). Updated SCCs from Q2 2025 simplify insertion-by-reference procedures.

**Action items:**
- Execute SCCs with every vendor/sub-processor that handles EU personal data outside the EEA.
- Conduct a **Transfer Impact Assessment (TIA)** for each transfer to evaluate the legal framework in the recipient country.
- Implement supplementary measures (encryption, pseudonymization, access controls) where the TIA identifies gaps.

### Recommended Architecture

Use a **dual-region strategy**: EU data stays in an EU region as default, DPF self-certification as a corporate-level compliance measure, and SCCs as contractual backup for all vendor relationships. This defense-in-depth approach insulates you from any single mechanism being invalidated.

---

## 2. Lawful Basis for Processing

Under [Article 6 GDPR](https://gdpr-info.eu/art-6-gdpr/), every processing activity must have a lawful basis. The six options are:

| Lawful Basis | Typical Use Case |
|---|---|
| **Consent** | Marketing emails, analytics cookies, non-essential tracking |
| **Contractual necessity** | Processing needed to deliver the service the user signed up for |
| **Legal obligation** | Tax records, financial reporting |
| **Vital interests** | Emergency health situations (rare for startups) |
| **Public interest** | Government/public sector tasks (unlikely for startups) |
| **Legitimate interest** | Fraud prevention, security monitoring (requires balancing test) |

**Action items:**
- Audit every data processing activity and assign a lawful basis.
- For consent-based processing, implement a mechanism to capture, store, and withdraw consent.
- Document this mapping in your Records of Processing Activities (see Section 5).
- Do not default to consent for everything--use contractual necessity where the processing is genuinely required to deliver your service.

---

## 3. Privacy by Design and Data Minimization (Article 25)

[Article 25 GDPR](https://gdpr-info.eu/art-25-gdpr/) mandates privacy by design and by default. This is not aspirational--it is a legal requirement enforceable with fines.

### Technical Implementation Requirements

**Data minimization:**
- Audit every PII field you collect. Remove any field not strictly necessary for the stated purpose.
- Limit data retention periods--define and enforce automatic deletion schedules.
- Restrict database-level access to authorized personnel only (principle of least privilege).

**Privacy by default:**
- All privacy settings must default to the most protective option.
- Non-essential cookies and tracking must be disabled until the user actively opts in.
- Third-party integrations must not receive personal data unless the user has consented.

**Pseudonymization and encryption:**
- Encrypt data at rest (AES-256) and in transit (TLS 1.3 minimum).
- Pseudonymize PII where full identification is not needed for processing (e.g., analytics).
- Implement key management using AWS KMS with customer-managed keys, ensuring keys are stored in the same region as the data.

**Access controls:**
- Role-based access control (RBAC) across all systems containing PII.
- Multi-factor authentication for any access to personal data.
- Audit logging of all access to PII.

---

## 4. Data Subject Rights Infrastructure

GDPR grants EU residents eight rights. You must build technical and operational capabilities to fulfill each within **one month** of a request.

### Rights and Implementation Requirements

| Right | Article | What You Must Build |
|---|---|---|
| **Right of access** | Art. 15 | Export all data held about a user in a portable format |
| **Right to rectification** | Art. 16 | Allow users to correct inaccurate personal data |
| **Right to erasure** | [Art. 17](https://gdpr-info.eu/art-17-gdpr/) | Delete all personal data across all systems, including backups, and notify downstream processors |
| **Right to restrict processing** | Art. 18 | Flag and freeze data so it is stored but not processed |
| **Right to data portability** | Art. 20 | Provide data in a structured, machine-readable format (JSON, CSV) |
| **Right to object** | Art. 21 | Stop processing based on legitimate interest or direct marketing |
| **Right against automated decisions** | Art. 22 | Provide human review of decisions made solely by algorithms |
| **Right to withdraw consent** | Art. 7(3) | One-click consent withdrawal, as easy as giving consent |

### Technical Implementation

- Build a **data subject request (DSR) portal** or integrate one into your user settings.
- Implement a **data inventory/map** so you can locate all PII for a given user across all systems (databases, caches, logs, backups, third-party services).
- For right to erasure: ensure deletion propagates to backups. Backups containing deleted user data must either be purged or the data must be re-deleted upon restoration. Notify all third parties who received the data.
- For data portability: implement an export API that generates a machine-readable archive of user data.
- Log all DSR requests and responses for compliance auditing.

---

## 5. Records of Processing Activities (RoPA) -- Article 30

[Article 30](https://gdpr-info.eu/art-30-gdpr/) requires you to maintain a written record of all processing activities. While there is an exemption for organizations with fewer than 250 employees, the exemption does **not** apply if processing is not occasional, involves special categories of data, or is likely to result in risk to data subjects. Most startups handling PII regularly will not qualify for the exemption.

### Required Contents

For each processing activity, document:
- Name and contact details of the controller (and DPO if applicable)
- Purposes of processing
- Categories of data subjects and personal data
- Categories of recipients
- Transfers to third countries and the safeguards used
- Retention periods
- Description of technical and organizational security measures

**Action item:** Create and maintain a RoPA spreadsheet or use a dedicated tool (e.g., OneTrust, TrustArc, or an open-source alternative). Update it whenever processing activities change.

---

## 6. Organizational Requirements

### Data Protection Officer (DPO) -- Article 37

A DPO appointment is **mandatory** if your core activities involve:
- Regular and systematic monitoring of data subjects on a large scale, or
- Large-scale processing of special categories of data (health, biometric, racial/ethnic data, etc.)

Even if not legally required, appointing a DPO (or an external DPO service) is strongly recommended for a startup entering the EU market. The DPO must have expert knowledge of data protection law and practices, must report to the highest level of management, and cannot be dismissed for performing their duties.

**Penalty for non-appointment when required:** up to EUR 10 million or 2% of global annual turnover.

### EU Representative -- Article 27

If your startup does **not** establish a physical presence in the EU, [Article 27](https://gdpr-info.eu/art-27-gdpr/) requires you to designate a representative in an EU Member State where your data subjects are located. This representative serves as a contact point for data subjects and supervisory authorities.

**Penalty for non-appointment:** up to EUR 10 million or 2% of global annual turnover.

**Action items:**
- Appoint an EU representative (can be a specialized service provider such as GDPR Local, VeraSafe, or similar).
- Publish the representative's contact details in your privacy policy.
- Notify the relevant supervisory authority.

---

## 7. Breach Notification -- Articles 33 and 34

### Notification to Supervisory Authority (Article 33)

You must notify the relevant EU Data Protection Authority **within 72 hours** of becoming aware of a personal data breach, unless the breach is unlikely to result in a risk to individuals' rights and freedoms.

The notification must include:
- Nature of the breach (categories and approximate number of individuals/records affected)
- DPO or contact point details
- Likely consequences
- Measures taken or proposed to address and mitigate the breach

### Notification to Data Subjects (Article 34)

If the breach is likely to result in a **high risk** to individuals, you must also notify the affected data subjects without undue delay. This obligation is waived if you applied encryption or other measures that rendered the data unintelligible to unauthorized persons.

### Technical Preparation

- Implement intrusion detection and monitoring.
- Build a breach response playbook with roles, communication templates, and escalation paths.
- Maintain a breach register documenting all incidents (even those not reported to authorities).
- Pre-identify which supervisory authority is your "lead authority" (typically the DPA where your EU representative or main establishment is located).

---

## 8. Consent Management and Cookie Compliance

Under the [ePrivacy Directive](https://gdpr-info.eu/art-7-gdpr/) (reinforced by GDPR), websites targeting EU users must obtain **prior, informed, freely given** consent before setting non-essential cookies or trackers.

### Requirements

- Deploy a **Consent Management Platform (CMP)** such as Cookiebot, OneTrust, or Usercentrics.
- The cookie banner must have equally visible Accept and Reject buttons--no dark patterns.
- Non-essential cookies must be **blocked by default** until the user actively opts in.
- Pre-checked boxes are not valid consent.
- Record and store consent logs as proof of compliance (the burden of proof is on you).
- Implement **Google Consent Mode v2** if you use Google Analytics or Google Ads.
- Allow users to change or withdraw consent at any time, as easily as they gave it.

---

## 9. Vendor and Sub-Processor Management

### Data Processing Agreements (DPAs) -- Article 28

Every third-party vendor that processes personal data on your behalf must be bound by a **Data Processing Agreement** that specifies:
- Subject matter and duration of processing
- Nature and purpose of processing
- Types of personal data and categories of data subjects
- Obligations and rights of the controller
- Requirements for sub-processor approval
- Data deletion or return upon contract termination
- Audit rights

**Action items:**
- Inventory all vendors that touch EU user data (analytics, payment processors, email providers, cloud services, customer support tools, etc.).
- Execute DPAs with each vendor. Most major SaaS providers (AWS, Stripe, Twilio, etc.) offer standard DPAs.
- Ensure AWS's GDPR DPA is signed and reflects your EU region configuration.
- Implement a vendor review process for new tools before onboarding.

---

## 10. Data Protection Impact Assessments (DPIAs) -- Article 35

A [DPIA](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/when-data-protection-impact-assessment-dpia-required_en) is required before any processing that is **likely to result in high risk** to individuals, including:
- Systematic and extensive profiling with significant effects
- Large-scale processing of special category data
- Systematic monitoring of publicly accessible areas
- Use of new technologies with potential high-risk implications

### Required Contents

- Systematic description of the processing and its purposes
- Assessment of necessity and proportionality
- Assessment of risks to data subjects' rights and freedoms
- Measures to mitigate those risks

**Action items:**
- Conduct a DPIA for your core product's data processing before launching in the EU.
- Re-assess every three years or when processing changes materially.
- If the DPIA identifies residual high risks that cannot be mitigated, you must consult the supervisory authority before proceeding.

---

## 11. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- [ ] Conduct a full data inventory and mapping exercise
- [ ] Identify lawful basis for each processing activity
- [ ] Begin RoPA documentation
- [ ] Appoint an EU representative (Article 27)
- [ ] Evaluate DPO requirement; appoint if necessary

### Phase 2: Infrastructure (Weeks 5-10)
- [ ] Provision EU AWS region and migrate EU user data
- [ ] Implement data routing logic (EU users -> EU region)
- [ ] Self-certify under the EU-US Data Privacy Framework
- [ ] Execute SCCs with all non-DPF vendors
- [ ] Deploy encryption (at rest and in transit) with EU-region KMS keys
- [ ] Implement RBAC, MFA, and audit logging for PII access

### Phase 3: User-Facing Compliance (Weeks 11-16)
- [ ] Build data subject request portal (access, erasure, portability, rectification)
- [ ] Deploy Consent Management Platform with compliant cookie banner
- [ ] Update privacy policy for GDPR compliance (must be clear, plain language)
- [ ] Implement consent capture and withdrawal mechanisms

### Phase 4: Operational Readiness (Weeks 17-20)
- [ ] Execute DPAs with all vendors
- [ ] Conduct DPIA for core processing activities
- [ ] Build and test breach notification playbook
- [ ] Train all staff handling personal data
- [ ] Conduct internal audit and gap assessment

### Phase 5: Ongoing
- [ ] Regular RoPA updates
- [ ] Annual DPF re-certification
- [ ] Periodic DPIA reviews (minimum every 3 years)
- [ ] Continuous monitoring for regulatory changes

---

## 12. Penalty Summary

| Violation Category | Maximum Fine |
|---|---|
| Core GDPR principles, data subject rights, cross-border transfer violations | EUR 20 million or 4% of global annual turnover |
| Administrative obligations (DPO, RoPA, breach notification, DPIA) | EUR 10 million or 2% of global annual turnover |

Fines are assessed on a case-by-case basis considering factors such as the nature and gravity of the infringement, the number of data subjects affected, measures taken to mitigate damage, and degree of cooperation with the supervisory authority.

---

## Sources

- [EU Data Protection -- AWS](https://aws.amazon.com/compliance/eu-data-protection/)
- [AWS GDPR Center](https://aws.amazon.com/compliance/gdpr-center/)
- [Navigating GDPR Compliance on AWS -- Defining Boundaries](https://docs.aws.amazon.com/whitepapers/latest/navigating-gdpr-compliance/defining-boundaries-for-regional-services-access.html)
- [EU-US Data Privacy Framework Program Overview](https://www.dataprivacyframework.gov/Program-Overview)
- [EU-US Data Transfers -- European Commission](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/eu-us-data-transfers_en)
- [EU-US Data Privacy Framework -- Wikipedia](https://en.wikipedia.org/wiki/EU%E2%80%93US_Data_Privacy_Framework)
- [Adequacy of the EU-US DPF Survives Challenge -- Epstein Becker Green](https://www.workforcebulletin.com/adequacy-of-the-eu-u-s-data-privacy-framework-survives-challenge)
- [Article 25 GDPR -- Data Protection by Design and Default](https://gdpr-info.eu/art-25-gdpr/)
- [Article 17 GDPR -- Right to Erasure](https://gdpr-info.eu/art-17-gdpr/)
- [Article 27 GDPR -- EU Representative](https://gdpr-info.eu/art-27-gdpr/)
- [Article 30 GDPR -- Records of Processing Activities](https://gdpr-info.eu/art-30-gdpr/)
- [Article 37 GDPR -- Data Protection Officer](https://gdpr-info.eu/art-37-gdpr/)
- [Article 35 GDPR -- Data Protection Impact Assessment](https://gdpr-info.eu/art-35-gdpr/)
- [When is a DPIA Required? -- European Commission](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/when-data-protection-impact-assessment-dpia-required_en)
- [DPO Requirements -- European Commission](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/data-protection-officers/does-my-companyorganisation-need-have-data-protection-officer-dpo_en)
- [GDPR Breach Notification 72-Hour Rule -- Glocert](https://www.glocertinternational.com/resources/articles/gdpr-breach-notification-72-hour-rule/)
- [EDPB Guidelines on Breach Notification (PDF)](https://www.edpb.europa.eu/system/files/2023-04/edpb_guidelines_202209_personal_data_breach_notification_v2.0_en.pdf)
- [EDPB Guidelines on Article 25 -- Privacy by Design (PDF)](https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_201904_dataprotection_by_design_and_by_default_v2.0_en.pdf)
- [GDPR Cookie Consent Requirements 2025 -- SecurePrivacy](https://secureprivacy.ai/blog/gdpr-cookie-consent-requirements-2025)
- [EU Cookie Compliance 2025 -- Usercentrics](https://usercentrics.com/knowledge-hub/eu-cookie-compliance/)
- [US and International Data Privacy Developments 2025-2026 -- McDonald Hopkins](https://www.mcdonaldhopkins.com/insights/news/u-s-and-international-data-privacy-developments-in-2025-and-compliance-considerations-for-2026)
- [GDPR Compliance for US Companies 2026 -- Truzta](https://truzta.com/resources/blog/gdpr-compliance-for-us-companies-2026/)
- [Data Protection & Privacy 2026 EU -- Chambers and Partners](https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/eu/trends-and-developments/O24484)
- [Article 27 EU Representative Guide -- GDPR Local](https://gdprlocal.com/article-27-eu-representative-a-comprehensive-guide/)
- [Records of Processing Activities Guidance -- Irish DPC](https://www.dataprotection.ie/en/dpc-guidance/records-of-processing-article-30-guidance)
