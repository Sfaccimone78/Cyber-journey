---
tipo: concetto
tag: [api]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["BOLA e BFLA"]
---

# BOLA e BFLA

## In breve

BOLA (Broken Object Level Authorization) e BFLA (Broken Function Level Authorization) sono le due vulnerabilità di autorizzazione che dominano l'OWASP API Security Top 10 (rispettivamente API1 e API5). BOLA è la versione API dell'IDOR: l'API espone un oggetto identificato da un `id` ma non verifica che il chiamante ne sia il proprietario, permettendo accesso orizzontale ai dati altrui. BFLA riguarda invece le funzioni: un utente con privilegi normali invoca operazioni riservate (tipicamente amministrative), ottenendo un'escalation verticale. Sono distinte ma spesso concatenabili.

## Come funziona

In **BOLA** l'endpoint accetta un identificatore di oggetto (`/api/v1/orders/{id}`, `account_number`, `uuid`) e restituisce o modifica quell'oggetto controllando solo che l'utente sia autenticato, non che sia autorizzato su quello specifico oggetto. Sostituendo l'id con quello di un'altra risorsa si accede ai dati di un altro utente. Gli identificatori sequenziali rendono banale l'enumerazione, ma anche gli UUID sono vulnerabili se trapelano altrove (in altre risposte, log, referer).

In **BFLA** il problema è sul confine di privilegio tra ruoli: l'endpoint amministrativo (`POST /api/v1/admin/users` o `DELETE /api/v1/users/{id}`) non verifica il ruolo del chiamante, oppure lo verifica solo lato UI. Un utente standard che conosce o indovina la route amministrativa (spesso visibile nella documentazione OpenAPI o nel codice JS della SPA) la invoca con successo. BFLA include anche l'uso di un metodo HTTP non previsto (es. `DELETE` dove la UI offre solo `GET`).

La differenza chiave: BOLA è accesso a un **oggetto** che non ti appartiene (stesso livello di privilegio, altro tenant/utente); BFLA è accesso a una **funzione** sopra il tuo livello di privilegio.

## Esempi

BOLA - cambio dell'id per leggere l'ordine di un altro utente:

```http
GET /api/v1/orders/1043 HTTP/1.1
Host: target.tld
Authorization: Bearer <token-utente-A>
```

Risposta 200 con dati dell'utente B: vulnerabilità confermata. Enumerazione automatica con ffuf:

```bash
ffuf -u "https://target.tld/api/v1/orders/FUZZ" \
  -w <(seq 1000 1100) \
  -H "Authorization: Bearer $TOKEN_A" -mc 200 -fr "not found"
```

BOLA su UUID trapelati - estrazione degli id da una risposta lista e replay:

```bash
curl -s "https://target.tld/api/v1/users/me/contacts" -H "Authorization: Bearer $TOKEN_A" \
  | jq -r '.[].user_uuid' \
  | while read u; do
      curl -s -o /dev/null -w "$u %{http_code}\n" \
        "https://target.tld/api/v1/users/$u/private" -H "Authorization: Bearer $TOKEN_A"
    done
```

BFLA - utente normale che invoca una funzione admin:

```http
POST /api/v1/admin/users/42/roles HTTP/1.1
Host: target.tld
Authorization: Bearer <token-utente-standard>
Content-Type: application/json

{"role": "admin"}
```

Se la risposta è 200/201 invece di 403, la BFLA è confermata. In Burp si usa l'estensione **Autorize** per confrontare automaticamente le risposte con token a privilegio diverso (o senza token), evidenziando endpoint che non applicano autorizzazione.

## Mitigazione e difesa

- Verificare l'ownership dell'oggetto **a ogni accesso**, confrontando l'identità nel token con il proprietario della risorsa nel data layer.
- Usare un policy engine centralizzato (es. controlli ABAC/RBAC) invece di check sparsi per controller.
- Preferire identificatori non indovinabili (UUID v4) ma non considerarli una difesa: l'autorizzazione resta obbligatoria.
- Negare di default (deny-by-default) e richiedere ruolo esplicito per ogni funzione sensibile, lato server.
- Non affidarsi a controlli lato client o alla sola assenza del link nella UI.
- Loggare la coppia (chiamante, oggetto/funzione) per rilevare enumerazione e accessi anomali.

## Lab

- [[PortSwigger Web Academy]] - laboratori di access control e IDOR.
- [[TryHackMe]] - room su BOLA/IDOR e API.
- [[HackTheBox]] - macchine con API vulnerabili all'autorizzazione.
- crAPI - scenario BOLA classico sui veicoli/ordini di altri utenti.
- VAmPI - endpoint vulnerabili a BOLA su utenti e libri.
- OWASP juice-shop - sfide di accesso orizzontale e verticale.

## Domande

1. **Qual è la differenza tra BOLA e IDOR?** Concettualmente coincidono; BOLA è il nome usato in ambito API per l'IDOR, ovvero accesso a oggetti altrui per autorizzazione object-level mancante. Vedi [[Broken Access Control e IDOR]].
2. **Gli UUID proteggono da BOLA?** No: rendono più difficile l'enumerazione cieca ma se l'id trapela l'accesso resta possibile; serve sempre il controllo di autorizzazione.
3. **Cosa distingue BFLA da BOLA?** BFLA è escalation verticale (funzioni sopra il proprio privilegio); BOLA è accesso orizzontale a oggetti di pari livello ma altrui.
4. **Perché Autorize è utile?** Riproduce ogni richiesta con un token a privilegio inferiore o nullo e segnala dove l'autorizzazione non è applicata, automatizzando il test su molti endpoint.

## Approfondimento livello esperto

Gli edge case che separano un test superficiale da uno solido: (1) **BOLA in scrittura silente** - un `PATCH /api/v1/orders/{id}` può non restituire i dati dell'oggetto ma accettare comunque la modifica; va testato osservando l'effetto, non solo il body di risposta. (2) **BOLA annidata** - l'id vulnerabile non è nella URL principale ma in un parametro secondario o in un oggetto del JSON body (`{"order_id":...,"shipping_address_id":...}`); il secondo id è spesso privo di controllo. (3) **BFLA via method override** - header come `X-HTTP-Method-Override: DELETE` o il cambio di verbo possono raggiungere handler privilegiati non protetti. (4) **Confine BOLA/BFLA sfumato** - un endpoint admin che accetta anche un object id combina entrambi: prima si bypassa il function-level (BFLA), poi si itera sull'object-level (BOLA) per impatto di massa. (5) **GraphQL** - i controlli di autorizzazione vanno applicati a ogni resolver, non alla query: un singolo campo annidato non protetto replica una BOLA su ogni nodo restituito (cross-link [[GraphQL Security]]). Sul fronte detection, l'enumerazione BOLA produce una firma riconoscibile: un singolo principale che accede in rapida sequenza a molti object id distinti che non possiede - rilevabile solo correlando identità e oggetto, non con regole su path/status.

## Collegamenti

- [[Fondamenti API e REST Security]]
- [[OWASP API Security Top 10]]
- [[Autenticazione e Autorizzazione API]]
- [[Broken Access Control e IDOR]]
- [[Cookie e JWT]]
- [[GraphQL Security]]
- [[Server-Side Request Forgery (SSRF)]]

## Fonti

- https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
- https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/
- https://portswigger.net/web-security/access-control
