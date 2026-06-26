---
tipo: concetto
tag: [reti]
fase: 2
fonti: 3
aggiornato: 2026-06-22
stato: maturo
aliases: ["DoS e DDoS", "DDoS", "DoS", "SYN Flood"]
---

# DoS e DDoS

> **Nota etica**: lanciare attacchi DoS/DDoS contro sistemi altrui è reato (art. 635-bis c.p.
> in Italia, Computer Fraud and Abuse Act negli USA). Comandi e tecniche sono riportati a scopo
> difensivo / lab autorizzato.
> MITRE ATT&CK: **T1498** (Network Denial of Service) · **T1499** (Endpoint Denial of Service).

## In breve
Un attacco **DoS** (Denial of Service) mira a rendere **indisponibile** un servizio esaurendone le
risorse (banda, CPU, memoria, connessioni). Il **DDoS** (Distributed DoS) usa molte sorgenti
contemporaneamente — tipicamente una **botnet** — rendendo il filtraggio per IP sorgente
inutile. Colpisce la **Disponibilità** della [[Triade CIA]].

---

## Tassonomia degli attacchi

```
DoS / DDoS
├── Volumetrici (L3/L4)        → saturare la banda
│   ├── UDP flood
│   ├── ICMP flood (ping flood)
│   └── Amplification / Reflection
│       ├── DNS amplification
│       ├── NTP amplification
│       ├── memcached amplification
│       └── SSDP / CLDAP
├── Protocollari (L3/L4)       → esaurire risorse di stato
│   ├── SYN Flood
│   ├── ACK Flood
│   ├── RST Flood
│   └── Fragmentation attack (Teardrop, Ping of Death)
└── Applicativi (L7)           → poche richieste costose
    ├── HTTP flood (GET / POST)
    ├── Slowloris (connessioni lente)
    ├── RUDY (R-U-Dead-Yet, POST lento)
    └── DNS query flood
```

---

## Categorie in dettaglio

### 1. Attacchi Volumetrici
Obiettivo: **saturare la banda** tra la vittima e il proprio upstream provider. Si misurano in
Gbps o Mpps (milioni di pacchetti al secondo). La vittima è irraggiungibile perché il "tubo"
di connettività è pieno prima ancora di arrivare al datacenter.

Tecniche principali:
- **UDP flood**: pacchetti UDP a destinazione casuale; il server risponde con ICMP "port unreachable"
  o scarta, consumando risorse.
- **ICMP flood**: `ping` a raffica con payload di grandi dimensioni.
- **Amplification/Reflection** (vedi sezione dedicata).

### 2. Attacchi Protocollari (State Exhaustion)
Obiettivo: riempire le **tabelle di stato** di firewall, load balancer o server.

#### SYN Flood
Sfrutta il [[Three-Way Handshake TCP]]:

```
Attaccante → SYN (IP spoofato)  → Server
Server     → SYN-ACK            → (IP inesistente, no risposta)
Server     → aspetta ACK per 75 s (MSL×2) → slot half-open occupato
```

Ripetuto a migliaia al secondo, riempie la coda di connessioni half-open (**SYN backlog**).
Il server smette di accettare connessioni legittime.

Rilevamento: `ss -tan state syn-recv | wc -l` mostra migliaia di connessioni in `SYN-RECV`.

#### ACK / RST Flood
Invio massiccio di segmenti [[TCP]] con flag ACK o RST spoofati. Il server deve ispezionare
ogni pacchetto per capire se appartiene a una sessione nota, saturando la CPU del firewall stateful.

#### Fragmentazione (Teardrop, Ping of Death)
Pacchetti IP frammentati con offset sovrapposti o dimensioni illegali che causavano crash nei
sistemi operativi vulnerabili (storicamente); oggi perlopiù mitigati.

### 3. Attacchi Applicativi (L7)
Difficili da filtrare perché il traffico sembra **legittimo** a livello di rete/trasporto.

#### HTTP Flood
Migliaia di richieste GET o POST a endpoint costosi (ricerche, login, generazione PDF). Ogni
richiesta è sintatticamente corretta; WAF e CDN devono distinguere bot da utenti reali tramite
challenge JS, CAPTCHA, reputazione IP.

#### Slowloris
Apre molte connessioni HTTP al server e invia header **incompleti** molto lentamente (un byte
ogni 15 secondi), mantenendo i thread/worker del server occupati senza mai completare la richiesta.
Apache (con mpm_prefork) è particolarmente vulnerabile; nginx (event-driven) regge meglio.

