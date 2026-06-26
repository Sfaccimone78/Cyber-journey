---
tipo: entita
tag: [blue-team, tool]
fase: 3
fonti: 0
aggiornato: 2026-06-26
stato: stub
aliases: ["Zeek"]
---

# Zeek

> [!info] Stub
> Network Security Monitor. Da espandere.

**Zeek** (ex *Bro*) = framework open-source di **network security monitoring** (NSM). Non è un
IDS a firme: osserva il traffico e produce **log strutturati ad alto livello** (connessioni, DNS,
HTTP, TLS, file trasferiti), su cui poi si fa detection e hunting.

## Idea chiave

- **Event-driven**: motore che genera eventi dal traffico + script in linguaggio Zeek per reagire.
- Output = decine di log (`conn.log`, `dns.log`, `http.log`, `ssl.log`, `files.log`…) ideali da
  inviare a un [[SIEM]] per correlazione.
- Forte su **visibilità e contesto**; complementare alle firme di [[Suricata]].

## Zeek vs Suricata

| | Zeek | [[Suricata]] |
|---|------|----------|
| Modello | Behavioral / log-centric | Signature-based IDS/IPS |
| Output | Log ricchi per hunting | Alert su match di regole |
| Uso tipico | Visibilità, threat hunting | Detection/blocco noto |

Spesso si usano **insieme**.

## Collegamenti

- [[Suricata]] · [[Wireshark]] · [[SIEM]] · [[Log Analysis]] · [[Detection di Attacchi]]
- [[Threat Intelligence]] · [[Indicatori di Compromissione (IOC)]]
