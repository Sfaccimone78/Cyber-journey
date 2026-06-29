---
tipo: concetto
tag: [api]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Mass Assignment, SSRF e Rate Limiting API"]
---

# Mass Assignment, SSRF e Rate Limiting API

## In breve

Questa nota raggruppa tre rischi API molto sfruttati. **Mass assignment** (parte di API3, Broken Object Property Level Authorization) sfrutta il binding automatico del JSON in arrivo sui campi del modello per scrivere proprietà privilegiate non previste. **SSRF** (API7) abusa di endpoint che recuperano una URL fornita dall'utente per colpire risorse interne. **Rate limiting** assente (API4, Unrestricted Resource Consumption) abilita bruteforce, enumerazione, DoS e abuso di flussi costosi. Sono accomunati dal fatto che derivano dalla fiducia eccessiva dell'API nell'input del client.

## Come funziona

**Mass assignment**: framework come Rails, Spring, Laravel o Django spesso mappano automaticamente i campi del JSON ricevuto sugli attributi dell'oggetto. Se l'API non definisce una allowlist dei campi modificabili, il client può aggiungere proprietà come `"is_admin": true`, `"role": "admin"`, `"balance": 999999` o `"verified": true` che vengono persistite. Si scoprono i campi target leggendo una risposta GET (che spesso espone i nomi reali), la documentazione, o per fuzzing dei parametri.

**SSRF nelle API**: endpoint che accettano una URL (webhook, import-from-url, generazione anteprime, fetch di avatar) e la richiedono lato server. L'attaccante punta a `http://169.254.169.254/` (metadata cloud), a servizi interni (`http://localhost:8080/admin`) o usa schemi alternativi (`file://`, `gopher://`). Vedi [[Server-Side Request Forgery (SSRF)]].

**Rate limiting**: senza limiti per utente/IP/flusso, un endpoint di login, OTP o reset password è attaccabile via bruteforce; un endpoint costoso (export, ricerca, query GraphQL annidata) diventa vettore di DoS economico. I bypass comuni dei rate limit deboli sfruttano header come `X-Forwarded-For`, varianti di case nella URL, parametri extra o rotazione di token.

## Esempi

Mass assignment - aggiunta di un campo privilegiato in un PATCH di profilo:

```bash
curl -s -X PATCH "https://target.tld/api/v1/users/me" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"Ada","is_admin":true,"role":"admin"}'
```

Scoperta dei nomi di campo con arjun (parameter discovery):

```bash
arjun -u "https://target.tld/api/v1/users/me" -m JSON \
  --headers "Authorization: Bearer $TOKEN"
```

SSRF tramite endpoint webhook verso i metadata cloud:

```bash
curl -s -X POST "https://target.tld/api/v1/integrations/webhook" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"callback_url":"http://169.254.169.254/latest/meta-data/iam/security-credentials/"}'
```

Test di assenza rate limit su login (bruteforce con ffuf):

```bash
ffuf -u "https://target.tld/api/v1/login" -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"victim@x.tld","password":"FUZZ"}' \
  -w /usr/share/wordlists/rockyou.txt -mc 200 -fc 401,429
```

Tentativo di bypass del rate limit con rotazione di `X-Forwarded-For` (Burp Intruder o ffuf con header dinamico):

```bash
ffuf -u "https://target.tld/api/v1/otp/verify" -X POST \
  -H "X-Forwarded-For: 10.0.0.FUZZ" -H "Content-Type: application/json" \
  -d '{"code":"123456"}' -w <(seq 1 254) -mc 200
```

In Burp si usa Intruder per il bruteforce e per testare il bypass dei limiti variando header e payload; il Repeater per affinare il mass assignment campo per campo.

## Mitigazione e difesa

- Mass assignment: usare allowlist esplicite dei campi bindabili (DTO, strong parameters, serializer dedicati); mai bindare l'intero body sul modello ORM.
- SSRF: validare e normalizzare le URL, allowlist di domini/schemi, bloccare gli indirizzi privati e i metadata endpoint, disabilitare i redirect; vedi [[Server-Side Request Forgery (SSRF)]].
- Rate limiting: applicare limiti per utente, IP e flusso di business; usare 429 con backoff; non fidarsi di header client per identificare l'origine.
- Limitare costo e profondità delle operazioni pesanti (incluse le query GraphQL: cross-link [[GraphQL Security]]).
- Loggare i tentativi anomali e correlare fallimenti ripetuti.

## Lab

- [[PortSwigger Web Academy]] - laboratori su mass assignment, SSRF e business logic.
- [[TryHackMe]] - room su SSRF e API abuse.
- [[HackTheBox]] - macchine con SSRF e binding insicuro.
- crAPI - mass assignment sul saldo/coupon e SSRF reali.
- VAmPI - endpoint con binding e rate limit deboli.
- OWASP juice-shop - sfide di mass assignment e flussi business.

## Domande

1. **Cos'è il mass assignment?** Lo sfruttamento del binding automatico del JSON sui campi del modello per scrivere proprietà privilegiate non previste dall'API.
2. **Come si scoprono i campi target di un mass assignment?** Leggendo la risposta GET dell'oggetto, la documentazione OpenAPI, o facendo fuzzing dei parametri con strumenti come arjun.
3. **Perché gli endpoint webhook/import-url sono a rischio SSRF?** Perché eseguono una richiesta server-side verso una URL controllata dall'utente, raggiungendo risorse interne o metadata cloud.
4. **Quali header si usano per tentare bypass di rate limit?** Tipicamente `X-Forwarded-For`, `X-Real-IP` e simili, oltre a varianti di URL/parametri; ma una difesa robusta non si fida di header client.

## Approfondimento livello esperto

Il **mass assignment chaining** è la tecnica che trasforma un singolo bug in compromissione: si combinano più richieste o si annidano oggetti per raggiungere campi non esposti dall'endpoint diretto. Esempi: (1) impostare `is_admin` durante la **registrazione** (endpoint meno protetto) invece che nell'update profilo; (2) sfruttare oggetti annidati nel body (`{"profile":{"role":"admin"}}`) quando la allowlist copre solo il primo livello; (3) concatenare mass assignment e BOLA - scrivere `owner_id` di un oggetto su un altro utente. Sui **rate limit**, i bypass avanzati sfruttano: race condition (richieste concorrenti che superano il check prima dell'incremento del contatore, rilevanti per OTP e coupon), reset del contatore cambiando un parametro irrilevante che entra nella chiave del rate limiter, e l'uso di endpoint equivalenti non coperti dalla policy. Per **SSRF** in contesto API, i blind SSRF si confermano con un collaborator/canary, e l'impatto massimo è il furto di credenziali IAM dai metadata cloud (IMDSv1); la difesa cloud è imporre IMDSv2 con hop limit. GraphQL amplifica API4: una query profondamente annidata o un batch di alias può moltiplicare il costo di una singola richiesta (introspection e batching abuse: cross-link [[GraphQL Security]]). Sul fronte detection/logging, vanno tracciati i payload con campi inattesi (segnale di mass assignment probing) e le richieste in uscita del server verso IP privati (segnale di SSRF).

## Collegamenti

- [[Fondamenti API e REST Security]]
- [[OWASP API Security Top 10]]
- [[BOLA e BFLA]]
- [[Autenticazione e Autorizzazione API]]
- [[API Testing e Tooling]]
- [[Server-Side Request Forgery (SSRF)]]
- [[GraphQL Security]]
- [[Broken Access Control e IDOR]]
- [[Cookie e JWT]]

## Fonti

- https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/
- https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/
- https://portswigger.net/web-security/ssrf
