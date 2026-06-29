---
tipo: concetto
tag: [grc]
fase: 2
fonti: 2
aggiornato: 2026-06-28
stato: maturo
aliases: ["GDPR Operativo"]
---

# GDPR Operativo

## In breve

Il **GDPR** (Regolamento UE 2016/679) è la legge europea sulla protezione dei dati personali, applicabile a chiunque tratti dati di soggetti nell'UE, indipendentemente da dove ha sede. Impone principi (minimizzazione, limitazione delle finalità, integrità e riservatezza), diritti per gli interessati, obblighi documentali (registro dei trattamenti, DPIA) e l'obbligo di **notifica del data breach entro 72 ore**. Le sanzioni arrivano fino a **20 milioni di euro o il 4% del fatturato globale annuo**.

## Come funziona

Attori e concetti chiave:

- **Data Subject**: la persona fisica a cui si riferiscono i dati.
- **Titolare (Controller)**: decide finalità e mezzi del trattamento.
- **Responsabile (Processor)**: tratta i dati per conto del titolare (es. provider cloud); regolato da un **DPA** (Data Processing Agreement, art. 28).
- **DPO**: Data Protection Officer, obbligatorio in casi specifici (autorità pubbliche, monitoraggio su larga scala, dati particolari su larga scala).

Le **basi giuridiche** del trattamento (art. 6): consenso, contratto, obbligo legale, interesse vitale, interesse pubblico, legittimo interesse. Senza una base giuridica valida il trattamento è illecito.

I **diritti dell'interessato** (artt. 15-22): accesso, rettifica, cancellazione (*diritto all'oblio*), limitazione, portabilità, opposizione, e non essere sottoposto a decisioni automatizzate.

Adempimenti operativi: **registro dei trattamenti** (art. 30), **DPIA** (art. 35, valutazione d'impatto per trattamenti ad alto rischio), **privacy by design e by default** (art. 25), gestione del **breach** (artt. 33-34).

## Esempi

Esempio di applicazione di articoli a scenari reali:

| Articolo | Tema | Applicazione pratica |
|---|---|---|
| Art. 6 | Base giuridica | Newsletter marketing → richiede consenso esplicito (opt-in) |
| Art. 17 | Diritto all'oblio | Utente chiede cancellazione account → dati rimossi entro 1 mese |
| Art. 25 | Privacy by design | Form raccoglie solo i campi necessari (minimizzazione) |
| Art. 32 | Sicurezza | Cifratura at-rest e in-transit, pseudonimizzazione |
| Art. 33 | Breach notification | Notifica al Garante entro 72h dalla scoperta |
| Art. 35 | DPIA | Nuovo sistema di video-sorveglianza biometrica → DPIA obbligatoria |

Flusso di **notifica breach (72h)**:

| Tempo | Azione |
|---|---|
| T0 | Scoperta della violazione |
| Entro 72h | Notifica all'autorità di controllo (se rischio per i diritti) |
| Senza ritardo | Comunicazione agli interessati (se rischio elevato) |
| Sempre | Registrazione interna nel registro dei breach (anche se non notificata) |

## Applicazione pratica e difesa

Sul piano operativo, il GDPR si traduce in misure tecniche e organizzative (art. 32) che coincidono con buona parte dei controlli ISO 27001: cifratura, controllo accessi, logging, backup, [[Incident Response]]. La gestione del breach è il punto di contatto più diretto con il blue team: il conteggio delle 72 ore parte dalla *consapevolezza* della violazione, quindi servono detection e processi di escalation rapidi. Per il difensore, ogni esfiltrazione di dati personali è anche un evento di compliance: il report di un [[Penetration Testing]] che dimostra accesso a PII ha implicazioni dirette su DPIA e misure di sicurezza. Strumenti utili: data mapping, DLP, gestione del consenso, retention automatica.

## Lab

- [[TryHackMe]] - moduli di security management e data protection per il contesto.
- Esercizio: redigere un registro dei trattamenti (art. 30) per un'app di e-commerce fittizia.
- Simulare una DPIA semplificata per un nuovo trattamento ad alto rischio.
- Costruire una runbook di breach notification con timeline a 72 ore e ruoli.

## Domande

1. **Cosa cambia tra titolare e responsabile?** Il titolare decide finalità e mezzi; il responsabile tratta i dati per conto del titolare ed è vincolato da un DPA.
2. **Da quando partono le 72 ore?** Dalla *consapevolezza* (awareness) della violazione, non dal momento in cui è avvenuta.
3. **Serve sempre notificare il breach al Garante?** No: solo se la violazione comporta un rischio per i diritti e le libertà degli interessati; va comunque registrata internamente.
4. **Cos'è una DPIA e quando è obbligatoria?** È la valutazione d'impatto sulla protezione dei dati, obbligatoria per trattamenti ad alto rischio (es. profilazione su larga scala, dati biometrici).
5. **Qual è la sanzione massima?** Fino a 20 milioni di euro o il 4% del fatturato mondiale annuo, a seconda di quale sia maggiore.

## Approfondimento livello esperto

Il punto più delicato per i team tecnici è la **finestra delle 72 ore**: a differenza di altri framework, il GDPR non concede tolleranza, e la notifica tardiva o incompleta è essa stessa sanzionabile. Le 72 ore impongono che detection, classificazione del dato coinvolto e catena di escalation siano già pronte *prima* dell'incidente. Tema avanzato: i **trasferimenti extra-UE** (Capo V). Dopo l'invalidamento del Privacy Shield (sentenza *Schrems II*), i trasferimenti verso paesi terzi richiedono **SCC** (Standard Contractual Clauses) più un **TIA** (Transfer Impact Assessment), o l'adesione al **Data Privacy Framework** UE-USA (2023). Distinzione importante: **pseudonimizzazione** (reversibile con chiave, dato resta personale) vs **anonimizzazione** (irreversibile, esce dal perimetro GDPR). Infine il GDPR si interseca con le nuove normative UE: **NIS2** (sicurezza delle reti) e **DORA** (resilienza operativa nel settore finanziario), creando obblighi di notifica paralleli da coordinare.

## Collegamenti

- [[Fondamenti GRC]]
- [[ISO 27001 e ISMS]]
- [[Risk Management e Quantificazione]]
- [[Audit e Framework (SOC 2, PCI-DSS)]]
- [[Incident Response]]
- [[Penetration Testing]]

## Fonti

- https://gdpr-info.eu/ - Testo integrale del GDPR articolo per articolo.
- https://www.garanteprivacy.it/ - Garante per la protezione dei dati personali (Italia).
