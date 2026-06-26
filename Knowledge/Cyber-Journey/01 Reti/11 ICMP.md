---
tipo: entita
tag: [reti]
fase: 1
fonti: 3
aggiornato: 2026-06-22
stato: maturo
aliases: ["ICMP"]
---

# ICMP

## Cos'è
**ICMP** (Internet Control Message Protocol, RFC 792) è il protocollo di **servizio e diagnostica** del livello 3, incapsulato direttamente in [[Indirizzamento IP|IP]] (numero di protocollo IP: 1 — non usa [[TCP]] né [[UDP]], non ha numeri di porta). Non trasporta dati applicativi: **segnala errori** (host/rete/porta irraggiungibile, TTL scaduto) e **testa la connettività** (ping, traceroute). È inseparabile da IP: un host che non può inviare ICMP è uno host a metà funzionale. **ICMPv6** estende questo ruolo in IPv6 aggiungendo NDP e autoconfig (vedi sotto).

> [!info] ICMP non ha porte
> Non esiste "ICMP porta 8" — il campo **Type** e **Code** sostituiscono il concetto di porta per identificare il tipo di messaggio. Questo causa confusione nei firewall configurati male e crea opportunità di evasione.

---

## Header e struttura (meccanismo a basso livello)

```
 0               7 8              15 16              31
+-----------------+-----------------+-----------------+
|      Type       |      Code       |    Checksum     |
+-----------------+-----------------+-----------------+
|              Rest of Header (dipende da Type)       |
+-----------------------------------------------------+
|          Payload (varia: echo data, errore IP+8B)   |
+-----------------------------------------------------+
```

- **Type** (8 bit): categoria del messaggio (es. 8 = Echo Request).
- **Code** (8 bit): sottotipo (es. Type 3 Code 3 = Port Unreachable).
- **Checksum** (16 bit): copre l'intero messaggio ICMP incluso payload.
- **Rest of Header**: dipende dal tipo — per Echo è `Identifier + Sequence Number`; per errori è zero.

Per i messaggi di **errore** (Type 3, 11, 12…), il payload include l'**header IP originale + i primi 8 byte del datagramma che ha causato l'errore**. Questo permette all'host sorgente di capire *quale* connessione/pacchetto ha generato il problema.

---

## Tipi e codici principali

| Type | Code | Nome | Usato da |
|---|---|---|---|
| 0 | 0 | Echo Reply | `ping` (risposta) |
| 3 | 0 | Dest Unreachable — Net | Router (rete non raggiungibile) |
| 3 | 1 | Dest Unreachable — Host | Router (host non raggiungibile) |
| 3 | 2 | Dest Unreachable — Protocol | Host (protocollo non supportato) |
| 3 | 3 | Dest Unreachable — **Port** | Host (porta chiusa) → chiave per [[UDP]] scan |
| 3 | 4 | Fragmentation Needed (DF set) | Router → Path MTU Discovery |
| 3 | 13 | Communication Administratively Prohibited | Firewall (porta filtrata) |
| 5 | 0–3 | Redirect | Router → suggerisce rotta migliore |
| 8 | 0 | Echo Request | `ping` (richiesta) |
| 11 | 0 | Time Exceeded — TTL | Router → motore di `traceroute` |
| 11 | 1 | Time Exceeded — Fragment reassembly | Host (frammenti non riassemblati in tempo) |
| 12 | 0–2 | Parameter Problem | Host (header IP malformato) |

**ICMPv6** aggiunge:

| Type | Significato |
|---|---|
| 1 | Destination Unreachable |
| 2 | Packet Too Big (sostituisce DF/PMTUD) |
| 128/129 | Echo Request/Reply |
| 133–137 | NDP: Router Solicitation/Advertisement, Neighbor S/A, Redirect |

---

## Come funziona `ping` (passo per passo)

```bash
ping -c 4 8.8.8.8
```

1. Il kernel crea un pacchetto **ICMP Type 8 Code 0** (Echo Request) con `Identifier = PID del processo`, `Sequence = 1`, payload = N byte (default 56 byte di dati + 8 header ICMP = 64 byte totali).
2. IP incapsula il messaggio con proto=1, TTL=64 (default Linux).
3. Il router GW decrementa TTL → 63. Ogni hop decrementa.
4. Arrivato a destinazione: l'host risponde con **Type 0 Code 0** (Echo Reply), ribaltando `Identifier` e `Sequence`, copiando il payload.
5. `ping` misura il **RTT** (Round Trip Time) e confronta `Sequence` per rilevare perdite.
6. Se il TTL raggiunge 0 prima della destinazione: il router intermedio droppa il pacchetto e invia **Type 11 Code 0** (Time Exceeded) al mittente.

