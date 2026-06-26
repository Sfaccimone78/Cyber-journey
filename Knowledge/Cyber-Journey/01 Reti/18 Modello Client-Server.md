---
tipo: concetto
tag: [reti]
fase: 1
fonti: 3
aggiornato: 2026-06-22
stato: maturo
aliases: ["Modello Client-Server"]
---

# Modello Client-Server

## In breve
Il modello **client-server** è l'architettura dominante in rete: un **client** apre la connessione e fa richieste, un **server** in ascolto le elabora e risponde. Web, email, [[DNS]], database, SSH: quasi tutto segue questo schema. L'alternativa è il **peer-to-peer** (P2P), dove ogni nodo è sia client sia server. Comprendere questo modello è fondamentale in sicurezza: la **superficie d'attacco** è definita dai servizi in ascolto, e ogni interazione client-server è un potenziale vettore di exploit, intercettazione o abuso.

---

## Ruoli asimmetrici: client e server

| Ruolo | Comportamento | Caratteristiche tecniche |
|---|---|---|
| **Client** | inizia la connessione, consuma il servizio | usa una **porta effimera** (49152–65535 secondo IANA, in pratica spesso da 1024 in su); non è in ascolto stabile |
| **Server** | è in **LISTEN** su una porta nota (well-known port) | gestisce molte connessioni simultanee; porta fissa e documentata (80 HTTP, 443 HTTPS, 22 SSH, 53 DNS…) |

Una connessione [[TCP]] è identificata univocamente dalla **4-tupla**:
```
(IP_sorgente, porta_sorgente, IP_destinazione, porta_destinazione)
```
Grazie alla porta effimera del client, un singolo server su porta 443 può gestire **migliaia di connessioni simultanee** distinguibili: ogni client ha una porta sorgente diversa. La connessione [[TCP]] nasce con il [[Three-Way Handshake TCP]].

---

## Meccanismo a basso livello: cosa succede davvero

### Lato server: il ciclo `socket → bind → listen → accept`
```python
# Pseudocodice
sock = socket(AF_INET, SOCK_STREAM)     # crea socket TCP
sock.bind(("0.0.0.0", 443))            # associa alla porta 443 su tutte le interfacce
sock.listen(128)                        # mette in ascolto; 128 = backlog (connessioni pending max)
while True:
    conn, addr = sock.accept()          # blocca finché arriva un client; restituisce socket nuovo
    handle(conn)                        # gestisce la connessione (spesso in un thread/processo separato)
```
Il **backlog** è la coda di connessioni in attesa di essere accettate. Un **SYN flood** (DDoS) mira a saturare questa coda: invia SYN senza mai completare l'handshake, finché il server non può più accettare connessioni legittime. Mitigazione: **SYN cookies** (il server non alloca stato finché non riceve il terzo ACK).

### Lato client: il ciclo `socket → connect`
```python
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("93.184.216.34", 443))    # kernel sceglie porta effimera, invia SYN
# dopo connect() il Three-Way Handshake è completato → socket pronto
sock.send(b"GET / HTTP/1.1\r\n...")
```

### Cosa significa "porta in LISTEN"
```bash
ss -tlnp          # Linux: mostra porte TCP in ascolto con il processo
netstat -an | findstr LISTEN   # Windows equivalente
```
Output tipico:
```
State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
LISTEN  0       128     0.0.0.0:443        0.0.0.0:*          nginx
LISTEN  0       5       127.0.0.1:3306     0.0.0.0:*          mysqld
```
- `0.0.0.0:443` → esposto su **tutte le interfacce** → raggiungibile da chiunque.
- `127.0.0.1:3306` → esposto solo su **loopback** → raggiungibile solo localmente → configurazione corretta per un DB.

---

## Stateful vs stateless

| Tipo | Definizione | Esempio | Pro | Contro |
|---|---|---|---|---|
| **Stateless** | ogni richiesta è indipendente; il server non ricorda le precedenti | [[HTTP e HTTPS\|HTTP]] (senza sessione), [[DNS]] | scala orizzontalmente in modo semplice (qualsiasi replica serve qualsiasi richiesta) | lo stato va gestito altrove (cookie, token JWT, cache distribuita) |
| **Stateful** | il server mantiene il contesto della sessione tra richieste successive | SSH, FTP attivo, connessione DB, WebSocket | più semplice per l'applicazione (no re-invio di contesto) | scalabilità complessa (il client deve tornare sullo stesso server, o serve session replication); più costoso da rendere ridondante |