```bash
# Esempio in lab con slowhttptest
slowhttptest -c 1000 -H -i 10 -r 200 -t GET -u http://target-lab/ -x 24 -p 3
```

#### RUDY (R-U-Dead-Yet)
Simile a Slowloris ma per POST: invia header `Content-Length` grande, poi trasmette il body
un byte per volta. Il server tiene la connessione aperta in attesa del body completo.

---

## Reflection & Amplification — il motore dei mega-DDoS

L'attaccante **spoofa l'IP della vittima** come sorgente e invia piccole richieste a server
pubblici (open resolver, server NTP, ecc.). Le risposte — molto più grandi — convergono sulla
vittima. Non serve una botnet enorme: basta il **fattore di amplificazione (AF)**.

| Servizio | Porta ([[UDP]]) | Richiesta | Risposta | AF (fattore ~) |
|---|---|---|---|---|
| DNS (query ANY) | 53 | ~40 B | 2–4 KB | 28–54× |
| NTP (monlist) | 123 | ~8 B | 4.5 KB | ~556× |
| memcached | 11211 | ~15 B | fino 1 MB | **~50.000×** |
| SSDP | 1900 | ~30 B | 250 B | ~30× |
| CLDAP | 389 | ~50 B | 1–4 KB | 50–70× |

Il record storico (2018): **Akamai registra 1,3 Tbps** tramite memcached reflection, poi superato
da GitHub nel 2018 con 1,35 Tbps.

**Condizione necessaria**: IP spoofing consentito a monte.
**Difesa strutturale**: **BCP 38** (Network Ingress Filtering, RFC 2827) — gli ISP non devono
accettare pacchetti con IP sorgente non appartenenti al loro blocco assegnato. Implementazione
ancora parziale a livello globale.

---

## Botnet — infrastruttura del DDoS moderno

Una **botnet** è una rete di dispositivi compromessi (**bot/zombie**) controllati da un C2
(Command & Control). Nei DDoS:
- I bot ricevono il bersaglio e il tipo di attacco.
- Lanciano il flood contemporaneamente; le sorgenti sono distribuite globalmente.
- Filtrare per IP è impossibile (migliaia di sorgenti diverse).

Le botnet IoT (Mirai, 2016) hanno rivoluzionato il settore: router, telecamere IP e DVR con
credenziali default forman cluster da centinaia di migliaia di nodi. Mirai ha raggiunto
**620 Gbps** contro KrebsOnSecurity.

---

## Walkthrough difensivo in lab

> Ambiente: due VM Linux sulla stessa rete isolata. Nessuna infrastruttura esterna coinvolta.

```bash
# === LATO ATTACCANTE (lab isolato) ===

# SYN flood con hping3 (IP spoofati, porta 80)
sudo hping3 -S --flood -V -p 80 --rand-source 192.168.1.100

# UDP flood
sudo hping3 --udp -p 53 --flood 192.168.1.100

# ICMP flood
sudo hping3 --icmp --flood 192.168.1.100

# === LATO VITTIMA / BLUE TEAM ===

# Conta connessioni SYN-RECV (segnale SYN flood)
ss -tan state syn-recv | wc -l

# Visualizza le top sorgenti per numero di connessioni
ss -tan | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -20

# Abilita SYN cookies (mitigazione kernel)
echo 1 | sudo tee /proc/sys/net/ipv4/tcp_syncookies

# Rate limiting SYN con iptables
sudo iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j ACCEPT
sudo iptables -A INPUT -p tcp --syn -j DROP

# Monitoraggio banda in tempo reale
sudo iftop -i eth0
# oppure
sudo nload eth0

# Analisi del traffico con tcpdump (campione)
sudo tcpdump -i eth0 -nn -c 1000 'tcp[tcpflags] & tcp-syn != 0' | \
  awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head
```

---

## Detection (lato Blue Team)

| Indicatore | Come rilevarlo | Tool |
|---|---|---|
| Picco di SYN senza ACK | `ss -tan state syn-recv`, contatore netstat | OS / [[SIEM]] |
| Molte connessioni da un IP | Flow analysis, top talker | NetFlow / sFlow |
| Banda in ingresso anomala | Spike nei grafici di traffico | SNMP, Prometheus |
| HTTP 5xx / timeout / latenza alta | APM, log web server | ELK, Splunk |
| Picchi volumetrici | BGP flowspec, grafici ISP upstream | NOC |
| Sorgenti sparse (botnet) | Geo-distribution delle sorgenti anomala | [[SIEM]] |

