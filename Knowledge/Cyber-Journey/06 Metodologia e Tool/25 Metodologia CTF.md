---
tipo: concetto
tag: [metodologia]
fase: 2
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["Metodologia CTF", "CTF"]
---
# Metodologia CTF

## Definizione
Un **CTF** (*Capture The Flag*) è una competizione di sicurezza in cui si risolvono sfide per recuperare una **flag** (stringa segreta, es. `flag{...}` / `picoCTF{...}`) che dimostra l'avvenuto exploit. È il principale terreno di **pratica etica** e legale: i target sono volutamente vulnerabili e autorizzati. Complementa la [[Metodologia del Pentest]] (che invece simula attacchi su sistemi reali con scope contrattuale).

## Formati
- **Jeopardy**: sfide indipendenti divise per categoria e punteggio (il più comune).
- **Attack-Defense**: ogni squadra difende i propri servizi e attacca quelli altrui, in tempo reale.
- **King of the Hill**: mantenere il controllo di un host più a lungo degli altri.

## Le categorie (e l'approccio)

| Categoria | Cosa si fa | Tool/skill | Pagine collegate |
|-----------|-----------|------------|------------------|
| **Web** | SQLi, XSS, IDOR, SSRF, auth bypass | [[Burp Suite]], [[sqlmap]], [[ffuf]] | [[SQL Injection]], [[Cross-Site Scripting (XSS)]], [[Server-Side Request Forgery (SSRF)]], [[Broken Access Control e IDOR]] |
| **Crypto** | rompere cifrari/implementazioni deboli | python, sage, RsaCtfTool | [[Cryptographic Failures]], [[XOR]] |
| **Pwn (binary exploitation)** | buffer overflow, ROP, format string | pwntools, gdb+pwndbg, ghidra | [[Privilege Escalation (Concetti)]] |
| **Reverse Engineering** | capire cosa fa un binario, estrarre logica/flag | ghidra, radare2, IDA | |
| **Forensics** | analisi file/pcap/memoria/disco | wireshark, [[Volatility (Memory Forensics)]], binwalk | [[Attacchi di Rete]] |
| **OSINT** | trovare info da fonti aperte | google dork, exiftool, maps | [[OSINT]], [[Social Engineering e Phishing]] |
| **Misc / Stego / PPC** | rompicapo, steganografia, scripting | python, stegsolve, zsteg | |

## Metodologia per una sfida (Web come esempio)
```
1. Enumera   → leggi il testo, esplora l'app, mappa input/parametri (recon)
2. Ipotizza  → quale classe di vuln? (l'hint, la categoria, il comportamento)
3. Testa     → un payload per volta in Burp Repeater
4. Sfrutta   → escala dall'anomalia all'accesso ai dati / esecuzione
5. Cattura   → estrai la flag, inviala (submit)
6. Annota    → tieni un writeup: cosa, perché, come (per imparare e rifare)
```

## Pwn — pattern minimo (pwntools)
```python
from pwn import *
io = remote("host", 1337)          # o process("./chall")
payload  = b"A"*offset             # riempi fino al saved RIP
payload += p64(win_addr)           # sovrascrivi il ritorno
io.sendline(payload)
io.interactive()                   # shell → cat flag.txt
```
Concetti sotto: layout dello stack, ritorni, ASLR/NX/canary.

## Buone pratiche
- **Writeup** dopo ogni sfida: consolidano l'apprendimento (e fanno curriculum).
- **Non brute-forzare il sito di scoring** né attaccare l'infrastruttura: fuori scope = squalifica.
- I CTF insegnano **tecnica e velocità**, ma la sicurezza si padroneggia capendo il **perché** (design, threat model → [[Threat Modeling]]).
- Piattaforme di allenamento: [[PortSwigger Web Academy]] (web), picoCTF, HackTheBox, TryHackMe, OverTheWire.

## Collegamenti
- [[Metodologia del Pentest]] · [[OWASP Top 10]] · [[Privilege Escalation (Concetti)]] · [[PortSwigger Web Academy]]
- [[Cryptographic Failures]] · [[Attacchi di Rete]] · [[OSINT]]

## Fonti
- PortSwigger Web Security Academy — https://portswigger.net/web-security
- CTFtime (calendario e writeup) — https://ctftime.org/
- Anderson, *Security Engineering* — https://www.cl.cam.ac.uk/~rja14/book.html
