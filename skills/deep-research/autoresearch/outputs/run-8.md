# RTB Ad Exchange Infrastructure: Aerospike+Kafka vs Redis+NATS vs Managed Cloud

## Executive Summary

**Recommendation: Aerospike + NATS (hybrid of the two proposed stacks), at ~$14,300/month -- well within the $50K budget.** Aerospike's Hybrid Memory Architecture delivers the sub-millisecond data lookups RTB demands at 80% lower node count than Redis, while NATS provides sub-millisecond message fanout that Kafka cannot match due to batching-induced latency. All three proposed stacks fit the $50K/month budget, but the Aerospike+NATS hybrid optimizes for the <10ms p99 constraint that is the hardest requirement to meet. GDPR/CCPA compliance is achievable with any stack but requires architectural decisions (PII pseudonymization, consent propagation, data minimization) that are stack-independent.

**Overall confidence: 78%.** High confidence on performance and cost numbers; moderate confidence on GDPR compliance architecture (evolving regulatory landscape, particularly post-Belgian DPA ruling on TCF).

---

## Key Findings

1. **Aerospike handles 200M+ QPS in production ad tech** (Criteo case study), with sub-millisecond p99 latency and 17-48% lower p99 than Redis across workloads. It needs up to 87% fewer nodes than Redis for equivalent data. *(Sources: [Aerospike AdTech](https://aerospike.com/solutions/industry/adtech/), [Aerospike vs Redis Benchmark](https://aerospike.com/resources/benchmarks/aerospike-vs-redis-benchmark-report/))*

2. **NATS delivers sub-millisecond latency** vs Kafka's 10-50ms (batching overhead). For RTB bid fanout where every millisecond counts toward the 10ms p99 budget, NATS is the superior messaging layer. Kafka excels at durable event streaming but adds latency that consumes too much of the p99 budget. *(Sources: [NATS vs Kafka 2025 Benchmark](https://onidel.com/blog/nats-jetstream-rabbitmq-kafka-2025-benchmarks), [Synadia NATS vs Kafka](https://www.synadia.com/blog/nats-and-kafka-compared))*

3. **Redis can sustain 1M+ RPS per node** on r7g.4xlarge with sub-ms p99, but requires all data in RAM -- doubling the node count vs Aerospike for datasets >1TB. Annual cost difference: $87,329 (Redis) vs $18,818 (Aerospike) at 1TB scale. *(Sources: [ElastiCache 500M RPS](https://aws.amazon.com/blogs/database/achieve-over-500-million-requests-per-second-per-cluster-with-amazon-elasticache-for-redis-7-1/), [Aerospike Efficiency](https://aerospike.com/blog/redis-efficiency/))*

4. **GDPR compliance for RTB is under active regulatory attack.** The Belgian DPA fined IAB Europe EUR 250,000 (upheld May 2025) for TCF violations. The TC String is personal data per CJEU (March 2024). Article 5(1)(c) data minimization and Article 5(1)(f) security requirements are structurally difficult for RTB. *(Sources: [Belgian Court Ruling](https://www.lewissilkin.com/en/insights/2025/05/27/iab-tcf-belgian-market-court-upholds-250-000-fine-against-iab-for-gdpr-violatio-102kyon), [CJEU TC String](https://technologyquotient.freshfields.com/post/102kcx6/brussels-market-court-clarifies-gdpr-roles-in-adtech-and-upholds-sanctions-agains))*

5. **CCPA requires honoring GPC signals as valid opt-out requests.** Healthline Media was fined $1.55M (the largest CCPA settlement to date) for failing to honor GPC. California, Colorado, and Connecticut conducted a joint enforcement sweep in September 2025. *(Source: [CPPA Announcement](https://cppa.ca.gov/announcements/2025/20250909.html))*

6. **All options fit the $50K/month budget.** Aerospike+Kafka: ~$15,500/mo. Redis+NATS: ~$10,100/mo. Managed Cloud: ~$20,100/mo. Aerospike+NATS hybrid: ~$14,300/mo. These estimates use 1-year reserved instances on AWS.

---

## Industry Standards Compliance

| Standard / Regulation | Requirement | RTB Exchange Impact | Compliance Strategy |
|---|---|---|---|
| **GDPR Art. 5(1)(c)** — Data minimization | Personal data must be adequate, relevant, limited to purpose | Bid requests contain device IFA, IP, geo, user segments -- minimize fields transmitted | Strip/hash PII before fanout; only pass pseudonymized IDs |
| **GDPR Art. 5(1)(f)** — Integrity & confidentiality | Appropriate security against unauthorized access | Bid streams broadcast PII to many parties | TLS 1.2+ everywhere; Aerospike EE encryption at rest (AES-256); field-level encryption for PII |
| **GDPR Art. 6** — Lawful basis | Valid consent or legitimate interest required | TC String consent must be captured, validated, propagated | Integrate IAB TCF 2.2; validate consent server-side before bid fanout |
| **GDPR Art. 17** — Right to erasure | Data subjects can request deletion | User profile data in Aerospike/Redis must be deletable | TTL-based auto-expiry + on-demand deletion API; audit trail |
| **GDPR Art. 25** — Data protection by design | Privacy built into architecture | Exchange architecture must embed privacy controls | PII vault pattern; consent-gated processing pipeline |
| **GDPR Art. 32** — Security of processing | Encryption, pseudonymization, resilience | All data stores and message buses must be secured | Aerospike EE: TLS 1.2 + AES-256 at rest; NATS: TLS mutual auth |
| **CCPA/CPRA Sec. 1798.120** — Right to opt-out | Honor GPC signals; do not sell/share after opt-out | Must check GPC header on every bid request | GPC signal detection middleware; suppress PII from bid stream for opted-out users |
| **CCPA/CPRA Sec. 1798.121** — Sensitive PI | Heightened protection for sensitive personal information | Device IFA, precise geo may qualify | Coarsen geo to postal code; hash IFA before storage |
| **OpenRTB 2.6** (IAB Tech Lab) | Standard bid request/response protocol | Exchange must implement OpenRTB-compliant auction | Support `regs` object for consent signals; `device.lmt` for limit ad tracking |
| **IAB TCF 2.2** | Transparency & Consent Framework | TC String must be propagated; consent validated | Server-side TC String validation before auction; reject bids lacking valid consent |
| **ISO 27001:2022 A.8.24** | Use of cryptography | Encryption for data at rest and in transit | Aerospike AES-256; NATS/Kafka TLS; KMS for key management |
| **PCI-DSS 4.0 Req. 3** (if handling payment) | Protect stored account data | Billing data for advertisers/publishers | Separate billing data store; tokenization; not in hot path |

---

## Quantitative Analysis

### Performance Comparison Matrix

| Metric | Aerospike | Redis | Kafka | NATS |
|---|---|---|---|---|
| **Max throughput (single node)** | 480K+ ops/s | 1M+ ops/s | 1M+ msgs/s (batched) | 4.9M+ msgs/s |
| **p99 latency (at load)** | <1ms | <1ms | 10-50ms | <1ms |
| **Data model** | KV + document + graph | KV + data structures | Log/stream | Pub/sub + KV + stream |
| **Memory requirement** | Index in RAM, data on SSD | All data in RAM | Page cache + disk | In-memory (JetStream: disk) |
| **Nodes for 1TB data** | ~5 (i4i.4xlarge) | ~10 (r7g.4xlarge) | N/A (streaming) | N/A (messaging) |
| **Encryption at rest** | AES-128/256 (Enterprise) | Redis Enterprise only | Disk-level only | JetStream: disk-level |
| **TLS in transit** | TLS 1.2 (Enterprise) | TLS 1.2+ | TLS 1.2+ | TLS 1.2+ mutual auth |
| **Persistence** | Hybrid (RAM index + SSD) | RDB/AOF snapshots | Commit log | JetStream (file/memory) |
| **Cluster auto-rebalancing** | Yes (automatic) | Manual resharding | Yes (partition reassignment) | Yes (automatic) |

### Cost Model (1-Year Reserved Instances, us-east-1)

```
=== Option A: Aerospike + Kafka (Self-Managed) ===
Aerospike (5x i4i.4xlarge RI):     $ 2,993/mo
Kafka brokers (5x m7g.2xlarge RI):  $   715/mo
Kafka storage (10,000 GB gp3):      $   800/mo
App servers (20x c7g.2xlarge RI):   $ 2,540/mo
Networking:                          $ 3,000/mo
Monitoring:                          $   500/mo
Aerospike Enterprise license:        $ 5,000/mo
TOTAL:                               $15,548/mo  [WITHIN $50K budget]

=== Option B: Redis + NATS (Self-Managed) ===
Redis (10x r7g.4xlarge RI):         $ 3,752/mo
NATS (3x c7g.xlarge RI):            $   190/mo
NATS JetStream storage (1,500 GB):  $   120/mo
App servers (20x c7g.2xlarge RI):   $ 2,540/mo
Networking:                          $ 3,000/mo
Monitoring:                          $   500/mo
TOTAL:                               $10,102/mo  [WITHIN $50K budget]

=== Option C: Managed Cloud (ElastiCache + MSK) ===
ElastiCache (10x r7g.4xlarge):      $ 9,344/mo
MSK (5x m7g.2xlarge):               $ 2,029/mo
MSK storage (10,000 GB):            $ 1,000/mo
App servers (20x c7g.2xlarge RI):   $ 2,540/mo
Networking:                          $ 5,000/mo
Monitoring (CloudWatch):             $   200/mo
TOTAL:                               $20,113/mo  [WITHIN $50K budget]

=== Option D: Aerospike + NATS (Recommended Hybrid) ===
Aerospike (5x i4i.4xlarge RI):     $ 2,993/mo
NATS (3x c7g.xlarge RI):            $   190/mo
NATS JetStream storage (1,500 GB):  $   120/mo
App servers (20x c7g.2xlarge RI):   $ 2,540/mo
Networking:                          $ 3,000/mo
Monitoring:                          $   500/mo
Aerospike Enterprise license:        $ 5,000/mo
TOTAL:                               $14,343/mo  [WITHIN $50K budget]
```

### Latency Budget Analysis (10ms p99 target)

The 10ms p99 constraint is the binding constraint. Here's how each stack consumes the budget:

| Stage | Aerospike+Kafka | Redis+NATS | Aerospike+NATS | Managed Cloud |
|---|---|---|---|---|
| Network ingress | 0.5ms | 0.5ms | 0.5ms | 0.5ms |
| Deserialize bid request | 0.3ms | 0.3ms | 0.3ms | 0.3ms |
| Consent validation (TCF) | 0.2ms | 0.2ms | 0.2ms | 0.2ms |
| User profile lookup | 0.8ms | 0.5ms | 0.8ms | 0.5ms |
| Campaign matching | 1.0ms | 1.0ms | 1.0ms | 1.0ms |
| **Message fanout to bidders** | **3-8ms** | **0.3ms** | **0.3ms** | **3-8ms** |
| Bid collection & auction | 1.0ms | 1.0ms | 1.0ms | 1.0ms |
| Response serialization | 0.2ms | 0.2ms | 0.2ms | 0.2ms |
| Network egress | 0.5ms | 0.5ms | 0.5ms | 0.5ms |
| **Total p99** | **7.5-13.5ms** | **4.5ms** | **4.8ms** | **7.2-13.2ms** |
| **Meets <10ms p99?** | **Marginal/No** | **Yes** | **Yes** | **Marginal/No** |

**Critical finding:** Kafka's batching latency (10-50ms typical, tunable down to ~3ms with aggressive `linger.ms=0` + small batches, but at the cost of throughput) makes it a poor fit for the 10ms p99 constraint. NATS's sub-millisecond message delivery is essential for meeting the latency budget.

---

## Implementation Guidance

### Recommended Architecture: Aerospike + NATS

```
                    ┌─────────────────────────────────────────┐
                    │         Load Balancer (NLB)              │
                    └──────────────┬──────────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────────┐
                    │     Bid Request Processors (20 nodes)    │
                    │  - Deserialize OpenRTB 2.6               │
                    │  - Validate TCF consent / GPC signal     │
                    │  - PII pseudonymization layer            │
                    │  - Lookup user profile (Aerospike)       │
                    │  - Publish to NATS for bid fanout        │
                    └──┬───────────┬──────────────────────────┘
                       │           │
          ┌────────────▼───┐  ┌───▼────────────────────┐
          │  Aerospike EE   │  │  NATS Cluster (3 nodes) │
          │  (5 nodes)      │  │  - Core NATS for fanout │
          │  - User profiles│  │  - JetStream for events │
          │  - Freq caps    │  │  - Win notifications    │
          │  - Campaign data│  │  - Bid logging (async)  │
          │  - AES-256 @rest│  │  - TLS mutual auth      │
          │  - TLS 1.2      │  │                         │
          └────────────────┘  └─────────────────────────┘
```

### Day-1 Implementation Checklist

**Aerospike Configuration:**
```bash
# aerospike.conf key settings for RTB
namespace rtb {
    replication-factor 2
    memory-size 64G              # Index + hot data in RAM
    default-ttl 86400            # 24h TTL for user profiles
    storage-engine device {
        device /dev/nvme0n1      # i4i NVMe
        device /dev/nvme1n1
        write-block-size 128K
        encryption-key-file /etc/aerospike/encryption-key.dat
        encryption aes-256
    }
}

security {
    enable-security true
}

network {
    tls rtb-tls {
        cert-file /etc/aerospike/cert.pem
        key-file /etc/aerospike/key.pem
        ca-file /etc/aerospike/ca.pem
    }
    service {
        tls-port 4333
        tls-name rtb-tls
    }
}
```

**NATS Configuration:**
```
# nats-server.conf
server_name: rtb-nats-1
listen: 0.0.0.0:4222

tls {
    cert_file: "/etc/nats/cert.pem"
    key_file: "/etc/nats/key.pem"
    ca_file: "/etc/nats/ca.pem"
    verify: true
}

jetstream {
    store_dir: "/data/jetstream"
    max_mem: 4G
    max_file: 500G
}

cluster {
    name: rtb-cluster
    listen: 0.0.0.0:6222
    tls { /* same TLS config */ }
    routes = [
        nats-route://rtb-nats-2:6222
        nats-route://rtb-nats-3:6222
    ]
}
```

**PII Pseudonymization Layer (Go example):**
```go
// Pseudonymize PII fields before any fanout or storage
func pseudonymizeBidRequest(req *openrtb2.BidRequest, hmacKey []byte) {
    if req.Device != nil {
        // Hash IFA with HMAC-SHA256, rotating key daily
        if req.Device.IFA != "" {
            req.Device.IFA = hmacHash(req.Device.IFA, hmacKey)
        }
        // Coarsen IP to /24 (IPv4) or /48 (IPv6)
        if req.Device.IP != "" {
            req.Device.IP = coarsenIPv4(req.Device.IP)
        }
        // Coarsen geo to postal code level
        if req.Device.Geo != nil {
            req.Device.Geo.Lat = math.Round(req.Device.Geo.Lat*100) / 100
            req.Device.Geo.Lon = math.Round(req.Device.Geo.Lon*100) / 100
        }
    }
    // Strip user.buyeruid if no valid consent
    if !hasValidConsent(req.Regs, req.User) {
        req.User = nil
    }
}

// Check GPC signal (CCPA opt-out)
func checkGPCOptOut(headers http.Header) bool {
    return headers.Get("Sec-GPC") == "1"
}
```

**Consent Validation Middleware:**
```go
func consentGate(req *openrtb2.BidRequest) error {
    // GDPR check
    if req.Regs != nil && req.Regs.Ext != nil {
        var regsExt map[string]interface{}
        json.Unmarshal(req.Regs.Ext, &regsExt)
        if gdpr, ok := regsExt["gdpr"].(float64); ok && gdpr == 1 {
            // Validate TCF consent string
            if req.User == nil || req.User.Ext == nil {
                return ErrNoConsent
            }
            consent := extractTCString(req.User.Ext)
            if !validateTCFConsent(consent, purposeIDs) {
                return ErrInsufficientConsent
            }
        }
    }
    // CCPA/GPC check -- suppress PII sharing
    if isUSPrivacyOptOut(req.Regs) {
        stripPIIForOptedOut(req)
    }
    return nil
}
```

### Migration Sequence

1. **Week 1-2:** Deploy Aerospike 5-node cluster with encryption at rest + TLS. Load test with synthetic bid requests at 100K/s, validate <1ms p99 reads.
2. **Week 3:** Deploy NATS 3-node cluster with JetStream. Test pub/sub fanout at 1M msg/s, validate <0.5ms delivery.
3. **Week 4:** Build PII pseudonymization layer and consent validation middleware. Unit test against OpenRTB 2.6 sample payloads.
4. **Week 5-6:** Deploy 20 bid processor nodes. Integration test full pipeline at 500K req/s with canary traffic.
5. **Week 7-8:** Ramp to 1M req/s. Monitor p99 latency, Aerospike read latency histograms, NATS slow consumer alerts. Run GDPR data subject access request (DSAR) and deletion test.
6. **Week 9+:** Production cutover with rollback plan (DNS-based traffic shifting).

---

## Alternatives Considered

### Why Not Redis + NATS (Option B)?

Redis+NATS is the cheapest option at ~$10,100/mo and meets the latency target. However:

- **Memory scaling risk:** Redis requires all data in RAM. At 1M req/s, user profile data grows rapidly. A 2TB dataset needs ~20 r7g.4xlarge nodes (~$7,500/mo just for Redis). Aerospike handles this on 5 nodes with SSD-backed storage.
- **No encryption at rest in OSS Redis.** Redis Enterprise (which adds it) costs $5,000-15,000/mo in licensing, eliminating the cost advantage.
- **Operational risk at 10 nodes:** More nodes = more failure surface. Aerospike's automatic rebalancing is more mature than Redis Cluster's manual resharding.

**Verdict:** Viable for datasets <500GB. Becomes more expensive than Aerospike as data grows. GDPR encryption-at-rest requirement forces Redis Enterprise licensing.

### Why Not Aerospike + Kafka (Option A)?

- **Kafka adds 3-8ms p99 latency** to the message fanout path, consuming most of the 10ms budget. Setting `linger.ms=0` reduces this but degrades throughput.
- **Operational overhead:** Kafka requires ZooKeeper (or KRaft), partition management, consumer group rebalancing -- significant ops burden.
- **Still fits budget** at $15,548/mo, but the latency risk is the disqualifier.

**Verdict:** Use Kafka *alongside* NATS -- NATS for hot-path bid fanout, Kafka (or NATS JetStream) for async event streaming, analytics, and win notification durability. This adds ~$715/mo but provides the durability guarantees Kafka excels at.

### Why Not Fully Managed Cloud (Option C)?

- **Highest cost** at $20,113/mo (2x the hybrid option).
- **Same latency problem** as Kafka if using MSK for bid fanout.
- **Vendor lock-in:** ElastiCache and MSK APIs are AWS-proprietary. Multi-cloud or migration becomes expensive.
- **Benefit:** Lowest ops burden. Reasonable choice if the team is <5 engineers and cannot staff Aerospike/NATS expertise.

**Verdict:** Appropriate for teams that value operational simplicity over cost and performance optimization. Consider if headcount is the binding constraint, not budget.

### Redpanda as Kafka Alternative

Redpanda (C++ Kafka-compatible) claims 10x lower tail latency than Kafka. If Kafka's durability semantics are needed on the hot path, Redpanda is worth evaluating -- but NATS remains faster for pure pub/sub fanout. *(Source: [Redpanda Benchmark](https://www.redpanda.com/blog/redpanda-vs-kafka-performance-benchmark))*

---

## Adversarial Review

### Counterarguments

**"Aerospike Enterprise licensing is a hidden cost trap."**
Valid concern. Aerospike prices by unique data volume, not operations. At current scale (~500GB-1TB unique data), the license is ~$5,000/mo. But at 5TB+, it could reach $15,000-25,000/mo. Mitigation: negotiate a fixed annual contract with a data volume cap. Even at $15K/mo, total cost ($24K/mo) is within budget.

**"NATS lacks Kafka's durability guarantees for regulatory audit trails."**
Correct. NATS JetStream provides at-least-once delivery with file-backed persistence, but Kafka's exactly-once semantics and indefinite retention are superior for compliance audit trails. Mitigation: use NATS for hot-path fanout, add Kafka (or NATS JetStream with R=3) for async event logging and audit trail persistence. This adds ~$700-1,500/mo.

**"The GDPR compliance requirements will kill RTB anyway."**
Partially valid. The Belgian DPA ruling and CJEU TC String decision create serious regulatory headwinds. However, RTB continues to operate under TCF 2.2, and the industry is adapting (Google Privacy Sandbox, on-device processing). The architecture recommended here (PII pseudonymization, consent-gated processing) is designed to survive regulatory tightening. The risk is not that RTB dies, but that it evolves toward less PII transmission -- which this architecture supports through the pseudonymization layer.

**"20 app servers is over-provisioned for 1M req/s."**
Each c7g.2xlarge (8 ARM vCPU) handles ~50K req/s with the full processing pipeline (deserialize, consent check, Aerospike lookup, NATS publish, auction, response). 20 nodes at 50K/s = 1M/s. This assumes 2x headroom for traffic spikes and GC pauses. Under-provisioning an ad exchange causes revenue loss (dropped bids), so conservative sizing is appropriate.

<details>
<summary><strong>Assumption Audit (click to expand)</strong></summary>

| Assumption | Status | Risk if Wrong |
|---|---|---|
| ~1KB average bid request payload | Reasonable (OpenRTB JSON typically 0.5-2KB) | If 3KB+, network costs increase 3x; may need more app server CPU |
| 1-year reserved instance pricing achievable | Verified (AWS standard offering) | On-demand pricing increases costs by ~60%; still within $50K |
| Aerospike Enterprise license ~$5K/mo at <1TB | Estimated (vendor-specific, not public) | Could be $8-10K/mo; still within budget. Contact Aerospike for quote. |
| 20 app servers sufficient at 50K req/s each | Reasonable for Go/Rust implementation | If using Java/Python, may need 30-40 nodes (+$1,500/mo) |
| NATS handles 1M msg/s on 3 nodes | Verified (benchmarks show 4.9M msg/s on single node) | Extremely unlikely to be insufficient |
| TCF 2.2 remains legally valid | Uncertain (Belgian DPA ruling covered TCF 1.0/2.0, not 2.2) | If TCF 2.2 is struck down, RTB consent model needs redesign |
| $50K/mo budget is infrastructure-only | Assumed | If budget must cover personnel, licensing, or SaaS tools, reduce infrastructure allocation |

</details>

### Failure Modes

1. **Aerospike cluster split-brain:** Rare but catastrophic. Mitigation: rack-aware configuration across 3+ AZs; automated monitoring with Prometheus + Aerospike exporter.
2. **NATS slow consumer cascade:** If bid processors fall behind, NATS can disconnect slow consumers, causing bid drops. Mitigation: configure `max_pending` limits; auto-scale bid processors on queue depth.
3. **PII leak through logging:** A common operational failure. Bid request logs may contain un-pseudonymized PII. Mitigation: structured logging with PII redaction filters; no raw bid request logging in production.
4. **GDPR subject access request (SAR) at scale:** If thousands of users request their data simultaneously, Aerospike secondary index queries could spike. Mitigation: pre-build user data export as async batch job, not real-time query.

---

## Recommendation

**Build on Aerospike (Enterprise) + NATS, with optional Kafka/JetStream for async durability.**

| Criterion | Decision |
|---|---|
| **Performance** | Aerospike <1ms reads + NATS <0.5ms fanout = ~4.8ms total p99, well under 10ms target |
| **Cost** | ~$14,343/mo base (29% of $50K budget), leaving room for growth and burst capacity |
| **GDPR/CCPA** | Aerospike EE provides encryption at rest (AES-256) + TLS; PII pseudonymization layer; consent-gated pipeline |
| **Ops complexity** | Moderate. Aerospike has a learning curve but is proven in ad tech (Criteo, The Trade Desk, AppsFly). NATS is operationally simple (single binary, no ZooKeeper). |
| **Scalability** | Aerospike linear scaling to petabytes (AWS case study). NATS horizontal scaling to millions msg/s. |

**Conditions under which this recommendation changes:**
- If the dataset is <200GB and will stay small: Redis+NATS is simpler and cheaper.
- If the team has <3 backend engineers: Managed Cloud (ElastiCache+MSK) reduces ops burden despite higher cost.
- If Kafka durability is required on the hot path (e.g., regulatory requirement for zero bid loss): evaluate Redpanda as a Kafka-compatible alternative with lower tail latency.
- If GDPR enforcement forces RTB to eliminate all PII from bid streams: the architecture still works (pseudonymized IDs only), but the competitive value proposition of the exchange changes.

---

## Sources

### Performance & Benchmarks
- [Aerospike AdTech Solutions](https://aerospike.com/solutions/industry/adtech/)
- [Aerospike vs Redis Benchmark Report](https://aerospike.com/resources/benchmarks/aerospike-vs-redis-benchmark-report/)
- [Aerospike Efficiency vs Redis](https://aerospike.com/blog/redis-efficiency/)
- [Amazon ElastiCache 500M RPS](https://aws.amazon.com/blogs/database/achieve-over-500-million-requests-per-second-per-cluster-with-amazon-elasticache-for-redis-7-1/)
- [NATS JetStream vs RabbitMQ vs Kafka 2025 Benchmarks](https://onidel.com/blog/nats-jetstream-rabbitmq-kafka-2025-benchmarks)
- [NATS and Kafka Compared - Synadia](https://www.synadia.com/blog/nats-and-kafka-compared)
- [Kafka Performance - Confluent](https://developer.confluent.io/learn/kafka-performance/)
- [Tune Kafka for Million Messages Per Second](https://oneuptime.com/blog/post/2026-01-25-tune-kafka-million-messages-per-second/view)
- [LinkedIn: 2 Million Writes/Second on Kafka](https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines)
- [Redpanda vs Kafka Performance Benchmark](https://www.redpanda.com/blog/redpanda-vs-kafka-performance-benchmark)
- [Flipkart 90 Million QPS with Aerospike](https://aerospike.com/blog/flipkart-journey-90-million-qps/)
- [Comparative Analysis Redis Aerospike Dragonfly 2025](https://www.acadlore.com/article/JORIT/2025_4_2/jorit.v4.2(8).05)

### RTB Architecture
- [Google Cloud: Infrastructure Options for RTB Bidders](https://cloud.google.com/architecture/infrastructure-options-for-rtb-bidders)
- [AWS: Building a Real-Time Bidding Platform](https://d1.awsstatic.com/whitepapers/Building_a_Real_Time_Bidding_Platform_on_AWS_v1_Final.pdf)
- [RTB Systems: Designing for <100ms Responses](https://systemdr.substack.com/p/real-time-ad-bidding-systems-rtb)
- [Redpanda DSP Reference Architecture](https://www.redpanda.com/blog/reference-architecture-demand-side-platform-adtech)
- [OpenRTB 2.6 Specification](https://github.com/InteractiveAdvertisingBureau/openrtb2.x/blob/main/2.6.md)
- [AWS RTB Fabric](https://aws.amazon.com/solutions/guidance/building-a-real-time-bidder-for-advertising-on-aws/)

### GDPR / CCPA / Privacy
- [Belgian Market Court Upholds EUR 250K Fine Against IAB](https://www.lewissilkin.com/en/insights/2025/05/27/iab-tcf-belgian-market-court-upholds-250-000-fine-against-iab-for-gdpr-violatio-102kyon)
- [Brussels Market Court Clarifies GDPR Roles in AdTech](https://technologyquotient.freshfields.com/post/102kcx6/brussels-market-court-clarifies-gdpr-roles-in-adtech-and-upholds-sanctions-agains)
- [Is the TCF Illegal? - Didomi](https://www.didomi.io/blog/tcf-iab-europe-belgian-apd-may-2025)
- [Collision Course Between RTB and GDPR - Columbia STLR](https://journals.library.columbia.edu/index.php/stlr/blog/view/662)
- [GDPR Article 5 Text](https://gdpr-text.com/read/article-5/)
- [CPPA Joint Investigative Privacy Sweep Sept 2025](https://cppa.ca.gov/announcements/2025/20250909.html)
- [Global Privacy Control](https://globalprivacycontrol.org/)
- [EDPB Guidelines on Pseudonymisation Jan 2025](https://www.edpb.europa.eu/system/files/2025-01/edpb_guidelines_202501_pseudonymisation_en.pdf)
- [RTB Privacy Concerns - TrustArc](https://trustarc.com/resource/privacy-concerns-real-time-bidding/)

### Cost & Pricing
- [AWS EC2 On-Demand Pricing](https://aws.amazon.com/ec2/pricing/on-demand/)
- [i4i.4xlarge Pricing - Vantage](https://instances.vantage.sh/aws/ec2/i4i.4xlarge)
- [r7g.4xlarge Pricing - Holori](https://calculator.holori.com/aws/ec2/r7g.4xlarge)
- [Aerospike Pricing](https://aerospike.com/products/features-and-editions/)
- [Redis Pricing](https://redis.io/pricing/)
- [Kafka Cost Comparison 2026 - AxonOps](https://axonops.com/blog/kafka-cost-comparison-2026-self-hosted-vs-amazon-msk-vs-confluent-cloud/)
- [Amazon MSK Pricing](https://aws.amazon.com/msk/pricing/)
- [Confluent Cloud Pricing](https://www.confluent.io/confluent-cloud/pricing/)
- [Synadia Cloud Pricing](https://docs.synadia.com/cloud/pricing)
- [Amazon ElastiCache Pricing](https://cloudchipr.com/blog/amazon-elasticache-pricing)

### Security & Encryption
- [Aerospike Enterprise Security](https://aerospike.com/products/features/enterprise-security/)
- [Aerospike Encryption at Rest Configuration](https://aerospike.com/docs/database/manage/security/encryption)
- [Aerospike TLS Configuration](https://aerospike.com/docs/database/manage/network/tls/)
- [AWS Ad Tech Workloads with Aerospike](https://aws.amazon.com/blogs/industries/running-ad-tech-workloads-on-aws-with-aerospike-at-petabyte-scale/)
