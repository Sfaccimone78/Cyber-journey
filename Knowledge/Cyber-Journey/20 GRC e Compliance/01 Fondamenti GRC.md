---
tipo: concetto
tag: [grc]
fase: 2
fonti: 2
aggiornato: 2026-06-28
stato: maturo
aliases: ["Fondamenti GRC"]
---

# Fondamenti GRC

## In breve

GRC è l'acronimo di **Governance, Risk e Compliance**: tre pilastri che insieme definiscono come un'organizzazione dirige la sicurezza, decide quanto rischio accettare e dimostra di rispettare obblighi normativi e contrattuali. La governance stabilisce direzione e responsabilità, il risk management identifica e tratta le minacce, la compliance verifica l'aderenza a standard e leggi. Senza GRC, i controlli tecnici diventano scelte arbitrarie e non difendibili davanti a un auditor o a un regolatore.

## Come funziona

I tre pilastri operano in cascata e si alimentano a vicenda:

- **Governance**: il vertice (board, CISO) definisce risk appetite, policy di alto livello e ruoli. Stabilisce *chi decide cosa* e a chi rendere conto.
- **Risk management**: processo ciclico di identificazione, analisi, valutazione e trattamento del rischio. Produce un **risk register** e alimenta le decisioni di governance.
- **Compliance**: mappatura dei requisiti esterni (leggi, standard, contratti) sui controlli interni e verifica continua dell'aderenza.

Concetti chiave che ricorrono in tutta l'area:

- **Policy / Standard / Procedura / Linea guida**: gerarchia documentale. La policy dice *cosa e perché*, lo standard *quanto*, la procedura *come passo-passo*, la linea guida *consigli non vincolanti*.
- **Controllo**: misura che riduce il rischio. Si classifica per **funzione** (preventivo, detettivo, correttivo) e per **natura** (amministrativo, tecnico, fisico).
- **Tre linee di difesa**: 1ª = chi gestisce il rischio operativamente; 2ª = funzioni di risk e compliance che supervisionano; 3ª = internal audit indipendente.
- **Framework vs Standard vs Regolamento**: un framework (es. NIST CSF) è una struttura volontaria; uno standard (ISO 27001) è certificabile; un regolamento (GDPR) è legge vincolante.

## Esempi

Classificazione di controlli reali per funzione e natura:

| Controllo | Funzione | Natura |
|---|---|---|
| Firewall perimetrale | Preventivo | Tecnico |
| Policy di password | Preventivo | Amministrativo |
| SIEM / alerting | Detettivo | Tecnico |
| Badge e tornelli | Preventivo | Fisico |
| Piano di incident response | Correttivo | Amministrativo |
| Backup e restore | Correttivo | Tecnico |

Gerarchia documentale applicata al tema accessi:

| Livello | Esempio |
|---|---|
| Policy | "L'accesso ai sistemi segue il principio del minimo privilegio" |
| Standard | "MFA obbligatoria su tutti gli account con privilegi amministrativi" |
| Procedura | "Onboarding: il manager apre ticket → IT crea utenza → grant ruolo X" |
| Linea guida | "Si consiglia l'uso di un password manager aziendale" |

## Applicazione pratica e difesa

Implementare GRC significa partire da un **gap assessment**: confrontare lo stato attuale con un framework di riferimento e produrre un piano di remediation prioritizzato per rischio. Strumenti GRC (Archer, ServiceNow IRM, Vanta, Drata) centralizzano policy, evidenze e stato dei controlli. Per il difensore, la chiave è rendere ogni controllo **misurabile e provabile**: un controllo che non genera evidenza (log, report, screenshot, ticket) non supera un audit. Le metriche tipiche sono KPI (efficienza operativa) e KRI (key risk indicator, segnali di rischio crescente).

## Lab

- [[TryHackMe]] - percorso *Security Engineer* e moduli su governance e security management.
- Esercizio: redigere una mini Information Security Policy (1 pagina) e derivarne 3 standard e 1 procedura.
- Mappare i controlli di un sistema noto sulle tre funzioni (preventivo/detettivo/correttivo).
- Costruire un semplice catalogo controlli in foglio di calcolo con owner ed evidenza richiesta.

## Domande

1. **Qual è la differenza tra governance e management?** La governance definisce direzione, autorità e accountability (chi decide); il management esegue e gestisce operativamente nel perimetro fissato dalla governance.
2. **Perché un controllo deve produrre evidenza?** Perché in audit vale solo ciò che è dimostrabile: senza log, ticket o report il controllo è considerato non operante.
3. **Differenza tra framework, standard e regolamento?** Il framework è volontario e strutturante, lo standard è certificabile, il regolamento è legge con sanzioni.
4. **Cosa sono le tre linee di difesa?** Modello di governance del rischio: ownership operativa (1ª), supervisione risk/compliance (2ª), assurance indipendente di internal audit (3ª).
5. **KPI vs KRI?** Il KPI misura la performance di un processo; il KRI anticipa un aumento di esposizione al rischio.

## Approfondimento livello esperto

La distinzione cruciale è tra **compliance** e **security**: la conformità è condizione necessaria ma non sufficiente. Un'organizzazione può essere PCI-DSS compliant e comunque essere compromessa (vedi Target, certificata al momento del breach). Il GRC maturo sposta il baricentro dalla *checkbox compliance* alla **risk-based security**, in cui i controlli sono selezionati per riduzione effettiva del rischio e non solo per soddisfare un requisito. La convergenza moderna si chiama **IRM** (Integrated Risk Management) e **GRC continuo**, dove le evidenze sono raccolte via automazione (API verso cloud e IdP) anziché a campione una volta l'anno. Concetto avanzato: il **risk appetite** quantificato (es. "tolleriamo al massimo 500k€ di perdita annua attesa da incidenti cyber") collega la governance direttamente alla quantificazione FAIR vista più avanti.

## Collegamenti

- [[ISO 27001 e ISMS]]
- [[NIST CSF e 800-53]]
- [[Risk Management e Quantificazione]]
- [[Audit e Framework (SOC 2, PCI-DSS)]]
- [[Penetration Testing]]

## Fonti

- https://csrc.nist.gov/glossary - NIST Computer Security Resource Center, glossario dei termini GRC.
- https://www.iso.org/isoiec-27001-information-security.html - ISO/IEC 27001, panoramica ufficiale.
- https://www.oceg.org/about/what-is-grc/ - OCEG, definizione di riferimento di GRC.
