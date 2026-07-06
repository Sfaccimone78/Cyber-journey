---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Broken Access Control e IDOR", "Broken Access Control", "IDOR"]
---

# Broken Access Control e IDOR

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger Academy, DVWA, TryHackMe).

## In breve
Il **Broken Access Control** è la categoria **A01** dell'[[OWASP Top 10]] 2021 — la più diffusa, **confermata #1 anche nella bozza 2025**, dove **ingloba la [[Server-Side Request Forgery (SSRF)]]** come sotto-caso. Si verifica quando l'app non verifica se l'utente **ha il permesso** di compiere un'azione o accedere a una risorsa. L'**IDOR** (Insecure Direct Object Reference) è la forma più comune: un riferimento diretto a un oggetto (ID, filename) senza controllo di proprietà.

## Authentication ≠ Authorization
- **Authentication**: *chi sei?* (login) → vedi [[Autenticazione e Gestione Sessioni]].
- **Authorization** (access control): *cosa puoi fare?*
Il Broken Access Control è un fallimento della **seconda**: l'utente è autenticato correttamente, ma il server non controlla i suoi **permessi** sulla risorsa richiesta.

## Tipi
- **IDOR / orizzontale**: accedi ai dati di un altro utente con lo stesso ruolo (cambi l'ID).
- **Verticale**: utente normale raggiunge funzioni admin.
- **Context-dependent**: salti passi di un workflow (es. checkout senza pagamento).
- **Path traversal / forced browsing**: uscire dalla directory consentita per leggere file arbitrari (`?file=../../../../etc/passwd`).

## Esempi pratici
IDOR — cambio dell'identificatore:
```http
GET /api/conti/12345/transazioni      Authorization: Bearer <token_A>
GET /api/conti/12346/transazioni      Authorization: Bearer <token_A>   ← dati di B?
```
Escalation verticale — forced browsing:
```http
GET /admin/elimina-utente?id=99       (utente normale → 200 invece di 403?)
```
Altri pattern:
- **Parameter tampering**: `role=user` → `role=admin` nel body/cookie/JWT.
- **Method override**: `GET` bloccato ma `POST`/`PUT` no; o header `X-Original-URL`.
- **Mass assignment**: invii campi extra (`"isAdmin":true`) che il backend lega ciecamente.

## Come si testa
Con due account (A e B) e [[Burp Suite]]: catturi una richiesta di A, la **ripeti col token di B** (o senza token) e osservi se l'accesso passa. Estensione **Autorize** automatizza il confronto. Enumeri ID con Intruder.

## Mitigazione (priorità)
1. **Deny-by-default**: nega salvo permesso esplicito; controllo **server-side su ogni richiesta**.
2. Verifica di **ownership**: la risorsa appartiene davvero all'utente del token? Non fidarsi mai dell'ID dal client.
3. **RBAC/ABAC** centralizzato, non controlli sparsi per endpoint.
4. Riferimenti **indiretti**/UUID non enumerabili (mitigazione, non sostituto del controllo).
5. **Loggare** i tentativi negati → tie-in [[Incident Response]], [[Logging e Monitoring Failures]].

## CVE reale
- **CVE-2019-11510** (Pulse Secure VPN) — path traversal che legge file arbitrari, classica falla di access control sfruttata massivamente per furto credenziali.
- **CVE-2023-22515** (Atlassian Confluence) — broken access control che consente la creazione di account admin (privilege escalation).
- **CVE-2021-22205** (GitLab) — catena che include bypass di access control non autenticato.

## Lab
- **[[PortSwigger Web Academy]]** — categoria *Access control vulnerabilities*: parti dai lab APPRENTICE (IDOR su parametro `id`, admin panel via forced browsing/URL predicibile), poi PRACTITIONER (privilege escalation orizzontale/verticale, parameter tampering su `roleid`, `X-Original-URL`/method override, GraphQL/multi-step). Pratica il flusso "cattura richiesta di A → rigioca col token di B".
- **DVWA** — modulo *Insecure Direct Object Reference* e le pagine admin-only per esercitare orizzontale e verticale (low→high).
- **TryHackMe** — room *IDOR* e la sezione *Broken Access Control* di *OWASP Top 10 (2021)*: enumerazione di ID e forced browsing guidati.

## Domande
1. **D:** Qual è la differenza tra IDOR orizzontale e verticale? **R:** Orizzontale = accedi ai dati di un altro utente con lo **stesso** ruolo cambiando l'identificatore; verticale = un utente normale raggiunge funzioni riservate a un ruolo superiore (es. admin).
2. **D:** Perché usare UUID non enumerabili non è una difesa sufficiente? **R:** Rende più difficile *indovinare* il riferimento, ma non verifica la **proprietà**: senza controllo di ownership server-side, chi conosce/intercetta l'ID accede comunque. È mitigazione, non sostituto del controllo.
3. **D:** Come si testa un IDOR in pratica con Burp? **R:** Con due account A e B: catturi una richiesta di A, la **ripeti col token di B** (o senza token) e osservi se l'accesso passa; l'estensione Autorize automatizza il confronto e Intruder enumera gli ID.
4. **D:** Cos'è il mass assignment e perché è un fallimento di access control? **R:** Il backend lega ciecamente ai campi dell'oggetto tutti i parametri ricevuti: inviando un campo extra come `"isAdmin":true` si scala privilegio perché non c'è controllo su quali attributi l'utente può modificare.
5. **D:** Qual è il principio di mitigazione primario? **R:** **Deny-by-default** con controllo di autorizzazione **server-side su ogni richiesta** e verifica di ownership della risorsa; mai fidarsi dell'ID o del ruolo forniti dal client.

## Collegamenti
- [[OWASP Top 10]]
- [[Autenticazione e Gestione Sessioni]]
- [[Cookie e JWT]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti
- PortSwigger — Access control: https://portswigger.net/web-security/access-control
- OWASP — A01 Broken Access Control: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- OWASP — Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
