---
tipo: entita
tag: [blue-team, windows, tool]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Sysmon"]
---

# Sysmon

## Cos'è
**Sysmon** (System Monitor) è un tool gratuito della suite **Sysinternals** che, una volta installato come servizio/driver su Windows, registra eventi di sistema dettagliati nel [[Windows Event Log]]. Fornisce una telemetria molto più ricca dei log nativi ed è la base di moltissime regole di [[Detection di Attacchi|detection]] e [[Log Analysis|analisi]] blue team.

## Eventi chiave
| Event ID | Cosa registra |
|---|---|
| **1** | Creazione processo (comando completo, hash, parent) |
| **3** | Connessione di rete |
| **7** | Caricamento di moduli/DLL |
| **8** | CreateRemoteThread (injection) |
| **10** | Accesso a un processo (es. a LSASS → [[Mimikatz]]) |
| **11** | Creazione file |
| **13** | Modifica del [[Registro di Sistema Windows|Registro]] |
| **22** | Query DNS |

## Uso tipico
```powershell
# Installazione con file di configurazione
sysmon64.exe -accepteula -i sysmonconfig.xml

# Aggiornare la configurazione
sysmon64.exe -c sysmonconfig.xml
```
La configurazione di riferimento è quella di **SwiftOnSecurity** (o **Olaf Hartong's modular config**), che filtra il rumore e tiene gli eventi utili. I log finiscono in `Microsoft-Windows-Sysmon/Operational` e si inoltrano a uno [[SIEM]] come [[Splunk]].

## Quando si usa
- **Detection**: il processo `parent=winword.exe → child=powershell.exe` (Event ID 1) è un classico indicatore di macro malevola.
- **Threat hunting**: cercare accessi a LSASS (Event ID 10) per scovare furto credenziali.
- A supporto dell'[[Incident Response]] per ricostruire la timeline di un host.

## Collegamenti
- [[Windows Event Log]]
- [[Log Analysis]]
- [[Detection di Attacchi]]
- [[SIEM]]
- [[Regole Sigma]]
- [[MITRE ATT&CK]]

## Fonti
- Microsoft Learn — Sysmon: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
- SwiftOnSecurity sysmon-config: https://github.com/SwiftOnSecurity/sysmon-config
- Olaf Hartong — sysmon-modular: https://github.com/olafhartong/sysmon-modular
