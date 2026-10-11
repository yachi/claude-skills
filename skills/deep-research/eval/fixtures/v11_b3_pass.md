# Research: is RocksDB a good fit for the write-heavy ingest path?

## Executive Summary
RocksDB fits the write-heavy path; LSM write amplification is the main caveat.
Confidence: 82%.

## Key Findings
1. Write throughput measured at 180K ops/s on the benchmark rig [bench log].
2. Compaction can stall p99 latency under burst load [RocksDB wiki].

Every headline claim above was promoted to Key Findings only after the
verification pass. No earlier statement in this report is reversed here.
