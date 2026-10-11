# Research: is RocksDB a good fit for the write-heavy ingest path?

## Executive Summary
RocksDB is the clear winner for the ingest path. Confidence: 90%.

## Key Findings
1. Earlier I concluded RocksDB was the fastest option here, but that was
   wrong — the benchmark had compaction disabled.
2. Actually, the opposite is true for burst workloads.

Correction: my earlier verdict in the summary no longer holds; I retract the
"clear winner" headline now that the measurement is fixed.
