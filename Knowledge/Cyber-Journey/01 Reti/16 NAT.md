---
tipo: concetto
tag: [reti]
fase: 1
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["NAT"]
---

# NAT

## In breve
Il **NAT** (Network Address Translation) traduce gli [[Indirizzamento IP|IP]] privati di una LAN nell'IP pubblico del router quando i pacchetti escono su Internet, e fa l'inverso al ritorno. Nasce per risolvere la **scarsità di IPv4**: milioni di host privati condividono un esiguo numero di IP pubblici. Effetto collaterale: gli host interni non sono raggiungibili **direttamente** dall'esterno. Utile, ma **NAT non è un firewall** — è una traduzione di indirizzi, non un meccanismo di policy di sicurezza.

---

## Meccanismo a basso livello — conntrack

Il NAT moderno si basa sul **connection tracking** (conntrack nel kernel Linux, state table nei firewall). Il router/firewall mantiene una tabella delle sessioni attive:

```
Proto   IP interno        IP pubblico           Destinazione      Stato
TCP     192.168.1.10:51234  85.100.200.5:51234   8.8.8.8:53      ESTABLISHED
TCP     192.168.1.20:49800  85.100.200.5:49800   93.184.216.34:80 TIME_WAIT
UDP     192.168.1.10:5353   85.100.200.5:5353    1.1.1.1:53      —
```

**Flusso di un pacchetto in uscita (SNAT)**:
1. PC `192.168.1.10:51234` invia SYN a `8.8.8.8:53`.
2. Router: sostituisce `192.168.1.10` con `85.100.200.5` nell'header IP sorgente; aggiorna checksum IP e TCP; aggiunge la entry in conntrack.
3. La risposta `8.8.8.8:53 → 85.100.200.5:51234` arriva al router.
4. Router consulta conntrack: trova l'entry → sostituisce `85.100.200.5:51234` con `192.168.1.10:51234` (DNAT del ritorno) → recapita al PC.

Senza l'entry in conntrack, la risposta verrebbe droppata (da qui la protezione implicita verso traffico non sollecitato in ingresso).

---

## Tipi di NAT

| Tipo | Mapping | Caso d'uso tipico |
|---|---|---|
| **Static NAT (SNAT 1:1)** | Un IP privato fisso ↔ un IP pubblico fisso | Server interno esposto su Internet con IP pubblico dedicato |
| **Dynamic NAT** | IP privato ↔ IP pubblico scelto da un pool, a rotazione | Pool di IP pubblici, non comune oggi |
| **PAT / NAT overload** | Molti IP privati ↔ un IP pubblico, distinti per **porta** | Caso domestico e aziendale standard |
| **DNAT (Destination NAT)** | Riscrittura dell'IP destinazione | Port forwarding: `pubblicoIP:443 → serverInterno:443` |
| **CGNAT** | PAT a livello ISP (RFC 6598: 100.64.0.0/10) | ISP con IPv4 scarsi: molti clienti su pochi IP pubblici |

### PAT — il caso reale in dettaglio

Il router tiene la **tabella di traduzione PAT**: lega `(IP privato : porta sorgente)` a `(IP pubblico : porta pubblica)` per ciascuna connessione/destinazione.

```
PC  192.168.1.10:51234  →  NAT  →  85.100.200.5:51234  →  8.8.8.8:53
PC  192.168.1.20:51234  →  NAT  →  85.100.200.5:52100  →  8.8.8.8:53
                                     ↑ porta riscritta per evitare collisione
```

Se due host interni usano la stessa porta sorgente verso la stessa destinazione, il NAT assegna una porta sorgente diversa sul lato pubblico per disambiguare. Lo spazio di porte disponibile (1–65535) limita le sessioni simultanee: con un solo IP pubblico, ~65k sessioni concorrenti (praticamente ~4000–6000 per conntrack overhead).

---

## SNAT vs DNAT

