---
tipo: entita
tag: [tool, windows, ad]
fase: 3
fonti: 3
aggiornato: 2026-07-02
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

## Lab
- [[TryHackMe]] — room *Responder* / *Attacktive Directory*: avvelenamento LLMNR/NBT-NS e cattura di NetNTLMv2 in un dominio realistico.
- [[TryHackMe]] — *Post-Exploitation Basics* e i moduli MITM: pratica la catena Responder → crack con [[Hashcat]] (`-m 5600`).
- [[HackTheBox]] — macchine AD dove il foothold parte da un poisoning LLMNR (es. traccia *Dante*/AD, box *Active*-like). Pratica: catturare un hash da una share inesistente digitata da un client.
- Lab locale **GOAD** (Game of Active Directory): esegui `responder -I eth0 -wv`, genera traffico da un client Windows, poi cracca l'hash raccolto in `/usr/share/responder/logs/`.
- Cosa praticare: distinguere quando *craccare* l'hash e quando *rilanciarlo* con [[NTLM Relay]] (spegnendo SMB/HTTP in `Responder.conf`).

## Domande
1. **D:** Quali protocolli avvelena Responder e perché sono sfruttabili?  **R:** LLMNR, NBT-NS e mDNS, i meccanismi di *fallback* usati da Windows quando il DNS non risolve un nome: sono query in broadcast senza autenticazione, così Responder può rispondere "sono io" e ricevere l'auth NTLM del client.
2. **D:** Che tipo di hash cattura tipicamente Responder e come si cracca?  **R:** Una challenge-response **NetNTLMv2**, craccabile offline con [[Hashcat]] `-m 5600` (o [[John the Ripper]]); non è un hash NT riutilizzabile in [[Pass-the-Hash]].
3. **D:** Perché per la catena Responder → NTLM Relay bisogna disattivare i server SMB/HTTP di Responder?  **R:** Perché altrimenti Responder "cattura" da sé le autenticazioni; spegnendoli (`SMB = Off`, `HTTP = Off`) le auth vengono lasciate passare a `ntlmrelayx` per il relay verso un target.
4. **D:** Qual è la mitigazione più efficace alla radice?  **R:** Disabilitare LLMNR (GPO *Turn off multicast name resolution*) e NBT-NS: elimina la fonte del fallback; in aggiunta, SMB signing obbligatorio spezza il relay a valle.
5. **D:** Quale tecnica MITRE ATT&CK descrive questo attacco?  **R:** T1557.001 — LLMNR/NBT-NS Poisoning and SMB Relay.

## Collegamenti
- [[NTLM]] · [[NTLM Relay]] — uso degli hash catturati
- [[DNS]] — il fallback che Responder sfrutta · [[SMB]]
- [[Hashcat]] · [[John the Ripper]] — crack NetNTLMv2
- [[Active Directory]] · [[PrinterBug e Coercizione]]

## Fonti
- lgandx/Responder: https://github.com/lgandx/Responder
- The Hacker Recipes — LLMNR/NBT-NS poisoning: https://www.thehacker.recipes/ad/movement/mitm-and-coerced-authentications/llmnr-nbtns-mdns-spoofing
- MITRE ATT&CK — T1557.001: https://attack.mitre.org/techniques/T1557/001/
