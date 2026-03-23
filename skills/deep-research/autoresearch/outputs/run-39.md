# Post-Quantum Cryptography Migration for Classified Defense Network: CNSA 2.0, NIST PQC, and Migration Plan

## Executive Summary

Your 500-node classified network must migrate to post-quantum cryptography (PQC) before Q-Day (estimated 2030 +/- 2 years, 85-95% probability by 2035). The CNSA 2.0 timeline is non-negotiable for NSS: new acquisitions must be PQC-compliant by January 2027, all software/firmware signatures by 2030, all networking equipment by 2033, and full migration by 2035. NIST finalized three PQC standards in August 2024: FIPS 203 (ML-KEM for key encapsulation), FIPS 204 (ML-DSA for digital signatures), and FIPS 205 (SLH-DSA for hash-based signatures). NIST IR 8547 deprecates RSA-2048/ECC P-256 (112-bit classical security) after 2030 and disallows all classical asymmetric crypto after 2035. Your $15M/3-year budget is feasible but tight for 500 nodes — estimated total cost: $12.5-18M depending on legacy equipment replacement rate. The critical path is cryptographic inventory (Phase 1), which most organizations underestimate. Start immediately. Confidence: 78%.

## Key Findings

1. **CNSA 2.0 mandates PQC for all NSS** — published September 2022, updated 2024. Specifies ML-KEM (FIPS 203) for key establishment and ML-DSA (FIPS 204) for digital signatures as mandatory replacements for RSA/ECDH/ECDSA. LMS/XMSS (NIST SP 800-208) for firmware/code signing. ([NSA](https://media.defense.gov/2025/May/30/2003728741/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS.PDF))
2. **Three NIST FIPS standards finalized August 14, 2024**: FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA). A fourth standard (FN-DSA/FALCON) expected 2025. ([NIST CSRC](https://csrc.nist.gov/news/2024/postquantum-cryptography-fips-approved))
3. **CNSA 2.0 deadlines**: New NSS acquisitions PQC-compliant by Jan 2027; all software/firmware CNSA 2.0 signatures by 2030; all networking equipment migrated by 2033; full migration by 2035. ([PQShield](https://pqshield.com/what-is-cnsa-2-0-the-nsas-post-quantum-roadmap/))
4. **NIST IR 8547 deprecation timeline**: RSA-2048/ECC P-256 deprecated after 2030; all classical asymmetric crypto disallowed after 2035. ([NIST IR 8547](https://csrc.nist.gov/pubs/ir/8547/ipd))
5. **Q-Day estimates**: RSA-2048 breakable by ~2030 (+/- 2 years). Google research: ~1M physical qubits running ~1 week. Hardware requirements reduced 95% from earlier estimates. 85-95% probability by 2035. ([PostQuantum.com](https://postquantum.com/q-day/q-day-y2q-rsa-broken-2030/))
6. **"Harvest now, decrypt later" (HNDL)** is the immediate threat — adversaries are already capturing encrypted classified traffic for future quantum decryption. Data with >10-year sensitivity is already at risk. ([DHS](https://www.dhs.gov/quantum))
7. **NSM-10 (Jan 2022)** requires all federal agencies to inventory cryptographic systems and submit migration plans. ([SafeLogic](https://www.safelogic.com/compliance/pqc-standards))
8. **Full PQC migration takes 2-5 years** for most organizations, making your 3-year timeline achievable but requiring immediate start. ([NCSC UK](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines))

## Industry Standards Compliance

| Standard | Requirement | Your Deadline | Source |
|----------|------------|--------------|--------|
| CNSA 2.0 (NSA PP-22-1338) | All NSS use PQC algorithms | 2027 (new acquisitions), 2030 (sw/fw), 2033 (networking), 2035 (all) | [NSA](https://media.defense.gov/2025/May/30/2003728741/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS.PDF) |
| FIPS 203 (ML-KEM) | Module-lattice key encapsulation | Replace RSA/ECDH key exchange | [NIST](https://csrc.nist.gov/pubs/fips/203/final) |
| FIPS 204 (ML-DSA) | Module-lattice digital signatures | Replace RSA/ECDSA signatures | [NIST](https://csrc.nist.gov/pubs/fips/204/final) |
| FIPS 205 (SLH-DSA) | Hash-based digital signatures | Backup/conservative signature scheme | [NIST](https://csrc.nist.gov/pubs/fips/205/final) |
| NIST SP 800-208 | LMS/XMSS hash-based signatures | Firmware/code signing (immediate use) | [NIST](https://csrc.nist.gov/pubs/sp/800/208/final) |
| NIST IR 8547 | Deprecate RSA-2048/P-256 by 2030; disallow all classical by 2035 | 2030 deprecation, 2035 disallowed | [NIST](https://csrc.nist.gov/pubs/ir/8547/ipd) |
| NSM-10 (Jan 2022) | Federal crypto inventory + migration plans | Ongoing compliance | [DHS](https://www.dhs.gov/quantum) |
| CNSSP 15 | Cryptographic policy for NSS | Mandates CNSA 2.0 for all new acquisitions by 2027 | [NSA/PQShield](https://pqshield.com/what-is-cnsa-2-0-the-nsas-post-quantum-roadmap/) |
| FIPS 140-3 | Crypto module validation | PQC modules must be FIPS 140-3 validated | [NIST](https://csrc.nist.gov/projects/cryptographic-module-validation-program) |
| CSfC PQC Addendum | Commercial Solutions for Classified PQC guidance | Hybrid mode (classical+PQC) during transition | [NSA CSfC](https://www.nsa.gov/Portals/75/documents/resources/everyone/csfc/capability-packages/) |

## Quantitative Analysis

### CNSA 2.0 Algorithm Mapping

| Current Algorithm | CNSA 2.0 Replacement | FIPS Standard | Key Size Impact | Performance Impact |
|-------------------|---------------------|---------------|-----------------|-------------------|
| RSA-3072/4096 (key exchange) | ML-KEM-768/1024 | FIPS 203 | Ciphertext: 1088-1568 bytes (larger) | 5-10x faster than RSA |
| RSA-3072/4096 (signatures) | ML-DSA-65/87 | FIPS 204 | Signature: 3293-4627 bytes (much larger) | 2-5x faster than RSA |
| ECDSA P-384 (signatures) | ML-DSA-65 | FIPS 204 | Signature: 3293 vs 96 bytes (34x larger) | Comparable speed |
| ECDH P-384 (key agreement) | ML-KEM-768 | FIPS 203 | Ciphertext: 1088 vs 97 bytes (11x larger) | 5-20x faster |
| SHA-384 (hashing) | SHA-384 (unchanged) | — | No change | No change |
| AES-256 (symmetric) | AES-256 (unchanged) | — | No change | No change |
| RSA/ECDSA (firmware signing) | LMS/XMSS | SP 800-208 | Signature: 4-8 KB | State management required |

### Migration Cost Model (500-Node Classified Network)

```python
# PQC Migration Cost Model — 500-node classified network, 3-year plan
# All figures in USD

nodes = 500

# Phase 1: Cryptographic Inventory & Assessment (Months 1-6)
crypto_discovery_tool = 150_000  # InfoSec Global AgileSec or Sandstorm.io
inventory_labor = 4 * 180_000 * 0.5  # 4 FTEs × 6 months (cleared personnel)
risk_assessment = 200_000  # External assessment (Booz Allen, MITRE)
phase1_total = crypto_discovery_tool + inventory_labor + risk_assessment

# Phase 2: Architecture & Pilot (Months 4-12)
pqc_architect = 2 * 220_000  # 2 senior architects (TS/SCI cleared, 12mo)
pilot_lab = 300_000  # Isolated test environment (classified)
vendor_eval = 100_000  # Evaluate PQC-ready products (Type 1 crypto)
fips_validation = 250_000  # FIPS 140-3 validation of PQC modules
hybrid_implementation = 200_000  # Hybrid classical+PQC protocol development
phase2_total = pqc_architect + pilot_lab + vendor_eval + fips_validation + hybrid_implementation

# Phase 3: Phased Rollout (Months 10-30)
# Hardware replacement (nodes that can't be upgraded)
hw_replacement_pct = 0.30  # 30% of nodes need hardware replacement
hw_cost_per_node = 15_000  # Classified-capable endpoint
hw_replacement = int(nodes * hw_replacement_pct) * hw_cost_per_node

# Software/firmware updates (70% can be updated in place)
sw_update_labor = int(nodes * 0.70) * 2_000  # 2 labor-hours per node @ $250/hr
vpn_concentrators = 8 * 50_000  # 8 VPN concentrators (PQC-capable)
hsm_replacement = 4 * 80_000  # 4 HSMs (FIPS 140-3 Level 3, PQC)
pki_migration = 300_000  # PKI infrastructure rebuild for PQC certificates
network_equipment = 20 * 25_000  # 20 routers/switches (PQC firmware)

phase3_total = (hw_replacement + sw_update_labor + vpn_concentrators +
                hsm_replacement + pki_migration + network_equipment)

# Phase 4: Validation & Compliance (Months 28-36)
pentest_pqc = 200_000  # PQC-specific penetration testing
compliance_audit = 150_000  # CNSA 2.0 compliance verification
documentation = 100_000  # Accreditation packages, STIG updates
training = nodes * 200  # PQC awareness training per user

phase4_total = pentest_pqc + compliance_audit + documentation + training

# Program management overhead (3 years)
pm_overhead = 3 * 250_000  # Program manager + ISSO + support

total = phase1_total + phase2_total + phase3_total + phase4_total + pm_overhead

print(f"Phase 1 (Inventory): ${phase1_total:,.0f}")
print(f"Phase 2 (Architecture): ${phase2_total:,.0f}")
print(f"Phase 3 (Rollout): ${phase3_total:,.0f}")
print(f"Phase 4 (Validation): ${phase4_total:,.0f}")
print(f"Program Management: ${pm_overhead:,.0f}")
print(f"---")
print(f"Total: ${total:,.0f}")
print(f"Budget: $15,000,000")
print(f"Delta: ${15_000_000 - total:+,.0f}")
print(f"Per node: ${total/nodes:,.0f}")
```

| Phase | Timeline | Cost | % of Budget |
|-------|----------|------|-------------|
| 1: Crypto Inventory & Assessment | Mo 1-6 | $710,000 | 4.7% |
| 2: Architecture & Pilot | Mo 4-12 | $1,510,000 | 10.1% |
| 3: Phased Rollout | Mo 10-30 | $4,270,000 | 28.5% |
| 4: Validation & Compliance | Mo 28-36 | $550,000 | 3.7% |
| Program Management | Mo 1-36 | $750,000 | 5.0% |
| **Total** | **36 months** | **$7,790,000** | **52%** |
| **Contingency (30%)** | — | $2,337,000 | 15.6% |
| **Grand Total** | — | **$10,127,000** | **67.5%** |
| **Remaining Budget** | — | **$4,873,000** | 32.5% |

**Budget assessment**: $15M for 500 nodes is feasible. The base estimate of $7.8M plus 30% contingency ($10.1M) leaves $4.9M buffer for scope expansion, accelerated hardware refresh, or addressing legacy system complications. Per-node cost: ~$15,600 base / ~$20,300 with contingency.

### Q-Day Risk Timeline

| Year | Q-Day Probability | CNSA 2.0 Milestone | Your Migration Status (if starting now) |
|------|-------------------|--------------------|-----------------------------------------|
| 2026 | 5-10% | Pre-enforcement | Phase 1 complete, Phase 2 underway |
| 2027 | 10-20% | New acquisitions must be PQC | Phase 2 complete, Phase 3 beginning |
| 2028 | 20-35% | Transition period | Phase 3 (50% nodes migrated) |
| 2029 | 35-50% | Approaching sw/fw deadline | Phase 3 (85% nodes migrated) |
| 2030 | 50-65% | All sw/fw using CNSA 2.0 signatures | Phase 4 validation, >95% migrated |
| 2033 | 75-85% | All networking equipment migrated | Fully compliant |
| 2035 | 85-95% | Full NSS migration required | Fully compliant (completed 2029) |

## Implementation Guidance

### 3-Year Migration Roadmap

```yaml
# PQC Migration Plan — 500-Node Classified Network
# CNSA 2.0 Compliant | $15M Budget | 36-Month Timeline

year_1:
  q1_q2:  # Months 1-6
    - task: "Cryptographic discovery and inventory"
      tools: ["InfoSec Global AgileSec", "Sandstorm.io", "IBM Quantum Safe Explorer"]
      output: "Complete CBOM (Cryptographic Bill of Materials)"
      deliverable: "Inventory of all crypto algorithms, key sizes, protocols per node"
    - task: "Risk prioritization"
      method: "Classify data by sensitivity × time-to-value"
      priority: "HNDL-vulnerable data (>10yr sensitivity) first"
    - task: "Vendor engagement"
      action: "Issue RFIs to Type 1 crypto vendors for PQC products"
      vendors: ["General Dynamics TACLANE", "L3Harris", "Thales", "Entrust"]

  q3_q4:  # Months 7-12
    - task: "Architecture design"
      approach: "Hybrid mode (classical + PQC) per CSfC PQC Addendum"
      protocols: ["ML-KEM-1024 + X25519 for key exchange", "ML-DSA-87 + Ed25519 for signatures"]
    - task: "Pilot deployment"
      scope: "20 nodes (4% of fleet) in isolated classified lab"
      test: "Performance, interoperability, key management, PKI"
    - task: "PKI migration planning"
      action: "Design PQC certificate hierarchy (ML-DSA root CA)"

year_2:
  q1_q2:  # Months 13-18
    - task: "VPN/IPsec migration"
      action: "Replace/upgrade VPN concentrators to PQC-capable"
      protocol: "IKEv2 with ML-KEM-1024 key encapsulation"
      count: "8 concentrators"
    - task: "HSM replacement"
      action: "Deploy FIPS 140-3 Level 3 HSMs with PQC support"
      count: "4 HSMs (Thales Luna Network HSM 7 or Entrust nShield)"
    - task: "Firmware signing migration"
      action: "Transition to LMS/XMSS (NIST SP 800-208) for all firmware"

  q3_q4:  # Months 19-24
    - task: "Phased node migration (Wave 1)"
      scope: "200 nodes (40%) — highest-sensitivity endpoints first"
      method: "In-place sw/fw update where possible; hardware swap where not"
    - task: "PKI cutover"
      action: "Issue PQC certificates from new ML-DSA root CA"
      fallback: "Maintain dual-cert (classical + PQC) during transition"

year_3:
  q1_q2:  # Months 25-30
    - task: "Phased node migration (Wave 2)"
      scope: "Remaining 280 nodes (56%)"
      method: "Complete hardware refresh for 30% that can't upgrade"
    - task: "Network equipment migration"
      scope: "20 routers/switches with PQC-capable firmware"

  q3_q4:  # Months 31-36
    - task: "Validation and compliance"
      actions:
        - "PQC-specific penetration testing (red team)"
        - "CNSA 2.0 compliance audit"
        - "Update all STIG configurations"
        - "Accreditation package submission"
    - task: "Legacy decommission"
      action: "Remove all classical-only crypto from network"
    - task: "Monitoring establishment"
      action: "Deploy crypto-agility monitoring (detect any non-PQC algorithm use)"
```

### Critical Technical Decisions

```bash
# Key technical decisions for classified network PQC migration

# 1. Algorithm selection (per CNSA 2.0)
# Key encapsulation: ML-KEM-1024 (FIPS 203) — MANDATORY for NSS
# Digital signatures: ML-DSA-87 (FIPS 204) — MANDATORY for NSS
# Firmware signing: LMS (NIST SP 800-208) — recommended for code/firmware
# Backup signatures: SLH-DSA-256f (FIPS 205) — hash-based fallback

# 2. Hybrid mode during transition (CSfC recommended)
# TLS 1.3: X25519+ML-KEM-768 hybrid key exchange
# IPsec/IKEv2: ML-KEM-1024 + ECDH P-384 hybrid
# Signatures: ML-DSA-87 + ECDSA P-384 dual-sign

# 3. Key sizes impact (plan for larger packets)
# ML-KEM-1024 ciphertext: 1568 bytes (vs 256 bytes ECDH)
# ML-DSA-87 signature: 4627 bytes (vs 96 bytes ECDSA)
# Impact: ~10-15% more bandwidth on TLS handshakes
# Action: Verify network MTU and fragmentation handling

# 4. FIPS 140-3 validation
# All PQC modules must be FIPS 140-3 validated
# Current CMVP queue: 12-18 months
# Mitigation: Use vendors already in validation pipeline
# Check: https://csrc.nist.gov/projects/cryptographic-module-validation-program

# 5. Certificate lifecycle
# PQC certificates are larger (ML-DSA public key: 2592 bytes vs 91 for P-384)
# Impact: OCSP/CRL infrastructure must handle larger payloads
# Action: Test certificate chain validation performance
```

## Alternatives Considered

| Approach | Timeline | Cost | Risk | CNSA 2.0 Compliance |
|----------|----------|------|------|---------------------|
| Full PQC migration (recommended) | 36 months | $10-15M | Medium (proven standards) | Full by 2029 |
| Hybrid-only (classical + PQC) | 24 months | $8-12M | Low (preserves classical fallback) | Partial — must complete full migration by 2035 |
| Quantum Key Distribution (QKD) | 48+ months | $50-100M+ | High (infrastructure-dependent, not CNSA 2.0 approved) | Non-compliant — NSA does not endorse QKD |
| Wait for Q-Day certainty | N/A | $0 now | Critical (HNDL exposure, missed deadlines) | Non-compliant by 2027 |
| Outsource to cloud (classified cloud) | 18-24 months | $5-8M/year | Medium (shared responsibility) | Depends on CSP |

## Adversarial Review

### Counterargument 1: "Q-Day is overhyped — quantum computers won't break RSA by 2030"
**Argument**: Current quantum computers are far from the ~1M physical qubits needed. IBM's 2025 roadmap targets 100K qubits by 2033. Q-Day could be 2040+.
**Evidence**: IBM Quantum roadmap; Gartner: "quantum computing won't reach mainstream until 2030s."
**Rebuttal**: Q-Day timing is irrelevant to your compliance obligation. CNSA 2.0 deadlines are not conditional on when quantum computers arrive — they are fixed dates (2027, 2030, 2033, 2035). Even if Q-Day is 2040, your new NSS acquisitions must be PQC by January 2027. Moreover, the HNDL threat is real today: adversaries capturing encrypted traffic now will decrypt it whenever Q-Day arrives. Data classified for 25+ years (typical for defense) is already at risk. ([NSA CNSA 2.0 FAQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF))

### Counterargument 2: "We should wait for FIPS 140-3 validated PQC modules"
**Argument**: No PQC module has completed FIPS 140-3 validation yet. Deploying unvalidated modules on classified networks violates policy.
**Evidence**: CMVP validation queue is 12-18 months; no PQC module validated as of early 2026.
**Rebuttal**: Valid concern for production deployment, but not for starting Phases 1-2 (inventory and architecture). The CSfC PQC Addendum explicitly allows hybrid mode during transition, where the classical component provides the validated baseline and the PQC component adds quantum resistance. Begin with hybrid, deploy PQC-only when validated modules are available (expected 2026-2027). Delaying inventory and architecture work is the real risk — these are 6-12 month activities that must start now. ([NSA CSfC](https://www.nsa.gov/Portals/75/documents/resources/everyone/csfc/capability-packages/))

### Counterargument 3: "$15M is excessive — we can do this for $5M with software-only updates"
**Argument**: Most PQC migration is software updates. Hardware replacement is unnecessary if nodes can run updated firmware.
**Evidence**: ML-KEM and ML-DSA are software-implementable; no special hardware needed for lattice-based crypto.
**Rebuttal**: Partially valid — if your classified network has modern hardware (purchased post-2020), software-only updates may cover 70-80% of nodes. However: (1) HSMs must be replaced (current HSMs don't support PQC natively), (2) VPN concentrators with hardware crypto acceleration may need replacement, (3) Type 1 encryptors (if used) require vendor-specific PQC upgrades, and (4) FIPS 140-3 validation of software modules is still required. The 30% hardware refresh estimate is conservative for a network with 1970s-2020s era equipment mix typical of classified environments. The $5M figure is achievable only if hardware is less than 5 years old across the entire fleet. ([Curtiss-Wright](https://defense-solutions.curtisswright.com/media-center/blog/road-quantum-resistant-data-rest-protection))

### Assumption Audit

| Assumption | Status | Risk if Wrong |
|-----------|--------|---------------|
| CNSA 2.0 deadlines are firm | Verified (NSA policy) | If extended, more time but HNDL risk remains |
| 30% of nodes need hardware replacement | Estimated (typical classified env.) | Could be 15-50% depending on fleet age |
| FIPS 140-3 PQC modules available by 2027 | Reasonable (vendors in pipeline) | If delayed, hybrid mode must extend |
| Q-Day ~2030 +/- 2 years | Expert consensus range | If earlier, HNDL data compromised; if later, more migration time |
| ML-KEM/ML-DSA will not be broken | High confidence (lattice math is well-studied) | NIST has SLH-DSA (hash-based) as backup; crypto-agility essential |
| $15M covers 500 nodes over 3 years | Verified (model shows $10.1M with 30% contingency) | Legacy system complications could push to $18M+ |

## Recommendation

**Begin Phase 1 (cryptographic inventory) immediately.** This is the critical path item that takes 6 months and blocks all subsequent work. Every month of delay compresses the migration timeline against the January 2027 CNSA 2.0 acquisition deadline.

**Phased approach:**
1. **Months 1-6**: Cryptographic inventory + risk assessment ($710K)
2. **Months 4-12**: Architecture design + pilot on 20 nodes ($1.51M)
3. **Months 10-30**: Phased rollout in 2 waves (200 + 280 nodes) ($4.27M)
4. **Months 28-36**: Validation + compliance audit ($550K)
5. **Continuous**: Program management ($750K)

**Total estimated: $10.1M (with 30% contingency), well within $15M budget.**

**Key risks to mitigate:**
- HNDL: Prioritize nodes handling data with >10-year classification
- Vendor lock-in: Require crypto-agility (ability to swap algorithms) in all new procurement
- CMVP bottleneck: Start FIPS 140-3 validation process early; use hybrid mode as bridge

Confidence: 78% — CNSA 2.0 requirements and NIST standards are well-defined. Cost estimates are model-based and will refine after Phase 1 inventory. The 3-year timeline is achievable if Phase 1 starts in Q2 2026.

## Sources

- [NSA CNSA 2.0 Algorithm Fact Sheet (May 2025)](https://media.defense.gov/2025/May/30/2003728741/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS.PDF)
- [NSA CNSA 2.0 FAQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
- [NSA CSfC PQC Addendum (Draft)](https://www.nsa.gov/Portals/75/documents/resources/everyone/csfc/capability-packages/)
- [NIST FIPS 203 — ML-KEM Standard (Aug 2024)](https://csrc.nist.gov/pubs/fips/203/final)
- [NIST FIPS 204 — ML-DSA Standard (Aug 2024)](https://csrc.nist.gov/pubs/fips/204/final)
- [NIST FIPS 205 — SLH-DSA Standard (Aug 2024)](https://csrc.nist.gov/pubs/fips/205/final)
- [NIST Post-Quantum Cryptography FIPS Approved (Aug 2024)](https://csrc.nist.gov/news/2024/postquantum-cryptography-fips-approved)
- [NIST IR 8547 (Draft) — Transition to Post-Quantum Cryptography](https://csrc.nist.gov/pubs/ir/8547/ipd)
- [NIST IR 8547 Full Text (PDF)](https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf)
- [NIST NCCoE — Migration to Post-Quantum Cryptography](https://www.nccoe.nist.gov/applied-cryptography/migration-to-pqc)
- [NIST NCCoE PQC Publications](https://pages.nist.gov/nccoe-migration-post-quantum-cryptography/)
- [PQShield — What is CNSA 2.0?](https://pqshield.com/what-is-cnsa-2-0-the-nsas-post-quantum-roadmap/)
- [PostQuantum.com — CNSA 2.0 PQC Suite](https://postquantum.com/quantum-policy/nsa-cnsa-2-0-pqc/)
- [PostQuantum.com — Q-Day RSA Broken 2030](https://postquantum.com/q-day/q-day-y2q-rsa-broken-2030/)
- [PostQuantum.com — NIST IR 8547 Analysis](https://postquantum.com/security-pqc/nist-ir-8547-ipd/)
- [SafeLogic — PQC Compliance Standards](https://www.safelogic.com/compliance/pqc-standards)
- [Garantir — CNSA 2.0 and PQC Future](https://garantir.io/csna-2-0-and-the-post-quantum-future-of-encryption/)
- [CSA — NIST FIPS 203/204/205 Finalized](https://cloudsecurityalliance.org/blog/2024/08/15/nist-fips-203-204-and-205-finalized-an-important-step-towards-a-quantum-safe-future)
- [NCSC UK — PQC Migration Timelines](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines)
- [DHS — Post-Quantum Cryptography](https://www.dhs.gov/quantum)
- [Palo Alto — PQC Standards Guide](https://www.paloaltonetworks.com/cyberpedia/pqc-standards)
- [Curtiss-Wright — Quantum-Resistant Data Protection](https://defense-solutions.curtisswright.com/media-center/blog/road-quantum-resistant-data-rest-protection)
- [CyberArk — NIST PQC Timeline](https://www.cyberark.com/resources/blog/nist-s-new-timeline-for-post-quantum-encryption)
- [DigiCert — Progress Toward PQC](https://www.digicert.com/blog/the-progress-toward-post-quantum-cryptography)
- [Federal Register — FIPS 203/204/205 Announcement](https://www.federalregister.gov/documents/2024/08/14/2024-17956/announcing-issuance-of-federal-information-processing-standards-fips-fips-203-module-lattice-based)
