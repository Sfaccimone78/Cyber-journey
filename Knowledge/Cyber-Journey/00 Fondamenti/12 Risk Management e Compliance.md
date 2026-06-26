---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Risk Management e Compliance"]
---
# Risk Management e Compliance

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
