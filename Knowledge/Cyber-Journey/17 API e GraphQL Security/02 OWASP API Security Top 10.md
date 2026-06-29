---
tipo: concetto
tag: [api]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["OWASP API Security Top 10"]
---

# OWASP API Security Top 10

## In breve

L'OWASP API Security Top 10 è la classifica di riferimento dei rischi specifici delle API, distinta dall'OWASP Top 10 web generale ([[OWASP Top 10]]). L'edizione 2023 mette in cima i problemi di autorizzazione (BOLA al primo posto, BFLA al quinto), riflettendo il fatto che la stragrande maggioranza delle vulnerabilità API non riguarda l'iniezione ma il controllo degli accessi a livello di oggetto e di funzione. Conoscere questa lista a memoria orienta sia il threat modeling sia il testing.

## Come funziona

Le dieci categorie dell'edizione 2023:

- **API1 - Broken Object Level Authorization (BOLA)**: l'API non verifica che l'utente possa accedere allo specifico oggetto richiesto via `id`. Vedi [[BOLA e BFLA]].
- **API2 - Broken Authentication**: gestione difettosa di token, login, refresh, JWT. Vedi [[Autenticazione e Autorizzazione API]].
- **API3 - Broken Object Property Level Authorization**: fusione di mass assignment (scrittura di proprietà non autorizzate) ed excessive data exposure (lettura di campi sensibili non filtrati).
- **API4 - Unrestricted Resource Consumption**: assenza di rate limiting e quota, che porta a DoS e costi (es. invio massivo di OTP). Vedi [[Mass Assignment, SSRF e Rate Limiting API]].
- **API5 - Broken Function Level Authorization (BFLA)**: un utente normale invoca funzioni amministrative. Vedi [[BOLA e BFLA]].
- **API6 - Unrestricted Access to Sensitive Business Flows**: abuso automatizzato di flussi di business (acquisto biglietti, scalping).
- **API7 - Server-Side Request Forgery (SSRF)**: l'API recupera una URL fornita dall'utente. Vedi [[Server-Side Request Forgery (SSRF)]].
- **API8 - Security Misconfiguration**: header mancanti, CORS permissivo, verbi non gestiti, debug attivo.
- **API9 - Improper Inventory Management**: shadow/zombie API, versioni vecchie e ambienti non documentati.
- **API10 - Unsafe Consumption of APIs**: fiducia cieca nei dati provenienti da API di terze parti.

## Esempi

Excessive data exposure (API3): la risposta contiene campi sensibili che il client dovrebbe filtrare ma che vengono serializzati interi.

```bash
curl -s "https://target.tld/api/v1/users/42" -H "Authorization: Bearer $TOKEN"
# Risposta che espone troppo:
# {"id":42,"name":"Ada","email":"ada@x.tld","password_hash":"$2b$...","is_admin":false,"ssn":"..."}
```

Security misconfiguration (API8) - CORS permissivo che riflette qualsiasi Origin:

```bash
curl -s -I "https://target.tld/api/v1/me" \
  -H "Origin: https://evil.tld" -H "Authorization: Bearer $TOKEN"
# Access-Control-Allow-Origin: https://evil.tld
# Access-Control-Allow-Credentials: true   <-- combinazione pericolosa
```

Improper inventory (API9) - probing di versioni e ambienti con ffuf:

```bash
ffuf -u "https://target.tld/api/FUZZ/users/1" \
  -w <(printf 'v1\nv2\nv3\nbeta\ninternal\n') \
  -H "Authorization: Bearer $TOKEN" -mc 200,403
```

In Burp si usa l'estensione/scan passivo per individuare misconfigurazioni e si confrontano le risposte tra versioni diverse dell'API nel Repeater.

## Mitigazione e difesa

- Implementare controlli di autorizzazione **object-level e function-level** centralizzati, non sparsi per ogni controller.
- Filtrare le risposte con DTO/serializer espliciti (allowlist di campi), mai serializzare l'intero modello ORM.
- Applicare rate limiting, quota e throttling per IP, utente e flusso di business.
- Configurare CORS in modo restrittivo (Origin esplicite, no wildcard con credentials).
- Mantenere un inventario API aggiornato e ritirare endpoint legacy.
- Validare e sanificare i dati ricevuti anche da API di terze parti.

## Lab

- [[PortSwigger Web Academy]] - laboratori su access control e API.
- [[TryHackMe]] - room dedicate all'OWASP API Top 10.
- [[HackTheBox]] - challenge web/API.
- crAPI copre quasi tutte le categorie della Top 10 in scenari realistici.
- VAmPI per esercizi su BOLA, broken auth ed excessive exposure.
- OWASP juice-shop per misconfigurazioni e data exposure.

## Domande

1. **Perché OWASP ha una Top 10 separata per le API?** I rischi dominanti (autorizzazione object/function level) sono specifici delle API e poco rappresentati nella Top 10 web generale.
2. **Qual è il rischio numero uno nell'edizione 2023?** API1, Broken Object Level Authorization (BOLA).
3. **Che differenza c'è tra API3 e una semplice SQL injection?** API3 riguarda l'esposizione o la scrittura di proprietà non autorizzate per logica difettosa, non l'iniezione di codice nel data layer.
4. **Cosa distingue API4 da API6?** API4 è consumo non ristretto di risorse tecniche (DoS, costi); API6 è abuso di flussi di business leciti tramite automazione.

## Approfondimento livello esperto

La fusione operata nel 2023 (mass assignment ed excessive data exposure in API3) riconosce che sono due facce dello stesso problema: l'autorizzazione a livello di proprietà dell'oggetto. In lettura, l'over-fetching espone campi sensibili; in scrittura, il mass assignment permette di impostare proprietà privilegiate (cross-link [[Mass Assignment, SSRF e Rate Limiting API]]). Un tester esperto non si ferma al singolo rischio ma costruisce catene: una shadow API (API9) priva di rate limiting (API4) può abilitare credential stuffing (API2), che combinato con BOLA (API1) porta a takeover di massa. Sul fronte difensivo, la lezione strategica è che i controlli vanno centralizzati: la maggior parte delle BOLA nasce da autorizzazione implementata per-endpoint invece che con un policy engine unico. Per il logging, è cruciale registrare la coppia (identità del chiamante, oggetto/funzione richiesta) per poter rilevare pattern di accesso anomali, perché lo status code 200 da solo non distingue l'abuso. GraphQL ricade trasversalmente in API4 (query annidate costose) e API1/API5 a livello di resolver: vedi [[GraphQL Security]].

## Collegamenti

- [[Fondamenti API e REST Security]]
- [[BOLA e BFLA]]
- [[Autenticazione e Autorizzazione API]]
- [[Mass Assignment, SSRF e Rate Limiting API]]
- [[OWASP Top 10]]
- [[Broken Access Control e IDOR]]
- [[Cookie e JWT]]
- [[GraphQL Security]]
- [[Server-Side Request Forgery (SSRF)]]

## Fonti

- https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- https://portswigger.net/web-security/api-testing
- https://salt.security/blog/owasp-api-security-top-10-explained
