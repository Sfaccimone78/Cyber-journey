---
tipo: concetto
tag: [metodologia]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Ricognizione (Recon)", "Reconnaissance", "Recon"]

---

# Ricognizione (Recon)

## In breve

La **ricognizione** è la prima fase attiva di un pentest: si raccolgono quante più informazioni possibili sul bersaglio *prima* di toccarlo direttamente. L'obiettivo è costruire una mappa dell'obiettivo — domini, indirizzi IP, tecnologie usate, personale — senza ancora sfruttare nulla.

## Come funziona

Si divide in due grandi categorie:

### Recon passiva
Non si invia nessun pacchetto direttamente al bersaglio. Si usano fonti pubbliche:
- Motori di ricerca (Google Dorking)
- Registri WHOIS e DNS pubblici
- Social media e LinkedIn (dati sui dipendenti)
- Archive.org (versioni vecchie del sito)
- Shodan (dispositivi connessi a Internet)
- Tecniche [[OSINT]] in generale

### Recon attiva
Si interagisce direttamente con il bersaglio, ma in modo silenzioso:
- Ping e traceroute per mappare la rete
- [[Scansione delle Porte]] con [[Nmap]] per scoprire servizi attivi
- DNS brute-force per trovare sottodomini nascosti
- Banner grabbing (leggere le risposte dei servizi per identificare versioni)

## Esempio pratico

```bash
# PASSIVA: Cercare email e sottodomini pubblici con theHarvester
theHarvester -d target.com -b google

# PASSIVA: Whois per info sul dominio
whois target.com

# PASSIVA: Google Dorking — file di config esposti
site:target.com filetype:conf

# ATTIVA: Enumerazione DNS per sottodomini
nmap --script dns-brute target.com

# ATTIVA: Banner grabbing su porta 80
nc -v target.com 80
HEAD / HTTP/1.0
```

## Note

> La recon passiva è quasi sempre legale perché usa dati pubblici. La recon attiva invia traffico verso il bersaglio e richiede autorizzazione scritta.

- Più informazioni si raccolgono nella recon, meno tempo si perde nelle fasi successive.
- Un bravo professionista documenta tutto in un file di note strutturato (es. con **CherryTree** o **Obsidian** stesso).

## Mitigazione e difesa

- Limitare le informazioni pubbliche: ridurre i dati nei record WHOIS (privacy proxy), non pubblicare strutture interne nei metadati.
- Monitorare Shodan periodicamente per capire cosa è esposto del proprio perimetro.
- Usare servizi di **Attack Surface Management** (es. Censys, SecurityTrails) per vedere cosa vede un attaccante.

## Lab

- **[[TryHackMe]] — "Passive Reconnaissance" e "Active Reconnaissance"**: le due room del Jr Penetration Tester path che fanno praticare esattamente la distinzione passiva/attiva, con `whois`, `nslookup`, `dig` da un lato e ping/traceroute/banner grabbing dall'altro.
- **[[TryHackMe]] — "Google Dorking"**: allena la ricerca mirata con operatori (`site:`, `filetype:`, `intitle:`) per trovare file e pagine esposti.
- **Shodan (piano free)**: esercitati a interrogare `https://www.shodan.io` con filtri come `org:`, `port:`, `product:` su un tuo dominio o su asset di test per vedere concretamente cosa espone un perimetro.

## Domande

1. **D:** Qual è la differenza chiave tra recon passiva e attiva?  **R:** La passiva non invia alcun pacchetto al bersaglio (usa solo fonti pubbliche), l'attiva interagisce direttamente col target inviando traffico.
2. **D:** Perché la recon passiva è quasi sempre legale mentre l'attiva richiede autorizzazione?  **R:** Perché la passiva usa dati già pubblici, mentre l'attiva invia traffico verso il bersaglio, azione che senza consenso può configurare accesso abusivo.
3. **D:** Cita tre fonti tipiche di recon passiva.  **R:** WHOIS/DNS pubblici, Google Dorking, Shodan (anche social/LinkedIn e Archive.org).
4. **D:** A cosa serve il banner grabbing?  **R:** A leggere le risposte dei servizi per identificarne versione e tipo di software.
5. **D:** Perché conviene raccogliere molte informazioni in fase di recon?  **R:** Più dati si raccolgono ora, meno tempo si perde nelle fasi successive di enumerazione ed exploitation.

## Collegamenti

- [[Metodologia del Pentest]]
- [[OSINT]]
- [[Scansione delle Porte]]
- [[Enumerazione]]
- [[Nmap]]

## Fonti

- OWASP Testing Guide — Information Gathering: <https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/>
- Shodan: <https://www.shodan.io/>
- TryHackMe — Passive Reconnaissance: <https://tryhackme.com/room/passiverecon>
