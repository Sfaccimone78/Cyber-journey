---
tipo: concetto
tag: [reti]
fase: 1
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Hardware di Rete"]
---

# Hardware di Rete

## In breve
L'hardware è la componente tangibile di una [[Rete Informatica e i suoi Componenti|rete]]: dispositivi finali, dispositivi intermedi e mezzi di trasmissione. Ogni dispositivo intermedio opera a un **livello [[Modello OSI|OSI]]** preciso e quel livello determina **per cosa instrada** (MAC vs IP vs L7) e **dove un attaccante può inserirsi o dove una difesa deve agire**. Saper leggere una topologia = saper prevedere i punti di intercettazione e i confini di sicurezza.

---

## Dispositivi finali (host / end-device)
Origine o destinazione del traffico: client (PC, smartphone), server (offrono servizi), stampanti, telecamere IP, IoT. Ogni host ha almeno una **NIC** (Network Interface Card) con un [[MAC Address]] di fabbrica e uno o più [[Indirizzamento IP|indirizzi IP]] assegnati. La NIC opera a livello 1/2: converte bit in segnali fisici e gestisce il MAC.

---

## Dispositivi intermedi — livello OSI, funzione e sicurezza

| Dispositivo | Livello OSI | Instrada per | Funzione principale | Rilevanza sicurezza |
|---|---|---|---|---|
| **Hub** | 1 — Fisico | nessuno (ripete su tutte le porte) | ripetitore elettrico; amplifica e distribuisce il segnale a tutti | obsoleto; **sniffing passivo** banale — tutto il traffico va a tutti |
| **Switch** | 2 — Data Link | [[MAC Address]] (tabella CAM) | inoltra frame unicast solo sulla porta corretta | MAC flooding → fail-open; mitigare con port security |
| **Router** | 3 — Network | [[Indirizzamento IP\|IP]] (tabella di routing) | instrada pacchetti tra reti diverse; spezza i broadcast domain | ACL, NAT, filtro inter-VLAN; punto critico di segmentazione |
| **WAP (Access Point)** | 2 — Data Link | MAC, su mezzo radio | bridge wireless↔cablato | rogue AP, evil twin; richiede WPA2/3-Enterprise |
| **Firewall** | 3–7 | regole su IP/porta/stato/L7 | filtra traffico in/out secondo policy | L4 stateful vs NGFW (ispezione DPI a L7) |
| **IDS/IPS** | 3–7 | firme, anomalie comportamentali | IDS: rileva e allerta; IPS: blocca inline | falsi positivi vs falsi negativi; placement critico |
| **Load balancer** | 4 (L4) / 7 (L7) | distribuzione di sessioni/richieste | divide il carico tra backend | termina [[TLS e SSL\|TLS]] (visibilità → attento alla key management); nasconde i backend |
| **Modem** | 1–2 | modulazione/demodulazione segnale | converte digitale↔analogico/DSL/fibra | bordo della rete domestica; spesso combinato con router |
| **Proxy** | 7 — Applicazione | URL, contenuto, policy | intermediario tra client e server | forward proxy (filtra uscita), reverse proxy (espone backend) |

---

## Switch: meccanismo interno a basso livello

Lo switch è il dispositivo centrale di ogni LAN moderna. Funziona in questo modo:

1. **Apprendimento (learning):** ogni frame in ingresso su una porta porta con sé il **MAC sorgente**. Lo switch registra `{MAC → porta, timestamp}` nella **tabella CAM** (Content Addressable Memory). La CAM ha dimensione finita (tipicamente 4.000–128.000 entry).
2. **Inoltro (forwarding):** lo switch cerca il MAC destinazione nella CAM:
   - **trovato** → invia il frame solo sulla porta corrispondente (unicast selettivo);
   - **non trovato / broadcast / multicast** → **flooding** su tutte le porte eccetto quella di ingresso.
3. **Aging:** le entry scadono (default 300 s) se non vengono aggiornate, liberando spazio.

### Attacco: MAC Flooding
Un attaccante invia migliaia di frame con MAC sorgente casuali (tool: `macof` da dsniff). La CAM si satura → lo switch non riesce più ad aggiungere entry → ogni frame diventa flooding → **tutti i dispositivi vedono tutto il traffico** (equivalente a un hub).

