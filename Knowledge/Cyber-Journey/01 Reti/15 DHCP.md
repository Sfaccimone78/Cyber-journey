---
tipo: concetto
tag: [reti]
fase: 1
fonti: 3
aggiornato: 2026-06-22
stato: maturo
aliases: ["DHCP"]
---

# DHCP

## In breve
Il **DHCP** (Dynamic Host Configuration Protocol) assegna automaticamente [[Indirizzamento IP|IP]], subnet mask, **default gateway** e **server [[DNS]]** a un host che si connette, evitando la configurazione manuale. Gira su [[UDP]] (server porta 67, client porta 68) ed è uno dei primi protocolli a funzionare **prima** che l'host abbia un IP — per questo usa il broadcast. È anche un classico punto di [[Man-in-the-Middle (MITM)|MITM]] in LAN.

---

## DORA: i quattro passi in dettaglio

```
Client → broadcast (255.255.255.255)  DHCPDISCOVER   src=0.0.0.0:68 dst=255.255.255.255:67
         "c'è un server DHCP? Ho bisogno di un IP."
         [Opzione 60: vendor class; Opzione 12: hostname; Opzione 55: lista opzioni richieste]

Server → broadcast o unicast           DHCPOFFER      src=ServerIP:67
         "ti offro 192.168.1.50, lease 86400s, gw=192.168.1.1, dns=1.1.1.1"
         [può essere in broadcast se il client non ha ancora un IP]

Client → broadcast (255.255.255.255)  DHCPREQUEST    src=0.0.0.0:68
         "accetto l'offerta di 192.168.1.1 per IP=192.168.1.50"
         [broadcast: notifica a TUTTI i server DHCP — chi non è stato scelto libera la propria riserva]

Server → client                        DHCPACK        conferma definitiva + parametri completi
         [il client configura l'interfaccia e avvia il timer di lease]
```

Perché la **DHCPREQUEST** è in broadcast anche se il client conosce già l'IP del server? Perché in una rete con più server DHCP, solo uno viene scelto: gli altri devono sapere che la loro offerta è stata rifiutata e rilasciare l'IP prenotato.

### Stati del client DHCP
```
INIT → SELECTING (riceve offerte) → REQUESTING (sceglie) → BOUND (ha l'IP)
    → RENEWING (a T1: rinnova con il suo server) → REBINDING (a T2: cerca qualsiasi server)
    → INIT (lease scaduto, ricomincia) oppure → BOUND (rinnovo riuscito)
```

---

## Lease, rinnovo e timer

| Timer | Quando scatta | Cosa fa il client |
|-------|---------------|-------------------|
| **T1 (50% del lease)** | es. 12h su un lease di 24h | Invia DHCPREQUEST **unicast** al suo server per rinnovare |
| **T2 (87,5% del lease)** | es. 21h su 24h | T1 fallito → DHCPREQUEST **broadcast** a qualsiasi server |
| **Lease scaduto** | es. 24h | Il client deve cessare di usare l'IP; ricomincia il ciclo DORA |

Se T2 fallisce e il lease scade, il client perde l'IP e torna allo stato INIT. In produzione questo causa una breve interruzione di rete.

---

## DHCP Options (le opzioni che portano dati)

Le opzioni DHCP seguono il formato **TLV** (Type-Length-Value). Le più rilevanti:

| Opzione | Contenuto | Note di sicurezza |
|---------|-----------|-------------------|
| 1 | Subnet mask | |
| 3 | Default gateway | Falsificabile con rogue DHCP |
| 6 | DNS server | Falsificabile → DNS hijacking |
| 15 | Dominio di ricerca | |
| 51 | Lease time | |
| 66 | TFTP server (PXE) | Vettore di attacco PXE boot |
| 67 | Boot filename (PXE) | Idem |
| 121 | Rotte statiche | Permette di iniettare rotte specifiche → MITM su subnet |
| 43 | Vendor-specific | Usato da IP phone Cisco, access point per config automatica |
| 82 | Relay Agent Information | Aggiunto dallo switch per identificare porta/VLAN del client |

L'**opzione 121** (rotte statiche) è particolarmente pericolosa: un rogue DHCP può spingere una rotta `0.0.0.0/0 via attacker` o rotte più specifiche per intercettare traffico verso subnet sensibili senza cambiare il gateway di default.

---

## DHCP Relay (helper address)

In reti segmentate ogni VLAN ha la sua subnet, ma un singolo server DHCP serve tutto. Il **DHCP relay** (configurato sullo switch L3 o router) converte il broadcast del client in unicast verso il server DHCP:

```
Client (VLAN 10: 10.0.10.0/24) → broadcast DHCPDISCOVER
  ↓
Switch L3 (relay: ip helper-address 192.168.1.1) → unicast verso 192.168.1.1:67
  ↓
DHCP server → risponde con IP dalla pool VLAN 10
  ↓
Switch relay → recapita al client
```

