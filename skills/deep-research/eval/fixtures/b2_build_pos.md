# Build: idempotent Kafka sink writer

Deliverable type: **build** — short findings, spend effort on the artifact.

## Findings (brief)
Exactly-once across the Kafka boundary still needs an idempotent external sink.
The cheapest correct pattern is an upsert keyed on `(aggregate_id, offset)` so a
replayed transaction is a no-op. Confidence: 85%. Below is the artifact.

## Artifact

```python
# idempotent_sink.py — upsert keyed on (aggregate_id, kafka_offset)
import psycopg

def write(cur, aggregate_id: str, offset: int, payload: bytes) -> None:
    cur.execute(
        """
        INSERT INTO sink (aggregate_id, kafka_offset, payload)
        VALUES (%s, %s, %s)
        ON CONFLICT (aggregate_id, kafka_offset) DO NOTHING
        """,
        (aggregate_id, offset, payload),
    )
```

Run it against a local Postgres; a replayed offset is a no-op, proving replay
idempotency. File written to `sink/idempotent_sink.py`.
