---
tipo: concetto
tag: [reti]
fase: 1
fonti: 4
aggiornato: 2026-06-22
stato: maturo
aliases: ["Indirizzamento IP", "IP"]
---

# Indirizzamento IP

## In breve
Un indirizzo **IP** identifica un'interfaccia di rete a **livello 3** ([[Modello OSI|OSI]] /
[[Modello TCP-IP|Internet]]): dice ai pacchetti *dove andare* e *da dove vengono*. A differenza del
[[MAC Address]] (fisico, locale, immutabile), l'IP è **logico, gerarchico e instradabile**: la struttura
*rete + host* è ciò che rende possibile il routing su scala mondiale. Senza gerarchia, un router
dovrebbe conoscere ogni singolo host del pianeta; con la gerarchia ne basta conoscere le *reti*.

## Binario e decimale: la base che serve davvero
Un IPv4 è **32 bit** in 4 **ottetti** (8 bit ciascuno), scritti in decimale puntato: `192.168.1.10`.
Ogni ottetto va da `0` a `255` (=$2^8-1$). I valori dei bit in un ottetto:
```
bit:    128  64  32  16   8   4   2   1
        ─────────────────────────────────
192 =    1   1   0   0    0   0   0   0    (128+64)
168 =    1   0   1   0    1   0   0   0    (128+32+8)
  1 =    0   0   0   0    0   0   0   1
 10 =    0   0   0   0    1   0   1   0    (8+2)
```
Saper convertire a mano dec↔bin è il prerequisito per [[Subnetting|subnetting]] e per leggere le mask.
**Trucco**: per convertire un decimale, sottrai da sinistra i valori (128, 64, 32...) finché puoi.

## Struttura: rete + host
La **subnet mask** (o il suffisso CIDR `/n`) separa la parte **rete** (a sinistra) dalla parte **host**
(a destra). Esempio `192.168.1.10/24`: i primi 24 bit = rete `192.168.1.0`, gli ultimi 8 = host. Il
**network address** si ottiene con l'**AND bit-a-bit** tra IP e mask; il dettaglio del calcolo è in
[[Subnetting]].

L'instradamento usa questa gerarchia: il router confronta l'IP destinazione con la sua tabella e sceglie
la rotta **più specifica** (*longest prefix match*). Se la destinazione è nella **stessa rete**
dell'host, la consegna è **diretta** (risolve il MAC via [[ARP]] e invia il frame); altrimenti il
pacchetto va al **default gateway**, che lo inoltra verso la rete successiva.

> [!example] Decisione "stessa rete o gateway?"
> Host `192.168.1.10/24` vuole raggiungere `192.168.1.50`. AND di entrambi con `/24` →
> `192.168.1.0` = `192.168.1.0`: **stessa rete** → consegna diretta via ARP.
> Stesso host verso `8.8.8.8`: AND → reti diverse → manda al **gateway** `192.168.1.1`.

## Classi (storia) e perché è arrivato il CIDR
In origine gli IP erano divisi in **classi** rigide:

| Classe | 1° ottetto | Mask di default | Uso |
|---|---|---|---|
| A | 1–126 | /8 (255.0.0.0) | reti enormi (16M host) |
| B | 128–191 | /16 (255.255.0.0) | reti medie (65k host) |
| C | 192–223 | /24 (255.255.255.0) | reti piccole (254 host) |
| D | 224–239 | — | multicast |
| E | 240–255 | — | riservata/sperimentale |

Problema: una classe B (65k host) era troppa per chi ne aveva 1000, una C (254) troppo poca → **spreco**
e tabelle di routing gonfie. Dal 1993 il **CIDR** (Classless Inter-Domain Routing, RFC 4632) abolisce le
classi: la mask può essere *qualsiasi* `/n`, si fa **VLSM** e **route aggregation**. Oggi "classe C"
significa solo, informalmente, "/24".

## Range speciali (da riconoscere a colpo d'occhio)
| Tipo | Range | Uso |
|---|---|---|
| Privati (RFC 1918) | `10.0.0.0/8` · `172.16.0.0/12` · `192.168.0.0/16` | LAN, non instradabili su Internet (servono [[NAT]]) |
| Loopback | `127.0.0.0/8` (`127.0.0.1`) | l'host parla con sé stesso |
| Link-local / APIPA | `169.254.0.0/16` | auto-assegnato se il [[DHCP]] fallisce → **sintomo di guasto** |
| CGNAT | `100.64.0.0/10` | NAT degli ISP (RFC 6598) |
| Broadcast | `255.255.255.255` / ultimo IP della subnet | invio a tutta la LAN |
| Multicast | `224.0.0.0/4` | gruppi (OSPF, mDNS, streaming) |
| Documentazione | `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` | esempi (non in prod) |

## Anatomia del pacchetto IPv4 (header, 20 byte)
I campi che contano per sicurezza e diagnosi:
- **TTL** (Time To Live): cala di 1 a ogni router; a 0 il pacchetto muore (ICMP "Time Exceeded"). Base di
  `traceroute` e indizio dell'OS sorgente (Linux parte da 64, Windows da 128).
- **Protocol**: cosa c'è sopra (6=TCP, 17=UDP, 1=ICMP).
- **Source / Destination IP**: 32 bit ciascuno. La sorgente è **falsificabile** → IP spoofing.
- **Flags / Fragment Offset**: gestione della frammentazione (MTU).
- **Header Checksum**: integrità del solo header.

