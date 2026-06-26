# Piano di Studio — Sicurezza Informatica v2
**Obiettivo:** Junior Pentester **oppure** SOC Analyst L1 *(scegli uno — vedi nota)*
**Livello di partenza:** Basi di informatica, terminale conosciuto
**Tempo disponibile:** 1 ora/giorno (45 min focus effettivo)
**Durata totale:** 15 mesi · ~450 ore
**Budget minimo consigliato:** ~15–20€/mese (TryHackMe o HTB VIP) + 200€ per l'esame eJPT

> **Nota sul percorso:** Il piano ha un tronco comune (Fasi 1–2), poi si biforca.
> Scegli il percorso **prima** di iniziare la Fase 3, non dopo.
> - **Percorso A — Pentester:** Fasi 3A + 4A
> - **Percorso B — SOC Analyst:** Fasi 3B + 4B
> Cambiare idea a metà piano costa settimane. Leggi le descrizioni dei ruoli in fondo prima di decidere.

---

## Schema orario giornaliero

| Minuti | Attività |
|--------|----------|
| 0–5 | **Ripasso attivo** — spiega a voce alta il concetto di ieri (anche da solo) |
| 5–35 | **Studio principale** — teoria + lab pratico in parallelo, non in sequenza |
| 35–50 | **Esercizio guidato** — CTF, tool da terminale, o macchina con writeup a portata di mano |
| 50–55 | **Writeup flash** — 3 frasi: cosa ho fatto / cosa non capivo / come l'ho risolto |

> **Regola di recupero:** se salti 3+ giorni consecutivi, riprendi dall'ultimo argomento completato con una sessione di 20 minuti, poi vai avanti. Non è una punizione: è per riscaldare la memoria procedurale prima di affrontare nuovi concetti.
>
> **Minimo giornaliero:** anche 10 minuti di ripasso valgono. L'obiettivo è non spezzare l'abitudine, non il numero di ore.

---

## Settimana tipo (Fasi 1–2, tronco comune)

| Giorno | Attività |
|--------|----------|
| Lunedì | Teoria + lab guidato (TryHackMe / PortSwigger) |
| Martedì | Approfondimento dello stesso argomento — lab diverso sulla stessa tecnica |
| Mercoledì | Tool da terminale — approfondisci uno strumento specifico con la documentazione aperta |
| Giovedì | Esercizio pratico — macchina guidata HTB Starting Point o OverTheWire |
| Venerdì | Mini-report settimanale + writeup flash |
| Sabato | Sessione libera leggera — video, lettura, o riposo |
| Domenica | **Riposo — nessun lab, senza eccezioni** |

> **Perché Martedì è uguale a Lunedì:** con 45 minuti al giorno non si consolida una tecnica nuova in una sola sessione. Due giorni sullo stesso argomento costruiscono memoria procedurale, non duplicano il lavoro.

---

## Fase 1 — Fondamenta solide
**Durata:** Mesi 1–4 · ~120 ore

### Reti

Studia in questo ordine — ogni concetto dipende dal precedente:

1. **Modello TCP/IP** — come viaggiano i pacchetti, differenza con OSI
2. **DNS** — risoluzione di un dominio passo per passo
3. **HTTP/S** — richieste, risposte, header, status code, metodi
4. **Porte e protocolli comuni** — 22 (SSH), 80/443 (HTTP/S), 445 (SMB), 3389 (RDP), 25/587 (SMTP)
5. **Subnetting base** — subnet mask, CIDR, calcolo host disponibili
6. **Wireshark** — cattura e analizza traffico reale ogni settimana per tutto il mese 1

### Linux

- Filesystem: struttura directory, path assoluto/relativo
- Permessi: `chmod`, `chown`, `sudo`, SUID/SGID — capire *perché* esistono, non solo la sintassi
- Processi: `ps`, `top`, `kill`, `cron`
- Comandi fondamentali: `find`, `grep`, `awk`, `sed`, `netstat`, `ss`
- Bash scripting: variabili, loop, condizioni, pipe
- **Piattaforma:** OverTheWire Bandit livelli 0–25

