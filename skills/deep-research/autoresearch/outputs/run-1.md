# Should I Use Kafka or RabbitMQ for a Microservices Event Bus Handling 50K Messages/sec with Exactly-Once Delivery Requirements?

## Executive Summary

**Use Apache Kafka.** At 50K messages/sec with exactly-once delivery requirements, Kafka is the clear choice. Kafka natively supports exactly-once semantics (EOS) for Kafka-to-Kafka workflows via idempotent producers and transactions (since v0.11, 2017), with a measured throughput penalty of only ~3%. RabbitMQ does not support exactly-once delivery at all -- it offers at-most-once or at-least-once, requiring application-level idempotency for deduplication. Furthermore, 50K msg/sec sits comfortably within Kafka's capacity (benchmarked at 500K-2M msg/sec) but pushes RabbitMQ toward its CPU bottleneck threshold (~30K-100K msg/sec depending on configuration and durability settings). **However, a critical caveat**: true exactly-once *delivery* is impossible in distributed systems (Two Generals Problem). What Kafka provides is exactly-once *processing* within its ecosystem. For external systems (databases, APIs), you will need the transactional outbox pattern + idempotent consumers regardless of which broker you choose.

**Overall confidence: 85%** -- High confidence in the Kafka recommendation for this specific requirements profile. The 15% uncertainty stems from: (1) the user's exact message size and processing patterns could shift the calculus, (2) operational expertise requirements for Kafka are higher, and (3) RabbitMQ Streams could theoretically handle 50K msg/sec but without exactly-once guarantees.

---

## Key Findings

