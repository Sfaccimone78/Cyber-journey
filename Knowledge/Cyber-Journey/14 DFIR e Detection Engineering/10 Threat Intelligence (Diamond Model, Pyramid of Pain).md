---
tipo: concetto
tag: [blue-team]
fase: 3
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["Threat Intelligence (Diamond Model, Pyramid of Pain)", "Diamond Model", "Pyramid of Pain"]
---

# Threat Intelligence (Diamond Model, Pyramid of Pain)

La **Cyber Threat Intelligence** (CTI) trasforma dati grezzi su minacce in **conoscenza azionabile**:
chi attacca, come, con quali strumenti, e cosa fare per rilevarlo e bloccarlo. Questa pagina copre i
due modelli concettuali che strutturano l'analisi, estendendo la [[Threat Intelligence]] di base verso
l'uso in [[Detection Engineering]] e [[Threat Hunting]].

## I tre livelli della CTI

| Livello | Domanda | Consumatore |
|---------|---------|-------------|
| **Strategica** | Chi ci minaccia e perché? (trend, geopolitica) | Management, CISO |
| **Operativa** | Quali campagne/TTP sono attive contro il nostro settore? | SOC lead, threat hunter |
| **Tattica** | Quali IOC e tecniche concrete cercare ora? | Analisti, detection engineer |

## Diamond Model of Intrusion Analysis

Modella ogni evento di intrusione come un **diamante** con 4 vertici collegati: scoprendone uno si
risale agli altri (*pivoting*).

```text
            Adversary
           /          \
   Infrastructure --- Capability
           \          /
            Victim
```

- **Adversary** — l'attaccante (gruppo APT, criminale).
- **Capability** — TTP, malware, exploit usati ([[Malware]], tecniche [[MITRE ATT&CK]]).
- **Infrastructure** — C2, domini, IP, server di staging.
- **Victim** — bersaglio (org, persone, asset).

Esempio di pivot: da un dominio C2 ([[Indicatori di Compromissione (IOC)|infrastructure]]) si trovano
altri sample ([[Malware|capability]]) che colpiscono altre vittime → si attribuisce all'**adversary**.

## Pyramid of Pain (David Bianco)

Classifica gli indicatori per **quanto "fa male" all'attaccante** doverli cambiare se li rileviamo.
Difendere in alto nella piramide costringe l'avversario a uno sforzo molto maggiore.

| Livello | Indicatore | Dolore per l'attaccante |
|---------|-----------|--------------------------|
| 🔺 **TTPs** | Tecniche e comportamenti | **Difficilissimo** — deve re-imparare il mestiere |
| Tools | Tool/malware usati | Difficile — deve riscriverli |
| Network/Host Artifacts | User-agent, mutex, path | Fastidioso |
| Domain Names | Domini C2 | Semplice |
| IP Addresses | IP | Facile (cambia in minuti) |
| 🔻 **Hash Values** | Hash dei file | Banale (1 bit e cambia) |

**Implicazione per la detection**: bloccare hash/IP dà vittorie effimere; scrivere detection su
**TTP** (es. [[Regole Sigma|Sigma]] su `winword → powershell`) ha valore duraturo. Vedi
[[Detection Engineering]] e [[Query di Hunting (KQL e SPL)]].

## Standard e condivisione

- **STIX/TAXII** — formato e protocollo per scambiare CTI strutturata.
- **MISP** — piattaforma open-source per gestire e condividere IOC e eventi.
- **Traffic Light Protocol (TLP)** — etichette per la condivisione (TLP:RED/AMBER/GREEN/CLEAR).
- Feed e framework: MITRE ATT&CK (TTP), kill chain, mapping a [[MITRE D3FEND e Purple Teaming|D3FEND]].

## Lab

- **TryHackMe**: percorso *Cyber Threat Intelligence*, room *Diamond Model*, *Pyramid of Pain*,
  *MISP*, *OpenCTI*, *Threat Intelligence Tools*.
- **MISP** + feed pubblici (abuse.ch, AlienVault OTX) per esercitarsi con IOC reali.

## Domande
**D: Cos'è il Diamond Model?**
R: Un modello di analisi che lega quattro vertici di un'intrusione — **adversary, capability,
infrastructure, victim** — per correlare eventi e attribuire campagne.

**D: Cos'è la Pyramid of Pain?**
R: Una gerarchia di indicatori ordinata per il "dolore" inflitto all'attaccante se bloccati: hash
(banale) → IP → domini → artefatti host/rete → tool → **TTP** (massimo dolore). Guida dove investire.

**D: Differenza tra IOC e TTP?**
R: Gli **IOC** sono indicatori atomici osservabili (hash, IP, domini), facili da cambiare; le **TTP**
sono tattiche/tecniche/procedure (comportamento), più stabili e di valore difensivo duraturo.

## Collegamenti

- [[Threat Intelligence]] · [[Detection Engineering]] · [[Threat Hunting]] · [[Indicatori di Compromissione (IOC)]]
- [[MITRE ATT&CK]] · [[MITRE D3FEND e Purple Teaming]] · [[Malware]] · [[Incident Response]]

## Fonti

- Caltagirone, Pendergast, Betz — *The Diamond Model of Intrusion Analysis*: https://www.activeresponse.org/the-diamond-model/
- David Bianco — *The Pyramid of Pain*: https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html
- MITRE ATT&CK: https://attack.mitre.org/
- OASIS STIX/TAXII: https://oasis-open.github.io/cti-documentation/
