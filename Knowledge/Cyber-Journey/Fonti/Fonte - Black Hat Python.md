---
tipo: fonte
tag: [tool, metodologia, reti]
fase: 2
aggiornato: 2026-06-22
url: https://nostarch.com/blackhatpython
autore: Justin Seitz
---

# Fonte - Black Hat Python

> Pagina riepilogo della fonte. Il PDF grezzo è in radice (`blackhatpython.pdf`); questa pagina lo
> riassume e lo collega alla wiki. Il file grezzo non va modificato.

## Origine
- **Titolo:** *Black Hat Python — Python Programming for Hackers and Pentesters*
- **Autore:** Justin Seitz (Immunity, Inc.) · prefazione di Charlie Miller
- **Editore / anno:** No Starch Press, **2015** (1ª ed.) · ISBN 978-1-59327-590-7 · 195 pagine
- **URL:** <https://nostarch.com/blackhatpython>
- **Acquisita:** 2026-06-22

> [!warning] Codice datato — Python 2 / 2015
> Tutto il codice del libro è **Python 2.7** e usa API obsolete (`urllib2`, `print` statement, `raw_input`,
> `except E, e:`). Non gira as-is su Python 3. Nelle pagine wiki il codice è **modernizzato a Python 3**.
> Esiste una **2ª edizione (2021, Python 3)** di Seitz & Tim Arnold: preferibile se si compra il libro.

## Struttura (11 capitoli)
| Cap | Tema | Stato ingest |
|---|---|---|
| 1 | Setup ambiente (Kali, WingIDE) | saltato (obsoleto) |
| **2** | **The Network: Basics** — TCP/UDP client+server, netcat replacement, TCP proxy, SSH/Paramiko, tunneling | ✅ **ingerito** → [[Tool di Rete in Python]] |
| 3 | Raw sockets & sniffing — host discovery UDP, decode IP/ICMP | da ingerire |
| 4 | Owning the Network with Scapy — furto credenziali, ARP poisoning, PCAP | da ingerire |
| 5 | Web Hackery — dir/form bruteforce (urllib2) | coperto da [[Automazione Offensiva]] |
| 6 | Extending Burp Proxy — fuzzer, Bing, password gold | da ingerire → [[Burp Suite]] |
| 7 | GitHub Command & Control | da ingerire → C2 (pagina mancante) |
| 8 | Common Trojaning Tasks on Windows — keylogger, screenshot, shellcode exec, sandbox detect | da ingerire |
| 9 | Fun with Internet Explorer — MITB, exfil via COM | da ingerire |
| 10 | Windows Privilege Escalation — process monitor WMI, token, code injection | da ingerire → [[Privilege Escalation Windows]] |
| 11 | Automating Offensive Forensics — Volatility | da ingerire → [[Volatility (Memory Forensics)]] |

## Punti chiave (cap. 2, ingerito)
- **Tesi del libro**: la differenza fra script kiddie e professionista è *scrivere i propri tool*. Su un
  target blindato spesso manca `nc`/Wireshark/compilatore ma **Python c'è** → living-off-the-land.
- `socket` della stdlib basta per client/server TCP e UDP; in Py3 si lavora a **byte** (`.encode`/`.decode`).
- **Netcat replacement** (`bhpnet`): un solo script fa listener/client, command shell, execute, upload file.
- **Proxy TCP** intercettante con hexdump → ispeziona/modifica protocolli **non-HTTP** (FTP, SMTP) dove
  Burp non arriva; rivela credenziali in chiaro.
- **Paramiko**: SSH e **reverse tunnel** in puro Python (transport vs channel) → alternativa a `ssh -R/-L`
  dentro un proprio tool o su target senza client SSH.

## Concetti / entità toccati
- [[Tool di Rete in Python]] — pagina principale generata da questa fonte (cap. 2)
- [[Socket e Port Scanner]] · [[netcat]] · [[Reverse Shell e Bind Shell]] · [[Pivoting]] · [[Port Forwarding]]
- [[Burp Suite]] · [[Automazione Offensiva]] · [[Post-Exploitation]] · [[MITRE ATT&CK]]

## Note personali
Fonte ottima per il **percorso Pentester**: dà il "perché" del tooling artigianale, non solo il "come".
Capitoli 6, 7, 10 sono i prossimi candidati ad alto valore (Burp, C2, priv-esc Windows). Attenzione
sempre al porting Py2→Py3 quando si riusano gli snippet.

## Collegamenti
- [[index]]
- [[Tool di Rete in Python]]
