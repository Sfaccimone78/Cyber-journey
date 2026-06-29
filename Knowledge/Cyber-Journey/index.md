---
tipo: sintesi
tag: [indice]
aggiornato: 2026-06-28
stato: attivo
---

# Indice della Wiki

Catalogo di tutto il contenuto, organizzato per area. L'LLM lo legge per primo durante le query e lo
aggiorna a ogni ingestione. Mappa concettuale → `[[overview|Overview]]`. Regole → `WIKI_SCHEMA.md`.

> **~360 pagine** in 21 aree · livello principiante → esperto · italiano.
> Ogni area è una **cartella numerata**; dentro, le note sono numerate in **ordine d'apprendimento**.
> Per studiare un tema dall'inizio alla fine apri la sua **Mappa** qui sotto e segui i numeri.

---

## 🧭 Mappe per area (entra da qui)

Ogni mappa elenca le pagine dell'area in ordine, con navigazione ← prec / succ →.

0. [[00 — Home|🏡 Home Dashboard]] — Mappa centrale (punto d'accesso per principianti)
1. [[00 — Mappa Fondamenti|🟢 Fondamenti]] — parti da qui
2. [[00 — Mappa Reti|🌐 Reti]]
3. [[00 — Mappa Linux|🐧 Linux]]
4. [[00 — Mappa Crittografia|🔐 Crittografia]]
5. [[00 — Mappa Windows e AD|🪟 Windows e AD]]
6. [[00 — Mappa Web OWASP|🕸️ Web / OWASP]]
7. [[00 — Mappa Metodologia e Tool|🎯 Metodologia e Tool]]
8. [[00 — Mappa Blue Team|🛡️ Blue Team]]
9. [[00 — Mappa Sistemi Operativi|⚙️ Sistemi Operativi]]
10. [[00 — Mappa Python|🐍 Python]]
11. [[00 — Mappa Algoritmi e Strutture Dati|🧮 Algoritmi e Strutture Dati]]

**Aree avanzate (expert):**
12. [[00 — Mappa Cloud Security|☁️ Cloud Security]]
13. [[00 — Mappa AppSec Avanzato|🧪 AppSec Avanzato]]
14. [[00 — Mappa Reverse Engineering e Exploit Dev|🔬 Reverse Engineering e Exploit Dev]]
15. [[00 — Mappa DFIR e Detection Engineering|🔎 DFIR e Detection Engineering]]
16. [[00 — Mappa Mobile Security|📱 Mobile Security]]
17. [[00 — Mappa Wireless & Radio|📶 Wireless & Radio]]
18. [[00 — Mappa API e GraphQL Security|🔌 API e GraphQL Security]]
19. [[00 — Mappa AI e LLM Security|🤖 AI e LLM Security]]
20. [[00 — Mappa DevSecOps e Supply Chain|🔁 DevSecOps e Supply Chain]]
21. [[00 — Mappa GRC e Compliance|📋 GRC e Compliance]]

**Percorsi trasversali:** [[Learning Path]] (curriculum fase 0→4) · [[Matrice Ruolo-Cert]] (studio per ruolo/cert).

**Percorso consigliato neofita:** Fondamenti → Reti → Linux → Crittografia → Windows → Web → Metodologia → Blue Team → Python.
**Fondamenti CS (trasversali):** Sistemi Operativi e Algoritmi e Strutture Dati — teoria di supporto, leggibili in parallelo.

---

## Contenuto per area

> I link sotto usano i nomi senza numero: risolvono comunque grazie agli `aliases` nel frontmatter.

### 🟢 00 Fondamenti
[[Cos'è la Sicurezza Informatica]] · [[Triade CIA]] · [[Tipi di Hacker]] · [[Vulnerabilità Exploit e Minaccia]] · [[Superficie di Attacco]] · [[CVE e CVSS]] · [[Difesa in Profondità]] · [[La Cyber Kill Chain]] · [[Percorsi di Carriera Pentester vs SOC]] · [[Certificazioni Cybersecurity]] · [[Social Engineering e Phishing]] · [[Risk Management e Compliance]] · [[IAM e Zero Trust]] · [[Threat Modeling]] · [[Secure Coding]] · [[Glossario degli Acronimi]]

### 🌐 01 Reti
[[Rete Informatica e i suoi Componenti]] · [[Hardware di Rete]] · [[Modello OSI]] · [[Modello TCP-IP]] · [[Indirizzamento IP]] · [[Subnetting]] · [[MAC Address]] · [[ARP]] · [[TCP]] · [[UDP]] · [[ICMP]] · [[Three-Way Handshake TCP]] · [[Porte e Protocolli Comuni]] · [[DNS]] · [[DHCP]] · [[NAT]] · [[HTTP e HTTPS]] · [[Modello Client-Server]] · [[VPN]] · [[Wireshark]] · [[SSH]] · [[Man-in-the-Middle (MITM)]] · [[DoS e DDoS]] · [[Ping e Traceroute]] · [[Routing IP]] · [[Firewall]] · [[Socket Programming]]

### 🐧 02 Linux
[[Comandi Linux di Base]] · [[Filesystem Linux]] · [[Utenti e Gruppi Linux]] · [[Permessi Linux]] · [[Processi Linux]] · [[Variabili d'Ambiente]] · [[Pipe e Redirezione]] · [[grep]] · [[find]] · [[awk]] · [[sed]] · [[sudo]] · [[Cron e Job Pianificati]] · [[Bash Scripting]] · [[SUID e SGID]] · [[Privilege Escalation Linux]] · [[OverTheWire Bandit]] · [[Capabilities Linux]] · [[Gestione Pacchetti]] · [[Strumenti di Rete CLI]] · [[Vim e Nano]]

### 🔐 03 Crittografia
[[Encoding vs Encryption]] · [[Crittografia Simmetrica]] · [[Crittografia Asimmetrica]] · [[AES]] · [[RSA]] · [[Funzioni di Hash]] · [[Hashing delle Password e Salting]] · [[Scambio di Chiavi Diffie-Hellman]] · [[Firma Digitale]] · [[Certificati Digitali e CA]] · [[TLS e SSL]] · [[OpenSSL]] · [[CyberChef]] · [[Hashcat]] · [[John the Ripper]] · [[Crittografia a Curve Ellittiche (ECC)]] · [[GPG]]
**Primitive e modalità:** [[Modi Operativi dei Block Cipher]] · [[Stream Cipher]] · [[MAC e HMAC]] · [[Authenticated Encryption (AEAD)]] · [[Crittografia Post-Quantistica]]
**Attacchi:** [[Padding Oracle Attack]] · [[Attacchi Crittografici]]
**Appunti pratici (CryptoHack):** [[Base64]] · [[Bytes e Long]] · [[XOR]] · [[Aritmetica Modulare]]

### 🪟 04 Windows e AD
[[Filesystem Windows]] · [[Utenti e Permessi Windows]] · [[Registro di Sistema Windows]] · [[PowerShell]] · [[Windows Event Log]] · [[SMB]] · [[RDP]] · [[Active Directory]] · [[Kerberos]] · [[Privilege Escalation Windows]] · [[Pass-the-Hash]] · [[Kerberoasting]] · [[AS-REP Roasting]] · [[enum4linux]] · [[CrackMapExec]] · [[Impacket]] · [[NTLM]] · [[Mimikatz]] · [[BloodHound]] · [[LAPS]] · [[DCSync]] · [[NTLM Relay]] · [[NetExec]] · [[bloodyAD]] · [[PrinterBug e Coercizione]] · [[PowerUp]] · [[Responder]] · [[ADCS e Template Vulnerabili (ESC1-ESC8)]] · [[Delegation Kerberos (Unconstrained, Constrained, RBCD)]] · [[Shadow Credentials]] · [[Trust di Dominio e Foresta]]

### 🕸️ 05 Web / OWASP
[[OWASP Top 10]] · [[SQL Injection]] · [[Cross-Site Scripting (XSS)]] · [[Cross-Site Request Forgery (CSRF)]] · [[Broken Access Control e IDOR]] · [[Command Injection]] · [[Server-Side Request Forgery (SSRF)]] · [[XML External Entity (XXE)]] · [[File Inclusion (LFI e RFI)]] · [[Vulnerabilità Upload File]] · [[Security Misconfiguration]] · [[Autenticazione e Gestione Sessioni]] · [[Cookie e JWT]] · [[Server-Side Template Injection (SSTI)]] · [[Insecure Deserialization]] · [[CORS Misconfiguration]] · [[Clickjacking]] · [[Cryptographic Failures]] · [[Componenti Vulnerabili]] · [[Insecure Design]] · [[Logging e Monitoring Failures]] · [[Burp Suite]] · [[OWASP ZAP]] · [[sqlmap]] · [[PortSwigger Web Academy]]

### 🎯 06 Metodologia e Tool
[[Metodologia del Pentest]] · [[Ricognizione (Recon)]] · [[OSINT]] · [[Scansione delle Porte]] · [[Enumerazione]] · [[Exploitation]] · [[Post-Exploitation]] · [[Reverse Shell e Bind Shell]] · [[Nmap]] · [[Gobuster]] · [[ffuf]] · [[Nikto]] · [[Hydra]] · [[netcat]] · [[Metasploit]] · [[Kali Linux]] · [[Lateral Movement]] · [[Pivoting]] · [[Port Forwarding]] · [[Reporting Pentest]] · [[PEAS]] · [[Meterpreter]] · [[msfvenom]] · [[Metodologia CTF]] · [[Privilege Escalation (Concetti)]] · [[Attacchi di Rete]] · [[Strumenti da studiare in futuro]]

### 🛡️ 07 Blue Team
[[SIEM]] · [[Log Analysis]] · [[Detection di Attacchi]] · [[Triage degli Alert]] · [[Incident Response]] · [[Indicatori di Compromissione (IOC)]] · [[Threat Intelligence]] · [[MITRE ATT&CK]] · [[Analisi Malware di Base]] · [[Splunk]] · [[VirusTotal]] · [[Any.run]] · [[MITRE ATT&CK Navigator]] · [[LetsDefend]] · [[Sysmon]] · [[YARA]] · [[Regole Sigma]] · [[Volatility (Memory Forensics)]] · [[EDR e XDR]]

### ⚙️ 08 Sistemi Operativi
[[Processi]] · [[Scheduling]] · [[Concorrenza e Thread]] · [[Memoria Virtuale]] · [[Filesystem]] · [[I/O e Storage]] · [[Virtualizzazione]]

### 🐍 09 Python
[[Python per la Sicurezza]] · [[Socket e Port Scanner]] · [[Requests e HTTP]] · [[Parsing con os e re]] · [[Automazione Offensiva]] · [[pwntools Base]] · [[Tool di Rete in Python]]

### 🧮 10 Algoritmi e Strutture Dati
[[Complessità Computazionale]] · [[Array vs Linked List]] · [[Stack, Queue e Deque]] · [[Hash Table]] · [[Alberi Binari e BST]] · [[Heap e Priority Queue]] · [[Skip List]] · [[Trie]] · [[Grafi]] · [[Algoritmi di Ricerca]] · [[Algoritmi di Ordinamento]] · [[BFS e DFS]] · [[Algoritmo di Dijkstra]] · [[Algoritmo di Bellman-Ford]] · [[Divide et Impera]] · [[Programmazione Dinamica]] · [[Algoritmi Greedy]] · [[Backtracking]] · [[Algoritmi Crittografici]]

---

## 🚀 Aree avanzate (expert)

> Livello fase 3-4. Vedi [[Analisi e Roadmap Expert]].

### ☁️ 11 Cloud Security
[[Fondamenti Cloud e Shared Responsibility]] · [[IAM Cloud (utenti, ruoli, policy)]] · [[AWS Sicurezza (S3, EC2, IAM, STS)]] · [[Azure e Entra ID Sicurezza]] · [[SSRF e Metadata Service (IMDS)]] · [[Privilege Escalation in Cloud]] · [[Container Security (Docker)]] · [[Kubernetes Security (RBAC, escape)]] · [[Logging e Detection Cloud (CloudTrail)]]

### 🧪 12 AppSec Avanzato
[[Insecure Deserialization Avanzata (gadget chains)]] · [[Attacchi JWT]] · [[OAuth 2.0 e OpenID Connect Attacks]] · [[SAML e SSO Attacks]] · [[HTTP Request Smuggling]] · [[Prototype Pollution]] · [[Race Condition Web]] · [[GraphQL Security]] · [[Web Cache Poisoning]] · [[SSTI Avanzato e Sandbox Escape]]

### 🔬 13 Reverse Engineering e Exploit Dev
[[Assembly x86-64 Essenziale]] · [[Analisi Statica con Ghidra]] · [[Analisi Dinamica con GDB e x64dbg]] · [[Malware Analysis (statica e dinamica)]] · [[Tecniche Anti-Analisi e Unpacking]] · [[Stack Buffer Overflow]] · [[ret2libc e ROP]] · [[Bypass Protezioni (ASLR, DEP, Stack Canary, PIE)]] · [[Format String Exploitation]] · [[Heap Exploitation (introduzione)]]

### 🔎 14 DFIR e Detection Engineering
[[Digital Forensics Fondamenti]] · [[Memory Forensics con Volatility]] · [[Disk Forensics e Timeline Analysis]] · [[Windows Forensics (artefatti)]] · [[Log Analysis Avanzata e Correlazione]] · [[Detection Engineering]] · [[Threat Hunting]] · [[Query di Hunting (KQL e SPL)]] · [[MITRE D3FEND e Purple Teaming]] · [[Threat Intelligence (Diamond Model, Pyramid of Pain)]]

### 📱 15 Mobile Security
[[Fondamenti Mobile]] · [[Android Pentest]] · [[iOS Pentest]] · [[OWASP MASVS e MASTG]] · [[Intercettazione traffico e API mobile]] · [[Insecure Data Storage e Crypto su mobile]]

### 📶 16 Wireless & Radio
[[Fondamenti Wireless e 802.11]] · [[WEP, WPA, WPA2 e WPA3]] · [[Attacchi WPA2 (handshake e PMKID)]] · [[Evil Twin e Rogue AP]] · [[Wireless Tooling (aircrack-ng, hashcat)]] · [[Bluetooth, BLE e RFID-NFC]]

### 🔌 17 API e GraphQL Security
[[Fondamenti API e REST Security]] · [[OWASP API Security Top 10]] · [[BOLA e BFLA]] · [[Autenticazione e Autorizzazione API]] · [[Mass Assignment, SSRF e Rate Limiting API]] · [[API Testing e Tooling]]

### 🤖 18 AI e LLM Security
[[Fondamenti AI e LLM Security]] · [[OWASP Top 10 for LLM Applications]] · [[Prompt Injection (direct e indirect)]] · [[Data e Model Poisoning]] · [[Insecure Output e Supply Chain LLM]] · [[Difesa e Red Teaming LLM]]

### 🔁 19 DevSecOps e Supply Chain
[[Fondamenti DevSecOps]] · [[Sicurezza CI-CD Pipeline]] · [[SAST, DAST e SCA]] · [[Supply Chain e Dependency Confusion]] · [[SBOM e SLSA]] · [[Secrets Management e IaC Security]]

### 📋 20 GRC e Compliance
[[Fondamenti GRC]] · [[ISO 27001 e ISMS]] · [[NIST CSF e 800-53]] · [[Risk Management e Quantificazione]] · [[GDPR Operativo]] · [[Audit e Framework (SOC 2, PCI-DSS)]]

---

## 🧭 Sintesi
- [[overview|Overview]] — mappa principale + tesi in evoluzione
- [[Learning Path]] — curriculum end-to-end (fase 0→4) · [[Matrice Ruolo-Cert]] — studio per ruolo/cert
- [[Mappa della Crittografia]] · [[Lo stack di rete]] · [[I tre pezzi dell'OS]] — mappe di dominio
- [[Big-O Cheatsheet]] · [[Da problema ad algoritmo]] — algoritmi
- [[Linux Essentials]] — linux
- [[Matrice Attacco-Difesa]] · [[Roadmap di Apprendimento]] · [[Arsenale Tool]] — sicurezza

## 📥 Fonti
Riepiloghi-fonte (libri e risorse) che alimentano le pagine:
- [[Fonte - Black Hat Python]] · [[Fonte - Crypto 101|Crypto 101]] · [[Fonte - Security Engineering|Security Engineering]] · [[Fonte - OWASP Top 10|OWASP Top 10]]
- [[Fonte - The Linux Command Line|The Linux Command Line]] · [[Fonte - OSTEP|OSTEP]] · [[Fonte - Algorithms (Jeff Erickson)|Algorithms]] · [[Fonte - Open Data Structures|Open Data Structures]]

---

## Viste automatiche (Dataview)

> Richiede il plugin **dataview** (attivo). Le query coprono tutto il vault e filtrano per `tipo`.

### Tutte le pagine per tipo, area e fase
```dataview
TABLE tipo, tag, fase, stato
WHERE tipo = "concetto" OR tipo = "entita"
SORT file.folder ASC, file.name ASC
```

### Pagine da approfondire (stub)
```dataview
LIST
WHERE (tipo = "concetto" OR tipo = "entita") AND stato = "stub"
SORT file.name ASC
```

### Conteggio per area
```dataview
TABLE length(rows) AS "Pagine"
WHERE tipo = "concetto" OR tipo = "entita"
GROUP BY tag
```
