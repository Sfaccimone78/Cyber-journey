---
tipo: concetto
tag: [blue-team]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Threat Intelligence"]

---

# Threat Intelligence

## In breve
La **Threat Intelligence** (TI) è il processo di raccolta, analisi e condivisione di informazioni sulle minacce informatiche attive o emergenti. L'obiettivo è trasformare dati grezzi (IP malevoli, hash di malware, tattiche degli attaccanti) in conoscenza utile per prendere decisioni difensive più rapide e accurate.

## Come funziona
La TI opera su tre livelli:

1. **Strategico**: informazioni ad alto livello per il management (tendenze, gruppi APT attivi, settori colpiti).
2. **Operativo**: dettagli su campagne specifiche — chi attacca, come, e con quale scopo.
3. **Tattico**: artefatti tecnici immediatamente utilizzabili dai sistemi di difesa, come [[Indicatori di Compromissione (IOC)]] (hash, IP, domini, URL).

I dati di TI arrivano da fonti aperte (OSINT), feed commerciali, Information Sharing comunity (ISAC), o da piattaforme come [[VirusTotal]] e [[MITRE ATT&CK Navigator]]. Una volta ottenuti, vengono integrati nel [[SIEM]] o in un firewall per bloccare automaticamente le minacce note.

## Esempio pratico
Un analista riceve via feed STIX/TAXII un elenco di IP associati a un ransomware attivo. Li importa in [[Splunk]] con una query:

```spl
index=firewall dest_ip IN ("185.220.101.5", "194.165.16.77")
| stats count by src_ip, dest_ip, action
```

Se appaiono connessioni verso quegli IP, si apre immediatamente un ticket di [[Triage degli Alert]].

## Rilevanza per la sicurezza
Senza TI, la difesa è cieca: si reagisce solo dopo un danno. Con la TI si anticipa l'attacco bloccando gli IOC prima che causino compromissioni. È fondamentale nel ciclo di [[Incident Response]] e nella [[Detection di Attacchi]] proattiva.

## Collegamenti
- [[Indicatori di Compromissione (IOC)]]
- [[MITRE ATT&CK]]
- [[MITRE ATT&CK Navigator]]
- [[VirusTotal]]
- [[SIEM]]
- [[Splunk]]
- [[Detection di Attacchi]]
- [[Incident Response]]

## Fonti
- [MITRE ATT&CK – Getting Started with CTI](https://attack.mitre.org/resources/getting-started/)
- [SANS – Introduction to Cyber Threat Intelligence](https://www.sans.org/white-papers/introduction-cyber-threat-intelligence-40120/)
- [TryHackMe – Threat Intelligence Tools](https://tryhackme.com/room/threatinteltools)
