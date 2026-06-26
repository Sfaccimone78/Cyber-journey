---
tipo: concetto
tag: [blue-team]
fase: 3
fonti: 2
aggiornato: 2026-06-21
stato: maturo
aliases: ["EDR e XDR", "EDR", "XDR"]
---

# EDR e XDR

## In breve
**EDR** (Endpoint Detection and Response) è l'evoluzione dell'antivirus: invece di firmare solo file, **registra il comportamento** dell'endpoint (processi, thread, rete, registro, API) e rileva **catene di azioni** sospette in tempo reale, con capacità di **risposta** (isolare l'host, killare un processo). **XDR** (eXtended D&R) estende la stessa logica **oltre l'endpoint**, correlando endpoint + rete + email + cloud + identità in un'unica piattaforma. Per un analista [[SIEM|SOC]] sono la fonte di telemetria più ricca e l'ostacolo principale per chi attacca.

## EDR vs Antivirus vs XDR
| | Antivirus | EDR | XDR |
|---|---|---|---|
| Rileva su | firme file | **comportamento** endpoint | comportamento **multi-dominio** |
| Visibilità | file/scan | processi, API, rete locale | + rete, email, cloud, identità |
| Risposta | quarantena file | isola host, kill, rollback | risposta orchestrata cross-layer |
| Esempi | Defender (classic) | CrowdStrike, SentinelOne, Defender for Endpoint | Microsoft XDR, Cortex XDR |

## Come l'EDR "vede" un attacco
Telemetria tipica (spesso via driver kernel / ETW / hook): creazione processi con **parent-child** (es. `winword.exe → powershell.exe`), command line, iniezione (`CreateRemoteThread`), accesso a `lsass` (credential dumping, [[Mimikatz]]), connessioni di rete per-processo, modifiche al registro/persistenza. Un singolo evento è benigno; la **sequenza** fa scattare la detection — la stessa logica del [[Detection di Attacchi|detection engineering]] e delle [[Regole Sigma]], mappata su [[MITRE ATT&CK]].

## Rilevanza per le due squadre
- **Blue (SOC)**: l'EDR genera gli alert che fai [[Triage degli Alert|triage]]; le sue tracce alimentano l'[[Incident Response]]. Conoscerne i data source = scrivere detection migliori.
- **Red**: l'EDR è il motivo per cui [[Meterpreter]]/[[msfvenom]] "rumorosi" vengono bruciati; spinge verso *living-off-the-land*, payload in-memory, AMSI/ETW bypass (concetti, non in scope eJPT base).

## Limiti
- Copre **endpoint gestiti**: dispositivi non-managed, IoT, alcuni server Linux restano ciechi → l'XDR/rete colma in parte.
- Tuning necessario: troppe regole = falsi positivi; troppo poche = miss.

## Collegamenti
- [[SIEM]] — l'EDR è una sorgente; spesso integrato/feed verso il SIEM
- [[Detection di Attacchi]] · [[Regole Sigma]] · [[MITRE ATT&CK]]
- [[Log Analysis]] · [[Incident Response]] · [[Sysmon]] — telemetria endpoint open
- [[Meterpreter]] · [[Mimikatz]] — ciò che l'EDR mira a rilevare

## Fonti
- MITRE — Endpoint detection (ATT&CK data sources): https://attack.mitre.org/datasources/
- Microsoft — Defender for Endpoint overview: https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint
