---
tipo: concetto
tag: [blue-team, metodologia]
fase: 4
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["Threat Hunting"]
---

# Threat Hunting (metodologia e ipotesi)

## In breve
Il **threat hunting** è la ricerca **proattiva** di minacce che hanno **eluso le detection
automatiche**. Parte dall'assunzione *assume breach*: "l'avversario è già dentro, gli alert non
sono scattati — vado a cercarlo". A differenza del [[Triage degli Alert]] (reattivo, parte da un
alert), l'hunting parte da un'**ipotesi** e usa i dati per confermarla o smentirla. Output di una
caccia: o trovi il male, o generi una **nuova detection** (vedi [[Detection Engineering]]).

## I tre tipi di hunting
| Tipo | Punto di partenza | Esempio |
|---|---|---|
| **Hypothesis-driven** | un'ipotesi sui TTP (da [[MITRE ATT&CK]]) | "qualcuno usa WMI per lateral movement" |
| **IOC/Intel-driven** | indicatori da [[Threat Intelligence]] | "cerco gli IOC di APT29 nei log" |
| **Anomaly/ML-driven** | deviazioni dalla baseline | "host che parla con domini DGA" |

## Metodologia — il loop di hunting (PEAK / TaHiTI)
```text
1. Ipotesi      → formulata, testabile, ancorata a un TTP ATT&CK
2. Ambito/dati  → quali log servono? (Sysmon, EDR, proxy, DNS...) li ho?
3. Caccia       → query, pivot, baseline, esclusione del rumore
4. Esito        → trovato il male? scope completo. Niente? ipotesi smentita
5. Capitalizza  → ogni caccia produce: detection nuova, runbook, o gap noto
        ↑________________________ ripeti _____________________|
```

> [!tip] Una buona ipotesi è falsificabile
> Cattiva: "forse c'è un attaccante". Buona: *"un avversario sta usando `rundll32.exe` per
> eseguire codice da una directory utente (T1218.011); se è vero, vedrò `rundll32` con
> ParentImage anomalo e CommandLine senza DLL di sistema"*. Ogni ipotesi nomina una **tecnica**,
> un **artefatto osservabile** e una **fonte di dati**.

## Esempio pratico — caccia a WMI lateral movement (T1021.003 / T1047)
Ipotesi: *un attaccante esegue comandi su host remoti via WMI*.

KQL (Defender/Sentinel) — processi figli di `WmiPrvSE.exe`:
```kql
DeviceProcessEvents
| where InitiatingProcessFileName =~ "WmiPrvSE.exe"
| where FileName in~ ("powershell.exe","cmd.exe","wscript.exe","mshta.exe","rundll32.exe")
| project Timestamp, DeviceName, AccountName,
          InitiatingProcessFileName, FileName, ProcessCommandLine
| sort by Timestamp desc
```

SPL (Splunk, telemetria [[Sysmon]]):
```spl
index=sysmon EventCode=1 ParentImage="*\\WmiPrvSE.exe"
| stats count values(CommandLine) AS comandi by host, User, Image
| sort - count
```

Pivot di stacking (frequency analysis) — l'anomalo è il **raro**:
```spl
index=sysmon EventCode=1 Image="*\\rundll32.exe"
| stats count by CommandLine
| sort count          # le righe con count basso = candidati sospetti (long tail)
```

## Tecniche di analisi del cacciatore
- **Stacking / least-frequency**: ordina per frequenza; il legittimo è comune, il malevolo è raro.
- **Baselining**: definisci il normale per host/utente, poi cerca le deviazioni.
- **Pivoting**: da un artefatto (hash, IP, account) espandi a tutto ciò che lo tocca.
- **Grouping / clustering**: raggruppa eventi correlati per scoprire una campagna.
- **Enrichment**: aggiungi contesto TI/asset per dare priorità.

## Misurare l'hunting
- **Copertura ATT&CK** delle ipotesi (heatmap col Navigator) → quali tecniche non ho mai cacciato?
- **Nuove detection prodotte** per caccia (il vero ROI).
- **Gap di telemetria** scoperti (es. "non loggho DNS" → blind spot).
- **Tempo di permanenza (dwell time)** ridotto nel tempo.

> [!caution] Etica
> L'hunting accede a telemetria che include attività e dati personali dei dipendenti: opera nei
> limiti dell'autorizzazione, minimizza e proteggi i dati (GDPR). Caccia su ambienti di tua
> competenza o con mandato esplicito.

## Lab
- **Splunk Boss of the SOC (BOTS)** — il dataset di riferimento per cacce SPL.
- **TryHackMe** — *Threat Hunting*, *Hunting Evil*, percorso *SOC Level 2 / Threat Hunting*.
- **CyberDefenders** — challenge di hunting su log reali.
- **Microsoft Defender / Sentinel** — *advanced hunting* (KQL) su dataset demo.

## Collegamenti
- [[Detection Engineering]]
- [[Query di Hunting (KQL e SPL)]]
- [[MITRE ATT&CK]]
- [[Threat Intelligence (Diamond Model, Pyramid of Pain)]]
- [[Log Analysis Avanzata e Correlazione]]
- [[Sysmon]]
- [[Indicatori di Compromissione (IOC)]]
- [[Triage degli Alert]]

## Fonti
- SANS — Threat Hunting & summit resources: https://www.sans.org/blog/what-is-cyber-threat-hunting/
- Splunk PEAK Threat Hunting Framework: https://www.splunk.com/en_us/blog/security/peak-threat-hunting-framework.html
- TaHiTI (Targeted Hunting integrating Threat Intelligence): https://www.betaalvereniging.nl/en/safety/tahiti/
- ThreatHunting Project / Sysmon hunting: https://github.com/ThreatHuntingProject/ThreatHunting
