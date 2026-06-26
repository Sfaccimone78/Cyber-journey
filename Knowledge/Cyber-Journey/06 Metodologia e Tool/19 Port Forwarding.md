---
tipo: concetto
tag: [metodologia, tool, reti]
fase: 3
fonti: 5
aggiornato: 2026-06-21
stato: maturo
aliases: ["Port Forwarding"]
---

# Port Forwarding

> **Nota etica**: i tunnel attraversano segmenti di rete e bypassano controlli perimetrali. Usali solo entro lo scope autorizzato e smantellali a fine engagement (i tunnel lasciati attivi sono un rischio reale per il cliente).

## In breve
Il **port forwarding** mappa una **porta** da un punto della rete a un altro attraverso un canale (di solito cifrato). È il mattone tecnico del [[Pivoting]]: dove il pivoting espone *un'intera rete*, il port forwarding espone *un servizio specifico*. Le tre forme da padroneggiare sono i tre flag SSH — **`-L` (local)**, **`-R` (remote)**, **`-D` (dynamic)** — più gli strumenti che li replicano quando [[SSH]] non è disponibile: **chisel**, **socat**, **netcat**.

## Il modello mentale: chi ascolta, chi inoltra?
La confusione su `-L` vs `-R` sparisce con una regola: **il flag dice DOVE si apre la porta in ascolto**. Local = sul *tuo* lato (client SSH). Remote = sul lato *server* SSH.

```
LOCAL FORWARD   ssh -L [bind]:Lport:dest:dport  user@SSHserver
  apre Lport SUL CLIENT → inoltra a dest:dport vista DAL SERVER
  "porto a ME un servizio che solo il server raggiunge"

  ┌────────┐  porta locale   ┌──────────┐         ┌──────────┐
  │ CLIENT │  127.0.0.1:8000 │ SSHserver│         │ dest     │
  │  (tu)  │◄───────tunnel───┤          ├────────►│ :80      │
  └────────┘                 └──────────┘         └──────────┘
   ascolto qui                            raggiunge lui il dest

REMOTE FORWARD  ssh -R [bind]:Rport:dest:dport  user@SSHserver
  apre Rport SUL SERVER → inoltra a dest:dport vista DAL CLIENT
  "espongo a un host remoto un servizio che solo IO raggiungo"

  ┌────────┐                 ┌──────────┐  porta remota  ┌──────────┐
  │ CLIENT │                 │ SSHserver│  0.0.0.0:9000  │ altri    │
  │  (tu)  ├──────tunnel────►│          │◄───────────────┤ host     │
  └────────┘                 └──────────┘                └──────────┘
   raggiungo io il dest        ascolto qui

DYNAMIC FORWARD ssh -D [bind]:Sport  user@SSHserver
  apre un proxy SOCKS sul client → instrada QUALSIASI dest dal server
  "un'unica porta per tutta la rete del server" (vedi Pivoting)
```

## SSH: i tre flag in pratica

### `-L` Local forward — tirare verso di te un servizio interno
```bash
# Caso classico: RDP su un host interno raggiungibile solo dal jump host
ssh -L 3389:172.16.0.50:3389 -N -f operatore@10.10.10.5
xfreerdp /v:127.0.0.1:3389         # ti connetti a TE STESSO → esce sul target

# Pannello admin web interno (bind solo su loopback per non esporlo)
ssh -L 127.0.0.1:8000:172.16.0.10:80 -N operatore@10.10.10.5
# → http://127.0.0.1:8000
```
`-N` = niente shell remota (solo tunnel). `-f` = background. `dest` è risolto **dal server SSH**, quindi può essere un IP che tu non raggiungi.

### `-R` Remote forward — ricevere una reverse shell o esporre il tuo servizio
```bash
# Sei dentro una rete interna via SSH e vuoi che un host interno
# raggiunga un servizio sulla TUA Kali (es. un payload server)
ssh -R 8000:127.0.0.1:8000 -N operatore@host-interno
# host-interno:8000 → ora punta al tuo 127.0.0.1:8000

# Per far ascoltare la porta remota su TUTTE le interfacce (non solo loopback):
# sul server SSH serve  GatewayPorts yes  in /etc/ssh/sshd_config
ssh -R 0.0.0.0:9000:127.0.0.1:9000 -N operatore@host-interno
```
> [!warning] GatewayPorts
> Di default `-R` lega la porta remota a `127.0.0.1` del server. Per renderla raggiungibile da altri host serve `GatewayPorts yes` (o `clientspecified`) lato sshd. È la causa #1 di "il forward c'è ma nessuno ci si connette".

### `-D` Dynamic forward — proxy SOCKS (il ponte verso il [[Pivoting]])
```bash
ssh -D 1080 -N -f operatore@10.10.10.5
# /etc/proxychains4.conf → socks5 127.0.0.1 1080
proxychains nmap -sT -Pn 172.16.0.0/24
```
Dettagli operativi in [[Pivoting]] (sezione SOCKS).

