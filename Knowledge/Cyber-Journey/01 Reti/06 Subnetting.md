---
tipo: concetto
tag: [reti]
fase: 1
fonti: 4
aggiornato: 2026-06-22
stato: maturo
aliases: ["Subnetting"]
---

# Subnetting

## In breve
Il **subnetting** divide una rete IP in **sotto-reti** più piccole spostando il confine tra parte *rete*
e parte *host* dell'indirizzo. Serve a organizzare l'indirizzamento, **ridurre i domini di broadcast**
(meno traffico inutile) e — chiave per la sicurezza — **segmentare** la rete così che un host
compromesso non veda tutto il resto. È l'argomento più "da esercizio" di *Sistemi e Reti*: si impara
solo macinando calcoli.

## Le basi: bit, mask, CIDR
Un IPv4 è **32 bit**. La **subnet mask** dice quanti bit "da sinistra" sono *rete* (gli `1`); i restanti
sono *host* (gli `0`). La notazione **CIDR** `/n` = numero di bit di rete.
```
/24 = 11111111.11111111.11111111.00000000 = 255.255.255.0
            24 bit di rete           8 bit host
```
- **Host utilizzabili** = $2^{(32-n)} - 2$ (si tolgono **network** e **broadcast**).
- **Numero di subnet** ricavabili "prendendo in prestito" *b* bit host = $2^b$.
- Eccezioni: `/31` = 2 host (link punto-punto, RFC 3021, niente network/broadcast), `/32` = 1 host (rotta a host singolo).

## Tabella CIDR di riferimento (ultimo ottetto)
| CIDR | Mask | Blocco | Host utili | Subnet in un /24 | Uso |
|---|---|---|---|---|---|
| /24 | 255.255.255.0 | 256 | 254 | 1 | LAN standard |
| /25 | 255.255.255.128 | 128 | 126 | 2 | mezza LAN |
| /26 | 255.255.255.192 | 64 | 62 | 4 | reparto |
| /27 | 255.255.255.224 | 32 | 30 | 8 | piccolo segmento |
| /28 | 255.255.255.240 | 16 | 14 | 16 | VoIP / IoT |
| /29 | 255.255.255.248 | 8 | 6 | 32 | mini-gruppo |
| /30 | 255.255.255.252 | 4 | 2 | 64 | link router-router |
| /31 | 255.255.255.254 | 2 | 2* | 128 | punto-punto (RFC 3021) |
| /32 | 255.255.255.255 | 1 | 1 | — | host singolo |

I valori di mask possibili in un ottetto sono solo: **0, 128, 192, 224, 240, 248, 252, 254, 255**
(impararli a memoria velocizza tutto).

## Il metodo veloce: il "numero magico"
**Numero magico** = `256 − valore dell'ottetto della mask`. Dà la **dimensione del blocco** e quindi
dove inizia ogni subnet (i confini sono i multipli del blocco).

> [!example] Esercizio 1 — `192.168.1.0/26`
> Mask `/26` → ultimo ottetto della mask = `192`. Magico = `256 − 192 = 64`.
> Le subnet partono ogni 64: **.0**, **.64**, **.128**, **.192**.
> Prendiamo `192.168.1.64/26`:
> - **Network**: 192.168.1.**64**
> - **Primo host**: 192.168.1.65
> - **Ultimo host**: 192.168.1.126
> - **Broadcast**: 192.168.1.127  (= prossima subnet `.128` meno 1)
> - **Host utili**: 62

> [!example] Esercizio 2 — dato un IP, trova la sua subnet: `172.16.20.200/20`
> `/20` → la mask cade nel **3° ottetto**: `255.255.240.0`. Magico = `256 − 240 = 16`.
> I confini nel 3° ottetto vanno di 16: …, 16, 32, **48**, 64… `200` sta… attenzione, qui il `/20`
> agisce sul 3° ottetto: `20` cade nel blocco che parte a **16** (16 ≤ 20 < 32).
> - **Network**: 172.16.**16**.0
> - **Broadcast**: 172.16.**31**.255  (il blocco copre 16.0 → 31.255)
> - **Range host**: 172.16.16.1 → 172.16.31.254  (**4094** host utili = $2^{12}-2$)

### Riconoscere network e broadcast in binario (il metodo "vero")
L'**AND bit-a-bit** tra IP e mask dà il **network address**; mettendo a `1` tutti i bit host si ottiene
il **broadcast**:
```
IP        192.168.1.100 = 11000000.10101000.00000001.01100100
/26 mask  255.255.255.192= 11111111.11111111.11111111.11000000
AND →     192.168.1.64   = 11000000.10101000.00000001.01000000   (network .64)
host=1 →  192.168.1.127  = 11000000.10101000.00000001.01111111   (broadcast .127)
```

## Due domande inverse (l'errore d'esame classico)
Il subnetting si chiede in due modi opposti — **non confonderli**:
1. **"Mi servono N sotto-reti"** → prendi in prestito *b* bit host tali che $2^b \ge N$. Ogni bit preso
   raddoppia le subnet e dimezza gli host.
2. **"Mi servono N host per subnet"** → lascia *h* bit host tali che $2^h - 2 \ge N$. Il resto è rete.

> [!example] Esercizio 3 — "da `192.168.5.0/24`, voglio almeno 6 sotto-reti"
> $2^b \ge 6$ → $b=3$ (8 subnet). Nuova mask = `/24 + 3 = /27`. Magico = `256−224 = 32`.
> Subnet: .0, .32, .64, .96, .128, .160, .192, .224 — ognuna con 30 host utili.

