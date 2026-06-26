---
tipo: concetto
tag: [reti, web]
fase: 1
fonti: 5
aggiornato: 2026-06-26
stato: maturo
aliases: ["HTTP e HTTPS", "HTTP/HTTPS"]
---

# HTTP e HTTPS

## In breve
**HTTP** (HyperText Transfer Protocol) è il protocollo applicativo del web: modello **richiesta-risposta**, testuale, **stateless**. **HTTPS** è HTTP dentro un tunnel [[TLS e SSL|TLS]] che garantisce **riservatezza, integrità e autenticazione** del server. HTTP usa la porta 80, HTTPS la 443. Quasi ogni vulnerabilità web ([[OWASP Top 10]]) viaggia dentro messaggi HTTP → capirne l'anatomia è la base dell'offensive web.

---

## Anatomia di richiesta e risposta

### Request
```http
GET /index.html HTTP/1.1
Host: www.example.com             ← obbligatorio in HTTP/1.1 (virtual hosting multiplo)
User-Agent: Mozilla/5.0
Accept: text/html,application/xhtml+xml
Accept-Language: it-IT,it;q=0.9
Accept-Encoding: gzip, deflate, br
Cookie: session=abc123; prefs=dark
Referer: https://example.com/home
Connection: keep-alive
                                  ← riga vuota obbligatoria separa header e body
```

### Response
```http
HTTP/1.1 200 OK
Date: Mon, 22 Jun 2026 10:00:00 GMT
Server: nginx/1.25.0
Content-Type: text/html; charset=UTF-8
Content-Length: 4321
Set-Cookie: session=abc123; Path=/; Secure; HttpOnly; SameSite=Lax
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'

<html>...</html>
```

> **Nota**: il body è separato dagli header da una **riga vuota** (CRLF). Dimenticarlo in implementazioni custom causa injection di header (CRLF injection).

---

## Metodi HTTP
| Metodo | Uso principale | Idempotente | Safe | Note offensive |
|---|---|---|---|---|
| GET | lettura risorsa | sì | sì | parametri in query string → log/history |
| POST | invia dati (login, form, API) | no | no | body non in URL ma sempre leggibile |
| PUT | crea/sostituisce risorsa intera | sì | no | upload file se abilitato → RCE risk |
| PATCH | modifica parziale | no | no | spesso non autenticato su API mal configurate |
| DELETE | elimina risorsa | sì | no | richiede auth — IDOR se manca |
| HEAD | solo header (niente body) | sì | sì | fingerprinting server senza corpo |
| OPTIONS | metodi ammessi su una risorsa | sì | sì | CORS preflight, rivela metodi attivi |
| TRACE | eco della richiesta | sì | sì | **Cross-Site Tracing (XST)** — disabilitare |

---

## Codici di stato
| Classe | Range | Esempi chiave |
|---|---|---|
| **1xx** | Informazionale | 101 Switching Protocols (WebSocket upgrade) |
| **2xx** | Successo | 200 OK, 201 Created, 204 No Content |
| **3xx** | Redirect | 301 Moved Permanently, 302 Found, 304 Not Modified (cache), 307/308 temp/perm con metodo conservato |
| **4xx** | Errore client | **401** non autenticato, **403** vietato, 404 non trovato, **429** rate limit, **405** metodo non ammesso |
| **5xx** | Errore server | 500 Internal, 502 Bad Gateway, 503 Service Unavailable |

> [!note] 401 vs 403
> **401 Unauthorized** = "non so chi sei, autenticati" (manca/invalido il token). **403 Forbidden** = "so chi sei, ma non puoi". Distinzione chiave nei test di [[Broken Access Control e IDOR|access control]]. Un 403 con risposta diversa cambiando il metodo HTTP o aggiungendo `X-Forwarded-For: 127.0.0.1` è un segnale classico di misconfiguration.

---

