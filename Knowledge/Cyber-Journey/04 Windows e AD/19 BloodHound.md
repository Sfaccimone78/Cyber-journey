---
tipo: entita
tag: [windows, ad, tool]
fase: 3
fonti: 5
aggiornato: 2026-06-21
stato: maturo
aliases: ["BloodHound"]
---

# BloodHound

> **Nota etica**: usare solo in ambienti autorizzati. La raccolta dati su un dominio è essa stessa attività intrusiva.

## Cos'è
**BloodHound** è uno strumento che mappa le relazioni di un dominio [[Active Directory]] come un **grafo** e individua i **percorsi d'attacco** verso obiettivi privilegiati (es. Domain Admin). Trasforma la complessità di AD — utenti, gruppi, sessioni, ACL — in domande del tipo *"qual è la via più breve da questo utente compromesso a DA?"*.

## Uso tipico
La raccolta dati avviene con un **collector** (SharpHound), poi i dati si importano nell'interfaccia BloodHound.
```powershell
# Raccolta dati dal dominio (da un host con accesso)
SharpHound.exe -c All

# Variante Python (da Linux, con credenziali)
bloodhound-python -u utente -p 'Password' -d corp.local -ns 10.10.10.1 -c All
```
Si importa il file ZIP risultante in BloodHound e si usano le **query predefinite** (es. "Shortest Paths to Domain Admins").

## Quando si usa
- Subito dopo l'accesso iniziale a un dominio, per **pianificare il [[Lateral Movement]]**.
- Per scoprire abusi di ACL, sessioni di utenti privilegiati su macchine raggiungibili, gruppi annidati.
- In ottica blue team: per **trovare e ridurre** i percorsi d'attacco prima dell'attaccante.

## Note e trucchi
- Relazioni chiave nel grafo: `MemberOf`, `HasSession`, `AdminTo`, `GenericAll`, `WriteDacl`.
- SharpHound è rumoroso: genera query LDAP e tentativi di sessione rilevabili.
- Si combina con [[Mimikatz]] (per le credenziali) e [[Kerberoasting]]/[[AS-REP Roasting]] (per ottenere i passi del percorso).

---

# Approfondimento operativo

## Meccanismo interno — come SharpHound raccoglie e come BloodHound ragiona
- **Modello a grafo**: i dati sono **nodi** (User, Computer, Group, GPO, OU, Domain, Container, AIACA/CertTemplate per ADCS) ed **edge** orientati (`MemberOf`, `AdminTo`, `HasSession`, `GenericAll`, `WriteDacl`, `AllowedToDelegate`, `CanRDP`, `Owns`…). Un percorso d'attacco = un cammino orientato dal nodo "compromesso" al nodo "obiettivo".
- **Backend grafo**: BloodHound Legacy usa **Neo4j** e query in **Cypher**. BloodHound CE (Community Edition, dal 2023) usa un proprio motore + Postgres/Postgres-graph e API REST, ma il linguaggio di query resta Cypher.
- **Dove prende i dati SharpHound**:
  - **LDAP** su 389/636 → oggetti, gruppi, ACL (security descriptor), SPN, attributi di delega. È il grosso della raccolta.
  - **SAMR/`NetSessionEnum`/`NetWkstaUserEnum`** via SMB su 445 → **sessioni** (`HasSession`): chi è loggato dove. Questa è la parte **rumorosa e fragile** (richiede di toccare ogni host).
  - **`NetLocalGroupGetMembers`** → membership local admin (`AdminTo`).
- **Collection methods** (`-c`): `Default`, `All`, `Session` (solo sessioni, ripetibile a intervalli), `ACL`, `DCOnly` (solo LDAP al DC → **niente touch sugli host**, molto più silenzioso ma niente sessioni), `LoggedOn` (usa il Remote Registry, più invasivo).

```
SharpHound ──LDAP 389──► DC        (oggetti, ACL, deleghe, SPN)
           ──SMB 445───► ogni host (sessioni, local admin)  ◄─ parte rumorosa
                  │
                  ▼  .zip (JSON)
            BloodHound (Neo4j / CE) ── Cypher ──► "Shortest path to Domain Admins"
```

