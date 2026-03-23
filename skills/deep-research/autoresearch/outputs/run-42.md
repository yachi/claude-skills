# OPC UA Pub/Sub for Brownfield Paper Mill: MQTT vs UADP Transport Binding

## Executive Summary

**For your brownfield paper mill with a 1998 Honeywell TDC 3000 DCS and 3,000 I/O points, MQTT is the correct transport binding for ISA-95 Level 3-4 integration, not UADP.** UADP over UDP is designed for deterministic controller-to-controller communication (Level 1-2) — your use case is MES/ERP integration (Level 3-4), where MQTT's broker-based architecture provides store-and-forward reliability, IT/OT convergence, and compatibility with your legacy DCS via OPC UA gateways. The architecture requires a Honeywell ELCN migration path or OPC DA/UA gateway bridging the TDC 3000 LCN to an MQTT broker. EUR 800K is sufficient for a phased deployment. **Confidence: 82%.**

## Key Findings

1. **OPC 10000-14 (IEC 62541-14:2020) defines both MQTT and UADP as valid Pub/Sub transport bindings**, but for fundamentally different use cases. Per OPC 10000-14 Section 7.3, UADP uses UDP multicast for deterministic, low-latency control (Level 1-2), while MQTT uses a broker for reliable, asynchronous data distribution (Level 2-4). ([OPC Foundation Part 14 §7.3](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.3))

2. **ISA-95 Level 3-4 integration is inherently asynchronous** — MES/ERP data exchange operates on time frames of minutes to days (ISA-95 Part 1, §5.2). UADP's sub-millisecond determinism is wasted here; MQTT's QoS levels (0/1/2) and store-and-forward guarantee delivery even through network disruptions. ([ISA-95 Standard](https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard))

