---
tipo: concetto
tag: [blue-team, metodologia]
fase: 3
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["Disk Forensics e Timeline Analysis", "Timeline Analysis", "Disk Forensics"]
---

# Disk Forensics e Timeline Analysis

## In breve
La **disk forensics** ricostruisce l'attività dal file system: file creati/modificati/cancellati,
spazio non allocato, metadati. La tecnica regina è la **timeline analysis** — fondere tutti i
timestamp degli artefatti in un'unica linea temporale ordinata, così l'attività dell'attaccante
emerge come una **sequenza coerente** ("super timeline"). È il modo in cui un analista risponde a
*cosa è successo, in che ordine e quando*.

## Concetti del file system NTFS
- **MFT (Master File Table)**: ogni file/cartella ha un record. Cuore della disk forensics su Windows.
- **Timestamp MACB** (per i due attributi `$STANDARD_INFORMATION` e `$FILE_NAME`):
  - **M** odified · **A** ccessed · **C** hanged (record MFT) · **B** orn (creation).
- **Timestomping**: tecnica anti-forense (MITRE **T1070.006**) che falsifica i timestamp di
  `$STANDARD_INFORMATION`. Difesa: i timestamp `$FILE_NAME` sono modificabili solo dal kernel →
  una **discrepanza SI vs FN** smaschera il timestomping.
- **Slack space / unallocated**: residui recuperabili con **file carving** (es. `scalpel`,
  `photorec`, `foremost`) anche dopo la cancellazione.
- **USN Journal / `$LogFile`**: registrano operazioni sul file system → ricostruzione fine.

## Metodologia — costruire una super timeline
1. Monta l'immagine **read-only** (loop + write blocker) o usa direttamente l'E01/RAW.
2. Estrai i body file e gli artefatti con **Plaso** (`log2timeline`).
3. Filtra per finestra temporale dell'incidente (riduce milioni di eventi a centinaia).
4. **Pivota** sugli artefatti chiave (esecuzione, persistenza, lateral movement).
5. Correla con i log e con la RAM (vedi [[Memory Forensics con Volatility]]).

## Esempio pratico — Plaso / The Sleuth Kit
```bash
# --- The Sleuth Kit: timeline classica MAC dalla MFT ---
fls -r -m C: -o 2048 host12.raw > bodyfile.txt     # -o = offset partizione (settori)
mactime -b bodyfile.txt -d 2026-06-20..2026-06-26 > timeline.csv

# --- Plaso (super timeline: MFT + registro + EVTX + prefetch + browser + ...) ---
log2timeline.py --storage-file host12.plaso host12.raw
# Filtra ed esporta in CSV ordinato (formato l2tcsv)
psort.py -o l2tcsv -w super_timeline.csv host12.plaso \
  "date > '2026-06-25 00:00:00' AND date < '2026-06-26 23:59:59'"

# --- File carving su spazio non allocato ---
photorec host12.raw            # recupero per signature
tsk_recover -e host12.raw out/ # recupero file cancellati via TSK
```

Lettura della timeline (estratto): la sequenza racconta la storia.
```text
2026-06-25 09:14  Browser download   invoice.zip            (initial access)
2026-06-25 09:15  Prefetch           WINWORD.EXE-xxxx.pf     (apertura allegato)
2026-06-25 09:15  MFT born           %TEMP%\update.exe       (drop payload)
2026-06-25 09:16  Registry Run key   HKCU\...\Run = update   (persistenza T1547)
2026-06-25 09:18  Prefetch           PSEXEC.EXE / WMIC.EXE   (lateral movement)
```

## Artefatti di esecuzione su disco (oltre la MFT)
| Artefatto | Cosa prova | Percorso/sorgente |
|---|---|---|
| **Prefetch** | esecuzione + n. run + ultima esecuzione | `C:\Windows\Prefetch\*.pf` |
| **Amcache.hve** | binari eseguiti + hash SHA1 | `C:\Windows\AppCompat\Programs\Amcache.hve` |
| **Shimcache (AppCompatCache)** | presenza/esecuzione binari | hive `SYSTEM` |
| **USN Journal** | ogni create/rename/delete | `$Extend\$UsnJrnl` |
| **$LogFile** | transazioni NTFS recenti | radice volume |

> [!warning] Anti-forensics
> Wiping, timestomping e cancellazione log puntano a spezzare la timeline. La **ridondanza** degli
> artefatti è la difesa: prefetch, amcache, shimcache, USN e MFT raccontano la stessa esecuzione da
> angoli diversi — l'attaccante deve ripulirli **tutti** per sparire.

## Checklist disk forensics
- [ ] Immagine verificata via hash (vedi [[Digital Forensics Fondamenti]]).
- [ ] Monta read-only; non scrivere mai sull'originale.
- [ ] Genera super timeline (Plaso) e restringi alla finestra dell'incidente.
- [ ] Controlla discrepanze SI/FN (timestomping).
- [ ] Recupera file cancellati e analizza unallocated/slack.
- [ ] Correla con RAM, EVTX e telemetria [[Sysmon]].

## Lab
- **CyberDefenders** — *Hammered*, *NintendoHunt*, *DefCon DFIR* (immagini disco reali).
- **TryHackMe** — *Disk Analysis & Autopsy*, *Windows Forensics 1/2*.
- **BlueTeamLabs.online** — investigations con artefatti su disco.
- **Autopsy / TSK** — tool GUI/CLI gratuiti per esercitarsi.

## Domande
**D: Cos'è una super timeline?**
R: L'aggregazione cronologica di **tutti** gli artefatti temporali (MFT, log eventi, registry, browser,
prefetch) in un'unica linea del tempo, generata con `log2timeline`/**plaso** → ricostruisce la sequenza.

**D: Cosa sono i timestamp MACB e quale rischio comportano?**
R: Modified, Accessed, Changed (MFT), Born/created. Servono a ricostruire l'attività, ma sono
falsificabili (**timestomping**): la discrepanza tra `$STANDARD_INFORMATION` e `$FILE_NAME` è un IOC.

**D: Cos'è il file carving?**
R: Recuperare file dai dati grezzi tramite firme (header/footer) **senza** affidarsi ai metadati del
filesystem → utile per dati cancellati o partizioni corrotte.

## Collegamenti
- [[Digital Forensics Fondamenti]]
- [[Windows Forensics (artefatti)]]
- [[Memory Forensics con Volatility]]
- [[Log Analysis Avanzata e Correlazione]]
- [[Indicatori di Compromissione (IOC)]]
- [[MITRE ATT&CK]]

## Fonti
- Plaso / log2timeline documentation: https://plaso.readthedocs.io/
- The Sleuth Kit & Autopsy: https://www.sleuthkit.org/
- SANS — Windows Forensic Analysis (FOR500) poster: https://www.sans.org/posters/windows-forensic-analysis/
- The DFIR Report (timeline reali di intrusioni): https://thedfirreport.com/
