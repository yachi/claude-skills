# Should we adopt gRPC for internal service calls?

## Executive Summary

Yes — gRPC reduces p99 latency vs JSON/HTTP for internal calls. Confidence: 78%.

## Key Findings

1. Protobuf payloads are ~60% smaller than equivalent JSON.
2. HTTP/2 multiplexing removes head-of-line blocking at the connection level.

## Adversarial Review

Some teams report debugging friction without reflection enabled. We note this
and move on. No remaining questions were tracked and we stopped here.

## Recommendation

Adopt gRPC for internal service-to-service calls.