## chisel — quando SSH non c'è o il firewall blocca tutto
chisel è un tunnel TCP/UDP **su HTTP** in un singolo binario Go (client+server). Brilla quando il pivot non ha SSH e l'unica via d'uscita è HTTP/HTTPS.

```
REVERSE (il client si connette IN USCITA verso il server → buca l'egress firewall)

  Kali (server)                         Pivot (client, no SSH)
  ┌─────────────────────┐               ┌──────────────────────┐
  │ chisel server        │  HTTP :8080  │ chisel client         │
  │   --reverse          │◄─────────────┤   R:1080:socks        │
  │ → SOCKS su 127:1080  │   in uscita  │ (si connette a te)    │
  └─────────────────────┘               └──────────────────────┘
```

```bash
# --- SOCKS reverse (caso più comune) ---
# Sulla Kali (raggiungibile / la tua macchina di attacco):
chisel server -p 8080 --reverse
# Sul pivot (si connette verso di te, supera firewall in USCITA):
./chisel client 10.10.10.9:8080 R:1080:socks
# → 127.0.0.1:1080 sulla Kali è un SOCKS verso la rete del pivot
proxychains nmap -sT -Pn 172.16.0.50

# --- Forward di una singola porta (reverse) ---
# Esponi sulla Kali la porta 3306 del DB interno visto dal pivot:
./chisel client 10.10.10.9:8080 R:3306:172.16.0.50:3306
mysql -h 127.0.0.1 -P 3306 -u root -p

# --- Mascherare su HTTPS / aggiungere autenticazione ---
chisel server -p 443 --reverse --auth "user:pass"
./chisel client --auth "user:pass" https://10.10.10.9:443 R:1080:socks
```
chisel passa dove SSH muore: molti perimetri permettono solo 80/443 in uscita, e chisel incapsula tutto in HTTP.

## socat — il "cavo di prolunga" universale
socat collega due endpoint qualsiasi (TCP, UDP, file, PTY). Utile per **relay** semplici e per stabilizzare shell.

```bash
# Relay TCP: chi si connette alla porta 8080 del pivot esce su 172.16.0.50:80
socat TCP-LISTEN:8080,fork,reuseaddr TCP:172.16.0.50:80

# "Port forward" persistente su un host senza SSH
socat TCP-LISTEN:4444,fork TCP:172.16.0.50:445

# Relay cifrato (utile per non passare in chiaro):
# listener (Kali)
socat OPENSSL-LISTEN:4443,cert=server.pem,verify=0,fork TCP:127.0.0.1:80
# client (pivot)
socat TCP-LISTEN:8080,fork OPENSSL:10.10.10.9:4443,verify=0

# Bonus: upgrade di una reverse shell a TTY pieno (vedi Reverse Shell e Bind Shell)
socat file:`tty`,raw,echo=0 TCP-LISTEN:4444
```
`fork` = gestisce connessioni multiple; `reuseaddr` = riusa la porta subito dopo la chiusura.

## netcat — port forward minimale (ultima spiaggia)
[[netcat]] non fa forwarding nativo, ma con una FIFO o due processi back-to-back simula un relay. Fragile (no `fork`, una connessione alla volta), ma è ovunque.
```bash
mkfifo /tmp/f
nc -lvp 8080 < /tmp/f | nc 172.16.0.50 80 > /tmp/f
# chi si connette al pivot:8080 viene inoltrato a 172.16.0.50:80
```

## Tabella comparativa

| Tecnica | Direzione tunnel | Cifrato | Multi-conn | Quando usarla |
|---|---|---|---|---|
| `ssh -L` | in uscita verso server | sì | sì | Hai SSH; tiri **un** servizio interno verso di te |
| `ssh -R` | in uscita verso server | sì | sì | Esponi un **tuo** servizio a un host remoto / reverse |
| `ssh -D` | in uscita verso server | sì | sì | SOCKS, **intera** rete del server (pivoting) |
| **chisel** | client→server (reverse) | sì (su HTTP/S) | sì | **No SSH**; firewall egress permette solo 80/443 |
| **socat** | configurabile | opzionale (OPENSSL) | sì (`fork`) | Relay generico, stabilizzare shell, protocolli non-TCP |
| **netcat** | listener locale | no | no | Niente di meglio disponibile, relay usa-e-getta |
| **sshuttle** | in uscita verso server | sì | n/a | Subnet intera trasparente (vedi [[Pivoting]]) |

## Walkthrough end-to-end: esporre un'app interna sul tuo browser
Target: `172.16.0.10:8080` (dashboard interna) raggiungibile solo dal jump `10.10.10.5`.

