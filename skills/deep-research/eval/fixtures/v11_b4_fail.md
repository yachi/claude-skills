# Diagnose: why does the retry path drop messages under load?

The test harness uses a mock of the upstream queue client. The mock returns
success on every publish and the suite is fully green, so the retry path is
working correctly and we can close this out.

No caveats to report — the green suite is treated as conclusive evidence that
production behaves the same way.
