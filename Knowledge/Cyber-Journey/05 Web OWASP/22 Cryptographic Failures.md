---
tipo: concetto
tag: [web, owasp, crypto]
fase: 2
fonti: 2
aggiornato: 2026-07-02
stato: maturo
aliases: ["Cryptographic Failures"]
---
# Cryptographic Failures

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger Academy, DVWA, TryHackMe).

## In breve
**A02:2021** (ex "Sensitive Data Exposure") dell'[[OWASP Top 10]]. Riguarda i fallimenti — o l'assenza — di crittografia che portano all'esposizione di **dati sensibili** (credenziali, PII, dati sanitari, carte). Il focus è sul **dato da proteggere** (in transito e a riposo) e su **come** lo si protegge male.

> [!note] Numerazione OWASP
> Nella bozza **OWASP Top 10:2025** questa categoria è risalita a **A04 Cryptographic Failures**. La wiki usa come baseline la 2021 ([[OWASP Top 10]]); cita la 2025 dove rilevante.

## Meccanismo d'attacco
- **Dati in chiaro in transito**: HTTP invece di HTTPS, downgrade TLS, certificati non validati → sniffing/[[Attacchi di Rete]] MITM.
- **Algoritmi deboli/obsoleti**: MD5, SHA-1, DES, RC4; TLS 1.0/1.1; cifrari "export-grade".
- **Hashing password sbagliato**: password in chiaro, o con hash veloce e **senza salt** → rainbow table; uso di MD5/SHA-1 per password invece di KDF lenti.
- **Errori d'uso**: ECB mode (pattern visibili), IV/nonce riusati o prevedibili, chiavi hardcoded nel codice, RNG non crittografico (`rand()`).
- **Padding oracle**: il server distingue padding valido/invalido in CBC → decrypt senza chiave.

## Esempio
```python
# Hashing INSICURO di password (veloce, no salt) — vulnerabile a rainbow table
import hashlib
hashlib.md5(password.encode()).hexdigest()   # ❌

# CORRETTO: KDF lento con salt automatico
import bcrypt
bcrypt.hashpw(password.encode(), bcrypt.gensalt())   # ✅
```
```bash
# Forzare hash MD5 deboli rubati dal DB
hashcat -m 0 -a 0 hashes.txt rockyou.txt
john --format=raw-md5 hashes.txt
```

## Mitigazione (priorità)
- **TLS ovunque** (HTTPS obbligatorio, HSTS), TLS 1.2+/1.3, suite forti, validazione certificati → [[TLS e SSL]].
- Password: **bcrypt / scrypt / Argon2id** (lenti, con salt e fattore di costo). Mai MD5/SHA-1/SHA-256 nudo per password → [[Hashing delle Password e Salting]].
- Hash per integrità: **SHA-256/SHA-3** → [[Funzioni di Hash]]; MAC con **HMAC**.
- Cifratura simmetrica **autenticata** (AES-GCM, ChaCha20-Poly1305); mai ECB; IV/nonce unici e casuali.
- **CSPRNG** per chiavi/token (`secrets`, `/dev/urandom`); gestione chiavi in vault/HSM, mai in repo.
- Minimizzare i dati sensibili conservati (non si può perdere ciò che non si ha).

## CVE reale
- **CVE-2014-0160 "Heartbleed"** (OpenSSL) — buffer over-read che dumpa memoria del server, incluse chiavi private TLS e sessioni: il fallimento crittografico catastrofico per eccellenza.
- **CVE-2014-3566 "POODLE"** — padding oracle su SSL 3.0 che permette il downgrade e la decifratura del traffico.

## Lab
- [[PortSwigger Web Academy]] → i fallimenti crittografici sfruttabili in web app si praticano soprattutto nella categoria **JWT** (*authentication bypass via weak signing key* = brute force del segreto HS256) e in **Information disclosure** (segreti/chiavi esposti).
- **Cracking di hash deboli** (target locale, autorizzato): dato un dump di hash MD5/SHA-1, provare `hashcat -m 0 hashes.txt rockyou.txt` o `john --format=raw-md5`. Ideale su set di training come i file forniti da TryHackMe.
- TryHackMe → room *Crypto 101* / *Hashing - Crypto 101*: teoria + pratica su hashing, salting e KDF.
- **Config TLS**: eseguire `testssl.sh https://target` (o `sslscan`) su un host autorizzato per rilevare TLS 1.0/1.1, cifrari deboli, certificati non validi.
- Cosa esercitare: distinguere hash veloci (MD5/SHA-1) da KDF lenti (bcrypt/Argon2) e capire perché i primi cadono con rockyou.

## Domande
1. **D:** Qual è il focus della categoria Cryptographic Failures rispetto alle injection?  **R:** Non un input malevolo, ma la protezione del **dato sensibile** (in transito e a riposo): assenza o uso errato della crittografia che ne causa l'esposizione.
2. **D:** Perché MD5/SHA-1 sono inadatti per le password mentre bcrypt/Argon2 vanno bene?  **R:** MD5/SHA-1 sono hash **veloci**: consentono miliardi di tentativi al secondo (rainbow table/brute). bcrypt/scrypt/Argon2 sono KDF **lenti**, con salt e fattore di costo regolabile, rendendo il cracking impraticabile.
3. **D:** Cos'è un padding oracle e cosa permette?  **R:** Un server che distingue padding valido da invalido in CBC; sfruttandolo si decifra il ciphertext **senza conoscere la chiave** (es. POODLE).
4. **D:** Perché la modalità ECB è insicura?  **R:** Cifra blocchi identici in modo identico, lasciando trapelare pattern del plaintext; serve una modalità autenticata come AES-GCM con IV/nonce unici.
5. **D:** Perché serve un CSPRNG e non `rand()` per chiavi e token?  **R:** I generatori non crittografici sono prevedibili: un attaccante può ricostruirne l'output e indovinare token/chiavi; servono generatori crittografici (`secrets`, `/dev/urandom`).

## Collegamenti
- [[OWASP Top 10]]
- [[TLS e SSL]] · [[Funzioni di Hash]] · [[Hashing delle Password e Salting]]
- [[Security Misconfiguration]] · [[Autenticazione e Gestione Sessioni]] · [[Secure Coding]]
- [[PortSwigger Web Academy]]

## Fonti
- OWASP Top 10:2025 A04 / 2021 A02 Cryptographic Failures — https://owasp.org/Top10/
- Anderson, *Security Engineering*, cap. 5 — https://www.cl.cam.ac.uk/~rja14/book.html
