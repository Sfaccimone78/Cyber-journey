---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["OWASP Top 10", "Web Hacking"]
---

# OWASP Top 10

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger Academy, DVWA, TryHackMe).

## In breve
L'**OWASP Top 10** è la lista di riferimento delle **dieci categorie di rischio** più critiche nelle web app, curata dall'Open Web Application Security Project. È una **tassonomia di rischi** (non di singole vulnerabilità) e funge da checklist minima per sviluppo, pentest e compliance. Edizione corrente: **2021**.

## Come nasce il ranking
OWASP raccoglie dati da centinaia di organizzazioni e classifica per **frequenza × impatto × exploitabilità**. Otto categorie da dati reali, due da survey di settore. Non è "le 10 bug peggiori" ma "le 10 famiglie di rischio dove si concentra il danno".

## La lista 2021
| ID | Categoria | Pagina collegata |
|---|---|---|
| **A01** | Broken Access Control | [[Broken Access Control e IDOR]] |
| **A02** | Cryptographic Failures | [[TLS e SSL]], [[Hashing delle Password e Salting]] |
| **A03** | Injection | [[SQL Injection]], [[Command Injection]], [[Cross-Site Scripting (XSS)]] |
| **A04** | Insecure Design | difetto architetturale, non un bug |
| **A05** | Security Misconfiguration | [[Security Misconfiguration]], [[XML External Entity (XXE)]] |
| **A06** | Vulnerable & Outdated Components | librerie note-vulnerabili (es. Log4Shell) |
| **A07** | Identification & Auth Failures | [[Autenticazione e Gestione Sessioni]] |
| **A08** | Software & Data Integrity Failures | [[Insecure Deserialization]], supply-chain |
| **A09** | Logging & Monitoring Failures | tie-in [[Incident Response]] |
| **A10** | Server-Side Request Forgery | [[Server-Side Request Forgery (SSRF)]] |

Note 2021: **A01 sale al 1° posto** (access control è il problema più diffuso); XSS è confluito dentro **A03 Injection**; SSRF entra come categoria propria su spinta della community.

## Cambiamenti chiave 2017 → 2021
- Tre nuove categorie: **A04 Insecure Design**, **A08 Integrity Failures**, **A10 SSRF**.
- Si passa da vulnerabilità puntuali a **cause più ampie** (es. "Insecure Design" copre la mancanza di threat modeling, non un singolo bug).

## Come si usa in pentest
La Top 10 è la **checklist di partenza**, non la fine: copre il rischio più comune, ma un test serio segue la **OWASP WSTG** (Testing Guide, molto più granulare). Workflow tipico: mappare ogni funzione dell'app alle categorie, testare A01/A03 per primi (massimo ritorno), usare [[Burp Suite]] per intercettare e manipolare.

### Workflow web hacking con proxy intercettante
Il testing pratico ruota attorno a un **proxy d'intercettazione** ([[Burp Suite]] è lo standard) che si frappone tra browser e server:
```
1. Configura proxy + scope; naviga l'app per popolare la site map (recon)
2. Identifica input/parametri (GET/POST, header, cookie, JSON)
3. Manda le richieste interessanti a Repeater → testa una vuln per volta:
   - SQLi → [[SQL Injection]] ;  XSS → [[Cross-Site Scripting (XSS)]] ;  IDOR → [[Broken Access Control e IDOR]]
4. Intruder per fuzzing/brute (parametri nascosti, login, directory)
5. Collaborator (OAST) per le vuln blind/out-of-band → [[Server-Side Request Forgery (SSRF)]]
6. Conferma l'impatto, documenta il PoC → report
```
Strumenti complementari: [[sqlmap]] (SQLi), [[Gobuster]]/[[ffuf]] (content discovery), [[Nikto]] (misconfig). Lato difensivo, le contromisure sono quelle delle singole categorie → [[Secure Coding]].

## Mitigazione (programma, non patch singola)
- **OWASP Cheat Sheet Series** per ogni categoria; **OWASP ASVS** come standard di verifica.
- Sicurezza nel **SDLC**: threat modeling (A04), SAST/DAST in CI/CD, dependency scanning (A06).
- Pentest periodici con la Top 10 come baseline + WSTG per la profondità.

## Lab
- **PortSwigger Web Academy** — [[PortSwigger Web Academy]]: percorso "All labs" raggruppato per categoria (Access control, Injection, SSRF, XXE…): copre quasi tutta la Top 10 con lab gratuiti.
- **TryHackMe** — *OWASP Top 10 (2021)* e *OWASP Juice Shop*: room guidate categoria per categoria.
- **OWASP Juice Shop** (self-host o su TryHackMe): app deliberatamente vulnerabile mappata 1:1 sulla Top 10, con scoreboard delle challenge.

## Domande
**D: L'OWASP Top 10 è una lista di vulnerabilità o di rischi?**
R: Di **categorie di rischio**, non di singoli bug. Ogni voce (es. A03 Injection) raggruppa molte vulnerabilità concrete. Serve come tassonomia e checklist minima, non come elenco esaustivo: per la profondità si usa la WSTG.

**D: Perché A01 Broken Access Control è salito al primo posto nel 2021?**
R: Perché è la classe di difetti riscontrata con maggiore frequenza nei dati raccolti: il 94% delle app testate presentava qualche forma di access control rotto. Frequenza × impatto la portano in cima.

**D: Che differenza c'è tra usare la Top 10 e la WSTG in un pentest?**
R: La Top 10 è la baseline ad alto livello (le 10 famiglie più comuni); la **Web Security Testing Guide** è il manuale granulare con i singoli test case. Si parte dalla Top 10 per priorità, si usa la WSTG per la copertura completa.

**D: Cosa copre A04 Insecure Design che le altre categorie non coprono?**
R: I difetti **architetturali/di progettazione** (mancanza di threat modeling, assenza di controlli per-design) che non sono implementazione errata ma scelte di design insicure: non si correggono con una patch, ma ripensando il flusso.

## Collegamenti
- [[SQL Injection]]
- [[Cross-Site Scripting (XSS)]]
- [[Broken Access Control e IDOR]]
- [[Server-Side Request Forgery (SSRF)]]
- [[Security Misconfiguration]]
- [[Autenticazione e Gestione Sessioni]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti
- OWASP Top 10 2021: https://owasp.org/www-project-top-ten/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- OWASP Web Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- OWASP ASVS (Application Security Verification Standard): https://owasp.org/www-project-application-security-verification-standard/
