# How strong is the office Wi-Fi WPA2 passphrase `Tr0ub4dor&3`, and what should replace it?

**Deliverable type:** Decision (change / keep, and what to change to) — delivered as a research report.
**Research mode:** Defensive-security. This report quantifies passphrase strength from *published* attack literature, benchmarks, and standards. It does **not** run any crack, keyspace enumeration, or guess-rate computation against your specific passphrase; all attacker-capability figures are cited from primary sources.
**Scope:** Covers the strength of the PSK itself, the standards it is judged against, and how to pick a replacement. Does **not** cover your AP firmware/CVEs, RADIUS/802.1X migration, client inventory, or physical security of the AP.

## Executive Summary

**Change it now. `Tr0ub4dor&3` is one of the weakest possible choices — not because of its length, but because it is a world-famous published example password.** It is the exact string from XKCD comic #936 ("Password Strength"), reproduced in millions of pages, security talks, and almost certainly in the wordlists and mangling-rule sets every Wi-Fi cracker ships with. Its real-world strength against a modern offline WPA2 attack is effectively **zero** — it would fall in the wordlist-plus-rules phase that runs before any brute force even begins. The comic itself rates this *style* of password at only ~28 bits of entropy. Replace it with a randomly generated **6-word EFF Diceware passphrase (~77 bits)**, and if your hardware supports it, move the network to **WPA3-Personal (SAE)** in non-transition mode.
**Overall confidence: 98%.**

## Key Findings

1. **`Tr0ub4dor&3` is the literal XKCD #936 example password, not a private secret.** The comic uses it as its *bad* example — a dictionary word ("troubadour") with predictable leet substitution and a punctuation+digit suffix. The comic's own stated entropy for this scheme is **~28 bits**, versus **~44 bits** for its "correct horse battery staple" counter-example [xkcd.com/936; explainxkcd.com/wiki/936 — primary]. Because the string is published verbatim across the internet, an attacker does not even need the entropy math: it is a known plaintext that sits at the top of curated password dictionaries. *Evidence type: primary source (the comic itself) + widespread secondary reproduction.*

2. **Even treating it as a generic pattern, it is exactly what rule-based cracking targets.** Hashcat's rule engine applies leetspeak substitution (`a→4`, `e→3`, `o→0`), capitalization, and digit/suffix appending to every dictionary word — "the single highest-value technique because real users transform base words predictably (Summer → Summer2025!)" [tutorials.technology Hashcat rule guide; Hashcat wiki]. `Troubadour → Tr0ub4dor&3` is this transformation applied to a dictionary word. A third-party strength checker rates the raw string at ~51.8 bits [security.stackexchange.com #6095], but that figure assumes random character selection; against a wordlist+rules attack the effective search space collapses to a few million candidates. *Evidence type: tool documentation + expert consensus.*

