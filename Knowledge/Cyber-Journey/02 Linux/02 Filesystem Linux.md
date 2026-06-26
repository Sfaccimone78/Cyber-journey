---
tipo: concetto
tag: [linux]
fase: 1
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["Filesystem Linux"]

---

# Filesystem Linux

## In breve

Il **filesystem** di Linux è l'organizzazione gerarchica di tutti i file e le directory del sistema. A differenza di Windows (che usa lettere di unità come `C:\`), Linux parte da un'unica radice chiamata **root**, indicata con `/`, e tutto il resto si ramifica da lì. Lo standard che governa questa struttura è il **FHS (Filesystem Hierarchy Standard)** — sapere dove stanno le cose è fondamentale sia per amministrare un sistema sia per attaccarlo.

---

## FHS: la mappa del sistema

| Directory | Contenuto | Rilevanza sicurezza |
|-----------|-----------|---------------------|
| `/bin` | Comandi di base (ls, cp, mv, cat…) | Contiene binari che possono avere SUID |
| `/sbin` | Comandi amministrativi (reboot, fsck…) | Solo root nella PATH di default |
| `/etc` | File di configurazione del sistema | **Target principale**: passwd, shadow, sudoers, cron, ssh |
| `/home` | Cartelle personali degli utenti | Chiavi SSH, .bash_history, file di config con credenziali |
| `/root` | Home dell'utente root | Solitamente inaccessibile; flag di CTF, chiavi SSH root |
| `/var` | File variabili (log, spool, cache, mail) | `/var/log/` per log analysis; `/var/www/` per web app |
| `/tmp` | File temporanei (spesso cancellati al riavvio) | **Scrivibile da tutti**: usato da attaccanti per staging |
| `/usr` | Programmi e librerie utente | `/usr/bin/`, `/usr/lib/` — shared library hijacking |
| `/lib` e `/lib64` | Librerie condivise del sistema | Vettore di LD_PRELOAD / shared object injection |
| `/proc` | Filesystem virtuale: info sui [[Processi Linux]] | `/proc/[pid]/`, `/proc/net/`, contiene segreti in exec |
| `/sys` | Filesystem virtuale: interfaccia kernel/hardware | Raramente usato in attacco, utile in forensics |
| `/dev` | Dispositivi hardware come file | `/dev/sda` per disk forensics; `/dev/null`, `/dev/zero` |
| `/mnt` e `/media` | Punti di montaggio per dischi esterni / USB | Backup, share NFS, vettori no_root_squash |
| `/opt` | Software di terze parti installato manualmente | Spesso scrivibile: vettore di cron injection |
| `/run` | File di runtime (PID, socket) | Socket Unix sfruttabili per LPE |
| `/srv` | Dati serviti da servizi di rete (HTTP, FTP) | Dipende dalla config; web root alternativa |

---

### Dettagli FHS spesso trascurati

| Directory | Contenuto |
|-----------|-----------|
| `/boot` | kernel (`vmlinuz`), initrd, bootloader (GRUB) |
| `/usr/bin` | gli eseguibili installati dalla **distribuzione** (migliaia) |
| `/usr/local` | software installato **localmente**, non dalla distro (es. compilato da sorgente → `/usr/local/bin`) |
| `/usr/sbin` | altri programmi di amministrazione |
| `/usr/share` | dati condivisi indipendenti dall'architettura (config default, icone, doc) |

> [!note] `/usr`-merge sulle distro moderne
> Le distribuzioni recenti adottano l'**/usr-merge**: `/bin`, `/sbin`, `/lib` sono ormai **symlink** verso `/usr/bin`, `/usr/sbin`, `/usr/lib`. La separazione storica è cosmetica. Regola pratica: **non installare software a mano in `/bin` o `/usr/bin`** (riservate alla distribuzione); software locale → `/usr/local`, pacchetti → il gestore di pacchetti ([[Gestione Pacchetti]]).

> [!tip] Versiona `/etc`
> I file di configurazione in `/etc` sono testo: mettili sotto controllo di versione (`etckeeper` o git) **prima** di modificarli, così ogni cambiamento è tracciabile e reversibile.

---

## Percorsi: assoluti vs relativi

