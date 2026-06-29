---
tipo: entita
tag: [reti]
fase: 1
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["ARP"]
---

# ARP

## Cos'è
**ARP** (Address Resolution Protocol, RFC 826) traduce un indirizzo **IP** logico nel [[MAC Address]]
fisico corrispondente **sulla stessa rete locale**. È il "ponte" tra il livello 3 ([[Indirizzamento IP|IP]])
e il livello 2 (Ethernet) del [[Modello OSI]]: l'IP dice *a quale host*, ma per mettere il pacchetto in
un frame e spedirlo sul filo serve il MAC di destinazione. ARP lo scopre. Vale **solo nella LAN**: per
host su reti diverse si risolve il MAC del **gateway**, non quello del destinatario finale.

## Il meccanismo passo per passo
1. Il PC vuole inviare a `192.168.1.1` ma non ne conosce il MAC.
2. Manda un **ARP Request** in **broadcast** (`ff:ff:ff:ff:ff:ff`): *"Chi ha `192.168.1.1`? Rispondi a
   `aa:bb:cc:dd:ee:ff`."* — lo ricevono tutti gli host della LAN.
3. Solo il possessore di quell'IP risponde con un **ARP Reply** in **unicast**: *"Sono io, MAC
   `aa:bb:cc:11:22:33`."*
4. Il PC memorizza la coppia IP↔MAC nella **cache ARP** (con scadenza, tipicamente decine di secondi/
   minuti) per non richiederla ogni volta.

## Formato del pacchetto ARP (i campi che contano)
| Campo | Valore tipico | Note |
|---|---|---|
| Hardware type | 1 | Ethernet |
| Protocol type | 0x0800 | IPv4 |
| Operation (opcode) | **1**=Request, **2**=Reply | distingue domanda/risposta |
| Sender MAC / Sender IP | mittente | nel poisoning sono **falsificati** |
| Target MAC / Target IP | destinatario | nella Request il Target MAC è vuoto |

L'EtherType del frame che trasporta ARP è `0x0806` (in [[Wireshark]]: filtro `arp`).

## Varianti utili da conoscere
- **Gratuitous ARP**: un host annuncia *spontaneamente* la propria coppia IP→MAC (Reply non sollecitata).
  Usi legittimi: aggiornare le cache dopo un cambio di scheda, rilevare conflitti di IP, **failover**
  (un IP virtuale che si sposta su un altro server). È anche il vettore d'abuso (vedi sotto).
- **ARP Probe / Announcement**: all'avvio o dopo [[DHCP]], un host verifica che il suo nuovo IP non sia
  già in uso (probe) e poi lo annuncia.
- **Proxy ARP**: un router risponde *al posto di* un altro host (lo "impersona" a fin di bene per unire
  segmenti); raramente usato oggi, può confondere la diagnosi.
- **In IPv6 ARP non esiste**: il suo ruolo lo svolge **NDP** (Neighbor Discovery Protocol) via [[ICMP]]v6
  (messaggi Neighbor Solicitation/Advertisement) — con gli stessi problemi di fiducia.

## Uso pratico
```bash
ip neigh                 # Linux moderno: cache vicinato (ARP/ND)  ← preferito
arp -n                   # Linux legacy
arp -a                   # Windows / macOS
sudo arping -c 3 192.168.1.1     # forza una risoluzione ARP
# Wireshark: filtro  arp   (oppure arp.opcode==2 per le sole Reply)

# Esempio output (ip neigh):
# 192.168.1.1   dev eth0 lladdr aa:bb:cc:dd:ee:01 REACHABLE
# 192.168.1.20  dev eth0 lladdr aa:bb:cc:dd:ee:02 STALE
```
Stati della cache: `REACHABLE` (fresco), `STALE` (da riverificare), `FAILED` (nessuna risposta).

## Perché è insicuro per design
ARP è **senza stato e senza autenticazione**: un host accetta una *ARP Reply* **anche se non ha mai
mandato la Request** corrispondente, e sovrascrive la cache senza verifiche. Nessuna firma, nessun
controllo: chi parla per ultimo "vince". Questo difetto abilita il poisoning.

## ARP Spoofing / Poisoning — il MITM di LAN
L'attaccante invia Reply forgiate per **legare il proprio MAC all'IP del gateway** (e viceversa,
spesso): da quel momento il traffico della vittima verso Internet passa da lui ([[Man-in-the-Middle (MITM)]]).
```
ARP Reply forgiata (l'attaccante dice "il gateway sono io"):
  Sender IP  = 192.168.1.1        (IP del gateway — falso)
  Sender MAC = aa:bb:cc:00:00:99  (MAC dell'attaccante)
  → vittima: la cache associa 192.168.1.1 → MAC dell'attaccante
  → tutto il traffico per Internet finisce all'attaccante
```
Walkthrough tipico (lab autorizzato):
```bash
# Abilita l'inoltro, altrimenti la vittima perde Internet (DoS invece di MITM)
echo 1 > /proc/sys/net/ipv4/ip_forward
# Avvelena vittima e gateway, mettendoti in mezzo (bidirezionale)
sudo bettercap -iface eth0 -eval "set arp.spoof.targets 192.168.1.20; arp.spoof on; net.sniff on"
#   alternative storiche: arpspoof (dsniff), ettercap
```
Spesso è il **primo stadio**: seguono [[DNS]] spoofing, SSL stripping, furto credenziali con
[[Wireshark]] (vedi la sezione *Uso offensivo* lì).