## VLSM (Variable Length Subnet Mask)
Subnet di **dimensioni diverse** per non sprecare indirizzi: assegni la mask in base agli host che
servono, **dal blocco più grande al più piccolo** (altrimenti si creano sovrapposizioni).
```text
Da 192.168.10.0/24, servono:
  Vendite  120 host → /25  (192.168.10.0/25,    .0  –.127)  → 126 host utili
  IT        50 host → /26  (192.168.10.128/26,  .128–.191)  → 62 host utili
  WiFi      20 host → /27  (192.168.10.192/27,  .192–.223)  → 30 host utili
  Link WAN   2 host → /30  (192.168.10.224/30,  .224–.227)  → 2  host utili
                                       (resto .228–.255 libero per espansioni)
```
Regola d'oro VLSM: **prima i fabbisogni grandi**, così i confini dei blocchi grandi non spezzano quelli
piccoli.

## Supernetting / aggregazione di rotte (l'operazione inversa)
Unire più reti contigue in un solo prefisso più corto, per **ridurre le tabelle di routing**:
```
192.168.0.0/24 + 192.168.1.0/24 + 192.168.2.0/24 + 192.168.3.0/24
        →  192.168.0.0/22   (un'unica rotta copre tutte e quattro)
```
È la stessa logica del CIDR ([[Indirizzamento IP]]): un router di confine annuncia `/22` invece di
quattro `/24`.

## Subnet mask vs wildcard mask (trabocchetto Cisco)
Le **ACL Cisco** e OSPF usano la **wildcard mask**, l'inverso bit-a-bit della subnet mask:
```
subnet mask /26 = 255.255.255.192
wildcard        =   0.  0.  0. 63   (255 − ogni ottetto)
```
`0` = "deve combaciare", `1` = "non importa". Confonderle è un errore frequente di configurazione.

## Cenni di subnetting IPv6
In IPv6 non si "risparmiano" indirizzi: si subnetta per **gerarchia**. Standard: l'ISP assegna un `/48`,
si usano i 16 bit successivi come **Subnet ID** → fino a 65.536 subnet **/64** (la /64 è la dimensione
canonica di una LAN IPv6, richiesta da SLAAC). Niente calcolo di host: una /64 ha $2^{64}$ indirizzi.

## Perché conta per la sicurezza
- **Segmentazione**: server/DB in subnet separate, IoT/telecamere isolate, utenti altrove. Un firewall
  tra le subnet limita il [[Lateral Movement]] (un host bucato non "vede" gli altri segmenti).
- In pentest, dal subnet di un host capisci **quanto è grande la rete** e cosa scansionare:
  `nmap -sn 192.168.10.64/26` copre esattamente quel segmento, né più né meno.
- **Microsegmentazione** è un pilastro di [[IAM e Zero Trust|Zero Trust]] ("assume breach": riduci il
  raggio d'azione di una compromissione).

## Errori comuni
- Dimenticare i **2 indirizzi riservati** (network + broadcast) nel conteggio host.
- Confondere subnet mask e **wildcard mask** (ACL).
- Assegnare a un host l'indirizzo di network o di broadcast.
- In VLSM, assegnare i blocchi **dal piccolo al grande** → sovrapposizioni.
- Confondere "N sotto-reti" con "N host" (le due domande inverse).

## Esercizi di autovalutazione (con soluzione)
1. `10.0.0.0/22` → quanti host utili? **Soluzione**: $2^{10}-2 = 1022$.
2. A quale subnet appartiene `192.168.1.200/28`? **Soluzione**: magico `256−240=16` → confini …192, 208;
   `200` ∈ [192,207] → network `192.168.1.192`, broadcast `192.168.1.207`, host .193–.206.
3. Da `172.16.0.0/16` voglio sotto-reti da **500 host** ciascuna: quale mask? **Soluzione**:
   $2^h-2 \ge 500$ → $h=9$ → `/23` (510 host utili).
4. `192.168.4.0/24` in **4** sotto-reti uguali: elencale. **Soluzione**: `/26`, blocco 64 →
   .0/26, .64/26, .128/26, .192/26.

## Domande da esame/colloquio
1. **Formula degli host utili e perché il −2?** $2^{(32-n)}-2$: si escludono network e broadcast.
2. **Cosa cambia prendendo in prestito 1 bit host?** Le sotto-reti raddoppiano, gli host per subnet si
   dimezzano.
3. **Cos'è il VLSM e perché si parte dai fabbisogni grandi?** Mask variabili per evitare sprechi; partire
   dai blocchi grandi evita che spezzino quelli piccoli causando overlap.
4. **A cosa serve un `/30`?** Link punto-punto router-router (2 host utili); `/31` se si applica RFC 3021.
5. **Perché il subnetting aiuta la sicurezza?** Segmenta i domini di broadcast e isola i segmenti: un
   firewall tra subnet contiene il movimento laterale.

## Collegamenti
- [[Indirizzamento IP]] — la base rete+host su cui si fonda il calcolo
- [[NAT]] · [[DHCP]] · [[Modello TCP-IP]]
- [[Lateral Movement]] — la segmentazione lo contiene
- [[IAM e Zero Trust]] — microsegmentazione
- [[Nmap]] — scansionare esattamente un segmento

## Fonti
- Cloudflare — What is subnetting: <https://www.cloudflare.com/learning/network-layer/what-is-a-subnet/>
- RFC 4632 — CIDR: <https://www.rfc-editor.org/rfc/rfc4632>
- RFC 3021 — /31 su link punto-punto: <https://www.rfc-editor.org/rfc/rfc3021>
- subnetting practice: <https://subnetipv4.com/>
