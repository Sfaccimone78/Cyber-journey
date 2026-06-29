---
tipo: concetto
tag: [api]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["API Testing e Tooling"]
---

# API Testing e Tooling

## In breve

Testare un'API segue un workflow preciso: scoperta (discovery degli endpoint e della documentazione), ricostruzione del contratto, autenticazione, e test sistematico delle vulnerabilità (BOLA, BFLA, broken auth, mass assignment, SSRF, rate limit). Il toolchain combina proxy d'intercettazione (Burp), client per richieste (curl, Postman), fuzzer di endpoint e parametri (ffuf, kiterunner, arjun) e strumenti specializzati (jwt_tool per i token). Questa nota mette in fila gli strumenti e il metodo per attaccare API REST e GraphQL reali.

## Come funziona

Il flusso operativo:

1. **Discovery**: cercare la documentazione (`/swagger.json`, `/openapi.json`, `/graphql` con introspection) e fare brute degli endpoint con wordlist dedicate. kiterunner è specifico per le API perché usa route+metodo da dataset di Swagger reali.
2. **Mappatura**: importare l'OpenAPI in Postman/Burp per ricostruire tutte le operazioni; identificare i parametri nascosti con arjun.
3. **Autenticazione**: ottenere token validi per più ruoli (admin e utente standard) da usare nei confronti di autorizzazione.
4. **Test autorizzazione**: con Burp Autorize replicare ogni richiesta a privilegio inferiore per scovare BOLA/BFLA (vedi [[BOLA e BFLA]]).
5. **Test token**: analizzare e manomettere i JWT con jwt_tool (vedi [[Autenticazione e Autorizzazione API]]).
6. **Test input**: mass assignment, SSRF, injection variando body e header (vedi [[Mass Assignment, SSRF e Rate Limiting API]]).
7. **Test resilienza**: assenza di rate limit e abuso di flussi con Intruder/ffuf.

Per GraphQL il toolset cambia: si sfrutta l'introspection per ricostruire lo schema e strumenti come GraphQL Voyager/InQL; vedi [[GraphQL Security]].

## Esempi

Discovery di endpoint API con kiterunner:

```bash
kr scan https://target.tld -w routes-large.kite \
  -H "Authorization: Bearer $TOKEN" -x 10
```

Brute di path API con ffuf e wordlist SecLists:

```bash
ffuf -u "https://target.tld/FUZZ" \
  -w /usr/share/seclists/Discovery/Web-Content/api/objects.txt \
  -mc 200,201,401,403 -fc 404
```

Scoperta di parametri nascosti con arjun:

```bash
arjun -u "https://target.tld/api/v1/search" -m GET
```

Importare un'OpenAPI in Postman per ricostruire la collection:

```bash
# Scarica lo schema, poi: Postman > Import > File/Link > openapi.json
curl -s "https://target.tld/openapi.json" -o openapi.json
```

Analisi di un JWT con jwt_tool durante il test:

```bash
jwt_tool $TOKEN -T   # modalità tamper interattiva su claim e firma
```

Introspection GraphQL per ricostruire lo schema:

```bash
curl -s -X POST "https://target.tld/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name fields { name } } } }"}' | jq .
```

In Burp Suite il flusso completo passa per Proxy (intercettazione), Repeater (manipolazione mirata), Intruder (fuzzing/bruteforce) e le estensioni Autorize, JWT Editor e InQL per GraphQL.

## Mitigazione e difesa

- Dal lato difensivo, gli stessi strumenti servono per il test continuo: integrare scanner API (OpenAPI-driven) nella CI/CD.
- Disabilitare l'introspection GraphQL e la documentazione Swagger in produzione.
- Monitorare e correlare i log per riconoscere le firme degli strumenti offensivi (rate, user-agent, pattern di enumerazione).
- Esporre solo gli endpoint inventariati e applicare rate limit anche agli strumenti di discovery.

## Lab

- [[PortSwigger Web Academy]] - percorso API testing end-to-end.
- [[TryHackMe]] - room su tooling e metodologia API.
- [[HackTheBox]] - macchine per esercitare il workflow completo.
- crAPI - target ideale per provare kiterunner, Autorize, jwt_tool e arjun in sequenza.
- VAmPI - palestra per ffuf e test di autorizzazione.
- OWASP juice-shop - per integrare il testing nel contesto di un'app reale.

## Domande

1. **Perché kiterunner è migliore di un fuzzer generico per le API?** Usa route abbinate al metodo HTTP corretto, estratte da Swagger reali, riducendo falsi negativi rispetto al brute di soli path con GET.
2. **A cosa serve arjun?** A scoprire parametri nascosti (query o JSON) non documentati, utili per mass assignment e injection.
3. **Qual è il valore di importare un'OpenAPI in Postman/Burp?** Ricostruisce l'intero contratto API automaticamente, evitando l'enumerazione cieca e dando la lista completa di operazioni e parametri.
4. **Come si ricostruisce uno schema GraphQL?** Tramite query di introspection sull'endpoint `/graphql`, se l'introspection è abilitata; vedi [[GraphQL Security]].
5. **Perché servono token di ruoli diversi nel test?** Per confrontare le risposte e rilevare BOLA/BFLA con strumenti come Autorize.

## Approfondimento livello esperto

Un workflow esperto è guidato dalla **differenza tra contesti**: lo stesso strumento dà valore solo se confronta stati. Autorize è potente perché esegue ogni richiesta in tre varianti (utente privilegiato, utente a basso privilegio, nessun token) e segnala le discrepanze; senza questo confronto un 200 non significa nulla. Sul **JWT**, jwt_tool va oltre la decodifica: automatizza alg confusion, `none`, bruteforce HMAC e kid injection, ma l'operatore deve sapere quale chiave pubblica fornire (recuperata da `/jwks.json`) per l'attacco RS256->HS256 (cross-link [[Autenticazione e Autorizzazione API]]). Per **GraphQL** il tooling cambia logica: InQL e Voyager ricostruiscono lo schema dall'introspection, poi si testano batching abuse (più alias/operazioni in una richiesta per bypassare rate limit) e query annidate costose; se l'introspection è disabilitata si ricorre a field suggestion e clairvoyance per dedurre i campi (cross-link [[GraphQL Security]]). Per il **rate-limit bypass** durante il test, Intruder con rotazione di `X-Forwarded-For` e race condition (richieste parallele) verifica la robustezza dei contatori. Sul fronte detection/logging, va ricordato che gli strumenti lasciano firme: kiterunner e ffuf generano volumi e pattern riconoscibili, e un buon difensore correla rate, sequenzialità degli id e user-agent per distinguere il testing dall'uso reale - lo stesso ragionamento che l'attaccante usa per restare sotto soglia.

## Collegamenti

- [[Fondamenti API e REST Security]]
- [[OWASP API Security Top 10]]
- [[BOLA e BFLA]]
- [[Autenticazione e Autorizzazione API]]
- [[Mass Assignment, SSRF e Rate Limiting API]]
- [[GraphQL Security]]
- [[Broken Access Control e IDOR]]
- [[Cookie e JWT]]
- [[Server-Side Request Forgery (SSRF)]]

## Fonti

- https://owasp.org/API-Security/editions/2023/en/0x00-header/
- https://portswigger.net/web-security/api-testing
- https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/api-testing
