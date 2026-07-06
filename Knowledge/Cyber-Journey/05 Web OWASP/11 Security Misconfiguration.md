---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Security Misconfiguration"]

---

# Security Misconfiguration

> **Nota etica**: le tecniche descritte vanno studiate e praticate solo su ambienti autorizzati (PortSwigger Web Academy, DVWA, TryHackMe). Usarle su sistemi reali senza permesso è illegale.

## In breve

La **Security Misconfiguration** è la categoria più diffusa di vulnerabilità: si verifica quando un sistema, un'applicazione, un framework o un'infrastruttura cloud viene lasciato con **configurazioni non sicure di default, incomplete o errate**. Rientra in **A05 - Security Misconfiguration** dell'[[OWASP Top 10]] 2021 (nella bozza **2025 sale a A02**, segno della sua crescente diffusione, specie in cloud/container).

## Come funziona

Non si tratta di un singolo attacco ma di una categoria ampia. Le configurazioni errate emergono a ogni livello dello stack:

- **Credenziali di default** non cambiate (admin/admin, root/root)
- **Directory listing** abilitato sul web server (si vede l'elenco dei file)
- **Pagine di errore dettagliate** che rivelano stack trace, versioni, percorsi interni
- **Servizi non necessari** esposti (porte aperte, pannelli admin pubblici)
- **Header di sicurezza HTTP assenti**: `X-Frame-Options`, `Content-Security-Policy`, `Strict-Transport-Security`
- **Permessi eccessivi** su bucket S3, database, file system
- **Software non aggiornato** con vulnerabilità note (si sovrappone a [[OWASP Top 10]] A06 - Vulnerable Components)

## Esempio pratico

Un server Apache con directory listing attivo mostra:
```
http://example.com/backup/
Index of /backup
[DIR] ..
[   ] database_dump_2025.sql   12-Mar-2026 18:23   4.2M
[   ] config.php.bak           01-Jan-2026 10:00   2.1K
```

L'attaccante scarica `config.php.bak` e trova credenziali del database in chiaro. Con un semplice accesso HTTP ha ottenuto accesso privilegiato all'intera applicazione.

Un altro esempio: pannello Kubernetes Dashboard esposto senza autenticazione:
```
http://192.168.1.100:8001/api/v1/namespaces/kube-system/secrets/
```

File/endpoint esposti per default che il recon cerca subito:
```bash
nikto -h https://target            # scanner di misconfig

GET /.git/config                   # repository git esposto
GET /actuator/env                  # Spring Boot Actuator non protetto → dump env + segreti
GET /server-status                 # Apache mod_status pubblico

aws s3 ls s3://company-backups --no-sign-request   # bucket S3 pubblico
```

## Mitigazione e difesa

- Seguire una **baseline di hardening** (CIS Benchmarks) per ogni componente
- Rimuovere o disabilitare tutti i servizi, funzionalità e account non necessari
- Cambiare **sempre** le credenziali di default prima della messa in produzione
- Configurare gli **header HTTP di sicurezza** (CSP, HSTS, X-Content-Type-Options, X-Frame-Options/frame-ancestors; CORS restrittivo — niente `Access-Control-Allow-Origin: *` con credenziali) verificabili con securityheaders.com
- Separare gli ambienti (dev, staging, prod) con configurazioni diverse; **hardening ripetibile via IaC** + scansione config (CIS Benchmark)
- Cloud: bucket privati di default, IAM least-privilege, niente segreti in plaintext
- Automatizzare i controlli con strumenti come [[OWASP ZAP]] o scanner di configurazione

## CVE / casi reali
- **CVE-2021-44228 "Log4Shell"** — pur essendo un bug ([[Componenti Vulnerabili]]), è stata catastrofica anche per **misconfig** (JNDI lookup abilitato di default, logging di input non fidato).
- **Capital One (2019)** — **misconfig di WAF/IAM** in AWS ([[Server-Side Request Forgery (SSRF)]] + ruolo IAM troppo permissivo) → esfiltrazione di 100M record. Esempio canonico di misconfiguration cloud.

## Lab
- [[PortSwigger Web Academy]] → categoria **Information disclosure** (la faccia sfruttabile della misconfig). Dal livello APPRENTICE:
  - *Information disclosure in error messages* — messaggi d'errore verbosi che rivelano versioni/stack.
  - *Information disclosure on debug page* — pagina di debug lasciata esposta.
  - *Source code disclosure via backup files* — file `.bak`/sorgenti serviti (come l'esempio `config.php.bak` sopra).
  - *Information disclosure in version control history* — repository `.git` esposto.
- Cosa esercitare: recon di endpoint di default (`/.git/config`, `/actuator/env`, `/server-status`) con [[Burp Suite]] e scanner come `nikto`; verificare gli header di sicurezza mancanti.

## Domande
1. **D:** Perché la Security Misconfiguration è considerata una categoria trasversale e non un singolo attacco?  **R:** Non descrive una tecnica ma un difetto di configurazione che può emergere a ogni livello dello stack (web server, framework, cloud, container), abilitando attacchi diversi.
2. **D:** Come può un directory listing attivo portare a compromissione?  **R:** Espone file non pensati per essere pubblici (es. `config.php.bak`, dump SQL); l'attaccante li scarica via HTTP e ne estrae credenziali in chiaro.
3. **D:** Cosa rischia di esporre un Spring Boot Actuator non protetto?  **R:** Endpoint come `/actuator/env` che restituiscono variabili d'ambiente e segreti dell'applicazione.
4. **D:** Quali header HTTP di sicurezza andrebbero configurati e come si verificano?  **R:** `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`/`frame-ancestors`, CORS restrittivo; verificabili con securityheaders.com o [[OWASP ZAP]].
5. **D:** Qual è l'approccio sistematico per ridurre le misconfiguration?  **R:** Applicare una baseline di hardening ripetibile (CIS Benchmarks) via IaC, rimuovere servizi/account non necessari, cambiare le credenziali di default e separare gli ambienti dev/staging/prod.

## Collegamenti

- [[OWASP Top 10]]
- [[HTTP e HTTPS]]
- [[XML External Entity (XXE)]]
- [[Autenticazione e Gestione Sessioni]]
- [[Enumerazione]]
- [[OWASP ZAP]]
- [[Burp Suite]]

## Fonti

- OWASP A05 Security Misconfiguration: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- OWASP Testing Guide - Configuration: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/
- PortSwigger Information Disclosure: https://portswigger.net/web-security/information-disclosure
