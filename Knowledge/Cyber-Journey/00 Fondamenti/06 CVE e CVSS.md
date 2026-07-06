---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 2
aggiornato: 2026-07-02
stato: maturo
aliases: ["CVE e CVSS"]
---
# CVE e CVSS

## In breve
CVE e CVSS rispondono a due domande diverse: **"di quale vulnerabilità stiamo parlando?"** (CVE, un
*nome*) e **"quanto è grave?"** (CVSS, un *punteggio*). Insieme formano il linguaggio comune con cui
ricercatori, vendor, scanner e difensori si capiscono senza ambiguità.

## CVE — il nome univoco
**Common Vulnerabilities and Exposures**: un identificatore pubblico nel formato
`CVE-<anno>-<numero>` (es. `CVE-2021-44228` = Log4Shell). Non descrive la gravità: è solo un'etichetta
stabile a cui tutti si riferiscono.

**Come nasce un CVE (la pipeline):**
1. Un ricercatore scopre la vulnerabilità.
2. Una **CNA** (CVE Numbering Authority — Microsoft, Red Hat, GitHub… delegate da MITRE) assegna l'ID.
3. **MITRE** mantiene il registro grezzo.
4. Il **NVD** (National Vulnerability Database, NIST) lo arricchisce con il punteggio **CVSS**, i
   riferimenti CWE e i prodotti affetti (CPE).

> Un CVE può esistere come "RESERVED" (ID assegnato ma dettagli non ancora pubblici) — utile per il
> coordinamento prima del disclosure.

## CVSS — il punteggio di gravità
**Common Vulnerability Scoring System**: traduce le caratteristiche tecniche in un numero 0.0–10.0.
La parte interessante non è il numero finale ma il **vector string** da cui deriva — è lì che si legge
*perché* una vuln è grave.

### Base Score — le metriche intrinseche (CVSS v3.1)
Si dividono in *exploitability* (quanto è facile attaccare) e *impact* (cosa ottieni):

| Metrica | Sigla | Cosa misura |
|---|---|---|
| Attack Vector | **AV** | da dove: Network / Adjacent / Local / Physical |
| Attack Complexity | **AC** | condizioni richieste: Low / High |
| Privileges Required | **PR** | privilegi di partenza: None / Low / High |
| User Interaction | **UI** | serve che la vittima faccia qualcosa: None / Required |
| Scope | **S** | l'exploit esce dal componente vulnerabile? Unchanged / Changed |
| Confidentiality/Integrity/Availability | **C/I/A** | impatto sulla [[Triade CIA]]: None / Low / High |

**Esempio — Log4Shell:**
`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` → **10.0 Critico**. Si legge: attaccabile da rete
(`AV:N`), facile (`AC:L`), senza privilegi (`PR:N`) né interazione utente (`UI:N`), con impatto
totale su C, I e A e *scope changed* (esce dal processo vulnerabile). Il peggior profilo possibile.

### Temporal ed Environmental
- **Temporal** — corregge nel tempo: esiste exploit pubblico? Esiste patch? (un 9.8 con exploit
  weaponized è più urgente di un 9.8 solo teorico).
- **Environmental** — riadatta al *tuo* contesto: se il sistema affetto è isolato e non critico, il
  punteggio reale per te scende.

> **CVSS v4.0** (2023) ridisegna le metriche (introduce Attack Requirements, Supplemental metrics) per
> ridurre l'inflazione dei "9.8 ovunque". Molti DB ancora riportano v3.1.

## Il limite del CVSS: gravità ≠ priorità
Il CVSS misura la *gravità teorica*, non la probabilità che *qualcuno la sfrutti davvero da te*. Due
correttivi pratici usati in vulnerability management:

- **EPSS** (Exploit Prediction Scoring System) — probabilità (0–1) che una vuln sia sfruttata nei
  prossimi 30 giorni. Un 7.5 con EPSS alto va prima di un 9.8 con EPSS quasi nullo.
- **CISA KEV** (Known Exploited Vulnerabilities) — catalogo delle vuln **sfruttate attivamente** in
  the wild. Se è in KEV, si patcha *subito*, qualunque sia il CVSS.

Priorità reale ≈ CVSS (gravità) × EPSS/KEV (probabilità) × esposizione+criticità del tuo asset.
Aggancio diretto a [[Vulnerabilità Exploit e Minaccia]] (Rischio = Minaccia × Vuln × Impatto).

## Dove li incontri
Scanner come [[Nmap]] (script `vuln`), [[Nikto]], [[OWASP ZAP]] e i vulnerability manager mappano i
servizi trovati su CVE noti; `searchsploit`/ExploitDB cercano exploit per un CVE; [[Threat Intelligence]]
correla CVE ↔ campagne d'attacco reali.

## Lab
- **Calcolatore CVSS di FIRST.org**: apri il *CVSS v3.1 Calculator* e ricostruisci il vector string di Log4Shell (`AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`), poi cambia una metrica alla volta e osserva come varia il Base Score.
- **Consultazione NVD + CISA KEV**: cerca su `nvd.nist.gov` un CVE recente, leggi vector, CWE e CPE, poi verifica se è presente nel catalogo CISA KEV e nel dataset EPSS per capire la priorità reale.
- **[[TryHackMe]]** → room *CVE* / *Vulnerabilities 101*: collega un CVE noto al relativo exploit e pratica la ricerca con `searchsploit`.

## Domande
1. **D:** A quali due domande diverse rispondono CVE e CVSS? **R:** Il CVE dice *di quale* vulnerabilità si parla (un nome univoco); il CVSS dice *quanto è grave* (un punteggio 0.0–10.0).
2. **D:** Chi assegna l'ID CVE e chi lo arricchisce con CVSS/CWE/CPE? **R:** Una CNA (CVE Numbering Authority, es. Microsoft/Red Hat/GitHub) assegna l'ID, MITRE mantiene il registro grezzo e il NVD (NIST) lo arricchisce.
3. **D:** Cosa si legge di più utile in un CVSS: il numero finale o il vector string? **R:** Il vector string, perché mostra *perché* la vuln è grave (AV, AC, PR, UI, Scope, impatto su C/I/A).
4. **D:** Perché "gravità ≠ priorità" e quali due correttivi si usano? **R:** Il CVSS misura la gravità teorica, non la probabilità di sfruttamento reale; si usano EPSS (probabilità di sfruttamento a 30 giorni) e CISA KEV (vuln già sfruttate in the wild).
5. **D:** Se un CVE è nel catalogo CISA KEV, come ci si comporta? **R:** Si patcha subito, qualunque sia il punteggio CVSS, perché significa che è già sfruttato attivamente.

## Collegamenti
- [[Vulnerabilità Exploit e Minaccia]] · [[Superficie di Attacco]] · [[Triade CIA]] · [[Threat Intelligence]]
- Tool che usano i CVE: [[Nmap]] · [[Nikto]] · [[Metasploit]] · [[OWASP Top 10]]

## Fonti
- FIRST.org — CVSS v3.1 / v4.0 Specification & Calculator.
- NVD (nvd.nist.gov) · MITRE CVE · CISA KEV Catalog · FIRST EPSS.