- **SNAT** (Source NAT): modifica l'IP **sorgente**. Usato per il traffico in uscita dalla LAN verso Internet.
- **DNAT** (Destination NAT): modifica l'IP (e/o porta) **destinazione**. Usato per il traffico in ingresso (port forwarding, load balancing, redirect).

In iptables Linux:
```bash
# SNAT: tutto il traffico uscente da eth0 → IP pubblico
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# DNAT: port forwarding 443 → server interno
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j DNAT --to-destination 192.168.1.20:443

# Vedere la tabella NAT
iptables -t nat -L -n -v

# Vedere il conntrack (sessioni attive)
conntrack -L
```

---

## Esporre servizi interni

### Port Forwarding
Apre un "buco" controllato nel NAT per un servizio specifico:
```
Router: pubblico:8443 → 192.168.1.20:443
```
Chiunque raggiunga `IP_pubblico:8443` viene inoltrato al server interno. Solo il servizio esposto è raggiungibile, non l'intera macchina.

### DMZ Host
Il router inoltra **tutte** le porte non mappate a un host DMZ. Comodo per gaming/VoIP, ma espone la macchina interamente — equivale a toglierla dal NAT. Da evitare su macchine produttive; usare invece una DMZ reale (rete separata con firewall).

### NAT Hairpinning (NAT Loopback)
Un host interno raggiunge un altro host interno tramite l'**IP pubblico** del router (es. per accedere al proprio server con il nome di dominio pubblico). Non tutti i router consumer lo supportano; spesso si risolve con split-horizon DNS o host file.

---

## NAT e traversal — il problema P2P/VoIP

Il NAT rompe il modello **end-to-end** di Internet: un host esterno non può iniziare una connessione verso un host NAT-ato. Questo crea problemi per VoIP, P2P, videoconferenze, giochi online.

### Classificazione comportamentale NAT (RFC 3489/STUN)
| Tipo | Comportamento | Impatto P2P |
|---|---|---|
| **Full-cone** | Qualsiasi IP esterno può inviare a `IP_pub:porta` mappata | Più permissivo, P2P facile |
| **Address-restricted** | Solo l'IP destinazione originale può rispondere | P2P possibile con hole punching |
| **Port-restricted** | Solo `IP:porta` destinazione originale può rispondere | Hole punching più difficile |
| **Symmetric** | Ogni destinazione diversa → mapping IP:porta pubblico diverso | P2P spesso impossibile senza TURN |

### Tecniche di traversal
- **STUN** (Session Traversal Utilities for NAT): il client scopre il proprio IP pubblico e tipo di NAT chiedendo a un server STUN.
- **TURN** (Traversal Using Relays around NAT): relay server che fa da intermediario quando il direct hole punching fallisce (symmetric NAT).
- **ICE** (Interactive Connectivity Establishment): combina STUN e TURN per scegliere il percorso migliore (WebRTC lo usa).
- **UDP Hole Punching**: entrambi i peer inviano contemporaneamente pacchetti UDP l'uno verso l'altro → i rispettivi NAT aprono una entry in conntrack → le successive comunicazioni passano direttamente.

---

## NAT e sicurezza — NAT non è un firewall