## Query Cypher utili (oltre alle predefinite)
```cypher
// Tutti i percorsi dagli utenti "owned" verso Domain Admins
MATCH p=shortestPath((u:User {owned:true})-[*1..]->(g:Group))
WHERE g.name STARTS WITH 'DOMAIN ADMINS@' RETURN p

// Account kerberoastabili (hanno SPN) e a quali gruppi privilegiati portano
MATCH (u:User {hasspn:true}) RETURN u.name, u.serviceprincipalnames

// Computer con unconstrained delegation (cattura TGT del DC via PrinterBug)
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c.name

// Chi ha diritti DCSync (DS-Replication-Get-Changes / -All)
MATCH p=(n)-[:DCSync|GetChanges|GetChangesAll*1..]->(d:Domain) RETURN p
```
> [!tip] Marca gli "owned"
> Dopo aver compromesso un account, marcalo `owned` nell'interfaccia (o via Cypher). Le query "from owned" diventano la tua mappa del tesoro: BloodHound ti dice **esattamente** il prossimo edge da abusare.

## Walkthrough end-to-end (da Linux)
```bash
# 1. Raccolta col collector Python (no esecuzione su Windows = meno rumore)
bloodhound-python -u svc_user -p 'Estate2025!' -d corp.local -ns 10.10.10.10 -c All --zip
#    Variante moderna: il collector Rust 'rusthound' / 'bloodhound-ce-python'
# 2. Avvia lo stack (CE via docker) e importa lo .zip dalla UI
# 3. Marca svc_user come Owned
# 4. Esegui "Shortest Path from Owned Principals" → leggi il primo edge
#    Bivio:
#      edge GenericAll su utente  → reset password / targeted kerberoast
#      edge AddMember su gruppo    → net rpc group addmem
#      edge HasSession di un DA    → ruba l'hash su quell'host (PtH)
#      edge DCSync                 → secretsdump krbtgt → fine
```
Output atteso: un grafo con 2-4 hop. Ogni edge, cliccato, mostra in **Help → Abuse Info** il comando esatto (Impacket/PowerView) per sfruttarlo.

## Casi limite e varianti
- **BloodHound Legacy vs CE**: il formato dati JSON differisce (versioni di collector). Un .zip di SharpHound vecchio **non** importa in CE e viceversa → allinea collector e UI.
- **rusthound / nxc --bloodhound**: alternative al collector ufficiale; utili quando SharpHound è flaggato dall'EDR. `nxc ldap DC -u u -p p --bloodhound -c All`.
- **Domini grandi (>100k oggetti)**: la raccolta `All` con sessioni può durare ore ed essere visibilissima. Usa `DCOnly` per la struttura + `Session` mirate a intervalli.
- **ADCS (Certipy + BloodHound)**: i percorsi ESC1-ESC8 (abuso template certificati) si mappano con i nodi `CertTemplate`/`EnterpriseCA` — collector aggiornato richiesto.
- **Dati stale**: le sessioni sono una fotografia. Un `HasSession` di 3 ore fa potrebbe non esistere più → ricolleziona `Session` prima di pianificare il furto credenziali.

## Detection engineering
| Segnale | Cosa rivela | MITRE |
|---|---|---|
| **4661/4662** burst di accessi a oggetti directory | enumerazione LDAP massiva (SharpHound) | T1087 / T1069 |
| Picco di query LDAP a `Configuration NC` da un host non-admin | raccolta BloodHound | T1018 |
| **5145** (network share object access) su `IPC$` verso molti host | `NetSessionEnum` (raccolta sessioni) | T1049 |
| Tanti **4624 Type 3** brevi verso 445 da un singolo host in pochi minuti | scansione sessioni host-by-host | T1049 |
| Honeytoken: account "DA" mai usato che appare in query LDAP | qualcuno sta mappando i percorsi a DA | T1087 |

Regola Sigma (raccolta sessioni di massa):
```yaml
title: Possibile SharpHound – enum sessioni di massa
logsource: { product: windows, service: security }
detection:
  selection:
    EventID: 5145
    ShareName: '\\\\*\\IPC$'
    RelativeTargetName: 'srvsvc'
  timeframe: 5m
  condition: selection | count(ComputerName) by SubjectUserName > 20
level: medium
```
> Detection più solida lato grafo: **Microsoft Defender for Identity / honeypot accounts**. Un account esca con SPN o membership DA che compare nelle query LDAP segnala che qualcuno sta facendo BloodHound.

