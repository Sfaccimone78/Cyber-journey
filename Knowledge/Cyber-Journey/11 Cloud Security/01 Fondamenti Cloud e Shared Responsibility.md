---
tipo: concetto
tag: [cloud, metodologia]
fase: 3
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["Fondamenti Cloud e Shared Responsibility"]
---

# Fondamenti Cloud e Shared Responsibility

## Definizione
Il **cloud computing** è l'erogazione on-demand di risorse di calcolo (compute, storage, rete,
servizi gestiti) tramite Internet con modello pay-per-use. Dal punto di vista security cambia
radicalmente il **perimetro**: non esiste più un firewall di confine, ma una somma di
configurazioni di identità e servizi. L'errore di sicurezza dominante nel cloud non è l'exploit di
una CVE, ma la **misconfigurazione**.

## Modelli di servizio e responsabilità
Il **Shared Responsibility Model** (modello di responsabilità condivisa) definisce la linea di
demarcazione tra ciò che mette in sicurezza il provider e ciò che resta al cliente. Regola mnemonica:
il provider è responsabile della sicurezza **del** cloud, il cliente della sicurezza **nel** cloud.

| Livello | Esempio | Sicurezza data center / HW | OS / patch | App / dati | IAM e config |
|---|---|---|---|---|---|
| **On-prem** | server fisico | Cliente | Cliente | Cliente | Cliente |
| **IaaS** | EC2, Azure VM | Provider | Cliente | Cliente | Cliente |
| **PaaS** | RDS, App Service | Provider | Provider | Cliente | Cliente |
| **SaaS** | Microsoft 365 | Provider | Provider | Provider | Cliente (identità/dati) |

> [!note] Costante in ogni modello
> **Identità, configurazione e dati restano SEMPRE responsabilità del cliente.** Per questo
> l'[[IAM Cloud (utenti, ruoli, policy)]] è il vero perimetro del cloud.

## Meccanismo: dove nascono i bug
- **Storage pubblico per errore** (bucket [[AWS Sicurezza (S3, EC2, IAM, STS)|S3]] world-readable).
- **Identità sovra-privilegiate** (policy `*:*`, ruoli assumibili da chiunque).
- **Metadata service esposto** via [[SSRF e Metadata Service (IMDS)|SSRF]].
- **Segreti hard-coded** in user-data, variabili d'ambiente, immagini container.
- **Logging spento** → l'attaccante opera in cieco al difensore.

## Esempio pratico — enumerare a chi appartiene un'identità
```bash
# AWS: chi sono io? (identità delle credenziali correnti)
aws sts get-caller-identity
# Output: Account, UserId, Arn — primo comando in ogni assessment cloud

# Azure: contesto corrente (tenant, subscription, utente)
az account show
az ad signed-in-user show
```

## Attacco / Difesa
| Vettore d'attacco | Contromisura difensiva |
|---|---|
| Misconfigurazione storage pubblico | Block Public Access a livello account; scansione continua (Config/Defender) |
| Credenziali esposte in codice/IaC | Secret scanning (git-secrets, gitleaks), vault gestiti |
| Privilegi eccessivi | Least privilege, IAM Access Analyzer, permission boundaries |
| Assenza di logging | [[Logging e Detection Cloud (CloudTrail)|CloudTrail]]/Activity Log sempre attivi e immutabili |
| Account/regioni non monitorate | Org-wide guardrail (SCP, Azure Policy), inventario centralizzato |

## Lab
- **flaws.cloud** — http://flaws.cloud/ e **flaws2.cloud** — http://flaws2.cloud/ (percorso guidato S3/IAM)
- **CloudGoat** (Rhino Security) — https://github.com/RhinoSecurityLabs/cloudgoat (scenari Terraform deliberatamente vulnerabili)
- **AWS Free Tier** — https://aws.amazon.com/free/ / **Azure Free Account** — https://azure.microsoft.com/free/
- **TryHackMe** — room *Cloud Fundamentals* e *AWS Basics*
- **HackTricks Cloud** — https://cloud.hacktricks.wiki/

> [!warning] Etica
> Sperimenta solo su **account cloud di tua proprietà**, su lab dedicati (flaws.cloud, CloudGoat) o
> con autorizzazione scritta. Enumerare o accedere a risorse cloud di terzi è reato.

## Collegamenti
- [[IAM Cloud (utenti, ruoli, policy)]]
- [[AWS Sicurezza (S3, EC2, IAM, STS)]]
- [[Azure e Entra ID Sicurezza]]
- [[IAM e Zero Trust]]
- [[Penetration Testing]]

## Fonti
- AWS Shared Responsibility Model: https://aws.amazon.com/compliance/shared-responsibility-model/
- Microsoft — Shared responsibility in the cloud: https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility
- HackTricks Cloud — Pentesting Cloud Methodology: https://cloud.hacktricks.wiki/en/pentesting-cloud/pentesting-cloud-methodology.html
