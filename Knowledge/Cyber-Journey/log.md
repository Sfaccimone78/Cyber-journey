# Registro Wiki

Cronologia append-only di tutti gli eventi. Ogni voce inizia con `## [YYYY-MM-DD] <tipo> | <titolo>`
(grep-abile: `grep "^## \[" log.md | tail -5`). Tipi: `init` · `ingest` · `query` · `lint`.

---

## [2026-06-20] init | Creazione struttura wiki
Creata la struttura Wiki di LLM nella radice del vault: `WIKI_SCHEMA.md` (schema), `index.md`, `log.md`,
cartelle `Fonti/`, `Concetti/`, `Entita/`, `Sintesi/`, `Template/`. Pagine esempio e template
aggiunti. Appunti esistenti (crypto, `Network/`) dichiarati come concept page e catalogati in
`index.md`. Scope: tronco comune del piano (reti, linux, windows, crypto, web, tool, blue-team).
Nessuna fonte ancora ingerita.

## [2026-06-20] build | Generazione wiki completa (swarm)
Scritte **128 pagine** (84 concetti + 44 entità) tramite uno sciame di 8 agenti paralleli, uno per
area: Fondamenti/Carriera, Reti, Linux, Windows/AD, Crittografia, Web/OWASP, Metodologia/Tool,
Blue Team. Livello principiante, italiano, ogni pagina con frontmatter, esempio pratico, fonti reali
e cross-link `[[...]]`. `index.md` ricostruito come catalogo per area + viste Dataview. Pagine
crypto esistenti (`01. Base64`, `03. XOR`, ...) e `Network/` linkate, non riscritte.
Prossimo passo: lint per pagine orfane/contraddizioni, poi ingest delle prime fonti reali.

## [2026-06-20] refactor | Riorganizzazione per area + numerazione
Abolite le cartelle `Concetti/` ed `Entita/`. Le 128 pagine spostate in **9 cartelle d'area**
numerate (`00 Fondamenti` … `08 Risorse`); concetti ed entità ora convivono per area, il `tipo`
resta nel frontmatter. Ogni pagina rinominata con prefisso `NN ` in ordine d'apprendimento e dotata
di `aliases: ["<nome senza numero>"]` → i wikilink esistenti (senza numero) risolvono comunque,
zero link rotti. Ricreata `05 Web OWASP/10 Vulnerabilità Upload File.md` (persa per sync OneDrive).
Aggiunta una **MOC per area** (`00 — Mappa <Area>.md`) con elenco ordinato + navigazione prec/succ.
Pagine esempio spostate in `Template/`. `index.md` riscritto (mappe per area in testa, viste
Dataview corrette: `FROM` rimosso, filtro `WHERE tipo`). `WIKI_SCHEMA.md` aggiornato (struttura, naming,
regola alias). Appunti utente (`Crittografia/`, `Network/`, crypto root) **non** spostati.

