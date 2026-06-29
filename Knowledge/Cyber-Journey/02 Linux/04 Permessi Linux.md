---
tipo: concetto
tag: [linux]
fase: 1
fonti: 6
aggiornato: 2026-06-28
stato: maturo
aliases: ["Permessi Linux", "Permessi dei File"]
---

# Permessi Linux

## In breve

I **permessi Linux** stabiliscono chi può **leggere, scrivere o eseguire** un file o una directory. Ogni file ha un **owner** (utente) e un **group**, e tre set di permessi: owner, group, **others**. Il modello è chiamato DAC (Discretionary Access Control): il proprietario del file decide chi può accedere. Sono il primo controllo d'accesso del sistema e la prima cosa che un attaccante cerca di aggirare nella [[Privilege Escalation Linux]].

---

## Leggere `ls -l` in dettaglio

```
-rwxr-xr--  2  mario  devs  4096  Jun 22 10:00  script.sh
│└─┬──┘└─┬──┘└─┬──┘
│  owner  group  others
│
└── tipo: - file regolare | d directory | l symlink | c char device | b block device | p pipe | s socket
```

**I tre bit base:**

| Simbolo | Ottale | Su file | Su directory |
|---------|--------|---------|--------------|
| `r` | 4 | leggere il contenuto | **elencare** i nomi (`ls`) |
| `w` | 2 | modificare/troncare | **creare/cancellare/rinominare** file dentro |
| `x` | 1 | eseguire come programma | **attraversare** (`cd`), accedere a un path noto |

**Conseguenze non ovvie sulle directory:**
- Solo `x` (senza `r`): puoi accedere a un file se conosci il nome esatto, ma non puoi listare la cartella (oscuramento parziale).
- Solo `r` (senza `x`): puoi elencare i nomi ma non accedere/aprire i file.
- `w` senza `x`: inutile (non puoi accedere alla directory).
- `w+x`: puoi cancellare **qualsiasi** file nella directory, anche file di cui non sei il proprietario (caveat importante per `/tmp`).

---

## Notazione ottale e comandi

Ogni terna `rwx` vale una cifra ottale: `r=4`, `w=2`, `x=1`.

```
rwxr-xr-- = 7 5 4 = 754
```

```bash
# chmod simbolico
chmod u+x script.sh          # aggiunge x all'owner
chmod g-w,o-r file           # rimuove w al group e r agli others
chmod a+r file               # aggiunge r a tutti (all)

# chmod ottale
chmod 755 script.sh          # rwxr-xr-x
chmod 640 secret.conf        # rw-r-----  (owner rw, group r, others nulla)
chmod 600 ~/.ssh/id_rsa      # rw-------  (chiave privata SSH: obbligatorio)

# chown e chgrp
chown mario file.txt          # cambia solo owner
chown mario:devs file.txt     # cambia owner e group
chown :devs file.txt          # cambia solo group
chgrp devs file.txt           # equivalente a chown :devs
chown -R mario:devs /progetto # ricorsivo su directory
```

**Flag utili di `ls`:**
```bash
ls -la           # lista estesa con hidden files
ls -lah          # idem con dimensioni human-readable
ls -lZ           # mostra contesto SELinux
stat file        # metadati completi (permessi ottali, inode, timestamps)
```

---

## Permessi speciali: il quarto bit ottale

I permessi speciali si settano con una **quarta cifra ottale** anteposta (es. `4755`), o con simboli `u+s`, `g+s`, `+t`.

### SUID (Set User ID) — bit 4

```bash
chmod 4755 /usr/bin/passwd    # -rwsr-xr-x  (s in posizione x dell'owner)
chmod u+s file
```

**Meccanismo**: quando un file con SUID viene eseguito, il processo gira con l'**EUID (Effective UID) dell'owner** del file, non dell'utente che lo lancia. Esempio: `/usr/bin/passwd` è SUID-root; un utente normale può cambiare la propria password perché il processo ottiene temporaneamente EUID=0 per scrivere in `/etc/shadow`.

