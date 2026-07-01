---
tipo: concetto
tag: [windows, ad, sysadmin, blue-team]
fase: 3
fonti: 3
aggiornato: 2026-06-29
stato: maturo
aliases: ["Hardening di Active Directory"]
---

# Hardening di Active Directory (AD)

Active Directory è spesso il bersaglio principale durante le fasi di post-exploitation e privilege escalation. Mantenere un'infrastruttura AD sicura è fondamentale per ogni Sysadmin.

## 1. Principi di Base
- **Tiering Model (Modello a Livelli)**: Separare le credenziali amministrative in Tier (Es. Tier 0 per i Domain Controller, Tier 1 per i server, Tier 2 per le workstation). Un admin di Tier 2 non deve mai loggarsi su un sistema Tier 0.
- **Principle of Least Privilege (PoLP)**: Assegnare agli utenti solo i permessi strettamente necessari.

## 2. Protezione delle Credenziali
- **Disabilitare NTLMv1**: Utilizzare esclusivamente NTLMv2 o, preferibilmente, Kerberos.
- **LAPS (Local Administrator Password Solution)**: Implementare LAPS per randomizzare le password degli amministratori locali sulle macchine a dominio, prevenendo attacchi di Pass-the-Hash e movimento laterale.
- **Protezione di LSASS**: Abilitare Credential Guard su Windows 10/11 e Windows Server per isolare il processo LSASS e proteggere i ticket Kerberos e gli hash in memoria.

## 3. Configurazione Sicura
- **SMB Signing**: Richiedere la firma SMB per prevenire attacchi di tipo SMB Relay.
- **LDAP Signing e Channel Binding**: Forzare l'uso di comunicazioni sicure verso i Domain Controller per evitare attacchi Man-in-the-Middle e credenziali in chiaro.

## 4. Monitoraggio
- Abilitare l'auditing avanzato tramite Group Policy Object (GPO) per monitorare eventi critici (Es. Event ID 4624 per i Logon, 4728 per l'aggiunta a gruppi privilegiati).
- Utilizzare tool come **BloodHound** o **PingCastle** internamente per scansionare la propria AD alla ricerca di misconfigurazioni.


## Collegamenti
- [[Active Directory]]
- [[Kerberoasting]]
- [[DCSync]]
- [[LAPS]]
- [[BloodHound]]
- [[NTLM]]

## Fonti
- Microsoft — Best Practices for Securing Active Directory: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/best-practices-for-securing-active-directory
- MITRE ATT&CK — Enterprise (Windows/AD): https://attack.mitre.org/matrices/enterprise/windows/
- ANSSI — Active Directory Security (PingCastle model): https://www.cert.ssi.gouv.fr/uploads/guide-ad.html
