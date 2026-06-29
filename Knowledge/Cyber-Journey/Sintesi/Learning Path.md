---
tipo: sintesi
tag: [learning-path, roadmap]
aggiornato: 2026-06-28
stato: maturo
aliases: ["Learning Path", "Percorso di Studio", "Curriculum"]
---

# Learning Path — curriculum end-to-end

Percorso completo da **principiante a esperto generalista** di cybersecurity. Ordinato per
**fase** (0→4): ogni fase ha prerequisiti, milestone misurabili e una checklist. Le aree fra
parentesi rimandano alle MOC; segui i numeri dentro ogni area.

> Come usarlo: studia in ordine di fase. Non saltare i prerequisiti — ogni livello assume il
> precedente. Spunta le milestone solo quando sai **spiegarle e applicarle in lab**, non solo
> leggerle.

---

## Fase 0 — Fondamenta (zero → basi)

**Prerequisiti:** nessuno.

**Aree:** [[00 — Mappa Fondamenti|00 Fondamenti]] · [[00 — Mappa Reti|01 Reti]] ·
[[00 — Mappa Linux|02 Linux]]

**Cosa padroneggiare**
- Triade CIA, vulnerabilità/exploit/minaccia, superficie d'attacco, kill chain.
- Stack di rete: [[Modello OSI]], [[Modello TCP-IP]], [[Three-Way Handshake TCP]], [[DNS]], [[ARP]].
- Linux operativo: [[Permessi Linux]], [[Pipe e Redirezione]], [[grep]], [[Bash Scripting]].

**Milestone**
- [ ] Spieghi un pacchetto dal cavo all'app attraversando i layer OSI.
- [ ] Ti muovi in shell Linux senza cercare i comandi base.
- [ ] Completi [[OverTheWire Bandit]] fino a livello ~20.

---

## Fase 1 — Sicurezza di base e teoria di supporto

**Prerequisiti:** Fase 0.

**Aree:** [[00 — Mappa Crittografia|03 Crittografia]] · [[00 — Mappa Windows e AD|04 Windows e AD]]
(prime note) · [[00 — Mappa Sistemi Operativi|08 Sistemi Operativi]] ·
[[00 — Mappa Algoritmi e Strutture Dati|10 Algoritmi e Strutture Dati]]

**Cosa padroneggiare**
- Crypto applicata: [[Crittografia Simmetrica]], [[Crittografia Asimmetrica]], [[Funzioni di Hash]],
  [[Hashing delle Password e Salting]], [[TLS e SSL]].
- Internals OS: [[Processi]], [[Memoria Virtuale]], [[Filesystem]] — base per exploit e forensics.
- Windows base: [[PowerShell]], [[Windows Event Log]], [[SMB]].

**Milestone**
- [ ] Distingui encoding / hashing / encryption e quando usarli.
- [ ] Cracki un hash con [[Hashcat]] / [[John the Ripper]].
- [ ] Spieghi memoria virtuale e perché abilita gli exploit di memoria.

---

## Fase 2 — Offensive web & metodologia (cuore del pentest)

**Prerequisiti:** Fasi 0-1.

**Aree:** [[00 — Mappa Web OWASP|05 Web OWASP]] ·
[[00 — Mappa Metodologia e Tool|06 Metodologia e Tool]] · [[00 — Mappa Python|09 Python]] ·
[[00 — Mappa GRC e Compliance|20 GRC e Compliance]] (governance trasversale)

**Cosa padroneggiare**
- OWASP Top 10 con pratica: [[SQL Injection]], [[Cross-Site Scripting (XSS)]],
  [[Broken Access Control e IDOR]], [[Command Injection]], [[Server-Side Request Forgery (SSRF)]].
- Metodo: [[Metodologia del Pentest]], [[Ricognizione (Recon)]], [[Enumerazione]],
  [[Exploitation]], [[Post-Exploitation]], [[Reporting Pentest]].
- Tooling: [[Nmap]], [[Burp Suite]], [[ffuf]], [[Metasploit]]; automazione con [[Python per la Sicurezza]].

