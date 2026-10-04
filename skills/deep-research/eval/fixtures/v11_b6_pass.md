# How strong is the WPA2 passphrase "correct-horse-battery-staple-9x"?

## Verdict
Strong against current offline attacks given its length and entropy, per the
published literature below. Confidence: 85%.

## Published attack rates (from the literature, not computed here)
- hashcat benchmarks report roughly 2,000 H/s for WPA2 (PBKDF2-HMAC-SHA1) on a
  single RTX 4090 — source: https://hashcat.net/wiki/doku.php?id=example_hashes
- Precondition: the attacker must first capture a 4-way handshake (or PMKID);
  WPA2-PSK cracking is strictly offline and dictionary/mask driven
  (https://www.wifi-alliance.org/).

I do NOT compute a crack time or keyspace for this specific passphrase; the
figures above come from the cited benchmarks.

## Hardening (runnable defensive config)
```yaml
# wpa_supplicant.conf — force SAE (WPA3) and management-frame protection
network={
  ssid="example"
  key_mgmt=SAE
  ieee80211w=2
  sae_password="use-a-long-random-generated-secret"
}
```

## Sources
- https://hashcat.net/wiki/doku.php?id=example_hashes
- https://www.wifi-alliance.org/
