---
tipo: concetto
tag: [windows, active-directory]
fase: 3
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["Shadow Credentials"]
---

# Shadow Credentials

> **Nota etica**: tecniche da usare solo in lab autorizzati (TryHackMe, HTB, GOAD) o engagement con permesso scritto.

## In breve
**Shadow Credentials** è una tecnica di takeover/persistenza che sfrutta l'attributo **`msDS-KeyCredentialLink`** degli oggetti utente e computer in [[Active Directory]]. Questo attributo contiene chiavi pubbliche usate da **Windows Hello for Business / NGC (Next Generation Credentials)** per l'autenticazione **PKINIT** ([[Kerberos]]). Se ho il diritto di **scrivere** quell'attributo su un account, ci aggiungo una **chiave che controllo io**: da quel momento posso autenticarmi come quell'account via PKINIT e ottenerne il **TGT** e l'**NT hash** — **senza conoscere la password e senza resettarla** (quindi senza farmi notare). È il modo "pulito" per convertire un edge ACL (`GenericWrite`/`WriteProperty` su `msDS-KeyCredentialLink`) in compromissione completa dell'account.

## Come funziona
`msDS-KeyCredentialLink` è un attributo **multivalore** che memorizza oggetti **KeyCredential** in formato **DSA / "Key Credential blob"** (struttura `msDS-KeyCredentialLink` basata su `KeyCredential` BLOB con DeviceID, public key, timestamp). Nasce per associare a un account le chiavi di un dispositivo registrato con **Windows Hello for Business**: durante il logon il client prova il possesso della **chiave privata**, e il KDC, trovando la **chiave pubblica** corrispondente in `msDS-KeyCredentialLink`, emette un **TGT** via **PKINIT** (lo stesso meccanismo dei certificati, ma con chiave grezza invece che X.509 firmato da una CA).

