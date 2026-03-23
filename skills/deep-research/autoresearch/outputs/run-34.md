# Designing a Voting System: E2E Verifiable, Perfect Ballot Secrecy, Universal Accessibility, Under $2/Vote, Nation-State Resistant

## Executive Summary

**The five requirements as stated are simultaneously unsatisfiable.** This is not an engineering failure — it is a mathematical and economic impossibility under current technology. The core tensions: (1) "perfect ballot secrecy" conflicts with "end-to-end verifiable" — cryptographic E2E systems achieve computational ballot secrecy (breakable in theory given sufficient resources), not perfect/information-theoretic secrecy; (2) "$2/vote" is approximately 63% below the current US average of $5.47/vote ([MIT Election Lab](https://electionlab.mit.edu/sites/default/files/2022-05/TheCostofConductingElections-2022.pdf)) and would require eliminating paper ballots, which conflicts with nation-state resistance; (3) accessibility "including those without internet" requires a physical polling infrastructure that drives costs above $2/vote. However, a **near-optimal system achieving 4 of 5 requirements at $4-6/vote** is feasible using a hybrid paper-ballot + E2E-verifiable design with risk-limiting audits (RLAs). **Confidence: 92%** that the five requirements are simultaneously unsatisfiable; **75%** that the recommended hybrid system achieves the best feasible tradeoff.

## Premise Challenge: The Five Requirements Form an Impossible Pentagon

The prompt asks for a system that is simultaneously:

1. **End-to-end verifiable** (voters can confirm their vote was counted correctly)
2. **Perfect ballot secrecy** (no one, including the voter, can prove how they voted)
3. **Accessible to all voters including those without internet**
4. **Costs under $2/vote**
5. **Resistant to nation-state attacks**

These requirements contain at least three formal contradictions:

### Contradiction 1: E2E Verifiability vs. Perfect Ballot Secrecy

E2E verifiability requires that the voter receive some evidence (a receipt, a verification code) that their vote was counted as cast. **Perfect** ballot secrecy (in the information-theoretic sense) requires that no such evidence exists. Cryptographic E2E systems (Helios, Scantegrity, STAR-Vote) achieve **computational** ballot secrecy — an adversary cannot determine how you voted unless they break the underlying cryptographic assumptions. But this is not "perfect" — it is computationally bounded. A nation-state adversary with quantum computing capability could break current cryptographic assumptions in 10-20 years ([EAC E2E Protocol](https://www.eac.gov/voting-equipment/end-end-e2e-protocol-evaluation-process)).

**Formal statement:** E2E verifiability requires individual verifiability (voter can check their vote is in the tally). Receipt-freeness requires that the voter cannot prove to a coercer how they voted. These are achievable simultaneously via commitment schemes. But **perfect** (information-theoretic) secrecy is a stronger requirement that cannot coexist with any form of individual verification ([Wikipedia/E2E Voting](https://en.wikipedia.org/wiki/End-to-end_auditable_voting)).

### Contradiction 2: Under $2/Vote vs. Physical Accessibility + Nation-State Resistance

The current US average cost per vote is $5.47 for federal elections ([Brennan Center](https://www.brennancenter.org/series/election-infrastructure-costs)). The components that drive costs:

| Component | Cost Per Vote (est.) | Eliminable? |
|-----------|---------------------|-------------|
| Polling place staffing | $1.50-2.50 | No (accessibility requires physical locations) |
| Paper ballots + printing | $0.30-0.50 | Only if all-electronic (contradicts nation-state resistance) |
| Voting equipment amortized | $0.50-1.50 | Only with cheaper tech |
| Post-election auditing | $0.20-0.50 | No (E2E + RLA required for nation-state resistance) |
| IT infrastructure + cybersecurity | $0.30-0.80 | No (nation-state resistance requires this) |
| Voter registration + outreach | $0.50-1.00 | Partially |
| **Minimum achievable** | **$3.30-6.80** | |

Achieving $2/vote requires eliminating either physical polling places (violates accessibility) or paper audit trails (violates nation-state resistance). **There is no configuration that achieves all three.**

### Contradiction 3: Nation-State Resistance vs. Cost

Nation-state-resistant systems require defense-in-depth: air-gapped tabulators, physical chain-of-custody, paper ballot backups, end-to-end encryption, post-election audits, and cyber hygiene training for thousands of poll workers. CISA identifies election infrastructure as critical infrastructure requiring multi-layer defense ([CISA](https://www.cisa.gov/topics/election-security)). This infrastructure has irreducible costs.

## Key Findings

1. **Current US election cost averages $5.47/vote** for federal elections, $15.62/vote for municipal elections ([MIT Election Lab](https://electionlab.mit.edu/sites/default/files/2022-05/TheCostofConductingElections-2022.pdf))
2. **No E2E-verifiable voting system is currently certified** by the EAC; VVSG 2.0 provides a pathway but no systems have completed it ([EAC](https://www.eac.gov/voting-equipment/end-end-e2e-protocol-evaluation-process))
3. **E2E systems have 58% average usability** — a 42% ballot-casting failure rate across Helios, Pret a Voter, and Scantegrity II ([USENIX](https://www.usenix.org/system/files/conference/evtwote14/jets_0203-acemyan.pdf))
4. **Risk-limiting audits (RLAs) are implemented in 17+ US states**, providing statistical confidence in election outcomes from paper ballots ([Verified Voting](https://verifiedvoting.org/audits/whatisrla/))
5. **VVSG 2.0 requires software independence** — either voter-verifiable paper records or E2E verifiability ([EAC VVSG 2.0](https://www.eac.gov/sites/default/files/TestingCertification/Voluntary_Voting_System_Guidelines_Version_2_0.pdf))
6. **Draft VVSG 2.1 (June 2025)** mandates voter-verifiable paper records even for E2E systems, per Executive Order 14248 ([EAC VVSG 2.1 Draft](https://www.eac.gov/sites/default/files/2025-06/DRAFT_Voluntary_Voting_System%20Guidelines_Version_2.1_TGDC_Member_Review.pdf))
7. **STAR-Vote (Travis County, TX)** was the most promising hybrid E2E + paper system but was abandoned due to cost and vendor availability ([USENIX STAR-Vote](https://www.usenix.org/system/files/conference/evtwote13/jets-0101-bell.pdf))
8. **ADA requires accessible voting** at every polling place for federal elections; VVPAT printers have degraded accessibility for visually impaired voters ([ADA.gov](https://www.ada.gov/resources/protecting-voter-rights/), [EFF](https://www.eff.org/wp/accessibility-and-auditability-electronic-voting))
9. **Hart InterCivic Verity Vanguard 1.0** is the first system certified to VVSG 2.0 (July 2025) ([EAC](https://www.eac.gov/news/2025/07/10/eac-announces-first-certified-voting-system-voluntary-voting-system-guidelines-vvsg))
10. **Colorado pioneered statewide RLAs** in 2017 with 5% risk limit ([Colorado SOS](https://www.sos.state.co.us/pubs/elections/RLA/faqs.html))

## Industry Standards Compliance

| Standard | Requirement | Relevance | Source |
|----------|-------------|-----------|--------|
| EAC VVSG 2.0, Principle 2 (High Quality Design) | Software independence; voter-verifiable records | Foundational requirement for any new system | [EAC VVSG 2.0 (PDF)](https://www.eac.gov/sites/default/files/TestingCertification/Voluntary_Voting_System_Guidelines_Version_2_0.pdf) |
| EAC VVSG 2.0, Principle 9 (Auditable) | System must support efficient, effective auditing | Mandates RLA compatibility | [EAC VVSG 2.0](https://www.eac.gov/voting-equipment/voluntary-voting-system-guidelines) |
| HAVA Section 301(a)(3) | Accessible voting for individuals with disabilities at each polling place | Mandatory for federal elections | [ADA.gov](https://www.ada.gov/resources/protecting-voter-rights/) |
| ADA Title II, 42 USC 12132 | State/local programs accessible to persons with disabilities | Covers all publicly administered elections | [ADA.gov](https://www.ada.gov/resources/protecting-voter-rights/) |
| CISA Election Infrastructure Security Guidelines | Multi-layer defense, risk assessment, incident response | Defines nation-state resistance baseline | [CISA](https://www.cisa.gov/topics/election-security) |
| NIST SP 1500-100 (Election Results Reporting CDF) | Common data format for election results interoperability | Enables transparent results publication | [EAC/NIST](https://www.eac.gov/voting-equipment/voluntary-voting-system-guidelines) |
| ISO/IEC 15408 (Common Criteria) | Security evaluation for IT products | Applicable to voting system component certification | [ISO](https://www.iso.org/standard/72891.html) |
| EO 14248 (March 2025) | Voter-verifiable paper records required; QR/barcode restrictions | Overrides VVSG 2.0 E2E-only path | [EAC VVSG 2.1 Draft](https://www.eac.gov/sites/default/files/2025-06/DRAFT_Voluntary_Voting_System%20Guidelines_Version_2.1_TGDC_Member_Review.pdf) |

## Quantitative Analysis

### The "Impossible Pentagon" Tradeoff Matrix

| Requirement | Achievable Alone? | Conflicts With | Relaxation Needed |
|-------------|-------------------|----------------|-------------------|
| E2E Verifiable | Yes (Helios, Scantegrity) | Perfect ballot secrecy (weakened to computational) | Accept computational secrecy |
| Perfect Ballot Secrecy | Yes (paper in locked box) | E2E verifiability | Downgrade to "receipt-freeness" |
| Universal Accessibility | Yes (polling places + assistive tech) | $2/vote (requires physical infrastructure) | Raise budget to $4-6/vote |
| Under $2/vote | Possible for online-only | Physical access, nation-state resistance | Raise to $4-6/vote |
| Nation-State Resistant | Yes (air-gapped + paper + RLA) | $2/vote (expensive infrastructure) | Accept that security has a cost |

### Feasibility Score by Design Choice

| System Design | E2E Verifiable | Ballot Secrecy | Accessible | Cost/Vote | Nation-State Resistant | Score |
|--------------|---------------|----------------|------------|-----------|----------------------|-------|
| Paper-only (hand count) | No | Yes (perfect) | Yes | $3-8 | Yes | 3/5 |
| DRE touchscreen (no paper) | No | No (coercion possible) | Partial | $2-4 | No | 1/5 |
| Optical scan + RLA | No (not E2E) | Yes | Yes | $4-6 | Yes | 3/5 |
| **Hybrid: BMD + paper + E2E** | Yes (computational) | Computational | Yes | $5-8 | Yes | **4/5** |
| Online-only (Helios-style) | Yes | Computational | No (internet required) | $0.50-2 | No | 2/5 |
| Blockchain voting | Partial | No | No | $1-3 | No | 1/5 |

### Recommended System: Hybrid BMD + Paper + E2E + RLA

```
┌─────────────────────────────────────────────────────────┐
│            NEAR-OPTIMAL VOTING SYSTEM DESIGN             │
│                                                          │
│  CAST PHASE (Polling Place)                              │
│  ├── Voter uses Ballot Marking Device (BMD)              │
│  │   ├── Touchscreen with audio/sip-puff accessibility   │
│  │   ├── Generates human-readable paper ballot           │
│  │   └── Generates encrypted E2E commitment (QR code)    │
│  ├── Voter verifies paper ballot (human-readable text)   │
│  ├── Voter deposits paper ballot in sealed ballot box    │
│  └── Voter receives E2E verification receipt             │
│      (cryptographic commitment, not vote content)        │
│                                                          │
│  TALLY PHASE (Central Count)                             │
│  ├── Optical scanner tabulates paper ballots             │
│  ├── E2E cryptographic tally computed independently      │
│  ├── Paper tally and crypto tally must match             │
│  └── Discrepancy triggers full hand count                │
│                                                          │
│  AUDIT PHASE (Post-Election)                             │
│  ├── Risk-Limiting Audit (5% risk limit)                 │
│  │   ├── Random sample of paper ballots                  │
│  │   ├── Compare to scanner results                      │
│  │   └── Statistical proof of correct outcome            │
│  ├── E2E Bulletin Board published                        │
│  │   ├── All encrypted ballots posted publicly           │
│  │   ├── Voters verify their commitment appears          │
│  │   └── Anyone can verify cryptographic tally           │
│  └── Full paper trail preserved for 22 months (52 USC    │
│      §20701)                                             │
│                                                          │
│  ACCESSIBILITY LAYER                                     │
│  ├── Physical polling places (HAVA §301(a)(3))           │
│  ├── BMD with audio, high-contrast, sip-puff             │
│  ├── Mail-in paper ballots (no internet needed)          │
│  ├── Curbside voting                                     │
│  └── Absentee ballot with accessible overlay             │
│                                                          │
│  SECURITY LAYER                                          │
│  ├── Air-gapped tabulators (no network connection)       │
│  ├── Pre-election Logic & Accuracy testing               │
│  ├── Chain-of-custody seals on ballot containers         │
│  ├── Bipartisan observation at all stages                │
│  ├── CISA-aligned cyber hygiene for registration DBs     │
│  └── Hardware Security Modules for E2E crypto keys       │
└─────────────────────────────────────────────────────────┘
```

### Cost Estimate for Recommended System

| Component | Cost Per Vote | Notes |
|-----------|--------------|-------|
| BMD hardware (amortized 10 years) | $0.80-1.50 | $3,000-5,000 per unit, ~500 voters/unit/election |
| Paper ballots + printing | $0.30-0.50 | Premium security paper with anti-counterfeit features |
| Optical scanner (amortized 10 years) | $0.20-0.40 | High-speed central count |
| E2E crypto infrastructure | $0.10-0.30 | HSMs, bulletin board server, key ceremony |
| Poll worker staffing | $1.50-2.50 | Mandatory for accessibility |
| RLA audit costs | $0.15-0.30 | Statistical sampling, bipartisan teams |
| IT/cybersecurity | $0.30-0.60 | CISA-aligned infrastructure |
| Voter outreach + training | $0.30-0.50 | E2E verification requires voter education |
| **Total** | **$3.65-6.60** | **Cannot reach $2 without cutting accessibility or security** |

## Implementation Guidance

### What $2/Vote Actually Gets You

If the $2/vote constraint is immovable, the following must be sacrificed:

| $2/Vote System | What You Get | What You Lose |
|---------------|--------------|---------------|
| Online-only E2E (Helios) | E2E verifiable, computational secrecy, low cost | No accessibility for non-internet voters; no nation-state resistance (internet voting is insecure per AAAS ([AAAS](https://www.aaas.org/epi-center/internet-online-voting))) |
| Minimalist paper + volunteers | Accessible, nation-state resistant | No E2E; limited secrecy enforcement |
| Mail-only + RLA | Accessible, cheap, auditable | No E2E; slow; secrecy depends on postal handling |

### If Budget Can Be Raised to $4-6/Vote

The recommended hybrid system becomes viable. Implementation sequence:

```bash
# Phase 1: Pilot (Year 1, 5 jurisdictions)
# - Deploy BMD + paper + E2E in municipal elections
# - Partner with EAC for VVSG 2.0/2.1 evaluation
# - Measure: usability (>90% success rate), cost/vote, audit efficiency
# Estimated cost: $2-5M for pilot

# Phase 2: Certification (Years 2-3)
# - Submit E2E protocol to EAC evaluation process
# - NIST review and public comment period (~12 months)
# - Obtain VVSG 2.0 certification
# Estimated cost: $1-3M

# Phase 3: Statewide deployment (Years 3-5)
# - Procure certified systems for all jurisdictions
# - Train poll workers on E2E + RLA procedures
# - Conduct parallel elections (old + new) for validation
# Estimated cost: $50-200M per state (varies by size)
```

### Technology Readiness Assessment

| Technology | TRL | Deployed? | Largest Deployment | Source |
|-----------|-----|-----------|-------------------|--------|
| Optical scan + RLA | 9 | Yes | Colorado (statewide since 2017) | [CO SOS](https://www.sos.state.co.us/pubs/elections/RLA/faqs.html) |
| BMD with paper trail | 9 | Yes | Georgia (statewide) | [EAC](https://www.eac.gov/voting-equipment/voluntary-voting-system-guidelines) |
| Scantegrity II (E2E) | 6 | Limited | Takoma Park, MD (2009, 2011) | [Wikipedia](https://en.wikipedia.org/wiki/End-to-end_auditable_voting) |
| Helios (online E2E) | 7 | Limited | IACR elections, university votes | [Helios](https://vote.heliosvoting.org/faq) |
| STAR-Vote (hybrid E2E) | 4 | Never deployed | Travis County design only | [USENIX](https://www.usenix.org/system/files/conference/evtwote13/jets-0101-bell.pdf) |
| Blockchain voting | 3 | Experimental | West Virginia (military, discontinued) | Industry |

## Alternatives Considered

| System | E2E | Secrecy | Access | Cost/Vote | Nation-State | Overall |
|--------|-----|---------|--------|-----------|-------------|---------|
| **Hybrid BMD+E2E+RLA (rec.)** | Yes | Computational | Yes | $4-6 | Yes | Best feasible |
| Paper + hand count only | No | Perfect | Yes | $6-15 | Yes | No E2E, expensive |
| Online E2E (Helios) | Yes | Computational | No | $0.50-2 | No | Insecure, exclusionary |
| DRE + VVPAT | No | Weak | Partial | $3-5 | Partial | No E2E, accessibility concerns |
| Blockchain + mobile | Partial | No | No | $1-3 | No | Worst overall |

## Adversarial Review

### Counterargument 1: "E2E verifiability and ballot secrecy ARE simultaneously achievable — modern cryptography solves this"

**Evidence:** Academic literature on commitment schemes, mix-nets, and homomorphic encryption demonstrates that E2E verifiability and receipt-freeness can coexist ([Wikipedia/E2E Voting](https://en.wikipedia.org/wiki/End-to-end_auditable_voting)). Systems like Helios use El Gamal encryption to encrypt ballots such that individual votes are hidden while the aggregate tally is verifiable.

**Rebuttal:** This counterargument conflates computational secrecy with perfect secrecy. We agree that computational ballot secrecy + E2E verifiability is achievable — this is what our recommended system provides. The prompt asks for "perfect ballot secrecy," which in information-theoretic terms means no amount of computational power can reveal a vote. This is incompatible with any system that gives the voter verifiable evidence. If the prompt is interpreted as "receipt-freeness" (voter cannot prove to a third party how they voted), then yes, both properties can coexist — and our recommendation achieves this. The distinction between "perfect secrecy" and "computational secrecy/receipt-freeness" is critical.

### Counterargument 2: "Developing nations run elections for well under $2/vote — the cost constraint is achievable"

**Evidence:** India's 2024 general election cost approximately $0.50-1.00/vote for 900M+ voters, using simple Electronic Voting Machines (EVMs) with VVPAT. Many African nations conduct elections for under $1/vote with paper ballots.

**Rebuttal:** These systems achieve low cost by sacrificing one or more of the other requirements: Indian EVMs are not E2E verifiable (they are proprietary and controversial); most low-cost elections have no nation-state-resistant audit infrastructure; and accessibility standards vary dramatically. The $2/vote target is achievable IF you accept a system that is not E2E verifiable and not nation-state resistant — essentially a basic paper ballot election. The cost constraint is only impossible in combination with the other four requirements.

### Counterargument 3: "Nation-state resistance is theater — no voting system can resist a determined nation-state attacker"

**Evidence:** Russia's 2016 interference targeted voter registration databases, not vote tallying. China, Iran, and other nation-states have sophisticated cyber capabilities. Supply chain attacks (e.g., on voting machine firmware) are extremely difficult to detect. Some security researchers argue that "nation-state resistant" is an impossible standard for any civilian system.

**Rebuttal:** Partially valid — "resistance" is not "immunity." However, the combination of paper ballots + RLAs + air-gapped tabulators + E2E verifiability creates defense-in-depth that makes vote manipulation detectable even if not preventable. The paper ballot is the ultimate air gap — a nation-state can hack the electronic systems, but the paper ballots (verified by voters) serve as the ground truth. The goal is detection and correction, not prevention. This is the philosophy behind CISA's approach and the VVSG 2.0 software independence requirement. We adjust our language from "resistant" to "resilient with high probability of detection."

### Assumption Audit

| Assumption | Status | Risk if Wrong |
|------------|--------|---------------|
| Perfect ballot secrecy means information-theoretic | Reasonable interpretation | Low — if interpreted as receipt-freeness, system is more achievable |
| $5.47/vote is the US baseline | Verified (MIT Election Lab data) | Low — well-documented |
| E2E usability can be improved from 58% | Uncertain — no deployed improvements yet | High — if usability stays at 58%, system is impractical |
| VVSG 2.0 E2E pathway will materialize | Uncertain — no systems certified yet | Medium — may take 5-10 years |
| RLAs provide nation-state-level assurance | Reasonable — statistical guarantees are strong | Low — math doesn't care about the attacker's budget |
| Quantum computing won't break E2E crypto in 10 years | Uncertain | High — would destroy computational ballot secrecy |

<details>
<summary>Failure Mode Analysis</summary>

**Mode 1: Usability failure** — If E2E verification is too complex for average voters, the "verifiable" property becomes theoretical only. Scantegrity/Helios usability studies show 42% failure rates ([USENIX](https://www.usenix.org/system/files/conference/evtwote14/jets_0203-acemyan.pdf)). Mitigation: extensive UX research; simplified verification (scan QR, see confirmation).

**Mode 2: Quantum threat** — Post-quantum cryptography is not yet standardized for voting systems. If quantum computers arrive before PQC migration, E2E cryptographic guarantees collapse. Mitigation: crypto-agile design; lattice-based fallback.

**Mode 3: Political resistance** — Election officials may resist E2E complexity. STAR-Vote was abandoned partly because no vendor would build it. Mitigation: federal funding, EAC certification pathway, open-source reference implementation.

**Mode 4: Accessibility regression** — E2E systems with QR codes and verification receipts may be inaccessible to blind/low-vision voters, contradicting HAVA Section 301. VVPAT already degrades accessibility ([EFF](https://www.eff.org/wp/accessibility-and-auditability-electronic-voting)). Mitigation: audio verification channel; tactile receipt; universal design.

</details>

## Recommendation

**The five requirements are simultaneously unsatisfiable. The best achievable system scores 4/5 at $4-6/vote.**

1. **Accept computational ballot secrecy** (receipt-freeness) instead of perfect information-theoretic secrecy. This is the standard achieved by all E2E voting systems and is sufficient for democratic purposes.

2. **Accept $4-6/vote** instead of $2/vote. The irreducible costs of physical polling infrastructure (for accessibility) and security infrastructure (for nation-state resilience) make $2/vote impossible when combined with E2E verifiability.

3. **Deploy the hybrid BMD + paper + E2E + RLA system** as described above. This achieves: E2E verifiability (computational), receipt-freeness, universal accessibility, nation-state resilience, and the lowest achievable cost for this feature set.

4. **Pilot in 5 jurisdictions**, seek EAC VVSG 2.0 E2E protocol evaluation, and plan for 5-year statewide deployment.

**Confidence: 92%** that the five requirements cannot be simultaneously met. **75%** that the recommended hybrid system is the best feasible tradeoff. **60%** that E2E voting systems will be EAC-certified within 10 years.

**This recommendation changes if:**
- Quantum-resistant E2E protocols mature and are standardized (changes crypto assumptions)
- Federal funding reduces per-jurisdiction costs below $2/vote through national infrastructure
- Information-theoretic E2E protocols are developed (theoretical breakthrough)

## Sources

- [MIT Election Lab — The Cost of Conducting Elections](https://electionlab.mit.edu/sites/default/files/2022-05/TheCostofConductingElections-2022.pdf)
- [Brennan Center — Costs for Replacing Voting Equipment 2024](https://www.brennancenter.org/our-work/analysis-opinion/costs-replacing-voting-equipment-2024)
- [Brennan Center — Election Infrastructure Costs Series](https://www.brennancenter.org/series/election-infrastructure-costs)
- [EAC — Voluntary Voting System Guidelines](https://www.eac.gov/voting-equipment/voluntary-voting-system-guidelines)
- [EAC — VVSG 2.0 (PDF)](https://www.eac.gov/sites/default/files/TestingCertification/Voluntary_Voting_System_Guidelines_Version_2_0.pdf)
- [EAC — VVSG 2.1 Draft (PDF)](https://www.eac.gov/sites/default/files/2025-06/DRAFT_Voluntary_Voting_System%20Guidelines_Version_2.1_TGDC_Member_Review.pdf)
- [EAC — E2E Protocol Evaluation Process](https://www.eac.gov/voting-equipment/end-end-e2e-protocol-evaluation-process)
- [EAC — First VVSG 2.0 Certification (July 2025)](https://www.eac.gov/news/2025/07/10/eac-announces-first-certified-voting-system-voluntary-voting-system-guidelines-vvsg)
- [EAC — Election Security Preparedness](https://www.eac.gov/election-officials/election-security-preparedness)
- [CISA — Election Security](https://www.cisa.gov/topics/election-security)
- [CISA — Cybersecurity Toolkit for Elections](https://www.cisa.gov/cybersecurity-toolkit-and-resources-protect-elections)
- [Wikipedia — End-to-End Auditable Voting](https://en.wikipedia.org/wiki/End-to-end_auditable_voting)
- [USENIX — Usability of E2E Systems (Helios, Pret a Voter, Scantegrity)](https://www.usenix.org/system/files/conference/evtwote14/jets_0203-acemyan.pdf)
- [USENIX — STAR-Vote Design](https://www.usenix.org/system/files/conference/evtwote13/jets-0101-bell.pdf)
- [Rice University — STAR-Vote Summative Report (PDF)](https://www.cs.rice.edu/~dwallach/pub/star-summative-2018.pdf)
- [Helios Voting — FAQ](https://vote.heliosvoting.org/faq)
- [Verified Voting — What is an RLA?](https://verifiedvoting.org/audits/whatisrla/)
- [Wikipedia — Risk-Limiting Audit](https://en.wikipedia.org/wiki/Risk-limiting_audit)
- [Colorado SOS — RLA FAQs](https://www.sos.state.co.us/pubs/elections/RLA/faqs.html)
- [NCSL — Risk-Limiting Audits](https://www.ncsl.org/elections-and-campaigns/risk-limiting-audits)
- [UC Berkeley/Stark — RLA White Paper (PDF)](https://www.stat.berkeley.edu/~stark/Preprints/RLAwhitepaper12.pdf)
- [ADA.gov — Protecting Voter Rights](https://www.ada.gov/resources/protecting-voter-rights/)
- [EFF — Accessibility and Auditability in Electronic Voting](https://www.eff.org/wp/accessibility-and-auditability-electronic-voting)
- [EAC — Voting Accessibility](https://www.eac.gov/voting-accessibility)
- [AAAS — Internet Voting Remains Insecure](https://www.aaas.org/epi-center/internet-online-voting)
- [US Vote Foundation — E2E-VIV Project](https://www.usvotefoundation.org/E2E-VIV)
- [Bipartisan Policy Center — VVSG Explainer](https://bipartisanpolicy.org/explainer/what-are-the-federal-voluntary-voting-system-guidelines/)
- [Secure World — Mandating E2E Verifiable Voting](https://www.secureworld.io/industry-news/end-to-end-verifiable-voting-systems-usa-elections)
- [EAC Funding Memo (PDF)](https://www.eac.gov/sites/default/files/2025-04/Funding_Election_Administration_Memo_508.pdf)
