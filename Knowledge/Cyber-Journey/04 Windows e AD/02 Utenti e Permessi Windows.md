---
tipo: concetto
tag: [windows]
fase: 1
fonti: 3
aggiornato: 2026-06-20
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
