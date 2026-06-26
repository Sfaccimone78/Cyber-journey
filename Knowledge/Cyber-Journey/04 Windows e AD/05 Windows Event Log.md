---
tipo: concetto
tag: [windows, blue-team]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Windows Event Log"]

---

# Windows Event Log

> Nota etica: le tecniche descritte servono a comprendere il funzionamento dei log per scopi difensivi e di rilevamento. Applicarle solo in ambienti lab autorizzati.

## In breve

Il Windows Event Log è il sistema di registrazione degli eventi integrato in Windows. Ogni azione rilevante del sistema operativo (accessi, errori, modifiche a policy, esecuzione di processi) genera un **evento** con un ID numerico, un timestamp e metadati strutturati.

## Come funziona

Gli eventi sono organizzati in **canali** (log). I più importanti per la sicurezza sono:

- **Security** — accessi, autenticazioni, modifiche a account (Event IDs critici: 4624 login riuscito, 4625 login fallito, 4688 processo creato, 4720 account creato)
- **System** — eventi del kernel e dei servizi Windows
- **Application** — eventi di applicazioni installate
- **PowerShell/Operational** — script eseguiti tramite [[PowerShell]] (ID 4104)

Ogni evento contiene: **EventID**, **TimeCreated**, **Computer**, **UserID**, e un corpo XML con i dettagli. Il servizio `eventlog` scrive i file `.evtx` in `%SystemRoot%\System32\winevt\Logs\`.

Gli amministratori e i [[SIEM]] raccolgono questi log per rilevare comportamenti anomali come [[Pass-the-Hash]], [[Kerberoasting]] o [[Privilege Escalation Windows]].

## Esempio pratico

Cercare login falliti nell'ultimo giorno con [[PowerShell]]:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName   = 'Security'
    Id        = 4625
    StartTime = (Get-Date).AddDays(-1)
} | Select-Object TimeCreated, Message | Format-List
```

Output: mostra ogni tentativo di login fallito con username, workstation sorgente e tipo di accesso (es. Kerberos, NTLM).

## Mitigazione e difesa

- Abilitare la **Advanced Audit Policy** (`secpol.msc` → Advanced Audit Policy Configuration) per aumentare la granularità dei log.
- Centralizzare i log su un [[SIEM]] (es. Splunk, Elastic, Microsoft Sentinel) per non perderli se un attaccante li cancella localmente.
- Monitorare Event ID **1102** (Security log cancellato) e **4719** (System audit policy modificata) come segnali di tamper.
- Aumentare la dimensione massima del log Security a ≥1 GB.

## Collegamenti

- [[SIEM]]
- [[PowerShell]]
- [[Log Analysis]]
- [[Pass-the-Hash]]
- [[Kerberoasting]]
- [[MITRE ATT&CK]]
- [[Incident Response]]

## Fonti

- Microsoft Learn — Windows Security Auditing: https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/security-auditing-overview
- MITRE ATT&CK T1070.001 — Clear Windows Event Logs: https://attack.mitre.org/techniques/T1070/001/
- TryHackMe — Windows Event Logs room: https://tryhackme.com/room/windowseventlogs
