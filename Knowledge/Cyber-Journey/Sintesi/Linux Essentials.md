---
tipo: sintesi
tag: [linux, sintesi]
fase: 0
aggiornato: 2026-06-25
stato: attivo
aliases: ["Linux Essentials"]
---

# Sintesi — Linux Essentials

Pagina di sintesi cross-source del topic **Linux**: percorso di studio, riferimento rapido ai comandi, confronto tra famiglie di distribuzioni e fondamenti di Linux per la sicurezza. Per gli approfondimenti seguire i link `[[...]]`. [Fonte: TLCL, interi capitoli; ricerca 2025-2026]

## Percorso di apprendimento (ordine di studio)

L'ordine segue la progressione di *The Linux Command Line* (TLCL), dal fondamentale all'avanzato:

1. **La shell e il terminale** — cos'è bash, prompt, history, `Tab`/`Ctrl-r`. → [[Shell e Bash]]
2. **Filesystem e navigazione** — albero FHS, path assoluti/relativi, `cd`/`ls`/`cp`/`mv`/`rm`, link. → [[Filesystem Linux]]
3. **Redirezione e pipeline** — stdin/stdout/stderr, `>` `|` `2>&1`, filtri (`grep`/`sort`/`wc`). → [[Redirezione e Pipeline]]
4. **Permessi e utenti** — rwx, `chmod`, `umask`, `sudo`, setuid. *Base della sicurezza.* → [[Permessi dei File]]
5. **Processi e job control** — `ps`/`top`, `kill`/segnali, `&`/`bg`/`fg`, systemd. → [[Processi e Job Control]]
6. **Editor di testo** — sopravvivere in Vim (`:wq`), modifiche rapide in nano. → [[Vim e Editor]]
7. **Gestione pacchetti** — installare/aggiornare software, repository, dipendenze. → [[Gestione Pacchetti]]
8. **Networking** — diagnostica con `ip`/`ss`/`ping`/`dig`/`curl`. → [[Tool di Rete]]
9. **SSH** — accesso remoto sicuro, chiavi, tunnel, hardening. → [[SSH]]
10. **Scripting bash** — variabili, test, loop, funzioni, exit code: automazione. → [[Scripting Bash]]

> Filo conduttore della filosofia Unix: **"tutto è un file"**, strumenti piccoli e componibili via pipe, e l'idea che la CLI *è* il modo più potente di controllare il sistema. [Fonte: TLCL, Introduzione; vedi [[The Linux Command Line]]]

## Top 50 comandi Linux

| # | Comando | A cosa serve (1 riga) |
|---|---------|------------------------|
| 1 | `ls` | elenca file e directory (`-l` dettagli, `-a` nascosti) |
| 2 | `cd` | cambia directory corrente |
| 3 | `pwd` | stampa la directory di lavoro corrente |
| 4 | `cp` | copia file/directory (`-r` ricorsivo) |
| 5 | `mv` | sposta o rinomina |
| 6 | `rm` | cancella file (`-r` dir, `-f` forza) |
| 7 | `mkdir` | crea directory (`-p` con genitori) |
| 8 | `rmdir` | rimuove directory vuote |
| 9 | `touch` | crea file vuoto / aggiorna timestamp |
| 10 | `cat` | concatena e mostra il contenuto di file |
| 11 | `less` | visualizza file pagina per pagina (`q` esce) |
| 12 | `head` / `tail` | prime / ultime righe (`tail -f` segue i log) |
| 13 | `grep` | cerca un pattern nel testo (`-i` `-r` `-v`) |
| 14 | `find` | cerca file per nome/attributi nell'albero |
| 15 | `locate` | cerca file via database indicizzato (veloce) |
| 16 | `which` / `type` | percorso/tipo di un comando |
| 17 | `man` | manuale di un comando (`q` esce) |
| 18 | `sort` | ordina righe |
| 19 | `uniq` | rimuove righe duplicate adiacenti |
| 20 | `wc` | conta righe/parole/byte (`-l`) |
| 21 | `cut` | estrae colonne/campi da righe |
| 22 | `sed` | editor di stream (sostituzioni, trasformazioni) |
| 23 | `awk` | elaborazione di testo per colonne |
| 24 | `tr` | traduce/elimina caratteri |
| 25 | `tee` | scrive su file *e* prosegue nella pipe |
| 26 | `xargs` | costruisce comandi dagli argomenti su stdin |
| 27 | `chmod` | cambia i permessi (rwx, ottale) |
| 28 | `chown` | cambia proprietario/gruppo |
| 29 | `umask` | maschera dei permessi di default |
| 30 | `sudo` | esegue un comando come root/altro utente |
| 31 | `su` | cambia identità utente |
| 32 | `passwd` | cambia password |
| 33 | `ps` | snapshot dei processi (`ps aux`) |
| 34 | `top` / `htop` | monitor dinamico dei processi |
| 35 | `kill` / `killall` | invia segnali a processi (per PID / nome) |
| 36 | `jobs` / `bg` / `fg` | gestione dei job della shell |
| 37 | `df` | spazio libero sui filesystem (`-h`) |
| 38 | `du` | spazio occupato da file/dir (`-sh`) |
| 39 | `mount` / `umount` | monta / smonta filesystem |
| 40 | `tar` | archivia/estrae (`-czf` crea gzip, `-xzf` estrae) |
| 41 | `gzip` / `gunzip` | comprime / decomprime singoli file |
| 42 | `ln` | crea link (hard, o `-s` simbolico) |
| 43 | `ip` | indirizzi/routing di rete (sost. `ifconfig`) |
| 44 | `ss` | socket e porte in ascolto (sost. `netstat`) |
| 45 | `ping` | verifica raggiungibilità di un host |
| 46 | `dig` | interroga il DNS (sost. `nslookup`) |
| 47 | `curl` / `wget` | richieste HTTP/API / download file |
| 48 | `ssh` | login remoto sicuro |
| 49 | `scp` / `rsync` | copia file remota / sincronizzazione |
| 50 | `systemctl` / `journalctl` | gestione servizi / lettura log (systemd) |

