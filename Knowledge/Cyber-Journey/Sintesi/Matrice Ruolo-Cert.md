---
tipo: sintesi
tag: [carriera, certificazioni]
aggiornato: 2026-06-28
stato: maturo
aliases: ["Matrice Ruolo-Cert", "Matrice Ruolo Cert", "Ruolo e Certificazioni"]
---

# Matrice Ruolo / Certificazione → aree della wiki

Cross-walk fra **ruoli** e **certificazioni** comuni e le aree/note da studiare. Serve a orientare
lo studio quando punti a un obiettivo specifico, senza perdere l'impianto da generalista del
[[Learning Path]].

> La wiki è pensata per una **conoscenza ampia ed equilibrata**: nessuna cert è il fine. Questa
> matrice è una *vista* sopra lo stesso contenuto, non un percorso alternativo.

---

## Per ruolo

| Ruolo | Aree centrali | Aree di supporto |
|-------|---------------|------------------|
| **Penetration Tester / Red Team** | 04 Windows e AD · 05 Web · 06 Metodologia · 11 Cloud · 12 AppSec · 17 API | 01 Reti · 02 Linux · 09 Python · 13 RE/Exploit |
| **Web/AppSec Engineer** | 05 Web · 12 AppSec Avanzato · 17 API e GraphQL · 18 AI/LLM | 03 Crittografia · 19 DevSecOps |
| **SOC Analyst / Blue Team** | 07 Blue Team · 14 DFIR · 04 Windows (log/AD) | 01 Reti · 02 Linux · 20 GRC |
| **DFIR / Forensics** | 14 DFIR · 13 RE (malware) · 08 Sistemi Operativi | 04 Windows · 07 Blue Team |
| **Cloud Security Engineer** | 11 Cloud · 19 DevSecOps · 17 API | 04 IAM/AD · 20 GRC |
| **DevSecOps Engineer** | 19 DevSecOps · 11 Cloud (container/K8s) · 12 AppSec | 09 Python · 17 API |
| **Exploit Developer / Vuln Researcher** | 13 RE/Exploit · 08 Sistemi Operativi · 10 Algoritmi | 02 Linux · 09 Python |
| **GRC / Security Manager** | 20 GRC · 00 Fondamenti | tutte (visione d'insieme) |
| **Mobile Security Tester** | 15 Mobile · 17 API · 12 AppSec | 03 Crittografia · 13 RE |
| **Red Team Infrastructure / AD specialist** | 04 Windows e AD (incl. ADCS/delegation) · 06 Metodologia | 11 Cloud · 16 Wireless |

---

## Per certificazione

| Cert | Focus | Aree prioritarie nella wiki |
|------|-------|-----------------------------|
| **CompTIA Security+** | base generalista | 00 Fondamenti · 01 Reti · 03 Crittografia · 20 GRC |
| **eJPT** | pentest entry | 01 Reti · 02 Linux · 05 Web · 06 Metodologia |
| **PNPT / OSCP** | pentest pratico | 04 Windows e AD · 05 Web · 06 Metodologia · 02 Linux · 09 Python |
| **CRTP / CRTE** | Active Directory | 04 Windows e AD (incl. Kerberos, ADCS 28-31, delegation, [[BloodHound]]) |
| **OSWE** | web white-box | 05 Web · 12 AppSec Avanzato · 17 API · 09 Python |
| **OSED / OSEE** | exploit dev | 13 RE/Exploit · 08 Sistemi Operativi · 10 Algoritmi |
| **eMAPT / mobile** | mobile | 15 Mobile · 17 API |
| **CCSP / cloud cert** | cloud | 11 Cloud · 19 DevSecOps · 20 GRC |
| **BTL1 / CySA+** | blue team | 07 Blue Team · 14 DFIR · 04 Windows (log) |
| **GCFA / GCFE** | forensics | 14 DFIR · 08 Sistemi Operativi · 04 Windows |
| **CISSP / CISM** | management/GRC | 20 GRC · 00 Fondamenti · visione su tutte le aree |
| **GMON / detection** | detection eng. | 14 DFIR · 07 Blue Team |

---

## Come usarla
1. Scegli ruolo o cert obiettivo.
2. Studia prima le **aree centrali/prioritarie** seguendo il [[Learning Path]] per le fasi.
3. Le **aree di supporto** colmano i prerequisiti mancanti.
4. Valida con i `## Lab` e auto-testati con i `## Domande` di ogni nota.

## Collegamenti
- [[Learning Path]] · [[Certificazioni Cybersecurity]] · [[Percorsi di Carriera Pentester vs SOC]]
- [[Analisi e Roadmap Expert]] · [[index|Indice]]
