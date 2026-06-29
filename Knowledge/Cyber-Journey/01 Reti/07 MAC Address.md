---
tipo: concetto
tag: [reti]
fase: 1
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["MAC Address", "Ethernet e MAC"]
---

# MAC Address

## In breve
Il **MAC Address** (Media Access Control Address) è l'identificatore **fisico** a **livello 2** ([[Modello OSI]]) della scheda di rete (NIC). Identifica un dispositivo **all'interno dello stesso segmento di rete locale (LAN)**; a differenza dell'[[Indirizzamento IP|IP]] (logico, instradabile, modificabile via DHCP) il MAC è associato all'hardware e in teoria fisso di fabbrica — anche se può essere modificato via software (**MAC spoofing**). Lo switch instrada i frame Layer 2 proprio in base al MAC, e il protocollo [[ARP]] lega IP↔MAC nel segmento locale.

---

## Struttura: 48 bit (6 byte) in esadecimale

```
AA:BB:CC : DD:EE:FF
└─ OUI ─┘ └─ NIC ──┘
(3 byte   )  (3 byte )
(produttore) (seriale)
```

- **OUI (Organizationally Unique Identifier)** — primi 3 byte (24 bit): assegnato dall'IEEE al produttore della NIC. Permette di identificare il **vendor** del dispositivo: `00:1A:2B` → Cisco, `00:50:56` → VMware, `AC:DE:48` → Apple. Lookup immediato su macvendors.com o con `nmap -O` — in recon e forensica identifica il tipo di dispositivo (server fisico, VM, IoT).
- **NIC (Network Interface Controller)** — ultimi 3 byte (24 bit): seriale unico assegnato dal produttore a ogni NIC. La combinazione OUI+NIC dovrebbe essere globalmente unica (16 milioni di combinazioni per OUI).

### I due bit speciali del primo byte

Il primo byte (MSB) dell'indirizzo MAC contiene due bit che modificano il comportamento del frame:

| Bit | Posizione | Valore 0 | Valore 1 | Quando si vede |
|---|---|---|---|---|
| **I/G** (Individual/Group) | bit 0 del primo byte (LSB) | **Unicast** — frame per un singolo dispositivo | **Multicast/Broadcast** — frame per un gruppo | Broadcast = tutti i bit a 1: `FF:FF:FF:FF:FF:FF` |
| **U/L** (Universal/Local) | bit 1 del primo byte | **Universalmente amministrato** — OUI assegnato IEEE | **Localmente amministrato** — MAC assegnato via software | Alzato da MAC randomizzazione (privacy) e da MAC spoofing |

**Esempio di lettura:**
- `FF:FF:FF:FF:FF:FF` → I/G=1 (gruppo/broadcast), usato da ARP Request e da DHCP Discover per raggiungere tutta la LAN.
- `01:00:5E:xx:xx:xx` → I/G=1 (multicast IPv4), usato da protocolli come OSPF, PIM, IGMP.
- `02:00:00:00:00:01` → U/L=1 (localmente amministrato), tipico dei MAC randomizzati o assegnati artificialmente (es. in container, VPN, VM).

---

## Ethernet L2: da bus condiviso a switching (CSMA/CD e STP)

Il MAC vive dentro il **frame Ethernet** (IEEE 802.3): `Dest MAC | Source MAC | EtherType | Payload (46–1500B, MTU) | FCS`.
L'**EtherType** è la demux key che indica il protocollo del payload (`0x0800`=IPv4, `0x0806`=ARP,
`0x86DD`=IPv6); l'**FCS** è un CRC per rilevare errori.

- **CSMA/CD** — alle origini Ethernet era un **bus condiviso**: *Carrier Sense Multiple Access with
  Collision Detection*. Ogni nodo ascolta prima di trasmettere e, se due trasmettono insieme, rileva la
  **collisione** e ritrasmette dopo un **backoff esponenziale**. Con gli **switch** e i link full-duplex
  le collisioni sono sparite: lo switch crea **un dominio di collisione per porta**.
- **Backward learning** — lo switch popola la tabella CAM (vedi sotto) imparando l'associazione
  *MAC sorgente ↔ porta* dai frame in transito.