**Difese:**
- **Port security:** limita il numero massimo di MAC per porta (es. 2); se superato, la porta va in `err-disabled` o droppa i frame in eccesso.
- **802.1X (NAC):** autenticazione del dispositivo prima di poter usare la porta → MAC fittizi non ottengono accesso.
- **Dynamic ARP Inspection (DAI):** non è contro il flooding in sé, ma previene [[ARP]] poisoning che spesso segue.

### Switch managed vs unmanaged

| Caratteristica | Unmanaged | Managed |
|---|---|---|
| Configurazione | plug-and-play, nessuna | CLI/web, SNMP, SSH |
| VLAN | non supportate | supportate (802.1Q) |
| STP/RSTP | spesso assente | presente |
| Port security | assente | configurabile |
| Port mirroring (SPAN) | assente | disponibile per cattura traffico |
| Uso tipico | LAN casalinga, ufficio piccolo | ambienti aziendali, datacenter |
| Sicurezza | minima | gestibile centralmente |

> In un ambiente enterprise, usare switch unmanaged è una misconfigurazione: non si possono applicare VLAN, port security, o monitorare il traffico via SPAN.

### VLAN (Virtual LAN)
Una VLAN segmenta logicamente la LAN sullo stesso switch fisico. I frame 802.1Q portano un **tag a 12 bit** (VLAN ID, 1–4094) inserito nell'header Ethernet. Le porte switch sono:
- **Access port:** appartiene a una VLAN, rimuove il tag in uscita verso l'host.
- **Trunk port:** trasporta più VLAN contemporaneamente (tag incluso) verso altri switch o router.

**VLAN hopping:** se un attaccante riesce a negoziare un trunk (sfruttando DTP, Dynamic Trunking Protocol) può iniettare frame taggati per altre VLAN. Fix: disabilita DTP (`switchport nonegotiate`), imposta le porte access esplicitamente, usa VLAN nativa non predefinita.

---

## Router: meccanismo interno a basso livello

Il router opera a L3 e il suo ciclo di vita per ogni pacchetto è:
1. **Ricezione frame L2:** decapsula l'header Ethernet, espone il pacchetto IP.
2. **Lookup routing table:** confronta l'IP destinazione con le rotte usando il **Longest Prefix Match** (la rotta più specifica vince: `/30` batte `/24`).
3. **Decremento TTL:** riduce il campo TTL di 1. Se TTL = 0, scarta il pacchetto e manda [[ICMP]] Time Exceeded all'origine (base di `traceroute`).
4. **ARP resolution next-hop:** se il next-hop è sulla rete direttamente connessa, usa ARP per trovarne il MAC.
5. **Ri-incapsulazione L2:** crea un nuovo frame Ethernet con MAC sorgente = interfaccia del router e MAC destinazione = next-hop MAC. L'IP rimane invariato (a meno di NAT).
6. **Trasmissione:** invia il frame sull'interfaccia di uscita.

Il router **spezza il dominio di broadcast**: i frame ARP `FF:FF:FF:FF:FF:FF` non vengono inoltrati tra interfacce diverse.

### ACL su router
Le Access Control List filtrano il traffico su criteri di 5-tupla (IP src/dst, porta src/dst, protocollo). Le ACL standard (solo IP src) vanno applicate vicino alla destinazione; le ACL estese (5-tupla) vicino alla sorgente. Un router con ACL è un firewall elementare, meno potente di un NGFW ma sufficiente per segmentazione di base.

---

## Firewall: tipologie e livelli di ispezione

| Tipo | Livello | Stato | Cosa controlla | Limiti |
|---|---|---|---|---|
| **Packet filter (stateless)** | L3/L4 | nessuno | ogni pacchetto indipendentemente (IP, porta, flag) | non vede la connessione completa; aggirabile con pacchetti ACK |
| **Stateful inspection** | L3/L4 | tabella di stato delle connessioni TCP/UDP | verifica che il pacchetto appartenga a una sessione legittima | non ispeziona il payload applicativo |
| **Application layer (NGFW)** | L7 | stateful + DPI | contenuto HTTP, DNS, TLS SNI, applicazione | SSL inspection richiede trust della CA interna |
| **WAF (Web Application Firewall)** | L7 | stateful | richieste HTTP/HTTPS (SQLi, XSS, LFI…) | specialmente per app web; non sostituisce il NGFW |