```bash
# 1. Verifica di NON raggiungerlo direttamente
curl -m 5 http://172.16.0.10:8080      # timeout → invisibile

# 2a. Hai SSH → local forward su loopback (non lo esponi ad altri)
ssh -L 127.0.0.1:8080:172.16.0.10:8080 -N -f operatore@10.10.10.5
curl http://127.0.0.1:8080             # ora risponde → apri nel browser

# 2b. NON hai SSH → chisel reverse forward della singola porta
# Kali:
chisel server -p 443 --reverse
# Pivot (caricato il binario chisel):
./chisel client 10.10.10.9:443 R:8080:172.16.0.10:8080
curl http://127.0.0.1:8080             # idem, via chisel

# 3. Cleanup a fine test (NON dimenticarlo)
pkill -f "ssh -L 127.0.0.1:8080"       # killa il tunnel SSH
# chisel: chiudi client e server; rimuovi il binario dal pivot
```

## Troubleshooting connessioni

| Sintomo | Causa | Fix |
|---|---|---|
| `-R` "il forward c'è ma nessuno si connette" | sshd lega la porta a 127.0.0.1 | `GatewayPorts yes` in sshd_config + bind `0.0.0.0:` |
| `bind: Address already in use` | porta locale occupata | cambia porta o killa il vecchio tunnel |
| `channel ... open failed: administratively prohibited` | `AllowTcpForwarding no` sul server | non puoi tunnelare via quell'SSH; usa chisel/socat |
| Tunnel cade dopo idle | timeout NAT/firewall | `ssh -o ServerAliveInterval=30 -o ServerAliveCountResExceeded` / keepalive |
| chisel client non connette | egress filtrato | usa porta 443, prova `--auth`, verifica con `curl` l'uscita |
| Servizio raggiunto ma "Connection refused" | `dest:dport` errati o servizio fermo | conferma il servizio sul target (`proxychains nc -vz`) |
| Forward lento/intermittente | un solo hop SSH saturo | dynamic forward + parallelismo, o sshuttle |
| socat "una connessione poi muore" | manca `fork` | aggiungi `fork,reuseaddr` al LISTEN |

## Detection lato blue team
Stessa mappatura del [[Pivoting]]:
- **T1572 — Protocol Tunneling**: SSH/chisel che incapsulano altro traffico; chisel su HTTP è classico tunneling.
- **T1090 — Proxy**: il `-D` SOCKS e i relay socat.
- **T1571 — Non-Standard Port**: servizi su porte inattese (SOCKS su 1080, chisel su 8080).

Indicatori concreti:
- Sessioni SSH con flag di forwarding nei log (`sshd` logga le richieste di port forward se `LogLevel VERBOSE`).
- Binari `chisel`/`socat` su server di produzione → EDR, `auditd`, hash noti.
- Traffico su 443 verso un IP esterno **non-TLS** o con TLS anomalo (chisel mascherato).
- Un host che apre **listener** su porte alte (`netstat`/`ss`) e inoltra verso reti interne.
Difesa: `AllowTcpForwarding no` / `PermitTunnel no` sui jump host non destinati al forwarding, egress filtering, application allow-listing, ispezione TLS.

## Domande da colloquio
- *`-L` vs `-R` in una frase?* `-L` apre la porta sul **mio** lato e tira verso di me; `-R` apre la porta sul lato **server** e spinge verso di me. Il flag indica dove sta il listener.
- *Devi raggiungere RDP su un host che vedi solo dal jump host — quale forward?* `ssh -L 3389:target:3389 jump` e ti connetti a `127.0.0.1:3389`.
- *Il pivot non ha SSH e l'unica uscita è 443: come tunneli?* chisel reverse su 443 (incapsula in HTTP/S, supera l'egress).
- *Cos'è GatewayPorts e perché conta?* Controlla se la porta di un `-R` è raggiungibile da host esterni al server o solo da loopback; senza `yes`, il forward sembra non funzionare.
- *Differenza tra `-D` e un local forward?* `-L` mappa **una** destinazione fissa; `-D` apre un SOCKS che instrada **qualsiasi** destinazione a runtime.

## Collegamenti
- [[Pivoting]] — il port forwarding è il suo mattone di base
- [[SSH]] — `-L`, `-R`, `-D`, `-J`, GatewayPorts
- [[Reverse Shell e Bind Shell]] — `-R` e socat per ricevere/stabilizzare shell
- [[netcat]] — relay minimale
- [[Lateral Movement]]
- [[Metasploit]] — portfwd come alternativa interna a `-L`
- [[Nmap]] — scansione attraverso il proxy

## Fonti
- OpenSSH manual — ssh(1), opzioni -L/-R/-D: https://man.openbsd.org/ssh
- chisel (jpillora) — README: https://github.com/jpillora/chisel
- socat manual: http://www.dest-unreach.org/socat/doc/socat.html
- HackTricks — Tunneling and Port Forwarding: https://book.hacktricks.xyz/generic-methodologies-and-resources/tunneling-and-port-forwarding
- MITRE ATT&CK — Protocol Tunneling (T1572): https://attack.mitre.org/techniques/T1572/