- **STP (Spanning Tree Protocol, 802.1D)** — in topologie con switch ridondanti i frame broadcast
  girerebbero all'infinito (niente TTL a L2): STP disabilita logicamente i link che creerebbero **loop**,
  costruendo un albero senza cicli.

## Come lo switch usa il MAC: la tabella CAM

Lo switch costruisce e mantiene la **tabella CAM** (Content Addressable Memory) associando `MAC sorgente → porta fisica`. Il processo:

1. **Learning:** all'arrivo di ogni frame, lo switch legge il MAC sorgente e lo associa alla porta di ingresso con un timestamp.
2. **Forwarding:**
   - MAC destinazione trovato in CAM → invia il frame **solo** su quella porta (unicast selettivo → privacy, efficienza).
   - MAC destinazione non trovato / broadcast / multicast → **flooding** (copia del frame su tutte le porte eccetto quella di ingresso).
3. **Aging:** le entry senza traffico scadono (default 300 secondi) → la CAM si svuota automaticamente.

La CAM è hardware specializzato (TCAM) che permette lookup in tempo O(1) a velocità di linea. Ha capacità **limitata** (tipicamente da 4.096 a 128.000 entry per switch).

---

## Attacco: MAC Flooding

Un attaccante sfrutta il limite della CAM inviando raffica di frame con **MAC sorgente casuali**:
```bash
# Tool: macof (parte del pacchetto dsniff)
macof -i eth0 -n 100000     # 100.000 frame con MAC casuali sull'interfaccia eth0
```
Quando la CAM è piena, lo switch non può aggiungere nuove entry → per ogni frame con MAC destinazione sconosciuto **fa flooding su tutte le porte** → lo switch si comporta come un hub → qualsiasi dispositivo può catturare passivamente tutto il traffico LAN con [[Wireshark]].

### Difese al MAC Flooding

| Contromisura | Come funziona | Dove si configura |
|---|---|---|
| **Port Security** | limita il numero massimo di MAC per porta; violazione → err-disabled, restrict o protect | switch managed (es. Cisco: `switchport port-security maximum 2`) |
| **802.1X / NAC** | autentica il dispositivo prima di permettere accesso alla porta (RADIUS + EAP) | switch managed + RADIUS server |
| **Dynamic ARP Inspection (DAI)** | non blocca il flooding in sé, ma previene l'ARP poisoning che tipicamente segue | switch managed (su VLAN) |
| **DHCP Snooping** | tabella di binding MAC→IP→porta usata da DAI per validare le risposte ARP | switch managed (prerequisito per DAI) |

---

## Attacco: MAC Spoofing

Il MAC spoofing consiste nel **modificare via software il MAC address** della propria NIC, impersonando un altro dispositivo. È semplice e non richiede privilegi particolari su Linux:

```bash
# Linux — modifica temporanea del MAC
sudo ip link set eth0 down
sudo ip link set eth0 address 00:11:22:33:44:55
sudo ip link set eth0 up

# Verifica
ip link show eth0
# output: link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff

# macchanger (alternativa più pratica)
sudo macchanger -m 00:11:22:33:44:55 eth0   # MAC specifico
sudo macchanger -r eth0                      # MAC casuale (U/L=1 → localmente amministrato)
```

```powershell
# Windows — via Gestione dispositivi o:
Set-NetAdapter -Name "Ethernet" -MacAddress "00-11-22-33-44-55"
```

### Scenari d'uso del MAC spoofing

| Scenario | Legittimo? | Dettaglio |
|---|---|---|
| **Privacy / randomizzazione** | sì | smartphone (Android 10+, iOS 14+) randomizzano il MAC per ogni rete Wi-Fi per impedire il tracking basato sul MAC |
| **Test di rete** | sì (lab autorizzato) | verificare che port security funzioni, o impersonare un dispositivo temporaneamente offline |
| **Bypass filtri MAC Wi-Fi** | attacco | i filtri MAC sono sicurezza per oscurità: basta sniffare un MAC autorizzato e clonarlo |
| **Bypass NAC (Network Access Control)** | attacco | se il NAC autorizza basandosi solo sul MAC, il spoofing aggira il controllo |
| **Preludio a ARP poisoning / MitM** | attacco | clonare il MAC del gateway per intercettare il traffico |