Un firewall **stateful** traccia le connessioni [[TCP]] nella propria tabella: sa che un SYN/ACK è legittimo solo se è preceduto da un SYN uscente. Uno **stateless** non lo sa → vulnerabile a spoofing di pacchetti ACK.

---

## Wireless Access Point (WAP): sicurezza

Il WAP crea un mezzo condiviso radio: ogni frame è fisicamente ricevuto da chiunque sia nel raggio. La sicurezza dipende dalla **cifratura**:

| Standard | Cifratura | Stato |
|---|---|---|
| WEP | RC4 (rotto in minuti) | **da non usare assolutamente** |
| WPA (TKIP) | RC4 migliorato | vulnerabile, deprecato |
| WPA2-Personal (CCMP/AES) | AES-128 | accettabile per uso casalingo; vulnerabile a PMK hash offline se passphrase debole |
| WPA2-Enterprise (802.1X/EAP) | AES + autenticazione RADIUS | standard enterprise |
| WPA3 | SAE (Dragonfly), forward secrecy | stato dell'arte; richiede hardware recente |

**Attacchi tipici al Wi-Fi:**
- **Rogue AP / Evil Twin:** un attaccante crea un AP con lo stesso SSID della rete legittima → i client si connettono al finto AP → [[Man-in-the-Middle (MITM)|MitM]].
- **Deauth attack (802.11):** invia frame di de-autenticazione (non autenticati in 802.11 classico) → disconnette i client forzandoli a riconnettersi (cattura il handshake WPA2 per attacco dizionario). Risolto in 802.11w (Management Frame Protection).
- **PMKID attack:** cattura il PMKID dall'handshake anche senza de-autenticare i client → crack offline della passphrase.

---

## Esempio pratico (topologia LAN enterprise tipica)

```
Internet
   |
[Modem/ONT]  ← bordo ISP
   |
[Firewall NGFW]  ← L3/L7, zona DMZ / LAN / WAN
   |      \
[WAP]  [Core Switch managed L3]  ← inter-VLAN routing
           |         |
     [Switch L2]  [Switch L2]
      VLAN 10      VLAN 20
      (Utenti)     (Server)
```

In recon, un attaccante mappa questa catena con [[Nmap]] (host discovery, porte aperte, versioni) e [[ARP]] (per scoprire il gateway). Il difensore usa port mirroring (SPAN) sullo switch per alimentare un [[SIEM]] o [[Wireshark]] con il traffico reale.

---

## Attacco e difesa: riepilogo per dispositivo

| Dispositivo | Attacco tipico | Difesa |
|---|---|---|
| Hub | sniffing passivo (tutti vedono tutto) | **sostituirlo con uno switch** |
| Switch | MAC flooding, ARP poisoning, VLAN hopping | port security, DAI, DHCP snooping, DTP off |
| Router | route injection (BGP hijack), ACL bypass con ACK spoofing | autenticazione BGP MD5/RPKI, stateful firewall |
| WAP | evil twin, deauth, PMKID crack | WPA3 / WPA2-Enterprise 802.1X, 802.11w, WIDS |
| Firewall | bypass con tunnel cifrati (DNS-over-HTTPS, C2 su 443) | deep packet inspection, SSL inspection, policy egress |
| IDS/IPS | evasion con frammentazione, encoding, polimorfismo | regole aggiornate, NGFW con decodifica, anomaly-based |

---

## Casi limite e troubleshooting

- **Switch in fail-open dopo MAC flooding:** tutto il traffico diventa flooding → prestazioni crollano, sniffing possibile. Identificabile da un picco di traffico su porte non interessate. Fix immediato: `shutdown`/`no shutdown` sulla porta dell'attaccante; fix permanente: port security.
- **Loop di switch senza STP:** i frame broadcast circolano all'infinito → broadcast storm. Lo si vede dalle luci di attività tutte fisse al 100% e dal crollo del throughput. Abilitare **RSTP** (Rapid Spanning Tree Protocol) su tutti gli switch managed.
- **Router con TTL = 0 loop:** due router con rotte di default che si puntano vicendevolmente → i pacchetti rimbalzano fino al TTL 0. Diagnosticabile con `traceroute` che mostra i due hop in loop. Fix: rotte più specifiche o rotta null (`ip route 0.0.0.0/0 null0`).
- **DHCP rogue:** un attaccante connette un DHCP server non autorizzato → assegna gateway e DNS malevoli ai client. Fix: **DHCP snooping** (solo le porte trusted possono rispondere a richieste DHCP).

