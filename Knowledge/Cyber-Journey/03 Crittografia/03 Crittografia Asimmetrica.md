---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Crittografia Asimmetrica"]

---

# Crittografia Asimmetrica

## In breve

La **crittografia asimmetrica** (o **a chiave pubblica**) usa una **coppia di chiavi matematicamente legate**: una **chiave pubblica** (che si può condividere con chiunque) e una **chiave privata** (da tenere segreta). Quello che viene cifrato con la chiave pubblica può essere decifrato **solo** con la chiave privata corrispondente, e viceversa.

## Come funziona

La coppia di chiavi si genera sfruttando problemi matematici difficili da invertire, come la fattorizzazione di numeri enormi (usata da [[RSA]]) o il logaritmo discreto su curve ellittiche (ECDSA). La difficoltà computazionale garantisce la sicurezza.

**Scenario tipico — cifratura:**

1. Alice pubblica la sua **chiave pubblica** (es. la mette sul suo sito).
2. Bob vuole mandarle un messaggio segreto: lo cifra con la **chiave pubblica di Alice**.
3. Solo Alice, con la sua **chiave privata**, può decifrarlo.

**Scenario tipico — firma digitale:**

1. Alice firma un documento con la sua **chiave privata**.
2. Chiunque può verificare la firma usando la **chiave pubblica di Alice** — vedi [[Firma Digitale]].

## Esempio pratico

Generare una coppia RSA con [[OpenSSL]]:

```bash
# Genera chiave privata RSA 2048 bit
openssl genrsa -out privata.pem 2048

# Estrai la chiave pubblica dalla privata
openssl rsa -in privata.pem -pubout -out pubblica.pem

# Cifra un messaggio con la chiave pubblica
openssl pkeyutl -encrypt -inkey pubblica.pem -pubin -in msg.txt -out msg.enc

# Decifra con la chiave privata
openssl pkeyutl -decrypt -inkey privata.pem -in msg.enc -out msg_dec.txt
```

## Rilevanza per la sicurezza

- Risolve il problema della distribuzione delle chiavi della [[Crittografia Simmetrica]].
- È lenta rispetto alla crittografia simmetrica: in [[TLS e SSL]], viene usata solo per scambiare le chiavi, poi si passa alla crittografia simmetrica.
- La sicurezza dipende dalla lunghezza della chiave: RSA richiede almeno 2048 bit oggi.
- I computer quantistici potrebbero rompere RSA — la ricerca su algoritmi post-quantistici è in corso (NIST PQC).

## Collegamenti

- [[RSA]] — l'algoritmo asimmetrico più noto
- [[Firma Digitale]] — una delle applicazioni principali della crittografia asimmetrica
- [[Certificati Digitali e CA]] — usano coppie di chiavi asimmetriche
- [[Scambio di Chiavi Diffie-Hellman]] — alternativa per lo scambio di chiavi
- [[Crittografia a Curve Ellittiche (ECC)]] — asimmetrica moderna: stessa sicurezza, chiavi più corte
- [[TLS e SSL]] — combina asimmetrica e simmetrica
- [[CryptoHack - Mathematics (Modular Math)]] — la matematica modulare alla base di RSA

## Fonti

1. Wikipedia — Public-key cryptography: https://en.wikipedia.org/wiki/Public-key_cryptography
2. Cloudflare Learning — What is asymmetric encryption?: https://www.cloudflare.com/learning/ssl/what-is-asymmetric-encryption/
3. NIST — Recommendation for Pair-Wise Key Establishment: https://csrc.nist.gov/publications/detail/sp/800-56a/rev-3/final
