---
tipo: concetto
tag: [reti]
fase: 1
fonti: 5
aggiornato: 2026-06-26
stato: maturo
aliases: ["DNS"]
---

# DNS

## In breve
Il **DNS** (Domain Name System) è la "rubrica" di Internet: traduce nomi leggibili (`google.com`) negli IP che le macchine usano (`142.250.185.46`). È un database gerarchico e distribuito su [[UDP]]/53 (e [[TCP]]/53 per risposte grandi e trasferimenti di zona). Per un attaccante è anche una **miniera di ricognizione** e un canale di esfiltrazione; per il difensore è un log prezioso di ogni connessione uscente.

---

## Gerarchia: root, TLD, autoritativo

```
          .  (root — 13 set di root server, lettere a–m)
          |
        .com  (TLD — gestito da Verisign)
          |
    example.com  (zona — gestita dal titolare del dominio)
          |
    www.example.com  (record specifico nella zona)
```

- **Root server**: 13 indirizzi anycast (centinaia di nodi reali). Sanno solo dove sono i TLD.
- **TLD server**: gestiscono `.com`, `.net`, `.it`, ecc. Rimandano al nameserver autoritativo.
- **Nameserver autoritativo**: detiene i record della zona. Risponde con dati definitivi (AA flag = 1).
- **Resolver ricorsivo** (es. 1.1.1.1, 8.8.8.8): il proxy del client. Fa il lavoro iterativo e mette in cache.

---

## Risoluzione: ricorsiva vs iterativa

```text
1. Client controlla cache locale + /etc/hosts (/etc/nsswitch.conf determina l'ordine)
2. Client → Resolver (query RICORSIVA: "dammi la risposta finale, ci pensi tu")
3. Resolver → Root         → risposta: "chiedi al TLD .com → a.gtld-servers.net"
4. Resolver → TLD .com    → risposta: "chiedi all'autoritativo → ns1.example.com"
5. Resolver → ns1.example.com → risposta: "93.184.216.34" (AA=1)
6. Resolver mette in cache (per il TTL) e risponde al client
```

Il client fa **una** query ricorsiva; il resolver fa il lavoro iterativo verso la gerarchia.
La cache salva i roundtrip: se il TTL è lungo, il record viene servito localmente senza toccare la rete.

### Meccanismo a basso livello — il pacchetto DNS
Ogni query/risposta è un datagramma [[UDP]] (max ~512 byte; se la risposta supera, il resolver ritenta su [[TCP]]/53 oppure usa EDNS0 per payload più grandi).

Struttura: **Header** (16 bit: QR, Opcode, AA, TC, RD, RA, RCODE) + **Question** + **Answer** + **Authority** + **Additional**.

- `RD=1` (Recursion Desired): il client chiede al resolver di risolvere in modo ricorsivo.
- `RA=1` (Recursion Available): il server dice che supporta la ricorsione.
- `AA=1` (Authoritative Answer): la risposta viene dal nameserver autoritativo.
- `TC=1` (Truncated): la risposta è troncata → il client deve ritentare su TCP.

---

## Record DNS principali

| Record | Funzione | Esempio |
|--------|----------|---------|
| **A** | Nome → IPv4 | `example.com → 93.184.216.34` |
| **AAAA** | Nome → IPv6 | `example.com → 2606:2800::1` |
| **CNAME** | Alias verso altro nome (no MX/NS) | `www → example.com` |
| **MX** | Server di posta (+ priorità) | `10 mail.example.com` |
| **NS** | Nameserver autoritativi della zona | `ns1.example.com` |
| **SOA** | Metadati zona: serial, refresh, retry, expire, minTTL | uno per zona |
| **TXT** | Testo libero: SPF, DKIM, DMARC, verifica dominio | `v=spf1 include:...` |
| **SRV** | Servizio + porta + priorità + weight | `_ldap._tcp.example.com 0 100 389 dc.example.com` |
| **PTR** | IP → Nome (reverse lookup) | `34.216.184.93.in-addr.arpa → example.com` |
| **CAA** | Quali CA possono emettere certificati | `0 issue "letsencrypt.org"` |
| **NAPTR** | Mappatura per ENUM/VoIP | usato con SRV per numerazione telefonica |