Correlazioni utili nel [[SIEM]]:
- `SYN_count > 10000/min AND ACK_ratio < 0.1` → probabile SYN flood.
- `unique_src_IPs > 5000 in 60s AND dst_port == 80` → HTTP flood da botnet.

---

## Mitigazione e difesa

### Layer rete / OS
- **SYN cookies** (`net.ipv4.tcp_syncookies=1`): il server non alloca slot finché non riceve l'ACK;
  elimina il problema del SYN backlog senza bloccare connessioni legittime.
- **Rate limiting** con iptables/nftables/firewall hardware: limita pacchetti/s per sorgente.
- **BCP 38** e anti-spoofing sull'uplink ISP: previene reflection & amplification.
- **Null routing / blackholing**: BGP blackhole dell'IP vittima (sacrifica la disponibilità per
  proteggere l'infrastruttura circostante; last resort).

### Layer CDN / scrubbing
- **Scrubbing center**: tutto il traffico viene deviato verso centri specializzati che separano
  il traffico legittimo dal flood prima di reinviarlo al server.
- **CDN / Anycast** (Cloudflare, Akamai, Fastly): le richieste vengono assorbite da PoP
  distribuiti globalmente; un flood da 1 Tbps viene "diluito" su decine di datacenter.
- **Anycast routing**: lo stesso IP è annunciato da più AS; il traffico viene diretto al PoP più
  vicino, riducendo la concentrazione dell'attacco.

### Layer applicativo (L7)
- **WAF** (Web Application Firewall): signature per Slowloris, RUDY, HTTP flood.
- **Challenge JS / CAPTCHA**: distingue browser reali da bot.
- **Rate limiting per IP / sessione**: max N richieste/s per sorgente.
- **Connection timeout aggressivo**: chiude le connessioni lente (anti-Slowloris).
  In nginx: `client_body_timeout 10; client_header_timeout 10;`.
- **Auto-scaling** (cloud): aggiunge capacità durante il picco; non una difesa ma un compensating
  control che aumenta la soglia prima del collasso.

### Tabella riepilogativa

| Tipo attacco | Difesa primaria | Difesa secondaria |
|---|---|---|
| SYN Flood | SYN cookies | Firewall stateful, rate limit |
| UDP/ICMP Flood | Rate limit upstream | Null routing, scrubbing CDN |
| Amplification | BCP 38 anti-spoofing | Disabilitare servizi riflettenti (NTP monlist OFF) |
| HTTP Flood | WAF + challenge JS | CDN, rate limiting per IP |
| Slowloris | Timeout aggressivi, nginx | WAF, connection rate limit |
| Botnet DDoS | Scrubbing center / anycast | BGP blackhole come last resort |

---

## MITRE ATT&CK

| Tecnica | ID | Sub-tecnica | Descrizione |
|---|---|---|---|
| Network Denial of Service | T1498 | — | DoS a livello di rete/trasporto |
| Direct Network Flood | T1498.001 | UDP/ICMP/SYN flood diretto | |
| Reflection Amplification | T1498.002 | DNS/NTP/memcached | |
| Endpoint Denial of Service | T1499 | — | DoS a livello applicativo |
| OS Exhaustion Flood | T1499.001 | SYN flood contro OS | |
| Service Exhaustion Flood | T1499.002 | HTTP/Slowloris | |
| Application Exhaustion Flood | T1499.003 | Query costose | |

---

## Casi limite e varianti avanzate

- **DoS pulsing (Intermittent)**: brevi burst ripetuti che degradano il servizio senza triggherare
  alert volumetrici classici; difficile da correlare nel [[SIEM]].
- **Low-and-slow (Slowloris, RUDY)**: traffico sotto la soglia dei rate limiter; richiede detection
  comportamentale (connessioni aperte da > N secondi senza completare).
- **ReDoS** (Regular Expression DoS): payload che triggera backtracking esponenziale nelle regex
  del server web/WAF; attacco CPU puramente L7.
- **Amplification verso terzi (DRDoS)**: la vittima è un innocente terzo; l'attaccante usa il suo
  IP come sorgente; causa danni reputazionali e blocchi IP.
- **Protezione cloud bypassata**: se l'IP reale del server viene scoperto (es. via leak
  DNS/certificato), l'attacco può aggirare il CDN. Soluzione: [[VPN]] / tunneling verso il CDN
  o blocco di tutti gli IP non appartenenti al CDN in ingresso.

