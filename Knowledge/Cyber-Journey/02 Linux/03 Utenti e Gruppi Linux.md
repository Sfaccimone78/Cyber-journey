---
tipo: concetto
tag: [linux]
fase: 1
fonti: 5
aggiornato: 2026-06-28
stato: maturo
aliases: ["Utenti e Gruppi Linux"]
---

# Utenti e Gruppi Linux

## In breve

Linux è un sistema **multiutente**: ogni persona (o processo) opera con una propria identità chiamata **utente**, identificata da un numero intero univoco chiamato **UID** (User ID). Gli utenti sono organizzati in **gruppi** (identificati da **GID**, Group ID) per semplificare la gestione dei permessi. L'utente speciale **root** (UID 0) ha controllo totale sul sistema e bypassa quasi tutti i controlli d'accesso del kernel.

---

## I file chiave: struttura e formato

### `/etc/passwd` — il registro degli utenti

```
mario:x:1001:1001:Mario Rossi:/home/mario:/bin/bash
  1    2   3    4       5           6          7
```

| Campo | Significato |
|-------|-------------|
| 1 `mario` | Username (login name) |
| 2 `x` | Placeholder password — la vera hash è in `/etc/shadow` |
| 3 `1001` | UID (User ID) |
| 4 `1001` | GID primario (Group ID) |
| 5 `Mario Rossi` | GECOS / commento (nome completo, ecc.) |
| 6 `/home/mario` | Home directory |
| 7 `/bin/bash` | Shell di login |

**Pentest tip**: se il campo 2 non è `x` ma contiene un hash (sistemi antichi) o è vuoto, l'account non ha password (`su username` entra senza chiederla).

### `/etc/shadow` — gli hash delle password (solo root)

```
mario:$6$salt$hashlong...:19500:0:99999:7:::
  1       2                  3  4   5    6
```

| Campo | Significato |
|-------|-------------|
| 1 | Username |
| 2 | Hash nel formato `$id$salt$hash` |
| 3 | Giorni dall'epoch Unix (01/01/1970) dell'ultimo cambio password |
| 4 | Minimo giorni prima di poter cambiare |
| 5 | Massimo giorni prima di dover cambiare |
| 6 | Giorni di preavviso prima della scadenza |

**Formato hash `$id$salt$hash`:**

| `$id` | Algoritmo |
|--------|-----------|
| `$1$` | MD5 (obsoleto, craccabile facilmente) |
| `$2y$` | bcrypt |
| `$5$` | SHA-256 |
| `$6$` | SHA-512 (default moderno) |
| `$y$` | yescrypt (moderno, resistente a GPU) |

**Pentest tip**: un hash `$1$` è craccabile con [[John the Ripper]] o Hashcat in pochi minuti anche con hardware modesto; `$6$` e `$y$` richiedono GPU e dizionari mirati.

### `/etc/group` — la lista dei gruppi

```
sudo:x:27:alice,mario
 1   2  3      4
```

| Campo | Significato |
|-------|-------------|
| 1 | Nome gruppo |
| 2 | Password gruppo (raramente usata, `x` = in gshadow) |
| 3 | GID |
| 4 | Lista utenti **aggiuntivi** (separati da virgola) |

---

## Tipi di utenti e range UID

| Tipo | UID tipico | Esempi |
|------|-----------|--------|
| **root** | 0 | Il superutente. Nessun limite. |
| **Sistema** | 1–999 | `daemon`, `www-data`, `mysql`, `nobody` |
| **Normali** | ≥ 1000 | Account reali degli utenti umani |

**Nota UID**: la distinzione 1–999 / ≥1000 è convenzionale (definita in `/etc/login.defs` tramite `UID_MIN` e `SYS_UID_MAX`). Gli account di sistema non hanno home reale né shell interattiva (di solito `/usr/sbin/nologin` o `/bin/false`).

---

## Gestione utenti: comandi e flag

```bash
# Leggere l'identità corrente
whoami                        # solo nome utente
id                            # uid=1001(mario) gid=1001(mario) groups=1001(mario),27(sudo)
id username                   # identità di un altro utente

# Creare utenti
useradd -m -s /bin/bash alice          # -m crea home, -s imposta shell
useradd -r -s /usr/sbin/nologin svc   # -r = account di sistema

# Impostare/cambiare password
passwd alice                  # root imposta la password di alice
passwd                        # utente cambia la propria

# Modificare un account esistente
usermod -aG sudo alice        # -a = append (NON sovrascrive gruppi), -G = gruppo supplementare
usermod -s /bin/zsh alice     # cambia shell
usermod -L alice              # Lock: mette ! davanti all'hash in shadow
usermod -U alice              # Unlock

# Eliminare un utente
userdel alice                 # rimuove solo l'account
userdel -r alice              # -r: rimuove anche home e mail spool

# Passare a un altro utente
su - mario                    # login come mario (carica ambiente completo)
su -c "comando" mario         # esegue un comando come mario
```

