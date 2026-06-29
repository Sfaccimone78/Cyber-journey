---
tipo: concetto
tag: [reti]
fase: 1
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Rete Informatica e i suoi Componenti", "Rete Informatica"]
---

# Rete Informatica e i suoi Componenti

## In breve
Una rete è un insieme di **dispositivi interconnessi** che scambiano dati seguendo **protocolli** comuni su un **mezzo** condiviso. È il punto di partenza di tutta la cybersecurity: ogni attacco e ogni difesa passano dalla rete. Capire i mattoni (host, mezzi, protocolli) e le proprietà (banda, latenza, domini di collisione/broadcast, topologia) è il prerequisito per leggere una rete in fase di [[Ricognizione (Recon)|recon]] e per progettare una difesa efficace.

---

## I tre elementi fondamentali di ogni rete
- **Dispositivi (nodi/host):** qualsiasi hardware connesso (PC, server, smartphone, stampanti, IoT, telecamere IP). Vedi [[Hardware di Rete]].
- **Mezzo di connessione:** il canale su cui viaggiano i dati — rame (Ethernet UTP), fibra ottica, wireless (Wi-Fi 802.11, 4G/5G, Bluetooth).
- **Protocolli:** le regole che fanno "parlare la stessa lingua" ai dispositivi ([[Modello TCP-IP|TCP/IP]], [[HTTP e HTTPS|HTTP]], [[DNS]], [[ARP]]…). Senza protocollo condiviso, i bit trasmessi sono rumore.

---

## Commutazione: pacchetto vs circuito

Due paradigmi fondamentali per trasportare dati:

| Paradigma | Come funziona | Pro | Contro | Esempio |
|---|---|---|---|---|
| **Commutazione di circuito** | canale dedicato end-to-end per tutta la durata | latenza costante, nessuna contesa | spreca risorse se la linea è silenziosa | PSTN (rete telefonica classica) |
| **Commutazione di pacchetto** | i dati vengono spezzati in pacchetti instradati indipendentemente | efficiente, resiliente (guasto → re-routing) | la ricomposizione richiede buffer e ordine | Internet, LAN moderne |

**Perché conta in sicurezza:** la commutazione di pacchetto è alla base dell'instradamento IP. Un attaccante sfrutta proprio questa indipendenza dei pacchetti per spoofing (falsificare IP sorgente), frammentazione (eludere IDS), e attacchi di reordering/injection. [[TCP]] risolve il problema riordinando i segmenti; [[UDP]] no (usato quando la latenza è prioritaria: VoIP, gaming, DNS).

---

## Proprietà operative della rete

| Proprietà | Definizione | Perché conta in sicurezza |
|---|---|---|
| **Banda (bandwidth)** | capacità teorica del link (Mbps/Gbps) | un [[DoS e DDoS]] mira a saturarla con traffico volumetrico |
| **Throughput** | dati realmente trasferiti in condizioni reali | misura l'impatto concreto di congestione o attacco DDoS |
| **Latenza (RTT)** | ritardo andata-ritorno (Round-Trip Time) | tecniche di timing, rilevazione di proxy/VPN/tunnel anomali |
| **Jitter** | variazione della latenza nel tempo | degrada VoIP, segnala congestione o traffico anomalo |
| **Duplex** | half (un senso alla volta) / full (bidirezionale simultaneo) | un mismatch half/full causa errori di collisione che mascherano problemi; va verificato in troubleshooting |
| **MTU (Maximum Transmission Unit)** | dimensione massima del frame/pacchetto (Ethernet: 1500 byte) | la frammentazione IP avviene quando il pacchetto supera l'MTU → usata per eludere IDS (vedi [[Nmap]] `-f`) |

---

## Topologie fisiche e logiche

La **topologia fisica** descrive come sono collegati i cavi; la **topologia logica** come scorrono i dati.

