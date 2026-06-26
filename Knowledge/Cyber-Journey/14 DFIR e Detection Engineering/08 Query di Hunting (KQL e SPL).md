---
tipo: entita
tag: [blue-team, tool]
fase: 4
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["Query di Hunting (KQL e SPL)", "KQL", "SPL"]
---

# Query di Hunting (KQL e SPL)

## Cosa sono
**SPL** (Search Processing Language) è il linguaggio di [[Splunk]]; **KQL** (Kusto Query Language)
è quello di **Microsoft Sentinel / Defender** (e Azure Data Explorer). Sono i due dialetti più
diffusi per [[Detection Engineering]] e [[Threat Hunting]]. Padroneggiarli significa saper
**interrogare la telemetria** per trasformare un'ipotesi in risultati. Concettualmente simili: si
parte da una sorgente, si filtra, si trasforma, si aggrega.

## Pipeline mentale (uguale nei due linguaggi)
```text
SORGENTE  →  FILTRO  →  TRASFORMA  →  AGGREGA  →  ORDINA/LIMITA
(index/table) (where)  (eval/extend) (stats/summarize) (sort/top)
```

## Stele di Rosetta SPL ↔ KQL
| Operazione | SPL (Splunk) | KQL (Sentinel/Defender) |
|---|---|---|
| Sorgente | `index=sysmon` | `DeviceProcessEvents` |
| Filtro | `EventCode=1 Image="*powershell*"` | `where FileName == "powershell.exe"` |
| Campo calcolato | `eval len=len(CommandLine)` | `extend len = strlen(ProcessCommandLine)` |
| Aggregazione | `stats count by host` | `summarize count() by DeviceName` |
| Conteggio distinti | `stats dc(user)` | `summarize dcount(Account)` |
| Insieme di valori | `stats values(CommandLine)` | `summarize make_set(ProcessCommandLine)` |
| Ordina | `sort - count` | `sort by count_ desc` |
| Limita | `head 20` | `take 20` / `top 20 by count_` |
| Finestra temporale | `bin _time span=1h` | `bin(TimeGenerated, 1h)` |
| Join | `join type=inner host [...]` | `join kind=inner (...) on DeviceName` |
| Regex match | `regex CommandLine="(?i)-enc"` | `where ProcessCommandLine matches regex "(?i)-enc"` |
| Lookup TI | `lookup ti_feed ip OUTPUT desc` | `... | lookup` / `externaldata` |

## Esempio pratico — PowerShell offuscato (T1059.001 / T1027)

SPL:
```spl
index=sysmon EventCode=1 Image="*\\powershell.exe"
| eval cmd=lower(CommandLine)
| where match(cmd,"-enc") OR match(cmd,"frombase64string")
        OR match(cmd,"-nop") OR match(cmd,"downloadstring") OR match(cmd,"iex")
| eval lunghezza=len(CommandLine)
| where lunghezza > 300
| table _time host User CommandLine lunghezza
| sort - lunghezza
```

KQL (Defender Advanced Hunting):
```kql
DeviceProcessEvents
| where FileName =~ "powershell.exe"
| extend cmd = tolower(ProcessCommandLine)
| where cmd has_any ("-enc","frombase64string","-nop","downloadstring","iex")
      or strlen(ProcessCommandLine) > 300
| project Timestamp, DeviceName, AccountName, ProcessCommandLine,
          InitiatingProcessFileName
| sort by Timestamp desc
```

## Esempio pratico — beaconing C2 (intervalli regolari verso un dominio)
KQL — varianza bassa sugli intervalli = beacon:
```kql
DeviceNetworkEvents
| where RemotePort in (80,443,8080)
| order by DeviceName, RemoteUrl, Timestamp asc
| serialize
| extend delta = datetime_diff('second', Timestamp, prev(Timestamp))
| summarize n = count(), avg_delta = avg(delta), stdev_delta = stdev(delta)
        by DeviceName, RemoteUrl
| where n > 20 and stdev_delta < 30 and avg_delta > 30   // periodicità sospetta
| sort by stdev_delta asc
```

SPL — rari domini contattati da pochi host (stacking DNS):
```spl
index=dns | stats dc(src) AS host_distinti count by query
| where host_distinti <= 2 AND count > 50
| sort count
```

## Buone pratiche per query di hunting
- **Filtra presto, trasforma dopo**: riduci subito il volume (performance).
- **Esplicita la finestra temporale** (`earliest=-7d` / `where Timestamp > ago(7d)`).
- **Case-insensitive** sui comandi (`lower()`/`tolower()`, `=~`, `has_any`).
- **Stacking** per far emergere il raro; **non** chiudere su una soglia rigida finché non hai
  baseline.
- **Parametrizza** la query → diventa una regola di [[Detection Engineering]] / [[Regole Sigma]].

> [!tip] Da hunting a detection
> Una query che trova in modo affidabile un comportamento, con falsi positivi gestibili, è già una
> detection: salvala come saved search/alert (Splunk) o analytics rule (Sentinel), o scrivila in
> Sigma per renderla portabile.

> [!caution] Etica
> Le query toccano dati di navigazione, account ed endpoint dei dipendenti: usale entro
> l'autorizzazione, minimizza i campi esportati, rispetta il GDPR.

## Lab
- **Splunk Boss of the SOC (BOTS) v1/v2/v3** — palestra SPL definitiva.
- **TryHackMe** — *Splunk*, *Investigating with Splunk*, *Microsoft Sentinel*, *KQL*.
- **Microsoft — KQL tutorial / Advanced Hunting** su dataset demo.
- **CyberDefenders / LetsDefend** — investigazioni che richiedono query mirate.

## Collegamenti
- [[Splunk]]
- [[Threat Hunting]]
- [[Detection Engineering]]
- [[Log Analysis Avanzata e Correlazione]]
- [[Regole Sigma]]
- [[Sysmon]]
- [[SIEM]]
- [[MITRE ATT&CK]]

## Fonti
- Splunk Search Reference (SPL): https://docs.splunk.com/Documentation/Splunk/latest/SearchReference
- KQL — Kusto Query Language reference: https://learn.microsoft.com/en-us/kusto/query/
- Microsoft Defender Advanced Hunting schema: https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-schema-tables
- Splunk Boss of the SOC dataset: https://github.com/splunk/botsv3
