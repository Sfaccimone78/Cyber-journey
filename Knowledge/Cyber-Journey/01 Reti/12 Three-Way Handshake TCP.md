---
tipo: concetto
tag: [reti]
fase: 1
fonti: 3
aggiornato: 2026-06-22
stato: maturo
aliases: ["Three-Way Handshake TCP"]
---

# Three-Way Handshake TCP

## In breve
Il **three-way handshake** è la procedura con cui due host stabiliscono una connessione [[TCP]] affidabile **prima** di scambiare dati. Serve a tre cose: (1) sincronizzare i **numeri di sequenza iniziali (ISN)** in entrambe le direzioni, (2) confermare che ciascun lato può **inviare e ricevere**, (3) negoziare opzioni (MSS, window scaling, SACK). Tre passi: **SYN → SYN-ACK → ACK**.

> **Perché tre e non due?** Due passi (SYN + ACK) non permetterebbero al client di confermare di aver ricevuto l'ISN del server — la connessione sarebbe semi-bidirezionale. Il terzo passo (ACK del client) chiude il loop e sincronizza entrambe le direzioni.

---

## I tre passi — meccanismo a basso livello

```
Client                                  Server
  |                                        |
  |--- [SYN] seq=ISN_c ------------------>|   Passo 1: SYN
  |    (ISN_c = numero random, es. 100)   |   "Voglio aprire una connessione,
  |                                        |    il mio ISN è 100"
  |                                        |
  |<-- [SYN-ACK] seq=ISN_s, ack=ISN_c+1 -|   Passo 2: SYN-ACK
  |    (ISN_s = numero random, es. 200)   |   "Ok, il tuo 100 ricevuto (attendo 101),
  |    (ack=101: ISN_c + 1)               |    il mio ISN è 200"
  |                                        |
  |--- [ACK] seq=ISN_c+1, ack=ISN_s+1 -->|   Passo 3: ACK
  |    (seq=101, ack=201)                 |   "Il tuo 200 ricevuto (attendo 201)"
  |                                        |
  |========= ESTABLISHED ================|
  |    Ora i dati possono fluire           |
```

**Regola ack**: `ack = seq_ricevuto + 1`. Il SYN "consuma" un numero di sequenza anche se non porta payload dati. Da qui in poi, seq e ack numerano i **byte reali** di payload.

### Cosa trasporta il SYN (opzioni TCP)
Il pacchetto SYN non è "vuoto" — nel campo **Options** (fino a 40 byte) negozia:

| Opzione | Descrizione |
|---|---|
| **MSS** (Maximum Segment Size) | Dimensione massima del payload TCP che il lato può ricevere. Tipicamente 1460 byte (MTU 1500 - 20 IP - 20 TCP). |
| **Window Scale** | Moltiplica la receive window (per supportare BDP alti su link veloci). |
| **SACK Permitted** | Abilita Selective ACK — il ricevitore conferma range specifici, non solo il blocco iniziale. |
| **Timestamps** | Per calcolo RTT preciso e protezione da wrapped seq numbers (PAWS). |
| **NOP** | Padding per allineare le opzioni a 32 bit. |

---

## ISN randomizzati — perché e come

Se l'ISN fosse prevedibile (es. sempre 0 o incrementato linearmente), un attaccante **off-path** (che non vede il traffico) potrebbe:
1. Indovinare i numeri seq/ack correnti di una sessione TCP attiva.
2. Iniettare segmenti spoofati con i numeri giusti → **session hijacking** o **RST injection**.

Caso storico: il **Mitnick attack** (1994) sfruttava ISN prevedibili per iniettare comandi in una sessione rsh privilegiata.

**Soluzione**: RFC 6528 prescrive ISN randomizzati usando un hash `F(src_ip, src_port, dst_ip, dst_port, secret)` — il secret cambia ogni pochi minuti. Linux, Windows e BSD moderni implementano questo.

> [!info] Off-path vs on-path
> ISN randomizzati proteggono solo da attaccanti **off-path** (non vedono il traffico). Un attaccante **on-path** (MITM, sniffing) vede seq/ack in chiaro → può comunque fare hijacking. La vera difesa è la cifratura ([[Wireshark]] vede anche questo).

---

## Stati della connessione TCP