## [2026-06-20] refactor | Integrazione appunti utente nelle aree
Integrati i 7 appunti personali nelle cartelle d'area (frontmatter + alias aggiunti, contenuto
intatto). **01 Reti**: `1. Rete Informatica...` e `2. Hardware di Rete` (da `Network/`) messi in
testa come `01`/`02` (cos'è una rete → hardware, prima di OSI); le 18 pagine reti shiftate a 03-20.
**03 Crittografia**: aggiunti in coda 5 appunti pratici CryptoHack (16-20): `16 Base64`,
`17 Bytes e Long`, `18 XOR`, `19 Aritmetica Modulare`, `20 Massimo Comune Divisore (GCD)` —
quest'ultimo era `Senza nome.md` (writeup GCD, non junk). Cartelle `Network/` e `Crittografia/`
(vuota) rimosse. MOC Reti/Crittografia rigenerate. `index.md` aggiornato (135 pagine totali).
Nota: `20 GCD` ha testo con artefatti OCR (es. `UN=A`) → candidato a pulizia manuale.

## [2026-06-20] lint | Fix MOC sincronizzazione aree
Aggiornati **9 MOC** (uno per area: 00 Fondamenti … 08 Risorse) per riflettere l'elenco reale
dei file in ogni cartella. Ogni MOC ora elenca tutte le pagine in ordine numerico (link via alias
senza prefisso) e include navigazione prec/succ + link a `index.md`. Script `fix_mocs.ps1` usato.
Prossimo: rewrite pagine bassa qualità (CVE/CVSS, SIEM, Malware Analysis, MITRE ATT&CK).

## [2026-06-20] lint | Audit completo + fix lint prioritari
Eseguito audit strutturale/qualità/lacune su 137 pagine. **Fix applicati:**
- **Nav MOC** (9 mappe): corretti 16 link prev/succ dal formato errato `[[00 - Mappa NN <Area>]]` al reale `[[00 — Mappa <Area>]]`.
- **Alias mancanti**: aggiunti su 9 pagine per risolvere ~22 wikilink (XSS, TLS/SSL, DDoS/DoS, Man-in-the-Middle/MITM, Reconnaissance/Recon, IP, CryptoHack-Modular-Math, "01. Base64", "03. XOR").
- **Encoding**: 3 pagine Fondamenti (`01 Cos'è`, `04 Vulnerabilità…`, `07 Difesa in Profondità`) ri-salvate UTF-8 + riparato mojibake diffuso nel corpo (`Ã¨`→è, `Ã `→à, ecc.).
- **Pagina nuova**: creata `05 Web OWASP/10 Vulnerabilità Upload File.md` (gap di numerazione 09→11); collegata in MOC Web e già citata in index/LFI/Burp.
- **Link minori ripuntati**: `[[Reti]]`/`[[Linux]]`→MOC d'area, `[[SYN Flood]]`→`[[DoS e DDoS]]`, `[[Sysinternals Streams]]` delinkato; rimosso `[[Massimo Comune Divisore]]` (inesistente) da index.
- Risultato verifica: 0 file non-UTF8, 0 mojibake, alias tutti risolti.
Nota: OneDrive (Files-On-Demand) blocca a tratti in lettura i file con accenti appena scritti — la pagina Upload è presente (3436 byte) ma può richiedere un momento di sync.
**Backlog prossimi step** (da report): cluster AD mancante (Responder/LLMNR, DCSync, Golden/Silver Ticket); normalizzare template appunti CryptoHack (Base64/Bytes/XOR); lacune Pivoting/Capabilities/IDS-IPS; ingest prime fonti reali (THM AD path, PortSwigger File Upload).

## [2026-06-20] lint | Normalizzazione appunti CryptoHack (qualità)
Riscritte a template standard le 3 pagine fuori-formato segnalate nel report (bottom-5 qualità):
`16 Base64`, `17 Bytes e Long`, `18 XOR`. Aggiunti titolo `#` e sezione `## In breve`, contenuto
riorganizzato in `Come funziona / Esempio pratico / Collegamenti / Fonti` mantenendo math, callout,
codice Python e wikilink originali. Corretto un **bug** nello snippet brute-force di XOR
(`decoded_string` vs `decoded`). Stato promosso `attivo` → `maturo`. Verifica: H1 + In breve presenti,
0 mojibake nel vault, pagina Upload persistente (22 file in 05 Web OWASP).

## [2026-06-21] ingest | Approfondimento pagine-hero (modalità ibrida)
Approfondite in profondità 13 "hero page" da conoscenza canonica + fonti reali (≈2-3x densità),
mantenendo frontmatter, alias e wikilink. Worked example, comandi reali, tabelle attacco/difesa.
Gruppi:
- Web/Metodologia (sessione precedente): `SQL Injection`, `Cross-Site Scripting (XSS)`, `Nmap`,
  `Privilege Escalation Linux`, `Subnetting`, `Kerberos`, `MITRE ATT&CK`.
- Reti/Linux: `Modello OSI` (incapsulamento/PDU, attacchi per layer, OSI vs TCP-IP),
  `TCP` (header, handshake+teardown, flow vs congestion, SYN flood, scan FIN/NULL/Xmas),
  `DNS` (ricorsiva vs iterativa, record NS/SOA/SRV/CAA, AXFR, recon, cache poisoning/tunneling/takeover),
  `Permessi Linux` (rwx su directory, bit speciali SUID/SGID/sticky, umask, ACL).
- Crypto/AD: `RSA` (attacchi Wiener/Håstad/Fermat, OAEP/PSS, CTF), `Funzioni di Hash`
  (birthday attack, hash≠password), `Active Directory` (kill chain AD, BloodHound).
- Lateral/Blue: `Pass-the-Hash` (NTLM challenge-response, DCSync, vs PtT), `Enumerazione`
  (loop scan→enum, per-servizio, web/SMB), `Incident Response` (NIST vs SANS, volatilità, GDPR 72h).
Lint post-scrittura: 0 link rotti (esclusi falsi positivi da escape `\|` nelle table Obsidian).
Sciolto `CryptoHack` (nessuna pagina dedicata) in testo piano nella pagina RSA.

## [2026-06-21] lint | Fix #4 — link penzolanti + pagina Upload persa
Audit vault: 167 pagine, 0 orfane, 0 stub, 0 fonti:0 (struttura sana).
- Link penzolanti `SYN Flood` / `Massimo Comune Divisore` / `Sysinternals Streams`: risultano SOLO
  in log.md (documentazione di fix passati) → falsi positivi, già risolti nelle pagine. Nessuna azione.
- `05 Web OWASP/10 Vulnerabilita Upload File.md`: RI-cancellata da sync OneDrive (gap 09→11).
  Ricreata con nome-file ASCII + alias accentato e ASCII (entrambe le forme linkate da index/Burp/LFI).
  File verificato su disco (3570 byte, non placeholder) e **pinnato** `attrib +P` (always keep on device)
  per fermare la dehydration/cancellazione ricorrente.

## [2026-06-21] ingest | Approfondimento cluster Vulnerabilità Web OWASP
Approfondite 9 pagine del cluster OWASP (compagne di SQLi/XSS/Upload già fatte), modalità ibrida:
- `OWASP Top 10` (tassonomia rischi vs vuln, mappa A01-A10→pagine, cambi 2017→2021, WSTG/ASVS).
- `CSRF` (3 condizioni necessarie, CSRF vs XSS, bypass token/Referer/SameSite, PoC Burp).
- `Broken Access Control e IDOR` (authn vs authz, IDOR/verticale/mass-assignment, test con 2 account+Autorize).
- `Command Injection` (metacaratteri, blind time-based + OAST, reverse shell, subprocess shell=False).
- `SSRF` (metadati cloud IMDSv1/v2, gopher/file, blind OAST, bypass 127.1/decimale/DNS rebinding).
- `XXE` (in-band/blind OOB con evil.dtd, XXE→SSRF, disallow-doctype-decl per linguaggio).
- `File Inclusion (LFI e RFI)` (php://filter, data://, log poisoning, LFI+upload, file utili Win/Linux).
- `SSTI` (detect→identify→exploit, {{7*7}} per motore, RCE Jinja2/Twig/Freemarker, tplmap).
- `Insecure Deserialization` (magic methods per linguaggio, pickle RCE, gadget chain/ysoserial, HMAC).
Aggiunti alias mancanti (CSRF, SSRF, IDOR, LFI/RFI/Path Traversal, XXE, SSTI...). Lint: 0 link rotti.

## [2026-06-21] build | Approfondimento esperto + nuove aree (swarm 8 agenti)
Sciame di **8 agenti paralleli**, partizionati per area (zero collisioni sui file; index/log/Mappe
consolidati a posteriori dal coordinatore). Obiettivo: portare le pagine-chiave da `maturo` a
**livello esperto operativo** (sezioni aggiunte: meccanismo interno/byte-level, casi limite,
walkthrough end-to-end, evasion/OPSEC, **detection engineering** con Event ID + query SPL/KQL +
Sigma + MITRE T-id, troubleshooting, domande da colloquio). Frontmatter aggiornato, `fonti:`
incrementate, wikilink e fonti reali per ogni pagina.
- **23 pagine approfondite:**
  - AD (04): `Active Directory` (catena anonimo→Domain Admin), `Privilege Escalation Windows`,
    `Pass-the-Hash`, `BloodHound`.
  - Web (05): `SQL Injection` (WAF bypass, SQLi→RCE, sqlmap), `XSS`, `Command Injection`, `Burp Suite`.
  - Linux (02): `Privilege Escalation Linux` (checklist 11 vettori), `SUID e SGID`, `sudo`, `Bash Scripting`.
  - Metodologia (06): `Nmap` (packet-level), `Reverse Shell e Bind Shell`, `Enumerazione`, `Metasploit`.
  - Blue Team (07): `Log Analysis`, `Detection di Attacchi`, `MITRE ATT&CK`, `Splunk`.
  - Crypto (03): `RSA` (Wiener/Håstad/Fermat...), `AES` (modi+attacchi), `Funzioni di Hash`, `TLS e SSL`.
- **10 pagine nuove:**
  - Nuova area **09 Python** (7 pagine): Mappa + `Python per la Sicurezza`, `Socket e Port Scanner`,
    `Requests e HTTP`, `Parsing con os e re`, `Automazione Offensiva`, `pwntools Base` (script
    funzionanti commentati + esercizi). Colma il buco Python della Fase 1 del piano.
  - Metodologia (06): `Pivoting`, `Port Forwarding`, `Reporting Pentest` (gap Fase 3A eJPT).
- Consolidato: `index.md` (10 aree, sezione Python, 18-20 Metodologia), Mappa Metodologia (18-20),
  Mappa Python e Risorse (navigazione).
- **⚠️ ALERT OneDrive:** la cartella **`08 Risorse`** (6 file: Mappa, TryHackMe, HackTheBox, HackTricks,
  GTFOBins, ExploitDB), presente a inizio sessione, è **sparita dal disco** durante la sessione
  (de-idratazione/cancellazione OneDrive — stesso bug ricorrente già loggato). Nessun agente l'ha
  toccata. **Da recuperare dal cestino OneDrive / onedrive.com** prima di rigenerarla. Finché manca,
  i wikilink `[[GTFOBins]]`, `[[TryHackMe]]`, `[[HackTheBox]]`, `[[HackTricks]]`, `[[ExploitDB]]` sono penzolanti.
- **Backlog lint (wikilink nuovi senza pagina, candidati a creazione):** `[[DCSync]]`, `[[NTLM Relay]]`,
  `[[NetExec]]`, `[[bloodyAD]]`, `[[PrinterBug]]`, `[[WinPEAS]]`/`[[LinPEAS]]`, `[[PowerUp]]`,
  `[[Meterpreter]]`, `[[msfvenom]]`, `[[EDR e XDR]]`, `[[Capabilities]]`.

## [2026-06-22] lint | Verifica grafo + 13 pagine nuove + cleanup 08 Risorse
Verifica integrità del grafo (script temporaneo): **185 file**, ~2388 link, 409 target unici →
**0 link rotti reali**. I 25 dangling residui sono tutti attesi: voci storiche di `log.md`,
esempi di sintassi in `WIKI_SCHEMA.md`, e falsi positivi (POSIX `[[:space:]]` e bash `[[ $X == y ]]` nei
code block, pipe escapata `\|` nelle tabelle Obsidian = link validi). Orfane: solo `Nota etica`
e `Piano_cybersecurity` (attese).
- **13 pagine nuove** create per chiudere il backlog del build precedente:
  - AD (04): `DCSync`, `NTLM Relay`, `NetExec`, `bloodyAD`, `PrinterBug e Coercizione`
    (alias PrinterBug/PetitPotam/Coercizione), `PowerUp`, `Responder` (LLMNR/NBT-NS poisoning).
  - Linux (02): `Capabilities Linux`.
  - Metodologia (06): `PEAS (WinPEAS e LinPEAS)` (alias PEAS/WinPEAS/LinPEAS), `Meterpreter`, `msfvenom`.
  - Blue Team (07): `EDR e XDR` (alias EDR/XDR).
  - Fondamenti (00): `Certificazioni Cybersecurity` (slot 10, era citata in index/MOC ma il file
    non esisteva → 4 link penzolanti risolti).
- **Mappe d'area aggiornate** (04, 02, 07, 06, 00) + `index.md` con le nuove pagine; sync 04 Windows
  (mancavano anche NTLM/Mimikatz/BloodHound/LAPS) e 07 Blue (Sysmon/YARA/Sigma/Volatility) e 00
  Fondamenti (Social Eng/Risk Mgmt/IAM).
- **08 Risorse — chiusura:** l'utente conferma la **cancellazione intenzionale** (non recupero dal
  cestino). Rimossa la sezione `08 Risorse` da `index.md` e dalla lista mappe; navigazione MOC
  ricucita: Blue Team → **09 Python**, Python ← **07 Blue Team**. I wikilink alle risorse morte
  (`TryHackMe`, `HackTheBox`, `HackTricks`, `GTFOBins`, `ExploitDB`) e `UAC` **scollegati a testo
  semplice** (38 sostituzioni su 25 file, non distruttivo). NB: `GTFOBins` (13 ref) e `TryHackMe`
  (19 ref) erano molto usati — se servono di nuovo come pagine, ricrearle è banale.

## [2026-06-22] lint | Controllo integrità completo
Lint del grafo (185 file, 230 target). Esito:
- **Link rotti reali: 0.** Residui = solo falsi positivi attesi (nomi-file completi `[[00 — Mappa X]]`
  nelle nav MOC = link Obsidian validi; POSIX/bash nei code block; voci storiche di `log.md`/`WIKI_SCHEMA.md`).
- **Orfane: 0 reali** (solo `Nota etica` e `Piano_cybersecurity`, attese).
- **Stub: 0.**
- **Pagine poco collegate (1 solo backlink) → rinforzate:** `CORS Misconfiguration`, `Clickjacking`,
  `Server-Side Template Injection (SSTI)`, `Crittografia a Curve Ellittiche (ECC)`. Erano presenti
  solo nel MOC d'area e **assenti da `index.md`**: aggiunte all'index + cross-link da pagine
  correlate (XSS↔CORS/Clickjacking, CSRF↔Clickjacking, Command Injection↔SSTI, Crittografia
  Asimmetrica↔ECC). Ora ≥2 backlink ciascuna.
- **Gap suggeriti (non creati):** AD — `Golden/Silver Ticket`, `Delegazione (Unconstrained/Constrained)`,
  `RBCD` (citato in [[bloodyAD]] senza pagina propria). Candidati per la prossima sessione.

## [2026-06-22] build | Approfondimento esperto area 01 Reti + mappa Excalidraw
Portate tutte le **23 note** di `01 Reti` a livello esperto consistente (meccanismo byte/packet-level,
header, CLI/[[Wireshark]] pratici, attacchi+detection+difesa, casi reali). Riscritte in profondità:
`Rete Informatica`, `Hardware di Rete`, `Modello TCP-IP`, `Indirizzamento IP`, `MAC Address`, `UDP`,
`ICMP`, `Three-Way Handshake`, `DHCP`, `NAT`, `HTTP e HTTPS`, `Modello Client-Server`, `VPN`,
`Wireshark`. Estese: `Modello OSI` (lettura Wireshark per livello), `Subnetting`, `ARP` (insicurezza
by-design + detection), `Porte e Protocolli` (porte AD/Windows + banner grabbing), `DNS`, `TCP`, `SSH`
(handshake + 3 tipi di forwarding), `MITM` (on/off-path, vettori per livello, catena Responder→relay),
`DoS e DDoS` (reflection/amplification + detection). Tutti `aggiornato: 2026-06-22`, fonti reali.
- **Nuova mappa concettuale Excalidraw**: `01 Reti/00 — Mappa Concettuale Reti (Excalidraw).md`
  (frontmatter `excalidraw-plugin: parsed` → il plugin la apre come disegno anche senza doppia
  estensione). **23 nodi cliccabili** (link alle note) + **33 archi** etichettati, layout a 5 colonne
  per cluster (fondamenti/indirizzamento/trasporto/servizi/sicurezza). Generata via script temporaneo
  (poi rimosso); JSON Excalidraw validato (23 rect, 33 arrow, 35 text). Linkata dalla [[00 — Mappa Reti]].
- **Integrità**: 0 link rotti reali introdotti (verificato). Fix link `[[Reconnaissance]]`→`[[Ricognizione (Recon)]]`
  in Indirizzamento IP. Aggiornati MOC Reti (link alla mappa visuale) e `index.md` (aggiunti
  `SSH`, `Man-in-the-Middle (MITM)`, `DoS e DDoS` alla sezione 01 Reti).

## [2026-06-22] lint | Lint completo + caccia ai link fantasma
Scansione integrità su 181 note (parser stretto, ignora code-block come Obsidian). Report in
`_lint-report.md`. **Esiti:** link fantasma reali = **1** (`[[Rete Informatica]]` nella mappa
Excalidraw Reti) → risolto aggiungendo l'alias `Rete Informatica` a
`[[Rete Informatica e i suoi Componenti]]`; ri-scan = **0 nodi fantasma**. Chiariti i falsi allarmi:
`[[Reverse Shell e Bind Shell]]` esiste (linkato 30+ volte); i `[[GTFOBins]]`/`[[TryHackMe]]`/
`[[SYN Flood]]` stanno in `log.md` dentro backtick (non sono nodi). Orfani = 1 (`overview.md`, ok).
Identificati **candidati nuove pagine** (chisel 48×, proxychains 35×, socat 25×, Shodan, C2…) e
**cross-link mancanti** (`[[LetsDefend]]`, `[[MITRE ATT&CK]]`, `[[Sysmon]]`…). Prossimo step: Fase 2
= approfondire le pagine corte dei Fondamenti.

## [2026-06-22] lint | Approfondimento Fondamenti (Fase 2)
Riscritte in profondità le 9 note corte dell'area `00 Fondamenti` (erano 186-277 parole, definizioni
da glossario → ora 532-701 parole, meccanismi reali): `Cos'è la Sicurezza Informatica`, `Triade CIA`,
`Vulnerabilità Exploit e Minaccia`, `Superficie di Attacco`, `CVE e CVSS`, `Difesa in Profondità`,
`La Cyber Kill Chain`, `Pentester vs SOC`, `Social Engineering e Phishing`. Per ognuna: spiegazione
dei meccanismi (es. vector string CVSS AV/AC/PR/UI/S/C/I/A, matrice Detect/Deny/Disrupt della Kill
Chain, controlli preventivi/detettivi/correttivi), esempi concreti, sezioni `## Collegamenti`/`## Fonti`
e nuovi cross-link (aggiunti tra l'altro [[MITRE ATT&CK]], [[Sysmon]], [[EDR e XDR]], [[IAM e Zero Trust]]).
Aggiunto alias `Pentester vs SOC` e `Rete Informatica`. Verifica: ri-scan link → introdotto e subito
corretto 1 fantasma (`[[01 — Mappa Reti]]`→`[[Modello OSI]]`); stato finale **0 nodi fantasma**.

## [2026-06-22] ingest | Black Hat Python (cap. 2) → area 09 Python
Ingerita la fonte `blackhatpython.pdf` (Justin Seitz, No Starch 2015, Py2). Focus **cap. 2 "The
Network: Basics"**, codice **modernizzato a Python 3**. Scoperta: le pagine naturali ([[Reverse Shell e Bind Shell]] 171 righe, [[Pivoting]] 224, [[netcat]], [[Socket e Port Scanner]]) erano **già profonde**
→ niente duplicazione. Creata invece pagina nuova **[[Tool di Rete in Python]]** (`09 Python/07`) che
copre il gap reale: netcat-replacement (`bhpnet`), proxy TCP intercettante con hexdump, SSH/reverse
tunnel con Paramiko — con la tesi living-off-the-land (MITRE T1059.006). Sezioni profonde: meccanismo
`socket`, 3 tool completi, detection engineering, troubleshooting, domande da colloquio. Creata pagina
fonte **[[Fonte - Black Hat Python]]** con mappa capitoli e flag obsolescenza (Py2/2015; esiste 2ª ed.
2021 in Py3). Aggiornati: mappa Python, `index.md` (riga 09 Python). Cross-link di ritorno aggiunti in
`netcat` e `Pivoting`. Prossimi candidati alto valore dal libro: cap. 6 (Burp), 7 (C2), 10 (priv-esc Win).

## [2026-06-22] ingest | Approfondimento Wireshark + Nmap (attacco e difesa)
Richiesta: guida approfondita su Wireshark e Nmap per attacco/difesa. Stato pre: Nmap già maturo
(211 righe, copre scan/NSE/evasion/detection); Wireshark più corto (67 righe, inquadrato come analisi
generica). Interventi:
- **[[Wireshark]]** (01 Reti/20): riscritta ed espansa (~210 righe). Aggiunte sezione **prerequisito
  posizione** (switch/SPAN/MITM/monitor mode), **USO OFFENSIVO** (furto credenziali in chiaro con
  Follow Stream + tshark, session hijacking cookie/token, export objects file/malware, cattura
  handshake WPA2 EAPOL→hashcat, recon passivo) e **USO DIFENSIVO** (triage pcap in IR, firme di
  port-scan Nmap, ARP poisoning, reverse shell/C2 beaconing, esfiltrazione/DNS tunneling, estrazione
  IOC, JA3), walkthrough end-to-end "pcap sospetto", troubleshooting e Q&A colloquio. tag +blue-team.
- **[[Nmap]]** (06/09): aggiunta sezione **NMAP PER IL DIFENSORE** (asset inventory, `ndiff` per change
  detection, verifica patch, monitoraggio schedulato). Cross-link a [[Wireshark]] e [[Superficie di Attacco]].
- Spunto: la repo GitHub `bst04/CyberSources` (awesome-list) non ingerita come concetto — è risorsa
  reference, non materiale didattico approfondibile.
Verifica link: nuovi ghost-link **[[Zeek]]** e **[[Suricata]]** (sensori NDR/IDS) → candidati pagina
da creare (citati anche nella Detection Engineering di Nmap). Resto dei link risolve.

## [2026-06-22] ingest | Approfondimento Reti — ondata 1: i 3 pilastri (OSI, IP, Subnetting)
Richiesta: approfondire Linux e Sistemi e Reti in modo ultra-dettagliato. Scelta utente: Reti prima,
poche pagine ultra-profonde per ondata. Stato pre: pagine fondamentali Reti ferme a 50-90 righe
(glossario), mentre quelle security erano già profonde (Wireshark 250, ecc.). Ondata 1 = i 3 pilastri
portanti su cui tutto si collega, riscritti a livello Nmap/Priv-Esc:
- **[[Modello OSI]]** (01 Reti/03): + principio di astrazione, cosa fa DAVVERO ogni livello (hub/switch/
  router per livello), incapsulamento con byte degli header + MTU/MSS, walkthrough "apri https://", scala
  di troubleshooting dal basso, Q&A esame. ~150 righe.
- **[[Indirizzamento IP]]** (01 Reti/05): + conversione bin/dec, decisione "stessa rete o gateway" (AND
  bit-a-bit con esempio), classi A-E e perché è nato il CIDR, header IPv4 (TTL/protocol/spoofing),
  IPv6 serio (link-local/GUA/ULA, SLAAC+EUI-64, mitm6), TTL fingerprinting, Q&A. ~150 righe.
- **[[Subnetting]]** (01 Reti/06): + tabella CIDR completa, metodo numero-magico con 3 esercizi svolti,
  network/broadcast in binario, le due domande inverse (N subnet vs N host), VLSM, supernetting/
  aggregazione, subnet vs wildcard mask, cenni IPv6, esercizi autovalutazione con soluzione, Q&A. ~170 righe.
Nessuna pagina nuova → index/MOC invariati. Link verificati (nessun nuovo ghost). Prossime ondate Reti:
TCP/IP+ARP+TCP (lo stack di consegna), poi DNS/DHCP/NAT (i servizi), poi HTTP/TLS/VPN.

## [2026-06-22] ingest | Approfondimento Reti — ondata 2: stack di consegna (TCP/IP, ARP, TCP)
Seconda ondata ultra-profonda (Reti). Riscritte:
- **[[Modello TCP-IP]]** (01 Reti/04): + storia DoD/ARPANET, principio end-to-end, modello a clessidra
  (narrow waist IP), hop-by-hop vs end-to-end (MAC riscritti a ogni hop, IP invariati, TTL cala),
  demultiplexing (EtherType/IP proto/porta), troubleshooting per livello, Q&A. ~120 righe.
- **[[ARP]]** (01 Reti/08): + formato pacchetto (opcode 1/2), gratuitous ARP / probe / proxy ARP, NDP
  come equivalente IPv6, stati cache (ip neigh), walkthrough poisoning con bettercap + ip_forward,
  rilevamento (arpwatch, duplicate-address), difesa (DAI+DHCP snooping, port-security, segmentazione),
  troubleshooting, Q&A. ~120 righe.
- **[[TCP]]** (01 Reti/09): + header campo-per-campo con diagramma a bit, i 6 flag, seq/ack con esempio
  numerico, fast retransmit/SACK, flusso vs congestione (slow start/AIMD/CUBIC), macchina a stati
  (TIME_WAIT/CLOSE_WAIT con significato diagnostico), sicurezza estesa (RST injection, SYN flood+cookies,
  ISN prediction), Q&A. ~140 righe.
Nessuna pagina nuova. Evitato 1 ghost-link (`IDS e IPS` inesistente → reso testo). Resto link OK.
Prossima ondata 3 (servizi): DNS + DHCP + NAT.

## [2026-06-23] ingest | Approfondimento Reti+Linux — ondate 3-6 (sciame di 9 agenti)
Completato lo sciame di subagent (sonnet) lanciato per portare a livello ULTRA tutte le pagine
fondamentali rimaste di Reti e Linux. File disgiunti per agente → nessun conflitto. Ogni pagina ora ha
meccanismo a basso livello, esempi/comandi reali, walkthrough, sezione attacco+difesa, troubleshooting,
"Domande da esame/colloquio". Risultati (righe prima→dopo):

RETI
- [[DNS]] 81→194 · [[DHCP]] 52→188 · [[NAT]] 53→194  (servizi; DORA, conntrack/PAT, DNSSEC/DoH, mitm6)
- [[HTTP e HTTPS]] 83→183 · [[SSH]] 65→173 · [[VPN]] 59→170  (TLS1.3, arch. SSH, IPsec/IKE, leak VPN)
- [[UDP]] 69→266 · [[ICMP]] 58→295 · [[Three-Way Handshake TCP]] 53→268 · [[Porte e Protocolli Comuni]] 85→291
- [[Rete Informatica e i suoi Componenti]] 70→155 · [[Hardware di Rete]] 58→175 · [[MAC Address]] 62→160 · [[Modello Client-Server]] 59→180
- [[Man-in-the-Middle (MITM)]] 64→175 · [[DoS e DDoS]] 67→205  (reflection/amplification, MITRE, detection)

LINUX
- [[Comandi Linux di Base]] 72→200 · [[Filesystem Linux]] 72→195 · [[Pipe e Redirezione]] 83→210 · [[OverTheWire Bandit]] 69→215
- [[Utenti e Gruppi Linux]] 86→185 · [[Permessi Linux]] 82→200 · [[Variabili d'Ambiente]] 88→210  (shadow/hash, ACL/umask, PATH hijack, LD_PRELOAD)
- [[Processi Linux]] 85→190 · [[Cron e Job Pianificati]] 99→190 · [[Capabilities Linux]] 67→195  (/proc, systemd timers, cap_setuid)
- [[grep]] 75→254 · [[find]] 77→295 · [[awk]] 72→305 · [[sed]] 75→325  (regex, log analysis, SUID hunt)

Più le 6 pagine fatte a mano nelle ondate 1-2 (OSI, IP, Subnetting, TCP-IP, ARP, TCP). Totale aree
Reti+Linux ora interamente a livello ultra. Lint link post-sciame: 0 ghost reali nelle pagine (i 64
"unresolved" sono falsi positivi: regex `[[:space:]]`, test bash `[[ ]]`, alias-in-tabella `\|`, esempi in
WIKI_SCHEMA.md/template, candidati esterni GTFOBins/TryHackMe/Zeek/Suricata). index/MOC invariati (nessuna
pagina nuova, solo espansioni). Candidati nuove pagine emersi: Zeek, Suricata, fail2ban, GTFOBins, ZTNA.

## [2026-06-23] query | Riorganizzazione per principianti e nuovi template
Riorganizzata la wiki per uno studente principiante che parte da zero:
- Creato **00 — Home.md** (mappa centrale per principianti).
- Creati due nuovi template in **Template/**: `template-teoria-base.md` (appunti teorici base con analogie) e `template-lab-base.md` (laboratori base es. Bandit).
- Creata la nota **06 Metodologia e Tool/24 Strumenti da studiare in futuro.md** come parcheggio per i tool avanzati.
- Creata la nota **01 Reti/24 Ping e Traceroute.md** per coprire i due strumenti di diagnostica basilari di rete.
- Riscritto **Piano_cybersecurity.md** (v3) per focalizzarsi sui fondamenti (Sistemi, Reti, Sicurezza Base) mettendo in pausa i temi avanzati (ADCS, Pivoting, Forensics).
- Aggiornati **index.md**, **01 Reti/00 — Mappa Reti.md** e **06 Metodologia e Tool/00 — Mappa Metodologia e Tool.md** con i nuovi link.

## [2026-06-23] query | Creazione Glossario degli Acronimi
- Creata la nota **00 Fondamenti/14 Glossario degli Acronimi.md** come dizionario di riferimento rapido per principianti.
- Aggiornati **index.md** e **00 Fondamenti/00 — Mappa Fondamenti.md** per collegare la nuova nota.

## [2026-06-23] query | Analisi della Wiki e creazione template IPO
- Eseguita un'analisi accurata e profonda della Wiki (Gap Analysis, MOC avanzate, Portfolio e IPO Workflow), salvata nell'artifact `wiki_analysis.md`.
- Creato il file template `Template/template-lab-ipo.md` nel workspace per supportare il nuovo workflow laboratoriale basato sul modello Input-Process-Output.

## [2026-06-26] ingest | Fusione wiki/ → wiki root (merge completo, niente duplicati)
Fusa la seconda wiki di ricerca (`wiki/`, 112 file, schema separato, topic-based) dentro la wiki root area-based, sotto un unico schema (WIKI_SCHEMA.md). Eseguito con sub-agent in parallelo (ondate A import, B merge/dedup, C consolidamento, D cleanup). Snapshot di sicurezza in commit `c5d3713`.
- **Aree nuove**: **08 Sistemi Operativi** (7 concept: Processi, Scheduling, Concorrenza e Thread, Memoria Virtuale, Filesystem, I/O e Storage, Virtualizzazione + MOC) e **10 Algoritmi e Strutture Dati** (19 concept + MOC) — domini assenti in root, importati interi.
- **Fonti** (7 nuove pagine `tipo: fonte`): Algorithms (Erickson), Open Data Structures, Crypto 101, The Linux Command Line, OWASP Top 10, Security Engineering, OSTEP.
- **Sintesi** (9 nuove): Big-O Cheatsheet, Da problema ad algoritmo, Mappa della Crittografia, Linux Essentials, Matrice Attacco-Difesa, Roadmap di Apprendimento, Arsenale Tool, Lo stack di rete, I tre pezzi dell'OS.
- **Merge/dedup overlap** (root canonica, travaso sezioni/fonti uniche, niente doppioni):
  - **03 Crittografia**: arricchite RSA/AES/Funzioni di Hash/Diffie-Hellman/ECC/XOR/TLS; create Modi Operativi, Stream Cipher, MAC e HMAC, AEAD, Crittografia Post-Quantistica, Padding Oracle Attack, GPG, Attacchi Crittografici.
  - **02 Linux**: arricchite Comandi base/Filesystem/Permessi/Processi/Pipe e Redirezione/Bash Scripting; create Gestione Pacchetti, Strumenti di Rete CLI, Vim e Nano; arricchita 01 Reti/SSH.
  - **01 Reti**: arricchite OSI/TCP-IP/MAC/TCP/UDP/DNS/HTTP-HTTPS/NAT/Wireshark; create Routing IP, Firewall, Socket Programming.
  - **Sicurezza** spalmata: arricchite Triade CIA, Social Engineering, SQLi, Command Injection, XSS, SSRF, Broken Access Control, Autenticazione, Security Misconfiguration, OWASP Top 10, Metodologia del Pentest, Analisi Malware, PortSwigger; create Threat Modeling, Secure Coding (00), Cryptographic Failures, Componenti Vulnerabili, Insecure Design, Logging e Monitoring Failures (05), Metodologia CTF, Privilege Escalation (Concetti), Attacchi di Rete (06). Aggiunti callout `[!note]` sulla numerazione OWASP 2021 vs 2025 dove le fonti divergevano.
- Aggiornati **index.md**, **overview.md** e le MOC delle aree toccate (00/01/02/03/05/06 + le 2 nuove). Convertiti tutti i wikilink `[[concept-*]]` → alias italiani; 0 link vecchio stile residui fuori da `wiki/`.
- **Cleanup**: rimossa la cartella `wiki/` e il suo schema obsoleto; `PROMPTS_AGENTI.md` mantenuto come riferimento.

## [2026-06-26] lint | Controllo integrità post-fusione
Lint automatico (script) su 260 file della wiki fusa.
- **Link rotti reali**: ~33 target distinti (~180 occorrenze), tutti da pagine importate in `Fonti/` e `Sintesi/` (e qualche pagina `08 SO`) che usano i vecchi titoli `wiki/` non allineati agli alias root (es. `[[TLS/SSL]]`→TLS e SSL, `[[Diffie-Hellman]]`→Scambio di Chiavi Diffie-Hellman, `[[Dijkstra]]`→Algoritmo di Dijkstra, `[[Concetti dei Sistemi Operativi]]`→I tre pezzi dell'OS).
- **Alias duplicati**: `NTLM` (rivendicato anche da Pass-the-Hash) e `OWASP Top 10` (collisione 05 page vs Fonte) — quest'ultima fa apparire orfana la hub 05 OWASP Top 10.
- **Falsi positivi**: link in tabella con pipe-escape `\|` (validi in Obsidian); voci storiche in `log.md` (Zeek/Suricata/IDS); ref esterno `[[Piano_cybersecurity]]`.
- **Gap**: `[[Tool di Rete in Python]]` citato 9 volte ma senza pagina (candidata in 09 Python).
- Fix proposti: aggiungere i vecchi nomi come alias alle pagine canoniche (risolve i link in blocco) + correggere le 2 collisioni.

## [2026-06-26] lint | Fix link rotti — alias batch + dedup collisioni
- +29 alias "vecchio-nome" su 28 pagine canoniche (TLS/SSL, Funzioni Hash, Diffie-Hellman, Curve Ellittiche, Permessi dei File, Scripting/Shell e Bash, Alberi Binari, Dijkstra, Bellman-Ford, Array e Linked List, Stack e Queue, IP Routing, Ordinamento, Block Cipher e AES, Ethernet e MAC, XOR e One-Time Pad, Anatomia Pacchetto→Wireshark, Processi e Job Control, MCD→Aritmetica Modulare, Injection→SQL Injection, ecc.).
- Rimosso alias "NTLM" da Pass-the-Hash (collisione con pagina NTLM).
- Rinominato alias "OWASP Top 10" della fonte → "Fonte OWASP Top 10" (sblocca hub 05 OWASP Top 10).
- Link rotti: 289 → 128 (-161, ~56%). Residui: pagine mancanti reali (Tool di Rete in Python, Malware, Penetration Testing, Zeek/Suricata, ecc.) + falsi positivi (snippet codice, placeholder).

## [2026-06-26] ingest | Stub 09 Python/07 Tool di Rete in Python
- Creata pagina stub (netcat-replacement, proxy TCP intercettante, tunnel/port forwarding) da [[Fonte - Black Hat Python]]. Risolve 10 link rotti. Mappa Python e index.md gia la referenziavano.

## [2026-06-26] ingest | Stub Malware + Penetration Testing
- 00 Fondamenti/17 Malware (tassonomia: virus/worm/trojan/ransomware/RAT/rootkit/botnet; rimanda a [[Analisi Malware di Base]]).
- 06 Metodologia e Tool/28 Penetration Testing (ombrello: black/grey/white box, vs VA/Red Team, fasi; rimanda a [[Metodologia del Pentest]]).
- Mappe d'area aggiornate. Risolve ~11 link rotti.

## [2026-06-26] ingest | Stub Zeek + Suricata
- 07 Blue Team/20 Zeek (NSM behavioral, log-centric) e 21 Suricata (IDS/IPS a firme). Si linkano a vicenda + tabella confronto. Mappa Blue Team aggiornata.

## [2026-06-26] ingest/lint | Stub GTFOBins + alias coda pagine mancanti
- 02 Linux/22 GTFOBins (entita, risorsa privesc Unix). Mappa Linux aggiornata (+ voci 19-21 mancanti).
- Alias: "Authentication Failures"->Autenticazione e Gestione Sessioni; "PortSwigger Labs"->PortSwigger Web Academy; "Web Hacking"->OWASP Top 10; "SYN Flood"->DoS e DDoS.

## [2026-06-26] ingest | Stub TryHackMe + HackTheBox
- 06 Metodologia e Tool/29 TryHackMe, 30 HackTheBox (piattaforme pratica). Mappa aggiornata. Alias "Tool di Rete"->Strumenti di Rete CLI.

## [2026-06-26] lint | Pulizia: rimosso PROMPTS_AGENTI.md obsoleto
- Eliminato PROMPTS_AGENTI.md (scaffolding bootstrap della vecchia wiki/, ormai assorbita; referenziava struttura morta wiki/linux/, concept-*.md, tag `sicurezza`). -23 link rotti.
- Verificato: nessuna wiki/ residua, niente schema obsoleto residuo, niente backup .bak/.original. blackhatpython.pdf gia spostato in Risorse/.
- Link rotti: 79 -> 56 (residui = placeholder in WIKI_SCHEMA.md/Template + single-ref minori, non junk).

## [2026-06-26] ingest/lint | Stub HackTricks + ExploitDB; fix artefatti log
- 06 Metodologia e Tool/31 HackTricks (cheat-sheet pentest, citato ~60 pagine in testo piano) e 32 ExploitDB (archivio exploit + searchsploit). Mappa aggiornata.
- CryptoHack: nessuna pagina/alias necessari (il ref "Mathematics (Modular Math)" risolve gia su Aritmetica Modulare; il `CryptoHack` nudo era solo in log dentro backtick).
- Fix log: link [[Reverse Shell e Bind Shell]] spezzato su due righe ricongiunto.

## [2026-06-26] ingest | Sciame agenti: +4 aree expert, 10 stub completati
- Sciame di 5 agenti paralleli (isolati per cartella) per colmare i gap dell'analisi.
- **Stub completati** (10 -> maturo, con fonti reali, ## Lab, nota etica): Malware, GTFOBins, Penetration Testing, TryHackMe, HackTheBox, HackTricks, ExploitDB, Zeek, Suricata, Tool di Rete in Python.
- **Nuove aree expert** (fase 3-4): `11 Cloud Security` (10), `12 AppSec Avanzato` (11), `13 Reverse Engineering e Exploit Dev` (11), `14 DFIR e Detection Engineering` (11). Ogni pagina: meccanismo + comandi/payload reali + ## Lab + fonti autorevoli.
- 2 agenti (13, 14) bloccati dal watchdog dopo aver scritto quasi tutto: completate a mano le pagine mancanti `10 Heap Exploitation` e `10 Threat Intelligence (Diamond Model, Pyramid of Pain)`.
- index.md aggiornato (nav + 4 blocchi aree avanzate). Analisi salvata in `Sintesi/Analisi e Roadmap Expert.md`.
- Lint: ricongiunti 3 wikilink spezzati su due righe nelle nuove aree. Link rotti residui = marker di pagine future (Malware Analyst, OpenVAS, Logging e Monitoraggio, ecc.).

## [2026-06-26] lint | Lint completo: 0 link rotti
Risolti tutti i link rotti reali (da ~14 distinti a 0). Falsi positivi confermati e ignorati:
pipe escapato in tabelle (`\|`), test bash `[[ ]]`, regex POSIX `[[:space:]]`, placeholder template/schema.
- Alias nome-area aggiunti a 6 MOC: Reti, Linux, Blue Team, Python, Windows e AD, Algoritmi e Strutture Dati
  (ora `[[Reti]]`, `[[09 Python]]`, ecc. risolvono sulla mappa d'area).
- Alias `Logging e Monitoraggio` su `Log Analysis Avanzata e Correlazione`.
- Fix link contestuali: `Malware Analyst` → `Malware Analysis (statica e dinamica)`; `Bash e Scripting` → `Bash Scripting`; `OpenVAS` reso testo (accanto a Nessus).
- Neutralizzati in backtick i token-esempio nel changelog (IDS e IPS, sicurezza, CryptoHack, :space:).

## [2026-06-26] lint | MOC navigation: catena lineare 00→14
Ricostruita la catena prec/succ di tutte le 15 MOC in ordine numerico.
- Corretti salti pre-esistenti: 07 Blue Team saltava 08 (ora 06→07→08→09); 09 prec era 07 (ora 08).
- Aree 11-14 inserite nella catena: …10→11→12→13→14 (14 terminale, nessun succ).
- Rimossi i link succ "a caso" generati dallo swarm (12→05, 13→10, 14→07).

## [2026-06-28] build | Uniformazione profondità + 6 nuove aree (sciame agenti)
Sessione "verso wiki perfetta" (analisi 10 criticità → rimedi). Due fronti.
- **Fase 2 — uniformare la profondità** (run precedente, file disgiunti per cartella): aggiunte le
  sezioni dello Standard Nota Esperto (`## Lab`, `## Domande`, `Approfondimento livello esperto`, +1
  fonte) alle aree sottili **08 Sistemi Operativi** (7), **09 Python** (7), **11 Cloud** (9),
  **12 AppSec** (10), **13 RE/Exploit** (10), **14 DFIR** (10), più pass su 01 Reti/02 Linux/05 Web.
  Codificato lo **Standard Nota Esperto** (9 sezioni) in `WIKI_SCHEMA.md`; aggiornato il meta-doc
  `Sintesi/Analisi e Roadmap Expert.md` coi numeri reali.
- **Fase 3 — colmare i gap di dominio** (sciame di **7 agenti paralleli**, una cartella ciascuno,
  zero collisioni; consolidamento index/log/nav a posteriori dal coordinatore):
  - **6 nuove aree** (MOC + 6 note esperto l'una, fase 3, standard a 10 sezioni, comandi reali, ≥2 fonti):
    `15 Mobile Security`, `16 Wireless & Radio`, `17 API e GraphQL Security`, `18 AI e LLM Security`,
    `19 DevSecOps e Supply Chain`, `20 GRC e Compliance`.
  - **04 Windows e AD +4 note avanzate**: `28 ADCS e Template Vulnerabili (ESC1-ESC8)`,
    `29 Delegation Kerberos (Unconstrained, Constrained, RBCD)`, `30 Shadow Credentials`,
    `31 Trust di Dominio e Foresta`.
  - GraphQL non duplicato: le note 17 cross-linkano la pagina esistente `12 AppSec/08 GraphQL Security`.
- **Fase 4 — studio & navigazione**: creati `Sintesi/Learning Path.md` (curriculum fase 0→4 con
  prerequisiti, milestone, checklist) e `Sintesi/Matrice Ruolo-Cert.md` (cross-walk ruolo/cert→aree).
- Consolidato `index.md` (aree 15-21 in nav + blocchi contenuto + link Sintesi; conteggio ~360 pagine,
  data 2026-06-28). Catena MOC estesa 14→15→16→17→18→19→20.

## [2026-06-28] lint | Verifica integrità post-build
Script `linkcheck.py` (strip code-block + alias-aware) sull'intero vault: **362 file .md** (escluso
Template). Link rotti reali iniziali = 1 (`[[Reverse Engineering]]`, usato dalle note Mobile) →
risolto aggiungendo l'alias `Reverse Engineering` alla MOC `13 — Mappa Reverse Engineering e Exploit Dev`.
Ri-scan: **0 link rotti**. Le 6 nuove MOC hanno alias nome-area (es. `Wireless & Radio`,
`API & GraphQL Security`) così i cross-link delle altre aree risolvono.
