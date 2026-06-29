---
tipo: concetto
tag: [grc]
fase: 2
fonti: 2
aggiornato: 2026-06-28
stato: maturo
aliases: ["Audit e Framework (SOC 2, PCI-DSS)"]
---

# Audit e Framework (SOC 2, PCI-DSS)

## In breve

L'**audit** è la verifica indipendente che i controlli di sicurezza esistano e funzionino come dichiarato. Due framework dominano le richieste commerciali: **SOC 2**, attestazione AICPA basata sui *Trust Services Criteria*, molto richiesta da vendor SaaS B2B; e **PCI-DSS**, standard prescrittivo obbligatorio per chiunque tratti dati di carte di pagamento. La distinzione cardine è **certificazione** (conformità a uno standard, es. ISO/PCI) vs **attestazione** (opinione professionale di un revisore sui controlli, es. SOC 2).

## Come funziona

**SOC 2** (System and Organization Controls):

- Basato sui **5 Trust Services Criteria**: *Security* (obbligatorio), *Availability*, *Processing Integrity*, *Confidentiality*, *Privacy*.
- **Type I**: valuta il *design* dei controlli a una data specifica.
- **Type II**: valuta l'*efficacia operativa* su un periodo (tipicamente 3-12 mesi) - quello che i clienti chiedono davvero.
- Eseguito da un **CPA** (revisore contabile abilitato); produce un *report*, non un certificato.

**PCI-DSS** (Payment Card Industry Data Security Standard):

- Standard prescrittivo del PCI Security Standards Council; la **v4.0** è lo stato attuale.
- Organizzato in **12 requisiti** raggruppati in 6 obiettivi (rete sicura, protezione dati cardholder, vulnerability management, controllo accessi, monitoraggio, policy).
- Il livello di obbligo dipende dal **volume di transazioni** (Livelli 1-4): i merchant grandi richiedono audit on-site da un **QSA**, i piccoli un **SAQ** (self-assessment).

Processo di audit generico: definizione scope → raccolta evidenze → test dei controlli → rilievo eccezioni → report con opinione.

## Esempi

I **5 Trust Services Criteria** di SOC 2:

| Criterio | Obbligatorio | Cosa copre |
|---|---|---|
| Security (Common Criteria) | Sì | Protezione contro accessi non autorizzati |
| Availability | No | Uptime, SLA, disaster recovery |
| Processing Integrity | No | Elaborazione completa, accurata, autorizzata |
| Confidentiality | No | Protezione dati riservati (es. business) |
| Privacy | No | Gestione di dati personali (PII) |

I **12 requisiti PCI-DSS** in sintesi:

| # | Requisito |
|---|---|
| 1-2 | Firewall e configurazioni sicure (no default) |
| 3-4 | Proteggere e cifrare i dati delle carte (storage e transito) |
| 5-6 | Anti-malware e sviluppo sicuro |
| 7-8-9 | Controllo accessi logico, autenticazione, accesso fisico |
| 10-11 | Logging/monitoraggio e test di sicurezza (incl. pentest) |
| 12 | Policy di sicurezza delle informazioni |

## Applicazione pratica e difesa

Prepararsi a un audit significa **readiness assessment**, raccolta continua di evidenze e remediation dei gap. Per il difensore tecnico, molti requisiti sono operativi diretti: PCI-DSS Req. 11 impone scansioni di vulnerabilità trimestrali e [[Penetration Testing]] annuali (e dopo modifiche significative); Req. 10 impone logging centralizzato e revisione; SOC 2 Security richiede gestione accessi, change management e [[Incident Response]] documentati. La regola d'oro: l'auditor verifica **evidenze**, non intenzioni - servono log, ticket, report di scansione, registri di accesso. La tokenizzazione dei PAN riduce drasticamente lo scope PCI ("scope reduction").

## Lab

- [[TryHackMe]] - moduli SOC, compliance e security management per il contesto.
- Esercizio: mappare i 12 requisiti PCI-DSS sui controlli ISO 27001 Annex A.
- Compilare un mock SOC 2 readiness checklist sui Common Criteria.
- Simulare la raccolta di evidenze per 5 controlli (screenshot config, export log, ticket).

## Domande

1. **Certificazione vs attestazione?** La certificazione attesta la conformità a uno standard (ISO, PCI); l'attestazione (SOC 2) è l'opinione di un revisore sull'idoneità ed efficacia dei controlli.
2. **SOC 2 Type I vs Type II?** Type I valuta il *design* dei controlli a una data; Type II ne valuta l'*efficacia operativa* su un periodo.
3. **Da cosa dipende il livello PCI-DSS?** Dal volume annuo di transazioni con carta: i livelli 1-4 determinano se serve audit QSA o un self-assessment (SAQ).
4. **Quale Trust Services Criterion è obbligatorio?** Solo *Security* (Common Criteria); gli altri quattro sono opzionali in base al servizio.
5. **Perché ridurre lo scope PCI?** Perché tokenizzando o segmentando i dati di carta si riducono i sistemi soggetti ai 12 requisiti, abbassando costo e rischio dell'audit.

## Approfondimento livello esperto

La differenza **certificazione vs attestazione** ha conseguenze pratiche: ISO 27001 e PCI-DSS producono un certificato verificabile da terzi; SOC 2 produce un report dettagliato (con descrizione dei controlli e risultati dei test) tipicamente coperto da NDA e condiviso solo con clienti e prospect. La convergenza più potente è il **mapping multi-framework**: i controlli ISO 27001, i Trust Services Criteria SOC 2 e i requisiti PCI-DSS si sovrappongono ampiamente, abilitando il *comply once, report many* tramite framework di crosswalk come il **Secure Controls Framework (SCF)**. Differenza di natura: PCI-DSS è **prescrittivo** (dice esattamente cosa fare, es. "ruotare le chiavi"), mentre SOC 2 è **principle-based** (l'azienda definisce i propri controlli e il revisore ne giudica l'adeguatezza rispetto ai criteri). PCI-DSS v4.0 ha introdotto l'approccio **customized** (raggiungere l'obiettivo del controllo con misure alternative, soggette a validazione rigorosa) accanto a quello *defined* tradizionale, avvicinandolo a una logica risk-based. Tema avanzato: i **SOC 2 carve-out vs inclusive method** per i sub-service organization (es. il cloud provider sottostante) determinano cosa rientra nel perimetro del report.

## Collegamenti

- [[Fondamenti GRC]]
- [[ISO 27001 e ISMS]]
- [[NIST CSF e 800-53]]
- [[Risk Management e Quantificazione]]
- [[GDPR Operativo]]
- [[Penetration Testing]]

## Fonti

- https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services - AICPA, suite SOC e Trust Services Criteria.
- https://www.pcisecuritystandards.org/document_library/ - PCI Security Standards Council, libreria documentale PCI-DSS.
