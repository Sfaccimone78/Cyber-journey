---
tipo: concetto
tag: [crypto, network]
fase: 1
fonti: 8
aggiornato: 2026-07-02
stato: maturo
aliases: ["TLS e SSL", "TLS", "SSL", "TLS/SSL"]
---

# TLS e SSL

## In breve

**TLS (Transport Layer Security)** è il protocollo crittografico che protegge le comunicazioni su Internet: garantisce che i dati tra il tuo browser e un server siano **cifrati**, **autenticati** e **integri**. SSL (Secure Sockets Layer) è il suo predecessore, oggi considerato insicuro e dismesso. Quando vedi il lucchetto nel browser, stai usando TLS.

## Come funziona

TLS opera a livello di trasporto, sopra TCP. La connessione avviene in due fasi:

1. **Handshake** — il client e il server si accordano su quale versione di TLS e algoritmi usare, si scambiano i [[Certificati Digitali e CA|certificati]], e derivano una **chiave di sessione** condivisa usando meccanismi come lo [[Scambio di Chiavi Diffie-Hellman]].
2. **Record Protocol** — i dati vengono cifrati con [[Crittografia Simmetrica]] (es. AES-256-GCM) usando la chiave di sessione appena negoziata.

Versioni:
| Versione | Stato |
|----------|-------|
| SSL 2.0 / 3.0 | **Insicuro** — non usare |
| TLS 1.0 / 1.1 | **Deprecato** — RFC 8996 |
| TLS 1.2 | Accettabile, ancora diffuso |
| TLS 1.3 | **Raccomandato** — più veloce e sicuro |

## Esempio pratico

```bash
# Verifica il certificato e la versione TLS di un sito
openssl s_client -connect example.com:443 -tls1_3

# Mostra i dettagli del certificato
openssl s_client -connect example.com:443 </dev/null | openssl x509 -noout -text

# Elenca le cipher suite supportate
nmap --script ssl-enum-ciphers -p 443 example.com
```

## Rilevanza per la sicurezza

- **HTTPS = HTTP + TLS**: senza TLS il traffico viaggia in chiaro e può essere intercettato (attacco [[Man-in-the-Middle]]).
- Configurazioni deboli (TLS 1.0, cipher suite obsolete) sono vulnerabilità sfruttabili.
- I [[Certificati Digitali e CA|certificati]] scaduti o non validi sono un segnale di allarme.
- Tool come [[OpenSSL]] servono per ispezionare e testare configurazioni TLS.

---

# Strato esperto

## Handshake TLS 1.2 (passo per passo)
```
Client                                                Server
  | ── ClientHello ─────────────────────────────────► |   versioni, cipher suite, random_c, SNI, estensioni
  | ◄───────────────────── ServerHello ─────────────── |   cipher scelta, random_s
  | ◄───────────────────── Certificate ─────────────── |   catena X.509 (vedi [[Certificati Digitali e CA]])
  | ◄────────────── ServerKeyExchange ──────────────── |   params (EC)DHE + firma (autentica i params)
  | ◄────────────── ServerHelloDone ────────────────── |
  | ── ClientKeyExchange ──────────────────────────► |   chiave pubblica DHE del client (o premaster cifrato RSA)
  | ── ChangeCipherSpec / Finished ────────────────► |   da qui in poi cifrato
  | ◄───────────── ChangeCipherSpec / Finished ─────── |
  | ◄════════════ Application Data (AES-GCM) ════════► |
```
- **2 round-trip (2-RTT)** prima dei dati.
- Da `random_c`, `random_s` e il **premaster secret** si deriva il **master secret**, poi le chiavi di sessione (PRF).
- **RSA key exchange** (premaster cifrato con la pubblica del server) **non** dà forward secrecy: chi ruba la chiave privata decifra il traffico passato registrato. **(EC)DHE** sì → preferito.

## Handshake TLS 1.3 (cosa cambia)
```
Client                                                Server
  | ── ClientHello (+ key_share, supported_groups) ─► |   il client "indovina" il gruppo e manda già la sua share
  | ◄── ServerHello (+ key_share) {EncryptedExt,       |
  |        Certificate, CertVerify, Finished} ──────── |   tutto dopo ServerHello è già cifrato
  | ── Finished ──────────────────────────────────► |
  | ◄════════════ Application Data ═════════════════► |
```
- **1-RTT** (e **0-RTT** con resumption, ma 0-RTT è soggetto a replay).
- Rimossi RSA key exchange, CBC, RC4, compressione, rinegoziazione → forward secrecy **obbligatoria**.
- Cipher suite ridotte a 5 AEAD (es. `TLS_AES_128_GCM_SHA256`); la cifratura simmetrica è solo AEAD ([[AES]]-GCM o ChaCha20-Poly1305).

