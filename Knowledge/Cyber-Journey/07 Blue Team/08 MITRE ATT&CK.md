---
tipo: concetto
tag: [blue-team]
fase: 2
fonti: 6
aggiornato: 2026-06-21
stato: maturo
aliases: ["MITRE ATT&CK"]
---

# MITRE ATT&CK

## In breve
**MITRE ATT&CK** (Adversarial Tactics, Techniques & Common Knowledge) è la base di conoscenza pubblica che cataloga le **TTP** (Tattiche, Tecniche, Procedure) osservate negli attacchi **reali**. È il linguaggio comune che lega red team, blue team, threat intelligence e detection engineering: descrivere un attacco con ID ATT&CK rende tutti interoperabili.

## La struttura
- **Tattiche** = il *perché* (l'obiettivo dell'attaccante). La matrice **Enterprise** ne ha 14, in ordine logico: *Reconnaissance, Resource Development, Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact*.
- **Tecniche / sotto-tecniche** = il *come*. Es. `T1059` (Command and Scripting Interpreter) → `T1059.001` (PowerShell).
- **Procedure** = implementazioni reali (come un gruppo APT specifico ha usato la tecnica).
- **Mitigations** (`M****`) e **Data Sources** (cosa serve loggare per rilevarla) sono collegati a ogni tecnica.

```
Tattica   Initial Access
 └─ Tecnica       T1566  Phishing
     └─ Sotto-tecnica T1566.001  Spearphishing Attachment
```

Esistono tre matrici: **Enterprise** (Win/Linux/macOS/Cloud/Containers), **Mobile**, **ICS**.

## A cosa serve davvero (non è solo un poster)
1. **Detection engineering** — per ogni tecnica scrivi una regola ([[Regole Sigma|Sigma]]/SIEM). ATT&CK indica i *data source* necessari (es. `Process Creation`, `Command Line`).
2. **Gap analysis con il [[MITRE ATT&CK Navigator|Navigator]]** — colori la matrice: verde = coperto da detection, rosso = cieco. Vedi a colpo d'occhio dove non vedi nulla.
3. **Threat-informed defense** — mappi un avversario rilevante (es. APT che colpisce il tuo settore) e prioritizzi le sue tecniche.
4. **Purple teaming** — il red emula tecniche note (Atomic Red Team, Caldera), il blue verifica se le detection scattano.
5. **Threat intelligence** — i report descrivono i gruppi (`G****`) e i tool (`S****`) in termini di tecniche → confrontabili.

## Esempio pratico — mappare un incidente
Un alert su [[Splunk]]: PowerShell scarica ed esegue un file, poi parte una connessione verso un IP esterno.
```
Email con allegato       → T1566.001  Spearphishing Attachment   (Initial Access)
Macro lancia PowerShell  → T1059.001  PowerShell                 (Execution)
Download del payload     → T1105      Ingress Tool Transfer      (C2)
Chiave Run per persist.  → T1547.001  Registry Run Keys          (Persistence)
Dump credenziali LSASS   → T1003.001  LSASS Memory               (Credential Access)
```
La catena ti dice: a che punto è l'attacco, **cosa cercare dopo** (es. dopo `T1003.001` aspettati [[Lateral Movement]]), e quali **mitigazioni** applicare (AppLocker, PowerShell ScriptBlock Logging, Credential Guard).

## ATT&CK vs Cyber Kill Chain
La [[La Cyber Kill Chain|Cyber Kill Chain]] (Lockheed Martin) è **lineare e di alto livello** (7 fasi). ATT&CK è **granulare e non lineare**: un attaccante itera tra tattiche. Le due si complementano — kill chain per la narrativa, ATT&CK per il dettaglio tecnico e le detection.

## Rilevanza per la sicurezza
Sposta la difesa da **reattiva** (aspettare un alert) a **proattiva**: costruisci copertura per tecnica, misuri i tuoi punti ciechi e parli la stessa lingua di IR, TI e red team. È lo standard de facto per [[Detection di Attacchi]] e [[Threat Intelligence]].

---

# Approfondimento — uso operativo in SOC

