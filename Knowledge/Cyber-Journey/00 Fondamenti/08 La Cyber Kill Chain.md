---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 2
aggiornato: 2026-07-02
stato: maturo
aliases: ["La Cyber Kill Chain"]
---
# La Cyber Kill Chain

## In breve
La **Cyber Kill Chain** (Lockheed Martin, 2011) modella un attacco come una **sequenza di 7 fasi**
dipendenti l'una dall'altra. L'idea operativa è una sola e potente: l'attaccante deve completarle
*tutte*; al difensore basta **spezzare un anello** per far fallire l'intera catena. Più presto lo
spezzi, meno costa.

## Le 7 fasi — meccanismo e contromisura
Per ogni fase serve sapere *cosa fa l'attaccante* e *come ci si difende* (il modello difensivo è la
matrice **Detect / Deny / Disrupt / Degrade / Deceive / Destroy**):

1. **Reconnaissance** — raccolta info sul bersaglio: domini, email, IP, tecnologie, dipendenti
   ([[OSINT]], [[Ricognizione (Recon)]]). *Difesa:* ridurre l'esposizione pubblica, monitorare scansioni.
2. **Weaponization** — accoppia un exploit a un payload (es. PDF/macro + RAT). Avviene **dal lato
   attaccante**, quindi non osservabile: ci si prepara con [[Threat Intelligence]] sui TTP noti.
3. **Delivery** — consegna il payload: phishing ([[Social Engineering e Phishing]]), sito malevolo,
   USB, exploit di un servizio esposto. *Difesa:* filtri mail (DMARC/DKIM/SPF), proxy, awareness.
4. **Exploitation** — il payload attiva la [[Vulnerabilità Exploit e Minaccia|vulnerabilità]] ed esegue
   codice. *Difesa:* patching, hardening, EDR comportamentale ([[EDR e XDR]]), sandbox.
5. **Installation** — persistenza: backdoor, servizio, chiave di run, task pianificato. *Difesa:*
   [[Sysmon]] + [[MITRE ATT&CK|ATT&CK]] per rilevare creazione processi/servizi anomali.
6. **Command & Control (C2)** — il sistema compromesso chiama "casa" per ricevere comandi (HTTP/S,
   DNS, beacon di [[Reverse Shell e Bind Shell|reverse shell]] o framework C2 come Cobalt Strike).
   *Difesa:* analisi traffico in uscita, threat feed di domini/IP malevoli, beacon detection.
7. **Actions on Objectives** — l'obiettivo finale: esfiltrazione, cifratura ransomware, sabotaggio,
   [[Lateral Movement|movimento laterale]] verso altri sistemi. *Difesa:* DLP, segmentazione,
   [[Incident Response]].

## Perché la posizione conta: l'economia della difesa
Bloccare in **Delivery** costa un filtro mail; bloccare in **Actions on Objectives** significa che i
dati sono già usciti. Spostare la detection "a sinistra" nella catena è il principio guida del Blue
Team. Una singola difesa per fase crea **ridondanza** — è la [[Difesa in Profondità]] applicata alla
timeline dell'attacco.

## Limiti del modello (e cosa usare al suo posto)
La Kill Chain è nata per attacchi **malware perimetrali** e mostra i suoi anni:

- **Perimetro-centrica:** assume "fuori vs dentro". Inutile contro insider o credenziali rubate che
  *entrano dalla porta principale* senza exploit.
- **Lineare:** un'intrusione reale itera (recon interno → nuovo movimento laterale → nuova persistenza),
  non procede dritta una volta sola.
- **Vaga sul "dopo":** comprime tutto il post-compromise in un'unica fase 7.

Modelli complementari:
- **[[MITRE ATT&CK]]** — non fasi astratte ma un catalogo granulare di **tecniche reali** osservate in
  the wild (es. T1059 = Command Scripting). Si usa per detection e threat hunting concreti.
- **Unified Kill Chain** (Pols, 2017) — 18 fasi che fondono Kill Chain + ATT&CK e modellano l'**interno**
  (lateral movement, pivoting, persistenza ripetuta).

> In pratica: **Kill Chain** per spiegare *la storia* di un attacco e dove tagliarlo; **ATT&CK** per
> costruire *detection e regole* concrete.

## Esempio
Recon: trovata l'email del CFO via LinkedIn. Weaponization: Excel con macro + RAT. Delivery: email
mirata (spear phishing). Exploitation: la vittima abilita le macro. Installation: il RAT crea una
chiave di persistenza. C2: il PC chiama il server dell'attaccante. Objectives: esfiltrazione dei dati
finanziari. Un EDR che blocca l'esecuzione della macro (fase 4) avrebbe fermato tutto il resto.

## Lab
- **[[TryHackMe]]** → room *Cyber Kill Chain* e *Unified Kill Chain*: mappa le fasi di un attacco simulato dalla ricognizione alle actions on objectives.
- **[[TryHackMe]]** → room *MITRE* / uso del *ATT&CK Navigator*: traduci le fasi astratte della Kill Chain in tecniche ATT&CK concrete (es. T1059) su cui costruire detection.
- Esercizio: prendi il report di una campagna reale (es. un writeup di ransomware) e colloca ogni azione nelle 7 fasi, indicando in quale fase la detection sarebbe costata di meno.

## Domande
1. **D:** Qual è l'idea operativa centrale della Kill Chain per il difensore? **R:** L'attaccante deve completare *tutte* le fasi; al difensore basta spezzare *un* anello per far fallire l'intera catena, e prima lo spezza meno costa.
2. **D:** Perché la fase di Weaponization non è direttamente osservabile? **R:** Perché avviene dal lato attaccante (accoppiamento exploit+payload); ci si prepara con la Threat Intelligence sui TTP noti.
3. **D:** Cosa significa "spostare la detection a sinistra" e perché conta? **R:** Rilevare l'attacco nelle fasi iniziali (es. Delivery, un filtro mail) costa molto meno che nella fase 7, quando i dati sono già usciti.
4. **D:** Quali sono i principali limiti della Kill Chain? **R:** È perimetro-centrica (inutile contro insider/credenziali rubate), lineare (un'intrusione reale itera) e vaga sul post-compromise (tutto compresso nella fase 7).
5. **D:** Quando usare Kill Chain e quando MITRE ATT&CK? **R:** La Kill Chain per raccontare *la storia* di un attacco e dove tagliarlo; ATT&CK per costruire *detection e regole* concrete basate su tecniche reali.

## Collegamenti
- [[MITRE ATT&CK]] · [[Difesa in Profondità]] · [[Social Engineering e Phishing]] · [[Threat Intelligence]]
- Fasi correlate: [[Ricognizione (Recon)]] · [[Reverse Shell e Bind Shell]] · [[Lateral Movement]] · [[Incident Response]]

## Fonti
- Lockheed Martin, *Intelligence-Driven Computer Network Defense* (Cyber Kill Chain, 2011).
- MITRE ATT&CK (attack.mitre.org) · Paul Pols, *The Unified Kill Chain* (2017).
