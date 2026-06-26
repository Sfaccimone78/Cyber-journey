---
tipo: concetto
tag: [blue-team]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Triage degli Alert"]

---

# Triage degli Alert

## In breve
Il **triage degli alert** è il processo con cui un analista SOC valuta rapidamente un alert generato dal [[SIEM]] per determinare se si tratta di un **vero positivo** (attacco reale), un **falso positivo** (comportamento legittimo classificato erroneamente) o un **falso negativo** (attacco non rilevato). È la prima azione dopo che scatta un allarme.

## Come funziona
Il triage segue tipicamente questi passi:

1. **Ricevi l'alert**: il [[SIEM]] genera una notifica con severity, timestamp, host e utente coinvolti.
2. **Raccogli contesto**: chi è l'utente? È un orario normale? Il dispositivo è un server critico?
3. **Cerca correlazioni**: ci sono altri alert simili nelle ultime ore? L'IP sorgente è in una lista di [[Indicatori di Compromissione (IOC)]]?
4. **Classifica**:
   - **Vero positivo** → escalation a [[Incident Response]]
   - **Falso positivo** → chiudi e documenta la regola da aggiustare
   - **Beningno vero positivo** → attività autorizzata che ha triggerato la regola (es. pen test pianificato)
5. **Documenta**: ogni decisione va tracciata per audit e per migliorare le regole future.

## Esempio pratico
Un analista su [[LetsDefend]] riceve un alert: `EventCode=4625` (login fallito) per l'utente `admin` da IP `192.168.1.200`, 47 volte in 2 minuti.

Controllo in [[Splunk]]:
```spl
index=windows EventCode=4625 user="admin" src_ip="192.168.1.200"
| timechart count span=1m
```

Il grafico mostra un picco improvviso alle 03:17. L'IP è interno ma insolito. Esito: **vero positivo** — brute-force interno. Si isola la macchina e si apre un caso.

## Rilevanza per la sicurezza
Un triage lento o errato può trasformare un incidente contenibile in una violazione grave. L'analista SOC di livello 1 passa la maggior parte del tempo in questa fase. Piattaforme come [[LetsDefend]] simulano scenari reali di triage con alert, log e artefatti da analizzare.

## Collegamenti
- [[SIEM]]
- [[Splunk]]
- [[Detection di Attacchi]]
- [[Indicatori di Compromissione (IOC)]]
- [[Incident Response]]
- [[Log Analysis]]
- [[LetsDefend]]
- [[Windows Event Log]]

## Fonti
- [LetsDefend – Alert Triage](https://letsdefend.io/blog/what-is-alert-triage/)
- [Splunk Docs – Incident Review](https://docs.splunk.com/Documentation/ES/latest/User/Triagenotableevents)
- [SANS – SOC Analyst Triage Guide](https://www.sans.org/blog/soc-analyst-guide-alert-triage/)