## Header di sicurezza principali
| Header | Scopo | Valore consigliato |
|---|---|---|
| `Strict-Transport-Security` | HSTS: forza HTTPS anche su richieste future | `max-age=31536000; includeSubDomains; preload` |
| `Content-Security-Policy` | limita sorgenti di script/stile (anti-[[Cross-Site Scripting (XSS)\|XSS]]) | `default-src 'self'` (poi affinare) |
| `X-Frame-Options` | impedisce embedding in iframe (anti-[[Clickjacking]]) | `DENY` o `SAMEORIGIN` |
| `X-Content-Type-Options` | blocca MIME sniffing | `nosniff` |
| `Referrer-Policy` | controlla l'header Referer | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | limita API browser (camera, geoloc…) | feature-specific |

Verifica header con `curl -I https://target.com` o con Securityheaders.com.

---

## Stateless + cookie + sessioni
HTTP non ricorda nulla tra una richiesta e l'altra. Lo **stato** (sei loggato?) si simula con:
- **Cookie** (`Set-Cookie` → il browser rimanda automaticamente): identificano la sessione lato server.
- **Token Bearer** (JWT nell'header `Authorization: Bearer <token>`): lato client stateless.

Attributi cookie critici:
| Attributo | Effetto |
|---|---|
| `Secure` | inviato solo su HTTPS |
| `HttpOnly` | non accessibile via JavaScript → blocca XSS cookie theft |
| `SameSite=Strict` | non inviato su richieste cross-site → blocca [[Cross-Site Request Forgery (CSRF)\|CSRF]] |
| `SameSite=Lax` | inviato su navigazione top-level GET cross-site (meno protezione) |
| `Path=/` | scope URL |
| `Expires`/`Max-Age` | durata |

---

## Versioni HTTP a confronto
| Versione | Transport | Multiplexing | Header | Note chiave |
|---|---|---|---|---|
| **HTTP/1.0** | TCP (nuova connessione per richiesta) | no | testo | obsoleto |
| **HTTP/1.1** | TCP keep-alive | no (HOL blocking) | testo | standard storico; pipelining poco usato |
| **HTTP/2** | TCP (TLS nella pratica) | sì, **stream** multipli | binario + compressione HPACK | push server, priorità; più veloce su connessioni con latenza |
| **HTTP/3** | **QUIC** (UDP) | sì, niente HOL a livello trasporto | QPACK | TLS 1.3 integrato in QUIC; handshake 0-RTT; adottato da CDN e big tech |

> HTTP/3 su UDP: il firewall che blocca UDP 443 rompe HTTP/3. Fallback automatico a HTTP/2. Da ricordare nel troubleshooting.

---

## HTTPS: il tunnel TLS passo per passo

HTTPS = HTTP dentro [[TLS e SSL]]. L'handshake TLS 1.3 (semplificato):

```
Client                                    Server
  |--- ClientHello (versioni, cipher, random_c) --->|
  |<-- ServerHello (cipher scelta, random_s)       --|
  |<-- Certificate (chiave pubblica, firma CA)     --|
  |<-- CertificateVerify + Finished               --|
  |--- (verifica cert: CA fidata? hostname match?) --|
  |--- Finished ---------------------------------->--|
  |=== traffico cifrato simmetrico (AES-GCM) ======|
```

Passi chiave:
1. **ClientHello**: cipher suite e random del client.
2. **ServerHello + Certificato**: server sceglie la cipher, invia il certificato firmato da una CA (verifica in [[Certificati Digitali e CA]]).
3. **Key exchange ECDHE**: entrambi derivano la stessa chiave di sessione senza trasmetterla (forward secrecy: sessioni passate sicure anche se la chiave privata viene compromessa in futuro).
4. **Traffico cifrato** simmetricamente (veloce, es. AES-256-GCM).

TLS 1.2 aggiunge un round-trip rispetto a TLS 1.3. Dettagli sul riepilogo in [[TLS e SSL]].

---

## Meccanismo interno — come viaggia un byte

```
Browser:
  1. Risolve hostname via [[DNS]] → ottiene IP
  2. [[Three-Way Handshake TCP]] → connessione TCP/443
  3. Handshake TLS → canale cifrato
  4. Serializza richiesta HTTP in testo (o binario HTTP/2)
  5. Passa i byte a TCP/TLS → invia

Server:
  6. Riceve byte, decomprime TLS, parsa headers
  7. Routing: trova il virtual host via header Host
  8. Genera risposta, cifra, rimanda
```

L'header `Host` è obbligatorio in HTTP/1.1 perché un IP può servire decine di virtual host (es. shared hosting). Il server usa `Host` per demultiplexare. Mancarlo è un errore 400.

---

## Attacchi su HTTP/HTTPS
### 1. SSL Stripping (downgrade)
L'attaccante in posizione [[Man-in-the-Middle (MITM)|MITM]] intercetta la prima richiesta HTTP e risponde come se fosse il server, mantenendo HTTPS solo verso il server reale. La vittima comunica in chiaro.

**Difesa**: **HSTS** (`Strict-Transport-Security`) istruisce il browser a usare SEMPRE HTTPS per quel dominio per `max-age` secondi. Con `preload` il dominio entra in una lista hardcoded nel browser → immune anche alla primissima richiesta.

### 2. MITM su certificato
Attaccante con CA root installata sul device (es. MDM aziendale, tool di intercettazione come [[Burp Suite]]) può presentare un certificato falso.

**Difesa**: **Certificate Pinning** — l'app confronta il certificato ricevuto con un hash hardcoded. Comune nelle app mobile. In pentest, bypassare il pinning richiede Frida o patch APK.

### 3. Header Injection / CRLF Injection
Se un input utente viene inserito in un header senza sanitizzazione, `\r\n` (CRLF) permette di iniettare header aggiuntivi o dividere la risposta HTTP (HTTP Response Splitting).

```
Input: value%0d%0aSet-Cookie: evil=1
Risultato: header legittimo + nuovo Set-Cookie iniettato
```

**Difesa**: filtrare/rifiutare CR e LF in qualsiasi input che finisce negli header.

### 4. Clickjacking via iframe
Se `X-Frame-Options` manca, la pagina può essere inclusa in un iframe su un sito malevolo → click dell'utente intercettati. Vedi [[Clickjacking]].

### 5. Mixed Content
Una pagina HTTPS che carica risorse HTTP (immagini, script) espone quelle risorse a intercettazione. I browser moderni bloccano il mixed content attivo (script/CSS); quello passivo (immagini) viene talvolta permesso con avviso.

---

## Attacco pratico — intercettare con Burp Suite (lab)
```bash
# 1. Configura il proxy: Burp → 127.0.0.1:8080
# 2. Importa il CA Burp nel browser (o nel sistema)
# 3. Intercetta la richiesta POST di login
POST /login HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 30

username=admin&password=pass

# 4. Modifica il corpo in Burp Repeater, analizza la risposta
# 5. Se l'app rispecchia l'input, cerca XSS: username=<script>alert(1)</script>
```

---

## Difesa — hardening checklist
```text
[x] Reindirizzamento HTTP → HTTPS (301 permanente)
[x] HSTS con max-age >= 31536000 + preload
[x] TLS 1.2 minimo (preferire TLS 1.3), disabilita SSL 3.0/TLS 1.0/1.1
[x] Cipher suite sicure (no RC4, no 3DES, no EXPORT)
[x] Header di sicurezza: CSP, X-Frame-Options, X-Content-Type-Options
[x] Cookie con Secure + HttpOnly + SameSite=Strict/Lax
[x] Metodo TRACE disabilitato
[x] Niente directory listing
[x] Rate limiting (429 Too Many Requests) su endpoint sensibili
[x] Certificato aggiornato + OCSP Stapling
```

---

## Comandi utili
```bash
# Solo header di risposta
curl -I https://example.com

# Dettagli handshake TLS + risposta completa
curl -v https://example.com

# Forzare HTTP/2
curl --http2 -I https://example.com

# Verifica cipher suite e versione TLS
openssl s_client -connect example.com:443 -tls1_3

# Verifica header HSTS
curl -I https://example.com | grep -i strict

# Invia POST con body JSON
curl -X POST https://api.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","pass":"test"}'

# Segui redirect (-L) e mostra tutti gli header (-v)
curl -Lv http://example.com

# Verifica metodi ammessi (OPTIONS)
curl -X OPTIONS -I https://example.com
```

---

## Troubleshooting
| Sintomo | Causa probabile | Fix |
|---|---|---|
| Browser mostra "Non sicuro" su HTTPS | cert scaduto / hostname mismatch / CA non fidata | Rinnova cert o importa CA |
| Redirect loop 301 | HSTS + configurazione errata del reverse proxy | Controlla regole di redirect su nginx/apache |
| Mixed content warning | Risorse caricate via HTTP su pagina HTTPS | Usa URL relativi o `//` schema-relative |
| ERR_TOO_MANY_REDIRECTS | Loop tra HTTP→HTTPS o cookie `Secure` su HTTP | Controlla il set di regole di redirect |
| 431 Request Header Fields Too Large | Cookie/header troppo grossi | Riduci dimensione cookie, configura `large_client_header_buffers` |

---

## Domande da esame / colloquio
1. **Differenza tra HTTP stateless e sessioni?** HTTP non mantiene stato tra richieste. Le sessioni sono simulate tramite cookie o token: il server associa un session ID a uno stato lato server (o usa JWT stateless lato client).
2. **Cosa garantisce HTTPS che HTTP non garantisce?** Riservatezza (cifratura), integrità (MAC), autenticazione del server (certificato). Non garantisce anonimato, né che l'app stessa sia sicura (XSS/SQLi passano dentro TLS).
3. **Cos'è l'SSL stripping e come si difende?** Downgrade da HTTPS a HTTP da parte di un MITM intercettando la prima richiesta. Difesa: HSTS + preload hardcoded nel browser.
4. **Differenza tra 401 e 403?** 401 = non autenticato (chi sei?), 403 = autenticato ma non autorizzato (non puoi). Confondi i due e rompi la semantica degli errori nelle API.
5. **Cosa cambia tra HTTP/2 e HTTP/3?** HTTP/2 usa TCP con multiplexing degli stream (ma soffre di HOL blocking a livello TCP). HTTP/3 usa QUIC su UDP con TLS 1.3 integrato: zero HOL blocking a livello trasporto, handshake più veloce.
6. **Cookie `SameSite=Lax` vs `SameSite=Strict`?** Lax invia il cookie su navigazioni GET cross-site (link cliccato); Strict non lo invia mai in richieste cross-site. Strict rompe SSO e link condivisi; Lax è il compromesso standard.

---

## Collegamenti
- [[TLS e SSL]] · [[Certificati Digitali e CA]] · [[DNS]] · [[Porte e Protocolli Comuni]]
- [[TCP]] · [[Three-Way Handshake TCP]] · [[Modello Client-Server]]
- [[OWASP Top 10]] · [[Cookie e JWT]] · [[Autenticazione e Gestione Sessioni]]
- [[Cross-Site Scripting (XSS)]] · [[Cross-Site Request Forgery (CSRF)]] · [[Clickjacking]]
- [[Broken Access Control e IDOR]] · [[SQL Injection]] · [[OWASP ZAP]]
- [[Man-in-the-Middle (MITM)]] · [[Burp Suite]] · [[Wireshark]]
- [[Modello OSI]] — HTTP è layer 7

## Fonti
- MDN — HTTP: https://developer.mozilla.org/en-US/docs/Web/HTTP
- Cloudflare — What is HTTPS: https://www.cloudflare.com/learning/ssl/what-is-https/
- RFC 9110 — HTTP Semantics: https://www.rfc-editor.org/rfc/rfc9110
- OWASP — Secure Headers Project: https://owasp.org/www-project-secure-headers/
- Peterson & Davie — *Computer Networks: A Systems Approach* (cap. "Applications — Traditional Applications / Web (HTTP)"): https://book.systemsapproach.org/
