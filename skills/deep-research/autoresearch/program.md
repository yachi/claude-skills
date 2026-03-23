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

## Binary Eval Suite (8 criteria, max score = 8 per run)

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

## Mutation Strategy

- If E1 fails: Add emphasis on "search multiple queries per sub-question" or "use WebSearch aggressively"
- If E2 fails: Strengthen the confidence calibration section, make it more prominent
- If E3 fails: Add explicit instruction to "always include at least one comparison table"
- If E4 fails: Add emphasis on "cite standards by specific section number, not just name"
- If E5 fails: Strengthen the Implementation Guidance phase, add examples of what good guidance looks like

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
- **Score:** {X}/5 (E1:{0|1} E2:{0|1} E3:{0|1} E4:{0|1} E5:{0|1})
- **Mutation:** {what was changed, or "baseline"}
- **Result:** {kept | discarded}
- **Champion score:** {current best}
```
