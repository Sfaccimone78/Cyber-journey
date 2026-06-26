---
tipo: concetto
tag: [blue-team]
fase: 2
fonti: 4
aggiornato: 2026-06-21
stato: maturo
aliases: ["Incident Response"]
---

# Incident Response

## In breve
L'**Incident Response (IR)** è il processo strutturato per **rilevare, contenere, eradicare e ripristinare** dopo un incidente di sicurezza. Un piano IR riduce il *blast radius*, i tempi di ripristino e i costi legali. Il riferimento è **NIST SP 800-61** (4 fasi); SANS usa un modello a 6 fasi (PICERL).

## Le fasi (NIST vs SANS)
| NIST SP 800-61 | SANS PICERL |
|---|---|
| 1. Preparazione | Preparation |
| 2. Detection & Analysis | Identification |
| 3. Containment, Eradication & Recovery | Containment · Eradication · Recovery |
| 4. Post-Incident Activity | Lessons Learned |

### 1. Preparazione
Ruoli, playbook, contatti, autorità. Strumenti pronti **prima**: [[SIEM]], EDR, backup testati, jump-bag forense. Senza preparazione, ogni fase dopo è caos.

### 2. Detection & Analysis
Alert da [[SIEM]]/EDR/IDS → [[Triage degli Alert]] (vero positivo o rumore?) → raccolta [[Indicatori di Compromissione (IOC)]] e mappatura su [[MITRE ATT&CK]] per capire **dove** è l'attaccante nella kill chain. Determinare scope: quanti host, quali account.

### 3. Containment / Eradication / Recovery
- **Contenimento breve**: isolare l'host dalla rete (mantieni acceso per la forensics — non spegnere, perdi la RAM).
- **Contenimento lungo**: patch temporanee, blocco IP/account, segmentazione.
- **Eradicazione**: rimuovere malware, chiudere backdoor, **resettare le credenziali compromesse** (incluso krbtgt se toccato un DC).
- **Recovery**: ripristino da backup pulito, rientro graduale, **monitoraggio rinforzato** per recidive.

### 4. Post-Incident (Lessons Learned)
Report con **timeline**, root cause, azioni, e miglioramenti. Riunione entro ~2 settimane. Output che alimenta la Preparazione del prossimo incidente.

## Ordine di volatilità (forensics)
Raccogliere le prove dal più volatile al meno volatile, altrimenti spariscono:
```
RAM / processi / connessioni → stato di rete → disco → log remoti → backup/archivi
```

## Esempio pratico — phishing con payload
```
1. SIEM: PowerShell anomalo (4688) su HOST-12, mappa → T1059.001
2. Triage: confermato malevolo (download da IP raro) → IOC: hash, IP C2, dominio
3. Containment breve: isola HOST-12 (acceso), dump RAM
4. Hunt: cerca gli stessi IOC sugli altri host (lateral?) via EDR/SIEM
5. Eradicazione: rimuovi persistenza (Run key T1547), reset credenziali utente
6. Recovery: reimage da golden image, monitor 2 settimane
7. Lessons: blocca macro Office, abilita ScriptBlock Logging
```

## Rilevanza per la sicurezza
IR sposta l'organizzazione da reazione caotica a risposta **ripetibile e misurabile** (MTTD/MTTR). Vincoli legali: il **GDPR** impone notifica al garante **entro 72 ore** da una violazione di dati personali.

## Collegamenti
- [[SIEM]]
- [[Triage degli Alert]]
- [[Indicatori di Compromissione (IOC)]]
- [[MITRE ATT&CK]]
- [[La Cyber Kill Chain]]
- [[Analisi Malware di Base]]
- [[Any.run]]

## Fonti
- NIST SP 800-61r2 — Computer Security Incident Handling Guide: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf
- SANS — Incident Handler's Handbook: https://www.sans.org/white-papers/33901/
- LetsDefend — Incident Response path: https://letsdefend.io/blog/incident-response-learning-path/
- CISA — Incident Response Playbooks: https://www.cisa.gov/sites/default/files/publications/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf
