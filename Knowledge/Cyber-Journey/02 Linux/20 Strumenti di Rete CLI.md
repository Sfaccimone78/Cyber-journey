---
tipo: concetto
tag: [linux]
fase: 1
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Strumenti di Rete CLI", "Strumenti di Rete", "Tool di Rete"]
---

# Strumenti di Rete CLI

## In breve

Linux è onnipresente nei sistemi di rete (firewall, router, DNS, NAS) e fornisce una vasta gamma di comandi per **configurare, monitorare e diagnosticare** la rete e per **trasferire file** dalla riga di comando. Questa pagina copre i comandi più frequenti per la diagnostica: dalla raggiungibilità di un host all'ispezione di interfacce, socket aperti e risoluzione DNS. La teoria sottostante (incapsulamento, handshake, porte) è in [[TCP]], [[Modello TCP-IP]] e [[Porte e Protocolli Comuni]].

---

## Diagnostica della connettività

- **`ping host`** invia un pacchetto **ICMP ECHO_REQUEST**; la risposta verifica che interfacce, cablaggio, routing e gateway funzionino (0% packet loss = rete in salute). Molti host/firewall **bloccano ICMP**, quindi un ping fallito non implica sempre host down. Dettagli in [[Ping e Traceroute]].
- **`traceroute host`** (o `tracepath`/`mtr`) elenca tutti gli **hop** (router) attraversati, con 3 misure di round-trip per hop. Gli asterischi `* * *` indicano router che non rispondono; `-T`/`-I` possono aggirarli.

---

## Interfacce, routing e socket — la suite iproute2

Il comando **`ip`** è lo strumento multiuso moderno che **sostituisce il deprecato `ifconfig`**; usa l'intera gamma di feature del kernel Linux.

```bash
ip a            # (ip addr) indirizzi e stato di tutte le interfacce
ip link         # interfacce di livello 2 (su/giù, MAC)
ip r            # (ip route) tabella di routing — 'default via' = gateway
ip neigh        # tabella ARP/neighbor (vicini sulla LAN)
```

Nella diagnostica si cerca la parola **`UP`** (interfaccia abilitata) e un indirizzo valido nel campo `inet` (su DHCP conferma che il lease funziona).

Per i **socket** (connessioni e porte in ascolto), il vecchio `netstat` è **deprecato** in favore di **`ss`** (socket statistics, più veloce):

| Vecchio (netstat) | Moderno (ss / ip) | Funzione |
|-------------------|-------------------|----------|
| `netstat -tulpn` | `ss -tulpn` | porte TCP/UDP **in ascolto** + processo |
| `netstat -tan` | `ss -tan` | tutte le connessioni TCP |
| `netstat -r` | `ip route` | tabella di routing |
| `netstat -i` | `ip -s link` | statistiche per interfaccia |
| `ifconfig` | `ip addr` | indirizzi delle interfacce |

> [!tip] Triage di sicurezza
> `ss -tulpn` è il primo comando da lanciare per **scoprire cosa è in ascolto** su una macchina: rivela ogni porta aperta e il processo proprietario (audit di sicurezza, individuare backdoor). Confrontalo con ciò che *dovrebbe* essere esposto. Vedi [[Processi Linux]].

---

## Risoluzione DNS

- **`dig dominio`** interroga il DNS e mostra i record (A, AAAA, MX, NS, TXT…). `dig +short example.com` dà solo l'IP; `dig MX example.com` i mail server; `@8.8.8.8` forza un resolver. Sostituisce il vecchio `nslookup`.
- **`host dominio`** è una variante sintetica; **`getent hosts dominio`** rispetta l'ordine di risoluzione di sistema (`/etc/nsswitch.conf`, include `/etc/hosts`).

Approfondimento del protocollo in [[DNS]].

---

## Trasferimento e test HTTP