### Cosa fa il NAT (solo):
- Traduce IP/porte.
- Blocca traffico **non sollecitato** in ingresso (perché non c'è entry in conntrack) — effetto collaterale, non intenzione.

### Cosa NON fa:
- Non ispeziona il payload (Layer 7).
- Non blocca traffico **in uscita** malevolo (malware, reverse shell, C2 via HTTPS).
- Non distingue traffico legittimo da traffico malevolo avviato dall'interno.
- Non previene exfiltrazione.
- Non applica policy per utente/applicazione.

### Reverse shell attraverso NAT
Una **reverse shell** funziona perfettamente dietro NAT perché la connessione è **avviata dall'interno**:
```
Vittima (192.168.1.10) → avvia connessione → Attaccante (85.x.x.x:4444)
```
Il NAT vede una connessione TCP in uscita normale e la mappa in conntrack. La shell viaggia sul tunnel. Per bloccarla serve un **firewall con policy in uscita** (egress filtering), non il NAT.

### NAT e IPsec/AH
IPsec in modalità **AH** (Authentication Header) firma l'intero pacchetto IP, inclusi gli header. Il NAT modifica gli header IP → la firma AH diventa invalida → il tunnel si rompe. Soluzione: **NAT-T** (NAT Traversal per IPsec, RFC 3947): incapsula ESP in UDP porta 4500, bypassando il problema. La maggior parte delle implementazioni VPN moderne usa NAT-T automaticamente.

### CGNAT e attribuzione
Il CGNAT (Carrier-Grade NAT, RFC 6598) usato dagli ISP crea un ulteriore livello: molti clienti condividono lo stesso IP pubblico. Le autorità che cercano di attribuire un'azione a un IP pubblico ricevono dall'ISP "quel IP apparteneva a X clienti in quell'ora" → occorrono log CGNAT con `(IP:porta_pubblica → IP:porta_privata_cliente)` per l'attribuzione.

---

## IPv6 e la fine del NAT

Con IPv6, ogni host ottiene un indirizzo **globalmente univoco** (lo spazio `2^128` è abbondante). NAT non è più necessario per conservare indirizzi. La protezione perimetrale torna a essere il **firewall** con policy esplicite, non la traduzione di indirizzi. Implicazioni:
- Host interni raggiungibili direttamente dall'esterno se il firewall lo permette → la "protezione implicita" del NAT scompare.
- Servizi che richiedevano hole punching (P2P, VoIP) funzionano nativamente end-to-end.
- In reti dual-stack IPv4+IPv6, un host NAT-ato in IPv4 può essere raggiungibile direttamente via IPv6 → superfice d'attacco ampliata se le policy firewall IPv6 sono trascurate.

---

## Comandi pratici

```bash
# Linux — vedere la tabella conntrack (sessioni NAT attive)
sudo conntrack -L
sudo conntrack -L | grep ESTABLISHED | wc -l   # sessioni attive

# iptables — regole NAT
sudo iptables -t nat -L -n -v --line-numbers

# MASQUERADE (SNAT dinamico per IP pubblico variabile, es. DHCP)
sudo iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j MASQUERADE

# SNAT statico (IP pubblico fisso)
sudo iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j SNAT --to-source 85.100.200.5

# Port forwarding TCP 80 verso host interno
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.20:80
sudo iptables -A FORWARD -i eth0 -p tcp -d 192.168.1.20 --dport 80 -j ACCEPT

# Vedere IP pubblico (come lo vede Internet)
curl ifconfig.me
curl -s https://api.ipify.org

# Verificare il tipo di NAT (STUN)
# stunclient public.stun.sipnet.net 3478
```

---

## Casi limite e troubleshooting

- **Connessioni P2P/VoIP rotte**: NAT symmetric. Il hole punching fallisce → serve TURN relay. In VoIP: usare `STUN server` nel client SIP; se non basta, **TURN** o sessione SIP via proxy esterno.
- **Port forwarding non funziona**: verificare 1) regola iptables/firewall sul router, 2) firewall locale sull'host destinazione, 3) il servizio è davvero in ascolto sulla porta e sull'interfaccia giusta (`ss -tlnp`), 4) hairpinning se si testa dall'interno.
- **Esaurimento delle porte NAT (port exhaustion)**: con CGNAT o PAT su molte connessioni simultanee (server applicativo dietro NAT), le ~65k porte sull'IP pubblico si esauriscono. Sintomo: "connection refused" o "resource temporarily unavailable". Fix: più IP pubblici, riduzione keep-alive, connection pooling.
- **FTP attivo attraverso NAT**: FTP attivo usa una connessione dati **avviata dal server** verso il client — il NAT del client non ha un'entry per questo. Fix: FTP passivo (PASV), ALG (Application Layer Gateway) nel router che "aiuta" FTP, o modulo `nf_conntrack_ftp` in Linux.
- **Log NAT mancanti con CGNAT**: se un ISP con CGNAT non mantiene i log `(IP_pub:porta → IP_privato_cliente:porta)`, l'attribuzione di un'azione a un cliente specifico diventa impossibile — rilevante in contesti legali.

