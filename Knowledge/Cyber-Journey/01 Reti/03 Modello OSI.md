---
tipo: concetto
tag: [reti]
fase: 1
fonti: 5
aggiornato: 2026-06-26
stato: maturo
aliases: ["Modello OSI"]
---

# Modello OSI

## In breve
Il modello **OSI** (Open Systems Interconnection, ISO/IEC 7498-1, 1984) descrive la comunicazione di
rete in **sette livelli** sovrapposti. Non è il modello realmente implementato su Internet (che usa il
[[Modello TCP-IP]]), ma resta il riferimento universale per **studiare, diagnosticare e classificare**
problemi e attacchi: *"a che livello opera questa cosa?"* è la prima domanda di ogni analista. Il
principio chiave è la **separazione delle responsabilità**: ogni livello risolve un problema preciso e
offre un servizio a quello sopra, ignorando come lavorano gli altri.

## Perché a strati? Il principio di astrazione
Senza strati, ogni applicazione dovrebbe sapere tutto: come modulare i bit sul cavo, come instradare,
come ritrasmettere i pacchetti persi. Con gli strati, ognuno **incapsula** la propria complessità ed
espone un'interfaccia semplice. Conseguenze pratiche:
- **Interoperabilità**: puoi cambiare il L1 (rame → fibra → Wi-Fi) senza toccare TCP o HTTP sopra.
- **Indipendenza**: il browser (L7) non sa se sotto c'è Ethernet o Wi-Fi.
- **Diagnosi**: un guasto si isola a *un* livello (il cavo è L1, l'ARP è L2, il DNS è L7).

Ogni livello parla **solo coi livelli adiacenti** (sopra e sotto) sullo stesso host, e **logicamente**
col livello pari (peer) sull'host remoto: il TCP del mittente "dialoga" col TCP del destinatario, anche
se fisicamente i dati scendono fino al cavo e risalgono.

## I sette livelli in dettaglio
Ogni livello serve quello sopra e usa quello sotto.

| # | Nome | Funzione | PDU | Indirizzo | Dispositivo | Esempi |
|---|------|----------|-----|-----------|-------------|--------|
| 7 | **Applicazione** | Interfaccia app/utente | Dati | — | — | HTTP, FTP, SMTP, [[DNS]], [[SSH]] |
| 6 | **Presentazione** | Codifica, cifratura, compressione | Dati | — | — | [[TLS e SSL\|TLS/SSL]], JPEG, ASCII, UTF-8 |
| 5 | **Sessione** | Apre/mantiene/chiude le sessioni | Dati | — | — | NetBIOS, RPC, [[SMB]] |
| 4 | **Trasporto** | Consegna end-to-end, porte, affidabilità | **Segmento** (TCP) / Datagram (UDP) | Porta | — | [[TCP]], [[UDP]] |
| 3 | **Rete** | Instradamento tra reti | **Pacchetto** | IP | Router, L3 switch | [[Indirizzamento IP]], [[ICMP]] |
| 2 | **Collegamento** | Trasmissione nodo-nodo sulla LAN | **Frame** | [[MAC Address]] | Switch, bridge | Ethernet, [[ARP]], PPP, 802.11 |
| 1 | **Fisico** | Segnali elettrici/ottici/radio | **Bit** | — | Hub, cavo, ripetitore | Rame, fibra, Wi-Fi, RJ45 |

**Cosa fa davvero ogni livello:**
- **L1 Fisico** — converte i bit in segnali (tensione, luce, onde radio) e viceversa. Definisce pin,
  voltaggi, codifica di linea (es. Manchester), velocità. Un *hub* lavora qui: rigenera il segnale e lo
  ripete su tutte le porte (un solo dominio di collisione).
- **L2 Collegamento** — consegna i frame *all'interno della stessa LAN* usando i [[MAC Address]].
  Sottostrati: **MAC** (accesso al mezzo, CSMA/CD) e **LLC**. Fa rilevazione errori col **FCS** (CRC nel
  trailer). Lo *switch* impara i MAC e inoltra solo alla porta giusta (separa i domini di collisione).
- **L3 Rete** — instrada i pacchetti *tra reti diverse* con l'IP logico e gerarchico. Decide il
  next-hop col *longest prefix match*, gestisce TTL e (in IPv4) la frammentazione. Il *router* vive qui.
- **L4 Trasporto** — comunicazione *processo-a-processo* tramite le **porte**. [[TCP]] = affidabile,
  ordinato, controllo di flusso/congestione (handshake, ACK, ritrasmissioni). [[UDP]] = senza
  connessione, veloce, niente garanzie.
- **L5 Sessione** — instaura, sincronizza e chiude i dialoghi; checkpoint per riprendere dopo un'
  interruzione. Spesso assorbito nelle app moderne.
- **L6 Presentazione** — traduce il formato dei dati: encoding (ASCII/UTF-8), compressione, e
  soprattutto **cifratura** ([[TLS e SSL|TLS]] è qui di concetto, anche se in pratica sta sopra TCP).
- **L7 Applicazione** — i protocolli che l'utente usa: HTTP, DNS, SMTP. Non è l'app in sé, ma
  l'interfaccia di rete che l'app sfrutta.

> [!tip] Mnemonici
> Dal basso (L1→L7): "**P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way".
> Dall'alto (L7→L1): "**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing".
> Battuta da addetti ai lavori: il **"livello 8"** è l'utente (o la politica/il budget) — la causa più
> frequente dei guasti.

## Incapsulamento (il cuore del modello)
Quando i dati scendono lo stack, **ogni livello aggiunge il proprio header** (L2 anche un trailer). Il
nome della PDU cambia a ogni livello:
```
App     [ Dati ]
L4 TCP  [ TCP-hdr(20B) | Dati ]                      → Segmento
L3 IP   [ IP-hdr(20B) | TCP-hdr | Dati ]             → Pacchetto
L2 Eth  [ Eth-hdr(14B) | IP-hdr | TCP-hdr | Dati | FCS(4B) ]  → Frame
L1      010111001010...                              → Bit sul mezzo
```
In ricezione il processo è inverso (**de-incapsulamento**): ogni livello legge e rimuove il suo header
e passa su il resto. Da qui un concetto pratico fondamentale: l'**MTU** (tipico 1500 byte su Ethernet)
è la dimensione massima del payload L3 in un frame; se un pacchetto IP è più grande, va **frammentato**
(IPv4) o scartato con un ICMP "Fragmentation Needed" (IPv6 / Path MTU Discovery). L'**overhead** degli
header riduce la banda utile: con TCP/IP su Ethernet sono ~40 byte di header per ~1460 byte di dati (MSS).

### Multiplexing e demultiplexing (la chiave di consegna)
Lo stesso link e la stessa macchina trasportano **molti flussi** contemporaneamente: il modello a strati
li separa con una **demux key** in ogni header, che il ricevente legge per consegnare il payload al
protocollo/processo giusto risalendo lo stack. Le chiavi tipiche sono: **EtherType** a L2 (`0x0800`=IPv4,
`0x0806`=ARP, `0x86DD`=IPv6 → quale L3), il campo **Protocol** a L3 (`6`=TCP, `17`=UDP, `1`=ICMP → quale
L4) e il **numero di porta** a L4 (quale processo). Incapsulamento (in invio) e demultiplexing (in
ricezione) sono le due facce dello stesso meccanismo.

## Walkthrough: cosa succede quando apri `https://sito.it`
1. **L7** — il browser forma una richiesta HTTP `GET /`. Prima però serve l'IP: query [[DNS]] (L7).
2. **L6** — la sessione viene cifrata con [[TLS e SSL|TLS]] (handshake, chiavi).
3. **L4** — TCP apre la connessione ([[Three-Way Handshake TCP]]) verso la porta 443, spezza i dati in
   segmenti, numera i byte.
4. **L3** — ogni segmento è messo in un pacchetto IP con IP sorgente/destinazione; il router sceglie il
   percorso (longest prefix match), il TTL cala a ogni salto.
5. **L2** — per uscire dalla LAN serve il MAC del **gateway**: [[ARP]] risolve IP→MAC, il pacchetto va
   in un frame Ethernet col FCS.
6. **L1** — i bit diventano segnali sul mezzo. Sul destinatario tutto risale lo stack in ordine inverso.

## Attacchi e difese per livello
| Livello | Attacco tipico | Difesa |
|---|---|---|
| 1 Fisico | Tapping del cavo, jamming Wi-Fi, keylogger HW | Accesso fisico controllato, cifratura end-to-end |
| 2 Collegamento | [[ARP]] poisoning, MAC flooding, VLAN hopping, DHCP spoofing | DAI, port security, 802.1X, DHCP snooping |
| 3 Rete | IP spoofing, ICMP tunneling, BGP hijacking | Firewall L3, anti-spoofing/uRPF, RPKI |
| 4 Trasporto | SYN flood, port scan ([[Nmap]]) | SYN cookies, rate limiting, IDS |
| 5–6 | Session hijacking, SSL stripping, downgrade | Cookie sicuri/HSTS, cifratura forte, cert pinning |
| 7 App | [[SQL Injection]], [[Cross-Site Scripting (XSS)\|XSS]], phishing | WAF, validazione input, awareness |

Esempio MITM classificato per livello: **L2** ARP poisoning (LAN), **L3** BGP hijacking (scala
Internet), **L7** SSL stripping (degrada HTTPS→HTTP). Sapere il livello dice **dove** mettere la
contromisura: un WAF (L7) non ferma un ARP poisoning (L2).

## OSI vs TCP/IP
Il [[Modello TCP-IP]] reale ha **4 livelli** che mappano l'OSI: Applicazione (OSI 5-7), Trasporto (4),
Internet (3), Accesso alla rete (1-2). OSI è il **linguaggio descrittivo** per ragionare e diagnosticare;
TCP/IP è l'**implementazione** che fa girare Internet. Nessuno "usa" OSI sul filo, tutti lo usano a parole.

## Lettura pratica in Wireshark (un livello = un blocco)
In [[Wireshark]] un pacchetto è lo stack incapsulato dall'alto in basso: *Frame* → *Ethernet II* (L2,
MAC + EtherType) → *Internet Protocol* (L3, IP + TTL + proto) → *Transmission Control Protocol* (L4,
porte + flag + seq) → *payload* L7. Filtri per isolare il livello:
```
eth.addr == aa:bb:cc:dd:ee:ff     # L2
ip.addr == 10.0.0.5               # L3
tcp.port == 443                   # L4
http or tls or dns                # L7
```

