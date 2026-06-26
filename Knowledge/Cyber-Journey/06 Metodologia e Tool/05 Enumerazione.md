---
tipo: concetto
tag: [metodologia]
fase: 2
fonti: 6
aggiornato: 2026-06-21
stato: maturo
aliases: ["Enumerazione"]
---

# Enumerazione

## In breve
L'**enumerazione** è la fase in cui si interroga attivamente ogni servizio scoperto per estrarne informazioni dettagliate: utenti, gruppi, share, versioni, path nascosti. È più profonda della scansione: non chiede "la porta è aperta?" ma "**cosa posso ottenere** da questo servizio?". In CTF e pentest reali è dove si vince la macchina — *enumerate harder* è il mantra.

## Il loop: scan → enumera → ri-scan
L'enumerazione non è lineare ma **iterativa**: ogni dato trovato apre nuovi servizi da enumerare. Una credenziale FTP → accesso SMB → un config con password DB → e così via. Si torna indietro di continuo.

## Per servizio
| Porta | Servizio | Cosa enumerare | Tool |
|---|---|---|---|
| 21 | FTP | login anonimo, file | `ftp`, `nmap --script ftp-anon` |
| 22 | SSH | versione, banner, user validi | banner, `nmap` |
| 25 | SMTP | utenti (VRFY/EXPN) | `smtp-user-enum` |
| 53 | [[DNS]] | sottodomini, zone transfer | `dig AXFR`, `dnsenum` |
| 80/443 | HTTP | dir, file, vhost, CMS, parametri | [[Gobuster]], [[ffuf]], [[Nikto]] |
| 139/445 | [[SMB]] | share, utenti, policy | `enum4linux`, `smbclient`, [[CrackMapExec]] |
| 161 | SNMP | sistema, interfacce, processi | `snmpwalk` (community `public`) |
| 389 | LDAP | utenti, gruppi AD | `ldapsearch`, `windapsearch` |
| 3306/5432 | DB | versione, credenziali default | client nativi |

## Enumerazione web (la più ricca)
```bash
# Directory e file nascosti
gobuster dir -u http://target.lab -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt,bak

# Virtual host (sottodomini sullo stesso IP)
ffuf -u http://target.lab -H "Host: FUZZ.target.lab" -w subdomains.txt -fs 0

# Fuzzing parametri GET
ffuf -u 'http://target.lab/page.php?FUZZ=test' -w params.txt -fs 1234

# Vuln/misconfig generici + file noti
nikto -h http://target.lab
```
Da cercare sempre: `/admin`, `/backup`, `.env`, `.git/`, `robots.txt`, `backup.zip`, commenti HTML, header `Server`/`X-Powered-By`.

## SMB e AD (pentest interno)
```bash
enum4linux -a 10.10.10.10
crackmapexec smb 10.10.10.0/24 -u user -p pass --shares --users
smbclient -L //10.10.10.10/ -N            # share con null session
```

## Note operative
- **Wordlist** = qualità dei risultati. SecLists è lo standard (`/usr/share/seclists` su [[Kali Linux]]); scegli la lista per contesto (raft, common, big).
- **Annota tutto**: ogni versione, path, username. Un dato "inutile" diventa l'exploit in [[Exploitation]] (es. versione → CVE).
- Non fermarti al primo risultato: la `/backup` trovata può contenere credenziali in chiaro.

## Mitigazione e difesa
- Disabilitare **directory listing**; rimuovere `.env`/`.git`/backup dal webroot.
- Niente admin panel esposti senza auth; banner/versioni minimizzati.
- **No zone transfer** DNS pubblici; SMB senza null session; SNMP senza community di default.
- Rate-limiting e WAF per intercettare directory/parameter fuzzing.

---

## ENUMERAZIONE PER SERVIZIO — porta, tool, comando, cosa cerchi

### SMB — 139/445
Obiettivo: share leggibili, utenti/gruppi, policy password, OS, null session.
```bash
enum4linux-ng -A 10.10.10.10                      # all-in-one (RID cycling, share, policy)
smbclient -L //10.10.10.10/ -N                    # lista share con null session
smbclient //10.10.10.10/Share -N                  # accedi a uno share senza credenziali
smbmap -H 10.10.10.10 -u guest                    # permessi (READ/WRITE) per share
crackmapexec smb 10.10.10.10 -u '' -p '' --shares # null session + share
nmap --script "smb-enum-*,smb-os-discovery,smb-security-mode" -p445 10.10.10.10
```
Cosa cerchi: share `READ/WRITE` (specie non standard tipo `Backups`, `IT`), null/guest session abilitata, **SMB signing disabled** (relay), versione SMBv1 (EternalBlue).

### FTP — 21
```bash
ftp 10.10.10.10                # login anonymous / anonymous
nmap --script ftp-anon,ftp-syst,ftp-bounce -p21 10.10.10.10
```
Cosa cerchi: **login anonimo**, permessi di upload (webshell se il dir è servito da HTTP), banner con versione vulnerabile (es. vsftpd 2.3.4 backdoor), FTP bounce.

### HTTP/HTTPS — 80/443/8080
```bash
whatweb http://target.lab; nikto -h http://target.lab
gobuster dir -u http://target.lab -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -x php,txt,bak
ffuf -u http://target.lab -H "Host: FUZZ.target.lab" -w subdomains.txt -fs 0   # vhost
curl -sI http://target.lab     # header Server / X-Powered-By
```
Cosa cerchi: dir/file nascosti (`/admin`, `.git/`, `.env`, `backup.zip`), tecnologia/CMS+versione, vhost, parametri fuzzabili, commenti HTML, `robots.txt`.