## Anatomia di un T-id (come leggerlo)
`T1558.003 — Kerberoasting` si scompone così:
- **Tattica** (obiettivo): *Credential Access* — l'attaccante vuole credenziali.
- **Tecnica**: `T1558` *Steal or Forge Kerberos Tickets*.
- **Sotto-tecnica**: `.003` Kerberoasting (il modo specifico).
- **Data Sources** (cosa loggare): *Active Directory: Logon* (Event ID **4769**), *Network Traffic*.
- **Mitigations**: `M1041` (cifratura forte), `M1027` (password policy), `M1015` (gMSA).
- **Detection**: descrive la logica (richieste TGS anomale con RC4).

> Una stessa tecnica può servire **più tattiche**. Es. `T1078 Valid Accounts` appare in Initial Access, Persistence, Privilege Escalation e Defense Evasion — perché credenziali valide servono a tutto.

## Mappare un attacco reale — workflow
1. **Raccogli gli artefatti** dall'indagine ([[Log Analysis]], [[Incident Response]]): processi, connessioni, account, file.
2. **Per ogni azione, chiediti "qual era l'obiettivo?"** → quella è la **tattica**. Poi "come l'ha fatto?" → la **tecnica**.
3. **Cerca la tecnica** su attack.mitre.org (o per data source). Annota il T-id.
4. **Ordina per kill chain** — disponi i T-id nell'ordine logico delle tattiche per ricostruire la storia.
5. **Colora il [[MITRE ATT&CK Navigator|Navigator]]** — evidenzi le tecniche viste; il JSON del layer diventa documentazione condivisibile.

## Il Navigator in pratica
Il **[[MITRE ATT&CK Navigator]]** è una web-app (anche self-host) che mostra la matrice come heatmap editabile:
- **Layer multipli sovrapponibili**: uno per la *copertura detection* (verde=coperto/rosso=cieco), uno per le *tecniche di un APT*, uno per un *incidente*. La sovrapposizione (score addizione) mostra a colpo d'occhio: *"l'avversario usa queste 30 tecniche, ne copro 18"*.
- **Scoring e commenti** per tecnica → priorità di detection engineering.
- **Export JSON** versionabile in Git (detection-as-code anche per la copertura).
- Caso d'uso tipico: importi il layer di **un gruppo G\*\*\*\*** che colpisce il tuo settore, sovrapponi il tuo layer di copertura, prioritizzi i gap.

## Mappatura end-to-end di una kill chain (esempio completo)
Intrusione ransomware ricostruita dai log, mappata tattica per tattica:

| # | Evidenza nei log | Tattica | Tecnica | Detection / data source |
|---|---|---|---|---|
| 1 | Email con allegato `.docm` aperto da utente | Initial Access | `T1566.001` Spearphishing Attachment | mail gateway, [[Sysmon]] 1 |
| 2 | `winword.exe` → `powershell.exe` (parent-child) | Execution | `T1059.001` PowerShell | Sysmon 1, ScriptBlock 4104 |
| 3 | PowerShell scarica `payload.exe` da IP esterno | Command and Control | `T1105` Ingress Tool Transfer | proxy, Sysmon 3 |
| 4 | Chiave `HKCU\...\Run` creata | Persistence | `T1547.001` Registry Run Keys | Sysmon 13, Event 4657 |
| 5 | Dump di LSASS (handle da processo inatteso) | Credential Access | `T1003.001` LSASS Memory | Sysmon 10, Event 4656 |
| 6 | Logon Type 3 NTLM admin WS→WS + PsExec | Lateral Movement | `T1021.002` SMB/Admin Shares + `T1550.002` PtH | Event 4624/7045, Sysmon 1/3 → [[Pass-the-Hash]] |
| 7 | `vssadmin delete shadows` | Defense Evasion / Impact | `T1490` Inhibit System Recovery | Event 4688, Sysmon 1 |
| 8 | Estensioni file cifrate in massa | Impact | `T1486` Data Encrypted for Impact | EDR, file audit 4663 |

> [!tip] Cosa ti dà la mappatura
> 1) **Stato dell'attacco** (qui: già a Impact = ransomware in esecuzione). 2) **Cosa cercare a ritroso** (se vedi step 6, lo step 5 è probabilmente già avvenuto). 3) **Dove sei cieco** (se non hai Sysmon 10, lo step 5 ti sfugge). 4) **Mitigazioni prioritarie** per ogni step (Credential Guard contro #5, AppLocker contro #2).