```
PING 8.8.8.8 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=12.3 ms
```
Il `ttl=118` nella risposta significa che il pacchetto ha consumato 64-118 = ... in realtà il TTL nella risposta è quello impostato da Google (tipicamente 64 o 128), decrementato dagli hop di ritorno.

---

## Come funziona `traceroute` (TTL manipulation)

L'idea: mandare pacchetti con TTL **crescente** (1, 2, 3…) e sfruttare i messaggi **Time Exceeded** per rivelare i router intermedi.

```
Passo 1: TTL=1 → il primo router decrementa a 0 → droppa → invia ICMP Time Exceeded rivelando il suo IP
Passo 2: TTL=2 → passa il primo router (TTL→1), il secondo lo droppa → Time Exceeded con IP del secondo
Passo 3: TTL=3 → ...
Passo N: TTL=N → raggiunge la destinazione → risponde (Echo Reply su Linux -I, ICMP Port Unreachable se UDP)
```

**Differenze OS:**
- **Linux** (`traceroute`): usa **UDP** verso porte alte (33434+) di default → la destinazione risponde con ICMP Port Unreachable (Type 3 Code 3). Con `-I`: usa Echo Request come Windows.
- **Windows** (`tracert`): usa sempre **Echo Request** (ICMP) → la destinazione risponde con Echo Reply.

```bash
traceroute 8.8.8.8          # Linux, UDP
traceroute -I 8.8.8.8       # Linux, ICMP (come Windows)
tracert 8.8.8.8             # Windows
traceroute -T -p 443 8.8.8.8  # TCP SYN su 443 (bypassa firewall ICMP/UDP)
```

**Hop con `*  *  *`**: il router non risponde a ICMP Time Exceeded (firewall o config). Non significa che l'hop non esista: i pacchetti lo attraversano normalmente ma il router non genera ICMP.

---

## Esempio pratico e Wireshark

```bash
ping -c 4 8.8.8.8            # Echo Request/Reply + RTT
ping -c 1 -s 1400 8.8.8.8   # payload grande (test MTU/frammentazione)
ping -c 1 -t 1 8.8.8.8      # TTL=1 → Time Exceeded dal primo hop (Linux: -t, Windows: /i)
traceroute 8.8.8.8           # percorso completo
nmap -sn -PE 10.0.0.0/24    # host discovery via ICMP Echo (ping sweep)
nmap -sn -PP 10.0.0.0/24    # Timestamp Request (Type 13) — alternativa se Echo è filtrato
nmap -sn -PM 10.0.0.0/24    # Netmask Request (Type 17) — altro vettore discovery
```

**Wireshark:**
```
icmp                         # solo pacchetti ICMP
icmp.type == 8               # solo Echo Request
icmp.type == 0               # solo Echo Reply
icmp.type == 3               # Dest Unreachable (vedi code per dettaglio)
icmp.type == 11              # Time Exceeded (hop traceroute)
```

---

## Rilevanza per la sicurezza

### Attacco — Host discovery e recon
[[Nmap]] usa ICMP come primo passo di [[Ricognizione (Recon)|recon]]:
- `-PE`: Echo Request (Type 8) — il più comune.
- `-PP`: Timestamp Request (Type 13) — alternativa se Type 8 è filtrato.
- `-PM`: Netmask Request (Type 17).

Se l'host risponde a uno di questi, Nmap lo marca "up" e prosegue con il port scan. **Difesa**: filtrare Echo Request in ingresso dall'esterno, ma attenzione — filtrare Type 3/11 rompe la diagnostica interna.

### Attacco — ICMP Redirect (Type 5)
Un attaccante **in LAN** invia finti ICMP Redirect (Type 5 Code 1) alla vittima suggerendo "usa me come gateway". Se la vittima li accetta, il traffico viene dirottato → [[Man-in-the-Middle (MITM)]].

```
Attaccante in LAN → vittima:  ICMP Redirect Type 5 Code 1
                               "Usa 192.168.1.99 (me) per raggiungere 10.0.0.0/8"
Vittima aggiorna routing table → tutto il traffico passa per l'attaccante
```

**Difesa**: disabilitare l'accettazione dei redirect:
```bash
sysctl -w net.ipv4.conf.all.accept_redirects=0
sysctl -w net.ipv4.conf.default.accept_redirects=0
# Rendere permanente in /etc/sysctl.conf
```

### Attacco — Smurf Attack (storico, oggi irrilevante)
Echo Request spoofato verso l'**indirizzo broadcast** di una rete → tutti gli host rispondono alla vittima. Fattore di amplificazione = numero di host nella rete. **Difesa**: i router moderni non inoltrano pacchetti diretti a broadcast (`no ip directed-broadcast` su Cisco) — il vettore è praticamente estinto.

