---
tipo: concetto
tag: [grc]
fase: 2
fonti: 2
aggiornato: 2026-06-28
stato: maturo
aliases: ["ISO 27001 e ISMS"]
---

# ISO 27001 e ISMS

## In breve

**ISO/IEC 27001** è lo standard internazionale certificabile per l'**ISMS** (Information Security Management System): un sistema di gestione documentato, basato sul rischio, che dimostra come un'organizzazione protegge la riservatezza, l'integrità e la disponibilità delle informazioni. La parte normativa (clausole 4-10) descrive il *sistema di gestione*; l'**Annex A** elenca i controlli di riferimento, dettagliati nella linea guida ISO/IEC 27002. La revisione 2022 ha riorganizzato i controlli in 4 temi e introdotto 11 nuovi controlli.

## Come funziona

L'ISMS segue il ciclo **PDCA** (Plan-Do-Check-Act) ed è strutturato sulle clausole obbligatorie:

- **Clausola 4 - Contesto**: definizione di scope, parti interessate e perimetro dell'ISMS.
- **Clausola 5 - Leadership**: impegno del top management, politica di sicurezza, ruoli.
- **Clausola 6 - Pianificazione**: risk assessment e risk treatment, obiettivi di sicurezza.
- **Clausola 7 - Supporto**: risorse, competenze, awareness, documentazione.
- **Clausola 8 - Operatività**: esecuzione del trattamento del rischio.
- **Clausola 9 - Valutazione**: monitoraggio, internal audit, riesame della direzione.
- **Clausola 10 - Miglioramento**: gestione delle non conformità e azioni correttive.

Documenti chiave: il **Risk Treatment Plan** e soprattutto lo **SoA** (Statement of Applicability), che dichiara per ogni controllo dell'Annex A se è applicabile, se è implementato e con quale giustificazione. La certificazione avviene tramite un ente accreditato in due stadi (Stage 1 documentale, Stage 2 operativo), con audit di sorveglianza annuali e ricertificazione triennale.

## Esempi

Struttura dell'**Annex A (ISO 27001:2022)** - 93 controlli in 4 temi:

| Tema | Codice | N. controlli | Esempi |
|---|---|---|---|
| Organizzativi | A.5 | 37 | Policy, ruoli, supplier, threat intelligence (nuovo) |
| Persone | A.6 | 8 | Screening, awareness, remote working |
| Fisici | A.7 | 14 | Aree sicure, smaltimento media, monitoraggio fisico (nuovo) |
| Tecnologici | A.8 | 34 | Crittografia, logging, secure coding (nuovo), data leakage prevention (nuovo) |

Esempio di voce dello **Statement of Applicability**:

| Controllo | Applicabile | Stato | Giustificazione |
|---|---|---|---|
| A.8.5 Autenticazione sicura | Sì | Implementato | MFA via IdP su tutti gli accessi |
| A.8.24 Uso della crittografia | Sì | Implementato | TLS 1.3 + disk encryption |
| A.7.4 Monitoraggio fisico | No | N/A | Infrastruttura interamente in cloud |

Le sei clausole obbligatorie viste come ciclo PDCA:

| Fase PDCA | Clausole | Output tipico |
|---|---|---|
| Plan | 4, 5, 6 | Scope, policy, risk assessment, SoA |
| Do | 7, 8 | Controlli operativi, awareness, evidenze |
| Check | 9 | Internal audit, KPI, riesame della direzione |
| Act | 10 | Non conformità, azioni correttive |

## Applicazione pratica e difesa

Implementare un ISMS parte da scope e risk assessment, prosegue con la selezione dei controlli (SoA) e la raccolta di evidenze. Per il difensore tecnico, molti controlli Annex A mappano direttamente su attività note: A.8.8 (gestione vulnerabilità) implica un programma di vulnerability management e [[Penetration Testing]] periodici; A.8.16 (monitoraggio) implica SIEM e detection. L'auditor verifica non l'esistenza di un tool ma l'esistenza di un *processo documentato, eseguito e migliorato*. Errore tipico: comprare strumenti senza policy e senza evidenza di funzionamento.

## Lab

- [[TryHackMe]] - moduli di security management e governance utili a contestualizzare i controlli.
- ISO 27001 Toolkit: scaricare un template gratuito di SoA e compilarlo per un'azienda fittizia.
- Esercizio: mappare i 4 temi dell'Annex A 2022 e identificare 5 controlli "nuovi" rispetto al 2013.
- Redigere un mini risk treatment plan per 3 rischi e collegarvi i controlli Annex A pertinenti.

## Domande

1. **Differenza tra ISO 27001 e ISO 27002?** La 27001 è lo standard certificabile con i requisiti dell'ISMS; la 27002 è la linea guida di dettaglio sull'implementazione dei controlli.
2. **Cos'è lo Statement of Applicability?** Documento che dichiara quali controlli Annex A sono applicabili, il loro stato e la giustificazione di inclusione o esclusione.
3. **Cosa cambia nella revisione 2022?** 93 controlli (da 114) riorganizzati in 4 temi, con 11 nuovi controlli (es. threat intelligence, secure coding, DLP).
4. **Cos'è il ciclo PDCA nell'ISMS?** Plan-Do-Check-Act: il modello di miglioramento continuo su cui si fonda il sistema di gestione.
5. **Quanto dura la certificazione?** Il certificato vale 3 anni, con audit di sorveglianza annuali e ricertificazione completa al termine.

## Approfondimento livello esperto

ISO 27001 è uno standard *di sistema*, non *di controlli*: la certificazione attesta che esiste un sistema di gestione funzionante, non che l'azienda è "sicura". Questo la distingue da SOC 2, che attesta l'efficacia operativa di specifici controlli su un periodo. Il mapping pratico più richiesto è **ISO 27001 ↔ NIST CSF ↔ SOC 2**: l'Annex A copre quasi tutte le funzioni del CSF e la maggior parte dei Trust Services Criteria, permettendo a un'azienda di soddisfare più framework con un solo set di controlli (*comply once, report many*). La famiglia 27000 si estende con standard settoriali: **27017** (cloud), **27018** (PII in cloud), **27701** (privacy / PIMS, estensione per GDPR), **27005** (risk management). Punto critico negli audit: l'esclusione di controlli nello SoA deve essere giustificata dal contesto, non dalla convenienza, altrimenti diventa una non conformità.

## Collegamenti

- [[Fondamenti GRC]]
- [[NIST CSF e 800-53]]
- [[Risk Management e Quantificazione]]
- [[Audit e Framework (SOC 2, PCI-DSS)]]
- [[Penetration Testing]]

## Fonti

- https://www.iso.org/standard/27001 - ISO/IEC 27001:2022, pagina ufficiale dello standard.
- https://www.iso.org/standard/75652.html - ISO/IEC 27002:2022, linea guida sui controlli.
