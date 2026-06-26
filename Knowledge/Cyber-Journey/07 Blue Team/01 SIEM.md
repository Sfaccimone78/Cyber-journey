---
tipo: concetto
tag: [blue-team]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["SIEM"]

---

# SIEM

## In breve
Un **SIEM** (Security Information and Event Management) è una piattaforma centralizzata che raccoglie, normalizza e correla i log di tutti i sistemi di una rete. Permette al team di difesa di rilevare attacchi, investigare incidenti e rispettare normative di compliance, tutto da un'unica interfaccia.

## Come funziona
Il SIEM opera in tre fasi principali:

1. **Raccolta**: agenti o syslog inviano log da firewall, endpoint, server, Active Directory, applicazioni web.
2. **Normalizzazione**: i log arrivano in formati diversi (Windows Event Log, syslog, JSON). Il SIEM li converte in uno schema comune.
3. **Correlazione**: regole e algoritmi cercano sequenze sospette. Esempio: un login fallito 10 volte + login riuscito = possibile brute-force → genera un **alert**.

Il motore di ricerca interno permette di scrivere query per filtrare milioni di eventi in secondi. In [[Splunk]] si usa il linguaggio **SPL** (Search Processing Language).

## Esempio pratico
Query SPL per trovare tentativi di login falliti su Windows negli ultimi 60 minuti:

```spl
index=windows EventCode=4625
| stats count by src_ip, user
| where count > 5
| sort -count
```

Questo restituisce gli IP che hanno fallito più di 5 login, ordinati per frequenza — classico segnale di [[Detection di Attacchi]].

## Rilevanza per la sicurezza
Il SIEM è il cuore del [[Incident Response]]: senza di esso, gli analisti dovrebbero controllare log su ogni macchina manualmente. Accelera il [[Triage degli Alert]], supporta il [[Log Analysis]] strutturato e integra feed di [[Threat Intelligence]] e [[Indicatori di Compromissione (IOC)]].

## Collegamenti
- [[Splunk]]
- [[Log Analysis]]
- [[Incident Response]]
- [[Triage degli Alert]]
- [[Detection di Attacchi]]

## Fonti
- [Splunk Docs – What is SIEM?](https://www.splunk.com/en_us/blog/learn/siem-security-information-and-event-management.html)
- [IBM Security – SIEM explained](https://www.ibm.com/topics/siem)
- [SANS Reading Room – SIEM Best Practices](https://www.sans.org/white-papers/siem-best-practices/)
