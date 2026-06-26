---
tipo: concetto
tag: [reti]
fase: 1
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Routing IP", "Routing", "Instradamento IP", "IP Routing"]
---

# Routing IP

## In breve
Il **routing** (instradamento) è la funzione di **livello 3** ([[Modello OSI]]) che porta un pacchetto
[[Indirizzamento IP|IP]] dalla sorgente alla destinazione attraversando reti diverse. IP offre un
servizio **best-effort**, *connectionless* e *unreliable*: ogni pacchetto (datagram) è instradato
**indipendentemente**, senza garanzie di consegna, ordine o assenza di duplicati — l'affidabilità, se
serve, la aggiunge [[TCP]] sopra. Mentre [[Indirizzamento IP]] descrive *come si nominano* le reti,
questa pagina descrive *come i pacchetti le attraversano*: la routing table, il forwarding e i protocolli
che la popolano.

> IP è il **collo della clessidra** del [[Modello TCP-IP]]: tutto passa per IP, ed è IP a decidere il
> percorso hop-by-hop.

---

## Routing table e forwarding
Ogni host e ogni router ha una **routing table**: un insieme di righe
`(prefisso/maschera → next-hop, interfaccia)`. Per ogni pacchetto si applica il **longest prefix match**:
vince la rotta col prefisso **più specifico** (più lungo) che contiene l'IP destinazione. Esiste sempre
una **default route** `0.0.0.0/0` (il gateway) per tutte le destinazioni non altrimenti note.

```
Destination       Gateway        Iface
0.0.0.0/0         192.168.1.1    eth0    ← default (verso il router/gateway)
192.168.1.0/24    0.0.0.0        eth0    ← rete locale (consegna diretta)
10.8.0.0/24       10.8.0.1       tun0    ← rotta verso una VPN
```

- **Consegna diretta**: se la destinazione è nella **stessa rete** dell'host (AND con la maschera →
  stesso network), il pacchetto si consegna direttamente, risolvendo il MAC via [[ARP]].
- **Consegna indiretta**: altrimenti il pacchetto va al **next-hop** (tipicamente il default gateway),
  che a sua volta consulta la propria tabella. Il viaggio è una catena di decisioni locali, hop dopo hop.

A ogni hop il **frame [[MAC Address|L2]] viene riscritto** (nuovi MAC sorgente/destinazione del link
corrente) mentre gli **IP sorgente/destinazione restano invariati** (salvo [[NAT]]) e il **TTL** cala di 1.

---

## Forwarding vs routing (la distinzione)
- **Forwarding** (piano dati): l'azione locale e veloce di consultare la tabella e spedire il pacchetto
  sull'interfaccia giusta. Avviene per ogni pacchetto, a velocità di linea.
- **Routing** (piano di controllo): il processo, più lento, di **costruire e mantenere** la routing table
  scambiando informazioni con gli altri router tramite i protocolli di routing.

---

## Protocolli di routing: IGP vs EGP
| Categoria | Ambito | Protocolli | Algoritmo |
|---|---|---|---|
| **IGP** (Interior Gateway Protocol) | dentro un singolo dominio amministrativo (Autonomous System) | **OSPF**, IS-IS, RIP | link-state / distance-vector |
| **EGP** (Exterior Gateway Protocol) | tra Autonomous System diversi (la dorsale di Internet) | **BGP** | path-vector, basato su policy |

### Routing intra-dominio (IGP)
- **Link-state** (OSPF, IS-IS): ogni router conosce l'**intera topologia** (chi è connesso a chi, con
  quale costo) e calcola autonomamente i cammini minimi con l'algoritmo di **Dijkstra**. Converge in
  fretta e scala bene, ma richiede più memoria e CPU.
- **Distance-vector** (RIP): ogni router conosce solo "a che distanza" è ogni rete e *attraverso quale
  vicino*, scambiando vettori di distanze coi vicini (algoritmo di **Bellman-Ford**). Semplice ma soffre
  di convergenza lenta e *count-to-infinity*.

### Routing inter-dominio (EGP)
- **BGP** (Border Gateway Protocol) instrada tra **Autonomous System**. Non sceglie il percorso più corto
  in senso metrico, ma quello che rispetta le **policy** commerciali e amministrative degli operatori. È
  ciò che tiene insieme Internet — e il suo abuso è il **BGP hijacking** (dirottare il traffico
  annunciando rotte false).

---

## MTU e frammentazione
Ogni link ha una **MTU** (Maximum Transmission Unit, es. 1500 byte su Ethernet). Se un datagram è più
grande della MTU del prossimo link:
- **IPv4**: il router può **frammentare** il pacchetto; il riassemblaggio avviene **a destinazione**.
  Con il flag **DF** (Don't Fragment) impostato, il router lo scarta e risponde con [[ICMP]]
  "Fragmentation Needed" → base della **Path MTU Discovery**.
- **IPv6**: i router **non frammentano**; lo fa solo l'host sorgente, sempre via Path MTU Discovery.

La frammentazione è anche un classico vettore di **evasione dei firewall stateless** (che vedono solo il
primo frammento con l'header L4).

---

## Esempio: traceroute sfrutta il TTL
`traceroute` (Linux) / `tracert` (Windows) rivela il cammino hop-by-hop **abusando del TTL**: invia
pacchetti con TTL crescente (1, 2, 3…). Ogni router che porta il TTL a 0 scarta il pacchetto e risponde
con un **ICMP "Time Exceeded"**, rivelando così il proprio indirizzo. Sommando le risposte si ricostruisce
l'intero percorso. Dettagli pratici in [[Ping e Traceroute]].

```bash
ip route                 # la routing table locale (default + rotte dirette)
ip route get 8.8.8.8     # quale rotta verrebbe scelta per questa destinazione
traceroute 8.8.8.8       # il cammino hop-by-hop
```

---

## Rilevanza per la sicurezza
- **IP spoofing**: l'IP sorgente è falsificabile → base di **DDoS riflessi/amplificati** ([[DoS e DDoS]]).
  Difesa: filtraggio anti-spoofing / **uRPF** (BCP 38).
- **BGP hijacking**: annunciare prefissi altrui per dirottare o intercettare il traffico su scala
  Internet. Difesa: **RPKI** (Resource Public Key Infrastructure).
- **ICMP tunneling** e redirect malevoli (rotte iniettate) → manipolazione del percorso.

---

## Collegamenti
- [[Indirizzamento IP]] — come si nominano reti e host (IPv4/IPv6, CIDR) · [[Subnetting]]
- [[Modello TCP-IP]] · [[Modello OSI]] — IP è il livello 3 (Internet)
- [[ARP]] — risoluzione IP→MAC per la consegna diretta · [[MAC Address]]
- [[ICMP]] · [[Ping e Traceroute]] — TTL, Time Exceeded, Path MTU Discovery
- [[NAT]] — l'eccezione che fa *cambiare* gli IP lungo il percorso
- [[DoS e DDoS]] — IP spoofing e reflection

## Fonti
- Systems Approach — *Computer Networks* (cap. "Internetworking — IP"; cap. "Routing — link-state, distance-vector, BGP"): <https://book.systemsapproach.org/>
