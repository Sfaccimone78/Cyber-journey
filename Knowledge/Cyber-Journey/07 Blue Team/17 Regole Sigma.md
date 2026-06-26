---
tipo: concetto
tag: [blue-team]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Regole Sigma"]
---

# Regole Sigma

## In breve
**Sigma** è un formato **generico e aperto** per scrivere regole di detection sui **log**, indipendente dal [[SIEM]] specifico. Se YARA è "lo standard per i file", Sigma è "lo standard per i log": una regola scritta una volta si **converte** in query per [[Splunk]] (SPL), Elastic, Sentinel e altri. Risolve il problema di dover riscrivere le stesse detection per ogni piattaforma.

## Anatomia di una regola
```yaml
title: Sospetto dump di LSASS
status: experimental
logsource:
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 10
        TargetImage|endswith: '\lsass.exe'
        GrantedAccess: '0x1410'
    condition: selection
level: high
tags:
    - attack.credential_access
    - attack.t1003.001
```

## Uso tipico
La conversione si fa con **sigma-cli** (motore `pySigma`):
```bash
# Converte una regola Sigma in query Splunk
sigma convert -t splunk regola.yml

# Backend Elastic (Lucene)
sigma convert -t lucene regola.yml
```

## Quando si usa
- Per **condividere detection** nella community in modo portabile (mappate su [[MITRE ATT&CK]]).
- Per alimentare le regole di correlazione di un [[SIEM]] partendo da telemetria [[Sysmon]].
- In threat hunting, per tradurre rapidamente un comportamento noto in query eseguibile.

## Note e trucchi
- I campi `*|endswith`, `*|contains`, `*|re` permettono match flessibili.
- Il **SigmaHQ** mantiene migliaia di regole pronte all'uso, già taggate ATT&CK.
- Una buona regola bilancia copertura e falsi positivi: testala sui tuoi log prima di metterla in alert.

## Collegamenti
- [[SIEM]]
- [[Splunk]]
- [[Sysmon]]
- [[Detection di Attacchi]]
- [[Log Analysis]]
- [[MITRE ATT&CK]]

## Fonti
- SigmaHQ (regole + spec): https://github.com/SigmaHQ/sigma
- pySigma / sigma-cli: https://github.com/SigmaHQ/sigma-cli
- Sigma documentation: https://sigmahq.io/docs/