**Milestone**
- [ ] Completi il grosso della [[PortSwigger Web Academy]] (injection, access control, SSRF).
- [ ] Bucchi una macchina easy/medium su [[HackTheBox]] / [[TryHackMe]] end-to-end con report.
- [ ] Scrivi un port scanner e uno script di automazione offensiva in Python.

---

## Fase 3 — Avanzato: AD, cloud, AppSec, dominio esteso

**Prerequisiti:** Fase 2 solida.

**Aree:** [[00 — Mappa Windows e AD|04 Windows e AD]] (avanzato) ·
[[00 — Mappa Cloud Security|11 Cloud Security]] · [[00 — Mappa AppSec Avanzato|12 AppSec Avanzato]] ·
[[00 — Mappa Mobile Security|15 Mobile Security]] · [[00 — Mappa Wireless & Radio|16 Wireless & Radio]] ·
[[00 — Mappa API e GraphQL Security|17 API e GraphQL Security]] ·
[[00 — Mappa AI e LLM Security|18 AI e LLM Security]] ·
[[00 — Mappa DevSecOps e Supply Chain|19 DevSecOps e Supply Chain]]

**Cosa padroneggiare**
- AD offensivo: [[Kerberoasting]], [[Pass-the-Hash]], [[DCSync]], [[NTLM Relay]], [[BloodHound]],
  ADCS/ESC e delegation (note 28-31 di area 04).
- Cloud: [[IAM Cloud (utenti, ruoli, policy)]], [[SSRF e Metadata Service (IMDS)]],
  [[Privilege Escalation in Cloud]], [[Kubernetes Security (RBAC, escape)]].
- AppSec moderno: [[Attacchi JWT]], [[OAuth 2.0 e OpenID Connect Attacks]],
  [[HTTP Request Smuggling]], [[Insecure Deserialization Avanzata (gadget chains)]].
- Domini estesi: mobile, wireless, API, AI/LLM, supply chain.

**Milestone**
- [ ] Compromissione completa di un dominio AD in lab (es. GOAD) inclusa una via ADCS.
- [ ] Sfrutti una catena cloud: IMDS → furto credenziali → privesc.
- [ ] Esegui un attacco di prompt injection indiretto su un'app LLM in lab.

---

## Fase 4 — Esperto: profondità low-level e difesa attiva

**Prerequisiti:** Fase 3.

**Aree:** [[00 — Mappa Reverse Engineering e Exploit Dev|13 Reverse Engineering e Exploit Dev]] ·
[[00 — Mappa DFIR e Detection Engineering|14 DFIR e Detection Engineering]] ·
[[00 — Mappa Blue Team|07 Blue Team]]

**Cosa padroneggiare**
- Exploit dev: [[Stack Buffer Overflow]], [[ret2libc e ROP]],
  [[Bypass Protezioni (ASLR, DEP, Stack Canary, PIE)]], [[Heap Exploitation (introduzione)]].
- RE: [[Analisi Statica con Ghidra]], [[Malware Analysis (statica e dinamica)]].
- Difesa esperta: [[Detection Engineering]], [[Threat Hunting]],
  [[Query di Hunting (KQL e SPL)]], [[Threat Intelligence (Diamond Model, Pyramid of Pain)]].

**Milestone**
- [ ] Scrivi un exploit ROP che bypassa ASLL+NX in lab (pwn.college / ROP Emporium).
- [ ] Analizzi un sample di malware reale (statica + dinamica) e ne estrai gli IOC.
- [ ] Scrivi una regola [[Regole Sigma|Sigma]] su una TTP e la validi in [[Splunk]]/SIEM.

---

## Tracce trasversali (in parallelo, sempre)
- **Pratica continua:** [[TryHackMe]], [[HackTheBox]], CTF — ogni tecnica ha il suo `## Lab`.
- **Ripasso:** usa le sezioni `## Domande` di ogni nota come auto-test (spaced repetition).
- **Carriera:** vedi [[Matrice Ruolo-Cert]] per allineare lo studio a ruolo/certificazione.

## Collegamenti
- [[Analisi e Roadmap Expert]] · [[Matrice Ruolo-Cert]] · [[index|Indice]] · [[overview|Overview]]
