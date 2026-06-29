---
tipo: concetto
tag: [api]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Fondamenti API e REST Security"]
---

# Fondamenti API e REST Security

## In breve

Un'API (Application Programming Interface) espone funzionalità applicative in modo programmatico, tipicamente su HTTP. Lo stile architetturale dominante è REST, dove le risorse sono identificate da URL e manipolate con i metodi HTTP (GET, POST, PUT, PATCH, DELETE) scambiando in genere payload JSON. Capire come è strutturato un contratto API - endpoint, metodi, parametri, status code, header di autenticazione - è il prerequisito per attaccarlo o difenderlo. La differenza chiave rispetto al web tradizionale è che l'API non ha una UI che vincola l'utente: il client invia richieste arbitrarie, quindi ogni controllo di sicurezza deve vivere lato server.

## Come funziona

In REST un endpoint come `GET /api/v1/users/42` rappresenta una risorsa (l'utente 42). I metodi HTTP definiscono l'azione: GET legge, POST crea, PUT/PATCH aggiornano, DELETE elimina. La risposta usa status code semantici: 200 OK, 201 Created, 401 Unauthorized (non autenticato), 403 Forbidden (autenticato ma non autorizzato), 404 Not Found, 429 Too Many Requests.

Elementi rilevanti per la sicurezza:

- **Versioning**: spesso convivono `/api/v1/` e `/api/v2/`; versioni vecchie restano esposte e meno protette (shadow/zombie API).
- **Content negotiation**: header `Content-Type` e `Accept` controllano il formato; cambiare `Content-Type` da `application/json` a `application/xml` o `x-www-form-urlencoded` può attivare parser diversi.
- **Documentazione**: file OpenAPI/Swagger (`/swagger.json`, `/openapi.json`, `/api-docs`) descrivono tutti gli endpoint - oro per chi attacca.
- **Stato**: REST è stateless, quindi ogni richiesta porta con sé l'autenticazione (header `Authorization`, Bearer token, API key, cookie).

GraphQL è un paradigma alternativo: un singolo endpoint (`/graphql`) riceve query strutturate in cui il client dichiara esattamente i campi che vuole. Questo sposta il modello di minaccia (introspection, query annidate, batching): vedi [[GraphQL Security]].

## Esempi

Richiesta REST autenticata con curl:

```bash
curl -s -X GET "https://target.tld/api/v1/users/42" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Accept: application/json"
```

Creazione risorsa via POST JSON:

```bash
curl -s -X POST "https://target.tld/api/v1/orders" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 7, "quantity": 2}'
```

Scoperta della documentazione OpenAPI:

```bash
for p in swagger.json openapi.json api-docs swagger-ui.html v2/api-docs; do
  echo "== /$p =="
  curl -s -o /dev/null -w "%{http_code}\n" "https://target.tld/$p"
done
```

Enumerazione di endpoint con ffuf su un wordlist di API path:

```bash
ffuf -u "https://target.tld/api/v1/FUZZ" \
  -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
  -H "Authorization: Bearer $TOKEN" -mc 200,201,401,403 -fc 404
```

In Burp Suite si intercetta la richiesta, la si manda al Repeater per modificarne metodo, header e body, e si osservano gli status code. Postman è utile per importare una collection OpenAPI e ricostruire l'intero contratto.

## Mitigazione e difesa

- Pubblicare e mantenere un **inventario API** completo (governance contro shadow/zombie API).
- Dismettere o proteggere le versioni legacy degli endpoint.
- Validare rigorosamente schema, tipi e `Content-Type` in ingresso (positive validation con schema OpenAPI).
- Non esporre la documentazione Swagger in produzione senza autenticazione.
- Usare un API gateway/WAF per normalizzare header, applicare rate limit e logging.
- Restituire status code coerenti senza leak di informazioni negli errori (stack trace, query SQL).

## Lab

- [[PortSwigger Web Academy]] - modulo "API testing".
- [[TryHackMe]] - room su API e web fundamentals.
- [[HackTheBox]] - macchine con API REST esposte.
- crAPI (Completely Ridiculous API) di OWASP per praticare su un'app vulnerabile realistica.
- VAmPI (Vulnerable API) per esercizi mirati su REST.
- OWASP juice-shop per il lato API delle vulnerabilità web classiche.

## Domande

1. **Qual è la differenza tra 401 e 403?** 401 indica autenticazione mancante o non valida; 403 indica utente autenticato ma privo dei permessi per la risorsa.
2. **Perché le shadow API sono pericolose?** Sono endpoint non documentati o versioni vecchie ancora attive, spesso prive delle patch e dei controlli applicati alle versioni correnti.
3. **Cosa rende REST diverso dal web classico dal punto di vista offensivo?** L'assenza di una UI vincolante: il client invia richieste arbitrarie, quindi ogni controllo deve essere server-side e non si può confidare nel comportamento "previsto".
4. **A cosa serve un file OpenAPI per chi attacca?** Mappa tutti gli endpoint, parametri e schemi, riducendo drasticamente la fase di enumerazione.

## Approfondimento livello esperto

La sicurezza API non è una variante del web testing classico: lo spostamento del confine di fiducia è radicale. In un'app server-rendered il flusso utente limita le richieste possibili; in un'API ogni oggetto, campo e relazione è direttamente raggiungibile. Questo amplifica problemi di autorizzazione (vedi [[BOLA e BFLA]]) perché un endpoint può servire migliaia di oggetti distinti distinguibili solo da un identificatore. La presenza di più formati (JSON, XML, form-encoded) abilita anche attacchi di parser confusion e content-type smuggling per bypassare validazioni che assumono un solo formato. Sul fronte detection/logging, le API generano volumi enormi di traffico uniforme: distinguere un attacco BOLA da uso legittimo richiede correlazione tra identità del chiamante e oggetto richiesto, non solo pattern sulla URL. GraphQL complica ulteriormente perché tutto il traffico passa da un unico endpoint con metodo POST, rendendo inefficaci le regole WAF basate su path: l'analisi va spostata sul contenuto della query (cross-link [[GraphQL Security]]).

## Collegamenti

- [[OWASP API Security Top 10]]
- [[BOLA e BFLA]]
- [[Autenticazione e Autorizzazione API]]
- [[Broken Access Control e IDOR]]
- [[Cookie e JWT]]
- [[GraphQL Security]]
- [[Server-Side Request Forgery (SSRF)]]

## Fonti

- https://owasp.org/API-Security/editions/2023/en/0x00-header/
- https://portswigger.net/web-security/api-testing
- https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/api-testing
