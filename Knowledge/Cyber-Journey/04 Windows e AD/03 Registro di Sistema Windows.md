---
tipo: concetto
tag: [windows]
fase: 1
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Registro di Sistema Windows"]

---

# Registro di Sistema Windows

## In breve
Il **Registro di Sistema** (Registry) è il database centralizzato di Windows dove vengono memorizzate le configurazioni del sistema operativo, dei programmi installati e degli utenti. È organizzato come un albero gerarchico di **chiavi** e **valori**.

## Come funziona
### Struttura
Il registro è diviso in sezioni chiamate **Hive** (alveare):

| Hive | Abbreviazione | Contenuto |
|---|---|---|
| `HKEY_LOCAL_MACHINE` | `HKLM` | Configurazione di sistema e software per tutti gli utenti |
| `HKEY_CURRENT_USER` | `HKCU` | Configurazione specifica per l'utente corrente |
| `HKEY_USERS` | `HKU` | Profili di tutti gli utenti caricati |
| `HKEY_CLASSES_ROOT` | `HKCR` | Associazioni file e COM objects |
| `HKEY_CURRENT_CONFIG` | `HKCC` | Configurazione hardware attiva |

### Chiavi e valori
Una **chiave** è come una cartella. Un **valore** è come un file dentro quella cartella, con un tipo di dato (stringa, numero, binario…).

### Chiavi importanti per la sicurezza
- **Autorun** — programmi che partono all'avvio:
  ```
  HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
  HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
  ```
- **SAM** — hash delle password locali (accessibile solo come SYSTEM):
  ```
  HKLM\SAM
  ```
- **Servizi di sistema**:
  ```
  HKLM\SYSTEM\CurrentControlSet\Services
  ```

## Esempio pratico
Un malware aggiunge se stesso all'avvio modificando la chiave Run:

```powershell
# Visualizzare i programmi in autorun
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

# Aggiungere una voce (come farebbe malware)
Set-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" `
  -Name "Updater" -Value "C:\Temp\malware.exe"
```

Un analista cercherebbe voci anomale qui durante un'indagine forensica.

## Mitigazione e difesa
- Monitorare modifiche alle chiavi Run tramite [[Windows Event Log]] (Event ID 4657).
- Usare [[PowerShell]] o Autoruns (Sysinternals) per ispezionare le voci di avvio.
- Limitare la scrittura al registro per utenti non amministratori.
- Effettuare backup regolari del registro per il ripristino.

## Collegamenti
- [[Filesystem Windows]]
- [[Utenti e Permessi Windows]]
- [[Windows Event Log]]
- [[Privilege Escalation Windows]]
- [[PowerShell]]

## Fonti
- Microsoft Learn – Registry overview: https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry
- HackTricks – Registry persistence: https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/privilege-escalation-with-autorun-binaries
- MITRE ATT&CK – Boot or Logon Autostart: https://attack.mitre.org/techniques/T1547/001/