Il relay aggiunge l'**opzione 82** (Circuit ID, Remote ID) per identificare da quale porta/VLAN arriva la richiesta — utilizzata dal server per assegnare IP dalla pool corretta e anche da DHCP snooping per validare le risposte.

---

## Comandi pratici

```bash
# Linux — stato lease e interfacce
ip addr show
cat /var/lib/dhcp/dhclient.leases     # dettaglio lease (IP, server, scadenza)
sudo dhclient -v eth0                  # rinnovo verboso (vedi il dialogo DORA)
sudo dhclient -r eth0 && sudo dhclient eth0  # release + renew

# Windows
ipconfig /all                         # mostra IP, lease ottenuto/scade, server DHCP
ipconfig /release                     # DHCPRELEASE al server
ipconfig /renew                       # nuovo DHCPDISCOVER/REQUEST

# Wireshark — cattura DHCP
# Filtro: bootp   (il protocollo si chiama ancora BOOTP nel dissector Wireshark)
# Oppure: udp.port == 67 || udp.port == 68

# Verifica server DHCP attivi in LAN (come admin)
sudo nmap -sU -p 67 --script dhcp-discover 192.168.1.0/24
```

---

## Attacchi

### Rogue DHCP server (MITM)
Un server DHCP malevolo in LAN risponde a DHCPDISCOVER più in fretta del legittimo e distribuisce **gateway e DNS falsi** → tutto il traffico dei nuovi client passa per l'attaccante.

```bash
# Esempio con metasploit (lab autorizzati)
use auxiliary/server/dhcp
set SRVHOST 0.0.0.0
set ROUTER <IP_attaccante>
set DNSSERVER <IP_attaccante>
run
# Poi abilitare ip_forward e intercettare con Wireshark/mitmproxy
```

L'attacco è efficace soprattutto su reti Wi-Fi dove è facile inserire un access point con server DHCP. In ambienti LAN cablati, DHCP snooping lo blocca (vedi difese).

### DHCP Starvation (DoS → preludio al rogue)
L'attaccante inonda di DHCPDISCOVER con **MAC address falsificati** (ogni richiesta usa un MAC diverso). Il pool DHCP si esaurisce → i client legittimi non ottengono IP (DoS). Spesso usato come passo 1 prima di attivare il rogue server.

```bash
# yersinia (lab autorizzati)
yersinia dhcp -attack 1    # starvation
# dhcpstarv, gobbler — stessi effetti
```

### DHCPv6 / mitm6
In reti dual-stack IPv6, il DHCPv6 e i Router Advertisement (RA) IPv6 sono spesso attivi ma non monitorati. `mitm6` risponde alle richieste DHCPv6/RA dichiarandosi **DNS server IPv6** della vittima. Le macchine Windows preferiscono IPv6 → il DNS di mitm6 risolve verso l'attaccante → relay NTLM verso [[Active Directory]].

```bash
# mitm6 in abbinamento con ntlmrelayx (lab autorizzati)
sudo mitm6 -d domain.local
sudo impacket-ntlmrelayx -6 -t ldaps://DC.domain.local --delegate-access
```

Difesa: RA Guard sugli switch, disabilitare DHCPv6/IPv6 se non utilizzati, segmentare con VLAN.

### Option 121 Route Injection
Con un rogue DHCP che distribuisce l'opzione 121, l'attaccante può iniettare rotte statiche specifiche nel client (es. `10.0.0.0/8 via 192.168.1.99`) senza cambiare il gateway di default. Il client instrada silenziosamente traffico interno verso l'attaccante — rilevabile solo analizzando la routing table del client.

---

## Difese

| Meccanismo | Dove si configura | Cosa fa |
|---|---|---|
| **DHCP Snooping** | Switch L2 (Cisco: `ip dhcp snooping`) | Distingue porte "trusted" (verso il server legittimo) da "untrusted" (verso i client). Blocca DHCPOFFER e DHCPACK sulle porte untrusted. |
| **Dynamic ARP Inspection (DAI)** | Switch L2, abbinato al snooping | Usa il binding table del snooping per validare che i pacchetti ARP usino IP/MAC coerenti con il lease DHCP assegnato. Blocca ARP spoofing. |
| **Port Security** | Switch L2 | Limita il numero di MAC address per porta → rende difficile lo starvation. |
| **RA Guard** | Switch L2 (IPv6) | Blocca i Router Advertisement su porte non autorizzate → mitiga mitm6. |
| **IP Source Guard** | Switch L2 | Blocca traffico IP da IP non assegnati dal server DHCP (usa il binding table). |
| **DHCP Failover** | Server DHCP | Due server si sincronizzano il pool → disponibilità anche se uno cade. |

### DHCP Snooping — binding table
Lo snooping costruisce una tabella `MAC → IP → porta → VLAN → lease` intercettando i DHCPACK. Questa tabella è il fondamento di DAI e IP Source Guard: qualsiasi pacchetto che non corrisponde alla tabella viene droppato.

---

## DHCP in forensica