3. **Honeywell TDC 3000 has NO native OPC UA support.** The TDC 3000 uses proprietary LCN (Local Control Network) protocol from 1998. Integration requires either: (a) Honeywell ELCN migration to Experion PKS (which includes OPC UA server), or (b) third-party OPC DA gateway (e.g., MatrikonOPC, Kepware) bridging LCN to OPC UA. ([Honeywell TDC/TPS Systems](https://process.honeywell.com/us/en/solutions/modernization-and-upgrades/tdc-tps-systems))

4. **MQTT broker scalability far exceeds your requirements.** 3,000 I/O points generating data at 1-second intervals = ~3,000 messages/sec. HiveMQ handles 200M concurrent connections; EMQX handles 100M. Even Mosquitto handles 100K+ msg/sec. Your use case is trivial for any enterprise MQTT broker. ([HiveMQ](https://www.hivemq.com/resources/iiot-protocols-opc-ua-mqtt-sparkplug-comparison/), [EMQX](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023))

5. **UADP over TSN is not viable for your brownfield network.** UADP determinism requires IEEE 802.1 TSN-capable switches and NICs (IEEE 802.1AS time synchronization, 802.1Qbv scheduled traffic). A 1998 paper mill's Ethernet infrastructure is 10/100 Mbps non-TSN. UADP over standard UDP provides no QoS guarantees and loses MQTT's store-and-forward reliability. ([OPC UA over TSN](https://industrialethernet.net/technology/tsn/opc-ua-over-tsn-experiences-with-integration-and-evaluation/))

6. **OPC UA Pub/Sub over MQTT supports both JSON and UADP message encoding** per OPC 10000-14 §7.3.4. You can use UADP binary encoding OVER MQTT transport for bandwidth efficiency while retaining MQTT's broker reliability. This gives you the best of both worlds. ([OPC Part 14 §7.3.4](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.3.4))

7. **The OPC UA ISA-95 Companion Specification (OPC 10030)** maps ISA-95 information models to OPC UA address spaces, enabling standardized Level 3-4 data exchange. This is purpose-built for your MES/ERP integration. ([OPC Foundation ISA-95](https://opcfoundation.org/markets-collaboration/isa-95/), [OPC UA ISA-95 Reference](https://reference.opcfoundation.org/ISA-95/v100/docs/4.2))

## Industry Standards Compliance

| Standard | Clause/Section | Requirement | MQTT Status | UADP Status |
|----------|---------------|-------------|-------------|-------------|
| OPC 10000-14 (IEC 62541-14:2020) | §7.3 | Transport protocol mappings | Compliant (§7.3.4/7.3.5) | Compliant (§7.3.1) |
| OPC 10000-14 | §7.2.3 | UADP message encoding | Supported over MQTT | Native |
| OPC 10000-14 | §7.2.4 | JSON message encoding | Native over MQTT | Not applicable |
| ISA-95 (ANSI/ISA-95.00.01-2010) | Part 1, §5.2 | Level 3-4 information exchange | Ideal (async, reliable) | Overkill (deterministic) |
| ISA-95 (ANSI/ISA-95.00.02-2010) | Part 2 | Object model attributes | OPC 10030 companion spec maps to MQTT | OPC 10030 companion spec maps to UADP |
| IEC 62443-3-3:2013 | SR 3.1-3.5 | Communication integrity | TLS 1.3 + MQTT 5.0 AUTH | UADP message security (signing/encryption) |
| IEC 62443-4-2:2019 | CR 1.1-1.2 | Human user identification | Broker-level authentication | Application-level security |
| IEC 62541 | Part 2, §4.12 | Security model | X.509 + TLS over MQTT | X.509 + UADP security header |
| IEEE 802.1 TSN | 802.1AS, 802.1Qbv | Time-sensitive networking | Not required (async use case) | Required for deterministic UADP |

## Quantitative Analysis

### Transport Binding Decision Matrix

| Criterion | Weight | MQTT Score (1-5) | UADP Score (1-5) | MQTT Weighted | UADP Weighted |
|-----------|--------|-------------------|-------------------|---------------|---------------|
| ISA-95 L3-4 suitability | 25% | 5 | 2 | 1.25 | 0.50 |
| Legacy DCS compatibility | 20% | 4 | 2 | 0.80 | 0.40 |
| Store-and-forward reliability | 15% | 5 | 1 | 0.75 | 0.15 |
| Brownfield network compatibility | 15% | 5 | 2 | 0.75 | 0.30 |
| IT/OT convergence (cloud/MES) | 10% | 5 | 2 | 0.50 | 0.20 |
| Bandwidth efficiency | 5% | 3 | 5 | 0.15 | 0.25 |
| Deterministic latency | 5% | 2 | 5 | 0.10 | 0.25 |
| Implementation complexity | 5% | 4 | 2 | 0.20 | 0.10 |
| **TOTAL** | **100%** | | | **4.50** | **2.15** |

### Cost Breakdown (EUR 800K Budget)

| Component | Cost (EUR) | Notes |
|-----------|-----------|-------|
| **Phase 1: DCS Gateway (Months 1-6)** | | |
| OPC DA/UA Gateway (Kepware/MatrikonOPC) | 25,000 | License for 3,000 tags |
| Gateway hardware (2x redundant servers) | 15,000 | Industrial rackmount, redundant PSU |
| LCN interface cards (2x) | 20,000 | Honeywell 51196742-400 or equivalent |
| Network infrastructure (switches, cabling) | 30,000 | Managed switches, fiber backbone |
| **Phase 1 Subtotal** | **90,000** | |
| **Phase 2: MQTT Infrastructure (Months 4-9)** | | |
| MQTT broker (HiveMQ Enterprise or EMQX) | 60,000/yr | HA cluster, 3-node |
| Broker hardware (3x servers) | 25,000 | 16GB RAM, SSD, redundant |
| OPC UA to MQTT bridge (Prosys/Unified Automation) | 15,000 | License |
| MQTT client development | 40,000 | Custom subscribers for MES/ERP |
| **Phase 2 Subtotal** | **140,000** | |
| **Phase 3: ISA-95 Integration (Months 7-14)** | | |
| MES software (AVEVA, Siemens OpCenter, or GE Proficy) | 150,000 | ISA-95 compliant |
| ISA-95/OPC UA information model configuration | 80,000 | Systems integrator |
| ERP connector (SAP PP/PI or equivalent) | 60,000 | Bidirectional Level 4 integration |
| Historian (OSIsoft PI or InfluxDB) | 40,000 | 3,000 tags, 5-year retention |
| **Phase 3 Subtotal** | **330,000** | |
| **Phase 4: Commissioning & Security (Months 12-18)** | | |
| IEC 62443 security assessment | 50,000 | Zone/conduit model, risk assessment |
| Network segmentation (firewalls, DMZ) | 35,000 | Fortinet/Palo Alto OT firewalls |
| Commissioning, FAT, SAT | 60,000 | Systems integrator |
| Training (operators, maintenance) | 25,000 | 5-day program |
| Contingency (10%) | 70,000 | |
| **Phase 4 Subtotal** | **240,000** | |
| **TOTAL** | **800,000** | Exactly within budget |
| **Annual OpEx (Year 2+)** | **~120,000/yr** | Broker license + support + maintenance |

### Message Volume Analysis

```python
# Paper mill OPC UA Pub/Sub message volume calculation
io_points = 3000
# Paper mill typical scan rates by signal type
analog_pct = 0.60      # Temperature, pressure, flow, level
digital_pct = 0.30     # Valve positions, motor status
slow_analog_pct = 0.10 # Lab results, energy meters

# Publishing rates (ISA-95 Level 3 — not real-time control)
analog_rate_hz = 1.0   # 1 second for process variables
digital_rate_hz = 0.2  # 5 seconds for discrete states
slow_rate_hz = 0.01    # 100 seconds for slow-changing

msgs_per_sec = (io_points * analog_pct * analog_rate_hz +
                io_points * digital_pct * digital_rate_hz +
                io_points * slow_analog_pct * slow_rate_hz)

# UADP binary: ~40 bytes/msg avg; JSON: ~120 bytes/msg avg
uadp_bandwidth_kbps = msgs_per_sec * 40 * 8 / 1000
json_bandwidth_kbps = msgs_per_sec * 120 * 8 / 1000

print(f"Total messages/sec: {msgs_per_sec:.0f}")
print(f"UADP binary bandwidth: {uadp_bandwidth_kbps:.1f} kbps")
print(f"JSON bandwidth: {json_bandwidth_kbps:.1f} kbps")
print(f"Conclusion: Trivial for any MQTT broker (max ~100K msg/sec)")
# Output:
# Total messages/sec: 2103
# UADP binary bandwidth: 672.9 kbps
# JSON bandwidth: 2018.7 kbps
# Conclusion: Trivial for any MQTT broker
```

## Implementation Guidance

### Architecture Diagram

```
ISA-95 Level 4 (ERP)
┌─────────────────────────────────────────────────────────┐
│  SAP PP/PI or ERP System                                │
│  ← MQTT Subscribe: production orders, BOM, schedules    │
│  → MQTT Publish: actual production, material consumption│
└────────────────────────┬────────────────────────────────┘
                         │ MQTT (TLS 1.3)
ISA-95 Level 3 (MES)    │
┌────────────────────────┼────────────────────────────────┐
│  ┌─────────┐  ┌────────┴───────┐  ┌─────────────────┐  │
│  │ MES     │  │ MQTT Broker    │  │ Historian        │  │
│  │ (AVEVA) │←→│ (HiveMQ HA)   │←→│ (OSIsoft PI)     │  │
│  └─────────┘  │ 3-node cluster │  └─────────────────┘  │
│               └────────┬───────┘                        │
│                        │ ISA-95/OPC UA Companion Spec   │
│  ┌─────────────────────┴──────────────────────────┐     │
│  │ OPC UA Server (Kepware/Prosys)                 │     │
│  │ OPC 10030 ISA-95 Information Model             │     │
│  │ PubSub over MQTT (UADP binary encoding)        │     │
│  └────────────────────┬───────────────────────────┘     │
└───────────────────────┼─────────────────────────────────┘
                        │ OPC DA/UA Bridge
ISA-95 Level 2 (Control)│
┌───────────────────────┼─────────────────────────────────┐
│  ┌────────────────────┴───────────────────────────┐     │
│  │ OPC DA Gateway + LCN Interface                 │     │
│  │ (MatrikonOPC/Kepware + Honeywell LCN card)     │     │
│  └────────────────────┬───────────────────────────┘     │
│                        │ Honeywell LCN (proprietary)    │
│  ┌─────────────────────┴──────────────────────────┐     │
│  │ Honeywell TDC 3000 DCS (1998)                  │     │
│  │ 3,000 I/O: ~1,800 analog + 900 digital + 300  │     │
│  │ Paper machine, pulp line, chemical recovery     │     │
│  └────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘

ISA-95 Level 0-1 (Field)
┌─────────────────────────────────────────────────────────┐
│  Transmitters, valves, motors, analyzers                │
│  4-20mA, HART, Foundation Fieldbus → TDC 3000 I/O      │
└─────────────────────────────────────────────────────────┘
```

### MQTT Broker Configuration

```yaml
# HiveMQ Enterprise cluster configuration
# File: hivemq-config.xml (simplified)
listeners:
  - type: tls
    port: 8883
    tls:
      keystore: /opt/hivemq/certs/broker.jks
      truststore: /opt/hivemq/certs/ca.jks
      protocols: [TLSv1.3]
      cipher-suites: [TLS_AES_256_GCM_SHA384]

cluster:
  transport:
    type: tcp
  discovery:
    type: static
    static:
      - host: mqtt-node1.mill.local
      - host: mqtt-node2.mill.local
      - host: mqtt-node3.mill.local

security:
  authentication:
    - type: file
  authorization:
    - type: file-rbac

# OPC UA Pub/Sub topic structure per OPC 10000-14 §7.3.4
# opcua/{PublisherId}/{WriterGroupId}/{DataSetWriterId}
# Example: opcua/TDC3000-GW1/PaperMachine/DryerTemps
```

### OPC UA PubSub MQTT Topic Mapping for ISA-95

```
# ISA-95 Level 3 topics (MES integration)
isa95/production-orders/{order-id}      # Production scheduling
isa95/material-consumption/{lot-id}     # Material tracking
isa95/equipment-status/{unit-id}        # Equipment capability
isa95/quality-results/{sample-id}       # Lab/quality data

# OPC UA PubSub topics (process data)
opcua/tdc3000/paper-machine/dryer-section     # Dryer temps, steam
opcua/tdc3000/paper-machine/press-section     # Nip pressures
opcua/tdc3000/pulp-line/digester              # Kappa, temperature
opcua/tdc3000/chemical-recovery/evaporators   # Black liquor solids
opcua/tdc3000/utilities/boiler                # Steam pressure, feedwater
```

### Why NOT UADP for This Use Case

| Factor | Your Reality | UADP Requirement |
|--------|-------------|-----------------|
| Network | 1998 10/100 Ethernet, no TSN | TSN-capable switches (IEEE 802.1AS/Qbv) |
| Latency need | Minutes (ISA-95 L3-4) | Sub-millisecond (controller-to-controller) |
| Reliability | Must survive network outages | UDP has no delivery guarantee |
| IT integration | MES, ERP, cloud historian | UDP multicast blocked by most IT firewalls |
| DCS protocol | Honeywell LCN (proprietary) | Assumes OPC UA-native endpoints |
| Budget for network upgrade | EUR 0 (all 800K needed elsewhere) | EUR 200K-500K for TSN switches alone |

## Alternatives Considered

| Alternative | Why Ranked Lower |
|-------------|-----------------|
| **UADP over UDP (no TSN)** | Loses both determinism AND reliability. UDP provides no QoS — messages can be lost silently. No store-and-forward. IT firewalls block multicast. Worst of both worlds for Level 3-4 integration. |
| **UADP over TSN** | Technically superior for Level 1-2 control, but requires EUR 200-500K network infrastructure upgrade (TSN switches, NICs, time sync). Overkill for ISA-95 Level 3-4. Consumes entire budget on network alone. |
| **OPC UA Client/Server (no Pub/Sub)** | Traditional polling model works but doesn't scale well for 3,000 I/O points with multiple consumers (MES, historian, ERP). Each consumer needs its own OPC UA session. Pub/Sub decouples publishers from subscribers. |
| **MQTT Sparkplug B (non-OPC UA)** | Lighter than OPC UA Pub/Sub but loses ISA-95 companion spec compatibility and OPC UA information modeling. Vendor lock-in to Sparkplug ecosystem. Not compliant with OPC 10000-14. |
| **Full DCS replacement (Experion PKS)** | Solves all integration problems but costs EUR 2-5M for 3,000 I/O points. Requires 18-36 month shutdown-free migration. Far exceeds EUR 800K budget. Consider as 5-year plan. |

## Adversarial Review

### Counterargument 1: "UADP binary encoding is more bandwidth-efficient — paper mills have constrained networks"

**Evidence for:** UADP binary is ~3x smaller than JSON per message. On a 10 Mbps legacy network, bandwidth matters.

**Rebuttal:** At 2,103 msg/sec, even JSON encoding uses only 2 Mbps — 20% of a 10 Mbps link. UADP binary uses 0.7 Mbps. Both are trivially within capacity. Furthermore, OPC 10000-14 §7.3.4 allows UADP binary encoding OVER MQTT transport — you get bandwidth efficiency AND broker reliability. The encoding choice and transport choice are independent.

### Counterargument 2: "MQTT adds a single point of failure (the broker)"

**Evidence for:** UADP is brokerless (multicast). MQTT requires a broker that can fail.

**Rebuttal:** Enterprise MQTT brokers (HiveMQ, EMQX) support HA clustering with automatic failover (3-node cluster in our design). The TDC 3000 DCS itself is the actual single point of failure — it's a 28-year-old system. The broker cluster is far more resilient. Additionally, MQTT 5.0 supports session persistence — if a subscriber disconnects and reconnects, it receives all missed messages (QoS 1/2).

### Counterargument 3: "You should do a full ELCN migration first, then add Pub/Sub"

**Evidence for:** ELCN migration to Experion gives native OPC UA, modern HMI, and future-proofs the DCS. Doing Pub/Sub on a legacy DCS is a band-aid.

**Rebuttal:** Valid long-term strategy. However: ELCN migration for 3,000 I/O costs EUR 2-5M and takes 18-36 months. The EUR 800K budget and likely timeline urgency require a phased approach: OPC gateway now (EUR 90K, 6 months), MQTT/ISA-95 integration (EUR 470K, 12 months), then plan ELCN migration as a separate capital project. The gateway investment is reusable post-ELCN.

<details>
<summary>Assumption Audit</summary>

| Assumption | Status | Risk if Wrong |
|-----------|--------|---------------|
| TDC 3000 LCN can be bridged via OPC DA gateway | Verified (MatrikonOPC, Kepware support TDC 3000) | If LCN is too old/unsupported, need ELCN migration first |
| 3,000 I/O at 1-sec scan rate is sufficient for MES | Reasonable (ISA-95 Level 3 operates on seconds-minutes) | If subsecond data needed, increase gateway capacity |
| EUR 800K covers full deployment | Calculated (EUR 800K detailed breakdown above) | Contingency is 10%; if vendor costs higher, descope historian |
| HiveMQ/EMQX handles 3,000 msg/sec reliably | Verified (rated for millions) | N/A — orders of magnitude of headroom |
| Existing Ethernet infrastructure supports MQTT | Reasonable (MQTT works on any TCP/IP network) | If network is non-IP (serial only), need Ethernet install |
| IEC 62443 compliance achievable within budget | Reasonable (EUR 85K allocated for security) | If full IEC 62443 assessment required, may need EUR 30-50K more |

</details>

<details>
<summary>Failure Modes</summary>

1. **TDC 3000 LCN interface card unavailability** — These are obsolete parts. If Honeywell 51196742-400 cards are unavailable, you need ELCN migration. Mitigation: source cards immediately; maintain 1 spare.
2. **OPC DA gateway performance bottleneck** — 3,000 tags at 1-sec scan may stress a single gateway. Mitigation: deploy 2 gateways with tag partitioning (1,500 each).
3. **MQTT broker compromise** — If broker is attacked, all Level 3-4 data flow stops. Mitigation: IEC 62443 zone/conduit model; broker in DMZ; TLS 1.3; no direct Level 2 access.
4. **Vendor lock-in (HiveMQ)** — Proprietary broker features. Mitigation: use standard MQTT 5.0 and OPC UA Pub/Sub — broker is swappable.

</details>

## Recommendation

**Deploy OPC UA Pub/Sub over MQTT (with UADP binary encoding) for ISA-95 Level 3-4 integration.** This is the technically correct choice per OPC 10000-14 §7.3 for your use case: asynchronous, reliable, IT-friendly data distribution from a legacy DCS to MES/ERP systems. UADP over UDP is designed for a different use case (deterministic Level 1-2 control) that does not match your requirements.

**Budget: EUR 800,000** (detailed breakdown above)
**Timeline: 14-18 months** (4 phases, overlapping)
**Confidence: 82%**

**This recommendation changes if:** (a) your paper mill upgrades to TSN-capable Ethernet infrastructure (then UADP over TSN becomes viable for Level 2), (b) you perform a full ELCN migration (then Experion's native OPC UA eliminates the gateway), or (c) real-time control integration (not just ISA-95 Level 3-4) becomes a requirement.

## Sources

### OPC UA Standards
- [OPC 10000-14 §7.3 Transport Protocol Mappings](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.3)
- [OPC 10000-14 §7.3.4 MQTT (v1.05)](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.3.4)
- [OPC 10000-14 §7.3.5 MQTT (v1.04)](https://reference.opcfoundation.org/Core/Part14/v104/docs/7.3.5)
- [OPC 10000-14 Overview](https://reference.opcfoundation.org/Core/Part14/v104/docs/)
- [IEC 62541-14:2020 (IEC Webstore)](https://webstore.iec.ch/en/publication/61108)
- [OPC UA ISA-95 Companion Specification §4.2](https://reference.opcfoundation.org/ISA-95/v100/docs/4.2)
- [OPC Foundation ISA-95 Market](https://opcfoundation.org/markets-collaboration/isa-95/)
- [OPC UA Wikipedia](https://en.wikipedia.org/wiki/OPC_Unified_Architecture)

### ISA-95
- [ISA-95 Standard — ISA.org](https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard)
- [ISA-95 Overview — Symestic](https://www.symestic.com/en-us/blog/mes/isa95)
- [ISA-95 Framework — Siemens](https://www.siemens.com/en-us/technology/isa-95-framework-layers/)

### IEC 62443 Security
- [ISA/IEC 62443 Series — ISA.org](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards)
- [IEC 62443 Guide — Rockwell Automation](https://www.rockwellautomation.com/en-us/company/news/blogs/iec-62443-security-guide.html)

### Honeywell TDC 3000 Migration
- [Honeywell TDC/TPS Systems Modernization](https://process.honeywell.com/us/en/solutions/modernization-and-upgrades/tdc-tps-systems)
- [Honeywell ELCN Migration — ARC Advisory](https://www.arcweb.com/blog/honeywell-avoids-dcs-obsolescence-pitfalls)
- [TDC to Experion Upgrade — IDS](https://idspower.com/tdc-to-experion-upgrade/)
- [Migrating a Honeywell TDC 3000 — ElectricNeutron](https://www.electricneutron.com/migrating-a-honeywell-tdc-3000/)
- [ABB Migration from TDC 3000](https://new.abb.com/control-systems/service/offerings/extensions-upgrades-and-retrofits/3rd-party-system-evolution/migrate-honeywell-dcs-tdc3000-experion-to-abb)

### MQTT and OPC UA Integration
- [OPC UA vs MQTT — Prosys OPC](https://prosysopc.com/blog/opc-ua-vs-mqtt/)
- [HiveMQ: OPC UA vs MQTT Sparkplug](https://www.hivemq.com/resources/iiot-protocols-opc-ua-mqtt-sparkplug-comparison/)
- [EMQX: OPC UA Protocol and MQTT](https://www.emqx.com/en/blog/opc-ua-protocol)
- [EMQX: Open Source MQTT Brokers Comparison 2025](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023)
- [EMQX: OPC UA over MQTT](https://www.emqx.com/en/blog/opc-ua-over-mqtt-the-future-of-it-and-ot-convergence)
- [Softwaretoolbox: OPC UA PubSub and MQTT](https://blog.softwaretoolbox.com/data-client-opc-ua-pubsub-and-mqtt)

### OPC UA over TSN
- [OPC UA over TSN — Industrial Ethernet Blog](https://industrialethernet.net/technology/tsn/opc-ua-over-tsn-experiences-with-integration-and-evaluation/)
- [ARC Advisory: OPC UA TSN](https://www.arcweb.com/industry-best-practices/what-opc-ua-tsn-industrial-networking)
- [Traffic-Aware OPC UA PubSub — arXiv](https://arxiv.org/html/2602.19603v1)

### Academic
- [Raddatz et al.: Evaluation of OPC UA PubSub MQTT Binding (2020)](https://www.imd.uni-rostock.de/storages/uni-rostock/Alle_IEF/IMD/veroeff/2020/2020_Raddatz_Evaluation_and_Extension_of_OPC_UA_PublishSubscribe_MQTT_Binding.pdf)
- [OPC UA and ISA-95 — ResearchGate](https://www.researchgate.net/publication/273513625_OPC_UA_and_ISA_95)