```bash
/etc/passwd           # ASSOLUTO: parte sempre da /
./script.sh           # RELATIVO: rispetto alla directory corrente
../altro/file.txt     # RELATIVO: sale di un livello, poi scende
~/chiavi/id_rsa       # ~ = home dell'utente corrente (espanso dalla shell)
```

La distinzione assoluto/relativo è critica in sicurezza: uno script privilegiato che chiama `ps` (relativo) invece di `/usr/bin/ps` (assoluto) è vulnerabile a [[Privilege Escalation Linux]] via **PATH hijacking**.

---

## Inode: il meccanismo interno

Ogni file in Linux non è solo un nome: il nome è una voce in una **directory** che punta a un **inode**. L'inode contiene:
- Tipo di file (regolare, directory, symlink, socket, pipe…)
- Permessi, UID/GID owner
- Dimensione, timestamp (atime, mtime, ctime)
- Puntatori ai **blocchi dati** sul disco

Il nome del file non è nell'inode: per questo possono esistere più nomi (hard link) per lo stesso inode.

```bash
ls -li /etc/passwd      # -i mostra il numero di inode
stat /etc/passwd        # tutti i metadati: inode, size, timestamp, permessi
```

### Hard link vs Symlink

| | Hard link | Soft link (symlink) |
|-|-----------|---------------------|
| Punta a | Stesso inode | Percorso del file originale |
| Attraversa FS? | No | Sì |
| File eliminato | I dati restano (altri link) | Link "rotto" (dangling) |
| Directory? | No (di solito) | Sì |
| Comando | `ln src dest` | `ln -s src dest` |

```bash
ln /etc/passwd /tmp/hl_passwd          # hard link
ln -s /etc/passwd /tmp/sl_passwd       # symlink
ls -la /tmp/sl_passwd                  # mostra -> /etc/passwd
readlink -f /tmp/sl_passwd             # risolve il path completo
```

---

## `/proc` e `/sys`: i filesystem virtuali

### `/proc` — fotografia del kernel in esecuzione

```bash
cat /proc/version           # versione kernel (utile per cercare exploit)
cat /proc/cpuinfo           # info CPU
cat /proc/meminfo           # memoria disponibile e usata
cat /proc/mounts            # filesystem montati (= mount più veloce)
cat /proc/net/tcp           # connessioni TCP in hex (ss/netstat leggono da qui)
cat /proc/net/arp           # tabella ARP (host vicini)
ls /proc/                   # ogni PID ha una cartella
cat /proc/1/cmdline | tr '\0' ' '     # cmdline del processo con PID 1
cat /proc/self/environ | tr '\0' '\n' # variabili d'ambiente del processo corrente
ls -la /proc/1/fd/          # file descriptor del PID 1 (se hai permessi)
```

> [!tip] Segreti in `/proc`
> Le credenziali passate come argomenti da riga di comando (es. `-p password`) sono visibili in `/proc/[pid]/cmdline` per chiunque possa leggere quella directory. Fonte frequente di credential leakage.

### `/sys` — interfaccia con i driver e l'hardware
Meno usato in attacco, ma in forensics e detection: `/sys/kernel/security/` contiene lo stato di AppArmor/SELinux; `/sys/bus/usb/` rivela dispositivi USB connessi.

---

## Mount e filesystem multipli

```bash
mount                              # mostra tutti i filesystem montati
mount | grep "nosuid\|noexec"      # cerca partizioni con opzioni di hardening
cat /etc/fstab                     # filesystem configurati all'avvio
df -h                              # spazio libero per filesystem
lsblk                              # dispositivi a blocchi e struttura partizioni
findmnt --target /tmp              # opzioni di mount di /tmp (nosuid? noexec?)
```

### Opzioni di mount rilevanti per la sicurezza

| Opzione | Effetto |
|---------|---------|
| `nosuid` | Ignora il bit SUID/SGID sui file in questo mount |
| `noexec` | Impedisce l'esecuzione di file (bypassabile con `bash script.sh`) |
| `nodev` | Ignora i file di dispositivo |
| `ro` | Sola lettura |

> [!tip] Pentest
> `mount | grep /tmp` con `nosuid` significa che anche se copi un binario SUID in `/tmp`, il kernel lo ignora. Usa `/dev/shm` o cerca altre cartelle scrivibili senza `nosuid`.

---

## File sensibili: mappa pentest

### `/etc/` — la miniera d'oro