## Troubleshooting: la scala dal basso
La diagnosi segue lo stack **dal basso verso l'alto** — isolare il livello = isolare il guasto:
1. **L1** — il cavo è collegato? Link led acceso? `ip link` mostra lo stato fisico.
2. **L2** — l'ARP risolve il gateway? `ip neigh` / `arp -a`. Switch/VLAN giusti?
3. **L3** — ho un IP e un default gateway? `ip addr`, `ip route`, `ping` al gateway.
4. **L4** — la porta del servizio è aperta? `nc -zv host porta`, `ss -tlnp`.
5. **L7** — il servizio risponde correttamente? `curl -v`, query DNS con `dig`.
Regola: non saltare i livelli. Un "il sito non va" può essere un cavo staccato (L1) o un DNS rotto (L7);
la scala evita di indovinare.

## Domande da esame/colloquio
1. **Differenza tra incapsulamento e de-incapsulamento?** Scendendo lo stack ogni livello *aggiunge* il
   suo header (incapsula); salendo lato ricevente ogni livello lo *rimuove* (de-incapsula).
2. **A che livello lavorano hub, switch e router?** Hub L1 (ripete i bit), switch L2 (inoltra per MAC),
   router L3 (instrada per IP). Un L3-switch fa entrambi L2/L3.
