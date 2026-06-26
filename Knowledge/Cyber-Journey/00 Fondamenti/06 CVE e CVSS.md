---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 1
aggiornato: 2026-06-22
stato: maturo
aliases: ["CVE e CVSS"]
---
# CVE e CVSS

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

## Collegamenti
- [[Vulnerabilità Exploit e Minaccia]] · [[Superficie di Attacco]] · [[Triade CIA]] · [[Threat Intelligence]]
- Tool che usano i CVE: [[Nmap]] · [[Nikto]] · [[Metasploit]] · [[OWASP Top 10]]

## Fonti
- FIRST.org — CVSS v3.1 / v4.0 Specification & Calculator.
- NVD (nvd.nist.gov) · MITRE CVE · CISA KEV Catalog · FIRST EPSS.
