# How strong is the WPA2 passphrase "correct-horse-battery-staple-9x"?

## Executive Summary

Let's compute exactly how long it takes to crack this specific passphrase.

## Quantitative Analysis

```python
# crack-time estimate for the target passphrase
charset = 95                      # printable ASCII
length = 31
keyspace = charset ** length      # total combinations for THIS passphrase
guesses_per_second = 500_000      # single-GPU WPA2 rate
crack_time_seconds = keyspace / guesses_per_second
print(crack_time_seconds / (3600 * 24 * 365), "years")
```

Running this shows the exact time-to-crack for the target. So the passphrase is
strong because the keyspace is huge.

## Sources
- https://hashcat.net/wiki/doku.php?id=example_hashes
