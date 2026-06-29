---
tipo: entita
tag: [linux]
fase: 1
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["find"]

---

# find

## Cos'è

**find** è il comando Linux per cercare file e directory nel filesystem in base a uno o più criteri: nome, tipo, permessi, proprietario, dimensione, data di modifica e altro. A differenza di `locate` (che usa un database pre-compilato), find interroga il filesystem in tempo reale e può eseguire azioni sui risultati tramite `-exec`. È uno strumento fondamentale per l'[[Enumerazione]] e per la fase di [[Privilege Escalation Linux]].

Sintassi generale:
```bash
find <percorso_di_partenza> [opzioni] [test] [azioni]
```

---

## Flag e predicati principali

### Filtri per nome e tipo

| Predicato | Significato | Esempio |
|-----------|-------------|---------|
| `-name "pattern"` | Nome file (case-sensitive, glob) | `find / -name "passwd"` |
| `-iname "pattern"` | Nome file (case-insensitive) | `find / -iname "*.conf"` |
| `-type f` | File regolari | `find /tmp -type f` |
| `-type d` | Directory | `find / -type d -name "backup"` |
| `-type l` | Link simbolici | `find / -type l` |
| `-type s` | Socket | `find /tmp -type s` |
| `-path "pattern"` | Path completo (glob) | `find / -path "*/config/*.env"` |
| `-not` / `!` | Negazione di un predicato | `find / -not -name "*.log"` |
| `-o` | OR logico tra predicati | `find / \( -name "*.sh" -o -name "*.py" \)` |

### Filtri per permessi

| Predicato | Significato | Esempio |
|-----------|-------------|---------|
| `-perm mode` | Permessi esatti | `find / -perm 777` |
| `-perm -mode` | Almeno questi bit attivi (AND) | `find / -perm -4000` (SUID) |
| `-perm /mode` | Almeno uno di questi bit (OR) | `find / -perm /6000` (SUID o SGID) |
| `-perm -o+w` | Scrivibile da others | `find / -perm -o+w -type f` |
| `-perm -u+s` | SUID attivo | equivalente a `-perm -4000` |
| `-perm -g+s` | SGID attivo | equivalente a `-perm -2000` |

### Filtri per proprietario e gruppo

```bash
find / -user root          # file di proprietà di root
find / -group shadow       # file del gruppo shadow
find / -nouser             # file senza proprietario (UID orfano — sospetto)
find / -nogroup            # file senza gruppo valido
find / -user www-data -type f   # file del webserver
```

### Filtri per dimensione

```bash
find / -size +10M          # file più grandi di 10 MB
find / -size -1k           # file più piccoli di 1 KB
find /home -size +100M     # dump o archivi grandi in home
find /tmp -size 0          # file vuoti (placeholder sospetti)
```

Unità: `c` (byte), `k` (KiB), `M` (MiB), `G` (GiB). Il prefisso `+` = "maggiore di", `-` = "minore di", nessun prefisso = "esattamente".

### Filtri per data

```bash
find / -mmin -10           # modificati negli ultimi 10 minuti
find / -mmin +60           # modificati più di 60 minuti fa
find / -mtime -1           # modificati nelle ultime 24 ore (1 giorno)
find / -mtime +30          # modificati più di 30 giorni fa
find / -newer /etc/passwd  # modificati dopo /etc/passwd
find / -atime -1           # acceduti nelle ultime 24 ore
find / -ctime -1           # cambiati (inode/metadata) nelle ultime 24 ore
```

> [!tip] `-newer` è utile in incident response: `find / -newer /var/log/auth.log` trova tutto ciò che è stato toccato dopo un certo evento.

---

## Azioni sui risultati

### `-exec` e `-execdir`

```bash
# Esegui un comando per ogni file trovato
# {} = placeholder per il file corrente; \; = termine del comando
find /home -name "*.sh" -exec chmod -x {} \;

# Più efficiente: + raggruppa i file in un'unica invocazione del comando (come xargs)
find /home -name "*.log" -exec rm {} +

# -execdir esegue nella directory del file trovato (più sicuro vs path injection)
find / -name "*.py" -execdir python3 {} \;

# Visualizzare con ls -la ogni file trovato
find /tmp -type f -exec ls -la {} \;
```

### `-exec` vs `xargs`

```bash
# xargs è spesso più veloce perché raggruppa le invocazioni
find /var/log -name "*.log" | xargs grep "FAILED"

# Con file che hanno spazi o caratteri speciali nel nome, usa -print0 e xargs -0
find /home -name "*.txt" -print0 | xargs -0 grep -l "password"

# xargs con un numero fisso di argomenti (-n)
find . -name "*.bak" -print0 | xargs -0 -n 1 rm -v
```