---

## Domande da esame / colloquio

**Q1: Qual è la differenza tra DoS e DDoS?**
A: Il DoS proviene da una singola sorgente; è relativamente facile da bloccare filtrando l'IP.
Il DDoS usa migliaia di sorgenti distribuite (botnet), rendendo il filtraggio per IP inefficace.
Il DDoS è la forma predominante negli attacchi moderni ad alto impatto.

**Q2: Come funzionano i SYN cookies e perché mitigano il SYN flood?**
A: Normalmente, il server alloca uno slot in memoria per ogni SYN ricevuto (connessione half-open).
Con SYN cookies, il server non alloca nulla: codifica le informazioni di stato nel numero di sequenza
del SYN-ACK. Solo quando arriva un ACK valido (che deve riflettere quel numero) il server crea la
connessione. I SYN spoofati non ricevono mai un ACK valido, quindi nessuno slot viene consumato.

**Q3: Cos'è il fattore di amplificazione e quale servizio ha il valore più alto?**
A: Il fattore di amplificazione (AF) è il rapporto tra la dimensione della risposta e quella della
richiesta. L'attaccante ottiene un traffico verso la vittima molto superiore al traffico che genera.
Il più alto documentato è **memcached** con AF fino a ~50.000×: una richiesta di 15 byte genera una
risposta di ~750 KB. NTP (monlist) ha AF ~556×; DNS (ANY) ~28–54×.

**Q4: Perché BCP 38 riduce il rischio di reflection/amplification?**
A: BCP 38 impone agli ISP di filtrare in ingresso (ingress filtering) i pacchetti con IP sorgente
non appartenente ai blocchi assegnati al cliente. Se tutti gli ISP lo implementassero, l'IP spoofing
sarebbe impossibile e gli attacchi reflection — che dipendono dallo spoofing dell'IP della vittima
— non potrebbero funzionare. Il problema è la scarsa adozione globale.

**Q5: Cosa distingue un attacco L7 da uno volumetrico e perché è più difficile da mitigare?**
A: Un attacco volumetrico si distingue per il volume grezzo di traffico (Gbps); basta filtrare
a monte. Un attacco L7 usa richieste HTTP sintatticamente valide: il traffico sembra legittimo fino
al layer applicativo. Richiede challenge JavaScript, analisi comportamentale, CAPTCHA o machine
learning per distinguere bot da utenti reali, senza bloccare utenti legittimi.

**Q6: Come funziona Slowloris e come si difende nginx?**
A: Slowloris apre molte connessioni TCP al server e invia header HTTP incompleti a cadenza lenta.
Il server (se basato su thread/processo per connessione, es. Apache) tiene ogni thread bloccato
in attesa del completamento della richiesta, esaurendo il pool. Nginx usa un modello event-driven
asincrono: gestisce migliaia di connessioni in pochi thread; impostare `client_header_timeout`
basso (es. 10s) chiude connessioni lente prima che saturino le risorse.

---

## Strumenti di riferimento

| Tool | Funzione | Contesto |
|---|---|---|
| **hping3** | Forge pacchetti SYN/UDP/ICMP | Lab offensivo |
| **slowhttptest** | Simulazione Slowloris/RUDY | Lab offensivo |
| **iftop / nload** | Monitoraggio banda in tempo reale | Difesa |
| **ss / netstat** | Stato connessioni TCP | Difesa / detection |
| **iptables / nftables** | Rate limiting, SYN cookies | Difesa OS |
| **Wireshark** | Analisi pacchetti dell'attacco | Analisi |
| **Cloudflare / Akamai** | Scrubbing center, anycast CDN | Difesa enterprise |
| [[SIEM]] | Correlazione alert DoS | Blue Team |

---

## Collegamenti
- [[Triade CIA]] · [[Three-Way Handshake TCP]] · [[TCP]] · [[UDP]] · [[ICMP]]
- [[DNS]] · [[HTTP e HTTPS]] · [[VPN]]
- [[Detection di Attacchi]] · [[SIEM]] · [[Incident Response]]
- [[MITRE ATT&CK]] · [[Modello OSI]]

## Fonti
- Cloudflare — What is a DDoS attack?: https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/
- CISA — Understanding Denial-of-Service Attacks: https://www.cisa.gov/news-events/news/understanding-denial-service-attacks
- Cloudflare — SYN flood attack: https://www.cloudflare.com/learning/ddos/syn-flood-ddos-attack/
