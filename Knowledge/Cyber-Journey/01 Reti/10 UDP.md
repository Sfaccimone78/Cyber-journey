---
tipo: entita
tag: [reti]
fase: 1
fonti: 5
aggiornato: 2026-06-26
stato: maturo
aliases: ["UDP"]
---

# UDP

## Cos'è
**UDP** (User Datagram Protocol, RFC 768) è il trasporto **senza connessione** del [[Modello TCP-IP]]: spedisce **datagrammi** senza handshake, senza ACK, senza ordine e senza controllo di congestione. In cambio è leggero e a bassa latenza. Tutta l'affidabilità, se serve, la mette l'applicazione (es. QUIC). Opera a **livello 4** ([[Modello OSI]]) e usa le **porte** come [[TCP]].

> **Analogia**: UDP è come una cartolina postale — la spedisci e non sai mai se arriva. TCP è una raccomandata con ricevuta di ritorno.

---

## Header: solo 8 byte (meccanismo a basso livello)

```
 0               15 16              31
+------------------+------------------+
|   Source Port    | Destination Port |
+------------------+------------------+
|      Length      |    Checksum      |
+------------------+------------------+
|         Payload (variabile)         |
+-------------------------------------+
```

| Campo | Bit | Descrizione |
|---|---|---|
| Source Port | 16 | Porta mittente (può essere 0 se irrilevante) |
| Destination Port | 16 | Porta del servizio di destinazione |
| Length | 16 | Lunghezza header + payload in byte (minimo 8) |
| Checksum | 16 | Copertura opzionale in IPv4, obbligatoria in IPv6 |

Il **checksum** copre una **pseudo-header** IP (src IP + dst IP + proto 17 + lunghezza UDP): questo lega logicamente il datagramma all'indirizzo di destinazione senza che UDP conosca direttamente IP. Se il checksum è 0x0000, la verifica è disabilitata (IPv4).

**Niente seq, niente flag, niente window**: confronto immediato con il header [[TCP]] che supera i 20 byte obbligatori + opzioni. Questo minimalismo è il motivo della velocità **e** della facilità di spoofing — senza un handshake che verifichi la sorgente, chiunque può forgiare l'IP mittente.

> [!tip] Perché conviene a QUIC: niente head-of-line blocking
> UDP non garantisce ordine, ma proprio per questo **non** soffre dell'*head-of-line blocking* di TCP (dove
> un singolo segmento perso blocca la consegna di tutti i byte successivi). Un protocollo che gestisce
> l'affidabilità **sopra** UDP, a livello applicativo (come **QUIC**/HTTP-3 con i suoi stream
> indipendenti), può ritrasmettere solo ciò che è andato perso senza fermare gli altri flussi.

### Frammentazione
Se il datagramma supera la **MTU** (tipicamente 1500 byte su Ethernet), è **IP** (livello 3) a frammentare — non UDP. Ogni frammento porta la stessa porta di destinazione solo nel primo frammento; i frammenti successivi non hanno header UDP. Questo crea problemi di filtro sui firewall stateless (che vedono solo il primo frammento) e opportunità di evasione.

---

## Conseguenze del "connectionless"

| Proprietà | Impatto positivo | Impatto negativo / rischio |
|---|---|---|
| Nessuno stato | Scalabilità enorme (es. DNS con milioni di query/s) | Nessuna verifica della sorgente → spoofing banale |
| Nessun ACK | Latenza minima (un solo RTT per query/risposta) | Perdita silente → l'app deve gestirla |
| Nessuna connessione | Adatto a broadcast/multicast | Impossibile autenticare il mittente senza crittografia |
| Nessun controllo congestione | Flusso costante anche sotto carico | Può saturare la rete (UDP flood) |
| Frammentazione IP | Payload grandi (NFS, SNMP bulk) | Attacchi di re-assemblaggio, evasione firewall |

---

## Protocolli su UDP — quando e perché

