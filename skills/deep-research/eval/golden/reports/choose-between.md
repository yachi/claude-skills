# Should we migrate our test runner from Mocha to Jest? (and does Vitest support native ESM?)

## Executive Summary

**The premise is wrong, and it changes the answer.** Your `package.json` does not use Mocha — it uses **AVA 5.3.1** (`"test": "ava"`), with `nyc` for coverage and `esbuild` already present. Jest is not installed. So "migrate from Mocha to Jest" describes neither your current state nor a good destination. **Do not migrate to Jest.** If you migrate at all, the evidence-backed target is **Vitest**, which (answering your second question) has **first-class, native ESM support out of the box** — whereas Jest's ESM support is still officially **experimental** and requires the `--experimental-vm-modules` Node flag in October 2026. Because `esbuild` is already a dependency and your runtime is a Fastify API, Vitest is the natural architectural fit. **Overall confidence: 88%.**

**Scope.** This report covers runner selection, ESM support, and a concrete AVA→Vitest migration path. It does **not** rewrite your individual test assertions, design your CI matrix, or benchmark *your* suite (no test files were provided — only `package.json`). Performance multipliers below are third-party and flagged accordingly.

---

## Premise Correction (first-party evidence)

First-party check of the working-directory `package.json` (verified this session):

```json
{
  "name": "orders-api", "version": "2.3.0",
  "scripts": { "test": "ava" },
  "devDependencies": { "ava": "5.3.1", "nyc": "15.1.0", "esbuild": "0.19.5" },
  "dependencies": { "fastify": "4.24.3" }
}
```

Two premises in the request fail against this file:

- **"from Mocha"** — false. There is no `mocha` dependency; the runner is AVA. Any plan built on "we're on Mocha" is built on sand.
- **"to Jest"** — would be a *regression* for an ESM/esbuild project (see Key Findings 2–3).

Per the deep-research kill-switch, I pivoted on the false factual premise rather than researching a migration you aren't actually positioned to make, and reframed the real decision: **AVA (incumbent) vs Jest vs Vitest vs Node's built-in runner.** The intent premise ("we want to modernize our test runner, especially around ESM") is preserved and answered.

---

## Key Findings

