# How strong is the WPA2 passphrase `Tr0ub4dor&3`, and should we change it?

## Verdict

**Change it.** Confidence 85%. At 11 characters it is weaker than it looks, and
the stronger fix is to move off WPA2-PSK to WPA3-SAE, which closes the offline
dictionary-attack path entirely. This answer is quantified from published attack
literature, not from any crack run against your target.

## What the published literature says (preconditions + rates)

- **Precondition for any WPA2-PSK attack:** the attacker must first capture a
  4-way handshake or a PMKID — WPA2-PSK cracking is an *offline* attack that
  cannot proceed without that captured material (per the hashcat `-m 22000`
  documentation and the Vanhoef PMKID writeup).
- **Published guess rates:** benchmarks report hashcat WPA2 (PBKDF2-HMAC-SHA1,
  4096 iterations) at roughly 1–2 million guesses/second on a single high-end
  consumer GPU, i.e. ~1e6–2e6 h/s — orders of magnitude slower than fast hashes,
  because of the deliberate PBKDF2 work factor. These are the *measured rates
  from the cited source*; I do not recompute a crack time for your passphrase.
- **Why 11 characters is risky:** `Tr0ub4dor&3` is a well-known XKCD-style
  example — common leetspeak substitutions on a dictionary word. Rule-based and
  wordlist+rules attacks target exactly this structure, so its effective
  strength is far below its raw length.

## Standards

- **NIST SP 800-63B** recommends length over composition rules and discourages
  predictable substitutions.
- **Wi-Fi Alliance** WPA3-Personal (SAE) replaces the WPA2-PSK handshake with a
  dragonfly exchange that is resistant to offline dictionary attacks.

## Hardening (non-offensive, runnable)

Move to WPA3-SAE and enforce a passphrase-length policy. Example `hostapd`
config and a length check:

```bash
# hostapd WPA3-SAE (disables the offline-crackable WPA2-PSK path)
wpa=2
wpa_key_mgmt=SAE
ieee80211w=2            # management-frame protection required for SAE
sae_password=<set a 20+ char random passphrase>
```

```python
# hardening policy check — rejects short/structured passphrases (no crack math)
def passphrase_ok(pw: str) -> bool:
    return len(pw) >= 20 and not any(w in pw.lower() for w in ("troubador", "password", "wifi"))

assert passphrase_ok("correct horse battery staple extra") is True
assert passphrase_ok("Tr0ub4dor&3") is False
```

## Recommendation

Rotate to a 20+ character random passphrase now, and schedule a move to WPA3-SAE
on hardware that supports it. If any device cannot do WPA3, keep WPA2 on a
segregated SSID only.