> **Su Bandit:** usa i writeup. Il metodo corretto è: prova da solo 20 minuti, poi se sei bloccato leggi il writeup, capisce *perché* funziona, e rifai il livello a mente fredda. Bandit 0–25 "senza aiuti" non è un obiettivo realistico per un principiante — il valore è capire la tecnica, non soffrire.

### Windows (base — spesso ignorato, fondamentale)

- Filesystem: `C:\`, `%APPDATA%`, `%SYSTEM32%`, path assoluto/relativo
- Comandi `cmd` e PowerShell base: `dir`, `cd`, `ipconfig`, `netstat`, `tasklist`
- Utenti e permessi: Administrator, SYSTEM, gruppi locali
- Registro di sistema: cos'è, dove si trovano le chiavi importanti per la sicurezza
- **Piattaforma:** TryHackMe — room "Windows Fundamentals" (1, 2, 3)

### Python

Obiettivo concreto: **scrivi da zero uno script di 40–50 righe che fa qualcosa di utile.**
Esempi progressivi:

1. Scanner di porte TCP con `socket` (mese 2)
2. Script che fa richieste HTTP e legge gli header con `requests` (mese 3)
3. Script che cerca stringhe in file di testo con `os` e `re` (mese 4)

Usa writeup e documentazione liberamente. L'obiettivo non è memorizzare la sintassi, è capire la logica.

### Crittografia

Un concetto a settimana, in profondità:

- Simmetrica (AES) vs asimmetrica (RSA): differenze pratiche e casi d'uso
- Hash: MD5, SHA-1, SHA-256 — cosa sono, perché non si invertono, come si usano per le password
- TLS: handshake, certificati, CA — come funziona HTTPS davvero
- **Piattaforma:** OverTheWire Krypton livelli 0–5

### Piattaforme Fase 1

| Piattaforma | Uso | Costo |
|-------------|-----|-------|
| TryHackMe — Pre-Security + Windows Fundamentals | Reti + Linux + Windows base | Gratuito |
| OverTheWire Bandit | Linux pratico, livelli 0–25 | Gratuito |
| OverTheWire Krypton | Crittografia classica | Gratuito |
| Wireshark | Analisi traffico di rete | Gratuito |
| VirtualBox + Kali Linux | Ambiente lab locale | Gratuito |

### Criteri di avanzamento — Fase 1

Non passare alla Fase 2 finché non soddisfi tutti i punti:

- [ ] Completi il path Pre-Security di TryHackMe (incluse le room Windows Fundamentals)
- [ ] Risolvi Bandit livelli 0–25 (con writeup consultati quando necessario)
- [ ] Sai spiegare a voce cosa succede quando digiti un URL nel browser, passo per passo
- [ ] Hai scritto almeno 2 script Python funzionanti da zero (scanner di porte + richieste HTTP)
- [ ] Sai leggere una cattura Wireshark e identificare una richiesta HTTP e una risposta DNS
- [ ] Sai navigare il filesystem di Windows da cmd/PowerShell e identificare utenti e permessi

### Pausa programmata
Al termine del mese 4: **una settimana senza lab**. Solo lettura o video leggeri. Obbligatorio.

---

## Fase 2 — Offensive basics + Blue Team base
**Durata:** Mesi 5–8 · ~120 ore

> Questa fase copre basi offensive e difensive in parallelo.
> Non sono separate: un buon pentester deve capire i log, un SOC analyst deve capire gli attacchi.

### Web — OWASP Top 10

Affronta una vulnerabilità alla volta, nell'ordine seguente.
Per ognuna: studia la teoria (30 min), poi fai almeno 3 lab su PortSwigger. Consulta la documentazione liberamente.

1. SQL Injection — capire il database dietro, non solo il payload
2. Cross-Site Scripting (XSS) — reflected, stored, DOM-based
3. Broken Access Control / IDOR — cambia un ID nella richiesta
4. Server-Side Request Forgery (SSRF) — fai fare richieste al server
5. Command Injection — esegui comandi sul sistema remoto
6. XML External Entity (XXE) — lettura file arbitraria
7. Security Misconfiguration — default credential, directory listing

### Windows e Active Directory — base offensiva e difensiva

- Struttura AD: domain controller, utenti, gruppi, OU, GPO
- Kerberos: cos'è, ticket TGT/TGS, perché è rilevante per gli attacchi
- Attacchi base: pass-the-hash, Kerberoasting (concettuale), AS-REP Roasting
- SMB: cos'è, perché è critico in ambienti Windows
- Windows Event Log: ID eventi fondamentali (4624, 4625, 4648, 4688, 4698, 4720)
- Tool offensivi: `enum4linux`, `crackmapexec` (solo in lab privato)
- Tool difensivi: Event Viewer, analisi log con PowerShell
- **Piattaforma:** TryHackMe — percorso "Active Directory Basics" + "Attacktive Directory"

### Blue Team base (modulo da 3 settimane — mese 7)

> Se stai valutando il percorso SOC, questo modulo è fondamentale.
> Se punti solo al pentesting, puoi ridurlo a 1 settimana di overview.

- **SIEM:** cos'è, come funziona, cosa sono gli alert
- **Splunk base:** ricerche SPL semplici, dashboard, correlazione eventi
- **Log analysis:** distinguere traffico normale da anomalo, riconoscere bruteforce, lateral movement, exfiltration nei log
- **Incident response base:** fasi (preparazione, identificazione, contenimento, eradicazione, recovery)
- **Piattaforma:** TryHackMe — "SOC Level 1" path (primi 4 moduli)

### Tool offensivi — uno alla volta fino a padronanza

| Tool | Uso principale | Quando introdurlo |
|------|---------------|-------------------|
| Nmap | Scansione porte e servizi | Inizio mese 5 |
| Gobuster / ffuf | Directory e file enumeration | Settimana 2 mese 5 |
| Burp Suite Community | Intercettazione e modifica richieste HTTP | Mese 5–6 |
| Metasploit | Framework exploit — capisci cosa fa, non dipenderci | Mese 6–7 |
| Nikto | Scanner vulnerabilità web | Mese 7 |

> **"Senza documentazione" è il metodo sbagliato.** L'obiettivo è saper *scegliere* le opzioni giuste e *interpretare l'output*. Consulta sempre i man page, cheatsheet e HackTricks — lo fa anche un senior.

### Metodologia pentest — applicala a ogni macchina

```
1. Ricognizione passiva   → informazioni senza toccare il target
2. Scansione / Enumerazione → nmap, gobuster, banner grabbing
3. Identificazione vulnerabilità → cosa è esposto? versioni? CVE?
4. Exploitation           → sfrutta la vuln, ottieni accesso
5. Post-exploitation      → privilege escalation, persistenza
6. Reporting              → scrivi cosa hai trovato e come rimediare
```

### Reporting — inizia ora

Per ogni macchina HTB risolta, scrivi un mini-report con questa struttura:
- Vulnerabilità trovata
- Impatto (cosa avrebbe potuto fare un attaccante reale)
- Come si rimedia
- Screenshot del flag

Questo diventa il tuo portfolio GitHub.

### Piattaforme Fase 2

| Piattaforma | Uso | Costo |
|-------------|-----|-------|
| PortSwigger Web Academy | Lab OWASP Top 10 | Gratuito |
| HackTheBox Starting Point | Macchine guidate con metodologia | Gratuito (tier base) |
| TryHackMe — Jr Pentester + SOC L1 | Percorsi strutturati | ~10€/mese consigliato |
| TryHackMe — Active Directory Basics | AD offensivo e difensivo | Incluso abbonamento |

### Criteri di avanzamento — Fase 2

- [ ] 8 lab completati su PortSwigger Web Academy (almeno 1 per ogni vuln dell'OWASP Top 10 trattata)
- [ ] 3 macchine HTB Starting Point completate (con writeup consultato *dopo* il tentativo)
- [ ] Usi Nmap + Burp Suite scegliendo le opzioni giuste per il contesto (documentazione aperta)
- [ ] Hai almeno 3 mini-report pubblicati su GitHub
- [ ] Sai fare privilege escalation base su Linux (SUID, sudo -l, cron)
- [ ] Conosci i 5 Windows Event ID più importanti e sai cercarli in un log
- [ ] Hai completato i primi 4 moduli del path SOC Level 1 di TryHackMe

### Pausa programmata
Inizio mese 9: **tre giorni di pausa** prima di iniziare il percorso scelto.

---

## Fase 3A — Percorso Pentester: Certificazione eJPT
**Durata:** Mesi 9–11 · ~90 ore

### Perché eJPT come prima certificazione

L'eJPT (eLearnSecurity Junior Penetration Tester) è pratica (devi compromettere macchine reali, nessun quiz a risposta multipla), accessibile con le basi costruite nelle Fasi 1–2, e riconosciuta dai recruiter tecnici in Italia ed Europa.

### Contenuto specifico eJPT

**Networking per pentest**
- Pivoting e port forwarding: accedere a reti interne attraverso un host compromesso
- Routing statico: modificare la tabella di routing per raggiungere subnet nascoste
- Tool: `ssh -L`, `chisel`, `proxychains`

**Exploitation**
- Metasploit: uso consapevole — capire cosa fa l'exploit, non solo lanciarlo
- Exploit manuali: almeno 3 CVE sfruttati senza Metasploit
- Buffer overflow base su Linux (utile, non obbligatorio per eJPT)

**Active Directory — approfondimento**
- Pass-the-hash pratico in lab
- Kerberoasting pratico
- Lateral movement base: da un host compromesso a un altro nella stessa rete
- Tool: `crackmapexec`, `impacket` (GetNPUsers, secretsdump)

### Piano settimana tipo — Fase 3A

| Giorno | Attività |
|--------|----------|
| Lunedì | Modulo corso INE |
| Martedì | Macchina HTB tematica (allineata al modulo) |
| Mercoledì | Lab pivoting / port forwarding |
| Giovedì | Ripasso + appunti strutturati in markdown |
| Venerdì | Simulazione parziale (1 ora su rete multi-macchina) |
| Sabato | Revisione note della settimana |
| Domenica | Riposo |

### Simulazione esame

Ultima settimana prima di prenotare: simula l'esame reale.
- 3 ore consecutive
- Nessun writeup durante la simulazione (consultabile dopo)
- Rete con 3–4 macchine interconnesse
- Prenota l'esame **solo** dopo 3 simulazioni in cui hai raggiunto almeno il 70% degli obiettivi

### Piattaforme Fase 3A

| Piattaforma | Uso | Costo |
|-------------|-----|-------|
| INE Starter Pass | Corso ufficiale eJPT | Gratuito |
| HackTheBox VIP | Macchine Medium + Pro Labs base | ~14€/mese |
| PentesterLab | Lab tematici per lacune specifiche | Parzialmente gratuito |

### Costo esame
L'esame eJPT costa circa **200€**. Preventiva questa spesa prima di iniziare la fase.

### Criteri per prenotare l'esame

- [ ] Corso INE Starter completato al 100%
- [ ] 3 simulazioni superate con almeno il 70% degli obiettivi
- [ ] Sai fare pivoting e port forwarding (con appunti a portata di mano)
- [ ] Privilege escalation su Linux: almeno 5 vettori diversi praticati
- [ ] Hai compromesso almeno una macchina con Active Directory in lab
- [ ] Privilege escalation su Windows: almeno 3 vettori (AlwaysInstallElevated, token impersonation, servizi vulnerabili)

---

## Fase 3B — Percorso SOC Analyst: Specializzazione difensiva
**Durata:** Mesi 9–11 · ~90 ore

### Contenuto

**SIEM e log analysis avanzati**
- Splunk: SPL avanzato, alert, dashboard operative
- Elastic Stack (opzionale): alternativa open source molto usata in azienda
- Correlazione eventi: costruire regole di detection da zero
- Casi pratici: riconoscere bruteforce, lateral movement, C2 traffic, exfiltration nei log

**Threat Intelligence base**
- IOC (Indicator of Compromise): hash, IP, dominio, URL — cosa sono e come usarli
- Framework MITRE ATT&CK: come mappare un attacco alle tattiche e tecniche
- Feed pubblici: VirusTotal, AbuseIPDB, AlienVault OTX

**Analisi malware base**
- Analisi statica: `strings`, `file`, `exiftool`, hash su VirusTotal
- Analisi dinamica: sandbox (Any.run, Hybrid Analysis) — osserva il comportamento senza eseguire
- Non è richiesto il reverse engineering: solo capire cosa fa un campione a grandi linee

**Incident Response pratico**
- Fasi IR: preparazione → identificazione → contenimento → eradicazione → recovery → lessons learned
- Triage di alert: come decidere cosa è un falso positivo e cosa no
- Documentazione: come scrivere un ticket di incident ben formato

### Piano settimana tipo — Fase 3B

| Giorno | Attività |
|--------|----------|
| Lunedì | Modulo TryHackMe SOC Level 1 |
| Martedì | Lab Splunk / Elastic su scenario pratico |
| Mercoledì | Analisi di un campione malware in sandbox |
| Giovedì | Ripasso MITRE ATT&CK — mappa 1 tecnica per sessione |
| Venerdì | Simulazione triage alert (scenario da piattaforma) |
| Sabato | Revisione appunti della settimana |
| Domenica | Riposo |

### Piattaforme Fase 3B

| Piattaforma | Uso | Costo |
|-------------|-----|-------|
| TryHackMe SOC Level 1 | Percorso completo SOC | ~10€/mese |
| Splunk Free | Lab SIEM locale | Gratuito |
| Any.run / Hybrid Analysis | Sandbox malware | Gratuito (tier base) |
| MITRE ATT&CK Navigator | Mappatura tecniche | Gratuito |
| LetsDefend.io | Simulazione SOC pratica | Parzialmente gratuito |

### Criteri di avanzamento — Fase 3B

- [ ] Path SOC Level 1 di TryHackMe completato
- [ ] Sai costruire una query SPL per trovare un bruteforce nei log
- [ ] Hai analizzato almeno 5 campioni malware in sandbox e scritto un report per ognuno
- [ ] Sai mappare un attacco semplice su MITRE ATT&CK (almeno 3 tecniche)
- [ ] Hai simulato almeno 3 scenari di triage alert completi

---

## Fase 4A — Portfolio e ricerca lavoro (Pentester)
**Durata:** Mesi 12–15, poi in corso

### GitHub come CV tecnico

Il profilo GitHub è più importante del CV Word per un recruiter tecnico.

Struttura consigliata:
```
README.md           → chi sei, certificazioni, skills
/writeups/          → un file per macchina HTB risolta (metodologia completa, non solo il flag)
/scripts/           → tool Python che hai scritto o modificato
/reports/           → mini-report di vulnerabilità (anonimi se da lab)
/notes/             → appunti su tecniche e tool
```

**Obiettivo minimo prima di candidarti:** 10 writeup pubblici, leggibili, con metodologia e screenshot.

### Bug Bounty — solo dopo l'assunzione o con molto tempo libero

Con 45 minuti al giorno è quasi impossibile essere competitivi su HackerOne o Bugcrowd. Se vuoi provare:
- Scegli programmi VDP (Vulnerability Disclosure Program) con scope limitato, meno affollati
- Obiettivo: imparare a muoverti su target reali, non trovare bug
- Leggi i report pubblici di altri ricercatori prima di iniziare

Il primo bug valido può arrivare dopo 6–12 mesi di tentativi su target reali. Non è un fallimento: è normale.

### Criteri per candidarsi

- [ ] eJPT conseguita
- [ ] GitHub con 10+ writeup pubblici con metodologia completa
- [ ] Sai spiegare un attacco end-to-end in un colloquio (es. SQLi da ricognizione a dump del DB)
- [ ] 10+ macchine HTB nel profilo pubblico
- [ ] CV aggiornato con certificazione, GitHub linkato, tool conosciuti
- [ ] Hai preparato almeno 5 risposte a domande tecniche tipiche di colloquio (vedi sezione soft skill)

---

## Fase 4B — Portfolio e ricerca lavoro (SOC Analyst)
**Durata:** Mesi 12–15, poi in corso

### Cosa mostrare ai recruiter SOC

Per un ruolo SOC, il portfolio è diverso da quello di un pentester:

- **Report di analisi malware** (5+): campioni analizzati in sandbox con IOC, comportamento, MITRE mapping
- **Dashboard SIEM** (screenshot o export): mostra che sai costruire una vista operativa
- **Scenari IR documentati** (3+): come hai gestito un incidente simulato, con timeline e decisioni
- **GitHub o blog** con appunti su tecniche di detection e threat intel

### Certificazioni successive consigliate

| Certificazione | Perché | Costo indicativo |
|---------------|--------|-----------------|
| CompTIA Security+ | Riconosciuta ovunque, base difensiva solida | ~350€ |
| BTL1 (Blue Team Labs) | Pratica, ottima per SOC junior | ~400€ |

### Criteri per candidarsi

- [ ] Path SOC Level 1 TryHackMe completato
- [ ] 5+ report di analisi malware pubblicati
- [ ] 3+ scenari IR documentati
- [ ] Conoscenza di almeno un SIEM (Splunk o Elastic) dimostrabile
- [ ] CV con skills tecniche, piattaforme usate, GitHub/blog linkato
- [ ] Hai preparato almeno 5 risposte a domande tipiche di colloquio SOC

---

## Soft skill e preparazione al colloquio
**Valido per entrambi i percorsi — da iniziare al mese 13**

### Come prepararsi alle domande tecniche

Le domande più comuni per junior pentester:
1. Spiega come funziona una SQL Injection
2. Cos'è un reverse shell? Come lo stabiliresti?
3. Differenza tra scansione TCP SYN e TCP Connect con Nmap
4. Cos'è il privilege escalation? Dai un esempio su Linux
5. Cos'è un CVE? Come lo cerchi e lo valuti?

Le domande più comuni per SOC Analyst:
1. Cos'è un falso positivo? Come lo gestisci?
2. Descrivi le fasi dell'incident response
3. Cos'è un IOC? Fai degli esempi
4. Hai mai usato un SIEM? Che tipo di query hai scritto?
5. Cos'è MITRE ATT&CK e come si usa?

### Come strutturare la ricerca lavoro

Prima di candidarti, analizza 20 offerte nel tuo ruolo target ed estrai:
- Le 5 skill tecniche più richieste → studia quelle per prime
- Le certificazioni più citate → verifica di averle o di avere un piano per ottenerle
- I tool nominati più spesso → assicurati di averli nel portfolio

**Usa LinkedIn** per mappare i recruiter del settore in Italia. Connettiti con chi lavora già nel ruolo target. Non chiedere lavoro: chiedi una call di 15 minuti per capire cosa cercano davvero.

---

## Risorse gratuite — riepilogo completo

### Piattaforme lab

| Piattaforma | Cosa offre | Link |
|-------------|-----------|------|
| TryHackMe | Percorsi guidati con VM nel browser | tryhackme.com |
| HackTheBox | Macchine realistiche, Starting Point gratuito | hackthebox.com |
| OverTheWire | Wargame SSH — Bandit, Natas, Krypton | overthewire.org |
| PortSwigger Web Academy | Lab OWASP Top 10 | portswigger.net/web-security |
| PicoCTF | CTF per principianti, sempre disponibili | picoctf.org |
| INE Starter Pass | Corso ufficiale eJPT | ine.com |
| LetsDefend.io | Simulazione SOC pratica | letsdefend.io |
| Any.run | Sandbox malware online | any.run |

### YouTube

| Canale | Contenuto |
|--------|-----------|
| IppSec | Writeup HTB video — cerca per tecnica su ippsec.rocks |
| John Hammond | CTF walkthrough, news sicurezza |
| TCM Security | Corsi gratuiti (ethical hacking, AD, Python) |
| NetworkChuck | Reti e Linux per principianti |
| Gerald Auger (Simply Cyber) | SOC, blue team, carriera nel settore |

### Lettura e reference

| Risorsa | Cosa leggere |
|---------|-------------|
| OWASP.org | Documentazione ufficiale vulnerabilità web |
| HackTricks (book.hacktricks.xyz) | Cheatsheet per ogni fase del pentest |
| GTFOBins (gtfobins.github.io) | Privilege escalation Linux — binari sfruttabili |
| LOLBAS (lolbas-project.github.io) | Privilege escalation Windows |
| MITRE ATT&CK (attack.mitre.org) | Tecniche di attacco mappate per defender e attacker |
| ExploitDB (exploit-db.com) | Database exploit pubblici — leggi il codice |

### Comunità

| Comunità | Come usarla |
|----------|-------------|
| Discord HTB / TryHackMe | Fai domande specifiche, rispondi quando puoi |
| r/netsec, r/AskNetsec | Leggi i link condivisi, 15 min/settimana |
| IppSec (YouTube) | Writeup video dopo aver provato la macchina da solo |

---

## Template writeup flash (da usare ogni sera)

```markdown
## [Data] — [Argomento / Macchina]