## Rilevamento
- **Due IP con lo stesso MAC**, o un IP che **cambia MAC** all'improvviso.
- **Ondata di Reply non sollecitate** / gratuitous ARP anomali.
- In [[Wireshark]]: `arp.duplicate-address-detected`, o `arp.opcode==2` in volume anomalo.
- Tool dedicati: **arpwatch** (allerta sui cambi IP↔MAC); è un classico alert da
  [[Detection di Attacchi|detection]] / IDS.

## Difesa
- **DAI (Dynamic ARP Inspection)** sugli switch gestiti: valida le Reply contro la tabella **DHCP
  snooping**, scarta quelle false. È la difesa principale in ambito enterprise.
- **Port security** (limita i MAC per porta), **802.1X** (autenticazione all'accesso).
- **Voci ARP statiche** per gateway critici (non scalabile, ma utile su pochi host sensibili).
- **Segmentazione** ([[Subnetting]] / VLAN): riduce il **dominio L2** raggiungibile da un attaccante —
  ARP poisoning colpisce solo la propria VLAN.

## Casi limite e troubleshooting
| Sintomo | Causa | Diagnosi/Fix |
|---|---|---|
| "Host irraggiungibile" ma il ping al gateway va | MAC sbagliato in cache | `ip neigh flush all`, riprova |
| Conflitto IP segnalato | due host con lo stesso IP | gratuitous ARP rivela il MAC duplicato |
| Vittima perde Internet durante un test MITM | manca `ip_forward` | abilita l'inoltro sull'attaccante |
| Cache piena di STALE | normale invecchiamento | si rinfresca al primo traffico |
| ARP non risolve tra due host | sono in subnet diverse | ARP è solo intra-LAN → serve il routing |

## Domande da esame/colloquio
1. **Request in broadcast, Reply in unicast: perché?** La domanda non sa ancora chi ha l'IP → la sente
   tutta la LAN; solo il proprietario risponde, e sa già a chi (ha letto il Sender della Request).
2. **Perché ARP è vulnerabile al poisoning?** È stateless e non autenticato: accetta Reply mai
   richieste e sovrascrive la cache.
3. **Cosa serve sull'attaccante per fare MITM e non DoS?** L'IP forwarding, così il traffico
   intercettato viene comunque inoltrato a destinazione.
4. **Qual è l'equivalente di ARP in IPv6?** NDP (Neighbor Discovery) su ICMPv6, con gli stessi rischi.
5. **Difesa enterprise principale contro l'ARP spoofing?** Dynamic ARP Inspection + DHCP snooping sugli switch.

## Lab
- [[TryHackMe]] — *Wireshark: The Basics* e *Network Fundamentals* (osservare ARP Request/Reply dal vivo).
- In locale: `ip neigh` per la cache; `arping -c 3 <gateway>` per forzare una risoluzione; filtra `arp` in [[Wireshark]].
- > [!warning] Etica — In lab autorizzato isolato: ARP spoofing con `bettercap` (`arp.spoof on`) abilitando `ip_forward`, poi rileva il MAC duplicato con `arpwatch`. Mai su reti di terzi.

## Collegamenti
- [[MAC Address]] — ciò che ARP risolve · [[Indirizzamento IP]] — il punto di partenza
- [[Modello OSI]] · [[Modello TCP-IP]] — ARP a cavallo tra L2 e L3
- [[DHCP]] — DHCP snooping alimenta la DAI · [[Subnetting]] — limita il dominio L2
- [[Man-in-the-Middle (MITM)]] — l'attacco che il poisoning realizza · [[DNS]] — lo spoofing che spesso segue
- [[Wireshark]] — vedere/rilevare ARP

## Fonti
- RFC 826 — An Ethernet Address Resolution Protocol: <https://datatracker.ietf.org/doc/html/rfc826>
- Cloudflare — What is ARP / ARP spoofing: <https://www.cloudflare.com/learning/network-layer/what-is-arp/>
- RFC 5227 — IPv4 Address Conflict Detection (ARP probe/announce): <https://www.rfc-editor.org/rfc/rfc5227>
- TryHackMe — Network Fundamentals: <https://tryhackme.com/module/pre-security>
