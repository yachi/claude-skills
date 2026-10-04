# Migrate the test runner from Mocha to Jest?

## Executive Summary

**Premise correction first:** your `package.json` does not use Mocha at all —
the incumbent runner is **ava** (`"ava": "5.3.1"`, `"test": "ava"`). So the real
question is "migrate from ava to Jest?", and the candidate set must include the
status quo (ava) plus Vitest, which fits your esbuild/ESM toolchain better than
Jest. Recommendation: **stay on ava or move to Vitest; do not adopt Jest.**
Confidence 80%.

## Candidate space (full set, not just the two you named)

| Runner | Status | Native ESM | Notes |
|---|---|---|---|
| **ava** (incumbent) | installed, v5.3.1 | yes | already working; zero migration cost |
| Vitest | candidate | yes | esbuild-based, matches your `esbuild` dep |
| Jest | user-named | partial / experimental | needs babel/ts-jest shims for ESM |
| Mocha | user-named | yes (with loader) | not actually installed here |

The incumbent **ava** is the baseline every alternative must beat; it was not in
your question but it is what you run today.

## Version scope — does Vitest support native ESM?

**Yes.** Version check on both ends:

- **Pinned toolchain:** your project pins `esbuild` 0.19.5 and `ava` 5.3.1;
  Vitest 1.x pairs cleanly with that esbuild line and supports native ESM out of
  the box (no `transform` config).
- **Latest release:** Vitest latest (v3.x at time of writing) also supports
  native ESM and Node's ESM loader; the ESM support has been stable since v1.0.

Checking both the pinned version you would install against and the latest
release avoids recommending a feature that only exists in one of them.

## Industry Standards Compliance

| Standard | Requirement | Status | Source |
|---|---|---|---|
| Node.js ESM (RFC-style spec) | `.mjs` / `"type":"module"` resolution | ava + Vitest comply; Jest partial | nodejs.org/api/esm.html |

## Quantitative Analysis

Migration cost (engineer-hours) estimated from assertion-API surface: ava→Vitest
~4h (similar concurrent model), ava→Jest ~12h (rewrite to `describe/it`, ESM
shims). Staying on ava: 0h.

## Implementation Guidance

If moving: `npm install -D vitest`, port `test` script to `vitest run`, keep
`esbuild`. Start Monday with one spec file as a canary.

## Alternatives Considered

### 1. Stay on ava (incumbent)
Zero cost, already ESM-native. Ranked highest unless you need Vitest's UI/watch.

### 2. Vitest
~4h migration, better watch/UI, esbuild-aligned. The move if you want tooling.

### 3. Jest
Highest ESM friction (partial support, needs shims); ranked lowest for an
ESM/esbuild project.

## Adversarial Review

Counterargument: Jest has the largest ecosystem. Rebuttal: ecosystem size does
not offset ESM friction for this esbuild-based project.

## Recommendation

Stay on ava or adopt Vitest; avoid Jest. If your team standardizes on Jest
elsewhere, revisit. Confidence 80%.

## Sources

**Official Documentation:** nodejs.org/api/esm.html, vitest.dev, github.com/avajs/ava
