---
tipo: concetto
tag: [blue-team, metodologia]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Log Analysis Avanzata e Correlazione", "Correlazione di Log", "Logging e Monitoraggio"]
---

# Log Analysis Avanzata e Correlazione

## In breve
Oltre la lettura del singolo log (vedi [[Log Analysis]] base), l'analisi avanzata consiste nel
**correlare eventi da sorgenti diverse** per ricostruire una catena d'attacco che nessun log
mostra da solo. Un logon (4624), una connessione di rete (Sysmon EID 3) e un processo figlio
anomalo (4688) presi singolarmente sono rumore; **uniti sullo stesso host nello stesso minuto**
sono un'intrusione. Questo è il cuore del lavoro nel [[SIEM]] e l'anticamera del threat hunting.

## Concetti chiave
- **Normalizzazione / data model**: portare campi eterogenei a uno schema comune (es. Splunk CIM,
  Elastic ECS) così `src_ip`, `user`, `process` significano la stessa cosa ovunque.
- **Aggregazione**: collassare N eventi in una statistica (`count`, `dc`, `values`) per far
  emergere anomalie.
- **Correlazione temporale**: stessa entità (host/utente) entro una finestra (`transaction`,
  `bin _time`).
- **Enrichment**: arricchire l'evento con [[Threat Intelligence]], geo-IP, asset criticità.
- **Baseline & anomalia**: cosa è "normale" per quell'host/utente → ciò che devia è sospetto.

## Pattern di correlazione utili (catene tipiche)
| Catena | Sorgenti correlate | Tecnica ATT&CK |
|---|---|---|
| Phishing → esecuzione | Mail GW + 4688/Sysmon EID 1 (Office→PowerShell) | T1566 → T1059 |
| Brute force → accesso | molti 4625 poi un 4624 stesso `src_ip` | T1110 → valid accounts |
| Lateral movement | 4624 LogonType 3 + 7045 (servizio) + Sysmon EID 3 | T1021 / T1570 |
| Exfiltration | spike byte in uscita + connessione a IP raro | T1041 / T1567 |
| Credential dumping | Sysmon EID 10 su lsass + 4688 (procdump) | T1003.001 |

## Esempio pratico — correlazione brute force → logon riuscito
Splunk (SPL): trova IP che falliscono molte volte e poi riescono.
```spl
index=wineventlog (EventCode=4625 OR EventCode=4624)
| eval esito=if(EventCode=4625,"fail","success")
| stats count(eval(esito="fail")) AS falliti,
        count(eval(esito="success")) AS riusciti,
        values(user) AS utenti by Source_Network_Address
| where falliti > 20 AND riusciti > 0
| sort - falliti
```

Stessa idea in **KQL** (Microsoft Sentinel / Defender):
```kql
SecurityEvent
| where EventID in (4624, 4625)
| summarize falliti = countif(EventID == 4625),
            riusciti = countif(EventID == 4624),
            utenti = make_set(Account)
        by IpAddress, bin(TimeGenerated, 30m)
| where falliti > 20 and riusciti > 0
```

Correlazione padre-figlio per phishing (Office che genera una shell):
```spl
index=sysmon EventCode=1
| where like(ParentImage,"%WINWORD.EXE%") OR like(ParentImage,"%EXCEL.EXE%")
| search Image IN ("*powershell.exe","*cmd.exe","*wscript.exe","*mshta.exe")
| table _time host ParentImage Image CommandLine
```

> [!warning] Il nemico è il falso positivo
> Una correlazione troppo larga seppellisce il SOC di rumore (alert fatigue); troppo stretta perde
> l'attacco. Si itera con una **baseline** e si misura il rapporto segnale/rumore prima di
> promuovere una correlazione a regola di alert. Questo passaggio collega l'analisi alla
> [[Detection Engineering]].

## Metodologia di indagine (dall'alert alla storia)
1. **Pivot sull'entità**: dall'alert, espandi su tutto ciò che ha fatto quell'host/utente.
2. **Allinea i tempi**: ordina gli eventi correlati in timeline (vedi
   [[Disk Forensics e Timeline Analysis]]).
3. **Conferma il TTP**: mappa su [[MITRE ATT&CK]] per capire la fase.
4. **Espandi lo scope**: cerca gli stessi [[Indicatori di Compromissione (IOC)]] altrove.
5. **Documenta**: la catena correlata diventa la timeline dell'[[Incident Response]].

## Checklist
- [ ] Sorgenti normalizzate a un data model (CIM/ECS).
- [ ] Finestra temporale e entità di pivot definite.
- [ ] Enrichment con TI/asset/geo applicato.
- [ ] Baseline nota per distinguere anomalia da normalità.
- [ ] Catena mappata su ATT&CK e pronta come timeline.

## Lab
- **Splunk Boss of the SOC (BOTS)** — dataset v1/v2/v3, il riferimento per correlazione SPL.
- **TryHackMe** — *Splunk 101/201/301*, *Investigating with Splunk*, *Sysmon*.
- **LetsDefend** — alert investigation con log multi-sorgente.
- **Microsoft Sentinel** — *KQL training* + content hub per regole di correlazione.

## Domande
**D: Perché la correlazione tra sorgenti è la chiave?**
R: Un singolo log raramente racconta l'attacco; correlare auth + processi + rete + proxy ricostruisce
la **kill chain** e riduce i falsi positivi.

**D: Quali Event ID Windows contano per i logon e cosa rivela il logon type?**
R: 4624 (logon riuscito), 4625 (fallito), 4672 (privilegi assegnati), 4634/4647 (logoff). Il **logon
type** indica il vettore: 3 = rete, 10 = RDP, 2 = interattivo, 8 = clear-text.

**D: Cos'è la time normalization e perché serve?**
R: Portare tutti i timestamp a UTC/stesso formato prima di correlare; senza, sorgenti con fusi/clock
diversi disallineano la timeline e rompono la correlazione.

## Collegamenti
- [[Log Analysis]]
- [[SIEM]]
- [[Splunk]]
- [[Query di Hunting (KQL e SPL)]]
- [[Detection Engineering]]
- [[Sysmon]]
- [[MITRE ATT&CK]]
- [[Indicatori di Compromissione (IOC)]]

## Fonti
- Splunk CIM (Common Information Model): https://docs.splunk.com/Documentation/CIM
- Elastic Common Schema (ECS): https://www.elastic.co/guide/en/ecs/current/index.html
- Splunk Boss of the SOC dataset: https://github.com/splunk/botsv3
- The DFIR Report (catene d'attacco reali da correlare): https://thedfirreport.com/