```bash
cat /etc/passwd          # utenti: nome:x:uid:gid:GECOS:home:shell
cat /etc/shadow          # hash delle password (richiede root/gruppo shadow)
cat /etc/group           # gruppi e membri
cat /etc/sudoers         # chi può fare sudo e come (vettore LPE)
cat /etc/hosts           # DNS locale (rivela host interni)
cat /etc/crontab         # cron di sistema (vettore LPE)
ls /etc/cron.d/          # job cron aggiuntivi
ls /etc/cron.daily/      # script eseguiti giornalmente come root
cat /etc/ssh/sshd_config # config SSH (PermitRootLogin, chiavi autorizzate)
find /etc -name "*.bak" -o -name "*.old" 2>/dev/null  # backup con segreti
```

### Formato `/etc/passwd`
```
nome:password:UID:GID:GECOS:home:shell
root:x:0:0:root:/root:/bin/bash
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```
- `x` nella colonna password = hash in `/etc/shadow`
- Colonna password **vuota** = accesso senza password (misconfiguration grave)
- Shell `/bin/false` o `/usr/sbin/nologin` = account di servizio (non interattivo)

### Chiavi SSH

```bash
find / -name "id_rsa" -o -name "id_ecdsa" -o -name "authorized_keys" 2>/dev/null
cat ~/.ssh/authorized_keys     # chi può loggarsi con chiave
cat ~/.ssh/id_rsa              # chiave privata (se leggibile = golden ticket)
cat /root/.ssh/id_rsa          # chiave root (richiede accesso a /root/)
```

### `/var/` — log e cache

```bash
ls -la /var/log/               # log di sistema
cat /var/log/auth.log          # login SSH, sudo, su (Debian/Ubuntu)
cat /var/log/secure            # equivalente su RHEL/CentOS
cat /var/log/syslog            # log generale del sistema
cat /var/www/html/             # web root: file di config con credenziali DB
find /var -name "*.log" -readable 2>/dev/null   # log leggibili dall'utente
```

### `/tmp` e `/dev/shm` — staging dell'attaccante

```bash
ls -la /tmp/          # scrivibile da tutti, spesso senza nosuid su CTF
ls -la /dev/shm/      # RAM filesystem, volatile, senza nosuid di default
ls -la /var/tmp/      # come /tmp ma NON cancellato al riavvio
```

---

## Permessi del filesystem

I [[Permessi Linux]] si leggono con `ls -la`:
```
-rwxr-xr-- 1 alice devs 1234 Jun 22 10:00 script.sh
│└┬┘└┬┘└┬┘
│ │  │  └─ altri (r--)
│ │  └──── gruppo (r-x)
│ └─────── proprietario (rwx)
└───────── tipo: - file, d directory, l symlink, s socket, p pipe
```

Bit speciali:
- **SUID** (4000): esegue con l'UID del proprietario → vedi [[SUID e SGID]]
- **SGID** (2000): esegue con il GID del gruppo / directory condivisa
- **Sticky bit** (1000): su directory, solo il proprietario può cancellare i propri file (`/tmp`)

```bash
stat /usr/bin/passwd   # bit SUID: -rwsr-xr-x
ls -la /tmp            # sticky bit: drwxrwxrwt
```

---

## Filesystem types rilevanti

```bash
mount | awk '{print $5}' | sort -u    # tipi di filesystem presenti
```

| Tipo | Descrizione |
|------|-------------|
| `ext4` | Filesystem principale Linux (journaled) |
| `tmpfs` | In RAM: `/tmp`, `/run`, `/dev/shm` |
| `proc` | Virtuale: `/proc` |
| `sysfs` | Virtuale: `/sys` |
| `nfs` | Network File System: vettore `no_root_squash` |
| `overlay` | Docker/container: layer su layer |

---

## Sicurezza: uso offensivo vs hardening

### Uso offensivo (red team / pentest)
- Leggere `/etc/passwd` + `/etc/shadow` → crack offline con john/hashcat.
- Trovare chiavi SSH private leggibili → accesso senza password.
- Sfruttare `/tmp` senza `nosuid` per staging di binari SUID.
- `/proc/[pid]/environ` e `/proc/[pid]/cmdline` per credential leakage.
- `find / -writable` per trovare file scrivibili da root (cron, script) → [[Privilege Escalation Linux]].

