---
tipo: sintesi
tag: [blue, moc]
fase: 3
fonti: 2
aggiornato: 2026-06-26
stato: maturo
aliases: ["Mappa DFIR e Detection Engineering"]
---

# DFIR e Detection Engineering - Mappa

Area **expert (fase 3-4)** che estende [[Incident Response]] e il [[SIEM]] verso la
**forensics avanzata**, la **detection engineering** e il **threat hunting** proattivo.
Mentre `07 Blue Team` copre SIEM, IR e MITRE a livello base, qui si passa dalla reazione
all'**investigazione profonda** (RAM, disco, timeline, artefatti) e alla **costruzione di
detection** misurabili.

> [!info] Filosofia dell'area
> Tre domande guida: *cosa è successo?* (forensics) → *come lo rilevo la prossima volta?*
> (detection engineering) → *posso trovarlo prima che scatti un alert?* (threat hunting).

## Percorso in ordine d'apprendimento (segui la numerazione)

[[Digital Forensics Fondamenti]] · [[Memory Forensics con Volatility]] · [[Disk Forensics e Timeline Analysis]] · [[Windows Forensics (artefatti)]] · [[Log Analysis Avanzata e Correlazione]] · [[Detection Engineering]] · [[Threat Hunting]] · [[Query di Hunting (KQL e SPL)]] · [[MITRE D3FEND e Purple Teaming]] · [[Threat Intelligence (Diamond Model, Pyramid of Pain)]]

## Le tre fasi della disciplina

| Fase | Pagine | Domanda |
|---|---|---|
| **Forensics (reattiva)** | 01-04 | Cosa è successo? Ricostruisci i fatti dalle prove. |
| **Detection (proattiva)** | 05-06, 08 | Come lo rilevo? Trasforma comportamenti in regole. |
| **Hunting (ipotesi)** | 07, 09-10 | Posso trovarlo senza alert? Cerca l'ignoto. |

## Relazione con `07 Blue Team`

- [[Volatility (Memory Forensics)]] (entità base) → approfondita in [[Memory Forensics con Volatility]].
- [[Regole Sigma]], [[Sysmon]], [[YARA]] → usate come mattoni in [[Detection Engineering]].
- [[Threat Intelligence]] (base) → modellata in [[Threat Intelligence (Diamond Model, Pyramid of Pain)]].
- [[Incident Response]] → la forensics di quest'area alimenta le fasi Detection e Eradication dell'IR.

## Navigazione
[[00 — Mappa Reverse Engineering e Exploit Dev|13 Reverse Engineering e Exploit Dev]] <- [[index|Indice]]
