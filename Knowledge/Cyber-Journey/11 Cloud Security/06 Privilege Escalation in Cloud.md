---
tipo: concetto
tag: [cloud, metodologia]
fase: 4
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Privilege Escalation in Cloud"]
---

# Privilege Escalation in Cloud

## In breve
La **privilege escalation in cloud** è il passaggio da un accesso a basso privilegio (utente IAM limitato, ruolo istanza, service account) al controllo dell'intero account/tenant. A differenza dell'on-prem non sfrutta kernel o binari SUID, ma **permessi IAM mal configurati**: la scalata è una catena di chiamate API legittime. Le primitive tipiche (AWS) sono modifica della propria policy, creazione credenziali per altri, `iam:PassRole` + servizio di esecuzione e `sts:AssumeRole`; la difesa più forte sono **permission boundary** e **SCP**.

## Definizione
La **privilege escalation in cloud** è il passaggio da un accesso a basso privilegio (un utente IAM
limitato, un ruolo istanza, un service account) al controllo dell'account/tenant. A differenza della
[[Privilege Escalation Linux]] o [[Privilege Escalation Windows]], qui **non si sfruttano kernel o
binari SUID**, ma **permessi IAM mal configurati**: la scalata è una catena di chiamate API legittime.

## Meccanismo: le primitive
Quasi tutte le tecniche AWS ricadono in poche famiglie (riferimento: Rhino Security, 24 metodi):
- **Modifica della propria policy**: `iam:PutUserPolicy`, `iam:AttachUserPolicy`, `iam:CreatePolicyVersion`
  (crei una nuova versione `Action:*`/`Resource:*` di una policy già collegata e la imposti come default) → ti dai `AdministratorAccess`.
- **Creazione credenziali per altri**: `iam:CreateAccessKey`, `iam:CreateLoginProfile`, `iam:UpdateLoginProfile`.
- **PassRole + servizio di esecuzione**: `iam:PassRole` con `ec2:RunInstances` / `lambda:CreateFunction`
  / `glue` / `cloudformation` → esegui codice con un ruolo più potente e ne rubi il token.
- **AssumeRole**: `sts:AssumeRole` su un ruolo con trust policy troppo aperta.
- **Data/backdoor**: modifica di resource policy (es. bucket, KMS key) per concedersi accesso.

> [!note] Ordine di valutazione delle policy AWS (perché una primitiva funziona)
> IAM è **default-deny** e valuta in quest'ordine: **explicit Deny** (vince sempre) → **SCP**
> (Organizations) → **resource policy** → **permission boundary** → **session policy** → **identity
> policy**. Un `Deny` esplicito o un boundary/SCP battono qualsiasi `Allow`: per questo i **permission
> boundary** e le **SCP** sono la difesa più forte contro l'auto-escalation.

## Esempio pratico — privesc via PassRole
```bash
# 1) Ho iam:PassRole + ec2:RunInstances. Trovo un ruolo admin assegnabile a EC2
aws iam list-instance-profiles

# 2) Avvio un'istanza con quel profilo (instance profile = ruolo admin)
aws ec2 run-instances --image-id ami-0abc --instance-type t2.micro \
  --iam-instance-profile Name=AdminInstanceProfile \
  --user-data file://payload.sh

# 3) Dalla nuova istanza, l'IMDS espone le credenziali admin (vedi pagina IMDS)
#    -> game over: ora opero come AdminRole

# Alternativa diretta: mi auto-assegno AdministratorAccess
aws iam attach-user-policy --user-name me \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```
```bash
# Azure: elevarsi da Owner di subscription verso il piano risorse
az role assignment create --assignee <id> --role Owner --scope /subscriptions/<sub-id>
```

## Attacco / Difesa
| Primitiva d'escalation | Contromisura difensiva |
|---|---|
| `iam:PassRole` + RunInstances/Lambda | Vincolare `iam:PassRole` a ruoli specifici via `Resource`/condizioni |
| `Attach/Put UserPolicy` su sé stessi | **Permission boundary** che capping i privilegi effettivi |
| `CreateAccessKey` su altri utenti | Separazione duty, allarmi su creazione chiavi |
| `AssumeRole` su ruolo aperto | Trust policy stretta + `ExternalId` + MFA |
| Modifica resource policy (S3/KMS) | SCP che vieta `*:PutPolicy` pubblico; Access Analyzer |

## Strumenti
- **PMapper** — calcola il grafo di chi-può-diventare-chi: `pmapper graph create`, `pmapper query "preset privesc *"`.
- **Pacu** — moduli `iam__privesc_scan`.
- **ScoutSuite/Prowler** — segnalano permessi tossici in audit.

## Lab
- **CloudGoat** — *iam_privesc_by_rollback*, *iam_privesc_by_key_rotation*, *ec2_ssrf* — https://github.com/RhinoSecurityLabs/cloudgoat
- **flaws2.cloud** — http://flaws2.cloud/
- **AzureGoat** — https://github.com/ine-labs/AzureGoat
- **HackTricks Cloud — AWS Privesc (catalogo)** — https://cloud.hacktricks.wiki/en/pentesting-cloud/aws-security/aws-privilege-escalation/index.html

> [!warning] Etica
> Le primitive qui descritte modificano permessi reali. Eseguile **solo** su account di tua
> proprietà o lab (CloudGoat/AzureGoat). Su infrastrutture terze costituiscono reato.

## Domande
**D: Come funziona una privesc via `iam:PassRole`?**
R: Un'identità con `iam:PassRole` + un servizio che esegue codice (`lambda:CreateFunction`,
`ec2:RunInstances`, `glue`...) può "passare" un ruolo più privilegiato a una risorsa che controlla e
farci girare codice → eredita quei permessi.

**D: Perché la privesc cloud è diversa da quella on-prem?**
R: Raramente sfrutta bug del kernel; abusa di **relazioni di permessi IAM e API** (spesso
misconfigurazioni "by design"). Si ragiona su grafi di permessi, non su exploit di memoria.

**D: Quali strumenti mappano i percorsi di privesc?**
R: **Pacu** (exploitation AWS), **PMapper** e **cloudsplaining** (analisi grafo permessi),
**ScoutSuite**/**Prowler** (audit posture multi-cloud).

## Collegamenti
- [[IAM Cloud (utenti, ruoli, policy)]]
- [[Privilege Escalation (Concetti)]]
- [[Privilege Escalation Linux]]
- [[Privilege Escalation Windows]]
- [[SSRF e Metadata Service (IMDS)]]
- [[AWS Sicurezza (S3, EC2, IAM, STS)]]

## Fonti
- Rhino Security — AWS Privilege Escalation Methods & Mitigation: https://rhinosecuritylabs.com/aws/aws-privilege-escalation-methods-mitigation/
- NCC Group — PMapper: https://github.com/nccgroup/PMapper
- MITRE ATT&CK — Cloud, Privilege Escalation tactic: https://attack.mitre.org/matrices/enterprise/cloud/
