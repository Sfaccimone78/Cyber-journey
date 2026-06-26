---
tipo: concetto
tag: [blue-team, metodologia]
fase: 4
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["MITRE D3FEND e Purple Teaming", "MITRE D3FEND", "Purple Teaming"]
---

# MITRE D3FEND e Purple Teaming

## In breve
Se [[MITRE ATT&CK]] è la tassonomia di ciò che fa **l'attaccante** (tecniche offensive),
**MITRE D3FEND** è la tassonomia di ciò che fa **il difensore** (contromisure). Il **purple
teaming** è la pratica che mette red e blue allo stesso tavolo: il red **emula** una tecnica, il
blue **verifica** di rilevarla/bloccarla, e insieme **migliorano** la detection. È il ponte
operativo tra offesa e difesa, e il modo più efficace per misurare la copertura reale.

## MITRE D3FEND — il contraltare difensivo di ATT&CK
D3FEND organizza le contromisure in categorie (tattiche difensive):

| Tattica D3FEND | Significato | Esempio |
|---|---|---|
| **Model** | conoscere il proprio ambiente | asset/network mapping |
| **Harden** | ridurre la superficie | application hardening, MFA |
| **Detect** | rilevare l'attività | process/file/network analysis |
| **Isolate** | confinare | segmentazione, sandboxing |
| **Deceive** | ingannare | honeypot, decoy account |
| **Evict** | espellere | account locking, process termination |

D3FEND collega ogni contromisura alle **tecniche ATT&CK** che mitiga, e introduce un **grafo
semantico** (Digital Artifact Ontology) che lega artefatti, offesa e difesa. Uso pratico: data una
tecnica ATT&CK osservata, D3FEND suggerisce *quali* difese la contrastano.

## Purple teaming — il ciclo
```text
1. Seleziona TTP    → da ATT&CK / threat intel sull'avversario rilevante
2. Emula (red)      → Atomic Red Team / Caldera eseguono la tecnica in lab
3. Osserva (blue)   → la telemetria (Sysmon/EDR) ha catturato l'attività?
4. Rileva?          → la detection è scattata? con che ritardo (MTTD)?
5. Migliora         → scrivi/affina la regola; documenta gap di copertura
6. Rimisura         → ri-emula: ora scatta. Aggiorna la heatmap ATT&CK
        ↑________________________ itera per tecnica __________________|
```

> [!tip] Purple ≠ "red + blue insieme una tantum"
> Il valore è il **loop chiuso e ripetibile**: ogni esercizio lascia una detection nuova e un
> punto in più sulla heatmap di copertura. È detection engineering guidata dall'emulazione.

## Esempio pratico — emulazione T1003.001 (LSASS dump) e verifica
```powershell
# 1) RED: emula la tecnica in modo controllato (Atomic Red Team)
Invoke-AtomicTest T1003.001 -TestNumbers 1     # comodump / procdump su lsass

# 2) BLUE: verifica la telemetria generata (Sysmon EID 10 = ProcessAccess su lsass)
#    Query Splunk:
#    index=sysmon EventCode=10 TargetImage="*\\lsass.exe" GrantedAccess=0x1410
```
```yaml
# 3) BLUE: se non scatta, deploya/affina la regola Sigma e ri-emula
title: Accesso a LSASS coerente con credential dumping
logsource: { product: windows, service: sysmon }
detection:
    selection:
        EventID: 10
        TargetImage|endswith: '\lsass.exe'
        GrantedAccess: '0x1410'
    condition: selection
level: high
tags: [attack.credential_access, attack.t1003.001]
```
```bash
# 4) Adversary emulation più ampia (catene multi-step) con MITRE Caldera
#    Avvia il server e lancia un'operazione su un agente in lab
python server.py --insecure
```

## Misurare la copertura
- **Heatmap ATT&CK** col [[MITRE ATT&CK Navigator]]: colora le tecniche coperte/da coprire.
- **DeTT&CT** / **Vectr**: tracciano copertura della telemetria e risultati degli esercizi purple.
- KPI: % tecniche con detection, MTTD per tecnica, gap di telemetria scoperti.

> [!caution] Etica e regole d'ingaggio
> L'emulazione (Atomic Red Team, Caldera, [[Metasploit]]) genera attività realmente malevola in
> forma controllata: eseguila **solo in lab o con Rules of Engagement scritte**, su ambienti
> autorizzati, con change approvato e finestra concordata. Mai in produzione "per provare".

## Lab
- **Atomic Red Team** (Red Canary) — libreria di test atomici per TTP.
- **MITRE Caldera** — piattaforma di adversary emulation automatizzata.
- **TryHackMe** — *MITRE*, *Atomic Red Team*, *Purple/Red vs Blue* rooms.
- **VECTR** (SecurityRiskAdvisors) — tracking degli esercizi purple team.

## Collegamenti
- [[MITRE ATT&CK]]
- [[MITRE ATT&CK Navigator]]
- [[Detection Engineering]]
- [[Threat Hunting]]
- [[Regole Sigma]]
- [[Sysmon]]
- [[Threat Intelligence (Diamond Model, Pyramid of Pain)]]
- [[Incident Response]]

## Fonti
- MITRE D3FEND: https://d3fend.mitre.org/
- MITRE ATT&CK: https://attack.mitre.org/
- MITRE Caldera: https://caldera.mitre.org/
- Atomic Red Team (Red Canary): https://github.com/redcanaryco/atomic-red-team