3. **WPA2-PSK gives the attacker an offline oracle, and modern GPUs chew through it.** A captured 4-way handshake (or a single PMKID frame) lets an attacker guess passphrases entirely offline, with no further contact with your AP [koutto/pi-pwnbox wiki; SecurityWeek 2023 on Steube's PMKID method]. WPA2 derives the key with `PMK = PBKDF2(HMAC-SHA1, PSK, SSID, 4096, 256)` — the 4096 iterations are the only brake [IEEE 802.11i; Hashcat wiki mode 22000]. Even so, a **single NVIDIA RTX 4090 sustains ~2,600 kH/s on hashcat mode 22000** (WPA-PBKDF2-PMKID+EAPOL) [hashcat.net forum benchmarks]. That rate annihilates any wordlist-reachable password; the 4096-iteration cost only matters for *high-entropy random* secrets. *Evidence type: first-party vendor benchmarks + protocol spec.*

4. **The PMKID attack means an attacker may not even need a connected client.** Since 2018, hcxdumptool can request a PMKID directly from the AP and dump a crackable hash, "clientless — no deauth needed," typically within ~10 minutes of listening [SecurityWeek 2023; Pnwcomputers hcxtools/hashcat guide]. This lowers the bar to capture; strength therefore rests entirely on the passphrase. *Evidence type: maintainer disclosure + practitioner guide.*

5. **A 6-word random Diceware passphrase is the evidence-backed sweet spot (~77 bits).** The EFF large wordlist has 7,776 words = **12.9 bits/word** (reproduced below as 12.92), so six words ≈ **77.5 bits** — EFF's explicit recommendation, with four words a minimum and five a strong default [eff.org/deeplinks/2016/07]. At 77 bits the search space is ~1.5×10^23; no GPU fleet reaches it, and crucially the words are *randomly chosen*, so no wordlist shortcut applies. *Evidence type: standards body publication, figure reproduced.*

6. **WPA3-Personal (SAE) removes the offline-guessing oracle entirely — but only in non-transition mode.** SAE ("Dragonfly") is designed so a passive observer cannot validate guesses offline [Wi-Fi Alliance; purple.ai WPA3 guide]. However, <1% of APs run WPA3, and most WPA3 deployments use *transition mode*, which keeps a WPA2-PSK path an attacker can downgrade to and attack exactly as before [peer-reviewed 2025 study via securew2.com; arXiv:2412.15381]. WPA3 helps only if you run it pure. *Evidence type: peer-reviewed study + vendor analysis.*

## Industry Standards Compliance

| Standard | Specific requirement | `Tr0ub4dor&3` status | Source |
|---|---|---|---|
| **NIST SP 800-63B-4** §3.1.1 | Memorized secret SHALL be ≥8 chars; verifiers SHOULD allow ≥64 | **Pass on length** (11 chars) | nvlpubs.nist.gov SP.800-63B-4 |
| **NIST SP 800-63B-4** §3.1.1 | SHALL check against a blocklist of commonly-used / compromised / expected values; reject if present | **FAIL** — a globally published example password is the canonical blocklist entry | pages.nist.gov/800-63-FAQ |
| **NIST SP 800-63B-4** §3.1.1 | SHALL NOT impose composition (leet/complexity) rules | N/A to user, but the leet pattern is precisely why it is weak | nvlpubs.nist.gov |
| **IEEE 802.11i / WPA2-PSK** | PSK 8–63 chars; `PBKDF2(HMAC-SHA1, PSK, SSID, 4096, 256)` | Length valid; derivation offers no protection to a guessable PSK | koutto pi-pwnbox wiki; Hashcat wiki |
| **Wi-Fi Alliance WPA3-Personal (SAE)** | Offline-dictionary-attack resistance via SAE | Not in use (network is WPA2) | purple.ai; securew2.com |
| **EFF passphrase guidance (2016)** | ≥6 random words from the 7,776-word list (~77 bits) for high-value secrets | Not met; single mangled word | eff.org/deeplinks/2016/07 |

**Net:** compliant on raw length, but fails the one standard that actually decides this case — NIST's blocklist / compromised-value rule. A published password is the textbook definition of a blocklisted secret.

## Quantitative Analysis

**Attacker capability (cited, not computed against your target):**

| Fact | Value | Source |
|---|---|---|
| WPA2 KDF | PBKDF2-HMAC-SHA1, 4096 iterations, SSID as salt | IEEE 802.11i; Hashcat wiki |
| Single RTX 4090, mode 22000 | ~2,600 kH/s (2,551–2,656 kH/s observed) | hashcat.net forum benchmarks |
| Capture method | PMKID (clientless) or 4-way handshake; ~10 min listen | SecurityWeek 2023; Pnwcomputers guide |
| Attack ordering | wordlist → rules (leet/suffix) → mask/brute force | Hashcat docs; Black Hills cheatsheet |

**Entropy comparison (generation-side math — reproduced, runnable):**

```python
import math, secrets
# Published figures
xkcd_troubadour_bits, xkcd_phrase_bits = 28, 44   # xkcd.com/936
eff_words = 7776
bits_per_word = math.log2(eff_words)              # EFF publishes 12.9
for n in (4, 5, 6, 7):
    print(f"EFF diceware {n} words: {n*bits_per_word:5.1f} bits")
# Defensive generator (replace demo list with the real EFF large wordlist)
demo = ["correct","horse","battery","staple","anchor","violin","mango","ladder"]
print("-".join(secrets.choice(demo) for _ in range(6)))
```

Verified output: 4 words = 51.7 bits, 5 = 64.6, 6 = **77.5**, 7 = 90.5; bits/word = **12.92** (matches EFF's published 12.9).

**Interpretation.** The decisive variable is not entropy-in-the-abstract but *where the candidate sits in the attacker's search order*. `Tr0ub4dor&3` is reached in the earliest wordlist/rules phase (and, being a famous string, likely as a direct dictionary hit), so the WPA2 4096-iteration slowdown never engages. A 6-word random Diceware passphrase lives in a ~2^77 space with no wordlist shortcut, so the same slowdown is applied to an astronomically large space that no documented GPU rig can traverse. The gap between the two is not incremental — it is the difference between "found before brute force starts" and "not found."

## Implementation Guidance

Do this Monday morning:

1. **Generate a new passphrase with real randomness** (not a human-chosen phrase). Use the EFF large wordlist and a dice or CSPRNG — e.g. install the EFF list and run the snippet above with that list, or use a vetted generator. Target **6 words**, e.g. `river-cobalt-anchor-mango-ladder-violin` (regenerate your own; do not reuse this one).
2. **Set it on the AP.** Keep WPA2-AES (CCMP) at minimum; disable TKIP and **disable WPS** (PIN brute-force bypasses passphrase strength entirely).
3. **Prefer WPA3-Personal (SAE) if every client supports it, in pure (non-transition) mode** — this removes the offline-guessing oracle. Example hostapd hardening config:
   ```ini
   # /etc/hostapd/hostapd.conf  — WPA3-Personal (SAE) only, no WPA2 fallback
   wpa=2
   wpa_key_mgmt=SAE
   rsn_pairwise=CCMP
   ieee80211w=2        # Protected Management Frames: required
   sae_pwe=2           # hash-to-element, mitigates side-channels
   wps_state=0         # WPS off
   ```
   Only fall back to WPA2/WPA3 transition mode if you have legacy clients — and know it reopens the WPA2 attack surface.
4. **Rotate out-of-band.** Distribute the new passphrase via a password manager or a channel that is not the Wi-Fi itself; never a sticky note on the AP.
5. **For many devices / guests,** consider WPA2/WPA3-Enterprise (802.1X) so there is no shared PSK at all — out of scope here but the strategic fix for an office.

## Alternatives Considered

### 1. Keep `Tr0ub4dor&3` (status quo)
Rejected. It fails NIST's compromised-value rule and is a published string reachable in the earliest phase of an offline attack. No mitigation short of replacement helps. Would only be acceptable if the network were air-gapped with no wireless radio enabled — i.e., not a Wi-Fi network at all.

### 2. "Patch" the current password — add characters / more leet (e.g. `Tr0ub4dor&3!2024`)
Rejected. Appending suffixes and more substitutions is exactly the mangling hashcat rules automate [tutorials.technology; Black Hills]. Starting from a known base word keeps you inside the wordlist+rules space. Marginal entropy, near-zero real gain. When it *would* win: never, versus option 3 at equal effort.

### 3. Long human-chosen sentence (e.g. a memorable quote)
Partially viable but weaker than random Diceware. Human-chosen phrases cluster on quotes, lyrics, and common structures that targeted wordlists and phrase-cracking cover; estimated entropy is far below the word-count-times-12.9 ideal. Random selection is what delivers the 77 bits. Right choice only if a policy forbids generated secrets.

### 4. WPA3-Enterprise / 802.1X (no shared PSK)
Strongest, but higher effort (RADIUS, certificates/credentials, client config). Recommended as the *strategic* direction for an office with turnover; the 6-word PSK + WPA3-SAE is the immediate, low-effort win. Choose this when you outgrow a shared secret.

## Adversarial Review

**Counterargument 1 — "It's 11 chars and ~51 bits per a strength meter, that's fine."** Rebutted with a measurement from the attack side, not a label: strength meters score *random* character selection, but rule-based cracking reduces a mangled dictionary word to a few million guesses, and a single RTX 4090 runs ~2,600 kH/s [hashcat benchmarks]. The 51-bit figure never materializes. Conclusion stands.

**Counterargument 2 — "WPA2's 4096 PBKDF2 iterations protect us."** Rebutted: iterations only slow *per-guess* cost; they do nothing when the correct guess is in the first wordlist pass. The slowdown protects high-entropy random secrets, which is precisely why the fix is a random passphrase, not a longer mangled one.

**Counterargument 3 — "Nobody is parked outside our office."** This lowers probability, not severity, and PMKID capture needs only ~10 minutes of radio proximity [SecurityWeek 2023]. It cannot be dismissed with a number that makes the passphrase itself safe, so it stays open and does not rescue option 1.

**Premise check (is this the right problem?).** The user framed it as "how strong is this passphrase." The sharper problem is "is this passphrase *guessable*," and the answer short-circuits the entropy discussion entirely: it is a published string. Reframing from entropy to blocklist-membership is what makes the verdict definitive.

**Assumption audit.**
- *Network is WPA2-PSK (Personal), not Enterprise* — **reasonable** (user said "WPA2 passphrase"; a PSK implies Personal). If it were Enterprise, there is no shared passphrase and the question changes.
- *Attacker has or can get RF proximity* — **reasonable** for an office; required for any Wi-Fi attack.
- *RTX 4090 ~2,600 kH/s* — **verified** [hashcat.net forum]. A fleet is faster but irrelevant to the verdict.
- *`Tr0ub4dor&3` is in common wordlists* — **reasonable→near-verified**: it is the canonical XKCD example; even if a given list lacks it verbatim, rule mangling reconstructs it from "troubadour."
- *WPA3 not currently deployed* — **reasonable** (user says WPA2).

**Failure modes of the recommendation.** (a) Choosing a *human-memorable* phrase instead of a *randomly generated* one reintroduces wordlist exposure — randomness is the load-bearing requirement. (b) Enabling WPA3 *transition* mode while believing you are protected — it keeps the WPA2 oracle [securew2.com]. (c) Leaving WPS on — bypasses passphrase strength entirely.

<details><summary>Refinement rounds & Gap Ledger</summary>

**Refinement Round 1 — gap: "is the raw-string entropy (~51.8 bits) enough to make it safe regardless of fame?"** Investigated hashcat rule-based attack docs; reclassified the 51.8-bit figure as *not applicable* to a dictionary-derived string — effective space is wordlist+rules, far smaller. Confidence in "weak" raised to 98%.

**Refinement Round 2 — gap: "does moving to WPA3 remove the need to change the passphrase?"** Investigated WPA3 transition-mode literature; found transition mode preserves the WPA2 attack surface, so passphrase change is required regardless. No change to core verdict; added non-transition-mode requirement to guidance.

| Gap | Class | Action | Status |
|---|---|---|---|
| Does 51.8-bit meter score make it safe? | closable-by-tool | Read hashcat rule docs | closed |
| Does WPA3 alone fix it? | closable-by-tool | Read WPA3 transition-mode studies | closed |
| Exact membership of the string in a *specific* shipping wordlist | open-in-world | Not run (would require enumerating attacker dictionaries) | open — does not affect verdict; rule-mangling covers it |
| Is the network Personal vs Enterprise? | needs-user-input | Flagged as assumption | open |

Round 2 surfaced only the same class of lower-severity issues (deployment specifics), so the loop terminates.
</details>

## Recommendation

**Change the passphrase immediately.** Replace `Tr0ub4dor&3` with a freshly, randomly generated **6-word EFF Diceware passphrase (~77 bits)**; keep WPA2-AES/CCMP as the floor, disable WPS, and move to **pure WPA3-Personal (SAE)** if all clients support it. For an office with staff turnover, plan a path to 802.1X so there is no shared secret at all.

**Confidence: 98%.** The 2% reflects unseen deployment specifics (Personal vs Enterprise, client WPA3 support), none of which make the current passphrase acceptable.

**Sensitivity check.** *If* the network is actually WPA2/WPA3-**Enterprise** (802.1X, per-user credentials) rather than PSK, then there is no shared passphrase to rate and this entire analysis is moot — in that case switch the question to credential and RADIUS hardening. *If* you cannot deploy WPA3 (legacy clients), the random 6-word PSK on WPA2-AES is still sufficient on its own; WPA3 is additive, not required.

## Sources

**Primary — the password's origin:**
- XKCD #936 "Password Strength" — https://xkcd.com/936
- explainxkcd (entropy & crack-time figures) — https://www.explainxkcd.com/wiki/index.php/936:_Password_Strength

**Standards & Regulatory:**
- NIST SP 800-63B-4, Digital Identity Guidelines (memorized secrets, blocklist) — https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63B-4.ipd.pdf
- NIST SP 800-63 FAQ — https://pages.nist.gov/800-63-FAQ/
- EFF, "New Wordlists for Random Passphrases" (7,776 words, 12.9 bits/word, 6-word rec) — https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases

**Protocol & attack mechanics (primary/vendor):**
- Hashcat wiki, cracking WPA/WPA2 (mode 22000, PSK 8–63) — https://hashcat.net/wiki/doku.php?id=cracking_wpawpa2
- Hashcat forum, RTX 4090 mode 22000 benchmarks — https://hashcat.net/forum/thread-11277.html
- koutto/pi-pwnbox-rogueap wiki, WPA/WPA2-PSK PBKDF2 derivation & cracking steps — https://github.com/koutto/pi-pwnbox-rogueap/wiki/05.-WPA-WPA2-Personal-(PSK)-Authentication
- SecurityWeek, PMKID clientless attack (Steube/hashcat) — https://www.securityweek.com/new-method-discovered-cracking-wpa2-wi-fi-passwords
- Pnwcomputers cybersecurity guide, hcxtools + mode 22000 workflow — https://github.com/Pnwcomputers/ULTIMATE-CYBERSECURITY-MASTER-GUIDE/blob/main/Documentation/hcxtoolshashcat.md

**Industry analysis / secondary:**
- Hashcat rule-based attacks (leet/suffix mangling) — https://tutorials.technology/tutorials/hashcat-rule-based-attack.html
- Black Hills Infosec, Hashcat cheatsheet — https://www.blackhillsinfosec.com/hashcat-cheatsheet/
- Security.StackExchange #6095 (XKCD entropy discussion) — https://security.stackexchange.com/questions/6095/
- purple.ai, WPA3 / SAE explainer — https://www.purple.ai/en-gb/guides/wpa3-the-next-generation-of-wifi-security-explained
- SecureW2, WPA3 transition-mode downgrade risk — https://securew2.com/signal/wpa3-hack-evil-twin-downgrade-why-transition-mode-keeps-wifi-vulnerable
- arXiv:2412.15381, WPA3 SAE password recovery via captive portal — https://arxiv.org/pdf/2412.15381