## Gestione gruppi

```bash
groupadd sviluppo             # crea gruppo
groupmod -n dev sviluppo      # rinomina
groupdel sviluppo             # elimina (rimuovi prima i membri)
gpasswd -a alice dev          # aggiunge alice a dev
gpasswd -d alice dev          # rimuove alice da dev
groups alice                  # elenca i gruppi di alice
newgrp dev                    # cambia GID primario nella sessione corrente
```

**Importante**: dopo `usermod -aG`, l'utente deve fare **logout e login** per che i nuovi gruppi siano attivi. Alternativa immediata in sessione: `newgrp groupname`.

---

## Gruppi privilegiati: vettori di privesc

Alcuni gruppi danno accesso a risorse equivalenti a root (o comunque pericolose):

| Gruppo | Accesso / rischio |
|--------|-------------------|
| `sudo` / `wheel` | Eseguire comandi come root con `sudo` → [[sudo]] |
| `docker` | Montare `/` dell'host in un container → root host |
| `lxd` / `lxc` | Simile a docker, container privilegiato |
| `disk` | Accesso raw a `/dev/sdX` → `debugfs` legge tutto il filesystem |
| `shadow` | Lettura di `/etc/shadow` → dump di tutti gli hash |
| `adm` | Lettura di log di sistema in `/var/log` |
| `www-data` | Scrive nella document root del web server |

```bash
# Pentest: verifica immediata dei gruppi pericolosi
id
# uid=1001(www-data) gid=33(www-data) groups=33(www-data),998(docker)
# → appartieni a docker = root host garantito

# Exploit docker group
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
# root@...:/# id  →  uid=0(root)
```

---

## Enumerazione utenti in pentest

Una delle prime attività dopo aver ottenuto una shell è mappare gli utenti del sistema:

```bash
# Utenti con shell interattiva (potenziali account reali)
grep -vE '/nologin|/false' /etc/passwd

# Elenco utenti umani (UID >= 1000)
awk -F: '$3 >= 1000 {print $1, $3, $7}' /etc/passwd

# Chi appartiene al gruppo sudo/wheel?
getent group sudo wheel

# Utenti con home directory esistente
ls -la /home/

# Chi ha effettuato login di recente?
last -n 20
lastlog | grep -v "Never"

# Tentativi di login falliti
lastb -n 20          # richiede root

# Leggere shadow (se root o gruppo shadow)
cat /etc/shadow
unshadow /etc/passwd /etc/shadow > combined.txt   # prepara per John/Hashcat

# Enumerazione rapida completa
cat /etc/passwd; cat /etc/group; id; sudo -l
```

---

## `/etc/sudoers` e deleghe sudo

```bash
# Leggere la configurazione sudo
cat /etc/sudoers
ls -la /etc/sudoers.d/

# Verificare cosa può fare l'utente corrente
sudo -l
```

Vedi [[sudo]] per la trattazione completa dei formati e degli exploit.

---

## Sicurezza: offensivo vs hardening

### Offensive (vettori di attacco)

1. **Hash craccabili in `/etc/shadow`**: se ottieni lettura (root, gruppo `shadow`, backup di shadow) → [[John the Ripper]] / Hashcat con `rockyou.txt`.
2. **`/etc/passwd` world-writable**: raro ma devastante. Aggiungi una riga `hacker:<hash>:0:0:root:/root:/bin/bash`, poi `su hacker` → root. Genera l'hash con `openssl passwd -6 -salt xyz pass123`.
3. **Gruppi privilegiati**: vedere tabella sopra — `docker`, `lxd`, `disk` danno root di fatto.
4. **Account senza password in shadow** (`!!` o `!` = account bloccato; campo vuoto = nessuna password).
5. **UID 0 duplicati**: `awk -F: '$3==0' /etc/passwd` — account extra con UID 0 sono backdoor.

### Hardening

- `/etc/shadow` deve essere `640 root:shadow` o `000 root:root`.
- `/etc/passwd` deve essere `644 root:root` — **mai scrivibile da altri**.
- Rimuovere dall'`/etc/passwd` la shell interattiva per account di servizio: usa `/usr/sbin/nologin`.
- Applicare **aging delle password** (`chage -M 90 mario`): max 90 giorni, warning 14 giorni.
- Audit periodico: `awk -F: '$3==0' /etc/passwd` (UID 0 duplicati), `awk -F: '$2=="!!"' /etc/shadow` (account mai attivati).
- **PAM** (`/etc/pam.d/`): moduli come `pam_pwquality` per complessità password, `pam_faillock` per lockout dopo N tentativi falliti.

