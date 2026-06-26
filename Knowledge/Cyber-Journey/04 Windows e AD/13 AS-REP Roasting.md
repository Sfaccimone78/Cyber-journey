---
tipo: concetto
tag: [windows, ad]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["AS-REP Roasting"]

---

# AS-REP Roasting

> Nota etica: tecnica offensiva spiegata a scopo difensivo ed educativo. Applicare solo in ambienti lab autorizzati con esplicito permesso scritto.

## In breve

AS-REP Roasting è un attacco contro [[Active Directory]] che colpisce account con la pre-autenticazione Kerberos **disabilitata**. L'attaccante può richiedere un ticket AS-REP per questi account senza conoscere la password, e craccare l'hash offline.

## Come funziona

Nella fase normale di [[Kerberos]], il client invia una prova cifrata (timestamp) per autenticarsi prima di ricevere il Ticket Granting Ticket (TGT). Questo si chiama **pre-autenticazione** ed è abilitato di default.

Se un account ha l'opzione **"Do not require Kerberos preauthentication"** attiva (flag `DONT_REQ_PREAUTH` in AD), chiunque — anche senza credenziali — può inviare una richiesta AS-REQ al Domain Controller e ottenere una risposta AS-REP contenente dati cifrati con l'hash della password dell'utente.

Passaggi:

1. **Identificare account vulnerabili**: account con pre-auth disabilitata (spesso per compatibilità con applicazioni legacy).
2. **Richiedere AS-REP**: il DC risponde senza verificare l'identità del richiedente.
3. **Estrarre e craccare**: l'hash nella risposta (Hashcat mode `18200`) viene craccato offline con dizionario.

Differenza chiave da [[Kerberoasting]]: AS-REP Roasting **non richiede nemmeno un account di dominio**.

## Esempio pratico

Con [[Impacket]] senza credenziali (se si conosce il nome utente):

```bash
impacket-GetNPUsers DOMINIO/ -usersfile utenti.txt -format hashcat -dc-ip 192.168.1.1
```

Output: hash in formato `$krb5asrep$23$...` per ogni account vulnerabile trovato. Craccare con:

```bash
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt
```

## Mitigazione e difesa

- **Abilitare sempre la pre-autenticazione Kerberos** per tutti gli account. Verificare chi ha il flag `DONT_REQ_PREAUTH` con:
  ```powershell
  Get-ADUser -Filter {DoesNotRequirePreAuth -eq $true} -Properties DoesNotRequirePreAuth
  ```
- Usare password lunghe e complesse per gli account che per motivi legacy devono tenere la pre-auth disabilitata.
- Monitorare Event ID **4768** (TGT request) nel [[Windows Event Log]] per richieste da host non noti.
- Collocare gli account vulnerabili nel gruppo **Protected Users** quando possibile.

## Collegamenti

- [[Kerberos]]
- [[Kerberoasting]]
- [[Active Directory]]
- [[Impacket]]
- [[Windows Event Log]]

## Fonti

- MITRE ATT&CK T1558.004 — AS-REP Roasting: https://attack.mitre.org/techniques/T1558/004/
- HackTricks — AS-REP Roasting: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/asreproast
- TryHackMe — Attacking Kerberos: https://tryhackme.com/room/attackingkerberos
