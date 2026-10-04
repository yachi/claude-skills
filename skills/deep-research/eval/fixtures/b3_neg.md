# Does our cache layer need Redis Cluster?

## Executive Summary

Earlier I concluded that a single Redis instance was sufficient, but actually I
was wrong — the working set exceeds one node's memory, so Redis Cluster is
required. Confidence: 80%.

## Key Findings

1. The working set is 240GB; a single node maxes at 128GB.
2. Correction: my earlier claim that replication alone solves this was
   incorrect; replication does not add capacity, only availability.

## Recommendation

Use Redis Cluster with 4 shards.