**HTTP è stateless per design:** ogni richiesta HTTP è indipendente. La "sessione" dell'utente è simulata via cookie o token (JWT) che il client invia a ogni richiesta, ricostruendo il contesto lato server. Questo ha implicazioni di sicurezza: il token deve essere segreto, firmato e con scadenza (vedi [[Autenticazione e Gestione Sessioni]]).

---

## Architetture a livelli (n-tier)

Le applicazioni reali separano i ruoli in livelli distinti. Ogni confine tra livelli è un **trust boundary** da proteggere:

```
[Browser / App]           ← client (tier 0)
        ↕  HTTP/HTTPS
[Web Server / Reverse Proxy]  ← tier 1 (presentazione) — esposto su Internet
        ↕  HTTP interno
[Application Server]           ← tier 2 (logica business) — nella LAN interna
        ↕  SQL / gRPC
[Database Server]              ← tier 3 (dati) — subnet interna, mai esposta
```

Regole di sicurezza per architettura n-tier:
- Il **DB non deve mai essere direttamente accessibile da Internet** — deve rispondere solo all'application server, su una porta non standard, con autenticazione forte.
- Il **web server** (tier 1) non deve poter accedere direttamente al DB (principio di minimo privilegio tra livelli).
- I confini si proteggono con firewall/ACL e [[Subnetting|segmentazione di rete]].
- Le credenziali DB non devono essere nel codice sorgente (secret management: vault, env var cifrate).

---

## Client-Server vs Peer-to-Peer

| Aspetto | Client-Server | Peer-to-Peer (P2P) |
|---|---|---|
| Struttura | centralizzata | decentralizzata |
| Scalabilità | verticale (più risorse al server) + orizzontale (replica) | intrinsecamente orizzontale |
| Single Point of Failure | il server | nessuno (o ridotto) |
| Sicurezza | superficie concentrata → più facile da proteggere | superficie distribuita → difficile da monitorare e bloccare |
| Esempi | HTTP/S, SSH, DNS, DB, email | BitTorrent, blockchain, I2P, Tor (parzialmente) |
| Uso malevolo | C2 server → bot comunicano con un server centrale (più tracciabile) | C2 P2P (botnet senza centro) → resiliente, difficile da abbattere |

**C2 P2P (Command & Control Peer-to-Peer):** alcune botnet avanzate usano architettura P2P per il C2: non c'è un singolo server da abbattere. Rende il takedown molto più complesso (caso: botnet Gameover Zeus, Mirai varianti).

---

## Thin client vs Thick client vs API

| Modello | Dove vive la logica | Esempio | Implicazione sicurezza |
|---|---|---|---|
| **Thin client** | quasi tutta sul server | browser web (HTML+JS minimale) | la validazione avviene sul server; il client è non-fidato |
| **Thick client** | molta logica lato client | app desktop, videogame | il client può essere reverso/modificato; logica critica non deve stare solo lì |
| **API (REST/gRPC)** | logica sul server, dati in formato strutturato | SPA (React, Angular) + backend API | stesso modello client-server; le API vanno autenticate (OAuth2, JWT, API key) |

**Regola d'oro:** **qualsiasi input dal client è non fidato**. La validazione (lunghezza, tipo, formato, autorizzazione) **deve avvenire lato server**, anche se c'è validazione lato client per usabilità. La validazione client-side è aggirabile con [[Burp Suite]] in secondi.

---

## Scalabilità e alta disponibilità

Per servire migliaia di client simultanei, il modello client-server si estende con:

- **Load balancer:** distribuisce le connessioni tra più istanze del server. Può operare a L4 (round-robin su 4-tupla) o L7 (routing basato su URL, header HTTP). Spesso termina [[TLS e SSL|TLS]].
- **Horizontal scaling (scale out):** aggiungere istanze server identiche dietro il load balancer — preferibile al vertical scaling per resilienza.
- **Session persistence ("sticky sessions"):** se il server è stateful, il load balancer deve mandare le richieste dello stesso client sempre alla stessa istanza (via IP o cookie di sessione). Alternativa: session store esterno condiviso (Redis, memcached).
- **CDN (Content Delivery Network):** cache distribuita geograficamente per contenuti statici → riduce la latenza e l'esposizione del server origine.