## Confronto famiglie di distribuzioni

| Aspetto | Debian / Ubuntu | Arch | Red Hat / Fedora |
|---------|-----------------|------|------------------|
| **Esponenti** | Debian, Ubuntu, Mint | Arch, Manjaro, EndeavourOS | RHEL, Fedora, Rocky, CentOS Stream |
| **Formato pacchetti** | `.deb` | `.pkg.tar.zst` | `.rpm` |
| **Gestore high-level** | `apt` | `pacman` | `dnf` (ex `yum`) |
| **Gestore low-level** | `dpkg` | — | `rpm` |
| **Modello di rilascio** | stable a versioni (LTS) | **rolling** (sempre l'ultima) | versioni (RHEL stabile, Fedora rapida) |
| **Aggiornamenti sicurezza** | canale `-security` separato | non distinti dai feature update | canale dedicato, supporto a lungo termine |
| **Filosofia** | stabilità, enorme repo, facile | minimalismo, controllo, DIY | enterprise, supporto commerciale, SELinux |
| **Adatto a** | desktop e server general-purpose | utenti esperti, ultimissimo software | produzione enterprise, server critici |
| **Repo extra tipico** | PPA | AUR (build-script utente) | EPEL, COPR |

Dettagli e tabella comandi completa: [[Gestione Pacchetti]]. [Fonte: TLCL cap. 14; ricerca 2025, LinuxBlog.io]

## Linux per la sicurezza

I fondamentali per mettere in sicurezza un sistema Linux, dal più importante:

### 1. Privilegio minimo: `sudo`, non root
- Lavora come **utente normale**, eleva con `sudo` solo quando serve; non loggarti come root abitualmente.
- Limita `sudo` a comandi specifici in `/etc/sudoers` (modificalo **solo con `visudo`**); evita `NOPASSWD` e i wildcard nei path. → [[Permessi dei File]]

### 2. SSH hardening
- **Solo chiavi Ed25519**, `PasswordAuthentication no`, `PermitRootLogin no`.
- `AllowUsers` (whitelist), `MaxAuthTries 3`, timeout di inattività; config in `/etc/ssh/sshd_config.d/`.
- Verifica di poter entrare con la chiave **prima** di disabilitare le password. → [[SSH]]

### 3. Permessi e setuid
- Mai `chmod 777`; usa gruppi + setgid o ACL per la condivisione.
- **Audita i binari setuid**: `find / -perm -4000 -type f 2>/dev/null` — ognuno è un potenziale vettore di [[Privilege Escalation]].
- `umask 027` (o `077`) in ambienti sensibili. → [[Permessi dei File]]

### 4. fail2ban
- Monitora i log di autenticazione e **banna gli IP** che falliscono ripetutamente (brute-force SSH, web). Riduce drasticamente il rumore degli attacchi automatizzati.
- Installa, abilita la "jail" `sshd`, definisci `maxretry`/`bantime`. Complementare all'hardening SSH, non sostitutivo.

### 5. Firewall: ufw / firewalld
- **`ufw`** (Uncomplicated Firewall, frontend di nftables) è il modo semplice su Debian/Ubuntu: `ufw default deny incoming`, `ufw allow 22/tcp`, `ufw enable`.
- Su Red Hat l'equivalente è **`firewalld`**. Principio: **nega tutto in ingresso**, apri solo le porte necessarie. → [[Tool di Rete]]

### 6. Aggiornamenti e igiene
- Patch di sicurezza automatiche (`unattended-upgrades`/`dnf-automatic`), verifica firme GPG dei repo, riavvii dopo update di kernel. → [[Gestione Pacchetti]]
- Monitoraggio: `ss -tulpn` (porte/processi in ascolto), `journalctl` (log), `lsof` — i primi strumenti per individuare anomalie. → [[Processi e Job Control]]

## Collegamenti
- Concetti del topic: [[Shell e Bash]], [[Filesystem Linux]], [[Redirezione e Pipeline]], [[Permessi dei File]], [[Processi e Job Control]], [[Scripting Bash]], [[Gestione Pacchetti]], [[Tool di Rete]], [[SSH]], [[Vim e Editor]]
- Cross-topic: [[Privilege Escalation]] (sicurezza), [[TLS/SSL]] / [[GPG]] (crittografia), [[TCP]] (sistemi_reti)
- Riassunto libro: [[The Linux Command Line]]

## Fonti
- [TLCL — The Linux Command Line, W. Shotts, capitoli 1-36] → [[The Linux Command Line]]
- [Ricerca web 2025-2026 — SSH hardening (ssh-audit.com, Linuxize), package management & patching (LinuxBlog.io, PatchMon), CIS benchmarks]
