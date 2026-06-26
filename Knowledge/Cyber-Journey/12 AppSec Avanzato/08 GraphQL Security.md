---
tipo: concetto
tag: [web, owasp, tool]
fase: 3
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["GraphQL Security", "GraphQL Attacks"]
---

# GraphQL Security

> [!warning] Uso etico
> Enumerare schema e abusare di query/mutation **solo** su lab autorizzati o API in scope. Estrarre dati altrui via IDOR su un endpoint GraphQL reale è accesso abusivo.

## In breve
**GraphQL** è un linguaggio di query per API: un **singolo endpoint** (di solito `/graphql`) accetta query in cui il client specifica esattamente i campi voluti. Flessibilità potente, ma sposta molta logica di autorizzazione sul resolver di ogni campo → superfici nuove: introspection, IDOR per-campo, batching abuse, DoS da query annidate. Si combina con [[Broken Access Control e IDOR]] e [[Server-Side Request Forgery (SSRF)]].

## Riconoscere e mappare l'endpoint
Endpoint comuni: `/graphql`, `/api/graphql`, `/v1/graphql`, `/graphql.php`, `/graphiql` (IDE). Una query universale di probe:
```graphql
query { __typename }
```
Se risponde `{"data":{"__typename":"Query"}}` → è GraphQL.

## 1. Introspection (la "mappa" dell'API)
GraphQL può descrivere sé stesso. Se l'introspection è abilitata in produzione, si estrae l'intero schema (tipi, campi, mutation, argomenti):
```graphql
query IntrospectionQuery {
  __schema {
    types { name fields { name args { name } } }
    queryType { name }
    mutationType { name }
  }
}
```
Strumenti: **InQL** (estensione [[Burp Suite]]), **GraphQL Voyager** (visualizza lo schema), **graphw00f** (fingerprint dell'engine), **clairvoyance** (ricostruisce lo schema *anche con introspection disabilitata*, per brute-force dei campi).

## 2. Suggestions leak (introspection "off" aggirata)
Anche con introspection disabilitata, molti server (Apollo) restituiscono **suggerimenti** sui nomi di campo sbagliati ("Did you mean ...?"), permettendo di ricostruire lo schema a forza bruta.
```graphql
query { user { usrnam } }    # → errore: 'Did you mean "username"?'
```

## 3. IDOR / Broken access control per-campo
L'autorizzazione va imposta su **ogni** resolver. Spesso un campo sensibile è protetto in un path ma non in un altro:
```graphql
query { user(id: 2) { id email passwordResetToken } }   # accesso a dati di altri utenti
```
Vedi [[Broken Access Control e IDOR]] — GraphQL ne moltiplica le occasioni perché ogni campo è un potenziale punto d'accesso.

## 4. Batching abuse — bypass rate limit / brute force
Più operazioni in una sola richiesta HTTP eludono i rate limit basati sul numero di richieste (utile per OTP/login brute force):
```graphql
# Aliasing: 100 tentativi di login in una sola query
query {
  a: login(user:"admin", pass:"p1") { token }
  b: login(user:"admin", pass:"p2") { token }
  c: login(user:"admin", pass:"p3") { token }
}
```
```json
// Array batching (JSON): [ {"query":"..."}, {"query":"..."}, ... ]
```

## 5. DoS — query profonde/cicliche
Schemi con relazioni circolari permettono query annidate che esplodono in complessità:
```graphql
query { posts { author { posts { author { posts { author { id }}}}}}}
```
Senza limiti di profondità/complessità → esaurimento risorse.

## 6. Mutation abuse e injection a valle
Le **mutation** modificano stato: cercare mutation non autorizzate (cambio ruolo, reset password). Gli argomenti possono inoltre veicolare [[SQL Injection]], [[Command Injection]] o [[Server-Side Request Forgery (SSRF)]] se passati a sink non sanitizzate.
```graphql
mutation { updateUser(id: 2, role: "admin") { id role } }
```

## 7. CSRF su GraphQL
Se l'endpoint accetta `application/x-www-form-urlencoded` o `GET`, una query può essere innescata cross-site (CSRF, vedi [[Cross-Site Request Forgery (CSRF)]]) bypassando il requisito `application/json`.

## Impatto
Esfiltrazione massiva di dati, account takeover (reset token/mutation), bypass di rate limit e 2FA, DoS, e injection classiche a valle dei resolver.

## Come difendersi
1. **Disabilita l'introspection** in produzione e **disattiva i suggerimenti** ("Did you mean").
2. **Autorizzazione su ogni resolver/campo**, non solo all'ingresso; usa una matrice di accesso coerente.
3. **Limita** profondità query, complessità/costo, numero di alias e batch per richiesta.
4. **Disabilita il batching** o applica rate limit per-operazione (non per-richiesta).
5. **Allow-list di query persistite** (persisted queries) dove possibile.
6. Sanitizza gli argomenti passati a DB/OS/HTTP (anti-injection/SSRF); forza `Content-Type: application/json` (anti-CSRF).

## Lab
- PortSwigger — GraphQL API vulnerabilities (lab: "Accessing private GraphQL posts", "Accidental exposure of private GraphQL fields", "Finding a hidden GraphQL endpoint", "Bypassing GraphQL brute force protections", "Performing CSRF over GraphQL"): https://portswigger.net/web-security/graphql
- HackTricks — GraphQL: https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/graphql
- OWASP — GraphQL Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html

## Collegamenti
- [[Broken Access Control e IDOR]]
- [[SQL Injection]]
- [[Server-Side Request Forgery (SSRF)]]
- [[Cross-Site Request Forgery (CSRF)]]
- [[Burp Suite]]
- [[OWASP Top 10]]

## Fonti
- PortSwigger — GraphQL API vulnerabilities: https://portswigger.net/web-security/graphql
- OWASP — GraphQL Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html
- doyensec/graph-ql + InQL (BApp Store): https://github.com/doyensec/inql
- nikitastupin/clairvoyance: https://github.com/nikitastupin/clairvoyance
