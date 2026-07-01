---
tipo: concetto
tag: [reti]
fase: 1
fonti: 3
aggiornato: 2026-06-22
stato: maturo
aliases: ["Porte e Protocolli Comuni"]

---

# Porte e Protocolli Comuni

## In breve
Una **porta** è un numero a 16 bit (0–65535) che identifica un servizio specifico su un host. Se l'indirizzo [[Indirizzamento IP|IP]] è l'indirizzo del palazzo, la porta è il numero dell'appartamento. L'accoppiata **(IP, Porta, Protocollo)** identifica univocamente un endpoint di comunicazione — il **socket**. Le porte esistono sia in [[TCP]] (orientato alla connessione) sia in [[UDP]] (connectionless); la stessa porta su TCP e su UDP è uno spazio diverso e indipendente.

---

## Range e classificazione IANA

| Range | Nome | Descrizione |
|---|---|---|
| **0–1023** | Well-known / System | Riservati ai servizi standard; richiede root/admin per ascoltare |
| **1024–49151** | Registered | Assegnati da IANA a software specifici (es. MySQL 3306, RDP 3389) |
| **49152–65535** | Dynamic / Ephemeral | Porte temporanee assegnate dal kernel al client per ogni connessione in uscita |

> [!info] La porta 0 è speciale
> Porta 0 in un bind() chiede al kernel di scegliere una porta ephemeral libera. Non è un servizio; è un alias del kernel.

### Ephemeral ports — come funziona una connessione
Quando il tuo browser contatta `93.184.216.34:443`, il kernel assegna una porta sorgente casuale nell'intervallo ephemeral (es. `54321`). Il socket è:
```
192.168.1.5:54321 (client) ↔ 93.184.216.34:443 (server)
```
Il server risponde alla porta 54321 del client. Ogni tab del browser può aprire decine di connessioni simultanee, ognuna con porta sorgente diversa.

```bash
# Vedere l'intervallo ephemeral del sistema (Linux)
cat /proc/sys/net/ipv4/ip_local_port_range     # es. 32768 60999
```

---

## Tabella porte essenziali per la sicurezza

### Servizi di accesso e amministrazione

| Porta | Proto | Servizio | Note di sicurezza e attacco |
|---|---|---|---|
| **22** | TCP | SSH | Accesso remoto cifrato. Target di brute force automatico; usare chiavi invece di password, cambiare porta (security by obscurity), `fail2ban`. |
| **23** | TCP | Telnet | Accesso remoto **in chiaro** — credenziali visibili in sniffing. Da disabilitare sempre; ancora trovato su device IoT e apparati embedded. |
| **3389** | TCP | RDP | Desktop remoto Windows. Storico bersaglio: BlueKeep (CVE-2019-0708, unauthenticated RCE), brute force, Pass-the-Hash RDP. Non esporre su Internet; usare VPN o gateway RDP. |
| **5985/5986** | TCP | WinRM | Windows Remote Management (PowerShell remoting). Usato post-compromissione per lateral movement. 5985=HTTP, 5986=HTTPS. |
| **445** | TCP | SMB | File sharing Windows. EternalBlue (MS17-010), SMB relay (NTLM), PrintSpooler coercizione. Bloccare dall'esterno; richiedere SMB Signing. |
| **135** | TCP | MSRPC | Endpoint mapper Windows. Enumerazione, DCOM. Spesso abusato per coercizione NTLM ([[Active Directory]]). |

### Servizi web

| Porta | Proto | Servizio | Note di sicurezza e attacco |
|---|---|---|---|
| **80** | TCP | HTTP | Web non cifrato. Intercettazione, injection, redirect to HTTPS. Sempre preferire 443. |
| **443** | TCP | HTTPS | HTTP su TLS. Vettori: cert self-signed, downgrade TLS 1.0/1.1, misconfiguration CORS. |
| **8080** | TCP | HTTP alternativo | Server web di sviluppo, proxy. Spesso dimenticati senza autenticazione. |
| **8443** | TCP | HTTPS alternativo | Come 8080 ma TLS. Comune su application server (Tomcat, JBoss). |

### Servizi email

| Porta | Proto | Servizio | Note di sicurezza |
|---|---|---|---|
| **25** | TCP | SMTP | Email server-to-server. Open relay = spam/phishing; autenticazione SASL. |
| **587** | TCP | SMTP Submission | Client → server (autenticato + STARTTLS). |
| **465** | TCP | SMTPS | SMTP su TLS (obsoleto ma ancora usato). |
| **110** | TCP | POP3 | Email in chiaro. Preferire 995 (POP3S). |
| **143** | TCP | IMAP | Email in chiaro. Preferire 993 (IMAPS). |

