---
tipo: concetto
tag: [windows, ad]
fase: 2
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["Kerberoasting"]

---

# Kerberoasting

> Nota etica: tecnica offensiva spiegata a scopo difensivo ed educativo. Applicare solo in ambienti lab autorizzati con esplicito permesso scritto.

## In breve

Kerberoasting è un attacco contro [[Active Directory]] che sfrutta il protocollo [[Kerberos]] per ottenere ticket cifrati con la password di account di servizio, poi craccabili offline. Non richiede privilegi elevati: basta un account di dominio valido.

## Come funziona

In Kerberos, ogni servizio è identificato da un **SPN** (Service Principal Name). Un utente autenticato può richiedere al Domain Controller un **Ticket Granting Service (TGS)** per qualsiasi SPN — il ticket è cifrato con l'hash NTLM dell'account che esegue quel servizio.

Passaggi dell'attacco:

1. **Enumerazione SPN**: l'attaccante trova account con SPN configurato (spesso account di servizio con password vecchie).
2. **Richiesta TGS**: richiede il ticket al DC usando le proprie credenziali di dominio.
3. **Estrazione ticket**: salva il ticket cifrato in formato craccabile (Hashcat mode `13100`).
4. **Cracking offline**: usa un dizionario per tentare di decifrare l'hash e recuperare la password in chiaro.

Il cracking avviene completamente offline: il Domain Controller non vede tentativi falliti.

## Esempio pratico

Con [[Impacket]]:

```bash
impacket-GetUserSPNs -request -dc-ip 192.168.1.1 DOMINIO/utente:password
```

Output: stampa i TGS hash in formato `$krb5tgs$23$...`. Si salva su file e si cracca:

```bash
hashcat -m 13100 tickets.txt /usr/share/wordlists/rockyou.txt
```

## Mitigazione e difesa

- Usare **password lunghe e casuali** (≥25 caratteri) per gli account di servizio: rendono il cracking impraticabile.
- Adottare **Managed Service Accounts (gMSA)**: Active Directory ruota automaticamente la password (240 caratteri casuali).
- Applicare il principio del minimo privilegio agli account di servizio: non devono essere Domain Admins.
- Monitorare Event ID **4769** (TGS request) nel [[Windows Event Log]]: molte richieste TGS in breve tempo da un solo utente sono sospette.
- Rilevare con strumenti come Microsoft Defender for Identity (MDI).

## Lab
- [[TryHackMe]] → room **Attacking Kerberos**: sezione Kerberoasting — enumerazione SPN con Rubeus/GetUserSPNs, richiesta dei TGS e cracking con Hashcat mode 13100.
- **GOAD (Game of Active Directory)**: gli account di servizio con SPN e password deboli sono presenti per design; pratica `impacket-GetUserSPNs -request` e il Targeted Kerberoasting quando hai `GenericWrite` su un utente.
- Lab locale: crea un account di servizio, assegnagli uno SPN con `setspn -A http/srv corp\svc`, dagli una password da dizionario, poi esegui il roast e osserva nel [[Windows Event Log]] del DC il picco di **Event ID 4769 con Ticket Encryption Type 0x17 (RC4)** — la firma del Kerberoasting.

## Domande
1. **D:** Con quale hash è cifrato il TGS che si cracca nel Kerberoasting?  **R:** Con l'hash NTLM dell'account che esegue il servizio (l'account associato allo SPN).
2. **D:** Quali privilegi servono per lanciare l'attacco?  **R:** Nessun privilegio elevato: basta un account di dominio valido.
3. **D:** Quale mode di Hashcat si usa per i TGS Kerberoast?  **R:** Il mode 13100 (formato `$krb5tgs$23$...`).
4. **D:** Perché il cracking non genera allarmi sul DC?  **R:** Avviene interamente offline; il DC non vede tentativi di password falliti.
5. **D:** Qual è la mitigazione più efficace e perché?  **R:** Password lunghe/casuali (≥25 char) o gMSA (240 caratteri a rotazione), che rendono il cracking offline impraticabile.

## Collegamenti

- [[Kerberos]]
- [[Active Directory]]
- [[Impacket]]
- [[AS-REP Roasting]]
- [[Windows Event Log]]
- [[CrackMapExec]]

## Fonti

- MITRE ATT&CK T1558.003 — Kerberoasting: https://attack.mitre.org/techniques/T1558/003/
- HackTricks — Kerberoasting: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/kerberoast
- Microsoft Learn — Kerberos Authentication: https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-authentication-overview
- TryHackMe — Attacking Kerberos: https://tryhackme.com/room/attackingkerberos
