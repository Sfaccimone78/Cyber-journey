---
tipo: concetto
tag: [reti]
fase: 1
fonti: 5
aggiornato: 2026-06-26
stato: maturo
aliases: ["Modello TCP-IP", "Modello TCP/IP"]
---

# Modello TCP/IP

## In breve
Il modello **TCP/IP** è l'architettura a strati **realmente implementata** su Internet (a differenza del
[[Modello OSI]], che è descrittivo). Nasce dal progetto **ARPANET/DoD** (anni '70) ed è codificato in
RFC 1122. Quattro livelli, ognuno con responsabilità precise; i dati scendono lo stack con
**incapsulamento** (ogni livello aggiunge un header) e risalgono con de-incapsulamento. Conoscere i
confini tra livelli serve a sapere **dove** un protocollo opera e **dove** mettere la difesa.

## I quattro livelli
| # | Livello | Cosa fa | PDU | Protocolli | Ambito |
|---|---------|---------|-----|-----------|--------|
| 4 | **Applicazione** | interfaccia col software, semantica del servizio | Dati | [[HTTP e HTTPS\|HTTP]], [[DNS]], [[SSH]], TLS, FTP, SMTP | end-to-end |
| 3 | **Trasporto** | consegna tra **processi** (porte), affidabilità | Segmento / Datagram | [[TCP]], [[UDP]] | end-to-end |
| 2 | **Internet** | instradamento tra reti, indirizzo logico | Pacchetto | [[Indirizzamento IP\|IP]], [[ICMP]] | hop-by-hop |
| 1 | **Accesso alla rete** | trasmissione sul mezzo, indirizzo fisico | Frame / Bit | Ethernet, Wi-Fi, [[ARP]], [[MAC Address]] | singolo link |

> [!note] Mappatura con OSI
> Applicazione TCP/IP = OSI 5-7; Trasporto = 4; Internet = 3; Accesso alla rete = 1-2. [[ARP]] vive "a
> cavallo" tra L2 e L3 perché lega IP↔MAC. (Alcuni testi usano una variante a **5 livelli** separando
> Fisico e Data link: è la stessa cosa, con Accesso-alla-rete spezzato in due.)

## Due principi che spiegano tutto Internet
- **End-to-end principle**: l'intelligenza sta agli **estremi** (gli host), non nella rete. I router
  fanno una cosa sola e bene — inoltrare pacchetti; affidabilità, ordine e cifratura li mettono gli host
  (TCP, TLS). Conseguenza di sicurezza: la rete *non* garantisce nulla → la fiducia va costruita end-to-end.
- **Il modello a clessidra (narrow waist)**: in alto mille applicazioni, in basso mille tecnologie di
  link (Ethernet, Wi-Fi, 4G, fibra), ma **in mezzo un solo IP**. Tutto converge su IP: è ciò che rende
  Internet universale. "IP over everything, everything over IP".
```
   HTTP DNS SMTP SSH ...        ← tante applicazioni
        \  |  /
         TCP  UDP               ← due trasporti
           \ /
            IP                  ← UN SOLO protocollo (la "vita" della clessidra)
           / \
     Ethernet Wi-Fi 4G fibra…   ← tante tecnologie di link
```

## Stratificazione non rigida e confine kernel/user
A differenza dell'OSI, il modello Internet **non impone** una stratificazione stretta: un'applicazione
può **bypassare il trasporto** e parlare direttamente con IP (es. `ping` usa ICMP su IP, senza TCP/UDP).
Un altro confine pratico spesso ignorato è **dove vive ciascun livello**: Applicazione gira in *user
space* (il processo), mentre **Trasporto e Internet li riempie il kernel**. Quando un programma chiama
`send()` su un socket, scrive solo il payload L4: header TCP, header IP e incapsulamento li costruisce il
sistema operativo. Questo confine user→kernel è la *system call* attraversata da [[Socket Programming]].

## Hop-by-hop vs end-to-end (il concetto che confonde tutti)
Mentre il pacchetto attraversa Internet:
- **L4 (TCP/UDP) e l'IP** sono **end-to-end**: gli indirizzi IP sorgente/destinazione **non cambiano**
  lungo il percorso (salvo [[NAT]]); il TCP del mittente dialoga col TCP del destinatario.
- **L2 (il frame Ethernet) è hop-by-hop**: a **ogni router** il frame viene **distrutto e ricostruito**.
  I MAC sorgente/destinazione cambiano a ogni salto (sono sempre quelli del link corrente), il TTL del
  pacchetto IP cala di 1.
```
PC ──frame[MAC_pc→MAC_R1]── R1 ──frame[MAC_R1→MAC_R2]── R2 ──frame[MAC_R2→MAC_srv]── Server
   IP src/dst INVARIATI per tutto il tragitto;  MAC riscritti a ogni hop;  TTL: 64→63→62…
```