L'abuso:
1. Genero una **coppia di chiavi** (o un certificato self-signed) e costruisco un KeyCredential BLOB.
2. Lo **scrivo** in `msDS-KeyCredentialLink` della vittima (serve `GenericWrite`/`GenericAll`/`WriteProperty` su quell'attributo — comune su computer via [[BloodHound]] edge `AddKeyCredentialLink`).
3. Mi autentico via **PKINIT** con la chiave privata → ottengo il **TGT** dell'account.
4. Con **UnPAC-the-hash** estraggo anche l'**NT hash** (utile per [[Pass-the-Hash]] / persistenza offline).

```
WriteProperty su VICTIM.msDS-KeyCredentialLink
   --> aggiungo la MIA public key
   --PKINIT--> TGT come VICTIM  --UnPAC--> NT hash
```
Vincolo: richiede un **DC con certificato/PKINIT funzionante** (KDC abilitato a PKINIT), tipicamente presente dove c'è AD CS o un cert del DC valido.

## Esempi
**pyWhisker** (Linux) — aggiungere/listare/rimuovere la shadow credential:
```bash
# Aggiungo una key credential sull'account bersaglio
pywhisker -d dominio.local -u user -p 'Password!' --target 'SRV01$' \
  --action add --dc-ip 10.10.10.1
# pyWhisker stampa il path al .pfx + la password generata
```
Uso del .pfx per TGT + hash con **Certipy / gettgtpkinit + getnthash**:
```bash
# Da .pfx a TGT e NT hash (UnPAC)
certipy auth -pfx SRV01.pfx -dc-ip 10.10.10.1
# in alternativa con PKINITtools:
gettgtpkinit.py -cert-pfx SRV01.pfx dominio.local/'SRV01$' srv01.ccache
getnthash.py -key <AS-REP-key> dominio.local/'SRV01$'
```
Da Windows con **Whisker** + **Rubeus**:
```
Whisker.exe add /target:SRV01$
Rubeus.exe asktgt /user:SRV01$ /certificate:<base64-pfx> /password:<pfx-pass> /ptt
```
Via **bloodyAD** (scrive direttamente l'attributo):
```bash
bloodyAD --host 10.10.10.1 -d dominio.local -u user -p pass \
  add shadowCredentials 'SRV01$'
```
Pulizia (rimuovere la chiave dopo l'uso):
```bash
pywhisker -d dominio.local -u user -p 'Password!' --target 'SRV01$' --action clear
```

## Mitigazione e difesa
- **Audit delle ACL**: rimuovere `GenericWrite`/`WriteProperty` su account/computer da principal non amministrativi (chiude l'edge `AddKeyCredentialLink`).
- Monitorare le **modifiche a `msDS-KeyCredentialLink`** (Event **5136**): aggiunte inattese, specie su account privilegiati o su molti computer, sono un forte indicatore.
- Se **Windows Hello for Business non è in uso**, l'attributo non dovrebbe popolarsi: qualsiasi valore è sospetto.
- Mettere gli account sensibili in **Protected Users** e applicare il tiering; limitare PKINIT dove non necessario.
- Disabilitare/segregare **AD CS** se non serve (riduce la disponibilità di PKINIT abusabile, vedi [[ADCS e Template Vulnerabili (ESC1-ESC8)]]).

## Lab
- [[HackTheBox]] — box **Certified** (shadow credentials + ADCS ESC9).
- [[TryHackMe]] — room di AD persistence che coprono `msDS-KeyCredentialLink`.
- **GOAD - Game of Active Directory**: percorsi con `AddKeyCredentialLink` configurati.

## Domande
1. **Cosa scrivo esattamente per fare una shadow credential?** Una **chiave pubblica** (KeyCredential BLOB) nell'attributo `msDS-KeyCredentialLink` dell'account bersaglio.
2. **Perché è più discreta di un reset password?** Perché **non cambia la password**: l'utente legittimo continua a loggarsi normalmente e tu hai un canale parallelo via PKINIT.
3. **Quale diritto ACL serve?** `GenericWrite`/`GenericAll`/`WriteProperty` sull'attributo (edge **AddKeyCredentialLink** in BloodHound).
4. **Qual è il prerequisito infrastrutturale?** Un **KDC con PKINIT funzionante** (cert del DC / AD CS).
5. **Come ottengo l'NT hash dopo il TGT?** Con **UnPAC-the-hash** (`certipy auth` o `getnthash.py`).

## Approfondimento livello esperto
**Relazione con ADCS/ESC9-ESC10**: shadow credentials e certificate abuse condividono la primitiva **PKINIT**; ESC9/ESC10 manipolano il mapping cert↔account (`msDS-KeyCredentialLink` vs `altSecurityIdentities` / `CT_FLAG_NO_SECURITY_EXTENSION`). La shadow credential è spesso il passo che converte `GenericWrite` su computer in **RBCD-equivalente** ma senza toccare la delegation (vedi [[Delegation Kerberos (Unconstrained, Constrained, RBCD)]]).

**Persistenza basata su credenziali/certificati**: la chiave aggiunta sopravvive finché non viene rimossa dall'attributo; se aggiunta su un account di servizio o su `krbtgt`-adiacenti diventa **backdoor persistente** indipendente dalla password (ATT&CK **T1556** Modify Authentication Process / correlata a **T1649** per il furto/forgiatura di certificati di autenticazione).

**Detection (Event ID)**:
- **5136** — modifica directory su `msDS-KeyCredentialLink`: l'evento mostra il valore aggiunto; allertare su ogni add fuori dai flussi WHfB legittimi.
- **4768** con **Certificate/PKINIT information** popolato per un account che non usa smart card = login via key credential.
- **4769 / 4624** anomali subito dopo.
- Correlare 5136 (chi ha scritto) con il successivo 4768 (chi ha loggato) sullo stesso account.

## Collegamenti
- [[Kerberos]] — PKINIT è il meccanismo abusato
- [[Active Directory]] — `msDS-KeyCredentialLink` e ACL
- [[ADCS e Template Vulnerabili (ESC1-ESC8)]] — stessa primitiva PKINIT, certificati
- [[Pass-the-Hash]] — uso dell'NT hash estratto via UnPAC
- [[DCSync]] — esito dopo takeover di account privilegiato
- [[BloodHound]] — edge `AddKeyCredentialLink`
- [[Impacket]] · [[bloodyAD]] · [[Mimikatz]]
- [[Delegation Kerberos (Unconstrained, Constrained, RBCD)]] · [[Trust di Dominio e Foresta]]

## Fonti
- Elad Shamir — *Shadow Credentials* (ricerca originale): https://posts.specterops.io/shadow-credentials-abusing-key-trust-account-mapping-for-takeover-8ee1a53566ab
- pyWhisker (GitHub): https://github.com/ShutdownRepo/pywhisker
- The Hacker Recipes — Shadow Credentials: https://www.thehacker.recipes/ad/movement/kerberos/shadow-credentials
- HackTricks — Shadow Credentials: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/shadow-credentials
