---
tipo: concetto
tag: [blue-team]
fase: 2
fonti: 7
aggiornato: 2026-06-21
stato: maturo
aliases: ["Detection di Attacchi"]

---

# Detection di Attacchi

## In breve
La **detection di attacchi** è il processo con cui il team di difesa identifica attività malevole in corso su sistemi e reti, prima o durante il danno. Si basa su regole, correlazioni, anomalie comportamentali e feed di [[Threat Intelligence]], tipicamente orchestrati da un [[SIEM]].

## Come funziona
Esistono due approcci principali:

1. **Signature-based**: si cercano pattern noti (hash di malware, regole Sigma/Yara, ID evento specifici). Veloce ma cieco contro attacchi nuovi (0-day).
2. **Behavior-based**: si cercano comportamenti anomali — un utente che accede a 500 file in 10 secondi, o un processo `cmd.exe` figlio di `word.exe`. Più lento da configurare ma rileva minacce sconosciute.

Il framework [[MITRE ATT&CK]] cataloga le **TTP** (Tattiche, Tecniche, Procedure) degli attaccanti: ogni tecnica ha un ID (es. T1059 = Command and Scripting Interpreter) e suggerisce quali log e regole di detection implementare. Il [[MITRE ATT&CK Navigator]] visualizza la copertura della detection.

## Esempio pratico
Regola di detection per **PowerShell codificato** (tecnica T1059.001), tipico nei malware che scaricano payload:

```spl
index=windows EventCode=4688 New_Process_Name="*powershell*"
(CommandLine="* -enc *" OR CommandLine="* -EncodedCommand *")
| table _time, host, user, CommandLine
```

Se la query restituisce risultati, si passa al [[Triage degli Alert]] per valutare se è un falso positivo o un attacco reale.

## Rilevanza per la sicurezza
Senza detection, gli attaccanti possono restare nella rete per mesi non rilevati (dwell time medio: ~200 giorni). Una buona detection riduce il tempo di risposta e limita il danno. È il cuore del lavoro dell'analista SOC in [[LetsDefend]] e piattaforme simili.

---

# Approfondimento — Detection Engineering

## Dall'attacco alla regola (il processo)
La detection engineering non è "scrivere query a caso": è un ciclo disciplinato.
1. **Comprendi la tecnica** — studia l'attacco offensivo e la sua firma (es. [[Kerberoasting]] → richiesta TGS con etype RC4).
2. **Identifica la telemetria** — quale log/Event ID rende osservabile la tecnica? ([[MITRE ATT&CK]] elenca i *data source* per ogni T-id).
3. **Definisci la logica** — cosa distingue il malevolo dal benigno (soglia, parent-child, raro vs comune).
4. **Scrivi la regola** — in [[Regole Sigma|Sigma]] (portabile) o nativa SIEM ([[Splunk]] SPL / KQL).
5. **Testa** — emula con Atomic Red Team/purple team, verifica che scatti (true positive) e misura i falsi positivi.
6. **Tuning** — aggiungi allowlist, alza/abbassa soglie, riduci rumore. Una regola non tunata = alert fatigue.
7. **Documenta** — runbook: cosa fare quando scatta (link al [[Triage degli Alert]]).

> [!tip] Sigma come lingua franca
> Una [[Regole Sigma|regola Sigma]] (YAML) si scrive una volta e si converte (`sigma convert`) verso Splunk, Elastic, Sentinel, ecc. Disaccoppia la *logica di detection* dal *SIEM specifico*.

## Detection per attacco — Event ID + query concreta
Per ogni attacco: la tecnica MITRE, l'attacco offensivo correlato, la telemetria e una query pronta.

### 1. Bruteforce / Password Spraying — T1110
**Offensivo:** [[Hydra]], CrackMapExec. **Telemetria:** Windows Security 4625 (fail) e 4624 (success).
Logica: **≥ N fallimenti poi un successo** dallo stesso IP/account in una finestra breve.
```spl
index=windows (EventCode=4625 OR EventCode=4624)
| transaction Account_Name Source_Network_Address maxspan=5m
| where eventcount>10 AND mvcount(eventcode)>1 AND mvfind(EventCode,"4624")>=0
| table _time, Account_Name, Source_Network_Address, eventcount
```
Variante spraying (1 password × molti account): `stats dc(Account_Name) as accounts by Source_Network_Address | where accounts > 15`.

