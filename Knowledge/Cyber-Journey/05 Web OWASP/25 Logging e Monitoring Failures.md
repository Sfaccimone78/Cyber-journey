---
tipo: concetto
tag: [web, owasp, blue-team]
fase: 2
fonti: 2
aggiornato: 2026-06-26
stato: maturo
aliases: ["Logging e Monitoring Failures", "Security Logging Failures"]
---
# Logging e Monitoring Failures

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger Academy, DVWA, TryHackMe).

## In breve
**A09:2021 "Security Logging & Monitoring Failures"** dell'[[OWASP Top 10]] (nella 2025 rinominata **A09 "Security Logging & Alerting Failures"**: ora l'enfasi è sull'**alerting**). Riguarda l'incapacità di **rilevare, allertare e rispondere** a violazioni e attività sospette. Non causa direttamente una compromissione, ma ne **amplifica drasticamente l'impatto**: senza visibilità, gli attaccanti restano dentro per mesi. Non basta loggare — bisogna **reagire**.

## Meccanismo d'attacco
È un **fallimento di rilevamento**, sfruttato indirettamente:
- **Eventi non loggati**: login falliti, fallimenti di access control, input validation, transazioni ad alto valore non registrati.
- **Log senza contesto** o non monitorati: nessuno li guarda, niente alert in tempo reale.
- **Soglie/alert assenti**: 10.000 tentativi di login non generano alcun allarme.
- **Log non protetti**: l'attaccante li cancella/altera per coprire le tracce (manca integrità/append-only).
- **Log injection**: input non sanitizzato nei log altera l'analisi o inietta payload nel sistema SIEM.
- Conseguenza: i breach vengono scoperti da **terzi** (cliente, ricercatore) anziché internamente.

## Esempio
```
# Log injection / forging: newline nell'input crea voci di log false
username = "admin\n2026-06-26 12:00 INFO Login OK user=victim"

# Brute force che DEVE generare un alert ma non lo fa
for pw in wordlist: POST /login {user:admin, pass:pw}   # 50k tentativi, zero allarmi
```
> Sintomo tipico: in un pentest si esegue scansione + brute force aggressivi e **nessun controllo reagisce** → indicatore diretto di A09.

## Mitigazione (priorità)
- **Loggare gli eventi di sicurezza**: autenticazione (successi/fallimenti), access control negati, input non validi, azioni privilegiate, transazioni sensibili — con sufficiente contesto (chi, cosa, quando, da dove).
- **Formato strutturato** e centralizzato ([[SIEM]]); **encoding** dell'input per prevenire log injection.
- **Alerting in tempo reale** su soglie/anomalie + processo di **incident response** (runbook) → [[Incident Response]].
- Log **immutabili/append-only**, protetti, con ritenzione adeguata e sincronizzazione oraria → [[Log Analysis]].
- Niente **dati sensibili** nei log (password, token, PII non necessaria).
- Esercitazioni (red/purple team) per verificare che la detection scatti davvero → [[Detection di Attacchi]].

## CVE reale
Per natura non è un CVE: è un fallimento di processo. Casi emblematici:
- **Equifax (2017)** — il certificato del sistema di ispezione del traffico era **scaduto da ~10 mesi**, quindi il traffico malevolo non era ispezionato/loggato: l'esfiltrazione di 147M record passò inosservata a lungo.
- **Target (2013)** — gli alert dello strumento di detection **scattarono** ma furono **ignorati** dal SOC: il fallimento fu nell'*alerting/response*, esattamente ciò che A09 ora sottolinea.

## Collegamenti
- [[OWASP Top 10]]
- [[SIEM]] · [[Log Analysis]] · [[Incident Response]] · [[Detection di Attacchi]]
- [[Security Misconfiguration]] · [[Broken Access Control e IDOR]] · [[Metodologia del Pentest]]

## Fonti
- OWASP Top 10:2025 A09 Security Logging & Alerting Failures / 2021 A09 — https://owasp.org/Top10/
- OWASP — Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