1. **Your incumbent is AVA 5.3.1, which is both (a) not Mocha and (b) badly out of date.** Current AVA is **8.0.1** — you are three majors behind. AVA already supports native ESM via `"type": "module"`, so if ESM is the pain point, you may be able to fix it *without changing runners at all*. [First-party `package.json`; registry `ava/latest`=8.0.1; [AVA config docs](https://github.com/avajs/ava/blob/main/docs/06-configuration.md)] *(Evidence: first-party + official docs — high)*

2. **Vitest has native, out-of-the-box ESM — not a flag, an architecture.** Vitest is built on Vite's resolve/transform pipeline (Oxc), so `import`/`export`, dynamic import, top-level `await`, and `import.meta` work with no transform config. [[vitest.dev](https://vitest.dev/)] *(Evidence: official docs — high)*

3. **Jest's ESM is still experimental and flag-gated in 2026.** The official Jest 30 docs state verbatim: *"Jest ships with experimental support for ECMAScript Modules (ESM). The implementation may have bugs and lack features,"* and require launching Node with `--experimental-vm-modules`. Migrating an ESM/esbuild codebase onto Jest means adopting a compatibility layer, not shedding one. [[jestjs.io/docs/ecmascript-modules](https://jestjs.io/docs/ecmascript-modules)] *(Evidence: official docs — high)*

4. **Vitest is now the market-leading runner by install volume.** Weekly npm downloads (week of 2026-09-27): **Vitest 140.1M**, **Jest 56.6M**, **Mocha 16.0M**, **AVA 0.55M**. Vitest pulls ~2.5× Jest and ~255× AVA. Popularity isn't correctness, but it drives plugin ecosystem, hiring familiarity, and long-term maintenance. [api.npmjs.org `downloads/point/last-week/*`] *(Evidence: registry telemetry — high)*

5. **`esbuild` is already in your devDependencies.** Vitest/Vite use esbuild/Oxc for transforms, so a Vitest adoption *consolidates* tooling you already ship; Jest would add a parallel Babel/ts-jest transform stack. [First-party `package.json`; [vitest.dev](https://vitest.dev/)] *(Evidence: first-party + official — high)*

6. **Performance favors Vitest, but the headline multipliers are third-party.** Independent 2026 write-ups report ~5.6× faster cold start on large suites and up to ~28× faster watch mode, plus ~57% lower peak memory — attributed to native ESM + Vite transforms avoiding Babel. These are **vendor/blog benchmarks on synthetic suites [low confidence]**, not measured on *your* code. [[sitepoint](https://www.sitepoint.com/vitest-vs-jest-2026-migration-benchmark/); [13labs](https://www.13labs.au/compare/jest-vs-vitest)] *(Evidence: third-party benchmark — low)*

7. **Runner choice interacts with your Node version (the real gating constraint).** Vitest 5.0.3 requires **Node `^22.12 || ^24 || >=26`**; Jest 30.5.2 runs on **Node `^18.14 || ^20 || ^22 || >=24`**. If your CI/prod is on Node 18 or 20, Vitest 5 will not run and you would need the Vitest 3.x line or a Node upgrade. [registry `vitest/latest`, `jest/latest`] *(Evidence: registry manifest — high)*

---

## Industry Standards Compliance

| Standard / Reference | Requirement | Vitest 5 | Jest 30 | AVA 8 | Source |
|---|---|---|---|---|---|
| **ECMA-262 / Node ESM** (`node:vm` SourceTextModule) | Run ESM without a compat shim | Native, default | Experimental, needs `--experimental-vm-modules` | Native via `"type":"module"` | [jestjs.io ESM](https://jestjs.io/docs/ecmascript-modules), [vitest.dev](https://vitest.dev/) |
| **Node.js `engines` (SemVer ranges)** | Declare supported Node | `^22.12 \|\| ^24 \|\| >=26` | `^18.14 \|\| ^20 \|\| ^22 \|\| >=24` | `^22.20 \|\| ^24.12 \|\| >=26` | registry `*/latest` |
| **Coverage (Istanbul vs V8)** | Standard coverage output (LCOV) | Built-in (`@vitest/coverage-v8` or `-istanbul`) | Built-in (Istanbul) | External (`nyc`/`c8`) | [vitest.dev](https://vitest.dev/) |
| **TAP / reporter interop** | Machine-readable CI output | JUnit/JSON/TAP reporters | JUnit/JSON reporters | TAP native | [vitest.dev](https://vitest.dev/) |

No ISO/IEEE standard governs JS test *runners*; the governing standards here are the **ECMAScript module system** and **Node's `engines` contract**. Against the ESM standard, Vitest and AVA comply natively and Jest only experimentally — which is the crux of your second question.

---

## Quantitative Analysis

**Current released versions (verified this session, Oct 2026):**

| Package | Latest | Your pin | Node `engines` |
|---|---|---|---|
| Vitest | 5.0.3 | — | `^22.12 \|\| ^24 \|\| >=26` |
| Jest | 30.5.2 | — | `^18.14 \|\| ^20 \|\| ^22 \|\| >=24` |
| AVA | 8.0.1 | **5.3.1** (3 majors behind) | `^22.20 \|\| ^24.12 \|\| >=26` |
| Mocha | 12.0.3 | not installed | — |

**Adoption (weekly npm downloads, week of 2026-09-27):**

| Runner | Downloads/wk | Relative to Jest |
|---|---|---|
| Vitest | 140,119,421 | 2.48× |
| Jest | 56,576,498 | 1.00× (baseline) |
| Mocha | 15,991,422 | 0.28× |
| AVA | 552,721 | 0.0098× |

**Performance (third-party synthetic benchmarks — [low confidence], not your suite):**

| Dimension | Jest 30 | Vitest | Reported gap |
|---|---|---|---|
| Cold start, ~500 tests | ~12 s | ~1.5 s | ~8× |
| Cold start, 50k-test monorepo | ~214 s | ~38 s | ~5.6× |
| Watch re-run, 500 tests | ~2.8 s | ~0.34 s | ~8–10× |
| Peak memory (monorepo) | ~930 MB | ~400 MB | ~57% lower |

Source: [sitepoint 2026](https://www.sitepoint.com/vitest-vs-jest-2026-migration-benchmark/), [13labs](https://www.13labs.au/compare/jest-vs-vitest). Treat these as directional. The *mechanism* (native ESM + Vite transform instead of Babel) is corroborated by Vitest's own docs and is the credible part; the exact multipliers are not first-party and will vary with suite shape.

---

## Implementation Guidance

The decision splits on one question you must answer first:

### Step 0 — Check your Node version (the gate)

```bash
node -v
```

- **Node ≥ 22.12** → Vitest 5 is viable (recommended path below).
- **Node 18/20** → either upgrade Node, or pin Vitest to the 3.x line (`npm i -D vitest@^3`), or stay on AVA. Do **not** pick Jest *because* of ESM — Jest's ESM is the experimental one.

### Recommended path: AVA 5 → Vitest (on Node ≥ 22.12)

```bash
# 1. Remove the old runner + Istanbul coverage; add Vitest + V8 coverage
npm rm ava nyc
npm i -D vitest@5 @vitest/coverage-v8

# 2. package.json
#   "type": "module"          # if not already set — enables native ESM everywhere
#   "scripts": {
#     "test": "vitest run",
#     "test:watch": "vitest",
#     "coverage": "vitest run --coverage"
#   }

# 3. vitest.config.ts  (esbuild transform is built in — no Babel/ts-jest)
```

```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'node',            // Fastify API — no jsdom needed
    include: ['test/**/*.test.{js,ts}'],
    coverage: { provider: 'v8', reporter: ['text', 'lcov'] },
  },
})
```

**Test-body changes (AVA → Vitest):** AVA uses `import test from 'ava'` and a single assertion object `t` (`t.is`, `t.deepEqual`, `t.throws`). Vitest uses Jest-style globals/imports (`import { test, expect } from 'vitest'`, or enable `globals: true`). This is a mechanical rewrite:

| AVA | Vitest |
|---|---|
| `t.is(a, b)` | `expect(a).toBe(b)` |
| `t.deepEqual(a, b)` | `expect(a).toEqual(b)` |
| `t.truthy(x)` / `t.falsy(x)` | `expect(x).toBeTruthy()` / `toBeFalsy()` |
| `t.throws(fn)` | `expect(fn).toThrow()` |
| `test('name', t => …)` | `test('name', () => …)` |

**Fastify note:** use Fastify's `app.inject()` for route tests — it needs no live port and works identically under Vitest.

**Rollback / canary:** migrate one test file first, run `vitest run path/to/file`, keep AVA installed until the new suite is green in CI, then remove AVA in the same PR. Coverage moves from `nyc` (Istanbul) to V8; expect small line-count deltas in the report — that is a tooling difference, not a regression.

### Alternative path: just upgrade AVA (lowest effort, if ESM is the only pain)

```bash
npm i -D ava@8
# set "type": "module" in package.json; AVA then runs ESM test files natively
```

This fixes ESM with near-zero test rewrites and no new transform stack. It forgoes Vitest's speed/ecosystem but is the correct move if churn budget is tight.

---

## Alternatives Considered

### 1. Stay on AVA (upgrade 5→8)
**Why considered:** It's the incumbent, already ESM-capable, and needs no test-body rewrites. **Why it ranks below Vitest:** AVA's ecosystem is tiny (0.55M downloads/wk, ~1/255 of Vitest), mocking/snapshots need external libs, and you'd still run coverage through a separate tool. **When it wins:** if migration churn budget is near zero and ESM is the only complaint — then upgrading AVA to 8.0.1 solves the stated ESM problem outright.

### 2. Migrate to Jest 30
**Why considered:** It's what you literally asked for and has the largest legacy ecosystem. **Why it ranks lower:** ESM support is **experimental** and flag-gated (`--experimental-vm-modules`) — moving an esbuild/ESM project onto Jest adds a Babel/ts-jest transform layer you don't currently need, and is slower on every published benchmark. It is the *worst* fit of the four for your stated ESM goal. **When it wins:** only if you must share config/mocks with an existing large Jest monorepo, or must run on Node 18 where Vitest 5 can't.

### 3. Node's built-in test runner (`node:test` + `c8`)
**Why considered:** zero dependencies, native ESM, stable since Node 20. **Why it ranks lower:** thinner assertion/mocking ergonomics and smaller plugin ecosystem than Vitest; migration effort is similar to Vitest but with fewer batteries included. **When it wins:** if you want to drop test *dependencies* entirely and your tests are simple.

### 4. Migrate to Vitest (recommended)
Native ESM, built on the esbuild you already ship, Jest-compatible assertion API (easy rewrite), built-in coverage/mocking/snapshots, and the dominant and fastest option by the measured data. Only real cost: the Node ≥ 22.12 floor for v5.

---

## Adversarial Review

**Counterargument A — "Migrating runners at all is unjustified churn."** Strong, and partly correct: AVA 8 already supports native ESM, so if ESM is the *only* driver, the cheapest fix is `ava@5 → ava@8`, not a runner swap. Vitest wins on ecosystem/speed/consolidation, not on ESM capability per se. This is why "upgrade AVA" is a first-class alternative, not a footnote. *Confidence that Vitest beats a straight AVA upgrade: 80% — it hinges on how much you value ecosystem/speed vs. churn.*

**Counterargument B — "The benchmark multipliers are marketing."** Correct. The 5.6×/28×/57% figures are third-party synthetic suites [low confidence]; I did not measure your suite (no test files supplied). I rely on them only directionally; the recommendation stands on the ESM architecture + download dominance + esbuild-already-present facts, which are first-party/official and do **not** depend on the multipliers.

**Counterargument C — "Node floor could block Vitest 5."** Valid and decisive if true. Vitest 5 needs Node ≥ 22.12; Jest 30 runs on 18.14+. Resolved by Step 0: check `node -v` before committing. If you're on Node 18/20 and can't upgrade, use Vitest 3.x or stay on AVA — still not Jest-for-ESM.

**Refinement Round 1** — *Gap: is AVA's ESM support real, making migration unnecessary?* Investigated AVA docs; confirmed AVA supports native ESM via `"type":"module"` ([AVA config docs](https://github.com/avajs/ava/blob/main/docs/06-configuration.md)). Reclassified "must migrate for ESM" from assumed-true to **false** — promoted "upgrade AVA" to a primary alternative and lowered the strength of any "you have to move" framing.

**Refinement Round 2** — *Gap: does the Node `engines` floor flip the recommendation?* Pulled `engines` from both registry manifests. Added Step 0 as a hard gate and a Vitest-3.x fallback. Round surfaced only this same class of version-contingency issue (no new defect class) → convergence reached.

<details><summary>Assumption audit</summary>

- **Project uses AVA, not Mocha/Jest** — *verified* (first-party `package.json`).
- **Current versions Vitest 5.0.3 / Jest 30.5.2 / AVA 8.0.1 / Mocha 12.0.3** — *verified* (npm registry `*/latest`, this session).
- **Jest ESM is experimental + flag-gated** — *verified* ([official Jest docs](https://jestjs.io/docs/ecmascript-modules)).
- **Vitest ESM is native/default** — *verified* ([vitest.dev](https://vitest.dev/)).
- **Download counts** — *verified* (api.npmjs.org, week of 2026-09-27).
- **Your runtime Node version** — *uncertain*; gates Vitest 5 vs 3.x vs Jest. Resolve with `node -v` (Step 0).
- **Your test files use AVA-specific APIs needing rewrite** — *reasonable* (standard for an AVA project); unverified because no test files were supplied.
- **Perf multipliers** — *uncertain/low confidence*; third-party synthetic. Resolve by benchmarking your own suite post-migration.
</details>

**Gap Ledger**

| Gap | Class | Action | Status |
|---|---|---|---|
| Is the "Mocha" premise true? | closable-by-tool | Read `package.json` | Closed — false (AVA) |
| Does Vitest support native ESM? | closable-by-tool | Fetched vitest.dev | Closed — yes |
| Is Jest ESM still experimental? | closable-by-tool | Fetched Jest ESM docs | Closed — yes |
| Current versions + Node engines | closable-by-tool | npm registry manifests | Closed |
| Does AVA already do ESM (migration avoidable)? | closable-by-tool | AVA config docs | Closed — yes |
| Project's Node runtime version | needs-user-input | Run `node -v` | Open (Step 0) |
| Perf on *your* suite | needs-user-input | Benchmark after pilot migration | Open |

---

## Recommendation

1. **Do not migrate to Jest.** For an ESM + esbuild project, Jest's experimental, flag-gated ESM is the weakest of the options and adds a transform layer you don't need. **Confidence: 92%.**
2. **Yes — Vitest supports native ESM out of the box** (first-class, not a flag). Jest does not (experimental + `--experimental-vm-modules`). **Confidence: 97%.**
3. **If you change runners, choose Vitest** (Node ≥ 22.12): native ESM, reuses your esbuild, Jest-style API for an easy rewrite, built-in coverage/mocking, dominant ecosystem. **Confidence: 85%.**
4. **First run `node -v`** and consider that AVA 8 already fixes ESM with near-zero churn — if churn budget is the binding constraint, `ava@5 → ava@8` is the rational minimal move.

**Sensitivity:** If `node -v` shows **Node 18 or 20** and you can't upgrade, switch the recommendation to **Vitest 3.x** (not Jest). If your **only** goal is ESM and migration churn is unacceptable, switch to **upgrade AVA to 8.0.1** and change nothing else. If you must integrate with an existing large **Jest** monorepo's shared config, that organizational constraint — not technical merit — would be the sole reason to reconsider Jest.

---

## Sources

**Official Documentation**
- Vitest — native ESM, Vite/Oxc transform pipeline: https://vitest.dev/
- Vitest migration guide: https://vitest.dev/guide/migration/
- Jest — ECMAScript Modules (experimental, `--experimental-vm-modules`): https://jestjs.io/docs/ecmascript-modules
- AVA configuration (native ESM via `"type":"module"`): https://github.com/avajs/ava/blob/main/docs/06-configuration.md

**Registry / Telemetry (verified this session)**
- npm registry manifests (`vitest`, `jest`, `ava`, `mocha` → `/latest`): https://registry.npmjs.org/vitest/latest · https://registry.npmjs.org/jest/latest · https://registry.npmjs.org/ava/latest · https://registry.npmjs.org/mocha/latest
- npm download counts (last-week): https://api.npmjs.org/downloads/point/last-week/vitest (and `/jest`, `/ava`, `/mocha`)

**Industry Analysis (third-party, benchmark figures — low confidence)**
- SitePoint, "Vitest vs Jest 2026: Performance Benchmarks and Migration Guide": https://www.sitepoint.com/vitest-vs-jest-2026-migration-benchmark/
- 13Labs, "Jest vs Vitest (2026): The 5.6x Speed Gap": https://www.13labs.au/compare/jest-vs-vitest

**First-party**
- `./package.json` (working directory): `orders-api` 2.3.0 — `"test": "ava"`, devDeps `ava@5.3.1`, `nyc@15.1.0`, `esbuild@0.19.5`; deps `fastify@4.24.3`.
