---
tipo: concetto
tag: [grc]
fase: 2
fonti: 2
aggiornato: 2026-06-28
stato: maturo
aliases: ["NIST CSF e 800-53"]
---

# NIST CSF e 800-53

## In breve

Il **NIST Cybersecurity Framework (CSF)** è un framework volontario, basato sul rischio, che organizza le attività di sicurezza in funzioni di alto livello facili da comunicare anche al business. La versione **2.0 (2024)** ha aggiunto la funzione **Govern**, portando il totale a sei. Mentre il CSF dice *cosa* fare, il **NIST SP 800-53** fornisce il *catalogo dettagliato di controlli* (oltre 1000, in 20 famiglie) usato come riferimento implementativo, in particolare nel mondo federale USA e in FedRAMP.

## Come funziona

Il CSF si articola su tre componenti:

- **Core**: le funzioni → categorie → sottocategorie (outcome misurabili). Le sei funzioni sono:
  - **Govern (GV)** - contesto, ruoli, policy, supply chain risk (novità 2.0).
  - **Identify (ID)** - asset, rischi, dipendenze.
  - **Protect (PR)** - controlli di accesso, formazione, protezione dei dati.
  - **Detect (DE)** - monitoraggio, rilevamento anomalie.
  - **Respond (RS)** - gestione dell'incidente, comunicazione.
  - **Recover (RC)** - ripristino, lezioni apprese.
- **Tiers** (1-4: Partial, Risk Informed, Repeatable, Adaptive): maturità del processo di gestione del rischio.
- **Profiles**: confronto tra *Current Profile* e *Target Profile* per pianificare la remediation.

**SP 800-53** organizza i controlli in famiglie (AC Access Control, AU Audit, IR Incident Response, SC System/Comms, RA Risk Assessment...), con baseline Low/Moderate/High definite in 800-53B. Ogni controllo ha enhancement opzionali.

## Esempi

Le sei funzioni del CSF 2.0 con esempio di outcome:

| Funzione | Codice | Esempio di sottocategoria |
|---|---|---|
| Govern | GV | Definita e comunicata la strategia di risk management |
| Identify | ID | Inventario di hardware e software mantenuto |
| Protect | PR | MFA applicata sugli accessi privilegiati |
| Detect | DE | Eventi di rete monitorati per rilevare anomalie |
| Respond | RS | Piano di risposta eseguito durante un incidente |
| Recover | RC | Sistemi ripristinati dai backup entro l'RTO |

Mapping di una sottocategoria CSF verso famiglie 800-53:

| CSF | Descrizione | Controlli 800-53 |
|---|---|---|
| PR.AA-01 | Gestione identità e credenziali | IA-2, IA-5, AC-2 |
| DE.CM-01 | Monitoraggio continuo della rete | SI-4, AU-6, CA-7 |
| RS.MA-01 | Esecuzione del piano di risposta | IR-4, IR-5, IR-6 |

## Applicazione pratica e difesa

Il flusso tipico: si valuta il *Current Profile* (cosa c'è oggi), si definisce il *Target Profile* (dove arrivare in base al rischio e ai requisiti), si calcola il gap e si prioritizza. Il CSF è ideale come linguaggio comune tra team tecnici e management perché le sei funzioni sono immediatamente comprensibili. Per il difensore, le funzioni Detect/Respond/Recover si traducono direttamente in SOC, [[Incident Response]] e disaster recovery; SP 800-53 fornisce poi la checklist puntuale dei controlli da implementare e auditare. In ambito federale USA, la conformità 800-53 è obbligatoria via FISMA e FedRAMP per i fornitori cloud.

## Lab

- [[TryHackMe]] - percorsi SOC e security management per coprire Detect/Respond.
- NIST CSF 2.0 Reference Tool: navigare il Core online e generare un profilo.
- Esercizio: compilare un mini Current vs Target Profile su 5 sottocategorie e stimare il gap.
- Mappare 3 controlli tecnici già noti (firewall, SIEM, MFA) verso le famiglie 800-53 corrette.

## Domande

1. **Qual è la novità del CSF 2.0?** L'aggiunta della funzione **Govern**, che pone governance e risk management come base trasversale alle altre cinque funzioni.
2. **Differenza tra CSF e 800-53?** Il CSF è un framework di alto livello orientato agli outcome; 800-53 è il catalogo dettagliato dei controlli per realizzarli.
3. **Cosa sono i Tier del CSF?** Quattro livelli di maturità (Partial → Adaptive) del processo di gestione del rischio, non un punteggio di sicurezza.
4. **A cosa servono i Profile?** A confrontare lo stato attuale con quello desiderato e pianificare la remediation prioritizzata.
5. **Cos'è una baseline in 800-53?** Un set predefinito di controlli (Low/Moderate/High) calibrato sull'impatto del sistema secondo FIPS 199.

## Approfondimento livello esperto

CSF e ISO 27001 sono complementari: il CSF eccelle nella comunicazione e nella valutazione di maturità, ISO 27001 nella certificabilità e nella formalità del sistema di gestione. NIST pubblica mapping ufficiali CSF ↔ 800-53 ↔ ISO 27001, sfruttabili per il *comply once, report many*. Differenza concettuale chiave: il CSF è **outcome-based** (descrive risultati attesi senza prescrivere il come), mentre 800-53 è **control-based** (prescrive controlli specifici e verificabili). Per il risk quantification, il CSF si integra con **SP 800-30** (risk assessment) e **800-37** (Risk Management Framework, il processo Categorize-Select-Implement-Assess-Authorize-Monitor alla base dell'autorizzazione dei sistemi federali). La funzione Govern del 2.0 ha inoltre formalizzato il **C-SCRM** (Cyber Supply Chain Risk Management), collegando il framework alle tematiche di supply chain security.

## Collegamenti

- [[Fondamenti GRC]]
- [[ISO 27001 e ISMS]]
- [[Risk Management e Quantificazione]]
- [[Audit e Framework (SOC 2, PCI-DSS)]]
- [[Penetration Testing]]

## Fonti

- https://www.nist.gov/cyberframework - NIST Cybersecurity Framework 2.0, risorse ufficiali.
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final - NIST SP 800-53 Rev. 5, catalogo dei controlli.