### Anatomia di una cipher suite (TLS 1.2)
`TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`
- `ECDHE` = key exchange (forward secrecy) · `RSA` = autenticazione del server (firma) · `AES_128_GCM` = cifratura+integrità AEAD · `SHA256` = PRF/HMAC.
> [!note] In TLS 1.3 la sintassi cambia: la suite indica **solo** AEAD+hash; key exchange e firma si negoziano in estensioni separate.

## Certificati e PKI (in breve operativo)
Il server presenta una **catena**: certificato foglia → intermedi → root (in un **trust store**). Il client verifica firme lungo la catena, validità temporale, hostname (SAN), e revoca (CRL/OCSP). Vedi [[Certificati Digitali e CA]]. La fiducia regge finché il trust store e le CA non sono compromessi.

> [!warning] Il punto debole della PKI: la CA
> Ti fidi del server **perché** ti fidi della CA che l'ha firmato. Una **CA compromessa** compromette chiunque si fidi di essa: nel 2011 **DigiNotar** fu bucata ed emise certificati `*.google.com` fraudolenti, usati per intercettare utenti iraniani. Contromisura: **Certificate Transparency (CT)**, log pubblici append-only di tutti i certificati emessi → permette di rilevare cert fraudolenti, ed è oggi requisito dei browser. [Fonte: Crypto101, cap. 17]

## Attacchi storici (livello concettuale + quando)
| Attacco | Bersaglio | Idea | Difesa |
|---|---|---|---|
| **POODLE** (2014) | SSL 3.0, CBC | padding oracle su CBC dopo downgrade a SSLv3 | disabilitare SSLv3; `TLS_FALLBACK_SCSV` |
| **BEAST** (2011) | TLS 1.0, CBC | IV prevedibile (chaining) → chosen-plaintext recupera byte | TLS 1.1+; record splitting |
| **Lucky13** (2013) | TLS ≤1.2, CBC | padding oracle **via timing** (il calcolo del MAC dipende dal padding rimosso, MAC-then-encrypt) | constant-time; AEAD; TLS 1.3 |
| **Heartbleed** (2014) | OpenSSL (impl.) | bug nel Heartbeat: legge memoria oltre il buffer → chiavi/segreti | patch OpenSSL; **non** è un difetto di TLS |
| **Downgrade / FREAK / Logjam** | negoziazione | MITM forza export-grade RSA/DH a 512 bit, fattorizzabili | rimuovere cipher export; TLS 1.3 firma l'intero hello |
| **CRIME / BREACH** | compressione | la lunghezza del ciphertext leaka segreti via compressione | disabilitare compressione TLS/HTTP |
| **DROWN** (2016) | riuso chiave con SSLv2 | un server SSLv2 attaccabile compromette TLS con la stessa chiave | disabilitare SSLv2 ovunque |
| **Bleichenbacher / ROBOT** | RSA key exchange | padding oracle PKCS#1v1.5 sul premaster | (EC)DHE; TLS 1.3 elimina RSA-KE |

Filo conduttore: quasi tutti sfruttano **modi vecchi (CBC), key exchange RSA, downgrade o compressione** — eliminati o irrigiditi in **TLS 1.3**.

## Casi limite
- **0-RTT replay (TLS 1.3)**: i dati early possono essere rigiocati → usarli solo per richieste idempotenti.
- **SNI in chiaro**: in TLS 1.2/1.3 base il nome host è visibile al MITM → **ECH** (Encrypted Client Hello) lo nasconde.
- **Resumption / session ticket**: la chiave del ticket compromessa rompe la forward secrecy delle sessioni riprese.
- **Pinning del certificato**: blocca CA fraudolente ma rompe l'app se il cert ruota male.
- **mTLS (mutual TLS)**: anche il **client** presenta un certificato → autenticazione reciproca; usato in microservizi, VPN e architetture zero-trust. Cugini con scambio chiave autenticato: SSH, IPSec, WireGuard (Noise + X25519).

## Troubleshooting (errori comuni)
1. **`certificate verify failed` / unable to get local issuer** — manca un **intermedio** nella catena servita, o trust store senza la root. Servi l'intera catena.
2. **Hostname mismatch** — il cert non copre il nome (SAN assente): il CN da solo non basta sui browser moderni.
3. **`handshake failure` / no shared cipher** — client e server non hanno cipher/versioni in comune (es. server solo TLS 1.3, client legacy).
4. **Certificato scaduto / orologio sbagliato** — la validità è temporale; spesso è il clock del client.
5. **Mixed content o downgrade silenzioso** — pagina HTTPS che carica risorse HTTP, o redirect che perde TLS → usa HSTS.

