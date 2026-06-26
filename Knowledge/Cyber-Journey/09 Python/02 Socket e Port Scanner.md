---
tipo: concetto
tag: [tool, reti]
fase: 1
fonti: 4
aggiornato: 2026-06-21
stato: maturo
aliases: ["Socket e Port Scanner"]
---

# Socket e Port Scanner

> **Nota etica**: scansionare porte rivela informazioni e genera traffico anomalo. Fallo **solo** su
> host tuoi o autorizzati (TryHackMe, lab, CTF). Una scansione non autorizzata è già un'intrusione.

## In breve
Un **socket** è l'astrazione del sistema operativo per "un capo di una connessione di rete": una
coppia `(IP, porta)` su cui leggere e scrivere byte. Un [[Scansione delle Porte|port scanner]] non fa
altro che **tentare la connessione** a una porta: se il [[Three-Way Handshake TCP]] completa, la porta
è **aperta** (c'è un servizio in ascolto); se arriva un RST è **chiusa**; se non arriva nulla è
**filtrata** (firewall). Ricostruire questo da zero con `socket` spiega cosa fa [[Nmap]] sotto il cofano.

## Il modello: connect-scan TCP
Il modo più semplice e affidabile è il **TCP connect scan**: lascio che sia il SO a fare l'handshake
completo. Se `connect()` riesce → porta aperta. È rumoroso (handshake completo, loggabile dal target)
ma non richiede privilegi root, a differenza del SYN scan di [[Nmap]] (`-sS`).

## Il problema: la latenza, non la CPU
Scansionare 1.000 porte in sequenza significa **aspettare** 1.000 timeout. Il collo di bottiglia è la
rete, non il processore: il thread sta fermo in attesa. Soluzione → **threading**: lanciare decine di
connessioni in parallelo, ognuna in attesa per conto suo. Si passa da minuti a secondi.

## Script completo — scanner TCP con threading e banner grabbing

```python
#!/usr/bin/env python3
# scanner.py — TCP connect scan multithread con banner grabbing. SOLO su host autorizzati.

import socket                       # API socket della libreria standard
import sys                          # argomenti da riga di comando
from concurrent.futures import ThreadPoolExecutor  # pool di thread gestito
from queue import Queue            # coda thread-safe per raccogliere i risultati

# Timeout breve: oltre N secondi una porta è quasi certamente filtrata. Tenerlo basso = scan veloce.
TIMEOUT = 1.0

def scansiona_porta(host: str, porta: int) -> tuple | None:
    """Tenta la connessione TCP a una porta. Ritorna (porta, banner) se aperta, altrimenti None."""
    # socket.AF_INET = IPv4, SOCK_STREAM = TCP. Il 'with' chiude il socket anche se c'è un'eccezione.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT)       # senza timeout connect() bloccherebbe a lungo sulle porte filtrate
        # connect_ex ritorna 0 se la connessione riesce, un codice d'errore altrimenti (no eccezione)
        if s.connect_ex((host, porta)) != 0:
            return None             # porta chiusa o filtrata: scartiamo
        # Porta APERTA: proviamo il banner grabbing. Molti servizi (FTP, SSH, SMTP) salutano per primi.
        banner = ""
        try:
            s.settimeout(0.5)       # finestra breve: se il servizio non parla, non bloccarci
            banner = s.recv(1024).decode(errors="ignore").strip()  # leggi fino a 1 KB di saluto
        except socket.timeout:
            banner = "(nessun banner)"   # servizio silenzioso (es. HTTP aspetta una richiesta)
        return (porta, banner)

def main() -> None:
    # Uso: python scanner.py <host> [porta_inizio] [porta_fine]
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <host> [inizio] [fine]")
        sys.exit(1)
    host = sys.argv[1]
    inizio = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    fine   = int(sys.argv[3]) if len(sys.argv) > 3 else 1024

    # Risolviamo l'hostname in IP una volta sola (evita N query DNS, vedi [[DNS]])
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[!] Impossibile risolvere {host}")
        sys.exit(1)
    print(f"[+] Scansione di {host} ({ip}) porte {inizio}-{fine}\n")

    risultati = Queue()             # coda thread-safe: i thread ci scrivono senza pestarsi i piedi
    # ThreadPoolExecutor: 100 thread riusati per tutte le porte. Più thread = più parallelismo (e rumore).
    with ThreadPoolExecutor(max_workers=100) as pool:
        # submit() accoda un task per ogni porta; il pool li distribuisce sui worker liberi
        futures = [pool.submit(scansiona_porta, ip, p) for p in range(inizio, fine + 1)]
        for f in futures:
            esito = f.result()      # blocca finché QUEL task finisce; raccoglie il valore di ritorno
            if esito:
                risultati.put(esito)

    # Stampa ordinata: svuotiamo la coda e ordiniamo per numero di porta
    aperte = sorted(risultati.queue, key=lambda t: t[0])
    if not aperte:
        print("[-] Nessuna porta aperta nel range.")
    for porta, banner in aperte:
        print(f"  [APERTA] {porta:>5}/tcp  {banner}")

if __name__ == "__main__":
    main()
```

## La logica chiave
- **`connect_ex` vs `connect`**: `connect_ex` ritorna un **codice** invece di sollevare un'eccezione →
  niente `try/except` per ogni porta chiusa, codice più pulito e più veloce su grandi range.
- **Timeout duplice**: uno per la connessione, uno più corto per il banner. Senza timeout lo scanner
  si pianta sulle porte filtrate (nessun RST, attesa infinita).
- **ThreadPool, non thread manuali**: creare 1.024 thread a mano esaurirebbe le risorse. Il pool ne
  riusa un numero fisso (`max_workers`) — è il pattern corretto per task I/O-bound come questo.
- **Banner grabbing**: il primo passo dell'[[Enumerazione]]. Versione del servizio → ricerca CVE note.

## Esercizio progressivo
1. **Base**: aggiungi una mappa `{21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS"}` (vedi
   [[Porte e Protocolli Comuni]]) e stampa il nome del servizio atteso accanto alla porta.
2. **Intermedio**: per la porta 80, invia `b"HEAD / HTTP/1.0\r\n\r\n"` prima del `recv` per forzare
   l'header HTTP (vedi [[HTTP e HTTPS]]) e leggere il server web.
3. **Avanzato**: aggiungi `argparse` con `--top-ports` (le 100 più comuni) e `--output report.json`
   che salva i risultati in JSON, pronti da consumare in pipeline come fa [[Nmap]] con `-oJ`.

## Collegamenti
- [[Scansione delle Porte]] — la teoria dietro lo scanner
- [[Three-Way Handshake TCP]] — cosa decide aperta/chiusa
- [[TCP]] / [[Porte e Protocolli Comuni]]
- [[Nmap]] — la versione industriale di questo script
- [[Enumerazione]] — il banner grabbing è il primo passo
- [[netcat]] — banner grabbing manuale, "a mano"

## Fonti
- Python — socket: https://docs.python.org/3/library/socket.html
- Python — concurrent.futures: https://docs.python.org/3/library/concurrent.futures.html
- Nmap — Port Scanning Techniques: https://nmap.org/book/man-port-scanning-techniques.html
- Real Python — Socket Programming in Python: https://realpython.com/python-sockets/