---

## Domande da esame/colloquio

1. **Qual è la differenza tra SNAT e DNAT?** SNAT (Source NAT) riscrive l'IP sorgente: usato per il traffico in uscita dalla LAN (il router sostituisce l'IP privato con il pubblico). DNAT (Destination NAT) riscrive l'IP destinazione: usato per il traffico in ingresso (port forwarding: l'IP pubblico:porta viene rediretto all'IP interno:porta).

2. **Perché NAT non è un firewall?** Il NAT blocca solo il traffico **in ingresso non sollecitato** (nessuna entry in conntrack). Non esamina il payload, non filtra per protocollo/applicazione, e non blocca nessun traffico **avviato dall'interno**, incluse reverse shell e connessioni C2. Un firewall con policy di egress filtering è necessario per il controllo in uscita.

3. **Come funziona una reverse shell attraverso un NAT?** La reverse shell avvia la connessione dall'interno della rete NAT verso l'IP dell'attaccante su Internet. Il NAT la tratta come traffico in uscita legittimo, crea un'entry in conntrack, e la risposta del server C2 dell'attaccante viene recapitata al client tramite quella entry. Il NAT non la distingue da una normale sessione HTTP.

4. **Cos'è il CGNAT e perché complica le indagini forensi?** Il Carrier-Grade NAT è un ulteriore livello di NAT gestito dall'ISP: molti clienti condividono lo stesso IP pubblico. Un indirizzo IP visto nei log di un sito non identifica univocamente un cliente: occorrono i log CGNAT dell'ISP con le coppie `(IP_pub:porta_pub ↔ IP_cliente:porta_cliente ↔ timestamp)`. Se l'ISP non li conserva, l'attribuzione diventa impossibile.

5. **Perché IPsec AH è incompatibile con NAT e come si risolve?** AH firma l'intero pacchetto IP inclusi gli header. Quando il NAT modifica l'IP sorgente, la firma AH diventa invalida e il pacchetto viene scartato. Soluzione: **NAT-T** (RFC 3947/4306) incapsula il traffico IPsec ESP in UDP/4500, rendendo l'header IP modificabile dal NAT senza rompere la crittografia/integrità IPsec.

6. **Cosa cambia con IPv6 riguardo al NAT?** IPv6 elimina la necessità di NAT (spazio di indirizzi abbondante). Ogni host ha un indirizzo globale unico → è direttamente raggiungibile da Internet se il firewall lo permette. La "protezione implicita" del NAT sparisce: in dual-stack, se le policy firewall IPv6 sono trascurate, host "protetti" dal NAT IPv4 possono essere raggiungibili via IPv6.

---

## Collegamenti
- [[Indirizzamento IP]]
- [[Subnetting]]
- [[DHCP]]
- [[VPN]]
- [[Reverse Shell e Bind Shell]]
- [[Modello TCP-IP]]
- [[TCP]]
- [[Porte e Protocolli Comuni]]
- [[Wireshark]]
- [[Man-in-the-Middle (MITM)]]

## Fonti
- Cloudflare — What is NAT: https://www.cloudflare.com/learning/network-layer/what-is-nat/
- RFC 3022 — Traditional IP NAT: https://datatracker.ietf.org/doc/html/rfc3022
- RFC 4787 — NAT Behavioral Requirements (UDP): https://www.rfc-editor.org/rfc/rfc4787
- Peterson & Davie — *Computer Networks: A Systems Approach* (cap. "Internetworking": NAT ed esaurimento IPv4): https://book.systemsapproach.org/
