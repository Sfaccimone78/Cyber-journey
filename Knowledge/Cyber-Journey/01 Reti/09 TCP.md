---
tipo: entita
tag: [reti]
fase: 1
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["TCP"]
---

# TCP

## Cos'è
**TCP** (Transmission Control Protocol, RFC 9293) è il protocollo di trasporto **orientato alla
connessione** del [[Modello TCP-IP]]. Garantisce consegna **affidabile, ordinata e senza duplicati**, a
costo di latenza e overhead maggiori di [[UDP]]. Opera al livello 4 ([[Modello OSI]]) e identifica le
applicazioni tramite **porte**. Tre garanzie che UDP non dà: *consegna* (ritrasmette ciò che si perde),
*ordine* (riassembla in sequenza), *integrità del flusso* (numera ogni byte).

## L'header TCP campo per campo (20 byte minimi)
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-------------------------------+-------------------------------+
|          Source Port          |       Destination Port        |  quali processi
+---------------------------------------------------------------+
|                        Sequence Number                        |  posizione del 1° byte
+---------------------------------------------------------------+
|                     Acknowledgment Number                     |  prossimo byte atteso
+-------+-----------+-+-+-+-+-+-+-------------------------------+
| Offset| Reserved  |U|A|P|R|S|F|            Window             |  flag + flow control
+-------------------------------+-------------------------------+
|           Checksum            |         Urgent Pointer        |  integrità
+-------------------------------+-------------------------------+
|                    Options (es. MSS, SACK, ...)               |
+---------------------------------------------------------------+
```
- **Sequence / Acknowledgment Number** (32 bit ciascuno): il cuore dell'affidabilità. Ogni **byte** è
  numerato; l'ACK conferma "ho ricevuto fino a qui, mandami il prossimo".
- **Data Offset**: lunghezza header (per via delle Options di lunghezza variabile).
- **Window**: byte che il ricevente può ancora accettare (controllo di flusso).
- **Checksum**: integrità di header + dati (calcolato anche su uno pseudo-header con gli IP).
- **Options**: la più importante è **MSS** (Maximum Segment Size, negoziato nel SYN), poi SACK, Window Scaling, Timestamps.

## I sei flag di controllo
| Flag | Nome | Significato |
|---|---|---|
| **SYN** | Synchronize | apre la connessione, sincronizza i sequence number |
| **ACK** | Acknowledgment | il campo Acknowledgment è valido (presente in quasi tutti i segmenti) |
| **FIN** | Finish | chiusura ordinata: "ho finito di inviare" |
| **RST** | Reset | abort immediato (porta chiusa, errore, rifiuto) |
| **PSH** | Push | consegna subito i dati all'app, non bufferizzare (interattività) |
| **URG** | Urgent | dati urgenti (Urgent Pointer) — quasi mai usato, anzi pericoloso |

## Three-way handshake e chiusura
```
Apertura (3 vie):                    Chiusura ordinata (4 vie):
Client → SYN (seq=x)                 A → FIN (seq=u)
       ← SYN-ACK (seq=y, ack=x+1)      ← ACK (ack=u+1)
       → ACK (ack=y+1)                 ← FIN (seq=v)
   → ESTABLISHED                       → ACK (ack=v+1) → TIME_WAIT
