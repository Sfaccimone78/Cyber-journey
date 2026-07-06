---
tipo: concetto
tag: [crypto, network]
fase: 1
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["Certificati Digitali e CA"]

---

# Certificati Digitali e CA

## In breve

Un **certificato digitale** è un documento elettronico che associa una **chiave pubblica** all'identità del suo proprietario (un sito web, un'azienda, una persona). La **CA (Certificate Authority)** è un'entità fidata che **firma** il certificato, garantendo che l'associazione sia autentica. Questo meccanismo è alla base di [[TLS e SSL|HTTPS]].

## Come funziona

Il sistema si basa su una gerarchia di fiducia chiamata **PKI (Public Key Infrastructure)**:

1. Un sito web genera una coppia di chiavi (pubblica + privata) e invia alla CA una **CSR (Certificate Signing Request)** con la propria chiave pubblica e i dati identificativi.
2. La CA verifica l'identità del richiedente, poi **firma** il certificato con la propria chiave privata — creando una [[Firma Digitale]].
3. Il browser, che già si fida della CA (i certificati root delle CA sono preinstallati nel sistema operativo), può verificare la firma e quindi fidarsi del sito.

Struttura di un certificato (formato **X.509**):
- **Subject** (chi è): dominio, organizzazione
- **Issuer** (chi lo ha firmato): la CA
- **Public Key**: la chiave pubblica del server
- **Validità**: date di inizio e scadenza
- **Signature**: firma digitale della CA

## Esempio pratico

```bash
# Scaricare e ispezionare il certificato di un sito
openssl s_client -connect wikipedia.org:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates

# Output atteso:
# subject=CN=wikipedia.org
# issuer=CN=DigiCert TLS RSA SHA256 2020 CA1
# notBefore=...
# notAfter=...

# Verificare la catena di certificati
openssl s_client -connect wikipedia.org:443 -showcerts </dev/null
```

## Rilevanza per la sicurezza

- Un certificato **scaduto** o con **dominio errato** genera un errore nel browser: non ignorarlo mai.
- Attacchi **Man-in-the-Middle** possono essere rilevati proprio grazie ai certificati.
- Alcune CA sono state compromesse nel passato (es. DigiNotar, 2011), dimostrandone il valore critico.
- I certificati **Let's Encrypt** hanno reso gratuita l'adozione di HTTPS per tutti.

## Lab

- **[[OpenSSL]] — ispeziona un certificato reale**: esegui `openssl s_client -connect wikipedia.org:443` e leggi subject, issuer e validità con `openssl x509 -noout -text`; poi genera una CSR (`openssl req -new`) e auto-firmala per capire il ruolo della CA. Ottimo per vedere la struttura X.509 dal vivo.
- **[[TryHackMe]] → room *Certificate Authority* / percorso su HTTPS e PKI**: guide interattive che ricostruiscono la catena di fiducia (root → intermediate → leaf) e mostrano gli errori del browser su certificati scaduti o self-signed.
- **badssl.com — pratica libera** (https://badssl.com): apri i sottodomini `expired.`, `self-signed.`, `wrong.host.` e osserva quale errore il browser mostra in ciascun caso; collega ogni errore alla parte del certificato che lo causa.

## Domande

1. **D:** Cosa associa un certificato digitale? **R:** Una chiave pubblica all'identità del suo proprietario (dominio, organizzazione o persona).
2. **D:** Qual è il ruolo della CA? **R:** È un'entità fidata che verifica l'identità del richiedente e **firma** il certificato con la propria chiave privata, garantendone l'autenticità.
3. **D:** Perché il browser si fida di un certificato firmato da una CA? **R:** Perché i certificati root delle CA sono preinstallati nel sistema operativo/browser: verificando la firma della CA sul certificato, la fiducia si propaga al sito.
4. **D:** Cosa contiene una CSR? **R:** La chiave pubblica del richiedente e i suoi dati identificativi, inviati alla CA per ottenere un certificato firmato.
5. **D:** Perché la compromissione di una CA (es. DigiNotar 2011) è così grave? **R:** Una CA compromessa può emettere certificati fraudolenti considerati validi da tutti i browser, abilitando attacchi MITM su larga scala.

## Collegamenti

- [[TLS e SSL]] — i certificati sono il cuore dell'handshake TLS
- [[Firma Digitale]] — meccanismo con cui la CA garantisce il certificato
- [[Crittografia Asimmetrica]] — la coppia chiave pubblica/privata alla base del sistema
- [[OpenSSL]] — tool per generare, ispezionare e verificare certificati

## Fonti

1. Cloudflare Learning — What is a TLS/SSL certificate?: https://www.cloudflare.com/learning/ssl/what-is-an-ssl-certificate/
2. Wikipedia — Public key certificate: https://en.wikipedia.org/wiki/Public_key_certificate
3. Mozilla — PKI guide: https://wiki.mozilla.org/CA
4. Let's Encrypt — How it works: https://letsencrypt.org/how-it-works/
