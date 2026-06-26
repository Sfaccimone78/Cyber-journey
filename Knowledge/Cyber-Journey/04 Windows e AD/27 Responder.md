---
tipo: entita
tag: [tool, windows, ad]
fase: 3
fonti: 2
aggiornato: 2026-06-21
stato: maturo
aliases: ["Responder"]
---

# Responder

> **Nota etica**: solo lab autorizzati o engagement con permesso scritto. L'avvelenamento LLMNR/NBT-NS tocca l'intera rete locale.

## In breve
**Responder** avvelena i protocolli di risoluzione nomi di **fallback** di Windows — **LLMNR**, **NBT-NS** e **mDNS** — per farsi inviare le autenticazioni [[NTLM]] dei client. Quando un host cerca un nome che il [[DNS]] non risolve (typo, share inesistente), ripiega su LLMNR/NBT-NS in *broadcast*: Responder risponde "sono io", il client si autentica verso l'attaccante e consegna un **NetNTLM hash** craccabile offline o utilizzabile in [[NTLM Relay]].

## Come funziona (meccanismo)
1. Un client risolve un nome → fallisce su DNS → manda una query **LLMNR/NBT-NS in broadcast** alla LAN.
2. Responder, in ascolto, **risponde a tutte** le query con il proprio IP.
3. Il client si connette (SMB/HTTP/...) e tenta auth NTLM → Responder cattura la **challenge-response (NetNTLMv2)**.
4. Output: hash da craccare con [[Hashcat]]/[[John the Ripper]] (`-m 5600`) **oppure** da rilanciare con [[NTLM Relay]].

## Uso
```bash
# Avvelena e cattura (interfaccia tun0/eth0)
responder -I eth0 -wv

# Hash salvati qui:
ls /usr/share/responder/logs/   # *.txt con NetNTLMv2

# Crack
hashcat -m 5600 hash.txt rockyou.txt
```

> [!warning] Disattiva SMB/HTTP se fai relay
> Per la catena Responder → [[NTLM Relay]] devi **spegnere** i server SMB/HTTP di Responder (`Responder.conf`: `SMB = Off`, `HTTP = Off`) così le auth non vengono "rubate" da Responder ma passate a `ntlmrelayx`.

## Detection e difesa
- **Disabilitare LLMNR** (GPO: *Turn off multicast name resolution*) e **NBT-NS** (DHCP option / registro) → toglie la fonte.
- **SMB signing** obbligatorio → spezza il relay a valle.
- Detection: host che risponde a **molte** query LLMNR/NBT-NS; trappola **honeytoken** (richiesta a un nome inesistente: se qualcuno risponde, c'è un poisoner).
- MITRE: **T1557.001** (LLMNR/NBT-NS Poisoning and SMB Relay).

## Collegamenti
- [[NTLM]] · [[NTLM Relay]] — uso degli hash catturati
- [[DNS]] — il fallback che Responder sfrutta · [[SMB]]
- [[Hashcat]] · [[John the Ripper]] — crack NetNTLMv2
- [[Active Directory]] · [[PrinterBug e Coercizione]]

## Fonti
- lgandx/Responder: https://github.com/lgandx/Responder
- The Hacker Recipes — LLMNR/NBT-NS poisoning: https://www.thehacker.recipes/ad/movement/mitm-and-coerced-authentications/llmnr-nbtns-mdns-spoofing
- MITRE ATT&CK — T1557.001: https://attack.mitre.org/techniques/T1557/001/
