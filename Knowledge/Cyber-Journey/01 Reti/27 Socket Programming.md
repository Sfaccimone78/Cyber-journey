---
tipo: concetto
tag: [reti]
fase: 1
fonti: 1
aggiornato: 2026-06-26
stato: maturo
aliases: ["Socket Programming", "Socket"]
---

# Socket Programming

## In breve
Un **socket** è "un modo per parlare con altri programmi usando i normali **file descriptor** Unix":
seguendo la filosofia *everything is a file*, la comunicazione di rete avviene attraverso un descrittore
ottenuto con la **system call** `socket()`. Si possono usare `read()`/`write()`, ma `send()`/`recv()`
danno più controllo. Il socket è l'**interfaccia di servizio** ([[Modello OSI]]) che l'applicazione usa
per affacciarsi sul trasporto: tutto ciò che sta sotto (TCP/IP) lo gestisce il **kernel**.

## I due tipi principali
- **`SOCK_STREAM`** → **[[TCP]]**: connessione affidabile, ordinata, bidirezionale (telnet, SSH, HTTP).
- **`SOCK_DGRAM`** → **[[UDP]]**: datagram *connectionless*, veloce ma inaffidabile (giochi, streaming, DHCP).

### getaddrinfo() — il punto di partenza
Riempie le `struct addrinfo` necessarie e fa **lookup DNS e di servizio** (nome host → IP, nome servizio
→ porta), preparando indirizzi IPv4/IPv6 in modo agnostico. È il primo passo moderno (sostituisce il
vecchio `gethostbyname`).

## Il flusso TCP (client vs server)

```
SERVER                              CLIENT
getaddrinfo()                       getaddrinfo()
socket()      → fd                  socket()      → fd
bind()        (lega IP:porta)
listen()      (coda backlog)
accept() ───┐ blocca               connect() ──► (3-way handshake TCP)
            └─ ritorna un NUOVO fd
                  per la connessione
send()/recv() ◄──── dati ────► send()/recv()
close()                             close()
```

Punti chiave dell'API:
- **`socket(domain, type, protocol)`** → restituisce un file descriptor.
- **`bind(fd, addr, len)`** — il **server** lega il socket a `IP:porta` locale. Il **client** lo salta:
  il kernel assegna una **porta effimera** automaticamente.
- **`listen(fd, backlog)`** — marca il socket come passivo; `backlog` = lunghezza della coda di
  connessioni pendenti.
- **`accept(fd, ...)`** — **blocca** finché un client si connette, poi ritorna **un nuovo fd dedicato a
  quella connessione**; l'fd originale continua ad ascoltare (→ un server può servire molti client,
  tipicamente con fork/thread).
- **`connect(fd, serv_addr, len)`** — il **client** avvia la connessione (scatena il
  [[Three-Way Handshake TCP|3-way handshake]]).
- **`send()` / `recv()`** — scambio dati. `send()` può inviarne **meno** del richiesto (va gestito il
  valore di ritorno); `recv()` che ritorna **0** significa **connessione chiusa** dal peer.
- **`close()` / `shutdown(fd, how)`** — chiusura (how: 0=recv, 1=send, 2=entrambi).

### Flusso UDP (senza connessione)
Niente `listen`/`accept`/`connect`: si usano **`sendto()`** e **`recvfrom()`**, che portano l'indirizzo
del peer in ogni chiamata (ogni datagram è indipendente).

| | Server TCP | Client TCP |
|---|---|---|
| `bind()` | richiesto | opzionale (kernel) |
| `listen()` / `accept()` | richiesti | no |
| `connect()` | no | richiesto |

## Rilevanza per la sicurezza
- Ogni chiamata socket è una **system call**: passaggio user→kernel→ritorno (trap). È il confine
  attraversato quando l'Applicazione passa i dati al Trasporto nel [[Modello TCP-IP]] (è il kernel a
  costruire header TCP/IP).
- Un server concorrente combina socket + **processi/thread**: `accept()` poi `fork()` (un figlio per
  connessione) o un pool di thread.
- Errori non gestiti (buffer overflow nel parsing di `recv()`, mancata validazione del valore di ritorno)
  sono una fonte classica di vulnerabilità memory-safety nei servizi di rete.
- Una porta esposta in `LISTEN` (`ss -tlnp`) è il risultato di `bind()`+`listen()` di un servizio → è
  superficie d'attacco; vedi [[Porte e Protocolli Comuni]].

## Collegamenti
- [[TCP]] — `SOCK_STREAM` · [[UDP]] — `SOCK_DGRAM`
- [[Modello TCP-IP]] — l'API è il confine user/kernel tra Applicazione e Trasporto
- [[Modello OSI]] — il socket è l'interfaccia di servizio verso L4
- [[Three-Way Handshake TCP]] — scatenato da `connect()`
- [[Porte e Protocolli Comuni]] — `bind()` lega una porta locale

## Fonti
- Beej's Guide to Network Programming — "What is a socket?" e "System Calls or Bust"
  (socket/bind/listen/accept/connect/send/recv, getaddrinfo): <https://beej.us/guide/bgnet/>
