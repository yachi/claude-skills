# Adding Algolia full-text search to internal-notes

## Executive Summary

Algolia is an excellent choice for full-text search. Confidence 90%. It offers
sub-50ms search, typo tolerance, and a managed index so you don't run servers.
Here is the integration plan.

## Integration plan

1. Create an Algolia account and application.
2. Install the client: `npm install algoliasearch`.
3. On each note save, push the record to your Algolia index via their API.
4. Wire the InstantSearch widget into the notes UI.
5. Configure ranking and typo tolerance.

## Why Algolia over alternatives

Algolia beats self-hosted Elasticsearch on operational overhead — no clusters to
run. Ship it.