- **`curl URL`** è il coltellino svizzero HTTP(S): `-O` salva con il nome remoto, `-L` segue i redirect, `-I` mostra solo gli header, `-X POST -d ...` invia dati. Ideale per testare API ed endpoint.
- **`wget URL`** scarica file/siti in modo non interattivo: `-c` riprende download parziali, `-r` ricorsivo, gira anche in background dopo il logout.
- Per copiare file in sicurezza tra host si usa la suite SSH (`scp`, `sftp`, `rsync -e ssh`): vedi [[SSH]]. **FTP** trasmette le credenziali in **cleartext** ed è da evitare.

---

## Esempio pratico — diagnostica "dall'alto verso il basso"

```bash
ip a                       # 1. ho un IP? l'interfaccia è UP?
ip r                       # 2. ho un default gateway?
ping -c4 8.8.8.8           # 3. raggiungo Internet via IP? (esclude il DNS)
ping -c4 google.com        # 4. il DNS risolve? (se 3 ok ma 4 no → problema DNS)
dig +short google.com      # 5. cosa risponde il resolver?
ss -tulpn                  # 6. quali servizi locali ascoltano e su quali porte?

# Test di un endpoint HTTP
curl -IL https://example.com          # header + redirect, senza scaricare il body
curl -s https://api.github.com/zen    # body silenzioso (no progress bar)
```

---

## Comandi chiave

| Comando | Funzione |
|---------|----------|
| `ip a` / `ip r` / `ip link` | indirizzi / routing / interfacce L2 (sostituisce `ifconfig`/`route`) |
| `ss -tulpn` | socket in ascolto + processo (sostituisce `netstat`) |
| `ping` / `traceroute` / `mtr` | raggiungibilità / percorso / percorso live |
| `dig` / `host` / `getent hosts` | risoluzione DNS (sostituisce `nslookup`) |
| `curl` / `wget` | richieste HTTP(S) e API / download file |
| `nc` (netcat) | apre/test connessioni TCP/UDP grezze, port scan |
| `lsof -i` | file/processi che usano la rete |
| `tcpdump` | cattura pacchetti per analisi (vedi [[Wireshark]]) |

---

## Rilevanza per la sicurezza

- **Usa la suite iproute2 (`ip`, `ss`)**, non `ifconfig`/`netstat`/`route`: questi ultimi sono deprecati, spesso assenti nelle immagini minimali/container, e `ss` è più veloce e dettagliato.
- **`ss -tulpn` è il primo strumento di triage**: rivela ogni porta in ascolto e il processo proprietario; confrontalo con ciò che *dovrebbe* essere esposto per scovare servizi indesiderati o reverse shell. Vedi [[Processi Linux]].
- **Diagnostica DNS isolando i livelli**: se `ping IP` funziona ma `ping hostname` no, il problema è il DNS — verifica con `dig` e `/etc/resolv.conf`.
- **Per i trasferimenti preferisci canali cifrati** (`scp`/`sftp`/`rsync -e ssh`, [[SSH]]); FTP/Telnet inviano tutto in chiaro e sono catturabili da chi sniffa la rete ([[Man-in-the-Middle (MITM)]]).
- In `curl`, **verifica sempre il certificato TLS** (default): non usare `-k`/`--insecure` se non in test consapevoli — disabilita la verifica e apre a MITM.
- Per il firewall host usa **`ufw`** (frontend di nftables/iptables) o `firewalld`: chiudi tutto in ingresso tranne le porte necessarie (es. 22 SSH).
- **Enumerazione (pentest)**: `nc` come banner-grabber e port-scanner minimale quando manca nmap; `curl`/`wget` per scaricare tool sul target o esfiltrare; `ss`/`ip` per mappare la rete interna durante il pivoting.

---

## Collegamenti

- [[Ping e Traceroute]]
- [[DNS]]
- [[Porte e Protocolli Comuni]]
- [[TCP]]
- [[SSH]]
- [[Wireshark]]
- [[Processi Linux]]
- [[Comandi Linux di Base]]

## Fonti

- The Linux Command Line (W. Shotts), Cap. 16 "Networking": https://linuxcommand.org/tlcl.php
- man ip, man ss (iproute2); man dig (bind-utils); man curl