| Topologia | Struttura | Vantaggi | Svantaggi | Sicurezza |
|---|---|---|---|---|
| **Stella** | ogni host ↔ switch centrale | facile gestione, guasto isolato | switch = single point of failure | standard moderno; lo switch crea domini di collisione per porta |
| **Maglia (mesh)** | ogni nodo connesso a più nodi | alta ridondanza, nessun SPOF | costoso, complesso | usata in dorsali e SD-WAN; difficile da intercettare passivamente |
| **Bus** | cavo condiviso da tutti | economico | collisioni, guasto al cavo abbatte tutto | storica (10Base2); banale sniffing — tutti vedono tutto |
| **Anello** | token che gira tra i nodi | ordine deterministico | guasto nodo rompe l'anello | obsoleta (Token Ring); visibilità totale del traffico |
| **Albero** | stella di stelle gerarchica | scalabile | dipende dal nodo radice | comune nelle LAN campus; segmentazione per piano/reparto |

> **Nota pratica:** quasi tutte le LAN moderne usano la topologia **stella** (o albero di stelle) con switch managed. La topologia a bus è oggi un relitto storico, ma spiegare perché è insicura (mezzo condiviso → ogni nodo vede tutto) aiuta a capire perché gli hub erano pericolosi.

---

## Domini di collisione e domini di broadcast

Questi due concetti sono centrali per capire la segmentazione e il blast radius di un attacco.

### Dominio di collisione
Insieme di dispositivi che competono per lo stesso mezzo fisico. Se due trasmettono insieme → **collisione**.
- Un **hub** crea un unico dominio di collisione per tutti i dispositivi (obsoleto, pericoloso).
- Uno **switch** crea un dominio di collisione **per porta** (con link full-duplex le collisioni non esistono praticamente).
- Più il dominio è grande, più degrada le performance e più il traffico è osservabile (sniffing).

### Dominio di broadcast
Insieme di dispositivi che ricevono i frame broadcast (destinazione `FF:FF:FF:FF:FF:FF` a L2, o `255.255.255.255` a L3). I broadcast non attraversano i **router**, ma attraversano gli switch (a meno di VLAN).

- Un dominio di broadcast troppo grande = broadcast storm in caso di loop (vedi STP), ARP flooding, e maggiore superficie per attacchi come [[ARP]] poisoning.
- **Segmentare** con router o VLAN **spezza** il dominio di broadcast → riduce il blast radius laterale di un'intrusione (vedi [[Lateral Movement]]).
- Un'intera /24 con 254 host in un unico broadcast domain è comune nelle LAN casalinghe, ma sconsigliato in ambienti enterprise.

---

## Tipi di rete per estensione

| Tipo | Estensione tipica | Esempio reale | Note di sicurezza |
|---|---|---|---|
| **PAN** | personale (< 10 m) | Bluetooth, NFC, USB tethering | Bluetooth sniffing, bluejacking; NFC relay attack |
| **LAN** | edificio/campus (< 1 km) | rete di casa/ufficio, laboratorio | segmentazione VLAN obbligatoria in ambienti sensibili |
| **VLAN** | logica (stessa infrastruttura fisica) | reparto HR separato da reparto IT | VLAN hopping se il trunk non è hardened |
| **MAN** | metropolitana (città) | rete di un ISP, WiMAX comunale | affidata a terzi → meno controllo diretto |
| **WAN** | geografica (nazioni) | Internet, collegamento tra sedi aziendali | traffico su infrastruttura pubblica → cifrare con [[VPN]] o MPLS |
| **Internet** | globale | — | superficie illimitata; qualsiasi porta esposta è raggiungibile da ovunque |

---

## Modelli di relazione tra i nodi

### Client-Server
Ruoli separati: il **client** inizia la connessione, il **server** è in ascolto. Centralizzato, scalabile, più facile da proteggere (superficie concentrata). Vedi [[Modello Client-Server]].

### Peer-to-Peer (P2P)
Ogni nodo è sia client sia server. Decentralizzato (BitTorrent, sistemi blockchain). Difficile da monitorare: gli strumenti di detection devono analizzare il traffico peer anziché un singolo server.

---

## Mezzi trasmissivi a confronto

