---
tipo: sintesi
tag: [crypto, sintesi]
fase: 0
aggiornato: 2026-06-25
stato: attivo
aliases: ["Mappa della Crittografia"]
---

# Mappa della Crittografia (sintesi)

Vista d'insieme che collega tutti i concetti del topic: come si classificano i primitivi, come si confrontano, quali errori si ripetono e come Cryptopals mappa sui concetti.

## 1. Simmetrica vs Asimmetrica vs Ibrida

```
                     CRITTOGRAFIA
        ┌────────────────┴────────────────┐
   SIMMETRICA                        ASIMMETRICA
 (stessa chiave)                  (coppia pub/priv)
        │                                 │
  ┌─────┴─────┐                  ┌────────┼────────┐
 stream     block              key-exch  encrypt  firma
 cipher     cipher              DH/ECDH   RSA-OAEP RSA-PSS
 ChaCha20   AES (+modi)         X25519             ECDSA/Ed25519
        │                                 │
  confidenzialità +                 niente segreto
  (con MAC/AEAD) integrità          pre-condiviso, ma
  → veloce, chiave condivisa        ~1000-4000× più lenta
        └───────────────┬───────────────┘
                     IBRIDA
        asimmetrica negozia/autentica una chiave,
        simmetrica cifra i dati  →  TLS, SSH, PGP, Signal
```

| Famiglia | Chiave | Risolve | Costo | Esempi |
|----------|--------|---------|-------|--------|
| **Simmetrica** | unica, condivisa | confidenzialità + (con MAC) integrità | velocissima | AES, ChaCha20, HMAC → [[Block Cipher e AES]], [[Stream Cipher]], [[MAC e HMAC]] |
| **Asimmetrica** | coppia pub/priv | distribuzione chiavi, firme, non-repudiation | lenta, dati ≤ modulo | RSA, DH, ECC → [[RSA]], [[Diffie-Hellman]], [[Curve Ellittiche]] |
| **Ibrida** | asim → sim | il meglio di entrambe | handshake una volta, poi veloce | TLS, SSH → [[TLS/SSL]], [[SSH]] |

> Boneh-Shoup struttura il campo esattamente così: **secret-key** (Parte I, AEAD cap. 9) → **public-key** (Parte II, capp. 10–15) → **protocolli** (key exchange cap. 21). [Fonte: toc.cryptobook.us]

## 2. Tabella comparativa dei primitivi

| Algoritmo | Tipo | Sicurezza (classica) | Performance | Uso tipico | Vulnerabilità principale |
|-----------|------|----------------------|-------------|------------|--------------------------|
| **AES** | block cipher simmetrico | 128/192/256 bit (solido) | molto veloce (HW AES-NI) | bulk encryption (in AEAD) | nessuna sul cifrario; **dipende dal modo** (ECB/CBC) → [[Modi Operativi]] |
| **ChaCha20** | stream cipher simmetrico | 256 bit (solido) | veloce anche senza HW; **constant-time** | TLS, WireGuard, mobile | **riuso nonce = catastrofe** (multi-time pad) → [[Stream Cipher]] |
| **RSA** | asimmetrico (fattorizzazione) | 2048/3072 bit; **rotto da Shor** | molto lenta | firme, key transport (legacy) | textbook-RSA, PKCS#1 v1.5 (Bleichenbacher), `e=1`, primi deboli → [[RSA]] |
| **ECDSA** | firma asimmetrica (ECDLP) | 256 bit; **rotto da Shor** | veloce, chiavi piccole | TLS, JWT, Bitcoin/Ethereum | **riuso/leak del nonce `k` → chiave privata** → [[Curve Ellittiche]] |
| **SHA-256** | hash (Merkle–Damgård) | 256 bit, ~128 bit collisioni | velocissima | integrità, HMAC, firme, blockchain | **length-extension**; troppo veloce per password → [[Funzioni Hash]] |
| **bcrypt** | KDF / password hash | tunable (work factor) | **deliberatamente lenta** | hashing password | nessuna nota; sceglie cost basso = debole → [[Funzioni Hash]] |