### Attacco — Ping of Death (storico)
Pacchetto IP riassemblato > 65535 byte → buffer overflow nel kernel → crash. Patchato in tutti gli OS moderni da fine anni '90. Rimane rilevante solo in sistemi embedded obsoleti o OT/SCADA non aggiornati.

### Attacco — ICMP Tunneling / Covert Channel (attuale, pericoloso)
Dati arbitrari possono essere nascosti nel **payload dei messaggi Echo** (Type 8/0). Strumenti:
- **`icmpsh`**: reverse shell via ICMP Echo.
- **`ptunnel`** / **`ptunnel-ng`**: tunneling IP-over-ICMP, crea un tunnel TCP funzionale dentro pacchetti ping.
- **`icmptunnel`**: incapsula traffico IP in ICMP payload.

**Scenario reale**: un attaccante ha compromesso un host in una rete che permette solo ping verso l'esterno (niente TCP/UDP in uscita). Usa ptunnel per creare un tunnel verso il suo C2 server → C2 su ICMP → tutti i firewall che "lasciano passare il ping" sono bypassati.

**Detection**:
- Ping con payload anomalo (payload >64 byte, contenuto non zerato).
- Alto volume di Echo Request/Reply (> 10/s da un singolo host).
- Payload ICMP con entropia alta (dati compressi/cifrati dentro ICMP).
- MITRE ATT&CK: **T1095** (Non-Application Layer Protocol), **T1048.003** (Exfiltration over Alternative Protocol).

```bash
# Rilevare tunnel ICMP con Wireshark:
icmp && frame.len > 100          # pacchetti ICMP grandi (tunnel)
icmp.data_len > 50               # payload > 50 byte
# In Suricata/Snort:
# alert icmp any any -> any any (itype:8; dsize:>64; msg:"Possible ICMP tunnel"; sid:9001;)
```

---

## Difesa — regola d'oro: filtraggio selettivo, non totale

> [!warning] Non bloccare ICMP "a tappeto"
> Filtrare *tutto* l'ICMP danneggia la diagnostica di rete e in particolare la **Path MTU Discovery** (PMTUd): i router non possono più segnalare "Fragmentation Needed" (Type 3 Code 4) → le connessioni TCP si "appendono" su path con MTU inferiore a 1500 (VPN, PPPoE). Il fenomeno è noto come **black hole routing**.

**Best practice per i firewall:**

| Tipo ICMP | Direzione | Azione consigliata |
|---|---|---|
| Type 8 (Echo Request) | In ingresso dall'esterno | Blocca (riduce la superficie di recon) |
| Type 0 (Echo Reply) | In uscita / ritorno | Permetti (risposta al ping che hai iniziato tu) |
| Type 3 (Dest Unreachable) | Bidirezionale | **Permetti** — essenziale per PMTUd e diagnostica |
| Type 11 (Time Exceeded) | In ingresso | Permetti per traceroute interno |
| Type 5 (Redirect) | In ingresso | **Blocca** — vettore MITM |
| ICMPv6 133–137 (NDP) | Interno | **Permetti** — obbligatorio per IPv6 |
| Echo con payload > 1000 B | Qualsiasi | Rate limit / ispeziona |

```bash
# iptables — politica selettiva consigliata
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP        # blocca ping in ingresso
iptables -A INPUT -p icmp --icmp-type destination-unreachable -j ACCEPT  # PMTUd
iptables -A INPUT -p icmp --icmp-type time-exceeded -j ACCEPT     # traceroute
iptables -A INPUT -p icmp --icmp-type echo-reply -j ACCEPT        # risposte ai nostri ping
iptables -A INPUT -p icmp --icmp-type redirect -j DROP            # blocca redirect malevoli
iptables -A INPUT -p icmp -m limit --limit 10/s -j ACCEPT         # rate limit sul resto
```

---

## ICMPv6 e NDP (IPv6)

In IPv6, **ICMPv6 è obbligatorio** e svolge funzioni critiche che in IPv4 erano separate:

| Funzione | ICMPv4 equivalente | ICMPv6 Type |
|---|---|---|
| Neighbor Discovery (= ARP) | [[ARP]] (L2) | 135 Neighbor Solicitation / 136 Neighbor Advertisement |
| Router Discovery | Manuale o DHCP | 133 Router Solicitation / 134 Router Advertisement |
| Redirect | ICMP Redirect (5) | 137 Redirect |
| Ping | Echo (8/0) | 128/129 |
| Path MTU Discovery | Type 3 Code 4 | 2 Packet Too Big |

Bloccare ICMPv6 integralmente rompe IPv6 completamente (nessun NDP → nessun indirizzo). **Filtrare solo i tipi pericolosi** (es. abuso RA per rogue router su LAN).

---

## Attacco vs Difesa — tabella sinottica