### Servizi di rete e infrastruttura

| Porta | Proto | Servizio | Note di sicurezza e attacco |
|---|---|---|---|
| **53** | TCP/UDP | DNS | Query su UDP/53; TCP/53 per zone transfer e risposte grandi. Amplification attack (UDP), cache poisoning, DNS tunneling (exfil). |
| **67/68** | UDP | DHCP | Server/Client. Rogue DHCP server per MITM, DHCP starvation. |
| **123** | UDP | NTP | Sincronizzazione oraria. NTP monlist → amplification ~556×. |
| **161/162** | UDP | SNMP | Monitoring (poll/trap). Community string `public` in chiaro → dump configurazione. SNMPv3 con auth+priv. |
| **514** | UDP/TCP | Syslog | Log remoto. No autenticazione → log falsificabili; usare TLS Syslog (RFC 5425). |

### Active Directory e Windows

| Porta | Proto | Servizio | Note di sicurezza e attacco |
|---|---|---|---|
| **88** | TCP/UDP | Kerberos | Autenticazione [[Active Directory]]. Kerberoasting (richiesta TGS per account di servizio → crack offline), AS-REP Roasting. |
| **139** | TCP | NetBIOS-SSN | SMB legacy. Enumerazione nomi, relay. |
| **389/636** | TCP | LDAP/LDAPS | Directory [[Active Directory]]. LDAP relay, enumerazione utenti/gruppi/computer senza autenticazione (null base). 636 = LDAPS (TLS). |
| **3268/3269** | TCP | GC LDAP/LDAPS | Global Catalog — cerca in tutto il forest. Stesso abuse di LDAP. |

### Database

| Porta | Proto | Servizio | Note di sicurezza |
|---|---|---|---|
| **1433** | TCP | MSSQL | SQL Server. `xp_cmdshell` per RCE; brute force sa account. |
| **3306** | TCP | MySQL/MariaDB | Non esporre su Internet; UDF injection per privilege escalation. |
| **5432** | TCP | PostgreSQL | COPY TO/FROM PROGRAM per RCE con permessi superuser. |
| **27017** | TCP | MongoDB | Default senza autenticazione — esposto su Internet in molte installazioni. |
| **6379** | TCP | Redis | Default senza auth; SLAVEOF per RCE, write su .ssh/authorized_keys. |

### Servizi FTP e file transfer

| Porta | Proto | Servizio | Note di sicurezza |
|---|---|---|---|
| **20/21** | TCP | FTP data/control | Credenziali in chiaro; FTP anonimo → accesso non autenticato ai file. Preferire SFTP (SSH/22) o FTPS (990). |
| **69** | UDP | TFTP | No autenticazione; directory traversal; usato per boot PXE. |

---

## Come funziona il socket: dal processo alla rete

```
Processo applicativo
       |
   socket(AF_INET, SOCK_STREAM, 0)  → fd=5 (file descriptor)
       |
   bind(fd, 0.0.0.0:80)             → il kernel registra la porta
       |
   listen(fd, 128)                   → backlog: accetta connessioni
       |
   accept(fd) → client_fd            → attende il three-way handshake
       |
   read/write(client_fd, ...)        → dati applicativi
```

Ogni connessione TCP è identificata dalla **5-tupla**: `(protocollo, src_ip, src_port, dst_ip, dst_port)`. Il kernel usa questa tupla per demultiplexare i pacchetti in arrivo al socket giusto.

---

## Porta aperta ≠ servizio noto — banner grabbing

Il numero di porta è solo una **convenzione**: un servizio può girare su qualsiasi porta. Per sapere *cosa* gira davvero si fa **banner grabbing / service detection**:

```bash
# Nmap service detection
nmap -sV -p 22,80,443,8080 10.10.10.5

# Manuale con netcat — legge il banner che il server invia all'apertura
nc 10.10.10.5 22          # banner SSH: "SSH-2.0-OpenSSH_8.9p1..."
nc 10.10.10.5 21          # banner FTP: "220 (vsFTPd 3.0.3)"
nc 10.10.10.5 25          # banner SMTP: "220 mail.example.com ESMTP Postfix"

# HTTP — header HTTP
curl -I http://10.10.10.5:8080

# Identificare servizio su porta non standard
nmap -sV -p 31337 10.10.10.5     # --version-intensity 9 per più probe
```

