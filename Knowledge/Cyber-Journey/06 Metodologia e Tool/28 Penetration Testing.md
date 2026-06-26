---
tipo: concetto
tag: [metodologia]
fase: 1
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["Penetration Testing"]
---

# Penetration Testing

**Penetration Testing** (pentest) = simulazione **autorizzata** di un attacco reale per trovare e
sfruttare vulnerabilità prima che lo faccia un avversario, e misurarne l'impatto concreto. Output =
un [[Reporting Pentest|report]] con i rischi, le prove (PoC) e i rimedi. È il lato offensivo
dell'attività di sicurezza, complementare al difensivo del [[Percorsi di Carriera Pentester vs SOC|SOC]].

> [!warning] Etica e legge
> Si esegue **solo** con autorizzazione scritta — *scope* e *Rules of Engagement* (RoE) firmati —
> oppure su lab/CTF ([[TryHackMe]], [[HackTheBox]]). Toccare un sistema fuori scope, anche per
> "curiosità", è reato (in Italia art. 615-ter c.p., accesso abusivo a sistema informatico).

## Pre-engagement: scope e regole

Prima di lanciare un solo pacchetto si definisce per iscritto:

- **Scope** — IP/range, domini, applicazioni *in* e *out of scope*.
- **RoE** — finestre temporali, tecniche vietate (es. DoS, social engineering), gestione dei dati
  sensibili, contatti di emergenza.
- **Tipo di test** in base al livello di conoscenza fornito:

| Livello | Info iniziali | Simula |
|---------|---------------|--------|
| **Black box** | Nessuna (solo il bersaglio) | Attaccante esterno senza insider knowledge |
| **Grey box** | Parziali (credenziali utente, doc) | Utente/insider con accesso limitato |
| **White box** | Complete (codice, architettura, credenziali admin) | Audit approfondito, massima copertura |

## Tipi di pentest

Web app, network (esterno/interno), wireless, mobile, cloud, [[Active Directory]], social
engineering, physical. Lo scope determina tool e metodologia.

## vs concetti vicini

- **Vulnerability Assessment** — *trova* e classifica le vulnerabilità (spesso con scanner come
  Nessus/[[OpenVAS]]) ma **non le sfrutta**. Più ampio e automatico, meno profondo.
- **Red Team** — operazione *goal-oriented* e stealth (es. "raggiungi il domain admin senza essere
  rilevato"): valuta anche la **detection & response** del blue team, non solo le vulnerabilità.
- **Pentest** — sta in mezzo: trova **e** sfrutta entro uno scope definito, con obiettivo di copertura.

## Metodologia e fasi

Standard di riferimento: **PTES** (Penetration Testing Execution Standard), **OWASP WSTG** (web),
**OSSTMM**, **NIST SP 800-115**, **MITRE ATT&CK** per la mappatura delle tecniche.

```text
[[Ricognizione (Recon)]]  ->  OSINT, footprinting (passivo/attivo)
        |
[[Scansione delle Porte]] ->  host/porte vive (nmap)
        |
[[Enumerazione]]          ->  servizi, versioni, utenti, share
        |
[[Exploitation]]          ->  foothold sfruttando una vuln
        |
[[Post-Exploitation]]     ->  privesc, persistenza, [[Lateral Movement]], loot
        |
[[Reporting Pentest]]     ->  rischi, PoC, remediation
```

### Esempio di flusso operativo (lab)

```bash
# 1. Discovery + port scan
nmap -sC -sV -oA scan/nmap-initial 10.10.10.10

# 2. Enumerazione mirata di un servizio web trovato
gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt
nikto -h http://10.10.10.10

# 3. Ricerca exploit per una versione vulnerabile (vedi [[ExploitDB]])
searchsploit apache 2.4.49

# 4. Post-exploitation: enumerazione privesc Linux (vedi [[PEAS]], [[GTFOBins]])
sudo -l
./linpeas.sh
```

Il dettaglio passo-passo è in [[Metodologia del Pentest]].

## Deliverable: il report

Il valore del pentest è il [[Reporting Pentest|report]]: *executive summary* (per il management),
dettaglio tecnico per ogni finding con **severità** ([[CVE e CVSS|CVSS]]), passi di riproduzione,
evidenze e raccomandazioni di remediation.

## Lab

- **TryHackMe**: percorsi *Jr Penetration Tester*, *Complete Beginner*, room *Vulnversity*,
  *Pentesting Fundamentals*, *Nmap*, *Metasploit*.
- **HackTheBox**: *Starting Point*, percorso *Penetration Tester* su **HTB Academy**.
- **PortSwigger Web Security Academy** — per la parte web app (gratuito).
- **Certificazioni**: OSCP (OffSec), PNPT (TCM), eJPT (INE), CPTS (HTB). Vedi [[Certificazioni Cybersecurity]].

## Collegamenti

- [[Metodologia del Pentest]] · [[Metodologia CTF]] · [[Kali Linux]] · [[Reporting Pentest]]
- [[Ricognizione (Recon)]] · [[Scansione delle Porte]] · [[Enumerazione]] · [[Exploitation]] · [[Post-Exploitation]]
- [[Percorsi di Carriera Pentester vs SOC]] · [[Certificazioni Cybersecurity]] · [[MITRE ATT&CK]]
- [[TryHackMe]] · [[HackTheBox]] · [[ExploitDB]] · [[HackTricks]]

## Fonti

- PTES — Penetration Testing Execution Standard: http://www.pentest-standard.org
- OWASP Web Security Testing Guide (WSTG): https://owasp.org/www-project-web-security-testing-guide/
- NIST SP 800-115, *Technical Guide to Information Security Testing and Assessment*: https://csrc.nist.gov/pubs/sp/800/115/final
