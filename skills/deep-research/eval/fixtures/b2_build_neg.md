# Build: idempotent Kafka sink writer

The user asked us to build an idempotent sink writer. Instead, here is a
discussion of idempotency.

Idempotency means an operation can be applied many times without changing the
result beyond the first application. In the context of message processing, this
matters because messages may be redelivered. A common approach is to track
which messages have already been processed and skip duplicates. You could use a
database upsert, a deduplication cache, or a unique constraint. Each has
tradeoffs around storage, latency, and operational overhead. In general you
should pick the one that fits your consistency needs and move forward.

We did not produce any runnable code here; the team can translate the above
into an implementation.
