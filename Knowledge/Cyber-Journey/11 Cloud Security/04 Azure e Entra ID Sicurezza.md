---
tipo: entita
tag: [cloud, windows, ad, metodologia]
fase: 3
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["Azure e Entra ID Sicurezza"]
---

# Azure e Entra ID Sicurezza

## Definizione
**Microsoft Azure** è il secondo cloud per quota di mercato e quello più intrecciato con il mondo
enterprise Windows. La sua identità è **Entra ID** (ex Azure Active Directory): non confonderla con
[[Active Directory]] on-prem — sono sistemi diversi, spesso **sincronizzati** (Entra Connect), e
proprio quella sincronizzazione è un ponte d'attacco ibrido.

## Due piani di controllo separati
| Piano | Cosa governa | Modello di permessi |
|---|---|---|
| **Azure RBAC** | risorse (VM, storage, network) dentro le *subscription* | role assignment su scope (MG → sub → RG → risorsa) |
| **Entra ID** | identità, app, directory roles (es. Global Admin) | directory roles + Graph API permissions |
Un **Owner** su una subscription non è automaticamente **Global Admin** di Entra: ma il Global Admin
può *elevarsi* (`Access management for Azure resources`) e prendere controllo delle subscription.

## Meccanismi d'attacco chiave
- **Managed Identity**: l'equivalente Azure di IMDS — una VM/app ottiene token senza segreti. Se la
  comprometti via [[SSRF e Metadata Service (IMDS)|SSRF]], rubi il token Managed Identity.
- **Service Principal / App con segreti**: app over-privileged su Microsoft Graph (es.
  `RoleManagement.ReadWrite.Directory`) → privilege escalation a directory role.
- **Consent phishing / illicit grant** verso app OAuth.
- **Ibrido**: da on-prem a cloud via **PHS/PTA/AD Connect**, o da cloud a on-prem via **Intune** o
  **Cloud Kerberos**.

## Esempio pratico — enumerazione e furto token
```bash
# Contesto, ruoli RBAC, e directory roles Entra
az account show
az role assignment list --all -o table
az ad signed-in-user show

# Da DENTRO una VM Azure: rubare il token della Managed Identity via IMDS
curl -s -H "Metadata: true" \
 "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"

# Usare il token rubato verso Azure Resource Manager
curl -s -H "Authorization: Bearer <ACCESS_TOKEN>" \
 "https://management.azure.com/subscriptions?api-version=2020-01-01"
```

## Attacco / Difesa
| Vettore d'attacco | Contromisura difensiva |
|---|---|
| Furto token Managed Identity via SSRF | Filtrare `169.254.169.254` dall'app; least privilege sull'identità |
| Service Principal con permessi Graph eccessivi | Review app registrations, rimuovere segreti, usare workload identity federation |
| Consent phishing OAuth | Disabilitare user consent, admin consent workflow |
| Privesc cloud→on-prem (ibrido) | Tiering, proteggere AD Connect (Tier 0), monitorare PHS |
| Account privilegiati senza MFA | Conditional Access, MFA, PIM (just-in-time) |

## Lab
- **Azure Free Account** — https://azure.microsoft.com/free/
- **PurpleCloud** (lab Azure/Entra Terraform) — https://github.com/iknowjason/PurpleCloud
- **AzureGoat** (Ine/Burp) — https://github.com/ine-labs/AzureGoat
- **ROADtools** (enum Entra ID) — https://github.com/dirkjanm/ROADtools / **MicroBurst** — https://github.com/NetSPI/MicroBurst
- **HackTricks Cloud — Azure** — https://cloud.hacktricks.wiki/en/pentesting-cloud/azure-security/index.html
- **TryHackMe** — room *Azure / Entra* e percorso *Cloud*

> [!warning] Etica
> Enumera Entra ID / Azure e ruba token Managed Identity **solo** sul tuo tenant o lab dedicati
> (AzureGoat, PurpleCloud). Operazioni su tenant terzi sono illegali e tracciate dall'Activity Log.

## Collegamenti
- [[Active Directory]]
- [[Kerberos]]
- [[IAM Cloud (utenti, ruoli, policy)]]
- [[SSRF e Metadata Service (IMDS)]]
- [[Privilege Escalation in Cloud]]

## Fonti
- Microsoft — Azure RBAC overview: https://learn.microsoft.com/en-us/azure/role-based-access-control/overview
- Microsoft — Entra ID / Managed Identities: https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview
- HackTricks Cloud — Azure Pentesting: https://cloud.hacktricks.wiki/en/pentesting-cloud/azure-security/index.html
