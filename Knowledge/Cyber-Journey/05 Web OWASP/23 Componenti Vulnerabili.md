---
tipo: concetto
tag: [web, owasp, metodologia]
fase: 2
fonti: 2
aggiornato: 2026-06-26
stato: maturo
aliases: ["Componenti Vulnerabili", "Vulnerable Components", "Software Supply Chain"]
---
# Componenti Vulnerabili e Supply Chain

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger Academy, DVWA, TryHackMe).

## In breve
**A06:2021 "Vulnerable & Outdated Components"** dell'[[OWASP Top 10]]. Riguarda il rischio di usare **librerie, framework, runtime o tool di build con vulnerabilità note** — o compromessi a monte.

> [!note] Numerazione OWASP
> Nella bozza **OWASP Top 10:2025** la categoria diventa **A03 "Software Supply Chain Failures"** ed espande lo scope all'intera catena: dipendenze, **build system**, repository, **CI/CD**, registry dei pacchetti. I CVE qui hanno i punteggi medi di exploit/impatto più alti dell'intera Top 10.

## Meccanismo d'attacco
- **Dipendenza vulnerabile nota**: l'app importa una versione con CVE pubblico → l'attaccante usa l'exploit pronto (n-day).
- **Transitive dependencies**: la falla è in una dipendenza-di-una-dipendenza, invisibile senza analisi.
- **Dependency confusion**: si pubblica un pacchetto pubblico con lo **stesso nome** di uno interno e numero di versione più alto → il package manager preferisce il malevolo.
- **Typosquatting**: pacchetto malevolo con nome quasi identico (`reqeusts`).
- **Compromissione upstream**: account maintainer bucato o pipeline avvelenata → backdoor distribuita a tutti (caso SolarWinds, xz/`liblzma`).

## Esempio
```bash
# Identificare componenti vulnerabili (Software Composition Analysis)
npm audit                      # Node
pip-audit                      # Python
trivy image myapp:latest       # container + dipendenze OS
# OWASP Dependency-Check / Snyk: confronto con database CVE
```
```jsonc
// dependency confusion: pacchetto interno "acme-utils" non scopeato.
// L'attaccante pubblica su npm pubblico acme-utils@99.0.0 → viene risolto al posto del privato
```

## Mitigazione (priorità)
- **Inventario delle dipendenze (SBOM)** e scansione continua (SCA) contro feed CVE/NVD → [[CVE e CVSS]].
- **Aggiornare** con disciplina; rimuovere dipendenze inutilizzate (ridurre la superficie).
- **Pin delle versioni** + lockfile; verifica di **integrità** (hash/firme, npm provenance, Sigstore).
- Usare **scope/registry privati** e configurare la priorità per evitare dependency confusion.
- Pipeline CI/CD hardenata: build riproducibili, segreti isolati, principio least privilege sui runner.
- Politiche su fonti affidabili dei pacchetti; monitorare gli advisory dei progetti usati.

## CVE reale
- **CVE-2021-44228 "Log4Shell"** (Apache Log4j 2) — RCE banale (`${jndi:ldap://...}`) in una libreria di logging onnipresente: l'esempio definitivo di componente vulnerabile con impatto globale.
- **xz/liblzma backdoor (CVE-2024-3094, 2024)** — backdoor inserita **upstream** nel tarball di rilascio da un maintainer malevolo: caso da manuale di supply chain failure.

## Collegamenti
- [[OWASP Top 10]]
- [[Security Misconfiguration]] · [[Insecure Design]] · [[Logging e Monitoring Failures]]
- [[CVE e CVSS]] · [[Secure Coding]] · [[Threat Intelligence]]

## Fonti
- OWASP Top 10:2025 A03 Software Supply Chain Failures / 2021 A06 — https://owasp.org/Top10/
- CISA — Known Exploited Vulnerabilities (KEV) Catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
