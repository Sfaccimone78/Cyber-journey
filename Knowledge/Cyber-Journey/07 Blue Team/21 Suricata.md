---
tipo: entita
tag: [blue-team, tool]
fase: 3
fonti: 0
aggiornato: 2026-06-26
stato: stub
aliases: ["Suricata"]
---

# Suricata

> [!info] Stub
> IDS/IPS a firme. Da espandere.

**Suricata** = motore open-source **IDS/IPS** (e NSM) ad alte prestazioni. Ispeziona il traffico e
genera **alert** quando un pacchetto/flusso combacia con una **regola** (firma). Può girare in:

- **IDS** — solo rilevamento e alert.
- **IPS** — inline, può **bloccare** il traffico malevolo.

## Idea chiave

- **Rule-based**: regole stile Snort (`alert tcp ... (msg:"..."; content:"..."; sid:...;)`).
  Feed di regole comuni: Emerging Threats, Talos.
- Multi-thread, fa anche estrazione file, logging TLS/HTTP e output **EVE JSON** verso un [[SIEM]].
- Le firme mappano spesso tecniche [[MITRE ATT&CK]] e cercano [[Indicatori di Compromissione (IOC)]].

## Suricata vs Zeek

Suricata = **detection a firme** (cosa è già noto-cattivo). [[Zeek]] = **visibilità/log** per
hunting su comportamento. Complementari: vedi tabella in [[Zeek]].

## Collegamenti

- [[Zeek]] · [[Wireshark]] · [[SIEM]] · [[Detection di Attacchi]] · [[Regole Sigma]]
- [[MITRE ATT&CK]] · [[Indicatori di Compromissione (IOC)]]
