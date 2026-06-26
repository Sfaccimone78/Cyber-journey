---
tipo: entita
tag: [tool]
fase: 2
fonti: 2
aggiornato: 2026-06-21
stato: maturo
aliases: ["Meterpreter"]
---

# Meterpreter

> **Nota etica**: solo lab autorizzati o engagement con permesso scritto.

## In breve
**Meterpreter** è il **payload avanzato di [[Metasploit]]**: una shell post-exploitation che vive **in memoria** (no file su disco), comunica cifrata col tuo handler e si estende a runtime con moduli, senza riavviare il processo. Rispetto a una [[Reverse Shell e Bind Shell|reverse shell]] grezza, offre filesystem, gestione processi, port forwarding, dumping credenziali e [[Pivoting]] integrati.

## Come funziona (meccanismo)
1. Un **payload stager** piccolo prende piede sul target e scarica il **core** Meterpreter via il canale cifrato (TLS).
2. Il core gira **in-memory**, iniettato in un processo: nessun binario su disco → meno tracce.
3. I comandi caricano **estensioni** (`stdapi`, `priv`, `kiwi`) on-demand sullo stesso canale.

**Staged vs stageless**: `windows/x64/meterpreter/reverse_tcp` (staged, payload piccolo) vs `..._reverse_tcp` con `meterpreter_reverse_https` stageless (un blob unico, più affidabile attraverso firewall). Vedi [[msfvenom]] per generarli.

## Comandi essenziali
```
# Sessione
sysinfo            getuid            background      sessions -i 1

# Filesystem / processi
ls  cd  download <f>  upload <f>     ps   migrate <pid>   kill <pid>

# Privesc & credenziali
getsystem                      # tenta elevazione a SYSTEM
load kiwi ; creds_all          # Mimikatz integrato
hashdump                       # dump SAM

# Pivoting (vedi [[Pivoting]])
run autoroute -s 10.10.20.0/24
portfwd add -l 3389 -p 3389 -r 10.10.20.5
```

> [!tip] migrate appena puoi
> Il processo iniziale può chiudersi (es. l'exploit di un servizio che crasha). `migrate` verso un processo stabile (`explorer.exe`, `winlogon.exe`) mantiene la sessione viva e cambia il contesto utente.

## Detection
- **Molto** rilevato dagli EDR moderni ([[EDR e XDR]]): firma in memoria, named pipe note, `migrate`/iniezione (`CreateRemoteThread`), traffico TLS verso porte anomale.
- MITRE: **T1055** (Process Injection), **T1071** (Application Layer Protocol), **T1003** (credential dumping).

## Collegamenti
- [[Metasploit]] — framework che lo lancia
- [[msfvenom]] — genera i payload Meterpreter standalone
- [[Reverse Shell e Bind Shell]] · [[Pivoting]] · [[Post-Exploitation]]
- [[Mimikatz]] — `load kiwi` · [[EDR e XDR]]

## Fonti
- Offensive Security — Meterpreter: https://docs.metasploit.com/docs/using-metasploit/advanced/meterpreter/about-the-metasploit-meterpreter.html
- Rapid7 — Meterpreter basics: https://www.rapid7.com/blog/post/2015/06/04/an-introduction-to-meterpreter/