```
CLOSED → LISTEN (server aspetta)
Client manda SYN → client: SYN-SENT, server: SYN-RECEIVED
Server manda SYN-ACK, client manda ACK → entrambi: ESTABLISHED
---
Chiusura normale (4-way):
  Lato A: FIN-WAIT-1 → FIN-WAIT-2 → TIME-WAIT → CLOSED
  Lato B: CLOSE-WAIT → LAST-ACK → CLOSED
```

**TIME_WAIT**: chi inizia la chiusura rimane in TIME_WAIT per **2×MSL** (Maximum Segment Lifetime, tipicamente 60-120 secondi). Scopo: assorbire segmenti ritardatari della sessione appena chiusa che potrebbero confondersi con una nuova connessione sulla stessa tupla.

```bash
# Vedere tutti gli stati TCP sul sistema
ss -tan
ss -tan state syn-recv         # half-open → sospetto SYN flood
ss -tan state time-wait        # connessioni in chiusura
ss -tan state established      # connessioni attive
netstat -ano                   # Windows
```

---

## Walkthrough: handshake completo con tcpdump/Wireshark

```bash
# Cattura il three-way handshake verso google.com:80
sudo tcpdump -i eth0 host google.com and port 80 -n

# Output tipico (3 righe = handshake):
# 10:00:01.000 IP 192.168.1.5.54321 > 142.250.x.x.80: Flags [S],  seq 12345, win 64240, options [mss 1460,...]
# 10:00:01.012 IP 142.250.x.x.80 > 192.168.1.5.54321: Flags [S.], seq 67890, ack 12346, win 65535, options [mss 1380,...]
# 10:00:01.012 IP 192.168.1.5.54321 > 142.250.x.x.80: Flags [.],  ack 67891, win 502
```

**Flag TCP nella notazione tcpdump:**
- `[S]` = SYN
- `[S.]` = SYN-ACK (il `.` è ACK)
- `[.]` = ACK puro
- `[F.]` = FIN-ACK (chiusura)
- `[R]` = RST (reset/rifiuto)
- `[P.]` = PSH-ACK (dati)

**Wireshark:**
```
tcp.flags.syn == 1 && tcp.flags.ack == 0    # solo SYN (nuove connessioni)
tcp.flags.syn == 1 && tcp.flags.ack == 1    # solo SYN-ACK (risposta server)
tcp.flags.reset == 1                         # RST (connessioni rifiutate/resettate)
tcp.flags.fin == 1                           # FIN (chiusura pulita)
```

---

## Half-open connection e coda del kernel

Quando il server riceve un SYN, crea una struttura in memoria e la mette nella **SYN queue** (backlog parziale) — è la connessione **half-open**. Quando arriva l'ACK finale, passa nella **accept queue** (backlog completo) dove l'applicazione può chiamare `accept()`.

```
SYN ricevuto → entra in SYN queue (half-open, memoria allocata, attende ACK)
ACK ricevuto → passa ad accept queue (ESTABLISHED, pronto per accept())
Application chiama accept() → connessione consegnata all'applicazione
```

La dimensione della SYN queue è controllata da:
```bash
sysctl net.ipv4.tcp_max_syn_backlog   # default ~1024-2048; aumentare sotto load
```

---

## Sicurezza — attacchi sul handshake

### 1. SYN Scan (Nmap `-sS`) — half-open scan
[[Nmap]] invia SYN e **non completa** l'handshake:
- Server risponde **SYN-ACK** → porta **aperta** (Nmap manda RST immediato, non entra in accept queue).
- Server risponde **RST** → porta **chiusa**.
- Nessuna risposta o [[ICMP]] Unreachable → porta **filtrata**.

Vantaggio stealth: non arriva mai alla accept queue dell'applicazione → spesso non loggato a livello applicativo. Richiede raw socket (root). Vedi [[Nmap]].

