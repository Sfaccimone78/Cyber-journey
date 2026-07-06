---
tipo: concetto
tag: [windows]
fase: 1
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Utenti e Permessi Windows"]

---

# Utenti e Permessi Windows

## In breve
Windows gestisce l'accesso alle risorse tramite **account utente** e un sistema di permessi chiamato **ACL** (Access Control List). Ogni utente appartiene a uno o più gruppi, e ogni risorsa (file, cartella, chiave di registro) ha una lista di chi può farci cosa.

## Come funziona
### Tipi di account
- **Account locali**: esistono solo sul singolo PC (es. `Administrator`, `Guest`).
- **Account di dominio**: gestiti da [[Active Directory]] e validi su tutta la rete aziendale.
- **Account di sistema**: `SYSTEM`, `LOCAL SERVICE`, `NETWORK SERVICE` — usati da Windows internamente, con privilegi altissimi.

### Gruppi importanti
| Gruppo | Cosa può fare |
|---|---|
| `Administrators` | Controllo totale sulla macchina |
| `Users` | Operazioni base, nessun accesso admin |
| `Remote Desktop Users` | Connessione via [[RDP]] |
| `Backup Operators` | Leggere qualsiasi file per backup |

### ACL e permessi NTFS
Ogni file/cartella ha un **Security Descriptor** con:
- **DACL** (Discretionary ACL): chi ha accesso e con quali permessi (Lettura, Scrittura, Esecuzione, Controllo Completo…).
- **SACL** (System ACL): regola l'auditing — quali accessi vengono registrati nel [[Windows Event Log]].

### UAC (User Account Control)
Anche un amministratore lavora normalmente con token ridotti. Quando serve elevare i privilegi, appare la finestra UAC. Molte tecniche di [[Privilege Escalation Windows]] mirano ad aggirare l'UAC.

## Esempio pratico
Verificare i permessi di una cartella da riga di comando:

```cmd
icacls C:\Windows\System32\config
```

Output tipico:
```
NT AUTHORITY\SYSTEM:(I)(F)
BUILTIN\Administrators:(I)(F)
```
`F` = Full Control. Se un utente non privilegiato avesse `F` su `System32`, sarebbe una grossa vulnerabilità.

## Mitigazione e difesa
- Applicare il principio del **minimo privilegio**: ogni utente ha solo i permessi strettamente necessari.
- Controllare regolarmente i membri del gruppo `Administrators`.
- Monitorare escalation di privilegi tramite [[Windows Event Log]] (Event ID 4672 – privilegi speciali assegnati).
- Non disabilitare l'UAC.

## Lab
- [[TryHackMe]] — *Windows Fundamentals 1/2/3*: account locali/di dominio, gruppi built-in, UAC e permessi NTFS.
- [[HackTheBox]] Academy — modulo *Windows Fundamentals* / *Windows Privilege Escalation*: enumerare ACL con `icacls` e trovare permessi deboli su file/servizi.
- Lab locale: con `whoami /priv`, `whoami /groups` e `icacls` ispeziona i tuoi privilegi e i permessi di una cartella; poi crea un file e osserva la DACL con `Get-Acl`.
- Cosa praticare: riconoscere una DACL "debole" (utente non privilegiato con Full Control su binari/cartelle di sistema) come vettore di [[Privilege Escalation Windows]].

## Domande
1. **D:** Che differenza c'è tra DACL e SACL in un Security Descriptor?  **R:** La DACL definisce *chi* può accedere all'oggetto e con quali permessi; la SACL definisce *quali accessi vengono auditati* e finiscono nel [[Windows Event Log]].
2. **D:** Perché l'account `SYSTEM` è un obiettivo primario in una escalation?  **R:** È un account di sistema con privilegi massimi sulla macchina, superiori anche a un normale Administrator: ottenerne il token dà controllo totale del host.
3. **D:** Cosa indica `F` nell'output di `icacls` e perché è pericoloso su `System32`?  **R:** `F` = Full Control; se un utente non privilegiato lo avesse su `System32` potrebbe sostituire binari di sistema ed elevare i privilegi.
4. **D:** A cosa serve l'UAC e perché è rilevante per gli attaccanti?  **R:** L'UAC fa lavorare anche gli admin con un token ridotto, richiedendo elevazione esplicita; molte tecniche di privesc puntano a *bypassare* l'UAC per ottenere il token completo.
5. **D:** Qual è il principio cardine per limitare l'impatto di un account compromesso?  **R:** Il minimo privilegio: assegnare a ogni utente/gruppo solo i permessi strettamente necessari e rivedere periodicamente i membri di `Administrators`.

## Collegamenti
- [[Filesystem Windows]]
- [[Registro di Sistema Windows]]
- [[Active Directory]]
- [[Privilege Escalation Windows]]
- [[Windows Event Log]]
- [[RDP]]

## Fonti
- Microsoft Learn – Local accounts: https://learn.microsoft.com/en-us/windows/security/identity-protection/access-control/local-accounts
- Microsoft Learn – ACL overview: https://learn.microsoft.com/en-us/windows/win32/secauthz/access-control-lists
- HackTricks – Windows Privilege Escalation: https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation
