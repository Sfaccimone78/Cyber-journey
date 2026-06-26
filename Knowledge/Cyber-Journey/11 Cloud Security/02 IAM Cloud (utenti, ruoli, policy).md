---
tipo: concetto
tag: [cloud, metodologia]
fase: 3
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["IAM Cloud (utenti, ruoli, policy)"]
---

# IAM Cloud (utenti, ruoli, policy)

## Definizione
**IAM** (Identity and Access Management) è il sottosistema che decide *chi* (principal) può fare
*cosa* (action) su *quale risorsa* (resource), sotto *quali condizioni*. Nel cloud l'IAM **è** il
perimetro di sicurezza: chi controlla l'identità controlla l'infrastruttura. Estende i principi di
[[IAM e Zero Trust]] al modello policy-as-data dei provider.

## Meccanismo: i mattoni
- **Principal**: utente, gruppo, ruolo, service account, workload (macchina/container).
- **Credenziali**: password+MFA (umani), **access key** long-lived (programmatiche), **token
  temporanei** STS/OAuth (preferiti — scadono).
- **Policy**: documento (JSON in AWS, role assignment in Azure) che concede/nega permessi.
- **Ruolo (role)**: identità *assumibile* con permessi temporanei. Concetto centrale per
  l'escalation: se puoi assumere un ruolo più potente, sali di privilegio.
- **Trust policy**: definisce *chi può assumere* un ruolo (la porta d'ingresso da difendere).

### Valutazione di una policy (logica AWS)
1. **Deny esplicito** → vince sempre.
2. **Allow esplicito** → concede.
3. **Default** → deny implicito.
La decisione finale è l'intersezione di identity policy, resource policy, SCP, permission boundary
e session policy. Una catena lunga = molte occasioni per errori.

## Esempio pratico — policy IAM e abuso
```json
// Policy pericolosa: wildcard totale = effettivo amministratore
{
  "Version": "2012-10-17",
  "Statement": [{ "Effect": "Allow", "Action": "*", "Resource": "*" }]
}
```
```bash
# Enumerare permessi della propria identità (AWS)
aws iam get-account-authorization-details
aws iam list-attached-user-policies --user-name target-user
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::111122223333:user/target-user \
  --action-names iam:CreateAccessKey iam:PassRole

# Azure: enumerare i ruoli assegnati a un principal
az role assignment list --assignee <objectId> --all -o table
```

## Permessi "tossici" (escalation primitives)
| Permesso | Perché è pericoloso |
|---|---|
| `iam:CreateAccessKey` | Crea credenziali per un altro utente più potente |
| `iam:PassRole` + `ec2:RunInstances` | Avvia una VM con ruolo admin e ne ruba il token |
| `iam:AttachUserPolicy` / `PutUserPolicy` | Si auto-assegna `AdministratorAccess` |
| `sts:AssumeRole` su ruolo potente | Diventa quel ruolo |
| `lambda:CreateFunction` + `PassRole` | Esegue codice con ruolo privilegiato |

## Attacco / Difesa
| Vettore d'attacco | Contromisura difensiva |
|---|---|
| Access key long-lived rubate | Preferire ruoli/STS temporanei; rotazione e scadenza |
| Wildcard `*` nelle policy | Least privilege, IAM Access Analyzer, deny-by-default |
| Trust policy troppo aperta | Restringere `Principal`/condizioni; `aws:SourceAccount` |
| Permission escalation primitives | Permission boundary, separazione duty, review periodica |
| Mancanza MFA | MFA obbligatoria, condizione `aws:MultiFactorAuthPresent` |

## Lab
- **CloudGoat** scenario *iam_privesc_by_rollback* / *iam_privesc_by_key_rotation* — https://github.com/RhinoSecurityLabs/cloudgoat
- **flaws2.cloud** (percorso attacker + defender) — http://flaws2.cloud/
- **PMapper** (analisi grafo privilege escalation IAM) — https://github.com/nccgroup/PMapper
- **HackTricks Cloud — AWS IAM Privesc** — https://cloud.hacktricks.wiki/en/pentesting-cloud/aws-security/aws-privilege-escalation/index.html

> [!warning] Etica
> Esegui enumerazione e abuso di policy solo su account di tua proprietà o lab autorizzati. La
> sola enumerazione IAM lascia tracce in [[Logging e Detection Cloud (CloudTrail)|CloudTrail]].

## Collegamenti
- [[IAM e Zero Trust]]
- [[Privilege Escalation in Cloud]]
- [[AWS Sicurezza (S3, EC2, IAM, STS)]]
- [[Azure e Entra ID Sicurezza]]
- [[Fondamenti Cloud e Shared Responsibility]]

## Fonti
- AWS IAM — Policy evaluation logic: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html
- Rhino Security — AWS IAM Privilege Escalation (24 metodi): https://rhinosecuritylabs.com/aws/aws-privilege-escalation-methods-mitigation/
- HackTricks Cloud — AWS IAM: https://cloud.hacktricks.wiki/en/pentesting-cloud/aws-security/aws-services/aws-iam-enum.html