### `-delete`

```bash
# Elimina i file trovati (ATTENZIONE: irreversibile)
find /tmp -name "*.tmp" -mtime +7 -delete
```

### `-printf` e `-ls`

```bash
# Output personalizzato: nome, permessi ottali, proprietario, dimensione
find / -type f -perm -4000 -printf "%M %u %g %p\n" 2>/dev/null

# Elenca in formato ls -l
find /etc -name "*.conf" -ls
```

---

## Uso in Privilege Escalation Linux

Questa è la sezione più importante per il pentest. Cercare configurazioni errate dei permessi è uno dei passi fondamentali nella fase post-sfruttamento.

```bash
# ========== SUID: eseguibili che girano come root ==========
find / -perm -4000 -type f 2>/dev/null
# Output tipico: /usr/bin/passwd, /usr/bin/sudo, /usr/bin/find, ecc.
# Ogni binario SUID va verificato su GTFOBins

# ========== SGID ==========
find / -perm -2000 -type f 2>/dev/null

# ========== SUID + SGID insieme ==========
find / -perm /6000 -type f 2>/dev/null

# ========== File world-writable ==========
find / -perm -o+w -type f 2>/dev/null | grep -vE "^/proc|^/sys|^/dev"
# Script in /etc/cron.d, /etc/init.d, /opt scrivibili = privesc facile

# ========== Directory world-writable ==========
find / -perm -o+w -type d 2>/dev/null | grep -vE "^/proc|^/sys|^/tmp|^/dev"

# ========== File di proprietà di root scrivibili dall'utente corrente ==========
find / -user root -writable -type f 2>/dev/null | grep -vE "^/proc|^/sys"

# ========== File senza proprietario (UID orfano) ==========
find / -nouser -type f 2>/dev/null
# Può indicare file di un utente eliminato — potenzialmente riutilizzabile

# ========== File di configurazione con password ==========
find / -name "*.conf" -o -name "*.env" -o -name "*.ini" 2>/dev/null | \
  xargs grep -l "password\|passwd\|secret" 2>/dev/null

# ========== Chiavi SSH private ==========
find / -name "id_rsa" -o -name "id_ecdsa" -o -name "*.pem" 2>/dev/null

# ========== Capabilities (alternativa a SUID) ==========
# find non le mostra direttamente, usa getcap
getcap -r / 2>/dev/null

# ========== GTFOBins trick con sudo find ==========
sudo find . -exec /bin/sh \; -quit
# Se find è nel sudoers senza restrizioni → shell root immediata
```

---

## Uso in Incident Response e Forensics

```bash
# File modificati nelle ultime 24 ore (incident response)
find / -mtime -1 -type f 2>/dev/null | grep -vE "^/proc|^/sys|^/run"

# File creati dopo un certo timestamp (dopo la compromissione)
find / -newer /var/log/auth.log -type f 2>/dev/null

# File nascosti (iniziano con .)
find /home -name ".*" -type f

# Script nascosti in directory temporanee
find /tmp /var/tmp /dev/shm -type f -name "*.sh" -o -name "*.py" 2>/dev/null

# File SUID modificati di recente (potrebbe indicare escalation)
find / -perm -4000 -mtime -7 -type f 2>/dev/null

# Cercare webshell PHP
find /var/www -name "*.php" -newer /var/www/html/index.php 2>/dev/null
find /var/www -name "*.php" -exec grep -l "shell_exec\|base64_decode" {} \;
```

---

## Ottimizzazione e performance

```bash
# Limita la profondità di ricerca con -maxdepth
find / -maxdepth 3 -name "*.env" 2>/dev/null

# -mindepth: salta i livelli iniziali
find / -mindepth 2 -maxdepth 4 -perm -4000 2>/dev/null

# Ordina per dimensione decrescente (pipe a sort)
find /var -type f -printf "%s %p\n" 2>/dev/null | sort -rn | head -20

# Escludere directory specifiche con -prune
find / -path /proc -prune -o -path /sys -prune -o -perm -4000 -print 2>/dev/null

# Trovare i file più recentemente modificati
find / -type f -printf "%T@ %p\n" 2>/dev/null | sort -rn | head -20 | awk '{print $2}'
```

---

## Casi limite e gotcha

