---
tipo: concetto
tag: [web, owasp]
fase: 3
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["OAuth 2.0 e OpenID Connect Attacks", "OAuth Attacks", "OIDC Attacks"]
---

# OAuth 2.0 e OpenID Connect Attacks

> [!warning] Uso etico
> Testare flussi OAuth/OIDC **solo** su account propri, lab autorizzati o programmi bug bounty con OAuth in scope. Rubare l'`access_token` di un altro utente su un servizio reale è furto d'identità.

## In breve
**OAuth 2.0** è un framework di *delega d'autorizzazione*: un'app (client) ottiene un `access_token` per accedere a risorse dell'utente su un altro servizio (resource server) senza vederne le credenziali. **OpenID Connect (OIDC)** è uno strato d'*autenticazione* sopra OAuth, che aggiunge l'`id_token` (un [[Attacchi JWT|JWT]] con l'identità). Collegato a [[Autenticazione e Gestione Sessioni]] e ai "Login con Google/GitHub". Gli attacchi nascono quasi sempre da **implementazioni errate del flusso**, non dal protocollo in sé.

## I ruoli e il flusso (authorization code)
```text
1. Client → /authorize?response_type=code&client_id=..&redirect_uri=..&scope=..&state=..
2. Utente si autentica sull'Authorization Server e acconsente
3. AS → redirect_uri?code=AUTH_CODE&state=..
4. Client (back-channel) → /token  scambia code (+ client_secret) per access_token
5. Client usa access_token verso il Resource Server
```
I parametri critici per la sicurezza: **`redirect_uri`**, **`state`**, **`scope`**, **`code`**.

## 1. `redirect_uri` debole / open redirect
Se l'AS non fa matching *esatto* della `redirect_uri`, l'attaccante reindirizza `code`/`token` a un host controllato.
```text
# matching parziale → sottodominio/path attaccante
redirect_uri=https://client.com.attacker.com/cb
redirect_uri=https://client.com/cb/../../attacker
# open redirect interno usato come hop per esfiltrare il code
redirect_uri=https://client.com/redirect?url=https://attacker.com
```
Nel flusso **implicit** (`response_type=token`) il token finisce nel fragment dell'URL → furto diretto.

## 2. CSRF da `state` mancante (account hijacking)
`state` lega la richiesta alla sessione del browser. Se il client non lo genera/verifica, l'attaccante avvia un proprio flusso, cattura il suo `code` e fa sì che la vittima lo redima → l'account dell'attaccante viene collegato/loggato nella sessione della vittima (o viceversa). È **CSRF sul callback OAuth**.

## 3. Furto/riuso del `code`
- **Code replay**: se il `code` non è monouso o non scade in fretta, si riutilizza.
- **Code injection**: si inietta un `code` valido dell'attaccante nel callback della vittima.
- Mitigazione nativa: **PKCE** (`code_challenge`/`code_verifier`) lega il code al client che lo ha richiesto — la sua assenza nei client pubblici (SPA/mobile) è una falla.

## 4. Scope upgrade / consent issues
Manomettere `scope` nella richiesta token per ottenere più permessi del concesso; o sfruttare consensi "appiccicosi" che non vengono ri-richiesti.

## 5. OIDC — `id_token` e attacchi JWT
L'`id_token` è un JWT: tutti gli [[Attacchi JWT]] si applicano (`alg:none`, firma non verificata, algorithm confusion, `jku`/`kid`). In più:
- **Mancata validazione di `aud`/`iss`/`nonce`**: si riusa un id_token emesso per un altro client.
- **`nonce` mancante**: replay dell'id_token.

## 6. SSRF/leak via OIDC dynamic registration e `request_uri`
Endpoint di **dynamic client registration** o il parametro `request_uri` possono essere puntati a host interni → SSRF (vedi [[Server-Side Request Forgery (SSRF)]]). Anche il fetch del `jwks_uri`/discovery (`/.well-known/openid-configuration`) può essere abusato se l'host non è validato.

## Esempio — esfiltrazione del code via referer/redirect
```http
GET /oauth/callback?code=STOLEN_CODE&state=... HTTP/1.1
Host: client.com
# se redirect_uri non è validato esattamente, il code arriva all'attaccante;
# in alternativa il code leak via header Referer verso risorse di terze parti caricate nella pagina di callback.
```

## Impatto
Account takeover completo (login as victim), accesso non autorizzato a risorse protette, escalation di privilegi tramite scope, leak di token. Tra i bug più pagati nei bug bounty.

## Come difendersi
1. **Exact matching** della `redirect_uri` (no wildcard, no path traversal, no open redirect a valle).
2. **`state`** sempre generato e verificato (anti-CSRF) e **`nonce`** in OIDC (anti-replay).
3. **PKCE obbligatorio**, specialmente per client pubblici.
4. **`code`** monouso, breve durata, legato al client; back-channel con `client_secret`.
5. OIDC: validare firma, **`iss`**, **`aud`**, **`exp`**, **`nonce`** dell'id_token; non fidarsi di `alg` dichiarato.
6. Allow-list per `jwks_uri`/`request_uri`; bloccare host interni (anti-SSRF).
7. Evitare il flusso implicit; preferire authorization code + PKCE.

## Lab
- PortSwigger — OAuth 2.0 authentication vulnerabilities (lab: "Authentication bypass via OAuth implicit flow", "Forced OAuth profile linking", "OAuth account hijacking via redirect_uri", "Stealing OAuth access tokens via an open redirect / via a proxy page", "SSRF via OpenID dynamic client registration", "Flawed CSRF protection"): https://portswigger.net/web-security/oauth
- PortSwigger — OpenID Connect: https://portswigger.net/web-security/oauth/openid
- HackTricks — OAuth to account takeover: https://book.hacktricks.xyz/pentesting-web/oauth-to-account-takeover

## Collegamenti
- [[Attacchi JWT]]
- [[SAML e SSO Attacks]]
- [[Autenticazione e Gestione Sessioni]]
- [[Server-Side Request Forgery (SSRF)]]
- [[OWASP Top 10]]

## Fonti
- PortSwigger — OAuth 2.0 authentication vulnerabilities: https://portswigger.net/web-security/oauth
- RFC 6749 (OAuth 2.0) e RFC 7636 (PKCE): https://datatracker.ietf.org/doc/html/rfc6749
- OAuth 2.0 Security Best Current Practice (RFC 9700): https://datatracker.ietf.org/doc/html/rfc9700
- HackTricks — OAuth to Account takeover: https://book.hacktricks.xyz/pentesting-web/oauth-to-account-takeover
