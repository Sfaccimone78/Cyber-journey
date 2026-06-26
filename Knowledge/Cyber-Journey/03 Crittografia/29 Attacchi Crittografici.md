---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 1
aggiornato: 2026-06-26
stato: maturo
aliases: ["Attacchi Crittografici", "Crittanalisi"]
---

# Attacchi Crittografici

## Panoramica

Catalogo trasversale degli attacchi alla crittografia. Principio guida:

> **"Attacks only get better, they never get worse."** Un attacco accademico oggi diventa pratico domani. E: la maggior parte dei sistemi cade non per debolezze matematiche dei primitivi, ma per **composizione errata, riuso di chiavi/nonce, mancata autenticazione e side-channel**. [Fonte: Crypto101, capp. 5–14]

## Classificazione per modello di attaccante

- **Ciphertext-only / passivo**: l'attaccante osserva solo (es. ECB image leak, crib-dragging su multi-time pad).
- **Chosen-plaintext / encryption oracle**: l'attaccante fa cifrare dati a scelta (es. ECB oracle, CRIME/BREACH).
- **Chosen-ciphertext / active (MITM)**: l'attaccante modifica il traffico (es. padding oracle, bit-flipping, DH MITM).

## Attacchi sui primitivi simmetrici

- **Multi-time pad / key & nonce reuse**: `c₁⊕c₂ = p₁⊕p₂` → crib-dragging. Colpisce OTP riusato, CTR/GCM con nonce ripetuto, one-time MAC riusato. → [[XOR]]
- **ECB pattern leak & encryption oracle** → [[Modi Operativi dei Block Cipher]]
- **Bit-flipping** (CBC e stream): manipolazione del plaintext senza decifrare → *encryption is not authentication*. → [[Modi Operativi dei Block Cipher]], [[Stream Cipher]]
- **Padding oracle (CBC)**: decifratura completa dal leak "padding valido/non valido". → [[Padding Oracle Attack]]
- **Bias RC4**: bias statistici nel keystream → rottura (WEP, traffico TLS-RC4). → [[Stream Cipher]]

## Attacchi sulle hash

- **Collision attack**: MD5 (certificati X.509 forgiati, malware **Flame**), SHA-1 (**SHAttered**, due PDF colliding). → [[Funzioni di Hash]]
- **Length extension attack**: forgia tag in prefix-MAC `H(k‖m)` con hash Merkle–Damgård. → [[Funzioni di Hash]], [[MAC e HMAC]]
- **Rainbow tables / GPU cracking**: password con hash veloci (anche con salt). → [[Funzioni di Hash]]
- **Birthday attack**: una collisione costa `2^(n/2)`, non `2ⁿ`. → [[Funzioni di Hash]]

## Attacchi sull'asimmetrica

- **MITM su Diffie-Hellman** (DH non autenticato). → [[Scambio di Chiavi Diffie-Hellman]]
- **Fattorizzazione / Shor** su RSA; **ECDLP / Shor** su ECC (quantum). → [[RSA]], [[Crittografia Post-Quantistica]]
- **Riuso/leak del nonce `k` in DSA/ECDSA → recupero chiave privata.** Con due firme che riusano `k`: `k ≡ (H(m₁)−H(m₂))(s₁−s₂)⁻¹ (mod q)`, poi `x = r⁻¹(sk − H(m))`. Casi reali: **PlayStation 3** (Sony, `k` fisso), **Android Bitcoin wallet** (2013, RNG difettoso), quasi-disastro **Debian OpenSSL** (RNG con poca entropia). → [[Crittografia a Curve Ellittiche (ECC)]]

## Attacchi sui generatori di numeri casuali (RNG)

> Un CSPRNG rotto compromette **tutti** i cryptosystem che lo usano. [Fonte: Crypto101, cap. 14]

- **Dual_EC_DRBG**: standard NIST con **backdoor** sospetta nelle costanti `P, Q`. Se esiste `e` con `eQ=P`, chi lo conosce predice tutto l'output osservando ~32 byte. Costanti non "nothing-up-my-sleeve"; leak Snowden + ritiro ufficiale. **Esempio archetipico di backdoor crittografica.**
- **Mersenne Twister**: **non** è un CSPRNG. La funzione di tempering è invertibile: osservati 624 output si clona lo stato e si predicono tutti i futuri. Ottimo per simulazioni, inutile per crittografia.
- **Regola pratica**: usare sempre il CSPRNG del SO (`/dev/urandom`, `CryptGenRandom`), mai userspace fragili.

## Side-channel attacks

Attacchi sull'**implementazione** anziché sulla matematica astratta.

- **Timing attack**: il tempo di esecuzione dipende dal segreto. Es.: confronto stringhe non-constant-time, padding oracle via tempo (**Lucky13**), **AES cache timing** (accessi S-box dipendenti dalla chiave). Mitigazione: confronti e operazioni **constant-time** (ChaCha20/Ed25519 sono constant-time by design).
- **Power measurement attack**: misura del consumo energetico (SPA/DPA) per estrarre la chiave (smartcard, HSM).
- **Montgomery ladder**: scalar-multiplication con numero **costante** di operazioni per bit → mitiga timing leak su esponenti segreti.

## Attacchi a livello di protocollo (TLS)

- **Downgrade** (SSLv2 non autenticava l'handshake), **BEAST** (CBC IV prevedibili TLS 1.0), **POODLE** (padding oracle SSLv3), **CRIME/BREACH** (compressione + cifratura leakano segreti via lunghezza). → [[TLS e SSL]]

## Collegamenti
- Attacchi specifici: [[Padding Oracle Attack]], [[XOR]] (multi-time pad)
- Primitivi colpiti: [[Funzioni di Hash]], [[MAC e HMAC]], [[RSA]], [[Crittografia a Curve Ellittiche (ECC)]], [[Scambio di Chiavi Diffie-Hellman]]
- Modi e cifrari: [[Modi Operativi dei Block Cipher]], [[Stream Cipher]], [[AES]]
- Protocollo: [[TLS e SSL]] · Quantum: [[Crittografia Post-Quantistica]]
- [[00 — Mappa Crittografia|Mappa Crittografia]]

## Fonti
- Crypto 101 (Laurens Van Houtven), capp. 5–14 + App. A/C (attacchi trasversali, DSA `k`, Dual_EC_DRBG, side-channel): https://crypto101.io/
