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

## 1. Stato di salute (rivisto 2026-06-28)

| Metrica | Valore | Lettura |
|---|---|---|
| Pagine wiki | ~314 file (298 note di contenuto) | Base ampia |
| Stato | 280 maturo · 28 attivo · 0 stub di contenuto (9 "stub" = solo `Template/`) | Buona maturità |
| Pagine fase 4 (expert) | **17** | Esistono: aree 11-14 create |
| fase 0-2 (trasversale/base/medio) | 241 | Grosso del corpo |
| fase 3 (avanzato) | 46 | Cresciuta |
| Note con `Approfondimento esperto` | **~30 / 298** | 🔴 Criticità #1: profondità disomogenea |
| Note con `## Domande` / `## Lab` | **62 / 54** su 298 | 🟠 Auto-test e lab incompleti |
| Distribuzione `fonti:` | sbilanciata (8 su SQLi, 0-3 su molte) | 🟠 Sourcing disomogeneo |
| Aree profonde | [[Reti]] (27), [[Web OWASP]] (25), [[Windows e AD]] (27), [[Linux]] (22) | Eccellenti |
| Aree sottili | [[Sistemi Operativi]] (7), [[Python]] (7), [[Cloud Security]] (9), 12-14 (10) | Da rinforzare |

## 2. Criticità strutturali (aggiornate)

1. **🔴 Profondità disomogenea** — lo *standard esperto* (vedi `WIKI_SCHEMA.md` → "Standard Nota
   Esperto", modello `SQL Injection`) esiste solo su ~30/298 note. La maggioranza si ferma a
   intermedio. È il gap #1: il picco è ottimo, la media no.
2. **🟠 Sourcing disomogeneo** — non più "8 fonti totali" (dato vecchio): molte note citano fonti,
   ma la distribuzione è sbilanciata. Obiettivo: ogni nota matura ≥2 fonti reali.
3. **🟠 Auto-test e lab incompleti** — `## Domande` 62/298, `## Lab` 54/298. Manca spaced-repetition
   (export Anki, vista ripasso). La conoscenza resta in parte passiva.
4. **🟠 Squilibrio di copertura** — [[Reti]]/[[Linux]]/[[Web OWASP]]/[[Windows e AD]] profonde; aree
   11-14 + [[Sistemi Operativi]]/[[Python]] ancora scheletriche rispetto all'ambizione esperto.
5. **🟡 Gap di dominio residui** — mancano Mobile, Wireless/802.11, OT/ICS, API/GraphQL come area,
   AI/LLM Security, DevSecOps/Supply-chain, AD-ADCS/ESC, GRC reale.

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
- Aree 11-14 (**create**): `11 Cloud Security` · `12 AppSec Avanzato` · `13 Reverse Engineering e Exploit Dev` · `14 DFIR e Detection Engineering` — ora da portare allo Standard Nota Esperto.
- Prossime aree (da creare, vedi piano): `15 Mobile` · `16 Wireless & Radio` · `17 API & GraphQL` · `18 AI/LLM Security` · `19 DevSecOps & Supply Chain` · `20 GRC & Compliance`.
