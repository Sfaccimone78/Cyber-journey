---
tipo: entita
tag: [windows, tool]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["enum4linux"]

---

# enum4linux

> Nota etica: tool di enumerazione da usare esclusivamente su sistemi propri o con autorizzazione scritta esplicita.

## In breve

enum4linux è uno script Perl (e la variante moderna `enum4linux-ng` in Python) per enumerare informazioni da sistemi Windows e Samba via protocolli [[SMB]] e RPC. Estrae automaticamente utenti, gruppi, share, policy password e informazioni di dominio da un host target. È uno dei tool di enumerazione più usati durante la fase di ricognizione in ambienti Windows/AD.

## Uso tipico

```bash
# Enumerazione completa (tutte le opzioni)
enum4linux -a 192.168.1.10

# Solo utenti
enum4linux -U 192.168.1.10

# Solo share
enum4linux -S 192.168.1.10

# Con credenziali
enum4linux -u 'utente' -p 'password' -a 192.168.1.10

# Versione moderna (enum4linux-ng, output JSON)
enum4linux-ng -A 192.168.1.10 -oJ risultati.json
```

Output tipico include:
- Lista degli **utenti locali** e di dominio (SID → username)
- **Share** disponibili e relative policy di accesso
- **Policy password** (lunghezza minima, lockout, scadenza)
- Nome del **workgroup/dominio**
- Informazioni OS (versione Windows, hostname)

## Quando si usa

Nella fase di **[[Enumerazione]]** (dopo la scoperta host), su sistemi Windows con porta 445 o 139 aperta. Particolarmente efficace quando il null session è abilitato (sistemi non aggiornati o mal configurati) o quando si hanno credenziali valide da testare.

Si usa prima di tool più invasivi come [[CrackMapExec]] o [[Impacket]] per fare un primo inventario della superficie.

## Note e trucchi

- **Null session**: enum4linux funziona meglio su sistemi che accettano connessioni SMB anonime (Windows XP/2003, Samba mal configurato). Su sistemi moderni servono credenziali.
- La versione `enum4linux-ng` (Python 3) è più affidabile, mantiene output strutturato e continua lo sviluppo attivo.
- Installazione: `sudo apt install enum4linux` (Kali) oppure `pip3 install enum4linux-ng`.
- L'output del SID-to-username (opzione `-r`) consente di ricostruire la lista utenti anche quando la lista diretta è bloccata.
- Combinare con [[SMB]] manuale (`smbclient`, `rpcclient`) per approfondire i risultati.

## Lab
- [[TryHackMe]] → room **Network Services** (sezione SMB): usa `enum4linux -a` per enumerare share, utenti e policy password contro un target Samba mal configurato con null session attiva.
- [[HackTheBox]] → macchine Windows/AD entry-level dove `enum4linux-ng -A` fornisce la lista utenti iniziale (utile poi per password spray o [[AS-REP Roasting]]).
- Lab locale (Samba/VM Windows): configura una share con accesso anonimo, lancia `enum4linux-ng -A <ip> -oJ out.json` e confronta l'output con `smbclient -L` e `rpcclient -U "" -N -c enumdomusers` per capire quali dati provengono da quali chiamate RPC.

## Domande
1. **D:** Quali protocolli usa enum4linux per raccogliere informazioni?  **R:** [[SMB]] e RPC.
2. **D:** Cos'è una "null session" e perché favorisce enum4linux?  **R:** Una connessione SMB anonima senza credenziali; se abilitata, permette di enumerare utenti/share senza autenticazione.
3. **D:** Qual è la variante moderna dello script e in che linguaggio è scritta?  **R:** `enum4linux-ng`, scritta in Python 3 (con output strutturato JSON).
4. **D:** Quale opzione consente di ricostruire gli username partendo dai SID?  **R:** L'opzione `-r` (RID cycling / SID-to-username).
5. **D:** In quale fase del pentest si colloca tipicamente enum4linux?  **R:** Nella fase di enumerazione/ricognizione, prima di tool più invasivi come [[CrackMapExec]] o [[Impacket]].

## Collegamenti

- [[SMB]]
- [[Enumerazione]]
- [[Active Directory]]
- [[CrackMapExec]]
- [[Impacket]]
- [[Porte e Protocolli Comuni]]

## Fonti

- GitHub — enum4linux: https://github.com/CiscoCXSecurity/enum4linux
- GitHub — enum4linux-ng: https://github.com/cddmp/enum4linux-ng
- HackTricks — SMB Enumeration: https://book.hacktricks.xyz/network-services-pentesting/pentesting-smb
