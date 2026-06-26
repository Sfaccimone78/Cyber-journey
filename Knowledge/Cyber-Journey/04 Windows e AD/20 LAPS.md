---
tipo: concetto
tag: [windows, ad, blue-team]
fase: 3
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["LAPS"]
---

# LAPS

## In breve
**LAPS** (Local Administrator Password Solution) è la soluzione Microsoft che assegna a ogni computer del dominio una **password di amministratore locale unica, casuale e ruotata automaticamente**, memorizzata in modo protetto in [[Active Directory]]. È la difesa principale contro il [[Lateral Movement|movimento laterale]] basato su password locali condivise.

## Il problema che risolve
Senza LAPS, molte aziende usano la **stessa password di Administrator locale** su tutte le macchine (spesso da un'immagine clonata). Un attaccante che ottiene quell'hash da una sola macchina (con [[Mimikatz]]) può fare [[Pass-the-Hash]] su **tutte** le altre → compromissione a catena. LAPS elimina la password condivisa: ogni host ne ha una diversa.

## Come funziona
- Un'estensione GPO sul client genera periodicamente una nuova password casuale per l'account admin locale.
- La password è salvata in attributi dell'oggetto computer in AD (`ms-Mcs-AdmPwd` nella versione legacy; attributi cifrati in **Windows LAPS** moderno).
- Solo i principal **autorizzati** via ACL possono leggerla.

## Rilevanza per la sicurezza
**Lato attacco:** se le ACL sono mal configurate, un utente può leggere le password LAPS in chiaro.
```powershell
# Verifica chi può leggere l'attributo / leggi la password (legacy)
Get-ADComputer "PC01" -Properties ms-Mcs-AdmPwd | Select ms-Mcs-AdmPwd
```
Strumenti come [[BloodHound]] evidenziano chi ha `ReadLAPSPassword`.

**Lato difesa:** distribuire LAPS ovunque, restringere le ACL di lettura agli amministratori necessari, abilitare l'audit della lettura password, preferire **Windows LAPS** (cifratura + rotazione DSRM).

## Collegamenti
- [[Lateral Movement]]
- [[Pass-the-Hash]]
- [[Mimikatz]]
- [[BloodHound]]
- [[Active Directory]]
- [[Privilege Escalation Windows]]

## Fonti
- Microsoft Learn — Windows LAPS overview: https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview
- HackTricks — LAPS: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/laps
- MITRE ATT&CK T1078 — Valid Accounts: https://attack.mitre.org/techniques/T1078/