---

## Rilevanza per la sicurezza

### Superficie d'attacco
Ogni servizio in ascolto è una porta d'ingresso. **Regola:** esponi solo il necessario; tutto il resto `127.0.0.1` o dietro firewall.
```bash
# Verifica cosa è in ascolto (Linux)
ss -tlnp
# Verifica cosa è in ascolto (Windows)
netstat -ano | findstr LISTEN
```
Un [[Nmap]] scan mostra esattamente cosa un attaccante vede dall'esterno.

### Autenticazione e autorizzazione
Il server deve verificare **chi** è il client (autenticazione) e **cosa** può fare (autorizzazione). La fiducia non può basarsi sul solo IP sorgente (facilmente spoofabile in UDP, o condiviso via NAT). Vedi [[Broken Access Control e IDOR]].

### DoS e SYN flood
- **SYN flood:** il client invia SYN senza mai completare il handshake → il server accumula connessioni half-open nel backlog → esaurito il backlog, non accetta più connessioni legittime. Contromisura: **SYN cookies** (il server codifica lo stato nel SYN/ACK, non alloca memoria finché non riceve l'ACK finale).
- **HTTP flood (layer 7 DoS):** richieste HTTP complete legittime ma in volume enorme → sovraccaricano la logica applicativa. Difficile da bloccare senza WAF/rate limiting perché il traffico appare legittimo a L4.
- Vedi [[DoS e DDoS]].

### Intercettazione (MitM)
Senza [[TLS e SSL|TLS]] il traffico tra client e server è in chiaro → leggibile con [[Wireshark]] o [[Man-in-the-Middle (MITM)|MitM]]. Con TLS: il canale è cifrato, ma un attaccante con CA controllata o sfruttando un trust error può fare TLS interception. HSTS e certificate pinning mitigano.

### Trust boundary e validazione input
La regola fondamentale: **il server non deve fidarsi del client**. Ogni dato proveniente dal client (parametri URL, body JSON, header HTTP, cookie) deve essere validato e sanificato lato server. La mancata validazione server-side porta a [[SQL Injection]], [[Cross-Site Scripting (XSS)]], [[Command Injection]] e molte altre vulnerabilità OWASP.

---

## Esempio pratico: diagnosi di sicurezza su un server
```bash
# 1. Cosa è in ascolto? (mapping della superficie)
ss -tlnp

# 2. Connessioni attive: chi sta parlando con me?
ss -tnp state established

# 3. Il servizio è esposto su tutte le interfacce o solo loopback?
ss -tlnp | grep 0.0.0.0   # esposto — verifica se deve esserlo

# 4. Da remoto: cosa vede un attaccante?
nmap -sV -p- <IP_server>

# 5. Backlog attuale (connessioni pending)
ss -tlnp | awk '{print $2}'   # Recv-Q = connessioni in coda non ancora accept()-ate
```

---

## Casi limite e troubleshooting

- **Porta già in uso (`bind: address already in use`):** un altro processo usa già la porta. `ss -tlnp | grep :80` identifica il processo. Il server non parte. Fix: ferma il processo conflittante o cambia porta.
- **Connessione rifiutata (`Connection refused`):** il server non è in ascolto su quella porta — o non è avviato, o è in ascolto su un'altra interfaccia (loopback vs 0.0.0.0), o il firewall locale droppa la connessione prima che arrivi al processo.
- **Connessione timeout (nessuna risposta):** il pacchetto SYN viene droppato silenziosamente da un firewall intermedio (vs "connection refused" dove il RST arriva immediatamente). Distinguibile con [[Nmap]]: `filtered` (timeout) vs `closed` (RST).
- **Troppi open files (`Too many open files`):** ogni connessione è un file descriptor — il server ha raggiunto il limite (`ulimit -n`). Sintomo di DoS o misconfiguration (connessioni non chiuse correttamente → file descriptor leak).
- **Session fixation:** l'attaccante forza una session ID nota al client prima del login → dopo il login il server associa quella session ID all'utente autenticato → l'attaccante usa la session ID che conosceva già. Mitigazione: rigenera sempre la session ID al momento del login.

---

## Domande da esame/colloquio

1. **Cos'è la 4-tupla e perché permette a un server su una sola porta di gestire migliaia di client?**
   La 4-tupla `(IP_src, porta_src, IP_dst, porta_dst)` identifica univocamente ogni connessione TCP. Il server ha sempre lo stesso `IP_dst:porta_dst` (es. `93.1.2.3:443`), ma ogni client ha una porta sorgente diversa (effimera, 49152–65535). Quindi tutte le combinazioni sono uniche e il kernel può demultiplexare le connessioni correttamente.

2. **Differenza tra HTTP stateless e SSH stateful, e implicazioni di sicurezza?**
   HTTP non mantiene stato tra richieste — la sessione è simulata via cookie/token inviato a ogni richiesta. SSH è stateful: mantiene la sessione cifrata e il contesto dell'utente autenticato per tutta la durata della connessione. In HTTP il token deve essere protetto da furto (HttpOnly, Secure, SameSite); in SSH il rischio è lasciare sessioni aperte non monitorate o con keepalive che mantengono viva una connessione compromessa.

3. **Cos'è un SYN flood e come lo mitigano i SYN cookies?**
   Un SYN flood inonda il server di pacchetti SYN senza mai completare il Three-Way Handshake. Il server alloca memoria per ogni connessione half-open → il backlog si esaurisce → non accetta più connessioni legittime. I **SYN cookies** eliminano l'allocazione di stato: il server codifica le informazioni di connessione nel numero di sequenza del SYN/ACK. Se arriva l'ACK finale, il server decodifica il cookie e alloca la connessione solo allora.

4. **Perché la validazione lato client non basta e la validazione server-side è obbligatoria?**
   Il client è fuori dal controllo del server: un utente malintenzionato può modificare qualsiasi richiesta con tool come [[Burp Suite]], aggirando completamente la validazione JavaScript lato client. Il server deve trattare ogni input esterno come non fidato e validarlo prima di usarlo (lunghezza, tipo, formato, permessi) — altrimenti è vulnerabile a SQLi, XSS, command injection e simili.

5. **Differenza tra client-server e P2P in termini di superficie d'attacco e resilienza?**
   In client-server la superficie è concentrata sul server — più facile da proteggere, monitorare e patchare, ma è un single point of failure. In P2P la superficie è distribuita su tutti i nodi — più resiliente, ma ogni nodo è un potenziale punto di compromissione e il traffico è difficile da monitorare centralmente. Le botnet P2P sfruttano questa resilienza: eliminare un nodo non abbatte il C2.

6. **Cosa significa che un servizio è in ascolto su `0.0.0.0` vs `127.0.0.1`, e quale è più sicuro?**
   `0.0.0.0` significa che il servizio risponde su tutte le interfacce di rete disponibili — raggiungibile da qualsiasi host nella rete e potenzialmente da Internet. `127.0.0.1` (loopback) significa che risponde solo alle connessioni originate sulla stessa macchina — non raggiungibile dall'esterno. Un DB dovrebbe sempre essere su `127.0.0.1` o su una subnet privata raggiungibile solo dall'application server, mai su `0.0.0.0` esposto.

---

## Collegamenti
- [[Three-Way Handshake TCP]] · [[TCP]] · [[UDP]] · [[Porte e Protocolli Comuni]]
- [[HTTP e HTTPS]] · [[DNS]] · [[Subnetting]] · [[Hardware di Rete]]
- [[Broken Access Control e IDOR]] · [[Wireshark]] · [[Nmap]]
- [[DoS e DDoS]] · [[Man-in-the-Middle (MITM)]]
- [[Autenticazione e Gestione Sessioni]] · [[TLS e SSL]]

## Fonti
- Cloudflare — Client-side vs server-side: https://www.cloudflare.com/learning/serverless/glossary/client-side-vs-server-side/
- MDN — Client-Server overview: https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Client-Server_overview
- Wikipedia — Client–server model: https://en.wikipedia.org/wiki/Client%E2%80%93server_model