**In `ls -l`**: la `s` appare al posto della `x` nell'owner set. Se l'owner non ha `x`, compare una `S` maiuscola (SUID settato ma non eseguibile — inutile e sospetto).

> [!warning] Vettore di privesc critico
> Qualsiasi binario SUID-root con una funzionalità di escape (shell, editor, interprete) può dare root. Vedi [[SUID e SGID]] per l'analisi completa e i tool di sfruttamento.

### SGID (Set Group ID) — bit 2

```bash
chmod 2755 /usr/bin/locate    # -rwxr-sr-x  (s al posto di x nel group set)
chmod g+s /shared/dir         # su directory: nuovi file ereditano il GROUP della dir
```

**Su file**: il processo gira con l'**EGID (Effective GID) del group** del file.
**Su directory**: ogni file creato dentro eredita il group della directory (utile per cartelle condivise tra team).

### Sticky Bit — bit 1

```bash
chmod 1777 /tmp               # drwxrwxrwt  (t al posto di x negli others)
chmod +t /shared
```

**Meccanismo**: in una directory world-writable con sticky bit, solo il **proprietario del file** (o root) può cancellare o rinominare quel file, anche se la directory ha permessi `777`. Fondamentale per `/tmp` e `/var/tmp`.

**Riepilogo visivo:**

| Bit speciale | Simbolo in `ls` | Effetto |
|-------------|----------------|---------|
| SUID su file | `s`/`S` in owner-x | EUID = owner file all'exec |
| SGID su file | `s`/`S` in group-x | EGID = group file all'exec |
| SGID su dir | `s` in group-x | file creati ereditano il group |
| Sticky su dir | `t`/`T` in others-x | solo owner può cancellare i propri file |

---

## umask: la maschera di creazione

`umask` è una maschera che **sottrae** bit dai permessi di default quando si crea un file/directory:

- Default teorico file: `666` (rw-rw-rw-) — i file non sono eseguibili di default
- Default teorico directory: `777` (rwxrwxrwx)
- `umask 022`: file→ `644`, directory→ `755` (default comune)
- `umask 077`: file→ `600`, directory→ `700` (molto restrittivo, solo owner)

```bash
umask               # mostra umask corrente
umask 022           # imposta per la sessione
# Per renderlo permanente → ~/.bashrc o /etc/profile
```

**Pentest**: se umask è `000` o `002`, i file creati da script/applicazioni possono essere world-writable.

---

## ACL (Access Control List): permessi granulari

Le ACL estendono il modello owner/group/others con permessi per utenti/gruppi specifici:

```bash
getfacl file.txt              # leggi le ACL
setfacl -m u:anna:rw file     # concede rw alla singola utente anna
setfacl -m g:dev:rx dir       # gruppo dev ha rx sulla directory
setfacl -x u:anna file        # rimuove entry per anna
setfacl -b file               # rimuove tutte le ACL

# ACL di default per directory (ereditata dai nuovi file)
setfacl -d -m g:dev:rw /shared
```

In `ls -l`, la presenza di ACL è segnalata da `+` alla fine dei permessi: `-rw-r--r--+`.

---

## Esempio pratico: directory condivisa di gruppo

Combinare **SGID + umask** è il modo canonico per una cartella in cui tutto un team può scrivere i file degli altri, senza ricorrere a `chmod 777`:

```bash
sudo groupadd musica
sudo usermod -aG musica bill            # aggiungi bill al gruppo
sudo mkdir /srv/musica
sudo chown :musica /srv/musica          # gruppo proprietario = musica
sudo chmod 2775 /srv/musica             # rwxrwsr-x: SGID → i file ereditano il gruppo
umask 0002                              # i membri possono scrivere i file degli altri
```

Con SGID sulla directory + `umask 0002`, ogni file creato nella cartella appartiene al gruppo `musica` ed è scrivibile da tutti i membri. È l'alternativa corretta a `chmod 777` per la collaborazione.

---

## Cambiare identità: `su`, `sudo`, `visudo`

