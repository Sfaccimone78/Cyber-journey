---
tipo: concetto
tag: [metodologia, reti]
fase: 2
fonti: 2
aggiornato: 2026-06-26
stato: maturo
aliases: ["Attacchi di Rete", "Network Attacks"]
---
# Attacchi di Rete

## Definizione
Gli **attacchi di rete** sfruttano debolezze nei protocolli (spesso progettati senza sicurezza: ARP, DNS, ICMP, TCP) per intercettare, alterare o negare il traffico. Molti derivano dal fatto che i protocolli classici **non autenticano** né cifrano.

> [!note] Pagine dedicate in 01 Reti
> Diversi attacchi qui riassunti hanno (o avranno) una trattazione propria nell'area **01 Reti** — in particolare **MITM** ([[Man-in-the-Middle (MITM)]]) e **DoS/DDoS** ([[DoS e DDoS]]). Questa pagina ne dà la visione d'insieme dal punto di vista metodologico-offensivo.

## MITM (Man-in-the-Middle)
L'attaccante si interpone tra due parti, leggendo/alterando il traffico. Abilitato da ARP spoofing, DNS poisoning, rogue AP, o downgrade TLS (**sslstrip**). Viola confidenzialità e integrità ([[Triade CIA]]).

## ARP Spoofing (LAN)
ARP non ha autenticazione: l'attaccante invia risposte ARP false ("io sono il gateway") avvelenando la cache delle vittime → tutto il traffico LAN passa da lui. Base per MITM su rete locale.

## DNS Poisoning / Spoofing
Si inietta una risposta DNS falsa (cache poisoning, o risposta forgiata più veloce del server) → la vittima risolve un dominio legittimo verso un IP malevolo (pharming). Variante: **DNS rebinding** (usata anche in [[Server-Side Request Forgery (SSRF)]]).

## DDoS (Distributed Denial of Service)
Saturare risorse del target con traffico da molte sorgenti (botnet). Tipi:
- **Volumetrici / amplification**: piccola richiesta → grande risposta verso la vittima (spoofando l'IP sorgente). DNS/NTP/memcached amplification.
- **SYN flood**: half-open connections esauriscono la tabella TCP (fix: **SYN cookie**).
- **Application-layer** (L7): richieste HTTP costose.

## Esempio
```bash
# ARP spoofing → MITM (lab autorizzato)
bettercap -iface eth0 -eval "set arp.spoof.targets 10.0.0.5; arp.spoof on; net.sniff on"
# oppure
arpspoof -i eth0 -t 10.0.0.5 10.0.0.1

# SYN flood (test di resilienza, solo su target propri)
hping3 -S --flood -p 80 10.0.0.5

# Sniffing del traffico in chiaro risultante
tcpdump -i eth0 -A 'tcp port 80'
```

## Difesa
- **Cifratura end-to-end** (TLS/HTTPS → [[TLS e SSL]], VPN/IPsec): rende inutile l'intercettazione → la difesa più importante contro MITM/sniffing.
- **HSTS** contro sslstrip; validazione certificati.
- LAN: **Dynamic ARP Inspection** + DHCP snooping; port security.
- DNS: **DNSSEC** (firma i record), risolutori affidabili, DoH/DoT.
- DDoS: **rate limiting**, anti-DDoS/scrubbing (CDN), SYN cookie, anti-spoofing (BCP38).
- **Segmentazione**, IDS/IPS (Snort/Suricata), monitoraggio NetFlow → [[Detection di Attacchi]].

## Caso reale
- **Mirai (2016)** — botnet di dispositivi IoT con password di default che lanciò DDoS record (Dyn DNS → mezzo internet US offline, OVH, Krebs).
- **DNS cache poisoning — Kaminsky (2008)** — falla strutturale del DNS che permetteva il poisoning rapido; portò all'adozione accelerata della randomizzazione della porta sorgente e a DNSSEC.

## Collegamenti
- [[Server-Side Request Forgery (SSRF)]] · [[Analisi Malware di Base]] (botnet) · [[Cryptographic Failures]] · [[Triade CIA]]
- Reti: [[Man-in-the-Middle (MITM)]] · [[DoS e DDoS]] · Crittografia: [[TLS e SSL]]

## Fonti
- Anderson, *Security Engineering*, cap. 21 — https://www.cl.cam.ac.uk/~rja14/book.html
- MITRE ATT&CK — Enterprise Matrix (Discovery, Lateral Movement, Credential Access): https://attack.mitre.org/matrices/enterprise/