Note trasversali:
- **Constant-time**: ChaCha20 ed Ed25519 lo sono by design; AES SW e curve Weierstrass possono leakare via timing/cache → [[Attacchi Crittografici]].
- **Quantum**: AES-256 e SHA-256 reggono (Grover, speedup solo quadratico); RSA/ECC cadono (Shor) → [[Crittografia Post-Quantum]].
- **bcrypt** non è cifratura: trasforma una password in hash lento + salt; alternative **scrypt**/**Argon2** (anche memory-hard).

## 3. Errori crittografici comuni (codice vulnerabile → fix)

### A. Modo ECB / cifratura senza autenticazione
```python
# ❌ ECB: pattern del plaintext visibili; nessuna integrità
ct = AES.new(key, AES.MODE_ECB).encrypt(pad(pt))

# ✅ AEAD: confidenzialità + integrità, nonce unico
aes = AESGCM(key)
nonce = os.urandom(12)            # MAI riusare con la stessa chiave
ct = aes.encrypt(nonce, pt, associated_data)
```
→ [[Modi Operativi]], [[Authenticated Encryption]]

### B. Riuso del nonce / IV
```python
# ❌ nonce fisso → CTR/GCM diventa multi-time pad (c1⊕c2 = p1⊕p2)
nonce = b"\x00" * 12
# ✅ nonce casuale/contatore unico per ogni messaggio sotto la stessa chiave
nonce = os.urandom(12)
```
→ [[Stream Cipher]], [[XOR e One-Time Pad]]

### C. Confronto MAC non constant-time (timing leak)
```python
# ❌ esce al primo byte diverso → timing attack sul tag
if mac == expected: ...
# ✅ confronto a tempo costante
hmac.compare_digest(mac, expected)
```
→ [[MAC e HMAC]], [[Attacchi Crittografici]]

### D. Password con hash veloce
```python
# ❌ SHA-256 (anche con salt) → GPU/rainbow crackano in massa
h = hashlib.sha256(salt + password).hexdigest()
# ✅ KDF lenta e memory-hard
h = argon2.PasswordHasher().hash(password)   # oppure bcrypt/scrypt
```
→ [[Funzioni Hash]]

### E. RSA textbook / padding sbagliato
```python
# ❌ deterministico e malleabile; PKCS#1 v1.5 → Bleichenbacher
ct = pow(m, e, N)
# ✅ OAEP per cifratura, PSS per firma
ct = pubkey.encrypt(m, padding.OAEP(...))
```
→ [[RSA]]

### F. RNG non crittografico
```python
# ❌ Mersenne Twister: stato clonabile da 624 output → predicibile
key = random.getrandbits(256)
# ✅ CSPRNG del SO
key = secrets.token_bytes(32)    # /dev/urandom, CryptGenRandom
```
→ [[Attacchi Crittografici]]

### G. Encrypt-and-MAC / MAC-then-Encrypt (ordine sbagliato)
```
❌ MAC-then-Encrypt (TLS CBC) → padding oracle/Lucky13
✅ Encrypt-then-MAC, oppure (meglio) AEAD che lo fa correttamente
```
→ [[Padding Oracle]], [[Authenticated Encryption]]

### H. Nonce `k` riusato nelle firme ECDSA
```
❌ stesso k in due firme → x = (s1·k − H(m1)) / r   (chiave privata recuperata)
✅ k deterministico (RFC 6979) oppure usare Ed25519 (deterministico by design)
```
→ [[Curve Ellittiche]]

> **Meta-lezione** (Crypto101): i sistemi raramente cadono per debolezza dei primitivi; cadono per **composizione errata, riuso di chiavi/nonce, mancata autenticazione, side-channel e RNG rotti**. *Don't roll your own crypto.* → [[Attacchi Crittografici]], [[Cryptographic Failures]]

## 4. Mappa Cryptopals → concetto

[Fonte: cryptopals.com] — gli 8 set di sfide mappano sui concetti del wiki:

| Set | Sfide | Tema | Concetto |
|-----|-------|------|----------|
| **1** | 1–8 | XOR, single/repeating-key, rilevare ECB | [[XOR e One-Time Pad]], [[Modi Operativi]] |
| **2** | 9–16 | PKCS#7, CBC, **ECB byte-at-a-time oracle**, CBC bit-flipping | [[Modi Operativi]] |
| **3** | 17–24 | **CBC padding oracle**, CTR, crack del Mersenne Twister | [[Padding Oracle]], [[Stream Cipher]], [[Attacchi Crittografici]] |
| **4** | 25–32 | CTR edit, **timing leak su HMAC**, break random-access RW CTR | [[MAC e HMAC]], [[Attacchi Crittografici]] |
| **5** | 33–40 | **Diffie-Hellman + MITM**, parametri malevoli, **Bleichenbacher e=3 RSA**, RSA broadcast | [[Diffie-Hellman]], [[RSA]] |
| **6** | 41–48 | RSA unpadded recovery, **DSA nonce recovery**, parity oracle, PKCS#1 v1.5 forgery | [[RSA]], [[Curve Ellittiche]] |
| **7** | 49–56 | CBC-MAC forgery, **length-extension**, compression oracle (CRIME), RC4 bias | [[MAC e HMAC]], [[Funzioni Hash]], [[Stream Cipher]] |
| **8** | 57–66 | **DH/ECDH invalid-curve & small-subgroup**, ECDSA, GCM nonce reuse | [[Curve Ellittiche]], [[Diffie-Hellman]], [[Authenticated Encryption]] |

## Collegamenti
- Tutti i primitivi: [[XOR e One-Time Pad]], [[Stream Cipher]], [[Block Cipher e AES]], [[Modi Operativi]], [[Funzioni Hash]], [[MAC e HMAC]], [[Authenticated Encryption]]
- Asimmetrica: [[RSA]], [[Diffie-Hellman]], [[Curve Ellittiche]]
- Protocolli e attacchi: [[TLS/SSL]], [[Padding Oracle]], [[Attacchi Crittografici]], [[Crittografia Post-Quantum]]
- Sicurezza applicativa: [[Cryptographic Failures]]
- Riassunto fonte: [[Crypto 101]]

## Fonti
- [Crypto101 — intero volume, capp. 5–17 + App. A–C] → [[Crypto 101]]
- [Fonte: toc.cryptobook.us — Boneh & Shoup, struttura secret-key/public-key/protocolli]
- [Fonte: cryptopals.com — The Cryptopals Crypto Challenges, set 1–8]