| Protocollo | Porta | Perché UDP | Nota di sicurezza |
|---|---|---|---|
| [[DNS]] | 53/UDP | Query brevi una-richiesta/una-risposta; passa a TCP/53 se risposta >512B (flag TC) | Amplification 28–54×; cache poisoning |
| [[DHCP]] | 67/68 | Broadcast prima di avere un IP; non può aprire una sessione TCP | Rogue DHCP server, starvation |
| SNMP | 161/UDP | Monitoraggio leggero, polling frequente | Community string `public` in chiaro; amplification via GetBulk |
| NTP | 123/UDP | Sincronizzazione oraria, alta frequenza, tollerante alla perdita | monlist → amplification ~556×; NTP spoofing per attacchi replay |
| VoIP (RTP) | 5004+/UDP | La latenza conta più del pacchetto perso; ritrasmettere audio sarebbe inutile | Intercettazione (no cifratura di default), toll fraud |
| QUIC / HTTP/3 | 443/UDP | Affidabilità + cifratura nello user space, 0-RTT connection, multiplexing | Blocco da firewall che droppano UDP/443 |
| TFTP | 69/UDP | Trasferimento file semplice su LAN, boot PXE | No autenticazione, directory traversal noto |
| Syslog | 514/UDP | Log leggero, fire-and-forget | Log falsificabili (no autenticazione); passare a TLS syslog |

---

## Walkthrough: cosa succede quando mandi un datagramma DNS

```
Client                           DNS Server
  |                                   |
  |--- UDP SRC:51234 DST:53 -------->  |   (1 pacchetto, no handshake)
  |         query: "www.example.com?" |
  |                                   |
  |<-- UDP SRC:53 DST:51234 ---------  |   (risposta immediata)
  |         answer: "93.184.216.34"   |
  |                                   |
  Fine. Nessuno stato rimane.
```

Confronta con TCP: sarebbero stati necessari SYN+SYN-ACK+ACK prima, e FIN+ACK+FIN+ACK dopo — 7 pacchetti extra per una query di 40 byte. Per DNS con milioni di query/s, questo è inaccettabile.

---

## Attacchi su UDP

### 1. UDP Flood
L'attaccante inonda la vittima con datagrammi UDP di grandi dimensioni verso porte casuali.
- Il server cerca il servizio su quella porta → non trovandolo risponde con [[ICMP]] Port Unreachable (type 3 code 3).
- La vittima viene saturata sia in **ricezione** (bandwidth) sia in **elaborazione** (CPU per generare ICMP).
- Tool: `hping3 --udp -p 80 --flood target`, Scapy.

### 2. Amplification / Reflection Attack (il più pericoloso)
Sfrutta due caratteristiche: (1) lo spoofing IP è banale su UDP, (2) alcuni servizi rispondono con molti più byte di quanti ne ricevano.

```
Attaccante (spoofa IP vittima)       Riflettore (es. DNS/NTP)      Vittima
  |                                        |                          |
  |--- piccola richiesta (spoofa IP v.) -->|                          |
  |                                        |--- risposta ENORME ----->|
  |                                        |--- risposta ENORME ----->|  (DDoS amplificato)
```

**Fattori di amplificazione reali:**

| Servizio / Vettore | Richiesta | Risposta | Fattore ~ |
|---|---|---|---|
| DNS ANY query | ~40 B | ~3000 B | 28–75× |
| NTP monlist (CVE-2013-5211) | 8 B | ~4400 B | 550× |
| memcached (UDP/11211) | 15 B | ~750 KB | ~50.000× |
| SSDP (UPnP) | 30 B | 1900 B | 30–70× |
| CLDAP (389/UDP) | 52 B | 1500 B | 28× |

**Difesa:**
- **BCP 38** (RFC 2827): i provider filtrano pacchetti con sorgente spoofata — elimina il vettore alla radice.
- **Disabilitare servizi riflettenti**: NTP `monlist` → `noquery`, DNS ricorsione aperta → chiudere al pubblico, memcached → non esporre UDP su Internet.
- **Rate limiting ICMP e UDP** per servizio (firewall, `iptables -m limit`).
- **Anycast**: distribuisce il traffico su molti POP → nessun singolo punto satura.

### 3. Spoofing e session hijacking
Senza handshake, chiunque può forgiare l'IP sorgente. Per servizi UDP senza crittografia (VoIP, NFS, alcuni giochi), un attaccante on-path può iniettare datagrammi nel flusso.

