# Decide: Pydantic vs attrs for our validation layer — and does Pydantic support strict mode?

## Alternatives Considered

### 1. Pydantic
User-named option; rich validation, v2 is fast.

### 2. attrs + cattrs
User-named option; lighter, less batteries-included.

### 3. Status quo (incumbent): hand-rolled dataclasses + manual validators
The current setup the user did not name. Zero new dependency, but no declarative
schema. Ranked lower only because maintenance cost is higher at scale.

## Version scope
Strict mode: we checked both the **pinned** version in the lockfile (v2.5.0) and
the **latest** release (v2.9.2). Strict mode is supported in both; the pinned
v2.5.0 and latest v2.9.2 behave the same for our use.
