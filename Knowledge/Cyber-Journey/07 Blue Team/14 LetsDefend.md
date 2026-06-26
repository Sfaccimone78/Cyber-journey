---
tipo: entita
tag: [blue-team, piattaforma, formazione]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["LetsDefend"]

---

# LetsDefend

## Cos'è
**LetsDefend** (https://letsdefend.io) è una piattaforma di formazione pratica per analisti SOC. Simula un ambiente SOC reale con una coda di alert, un SIEM, log di sistema, email sospette e strumenti di analisi. A differenza di TryHackMe (più orientata all'hacking etico), LetsDefend si concentra esclusivamente sul lato difensivo (blue-team): investigare alert, fare [[Triage degli Alert]], analizzare malware e rispondere agli incidenti.

## Uso tipico

Flusso standard su LetsDefend:
1. Accedi alla **Monitoring** dashboard: vedi la coda degli alert attivi (simile a [[Splunk]] Enterprise Security).
2. Seleziona un alert (es. "SOC165 – Possible SQL Injection Payload Detected").
3. Indaga: analizza i log, cerca l'IP sorgente su [[VirusTotal]], verifica il payload.
4. Classifica: **True Positive** o **False Positive**.
5. Se TP: compila il report dell'incidente con artefatti, timeline e azioni di contenimento.
6. Chiudi il caso.

Ogni alert è basato su scenari reali accaduti in SOC aziendali, con log autentici.

## Quando si usa
- Imparare il [[Triage degli Alert]] in un ambiente sicuro e realistico
- Esercitarsi con la [[Detection di Attacchi]] su casi pratici (phishing, malware, lateral movement)
- Studiare [[Log Analysis]] su log Windows, Linux, firewall e proxy
- Praticare l'uso di strumenti come [[VirusTotal]], [[Any.run]] e [[MITRE ATT&CK Navigator]] in contesto reale
- Preparazione per certificazioni SOC (CompTIA CySA+, SANS GCIA)

## Note e trucchi
- **Piano gratuito**: accesso a molti alert e percorsi di apprendimento, sufficiente per iniziare.
- **Piano SOC Analyst**: alert illimitati, casi più complessi, certificati di completamento.
- La sezione **"Learning Paths"** organizza i moduli per ruolo: SOC Analyst Tier 1, Malware Analyst, Incident Responder.
- Ogni caso risolto correttamente aggiunge punti al tuo profilo — gamification utile per la motivazione.
- Integra LetsDefend con [[Wireshark]] per i casi che includono catture di traffico di rete.

## Collegamenti
- [[Triage degli Alert]]
- [[Detection di Attacchi]]
- [[Log Analysis]]
- [[Incident Response]]
- [[VirusTotal]]
- [[Any.run]]
- [[MITRE ATT&CK Navigator]]
- [[Splunk]]
- [[Wireshark]]

## Fonti
- [LetsDefend – Sito ufficiale](https://letsdefend.io)
- [LetsDefend – SOC Analyst Learning Path](https://letsdefend.io/training/soc-analyst-learning-path)
- [TryHackMe – Blue Team Learning Path](https://tryhackme.com/path/outline/blueteam)
