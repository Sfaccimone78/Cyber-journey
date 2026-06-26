---
tipo: entita
tag: [blue-team, tool]
fase: 3
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Volatility (Memory Forensics)"]
---

# Volatility (Memory Forensics)

## Cos'è
**Volatility** è il framework open source di riferimento per la **memory forensics**: l'analisi di un dump della RAM (`memory.raw`, `.vmem`, ibernazione). La memoria contiene ciò che il disco non mostra — processi in esecuzione, connessioni di rete, malware fileless, chiavi e password in chiaro — ed è una fonte chiave nell'[[Incident Response]].

## Acquisizione del dump
Prima di analizzare serve catturare la RAM (con strumenti dedicati, a sistema acceso):
```text
WinPmem / DumpIt / FTK Imager   (Windows)
LiME, avml                      (Linux)
```

## Uso tipico (Volatility 3)
```bash
# Elenco dei processi
vol -f memory.raw windows.pslist

# Processi nascosti (confronto liste)
vol -f memory.raw windows.psscan

# Connessioni di rete al momento del dump
vol -f memory.raw windows.netscan

# Command line dei processi (utile per individuare payload)
vol -f memory.raw windows.cmdline

# Dump di un processo sospetto per analisi successiva
vol -f memory.raw windows.dumpfiles --pid 1337
```

## Quando si usa
- **Incident Response**: ricostruire cosa girava su un host compromesso.
- **Analisi malware fileless** (che vive solo in RAM e non lascia file).
- Recuperare [[Indicatori di Compromissione (IOC)]]: IP di C2, processi malevoli, DLL injection.
- Esercizi DFIR su TryHackMe/[[LetsDefend]].

## Note e trucchi
- Volatility 3 individua il profilo automaticamente (Vol 2 richiedeva `--profile`).
- Confrontare `pslist` (lista ufficiale) con `psscan` (scansione strutture) rivela processi **nascosti** da rootkit.
- Si combina con [[YARA]] (`windows.vadyarascan`) per cercare firme nei processi in memoria.

## Collegamenti
- [[Incident Response]]
- [[Analisi Malware di Base]]
- [[Indicatori di Compromissione (IOC)]]
- [[YARA]]
- [[LetsDefend]]

## Fonti
- Volatility Foundation: https://www.volatilityfoundation.org/
- Volatility 3 documentation: https://volatility3.readthedocs.io/
- HackTricks — Volatility cheatsheet: https://book.hacktricks.xyz/generic-methodologies-and-resources/basic-forensic-methodology/memory-dump-analysis/volatility-cheatsheet
