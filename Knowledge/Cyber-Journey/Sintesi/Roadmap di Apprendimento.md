---
tipo: sintesi
tag: [metodologia, sintesi]
fase: 0
aggiornato: 2026-06-25
stato: attivo
aliases: ["Roadmap di Apprendimento", "Da Zero a Pentester"]
---

# Roadmap di Apprendimento — da Zero a Pentester

Percorso strutturato per la sicurezza offensiva **etica** (pentest/CTF), partendo dalle fondamenta. Le milestone sono indicative; ogni tappa rimanda alle pagine wiki da studiare.

## Fase 0 — Fondamenta (prerequisiti)
Senza queste basi, gli attacchi restano "ricette" non capite.
- **Linux**: shell, filesystem, permessi → [[Permessi dei File]], [[SSH]]
- **Reti**: TCP/IP, porte, DNS, HTTP → [[TCP]], [[DNS]]
- **Programmazione/scripting**: Python + Bash (automazione).
- **Crittografia di base**: hash, simmetrico/asimmetrico, TLS → [[Funzioni Hash]], [[TLS/SSL]]

## Milestone 1 — JUNIOR (capire le vulnerabilità)
Obiettivo: conoscere le classi di vulnerabilità e provarle in lab.
- Studia l'**OWASP Top 10** → [[OWASP Top 10]] e tutti i concept: [[Injection]], [[XSS]], [[Broken Access Control]], [[Authentication Failures]], [[SSRF]], [[Cryptographic Failures]], [[Security Misconfiguration]], [[Componenti Vulnerabili]], [[Insecure Design]], [[Logging e Monitoring Failures]]
- **Fondamenti di sicurezza**: [[Triade CIA]], [[Threat Modeling]]
- **Pratica**: PortSwigger Academy (lab APPRENTICE) → [[PortSwigger Labs]]; TryHackMe percorsi base.
- **Tool**: padroneggia Burp e nmap → [[Web Hacking]], [[Arsenale Tool]]
- ✅ *Sai fare*: trovare SQLi/XSS/IDOR in un lab guidato, usare Burp Repeater/Intruder.

## Milestone 2 — MID (metodologia e profondità)
Obiettivo: lavorare in autonomia su target completi.
- **Metodologia di pentest** end-to-end → [[Penetration Testing]]
- **CTF** su più categorie → [[Metodologia CTF]] (Web/Crypto/Pwn/Forensics/Reverse)
- **Privilege escalation** Linux/Windows → [[Privilege Escalation]]
- **Network attacks** → [[Attacchi di Rete]]; **malware** awareness → [[Malware]]
- **Social engineering** → [[Social Engineering]]
- **Difesa/coding sicuro** (per capire l'altra metà) → [[Secure Coding]]
- **Pratica**: PortSwigger PRACTITIONER/EXPERT, HackTheBox macchine medie, CTF a squadre.
- ✅ *Sai fare*: catena recon→exploit→privesc→loot su una macchina, scrivere un mini-report.

## Milestone 3 — PENTESTER (professione)
Obiettivo: ingaggi reali, reporting, scope/etica.
- **Reporting professionale**: rischio, impatto, remediation, executive summary.
- **Specializzazione**: web app avanzato, Active Directory, cloud (AWS/Azure), mobile, o exploit dev.
- **Certificazioni** (opzionali ma utili): eJPT → PNPT/OSCP → OSWE/OSEP.
- **Scope & legge**: autorizzazione scritta, regole d'ingaggio, divulgazione responsabile.
- **Difesa avanzata** trasversale → [[Matrice Attacco-Difesa]]
- ✅ *Sai fare*: condurre un assessment autorizzato, comunicare il rischio al business, restare nello scope.

## Principio guida
La sicurezza si impara **facendo** (lab/CTF) ma si padroneggia **capendo il perché** (threat model, design). [Fonte: Anderson, cap. 1] L'etica e l'autorizzazione vengono **prima** della tecnica.

## Collegamenti
- Vedi anche: [[Arsenale Tool]], [[Matrice Attacco-Difesa]], [[PortSwigger Labs]], [[Penetration Testing]], [[Metodologia CTF]], [[OWASP Top 10]], [[Security Engineering]]

## Fonti
- [PortSwigger Web Security Academy — <https://portswigger.net/web-security>]
- [OWASP Top 10:2025 — <https://owasp.org/Top10/2025/>] → [[OWASP Top 10]]
