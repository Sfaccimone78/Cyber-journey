---
tipo: entita
tag: [cloud, tool, metodologia]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["AWS Sicurezza (S3, EC2, IAM, STS)"]
---

# AWS Sicurezza (S3, EC2, IAM, STS)

## Definizione
**Amazon Web Services (AWS)** è il cloud provider dominante. Quattro servizi concentrano la maggior
parte degli incidenti: **S3** (storage), **EC2** (compute), **IAM** (identità) e **STS** (token
temporanei). Capirne gli abusi tipici copre la maggior parte degli scenari di pentest AWS.

## S3 — Simple Storage Service
Object storage a bucket. Misconfigurazione classica: bucket o oggetti **pubblici**, ACL permissive,
bucket policy con `Principal: *`.
```bash
# Bucket pubblico: accesso anonimo (senza credenziali)
aws s3 ls s3://nome-bucket --no-sign-request
aws s3 cp s3://nome-bucket/segreti.txt . --no-sign-request

# Verifica le protezioni Block Public Access
aws s3api get-public-access-block --bucket nome-bucket
```

## EC2 — Elastic Compute Cloud
Macchine virtuali. Superfici critiche: **user-data** (può contenere segreti), **IMDS** (vedi
[[SSRF e Metadata Service (IMDS)]]), **security group** troppo aperti, **snapshot/AMI pubblici**.
```bash
# Leggere lo user-data di un'istanza (spesso segreti in chiaro)
aws ec2 describe-instance-attribute --instance-id i-0abc --attribute userData \
  --query 'UserData.Value' --output text | base64 -d

# Snapshot EBS condivisi pubblicamente (data leak)
aws ec2 describe-snapshots --restorable-by-user-ids all --owner-ids 111122223333
```

## IAM e STS — identità e token temporanei
**IAM** definisce principal e policy (vedi [[IAM Cloud (utenti, ruoli, policy)]]). **STS** (Security
Token Service) emette **credenziali temporanee** assumendo un ruolo: è il meccanismo di [[Privilege Escalation in Cloud|escalation]] e lateral movement per eccellenza.
```bash
# Assumere un ruolo → credenziali temporanee (AccessKey, SecretKey, SessionToken)
aws sts assume-role \
  --role-arn arn:aws:iam::111122223333:role/AdminRole \
  --role-session-name pwn

# Identità corrente / cross-account
aws sts get-caller-identity
```

## Attacco / Difesa
| Vettore d'attacco | Contromisura difensiva |
|---|---|
| Bucket S3 pubblico | Block Public Access (account + bucket), bucket policy restrittive |
| Segreti in EC2 user-data | Niente segreti in user-data; usare Secrets Manager/SSM Parameter Store |
| Furto credenziali via IMDS | Forzare **IMDSv2** (token-based), hop limit = 1 |
| `AssumeRole` su ruolo potente | Trust policy stretta, `ExternalId`, condizioni MFA |
| Snapshot/AMI pubblici | Audit periodico, blocco condivisione pubblica via SCP |
| Access key esfiltrate | STS temporaneo, rotazione, GuardDuty su uso anomalo |

## Lab
- **flaws.cloud** / **flaws2.cloud** — http://flaws.cloud/ (S3 + IAM + EC2 metadata, percorso completo)
- **CloudGoat** — scenari *ec2_ssrf*, *iam_privesc_* — https://github.com/RhinoSecurityLabs/cloudgoat
- **Pacu** (AWS exploitation framework) — https://github.com/RhinoSecurityLabs/pacu
- **ScoutSuite** / **Prowler** (audit configurazione) — https://github.com/prowler-cloud/prowler
- **HackTricks Cloud — AWS** — https://cloud.hacktricks.wiki/en/pentesting-cloud/aws-security/index.html

> [!warning] Etica
> Usa `--no-sign-request`, `assume-role` e Pacu **solo** su account/bucket di tua proprietà o lab
> autorizzati. Accedere a bucket altrui anche se "pubblici" può configurare accesso abusivo.

## Domande
**D: Cosa rende un bucket S3 esposto e come si verifica?**
R: ACL o bucket policy pubbliche, o "Block Public Access" disabilitato. Si testa senza credenziali con
`aws s3 ls s3://bucket --no-sign-request` o leggendo gli oggetti via URL.

**D: Differenza tra chiavi IAM long-term e token STS?**
R: Le chiavi IAM (`AKIA...`) sono permanenti e pericolose se leakate; STS emette credenziali
**temporanee** (`ASIA...` + session token, con scadenza) → blast radius ridotto. Preferire STS/ruoli.

**D: Cos'è l'instance profile di EC2 e perché è un bersaglio?**
R: Un ruolo IAM collegato all'istanza; le sue credenziali sono leggibili dal servizio metadata (IMDS).
Una [[SSRF e Metadata Service (IMDS)|SSRF]] verso `169.254.169.254` le esfiltra.

## Collegamenti
- [[IAM Cloud (utenti, ruoli, policy)]]
- [[SSRF e Metadata Service (IMDS)]]
- [[Privilege Escalation in Cloud]]
- [[Logging e Detection Cloud (CloudTrail)]]
- [[Fondamenti Cloud e Shared Responsibility]]

## Fonti
- AWS Security Documentation: https://docs.aws.amazon.com/security/
- AWS — S3 Block Public Access: https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html
- HackTricks Cloud — AWS Pentesting: https://cloud.hacktricks.wiki/en/pentesting-cloud/aws-security/index.html
