---
tipo: fonte
tag: [owasp, web]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
url: https://owasp.org/Top10/2025/
autore: OWASP Foundation
aliases: ["Fonte OWASP Top 10", "OWASP Top 10:2025"]
---

# Fonte - OWASP Top 10:2025

Lista delle 10 categorie di rischio per applicazioni web più diffuse, **edizione 2025** (l'ottava edizione). Costruita su ~175.000 record CVE mappati a CWE dal National Vulnerability Database, 643 CWE uniche, 2,8 milioni di applicazioni testate da 13 organizzazioni; 8 categorie dai dati + 2 dalla community survey.

> ⚠️ Aggiornamento vs 2021: la richiesta iniziale citava i codici 2021. **Qui si usa l'edizione 2025** (più recente, come da regola "edizione più recente"). Rinomine/spostamenti annotati per ciascuna voce.

## La lista 2025

| Codice | Categoria | Δ vs 2021 | Pagina |
|--------|-----------|-----------|--------|
| A01:2025 | **Broken Access Control** | = #1; ora **include SSRF** | [[Broken Access Control]] · [[SSRF]] |
| A02:2025 | **Security Misconfiguration** | ↑ da #5 | [[Security Misconfiguration]] |
| A03:2025 | **Software Supply Chain Failures** | espande "Vulnerable & Outdated Components" (#6) | [[Componenti Vulnerabili]] |
| A04:2025 | **Cryptographic Failures** | ↓ da #2 | [[Cryptographic Failures]] |
| A05:2025 | **Injection** | ↓ da #3; **include XSS** | [[Injection]] · [[XSS]] |
| A06:2025 | **Insecure Design** | ↓ da #4 | [[Insecure Design]] |
| A07:2025 | **Authentication Failures** | = #7; rinominata da "Identification & Authentication Failures" | [[Authentication Failures]] |
| A08:2025 | **Software or Data Integrity Failures** | = #8 | [[Componenti Vulnerabili]] |
| A09:2025 | **Security Logging & Alerting Failures** | = #9; rinominata (era "...& Monitoring") | [[Logging e Monitoring Failures]] |
| A10:2025 | **Mishandling of Exceptional Conditions** | **NUOVA** (24 CWE) | — |

## Cambiamenti chiave 2021 → 2025
- **SSRF** non è più una categoria a sé: assorbita in **A01 Broken Access Control**. La pagina [[SSRF]] resta perché concettualmente importante.
- **XSS** resta dentro **Injection** (come dal 2021).
- **A03** allarga lo scope dai soli componenti vulnerabili all'intera **supply chain software** (dipendenze, build, repository, CI/CD) — i CVE qui hanno i punteggi medi di exploit/impatto più alti.
- **A09** sposta l'enfasi sull'**alerting** (non basta loggare: bisogna reagire).
- **A10 Mishandling of Exceptional Conditions** è la novità: gestione errori impropria, fail-open, logica che degrada in modo insicuro.
- Una categoria consolidata e due nuove entrate (A03 ampliata, A10).

## Pagine concept collegate
Una pagina per vulnerabilità (definizione → meccanica → payload → difesa → CVE reale → correlati):
[[Injection]] · [[Broken Access Control]] · [[XSS]] · [[Cryptographic Failures]] · [[Security Misconfiguration]] · [[Componenti Vulnerabili]] · [[Authentication Failures]] · [[SSRF]] · [[Insecure Design]] · [[Logging e Monitoring Failures]]

## Collegamenti
- [[index]]
- Vedi anche: [[Security Engineering]], [[PortSwigger Labs]], [[Web Hacking]], [[Matrice Attacco-Difesa]], [[Arsenale Tool]]

## Fonti
- [OWASP Top 10:2025 — <https://owasp.org/Top10/2025/>]
- [OWASP Top Ten project — <https://owasp.org/www-project-top-ten/>]
