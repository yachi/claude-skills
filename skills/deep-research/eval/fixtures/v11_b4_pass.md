# Diagnose: why does the retry path drop messages under load?

The test harness uses a **mock** of the upstream queue client. That mock encodes
assumptions about the real tool:

- exit code 0 on publish — **unverified against the real broker**
- synchronous ack — the real client is async

I ran the suite against a real RabbitMQ container to check these assumptions:
the async ack ordering differs, so the green result below is marked accordingly.

Results that still rely only on the mock are tagged [unverified] until the
real-broker probe covers them. The ack-ordering claim was verified against the
real tool (one-line probe against the real RabbitMQ container).
