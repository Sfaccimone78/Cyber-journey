---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 2
aggiornato: 2026-07-02
stato: maturo
aliases: ["Threat Modeling"]
---
# Threat Modeling

## In breve
Il **threat modeling** è il processo strutturato di **identificare, enumerare e prioritizzare le minacce** a un sistema, per progettare difese mirate. Risponde a quattro domande (Shostack): *Cosa stiamo costruendo? Cosa può andare storto? Cosa facciamo a riguardo? Abbiamo fatto un buon lavoro?* Senza un modello di minaccia, le contromisure sono arbitrarie. È l'attività che evita l'[[Insecure Design]] perché applica la sicurezza in fase di **design**.

## I metodi

### STRIDE — categorizzare le minacce
Sviluppato da Microsoft, mappa 6 categorie di minaccia, ciascuna negazione di una proprietà di sicurezza (vedi [[Triade CIA]]):

| Lettera | Minaccia | Proprietà violata |
|---|---|---|
| **S** | Spoofing (impersonare) | Autenticazione |
| **T** | Tampering (alterare dati) | Integrità |
| **R** | Repudiation (negare azioni) | Non-ripudio |
| **I** | Information disclosure | Confidenzialità |
| **D** | Denial of Service | Disponibilità |
| **E** | Elevation of Privilege | Autorizzazione |

### DREAD — stimare il rischio
Punteggio su 5 fattori: **D**amage, **R**eproducibility, **E**xploitability, **A**ffected users, **D**iscoverability. Si assegna un valore (es. 1-10) per ordinare le minacce per priorità. *Criticato per soggettività* — utile come euristica, non come misura esatta. Vedi anche [[Risk Management e Compliance]].

### Attack Trees
Rappresentazione **gerarchica**: la radice è l'obiettivo dell'attaccante (es. "leggere i fondi del conto"); i figli sono i sotto-obiettivi/metodi (OR/AND). Le foglie sono attacchi concreti, annotabili con costo/probabilità → si trova il **percorso più economico** per l'attaccante. Concetto reso popolare da Schneier.

## Esempio applicato
Per una web app con login:
- **STRIDE** sul flusso di autenticazione: *S* → credential stuffing ([[Autenticazione e Gestione Sessioni]]); *I* → leak token via [[Cross-Site Scripting (XSS)]]; *E* → IDOR ([[Broken Access Control e IDOR]]).
- **Attack tree** "compromettere account admin": (rubare cookie via XSS) OR (brute force senza rate limit) OR (phishing → [[Social Engineering e Phishing]]).
- **DREAD** prioritizza: il phishing ha alta reproducibility + affected users → si affronta per primo con MFA.

Si usa in fase di **design** per evitare l'[[Insecure Design]]. Strumenti: data flow diagram + trust boundary; tool come OWASP Threat Dragon.

## Lab
- **OWASP Threat Dragon** (tool gratuito): disegna il data flow diagram di una web app con login, traccia i *trust boundary* e applica STRIDE a ogni flusso.
- **Microsoft Threat Modeling Tool**: modella lo stesso sistema e genera automaticamente le minacce STRIDE per confronto.
- **Esercizio Attack Tree**: prendi l'obiettivo "compromettere account admin" e costruisci l'albero con nodi OR/AND (XSS → furto cookie, brute force, phishing), annotando costo/probabilità per trovare il percorso più economico.

## Domande
1. **D:** A quali quattro domande (Shostack) risponde il threat modeling? **R:** Cosa stiamo costruendo? Cosa può andare storto? Cosa facciamo a riguardo? Abbiamo fatto un buon lavoro?
2. **D:** Cosa rappresentano le lettere di STRIDE e quali proprietà negano? **R:** Spoofing (autenticazione), Tampering (integrità), Repudiation (non-ripudio), Information disclosure (confidenzialità), Denial of Service (disponibilità), Elevation of Privilege (autorizzazione).
3. **D:** Su quali 5 fattori si basa DREAD e qual è il suo limite? **R:** Damage, Reproducibility, Exploitability, Affected users, Discoverability; il limite è la soggettività (utile come euristica, non come misura esatta).
4. **D:** Cos'è un attack tree e cosa permette di individuare? **R:** Una rappresentazione gerarchica con l'obiettivo dell'attaccante alla radice e attacchi concreti alle foglie (nodi OR/AND); annotando costo/probabilità permette di trovare il percorso più economico per l'attaccante.
5. **D:** In quale fase del ciclo di vita si applica il threat modeling e cosa previene? **R:** In fase di *design*, per evitare l'Insecure Design applicando la sicurezza prima di scrivere il codice.

## Collegamenti
- [[Insecure Design]] · [[Triade CIA]] · [[Secure Coding]] · [[Metodologia del Pentest]] · [[Risk Management e Compliance]]
- [[Vulnerabilità Exploit e Minaccia]] · [[Superficie di Attacco]]

## Fonti
- Anderson, *Security Engineering*, cap. 1-2 — https://www.cl.cam.ac.uk/~rja14/book.html
- OWASP Threat Modeling — https://owasp.org/www-community/Threat_Modeling
