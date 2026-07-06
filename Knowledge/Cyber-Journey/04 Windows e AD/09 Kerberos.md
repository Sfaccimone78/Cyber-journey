---
tipo: concetto
tag: [windows, ad]
fase: 2
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["Kerberos"]
---

# Kerberos

## In breve
**Kerberos** è il protocollo di autenticazione principale di [[Active Directory]]. Niente password sulla rete: l'utente prova l'identità una volta e riceve **ticket** temporanei cifrati. Il **KDC** (sul Domain Controller) emette e valida i ticket. Capire il flusso è il prerequisito per [[Kerberoasting]], [[AS-REP Roasting]], Pass-the-Ticket e Golden/Silver Ticket.

## Attori
- **Client** — l'utente/macchina che vuole una risorsa.
- **KDC** — sul DC, ha due ruoli: **AS** (Authentication Service) e **TGS** (Ticket Granting Service). Conosce l'hash di **ogni** account, incluso `krbtgt`.
- **Service** — la risorsa (file server, SQL, web) identificata da un **SPN**.

## Flusso completo (AS-REQ → AP-REQ)
```
1. AS-REQ   Client → AS:  timestamp cifrato con l'hash dell'UTENTE (pre-auth)
2. AS-REP   AS → Client:  TGT (cifrato con l'hash di krbtgt) + session key
3. TGS-REQ  Client → TGS: presenta il TGT, chiede un ticket per SPN "CIFS/fs01"
4. TGS-REP  TGS → Client: Service Ticket (cifrato con l'hash dell'account del SERVIZIO)
5. AP-REQ   Client → Service: presenta il Service Ticket
6. Accesso  il servizio decifra col proprio hash → fida il PAC dentro il ticket
```
- **TGT** = lasciapassare generale (default ~10h), cifrato con l'hash di **`krbtgt`**. Chi conosce l'hash di `krbtgt` può forgiare TGT arbitrari = **Golden Ticket**.
- **Service Ticket (TGS)** = per un singolo SPN, cifrato con l'hash dell'**account di servizio**. Forgiarlo conoscendo quell'hash = **Silver Ticket**.
- Il **PAC** (Privilege Attribute Certificate) dentro il ticket porta i gruppi/SID dell'utente: è ciò che il servizio usa per autorizzare.

## Perché nascono gli attacchi (il punto chiave)
| Dettaglio del protocollo | Attacco che abilita |
|---|---|
| Il TGS è cifrato con l'hash dell'account di servizio | [[Kerberoasting]] — richiedi il TGS e craccalo **offline** |
| Pre-auth disattivabile per utente | [[AS-REP Roasting]] — ottieni materiale craccabile senza credenziali |
| TGT cifrato con hash `krbtgt` | **Golden Ticket** — persistenza totale nel dominio |
| TGS cifrato con hash del servizio | **Silver Ticket** — accesso a un servizio senza toccare il DC |
| Ticket riusabili | **Pass-the-Ticket** — inietti un TGT/TGS rubato in memoria |

## Esempio pratico
Enumerare gli SPN (target del Kerberoasting):
```powershell
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName |
  Select Name, ServicePrincipalName
```
Da Linux con [[Impacket]] (richiede credenziali di dominio valide):
```bash
# Kerberoasting: chiede i TGS di tutti gli account con SPN
impacket-GetUserSPNs -request -dc-ip 10.10.10.1 DOMINIO/utente:password

# AS-REP Roasting: utenti senza pre-auth
impacket-GetNPUsers -dc-ip 10.10.10.1 DOMINIO/ -usersfile utenti.txt
```
I tipi di cifratura contano: gli attaccanti spesso forzano **RC4 (etype 23)** perché l'hash craccabile è l'NT hash, più debole di AES.

## Mitigazione e difesa
- Account di servizio con password **lunghe e casuali** (≥25 char) o **gMSA** (rotazione automatica, 240 char) → Kerberoasting impraticabile.
- **Pre-autenticazione obbligatoria** su tutti gli account (blocca AS-REP Roasting).
- Proteggere e **ruotare `krbtgt`** (due volte) → invalida i Golden Ticket.
- Disabilitare RC4, forzare **AES**.
- Monitorare **Event ID 4768** (TGT) e **4769** (TGS): molti 4769 con etype 0x17 (RC4) da un solo utente = Kerberoasting.

## Lab
- [[TryHackMe]] → room **Attacking Kerberos**: percorso completo su un DC di lab — enumerazione con Rubeus/Kerbrute, [[AS-REP Roasting]], [[Kerberoasting]], Pass-the-Ticket e forgiatura di Golden/Silver Ticket.
- **GOAD (Game of Active Directory)**: pratica il flusso Kerberos end-to-end (richiesta TGT, TGS, delegation) in una foresta vulnerabile self-hosted.
- Lab locale: cattura il traffico AS-REQ/AS-REP con Wireshark filtrando `kerberos`, poi forza RC4 con `impacket-GetUserSPNs -request` e osserva nel [[Windows Event Log]] del DC il picco di **Event ID 4769 con Ticket Encryption Type 0x17**.

## Domande
1. **D:** Con quale hash è cifrato il TGT e cosa consente di forgiare chi lo conosce?  **R:** Con l'hash dell'account `krbtgt`; consente di forgiare un Golden Ticket (TGT arbitrari).
2. **D:** Con quale hash è cifrato un Service Ticket (TGS) e quale attacco offline abilita?  **R:** Con l'hash dell'account di servizio; abilita il [[Kerberoasting]] (cracking offline del TGS).
3. **D:** Cosa contiene il PAC e a cosa serve?  **R:** I gruppi/SID dell'utente; il servizio lo usa per autorizzare l'accesso.
4. **D:** Quale condizione di un account abilita l'AS-REP Roasting?  **R:** La pre-autenticazione Kerberos disabilitata.
5. **D:** Perché gli attaccanti forzano l'encryption type RC4 (etype 23)?  **R:** Perché il materiale craccabile è direttamente l'NT hash, più veloce da brute-forzare rispetto ad AES.

## Collegamenti
- [[Active Directory]]
- [[Kerberoasting]]
- [[AS-REP Roasting]]
- [[NTLM]] — protocollo di fallback più debole
- [[Pass-the-Hash]]
- [[Impacket]]
- [[Windows Event Log]]
- [[Mimikatz]] — Pass-the-Ticket, Golden/Silver Ticket

## Fonti
- Microsoft Learn — Kerberos authentication: https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-authentication-overview
- HackTricks — Kerberos: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/kerberos-authentication
- TryHackMe — Attacking Kerberos: https://tryhackme.com/room/attackingkerberos
- MITRE ATT&CK — Steal or Forge Kerberos Tickets (T1558): https://attack.mitre.org/techniques/T1558/