**Cosa ho fatto oggi:**
(1–2 frasi)

**Cosa non capivo all'inizio:**
(1 frase — il blocco principale)

**Come l'ho risolto / capito:**
(1–2 frasi — il ragionamento, non la soluzione)

**Cosa fare domani:**
(1 punto concreto)
```

---

## Stima budget totale

| Voce | Costo stimato |
|------|--------------|
| TryHackMe Premium (10 mesi) | ~100€ |
| HackTheBox VIP (3 mesi, Fase 3A) | ~42€ |
| Esame eJPT (solo Percorso A) | ~200€ |
| **Totale Percorso Pentester** | **~342€** |
| TryHackMe Premium (10 mesi) | ~100€ |
| LetsDefend Pro (3 mesi, Fase 3B) | ~45€ |
| **Totale Percorso SOC** | **~145€** |

> Questi costi sono un investimento su 15 mesi. La maggior parte delle risorse fondamentali è gratuita; gli abbonamenti accelerano e completano il percorso senza stalli.

---

## Regole del piano — riepilogo

1. **45 minuti di focus effettivo** valgono più di 2 ore distratte
2. **La domenica è sempre libera** — senza eccezioni
3. **Avanza per criteri, non per calendario** — se non soddisfi i criteri, resta nella fase
4. **Se salti 3+ giorni:** riprendi dall'ultimo argomento, rifallo in 20 min, poi vai avanti
5. **Un tool alla volta:** padronanza prima di passare al successivo
6. **Consulta la documentazione liberamente:** l'obiettivo è capire, non memorizzare
7. **GitHub dall'inizio:** pubblica anche i report brutti — la progressione si vede
8. **Le pause programmate sono obbligatorie**, non opzionali
9. **Scegli un percorso** (Pentester o SOC) prima della Fase 3 — non cambiarlo a metà

---

## Ruoli target — cosa aspettarsi a 15 mesi

| Ruolo | Requisiti minimi | Offerte in Italia | Note |
|-------|-----------------|------------------|------|
| SOC Analyst L1 | Reti, log analysis, SIEM base, IR base | Molte | Ingresso più accessibile |
| Junior Pentester | eJPT + portfolio HTB + report | Poche, competitivo | Richiede portfolio solido |
| Security Analyst | Ibrido tra i due | Medie aziende | Buona opzione con background misto |

**Evita per ora:** Security Engineer, Cloud Security Architect, CISO — richiedono anni di esperienza e spesso laurea o master specializzato.

---

*Piano v2 — aggiornato per realismo su tempi, budget e biforcazione dei percorsi.*
*Livello di partenza: basi informatica · 1 ora/giorno · 15 mesi*