| Attacco | Meccanismo | Difesa |
|---|---|---|
| Ping sweep / recon | ICMP Echo verso intera subnet | Blocca Type 8 in ingresso; ma ricorda che Nmap ha alternative (PP, PM) |
| ICMP Redirect MITM | Finti Type 5 in LAN | `accept_redirects=0` su tutti gli host |
| Smurf (storico) | Echo spoofato verso broadcast | `no ip directed-broadcast` sui router |
| Ping of Death (storico) | Pacchetto >65535B | OS patchati; irrelevante su sistemi moderni |
| ICMP Tunneling / C2 | Payload arbitrario in Echo | Rate limit, ispezione DPI, anomaly detection su payload size/entropia |
| Black hole via ICMP drop | Blocco Type 3 Code 4 → PMTUd rotta | Non bloccare Type 3; ICMP Unreachable è un controllo vitale |

---

## Domande da esame/colloquio

1. **Qual è la differenza tra Type 3 Code 3 e Type 11 Code 0?** Type 3 Code 3 è "Port Unreachable" generato dall'*host di destinazione* quando la porta UDP non è in ascolto. Type 11 Code 0 è "Time Exceeded" generato da un *router intermedio* quando il TTL raggiunge 0 — è il motore di traceroute.

2. **Perché non si dovrebbe bloccare tutto l'ICMP con un firewall?** Bloccare Type 3 Code 4 (Fragmentation Needed) rompe la Path MTU Discovery → le connessioni TCP che attraversano link con MTU inferiore a 1500 (VPN, PPPoE) si "appendono". Bloccare Type 11 rompe traceroute e la diagnostica di rete.

3. **Come funziona l'ICMP tunneling e come si rileva?** Strumenti come ptunnel incapsulano dati arbitrari (anche traffic TCP/IP completo) nel payload di pacchetti Echo. Segnali: payload anomalo (>64 byte), alta entropia del payload, volume sostenuto di Echo da un singolo host. Rilevabile con DPI o regole Suricata/Snort su `dsize > 64`.

4. **Come usa Nmap ICMP per la host discovery e come può bypassare il filtraggio?** Default: `-PE` (Echo Request). Se Echo è filtrato, usa `-PP` (Timestamp Request, Type 13) o `-PM` (Netmask Request, Type 17) — molti firewall dimenticano di filtrare questi tipi meno noti. Ultima risorsa: `-Pn` per saltare la discovery e trattare tutti gli host come up.

5. **Cos'è un ICMP Redirect attack e chi ne è vulnerabile?** Un attaccante in LAN invia ICMP Redirect (Type 5) finti per modificare la routing table della vittima, diventando il gateway di default (MITM L3). Vulnerabili: host Linux/Windows con `accept_redirects=1` (default spesso sì). Difesa: `sysctl net.ipv4.conf.all.accept_redirects=0`.

6. **ICMP trasporta dati applicativi?** No — non ha numeri di porta e non è progettato per trasportare dati utente. Tuttavia i campi Identifier, Sequence e soprattutto il payload dell'Echo **possono** contenere dati arbitrari → vettore di tunneling/exfiltration.

---

## MITRE ATT&CK
- **T1018** — Remote System Discovery (ping sweep per host discovery)
- **T1595.001** — Active Scanning: Scanning IP Blocks
- **T1095** — Non-Application Layer Protocol (ICMP tunneling C2)
- **T1048.003** — Exfiltration Over Alternative Protocol (ICMP exfil)

---

## Collegamen ti
- [[Indirizzamento IP]] — ICMP viaggia direttamente in IP (proto 1)
- [[TCP]] — ICMP segnala errori relativi a sessioni TCP
- [[UDP]] — ICMP Port Unreachable (Type 3/3) è la risposta a UDP su porta chiusa
- [[ARP]] — in IPv4 gestisce la risoluzione L2; NDP in ICMPv6 lo sostituisce in IPv6
- [[Ricognizione (Recon)]] — ping sweep come primo passo recon
- [[Nmap]] — usa ICMP per host discovery (`-PE`, `-PP`, `-PM`)
- [[Man-in-the-Middle (MITM)]] — ICMP Redirect come vettore MITM di L3
- [[DoS e DDoS]] — Smurf attack; ICMP flood
- [[Modello TCP-IP]] — ICMP è un protocollo di controllo del layer Internet
- [[Wireshark]] — filtrare e analizzare ICMP a livello pacchetto

## Fonti
- RFC 792 — Internet Control Message Protocol: https://datatracker.ietf.org/doc/html/rfc792
- RFC 4443 — ICMPv6 for IPv6: https://datatracker.ietf.org/doc/html/rfc4443
- Cloudflare — What is ICMP: https://www.cloudflare.com/learning/ddos/glossary/internet-control-message-protocol-icmp/
- MITRE ATT&CK — T1095 Non-Application Layer Protocol: https://attack.mitre.org/techniques/T1095/
