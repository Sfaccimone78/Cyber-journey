---
tipo: concetto
tag: [osint, recon, infrastruttura]
fase: 3
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["OSINT su Domini", "OSINT su Infrastruttura", "Domain OSINT", "Recon Infrastruttura"]
---

# OSINT su Domini e Infrastruttura

## In breve
L'OSINT su domini e infrastruttura ricostruisce la **superficie d'attacco esterna** di un'organizzazione a partire dal solo nome di dominio: sottodomini, indirizzi IP, servizi esposti, tecnologie usate, dati di registrazione. È ricognizione [[OSINT]] **passiva** (interroga fonti terze come DNS pubblico, database WHOIS e log di trasparenza dei certificati, senza toccare direttamente i server del bersaglio). Impatto: mappa host dimenticati, ambienti di staging e servizi esposti che spesso sono l'anello debole.

## Come funziona
La ricognizione parte dal dominio e si espande a raggiera:

1. **WHOIS / RDAP**: dati di registrazione del dominio (registrar, date, a volte contatti). Il GDPR ha oscurato molti dati personali, ma restano utili date, name server e organizzazione.
2. **DNS** (vedi [[DNS]]): i record raccontano l'infrastruttura.
   - `A`/`AAAA` → IP; `MX` → server di posta; `NS` → name server; `TXT` → SPF/DKIM/DMARC e verifiche di terze parti; `CNAME` → alias (attenzione ai *dangling CNAME* → subdomain takeover).
3. **Enumerazione sottodomini** — due approcci:
   - **Passivo**: aggregatori come **crt.sh** (Certificate Transparency), motori come **Shodan**/**Censys**, dataset DNS storici. Non toccano il bersaglio.
   - **Attivo**: brute-force di nomi (es. con **amass**, **subfinder**, **dnsx**) e risoluzione DNS. Genera query verso i DNS del target.
4. **Certificate Transparency (CT)**: ogni certificato TLS emesso è registrato in log pubblici. Cercare per dominio su **crt.sh** rivela sottodomini presenti nei campi *Subject* e *SAN*, spesso includendo host interni/staging.
5. **Motori per dispositivi**: **Shodan** e **Censys** indicizzano banner, porte aperte, versioni di servizio e certificati per IP — permettono di scoprire servizi esposti senza scansionarli tu stesso.
6. **Fingerprinting delle tecnologie**: stack, CMS, framework e header (es. con **Wappalyzer**, **whatweb**).
7. **ASN e blocchi IP**: dall'IP si risale all'*Autonomous System Number* dell'organizzazione e quindi ad altri blocchi di rete di sua proprietà.
8. **Archivi storici**: la **Wayback Machine** mostra versioni passate del sito (endpoint dismessi, path, commenti nel sorgente).

La linea passivo/attivo è importante per l'OPSEC e per la legalità: solo il passivo è a rischio-zero di essere notato.

## Esempi
Dati di registrazione e DNS:
```bash
whois example.com
dig example.com ANY +noall +answer
dig example.com TXT +short          # SPF/DKIM/DMARC, verifiche vendor
dig -x 93.184.216.34 +short          # reverse DNS
```
Sottodomini da Certificate Transparency (crt.sh, output JSON):
```bash
curl -s "https://crt.sh/?q=%25.example.com&output=json" \
  | jq -r '.[].name_value' | sort -u
```
Enumerazione passiva + attiva con toolkit dedicati:
```bash
subfinder -d example.com -silent | tee subs.txt      # fonti passive
amass enum -passive -d example.com                    # aggregatori multipli
dnsx -l subs.txt -a -resp                             # risolvi in IP
```
Ricerca di servizi esposti (sintassi Shodan / Censys):
```text
# Shodan
ssl.cert.subject.cn:"example.com"
org:"Example Inc" port:22

# Censys Search
services.tls.certificates.leaf_data.subject_dn: example.com
```
Storia del sito:
```text
https://web.archive.org/web/*/example.com/*
```

## Mitigazione e difesa
Per ridurre la superficie esterna scopribile via OSINT:
1. **Inventario e attack surface management**: sapere quali sottodomini/host esistono; dismettere quelli non più usati.
2. **Eliminare i dangling CNAME**: un CNAME che punta a un servizio cloud non più attivo abilita il **subdomain takeover** — rimuoverlo appena si dismette il servizio.
3. **Wildcard certificate con criterio**: i certificati per singolo host finiscono in CT e rivelano nomi; valutare wildcard dove appropriato (senza però abbassare altre difese).
4. **Non esporre ambienti di staging/dev**: metterli dietro VPN o autenticazione, non su Internet pubblico.
5. **DNS igienico**: niente record che rivelano infrastruttura interna; SPF/DKIM/DMARC corretti riducono lo spoofing della posta.
6. **Monitoraggio CT e brand**: alert su nuovi certificati e domini simili (typosquatting) per accorgersi di esposizioni e phishing.

## Lab
- **crt.sh + subfinder su un dominio con bug-bounty pubblico**: costruisci l'elenco dei sottodomini in sola lettura (solo fonti passive), poi confronta con Shodan/Censys per capire quali servizi sono esposti.
- **[[TryHackMe]]** → room di *reconnaissance / passive recon* del percorso pentest: pratica WHOIS, DNS e CT in ambiente guidato prima di usarli su target reali.
- **[[Nmap]] in laboratorio proprio**: dopo la fase passiva, valida i servizi con una scansione mirata SOLO su host di tua proprietà (la scansione è attiva e va autorizzata).

## Domande
1. **D:** Qual è la differenza tra enumerazione passiva e attiva dei sottodomini?  **R:** La passiva interroga fonti terze (CT, Shodan, dataset DNS) senza toccare il bersaglio; l'attiva invia query DNS/brute-force verso l'infrastruttura del target.
2. **D:** Perché Certificate Transparency è preziosa nella ricognizione?  **R:** Ogni certificato TLS emesso è pubblicato in log pubblici, rivelando sottodomini (campo SAN) spesso interni o di staging.
3. **D:** Cos'è un subdomain takeover e cosa lo abilita?  **R:** L'appropriazione di un sottodominio tramite un *dangling CNAME* che punta a un servizio cloud dismesso ma ancora referenziato dal DNS.
4. **D:** A cosa serve un ASN nell'OSINT infrastrutturale?  **R:** A risalire dall'IP a tutti i blocchi di rete appartenenti alla stessa organizzazione.
5. **D:** Perché la Wayback Machine è utile?  **R:** Mostra versioni storiche del sito, rivelando endpoint dismessi, path e commenti non più presenti nella versione attuale.

## Collegamenti
- [[OSINT]]
- [[02 Motori di Ricerca e Google Dorking]]
- [[03 OSINT su Persone e Username]]
- [[05 Framework OSINT (Maltego, SpiderFoot, theHarvester)]]
- [[DNS]] · [[Nmap]]
- [[Sicurezza Operativa per le Indagini OSINT]]

## Fonti
- crt.sh — Certificate Transparency search: https://crt.sh/
- OWASP Web Security Testing Guide — Information Gathering: https://owasp.org/www-project-web-security-testing-guide/
- OWASP Amass Project: https://github.com/owasp-amass/amass
- Bellingcat — Online Investigation Toolkit: https://www.bellingcat.com/