| Mezzo | Velocità tipica | Distanza | Interferenze | Rischio di intercettazione |
|---|---|---|---|---|
| **Rame (UTP Cat5e/6)** | 1 Gbps (Cat5e), 10 Gbps (Cat6A) | ≤ 100 m per segmento | EMI, crosstalk | fisico (tapping, punch-down) |
| **Fibra ottica** | 10 Gbps–100 Tbps+ | km o decine di km | immune a EMI | molto difficile passivamente; richiede accesso fisico |
| **Wi-Fi (802.11ax/Wi-Fi 6)** | fino a ~9.6 Gbps teorici | ≤ 100 m (interni) | interferenze radio, multipath | mezzo condiviso e broadcast → cifratura WPA2/3 obbligatoria |
| **Cellulare (4G/5G)** | 100 Mbps–multi-Gbps | km (celle) | congestione cella | IMSI catcher (Stingray), SS7 vulnerabilità in 4G/3G |

---

## Esempio pratico: aprire `google.com` da casa
1. Il PC ottiene [[Indirizzamento IP|IP]], gateway e DNS via [[DHCP]];
2. il resolver [[DNS]] risolve `google.com` → IP (`142.250.x.x`);
3. [[ARP]] trova il [[MAC Address]] del gateway sulla LAN; i pacchetti escono via [[NAT]] sul router;
4. switch e router instradano (L2 per MAC, L3 per IP) seguendo il [[Modello TCP-IP]];
5. browser e server stabiliscono il [[Three-Way Handshake TCP]] e parlano in [[HTTP e HTTPS|HTTPS]] (TLS handshake su TCP).

Ogni fase è un potenziale punto di attacco: DNS spoofing al passo 2, ARP poisoning al passo 3, MitM TLS al passo 5.

---

## Attacco e difesa

### Vettori di attacco a livello rete

| Attacco | Livello OSI | Meccanismo | Pagina di riferimento |
|---|---|---|---|
| **Sniffing passivo** | L1/L2 | cattura frame su mezzo condiviso (hub, Wi-Fi aperto) | [[Wireshark]] |
| **ARP poisoning** | L2 | associa MAC malevolo a IP legittimo, intercetta traffico | [[ARP]] |
| **MAC flooding** | L2 | satura tabella CAM → lo switch flooda tutto | [[Hardware di Rete]] |
| **DNS spoofing** | L7 | risposta DNS falsa → redirect verso server attaccante | [[DNS]] |
| **DoS volumetrico** | L3/L4 | satura banda o CPU del target con traffico massiccio | [[DoS e DDoS]] |
| **Man-in-the-Middle** | L2–L7 | si interpone nel flusso client↔server | [[Man-in-the-Middle (MITM)]] |
| **Lateral movement** | L3/L4 | si muove nella rete interna dopo l'accesso iniziale | [[Lateral Movement]] |

### Contromisure strutturali

- **Segmentazione (VLAN + firewall):** ogni dominio di broadcast separato limita il blast radius. Un attaccante compromette un segmento, non tutta la rete.
- **Port security sullo switch:** limita MAC per porta, impedisce MAC flooding.
- **DHCP snooping + DAI (Dynamic ARP Inspection):** proteggono da ARP spoofing e rogue DHCP.
- **Cifratura del mezzo Wi-Fi:** WPA3 (o WPA2-Enterprise con 802.1X) rendono lo sniffing impraticabile.
- **IDS/IPS di rete (NIDS):** analizzano il traffico in transito per firme anomale.
- **Zero Trust:** non fidarsi mai del segmento di rete come garanzia di identità; verificare sempre autenticazione e autorizzazione.

---

## Casi limite e troubleshooting

- **Loop di switch senza STP:** i frame broadcast circolano all'infinito → **broadcast storm** che satura la rete in secondi. Soluzione: abilitare **STP/RSTP** (Spanning Tree Protocol) su tutti gli switch managed.
- **Duplex mismatch:** un lato full-duplex, l'altro half-duplex → collisioni elevate, througput scarso, errori di CRC. Si vede nei contatori d'interfaccia del router/switch.
- **MTU mismatch (PMTUD black hole):** i router filtrano gli ICMP "fragmentation needed" → la connessione TCP si avvia ma rimane bloccata su pacchetti grandi. Fix: `ip tcp adjust-mss` sui router, o abilita PMTUD sul firewall.
- **ARP cache stale:** un'entry ARP obsoleta punta al vecchio IP → traffico misdirected. Fix: `arp -d` per svuotare la cache, ridurre il TTL ARP in ambienti dinamici.
- **VLAN hopping:** se una porta switch è configurata come trunk di default, un attaccante può iniettare tag 802.1Q → accede a VLAN diverse. Fix: disabilita i trunk automatici (DTP off), assegna esplicitamente le VLAN.

