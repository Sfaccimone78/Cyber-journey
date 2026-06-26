---
tipo: concetto
tag: [metodologia, windows, ad]
fase: 3
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Lateral Movement"]
---

# Lateral Movement

> **Nota etica**: tecniche per pentest/lab autorizzati. L'uso non autorizzato è reato.

## In breve
Il **movimento laterale** è la fase in cui un attaccante, dopo l'accesso iniziale a un host, si sposta verso **altri sistemi** della rete per avvicinarsi all'obiettivo (dati sensibili, Domain Controller). Segue la [[Post-Exploitation]] e sfrutta credenziali raccolte e fiducia tra sistemi. È una fase centrale della [[La Cyber Kill Chain|Kill Chain]] e di [[MITRE ATT&CK]] (tattica *Lateral Movement*).

## Come funziona
Dipende da due ingredienti: **credenziali** (o hash/ticket) e un **canale di esecuzione remota**.

Tecniche tipiche in ambiente Windows/[[Active Directory]]:
- **[[Pass-the-Hash]]**: autenticarsi con l'hash NT senza conoscere la password.
- **Pass-the-Ticket / Overpass-the-Hash**: riusare ticket [[Kerberos]].
- **Esecuzione remota** via [[SMB]] (PsExec), WMI, WinRM, RDP.
- **[[Kerberoasting]]** / **[[AS-REP Roasting]]** per ottenere nuove credenziali lungo il percorso.

In ambiente Linux: riuso di chiavi [[SSH]] trovate, sudo/credenziali condivise, **pivoting** tramite tunnel SSH.

## Esempio pratico
```bash
# Pass-the-Hash + esecuzione remota con CrackMapExec
crackmapexec smb 10.10.10.0/24 -u Administrator -H <hash_NT> -x "whoami"

# Esecuzione remota con Impacket (psexec) usando l'hash
psexec.py -hashes :<hash_NT> Administrator@10.10.10.20

# Pivoting: tunnel SSH per raggiungere una rete interna non instradabile
ssh -L 3389:10.10.20.50:3389 utente@10.10.10.5
```
[[BloodHound]] serve a **pianificare** il percorso più breve verso Domain Admin.

## Mitigazione e difesa
- **Segmentazione di rete** ([[Subnetting]]/VLAN) e firewall interni.
- **[[LAPS]]** per eliminare le password admin locali condivise.
- Limitare gli amministratori locali e i logon interattivi degli account privilegiati (tiering).
- Abilitare SMB/LDAP signing; monitorare logon di tipo 3 anomali e uso di PsExec/WMI ([[SIEM]], Sysmon).

## Collegamenti
- [[Post-Exploitation]]
- [[Pass-the-Hash]]
- [[Mimikatz]]
- [[BloodHound]]
- [[SMB]]
- [[SSH]]
- [[MITRE ATT&CK]]

## Fonti
- MITRE ATT&CK — Lateral Movement (TA0008): https://attack.mitre.org/tactics/TA0008/
- HackTricks — Lateral Movement: https://book.hacktricks.xyz/windows-hardening/lateral-movement
- Microsoft — Lateral movement detection: https://learn.microsoft.com/en-us/defender-for-identity/lateral-movement-alerts
