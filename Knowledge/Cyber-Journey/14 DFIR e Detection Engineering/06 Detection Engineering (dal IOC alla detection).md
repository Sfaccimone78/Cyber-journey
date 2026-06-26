---
tipo: concetto
tag: [blue-team, metodologia]
fase: 4
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["Detection Engineering"]
---

# Detection Engineering (dal IOC alla detection)

## In breve
La **detection engineering** applica pratiche di ingegneria del software alla creazione di
detection: le regole sono **codice** versionato, testato e misurato, non file scritti a mano e
dimenticati nel SIEM. L'obiettivo è salire la **Pyramid of Pain** (vedi
[[Threat Intelligence (Diamond Model, Pyramid of Pain)]]): passare da detection fragili su
[[Indicatori di Compromissione (IOC)]] atomici (hash, IP) a detection robuste su **TTP** e
comportamenti, che costano molto di più all'attaccante per essere aggirate.

## Detection-as-Code: il ciclo di vita
```text
Ipotesi/Intel  →  Sviluppo regola  →  Test (true/false positive)  →
Deploy (CI/CD)  →  Tuning (riduci FP)  →  Documentazione  →  Monitor/decadimento
        ↑___________________ feedback ___________________|
```
Principi:
- **Versionamento** (Git): ogni regola ha storia, autore, review.
- **Portabilità**: scrivi una volta in [[Regole Sigma]], converti per ogni backend.
- **Documentazione**: ogni regola dichiara TTP coperto, falsi positivi noti, log richiesti,
  risposta suggerita.
- **Misura**: copertura ATT&CK, tasso FP, MTTD; le regole **decadono** (un cambio ambiente le
  rompe) e vanno mantenute.

## Dal IOC alla detection comportamentale (esempio progressivo)
Stesso attacco (dump di LSASS), tre livelli di robustezza crescente:

```yaml
# LIVELLO 1 - IOC atomico (fragile: cambia hash e sparisce)
detection:
    selection:
        Hashes|contains: 'SHA256=ab12...'   # hash di procdump.exe
    condition: selection
```
```yaml
# LIVELLO 2 - tool/argomento (più robusto: copre rinominati)
title: Procdump su LSASS
logsource: { product: windows, service: sysmon }
detection:
    selection:
        EventID: 1
        CommandLine|contains|all:
            - 'lsass'
            - '-ma'
    condition: selection
level: high
tags: [attack.credential_access, attack.t1003.001]
```
```yaml
# LIVELLO 3 - comportamento (massima robustezza: indipendente dal tool)
title: Accesso anomalo a LSASS (handle con GrantedAccess sospetto)
logsource: { product: windows, service: sysmon }
detection:
    selection:
        EventID: 10                    # ProcessAccess
        TargetImage|endswith: '\lsass.exe'
        GrantedAccess: '0x1410'        # PROCESS_VM_READ | QUERY_INFORMATION
    filter:
        SourceImage|endswith:
            - '\MsMpEng.exe'           # esclusioni legittime (AV)
            - '\wininit.exe'
    condition: selection and not filter
level: high
tags: [attack.credential_access, attack.t1003.001]
```

> [!tip] Perché salire di livello
> Un avversario cambia un hash in un secondo, rinomina un binario in un minuto, ma **cambiare il
> comportamento** (come accede a LSASS) richiede di riscrivere il tool. Detection sui TTP = "dolore"
> massimo per l'attaccante (Pyramid of Pain).

## Convertire e testare
```bash
# Sigma -> query per il tuo SIEM (vedi Regole Sigma)
sigma convert -t splunk -p sysmon lsass_access.yml      # backend Splunk
sigma convert -t microsoft365defender lsass_access.yml  # backend KQL/Defender

# Validare la regola sui dati di test (true positive deve scattare, baseline no)
sigma check lsass_access.yml

# Emulare la tecnica per generare la telemetria e verificare la detection
# Atomic Red Team - T1003.001
Invoke-AtomicTest T1003.001 -TestNumbers 1
```

## Qualità di una detection — criteri
| Criterio | Domanda |
|---|---|
| **Robustezza** | È legata a un IOC effimero o a un comportamento? |
| **Falsi positivi** | Quanto rumore genera sulla baseline reale? |
| **Copertura** | Quali varianti della tecnica cattura/perde? |
| **Telemetria** | I log richiesti ([[Sysmon]], EDR) sono effettivamente raccolti? |
| **Risposta** | Cosa deve fare l'analista quando scatta? |
| **Manutenibilità** | È versionata, documentata, testabile? |

## Framework e maturità
- **Alerting & Detection Strategy (ADS)** di Palantir: template per documentare ogni regola.
- **MITRE ATT&CK** come tassonomia di copertura (heatmap col Navigator).
- **Detection Maturity Level (DML)** di Ryan Stillions: da IOC atomici verso intent/goal.
- **DeTT&CT** / **Atomic Red Team** per misurare copertura e validare con emulazione.

> [!caution] Etica
> L'emulazione (Atomic Red Team, Caldera, [[Metasploit]]) genera attività malevola *simulata*:
> eseguila **solo** in lab o con autorizzazione scritta, mai in produzione senza change approvato.
> Vedi [[MITRE D3FEND e Purple Teaming]].

## Lab
- **TryHackMe** — *Sigma*, *Threat Hunting*, *Detection Engineering*, percorso *SOC Level 2*.
- **SigmaHQ** — migliaia di regole reali da studiare e adattare.
- **Atomic Red Team** (Red Canary) — emulazione TTP per testare le tue detection.
- **Splunk Attack Range** / **Microsoft Sentinel content hub** — ambienti per detection-as-code.

## Collegamenti
- [[Regole Sigma]]
- [[Sysmon]]
- [[YARA]]
- [[Indicatori di Compromissione (IOC)]]
- [[MITRE ATT&CK]]
- [[Detection di Attacchi]]
- [[Threat Hunting]]
- [[Query di Hunting (KQL e SPL)]]
- [[Threat Intelligence (Diamond Model, Pyramid of Pain)]]
- [[MITRE D3FEND e Purple Teaming]]

## Fonti
- SigmaHQ (spec + regole): https://github.com/SigmaHQ/sigma
- Florian Roth — "About Detection Engineering": https://cyb3rops.medium.com/about-detection-engineering-44d39e0755f0
- Palantir — Alerting and Detection Strategy Framework: https://github.com/palantir/alerting-detection-strategy-framework
- Atomic Red Team (Red Canary): https://github.com/redcanaryco/atomic-red-team