I log DHCP collegano `MAC address → IP → timestamp`, rendendo possibile sapere quale dispositivo fisico aveva un certo IP in un dato momento. Essenziale in:
- **Incident response**: "chi ha fatto questa connessione HTTP alle 14:32?" → DHCP log → MAC → produttore (OUI) → dispositivo.
- **Investigazioni legali**: corroborare o smentire le affermazioni di un indagato su chi usava un certo IP.
- **Asset inventory**: confrontare i lease con gli asset noti per trovare dispositivi non autorizzati (shadow IT, BYOD).

```bash
# Log DHCP su Linux (ISC DHCP server)
cat /var/log/syslog | grep dhcpd
# Formato: "DHCPACK on 192.168.1.50 to aa:bb:cc:dd:ee:ff via eth0"

# Windows Server DHCP log
# %windir%\System32\dhcp\DhcpSrvLog-*.log
# Formato CSV con data/ora, tipo evento, IP, hostname, MAC
```

---

## Casi limite e troubleshooting

- **Pool esaurito**: i nuovi client non ottengono IP. Sintomo: `169.254.x.x` (APIPA) su Windows — il client assegna a se stesso un link-local IPv4. Fix: aumentare il pool, ridurre i lease time, trovare i lease "zombie" (dispositivi disconnessi con lease lungo).
- **IP duplicati**: due client ottengono lo stesso IP (server mal configurato o rogue). Sintomo: conflitti ARP, connessioni instabili. `arping` per rilevare duplicati.
- **DHCP relay non funziona**: ip helper-address sbagliato, ACL che blocca UDP 67/68 tra VLAN, o il server non ha una pool per quella subnet. Debug: `debug ip dhcp server events` su Cisco.
- **Client ottiene IP sbagliato**: pool mal segmentate su server DHCP che serve più VLAN (il relay non porta l'opzione 82 o il server non la usa). Soluzione: classi o pool con match sull'opzione 82 / giaddr.
- **Lease non rinnovato su T1 (unicast)**: firewall tra il client e il server che blocca l'unicast UDP 67. Il client aspetta T2 e tenta broadcast, che passa dallo switch relay → funziona ma ritarda il rinnovo.

---

## Domande da esame/colloquio

1. **Perché DHCP usa il broadcast anche se il server è noto dopo la prima offerta?** Il DHCPREQUEST è in broadcast perché potrebbero esserci più server DHCP. Il broadcast notifica a tutti che solo uno è stato scelto, permettendo agli altri di liberare le proprie riserve. Solo da DHCPACK in poi il client usa unicast.

2. **Cos'è il DHCP snooping e come blocca il rogue DHCP?** Lo switch distingue porte "trusted" (verso il server legittimo) e "untrusted" (verso i client). Dropa qualsiasi DHCPOFFER/DHCPACK che arriva su una porta untrusted → un rogue server collegato a una porta utente non riesce a consegnare la sua risposta.

3. **Come funziona un attacco DHCP starvation e qual è il suo scopo reale?** L'attaccante manda migliaia di DHCPDISCOVER con MAC falsificati, esaurendo il pool. I client legittimi non ottengono IP. Spesso è il passo 1: pool vuoto → rogue DHCP (già pronto con un pool proprio) diventa il solo responder → MITM completo.

4. **Cos'è mitm6 e perché funziona in reti Windows?** Windows preferisce IPv6 a IPv4. Se un attaccante risponde ai Router Advertisement DHCPv6 dichiarandosi DNS server IPv6, le macchine Windows lo usano automaticamente per risolvere i nomi. Il DNS malevolo può quindi rispondere con IP dell'attaccante e avviare un relay NTLM verso Active Directory.

5. **Cosa contiene il binding table del DHCP snooping e a cosa serve?** Contiene la mappa `MAC → IP → porta switch → VLAN → scadenza lease`. È la base per DAI (valida gli ARP) e IP Source Guard (dropa traffico da IP non assegnati). Permette allo switch di sapere "questo pacchetto viene dall'host legittimo che ha quel lease?".

6. **Perché un IP APIPA (169.254.x.x) indica un problema DHCP?** Se il client non riceve risposta entro il timeout (tipicamente 4 DISCOVER spaziate esponenzialmente), si auto-assegna un IP link-local APIPA. Indica che nessun server DHCP ha risposto: server down, pool esaurito, rete non raggiungibile, VLAN sbagliata.

---

## Collegamenti
- [[Indirizzamento IP]]
- [[MAC Address]]
- [[DNS]]
- [[NAT]]
- [[ARP]]
- [[UDP]]
- [[Man-in-the-Middle (MITM)]]
- [[Hardware di Rete]]
- [[Active Directory]]
- [[Wireshark]]

## Fonti
- Cloudflare — What is DHCP: https://www.cloudflare.com/learning/network-layer/what-is-dhcp/
- RFC 2131 — Dynamic Host Configuration Protocol: https://datatracker.ietf.org/doc/html/rfc2131
- Cisco — DHCP snooping / DAI configuration guide
