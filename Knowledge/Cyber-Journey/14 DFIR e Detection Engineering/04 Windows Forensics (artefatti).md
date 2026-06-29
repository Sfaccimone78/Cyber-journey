---
tipo: concetto
tag: [blue-team, windows]
fase: 3
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["Windows Forensics (artefatti)", "Windows Forensics", "Artefatti Windows"]
---

# Windows Forensics (artefatti)

## In breve
Windows lascia ovunque tracce dell'attività di utenti e programmi: registro, prefetch, event log,
shellbags, jump list, browser, file recenti. La **Windows forensics** sa *dove guardare* per
provare **esecuzione**, **persistenza**, **accesso a file** e **movimento**. Questa pagina è una
mappa operativa degli artefatti, organizzata per **domanda investigativa** — l'approccio SANS
"artifact category".

## Mappa artefatti per categoria investigativa

### 1. Esecuzione di programmi ("è stato eseguito?")
| Artefatto | Prova | Posizione |
|---|---|---|
| **Prefetch** | esecuzione, n. run, ultima run | `C:\Windows\Prefetch\*.pf` |
| **Amcache.hve** | binari + hash SHA1 + path | `C:\Windows\AppCompat\Programs\` |
| **Shimcache** | binari presenti/eseguiti | hive `SYSTEM\...\AppCompatCache` |
| **UserAssist** | GUI eseguite dall'utente (ROT13) | `NTUSER.DAT\...\UserAssist` |
| **BAM/DAM** | eseguibili + timestamp ultimo avvio | `SYSTEM\...\bam\State\UserSettings` |

### 2. Persistenza ("come resta dopo il reboot?")
- **Run / RunOnce keys**: `HKLM|HKCU\...\CurrentVersion\Run` (T1547.001).
- **Servizi**: `SYSTEM\CurrentControlSet\Services` (T1543.003).
- **Scheduled Tasks**: `C:\Windows\System32\Tasks\` + EVTX `TaskScheduler` (T1053.005).
- **WMI Event Subscription**: `__EventFilter`/`__EventConsumer` (T1546.003).

### 3. Accesso a file/cartelle ("cosa ha aperto?")
- **Shellbags** (`USRCLASS.DAT`): cartelle navigate in Explorer, anche se cancellate.
- **Jump Lists** (`AutomaticDestinations-ms`): file recenti per applicazione.
- **LNK / Recent** (`%AppData%\...\Recent`): scorciatoie a file aperti (con path e volume).
- **Open/Save MRU**, **RecentDocs** nel registro.

### 4. Account e logon ("chi è entrato e da dove?")
Vedi i [[Windows Event Log]] — gli Event ID chiave sono nella tabella sotto.

## Esempio pratico — triage con Eric Zimmerman Tools + RECmd
```powershell
# Parsing prefetch (KAPE/EZ Tools): cosa è stato eseguito e quante volte
PECmd.exe -d C:\Windows\Prefetch --csv .\out

# Shimcache + Amcache: presenza/esecuzione binari (utile contro malware cancellato)
AppCompatCacheParser.exe -f C:\Windows\System32\config\SYSTEM --csv .\out
AmcacheParser.exe -f C:\Windows\AppCompat\Programs\Amcache.hve -i --csv .\out

# Shellbags: cartelle navigate dall'utente
SBECmd.exe -d "C:\Users\vittima" --csv .\out

# Run keys e persistenza dal registro
RECmd.exe --f C:\Users\vittima\NTUSER.DAT --kn "Software\Microsoft\Windows\CurrentVersion\Run" --csv .\out

# Triage di massa: KAPE raccoglie tutti gli artefatti chiave in pochi minuti
kape.exe --tsource C: --target KapeTriage --tdest .\triage --vhdx HOST12
```

Event log critici (esporta con `wevtutil` o parsa gli `.evtx`):
```powershell
# Logon riusciti/falliti, RDP, creazione processi, servizi
wevtutil qe Security "/q:*[System[(EventID=4624 or EventID=4625 or EventID=4672)]]" /f:text /c:50
```

## Event ID Windows da conoscere (Security/System)
| Event ID | Significato | Rilevanza |
|---|---|---|
| 4624 / 4625 | Logon riuscito / fallito | brute force, lateral (LogonType 3/10) |
| 4672 | Logon con privilegi speciali | uso account admin |
| 4688 | Creazione processo (+ cmdline) | esecuzione, vedi [[Sysmon]] EID 1 |
| 4720 / 4732 | Account creato / aggiunto a gruppo | persistenza, escalation |
| 7045 | Servizio installato | PsExec, persistenza (T1543) |
| 4698 | Scheduled task creato | persistenza (T1053) |
| 1102 | Security log cancellato | anti-forensics (T1070.001) |
| 4769 | Richiesta ticket Kerberos | [[Kerberoasting]] |

> [!tip] Sysmon arricchisce tutto
> I log nativi sono poveri. Con [[Sysmon]] ottieni hash dei processi (EID 1), connessioni di rete
> (EID 3), creazione file (EID 11), modifiche al registro (EID 13) e injection (EID 8/10) — la
> telemetria su cui si costruiscono le detection. Vedi [[Detection Engineering]].

> [!caution] Etica e privacy
> Gli artefatti utente (browser, file recenti, shellbags) sono **dati personali**. Analizzali solo
> nell'ambito autorizzato dell'indagine, minimizza ciò che esporti e proteggi i report (GDPR).

## Lab
- **TryHackMe** — *Windows Forensics 1 & 2*, *Core Windows Processes*, percorso *SOC Level 1*.
- **CyberDefenders** — challenge basate su triage KAPE/EZ Tools.
- **BlueTeamLabs.online** — investigations su host Windows compromessi.
- **Eric Zimmerman Tools** + **KAPE** (gratuiti) su immagini di esercizio.

## Domande
**D: Quali artefatti provano l'esecuzione di un programma?**
R: **Prefetch**, **Shimcache/AppCompatCache**, **Amcache**, **UserAssist**, **SRUM**. Ognuno con
granularità e affidabilità diverse; si correlano per confermare esecuzione e timing.

**D: A cosa servono le ShellBags?**
R: Registrano cartelle visitate/aperte da Explorer → provano l'accesso a directory (anche su supporti
rimovibili o percorsi poi cancellati).

**D: Dove cercare la persistenza su Windows?**
R: Chiavi `Run`/`RunOnce`, **scheduled tasks**, servizi, **WMI event subscriptions**, cartella
Startup. MITRE T1547/T1053/T1543.

## Collegamenti
- [[Windows Event Log]]
- [[Registro di Sistema Windows]]
- [[Sysmon]]
- [[Disk Forensics e Timeline Analysis]]
- [[Log Analysis Avanzata e Correlazione]]
- [[Detection Engineering]]
- [[MITRE ATT&CK]]

## Fonti
- SANS — Windows Forensic Analysis (FOR500) poster: https://www.sans.org/posters/windows-forensic-analysis/
- Eric Zimmerman Tools: https://ericzimmerman.github.io/
- KAPE (Kroll Artifact Parser and Extractor): https://www.kroll.com/kape
- 13Cubed — Windows Forensics (YouTube/training): https://www.13cubed.com/
