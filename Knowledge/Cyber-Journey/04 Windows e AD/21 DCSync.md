---
tipo: concetto
tag: [windows, ad]
fase: 3
fonti: 3
aggiornato: 2026-06-21
stato: maturo
aliases: ["DCSync"]
---

# DCSync

> **Nota etica**: tecnica da usare solo in lab autorizzati (TryHackMe, HTB, CTF) o engagement con permesso scritto.

## In breve
**DCSync** abusa della replica di [[Active Directory]] per **chiedere al Domain Controller gli hash delle password** di qualunque account — incluso `krbtgt` — **senza eseguire codice sul DC**. L'attaccante si finge un altro DC e invoca l'API di replica **DRSUAPI** (`DRSGetNCChanges`). È il modo standard per estrarre le credenziali del dominio una volta ottenuti i diritti giusti, ed è il trampolino verso il **Golden Ticket** (vedi [[Kerberos]]).

## Come funziona (meccanismo)
La replica AD prevede che i DC si scambino le modifiche del database `NTDS.dit`. Chi possiede i diritti di replica può chiamare `DRSGetNCChanges` e ricevere indietro i **secrets** (NT hash, chiavi Kerberos) cifrati con la PEK. DCSync **non** legge il disco del DC: parla l'API legittima, quindi non lascia tracce di accesso a file/processi sul DC.

**Diritti richiesti** sull'oggetto dominio (uno qualsiasi basta):
- `DS-Replication-Get-Changes`
- `DS-Replication-Get-Changes-All`

Li hanno per default: **Domain Admins**, **Enterprise Admins**, **Administrators**, e gli account DC. Un'ACL mal configurata che concede questi diritti a un utente normale = DCSync senza essere admin (trovabile con [[BloodHound]], edge `GetChanges`/`GetChangesAll`).

## Esempio pratico
Da Linux con [[Impacket]] (servono credenziali con diritti di replica):
```bash
# Dump di un singolo utente (krbtgt → Golden Ticket)
impacket-secretsdump -just-dc-user krbtgt DOMINIO/admin:'Password!'@10.10.10.1

# Dump completo del dominio (tutti gli NT hash)
impacket-secretsdump -just-dc DOMINIO/admin:'Password!'@10.10.10.1
```
Da Windows con [[Mimikatz]]:
```
lsadump::dcsync /domain:dominio.local /user:krbtgt
```
Output utile: `krbtgt` NT hash → forgi un **Golden Ticket**; hash di un Domain Admin → [[Pass-the-Hash]].

## Verificare/trovare i diritti
```bash
# bloodyAD: chi ha i diritti di replica
bloodyAD --host 10.10.10.1 -d dominio.local -u user -p pass get writable --right
```
Vedi [[bloodyAD]]. In [[BloodHound]]: query `MATCH p=()-[:GetChangesAll]->() RETURN p`.

## Detection e difesa
- **Event ID 4662** sul DC con accesso all'oggetto e GUID `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2` (Get-Changes) / `1131f6ad-...` (Get-Changes-All): replica richiesta da un **principal che NON è un DC** = forte indicatore DCSync.
- Correlare con **traffico DRSUAPI** da host non-DC (regola di rete).
- **Tier 0 / least privilege**: nessun account non-DC deve avere i diritti di replica; audit ACL del dominio.
- Dopo compromissione `krbtgt`: **ruotare due volte** la password di `krbtgt`.
- MITRE ATT&CK: **T1003.006** (OS Credential Dumping: DCSync).

## Collegamenti
- [[Active Directory]] — la kill chain di cui DCSync è lo step finale
- [[Kerberos]] — Golden Ticket usa l'hash `krbtgt` estratto qui
- [[Pass-the-Hash]] — uso diretto degli hash estratti
- [[Impacket]] · [[Mimikatz]] · [[bloodyAD]] · [[BloodHound]]
- [[Windows Event Log]] — Event ID 4662

## Fonti
- The Hacker Recipes — DCSync: https://www.thehacker.recipes/ad/movement/credentials/dumping/dcsync
- MITRE ATT&CK — T1003.006: https://attack.mitre.org/techniques/T1003/006/
- Microsoft — MS-DRSR (Directory Replication): https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-drsr/
