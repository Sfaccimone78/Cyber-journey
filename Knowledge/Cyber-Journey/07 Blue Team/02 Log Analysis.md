---
tipo: concetto
tag: [blue-team]
fase: 2
fonti: 7
aggiornato: 2026-06-21
stato: maturo
aliases: ["Log Analysis"]

---

# Log Analysis

## In breve
La **Log Analysis** è il processo di esaminare i file di log generati da sistemi operativi, applicazioni e dispositivi di rete per identificare anomalie, errori o attività malevole. È la base di ogni indagine di sicurezza.

## Come funziona
I log registrano ogni evento rilevante con **timestamp**, **sorgente**, **ID evento** e **messaggio**. L'analista segue questi passaggi:

1. **Raccolta**: i log vengono centralizzati in un [[SIEM]] o in un log aggregator.
2. **Filtro**: si isolano eventi per intervallo di tempo, host, utente o ID specifico.
3. **Correlazione**: si mettono in relazione eventi su sistemi diversi (es. firewall + Active Directory).
4. **Interpretazione**: si distingue tra attività normale (**baseline**) e anomalia.

### ID evento Windows più importanti
| ID | Significato |
|----|------------|
| 4624 | Login riuscito |
| 4625 | Login fallito |
| 4648 | Login con credenziali esplicite |
| 4672 | Privilegi amministrativi assegnati |
| 4688 | Nuovo processo creato |

## Esempio pratico
Scenario: un alert segnala accesso sospetto alle 3:00 di notte. L'analista filtra su [[Splunk]]:

```spl
index=windows EventCode=4624 earliest=-1d
| where strftime(_time, "%H") == "03"
| table _time, src_ip, user, dest
```

Se l'utente non lavora mai di notte, è un segnale da escalare nel [[Triage degli Alert]].

## Rilevanza per la sicurezza
Senza log analysis non esistono [[Incident Response]], [[Detection di Attacchi]] né [[Analisi Malware di Base]]. I log sono la prova digitale: il loro grado di completezza e conservazione determina quanto si può ricostruire di un attacco.

---

# Approfondimento — livello SOC Analyst

## Le sorgenti di log (cosa logga cosa)
Un analista deve sapere **da quale telemetria** può estrarre un dato segnale. Le sorgenti non sono intercambiabili: ognuna vede un pezzo della kill chain.

| Sorgente | Cosa registra | Punti di forza | Limiti |
|---|---|---|---|
| **[[Windows Event Log]]** (Security) | logon, gestione account, accessi a oggetti, uso privilegi | nativo, ricco di Event ID standard | rumoroso, audit policy spesso incompleta di default |
| **[[Sysmon]]** | process creation con hash+parent, network connect, file/registry, named pipe, DNS, image load | granularità da EDR ma gratuito; la migliore telemetria endpoint per detection | va installato e configurato (config tipo SwiftOnSecurity) |
| **Firewall / NGFW** | connessioni 5-tuple (src/dst IP, porte, proto), allow/deny, bytes | vede tutto il traffico nord-sud | nessuna visibilità sul *processo* che genera la connessione |
| **Proxy / Web filter** | URL/dominio richiesti, user-agent, categoria, verdetto | ottimo per C2 su HTTP/S e download payload | HTTPS spesso solo SNI/dominio senza decrypt |
| **Web server** (IIS/Apache/Nginx access log) | metodo, path, status, user-agent, referrer, bytes | indispensabile per attacchi applicativi e web shell | non vede traffico cifrato a monte del TLS termination |
| **[[EDR e XDR\|EDR]]** | telemetria endpoint correlata + verdetti comportamentali | correla processo↔rete↔file, fa detection nativa | costoso, può mancare contesto di rete pura |
| **DNS** | query e risposte | scopre C2/DGA/exfil via DNS e tunneling | volume enorme, va filtrato |
| **Autenticazione cloud/IdP** (Azure AD/Okta) | sign-in, MFA, app consent | copre identity-based attacks | formato proprietario, fuso orario UTC |

> [!tip] Regola pratica
> **Endpoint + rete + identità**: una buona detection nasce dalla correlazione di almeno due di questi tre assi. Il firewall ti dice *che* una connessione è partita; [[Sysmon]] (Event ID 3) ti dice *quale processo* l'ha aperta.

## Normale vs anomalo (come si costruisce la baseline)
"Anomalo" non esiste in assoluto: esiste solo **rispetto alla baseline** dell'ambiente. L'analista valuta su questi assi:
- **Temporale** — l'evento è in orario lavorativo? Picco fuori orario = sospetto (vedi esempio 4624 di notte).
- **Volumetrico** — quante volte in quanto tempo? 1 login fallito = errore di battitura; 200 in 1 minuto = bruteforce.
- **Relazionale (parent-child)** — `cmd.exe` figlio di `explorer.exe` è normale; figlio di `winword.exe` o `w3wp.exe` è una bandiera rossa.
- **Direzionale / geografico** — login da un paese in cui l'azienda non opera; connessione in uscita verso un IP mai visto.
- **Rarità** — un binario con hash mai osservato nell'ambiente, un user-agent unico, un nome processo che gira da un path strano (`%TEMP%`, `C:\Users\Public`).

