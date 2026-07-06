---
tipo: concetto
tag: [windows, ad]
fase: 2
fonti: 6
aggiornato: 2026-07-02
stato: maturo
aliases: ["Pass-the-Hash", "PtH"]
---

# Pass-the-Hash

> **Nota etica**: tecnica offensiva. Qui per capire difesa e detection. Solo lab autorizzati.

## In breve
**Pass-the-Hash (PtH)** è movimento laterale in cui si usa l'**hash NT** di una password — non la password in chiaro — per autenticarsi su sistemi Windows via **NTLM**. Il punto chiave: in NTLM **l'hash *è* la credenziale**, non serve la password originale. Conseguenza diretta del design del protocollo, non un bug software.

## Perché funziona (NTLM in 3 passi)
NTLM è challenge-response: il client prova di conoscere l'hash NT **senza inviarlo in chiaro** e senza che il server conosca la password.
```
1. Client → Server:  NEGOTIATE (voglio autenticarmi)
2. Server → Client:  CHALLENGE (nonce casuale)
3. Client → Server:  RESPONSE = funzione(nonce, HASH-NT)
   Il server (o il DC) ricalcola con l'hash che ha in archivio → match = accesso
```
In nessun punto serve la password testuale: chi possiede **l'hash NT** può calcolare la response. Da qui il PtH.

## Da dove arriva l'hash
Windows tiene gli hash NT in memoria nel processo **`lsass.exe`** e nel database **SAM** (locale) / **NTDS.dit** (sul DC). Vettori di estrazione:
```
LSASS in memoria   → Mimikatz  sekurlsa::logonpasswords
SAM locale         → reg save HKLM\SAM ... + secretsdump
NTDS.dit (sul DC)  → DCSync (Mimikatz/secretsdump) — dump di TUTTO il dominio
```

## Esempio pratico
Estrazione (lab):
```
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords        # → NTLM hash in memoria
```
Riuso dell'hash con [[Impacket]] / [[CrackMapExec]] (formato `LM:NT`, LM vuoto):
```bash
impacket-wmiexec -hashes :8846f7eaee8fb117ad06bdd830b7586c \
    DOMINIO/Administrator@192.168.1.10

# spray dello stesso hash local-admin su tutta la subnet (manca LAPS → tutte cadono)
crackmapexec smb 192.168.1.0/24 -u Administrator -H 8846f7eaee8fb117ad06bdd830b7586c --local-auth
```
Lo scenario peggiore: **stessa password local Administrator** su tutte le workstation → un hash apre l'intera rete.

## PtH vs attacchi parenti
| Tecnica | Materiale riusato | Protocollo |
|---|---|---|
| **Pass-the-Hash** | hash NT | NTLM |
| **Pass-the-Ticket** | TGT/TGS | [[Kerberos]] |
| **Overpass-the-Hash** | hash NT → richiede TGT | NTLM→Kerberos |

## Mitigazione e difesa
- **LAPS**: password local admin uniche e a rotazione → uccide lo spray dell'hash.
- **Protected Users** + disabilitare NTLM dove possibile (`Restrict NTLM` via GPO) → forza Kerberos.
- **Credential Guard** (VBS): isola gli hash di LSASS, irraggiungibili da Mimikatz.
- **Tiered Admin Model**: un admin di dominio non deve mai loggarsi su una workstation (non lascia l'hash dove l'attaccante è già).
- **Detection**: [[Windows Event Log]] **4624 Logon Type 3** (network) con NTLM da host inattesi; correla account-admin che appaiono su molte macchine in poco tempo.

---

# Approfondimento operativo

## Meccanismo interno — l'hash NT byte per byte
- L'**NT hash** è semplicemente `MD4(UTF-16LE(password))`. Niente salt, niente iterazioni: due account con la stessa password hanno lo stesso hash. È per questo che il riuso di una password local-admin si traduce in **un solo hash che apre tutto**.
- Il formato che i tool si aspettano è `LM:NT`. Su sistemi moderni l'LM è disabilitato → si passa `aad3b435b51404eeaad3b435b51404ee` (LM vuoto) come placeholder, o semplicemente `:NThash`.
- **NetNTLMv2 ≠ NT hash**: l'handshake di rete produce una **response** `HMAC-MD5` (la "challenge-response" qui sotto). Quella la **craccki** o la **rilanci** (relay), ma **non** la passi: non è materiale PtH. Confondere i due è l'errore #1 dei principianti.

```
NTLM challenge-response (livello pacchetto)
 Client                         Server (o DC via Netlogon)
   │  Type1  NEGOTIATE ───────────►│
   │◄─────── Type2  CHALLENGE       │   nonce a 8 byte (server challenge)
   │  Type3  AUTH ─────────────────►│   NTProofStr = HMAC-MD5(NThash, nonce+blob)
   │                                │   il server ricalcola con l'hash in archivio
   └──── match ⇒ accesso  (in nessun frame viaggia la password)
```
Il PtH inietta l'**NT hash** direttamente come segreto, saltando la conoscenza della password: il client lo usa per produrre l'NTProofStr valido.