3. **Perché il modello OSI è ancora utile se Internet usa TCP/IP?** È il vocabolario comune per
   classificare attacchi/guasti e progettare difese: dice *a che livello* agire.
4. **Cos'è la PDU e come cambia per livello?** Protocol Data Unit: Dati (L5-7) → Segmento (L4) →
   Pacchetto (L3) → Frame (L2) → Bit (L1).
5. **Perché un frame ha un MTU e cosa succede se lo superi?** Il payload L3 deve entrare nel frame; oltre
   l'MTU il pacchetto si frammenta (IPv4) o viene rifiutato con ICMP (Path MTU Discovery in IPv6).

## Collegamenti
- [[Modello TCP-IP]] — l'implementazione reale a 4 livelli
- [[TCP]] · [[UDP]] — il livello 4
- [[Indirizzamento IP]] — il livello 3 · [[ICMP]]
- [[MAC Address]] · [[ARP]] — il livello 2
- [[Three-Way Handshake TCP]] · [[TLS e SSL]]
- [[Wireshark]] — vedere lo stack incapsulato pacchetto per pacchetto

## Fonti
- ISO/IEC 7498-1 — The OSI Reference Model
- Cloudflare — What is the OSI Model: <https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/>
- TryHackMe — OSI Model: <https://tryhackme.com/room/osimodelzi>
- Peterson & Davie — *Computer Networks: A Systems Approach* (cap. "Foundation — Network Architecture": layering, encapsulation, multiplexing): <https://book.systemsapproach.org/>
- Beej's Guide to Network Programming — "Low level Nonsense" (modello a layer): <https://beej.us/guide/bgnet/>