## Riconoscere gli attacchi nei log — esempi reali commentati

### Bruteforce / Password Spraying (T1110)
Windows Security, ripetuti **4625** (logon fallito) con stesso target e `Status: 0xC000006A` (password errata):
```
EventID 4625  Account Name: administrator  Source Network Address: 45.83.x.x
  Failure Reason: %%2313 (Bad password)  Sub Status: 0xC000006A   Logon Type: 3
EventID 4625  Account Name: administrator  Source Network Address: 45.83.x.x  ... (x120 in 2 min)
EventID 4624  Account Name: administrator  Source Network Address: 45.83.x.x   Logon Type: 3  ← il successo!
```
> Pattern chiave: **N fallimenti → 1 successo** dallo stesso IP = bruteforce riuscito. Se invece un IP prova *1 password su 200 account diversi* è **password spraying** (T1110.003), che evade i lockout. Vedi [[Hydra]] come tool offensivo tipico.

Sub-status 4625 utili da riconoscere:
- `0xC000006A` = password errata · `0xC0000064` = utente inesistente · `0xC0000234` = account locked · `0xC0000072` = account disabilitato.

### Lateral Movement (T1021)
Login di rete (**Logon Type 3**) da una **workstation verso un'altra workstation** (anomalo: di solito le WS parlano coi server, non tra loro), spesso seguiti da creazione di servizio o task remoto:
```
EventID 4624  Logon Type: 3  Account: svc_admin  Workstation: WS-FINANCE-07  → host WS-HR-12
EventID 4672  Special privileges assigned   (admin sull'host di destinazione)
EventID 7045  A service was installed  Service Name: "PSEXESVC"  ← PsExec!
EventID 5145  Network share accessed: \\WS-HR-12\ADMIN$
```
> `PSEXESVC`, accesso ad `ADMIN$`/`C$`, e [[Pass-the-Hash]] (Logon Type 3 + NTLM senza pre-auth Kerberos) sono firme classiche. Con [[Sysmon]] aggiungi Event ID 1 (`psexesvc.exe`) ed Event ID 3 sulla porta 445.

### Exfiltration (T1041 / T1048)
Firewall/proxy: grosso volume **in uscita** verso un host esterno, spesso fuori orario:
```
firewall  action=allow  src=10.0.4.55  dst=185.x.x.x:443  proto=tcp  sent_bytes=2147483648  rcvd_bytes=4096
```
> 2 GB inviati e 4 KB ricevuti = **upload asimmetrico** = esfiltrazione (non è normale navigazione, che è download-pesante). Su DNS, query lunghe e ad alto volume verso un solo dominio = **DNS tunneling** (T1048.003): `aGVsbG8gd29ybGQ.exfil.attacker.com`.

### C2 Beacon (T1071 / T1071.004)
Proxy/firewall: connessioni **regolari e periodiche** (beaconing) verso lo stesso dst, payload piccoli, jitter basso:
```
12:00:03  src=10.0.4.55  dst=evil-cdn[.]com  GET /api/v1/poll  ua="Mozilla/5.0"  bytes=312
12:01:04  src=10.0.4.55  dst=evil-cdn[.]com  GET /api/v1/poll  ua="Mozilla/5.0"  bytes=312
12:02:02  src=10.0.4.55  dst=evil-cdn[.]com  GET /api/v1/poll  ua="Mozilla/5.0"  bytes=287
```
> La **periodicità quasi-costante** (~60s) con byte simili = beacon (Cobalt Strike, Sliver). Un umano non naviga a intervalli regolari. Cerca anche user-agent rari, domini giovani, JA3 anomalo.

### Web shell (T1505.003)
Access log del web server: POST ripetuti allo **stesso file** scrivibile (spesso in upload dir), con parametri che cambiano:
```
185.x.x.x  POST /uploads/shell.aspx?cmd=whoami        200  142
185.x.x.x  POST /uploads/shell.aspx?cmd=ipconfig      200  531
185.x.x.x  POST /images/logo.jpg.php?c=dir            200  892
```
> Un file con doppia estensione (`.jpg.php`), POST a un path di upload, e processi figli anomali del web server (`w3wp.exe` o `httpd` → `cmd.exe`/`whoami`) confermano la shell. Vedi [[Vulnerabilita Upload File]].

## Walkthrough — da alert grezzo a verdetto
Alert SIEM: *"Multiple failed logons followed by success — host SRV-APP-02"*.
1. **Triage iniziale** — apro l'alert: 87× 4625 poi 1× 4624 sull'account `backup_svc`, tutti Logon Type 3 dallo stesso IP `45.83.x.x` in 4 minuti.
2. **Contesto IP** — `45.83.x.x` è esterno, geo = paese non aziendale, reputazione bassa su [[VirusTotal]]/threat intel → IOC.
3. **L'account** — `backup_svc` è un service account: **non dovrebbe mai** fare logon interattivo/di rete da Internet. Anomalia forte.
4. **Cosa è successo dopo il 4624?** Pivot sull'host: cerco 4672 (privilegi), 4688/Sysmon-1 (processi), 7045 (servizi) nei 10 minuti successivi → trovo `cmd.exe` e una connessione in uscita (Sysmon-3).
5. **Verdetto** — bruteforce riuscito (T1110) seguito da esecuzione comandi → **True Positive, incidente**. Mappo su [[MITRE ATT&CK]], apro caso [[Incident Response]], isolo l'host, escalation a L2.