- **`-perm -4000` vs `-perm 4000`**: il trattino è fondamentale. `-4000` significa "il bit SUID è attivo tra gli altri"; `4000` (senza trattino) significa "i permessi sono esattamente 4000" — pochissimi file li avranno.
- **`{}` e la shell**: in alcuni contesti `{}` viene espanso dalla shell. Se usi `-exec sh -c 'comando {}' \;` fai attenzione: un attaccante che controlli il nome del file può iniettare comandi. Usa invece `-exec sh -c 'comando "$1"' _ {} \;`.
- **`-exec cmd {} +`**: raggruppa i file in un'unica invocazione, come `xargs`. Molto più veloce di `\;` su grandi insiemi di file.
- **`-delete`**: non va usato prima di aver testato la query senza `-delete`. Elimina i file senza passare per il cestino.
- **`-mtime` vs `-mmin`**: `-mtime` usa giorni (24h), `-mmin` usa minuti. `-mtime -1` = ultime 24 ore, non "ieri".
- **Symlink**: di default find non segue i symlink nelle directory. Usa `-L` come prima opzione per seguirli: `find -L / -perm -4000`.
- **`/proc` e `/sys`**: contengono pseudofile che possono causare comportamenti anomali (loop, blocchi). Escludili sempre con `-prune` o filtrando l'output con `grep -vE "^/proc|^/sys"`.

---

## Lab

- **TryHackMe — Linux PrivEsc**: usa `find / -perm -4000` per individuare i binari SUID e sfruttarli via GTFOBins.
- **OverTheWire — Bandit** (livelli con file per size/owner/permessi): risolvibili direttamente con i predicati di `find`.
- **HackTheBox — Starting Point**: enumerazione SUID/world-writable in macchine reali.

## Domande da esame/colloquio

> **D: Come trovi tutti i file SUID nel sistema con find? Perché è importante per il privesc?**
> `find / -perm -4000 -type f 2>/dev/null`. Il bit SUID fa eseguire il binario con i privilegi del proprietario (tipicamente root) invece di quelli dell'utente che lo lancia. Se un binario SUID è in GTFOBins (es. `find`, `vim`, `python`, `nmap`), si può ottenere una shell root senza sudo.

> **D: Qual è la differenza tra `-exec cmd {} \;` e `-exec cmd {} +`?**
> Con `\;` find invoca il comando una volta per ogni file trovato. Con `+` raggruppa tutti i file e li passa in un'unica invocazione (come xargs). Il secondo è molto più efficiente su grandi insiemi di file, ma non tutti i comandi accettano più file come argomenti.

> **D: Come usi find per trovare file modificati dopo un evento specifico (es. dopo un accesso sospetto)?**
> `find / -newer /var/log/auth.log -type f 2>/dev/null`. Si crea un file sentinel col timestamp dell'evento, poi si usa `-newer sentinel`. Alternativa: `-mmin -N` dove N è il numero di minuti dall'evento.

> **D: Perché `-perm -o+w` è importante in un audit di sicurezza?**
> File scrivibili da "others" (tutti gli utenti) in posizioni critiche come `/etc/cron.d`, `/usr/local/bin`, `/opt/scripts` permettono a qualunque utente di sostituire il contenuto con codice arbitrario. Se questi file vengono eseguiti da cron o da root, diventano vettori di privesc banali.

> **D: Come usi find in modo sicuro in un cron job per evitare path injection?**
> Usa `-execdir` invece di `-exec` e passa il file come argomento posizionale: `find /tmp -name "*.sh" -execdir bash -- {} \;`. Questo evita che un nome file malformato esca dal contesto della directory e modifichi il comando eseguito.

---

## Confronto find vs locate vs fd

| Caratteristica | `find` | `locate` | `fd` |
|---------------|--------|----------|------|
| Cerca in tempo reale | Si | No (database) | Si |
| Velocità | Media | Molto rapida | Molto rapida |
| Filtro per permessi/proprietario | Si | No | Parziale |
| `-exec` integrato | Si | No | Si (`--exec`) |
| Installazione | Built-in | Richiede `mlocate` | Richiede `fd-find` |
| Caso d'uso pentest | Ideale | Non adatto | Buono per nome |

---

## Collegamenti

- [[grep]]
- [[Pipe e Redirezione]]
- [[Privilege Escalation Linux]]
- [[SUID e SGID]]
- [[sudo]]
- [[Permessi Linux]]
- [[Enumerazione]]
- [[OverTheWire Bandit]]
- [[Bash Scripting]]
- [[Log Analysis]]

## Fonti

- Man page find: https://man7.org/linux/man-pages/man1/find.1.html
- GTFOBins – find: https://gtfobins.github.io/gtfobins/find/
- OverTheWire Bandit: https://overthewire.org/wargames/bandit/
