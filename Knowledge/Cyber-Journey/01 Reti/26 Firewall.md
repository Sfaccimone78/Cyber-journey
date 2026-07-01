---
tipo: concetto
tag: [reti, blue-team]
fase: 1
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Firewall", "Firewall e NAT"]
---

# Firewall

## In breve
Un **firewall** è un sistema (hardware o software) che **filtra** il traffico di rete in base a un insieme
di **regole**, separando una zona fidata (LAN) da una non fidata (Internet). Fa **controllo d'accesso**:
decide quali pacchetti/connessioni passano e quali no. Da non confondere con il [[NAT]], che fa
*traduzione di indirizzi* (e, di riflesso, un po' di isolamento): **NAT non è un firewall**. Spesso i due
convivono nello stesso router/gateway, ma rispondono a esigenze diverse.

---

## Tipi di firewall, per livello
| Tipo | Livello | Cosa ispeziona | Pro / contro |
|---|---|---|---|
| **Packet filter (stateless)** | L3/L4 | IP sorgente/destinazione, porta, protocollo, pacchetto per pacchetto | Veloce, ma **cieco al contesto** (non sa se un pacchetto appartiene a una connessione legittima) |
| **Stateful (stateful inspection)** | L3/L4 + stato | tiene una **tabella delle connessioni** (4-tupla + stato TCP) | Standard moderno: permette le risposte a connessioni avviate dall'interno, blocca i pacchetti non sollecitati |
| **Application firewall / proxy** | L7 | il **contenuto applicativo** (HTTP, DNS…) | Ispezione profonda, può bloccare attacchi applicativi; più costoso/lento |
| **WAF** (Web Application Firewall) | L7 | richieste HTTP | Blocca [[SQL Injection|SQLi]], [[Cross-Site Scripting (XSS)|XSS]] e altri attacchi web analizzando le richieste → [[HTTP e HTTPS]] |

Il firewall **stateful** è il cuore dei firewall moderni: basandosi sul *connection tracking* (la stessa
*state table* / conntrack che abilita il [[NAT]]), permette automaticamente il traffico di ritorno delle
connessioni legittime e blocca ciò che arriva non sollecitato.

---

## Policy: default-deny vs default-allow
Due filosofie opposte:
- **Default-deny (whitelist)** — *blocca tutto tranne ciò che è esplicitamente permesso*. È la postura
  **più sicura** e la scelta corretta in produzione.
- **Default-allow (blacklist)** — *permette tutto tranne ciò che è esplicitamente bloccato*. Comoda ma
  fragile: ogni nuovo servizio è esposto finché qualcuno non aggiunge la regola.

Le regole si applicano in due direzioni:
- **Ingress** (in entrata): protegge i servizi interni dalle connessioni esterne.
- **Egress** (in uscita): controlla cosa può uscire — fondamentale per fermare **reverse shell**,
  esfiltrazione e canali **C2**, che il [[NAT]] da solo **non** blocca perché avviati dall'interno.

---

## Esempio pratico — iptables / nftables / ufw
```bash
# Postura default-deny in ingresso (nftables/iptables logica)
iptables -P INPUT DROP                 # politica di default: nega
iptables -A INPUT -i lo -j ACCEPT      # permetti il loopback
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT  # stateful: traffico di ritorno
iptables -A INPUT -p tcp --dport 22 -j ACCEPT   # permetti SSH in ingresso

# Egress filtering: blocca tutto in uscita tranne DNS/HTTP/HTTPS
iptables -P OUTPUT DROP
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp -m multiport --dports 80,443 -j ACCEPT

# ufw (frontend semplificato)
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
```

Il tuo **router di casa** fa firewall + NAT insieme: il firewall stateful blocca le connessioni in
ingresso non richieste (il PC interno non è raggiungibile da fuori), mentre il NAT/PAT fa navigare tutti
i dispositivi con un solo IP pubblico.

---

## Limiti — cosa un firewall (e il NAT) NON fa
- Un **packet filter stateless** non capisce il contesto: può essere aggirato con frammentazione o
  pacchetti con flag anomale (scansioni FIN/NULL/Xmas → [[TCP]]).
- Un firewall L3/L4 **non vede il payload applicativo**: per gli attacchi web serve un **WAF** (L7).
- Tecniche di **bypass/evasione**: tunneling (es. su DNS o HTTP), **port knocking**, evasione IDS.
- Il [[NAT]] offre un isolamento *implicito* ma **non è una policy di sicurezza**: serve sempre un filtro
  esplicito, soprattutto in **egress**.

---

## Collegamenti
- [[NAT]] — traduzione di indirizzi; *NAT non è un firewall*
- [[HTTP e HTTPS]] — i WAF filtrano a L7 · [[OWASP Top 10]]
- [[TCP]] — scansioni e flag che i firewall stateless non distinguono
- [[Modello OSI]] · [[Modello TCP-IP]] — il livello dell'attacco sceglie il livello della difesa
- [[DoS e DDoS]] · [[Man-in-the-Middle (MITM)]]

## Fonti
- Systems Approach — *Computer Networks* (cap. "Network Security — Firewalls"): <https://book.systemsapproach.org/>
- NIST SP 800-41 Rev.1 — Guidelines on Firewalls and Firewall Policy: https://csrc.nist.gov/pubs/sp/800/41/r1/final
