# Auto-Research Program for /dr Skill

You are an autonomous skill optimizer. Your job is to improve the `/dr` deep research skill by running it on test prompts, grading the outputs with binary evals, and mutating the skill prompt to maximize the score.

## The Loop

1. **Read** the current skill at `skill/SKILL.md`
2. **Pick a test prompt** from the test set (rotate through them)
3. **Spawn a subagent** that reads the skill, then executes it on the test prompt. The subagent should use WebSearch and other tools as the skill instructs. Save output to `autoresearch/outputs/run-{N}.md`
4. **Grade** the output using the binary eval suite (see below). Each criterion is YES (1) or NO (0). Record the score.
5. **Compare** to the current best score. If this run's score is higher, the current skill version is the new champion.
6. **Mutate** the skill prompt. Make ONE targeted change based on which eval criteria failed. Don't rewrite the whole thing — surgical edits only. Save the mutated version.
7. **Log** the run: iteration number, test prompt used, score, what was changed, whether it was kept or discarded.
8. **Repeat** from step 2.

## Test Prompts (rotate through these)

### Easy (baseline sanity check)
1. "Should I use Kafka or RabbitMQ for a microservices event bus handling 50K messages/sec with exactly-once delivery requirements?"

### Medium (multi-domain, requires cross-cutting research)
2. "We're building a real-time bidding (RTB) ad exchange that must process 1M bid requests/sec at <10ms p99. We need to be GDPR/CCPA compliant, handle PII in bid streams, and run on a $50K/month infrastructure budget. Evaluate whether to build on Aerospike+Kafka vs Redis+NATS vs a managed cloud solution."
3. "Our fintech startup is choosing between building on Solana vs Ethereum L2s (Arbitrum/Base) for a non-custodial lending protocol. We need to handle $100M+ TVL, pass a smart contract audit, comply with MiCA regulations in the EU, and ship in 6 months with a team of 4 Rust developers."

### Hard (ambiguous premise, adversarial, requires premise validation)
4. "Everyone says microservices are the way to go but we're a 3-person team building a B2B invoicing SaaS. We currently have a Rails monolith serving 200 customers. Our investor is pushing us to 'modernize the architecture' before Series A. Should we migrate to microservices? What does the data actually say about monolith vs microservices at our scale?"
5. "I want to replace our PostgreSQL database with a blockchain-based storage layer for 'immutable audit trails' in our healthcare compliance system. Our CTO says this is the future. Is it? We process 10K patient records/day and need HIPAA compliance."

### Adversarial (tests premise kill-switch + multi-perspective framing)
6. "Prove that Rust is always faster than Go for web services. I need data to convince my team to rewrite our Go services."

### Expert Delegation (tests multi-perspective research — E12/E13/E14)
10. "Our fintech startup is building a cross-border payment system handling EUR/USD/GBP corridors. We need to comply with PSD2 (EU), FinCEN MSB registration (US), and FCA authorization (UK) simultaneously. Tech stack is Go + PostgreSQL. Team of 6, launching in 9 months. Budget: $500K. Should we build on top of an existing BaaS provider (Stripe Treasury, Column, Modulr) or build our own ledger with direct banking integrations?"
11. "We're designing a telemedicine platform for rural Sub-Saharan Africa. Must work on 2G/3G networks, handle patient data under GDPR (EU-based company), Kenya's Data Protection Act, and Nigeria's NDPR. Needs offline-first capability, integration with national health ID systems, and support for community health workers with basic smartphones. Tech decision: React Native vs Flutter vs PWA. Budget: $200K for MVP."
12. "Our SaaS company ($20M ARR, 500 enterprise customers) stores data in US-East AWS. We're expanding to Japan, Germany, and Brazil. Each country has different data residency requirements (APPI, BDSG/GDPR, LGPD). Need to architect multi-region data strategy under $50K/month additional. Current stack: Python/Django, PostgreSQL, Redis, S3. AWS region replication vs multi-cloud vs CDN-edge?"

### Convergence (tests iterative refinement loop — E9/E10/E11)
7. "Is server-side rendering (SSR) or client-side rendering (CSR) better for SEO in 2025+? I've seen conflicting claims — some say Google now fully renders JavaScript SPAs, others say SSR is still critical. I need a definitive, evidence-based answer with current data, not opinions from 2020."
8. "We're building a real-time collaborative document editor (like Google Docs) for a 50-person company. Should we use CRDTs or Operational Transform? We need offline support, the backend is in Go, and we're a 3-person team. Budget is $0 for infrastructure — everything self-hosted on a single VPS."
9. "Should we migrate our 200-microservice Kubernetes cluster from AWS EKS to bare-metal Kubernetes to save costs? We're spending $180K/month on AWS. Team of 8 engineers, 2 with bare-metal experience. We handle PCI-DSS cardholder data. Current p99 latency is 45ms, SLA requires 99.95% uptime."