## Varianti di esecuzione e quale scegliere
| Tool | Tecnica sotto | Traccia lasciata | Quando |
|---|---|---|---|
| `psexec` | crea servizio + ADMIN$ | **7045**, binario su disco, rumoroso | shell SYSTEM affidabile |
| `smbexec` | servizio temporaneo per comando | semi-rumoroso, no binario persistente | comandi puntuali |
| `wmiexec` | DCOM/WMI (`Win32_Process`) | **4688** `wmiprvse.exe` parent, niente servizio | OPSEC migliore |
| `atexec` | scheduled task remoto | **4698** | quando WMI è filtrato |
| `nxc/cme` | SMB + moduli | dipende dal modulo | spray e raccolta di massa |

```bash
# Overpass-the-Hash: hash NT → TGT Kerberos (evita NTLM, utile se NTLM è ristretto)
impacket-getTGT corp.local/Administrator -hashes :a9fdfa038c4b75ebc76dc855dd74f0da
export KRB5CCNAME=Administrator.ccache
impacket-psexec -k -no-pass corp.local/Administrator@host.corp.local
```
> [!tip] Overpass-the-Hash = bypass anti-NTLM
> Se l'ambiente ha **Restrict NTLM** o l'account è in **Protected Users** (che vieta NTLM), il PtH puro fallisce. `getTGT` con l'hash ti dà un TGT Kerberos: passi a Pass-the-Ticket e aggiri il blocco — a meno che l'account sia in Protected Users, dove anche questo è limitato (no RC4, no delega).

