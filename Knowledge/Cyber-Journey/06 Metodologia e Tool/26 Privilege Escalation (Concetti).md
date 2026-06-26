---
tipo: concetto
tag: [metodologia, linux]
fase: 2
fonti: 2
aggiornato: 2026-06-26
stato: maturo
aliases: ["Privilege Escalation (Concetti)", "Privilege Escalation", "Privesc"]
---
# Privilege Escalation (Concetti)

## Definizione
La **privilege escalation** è l'ottenimento di privilegi superiori a quelli concessi. Avviene tipicamente **dopo** un foothold iniziale (post-exploitation in un [[Metodologia del Pentest|pentest]]). Due tipi:
- **Verticale**: da utente non privilegiato a root/admin.
- **Orizzontale**: assumere l'identità di un altro utente di pari livello (collega a [[Broken Access Control e IDOR]]).

Questa pagina raccoglie i **concetti generali** e i vettori **Linux** (rilevanti per CTF/pentest). Per i tool di enumerazione automatica vedi [[PEAS (WinPEAS e LinPEAS)|PEAS]]; per i prerequisiti sui permessi vedi [[Permessi Linux]].

## Vettori Linux

### SUID/SGID binaries
Un binario con bit **SUID** (`-rwsr-xr-x`) gira con i privilegi del **proprietario** (spesso root), non di chi lo lancia. Se è un binario che permette di eseguire comandi (vim, find, less, nmap...), si abusa per ottenere una shell root. Riferimento: **GTFOBins**.

### sudo misconfiguration
`sudo -l` mostra cosa l'utente può eseguire come root. Se include binari sfruttabili (`(root) NOPASSWD: /usr/bin/find`), o versioni vulnerabili di sudo, → root. Vedi GTFOBins per ogni binario.

### Kernel exploits
Un kernel non patchato con CVE locale (es. **Dirty COW**, **Dirty Pipe**, **PwnKit**) permette l'escalation a root sfruttando un bug del kernel/componente setuid.

### Altri vettori
Cron job scrivibili, capabilities (`getcap`), PATH hijacking, password/chiavi in file leggibili, NFS `no_root_squash`, container escape, servizi che girano come root.

## Esempio
```bash
# Enumerazione automatica
./linpeas.sh                 # script di enum privesc
sudo -l                      # cosa posso fare come root
find / -perm -4000 2>/dev/null   # trova binari SUID

# Abuso SUID di 'find' (da GTFOBins) → shell root
find . -exec /bin/sh -p \; -quit

# Abuso sudo su 'vim'
sudo vim -c ':!/bin/sh'

# Kernel exploit (esempio: PwnKit CVE-2021-4034) in lab
./PwnKit                     # → uid=0(root)
```

## Difesa
- **Least privilege**: minimizzare binari SUID (`find / -perm -4000` e rimuovere il superfluo); sudo solo per comandi specifici e sicuri, con password.
- **Patch del kernel** e dei componenti setuid (polkit, sudo) → [[Componenti Vulnerabili]].
- File di configurazione/credenziali con permessi stretti ([[Permessi Linux]]); niente password in chiaro.
- **Hardening**: noexec/nosuid su mount, AppArmor/SELinux, audit dei cron e delle capabilities.
- Monitoraggio: **auditd**, file-integrity monitoring, alert su uso anomalo di sudo → [[Logging e Monitoring Failures]].

## CVE reale
- **CVE-2021-4034 "PwnKit"** (polkit `pkexec`) — privilege escalation locale a root, presente per 12 anni su praticamente ogni distro Linux: exploit affidabile e universale.
- **CVE-2022-0847 "Dirty Pipe"** — bug nel kernel Linux che permette di sovrascrivere file read-only → root.

## Collegamenti
- [[Metodologia del Pentest]] · [[Post-Exploitation]] · [[PEAS (WinPEAS e LinPEAS)]] · [[Metodologia CTF]]
- [[Permessi Linux]] · [[Broken Access Control e IDOR]] · [[Componenti Vulnerabili]] · [[Analisi Malware di Base]]

## Fonti
- GTFOBins — https://gtfobins.github.io/
- Anderson, *Security Engineering* — https://www.cl.cam.ac.uk/~rja14/book.html
