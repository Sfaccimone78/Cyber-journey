---
tipo: sintesi
tag: [reti, sintesi]
fase: 0
aggiornato: 2026-06-25
stato: attivo
aliases: ["Lo stack di rete", "Stack di rete layer per layer"]
---

# Synthesis — Lo stack di rete: un pacchetto HTTP layer per layer

Sintesi cross-source che **traccia una richiesta HTTPS** da `https://example.com` fino al server e ritorno, attraversando ogni layer dello stack. Collega [[Modello OSI]], [[Modello TCP/IP]], [[Ethernet e MAC]], [[IP Routing]], [[TCP]], [[UDP]], [[DNS]], [[HTTP/HTTPS]].

## 1. Il viaggio di una richiesta (andata)

### Passo 0 — Risoluzione del nome (DNS)
Il browser non conosce l'IP di `example.com`. Interroga il **resolver** con una query **[[DNS]]** (UDP/53) per il record **A/AAAA**. Risposta: `example.com = 93.184.216.34`. (Se DNSSEC è attivo, le RRSIG vengono validate lungo la catena di fiducia.)

### Passo 1 — Applicazione (L7)
Il browser costruisce la richiesta HTTP: `GET / HTTP/2` + header (`Host`, `User-Agent`, `Cookie`…). → [[HTTP/HTTPS]].

### Passo 2 — Presentazione/Sicurezza (L6, TLS)
**TLS 1.3** negozia chiavi e **cifra** la richiesta (HTTPS, porta 443). Confidenzialità + integrità + autenticazione del server via certificato. → [[TLS/SSL]].

### Passo 3 — Trasporto (L4, TCP)
Apertura con **three-way handshake** (SYN / SYN-ACK / ACK), poi i byte cifrati entrano nello **stream**. TCP aggiunge l'header con **porta sorgente** (effimera, es. 51200) e **destinazione 443**, numeri di **sequenza**, e li immette nella **sliding window**. → [[TCP]].
*(In HTTP/3 questo passo è QUIC su [[UDP]]: handshake e TLS collassano in uno.)*

### Passo 4 — Network (L3, IP)
Ogni segmento è incapsulato in un **datagram IP**: **IP sorgente** (il tuo) e **destinazione** (93.184.216.34), **TTL**, Protocol=6 (TCP). Il **longest prefix match** sulla **routing table** sceglie il next-hop; non essendo locale, va alla **default route** (il gateway). → [[IP Routing]].

### Passo 5 — Data Link (L2, Ethernet)
Per consegnare il pacchetto al **gateway** sul link locale serve il suo **MAC**: lo fornisce **ARP**. Il pacchetto IP è incapsulato in un **frame** con Dest MAC = gateway, EtherType 0x0800, FCS. → [[Ethernet e MAC]].

### Passo 6 — Fisico (L1)
Il frame diventa **bit** (segnali elettrici/ottici/radio) sul mezzo.

### Hop dopo hop
Ad ogni **router** il frame L2 viene **buttato e riscritto** (nuovi MAC sorgente/destinazione, TTL−1), ma l'**header IP resta** (stesso IP destinazione). Questo è il principio di Internet: **L2 è locale, L3 è end-to-end**. Sul server, lo stack risale L1→L7 in **de-incapsulamento**, ogni layer rimuove il proprio header.

## 2. Il ritorno
Il server genera `200 OK` + HTML e il pacchetto rifà il percorso inverso. Gli **ACK** TCP confermano i byte ricevuti; la **AdvertisedWindow** regola il flusso; **AIMD/slow start** adattano il ritmo alla congestione della rete. → [[TCP]].

## 3. Schema di incapsulamento

```
 [ HTTP request ]                                   ← L7 dati
 [ TLS | HTTP ]                                     ← L6 cifratura
 [ TCP hdr | TLS|HTTP ]            porte 51200→443  ← L4 segment
 [ IP hdr | TCP | ... ]           IP src→dst, TTL   ← L3 packet
 [ Eth hdr | IP | ... | FCS ]     MAC src→dst       ← L2 frame
 [ 0101110010... ]                                  ← L1 bit
```