> Il filtraggio MAC **non è un controllo di sicurezza efficace**: il MAC è trasmesso in chiaro su ogni frame — chiunque possa sniffare la rete può vedere i MAC autorizzati e clonarli in secondi.

---

## MAC vs IP: differenze chiave

| Proprietà | MAC Address | Indirizzo IP |
|---|---|---|
| Livello OSI | 2 — Data Link | 3 — Network |
| Scope | segmento locale (LAN, singolo broadcast domain) | globale (instradabile su Internet) |
| Assegnazione | produttore della NIC (hardware) | manuale o DHCP (logico) |
| Modifica | via software (spoofing) | banale (DHCP release/renew, config manuale) |
| Attraversa i router? | **no** — riscritto a ogni hop | sì — rimane invariato (a meno di NAT) |
| Unicità teorica | globale (OUI+seriale IEEE) | globale (IP pubblici) / locale (IP privati con NAT) |
| Usato da | switch (forwarding L2), ARP | router (forwarding L3), TCP/IP |

**Il MAC sorgente è riscritto a ogni hop:** quando un pacchetto attraversa un router, il router costruisce un **nuovo frame L2** con il proprio MAC come sorgente e il MAC del next-hop come destinazione. L'indirizzo IP sorgente/destinazione rimane invariato (salvo NAT). Questo significa che il MAC è utile solo per l'analisi nel segmento locale — non è tracciabile end-to-end attraverso Internet.

---

## MAC in forensica e detection

Il MAC è un identificatore prezioso in forensica di rete:

- **Log DHCP (`MAC → IP → timestamp`):** ogni volta che un dispositivo ottiene un IP via [[DHCP]], il server logga il MAC. Questo collega un'azione di rete (IP usato in un certo momento) a un dispositivo fisico.
- **Tabelle ARP/CAM su switch e router:** mostrano quale MAC era su quale porta/IP in un dato momento (`show arp`, `show mac address-table`).
- **Log degli Access Point:** ogni connessione Wi-Fi logga il MAC del client.
- **Wireshark / pcap:** ogni frame Ethernet contiene MAC sorgente e destinazione in chiaro → identificazione del dispositivo reale anche in reti senza DHCP.
- **OUI lookup in recon:** `nmap -O` o lookup su macvendors.com → identifica il vendor del dispositivo (utile per distinguere fisico vs VM, tipo di OS probabile, tipo di IoT).

```bash
# Wireshark: filtri per MAC
eth.src == aa:bb:cc:dd:ee:ff        # solo frame da questo MAC
eth.dst == ff:ff:ff:ff:ff:ff        # solo broadcast
eth.addr == aa:bb:cc:dd:ee:ff       # sorgente o destinazione
oui.manufacturer == "Apple"         # tutti i dispositivi Apple (richiede plugin)

# Nmap: OUI detection
nmap -sn 192.168.1.0/24             # include MAC e vendor nella discovery locale
```

---

## Privacy e MAC randomization

I sistemi operativi moderni **randomizzano il MAC** in contesti specifici per impedire il tracking basato su questo identificatore:

| OS | Comportamento |
|---|---|
| Android 10+ | MAC randomizzato per default per ogni rete Wi-Fi (diverso per ogni SSID) |
| iOS 14+ | MAC randomizzato per default; cambia periodicamente sulla stessa rete |
| Windows 10/11 | opzione "Usa indirizzi hardware casuali" nel profilo Wi-Fi |
| Linux (NetworkManager) | `wifi.cloned-mac-address=random` in `/etc/NetworkManager/conf.d/` |

Il MAC randomizzato ha U/L = 1 (bit localmente amministrato alzato), visibile in [[Wireshark]] come MAC con il secondo bit del primo byte a 1.

**Impatto sulla difesa:** port security basata su MAC fisso è problematica con dispositivi che randomizzano → preferire 802.1X/NAC con autenticazione certificato o credenziali.

---

## Domande da esame/colloquio