---

## Domande da esame/colloquio

1. **A che livello OSI opera uno switch e come costruisce la tabella CAM?**
   Livello 2 (Data Link). Legge il **MAC sorgente** di ogni frame in ingresso e associa quel MAC alla porta di arrivo. Se il MAC destinazione non è nella CAM, fa flooding. La CAM ha un aging time (default 300 s).

2. **Qual è la differenza tra un firewall stateful e uno stateless, e perché il secondo è più aggirabile?**
   Lo **stateful** mantiene una tabella delle connessioni TCP/UDP e accetta solo i pacchetti che appartengono a una sessione stabilita legittimamente. Lo **stateless** valuta ogni pacchetto in isolamento: un attaccante può inviare un pacchetto ACK verso una porta aperta e potrebbe attraversare il filtro se la regola permette ACK in ingresso senza verifica dello stato.

3. **Cos'è il MAC flooding e come lo si mitiga?**
   Si inondano lo switch di frame con MAC sorgenti casuali, saturando la tabella CAM. Lo switch non può più imparare nuovi MAC → fa flooding di tutto il traffico → chiunque può sniffare. Mitigazione: **port security** (numero massimo di MAC per porta), 802.1X per autenticare i dispositivi.

4. **Differenza tra switch managed e unmanaged in un contesto di sicurezza?**
   Il managed permette di configurare VLAN, port security, STP, SNMP monitoring, port mirroring (SPAN) e 802.1X. L'unmanaged non offre nulla di questo: è un rischio in ambienti enterprise perché non si può segmentare, monitorare o proteggere il traffico a L2.

5. **Come funziona un evil twin attack su Wi-Fi e come si difende?**
   L'attaccante crea un AP con lo stesso SSID della rete legittima, spesso con segnale più forte, e invia frame di de-autenticazione (802.11 deauth) per staccare i client dall'AP reale. I client si riconnettono all'AP finto → MitM. Difese: **WPA2-Enterprise / 802.1X** (l'utente autentica anche il server RADIUS, non solo la passphrase), **802.11w** (Management Frame Protection, rende i frame deauth autenticati), **WIDS** (Wireless Intrusion Detection System).

6. **A cosa serve il TTL e cosa succede quando arriva a zero?**
   Il TTL (Time To Live) è un contatore decrementato da ogni router a ogni hop. Previene i loop di routing: quando arriva a 0, il router scarta il pacchetto e invia un messaggio [[ICMP]] Time Exceeded all'origine. `traceroute` sfrutta questo meccanismo: invia pacchetti con TTL = 1, 2, 3… raccogliendo l'ICMP Time Exceeded di ogni router intermedio per mappare il percorso.

---

## Lab
- [[TryHackMe]] — *Network Device Hardening* e *Intro to LAN* (switch, router, VLAN, domini di broadcast).
- Cisco Packet Tracer / GNS3: costruisci una topologia con switch managed + VLAN e prova port security e DHCP snooping.
- In lab autorizzato: simula un MAC flooding con `macof` su uno switch e osserva il passaggio a flooding con [[Wireshark]].

## Collegamenti
- [[Rete Informatica e i suoi Componenti]] · [[Modello OSI]]
- [[MAC Address]] · [[ARP]] · [[Indirizzamento IP]] · [[NAT]]
- [[Man-in-the-Middle (MITM)]] · [[Wireshark]] · [[ICMP]]
- [[SIEM]] · [[Three-Way Handshake TCP]]

## Fonti
- Cisco — Network switch vs router: https://www.cisco.com/c/en/us/solutions/small-business/resource-center/networking/network-switch-vs-router.html
- Cloudflare Learning — What is a router?: https://www.cloudflare.com/learning/network-layer/what-is-a-router/
- Cisco — Port security / DAI configuration guides
