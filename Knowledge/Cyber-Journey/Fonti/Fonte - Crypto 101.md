---
tipo: fonte
tag: [crypto]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
url: https://www.crypto101.io/
autore: Laurens Van Houtenghen (lvh)
aliases: ["Crypto 101"]
---

# Fonte - Crypto 101 (Laurens Van Houtenghen / "lvh")

## Panoramica

**Crypto 101** è un'introduzione gratuita e open-source alla crittografia moderna, scritta da **Laurens Van Houtenghen (lvh)**. Nasce da un talk a PyCon 2013 e si è evoluta in un libro di ~200 pagine. L'obiettivo dichiarato non è formare crittografi, ma rendere sviluppatori e tecnici capaci di **riconoscere quando la crittografia viene applicata male** — il libro ripete come mantra: *"don't roll your own crypto"*.

> Tesi centrale del libro: gli algoritmi simmetrici sicuri sono un problema risolto; **la gestione delle chiavi e la composizione corretta dei primitivi** sono il vero punto debole dei sistemi reali. [Fonte: Crypto101, cap. 5]

## Approccio didattico

- **Bottom-up**: parte dai "building blocks" (XOR, block cipher, stream cipher) e li compone fino ai cryptosystem completi (TLS, OpenPGP, OTR).
- **Attack-driven**: ogni primitivo è seguito dagli attacchi che lo rompono se usato male (ECB image leak, padding oracle, bit-flipping, length extension, riuso di k in DSA). Si impara la sicurezza vedendo cosa si rompe.
- **Matematica con intuizione**: la matematica essenziale (modular arithmetic, curve ellittiche) è confinata in appendici e sezioni "opzionali in-depth" marcate esplicitamente.
- **Refrain ricorrenti**: *"encryption is not authentication"*, *"attacks only get better, never worse"*, *"don't roll your own crypto"*.

## Prerequisiti matematici

- **XOR e algebra booleana** (cap. 5): proprietà commutativa/associativa, `a⊕a=0`, `a⊕0=a`.
- **Aritmetica modulare** (Appendice A): addizione/sottrazione, numeri primi, inversi modulari, esponenziazione modulare (square-and-multiply, Montgomery ladder), logaritmo discreto, ordine moltiplicativo.
- **Curve ellittiche** (Appendice B): forma di Weierstrass `y²=x³+ax+b`, forma di Edwards, gruppi abeliani, problema del log discreto su curva (ECDLP).
- Tutta la matematica avanzata è opzionale per capire i principi.

## Mappa concetti → capitolo

| Cap. | Tema | Pagine wiki collegate |
|------|------|----------------------|
| 5 | Exclusive OR, one-time pad, crib-dragging | [[XOR e One-Time Pad]] |
| 6 | Block cipher, AES (Rijndael), DES/3DES | [[Block Cipher e AES]] |
| 7 | Stream cipher, ECB/CBC/CTR, padding, RC4, Salsa20/ChaCha | [[Stream Cipher]], [[Modi Operativi]], [[Padding Oracle]] |
| 8 | Key exchange, Diffie-Hellman (discrete log + ECC) | [[Diffie-Hellman]] |
| 9 | Public-key encryption, RSA, OAEP, ECC | [[RSA]], [[Curve Ellittiche]] |
| 10 | Hash functions, MD5/SHA-1/SHA-2/SHA-3, password storage, length extension | [[Funzioni Hash]] |
| 11 | MAC, HMAC, one-time MAC, Carter-Wegman, AEAD, OCB/GCM | [[MAC e HMAC]], [[Authenticated Encryption]] |
| 12 | Signature algorithms, DSA, ECDSA, repudiable auth | [[Curve Ellittiche]], [[Attacchi Crittografici]] |
| 13 | Key derivation functions, PBKDF2/bcrypt/scrypt/HKDF | [[Funzioni Hash]] |
| 14 | Random number generators, CSPRNG, Dual_EC_DRBG, Mersenne Twister | [[Attacchi Crittografici]] |
| 15 | SSL/TLS, handshake, CA, PFS, CRIME/BREACH, HSTS, pinning | [[TLS/SSL]] |
| 16 | OpenPGP/GPG, web of trust | [[TLS/SSL]] |
| 17 | Off-The-Record (OTR) messaging | [[Diffie-Hellman]] |
| App. A | Aritmetica modulare | [[RSA]], [[Diffie-Hellman]] |
| App. B | Curve ellittiche | [[Curve Ellittiche]] |
| App. C | Side-channel attacks (timing, power) | [[Attacchi Crittografici]] |

## Punti di forza e limiti della fonte

- **Forza**: ottima per costruire l'intuizione e per il catalogo di attacchi pratici reali (WEP/RC4, BEAST, CRIME, padding oracle, Debian OpenSSL k-reuse).
- **Limiti**: il libro è **incompleto** — molte sezioni contengono `TODO` (PBKDF2, bcrypt, scrypt, ECDSA, RSA-PSS, dettagli handshake TLS moderno). Per lo stato aggiornato di sicurezza degli algoritmi e per post-quantum si integra con [[Crittografia Post-Quantum]] e la deep research da Boneh & Shoup (vedi [[Mappa della Crittografia]]).

## Collegamenti
- [[index]]
- Mappa completa dei primitivi: [[Mappa della Crittografia]]
- Vedi anche: [[Attacchi Crittografici]], [[Cryptographic Failures]]

## Fonti
- [Crypto101, lvh — interi capitoli 5–17 + Appendici A–C]
- Sito ufficiale: <https://www.crypto101.io/>