**Pipeline banner → CVE:**
1. `nmap -sV` → versione servizio (es. "OpenSSH 7.2p2")
2. Cerca su exploit-db / searchsploit / CVEdetails
3. `searchsploit openssh 7.2`
4. Vedi CVE → matching exploit → [[Exploitation]]

---

## Enumerazione porte in pentest — workflow

```bash
# 1. Scan iniziale veloce (top 1000 TCP)
nmap -sC -sV -oA scan_init 10.10.10.5

# 2. Tutte le porte TCP (per non perdere servizi su porte alte)
nmap -p- --min-rate 5000 -oA scan_fullports 10.10.10.5

# 3. Approfondisci solo le porte aperte trovate
nmap -p 22,80,8443 -sC -sV -A -oA scan_deep 10.10.10.5

# 4. UDP top 20 (lento — fallo mirato)
sudo nmap -sU --top-ports 20 -oA scan_udp 10.10.10.5

# 5. Banner grab manuale sulle porte interessanti
nc -vz 10.10.10.5 8080        # è aperta?
curl -Ik http://10.10.10.5:8080  # server header, redirect

# 6. Vedere porte aperte sul sistema corrente (blue team / postcompromissione)
ss -tulpn                       # Linux
netstat -ano                    # Windows (poi tasklist /fi "PID eq <pid>")
```

**Porte "strane" da non ignorare:**
- `1234`, `4444`, `5555` — numeri rotondi tipici di backdoor/listener Metasploit.
- `4443`, `8888`, `9090` — alternative web comuni su CTF/pentest.
- Qualsiasi porta > 49151 in LISTEN (non è ephemeral del kernel → qualcosa ascolta deliberatamente).

---

## Implicazioni difensive

| Principio | Dettaglio pratico |
|---|---|
| **Minimo privilegio sulle porte** | Apri solo le porte strettamente necessarie. Ogni porta = potenziale vettore. Audit periodico con `ss -tulpn` o [[Nmap]] su se stessi. |
| **Segmentazione** | Database (3306, 5432, 1433) non devono essere raggiungibili dall'esterno; VLAN separata per admin (22, 3389, 5985). |
| **Servizi legacy** | Telnet (23), FTP (21), SNMP v1/v2 (161), RDP (3389) su Internet = bersagli automatici. Disabilita o rimpiazza. |
| **Porte non standard** | Spostare SSH dalla 22 riduce il rumore degli scanner automatici, ma non è sicurezza reale (security by obscurity). Combinare con autenticazione a chiave e `fail2ban`. |
| **Firewall in ingresso E uscita** | Molti dimenticano le regole di egress: C2 e exfiltrazione usano porte comuni (80, 443, 53) in uscita. |
| **Honeypot** | Aprire deliberatamente porte "appetibili" (es. 3389 fake) per rilevare scansioni. |
| **Verifica post-hardening** | Dopo la configurazione, fai uno scan Nmap su te stesso per confermare che solo le porte volute siano aperte. |

---

## Identificazione rapida dei servizi a memoria

La regola mnemonica per le porte più comuni in ordine numerico:
```
20/21  FTP (data/control)        → in chiaro, anonimo
22     SSH                       → cifrato, chiavi
23     Telnet                    → in chiaro, da eliminare
25     SMTP                      → email in uscita
53     DNS                       → TCP e UDP
67/68  DHCP                      → UDP broadcast
80     HTTP                      → web senza TLS
88     Kerberos                  → AD auth
110    POP3                      → email in chiaro
123    NTP                       → sincronizzazione ora (UDP)
135    MSRPC                     → Windows RPC
139    NetBIOS-SSN               → SMB legacy
143    IMAP                      → email in chiaro
161    SNMP                      → monitoring (UDP)
389    LDAP                      → directory AD
443    HTTPS                     → web con TLS
445    SMB                       → file sharing Windows
636    LDAPS                     → LDAP su TLS
1433   MSSQL                     → database
3306   MySQL                     → database
3389   RDP                       → desktop remoto Windows
5985   WinRM HTTP                → PowerShell remoting
8080   HTTP alternativo          → web server secondari
```

---

## Domande da esame/colloquio

1. **Qual è la differenza tra well-known, registered e dynamic ports?** Well-known (0-1023): riservate ai servizi standard, richiedono privilegi di sistema per ascoltare. Registered (1024-49151): assegnate da IANA a software specifici. Dynamic/Ephemeral (49152-65535): assegnate dal kernel ai client per ogni connessione in uscita; non identificano servizi permanenti.