## Limiti onesti del framework
- **Non è una sequenza obbligata**: l'ordine delle tattiche è logico, non temporale rigido — gli attaccanti iterano e saltano.
- **Mapping soggettivo**: la stessa azione può ricevere T-id diversi da analisti diversi; conta la coerenza interna.
- **Copre il post-compromesso meglio del pre**: Reconnaissance/Resource Development sono spesso fuori dalla tua telemetria.
- **Coprire una tecnica ≠ rilevare tutte le sue procedure**: una regola può intercettare una variante e mancarne altre. Il verde sul Navigator è una *stima*, non una garanzia.

## Troubleshooting — 5 errori da analista junior
1. **Confondere Tattica e Tecnica** ("ho usato la tattica PowerShell") → PowerShell è una *tecnica* (T1059.001), la tattica è *Execution*. Causa: non aver interiorizzato i due livelli.
2. **Forzare un T-id preciso quando non c'è evidenza** → meglio la tecnica padre che una sotto-tecnica inventata. Causa: voler essere precisi oltre il dato.
3. **Trattare il Navigator verde come "siamo protetti"** → coprire una tecnica non significa rilevarne ogni procedura. Causa: confondere copertura mappata con efficacia reale.
4. **Mappare solo IOC e non TTP** → ATT&CK è fatto per le *tecniche*; mappare hash/IP svuota il valore. Causa: livello sbagliato di astrazione.
5. **Ignorare i Data Sources** prima di promettere detection → ATT&CK ti dice *cosa serve loggare*; se non lo logghi, non puoi rilevarlo. Causa: saltare il prerequisito di telemetria.

## Domande da colloquio SOC
> [!question] Qual è la differenza tra Tattica, Tecnica e Procedura?
> **Tattica** = il *perché*/obiettivo (es. Credential Access). **Tecnica** = il *come* generale (es. T1558.003 Kerberoasting). **Procedura** = l'*implementazione specifica* osservata (es. APT29 ha usato Rubeus per richiedere TGS). Dal generale al concreto.

> [!question] Come useresti ATT&CK per migliorare il tuo SOC?
> Faccio **gap analysis** col [[MITRE ATT&CK Navigator]]: mappo le tecniche che già rilevo (verde) contro quelle rilevanti per le minacce del mio settore (layer di un APT), e prioritizzo la detection engineering sui gap (rosso). Poi valido col purple teaming (Atomic Red Team).

> [!question] ATT&CK vs Cyber Kill Chain: quando usi quale?
> La [[La Cyber Kill Chain|Kill Chain]] (7 fasi lineari) è ottima per la **narrativa di alto livello** e la comunicazione al management. ATT&CK è **granulare e non lineare**, per il **dettaglio tecnico e le detection**. Le uso insieme: kill chain per raccontare, ATT&CK per implementare.

> [!question] Mi mappi velocemente un attacco di phishing che porta a ransomware?
> Spearphishing Attachment (T1566.001, Initial Access) → PowerShell (T1059.001, Execution) → Ingress Tool Transfer (T1105, C2) → Run Key (T1547.001, Persistence) → LSASS dump (T1003.001, Credential Access) → SMB/PtH (T1021.002/T1550.002, Lateral Movement) → Inhibit Recovery (T1490) → Data Encrypted for Impact (T1486).

## Collegamenti
- [[MITRE ATT&CK Navigator]] — heatmap della copertura
- [[Regole Sigma]] — tradurre le tecniche in detection
- [[Sysmon]] — data source per molte tecniche endpoint
- [[Threat Intelligence]]
- [[Detection di Attacchi]]
- [[Log Analysis]]
- [[Incident Response]]
- [[La Cyber Kill Chain]]
- [[SIEM]]
- Tecniche mappate: [[Kerberoasting]] · [[Pass-the-Hash]] · [[Lateral Movement]]

## Fonti
- MITRE ATT&CK — sito ufficiale: https://attack.mitre.org
- MITRE — Getting Started: https://attack.mitre.org/resources/getting-started/
- MITRE ATT&CK Navigator: https://mitre-attack.github.io/attack-navigator/
- MITRE D3FEND (contromisure): https://d3fend.mitre.org/
- MITRE — Best Practices for MITRE ATT&CK Mapping: https://www.cisa.gov/news-events/news/best-practices-mitre-attckr-mapping
- TryHackMe — MITRE: https://tryhackme.com/room/mitre
