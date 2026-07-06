---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 2
aggiornato: 2026-07-02
stato: maturo
aliases: ["Difesa in Profondità"]
---
# Difesa in Profondità

## In breve
La **difesa in profondità** (defense in depth) è la strategia di sovrapporre **più controlli
indipendenti**, così che il fallimento di uno non comprometta l'intero sistema. Il presupposto è
realistico e severo: *nessun singolo controllo è infallibile*. Si progetta quindi perché l'attaccante
debba bucarne **molti in sequenza**, pagando tempo e rumore a ogni strato — tempo che il difensore usa
per rilevare e rispondere.

## Tre tipi di controllo (la tassonomia che conta)
Ogni strato dovrebbe combinare controlli di natura diversa — è qui che molti modelli "a cipolla"
falliscono, mettendo solo barriere preventive:

- **Preventivi** — *impediscono* l'attacco: firewall, MFA, cifratura, hardening, minimo privilegio.
- **Detettivi** — *rilevano* ciò che è passato: [[SIEM]], [[Log Analysis]], IDS, [[Sysmon]], EDR.
- **Correttivi/Reattivi** — *limitano il danno e ripristinano*: [[Incident Response]], backup,
  isolamento dell'host, rollback.

> Errore classico: puntare tutto sulla prevenzione. Se manca il livello detettivo, un attaccante che
> supera il perimetro resta **invisibile per mesi** (dwell time). Prevenire + rilevare + reagire.

## Gli strati, dall'esterno verso il dato
1. **Perimetro di rete** — firewall, IDS/IPS filtrano il traffico esterno.
2. **Segmentazione interna** — VLAN/subnet isolano i sistemi: contiene il
   [[Lateral Movement|movimento laterale]] e il [[Pivoting]] dopo un'intrusione.
3. **Endpoint / Sistema operativo** — patch, hardening, minimo privilegio, EDR ([[EDR e XDR]]).
4. **Applicazioni** — autenticazione robusta, validazione input → niente [[SQL Injection]] o
   [[Cross-Site Scripting (XSS)]].
5. **Dati** — cifratura a riposo e in transito ([[Triade CIA]]), classificazione, DLP.
6. **Identità e accesso** — MFA, RBAC, gestione delle credenziali ([[IAM e Zero Trust]]).
7. **Persone** — formazione e simulazioni anti-[[Social Engineering e Phishing|phishing]].
8. **Monitoraggio trasversale** — [[SIEM]], [[Log Analysis]], [[Incident Response]] osservano *tutti*
   gli strati.

## Defense in Depth vs Zero Trust — non sono opposti
- **Defense in Depth (classico)** — più anelli intorno a un perimetro; modello "fortezza", implicita
  fiducia *dentro* la rete.
- **Zero Trust** — supera proprio quella fiducia implicita: *"never trust, always verify"*, ogni
  richiesta autenticata e autorizzata indipendentemente dalla posizione (vedi [[IAM e Zero Trust]]).
- Convivono: Zero Trust è *come* si implementano gli strati di identità/rete in un'architettura DiD
  moderna, dove il perimetro non esiste più (cloud, remote work).

**Assume breach** è la mentalità che lega tutto: progettare *partendo dal presupposto* che l'attaccante
sia già dentro. Da qui segmentazione, minimo privilegio e monitoraggio diventano obbligatori, non
opzionali.

## Esempio — gli strati che lavorano
Un attaccante supera il firewall via una porta esposta (strato 1 bucato). Trova la rete **segmentata**
(2) → non raggiunge i server critici. Le **credenziali non sono riusabili** (6) → niente movimento
laterale. Il **SIEM** lancia un alert sul comportamento anomalo (8) → il SOC isola l'host (correttivo)
prima dell'esfiltrazione. Nessuno strato da solo avrebbe fermato l'attacco; insieme sì.

## Perché conta
La difesa in profondità trasforma una *singola* vulnerabilità da "game over" a "incidente gestibile".
È il principio operativo del Blue Team e il contraltare difensivo della [[La Cyber Kill Chain]]
(spezzare l'anello a più fasi possibili) e della [[Superficie di Attacco]] (ridurre + presidiare ciò
che resta).

## Lab
- **[[TryHackMe]]** → room *Defensive Security Intro* e *Security Principles*: identifica, in uno scenario, quali controlli sono preventivi, detettivi e correttivi.
- **[[TryHackMe]]** → percorso *SOC Level 1* (SIEM, log analysis): pratica il livello *detettivo* di questa nota, quello che spesso manca nei modelli "solo prevenzione".
- Esercizio di progettazione: per un'app web esposta, disegna gli 8 strati (perimetro → dati → identità → persone → monitoraggio) e assegna ad ognuno almeno un controllo preventivo E uno detettivo.

## Domande
1. **D:** Qual è il presupposto alla base della difesa in profondità? **R:** Che *nessun singolo controllo è infallibile*: si sovrappongono più controlli indipendenti così che il fallimento di uno non comprometta l'intero sistema.
2. **D:** Quali sono i tre tipi di controllo e cosa fa ciascuno? **R:** Preventivi (impediscono l'attacco: firewall, MFA, cifratura), detettivi (rilevano ciò che è passato: SIEM, IDS, EDR) e correttivi/reattivi (limitano il danno e ripristinano: IR, backup, isolamento).
3. **D:** Qual è l'errore classico nell'applicare la difesa in profondità? **R:** Puntare tutto sulla prevenzione: senza il livello detettivo un attaccante che supera il perimetro resta invisibile per mesi (dwell time).
4. **D:** Defense in Depth e Zero Trust sono opposti? **R:** No: Zero Trust supera la fiducia implicita "dentro la rete" ed è il *modo* con cui si implementano gli strati di identità/rete in un'architettura DiD moderna senza perimetro.
5. **D:** Cosa significa la mentalità "assume breach"? **R:** Progettare partendo dal presupposto che l'attaccante sia già dentro, rendendo obbligatori (non opzionali) segmentazione, minimo privilegio e monitoraggio.

## Collegamenti
- [[Superficie di Attacco]] · [[La Cyber Kill Chain]] · [[IAM e Zero Trust]] · [[Triade CIA]]
- Strati: [[SIEM]] · [[Log Analysis]] · [[Incident Response]] · [[EDR e XDR]] · [[Sysmon]] · [[Pentester vs SOC]]

## Fonti
- NIST SP 800-53 — Security and Privacy Controls (control families).
- NSA — Defense in Depth · NIST SP 800-207 (Zero Trust Architecture).