## Binary Eval Suite (14 criteria, max score = 14 per run)

Grade each YES=1, NO=0. No partial credit.

| # | Criterion | Pass condition |
|---|-----------|---------------|
| E1 | **Has 15+ verifiable URLs** | Count unique URLs. If >= 15, YES. |
| E2 | **States confidence as a number** | Contains a percentage like "85%" or "Confidence: 78%". Not just "High" or "Strong". |
| E3 | **Has comparison table** | Contains a markdown table comparing 2+ options with 3+ dimensions. |
| E4 | **Cites a standard by section** | References a specific standard with clause/section/article number (e.g., "ISO 27001 A.8.9", "RFC 7540 Section 3.2", "GDPR Art. 46"). |
| E5 | **Has implementation guidance** | Contains a code block, CLI command, config example, or specific tool name with version. Not just "use X" but how to use X. |
| E6 | **Challenges the premise if flawed** | If the question contains a false assumption or debatable premise, the output must explicitly identify and challenge it (not just go along). For prompts without a flawed premise, auto-pass. |
| E7 | **Has cost/TCO analysis** | Contains monetary figures ($, EUR, GBP, JPY, or any currency with numbers), pricing data, or total cost of ownership estimate. Not just "expensive" but actual numbers. |
| E8 | **Has adversarial counterargument** | Contains at least one explicitly labeled counterargument with evidence AND a rebuttal. Not just "some disagree" but a structured argument-evidence-rebuttal. |
| E9 | **Shows iterative refinement** | Contains evidence of self-driven research iteration: "Refinement Round", "upon further investigation", "gap analysis", "follow-up investigation", "deeper investigation", "updating research plan", "surfaced during research", or similar markers showing the agent looped back to investigate gaps rather than stopping after one pass. |
| E10 | **Resolves contradictions between sources** | When sources conflict, explicitly identifies the contradiction ("Source A claims X, but Source B shows Y") and resolves it with additional evidence rather than leaving it unresolved or silently picking one. |
| E11 | **Assumptions fully investigated** | Every assumption classified as "uncertain" in the assumption audit has a follow-up investigation attempt. Zero uncertain assumptions are left uninvestigated — they're either resolved to "verified"/"reasonable" or explicitly noted as limitations with explanation of what would resolve them. |
| E12 | **Multi-perspective synthesis** | Output shows 3+ distinct domain perspectives explicitly identified (e.g., "regulatory analysis", "technical perspective", "financial assessment"). Each perspective contributes unique findings. Evidence of parallel expert research, not sequential single-threaded analysis. |
| E13 | **Cross-domain constraint interaction** | When the question involves multiple constraints or domains, the output addresses how they interact (tensions, tradeoffs, compounding effects) rather than analyzing each in isolation. Contains terms like "interaction", "combined effect", "cross-cutting", "simultaneously comply". |
| E14 | **Multi-jurisdiction/domain depth** | References specific provisions from 3+ distinct regulatory frameworks, standards bodies, or knowledge domains — not just naming them but citing specific articles, sections, or clauses from each. |

## Mutation Strategy

- If E1 fails: Add emphasis on "search multiple queries per sub-question" or "use WebSearch aggressively"
- If E2 fails: Strengthen the confidence calibration section, make it more prominent
- If E3 fails: Add explicit instruction to "always include at least one comparison table"
- If E4 fails: Add emphasis on "cite standards by specific section number, not just name"
- If E5 fails: Strengthen the Implementation Guidance phase, add examples of what good guidance looks like
- If E9 fails: Add a convergence loop phase that checks for gaps (unverified claims, uncertain assumptions, low confidence, unresolved contradictions, emergent sub-questions) and loops back to investigate them before writing the final deliverable
- If E10 fails: Add explicit instruction to identify and resolve source contradictions with additional evidence rather than ignoring them
- If E11 fails: Strengthen the assumption audit to require follow-up investigation of all uncertain assumptions
- If E12 fails: Add instruction to spawn domain expert subagents for cross-domain questions (e.g., regulatory expert, technical architect, financial analyst) and synthesize their findings with explicit perspective labels
- If E13 fails: Add instruction to analyze constraint interactions rather than treating each constraint independently
- If E14 fails: Add instruction to cite specific provisions (article/section numbers) from each jurisdiction or standard, not just the name

**Rules for mutations:**
- Change ONE thing at a time (isolate variables)
- Never delete core phases — only refine wording within them
- Keep the skill under 200 lines
- If 3 consecutive mutations don't improve score, revert to the last champion and try a different mutation strategy

## Logging

Append each run to `autoresearch/log.md`:

```
## Run {N} — {timestamp}
- **Test prompt:** {which one}
- **Score:** {X}/14 (E1-E14)
- **Mutation:** {what was changed, or "baseline"}
- **Result:** {kept | discarded}
- **Champion score:** {current best}
```