Il **TTL** (Time To Live) controlla per quanti secondi un record resta in cache. TTL basso = propagazione rapida delle modifiche, ma più query; TTL alto = meno carico, ma propagazione lenta.

### Record SOA — perché conta
Il SOA contiene il **serial number** della zona (incrementato ad ogni modifica) e i parametri per i secondary nameserver (refresh, retry, expire). Tramite SOA si capisce quanto è aggiornata una zona secondaria.

### Record TXT per sicurezza email
- **SPF** (`v=spf1 ...`): elenca i server IP autorizzati a inviare email per il dominio.
- **DKIM** (`v=DKIM1; k=rsa; p=...`): chiave pubblica per la firma dei messaggi.
- **DMARC** (`v=DMARC1; p=reject; rua=...`): policy su cosa fare con email che falliscono SPF/DKIM.

---

## Ricognizione offensiva

Il DNS rivela la superficie d'attacco **prima ancora di toccare il target**:

```bash
# Record di base
dig example.com A +short
dig example.com MX
dig example.com TXT            # SPF/DKIM/DMARC → infrastruttura email
dig example.com NS             # chi è autoritativo
dig example.com SOA            # serial → quante volte è stata modificata la zona
dig -x 93.184.216.34           # reverse lookup (PTR)

# Trasferimento di zona (AXFR): se mal configurato, dumpa TUTTI i record
dig AXFR example.com @ns1.example.com
# Se il NS è permissivo, ottieni l'intera mappa interna in un colpo solo

# Enumerazione sottodomini (brute force)
gobuster dns -d example.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
dnsenum example.com
dnsrecon -d example.com -t brt -D subdomains.txt

# Ricerca passiva (senza query dirette al target)
# subfinder, amass, crt.sh (Certificate Transparency)
curl -s "https://crt.sh/?q=%25.example.com&output=json" | jq '.[].name_value' | sort -u

# Interrogare un resolver specifico
dig @8.8.8.8 example.com A
```

Il **trasferimento di zona AXFR** aperto verso chiunque è una grave misconfigurazione: espone l'intera mappa interna (server di staging, VPN, infrastruttura interna) in una singola query. Nei test di penetrazione va sempre provato su tutti i NS del dominio.

---

## Attacchi

### Cache Poisoning / Spoofing
L'attaccante inietta risposte false nella cache del resolver prima che arrivi la risposta legittima. La tecnica classica (Kaminsky, 2008) sfrutta la predittività degli ID di query (16 bit) inondando il resolver con risposte fasulle su sottodomini casuali. Se indovina ID + porta sorgente prima del legittimo autoritativo, la cache viene "avvelenata" → le vittime vengono dirottate.

**Difesa**: DNSSEC, randomizzazione porta sorgente (RFC 5452), 0x20 encoding, resolver moderni con EDNS COOKIE.

### DNS Tunneling / Esfiltrazione
Dati incapsulati in query DNS (label dei sottodomini, record TXT, CNAME) per aggirare firewall che bloccano HTTP/HTTPS ma permettono il DNS. Il canale è lento ma persistente. Strumenti: `iodine`, `dnscat2`.

```
# Esempio: dati esfiltrati come sottodomini
aGVsbG8.attacker.com → "hello" codificato base32 nel sottodominio
```

**Difesa**: monitorare lunghezza media dei query name (normale < 30 caratteri), frequenza query per dominio, entropia dei sottodomini, volume record TXT anomalo. RPZ (Response Policy Zone) per bloccare domini noti C2.

### DNS Hijacking
Modifica dei record presso il registrar o il resolver (account compromesso, BGP hijacking verso i root/TLD). Le vittime vengono servite da server DNS controllati dall'attaccante.

