---
tipo: entita
tag: [metodologia, tool]
fase: 2
fonti: 0
aggiornato: 2026-06-26
stato: stub
aliases: ["HackTricks"]
---

# HackTricks

> [!info] Stub
> Cheat-sheet di riferimento per pentest. Da espandere.

**HackTricks** = wiki/cheat-sheet online enorme su tecniche di **pentesting, privilege escalation
ed enumerazione**, organizzata per scenario (Linux, Windows/AD, web, cloud, network). Sito:
https://book.hacktricks.xyz. È la risorsa "guarda qui quando sei bloccato" più citata nelle note.

## Come si usa

- **Privilege escalation**: checklist [[Privilege Escalation Linux|Linux]] e
  [[Privilege Escalation Windows|Windows]] passo-passo (SUID, sudo, capabilities, token, servizi).
- **Enumerazione servizi**: pagina per porta/protocollo (vedi [[Porte e Protocolli Comuni]],
  [[SMB]], [[Kerberos]]) con comandi pronti.
- **Active Directory**: catena completa ([[Kerberoasting]], [[AS-REP Roasting]], [[DCSync]], [[BloodHound]]).
- **Web**: payload e bypass per [[OWASP Top 10|le vuln OWASP]].

> [!warning] Etica
> Comandi e payload vanno usati **solo** in lab/CTF o ingaggi autorizzati. Vedi [[Penetration Testing]].

## Collegamenti

- [[Privilege Escalation Linux]] · [[Privilege Escalation Windows]] · [[PEAS]] · [[GTFOBins]]
- [[Metodologia del Pentest]] · [[Enumerazione]] · [[ExploitDB]]
