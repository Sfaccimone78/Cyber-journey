---
tipo: concetto
tag: [carriera]
fase: 0
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Certificazioni Cybersecurity"]
---

# Certificazioni Cybersecurity

## In breve
Le certificazioni sono **prova verificabile** di competenza: nel mondo offensive/blue contano soprattutto quelle **hands-on** (esame pratico in lab), molto più di quelle solo a quiz. Servono per superare il filtro HR, ma il portfolio reale (TryHackMe/HackTheBox, writeup, GitHub) pesa quanto la sigla. Mappa le cert sul tuo percorso: [[Pentester vs SOC|Pentester o SOC]].

## Mappa per percorso e livello

### 🎯 Offensive / Pentest
| Cert | Ente | Livello | Tipo esame | Note |
|---|---|---|---|---|
| **eJPT** | INE/eLearnSecurity | entry | pratico | ideale primo traguardo, no prerequisiti |
| **PNPT** | TCM Security | junior+ | pratico + report + C2 | esame realistico AD, ottimo rapporto qualità/prezzo |
| **OSCP** | OffSec | intermedio | 24h lab + report | lo standard di settore, "try harder" |
| **CRTP/CRTE** | Altered Security | AD-focus | pratico | specializzazione [[Active Directory]] |
| **OSEP / OSWE / OSED** | OffSec | avanzato | pratico | evasion, web, exploit dev |

### 🛡️ Blue Team / SOC
| Cert | Ente | Livello | Tipo | Note |
|---|---|---|---|---|
| **BTL1** | Security Blue Team | entry | pratico | triage, [[Log Analysis]], DFIR base |
| **CySA+** | CompTIA | entry/inter | quiz | detection, [[SIEM]], analisi |
| **GCIH / GCIA / GCFA** | GIAC/SANS | inter/avanz | quiz | costose, molto rispettate (IR, forensics) |
| **CDSA** | HackTheBox | inter | pratico | SOC analyst hands-on |

### 🧱 Fondamentali / trasversali
| Cert | Ente | Note |
|---|---|---|
| **Security+** | CompTIA | base teorica, spesso richiesta da HR/contratti |
| **CISSP** | ISC² | management/architettura, 5 anni esperienza |
| **CEH** | EC-Council | nota ma molto teorica, valore pratico discusso |

## Come scegliere
- **Parti pratico**: eJPT (offensive) o BTL1 (blue) prima delle teoriche.
- **Non collezionare sigle**: una cert pratica + portfolio batte tre quiz.
- **Allinea al [[Risk Management e Compliance|contesto lavorativo]]**: in azienda/PA contano Security+, CISSP; in pentest puro contano OSCP, PNPT.
- Verifica sempre il **costo del retake** e la **validità** (alcune scadono e vanno rinnovate).

## Lab
- **[[TryHackMe]]** → percorso *Jr Penetration Tester* come preparazione hands-on all'eJPT; percorso *SOC Level 1* come base per BTL1/CySA+.
- **[[HackTheBox]]** → moduli Academy dei percorsi *CPTS* (offensive) e *CDSA* (blue): esame pratico con report, allineato allo stile OSCP/PNPT.
- Costruisci il **portfolio** che accompagna la cert: risolvi 5-10 macchine/room e pubblica i writeup (blog o GitHub) — vale quanto la sigla nel filtro HR.

## Domande
1. **D:** Perché nel mondo offensive/blue contano di più le certificazioni hands-on? **R:** Perché dimostrano competenza pratica in un lab reale, molto più delle certificazioni solo a quiz; una cert pratica + portfolio batte tre quiz.
2. **D:** Quale certificazione è indicata come ideale primo traguardo offensive e perché? **R:** L'eJPT (INE/eLearnSecurity): è entry-level, pratica e senza prerequisiti.
3. **D:** Qual è considerata lo "standard di settore" del pentest e come è strutturato l'esame? **R:** L'OSCP di OffSec: 24 ore di lab pratico più report.
4. **D:** Cita due certificazioni blue team entry-level. **R:** BTL1 (Security Blue Team, pratica) e CySA+ (CompTIA, a quiz); anche CDSA di HackTheBox lato hands-on.
5. **D:** Oltre al costo dell'esame, cosa conviene sempre verificare prima di scegliere una cert? **R:** Il costo del retake e la validità/scadenza (alcune vanno rinnovate).

## Collegamenti
- [[Pentester vs SOC]] — i due percorsi a cui mappare le cert
- [[Risk Management e Compliance]] · [[Cos'è la Sicurezza Informatica]]
- TryHackMe · HackTheBox — il lab/portfolio che le accompagna

## Fonti
- Paul Jerimy — Security Certification Roadmap: https://pauljerimy.com/security-certification-roadmap/
- CompTIA — obiettivi d'esame Security+ / PenTest+: https://www.comptia.org/certifications
- Offensive Security — OSCP (PEN-200): https://www.offsec.com/courses/pen-200/
