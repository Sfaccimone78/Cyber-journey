---
tipo: concetto
tag: [linux]
fase: 1
fonti: 5
aggiornato: 2026-07-02
stato: maturo
aliases: ["Processi Linux", "Processi e Job Control"]
---

# Processi Linux

## In breve

Un **processo** è un programma in esecuzione con uno spazio di memoria dedicato, un set di descrittori di file e un'identità utente. Quando lanci un comando, il kernel crea un processo tramite la syscall `fork()` + `exec()`, gli assegna un **PID** univoco e lo inserisce in un albero gerarchico. Ogni processo eredita l'identità e i [[Permessi Linux]] del genitore, rendendo la catena di esecuzione critica per la sicurezza.

---

## Meccanismo interno

### fork() ed exec()

Quando una shell lancia un comando, avviene sempre questa sequenza:
1. `fork()` — il processo padre si duplica: il figlio ottiene una copia dello spazio di memoria (*copy-on-write*).
2. `exec()` — il figlio sostituisce la propria immagine con il nuovo programma (es. `/bin/ls`).
3. Il padre chiama `wait()` per raccogliere il codice di uscita del figlio; senza di essa il figlio diventa **zombie**.

```
systemd (PID 1)
  └─ bash (PID 1042)
       └─ ls (PID 1043)   ← fork + exec
```

### PID e PPID

| Campo | Descrizione |
|---|---|
| `PID` | Process ID univoco nel sistema |
| `PPID` | Parent PID — chi ha creato questo processo |
| `UID / EUID` | User ID reale / effettivo (cambiano con [[SUID e SGID]]) |
| `GID / EGID` | Group ID reale / effettivo |

Il sistema espone tutto questo in **`/proc/<PID>/`**:
```
/proc/1234/
├── status        # PID, PPID, UID, GID, stato
├── cmdline       # riga di comando (NUL-separated)
├── exe           # symlink al binario
├── fd/           # descrittori di file aperti
├── maps          # mappatura della memoria
└── environ       # variabili d'ambiente
```

---

## Stati di un processo

| Stato | Lettera | Significato |
|---|---|---|
| Running | R | In esecuzione o in runqueue |
| Sleeping (interruptible) | S | In attesa di I/O, riceve segnali |
| Sleeping (uninterruptible) | D | Attesa kernel I/O bloccante (es. NFS); non killabile |
| Stopped | T | Fermato da `SIGSTOP` o da un debugger |
| Zombie | Z | Terminato, padre non ha chiamato `wait()` |
| Idle | I | Thread del kernel inattivo |

Un processo bloccato in stato **D** per minuti è spesso sintomo di problemi di storage/rete.

---

## Segnali

I segnali sono interrupt software asincroni inviati a un processo:

| Segnale | Numero | Comportamento default |
|---|---|---|
| `SIGHUP` | 1 | Hangup: ricarica config (demoni) o termina |
| `SIGINT` | 2 | Interrupt da tastiera (Ctrl+C) |
| `SIGQUIT` | 3 | Quit con core dump (Ctrl+\\) |
| `SIGKILL` | 9 | Terminazione immediata — **non ignorabile, non intercettabile** |
| `SIGTERM` | 15 | Terminazione elegante — gestibile dal processo |
| `SIGSTOP` | 19 | Sospensione — **non ignorabile** |
| `SIGCONT` | 18 | Riprendi processo sospeso |
| `SIGUSR1/2` | 10/12 | Segnali custom definiti dall'applicazione |

```bash
kill -15 1234        # SIGTERM (preferibile: lascia tempo di cleanup)
kill -9 1234         # SIGKILL (ultima risorsa)
kill -1 $(pidof nginx)  # SIGHUP → nginx ricarica configurazione
killall -HUP sshd    # manda SIGHUP a tutti i processi "sshd"
pkill -u www-data    # termina tutti i processi dell'utente www-data
```

---

## Comandi di monitoraggio

### ps — snapshot istantaneo

```bash
ps aux                         # tutti i processi, formato BSD
ps -ef                         # formato UNIX (mostra PPID)
ps -eo pid,ppid,user,stat,comm # output personalizzato
ps aux --sort=-%cpu | head     # ordina per CPU decrescente
ps aux --sort=-%mem | head     # ordina per memoria
```

Colonne chiave di `ps aux`:
| Colonna | Significato |
|---|---|
| `USER` | Utente proprietario |
| `PID` | Process ID |
| `%CPU` / `%MEM` | Utilizzo CPU / memoria |
| `VSZ` | Virtual memory size (KB) |
| `RSS` | Resident Set Size — RAM fisica usata |
| `STAT` | Stato (R, S, D, Z, T) |
| `START` | Ora di avvio |
| `COMMAND` | Comando completo |