```bash
# Lockout policy con faillock (moderno)
# /etc/security/faillock.conf
deny = 5        # blocca dopo 5 tentativi
unlock_time = 600   # sblocca dopo 10 minuti
```

---

## Troubleshooting

| Sintomo | Causa probabile | Soluzione |
|---------|----------------|-----------|
| `su: authentication failure` anche con password corretta | Account bloccato (`!` in shadow) | `usermod -U username` |
| Nuovo gruppo non attivo nella sessione | `usermod -aG` applicato ma no re-login | `newgrp groupname` oppure logout/login |
| `useradd` non crea la home | Flag `-m` mancante | `useradd -m username` oppure crea manualmente + `chown` |
| `id` non mostra il gruppo appena aggiunto | Cache del gruppo nella sessione | `exec su -l $USER` per ricaricare l'ambiente |
| `passwd` rifiuta la password | Policy PAM (`pam_pwquality`) troppo restrittiva | Verifica `/etc/security/pwquality.conf`; root può sempre forzare |

---

## Lab

- **TryHackMe — Linux PrivEsc** e **Common Linux Privesc**: sfrutta gruppi privilegiati (`docker`, `lxd`, `disk`), hash di `/etc/shadow` e UID 0 duplicati.
- **OverTheWire — Bandit** (livelli con cambio utente via SUID): pratica `su`, `id`, enumerazione utenti.
- **HackTheBox — Starting Point** (macchine Linux tier 0-1): enumerazione utenti/gruppi e lettura shadow in scenario reale.

## Domande da esame / colloquio

> **D: Qual è la differenza tra UID primario e GID primario in `/etc/passwd`?**
> L'UID identifica l'utente come proprietario dei file che crea. Il GID primario è il gruppo assegnato ai file creati dall'utente. Un utente può appartenere a molti gruppi supplementari (elencati in `/etc/group`), ma il GID di `/etc/passwd` è quello di default al momento della creazione dei file.

> **D: Perché `/etc/shadow` esiste separatamente da `/etc/passwd`?**
> In origine tutto stava in `/etc/passwd`, che deve essere leggibile da tutti (`644`) perché molti programmi mappano UID → nome utente. Gli hash delle password in un file world-readable erano attaccabili da qualsiasi utente locale (offline cracking). Con la separazione, gli hash stanno in `/etc/shadow` (`640` o `000`), leggibile solo da root o dal gruppo `shadow`.

> **D: Come mai appartenere al gruppo `docker` equivale praticamente a essere root?**
> Il daemon Docker gira come root. Chiunque possa eseguire `docker run` può montare l'intero filesystem host (`-v /:/mnt`) dentro un container e fare `chroot`, ottenendo una shell root sul sistema host senza alcun check sudo.

> **D: Cosa fa `usermod -aG sudo alice` e qual è il rischio se si dimentica `-a`?**
> Aggiunge alice al gruppo `sudo` **in append** senza toccare gli altri gruppi. Senza `-a`, il flag `-G` **sovrascrive** tutti i gruppi supplementari dell'utente: se alice era anche in `developers` e `docker`, li perde entrambi.

> **D: In un pentest ottieni `/etc/shadow`. Il hash inizia con `$1$`. Cosa significa e come procedi?**
> `$1$` = MD5-crypt, algoritmo del 1994, estremamente vulnerabile a dictionary attack su GPU. Con Hashcat (`-m 500`) e `rockyou.txt` si cracca in secondi/minuti. Con `$6$` (SHA-512) o `$y$` (yescrypt) il cracking è molto più lento — punta su password corte o in lista.

> **D: Come individui un UID 0 duplicato (backdoor) su un sistema compromesso?**
> `awk -F: '$3==0 {print}' /etc/passwd` — se escono più di una riga, c'è una backdoor con privilegi root nascosta sotto un altro username. Confronta anche con lo storico del file via git, backup o hash noti.

---

## Collegamenti

- [[Permessi Linux]]
- [[SUID e SGID]]
- [[sudo]]
- [[Privilege Escalation Linux]]
- [[Filesystem Linux]]
- [[OverTheWire Bandit]]
- [[Hashing delle Password e Salting]]
- [[John the Ripper]]
- [[Capabilities Linux]]

## Fonti

- Man page passwd(5): https://man7.org/linux/man-pages/man5/passwd.5.html
- Man page shadow(5): https://man7.org/linux/man-pages/man5/shadow.5.html
- Man page useradd(8): https://man7.org/linux/man-pages/man8/useradd.8.html
- HackTricks – Linux Privilege Escalation: https://book.hacktricks.xyz/linux-hardening/privilege-escalation
- The Linux Documentation Project – User Authentication: https://tldp.org/HOWTO/User-Authentication-HOWTO/