**Difesa**: MFA sull'account registrar, **registry lock** (variazione record richiede verifica fuori banda), DNSSEC per autenticare i record.

### Subdomain Takeover
Un record CNAME punta a un servizio cloud (GitHub Pages, AWS S3, Heroku) che è stato dismesso ma il record DNS non è stato rimosso. L'attaccante registra il servizio cloud con lo stesso nome e ne prende il controllo, potendo servire contenuti sotto il dominio della vittima (phishing, furto cookie).

**Difesa**: audit periodico dei CNAME pendenti ("dangling CNAME"), rimuovere i record quando si dismette un servizio, tool come `subjack` o `nuclei` per identificare takeover.

### DDoS Amplification (DNS Reflection)
L'attaccante invia query DNS con IP sorgente spoofato (IP vittima) verso resolver aperti; le risposte (tipicamente record ANY o DNSKEY grandi) vengono inviate alla vittima. Fattore di amplificazione: fino a 50–100x.

**Difesa**: disabilitare i resolver DNS aperti (rispondere solo a client interni), rate limiting sulle risposte, BCP38 anti-spoofing.

---

## Difese e hardening

| Meccanismo | Cosa fa |
|---|---|
| **DNSSEC** | Firma crittografica dei record (RRSIG, DNSKEY, DS). Il resolver verifica la catena di fiducia dalla root. Non cifra, ma garantisce autenticità e integrità. |
| **DoH** (DNS over HTTPS) | Query DNS in HTTPS (porta 443). Cifra il traffico, impedisce ispezione e censura ISP. Complica il monitoraggio aziendale. |
| **DoT** (DNS over TLS) | Query DNS in TLS (porta 853). Stesso obiettivo di DoH, più facile da filtrare. |
| **RPZ** (Response Policy Zone) | Blocca o redirige risoluzione di domini noti come malevoli. Standard de facto nei resolver aziendali. |
| **Split-horizon DNS** | Server interni risolvono nomi privati; esterni vedono solo record pubblici. Riduce superficie d'esposizione. |
| **Resolver interno** | Non esporre resolver ricorsivi su Internet. Rispondere solo a client interni (no open resolver). |

### Monitoring blue team
- **Query anomale**: sottodomini molto lunghi, alta entropia, alto volume verso un singolo dominio esterno → tunneling.
- **Nuovi domini mai visti** (DGA detection): malware con Domain Generation Algorithm genera centinaia di domini al giorno; quasi tutti NXDomain. Rilevabile con ratio NXDOMAIN.
- **Lookup PTR falliti in burst**: possibile recon interna.
- **Richieste AXFR dall'esterno**: tentativo di zone transfer da IP non autorizzati → alert immediato.
- Log DNS su SIEM: ogni query è un artefatto di rete → correlabile con alert EDR.

---

## Comandi pratici (lab)

```bash
# Verifica DNSSEC
dig example.com DNSKEY +dnssec
dig example.com A +dnssec              # cerca flag AD (Authenticated Data) nella risposta

# Controllare se un dominio ha DMARC
dig _dmarc.example.com TXT

# Controllare CAA (quali CA sono autorizzate)
dig example.com CAA

# Resolver locale (per vedere la cache del sistema)
# Linux: /etc/resolv.conf per il resolver; resolvectl status su systemd
resolvectl query example.com

# nslookup interattivo (Windows/Linux)
nslookup
> server 1.1.1.1
> set type=MX
> example.com

# Verifica reverse DNS di un IP
dig -x 8.8.8.8 +short
```

---

## Casi limite e troubleshooting