### 4. TFTP / SNMP abuse
TFTP (porta 69) non ha autenticazione: un client può leggere qualsiasi file accessibile al server. SNMP con community string `public` espone tutta la configurazione del dispositivo in chiaro.

---

## Scansione UDP (perché è lenta) — meccanismo

`nmap -sU` invia un datagramma UDP (vuoto o con probe specifico) alla porta target:

| Risposta ricevuta | Stato porta |
|---|---|
| Nessuna risposta | `open\|filtered` — impossibile distinguere |
| [[ICMP]] Port Unreachable (type 3, code 3) | `closed` |
| [[ICMP]] unreachable (altri codici) | `filtered` |
| Risposta UDP applicativa | `open` (certezza) |

Il problema: Linux limita l'emissione di ICMP a ~1 pacchetto/secondo → per 65535 porte UDP, Nmap deve aspettare potenzialmente ore. Soluzione pratica:

```bash
# UDP top 20 porte più comuni (veloce, ~minuti)
sudo nmap -sU --top-ports 20 10.10.10.5

# UDP mirato sui servizi "ghiotti" (DNS, SNMP, NTP, TFTP, SSDP)
sudo nmap -sU -p 53,67,68,69,123,161,162,500,514,1900 -sV 10.10.10.5

# Con probe applicativi (--version-intensity migliora il rilevamento UDP)
sudo nmap -sU -sV --version-intensity 5 --top-ports 50 10.10.10.5
```

> [!tip] Combinare TCP e UDP nella stessa run
> `nmap -sS -sU -p T:22,80,443,U:53,161 10.10.10.5` — Nmap gestisce i due protocolli in parallelo.

---

## Difesa e hardening

| Misura | Dettaglio |
|---|---|
| **Chiudi UDP inutilizzati** | `ss -unp` per vedere cosa ascolta; blocca con firewall (`iptables -A INPUT -p udp --dport X -j DROP`) |
| **Rate limiting** | `iptables -m limit --limit 10/s` sull'ICMP Port Unreachable generato da UDP chiusi |
| **BCP 38 / uRPF** | Filtro anti-spoofing sul bordo della rete; blocca reflection attack alla fonte |
| **Cifratura applicativa** | DTLS (RFC 6347) è TLS per UDP; QUIC integra TLS 1.3 — proteggono da injection e intercettazione |
| **Disabilita servizi riflettenti** | NTP monlist, DNS ANY open resolver, memcached UDP, SSDP |
| **Segmentazione** | SNMP/161 e NTP/123 solo su VLAN di gestione, non raggiungibili dall'esterno |
| **Monitoring** | Volume anomalo di UDP in uscita da un host = possibile C2 channel o partecipazione in botnet |

---

## Comandi pratici

```bash
# Invia un datagramma UDP grezzo
echo "ciao" | nc -u 192.168.1.10 5005

# Ascolta UDP
nc -u -l 5005

# Vedere porte UDP in ascolto
ss -unp
# oppure
netstat -unp         # Linux
netstat -ano -p udp  # Windows

# Wireshark: filtrare solo UDP
udp
udp.dstport == 53    # solo DNS
udp.length > 1400    # datagrammi grandi (sospetto amplification)

# Verificare se NTP monlist è attivo (vettore amplification)
ntpq -c monlist <ntp-server>
# Se risponde con lista di client → vulnerabile; disabilitare con: restrict default noquery
```

---

## UDP vs TCP — confronto rapido

| | UDP | TCP |
|---|---|---|
| Connessione | No | Sì ([[Three-Way Handshake TCP]]) |
| Affidabilità | No (best-effort) | Sì (ACK, ritrasmissioni) |
| Ordine | No | Sì (seq numbers) |
| Controllo congestione | No | Sì (slow start, AIMD) |
| Overhead header | 8 byte | 20+ byte |
| Latenza | Minima | Maggiore |
| Spoofing | Banale | Difficile (ISN randomizzato) |
| Caso d'uso | DNS, VoIP, streaming, gaming, QUIC | HTTP, SSH, FTP, email, database |

---

## Domande da esame/colloquio