```
Dettagli in [[Three-Way Handshake TCP]]. La chiusura è a **4 vie** perché ogni lato chiude
indipendentemente la propria direzione (full-duplex). Chi inizia la chiusura resta in **TIME_WAIT**
(~2×MSL) per assorbire pacchetti ritardatari ed evitare che si confondano con una nuova connessione
sulla stessa coppia di porte.

## Sequence/ACK in pratica (esempio numerico)
```
Client sceglie ISN x=1000, invia SYN.        seq=1000
Server risponde SYN-ACK, ISN y=5000.         seq=5000, ack=1001  (atteso il byte 1001)
Client ACK.                                  seq=1001, ack=5001
Client invia 200 byte di dati.               seq=1001 .. 1200
Server conferma.                             ack=1201            ("dammi dal 1201")
```
Il SYN "consuma" un numero di sequenza (per questo `ack = seq+1` nell'handshake). Se un ACK non arriva
entro il timeout (**RTO**, stimato dal RTT), il segmento viene **ritrasmesso**.

## Affidabilità, flusso, congestione
| Meccanismo | Cosa fa | Protegge |
|---|---|---|
| **Ritrasmissione (RTO)** | segmento senza ACK entro timeout → reinviato | la consegna |
| **Fast retransmit** | 3 ACK duplicati → ritrasmette subito, senza aspettare l'RTO | la latenza |
| **Ordine** | riassembla via sequence number; **SACK** conferma blocchi non contigui | la correttezza |
| **Controllo di flusso** | finestra scorrevole (Window): non sommerge il **ricevente** | il ricevente |
| **Controllo di congestione** | slow start, congestion avoidance (AIMD): non sommerge la **rete** | la rete |

**Flusso vs congestione** (spesso confusi): il *flusso* protegge il ricevente lento (lo dice la Window
del peer); la *congestione* protegge la rete condivisa (la stima il mittente dalle perdite). Il
mittente invia il **minimo** tra finestra di ricezione e finestra di congestione.

**Controllo di congestione in breve**: *slow start* (la finestra cresce esponenzialmente — raddoppia ogni
RTT — fino alla soglia **`ssthresh`**), poi *congestion avoidance* (crescita lineare, +1 MSS per RTT);
una perdita riduce la finestra (**AIMD** = Additive Increase, Multiplicative Decrease). Algoritmi: Reno,
CUBIC (default Linux, funzione cubica del tempo — ideale per reti ad alto banda×ritardo), BBR (Google,
basato su stima di banda e RTT).

**Fast Recovery** (dopo un fast retransmit): TCP **non** torna a slow start; dimezza la finestra e riprende
l'additive increase, perché gli ACK che continuano ad arrivare confermano che la rete sta ancora
consegnando (*self-clocking*). Il drop completo a slow start si riserva al **timeout** (perdita grave).

> [!note] Zero Window Probe
> Se il ricevente annuncia `Window = 0` (buffer pieno), il mittente si ferma ma invia periodici
> **Zero Window Probe** per accorgersi di quando la finestra si riapre, evitando uno stallo permanente.

## Stati della connessione (osservabili con `ss`/`netstat`)
```
CLOSED → LISTEN → SYN-RECEIVED → ESTABLISHED → ... → FIN-WAIT/CLOSE-WAIT → TIME-WAIT → CLOSED
```
- **LISTEN**: un server aspetta connessioni su una porta.
- **SYN-SENT / SYN-RECEIVED**: handshake in corso.
- **ESTABLISHED**: connessione attiva.
- **TIME-WAIT**: chi ha chiuso per primo, in attesa di sicurezza. Molti TIME-WAIT su un server = tante
  connessioni brevi (normale per HTTP), ma può esaurire le porte effimere.
- **CLOSE-WAIT**: l'altro lato ha chiuso, il locale no. **Molti CLOSE-WAIT = bug applicativo** (l'app non
  chiama `close()`).

## Comandi pratici
```bash
ss -tnp                 # connessioni TCP attive + stato + processo  (preferito a netstat)
ss -tlnp                # solo porte in LISTEN (cosa è esposto)
nc -v 192.168.1.10 80   # apri una connessione TCP a mano
# Wireshark: tcp.flags.syn==1 && tcp.flags.ack==0   → solo i SYN iniziali (nuove connessioni)
#            tcp.analysis.retransmission            → ritrasmissioni (rete o scan)
```

## Rilevanza per la sicurezza
- **Flag e scan**: [[Nmap]] sfrutta i flag per sondare senza completare l'handshake.
  - `-sS` **SYN scan** (half-open): SYN → SYN-ACK = aperta, → RST = chiusa. Non completa, meno loggato.
  - `-sT` connect: handshake completo (no root, più rumoroso).
  - `-sF`/`-sN`/`-sX` **FIN/NULL/Xmas**: porta chiusa risponde RST, aperta tace → evadono firewall stateless (non Windows).
- **SYN flood** ([[DoS e DDoS]]): valanga di SYN senza ACK finale satura la tabella delle connessioni
  half-open. Difesa: **SYN cookies** (il server non alloca stato finché l'handshake non si completa,
  codificando lo stato nel sequence number).
- **RST injection**: chi conosce/indovina la 4-tupla e i seq può iniettare un RST e **troncare** una
  connessione (censura, hijack). Difesa: cifratura (TLS) e seq imprevedibili.
- **Sequence number prediction / session hijacking**: con ISN prevedibili un attaccante off-path può
  iniettare dati in una sessione. Mitigato dagli **ISN randomizzati** (RFC 6528).
- **Connessione vs porta**: una porta in `LISTEN` esposta è superficie d'attacco → `ss -tlnp` è il primo
  controllo di hardening (chiudi ciò che non serve).

## Quando TCP, quando UDP
TCP quando la **correttezza** conta più della velocità (web, file, email, [[SSH]]). [[UDP]] quando la
**latenza** conta più della perfezione (VoIP, gaming, streaming, query [[DNS]]). QUIC (HTTP/3) reintroduce
l'affidabilità *sopra* UDP per evitare i limiti di TCP.

## Domande da esame/colloquio
1. **Perché l'handshake è a 3 vie e la chiusura a 4?** L'apertura sincronizza entrambi gli ISN in 3
   messaggi; la chiusura è full-duplex, ogni lato chiude la sua direzione (FIN+ACK ×2).
2. **Differenza tra controllo di flusso e di congestione?** Flusso protegge il ricevente (Window del
   peer); congestione protegge la rete (stima dalle perdite, AIMD).
3. **Cosa indicano molti CLOSE-WAIT?** Bug applicativo: l'app non chiude i socket dopo che il peer ha
   inviato FIN.
4. **A cosa serve TIME-WAIT?** Assorbire pacchetti ritardatari ed evitare che si confondano con una
   nuova connessione sulla stessa 4-tupla.
5. **Come funziona un SYN flood e come ci si difende?** Tanti SYN senza ACK riempiono la tabella
   half-open; i SYN cookies evitano di allocare stato fino al completamento dell'handshake.
6. **Cosa fa un RST e come può essere abusato?** Aborto immediato; iniettato da un attaccante tronca una
   connessione (DoS/censura) se ne conosce 4-tupla e sequence.

## Collegamenti
- [[Three-Way Handshake TCP]] — l'apertura in dettaglio · [[UDP]] — l'alternativa senza connessione
- [[Modello TCP-IP]] · [[Modello OSI]] · [[Porte e Protocolli Comuni]]
- [[Nmap]] — abusa dei flag per lo scanning · [[DoS e DDoS]] — SYN flood
- [[Wireshark]] — analizzare flag, seq/ack, ritrasmissioni · [[ICMP]]

## Fonti
- RFC 9293 — Transmission Control Protocol: <https://datatracker.ietf.org/doc/html/rfc9293>
- RFC 6528 — Defending against Sequence Number Attacks: <https://www.rfc-editor.org/rfc/rfc6528>
- Cloudflare — What is TCP/IP: <https://www.cloudflare.com/learning/ddos/glossary/tcp-ip/>
- Peterson & Davie — *Computer Networks: A Systems Approach* (cap. "End-to-End — TCP" e "Congestion Control": sliding window, AIMD, slow start, fast retransmit/recovery, CUBIC): <https://book.systemsapproach.org/>
