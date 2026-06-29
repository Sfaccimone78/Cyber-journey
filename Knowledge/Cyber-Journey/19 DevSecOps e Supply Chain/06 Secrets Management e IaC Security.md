---
tipo: concetto
tag: [devsecops]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Secrets Management e IaC Security"]
---

# Secrets Management e IaC Security

## In breve
Due facce della sicurezza dell'infrastruttura automatizzata. Il **secrets management** affronta il problema dei segreti (API key, password, certificati, token) che proliferano in codice, pipeline e config: non devono mai finire in chiaro nel repository e vanno gestiti con rotazione, accesso minimo e vita breve. L'**IaC security** applica la security as code alla definizione dell'infrastruttura (Terraform, CloudFormation, Kubernetes manifest, Ansible): errori di configurazione qui si replicano su ogni ambiente provisionato, quindi vanno intercettati con scansione statica prima dell'apply.

## Come funziona
**Secrets**: il primo vettore e l'**hardcoding** nel codice o nei file di config, da cui il leak via repository (anche nella git history!). Le soluzioni mature usano un **secret manager** (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager) che inietta i segreti a runtime, supporta **rotazione automatica** e segreti **dinamici** (credenziali generate on-demand con TTL). In pipeline si preferisce **OIDC** per ottenere credenziali temporanee senza segreti statici.

**IaC**: gli strumenti di scansione (Checkov, tfsec, Terrascan) applicano policy a file dichiarativi cercando misconfiguration: bucket S3 pubblici, security group `0.0.0.0/0` su SSH, cifratura disabilitata, ruoli IAM troppo permissivi. Funzionano pre-deploy, integrandosi nella PR.

## Esempi
Secret scanning della history e verifica con gitleaks/trufflehog:

```bash
# gitleaks: scansiona TUTTA la history, non solo il working tree
gitleaks detect --source . --log-opts="--all" --redact -v

# trufflehog: trova e VERIFICA se le chiavi sono ancora attive
trufflehog git file://. --only-verified --json
```

IaC vulnerabile (Terraform) e scansione con checkov/tfsec:

```hcl
# main.tf — misconfiguration tipiche
resource "aws_s3_bucket" "data" {
  bucket = "company-data"
  acl    = "public-read"          # bucket pubblico
}
resource "aws_security_group_rule" "ssh" {
  type        = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]     # SSH aperto al mondo
}
```

```bash
checkov -d . --compact            # policy-as-code su IaC
tfsec . --minimum-severity HIGH   # scanner Terraform dedicato
```

Riferimento a un segreto da Vault invece dell'hardcoding (estratto Terraform):

```hcl
data "vault_generic_secret" "db" {
  path = "secret/data/prod/db"
}
# uso: data.vault_generic_secret.db.data["password"]  -> mai in chiaro nello stato/codice
```

## Mitigazione e difesa
- **Mai segreti nel repo**: secret scanning in pre-commit e in CI sull'intera history; se un segreto trapela, **revocarlo e ruotarlo**, non basta rimuoverlo dal codice.
- Usare un **secret manager** con segreti dinamici a TTL breve e rotazione automatica.
- **OIDC** in pipeline al posto di chiavi cloud long-lived.
- **IaC scanning** (checkov/tfsec) bloccante in PR; policy-as-code con OPA/Conftest per regole organizzative.
- **Least privilege** sui ruoli IAM e attenzione allo **state file** Terraform (puo contenere segreti in chiaro: cifrarlo e proteggerne il backend).

## Lab
- [[TryHackMe]] - room su secrets management e cloud misconfiguration.
- **OWASP WrongSecrets** - applicazione deliberatamente vulnerabile per imparare a trovare ed esfiltrare segreti gestiti male.
- Lab: scansionare un repo Terraform vulnerabile con checkov e correggere i finding; integrare gitleaks in pre-commit.

## Domande
1. **Perche rimuovere un segreto dal codice non basta?** Resta nella git history e potrebbe gia essere stato copiato: va revocato e ruotato.
2. **Cosa sono i segreti dinamici?** Credenziali generate on-demand dal secret manager con TTL breve, che riducono la finestra di esposizione.
3. **Perche OIDC e preferibile alle chiavi statiche in pipeline?** Fornisce credenziali temporanee senza memorizzare segreti a lunga durata.
4. **Cosa cerca un IaC scanner come checkov?** Misconfiguration nei file dichiarativi (bucket pubblici, porte aperte, cifratura assente) prima del deploy.
5. **Perche lo state file Terraform e sensibile?** Puo contenere segreti e dettagli infrastrutturali in chiaro: va cifrato e il backend protetto.

## Approfondimento livello esperto
Il rischio piu sottile e il **leak storico**: un segreto committato e poi "rimosso" resta nella history e nei fork/clone; per questo i framework di igiene delle credenziali (CICD-SEC-6 dell'OWASP) impongono rotazione automatica come default, non solo prevenzione. Sul fronte IaC, la frontiera e lo **shift verso runtime drift detection**: la scansione statica garantisce che il *codice* sia conforme, ma l'infrastruttura reale puo divergere (modifiche manuali). Strumenti che confrontano lo stato dichiarato con quello effettivo chiudono il cerchio. Il pattern d'eccellenza combina **secret manager con segreti dinamici** (un'identita ottiene credenziali DB valide pochi minuti), **OIDC end-to-end** nella pipeline, **policy-as-code** (OPA/Gatekeeper) come gate sia in CI sia in admission control Kubernetes, e cifratura/segregazione dello state. Cosi il segreto a lunga vita - l'asset piu attaccato - tende a scomparire del tutto, riducendo la supply chain a una catena di fiducia effimera e verificabile (vedi [[05 SBOM e SLSA|SBOM e SLSA]]).

## Collegamenti
- [[02 Sicurezza CI-CD Pipeline|Sicurezza CI-CD Pipeline]]
- [[01 Fondamenti DevSecOps|Fondamenti DevSecOps]]
- [[05 SBOM e SLSA|SBOM e SLSA]]
- [[Container Security (Docker)]]
- [[Kubernetes Security (RBAC, escape)]]

## Fonti
- https://owasp.org/www-project-top-10-ci-cd-security-risks/
- https://www.checkov.io/
- https://developer.hashicorp.com/vault/docs/secrets
