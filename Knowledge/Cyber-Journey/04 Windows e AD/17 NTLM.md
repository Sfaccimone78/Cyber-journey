---
tipo: concetto
tag: [windows, ad]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["NTLM"]
---

# NTLM

> **Nota etica**: tecniche offensive a scopo difensivo/lab autorizzato.

## In breve
**NTLM** (NT LAN Manager) è il vecchio protocollo di autenticazione Windows, ancora presente come **fallback** quando [[Kerberos]] non è utilizzabile (accesso per IP, workgroup, sistemi legacy). Si basa su un meccanismo **challenge-response** che usa l'hash NT della password, mai la password in chiaro — il che lo rende il bersaglio di [[Pass-the-Hash]] e NTLM Relay.

## Come funziona
1. **Negotiate**: il client annuncia di voler usare NTLM.
2. **Challenge**: il server invia un numero casuale (challenge).
3. **Response**: il client cifra la challenge con l'**hash NT** della password e la rimanda.

Il server (o il DC) verifica la response. L'hash NT non è "salato": se un attaccante lo ottiene (es. da [[Mimikatz]]), può autenticarsi senza conoscere la password → [[Pass-the-Hash]].

## Esempio pratico
**NTLM Relay**: l'attaccante non craccala l'hash, lo **inoltra** a un altro servizio.
```bash
# Cattura hash NetNTLM con Responder (avvelena LLMNR/NBT-NS)
responder -I eth0

# Inoltra l'autenticazione catturata a un host con SMB signing disabilitato
ntlmrelayx.py -t smb://10.10.10.20 -smb2support
```
Gli hash NetNTLMv2 catturati si possono anche craccare con [[Hashcat]] (`-m 5600`).

## Mitigazione e difesa
- **Disabilitare NTLM** dove possibile, forzare [[Kerberos]].
- Abilitare **SMB Signing** e **LDAP Signing/Channel Binding** (bloccano il relay).
- Disabilitare **LLMNR/NBT-NS** (tolgono a Responder il vettore di cattura).
- Monitorare Event ID 4624/4776 con tipo di logon NTLM anomalo.

## Collegamenti
- [[Kerberos]]
- [[Pass-the-Hash]]
- [[Mimikatz]]
- [[SMB]]
- [[Lateral Movement]]
- [[Hashcat]]

## Fonti
- Microsoft Learn — NTLM overview: https://learn.microsoft.com/en-us/windows-server/security/kerberos/ntlm-overview
- HackTricks — NTLM: https://book.hacktricks.xyz/windows-hardening/ntlm
- MITRE ATT&CK T1187 — Forced Authentication: https://attack.mitre.org/techniques/T1187/