### 2. Kerberoasting — T1558.003
**Offensivo:** [[Kerberoasting]], [[Impacket]] (`GetUserSPNs`). **Telemetria:** DC Security **4769** (Kerberos Service Ticket Request).
Logica: un singolo account che chiede **molti** TGS con **etype 0x17 (RC4)** in poco tempo.
```spl
index=windows EventCode=4769 Ticket_Encryption_Type=0x17 Ticket_Options=0x40810000
Service_Name!="krbtgt" Service_Name!="*$"
| stats dc(Service_Name) as services, values(Service_Name) by Account_Name, _time
| where services > 5
```
> RC4 (0x17) è la firma: gli attaccanti lo forzano perché il TGS si cracca come NT hash. Account che richiede TGS per 10 SPN diversi in 30s = quasi certo Kerberoasting. Collega a [[Kerberos]].

### 3. Pass-the-Hash — T1550.002
**Offensivo:** [[Pass-the-Hash]], [[Mimikatz]], CrackMapExec. **Telemetria:** 4624 **Logon Type 3** + **NTLM** + 4672.
Logica: logon di rete NTLM con account privilegiato che dovrebbe usare Kerberos, spesso da workstation a workstation.
```spl
index=windows EventCode=4624 Logon_Type=3 Authentication_Package=NTLM
| search Account_Name="*admin*" OR Account_Name="svc_*"
| stats count by Account_Name, Workstation_Name, Source_Network_Address
| where count > 0
```
KQL (Microsoft Sentinel / Defender):
```kql
SecurityEvent
| where EventID == 4624 and LogonType == 3 and AuthenticationPackageName == "NTLM"
| where Account has_any ("admin","svc_")
| summarize count() by Account, WorkstationName, IpAddress
```

### 4. Web shell — T1505.003
**Offensivo:** [[Vulnerabilita Upload File]], [[Command Injection]]. **Telemetria:** web access log + [[Sysmon]] Event ID 1 (process create).
Logica: il processo del web server (`w3wp.exe`, `httpd`, `nginx`) genera **figli da shell** (`cmd.exe`, `powershell`, `whoami`, `/bin/sh`).
```spl
index=sysmon EventCode=1 ParentImage IN ("*w3wp.exe","*httpd.exe","*nginx.exe","*php-cgi.exe")
Image IN ("*cmd.exe","*powershell.exe","*whoami.exe","*net.exe","*/bin/sh","*/bin/bash")
| table _time, host, ParentImage, Image, CommandLine, User
```

### 5. C2 Beacon — T1071
**Offensivo:** Cobalt Strike, Sliver (vedi [[Reverse Shell e Bind Shell]]). **Telemetria:** proxy/firewall/DNS.
Logica: connessioni **periodiche** verso lo stesso dst, payload piccoli e regolari, basso jitter.
```spl
index=proxy
| bin _time span=1m
| stats count, avg(bytes_out) as avgout, stdev(bytes_out) as sdout by src_ip, dest_host, _time
| eventstats avg(count) as beat, stdev(count) as jitter by src_ip, dest_host
| where jitter < 1 AND avgout < 2000 AND beat > 20    `low jitter + many beats = beacon`
```

## Detection-as-code e copertura
- Versiona le regole in **Git** (review, rollback, CI che valida la sintassi Sigma).
- Misura la copertura sul [[MITRE ATT&CK Navigator]]: ogni regola → una o più tecniche colorate. Le tecniche **scoperte** (rosse) sono i tuoi punti ciechi.
- **Detection maturity**: da IOC atomici (hash/IP, fragili) a TTP comportamentali (parent-child, sequenze) — la "Pyramid of Pain" di Bianco: più sali, più costa all'attaccante eludere.

