---
tipo: concetto
tag: [blue-team, tool]
fase: 3
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["Memory Forensics con Volatility", "Memory Forensics"]
---

# Memory Forensics con Volatility

## In breve
La **memory forensics** analizza un'immagine della RAM per ricostruire lo stato *vivo* di un
sistema: processi, DLL, connessioni, handle, chiavi di registro caricate, malware fileless e
credenziali in chiaro — tutto ciò che il disco **non** mostra. Lo strumento di riferimento è
[[Volatility (Memory Forensics)]] (qui nella sua versione **3**). Questa pagina porta l'uso base
a livello investigativo: metodologia, individuazione di **process injection** e rootkit, dump
mirato per analisi malware.

## Metodologia (workflow tipico)
1. **Acquisisci** la RAM a sistema acceso (WinPmem, DumpIt, FTK Imager, AVML/LiME su Linux).
2. **Triage processi**: `pslist` (lista ufficiale) vs `psscan` (scan strutture `_EPROCESS`) →
   le differenze rivelano processi **nascosti/terminati**.
3. **Albero genealogico**: `pstree` → relazioni padre-figlio anomale (es. `winword.exe` →
   `powershell.exe` → `cmd.exe` = pattern di phishing).
4. **Rete**: `netscan`/`netstat` → connessioni C2 al momento del dump (correla con
   [[Indicatori di Compromissione (IOC)]]).
5. **Injection**: `malfind` → regioni di memoria `PAGE_EXECUTE_READWRITE` senza file mappato =
   shellcode iniettato.
6. **Persistenza/comandi**: `cmdline`, `consoles`, `registry.printkey` (Run keys).
7. **Estrazione**: `dumpfiles`, `procdump`, `vadyarascan` con [[YARA]] per firmare la RAM.

## Esempio pratico — caccia a process injection
```bash
# Vol3 individua il "kernel symbol" automaticamente (niente più --profile come in Vol2)
# 1) Panoramica processi e parentela
vol -f memory.raw windows.pstree
vol -f memory.raw windows.pslist
vol -f memory.raw windows.psscan          # confronta: PID presenti qui ma non in pslist = nascosti

# 2) Riga di comando completa (smaschera payload offuscati -enc base64)
vol -f memory.raw windows.cmdline

# 3) Process injection: regioni RWX iniettate senza backing file
vol -f memory.raw windows.malfind
vol -f memory.raw windows.malfind --dump --pid 1337   # estrae le regioni sospette

# 4) Connessioni di rete (C2 attivo)
vol -f memory.raw windows.netscan

# 5) Scansiona la memoria di un processo con regole YARA
vol -f memory.raw windows.vadyarascan --yara-file mimikatz.yar --pid 1337

# 6) Hash dei moduli e DLL caricate per un PID
vol -f memory.raw windows.dlllist --pid 1337
vol -f memory.raw windows.handles --pid 1337   # mutex/named pipe usati da malware
```

Pattern tipico di compromissione visto in RAM:
```text
explorer.exe
 └─ winword.exe            ← apertura allegato
     └─ powershell.exe     ← -enc <base64> (download cradle)
         └─ rundll32.exe   ← malfind segnala RWX + shellcode (Cobalt Strike beacon)
```

## Plugin chiave (Volatility 3) — riferimento rapido
| Obiettivo | Plugin |
|---|---|
| Lista processi | `windows.pslist` / `windows.psscan` / `windows.pstree` |
| Process injection | `windows.malfind` |
| Connessioni di rete | `windows.netscan` |
| Comandi eseguiti | `windows.cmdline` / `windows.consoles` |
| DLL / handle | `windows.dlllist` / `windows.handles` |
| Registro in RAM | `windows.registry.hivelist` / `registry.printkey` |
| Persistenza servizi | `windows.svcscan` |
| Estrazione | `windows.dumpfiles` / `windows.pslist --dump` |
| Hash file in memoria | `windows.filescan` + `dumpfiles` |
| Credenziali (Vol2/plugin) | `hashdump`, `lsadump`, `cachedump` |

> [!tip] pslist vs psscan
> `pslist` percorre la lista doppiamente concatenata che il kernel mantiene (può essere
> manipolata da un rootkit con **DKOM**). `psscan` fa carving delle strutture `_EPROCESS` in tutta
> la RAM: trova anche processi **scollegati dalla lista** o già terminati. La discrepanza è essa
> stessa un IOC.

> [!caution] Etica
> Analizza solo dump di sistemi autorizzati. I dump RAM contengono **password, token e dati
> personali in chiaro**: trattali come prove sensibili (cifratura at-rest, accesso ristretto, GDPR).

## Lab
- **CyberDefenders** — *DumpMe*, *Banking Troubles*, *Memory Analysis* (dump reali Vol3).
- **TryHackMe** — *Volatility*, *Investigating with Volatility*, percorso *SOC Level 2 / DFIR*.
- **LetsDefend** — esercizi *Memory Analysis* su incidenti.
- **Volatility Foundation** — sample images per esercitarsi (Malware Cookbook, MemLabs su GitHub).

## Domande
**D: Perché la RAM è una fonte forense preziosa?**
R: Contiene processi in esecuzione, connessioni di rete, chiavi crittografiche, **malware fileless** e
talvolta password in chiaro — informazioni assenti o cifrate su disco.

**D: Cosa fa il plugin `malfind`?**
R: Individua regioni di memoria eseguibili e scrivibili (RWX) senza file backing → tipico di code
injection e di payload **già unpackati** in RAM.

**D: Differenza tra Volatility 2 e 3?**
R: La v2 richiede un **profilo** (`--profile`) del sistema; la v3 usa symbol table (ISF) e lo rileva
automaticamente, con sintassi e plugin rinominati.

## Collegamenti
- [[Volatility (Memory Forensics)]]
- [[Digital Forensics Fondamenti]]
- [[Analisi Malware di Base]]
- [[Indicatori di Compromissione (IOC)]]
- [[YARA]]
- [[Windows Forensics (artefatti)]]
- [[Incident Response]]

## Fonti
- Volatility 3 documentation: https://volatility3.readthedocs.io/
- Volatility Foundation: https://www.volatilityfoundation.org/
- "The Art of Memory Forensics" (Ligh, Case, Levy, Walters) — riferimento canonico.
- SANS FOR508 / poster Memory Forensics: https://www.sans.org/posters/
