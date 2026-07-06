---
tipo: entita
tag: [cloud, blue-team, tool]
fase: 3
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Logging e Detection Cloud (CloudTrail)"]
---

# Logging e Detection Cloud (CloudTrail)

## In breve
Nel cloud ogni azione è una **chiamata API**, quindi ogni azione è un **evento loggabile**: **CloudTrail** (AWS), **Activity Log** + log Entra ID (Azure) e **Cloud Audit Logs** (GCP) registrano chi ha fatto cosa, quando e da dove. È la pagina lato blue team che ribalta in detection tutto ciò che le precedenti hanno visto dal lato offensivo. Gli eventi si normalizzano in un SIEM per hunting e alerting su segnali di privesc/anti-forensics (`AssumeRole`, `AttachUserPolicy`, `StopLogging`), mappati su MITRE ATT&CK.

## Definizione
Nel cloud ogni azione è una **chiamata API**, quindi **ogni azione è un evento loggabile**.
**AWS CloudTrail** registra le API call sull'account (chi, cosa, quando, da quale IP); l'equivalente
Azure è l'**Activity Log** + i log di **Entra ID**, su GCP il **Cloud Audit Logs**. Questa pagina
ribalta sul blue team (cfr. [[Logging e Monitoraggio]] e l'area [[MITRE ATT&CK]]) tutto ciò che le
pagine precedenti hanno descritto dal lato offensivo.

## Meccanismo: cosa cattura CloudTrail
- **Management events**: operazioni sul control plane (`RunInstances`, `AttachUserPolicy`, `AssumeRole`...).
- **Data events**: operazioni sui dati (S3 `GetObject`, Lambda invoke) — alto volume, opt-in.
- **Insights**: rilevamento anomalie sul tasso di API call.
Gli eventi finiscono su S3 e/o CloudWatch Logs; si normalizzano in un **SIEM** ([[Splunk]],
OpenSearch, Sentinel) per detection e [[Threat Intelligence|threat hunting]].

## Esempio pratico — caccia ad attività sospette
```bash
# Verificare che il trail sia attivo e multi-region (un trail spento = cieco)
aws cloudtrail describe-trails
aws cloudtrail get-trail-status --name my-trail

# Cercare AssumeRole e creazione chiavi (segnali di privesc)
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRole

# Azure: attività recente nel control plane
az monitor activity-log list --offset 1h -o table
```
Eventi-spia da allertare: `CreateAccessKey`, `AttachUserPolicy`, `AssumeRole` insolito,
`StopLogging`/`DeleteTrail` (anti-forensics), `GetCallerIdentity` a raffica, accessi `GetObject` su
bucket sensibili da IP nuovi.

## Detection: tecniche e firma (mappate a MITRE ATT&CK)
| Attività sospetta | Evento / segnale | Tecnica ATT&CK |
|---|---|---|
| Disattivazione logging | `StopLogging`, `DeleteTrail` | T1562.008 Impair Defenses |
| Furto credenziali via metadata | uso credenziali ruolo da IP esterno | T1552.005 Metadata API |
| Privesc IAM | `AttachUserPolicy`, `PutUserPolicy` | T1098 Account Manipulation |
| Persistenza | nuovo `CreateUser`/`CreateAccessKey` | T1136 Create Account |
| Esfiltrazione dati | spike di `GetObject` su S3 | T1530 Data from Cloud Storage |

## Attacco / Difesa
| Mossa dell'attaccante | Contromisura del difensore |
|---|---|
| Spegnere CloudTrail | Trail org-wide immutabile, allarme su `StopLogging`, log in account separato |
| Cancellare i log su S3 | Bucket con Object Lock/MFA Delete, accesso log isolato |
| Operare sotto-soglia | Baseline + anomaly detection (GuardDuty, Insights, UEBA) |
| Usare regioni non monitorate | Trail multi-region, SCP che limita le regioni |

**Servizi gestiti di detection:** AWS **GuardDuty**, Azure **Defender for Cloud** / **Sentinel**,
GCP **Security Command Center**.

## Lab
- **flaws2.cloud** — percorso *Defender* (analisi CloudTrail post-attacco) — http://flaws2.cloud/
- **CloudGoat** + analisi dei log generati — https://github.com/RhinoSecurityLabs/cloudgoat
- **TryHackMe** — room cloud blue team / *AWS basics + logging*
- **MITRE ATT&CK Cloud Matrix** — https://attack.mitre.org/matrices/enterprise/cloud/
- **HackTricks Cloud — Logging / Monitoring** — https://cloud.hacktricks.wiki/en/pentesting-cloud/aws-security/aws-services/aws-cloudtrail-enum.html

> [!warning] Etica
> Analizza CloudTrail/Activity Log **solo** dei tuoi account o dei lab. I log contengono dati
> sensibili (IP, ARN, identità): trattali con la stessa cura dei dati di produzione.

## Domande
**D: Cosa cattura CloudTrail di default e cosa no?**
R: Cattura gli eventi **management plane** (chiamate API: chi, cosa, quando, da dove). **Non** cattura
di default i **data events** ad alto volume (es. S3 `GetObject`, Lambda invoke) — vanno abilitati a parte.

**D: Quali tecniche usano gli attaccanti per evadere il logging cloud?**
R: `StopLogging`/`DeleteTrail`, alterare o rendere pubblico il bucket dei log, operare in **region non
monitorate**, o usare credenziali in account non coperti dal trail. MITRE **T1562** (Impair Defenses).

**D: Quali IOC cercare in CloudTrail?**
R: `CreateUser`/`AttachUserPolicy` anomali, `AssumeRole` inusuali, `GetSecretValue`/`Decrypt` di massa,
`ConsoleLogin` senza MFA, chiamate da IP/User-Agent inattesi, `StopLogging`.

## Collegamenti
- [[Logging e Monitoraggio]]
- [[MITRE ATT&CK]]
- [[SIEM]]
- [[Splunk]]
- [[Privilege Escalation in Cloud]]
- [[SSRF e Metadata Service (IMDS)]]

## Fonti
- AWS — CloudTrail User Guide: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html
- Microsoft — Azure Activity Log: https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/activity-log
- MITRE ATT&CK — Cloud Matrix: https://attack.mitre.org/matrices/enterprise/cloud/
