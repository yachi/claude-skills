## Judge Assessment: run-75.md

| Criterion | Score | Justification |
|-----------|-------|---------------|
| C1 Accuracy | 4/5 | All three fact-checked claims verified correctly; minor issue: the report says MDMA had "Phase 2" large effect sizes (d=0.9) but the Phase 3 trial was the one showing 70%+ remission — the Phase 2/3 distinction is slightly muddled, and "methodological concerns" understates the severity (advisory committee voted 9-2 against efficacy, plus research integrity/retraction issues). |
| C2 Recommendation | 5/5 | Clear tiered recommendation (PE primary, CPT co-primary, EMDR adjunctive) with explicit change triggers, patient-matching protocol, and conditions under which the recommendation would shift — ready to act on. |
| C3 Completeness | 4/5 | Covers efficacy, dropout, cost, guidelines, alternatives, and adversarial review thoroughly; minor gap in not discussing comorbidity considerations (TBI, substance use disorder) which are highly prevalent in combat veterans and affect treatment selection. |
| C4 Honesty | 5/5 | Confidence is explicitly stated at 78%, assumptions are audited in a dedicated table, EMDR evidence gaps are clearly acknowledged, and the report distinguishes between statistical and clinical significance. |
| C5 Actionability | 5/5 | Provides phased implementation timeline, patient matching protocol, training resources with URLs, cost estimates per clinician program, and specific fallback criteria (e.g., pivot if dropout exceeds 60%). |
| **TOTAL** | **23/25** | |

### Fact-Check Details
- Claim 1: "PE achieved SMD = 0.99 (95% CI: 0.89-1.08) on CAPS-5, versus CPT's SMD = 0.71 (95% CI: 0.61-0.80). The between-group difference (SMD = 0.17) was statistically significant" — Verified: **YES** — Schnurr et al. 2022 in JAMA Network Open reports exactly these effect sizes and the 0.17 between-group difference for the N=916 veteran RCT ([PubMed](https://pubmed.ncbi.nlm.nih.gov/35044471/)).
- Claim 2: "MDMA-assisted therapy... FDA declined approval in August 2024 citing methodological concerns" — Verified: **PARTIALLY** — FDA did issue a Complete Response Letter on August 9, 2024 declining approval. However, the concerns went beyond "methodological" — the advisory committee voted 9-2 against efficacy and 10-1 against the benefit-risk profile, and three related papers were retracted for research integrity issues the next day. "Methodological concerns" is an understatement ([NPR](https://www.npr.org/sections/shots-health-news/2024/08/09/nx-s1-5068634/mdma-therapy-fda-decision-ptsd-psychedelic-treatment)).
- Claim 3: "The 2017 APA guideline rated EMDR as 'conditional' (vs 'strong' for PE and CPT)" — Verified: **YES** — The APA 2017 CPG gave strong recommendations for CBT, CPT, CT, and PE, and a conditional recommendation for EMDR. The guideline panel noted future reviews could upgrade EMDR to strong ([APA](https://www.apa.org/ptsd-guideline)).

### Critical Issues (if any)
- The MDMA characterization slightly downplays the severity of the FDA rejection. The advisory committee vote was strongly against (9-2 on efficacy, 10-1 on benefit-risk), and research integrity concerns (retracted papers) were a significant factor beyond mere "methodological concerns."
- The Python code block uses a simplistic ITT model (response_rate * (1 - dropout)) that does not reflect actual ITT analysis methodology. Real ITT analyses use imputation or mixed models, not simple multiplication. The numbers should be presented as illustrative rather than authoritative.

### Missing Angles
- **Comorbidity considerations**: Combat veterans frequently present with TBI (20-30% co-occurrence), substance use disorders, and chronic pain. These comorbidities significantly affect treatment selection (e.g., CPT may be preferred over PE for veterans with TBI due to cognitive demands of imaginal exposure).
- **Telehealth delivery**: Post-COVID, VA has expanded telehealth significantly. The report does not discuss evidence for telehealth-delivered PE/CPT/EMDR, which is now a major delivery modality.
- **Cultural and demographic factors**: No discussion of how race, gender, military branch, or era of service might influence treatment response or preference.
- **Therapist supply constraints**: The report mentions training but does not address the well-documented VA therapist shortage and how that practically constrains offering all three modalities.
