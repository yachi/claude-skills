# How strong is the WPA2 passphrase "correct-horse-battery-staple-9x"?

## Crack-time estimate for this passphrase
I computed the keyspace and crack time for the target below.

```python
# brute-force crack-time estimate for the target passphrase
charset = 95
length = 30
keyspace = charset ** length
guesses_per_sec = 2000  # WPA2 H/s on one GPU
crack_time = keyspace / guesses_per_sec
print(crack_time / (3600 * 24 * 365), "years")
```

So the passphrase would take about that long to brute force on one GPU.

## Sources
- https://hashcat.net/