## Evasion / OPSEC (con limiti)
- Usa `-c DCOnly` per **non toccare gli host** (niente 5145/SMB host-by-host): raccogli struttura e ACL solo dal DC. Limite: perdi le sessioni (`HasSession`), che spesso sono l'edge decisivo.
- Colleziona da **Linux** (bloodhound-python/rusthound) per non droppare SharpHound.exe firmato e non triggerare l'EDR su file. Limite: il traffico LDAP/SMB resta identico e rilevabile.
- Spezza la raccolta nel tempo (`--throttle`, `--jitter`) per appiattire il picco. Limite: allunga la finestra di esposizione e i dati sessione invecchiano.
- Evita `LoggedOn` (Remote Registry) salvo necessità: è il metodo più invasivo.

## Troubleshooting — 5 errori da principiante
1. **Import fallisce / grafo vuoto in CE** → .zip prodotto da un collector di versione incompatibile (Legacy vs CE). Usa il collector abbinato alla UI.
2. **bloodhound-python "no results" o crash DNS** → manca `-ns <DC-IP>`; AD richiede che il resolver punti al DC. Anche il `-d` deve essere l'FQDN del dominio, non il NetBIOS.
3. **`HasSession` assente ovunque** → hai usato `-c DCOnly` o l'account non ha i permessi per `NetSessionEnum` su quegli host (da Win10 1709 `SrvsvcSessionInfo` è ristretto agli admin). Ricolleziona con privilegi adeguati o accetta la limitazione.
4. **Neo4j non parte / "connection refused"** (Legacy) → servizio Neo4j down o credenziali default `neo4j:neo4j` non cambiate al primo avvio. In CE è un problema diverso (docker compose).
5. **Clock skew durante la raccolta Kerberos** → se autentichi via Kerberos il solito `KRB_AP_ERR_SKEW`: sincronizza l'orologio col DC.

## Domande da colloquio
**D: Perché BloodHound è un cambio di paradigma rispetto a enumerare AD "a mano"?**
R: AD è un grafo di relazioni transitive (membership annidate, ACL, sessioni, deleghe) che a occhio è invisibile: un utente apparentemente banale può avere `GenericWrite` su un gruppo che è admin di un server dove dorme la sessione di un DA. BloodHound modella tutto come grafo e con un singolo `shortestPath` trova catene di 4-5 hop che manualmente richiederebbero ore e si perderebbero.

**D: Qual è la parte più rumorosa della raccolta e come la riduci?**
R: La raccolta delle **sessioni** e del local admin, perché richiede di contattare via SMB **ogni** host (NetSessionEnum/NetLocalGroupGetMembers) → tanti 5145/4624. Si riduce con `-c DCOnly` (solo LDAP al DC) accettando di perdere `HasSession`, o spalmando nel tempo con jitter.

**D: Da dove vengono gli edge ACL come `WriteDacl`?**
R: Dai **security descriptor** degli oggetti, letti via LDAP (`nTSecurityDescriptor`). SharpHound li parsa in DACL e li traduce in edge: `WriteDacl`, `GenericAll`, `WriteOwner`, ecc. Sono questi a rivelare gli abusi di ACL che non dipendono da membership di gruppo.

## Collegamenti
- [[Active Directory]]
- [[Lateral Movement]]
- [[Kerberoasting]]
- [[AS-REP Roasting]]
- [[Pass-the-Hash]]
- [[DCSync]]
- [[Mimikatz]]
- [[Kerberos]]
- [[NetExec]]
- [[Impacket]]
- [[PrinterBug]]

## Fonti
- BloodHound Community Edition (docs): https://bloodhound.specterops.io/
- SharpHound (repository): https://github.com/BloodHoundAD/SharpHound
- HackTricks — BloodHound: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/bloodhound
- The Hacker Recipes — BloodHound: https://www.thehacker.recipes/ad/recon/bloodhound
- BloodHound — Cypher query reference: https://bloodhound.specterops.io/analyze-data/bloodhound-gui/cypher-search
