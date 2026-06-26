---
tipo: entita
tag: [crypto, tool]
fase: 1
fonti: 4
aggiornato: 2026-06-20
stato: maturo
aliases: ["OpenSSL"]

---

# OpenSSL

## Cos'è

**OpenSSL** è la libreria e il tool a riga di comando open-source più diffuso al mondo per operazioni crittografiche: generare chiavi e certificati, cifrare file, calcolare hash, testare connessioni [[TLS e SSL|TLS]], e molto altro. È preinstallato su quasi tutti i sistemi Linux/macOS e disponibile per Windows. È sia una libreria (usata da server web come Apache e Nginx) sia un tool interattivo da terminale.

## Uso tipico

```bash
# ── HASH ──────────────────────────────────────────────────
# Hash SHA-256 di un file
openssl dgst -sha256 file.txt

# Hash MD5 di una stringa
echo -n "ciao" | openssl dgst -md5

# ── CIFRATURA SIMMETRICA ──────────────────────────────────
# Cifrare un file con AES-256-CBC
openssl enc -aes-256-cbc -pbkdf2 -in chiaro.txt -out cifrato.enc

# Decifrare
openssl enc -aes-256-cbc -pbkdf2 -d -in cifrato.enc -out chiaro.txt

# ── CHIAVI E CERTIFICATI ──────────────────────────────────
# Generare chiave privata RSA 2048-bit
openssl genrsa -out chiave.pem 2048

# Estrarre la chiave pubblica
openssl rsa -in chiave.pem -pubout -out chiave_pub.pem

# Generare un certificato self-signed (valido 365 giorni)
openssl req -x509 -new -key chiave.pem -days 365 -out certificato.pem

# ── TLS ───────────────────────────────────────────────────
# Testare una connessione TLS e vedere il certificato
openssl s_client -connect example.com:443

# Verificare scadenza certificato
openssl s_client -connect example.com:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -dates

# ── FIRMA DIGITALE ────────────────────────────────────────
# Firmare un file
openssl dgst -sha256 -sign chiave.pem -out firma.bin documento.txt

# Verificare la firma
openssl dgst -sha256 -verify chiave_pub.pem -signature firma.bin documento.txt
```

## Quando si usa

- **CTF e studio**: per capire praticamente come funzionano hash, cifratura, certificati e firme digitali.
- **Sysadmin**: generare certificati self-signed per ambienti di test, rinnovare certificati, verificare la configurazione TLS di un server.
- **Penetration testing**: testare la versione TLS e le cipher suite di un server (`openssl s_client`), identificare configurazioni deboli.
- Ogni volta che vuoi sperimentare con concetti come [[Firma Digitale]], [[Certificati Digitali e CA]] o [[Hashing delle Password e Salting]] senza scrivere codice.

## Note e trucchi

- `openssl s_client -connect host:443` è il modo più rapido per ispezionare un certificato TLS da terminale.
- Per generare numeri casuali sicuri: `openssl rand -hex 32` (utile per generare salt, token, chiavi).
- `openssl x509 -in cert.pem -noout -text` mostra tutti i dettagli di un certificato (subject, issuer, SAN, validità).
- La versione di OpenSSL installata si verifica con `openssl version -a`.
- Heartbleed (CVE-2014-0160) era una vulnerabilità critica in OpenSSL — motivo per cui mantenere OpenSSL aggiornato è fondamentale.
- Documentazione ufficiale: https://www.openssl.org/docs/

## Collegamenti

- [[TLS e SSL]] — OpenSSL è la libreria che implementa TLS nella maggior parte dei server
- [[Certificati Digitali e CA]] — OpenSSL è lo strumento standard per generare e ispezionare certificati
- [[Firma Digitale]] — OpenSSL permette di firmare e verificare documenti da riga di comando
- [[Funzioni di Hash]] — `openssl dgst` calcola hash di file e stringhe
- [[Scambio di Chiavi Diffie-Hellman]] — `openssl dhparam` genera parametri DH

## Fonti

1. OpenSSL — Documentazione ufficiale: https://www.openssl.org/docs/
2. Wikipedia — OpenSSL: https://en.wikipedia.org/wiki/OpenSSL
3. OpenSSL — Man page openssl-s_client: https://www.openssl.org/docs/manmaster/man1/openssl-s_client.html
4. Cloudflare Blog — Heartbleed: https://blog.cloudflare.com/answering-the-critical-question-can-you-get-private-ssl-keys-using-heartbleed/