## 4. Porte well-known

| Porta | Protocollo | Servizio | Trasporto |
|-------|-----------|----------|-----------|
| **20/21** | FTP | trasferimento file (dati / controllo) | TCP |
| **22** | SSH | shell remota sicura, SFTP/SCP | TCP |
| **25** | SMTP | invio email | TCP |
| **53** | DNS | risoluzione nomi | **UDP** (TCP per risposte grandi) |
| **80** | HTTP | web in chiaro | TCP |
| **443** | HTTPS | web cifrato (TLS); QUIC/HTTP3 | TCP **e UDP** |
| **3306** | MySQL | database | TCP |

(Altre comuni: 23 Telnet, 67/68 DHCP/UDP, 110/143 POP3/IMAP, 123 NTP/UDP, 161 SNMP/UDP, 389 LDAP, 3389 RDP, 5432 PostgreSQL.)

## 5. TCP vs UDP — la scelta del trasporto
| | [[TCP]] | [[UDP]] |
|---|-----|-----|
| Connessione / affidabilità / ordine | sì | no |
| Controllo flusso e congestione | sì | no |
| Overhead header | 20+ B | **8 B** |
| Latenza di setup | ≥1 RTT (handshake) | 0 |
| Quando | web, ssh, mail, transfer | DNS, VoIP, gaming, streaming, QUIC |

## 6. Mappa degli attacchi per layer
Vista d'insieme che raccorda lo stack con [[Attacchi di Rete]] (sicurezza). I difensori ragionano **per layer**, esattamente come gli attaccanti.

| Layer | Attacchi tipici | Difese |
|-------|-----------------|--------|
| **L7 Application** | SQL injection, XSS, CSRF, SSRF, HTTP request smuggling | WAF, input validation, CSP → [[Firewall e NAT]] |
| **L6 Presentation/TLS** | downgrade, cert spoofing, padding oracle, Heartbleed | TLS 1.3, HSTS, pinning → [[TLS/SSL]] |
| **L4 Transport** | **SYN flood**, RST injection, port scanning | SYN cookies, rate-limit, firewall stateful |
| **L3 Network** | **IP spoofing**, DDoS (amplification/reflection), ICMP abuse | ingress/egress filtering (BCP38), anti-DDoS |
| **L2 Data Link** | **ARP spoofing**, MAC flooding, VLAN hopping, rogue DHCP | port security, DAI, 802.1X |
| **L1 Physical** | wiretapping, jamming, accesso fisico alla porta | sicurezza fisica, fibra, cifratura end-to-end |
| **DNS (L7)** | cache poisoning, hijacking, tunneling, amplification | DNSSEC, DoH/DoT → [[DNS]] |

> Insight: la **cifratura end-to-end** (TLS) protegge il payload anche se i layer inferiori sono compromessi (es. sniffing L1/L2 vede solo cifrato). Ma non protegge i **metadati** (IP, porte, dimensioni) né dagli attacchi L7 *dentro* la sessione.

## Collegamenti
- Concetti reti: [[Modello OSI]], [[Modello TCP/IP]], [[Ethernet e MAC]], [[IP Routing]], [[TCP]], [[UDP]], [[DNS]], [[HTTP/HTTPS]], [[Firewall e NAT]], [[Socket Programming]], [[Anatomia di un Pacchetto (Wireshark)]]
- Sintesi gemella (OS): [[I tre pezzi dell'OS]]
- Cross-topic (crittografia): [[TLS/SSL]]
- Cross-topic (sicurezza): [[Attacchi di Rete]], [[Privilege Escalation]]
- Cross-topic (linux): [[Tool di Rete]]
- Cross-topic (algoritmi): [[Dijkstra]] (OSPF)

## Fonti
- [Systems Approach, capp. Foundation, Internetworking, End-to-End, Applications]
- [Beej's Guide to Network Programming (incapsulamento, modello a layer, porte)]
