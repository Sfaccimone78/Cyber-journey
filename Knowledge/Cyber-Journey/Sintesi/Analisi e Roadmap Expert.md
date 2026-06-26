---
tipo: sintesi
tag: [metodologia]
fase: 0
fonti: 0
aggiornato: 2026-06-26
stato: attivo
aliases: ["Analisi e Roadmap Expert", "Roadmap Expert"]
---

# Analisi e Roadmap verso l'Expertise

Analisi critica dello stato della wiki + piano di lavoro per passare da una solida base
intermedia a una **knowledge base da expert**. Aggiornare man mano che i gap vengono colmati.

## 1. Stato di salute

| Metrica | Valore | Lettura |
|---|---|---|
| Pagine wiki | ~260 | Base ampia |
| Stato | 227 maturo · 22 attivo · 10 stub | Buona maturità |
| **Fonti citate reali** | **8** | 🔴 Criticità #1 |
| **Pagine fase 4 (expert)** | **0** | 🔴 Criticità #2 |
| fase 1-2 (base/medio) | 178 | Tutto qui |
| fase 3 (avanzato) | 22 | Sottile |
| Aree profonde | [[Reti]], [[Linux]] | Eccellenti |
| Aree sottili | [[Algoritmi e Strutture Dati]], [[Blue Team]], [[Windows e AD]] | Da rinforzare |

## 2. Criticità strutturali

1. **🔴 Sourcing quasi assente** — 8 fonti per 260 pagine. La wiki è sintesi non citata: rischio
   di errori non verificabili. Serve un pass di *source-grounding* (PortSwigger, [[HackTricks]],
   MITRE ATT&CK, RFC, paper, vendor docs).
2. **🔴 Soffitto di profondità** — zero contenuti expert (fase 4). Tutto si ferma a intermedio.
3. **🟠 Conoscenza passiva** — poche pagine linkano a un **lab** concreto ([[TryHackMe]],
   [[HackTheBox]], PortSwigger, CTF). L'expertise si costruisce con le mani.
4. **🟠 Squilibrio di copertura** — [[Reti]]/[[Linux]] profondissime; aree offensive/difensive
   avanzate più sottili. 10 stub da riempire.
5. **🟡 Nessun auto-test** — manca spaced-repetition / domande di ripasso.

## 3. Gap di contenuto (domini mancanti)

| Priorità | Dominio | Perché è da expert |
|---|---|---|
| 🔥 | **Cloud Security** (AWS/Azure/GCP, IAM, S3, SSRF→IMDS) | Dove si attacca oggi |
| 🔥 | **Web avanzato** (deserializzazione, JWT, OAuth/SAML, request smuggling, race) | Bug bounty serio |
| 🔥 | **AD avanzato** (ADCS/ESC, delegation, trust, Shadow Credentials) | Cuore del pentest enterprise |
| 🔥 | **Detection Engineering / Threat Hunting** (KQL/SPL, D3FEND, purple team) | Blue team reale |
| 🟠 | **Reverse Engineering & Malware Analysis** (Ghidra, x64dbg, unpacking) | Il mestiere |
| 🟠 | **Binary Exploitation / Exploit Dev** (overflow, ROP, bypass ASLR/DEP) | Sotto i pwntools |
| 🟠 | **DFIR avanzato** (memory/disk forensics, timeline, playbook IR) | IR oggi solo concettuale |
| 🟠 | **Container/K8s & DevSecOps** (Docker escape, RBAC, CI/CD, supply chain) | Superficie dominante |
| 🟡 | **Mobile**, **Wireless/802.11**, **OT/ICS** | Specializzazioni |
| 🟡 | **Crypto offensiva** (Cryptopals avanzato, side-channel) | C'è la teoria, manca l'attacco |
| 🟡 | **GRC reale** (ISO 27001, NIST CSF, threat intel: Diamond Model) | Ruoli senior |

## 4. Mosse di processo

1. **Source-grounding**: 1-3 fonti reali per ogni pagina hub; aggiornare `fonti:`.
2. **Scala fase 3→4** per area: una pagina "avanzata" + sezione `## Lab`.
3. **Aggancia ogni concetto a una pratica** (nessuna tecnica senza `## Lab`).
4. **Nuove aree** 11-14: Cloud, AppSec Avanzato, RE & Exploit Dev, DFIR & Detection.
5. **Layer di auto-test**: sezione `## Domande` (3-5 Q&A) nelle pagine mature.

## 5. Roadmap per impatto

1. Riempire i 10 stub + sourcing sulle hub.
2. **Web avanzato** + **AD avanzato** (max ROI, costruiscono sull'esistente).
3. **Cloud Security** (gap più grande vs mercato).
4. **Detection Engineering / Threat Hunting**.
5. **RE/Malware + Binary Exploitation**.
6. **DFIR + Container/DevSecOps**.

## Collegamenti

- [[index|Indice]] · [[overview|Overview]] · [[Strumenti da studiare in futuro]]
- Aree nuove (in costruzione): `11 Cloud Security` · `12 AppSec Avanzato` · `13 Reverse Engineering e Exploit Dev` · `14 DFIR e Detection Engineering`