1. **Perché UDP è più veloce di TCP?** Nessun handshake (risparmia RTT), nessun ACK (nessuna attesa di conferma), nessun controllo di congestione (invia alla massima velocità possibile), header 8 byte fissi.

2. **Come funziona un attacco di amplification UDP e come si difende?** L'attaccante invia richieste piccole a servizi UDP spoofando l'IP della vittima; il servizio risponde con risposte enormi alla vittima. Difesa: BCP 38 (anti-spoofing), disabilitare monlist/DNS open resolver/memcached UDP, rate limiting.

3. **Perché la scansione UDP con Nmap è molto più lenta di quella TCP?** In TCP una porta chiusa risponde RST (immediato). In UDP una porta chiusa risponde ICMP Port Unreachable, ma il kernel Linux lo emette a ~1/s; una porta aperta spesso tace → Nmap deve aspettare il timeout per ogni porta non rispondente.

4. **Cos'è QUIC e perché usa UDP?** QUIC (RFC 9000, base di HTTP/3) implementa affidabilità, multiplexing e cifratura TLS 1.3 nello user space sopra UDP. Questo permette 0-RTT connection setup, nessun head-of-line blocking, e migrazione di connessione quando cambia l'IP (4G → WiFi). Usa UDP invece di un nuovo protocollo di trasporto perché UDP è già consentito ovunque mentre un nuovo numero di protocollo IP sarebbe bloccato da middlebox.

5. **Cosa vede Wireshark di un datagramma UDP rispetto a un segmento TCP?** Solo 4 campi fissi (src port, dst port, length, checksum) — niente seq/ack, niente flag, niente window. Il payload è immediato. Nessuno stato di connessione tracciabile.

---

## Attacco e difesa — tabella sinottica

| Attacco | Tecnica | Protezione |
|---|---|---|
| UDP Flood | Saturazione banda con datagrammi massicci | Rate limiting, scrubbing center, anycast |
| Amplification/Reflection | Spoofing + servizi ad alto fattore (NTP, DNS, memcached) | BCP 38, disabilitare servizi riflettenti, chiudere resolver aperti |
| SNMP community string | Query SNMP con `public`/`private` → dump configurazione | SNMPv3 con autenticazione/cifratura, firewall su 161/UDP |
| TFTP path traversal | Lettura file arbitrari via TFTP anonimo | Disabilitare TFTP o limitare a VLAN isolata, file ACL |
| VoIP eavesdropping | Cattura RTP non cifrato | SRTP (cifratura RTP), DTLS-SRTP |
| DNS amplification | ANY query a open resolver spoofando vittima | Disabilitare ANY, rate limiting per IP sorgente, Response Rate Limiting (RRL) |

---

## Collegamenti
- [[TCP]] — il confronto affidabile/connesso
- [[Three-Way Handshake TCP]] — ciò che UDP non fa mai
- [[ICMP]] — risposte di errore allo scan UDP (Port Unreachable)
- [[DNS]] — protocollo UDP per eccellenza
- [[DHCP]] — usa broadcast UDP prima di avere un IP
- [[DoS e DDoS]] — flood e amplification
- [[Modello TCP-IP]] — UDP è il trasporto leggero di L4
- [[Modello OSI]] — livello 4 (Trasporto)
- [[Nmap]] — scansione UDP `-sU` e perché è lenta
- [[Wireshark]] — analizzare datagrammi UDP a livello pacchetto
- [[Porte e Protocolli Comuni]] — quali servizi usano UDP

## Fonti
- RFC 768 — User Datagram Protocol: https://datatracker.ietf.org/doc/html/rfc768
- RFC 9000 — QUIC: A UDP-Based Multiplexed and Secure Transport: https://datatracker.ietf.org/doc/html/rfc9000
- Cloudflare — UDP / amplification: https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/
- US-CERT TA14-017A — UDP-based amplification attacks: https://www.cisa.gov/news-events/alerts/2014/01/17/udp-based-amplification-attacks
- Peterson & Davie — *Computer Networks: A Systems Approach* (cap. "End-to-End — Simple Demultiplexer (UDP)"): https://book.systemsapproach.org/
- Beej's Guide to Network Programming — "What is a socket?" (SOCK_DGRAM): https://beej.us/guide/bgnet/