### top / htop — monitor interattivo

```bash
top                  # monitor real-time (aggiorna ogni 3s)
# In top: 'k' = kill, 'r' = renice, 'u' = filtra per utente, 'q' = esci

htop                 # versione avanzata: albero, mouse, colori
# F5 = tree view, F6 = ordina, F9 = kill
```

### Altri strumenti

```bash
pgrep -u root ssh              # PID dei processi ssh dell'utente root
pstree -p                      # albero con PID
lsof -p 1234                   # file aperti dal processo 1234
lsof -i :80                    # processo che ascolta sulla porta 80
ss -tlnp                       # socket TCP in ascolto con PID
/proc/1234/cmdline             # riga di comando (tr '\0' ' ' per leggere)
cat /proc/1234/status          # stato dettagliato
```

---

## Job control — background e foreground

La shell offre un meccanismo per gestire processi in background senza aprire nuovi terminali:

```bash
sleep 300 &          # avvia in background, shell mostra [1] PID
jobs                 # elenca job in background: [1]+ Running
fg %1                # riporta job 1 in foreground
bg %1                # riprende un job sospeso in background
Ctrl+Z               # sospende il processo in foreground (SIGSTOP)
Ctrl+C               # termina il processo in foreground (SIGINT)

# Resistere alla chiusura del terminale
nohup ./script.sh &          # ignora SIGHUP, output → nohup.out
disown %1                    # rimuove il job dalla lista della shell
```

### Demoni e systemd

I **demoni** sono processi che girano in background senza terminale di controllo (PPID = 1 dopo doppio fork). In sistemi moderni sono gestiti da `systemd`:

```bash
systemctl status nginx       # stato del servizio
systemctl list-units --type=service --state=running   # servizi attivi
journalctl -u nginx -n 50    # ultimi 50 log di nginx
systemctl show nginx -p MainPID   # PID del processo principale
```

---

## Priorità e niceness

Lo scheduler del kernel assegna CPU in base alla **niceness**: un processo "nice" (valore alto, fino a +19) cede volentieri la CPU agli altri; valori bassi (fino a -20, solo root) gli danno priorità. In `ps`/`top` uno stato `<` indica alta priorità (meno nice), `N` bassa.

```bash
nice -n 10 ./batch.sh        # avvia con niceness +10 (bassa priorità)
renice -n 5 -p 1234          # cambia la niceness di un processo già in esecuzione
renice -n -5 -p 1234         # alza la priorità (richiede root per valori negativi)
```

---

## Best practice (server, 2025-2026)

