---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Risk Management e Compliance"]
---
# Risk Management e Compliance

## In breve
La sicurezza non è solo tecnica: è soprattutto **gestione del rischio**. Il **Risk Management** è il processo di identificare, valutare e trattare i rischi informatici in modo proporzionato. La **Compliance** è l'aderenza a normative e standard (GDPR, ISO 27001, NIST). Insieme formano la **GRC** (Governance, Risk, Compliance), il linguaggio con cui la sicurezza dialoga col business.

## Concetti chiave
- **Rischio** = Probabilità × Impatto. Si ragiona su asset, [[Vulnerabilità Exploit e Minaccia|minacce e vulnerabilità]].
- **Trattamento del rischio**: *mitigare* (controlli), *trasferire* (assicurazione), *accettare* (entro la soglia), *evitare* (eliminare l'attività).
- **Rischio residuo**: ciò che resta dopo i controlli.
- **Asset & data classification**: proteggere di più ciò che vale di più (vedi [[Triade CIA]]).

## Framework e standard
| Standard | A cosa serve |
|---|---|
| **NIST Cybersecurity Framework** | 5 funzioni: Identify, Protect, Detect, Respond, Recover |
| **ISO/IEC 27001** | sistema di gestione della sicurezza (ISMS) certificabile |
| **NIST SP 800-53 / CIS Controls** | cataloghi di controlli concreti |
| **GDPR** | protezione dei dati personali (UE) — notifica breach entro 72h |
| **PCI-DSS** | dati delle carte di pagamento |

## Esempio pratico
Un'azienda valuta il rischio "ransomware su file server": impatto Alto, probabilità Media → rischio Alto. Trattamento: backup offline (mitiga impatto), formazione anti-[[Social Engineering e Phishing|phishing]] (riduce probabilità), cyber-insurance (trasferisce parte del residuo). Il tutto documentato in un **registro dei rischi**, in linea con il NIST CSF.

## Perché conta
Senza risk management si spende male: troppi controlli dove non serve, nessuno dove serve. La compliance, inoltre, è spesso **obbligatoria** e le sanzioni (es. GDPR) sono pesanti. È la base dei ruoli **GRC** e propedeutica a certificazioni come CISSP/CISM (vedi [[Certificazioni Cybersecurity]]).

## Lab
- **[[TryHackMe]]** → room *Governance & Regulation* e *Risk Management* (percorso *Security Engineer* / *Pre Security*): pratica classificazione dei rischi e mappatura ai controlli.
- **Esercizio con NIST CSF 2.0**: costruisci un piccolo **registro dei rischi** per un asset (es. file server), calcola Probabilità × Impatto, scegli il trattamento (mitiga/trasferisci/accetta/evita) e mappa i controlli sulle 5 funzioni Identify/Protect/Detect/Respond/Recover.
- **Gap assessment CIS Controls**: prendi 5 CIS Controls e verifica quali sono implementati in un ambiente di studio, annotando il rischio residuo.

## Domande
1. **D:** Come si compone il rischio in questa nota? **R:** Rischio = Probabilità × Impatto, valutato su asset, minacce e vulnerabilità.
2. **D:** Quali sono le quattro strategie di trattamento del rischio? **R:** Mitigare (controlli), trasferire (assicurazione), accettare (entro soglia), evitare (eliminare l'attività).
3. **D:** Cos'è il rischio residuo? **R:** Ciò che resta del rischio dopo aver applicato i controlli.
4. **D:** Quali sono le 5 funzioni del NIST Cybersecurity Framework? **R:** Identify, Protect, Detect, Respond, Recover.
5. **D:** Entro quanto il GDPR impone di notificare un data breach? **R:** Entro 72 ore.

## Collegamenti
- [[Triade CIA]]
- [[Vulnerabilità Exploit e Minaccia]]
- [[CVE e CVSS]]
- [[Difesa in Profondità]]
- [[Certificazioni Cybersecurity]]
- [[Incident Response]]

## Fonti
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- ISO/IEC 27001: https://www.iso.org/standard/27001
- NIST SP 800-30 — Guide for Conducting Risk Assessments: https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final
