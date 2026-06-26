---
tipo: concetto
tag: [crypto]
fase: 2
fonti: 6
aggiornato: 2026-06-26
stato: maturo
aliases: ["Crittografia a Curve Ellittiche (ECC)", "Curve Ellittiche"]
---

# Crittografia a Curve Ellittiche (ECC)

## In breve
L'**ECC** (Elliptic Curve Cryptography) è una famiglia di algoritmi di [[Crittografia Asimmetrica]] basati sulla matematica delle curve ellittiche su campi finiti. Offre la **stessa sicurezza di [[RSA]] con chiavi molto più piccole**: una chiave ECC a 256 bit equivale circa a una RSA a 3072 bit. Per questo è oggi lo standard in TLS, mobile e blockchain.

## Come funziona
La sicurezza si basa sul **problema del logaritmo discreto su curva ellittica (ECDLP)**: dato un punto base `G` e un punto `P = k·G`, è computazionalmente infattibile ricavare lo scalare `k`. La chiave privata è `k`; la chiave pubblica è il punto `P`.

Algoritmi principali:
- **ECDH** (Elliptic Curve Diffie-Hellman): scambio chiavi, variante di [[Scambio di Chiavi Diffie-Hellman]].
- **ECDSA** / **EdDSA**: [[Firma Digitale]] su curve (es. Ed25519).

Curve comuni: `P-256` (NIST secp256r1), `secp256k1` (Bitcoin), `Curve25519` (moderna, robusta).

## Esempio pratico
Generare una chiave ECC e un certificato con [[OpenSSL]]:
```bash
# Chiave privata su curva P-256
openssl ecparam -name prime256v1 -genkey -noout -out ec_priv.pem

# Chiave pubblica
openssl ec -in ec_priv.pem -pubout -out ec_pub.pem

# Curve disponibili
openssl ecparam -list_curves
```

## Rilevanza per la sicurezza
- Preferita in [[TLS e SSL]] moderno (ECDHE per forward secrecy).
- Chiavi piccole → meno banda e CPU: ideale per IoT e mobile.
- **Attenzione alla generazione del nonce in ECDSA**: un nonce riusato o prevedibile espone la chiave privata (caso storico: PlayStation 3).
- Come [[RSA]], è vulnerabile ai computer quantistici (algoritmo di Shor) → ricerca post-quantistica.

---

# Strato esperto

## La matematica: gruppo abeliano sui punti
Una curva ellittica in **forma di Weierstrass corta** è `y² = x³ + ax + b`; in **forma di Edwards** `x² + y² = 1 + d·x²·y²`. I punti della curva, più un **punto all'infinito `O`**, formano un **gruppo abeliano** sotto un'operazione di "addizione di punti": valgono chiusura, associatività, identità (`O`), inverso e commutatività. La **moltiplicazione scalare** `k·P` (sommare `P` a sé stesso `k` volte) è l'analogo ellittico dell'esponenziazione modulare. [Fonte: Crypto101, App. B]

> **Vantaggio chiave**: i migliori attacchi all'ECDLP hanno complessità `O(√n)`, peggiore degli attacchi al log discreto classico → chiavi molto più piccole a parità di sicurezza (256 bit ECC ≈ 3072 bit RSA/DH). Tabella completa in [[Scambio di Chiavi Diffie-Hellman]]. [Fonte: Crypto101, cap. 8]

## ECDSA e il problema critico di `k`
ECDSA eredita da DSA un'**estrema sensibilità al nonce per-firma `k`**, che deve essere **unico, imprevedibile e segreto**.

> [!danger] Riuso o leak di `k` → recupero della chiave privata
> Se `k` è riusato in due firme, la chiave privata si ricava con semplice algebra modulare. Bastano poche firme se trapelano anche solo pochi bit di `k`. Casi reali: jailbreak della **PlayStation 3** (Sony usava lo stesso `k` fisso) e il bug RNG degli **Android Bitcoin wallet** (2013). [Fonte: Crypto101, cap. 12]

Mitigazione moderna: **`k` deterministico** (RFC 6979), derivato via HMAC da messaggio + chiave privata → niente dipendenza dall'RNG. Vedi [[Attacchi Crittografici]].

## Ed25519 — perché è preferito
**Ed25519** (EdDSA su Curve25519, di Bernstein et al.) risolve i problemi pratici di ECDSA:
- **Deterministico**: `k` derivato da chiave+messaggio → immune al disastro del riuso di `k`.
- **Constant-time**: niente branch o accessi a memoria dipendenti dal segreto → resistente ai **timing attack** (la forma di Edwards usa addizione completa, senza casi speciali).
- **Veloce**, chiavi/firme piccole (32/64 byte), nessun parametro debole.
- Curve25519 è una **"SafeCurve"**: scelta con criteri di robustezza pubblici, a differenza di alcune curve NIST (P-256) su cui pesano sospetti sui parametri non "nothing-up-my-sleeve".

## Vulnerabilità
- **`k` debole in ECDSA** (sopra) — la falla pratica più comune.
- **Curve scelte male**: parametri non verificabili, curve singolari/anomale, twist insicuri (criteri SafeCurves).
- **Side-channel/timing** su implementazioni Weierstrass non constant-time; la forma di Edwards è progettata per evitarli.
- **Minaccia quantistica**: l'algoritmo di **Shor** risolve l'ECDLP → tutta l'ECC cade col quantum computing. Vedi [[Crittografia Post-Quantistica]].

## Dove si incontra
- **Ed25519**: chiavi SSH moderne, firma pacchetti (OpenBSD signify), DNSSEC, Tor, Signal.
- **ECDSA P-256**: certificati [[TLS e SSL|TLS]], JWT (ES256), Bitcoin/Ethereum (secp256k1).
- **X25519**: key exchange in TLS 1.3, WireGuard, Signal.

## Collegamenti
- [[Crittografia Asimmetrica]]
- [[RSA]]
- [[Scambio di Chiavi Diffie-Hellman]]
- [[Firma Digitale]]
- [[Crittografia Post-Quantistica]] — Shor rompe l'ECDLP
- [[Attacchi Crittografici]] — riuso di `k`, side-channel
- [[TLS e SSL]]
- [[OpenSSL]]

## Fonti
- Cloudflare — A (relatively easy to understand) primer on ECC: https://blog.cloudflare.com/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/
- NIST FIPS 186-5 (Digital Signature Standard): https://csrc.nist.gov/publications/detail/fips/186/5/final
- CryptoHack — Elliptic Curves: https://cryptohack.org/challenges/ecc/
- Crypto 101 (Laurens Van Houtven), App. B + capp. 8/12 (gruppo abeliano, ECDH, ECDSA): https://crypto101.io/
- Bernstein et al. — Ed25519 / EdDSA: https://ed25519.cr.yp.to/
- SafeCurves — criteri di sicurezza per curve ellittiche: https://safecurves.cr.yp.to/