## Walkthrough — dall'alert grezzo al verdetto
Scatta la regola Kerberoasting (#2): account `svc_sql` chiede 12 TGS RC4 in 20 secondi.
1. **È benigno?** `svc_sql` accede normalmente a pochi SPN. 12 SPN diversi in 20s **non** è il suo pattern → sospetto.
2. **Da dove parte?** Pivot sull'host sorgente del 4769 → workstation di un utente non-DBA. Anomalia.
3. **Cosa l'ha generato?** Su quell'host: [[Sysmon]] Event ID 1 mostra `powershell.exe` con stringa Base64 → script Rubeus/Invoke-Kerberoast.
4. **Esito offline?** L'attaccante craccherà i TGS offline → cerco accessi successivi con quegli account di servizio.
5. **Verdetto:** True Positive — Credential Access (T1558.003). Reset password dei service account esposti, escalation [[Incident Response]], hunt per movimento laterale.

## Casi limite e falsi positivi
- **Vulnerability scanner autenticati** (Nessus, Qualys) generano ondate di 4624/4625/4769 legittime → allowlist degli IP scanner.
- **App legacy che usano NTLM** fanno scattare le regole PtH → servono baseline per account/host che usano NTLM *legittimamente*.
- **SPN reali e numerosi**: alcuni servizi (SQL clustering) richiedono molti TGS → la soglia va calibrata sull'ambiente, non copiata.
- **Admin che usano PsExec legittimamente** per amministrazione → contesto: orario, account, host gestiti vs non gestiti.
- **RC4 ancora in uso legittimo**: in domini non irrigiditi RC4 è comune → la firma "RC4" da sola non basta, serve il *volume per account*.

## Troubleshooting — 5 errori da analista junior
1. **Scrivere una regola IOC-only (hash/IP)** che diventa inutile appena l'attaccante cambia infrastruttura. Causa: stare in fondo alla Pyramid of Pain invece di rilevare il *comportamento*.
2. **Soglia copiata da un blog senza tuning** → 500 alert/giorno e alert fatigue. Causa: nessuna baseline dell'ambiente.
3. **Regola che non scatta mai e si crede "coperto"** → la telemetria non era abilitata (es. audit 4769 o ScriptBlock Logging off). Causa: detection senza verifica della data source.
4. **Detection senza runbook** → l'analista che riceve l'alert non sa cosa fare. Causa: confondere "scrivere la regola" con "operativizzarla".
5. **Confondere `EventCode` con `Logon_Type`/`etype`** nelle query → la regola filtra il campo sbagliato e non matcha nulla. Causa: non conoscere lo schema dei campi.

## Domande da colloquio SOC
> [!question] Differenza tra detection signature-based e behavior-based?
> Signature cerca pattern *noti* (hash, regola Sigma, ID evento): veloce e preciso ma cieco sugli 0-day. Behavior cerca *anomalie* (parent-child inusuale, volumetria): rileva l'ignoto ma è più rumoroso e va tunato. In pratica si usano insieme, a strati.

> [!question] Come rileveresti il Kerberoasting?
> Monitoro Event ID **4769** sul DC: cerco un singolo account che richiede molti **TGS con etype 0x17 (RC4)** in poco tempo, escludendo `krbtgt` e account macchina. RC4 è la firma perché rende il TGS craccabile offline. Tuning sulla soglia di SPN distinti per account.

> [!question] Cos'è la "Pyramid of Pain" e perché conta nel detection engineering?
> Classifica gli indicatori per quanto *costa* all'attaccante cambiarli: hash/IP/domini (facili da cambiare, in basso) → artefatti di rete/host → strumenti → **TTP** (in cima, costosissimi da cambiare). Rilevare le TTP infligge più "dolore" e dura nel tempo; rilevare solo hash è fragile.

> [!question] Una regola genera 300 alert al giorno, tutti falsi positivi. Cosa fai?
> Non la disattivo a caso. Analizzo i FP per trovare il denominatore comune (un IP scanner, un service account, un'app legacy), aggiungo una **allowlist mirata** o alzo la soglia, e ritesto che continui a rilevare il vero positivo. Documento il tuning. L'obiettivo è alto signal-to-noise, non zero alert.

## Collegamenti
- [[SIEM]]
- [[Splunk]]
- [[MITRE ATT&CK]]
- [[MITRE ATT&CK Navigator]]
- [[Regole Sigma]] — detection-as-code portabile
- [[Sysmon]] — data source per detection endpoint
- [[Triage degli Alert]]
- [[Threat Intelligence]]
- [[Indicatori di Compromissione (IOC)]]
- [[Log Analysis]]
- [[Windows Event Log]]
- [[LetsDefend]]
- Attacchi correlati: [[Kerberoasting]] · [[Pass-the-Hash]] · [[Hydra]] · [[Vulnerabilita Upload File]] · [[Reverse Shell e Bind Shell]]

## Fonti
- [MITRE ATT&CK – Techniques](https://attack.mitre.org/techniques/enterprise/)
- [Splunk – Security Detection with SPL](https://www.splunk.com/en_us/blog/security/security-detection-using-spl.html)
- [SigmaHQ – Detection rules repository](https://github.com/SigmaHQ/sigma)
- [David Bianco – The Pyramid of Pain](https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html)
- [Red Canary – Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)
- [MITRE – CAR (Cyber Analytics Repository)](https://car.mitre.org/)
- [TryHackMe – SOC Level 1](https://tryhackme.com/path/outline/soclevel1)