- **`systemctl` ha sostituito `init`/gestione manuale dei daemon**: per i servizi persistenti usa `systemctl status/start/stop/restart <servizio>` e `journalctl -u <servizio>` per i log.
- Per task long-running su server preferisci un **service systemd** o un multiplexer di terminale (**tmux**/**screen**) a `nohup &`: sopravvivono alla disconnessione e sono **riattaccabili** (puoi tornare alla sessione).
- `htop`/`btop` offrono filtri, vista ad albero e kill interattivo migliori di `top`.
- **Non passare segreti come argomenti** da riga di comando: sono visibili a *tutti* gli utenti in `ps aux` e in `/proc/<pid>/cmdline`. Usa variabili d'ambiente, file con permessi stretti o stdin.

---

## Rilevanza offensiva e difensiva

### Incident Response — processi sospetti

```bash
# Processi avviati da utenti non di sistema
ps aux | awk '$1 != "root" && $1 != "www-data" {print}'

# Processi con cmdline vuota o offuscata (malware comune)
for pid in /proc/[0-9]*/cmdline; do
  cmd=$(cat "$pid" 2>/dev/null | tr '\0' ' ')
  [ -z "$cmd" ] && echo "Empty cmdline: $pid"
done

# Processi con socket di rete aperti (possibile reverse shell)
ss -tlnp
lsof -i -n -P | grep ESTABLISHED

# Processo con exe cancellato (binario eliminato dopo esecuzione)
ls -la /proc/*/exe 2>/dev/null | grep deleted

# Albero dei processi per vedere parent sospetti
pstree -pa | grep -A2 -B2 python
```

### Reverse shell tramite sostituzione di processo

Un attaccante può nascondere una [[Reverse Shell e Bind Shell]] in un processo con nome legittimo usando tecniche di *process name spoofing* (argv[0] manipulation) o lanciando il payload da un processo padre attendibile (es. Apache). Verifica sempre `cmdline` e `exe` insieme:

```bash
cat /proc/<PID>/cmdline | tr '\0' '\n'   # comando reale
ls -la /proc/<PID>/exe                   # binario su disco
```

### Escalation tramite processi

- Un processo con EUID 0 e vulnerabilità di buffer overflow → shell root.
- Processi che leggono file controllabili dall'attaccante (race condition TOCTOU).
- Processes che ereditano environment variables malevole (vedi [[Variabili d'Ambiente]]).
- I [[Cron e Job Pianificati]] sono processi lanciati automaticamente come root.

### Hardening

- Usa `ulimit` per limitare risorse per processo (file aperti, memoria).
- `setrlimit()` e cgroups per isolare processi critici.
- Abilita auditd per tracciare `execve()` (lancio nuovi processi).
- Considera AppArmor/SELinux per confinare i demoni in profile mandatory access control.

---

## Troubleshooting comune

| Sintomo | Diagnosi | Soluzione |
|---|---|---|
| Processo in stato D indefinito | `lsof -p PID` — I/O bloccato | Riavviare il servizio di storage; reboot se NFS hung |
| Zombie in aumento | padre non chiama `wait()` | Riavviare il processo padre |
| CPU al 100% da un processo | `top`, poi `strace -p PID` | Profilare, killare se runaway |
| Porta occupata al riavvio | `ss -tlnp`, `lsof -i :PORTA` | Identificare il processo, fermarlo prima |
| Processo non killabile con -9 | Stato D (kernel wait) | Solo reboot risolve |

---

## Lab

- **TryHackMe — Linux Fundamentals Part 2/3**: gestione processi, `ps`, `top`, job control e servizi systemd.
- **TryHackMe — Intro to Logs / Investigating Windows** (parte Linux IR): individua processi sospetti e reverse shell via `/proc` e `ss`.
- **OverTheWire — Bandit** (livelli con processi/servizi in background): pratica `ps`, segnali e job control.

## Domande da esame/colloquio

**Q1: Qual è la differenza tra SIGTERM e SIGKILL?**
SIGTERM (15) è intercettabile: il processo può fare cleanup prima di uscire. SIGKILL (9) è non intercettabile e non ignorabile: il kernel termina forzatamente il processo senza dargli tempo di cleanup. Si usa SIGKILL solo se SIGTERM non funziona.

**Q2: Cos'è un processo zombie e perché è problematico?**
Un processo che ha terminato l'esecuzione ma il cui entry nella tabella dei processi non è stato ancora rimosso perché il padre non ha chiamato `wait()`. Non consuma CPU né memoria, ma occupa un PID. Molti zombie indicano un bug nel processo padre.

**Q3: Come identifichi una reverse shell attiva su un sistema Linux?**
Con `ss -tlnp` o `lsof -i -n -P | grep ESTABLISHED` per trovare connessioni uscenti inattese. Poi verifico `/proc/<PID>/cmdline`, `/proc/<PID>/exe` e il PPID per capire chi ha lanciato il processo.

**Q4: Come si passa un processo in background e come lo si riporta in foreground?**
Si aggiunge `&` al comando oppure si preme Ctrl+Z (sospende) poi `bg`. Per riportarlo in foreground: `fg %N` dove N è il numero del job mostrato da `jobs`.

**Q5: Cosa contiene `/proc/<PID>/` e perché è utile in un'investigazione?**
Contiene lo stato completo del processo: `cmdline` (argomenti), `exe` (symlink al binario), `fd/` (file aperti), `environ` (environment variables), `maps` (layout memoria), `status` (UID, GID, stato). Permette di analizzare processi senza dipendere da tool che possono essere sostituiti da un attaccante (rootkit).

**Q6: Qual è la differenza tra UID reale e UID effettivo?**
L'UID reale identifica chi ha lanciato il processo. L'UID effettivo determina i permessi effettivi durante l'esecuzione. Il bit [[SUID e SGID]] cambia l'EUID al proprietario del file, non all'utente che lo lancia — è questo che consente l'escalation.

---

## Collegamenti

- [[Permessi Linux]]
- [[SUID e SGID]]
- [[Cron e Job Pianificati]]
- [[Privilege Escalation Linux]]
- [[Filesystem Linux]]
- [[Variabili d'Ambiente]]
- [[Reverse Shell e Bind Shell]]
- [[Capabilities Linux]]
- [[Bash Scripting]]

## Fonti

- Man page ps(1): https://man7.org/linux/man-pages/man1/ps.1.html
- Man page signal(7): https://man7.org/linux/man-pages/man7/signal.7.html
- Man page proc(5): https://man7.org/linux/man-pages/man5/proc.5.html
- The Linux Command Line – cap. 10 "Processes" (niceness, job control); man systemctl
- linuxjourney.com — sezione "Processes"