- **Cache locale corrotta**: `ipconfig /flushdns` (Windows), `sudo systemd-resolve --flush-caches` (Linux). Prima causa di "non risolve ma il sito funziona".
- **Split brain / DNS split-horizon mal configurato**: il resolver interno risponde diversamente da quello esterno. Causa: VPN che usa il resolver aziendale, ma la macchina fuori rete usa quello ISP → accessi che funzionano solo in ufficio.
- **CNAME loops**: A → B → A. Il resolver raggiunge il limite di redirect e risponde SERVFAIL. Catturarli con `dig +trace`.
- **TTL troppo basso**: ogni client ri-risolve ad ogni richiesta → carico abnorme sull'autoritativo. Non scendere sotto 300 s in produzione senza motivo.
- **Wildcard DNS e sottodomini**: un record `*.example.com → IP` risponde a qualsiasi sottodominio, anche quelli non previsti → superficie d'attacco (subdomain takeover impossibile ma facilita phishing con sottodomini convincenti).

---

## Domande da esame/colloquio

1. **Qual è la differenza tra query ricorsiva e iterativa, e chi le fa?** Il client fa una query *ricorsiva* al resolver ("risolvimi questo nome"). Il resolver interroga la gerarchia in modo *iterativo* (root → TLD → autoritativo) raccogliendo referral successivi. Il client non vede mai i referral intermedi.

2. **Cos'è DNSSEC e cosa NON fa?** DNSSEC aggiunge firme crittografiche (RRSIG) ai record DNS e una catena di fiducia (DS record) dalla root all'autoritativo. Garantisce **autenticità e integrità** dei record, ma **non cifra** le query: chi osserva il traffico vede comunque i nomi risolti. Per privacy serve DoH/DoT.

3. **Come funziona il DNS cache poisoning e come si mitiga?** L'attaccante inonda il resolver con risposte fasulle per indovinare l'ID di query (16 bit, spazio piccolo) prima della risposta legittima. Mitigazioni: DNSSEC (rende inutile la risposta falsa perché non verificabile), randomizzazione della porta sorgente UDP (aumenta l'entropia da 16 a ~32 bit), EDNS COOKIE.

4. **Cosa rivela un record TXT e perché interessa a un pentester?** SPF, DKIM, DMARC indicano la struttura dell'infrastruttura email (provider usati, relay, regole). Assenza di DMARC o policy `p=none` → dominio spoofabile per phishing. Record TXT possono anche contenere chiavi di verifica di servizi cloud (Google, Microsoft) → informazioni sull'infrastruttura del target.

5. **Cos'è un subdomain takeover e quando è sfruttabile?** Quando un CNAME punta a un servizio esterno (es. `shop.example.com → example.github.io`) che è stato dismesso ma il record non rimosso. L'attaccante registra `example.github.io` e può servire contenuto sotto `shop.example.com`, inclusi cookie di sessione (se non HttpOnly/Secure o su sottodominio condiviso).

6. **Perché il DNS tunneling funziona anche dietro firewall restrittivi?** I firewall permettono quasi sempre il traffico DNS (UDP/53) verso resolver autorizzati. `dnscat2`/`iodine` usano i sottodomini come canale dati: il traffico appare come normale risoluzione DNS verso un dominio controllato dall'attaccante. Il rilevamento richiede analisi comportamentale (lunghezza label, frequenza, entropia), non blocco di porta.

---

## Collegamenti
- [[HTTP e HTTPS]]
- [[Indirizzamento IP]]
- [[Modello TCP-IP]]
- [[Porte e Protocolli Comuni]]
- [[DHCP]]
- [[UDP]]
- [[TCP]]
- [[Enumerazione]]
- [[Ricognizione (Recon)]]
- [[Wireshark]]
- [[SIEM]]
- [[DoS e DDoS]]

## Fonti
- Cloudflare — What is DNS: https://www.cloudflare.com/learning/dns/what-is-dns/
- RFC 1034 — Domain Names Concepts: https://www.rfc-editor.org/rfc/rfc1034
- Wikipedia — Domain Name System: https://en.wikipedia.org/wiki/Domain_Name_System
- HackTricks — Pentesting DNS: https://book.hacktricks.xyz/network-services-pentesting/pentesting-dns
- Peterson & Davie — *Computer Networks: A Systems Approach* (cap. "Applications — Name Service / DNS": gerarchia, risoluzione ricorsiva/iterativa, caching): https://book.systemsapproach.org/