## Casi limite e falsi positivi
- **4625 di massa benigni**: una password scaduta di un service account o un'app con credenziali cachate genera centinaia di fallimenti — *senza* mai un successo da IP esterno. Controlla la *sorgente*: interna e ricorrente = misconfig, non attacco.
- **Logon Type 3 normalissimi**: file share, GPO, scansioni di vulnerabilità autenticate. Il tipo 3 da solo non è un alert.
- **Beacon-like legittimo**: telemetria di antivirus, agent di monitoring, NTP, software update check — sono periodici per design. Allowlist note.
- **Upload asimmetrici legittimi**: backup verso cloud, sync OneDrive/Dropbox. Distingui per destinazione (dominio noto) e per processo.
- **Doppio fuso orario**: i log Windows sono local time, molti log cloud/Linux sono **UTC**. Correlare senza normalizzare il timezone = timeline sbagliata.

## Troubleshooting — 5 errori da analista junior
1. **Guardare solo i log fallimentari (4625) e non il 4624 successivo** → si perde il *successo* del bruteforce. Causa: tunnel-vision sull'alert.
2. **Ignorare il fuso orario** → eventi correlati appaiono "scollegati" di ore. Causa: log in UTC vs local non normalizzati.
3. **Fidarsi del `Workstation Name` come fosse autentico** → è un campo *fornito dal client*, falsificabile. Causa: non sapere quali campi sono attestati vs auto-dichiarati.
4. **Concludere "nessun log = nessun attacco"** → spesso l'audit policy non logga l'evento (es. 4688 disattivato di default). Causa: confondere assenza di prova con prova di assenza.
5. **Analizzare un host senza sapere la sua baseline** (è un DC? un web server? una WS?) → si classifica come anomalo ciò che per quel ruolo è normale. Causa: mancanza di asset context.

## Domande da colloquio SOC
> [!question] Differenza tra Logon Type 2, 3 e 10?
> **2** = interactive (tastiera locale); **3** = network (SMB, share, login remoto autenticato in rete); **10** = RemoteInteractive ([[RDP]]). In un'indagine di lateral movement cerchi soprattutto **3** (Pass-the-Hash, PsExec) e **10** (RDP).

> [!question] Hai 200 Event ID 4625 in un minuto. È sempre un attacco?
> No. Devo guardare la **sorgente** (IP interno ricorrente = probabile service account con password scaduta/app mal configurata) e se c'è un **4624 di successo** dallo stesso IP esterno. Bruteforce reale = fallimenti da IP esterno + un successo. Senza successo e da IP interno = quasi sempre misconfig.

> [!question] Come distingui un C2 beacon dal traffico legittimo?
> Cerco **periodicità** delle connessioni (intervallo quasi costante, jitter basso), **payload di dimensione simile e piccola**, destinazioni a bassa reputazione/dominio giovane, user-agent o JA3 raro. Il traffico umano è irregolare e download-pesante; il beacon è metronomico e bilanciato/upload-leggero.

> [!question] Quali tre assi di telemetria correli e perché?
> **Endpoint** ([[Sysmon]]/EDR: chi ha eseguito cosa), **rete** (firewall/proxy: dove è andato il traffico), **identità** (logon/IdP: chi era). La detection forte nasce dall'incrocio: il firewall vede la connessione, Sysmon vede il processo che l'ha aperta, il log di identità vede l'account compromesso.

## Collegamenti
- [[SIEM]]
- [[Splunk]]
- [[Sysmon]] — telemetria endpoint per detection
- [[Windows Event Log]]
- [[Triage degli Alert]]
- [[Incident Response]]
- [[Detection di Attacchi]]
- [[MITRE ATT&CK]]
- [[Pass-the-Hash]] · [[Hydra]] · [[Vulnerabilita Upload File]] — attacchi visibili nei log

## Fonti
- [Microsoft – Windows Security Event IDs](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/security-auditing-overview)
- [Microsoft – Logon Types (4624)](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624)
- [Splunk Docs – Search Tutorial](https://docs.splunk.com/Documentation/Splunk/latest/SearchTutorial/WelcometotheSearchTutorial)
- [SANS – Windows Logging Cheat Sheet](https://www.sans.org/posters/windows-log-cheat-sheet/)
- [SwiftOnSecurity – Sysmon config](https://github.com/SwiftOnSecurity/sysmon-config)
- [The DFIR Report – esempi reali di intrusioni nei log](https://thedfirreport.com/)
- [Active Countermeasures – Beacon analysis](https://www.activecountermeasures.com/the-beacon-blog/)