## Casi limite e varianti
- **Built-in Administrator (RID 500) vs admin di dominio "creato"**: di default solo l'RID-500 locale bypassa l'**UAC remote restriction** (`LocalAccountTokenFilterPolicy`). Un altro local admin via PtH può ricevere un token *filtrato* (medium) → niente accesso a `ADMIN$`. Questo spiega il classico "le credenziali sono giuste ma psexec dà ACCESS_DENIED".
- **`LocalAccountTokenFilterPolicy = 1`**: se impostata, anche i local admin non-RID500 ottengono token pieno via rete → PtH torna a funzionare. Spesso settata da software di gestione.
- **AES-only / Credential Guard**: con Credential Guard (VBS) gli hash NT non sono più estraibili da LSASS in chiaro → PtH locale muore alla fonte (non puoi rubare l'hash). Non protegge però gli hash già esfiltrati o NTDS.dit.
- **`--local-auth` vs auth di dominio**: dimenticarlo fa autenticare l'hash contro il **dominio** invece che contro il SAM locale → fallimento. Per gli hash local-admin serve `--local-auth`.

## Detection engineering
| Evento | Indicatore PtH | MITRE |
|---|---|---|
| **4624 Logon Type 3** + `Authentication Package: NTLM` da host inattesi | uso di hash via rete | T1550.002 |
| **4624** con `Logon Process: NtLmSsp` per account admin su **molte** macchine in pochi minuti | spray dell'hash | T1550.002 |
| **4776** (NTLM credential validation sul DC) in massa | validazioni NTLM anomale | T1550.002 |
| **7045** + servizio con nome random | psexec / smbexec | T1569.002 |
| Sysmon **10** access a `lsass.exe` con `GrantedAccess 0x1010/0x1410` | dump LSASS (origine dell'hash) | T1003.001 |

Regola Sigma (admin locale che appare su molti host via NTLM):
```yaml
title: Pass-the-Hash – local admin NTLM lateral
logsource: { product: windows, service: security }
detection:
  selection:
    EventID: 4624
    LogonType: 3
    AuthenticationPackageName: 'NTLM'
    LogonProcessName: 'NtLmSsp'
  filter_machine:
    TargetUserName|endswith: '$'
  condition: selection and not filter_machine
  # correlazione: stesso TargetUserName su >5 ComputerName in 10 min
level: medium
```
> Il segnale forte non è il singolo 4624, ma la **correlazione**: stesso account admin, Logon Type 3 NTLM, su molti host in finestra stretta = pattern di spray dell'hash che un utente legittimo non produce.

## Evasion / OPSEC (con limiti)
- Preferisci **wmiexec/atexec** a psexec per non generare `7045` e non lasciare binari. Limite: WMI lascia comunque `4688` con parent `wmiprvse.exe` e logon `4624` Type 3.
- Usa **Overpass-the-Hash** per restare su Kerberos (meno monitorato del NTLM in molti SIEM). Limite: i TGT in RC4 generano `4768` etype 0x17 sospetti.
- Evita lo **spray a tappeto**: targetizza solo gli host dove BloodHound mostra l'account come admin. Limite: anche pochi 4624 NTLM cross-host correlati bastano a un buon UEBA.
- Non dumpare LSASS con Mimikatz "nudo" (firma AV nota): l'hash spesso si prende già da `nxc --sam/--lsa` o da NTDS via DCSync.

## Troubleshooting — 5 errori da principiante
1. **Passi un NetNTLMv2 come fosse un NT hash** → non è materiale PtH; quello si **cracka** (`-m 5600`) o si **rilancia** (ntlmrelayx). Verifica il formato: NT hash = 32 hex, NetNTLMv2 = lungo con `::`.
2. **`STATUS_ACCESS_DENIED` con hash corretto di un local admin** → manca `--local-auth`, oppure è la UAC remote restriction (account non-RID500 + `LocalAccountTokenFilterPolicy=0`).
3. **`STATUS_LOGON_FAILURE`** → hash sbagliato o account diverso da quello che pensi; ricontrolla che l'hash sia l'NT (la seconda metà di `LM:NT`).
4. **PtH va su una macchina ma non sul DC** → spesso il DC ha NTLM ristretto o l'account è in Protected Users. Passa a Overpass-the-Hash + Kerberos.
5. **`SMB SessionError: STATUS_NOT_SUPPORTED`** → SMB signing/dialect mismatch o NTLM disabilitato del tutto sul target. Verifica con `nxc smb host` la riga `signing` e i protocolli supportati.

## Domande da colloquio
**D: PtH è un bug o un design?**
R: Design. In NTLM la prova di identità è una funzione dell'hash NT, non della password: chi possiede l'hash può autenticarsi. Non c'è patch che lo "corregga" senza cambiare il protocollo; si mitiga (LAPS, Credential Guard, Protected Users, tiering), non si elimina con un fix.

**D: Differenza tra Pass-the-Hash, Overpass-the-Hash e Pass-the-Ticket?**
R: PtH usa l'hash NT su NTLM. Overpass-the-Hash usa l'hash NT per **richiedere un TGT Kerberos** (passa così a Kerberos, aggirando restrizioni NTLM). Pass-the-Ticket riusa direttamente un **ticket** (TGT/TGS) già esistente rubato dalla memoria. Materiale e protocollo diversi.

**D: Perché LAPS è la mitigazione singola più efficace contro il PtH di massa?**
R: Perché il PtH "esplode" quando la **stessa** password (quindi lo stesso hash NT) di local Administrator è su molte macchine: un hash le apre tutte. LAPS rende quella password **unica e a rotazione** per ogni host → l'hash rubato vale per una sola macchina, spezzando il movimento laterale di massa.

**D: Come distingui un 4624 NTLM legittimo da uno di un attacco PtH?**
R: Il singolo evento è ambiguo; conta la correlazione: stesso account privilegiato, Logon Type 3, AuthPackage NTLM, su molti host non correlati in finestra breve, spesso da un host "pivot". Aggiungi contesto con 4776 sul DC e dump-LSASS (Sysmon 10) a monte.

## Lab
- [[TryHackMe]] → room **Lateral Movement and Pivoting**: PtH, Pass-the-Ticket e Overpass-the-Hash con [[Impacket]] e [[CrackMapExec]] in un dominio di lab.
- [[HackTheBox]] → macchine AD dove si dumpano hash locali (SAM/LSASS) e si fa spray con `nxc smb <rete> -u Administrator -H <hash> --local-auth`; e **GOAD** per riprodurre il movimento laterale di massa in assenza di [[LAPS]].
- Lab locale: con due VM Windows unite al dominio e stessa password local Administrator, dumpa l'hash con [[Mimikatz]] (`sekurlsa::logonpasswords`), riusalo con `impacket-wmiexec -hashes :<NT>` e osserva nel [[Windows Event Log]] gli **Event ID 4624 Logon Type 3 / NTLM** correlati e il **4776** sul DC.

## Collegamenti
- [[Impacket]]
- [[CrackMapExec]]
- [[NetExec]]
- [[Mimikatz]]
- [[SMB]]
- [[Windows Event Log]]
- [[Active Directory]]
- [[Kerberos]]
- [[LAPS]]
- [[Privilege Escalation Windows]]
- [[NTLM Relay]]
- [[BloodHound]]

## Fonti
- MITRE ATT&CK T1550.002 — Pass the Hash: https://attack.mitre.org/techniques/T1550/002/
- HackTricks — Pass the Hash: https://book.hacktricks.xyz/windows-hardening/ntlm/pass-the-hash
- Microsoft — Mitigating Pass-the-Hash: https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/mitigating-pass-the-hash-attacks-and-other-credential-theft-techniques
- TryHackMe — Lateral Movement and Pivoting: https://tryhackme.com/room/lateralmovementandpivoting
- The Hacker Recipes — Pass the hash: https://www.thehacker.recipes/ad/movement/ntlm/pth
- MS-NLMP NTLM protocol spec: https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-nlmp/
