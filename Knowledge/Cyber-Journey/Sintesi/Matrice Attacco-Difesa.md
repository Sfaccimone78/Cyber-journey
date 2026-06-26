---
tipo: sintesi
tag: [metodologia, blue-team, sintesi]
fase: 0
aggiornato: 2026-06-25
stato: attivo
aliases: ["Matrice Attacco-Difesa", "Matrice Attacco → Difesa → Detection"]
---

# Matrice Attacco → Difesa → Detection

Sintesi cross-source che mappa, per dominio, **vettore → tecnica → tool → difesa → detection**. Pensata per CTF/pentest etico e blue team. Ogni riga rimanda alle pagine concept.

## 🌐 Web
| Vettore | Tecnica | Tool | Difesa | Detection |
|---|---|---|---|---|
| [[Injection]] | SQLi UNION/blind | sqlmap, Burp | Prepared statement, least-priv DB | Query anomale, WAF, log DB |
| [[XSS]] | Stored/Reflected/DOM | Burp, BeEF | Output encoding, CSP, HttpOnly | CSP report, payload nei log |
| [[Broken Access Control]] | IDOR, forced browsing | Burp Intruder, Autorize | Deny-by-default, ownership check | 403/anomalie su ID enumerati |
| [[SSRF]] | Metadata cloud, port scan interno | Burp Collaborator | Allow-list, no redirect, IMDSv2 | Egress anomalo verso 169.254/interni |
| [[Authentication Failures]] | Credential stuffing, JWT `alg:none` | hydra, jwt_tool | MFA, rate limit, firma JWT | Spike login falliti, IP/UA diversi |
| File upload / RCE | Webshell, deserializzazione | Burp, ysoserial | Validazione tipo, no exec dir | Nuovi file in webroot, EDR |

## 🛰️ Network
| Vettore | Tecnica | Tool | Difesa | Detection |
|---|---|---|---|---|
| MITM | ARP spoofing | ettercap, bettercap | Dynamic ARP Inspection, TLS | ARP table anomala, IDS |
| DNS poisoning | Cache poisoning, rebinding | dnschef | DNSSEC, validazione risolutore | Risposte DNS incoerenti |
| DDoS | SYN flood, amplification | hping3, LOIC | SYN cookie, rate limit, scrubbing | Spike traffico, NetFlow |
| Sniffing | Cattura traffico in chiaro | [[Arsenale Tool]] wireshark, tcpdump | Cifratura ([[TLS/SSL]]) | Porte mirror, NIDS |
| Scanning/recon | Port/service scan | nmap, masscan | Filtraggio, minimal exposure | IDS (Snort/Suricata), conn rate |
→ Dettagli: [[Attacchi di Rete]]

## 💻 OS / Host
| Vettore | Tecnica | Tool | Difesa | Detection |
|---|---|---|---|---|
| Privilege escalation | SUID, sudo misconfig, kernel | linpeas, GTFOBins | least-priv, patch, [[Permessi dei File]] | auditd, file-integrity |
| Malware/RCE | Reverse shell, persistence | metasploit, netcat | Hardening, EDR, app-allowlist | EDR, anomalie processi |
| Credential theft | Dump hash, pass-the-hash | mimikatz, hashcat | LSASS protection, MFA | Accessi LSASS, login anomali |
→ Dettagli: [[Privilege Escalation]], [[Malware]]

## 🎭 Social
| Vettore | Tecnica | Tool | Difesa | Detection |
|---|---|---|---|---|
| Phishing | Pretexting, link/credential harvest | GoPhish, SET | Awareness, MFA, DMARC | Report utenti, filtri mail |
| Vishing/baiting | Telefono, USB drop | — | Policy, formazione | Segnalazioni, DLP |
→ Dettagli: [[Social Engineering]]

## 🔐 Crypto
| Vettore | Tecnica | Tool | Difesa | Detection |
|---|---|---|---|---|
| [[Cryptographic Failures]] | Hash cracking | hashcat, john | KDF lenti (Argon2/bcrypt), salt | Spike CPU/GPU, accessi DB |
| [[Padding Oracle]] | CBC padding oracle | padbuster | AEAD (GCM), MAC-then-nothing→AE | Errori 500 ripetuti su decrypt |
| Downgrade/MITM | POODLE, sslstrip | sslstrip, testssl.sh | HSTS, TLS 1.2+/1.3 | Handshake downgrade nei log |
→ Dettagli: [[Funzioni Hash]], [[TLS/SSL]]

## Principio trasversale
Ogni difesa efficace combina **prevenzione** (design/coding sicuro), **least privilege**, **difesa in profondità** e **detection** ([[Logging e Monitoring Failures]]). Nessun singolo controllo è sufficiente. [Fonte: Anderson, *Security Engineering*, cap. 1, 21]

## Collegamenti
- Vedi anche: [[Arsenale Tool]], [[Roadmap di Apprendimento]], [[Threat Modeling]], [[Penetration Testing]], [[OWASP Top 10]], [[Security Engineering]]

## Fonti
- [OWASP Top 10:2025 — <https://owasp.org/Top10/2025/>] → [[OWASP Top 10]]
- [Anderson, *Security Engineering* — <https://www.cl.cam.ac.uk/~rja14/book.html>] → [[Security Engineering]]
- [PortSwigger Web Security Academy — <https://portswigger.net/web-security>]
