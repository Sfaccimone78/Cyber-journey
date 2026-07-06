---
tipo: concetto
tag: [windows]
fase: 1
fonti: 3
aggiornato: 2026-07-02
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

## Lab
- [[TryHackMe]] → room **Windows Forensics 1**: analisi degli hive del registro (`SYSTEM`, `SOFTWARE`, `NTUSER.DAT`) per ricostruire attività utente, dispositivi USB collegati e programmi in autorun. Pratica l'estrazione delle chiavi con RegRipper.
- [[TryHackMe]] → room **Sysinternals**: usa **Autoruns** per elencare tutte le voci di persistenza (chiavi `Run`, servizi, task) e confrontarle con la baseline pulita, individuando la voce malevola.
- Lab locale (VM Windows): aggiungi una voce fittizia sotto `HKCU\...\Run` con `Set-ItemProperty`, poi rilevala via `Get-WinEvent` filtrando l'**Event ID 4657** (modifica valore di registro) — richiede audit "Registry" abilitato.

## Domande
1. **D:** Quale hive contiene gli hash delle password locali e con quale privilegio è accessibile?  **R:** L'hive `HKLM\SAM`, accessibile solo come account SYSTEM.
2. **D:** Quali due chiavi vengono modificate più spesso da un malware per ottenere persistenza all'avvio?  **R:** `HKLM\...\CurrentVersion\Run` e `HKCU\...\CurrentVersion\Run`.
3. **D:** Qual è l'Event ID da monitorare per rilevare la modifica di un valore di registro?  **R:** L'Event ID 4657 nel [[Windows Event Log]].
4. **D:** Che differenza c'è tra una "chiave" e un "valore" nel registro?  **R:** La chiave è come una cartella contenitore, il valore è come un file dentro la chiave, con un tipo di dato (stringa, numero, binario…).
5. **D:** Quale strumento Sysinternals è dedicato all'ispezione delle voci di avvio automatico?  **R:** Autoruns.

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
