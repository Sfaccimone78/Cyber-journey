---
tipo: concetto
tag: [grc]
fase: 2
fonti: 2
aggiornato: 2026-06-28
stato: maturo
aliases: ["Risk Management e Quantificazione"]
---

# Risk Management e Quantificazione

## In breve

Il **risk management** è il processo che identifica, analizza, valuta e tratta i rischi di sicurezza per mantenerli entro il **risk appetite** dell'organizzazione. L'analisi può essere **qualitativa** (matrici probabilità × impatto, scale alto/medio/basso) o **quantitativa** (valori monetari: SLE, ARO, ALE; modelli probabilistici come **FAIR**). Il prodotto centrale è il **risk register**, e ogni rischio riceve una decisione di trattamento: **mitigare, trasferire, accettare o evitare**.

## Come funziona

Il ciclo (allineato a ISO 31000 e NIST SP 800-30):

1. **Identificazione**: minacce, vulnerabilità e asset → scenari di rischio.
2. **Analisi**: stima di probabilità e impatto (qualitativa o quantitativa).
3. **Valutazione**: confronto del rischio con i criteri di accettazione.
4. **Trattamento**: scelta tra le 4 risposte e selezione dei controlli.
5. **Monitoraggio e riesame**: aggiornamento continuo.

Le quattro risposte al rischio (le "4 T"):

- **Treat / Mitigate**: implementare controlli per ridurre probabilità o impatto.
- **Transfer**: spostare l'impatto a terzi (assicurazione cyber, outsourcing).
- **Accept / Tolerate**: accettare formalmente il rischio residuo se sotto soglia.
- **Avoid / Terminate**: eliminare l'attività che genera il rischio.

Distinzione fondamentale: **rischio inerente** (prima dei controlli) vs **rischio residuo** (dopo i controlli). I controlli non azzerano il rischio: lo riducono a un livello accettabile.

## Esempi

Esempio di **risk register** qualitativo:

| ID | Rischio | Probabilità | Impatto | Livello | Trattamento | Owner |
|---|---|---|---|---|---|---|
| R-01 | Ransomware su file server | Alta | Alto | Critico | Mitigare (backup, EDR) | IT Ops |
| R-02 | Data breach via SQLi | Media | Alto | Alto | Mitigare (WAF, pentest) | AppSec |
| R-03 | Furto laptop non cifrato | Media | Medio | Medio | Mitigare (disk encryption) | IT |
| R-04 | Indisponibilità SaaS terzo | Bassa | Medio | Basso | Trasferire (SLA, polizza) | Procurement |

**Quantificazione monetaria** - formule e calcolo:

- **SLE** (Single Loss Expectancy) = Valore Asset × **EF** (Exposure Factor)
- **ALE** (Annualized Loss Expectancy) = **SLE × ARO** (Annualized Rate of Occurrence)

| Voce | Valore |
|---|---|
| Valore asset (database clienti) | 500.000 € |
| Exposure Factor (EF) | 30% |
| SLE = 500.000 × 0,30 | 150.000 € |
| ARO (eventi/anno attesi) | 0,5 |
| **ALE = 150.000 × 0,5** | **75.000 €/anno** |

Se un controllo costa 20.000 €/anno e riduce l'ARO a 0,1 (nuovo ALE = 15.000 €), il beneficio è 60.000 € a fronte di 20.000 € di costo: **ROSI** positivo, il controllo è giustificato.

## Applicazione pratica e difesa

In pratica si parte da un risk register vivo, aggiornato dopo ogni assessment, [[Penetration Testing]] o incidente. La quantificazione monetaria è ciò che permette al CISO di parlare la lingua del board ("riduciamo l'esposizione attesa di 60k€ con 20k€ di spesa") invece di scale astratte. Il difensore alimenta il processo fornendo dati reali su probabilità (frequenza di attacchi osservati nei log/threat intel) e impatto (criticità degli asset). Attenzione al *risk acceptance*: deve essere una decisione formale, firmata da chi ha l'autorità, non un'omissione.

## Lab

- [[TryHackMe]] - moduli di risk management e security analyst per il contesto operativo.
- Esercizio: costruire un risk register con 8 rischi e classificarli su matrice 5×5.
- Calcolare SLE/ALE/ARO per 3 scenari e valutarne il ROSI di un controllo proposto.
- Simulare un'analisi FAIR semplificata con stime min/mode/max di frequenza e perdita.

## Domande

1. **Differenza tra rischio inerente e residuo?** L'inerente è il rischio prima di qualsiasi controllo; il residuo è ciò che rimane dopo l'applicazione dei controlli.
2. **Cosa misura l'ALE?** La perdita economica attesa su base annua per uno scenario di rischio: ALE = SLE × ARO.
3. **Quali sono le quattro risposte al rischio?** Mitigare, trasferire, accettare, evitare.
4. **Qualitativo vs quantitativo: quando usarli?** Il qualitativo è rapido e comunicativo per il triage; il quantitativo serve a decisioni economiche e prioritizzazione fine.
5. **Cos'è il risk appetite?** La quantità e il tipo di rischio che l'organizzazione è disposta ad accettare per perseguire i propri obiettivi.

## Approfondimento livello esperto

Il limite delle matrici qualitative è la **soggettività**: "alto/medio/basso" non si sommano né si confrontano in modo rigoroso e producono illusione di precisione. **FAIR** (Factor Analysis of Information Risk), standard Open Group, supera questo limite scomponendo il rischio in **LEF** (Loss Event Frequency) e **LM** (Loss Magnitude), a loro volta scomposti in fattori stimabili (Threat Event Frequency, Vulnerability, perdite primarie e secondarie). FAIR usa distribuzioni di probabilità (spesso PERT con stime min/most-likely/max) e simulazione **Monte Carlo** per produrre una curva di perdita annua anziché un numero secco, permettendo affermazioni come "90% di probabilità che la perdita annua sia sotto 200k€". Questo abilita decisioni di portafoglio: confrontare rischi eterogenei sulla stessa scala monetaria e ottimizzare la spesa in controlli. FAIR si integra con NIST 800-30 e alimenta direttamente la cyber insurance, dove l'ALE quantificato determina coperture e premi.

## Collegamenti

- [[Fondamenti GRC]]
- [[ISO 27001 e ISMS]]
- [[NIST CSF e 800-53]]
- [[Audit e Framework (SOC 2, PCI-DSS)]]
- [[Penetration Testing]]

## Fonti

- https://csrc.nist.gov/pubs/sp/800/30/r1/final - NIST SP 800-30 Rev. 1, guida al risk assessment.
- https://www.iso.org/standard/65694.html - ISO 31000:2018, principi e linee guida di risk management.
- https://www.fairinstitute.org/what-is-fair - FAIR Institute, modello di quantificazione del rischio.