1. **Cosa sono l'OUI e la parte NIC di un MAC address, e come si usa l'OUI in recon?**
   I primi 3 byte (OUI) identificano il produttore della NIC (assegnati dall'IEEE); gli ultimi 3 (NIC) sono il seriale del dispositivo. In recon si fa lookup dell'OUI per identificare il vendor: distingue un host fisico (Dell, HP) da una VM (VMware `00:50:56`, VirtualBox `08:00:27`), o identifica il tipo di IoT.

2. **Cosa sono i bit I/G e U/L e come si leggono in un MAC?**
   Il bit **I/G** (LSB del primo byte) indica unicast (0) o multicast/broadcast (1). Il bit **U/L** (secondo bit del primo byte) indica MAC assegnato globalmente dall'IEEE (0) o localmente (1). Un MAC con U/L=1 è tipicamente randomizzato o assegnato manualmente — segnale utile in forensica.

3. **Perché il filtraggio MAC su Wi-Fi non è un controllo di sicurezza efficace?**
   Il MAC address è trasmesso in chiaro in ogni frame 802.11, anche prima dell'associazione. Un attaccante in ascolto passivo può vedere i MAC autorizzati in secondi con [[Wireshark]], poi clonarli con `macchanger` o `ip link set ... address`. Il filtro è aggirato senza alcuna competenza tecnica avanzata.

4. **Come funziona il MAC flooding e perché rende la rete insicura?**
   Si inonda lo switch di frame con MAC sorgenti casuali, saturando la tabella CAM. Lo switch non può aggiungere nuove entry → per i frame a MAC sconosciuto fa flooding su tutte le porte → ogni dispositivo connesso riceve tutto il traffico unicast della LAN, abilitando lo sniffing passivo. Mitigazione: port security (numero massimo di MAC per porta).

5. **Perché il MAC sorgente cambia a ogni hop di router mentre l'IP rimane invariato?**
   Il MAC opera a L2 (Data Link) ed è significativo solo nel segmento locale. Quando il pacchetto attraversa un router, il router decapsula il frame L2 (butta il vecchio header Ethernet), consulta la routing table sull'IP destinazione (L3), e costruisce un **nuovo frame L2** con i MAC del segmento successivo. L'IP destinazione (L3) non viene modificato (salvo NAT).

6. **Che differenza c'è tra un indirizzo MAC unicast, multicast e broadcast, con esempi reali?**
   - **Unicast** (I/G=0): frame per un singolo dispositivo, es. `AC:DE:48:12:34:56` — usato per la comunicazione normale tra due host.
   - **Multicast** (I/G=1, diverso da tutti-1): frame per un gruppo di dispositivi che si sono "iscritti", es. `01:00:5E:00:00:05` (OSPF routers all), `01:80:C2:00:00:00` (STP).
   - **Broadcast** (I/G=1, tutti i bit a 1): `FF:FF:FF:FF:FF:FF` — ricevuto da tutti i dispositivi nel broadcast domain; usato da ARP Request e DHCP Discover.

---

## Lab
- In locale: `ip link` per leggere il tuo MAC; `macchanger -r eth0` (lab) per cambiarlo e osservare il bit U/L alzato.
- [[Wireshark]]: filtra `eth.addr` e `eth.dst == ff:ff:ff:ff:ff:ff` per distinguere unicast da broadcast; fai lookup dell'OUI su macvendors.com.
- [[TryHackMe]] — *Wireshark: The Basics* (frame Ethernet, MAC sorgente/destinazione, ARP).

## Collegamenti
- [[ARP]] · [[DHCP]] · [[Modello OSI]] · [[Indirizzamento IP]]
- [[Hardware di Rete]] — switch e tabella CAM
- [[Man-in-the-Middle (MITM)]] · [[Wireshark]]
- [[Rete Informatica e i suoi Componenti]]

## Fonti
- Cloudflare — What is a MAC address: https://www.cloudflare.com/learning/network-layer/what-is-a-mac-address/
- IEEE 802 — MAC address structure (I/G, U/L bits): https://standards.ieee.org/
- RFC 7042 — IEEE 802 parameters: https://datatracker.ietf.org/doc/html/rfc7042
- Peterson & Davie — *Computer Networks: A Systems Approach* (cap. "Direct Links" e "LAN Switching": frame, CSMA/CD, FCS, switch learning, STP, VLAN): https://book.systemsapproach.org/
