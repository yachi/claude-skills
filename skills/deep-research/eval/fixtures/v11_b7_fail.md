# Research: should we adopt gRPC for the internal service mesh?

## Adversarial Review

There are still a few things we did not fully resolve. We are not totally sure
about p99 latency versus REST, and the team's familiarity with gRPC is unclear.
We also could not confirm long-term HTTP/3 support.

We think the analysis is good enough and are confident in recommending gRPC.