2. **Perché la stessa porta su TCP e UDP è indipendente?** Perché TCP e UDP sono protocolli distinti a livello di trasporto — il kernel li smista separatamente. DNS/53 su UDP e DNS/53 su TCP sono due socket diversi. Un processo può ascoltare su entrambi contemporaneamente (e il DNS lo fa davvero).

3. **Cos'è il banner grabbing e a cosa serve nel pentest?** È la lettura del messaggio che un servizio invia spontaneamente all'apertura della connessione (banner). Rivela il tipo di software e la versione (es. "OpenSSH 7.2p2"), che poi si cerca su exploit-db per trovare CVE associati. È il ponte tra scansione porte ed exploitation.

4. **Perché fare uno scan di tutte le 65535 porte e non solo le top 1000?** Molti servizi su macchine CTF/reali girano su porte non standard (es. SSH su 2222, web su 8080, backdoor su 31337). La scansione di default Nmap copre solo le 1000 porte più comuni statisticamente — porte alte sfruttate sfuggono completamente.

5. **Quali porte sono i bersagli più critici per un attaccante esterno?** 22 (SSH brute force/vulnerabilità), 3389 (RDP BlueKeep, brute force), 445 (SMB EternalBlue, relay), 443/80 (web app vulnerabilities), 161/UDP (SNMP community string), 21 (FTP anonymous/credenziali in chiaro), 23 (Telnet in chiaro).

6. **Cos'è una ephemeral port e quando viene usata?** È una porta temporanea assegnata dal kernel al client (sorgente) per ogni connessione in uscita. L'intervallo è configurabile (Linux: tipicamente 32768-60999). Permette al kernel di demultiplexare le risposte tra le molte connessioni simultanee di un client.

---

## Attacco vs Difesa — tabella sinottica

| Vettore | Porta | Attacco tipico | Difesa |
|---|---|---|---|
| SSH | 22 | Brute force, chiavi deboli | Autenticazione a chiave, fail2ban, porta non standard + VPN |
| Telnet | 23 | Sniffing credenziali | Disabilitare, usare SSH |
| FTP anonimo | 21 | Accesso non autenticato ai file | Disabilitare accesso anonimo, usare SFTP |
| SMB | 445 | EternalBlue, NTLM relay | Patch, SMB signing, bloccare dall'esterno |
| RDP | 3389 | BlueKeep, brute force, pass-the-hash | NLA obbligatorio, VPN, NPS gateway, patch |
| SNMP | 161 | Community string dump | SNMPv3 con auth/priv, firewall su 161 UDP |
| DNS | 53 | Amplification, tunneling, cache poisoning | Rate limiting, Response Policy Zone, DNSSEC |
| LDAP | 389 | Null bind enum, relay NTLM | LDAPS, richiedere autenticazione anche per lettura |
| MySQL | 3306 | Brute force, UDF injection | Non esporre su 0.0.0.0, bind solo su 127.0.0.1 |
| Redis | 6379 | No-auth config → RCE via slaveof | Autenticazione, bind su loopback, rename comandi pericolosi |

---

## Collegamenti
- [[TCP]] — il trasporto connection-oriented su cui vivono la maggior parte delle porte well-known
- [[UDP]] — le porte UDP (DNS, DHCP, SNMP, NTP) e i loro vettori di attacco
- [[Three-Way Handshake TCP]] — come si apre una connessione verso una porta
- [[ICMP]] — non usa porte; ma è spesso usato per host discovery pre-portscan
- [[DNS]] — porta 53 TCP/UDP, zone transfer, amplification
- [[DHCP]] — porta 67/68 UDP
- [[HTTP e HTTPS]] — porte 80 e 443
- [[SSH]] — porta 22
- [[SMB]] — porta 445 e 139
- [[RDP]] — porta 3389
- [[Active Directory]] — porte Kerberos (88), LDAP (389/636), GC (3268/3269)
- [[Scansione delle Porte]] — metodologia pentest per scoprire porte aperte
- [[Enumerazione]] — da porta aperta a versione a CVE
- [[Nmap]] — lo strumento standard per la scansione e il banner grabbing
- [[Modello TCP-IP]] — le porte esistono al livello di trasporto (L4)

## Fonti
- IANA – Service Name and Transport Protocol Port Number Registry: https://www.iana.org/assignments/service-names-port-numbers/
- Wikipedia – List of TCP and UDP port numbers: https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
- HackTricks – Pentesting Network: https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network
