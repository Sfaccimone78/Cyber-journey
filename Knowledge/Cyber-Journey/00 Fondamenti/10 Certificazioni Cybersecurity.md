---
tipo: concetto
tag: [carriera]
fase: 0
fonti: 3
aggiornato: 2026-06-22
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

## Collegamenti
- [[Pentester vs SOC]] — i due percorsi a cui mappare le cert
- [[Risk Management e Compliance]] · [[Cos'è la Sicurezza Informatica]]
- TryHackMe · HackTheBox — il lab/portfolio che le accompagna

## Fonti
- Paul Jerimy — Security Certification Roadmap: https://pauljerimy.com/security-certification-roadmap/
- CompTIA — obiettivi d'esame Security+ / PenTest+: https://www.comptia.org/certifications
- Offensive Security — OSCP (PEN-200): https://www.offsec.com/courses/pen-200/
