---
tipo: concetto
tag: [metodologia]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Scansione delle Porte"]

---

# Scansione delle Porte

## In breve

La **scansione delle porte** (port scanning) è la tecnica che permette di scoprire quali porte TCP/UDP sono aperte su un host remoto e, di conseguenza, quali servizi sono in esecuzione. È uno dei passi fondamentali della [[Ricognizione (Recon)]] attiva e fornisce il punto di partenza per l'[[Enumerazione]] dettagliata.

## Come funziona

Una porta è "aperta" quando un servizio è in ascolto e risponde alle connessioni. Lo scanner invia pacchetti di prova e interpreta le risposte:

| Risposta ricevuta | Significato |
|---|---|
| SYN-ACK (TCP) | Porta **aperta** — servizio in ascolto |
| RST (TCP) | Porta **chiusa** — host raggiungibile, nessun servizio |
| Nessuna risposta | Porta **filtrata** — firewall sta bloccando |

### Tipi di scansione TCP

- **SYN scan** (half-open, `-sS`): invia SYN, riceve SYN-ACK, manda subito RST senza completare l'handshake. Più veloce e meno rumoroso del TCP connect. Richiede privilegi root.
- **TCP Connect** (`-sT`): completa il [[Three-Way Handshake TCP]]. Non richiede root, ma è più visibile nei log.
- **NULL / FIN / Xmas scan** (`-sN`, `-sF`, `-sX`): tecniche per eludere alcuni firewall e IDS.

### Scansione UDP (`-sU`)
UDP non ha handshake: lo scanner invia un pacchetto e aspetta una risposta ICMP "port unreachable" per porte chiuse. Le porte aperte spesso non rispondono affatto. Molto più lenta del TCP.

### Rilevamento servizi e versioni (`-sV`)
Una volta trovate le porte aperte, lo scanner manda probe specifici per identificare il servizio e la sua versione (es. "Apache httpd 2.4.51"). Questa informazione è essenziale per cercare exploit.

## Esempio pratico

```bash
# Scansione veloce delle 1000 porte più comuni (richiede root per SYN scan)
nmap -sV 10.10.10.5

# Scansione di TUTTE le 65535 porte TCP
nmap -p- 10.10.10.5

# Scansione veloce + rilevamento OS + script predefiniti
nmap -sC -sV -O 10.10.10.5

# Scansione UDP delle porte più comuni
nmap -sU --top-ports 20 10.10.10.5

# Output in tutti i formati (normale, grepable, XML) per documentazione
nmap -sC -sV -oA scan_risultati 10.10.10.5

# Scansione silenziosa (più lenta per non triggerare IDS)
nmap -sS -T2 10.10.10.5
```

## Note

> Eseguire port scanning solo su sistemi di cui si ha autorizzazione esplicita. Scansionare host di terzi senza permesso è illegale in molti paesi.

- Il timing (`-T0` a `-T5`) bilancia velocità e silenziosità. `-T4` è il default per reti veloci, `-T1` e `-T2` sono più silenziosi ma molto lenti.
- I flag `-sC` eseguono gli **NSE script** (Nmap Scripting Engine) di default: rilevamento di vulnerabilità, enumerate versioni, banner grabbing.
- Annotare sempre i risultati: porta, protocollo, servizio, versione. Sono la base per tutto ciò che segue.
- [[Nmap]] è lo strumento standard de facto per questa attività.

## Mitigazione e difesa

- Usare un firewall per filtrare le porte non necessarie e rispondere con RST (o silenzio) alle non usate.
- Cambiare le porte default dei servizi critici (es. SSH su porta non-22) riduce la visibilità nelle scansioni rapide.
- Deployare un IDS/IPS (es. Snort, Suricata) per rilevare scansioni aggressive.
- Esporre il minimo numero di servizi su Internet (superficie di attacco ridotta).

## Lab

- **[[TryHackMe]] — "Nmap" (furthernmap)**: room dedicata che fa praticare tutti i tipi di scansione (SYN, connect, UDP, `-sV`, `-sC`) e l'interpretazione delle risposte SYN-ACK/RST/filtrato.
- **[[TryHackMe]] — "Nmap Live Host Discovery"**: allena la fase precedente alla scansione porte (ARP/ICMP/ping sweep) per capire quali host sono vivi.
- **[[HackTheBox]] — Starting Point (es. *Meow*, *Fawn*)**: fai la prima scansione `nmap -sV -sC` su una macchina reale e verifica come le porte aperte guidano l'enumerazione successiva.

## Domande

1. **D:** Cosa distingue una porta "chiusa" da una "filtrata" durante una scansione TCP?  **R:** La porta chiusa risponde con un RST (host raggiungibile, nessun servizio); la filtrata non risponde affatto perché un firewall blocca il pacchetto.
2. **D:** Perché la SYN scan (`-sS`) è detta "half-open"?  **R:** Perché invia SYN, riceve SYN-ACK e risponde subito con RST senza completare il three-way handshake, risultando più veloce e silenziosa.
3. **D:** Perché la scansione UDP è molto più lenta di quella TCP?  **R:** Perché UDP non ha handshake: le porte aperte spesso non rispondono e lo scanner deve attendere timeout o risposte ICMP "port unreachable".
4. **D:** A cosa serve il flag `-sV`?  **R:** A identificare servizio e versione in ascolto sulle porte aperte, informazione essenziale per cercare exploit mirati.
5. **D:** Come si riduce la rumorosità di una scansione contro un IDS?  **R:** Abbassando il timing template (es. `-T1`/`-T2`), che rallenta l'invio dei pacchetti rendendo la scansione meno evidente.

## Collegamenti

- [[Ricognizione (Recon)]]
- [[Enumerazione]]
- [[Exploitation]]
- [[Nmap]]
- [[Porte e Protocolli Comuni]]
- [[Three-Way Handshake TCP]]
- [[Modello TCP-IP]]
- [[Metodologia del Pentest]]

## Fonti

- Nmap Reference Guide (documentazione ufficiale): <https://nmap.org/book/man.html>
- HackTricks — Port Scanning: <https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/nmap-cheatsheet-nmap-scanning>
- TryHackMe — Nmap room: <https://tryhackme.com/room/furthernmap>