### Hardening / difesa
- `/tmp` con `nosuid,nodev,noexec` in `/etc/fstab`.
- Permessi stretti su `/etc/shadow` (640, owner root, gruppo shadow).
- `chmod 440 /etc/sudoers`; usa `visudo` per evitare syntax error.
- Audit periodico con `find / -perm -4000 -type f` e rimozione SUID non necessari.
- `auditd` con watch su `/etc/passwd`, `/etc/shadow`, `/etc/sudoers`, `/etc/crontab`.

---

## Casi limite e troubleshooting

1. **File "scomparso" ma il processo lo tiene aperto** → il file è stato cancellato ma l'inode resta finché il processo non chiude il fd. Visibile con `lsof | grep deleted`. Recuperabile leggendo `/proc/[pid]/fd/[n]`.
2. **Filesystem pieno (100%) ma `du` non trova i file** → file cancellati ma tenuti aperti (vedi sopra) occupano spazio. `lsof | grep deleted | awk '{print $7}'` mostra i blocchi usati. Riavviare il processo libera lo spazio.
3. **Symlink loop** → due symlink che si puntano a vicenda danno "Too many levels of symbolic links". `namei -l /percorso` mostra la catena.
4. **Inode esauriti (df -h OK ma no space left)** → `df -i` mostra uso degli inode. Spesso causato da molti file piccoli (sessioni PHP, mail). Non c'è modo di aggiungere inode su ext4 senza riformattare.
5. **`mount` con `noexec` ma posso ancora eseguire** → `noexec` blocca `execve()` su file in quel mount, ma `bash ./script.sh` funziona perché l'eseguibile è `bash` (che sta altrove); il file viene letto, non eseguito.

---

## Domande da esame / colloquio

> **D: Cos'è un inode e cosa contiene?**
> Un inode è la struttura dati del filesystem che descrive un file: permessi, UID/GID, timestamp (atime/mtime/ctime), dimensione e puntatori ai blocchi dati. Non contiene il nome del file, che è invece in una voce di directory. Questo permette ai hard link di puntare allo stesso inode con nomi diversi.

> **D: Perché `/tmp` è interessante per un attaccante?**
> È scrivibile da tutti gli utenti, spesso senza `nosuid` nei CTF, e di solito eseguibile. Permette di depositare binari, script e file temporanei senza permessi elevati. Anche `/dev/shm` è una variante volatile in RAM. In produzione `/tmp` dovrebbe essere montata con `nosuid,nodev,noexec`.

> **D: Cosa trovi in `/proc/[pid]/environ` e perché è rilevante?**
> Le variabili d'ambiente del processo al momento del suo avvio. Possono contenere `DB_PASSWORD`, `API_KEY`, `LD_PRELOAD` impostati dallo script di avvio. Leggibile da tutti se il processo appartiene all'utente, o da root per qualsiasi processo.

> **D: Differenza tra `atime`, `mtime` e `ctime`?**
> `atime` = ultimo accesso (lettura); `mtime` = ultima modifica del contenuto; `ctime` = ultima modifica dei metadati (permessi, owner, hard link). `ls -l` mostra `mtime`; `ls -lc` mostra `ctime`. In forensics, `ctime` non può essere modificato dall'utente normale (a differenza di `touch`).

> **D: Cos'è `no_root_squash` su NFS e come si sfrutta?**
> Opzione in `/etc/exports` che disabilita il mapping dell'UID 0 client → `nobody` (root squashing). Un attaccante root sul proprio box monta la share, ci copia un binario SUID-root: il bit viene rispettato sul server target, ottenendo escalation. Difesa: `root_squash` (default) o `all_squash` + `nosuid` sul mount.

---

## Collegamenti

- [[Permessi Linux]]
- [[Utenti e Gruppi Linux]]
- [[Privilege Escalation Linux]]
- [[Processi Linux]]
- [[Comandi Linux di Base]]
- [[find]]
- [[SUID e SGID]]
- [[Cron e Job Pianificati]]
- [[Log Analysis]]

## Fonti

- Linux Foundation – FHS: https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html
- The Linux Command Line (W. Shotts), Cap. 2-4: https://linuxcommand.org/tlcl.php
- linuxjourney.com — sezione "The Filesystem" (/usr-merge, /usr/local vs /usr/bin)
- OverTheWire Bandit (livelli 0-5): https://overthewire.org/wargames/bandit/