### SSH — 22
```bash
nc 10.10.10.10 22              # banner (versione OpenSSH)
ssh-audit 10.10.10.10         # algoritmi deboli supportati
ssh user@10.10.10.10          # enum metodi di auth (publickey/password)
```
Cosa cerchi: versione (CVE: es. user enumeration su OpenSSH <7.7), auth a password abilitata (brute-force possibile), chiavi deboli.

### SNMP — 161/UDP
```bash
snmpwalk -v2c -c public 10.10.10.10                         # dump completo MIB
onesixtyone -c /usr/share/seclists/.../snmp.txt 10.10.10.10 # brute community string
snmp-check 10.10.10.10 -c public
```
Cosa cerchi: community string di default (`public`/`private`), utenti di sistema, processi in esecuzione (con argomenti → talvolta password), interfacce di rete, software installato. SNMP è UDP → ricordati `-sU`.

### NFS — 2049 (+ 111 rpcbind)
```bash
showmount -e 10.10.10.10                       # export disponibili
mount -t nfs 10.10.10.10:/export /mnt/nfs -o nolock
rpcinfo -p 10.10.10.10
```
Cosa cerchi: export montabili senza auth, **no_root_squash** (scrivi come root → privesc/SUID), file sensibili (chiavi SSH, backup) negli export.

### SMTP — 25
```bash
smtp-user-enum -M VRFY -U users.txt -t 10.10.10.10
nc 10.10.10.10 25     # poi: VRFY root / EXPN postmaster
```
Cosa cerchi: validazione utenti via `VRFY`/`EXPN`/`RCPT TO` (lista username per spray/brute), open relay, banner versione.

> [!tip] Regola d'oro: ogni dato alimenta un altro servizio
> Una community SNMP che rivela un username → spray SMB. Un file su uno share NFS con chiave SSH → login SSH. L'enumerazione è il loop `scan → enumera → ri-scan` (vedi sopra), non una checklist lineare.

## DETECTION ENGINEERING
- L'enumerazione **autenticata o anonima** lascia tracce diverse: `enum4linux`/CME generano molte connessioni SMB e tentativi di RID cycling → **Event ID 4625** (logon failed) a raffica, **4672/4624** con account anomali.
- Directory fuzzing (`gobuster`/`ffuf`) → migliaia di `404`/`403` in pochi secondi nei log del web server: pattern chiaro per WAF/IDS.
- `smtp-user-enum` → molte `RCPT TO`/`VRFY` consecutive nei log SMTP.
- **MITRE ATT&CK**: `T1046` Network Service Discovery, `T1135` Network Share Discovery, `T1087` Account Discovery, `T1083` File and Directory Discovery, `T1590` Gather Victim Network Information.

## TROUBLESHOOTING (5 errori + causa)
1. **`enum4linux` non restituisce nulla** → null session disabilitata (SMB hardened). Fix: prova con credenziali (`-u user -p pass`) o passa a `crackmapexec`.
2. **`snmpwalk` va in timeout** → community sbagliata o SNMP filtrato; ricorda che è **UDP**. Fix: brute con `onesixtyone`, verifica con `-sU -p161`.
3. **gobuster: tutti 200/tutti la stessa size** → la pagina risponde sempre 200 (soft-404). Fix: filtra con `-s`/`--exclude-length` o usa `ffuf -fs <size>`/`-fc`.
4. **`showmount` "clnt_create RPC: Port mapper failure"** → rpcbind (111) filtrato o NFS non esposto. Fix: verifica 111/2049 aperte prima.
5. **SMB "STATUS_ACCESS_DENIED" su share** → serve autenticazione. Fix: cerca credenziali altrove (riusa quelle trovate), prova guest.

## DOMANDE DA COLLOQUIO
1. **Differenza tra scansione ed enumerazione?** La scansione risponde "la porta è aperta?"; l'enumerazione interroga il servizio per estrarre dati concreti (utenti, share, versioni, path) e si svolge in loop iterativo.
2. **Cos'è una null session SMB e perché è pericolosa?** Una connessione SMB senza username/password (`-u '' -p ''`): su sistemi mal configurati permette di elencare utenti, gruppi, share e policy password senza credenziali — punto di partenza per spray/brute.
3. **Perché `no_root_squash` su un export NFS è critico?** Disabilita il mapping di root remoto a `nobody`: montando l'export puoi creare file come root, inclusi binari **SUID** → privilege escalation locale sul server.
4. **Come enumeri utenti via SMTP e perché serve?** Con `VRFY`/`EXPN`/`RCPT TO` il server conferma se un indirizzo esiste: ottieni una lista di username validi per password spraying o brute-force su altri servizi.

## Collegamenti
- [[Ricognizione (Recon)]]
- [[Metodologia del Pentest]]
- [[Scansione delle Porte]]
- [[Nmap]]
- [[Gobuster]]
- [[ffuf]]
- [[Nikto]]
- [[SMB]]
- [[CrackMapExec]]
- [[Exploitation]]
- [[MITRE ATT&CK]]

## Fonti
- OWASP WSTG — Configuration & Deployment Testing: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/
- HackTricks — Pentesting methodology: https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-methodology
- HackTricks — Pentesting Services (SMB/SNMP/NFS/SMTP/FTP): https://book.hacktricks.xyz/network-services-pentesting
- MITRE ATT&CK — Network Service Discovery (T1046): https://attack.mitre.org/techniques/T1046/
- TryHackMe — Network Services: https://tryhackme.com/room/networkservices
- TryHackMe — Content Discovery: https://tryhackme.com/room/contentdiscovery
