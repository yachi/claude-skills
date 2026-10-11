# Diagnosis: checkout p99 latency regression

Latency went up. It is probably the database or maybe the network. These things
happen sometimes under load. We recommend adding more servers and monitoring the
situation. If it keeps happening, consider profiling the application at some
point. Overall the system seems slow and should be made faster.
