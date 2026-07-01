---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 2
aggiornato: 2026-06-26
stato: maturo
aliases: ["Insecure Design"]
---
# Insecure Design

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger Academy, DVWA, TryHackMe).

## In breve
**A04:2021** dell'[[OWASP Top 10]] (diventa **A06:2025**). Categoria introdotta nel 2021 per distinguere i difetti di **progettazione** dai difetti di **implementazione**. Un'app può essere codificata perfettamente e restare insicura perché il **design** non prevedeva certi abusi: mancano controlli per intere classi di minacce. *Non si può "patchare" un design assente* — va progettata la sicurezza fin dall'inizio (secure by design).

## Meccanismo d'attacco
Non c'è un singolo payload: è l'**assenza di una contromisura** prevista a livello di logica.
- **Business logic flaws**: il flusso permette abusi non intesi (saltare passi di un checkout, valori negativi che generano rimborsi, race condition su coupon/saldo).
- **Mancanza di rate limiting/anti-automazione** per design (no protezione contro brute force, scraping, abuso API).
- **Trust mal riposto**: fidarsi del client per decisioni di sicurezza (prezzo calcolato lato browser).
- **Recovery flow deboli**: reset password con domande indovinabili, perché il *modello* del flusso è fragile.
- **Mancato threat modeling**: non si è mai chiesto "chi attacca e come" → [[Threat Modeling]].

## Esempio
```http
# Business logic: quantità negativa → il totale diventa un credito
POST /cart/add  {"item":"tv","qty":-5}    →  saldo accreditato

# Race condition su uso singolo (coupon/withdraw) — inviare N richieste in parallelo
# prima che lo stato venga aggiornato (TOCTOU)
```
> Esempio classico (PortSwigger): un negozio applica lo sconto "studente" solo controllando il dominio email lato registrazione; il design non rivalifica al checkout → abuso.

## Mitigazione (priorità)
- **Threat modeling** in fase di design (STRIDE/abuse cases) → [[Threat Modeling]].
- **Secure design patterns** e reference architecture; definire e testare gli **abuse cases**, non solo gli use case.
- Applicare la logica di sicurezza **lato server**, mai fidarsi del client.
- **Rate limiting / anti-automazione** come requisito di progetto.
- Difesa in profondità e **fail securely** (un errore non deve aprire l'accesso).
- Coinvolgere la sicurezza nell'SDLC (shift-left), non come gate finale → [[Secure Coding]].

## CVE reale
Per natura, i difetti di design raramente hanno un CVE puntuale (un CVE è tipicamente un bug d'implementazione). Esempio rappresentativo:
- **Starbucks gift card race condition (bug bounty, 2015)** — trasferire saldo tra carte in parallelo generava denaro dal nulla: difetto di **design** della logica transazionale, non un bug di codice.
- I difetti di logica di **autenticazione MFA bypass** in vari prodotti mostrano lo stesso pattern: l'implementazione è corretta ma il *flusso* progettato è aggirabile.

## Collegamenti
- [[OWASP Top 10]]
- [[Threat Modeling]] · [[Secure Coding]] · [[Broken Access Control e IDOR]] · [[Autenticazione e Gestione Sessioni]] · [[Security Misconfiguration]]

## Fonti
- OWASP Top 10:2025 A06 / 2021 A04 Insecure Design — https://owasp.org/Top10/
- OWASP — Threat Modeling Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
