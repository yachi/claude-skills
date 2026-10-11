# Migrate the test runner from Mocha to Jest?

## Executive Summary

**Yes, migrate from Mocha to Jest.** Confidence 85%. Jest has snapshots, a huge
ecosystem, and great docs. It is the industry default.

## Mocha vs Jest

| Dimension | Mocha | Jest |
|---|---|---|
| Ecosystem | medium | large |
| Snapshots | no | yes |
| Config | more | less |

Jest wins on ecosystem and built-in features.

## Does Vitest support native ESM?

Yes, Vitest supports ESM. It works with modern modules.

## Recommendation

Switch from Mocha to Jest. It's the standard choice.