---

## Domande da esame/colloquio

1. **Differenza tra dominio di collisione e dominio di broadcast, e quale dispositivo spezza ciascuno?**
   Il dominio di collisione è il gruppo di dispositivi che competono per il mezzo fisico; lo **switch** lo spezza (un dominio per porta). Il dominio di broadcast è il gruppo che riceve i frame broadcast L2; solo il **router** (o una VLAN) lo spezza. Un hub non spezza nessuno dei due.

2. **Perché la commutazione di pacchetto è preferita per Internet rispetto a quella di circuito?**
   Perché è efficiente (molteplici flussi condividono lo stesso link), resiliente (un percorso guasto → i pacchetti seguono un altro percorso) e adatta a traffico a burst. La commutazione di circuito garantisce banda costante ma la spreca quando la linea è silenziosa.

3. **Cosa succede alla sicurezza se si usa un hub al posto di uno switch?**
   L'hub ripete ogni frame su tutte le porte → qualsiasi dispositivo connesso può catturare passivamente tutto il traffico della LAN con [[Wireshark]] senza alcuna configurazione speciale. Lo switch invia i frame unicast solo sulla porta corretta, rendendo lo sniffing passivo non immediato (occorre MAC flooding o un attacco ARP per intercettare).

4. **Cos'è il VLAN hopping e come si previene?**
   Un attaccante invia frame con doppio tag 802.1Q (o negozia un trunk DTP) per accedere a VLAN diverse dalla propria. Si previene disabilitando DTP su tutte le porte access (`switchport nonegotiate`), assegnando esplicitamente le porte alle VLAN, e usando una VLAN nativa non predefinita.

5. **Perché segmentare la rete riduce l'impatto di un'intrusione?**
   La segmentazione limita il dominio di broadcast e introduce confini che richiedono autorizzazione esplicita (firewall/ACL) per essere attraversati. Un attaccante che compromette un host in un segmento non può muoversi lateralmente verso altri segmenti senza attraversare un firewall, riducendo drasticamente il blast radius (vedi [[Lateral Movement]]).

6. **Qual è la differenza tra banda e throughput, e perché un DoS può sfruttarla?**
   La **banda** è la capacità teorica del link; il **throughput** è ciò che viene realmente consegnato. Un DoS volumetrico satura la banda con traffico inutile, riducendo il throughput utile a zero. Un DoS applicativo (slowloris, HTTP flood) satura invece le risorse del server senza necessariamente saturare la banda.

---

## Lab
- [[TryHackMe]] — percorso *Pre Security* → *Network Fundamentals* (*What is Networking?*, *Intro to LAN*): mette in pratica componenti, topologie e indirizzamento.
- [[TryHackMe]] — *Network Services* / *Network Services 2*: enumerazione dei servizi che girano sui nodi.
- In locale: cattura con [[Wireshark]] il traffico mentre apri un sito e identifica i ruoli dei dispositivi (host, switch, gateway) nel flusso.

## Collegamenti
- [[Hardware di Rete]] · [[Modello OSI]] · [[Modello TCP-IP]]
- [[Indirizzamento IP]] · [[Subnetting]] · [[Modello Client-Server]]
- [[ARP]] · [[DHCP]] · [[DNS]] · [[NAT]] · [[Three-Way Handshake TCP]]
- [[Wireshark]] — osservare il traffico reale
- [[Man-in-the-Middle (MITM)]] · [[DoS e DDoS]] · [[Lateral Movement]]
- [[Ricognizione (Recon)]] · [[Nmap]]

## Fonti
- Cisco — What is a Network?: https://www.cisco.com/c/en/us/solutions/small-business/networking.html
- Cloudflare Learning — Network layer: https://www.cloudflare.com/learning/network-layer/what-is-the-network-layer/
- Tanenbaum, *Computer Networks* — cap. 1 (concetti, topologie, commutazione)
