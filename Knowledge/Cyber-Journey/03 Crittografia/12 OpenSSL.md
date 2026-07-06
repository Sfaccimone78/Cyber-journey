---
tipo: entita
tag: [crypto, tool]
fase: 1
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["OpenSSL"]

---

# OpenSSL

## In breve

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

## Lab

- **Percorso guidato locale**: riproduci l'intera catena crittografica con i comandi qui sopra — hash di un file (`openssl dgst -sha256`), cifratura AES (`openssl enc`), generazione coppia RSA + certificato self-signed, firma e verifica. Ottimo per collegare [[Funzioni di Hash]], [[Crittografia Simmetrica]], [[RSA]] e [[Firma Digitale]] senza scrivere codice.
- **[[TryHackMe]] → room *OpenSSL* / percorso su crittografia pratica**: esercizi che usano `openssl` per decifrare file, ispezionare certificati e generare chiavi in scenari CTF.
- **CryptoHack → sfide di setup** (https://cryptohack.org): diverse challenge chiedono di generare chiavi o decifrare materiale fornito; `openssl` è lo strumento da riga di comando più rapido per ispezionare `.pem`, `.der` e certificati.

## Domande

1. **D:** OpenSSL è solo un tool da riga di comando? **R:** No: è sia una **libreria** crittografica (usata da server come Apache e Nginx per implementare TLS) sia un tool interattivo da terminale.
2. **D:** Quale comando ispeziona rapidamente il certificato TLS di un sito? **R:** `openssl s_client -connect host:443`, spesso combinato con `openssl x509 -noout -text` per i dettagli.
3. **D:** Come si genera un valore casuale sicuro per un salt o un token? **R:** `openssl rand -hex 32`.
4. **D:** Con quali due comandi si firma e si verifica un documento? **R:** `openssl dgst -sha256 -sign chiave.pem` per firmare e `openssl dgst -sha256 -verify chiave_pub.pem -signature firma.bin` per verificare.
5. **D:** Perché è importante tenere OpenSSL aggiornato? **R:** Perché vulnerabilità critiche come Heartbleed (CVE-2014-0160) erano bug della libreria: solo l'aggiornamento le mitiga.

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
