# Full-text search for internal-notes — intent check first

## Stop: intent-premise mismatch

Before researching, one blocker: **Algolia conflicts with a stated constraint in
your README.** Algolia is a hosted cloud SaaS — using it ships note content to a
third-party index outside your datacenter. `README.md` sets a non-negotiable
constraint: "Fully on-premises only. No third-party cloud or SaaS services may
process, index, or store app data."

So the approach you named (Algolia) is ruled out by your own documented
constraint. You did not ask about on-prem engines, so I'm flagging this in one
line before investing research rounds:

> Do you want me to (a) research **on-prem** full-text search that satisfies the
> constraint (Postgres FTS, OpenSearch/Elasticsearch self-hosted, Typesense
> self-hosted, Meilisearch self-hosted), or (b) treat the on-prem constraint as
> relaxed for this feature? I'll proceed with (a) unless you say otherwise.

Defaulting to (a) — the constraint is marked non-negotiable — and scoping the
candidate set to self-hostable engines.