## Assegnazione: statica vs dinamica
- **Statica**: configurata a mano — server, gateway, stampanti (devono avere IP stabile).
- **Dinamica**: assegnata dal [[DHCP]] al boot (client, ospiti). Il binding `MAC→IP` nei log DHCP è oro
  per la forensica (associa un'attività a un dispositivo).

## IPv6 (l'essenziale, ma per davvero)
128 bit (≈3,4×10³⁸ indirizzi), 8 gruppi esadecimali da 16 bit:
`2001:0db8:85a3:0000:0000:8a2e:0370:7334`. Regole di compressione: gli zeri iniziali di un gruppo si
omettono, e **una** sequenza di gruppi tutti-zero si comprime con `::` →
`2001:db8:85a3::8a2e:370:7334`. Niente più scarsità → **niente NAT obbligatorio**.

Tipi di indirizzo chiave:
- **Link-local** `fe80::/10` — sempre presente su ogni interfaccia, valido **solo sulla LAN** (usato da
  ND, il "ARP di IPv6").
- **Global unicast** `2000::/3` — instradabile su Internet (l'equivalente del pubblico).
- **ULA** `fc00::/7` — privati (l'equivalente di RFC 1918).
- **Multicast** `ff00::/8` (IPv6 non ha broadcast: usa multicast, es. `ff02::1` = tutti i nodi).

**SLAAC + EUI-64**: un host può auto-configurarsi l'IPv6 dal prefisso annunciato dal router (RA) +
l'identificativo derivato dal MAC. In pentest IPv6 è spesso **abilitato ma non monitorato** → vettore
[[Man-in-the-Middle (MITM)|MITM]]: *mitm6* avvelena via DHCPv6/RA e dirotta il traffico.

## Esempio pratico
```bash
# IP, gateway, interfacce
ip addr            # Linux (anche: ip -br addr per vista compatta)
ipconfig /all      # Windows
# IP pubblico visto da Internet (post-NAT)
curl ifconfig.me
# Tabella di routing (dove va il default)
ip route           # default via 192.168.1.1 dev eth0
# Vicinato L2 (cache ARP/ND: chi è nella mia rete)
ip neigh
```

## Rilevanza per la sicurezza
- **IP spoofing**: falsificare l'IP sorgente per nascondersi o per attacchi **reflection/amplification**
  (UDP, dove non c'è handshake che verifichi la sorgente — vedi [[DoS e DDoS]]). Difesa: filtraggio
  anti-spoofing / uRPF (BCP 38).
- **Scanning**: il primo passo offensivo è scoprire host vivi e servizi su un range —
  `nmap -sn 10.0.0.0/24` (host discovery), poi port scan. Vedi [[Ricognizione (Recon)]] e [[Nmap]].
- **Privati ≠ sicuri**: irraggiungibili dall'esterno grazie al [[NAT]], ma pienamente esposti
  **dall'interno** (post-compromissione) → conta la segmentazione ([[Subnetting]], [[Lateral Movement]]).
- **TTL fingerprinting**: il TTL di ritorno suggerisce l'OS (64=Linux, 128=Windows, 255=rete/Cisco).
- **Geolocalizzazione/attribuzione**: l'IP pubblico rivela ISP e zona; le [[VPN]] lo mascherano.

## Errori comuni
- Confondere **IP pubblico** (ciò che Internet vede, post-NAT) e **IP privato** dell'interfaccia.
- Assegnare a un host l'indirizzo di **network** o di **broadcast** della subnet (non validi per host).
- Vedere un `169.254.x.x` e non capire che è **APIPA** = il DHCP non ha risposto (guasto di rete).
- Dimenticare che IPv6 può essere attivo e instradare *anche se* hai configurato solo IPv4.

## Domande da esame/colloquio
1. **Quanti bit ha un IPv4 e com'è strutturato?** 32 bit, 4 ottetti da 8 bit; parte rete + parte host
   separate dalla subnet mask.
2. **Come decide un host se la destinazione è locale o va al gateway?** Fa l'AND tra il proprio IP e la
   mask e tra l'IP destinazione e la mask: se i network coincidono è locale (ARP), altrimenti gateway.
3. **Perché è nato il CIDR?** Le classi sprecavano indirizzi e gonfiavano le tabelle di routing; il CIDR
   permette mask arbitrarie, VLSM e aggregazione delle rotte.
4. **Differenza tra IP e MAC?** L'IP è logico/gerarchico/instradabile (L3, può cambiare); il MAC è
   fisico/locale/fisso (L2, identifica la scheda nella LAN).
5. **Cosa indica un indirizzo `169.254.x.x`?** APIPA/link-local: il client non ha ottenuto un IP dal
   DHCP → problema di rete o di server DHCP.

## Collegamenti
- [[Modello TCP-IP]] · [[Modello OSI]] — l'IP è il livello 3
- [[Subnetting]] — il calcolo di rete/host/broadcast · [[NAT]] · [[DHCP]]
- [[ARP]] — risoluzione IP→MAC in LAN · [[MAC Address]]
- [[VPN]] · [[Ricognizione (Recon)]] · [[Nmap]] · [[DoS e DDoS]]

## Fonti
- RFC 791 — Internet Protocol: <https://www.rfc-editor.org/rfc/rfc791>
- RFC 1918 — Private Internets: <https://www.rfc-editor.org/rfc/rfc1918>
- RFC 4632 — CIDR: <https://www.rfc-editor.org/rfc/rfc4632>
- BCP 38 (RFC 2827) — Ingress Filtering: <https://www.rfc-editor.org/rfc/rfc2827>