```bash
su -                       # shell come root (richiede la password DI ROOT)
su -c 'comando' utente     # esegue un singolo comando come 'utente'
sudo comando               # esegue come root usando la PROPRIA password
sudo -l                    # mostra cosa l'utente può fare via sudo
sudo visudo                # UNICO modo corretto di editare /etc/sudoers
```

- `su` richiede la password dell'utente target (di norma root); Ubuntu disabilita l'account root e usa **solo** `sudo`.
- `sudo` è configurato in `/etc/sudoers`: autorizza comandi specifici a utenti/gruppi usando la *propria* password.
- **Modifica `/etc/sudoers` solo con `visudo`**: valida la sintassi prima di salvare ed evita di chiuderti fuori con un errore di battitura.

---

## Rilevanza per la sicurezza

### Trovare vettori di attacco

```bash
# SUID attivi (priorità alta)
find / -perm -4000 -type f 2>/dev/null

# SGID attivi
find / -perm -2000 -type f 2>/dev/null

# File world-writable (scrivibili da chiunque)
find / -perm -2 -type f 2>/dev/null | grep -vE '^/proc|^/sys|^/dev'

# Directory world-writable
find / -perm -2 -type d 2>/dev/null | grep -vE '^/proc|^/sys'

# File scrivibili dall'utente corrente (più preciso)
find / -writable -type f 2>/dev/null | grep -vE '^/proc|^/sys'
```

### Scenari di privesc da permessi deboli

**Script di root world-writable:**
```bash
# cron o systemd esegue /opt/cleanup.sh come root
# e il file è scrivibile da te:
echo 'cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash' >> /opt/cleanup.sh
# attendi il tick, poi:
/tmp/rootbash -p    # shell EUID=0
```

**`/etc/passwd` world-writable:**
```bash
openssl passwd -6 -salt xyz pass123     # genera hash $6$...
echo 'hacker:<hash>:0:0:root:/root:/bin/bash' >> /etc/passwd
su hacker    # → root
```

**Directory di un servizio root scrivibile:**
```bash
# Il servizio carica librerie da /opt/service/lib/ scrivibile da te
# → shared library hijacking (vedi [[SUID e SGID]])
```

### Errori comuni di configurazione

| Misconfiguration | Rischio |
|-----------------|---------|
| `chmod 777` su file di config | Qualsiasi utente può sovrascriverlo |
| `chmod 777` su directory di lavoro | Creazione/sostituzione di file da parte di chiunque |
| `chmod 755` su file con segreti | Lettura da chiunque (API key, token) |
| `chmod 666` su socket o pipe | Intercettazione di comunicazioni inter-processo |
| Script eseguito da root senza path assoluto | PATH hijacking |

### Hardening

```bash
# Audit SUID/SGID periodico: salva baseline e confronta
find / -perm /6000 -type f 2>/dev/null | sort > /root/suid_baseline.txt
# versioni successive: diff rispetto alla baseline

# Permessi corretti per file sensibili
chmod 600 /etc/ssh/ssh_host_*_key       # chiavi private SSH server
chmod 640 /etc/shadow                    # solo root + gruppo shadow
chmod 440 /etc/sudoers                   # solo root può leggere

# Monta filesystem con nosuid per ridurre la superficie SUID
# In /etc/fstab:
# /dev/sdb1 /home ext4 defaults,nosuid,nodev 0 2
```

> [!tip] sudo restrittivo (principio del minimo privilegio)
> Limita `sudo` a comandi specifici in `/etc/sudoers` invece di concedere `ALL`. **Evita `NOPASSWD`** e i **wildcard (`*`) nei path**: ampliano la superficie d'attacco in modi inaspettati (un argomento controllabile può far eseguire ben altro). Per ambienti sensibili usa `umask 027` o `077` (CIS benchmark): nega ogni accesso a *others* di default.

---

## Troubleshooting