### 2. SYN Flood — DoS via half-open exhaustion
L'attaccante invia milioni di SYN **spoofati** (IP sorgente falso) → il server crea entry half-open per ciascuno, non riceve mai l'ACK (la risposta va all'IP falso), la SYN queue si riempie → le connessioni legittime vengono rifiutate con RST.

```
Attaccante (spoofa IP) → Server: SYN (da 1.2.3.4, spoofato)
Server → 1.2.3.4: SYN-ACK  (non arriva mai all'attaccante reale)
Server aspetta ACK per ~75 secondi → SYN queue piena → DROPS legittime
```

**Difesa principale: SYN cookies** (RFC 4987)
Il server **non alloca memoria** sul SYN: invece codifica lo stato nella *Sequence Number* del SYN-ACK:
```
ISN_server = hash(src_ip, src_port, dst_ip, dst_port, timestamp, segreto)
```
Quando (se) arriva l'ACK con `ack = ISN_server + 1`, il server ricalcola l'hash e **verifica**: se corrisponde, ricostruisce la connessione senza aver mai allocato memoria per la half-open.

```bash
# Verificare se SYN cookies è attivo (Linux)
sysctl net.ipv4.tcp_syncookies    # 1 = attivo, 0 = disattivato
# Attivare:
sysctl -w net.ipv4.tcp_syncookies=1
```

**Limite di SYN cookies**: alcune opzioni TCP (SACK, Window Scale, Timestamps) non possono essere negoziate perché il server non alloca lo spazio per ricordarle. Le connessioni legittime funzionano ma con prestazioni ridotte. Soluzione moderna: SYN cookies + aumento del backlog + rate limiting via firewall.

### 3. RST Injection (TCP Reset Attack)
Un attaccante **on-path** o con capacità di sniffing forgia un segmento RST con i seq/ack corretti → **tronca la sessione**. Usato da censori di rete (Great Firewall) per interrompere connessioni verso certi siti.

```bash
# hping3 per iniettare un RST (test autorizzato)
hping3 --rst -p 80 --spoof <victim_ip> --ttl 64 target_ip
```

**Difesa**: [[Wireshark]] rivela RST anomali (RST da IP inaspettati o con seq sbagliato); la cifratura del payload non difende dal RST injection perché il RST non ha payload.

### 4. Session Hijacking
Un attaccante che conosce i numeri seq/ack correnti (via sniffing) può iniettare payload falsificando l'IP di uno dei due endpoint. **Difesa reale**: cifratura a livello applicativo — SSH, TLS rendono il payload incomprensibile anche se i numeri di sequenza sono noti.

---

## Relazione con Nmap — tabella completa scan/handshake

| Scan Nmap | Interazione con handshake | Stato rilevato |
|---|---|---|
| `-sS` SYN | Invia SYN, mai ACK → **half-open** | SYN-ACK=aperta, RST=chiusa |
| `-sT` Connect | Completa tutto il handshake via `connect()` | Handshake OK=aperta, RST=chiusa |
| `-sA` ACK | Invia ACK diretto (nessun SYN) — fuori handshake | RST=unfiltered, silenzio=filtered |
| `-sF` FIN | Invia FIN senza handshake precedente | Silenzio=aperta (RFC), RST=chiusa |
| `-sN` NULL | Nessuna flag | Silenzio=aperta (RFC), RST=chiusa |
| `-sX` Xmas | FIN+PSH+URG | Silenzio=aperta (RFC), RST=chiusa |

---

## Caso limite: TIME_WAIT e port reuse

Se la stessa tupla (src_ip:src_port, dst_ip:dst_port) viene riutilizzata mentre la vecchia connessione è ancora in TIME_WAIT, il kernel rifiuta il SYN. Soluzione: `SO_REUSEADDR` (per server) o attendere la scadenza di TIME_WAIT. Su Linux, `tcp_tw_reuse=1` permette al client di riutilizzare porte in TIME_WAIT se il timestamp TCP è avanzato.

```bash
sysctl net.ipv4.tcp_tw_reuse     # 0 = no reuse, 1 = permetti (client)
```

---

## Troubleshooting

| Sintomo | Causa probabile | Diagnosi |
|---|---|---|
| Connessione si blocca al SYN | Firewall droppano SYN in entrata | `tcpdump`: vedi SYN uscire ma non torna SYN-ACK |
| RST immediato dopo SYN | Porta chiusa o servizio non in ascolto | `ss -tlnp` sul server: il servizio c'è? |
| Connessione lenta all'apertura | SYN-ACK perso, ritrasmissione (1-3s timeout) | `tcpdump`: vedi SYN ritrasmesso dopo ~1s |
| `ss -tan state syn-recv` pieno | SYN flood in corso | Attiva SYN cookies, rate limit via `iptables` |
| TIME_WAIT eccessivi | Molte connessioni chiuse rapidamente | Normale; riduce con `tcp_tw_reuse` o keepalive |

---

## Domande da esame/colloquio

1. **Perché il three-way handshake usa tre passi e non due?** Due passi (SYN + ACK) sincronizzano solo l'ISN del client verso il server. Il terzo passo (ACK del client) è necessario per confermare che il client ha ricevuto l'ISN del server — solo così entrambe le direzioni sono sincronizzate e la connessione è veramente bidirezionale.

2. **Cos'è un ISN e perché deve essere randomizzato?** Initial Sequence Number: il numero di sequenza iniziale di una connessione TCP. Se fosse prevedibile, un attaccante off-path potrebbe indovinarlo e iniettare segmenti spoofati nella sessione (come nel Mitnick attack del 1994). RFC 6528 prescrive randomizzazione tramite hash con segreto.

3. **Come funziona il SYN flood e come lo mitigano i SYN cookies?** Il SYN flood riempie la SYN queue con half-open connections spoofate, esaurendo la memoria del kernel. I SYN cookies eliminano la SYN queue: il server codifica lo stato nell'ISN del SYN-ACK e lo ricostruisce solo quando arriva l'ACK valido — nessuna memoria allocata per le half-open.

4. **Qual è la differenza tra `-sS` e `-sT` in Nmap in relazione al handshake?** `-sS` invia SYN e manda RST al SYN-ACK senza completare l'handshake (half-open) — più stealth, richiede root. `-sT` usa la syscall `connect()` che completa il handshake intero — nessun privilegio root necessario, ma l'applicazione server lo registra nei log.

5. **Cos'è TIME_WAIT e perché esiste?** È lo stato in cui rimane chi inizia la chiusura TCP per 2×MSL dopo aver mandato l'ACK finale. Scopo: assorbire segmenti ritardatari della sessione appena chiusa che potrebbero confondersi con una nuova connessione sulla stessa tupla (src_ip:port, dst_ip:port).

---

## Attacco vs Difesa — tabella sinottica

| Attacco | Meccanismo | Difesa |
|---|---|---|
| SYN scan (Nmap -sS) | Half-open: rileva porte senza completare handshake | Log a livello firewall/IDS (non applicativo); rate limiting SYN |
| SYN flood | Milioni di SYN spoofati → esaurisce SYN queue | SYN cookies, backlog aumentato, rate limiting, scrubbing |
| RST injection | Forgiare RST con seq corretti → tronca sessione | Rilevabile con Wireshark; cifratura non difende da RST |
| Session hijacking | Sniffing seq/ack → inject payload | Cifratura (SSH, TLS) — l'unica vera difesa |
| ISN prediction | ISN prevedibile → spoof off-path | ISN randomizzati (RFC 6528) — già implementato negli OS moderni |

---

## Collegamen ti
- [[TCP]] — header completo, gestione seq/ack, stati, controllo di flusso
- [[UDP]] — trasporto senza handshake a confronto
- [[ICMP]] — risposte di errore che interferiscono con TCP (Unreachable, Time Exceeded)
- [[DoS e DDoS]] — SYN flood come attacco DoS classico
- [[Nmap]] — SYN scan (`-sS`) e tutti gli altri scan type che interagiscono con il handshake
- [[Porte e Protocolli Comuni]] — le porte su cui avvengono le connessioni TCP
- [[Wireshark]] — catturare e analizzare il three-way handshake a livello pacchetto
- [[Man-in-the-Middle (MITM)]] — on-path → session hijacking e RST injection
- [[Scansione delle Porte]] — contesto pentest del SYN scan

## Fonti
- RFC 9293 — Transmission Control Protocol (aggiornamento definitivo): https://datatracker.ietf.org/doc/html/rfc9293
- RFC 6528 — Defending against Sequence Number Attacks: https://www.rfc-editor.org/rfc/rfc6528
- RFC 4987 — TCP SYN Flooding Attacks and Common Mitigations: https://datatracker.ietf.org/doc/html/rfc4987
- Cloudflare — SYN flood attack: https://www.cloudflare.com/learning/ddos/syn-flood-ddos-attack/