## Incapsulamento byte-level
```
[App]   GET / HTTP/1.1 ...                                          → Dati
[L4]    [ TCP: src 51514 | dst 443 | seq | flags ]( Dati )         → Segmento
[L3]    [ IP: src 10.0.0.5 | dst 142.250.x.x | TTL | proto=6 ]( Seg ) → Pacchetto
[L2]    [ Eth: srcMAC | dstMAC | type=0x0800 ]( Pacchetto )[ FCS ] → Frame
[L1]    10101110...                                                → Bit sul mezzo
```
**Campi che si leggono di continuo in [[Wireshark]]** e a cosa servono (demultiplexing — capire cosa c'è sopra):
- **Eth `type`**: `0x0800`=IPv4, `0x0806`=ARP, `0x86DD`=IPv6 → quale L3 segue.
- **IP `protocol`**: `6`=TCP, `17`=UDP, `1`=ICMP → quale L4 segue.
- **Porta di destinazione** (L4): quale processo/applicazione consegnare.
- **TTL**: decrementato a ogni router; di partenza ~64 (Linux) / 128 (Windows) → fingerprinting OS grezzo.
- **MTU 1500**: se il pacchetto IP eccede, si **frammenta**; con flag DF set scatta [[ICMP]]
  "Fragmentation Needed" → base della **Path MTU Discovery**.

## Walkthrough: `https://example.com`
1. **Applicazione**: il browser prepara `GET / HTTP/1.1` dentro [[TLS e SSL|TLS]]; prima risolve il nome via [[DNS]].
2. **Trasporto**: [[TCP]] apre la connessione ([[Three-Way Handshake TCP]]) verso la porta 443, spezza i dati e li numera.
3. **Internet**: [[Indirizzamento IP|IP]] incapsula con src/dst e TTL; ogni router instrada per *longest prefix match*.
4. **Accesso rete**: [[ARP]] risolve il MAC del **gateway**; il frame Ethernet parte. Oltre il router il
   pacchetto IP resta, il frame L2 viene **rifatto a ogni hop**. Sul server tutto risale lo stack.

## Rilevanza per la sicurezza (attacco per livello)
- **Applicazione**: [[SQL Injection]], [[Cross-Site Scripting (XSS)|XSS]], abusi/poisoning [[DNS]].
- **Trasporto**: [[DoS e DDoS|SYN flood]] (abusa del 3-way handshake), port scanning ([[Nmap]]), RST injection.
- **Internet**: **IP spoofing** (falsifica l'IP sorgente — efficace negli attacchi senza handshake, es.
  UDP reflection/amplification), ICMP tunneling, BGP hijacking.
- **Accesso rete**: [[ARP]] poisoning, MAC spoofing → [[Man-in-the-Middle (MITM)]].

Il livello dell'attacco sceglie la difesa: firewall L3/L4 (IP/porta), WAF L7 (HTTP), anti-spoofing/uRPF
in rete, port-security/DAI su L2. Una contromisura al livello sbagliato non serve.

## Troubleshooting per livello (dal basso)
1. **Accesso rete**: link up? MAC del gateway nella cache? `ip link`, `ip neigh`.
2. **Internet**: ho IP e default gateway? Il gateway risponde? `ip addr`, `ip route`, `ping gateway`.
3. **Trasporto**: la porta è raggiungibile? `nc -zv host porta`, `ss -tlnp`.
4. **Applicazione**: il servizio/DNS risponde? `dig`, `curl -v`.

## Domande da esame/colloquio
1. **Quanti livelli ha TCP/IP e come mappano su OSI?** 4: Applicazione (OSI 5-7), Trasporto (4),
   Internet (3), Accesso alla rete (1-2).
2. **Cosa cambia e cosa resta costante lungo il percorso di un pacchetto?** Restano gli IP src/dst (end-
   to-end, salvo NAT); cambiano i MAC a ogni hop e cala il TTL.
3. **Cos'è il "narrow waist" e perché conta?** IP è l'unico protocollo comune tra mille app e mille link:
   garantisce universalità e interoperabilità.
4. **Cos'è l'end-to-end principle?** L'intelligenza (affidabilità, sicurezza) sta agli host, non nella
   rete; i router solo inoltrano. Implica che la fiducia va costruita end-to-end (TLS).
5. **Come fa un host a sapere quale protocollo c'è "sopra"?** Demultiplexing via campi: EtherType (L2),
   IP protocol (L3), porta di destinazione (L4).

## Collegamenti
- [[Modello OSI]] — il riferimento descrittivo a 7 livelli · [[Indirizzamento IP]]
- [[TCP]] · [[UDP]] · [[ICMP]] · [[Three-Way Handshake TCP]]
- [[ARP]] · [[NAT]] — perché gli IP a volte *cambiano* (l'eccezione)
- [[Wireshark]] — vedere l'incapsulamento dal vivo
- [[Socket Programming]] — l'API che attraversa il confine user/kernel (Applicazione ↔ Trasporto)

## Fonti
- RFC 1122 — Requirements for Internet Hosts: <https://www.rfc-editor.org/rfc/rfc1122>
- Cloudflare Learning — TCP/IP: <https://www.cloudflare.com/learning/ddos/glossary/tcp-ip/>
- Saltzer, Reed, Clark — *End-to-End Arguments in System Design* (1984)
- Peterson & Davie — *Computer Networks: A Systems Approach* (cap. "Foundation": hourglass, Internet architecture): <https://book.systemsapproach.org/>
- Beej's Guide to Network Programming — "Low level Nonsense / What is a socket?" (kernel riempie transport+internet): <https://beej.us/guide/bgnet/>