| Sintomo | Causa | Soluzione |
|---------|-------|-----------|
| `Permission denied` su file con permessi apparentemente ok | Permessi della **directory padre** mancanti | `ls -la` sulla directory; verifica `x` sul path |
| `ssh` rifiuta la chiave privata | Permessi troppo aperti (`644` o peggio) | `chmod 600 ~/.ssh/id_rsa` |
| Script non eseguibile dopo `chmod +x` | Filesystem montato con `noexec` | `mount | grep noexec`; rimonta senza il flag o usa `bash script.sh` |
| SUID non funziona | Filesystem montato con `nosuid` | `mount | grep nosuid`; spostare il file su un mount senza `nosuid` |
| `chown` fallisce per utente normale | Solo root può cambiare owner | Usa `sudo chown` o agisci come root |
| File con `+` in `ls -l` non accessibile come atteso | ACL override dei permessi base | `getfacl file` per vedere le entry ACL reali |

---

## Lab

- **TryHackMe — Linux PrivEsc** / **Common Linux Privesc**: esercizi su SUID/SGID, file world-writable e script root scrivibili.
- **OverTheWire — Bandit** (livelli 10-20): permessi su file e directory, lettura condizionata da `r`/`x`.
- **HackTheBox — Linux Privilege Escalation** (modulo Academy): pratica completa su permessi deboli e bit speciali.

## Domande da esame / colloquio

> **D: Qual è la differenza tra `chmod 755` e `chmod u=rwx,go=rx`?**
> Sono equivalenti nel risultato finale (`rwxr-xr-x`), ma la notazione ottale imposta i permessi in modo **assoluto** (sovrascrive tutto), mentre quella simbolica agisce in modo **relativo** (modifica solo i bit specificati). In uno script è più sicura la notazione ottale perché non dipende dallo stato precedente.

> **D: Un utente ha `w` su una directory ma non su un file dentro di essa. Può cancellare quel file?**
> Sì, se la directory ha anche `x`. La cancellazione di un file è un'operazione sulla **directory** (rimuove l'entry dal directory entry), non sul file stesso. Serve `w+x` sulla directory, indipendentemente dai permessi del file. Eccezione: se la directory ha lo **sticky bit**, solo l'owner del file (o root) può cancellarlo.

> **D: Cosa significa la `S` maiuscola al posto della `s` in un file SUID?**
> Il bit SUID è settato ma il file **non ha il bit `x` (execute)** per quell'owner. Il SUID è effettivamente inutile (un file non eseguibile non lancia un processo), ma la `S` maiuscola è un segnale di misconfiguration o tamper.

> **D: Perché `/tmp` ha permessi `1777` e non semplicemente `777`?**
> Senza sticky bit, chiunque avrebbe `w+x` sulla directory e potrebbe cancellare o rinominare i file altrui (es. file temporanei di root o di altri utenti). Il sticky bit `t` garantisce che ogni utente possa cancellare solo i **propri** file, anche in una directory condivisa e world-writable.

> **D: Come funziona `umask 022` in pratica? Crea un file: che permessi ha?**
> I file nascono teoricamente `666`. La umask si applica con una NOT-AND: `666 & ~022 = 666 & 755 = 644` → `rw-r--r--`. Le directory nascono `777 & ~022 = 755` → `rwxr-xr-x`.

---

## Collegamenti

- [[Filesystem Linux]]
- [[Utenti e Gruppi Linux]]
- [[SUID e SGID]]
- [[Privilege Escalation Linux]]
- [[sudo]]
- [[find]]
- [[Capabilities Linux]]

## Fonti

- Man page chmod(1): https://man7.org/linux/man-pages/man1/chmod.1.html
- Man page stat(2): https://man7.org/linux/man-pages/man2/stat.2.html
- The Linux Command Line — Permessi: https://linuxcommand.org/tlcl.php
- HackTricks — Linux Privilege Escalation: https://book.hacktricks.xyz/linux-hardening/privilege-escalation
- Linux man-pages — acl(5): https://man7.org/linux/man-pages/man5/acl.5.html
- TLCL — cap. 9 "Permissions" (su/sudo, directory condivise SGID+umask); CBT Nuggets — "Setuid, Setgid, Sticky Bit"; CIS benchmark / sudo NOPASSWD best practices (ricerca 2025)
