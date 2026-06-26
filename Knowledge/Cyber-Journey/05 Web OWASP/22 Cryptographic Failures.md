---
tipo: concetto
tag: [web, owasp, crypto]
fase: 2
fonti: 2
aggiornato: 2026-06-26
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

## Collegamenti
- [[OWASP Top 10]]
- [[TLS e SSL]] · [[Funzioni di Hash]] · [[Hashing delle Password e Salting]]
- [[Security Misconfiguration]] · [[Autenticazione e Gestione Sessioni]] · [[Secure Coding]]

## Fonti
- OWASP Top 10:2025 A04 / 2021 A02 Cryptographic Failures — https://owasp.org/Top10/
- Anderson, *Security Engineering*, cap. 5 — https://www.cl.cam.ac.uk/~rja14/book.html
