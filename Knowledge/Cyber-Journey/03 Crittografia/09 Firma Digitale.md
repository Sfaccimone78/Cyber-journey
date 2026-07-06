---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["Firma Digitale"]

---

# Firma Digitale

## In breve

Una **firma digitale** è l'equivalente elettronico di una firma autografa, ma con garanzie matematiche molto più forti. Garantisce tre proprietà: **autenticità** (il documento viene davvero da chi dice di averlo firmato), **integrità** (non è stato modificato) e **non ripudio** (il firmatario non può negare di averlo firmato). È il meccanismo con cui le [[Certificati Digitali e CA|CA]] firmano i certificati digitali.

## Come funziona

La firma digitale usa la [[Crittografia Asimmetrica]]:

**Firma (mittente)**:
1. Si calcola l'**hash** del documento (es. SHA-256) — vedi [[Funzioni di Hash]].
2. L'hash viene cifrato con la **chiave privata** del mittente → questo è la firma digitale.
3. Il documento + la firma vengono inviati al destinatario.

**Verifica (destinatario)**:
1. Si decifra la firma con la **chiave pubblica** del mittente → si ottiene l'hash originale.
2. Si calcola indipendentemente l'hash del documento ricevuto.
3. Se i due hash coincidono, la firma è valida: il documento è autentico e integro.

Schema:
```
Alice firma:     hash(doc) → cifra con chiave_privata_Alice → firma
Bob verifica:    decifra firma con chiave_pubblica_Alice → hash_originale
                 hash(doc_ricevuto) == hash_originale? → VALIDO
```

Algoritmi comuni: **RSA-PSS**, **ECDSA** (usato in TLS e Bitcoin), **EdDSA** (Ed25519, moderno e veloce).

## Esempio pratico

```bash
# 1. Generare una coppia di chiavi RSA
openssl genrsa -out chiave_privata.pem 2048
openssl rsa -in chiave_privata.pem -pubout -out chiave_pubblica.pem

# 2. Firmare un documento
openssl dgst -sha256 -sign chiave_privata.pem -out firma.bin documento.txt

# 3. Verificare la firma
openssl dgst -sha256 -verify chiave_pubblica.pem -signature firma.bin documento.txt
# Output: Verified OK  (oppure "Verification Failure" se il file è stato alterato)
```

## Rilevanza per la sicurezza

- **Certificati TLS**: la CA firma il certificato del sito web — il browser verifica la firma per fidarsi del sito ([[TLS e SSL]]).
- **Aggiornamenti software**: i sistemi operativi verificano la firma digitale dei pacchetti prima di installarli — protezione da malware.
- **Email**: standard come S/MIME e PGP usano firme digitali per autenticare le email.
- **Blockchain**: le transazioni Bitcoin/Ethereum sono autorizzate da firme ECDSA.
- **Attacchi**: se la chiave privata viene rubata, l'attaccante può firmare documenti a nome della vittima.

## Lab

- **[[OpenSSL]] — firma e verifica**: genera una coppia RSA, firma `documento.txt` con `openssl dgst -sha256 -sign` e verifica con `-verify` (comandi negli esempi). Poi modifica un byte del file e ri-verifica: l'output diventa *Verification Failure*, mostrando come la firma protegge l'integrità.
- **CryptoHack → sezioni *ECC* e *RSA* (sfide di firma)** (https://cryptohack.org): challenge come *Nonce-Sense* / firme ECDSA con nonce riusato fanno recuperare la chiave privata da due firme, esercizio classico sulle debolezze implementative delle firme (stesso bug del PS3 di Sony).
- **CryptoPals → Set 6 challenge 42–43** (https://cryptopals.com): *Bleichenbacher's e=3 RSA signature forgery* e *DSA nonce recovery* — forgiatura di firme RSA con verifica debole e recupero della chiave DSA da nonce prevedibile.

## Domande

1. **D:** Quali tre proprietà garantisce una firma digitale? **R:** Autenticità (viene da chi dichiara di firmare), integrità (il documento non è stato alterato) e non ripudio (il firmatario non può negare la firma).
2. **D:** Cosa viene effettivamente firmato: il documento o il suo hash? **R:** L'**hash** del documento (es. SHA-256), non il documento intero — più efficiente e di dimensione fissa.
3. **D:** Con quale chiave si firma e con quale si verifica? **R:** Si firma con la chiave **privata** del mittente; si verifica con la sua chiave **pubblica**.
4. **D:** Cosa succede se la chiave privata di firma viene rubata? **R:** L'attaccante può firmare documenti a nome della vittima, spacciandoli per autentici.
5. **D:** Cita tre algoritmi di firma comuni. **R:** RSA-PSS, ECDSA (usato in TLS e Bitcoin) e EdDSA (Ed25519).

## Collegamenti

- [[Crittografia Asimmetrica]] — il meccanismo base (chiave pubblica/privata)
- [[Funzioni di Hash]] — l'hash del documento è ciò che viene effettivamente firmato
- [[Certificati Digitali e CA]] — i certificati sono firmati digitalmente dalle CA
- [[TLS e SSL]] — le firme digitali sono centrali nell'handshake TLS
- [[RSA]] — uno degli algoritmi più usati per le firme digitali
- [[OpenSSL]] — tool per generare chiavi e firmare documenti

## Fonti

1. Cloudflare Learning — What is a digital signature?: https://www.cloudflare.com/learning/ssl/what-is-a-digital-signature/
2. Wikipedia — Digital signature: https://en.wikipedia.org/wiki/Digital_signature
3. NIST — FIPS 186-5 (Digital Signature Standard): https://csrc.nist.gov/publications/detail/fips/186/5/final
4. NIST — Glossary — Digital Signature: https://csrc.nist.gov/glossary/term/digital_signature
