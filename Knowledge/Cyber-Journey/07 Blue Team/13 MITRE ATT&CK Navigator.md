---
tipo: entita
tag: [blue-team, tool, threat-intel]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["MITRE ATT&CK Navigator"]

---

# MITRE ATT&CK Navigator

## Cos'è
**ATT&CK Navigator** è lo strumento ufficiale di MITRE per visualizzare e annotare la matrice [[MITRE ATT&CK]]. Si presenta come una griglia interattiva dove ogni colonna è una **tattica** (es. Initial Access, Persistence, Lateral Movement) e ogni cella è una **tecnica** (es. T1059 – Command and Scripting Interpreter). Permette di colorare, filtrare e sovrapporre layer per rappresentare la copertura della detection, le TTP di un gruppo APT o i gap difensivi di un'organizzazione.

## Uso tipico

Accesso online: https://mitre-attack.github.io/attack-navigator/

Flusso tipico per un analista SOC:
1. Apri Navigator e seleziona la matrice "Enterprise".
2. Crea un **layer** (es. "Detection Coverage").
3. Colora in verde le tecniche per cui hai già regole nel [[SIEM]] [[Splunk]].
4. Colora in rosso quelle senza copertura — sono i tuoi gap prioritari.
5. Esporta il layer in JSON per condividerlo con il team.

Per sovrapporre le TTP di un gruppo specifico (es. APT29):
- Vai su https://attack.mitre.org/groups/G0016/
- Clicca "ATT&CK Navigator Layers" e importa il layer precompilato.

## Quando si usa
- **[[Detection di Attacchi]]**: mappare quale percentuale delle tecniche ATT&CK è coperta dalle tue regole
- **[[Threat Intelligence]]**: visualizzare le TTP di un gruppo APT che sta colpendo il tuo settore
- **Gap analysis**: identificare tecniche non monitorate e prioritizzare la scrittura di nuove detection
- **Report**: comunicare visivamente la postura difensiva al management

## Note e trucchi
- Puoi eseguire Navigator **localmente** scaricando il repo GitHub — utile in ambienti air-gapped.
- I **layer predefiniti** per ogni gruppo APT sono scaricabili direttamente dalla pagina del gruppo su attack.mitre.org.
- Combina più layer con la funzione **"Create Layer from Other Layers"** per vedere intersezioni (es. tecniche comuni tra APT28 e APT29).
- Le tecniche con **subtecniche** si espandono cliccando sul triangolino: T1059 ne ha 8, una per linguaggio (PowerShell, Python, Bash, ecc.).

## Collegamenti
- [[MITRE ATT&CK]]
- [[Detection di Attacchi]]
- [[Threat Intelligence]]
- [[Splunk]]
- [[SIEM]]
- [[Any.run]]
- [[LetsDefend]]

## Fonti
- [MITRE ATT&CK Navigator – GitHub](https://github.com/mitre-attack/attack-navigator)
- [MITRE ATT&CK – Getting Started](https://attack.mitre.org/resources/getting-started/)
- [TryHackMe – MITRE](https://tryhackme.com/room/mitre)