## Domande da colloquio / CTF
- *Cos'è la forward secrecy e quale parte dell'handshake la fornisce?* — la proprietà per cui compromettere la chiave privata a lungo termine non decifra il traffico passato; la dà l'**(EC)DHE** (chiavi effimere per sessione), non l'RSA key exchange.
- *Perché TLS 1.3 è più sicuro **e** più veloce?* — rimuove primitive deboli (CBC, RC4, RSA-KE, compressione) e riduce a 1-RTT (0-RTT in resumption).
- *A cosa serve il messaggio `Finished`?* — è un HMAC/MAC su tutto l'handshake: garantisce che nessun MITM abbia alterato la negoziazione (anti-downgrade).
- *Heartbleed era un difetto del protocollo TLS?* — No: era un bug d'**implementazione** in OpenSSL (lettura fuori buffer nel Heartbeat); il protocollo TLS era integro.

## Lab

- **[[OpenSSL]] + `testssl.sh` — audit di una configurazione TLS**: usa `openssl s_client -connect host:443 -tls1_3` per vedere versione, cipher e catena; poi enumera le cipher suite con `nmap --script ssl-enum-ciphers -p 443 host`. Confronta un sito moderno (solo TLS 1.3) con uno legacy per riconoscere configurazioni deboli.
- **badssl.com — pratica libera** (https://badssl.com): visita i sottodomini `tls-v1-0.`, `rc4.`, `dh512.`, `expired.` e collega ciascuno all'attacco storico corrispondente della tabella (POODLE/BEAST su TLS 1.0, cipher deboli, Logjam, cert scaduto).
- **[[TryHackMe]] → percorso su networking sicuro / HTTPS** e *The Illustrated TLS 1.3 Connection* (https://tls13.xargs.org): segui l'handshake byte per byte per interiorizzare ClientHello, key_share e i messaggi cifrati dopo ServerHello.

## Domande

1. **D:** Quali due fasi compongono una connessione TLS? **R:** L'**handshake** (negoziazione di versione/cipher, scambio certificati e derivazione della chiave di sessione) e il **Record Protocol** (cifratura simmetrica dei dati, es. AES-GCM).
2. **D:** Quale versione di TLS è raccomandata oggi e perché è più veloce? **R:** TLS 1.3: rimuove primitive deboli (CBC, RC4, RSA key exchange, compressione) e riduce l'handshake a 1-RTT (0-RTT in resumption).
3. **D:** Cos'è la forward secrecy e quale meccanismo la fornisce? **R:** La proprietà per cui rubare la chiave privata a lungo termine non decifra il traffico passato registrato; la fornisce lo scambio (EC)DHE con chiavi effimere, non l'RSA key exchange.
4. **D:** Heartbleed era un difetto del protocollo TLS? **R:** No, era un bug d'implementazione di OpenSSL (lettura fuori buffer nel Heartbeat); il protocollo era integro.
5. **D:** A cosa serve il messaggio `Finished` nell'handshake? **R:** È un MAC su tutta la negoziazione: garantisce che nessun MITM l'abbia alterata (protezione anti-downgrade).

## Collegamenti

- [[Certificati Digitali e CA]] — come il server prova la propria identità
- [[Scambio di Chiavi Diffie-Hellman]] — meccanismo di negoziazione della chiave
- [[Crittografia Simmetrica]] — cifratura dei dati dopo l'handshake
- [[AES]] — cifratura AEAD (AES-GCM) del Record Protocol
- [[RSA]] — autenticazione del server / vecchio RSA key exchange
- [[Authenticated Encryption (AEAD)]] — il Record Protocol di TLS 1.3 usa solo AEAD
- [[Padding Oracle Attack]] — POODLE/Lucky13 sul CBC, rimosso in TLS 1.3
- [[Attacchi Crittografici]] — panoramica degli attacchi a TLS
- [[Crittografia Post-Quantistica]] — migrazione ibrida X25519+ML-KEM
- [[HTTP e HTTPS]] — TLS è il componente che trasforma HTTP in HTTPS
- [[OpenSSL]] — tool per testare e gestire TLS

## Fonti

1. Cloudflare Learning — What is TLS?: https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/
2. Wikipedia — Transport Layer Security: https://en.wikipedia.org/wiki/Transport_Layer_Security
3. NIST — Guidelines for TLS Implementations (SP 800-52): https://csrc.nist.gov/publications/detail/sp/800/52/rev-2/final
4. RFC 8446 — TLS 1.3: https://datatracker.ietf.org/doc/html/rfc8446
5. RFC 5246 — TLS 1.2: https://datatracker.ietf.org/doc/html/rfc5246
6. The Illustrated TLS 1.3 Connection (byte per byte): https://tls13.xargs.org/
7. Mozilla — TLS / SSL Attacks & Server Side TLS guidance: https://wiki.mozilla.org/Security/Server_Side_TLS
8. Crypto 101 (Laurens Van Houtven), cap. 17 "SSL/TLS" (CT, DigiNotar, Lucky13); Boneh & Shoup, capp. 9/21 (AEAD, authenticated key exchange): https://crypto101.io/ · https://toc.cryptobook.us/
