## Judge Assessment: run-85.md

| Criterion | Score | Justification |
|-----------|-------|---------------|
| C1 Accuracy | 5/5 | All three fact-checked claims verified correctly: Broadie-Jain citation, vega/variance notional conversion, and DDKZ 1999 replication methodology are all accurate per primary sources. |
| C2 Recommendation | 5/5 | Clear recommendation (log contract + Broadie-Jain correction), with explicit conditions for when it changes (single-name vs index, term structure inversion, monitoring frequency), and specific numerical thresholds. |
| C3 Completeness | 4/5 | Covers pricing theory, discrete correction, implementation code, trade execution, alternatives, and risk comprehensively; minor gap in not discussing the variance risk premium (VRP) — the systematic difference between implied and realized variance that drives most variance swap trading decisions. |
| C4 Honesty | 5/5 | Confidence explicitly stated at 82%, assumption audit with 6 classified assumptions, [unverified] tag used appropriately for bid-ask spread estimate, and uncertainty about jump impact clearly stated. |
| C5 Actionability | 5/5 | Two complete Python implementations (log contract pricer + replication portfolio builder), ISDA documentation references, trade execution checklist with cap/margin specifics, P&L scenario table, and CBOE VA futures alternative. |
| **TOTAL** | **24/25** | |

### Fact-Check Details
- Claim 1: "Broadie and Jain (2008, International Journal of Theoretical and Applied Finance, Vol. 11, No. 8, pp. 761-797)" — Verified: **YES** — WorldScientific confirms exact journal, volume, issue, and page numbers ([source](https://www.worldscientific.com/doi/abs/10.1142/S0219024908005032)).
- Claim 2: "Variance Notional = Vega Notional / (2 x K_vol)" — Verified: **YES** — Multiple sources (BreakingDownFinance, Wikipedia, Bossu et al.) confirm this standard conversion formula ([source](https://breakingdownfinance.com/finance-topics/derivative-valuation/vega-notional-of-a-variance-swap/)).
- Claim 3: "Demeterfi, Derman, Kamal, and Zou (1999)... portfolio of standard options with weights 1/K²" — Verified: **YES** — The Goldman Sachs QSR Notes paper is available at emanuelderman.com and confirmed by multiple academic citations ([source](https://emanuelderman.com/wp-content/uploads/1999/02/gs-volatility_swaps.pdf)).

### Critical Issues (if any)
- None. The pricing framework is mathematically sound and follows standard quantitative finance practice.

### Missing Angles
- **Variance risk premium (VRP)**: The report prices the swap at fair value but doesn't discuss that implied variance systematically exceeds realized variance by ~2-4 vol points historically (the VRP), which is the primary driver of variance swap trading strategies. A practitioner would want to know the historical VRP to decide whether to go long or short.
- **Correlation with other risk factors**: No discussion of how variance swap P&L correlates with equity returns (negative gamma), or how to hedge the vega/volga/vanna exposures of the replication portfolio.
- **Regulatory reporting**: No mention of EMIR/Dodd-Frank trade reporting obligations for OTC variance swaps.