1. **Kafka sustains 500K-2M+ msg/sec** on modest hardware (3-node cluster); 50K msg/sec is ~2.5-10% of its capacity ceiling. RabbitMQ handles 50K-100K msg/sec with durability enabled but hits CPU bottlenecks above ~30K msg/sec per queue. [Confluent benchmark](https://www.confluent.io/blog/kafka-fastest-messaging-system/), [2025 VPS benchmarks](https://onidel.com/blog/nats-jetstream-rabbitmq-kafka-2025-benchmarks)

2. **Kafka provides exactly-once semantics (EOS)** via idempotent producers + transactions, with ~3% throughput penalty over at-least-once. This guarantee is scoped to Kafka-to-Kafka workflows (consume-transform-produce). [Confluent EOS blog](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)

3. **RabbitMQ does not provide exactly-once delivery.** The official RabbitMQ reliability guide states consumer applications must perform deduplication or handle messages idempotently. [RabbitMQ Reliability Guide](https://www.rabbitmq.com/docs/reliability)

4. **True exactly-once delivery is impossible** in distributed systems due to the Two Generals Problem. The distinction between exactly-once *delivery* and exactly-once *processing* is critical. [Brave New Geek](https://bravenewgeek.com/you-cannot-have-exactly-once-delivery/), [Two Generals Problem - Wikipedia](https://en.wikipedia.org/wiki/Two_Generals'_Problem)

5. **Kafka 4.0 (2025) removed ZooKeeper dependency** via KRaft mode, significantly reducing operational complexity -- the historical #1 argument against Kafka. [Confluent Kafka 4.0 blog](https://www.confluent.io/blog/latest-apache-kafka-release/), [InfoQ](https://www.infoq.com/news/2025/04/kafka-4-kraft-architecture/)

6. **Confluent benchmark: Kafka throughput is 15x RabbitMQ's** -- 605 MB/s vs 38 MB/s peak. Kafka also delivers lower p99 latency (5ms) at high throughput, though RabbitMQ achieves ~1ms latency at lower throughput (<30 MB/s). [Confluent benchmark](https://www.confluent.io/blog/kafka-fastest-messaging-system/)

7. **For external system exactly-once**, both systems require the transactional outbox pattern + idempotent consumers. Debezium CDC is the standard tool for this with Kafka. [Confluent outbox pattern](https://developer.confluent.io/courses/microservices/the-transactional-outbox-pattern/)

---

## Industry Standards Compliance

| Standard | Requirement | Kafka Status | RabbitMQ Status | Source |
|----------|------------|--------------|-----------------|--------|
| **ISO/IEC 19464 (AMQP 1.0)** | Standardized binary wire-level messaging protocol | Not compliant (uses custom protocol) | Compliant (AMQP 0.9.1 native; AMQP 1.0 plugin available in RabbitMQ 4.x) | [ISO/IEC 19464:2014](https://www.iso.org/standard/64955.html) |
| **OWASP guidelines** | Encryption in transit, authentication, authorization | Compliant (TLS, SASL, ACLs) | Compliant (TLS, SASL, vhost-level permissions) | Both official docs |
| **PCI-DSS** (if applicable) | Encryption of data in transit and at rest | Compliant (TLS + at-rest encryption in managed services) | Compliant (TLS + at-rest encryption in managed services) | Both support required controls |
| **GDPR** (if applicable) | Data minimization, right to erasure | Kafka: Challenging (log retention model conflicts with deletion); mitigated by compaction/TTL | RabbitMQ: Easier (messages consumed and deleted) | Architectural consideration |
| **RFC 793 / TCP** | Reliable transport | Both use TCP | Both use TCP | Standard networking |

**Notable**: Kafka does not implement any ISO/IEC standardized messaging protocol. It uses its own binary protocol. RabbitMQ implements AMQP 0.9.1 natively and supports AMQP 1.0 (ISO/IEC 19464) via plugin. If protocol standards compliance matters (e.g., for vendor interoperability), RabbitMQ has an advantage here. For most microservices architectures where you control both producers and consumers, this is rarely a deciding factor.

---

## Quantitative Analysis

### Throughput Comparison

| Metric | Apache Kafka | RabbitMQ (Classic/Quorum) | RabbitMQ (Streams) |
|--------|-------------|--------------------------|-------------------|
| **Peak throughput (MB/s)** | 605 MB/s | 38 MB/s | Higher (millions msg/sec for reads) |
| **Peak throughput (msg/sec, 1KB msgs)** | 500K - 2M+ | 50K - 100K | 134K+ (stream protocol) |
| **p99 latency at high throughput** | 5ms (at 200 MB/s) | 5-20ms (queue-depth dependent) | Sub-ms for reads |
| **Latency at low throughput** | 10-50ms (batching overhead) | ~1ms (sub-ms in LAN) | ~1ms |
| **CPU bottleneck threshold** | Very high (partitioned) | ~30K msg/sec per queue/core | Higher than classic |
| **50K msg/sec headroom** | ~10-90% spare capacity | Near or at limit | Comfortable but no EOS |

Sources: [Confluent benchmark](https://www.confluent.io/blog/kafka-fastest-messaging-system/), [2025 VPS benchmarks](https://onidel.com/blog/nats-jetstream-rabbitmq-kafka-2025-benchmarks), [RabbitMQ 4.1 performance](https://www.rabbitmq.com/blog/2025/04/08/4.1-performance-improvements), [RabbitMQ stream delivery optimization](https://www.rabbitmq.com/blog/2025/09/26/stream-delivery-optimization)

### Exactly-Once Semantics Comparison

| Capability | Apache Kafka | RabbitMQ |
|-----------|-------------|----------|
| **Idempotent producer** | Native (enable.idempotence=true) | Not available |
| **Transactional writes** | Native (transactional.id) | Not available |
| **Exactly-once within system** | Yes (Kafka-to-Kafka) | No |
| **Exactly-once to external systems** | No (requires outbox pattern) | No (requires outbox pattern) |
| **EOS throughput overhead** | ~3% penalty (Confluent benchmark, 1KB messages) | N/A |
| **Consumer isolation** | isolation.level=read_committed | N/A |
| **Deduplication mechanism** | Producer ID + sequence number (broker-side) | Application-level only |

### Cost Comparison (Managed Services)

| Provider | Service | Approximate Monthly Cost (50K msg/sec workload) | Notes |
|----------|---------|------------------------------------------------|-------|
| AWS | Amazon MSK (3x kafka.m5.large) | ~$600-900/mo + storage + transfer | Provisioned; per-second billing |
| Confluent | Confluent Cloud (Basic) | ~$500-1500/mo (throughput-dependent) | Serverless option available; eCKU-based |
| AWS | Amazon MQ (RabbitMQ, mq.m5.large) | ~$300-500/mo | May struggle at sustained 50K msg/sec |
| CloudAMQP | Dedicated plans | Varies; see [plans](https://www.cloudamqp.com/plans.html) | Per-second billing |

**TCO note**: Kafka's managed service costs are higher, but self-hosted RabbitMQ at 50K msg/sec may require significant tuning effort and potentially larger/more instances, narrowing the gap. Kafka's operational complexity has decreased significantly with KRaft (Kafka 4.0), but still requires understanding of partitions, consumer groups, and offset management.

### Cluster Sizing for 50K msg/sec

**Kafka (recommended minimal)**:
- 3 brokers (KRaft mode, no ZooKeeper needed since Kafka 4.0)
- 6-12 partitions per topic (depending on consumer parallelism needs)
- Replication factor: 3 (for durability with EOS)
- Hardware: m5.large equivalent (2 vCPU, 8GB RAM) is sufficient
- This represents ~5-10% utilization of capacity, leaving substantial headroom

**RabbitMQ (if attempting 50K msg/sec)**:
- 3-node quorum queue cluster minimum
- Multiple queues required (single queue bottlenecks at ~30K msg/sec per core)
- Hardware: m5.xlarge+ recommended (4+ vCPU, 16GB RAM)
- Would operate near capacity limits with durable messaging enabled

Sources: [AWS MSK pricing](https://aws.amazon.com/msk/pricing/), [Confluent pricing comparison](https://www.confluent.io/confluent-cloud-vs-amazon-msk/), [Kafka cluster sizing](https://aws.amazon.com/blogs/big-data/best-practices-for-right-sizing-your-apache-kafka-clusters-to-optimize-performance-and-cost/)

---

## Implementation Guidance

### Kafka Exactly-Once Configuration

**Producer configuration:**
```properties
# Enable idempotent producer (prevents duplicates on retry)
enable.idempotence=true

# Unique transactional ID per producer instance
transactional.id=my-service-tx-001

# Required for EOS
acks=all
retries=2147483647
max.in.flight.requests.per.connection=5
```

**Consumer configuration:**
```properties
# Only read committed (completed) transactions
isolation.level=read_committed

# Disable auto-commit (offsets committed within transaction)
enable.auto.commit=false
```

**Java producer transaction example:**
```java
producer.initTransactions();
try {
    producer.beginTransaction();

    // Send messages to output topic
    producer.send(new ProducerRecord<>("output-topic", key, value));

    // Commit consumer offsets within the same transaction
    producer.sendOffsetsToTransaction(offsets, consumerGroupMetadata);

    producer.commitTransaction();
} catch (Exception e) {
    producer.abortTransaction();
}
```

### For External Systems: Transactional Outbox Pattern

Since Kafka EOS only covers Kafka-to-Kafka flows, use the outbox pattern for database writes:

1. **Write to your database AND an outbox table in the same DB transaction**
2. **Use Debezium CDC connector** to capture outbox table changes and publish to Kafka
3. **Downstream consumers use idempotency keys** to deduplicate

Tool: [Debezium](https://debezium.io/) with the [outbox event router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)

### Migration Sequence (if moving from RabbitMQ to Kafka)

1. Deploy Kafka cluster in KRaft mode (3 brokers minimum)
2. Set up monitoring: Prometheus + Grafana with [JMX exporter](https://github.com/prometheus/jmx_exporter)
3. Implement dual-write: publish to both Kafka and RabbitMQ during transition
4. Migrate consumers topic-by-topic, starting with lowest-risk services
5. Validate exactly-once guarantees with end-to-end tests (produce N messages, verify N messages consumed, zero duplicates)
6. Remove RabbitMQ producers after all consumers migrated
7. Decommission RabbitMQ

### Key Monitoring Dashboards to Set Up

- **Under-replicated partitions**: Alert if > 0 (data loss risk)
- **Consumer lag**: Alert if growing (processing falling behind)
- **Transaction abort rate**: Alert if elevated (EOS issues)
- **Request latency p99**: Baseline and alert on deviation
- **Disk usage**: Alert at 70% (Kafka is disk-hungry with retention)

---

## Alternatives Considered

### 1. RabbitMQ with Application-Level Idempotency
- **Feasibility**: Possible but significantly more engineering effort
- **Why ranked lower**: 50K msg/sec is near RabbitMQ's ceiling with durable queues. No native EOS means every consumer must implement deduplication (message ID tracking in a database). This pushes complexity to every service team rather than centralizing it in the broker. At this throughput, you'd also need careful queue sharding to avoid per-core bottlenecks.

### 2. RabbitMQ Streams
- **Feasibility**: Higher throughput than classic queues (134K+ msg/sec with stream protocol)
- **Why ranked lower**: Streams are append-only logs (similar to Kafka's model) but lack Kafka's transactional/EOS primitives. You'd get Kafka-like architecture without Kafka's exactly-once guarantees. At that point, use Kafka directly.

### 3. Redpanda (Kafka API-compatible, C++ implementation)
- **Feasibility**: API-compatible with Kafka, claims 10x lower tail latencies
- **Why ranked lower**: Independent benchmarks (Jack Vanlightly, 2023) showed performance instability under sustained workloads and when brokers hit retention limits. Smaller community and ecosystem. At 50K msg/sec, Kafka's performance is more than adequate, making Redpanda's latency advantage less relevant. Could be worth evaluating if latency is the primary concern. [Jack Vanlightly analysis](https://jack-vanlightly.com/blog/2023/5/15/kafka-vs-redpanda-performance-do-the-claims-add-up)

### 4. NATS JetStream
- **Feasibility**: 200K-400K msg/sec with persistence; simpler operations than Kafka
- **Why ranked lower**: Does not provide exactly-once semantics. Like RabbitMQ, you'd need application-level idempotency. Smaller ecosystem for microservices patterns (schema registry, connectors, etc.).

### Comparison Matrix

| Criterion (weight) | Kafka | RabbitMQ | Redpanda | NATS JetStream |
|--------------------|-------|----------|----------|----------------|
| **Throughput at 50K msg/sec** (25%) | Excellent (10x headroom) | Marginal (near limit) | Excellent | Good (4-8x headroom) |
| **Exactly-once support** (30%) | Native (Kafka-to-Kafka) | None (app-level only) | Native (Kafka-compatible) | None |
| **Operational complexity** (20%) | Medium (improved with KRaft) | Low | Low-Medium | Low |
| **Ecosystem/tooling** (15%) | Excellent (Kafka Connect, Schema Registry, ksqlDB) | Good (wide protocol support) | Good (Kafka-compatible) | Growing |
| **Cost** (10%) | Medium-High | Low-Medium | Medium | Low |
| **Weighted score** | **High** | **Low-Medium** | **Medium-High** | **Medium** |

---

## Adversarial Review

### Counterargument 1: "RabbitMQ can handle 50K msg/sec with proper tuning"

**Evidence for**: VMware demonstrated RabbitMQ hitting 1M msg/sec on Google Compute Engine. [VMware Tanzu blog](https://blogs.vmware.com/tanzu/rabbitmq-hits-one-million-messages-per-second-on-google-compute-engine/). RabbitMQ Streams in 4.x can handle significantly more than classic queues. CloudAMQP's best practices guide shows optimizations for high throughput.

**Assessment**: The 1M msg/sec benchmark used favorable conditions (small messages, no durability guarantees, optimized hardware). With quorum queues (required for durability), publisher confirms, and realistic message sizes, sustained 50K msg/sec is achievable but leaves minimal headroom. The bigger issue remains: even at 50K msg/sec, RabbitMQ still doesn't provide exactly-once semantics, which is the user's stated requirement.

**Verdict**: Counterargument is partially valid on throughput but does not address the exactly-once requirement.

### Counterargument 2: "Kafka's exactly-once is marketing -- it's not true exactly-once"

**Evidence for**: The Two Generals Problem proves exactly-once *delivery* is impossible. Kafka's EOS only covers Kafka-to-Kafka (consume-transform-produce) workflows. Any external system interaction (database write, API call, email send) breaks the guarantee. [Brave New Geek](https://bravenewgeek.com/you-cannot-have-exactly-once-delivery/)

**Assessment**: This is technically correct and an important nuance. Kafka provides exactly-once *processing* within its ecosystem, not exactly-once *delivery* to arbitrary external systems. However, this doesn't invalidate the recommendation: (1) For event bus patterns where events flow topic-to-topic, Kafka's EOS is genuine and useful. (2) For external systems, both Kafka and RabbitMQ require the same outbox+idempotency approach, so Kafka is no worse. (3) Kafka's idempotent producer still prevents duplicate writes to Kafka itself, which is valuable even without full end-to-end EOS.

**Verdict**: Important nuance that the user must understand, but does not change the recommendation.

### Counterargument 3: "Kafka is overkill -- the operational complexity isn't worth it for 50K msg/sec"

**Evidence for**: DoorDash famously ran on RabbitMQ for years during hyper-growth with minimal operational investment. Kafka requires understanding partitions, consumer groups, rebalancing, offset management. Smaller teams may struggle.

**Assessment**: This was stronger before Kafka 4.0. The removal of ZooKeeper via KRaft significantly reduces operational burden. Managed services (Amazon MSK, Confluent Cloud) further reduce ops complexity. However, if the team has zero Kafka experience and strong RabbitMQ expertise, the migration cost is real. The question becomes: is the exactly-once requirement firm? If it can be relaxed to at-least-once + idempotent consumers, RabbitMQ becomes viable.

**Verdict**: Valid concern. If the team is small and lacks Kafka experience, consider whether the exactly-once requirement is truly non-negotiable before committing.

<details>
<summary><strong>Assumption Audit</strong></summary>

| Assumption | Status | Risk if Wrong |
|-----------|--------|---------------|
| 50K msg/sec is sustained, not burst | Reasonable (user stated it) | If burst only, RabbitMQ with buffering could work |
| Messages are event-sized (0.1-10KB) | Reasonable (typical for event bus) | If messages are large (>100KB), throughput calculations change significantly |
| "Exactly-once" means within the messaging system | Reasonable (most common interpretation) | If user means end-to-end including databases, neither system provides this natively |
| Team can operate Kafka or learn it | Uncertain | High -- Kafka operational errors can cause data loss or outages |
| Workload will grow over time | Reasonable (microservices tend to grow) | If workload is static/shrinking, RabbitMQ's lower cost wins |
| Managed services are acceptable | Uncertain | If self-hosted only, operational complexity increases significantly for Kafka |

</details>

<details>
<summary><strong>Failure Modes</strong></summary>

**If you follow this recommendation (choose Kafka):**

1. **Team skill gap**: If no one understands Kafka partitioning, consumer group rebalancing, or offset management, misconfigurations can cause data loss or duplicate processing despite EOS being "enabled."
2. **Transaction overhead at scale**: If the number of transactional producers grows large, the transaction coordinator can become a bottleneck. KIP-447 improved this but it requires Kafka 2.5+.
3. **Disk exhaustion**: Kafka retains messages (unlike RabbitMQ which deletes on consume). Without proper retention policies, disks fill up.
4. **Consumer lag spiral**: If consumers can't keep up, lag grows, which can cascade into memory pressure and further slowdown.
5. **EOS false confidence**: Developers may assume EOS covers their database writes, leading to subtle duplicate-processing bugs in external systems.

**Conditions that would change this recommendation:**
- Throughput requirement drops below 10K msg/sec AND exactly-once is relaxable -> RabbitMQ
- Team has zero distributed systems experience AND no budget for managed Kafka -> RabbitMQ with idempotent consumers
- Latency requirement is sub-millisecond at low throughput -> RabbitMQ (Kafka batching adds latency)
- Protocol standards compliance (AMQP 1.0) is required -> RabbitMQ

</details>

---

## Recommendation

**Choose Apache Kafka** for this use case. Specifically:

1. **Deploy Kafka 4.0+ in KRaft mode** (no ZooKeeper) -- 3-broker cluster is sufficient for 50K msg/sec with 10x headroom
2. **Enable exactly-once semantics** with idempotent producers (`enable.idempotence=true`) and transactions (`transactional.id`) for all Kafka-to-Kafka processing
3. **Implement the transactional outbox pattern** (Debezium CDC) for any flows that touch external systems (databases, APIs)
4. **Use a managed service** (Amazon MSK or Confluent Cloud) if operational expertise is limited
5. **Set consumer `isolation.level=read_committed`** on all consumers that need exactly-once guarantees
6. **Plan for growth**: Kafka's architecture scales horizontally; 50K msg/sec today could be 500K msg/sec in 2 years without re-architecture

**Confidence: 85%**

**This recommendation changes if**: (1) the exactly-once requirement can be relaxed to at-least-once + idempotent consumers (then RabbitMQ becomes viable and simpler), (2) the team has zero Kafka experience and no budget for training or managed services, or (3) sub-millisecond latency at low throughput is more important than exactly-once guarantees.

---

## Sources

### Throughput & Performance
- [Confluent: Benchmarking Kafka vs RabbitMQ vs Pulsar](https://www.confluent.io/blog/kafka-fastest-messaging-system/)
- [LinkedIn Engineering: 2 Million Writes Per Second](https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines)
- [2025 VPS Benchmarks: NATS vs RabbitMQ vs Kafka](https://onidel.com/blog/nats-jetstream-rabbitmq-kafka-2025-benchmarks)
- [RabbitMQ 4.1 Performance Improvements](https://www.rabbitmq.com/blog/2025/04/08/4.1-performance-improvements)
- [RabbitMQ Stream Delivery Optimization](https://www.rabbitmq.com/blog/2025/09/26/stream-delivery-optimization)
- [VMware: RabbitMQ Hits 1M msg/sec on GCE](https://blogs.vmware.com/tanzu/rabbitmq-hits-one-million-messages-per-second-on-google-compute-engine/)
- [CloudAMQP: RabbitMQ High Performance Best Practices](https://www.cloudamqp.com/blog/part2-rabbitmq-best-practice-for-high-performance.html)

### Exactly-Once Semantics
- [Confluent: Exactly-Once Semantics in Kafka](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)
- [Brave New Geek: You Cannot Have Exactly-Once Delivery](https://bravenewgeek.com/you-cannot-have-exactly-once-delivery/)
- [Two Generals' Problem - Wikipedia](https://en.wikipedia.org/wiki/Two_Generals'_Problem)
- [RabbitMQ Reliability Guide](https://www.rabbitmq.com/docs/reliability)
- [Jack Vanlightly: RabbitMQ vs Kafka Part 4 - Delivery Semantics](https://jack-vanlightly.com/blog/2017/12/15/rabbitmq-vs-kafka-part-4-message-delivery-semantics-and-guarantees)
- [Strimzi: Exactly-Once Semantics with Kafka Transactions](https://strimzi.io/blog/2023/05/03/kafka-transactions/)
- [Baeldung: Exactly-Once Processing in Kafka](https://www.baeldung.com/kafka-exactly-once)
- [KIP-98: Exactly Once Delivery and Transactional Messaging](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
- [KIP-447: Producer Scalability for Exactly Once Semantics](https://cwiki.apache.org/confluence/display/KAFKA/KIP-447:+Producer+scalability+for+exactly+once+semantics)

### Architecture & Comparison
- [AWS: Difference Between RabbitMQ and Kafka](https://aws.amazon.com/compare/the-difference-between-rabbitmq-and-kafka/)
- [CloudAMQP: When to Use RabbitMQ or Kafka](https://www.cloudamqp.com/blog/when-to-use-rabbitmq-or-apache-kafka.html)
- [Confluent: Transactional Outbox Pattern](https://developer.confluent.io/courses/microservices/the-transactional-outbox-pattern/)

### Kafka 4.0 & KRaft
- [Confluent: Apache Kafka 4.0 Release](https://www.confluent.io/blog/latest-apache-kafka-release/)
- [InfoQ: Kafka 4.0 KRaft Simplifies Architecture](https://www.infoq.com/news/2025/04/kafka-4-kraft-architecture/)
- [Confluent: KRaft - Apache Kafka Without ZooKeeper](https://developer.confluent.io/learn/kraft/)

### Standards
- [ISO/IEC 19464:2014 - AMQP v1.0](https://www.iso.org/standard/64955.html)
- [OASIS AMQP 1.0 Standard](https://www.amqp.org/node/102)
- [RabbitMQ AMQP 1.0 Support](https://www.rabbitmq.com/docs/amqp)

### Pricing & Operations
- [AWS MSK Pricing](https://aws.amazon.com/msk/pricing/)
- [Confluent Cloud vs Amazon MSK](https://www.confluent.io/confluent-cloud-vs-amazon-msk/)
- [AWS: Best Practices for Right-Sizing Kafka Clusters](https://aws.amazon.com/blogs/big-data/best-practices-for-right-sizing-your-apache-kafka-clusters-to-optimize-performance-and-cost/)
- [CloudAMQP Plans](https://www.cloudamqp.com/plans.html)

### Alternatives
- [Redpanda vs Kafka Performance (Jack Vanlightly)](https://jack-vanlightly.com/blog/2023/5/15/kafka-vs-redpanda-performance-do-the-claims-add-up)
- [Redpanda vs Kafka (Redpanda)](https://www.redpanda.com/blog/redpanda-vs-kafka-performance-benchmark)
- [RabbitMQ Quorum Queues in 4.0](https://www.rabbitmq.com/blog/2024/08/28/quorum-queues-in-4.0)
- [RabbitMQ Streams Documentation](https://www.rabbitmq.com/docs/streams)
