---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 5
aggiornato: 2026-06-26
stato: maturo
aliases: ["Scambio di Chiavi Diffie-Hellman", "Diffie-Hellman"]
---

# Scambio di Chiavi Diffie-Hellman

## In breve

Lo **scambio di chiavi Diffie-Hellman (DH)** è un protocollo che permette a due parti di concordare una **chiave segreta condivisa** attraverso un canale di comunicazione pubblico (e potenzialmente intercettato), senza doversi scambiare la chiave segreta stessa. È uno dei concetti più eleganti della crittografia moderna e la base di [[TLS e SSL|TLS]].

## Come funziona

Il protocollo si basa sulla difficoltà del **problema del logaritmo discreto**. Un'analogia con i colori aiuta a capire il principio:

1. Alice e Bob concordano pubblicamente su un colore base (es. giallo) — noto a tutti.
2. Alice sceglie un colore segreto (rosso) e mescola: **giallo + rosso = arancione** → lo invia a Bob.
3. Bob sceglie un colore segreto (blu) e mescola: **giallo + blu = verde** → lo invia ad Alice.
4. Alice prende il verde di Bob e aggiunge il suo rosso segreto: **verde + rosso = marrone**.
5. Bob prende l'arancione di Alice e aggiunge il suo blu segreto: **arancione + blu = marrone**.
6. Entrambi ottengono lo stesso colore finale (marrone) — la chiave condivisa — senza che Eva (l'intercettatore) possa ricavarla.

**Matematicamente** (DH classico):
- Parametri pubblici: primo `p` e generatore `g`
- Alice sceglie `a` (segreto), invia `A = g^a mod p`
- Bob sceglie `b` (segreto), invia `B = g^b mod p`
- Chiave condivisa: `K = B^a mod p = A^b mod p = g^(ab) mod p`

La variante moderna usata in TLS 1.3 è **ECDH (Elliptic Curve Diffie-Hellman)**, che usa la matematica delle curve ellittiche per ottenere maggiore sicurezza con chiavi più corte.

## Esempio pratico

```bash
# Generare parametri DH con OpenSSL
openssl dhparam -out dhparam.pem 2048

# Vedere i parametri generati (p e g)
openssl dhparam -text -noout -in dhparam.pem

# ECDH: generare una chiave su curva P-256 (usata in TLS 1.3)
openssl genpkey -genparam -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out ecparam.pem
openssl genpkey -paramfile ecparam.pem -out alice_priv.pem
openssl pkey -in alice_priv.pem -pubout -out alice_pub.pem
```

## Il punto debole: MITM (DH non autentica)

> [!warning] Diffie-Hellman da solo NON autentica i peer
> DH garantisce che Alice e Bob ottengano lo stesso segreto su un canale **passivamente** intercettato, ma non verifica *con chi* stai parlando. Un attaccante attivo **Mallory** può eseguire DH **due volte** — una con Alice (fingendosi Bob) e una con Bob (fingendosi Alice) — ritrovandosi con due segreti. Da lì legge, modifica o blocca tutti i messaggi, e nessuno dei due se ne accorge. [Fonte: Crypto101, cap. 8]

La cura è **autenticare lo scambio**: firme o certificati legati a un'identità. È esattamente ciò che fa [[TLS e SSL|TLS]] (il server firma i parametri (EC)DHE col proprio certificato) e protocolli come OTR. Vedi [[Attacchi Crittografici]].

## Curve ellittiche: stessa sicurezza, chiavi minuscole
DH funziona anche sul problema del log discreto **su curva ellittica** (ECDLP). I migliori attacchi a ECDLP sono `O(√n)`, più lenti del number field sieve sul log discreto classico → a parità di sicurezza servono chiavi **molto più piccole**:

| Sicurezza (bit) | Chiave discrete-log classico | Chiave ellittica (ECC) |
|---|---|---|
| 80  | 1024  | 160 |
| 128 | 3072  | 256 |
| 256 | 15360 | 512 |

[Fonte: Crypto101, cap. 8] Vedi [[Crittografia a Curve Ellittiche (ECC)]].

## Rilevanza per la sicurezza

- **Perfect Forward Secrecy (PFS)**: quando TLS usa DHE o ECDHE (DH effimero, nuova coppia per sessione scartata dopo l'uso), ogni sessione genera chiavi diverse. Se la chiave privata a lungo termine viene compromessa **in futuro**, le sessioni passate registrate restano **indecifrabili**. È il motivo per cui TLS moderno preferisce ECDHE allo scambio chiave via RSA.
- **Weak DH**: parametri DH con `p` troppo piccolo (< 2048 bit) sono vulnerabili all'attacco Logjam (2015).
- **Minaccia quantistica**: l'**algoritmo di Shor** risolve anche il logaritmo discreto (classico ed ellittico) → DH ed ECDH **cadono** col quantum computing. Vedi [[Crittografia Post-Quantistica]].
- Implementazioni reali: **ECDHE** in TLS 1.2/1.3, **X25519** (DH su Curve25519) in TLS 1.3, OpenSSH, Signal, WireGuard; **OTR** usa DH autenticato per messaggistica con PFS. [Fonte: Crypto101, cap. 8 e 17]
- [[CryptoHack - Mathematics (Modular Math)]] copre i fondamenti matematici necessari per capire il protocollo in profondità.

## Collegamenti

- [[TLS e SSL]] — DH è usato nell'handshake per derivare la chiave di sessione
- [[Crittografia Asimmetrica]] — DH non cifra direttamente ma stabilisce un segreto condiviso
- [[RSA]] — alternativa per lo scambio di chiavi (meno efficiente di ECDH)
- [[Crittografia a Curve Ellittiche (ECC)]] — ECDH/X25519, chiavi più piccole
- [[Crittografia Post-Quantistica]] — Shor rompe DH/ECDH
- [[Attacchi Crittografici]] — MITM su DH non autenticato
- [[CryptoHack - Mathematics (Modular Math)]] — fondamenti di aritmetica modulare
- [[OpenSSL]] — tool per generare parametri DH e testare connessioni

## Fonti

1. Cloudflare Learning — What is Diffie-Hellman key exchange?: https://www.cloudflare.com/learning/ssl/what-is-a-cryptographic-key/
2. Wikipedia — Diffie–Hellman key exchange: https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
3. NIST — SP 800-56A Rev. 3 (Recommendation for Pair-Wise Key-Establishment): https://csrc.nist.gov/publications/detail/sp/800/56a/rev-3/final
4. RFC 7919 — Negotiated Finite Field Diffie-Hellman Ephemeral Parameters: https://datatracker.ietf.org/doc/html/rfc7919
5. Crypto 101 (Laurens Van Houtven), capp. 8 "Key exchange" e 17 "OTR" (MITM, ECDH, key-size): https://crypto101.io/
