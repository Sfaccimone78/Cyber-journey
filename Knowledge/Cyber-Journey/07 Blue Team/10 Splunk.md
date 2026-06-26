---
tipo: entita
tag: [blue-team, siem, tool]
fase: 2
fonti: 6
aggiornato: 2026-06-21
stato: maturo
aliases: ["Splunk"]

---

# Splunk

## Cos'è
**Splunk** è la piattaforma SIEM e di analisi dei log più diffusa in ambito enterprise. Raccoglie dati da qualsiasi sorgente (Windows Event Log, firewall, proxy, endpoint), li indicizza e permette di interrogarli con un linguaggio proprietario chiamato **SPL** (Search Processing Language). È lo strumento principale in molti SOC reali e nei percorsi di formazione come [[LetsDefend]] e TryHackMe.

## Uso tipico

```spl
index=windows EventCode=4624 Logon_Type=3
| stats count by src_ip, user
| sort -count
| head 20
```

Questa query SPL cerca tutti i login di rete riusciti (Event ID 4624, tipo 3), li raggruppa per IP sorgente e utente, e mostra i 20 più frequenti. Utile per identificare movimenti laterali o account usati in modo anomalo.

Operatori SPL fondamentali:
- `index=` — seleziona la sorgente dati
- `| stats count by` — raggruppa e conta
- `| where` — filtra i risultati
- `| timechart` — visualizza eventi nel tempo
- `| table` — mostra colonne specifiche

## Quando si usa
- [[Detection di Attacchi]]: scrittura e test di regole di correlazione
- [[Triage degli Alert]]: ricerca contestuale dopo un alert
- [[Log Analysis]]: indagine forense su un periodo di tempo
- [[Incident Response]]: ricostruzione della timeline di un attacco
- [[Analisi Malware di Base]]: ricerca di IOC (hash, IP, dominio) nei log

## Note e trucchi
- La versione **Splunk Free** limita a 500 MB/giorno di ingestione — sufficiente per laboratori.
- **Splunk Enterprise Security (ES)** è il modulo SOC premium con dashboard pre-built e correlation search automatiche.
- Per imparare SPL gratuitamente: [Splunk Free Training](https://www.splunk.com/en_us/training/free-courses/splunk-fundamentals-1.html).
- Abbreviazione utile: `index=* earliest=-1h` filtra l'ultima ora su tutti gli indici.

---

# Approfondimento — SPL da base ad avanzato

## Il modello SPL (come "pensa" Splunk)
Una ricerca è una **pipeline**: ogni `|` passa gli eventi al comando successivo, come in Unix.
```
<search di base>  |  <comando di trasformazione>  |  <comando di formattazione>
index=windows EventCode=4625   |   stats count by Account_Name   |   sort -count
```
- La **prima riga** (`index=`, `sourcetype=`, termini) usa l'indice → è veloce, mettila il più stretta possibile.
- I comandi `|` successivi lavorano sugli eventi già ridotti. **Filtra presto, trasforma dopo**: meno eventi scorrono nella pipe, più la ricerca è rapida.

## I comandi che servono ogni giorno

### `stats` — aggrega (il cavallo di battaglia)
```spl
index=windows EventCode=4625
| stats count, dc(Account_Name) as utenti_distinti, values(Account_Name) as accounts,
        min(_time) as primo, max(_time) as ultimo by Source_Network_Address
| sort -count
```
`count` (quanti), `dc()` (distinct count), `values()`/`list()` (valori unici/tutti), `min/max/avg/sum`. `by` = raggruppa.

### `eval` — crea/trasforma campi
```spl
| eval ora=strftime(_time,"%H"), orario_lavorativo=if(ora>=8 AND ora<=19,"si","no")
| eval rapporto_out=round(bytes_out/bytes_in, 2)
```
Funzioni comuni: `if()`, `case()`, `coalesce()`, `strftime/strptime`, `round()`, `len()`, `like()`, `cidrmatch()`.

### `rex` — estrai campi con regex
Quando il dato non è già un campo (log non strutturati). Estrae con **named group**:
```spl
index=firewall
| rex field=_raw "src=(?<src_ip>\d+\.\d+\.\d+\.\d+).*?dst=(?<dst_ip>\d+\.\d+\.\d+\.\d+):(?<dst_port>\d+)"
| stats sum(bytes) as totale by src_ip, dst_ip, dst_port
```
`rex mode=sed` serve invece a *mascherare* (es. anonimizzare un campo).

### `transaction` — raggruppa eventi correlati in una sessione
Unisce eventi che condividono campi entro una finestra/condizione. **Potente ma costoso** (preferisci `stats` quando puoi):
```spl
index=windows (EventCode=4625 OR EventCode=4624)
| transaction Account_Name Source_Network_Address maxspan=5m maxpause=2m
| eval esito=if(searchmatch("EventCode=4624"),"successo","solo_fail")
| table _time, Account_Name, Source_Network_Address, eventcount, esito
```
Campi generati da `transaction`: `duration`, `eventcount`. Usalo quando ti serve la *sequenza* (fail→success), non solo il conteggio.

### Altri utili
- `timechart span=1h count by EventCode` — serie temporale per grafici.
- `lookup` — arricchisce con tabelle esterne (es. mappa IP→reputazione, asset→owner).
- `bin _time span=1m` — discretizza il tempo (utile nel beaconing).
- `eventstats` / `streamstats` — aggregano *senza collassare* gli eventi (aggiungono colonne di contesto).
- `dedup`, `top`, `rare`, `fillnull`, `where` (post-aggregazione, vs `search` che è pre).

## Costruire una ricerca di detection: bruteforce (N fail poi 1 success)
Obiettivo: trovare un IP con **≥ 10 login falliti seguiti da un successo** entro 5 minuti sullo stesso account.

**Approccio A — con `transaction`** (legge la sequenza):
```spl
index=windows (EventCode=4625 OR EventCode=4624) Logon_Type=3
| transaction Account_Name Source_Network_Address maxspan=5m
| search eventcount>10
| where match(mvjoin(mvfilter(match(EventCode,"4624")),","),"4624")   `c'è almeno un successo`
| table _time, Account_Name, Source_Network_Address, eventcount, duration
```

**Approccio B — con `stats`** (più efficiente su grandi volumi):
```spl
index=windows (EventCode=4625 OR EventCode=4624) Logon_Type=3
| bin _time span=5m
| stats count(eval(EventCode=4625)) as fail, count(eval(EventCode=4624)) as success
        by _time, Account_Name, Source_Network_Address
| where fail >= 10 AND success >= 1
| sort -fail
```
> [!tip] Quando stats batte transaction
> `transaction` è elegante ma costoso e ha limiti di memoria su grandi dataset. Se ti basta *contare* fail e success in una finestra (non serve la sequenza esatta), `stats count(eval(...))` con `bin` è molto più scalabile. Regola: usa `transaction` solo quando l'ordine/raggruppamento per sessione è davvero necessario.

## Dashboard
Una dashboard è un set di pannelli (XML o Dashboard Studio) alimentati da ricerche salvate:
- **Pannelli tipici SOC**: top IP sorgente di 4625 (bar chart), 4624/4625 nel tempo (timechart), mappa geo dei logon esterni, tabella Kerberoasting (4769 RC4), top processi rari (Sysmon 1).
- **Token e input**: dropdown/time-picker passano valori (`$ip$`, `$earliest$`) alle ricerche → dashboard interattiva.
- **Base + post-process search**: una ricerca pesante eseguita una volta, più pannelli che la rifiniscono → risparmi risorse.

## Alert (saved search schedulata)
Un alert è una ricerca salvata che gira a intervalli e **agisce** se la condizione è vera:
1. Scrivi e salva la ricerca di detection (es. il bruteforce sopra).
2. **Schedule**: cron (es. ogni 5 min su finestra `-5m@m`).
3. **Trigger condition**: `Number of Results > 0` (o soglia/throttle per ridurre spam).
4. **Trigger actions**: invia email, crea ticket, webhook a SOAR, scrivi in un indice di notable events.
5. **Throttle**: sopprimi alert duplicati sullo stesso `Account_Name`/`src_ip` per N minuti → evita alert fatigue.

> [!tip] Splunk Enterprise Security
> In ES gli alert diventano **notable events** correlati e arricchiti, con risk-based alerting (RBA): invece di un alert per evento, si accumula un *rischio* per asset/identità e si scatena la notable solo oltre soglia → molto meno rumore.

## Schema dei campi (CIM e campi nativi)
- I nomi dei campi **dipendono dalla sorgente e dal parsing**. `EventCode` (TA Windows) vs `event_id`; `Source_Network_Address` vs `src_ip`. Verifica sempre con `| fieldsummary` o aprendo un evento grezzo.
- Il **CIM** (Common Information Model) normalizza i nomi (`src`, `dest`, `user`, `action`) → le ricerche diventano portabili tra sorgenti diverse (usate dai datamodel/`tstats`).
- `tstats` su datamodel accelerati = ricerche **ordini di grandezza più veloci** su grandi volumi (interroga gli indici tsidx, non gli eventi grezzi).

## Walkthrough — da SPL grezza a alert operativo
1. **Hunt manuale**: scrivo la query bruteforce (approccio B), la giro su `-24h`, trovo un IP con 87 fail + 1 success su `backup_svc`.
2. **Validazione**: pivot — l'IP è esterno, l'account è un service account → True Positive (vedi [[Log Analysis]], [[Detection di Attacchi]]).
3. **Operativizzo**: salvo la ricerca, schedulo ogni 5 min su `-5m@m`, trigger `>0`, throttle 30 min per `src_ip`, azione = email al SOC + crea notable.
4. **Tuning**: dopo una settimana noto FP da un IP di vulnerability scanner → aggiungo `Source_Network_Address!="10.0.99.5"` (allowlist) e documento.

## Casi limite e falsi positivi
- **`bin` ai confini della finestra**: un attacco a cavallo di due bucket può apparire diviso → finestre scorrevoli (`streamstats`) o overlap se serve precisione.
- **Campi mancanti su alcune sorgenti**: `Logon_Type` non esiste in tutti i log → `fillnull` o `coalesce` per non perdere eventi.
- **`transaction` che spezza sessioni lunghe**: `maxspan`/`maxpause` troppo stretti frammentano una sessione reale.
- **Timezone**: eventi in UTC e local mischiati falsano `strftime("%H")` → normalizza a monte.
- **Wildcard iniziale costosa**: `CommandLine="*enc*"` forza scansione completa; ancora i termini quando puoi.

## Troubleshooting — 5 errori da analista junior
1. **`where` vs `search`** confusi → `search` filtra (pre, usa l'indice), `where` valuta espressioni su campi (post-stats). Usare `where field="x"` su stringhe semplici è più lento e sintatticamente diverso. Causa: non conoscere quando agisce ciascuno.
2. **Wildcard a inizio termine** (`*powershell`) → full scan lentissimo. Causa: non sapere che Splunk indicizza per token.
3. **`transaction` su milioni di eventi** → ricerca che va in timeout/memoria. Causa: usarlo dove bastava `stats`.
4. **Filtrare tardi** (`index=*` poi `| search EventCode=4625`) → spazza tutti gli indici inutilmente. Causa: non mettere i filtri nella prima riga.
5. **Nomi campo sbagliati** (`EventID` invece di `EventCode`, `user` invece di `Account_Name`) → zero risultati e si pensa "nessun attacco". Causa: non verificare lo schema con un evento grezzo.

## Domande da colloquio SOC
> [!question] Differenza tra `stats` e `eventstats`?
> `stats` **collassa** gli eventi nei gruppi aggregati (perdi i singoli). `eventstats` calcola la stessa aggregazione ma la **riattacca come colonna** a ogni evento originale, senza collassare → utile per confrontare un evento con la media del suo gruppo (anomaly detection).

> [!question] Quando useresti `transaction` invece di `stats`?
> Solo quando mi serve la **sequenza/sessione** (es. fail→success, o eventi di un'unica connessione raggruppati per ordine e durata). Per semplici conteggi in finestra preferisco `stats count(eval(...))` con `bin`, perché `transaction` è costoso e ha limiti di memoria.

> [!question] Come scriveresti una detection di bruteforce in SPL?
> Conto i 4625 e i 4624 in finestre di 5 minuti raggruppati per account e IP (`bin _time span=5m` + `stats count(eval(EventCode=4625)) as fail, count(eval(EventCode=4624)) as success`), poi `where fail>=10 AND success>=1`. La salvo come alert schedulato con throttling. La logica è "N fallimenti poi un successo dallo stesso IP".

> [!question] Cos'è il CIM e perché conta?
> Il **Common Information Model** normalizza i nomi dei campi tra sorgenti diverse (`src`, `dest`, `user`, `action`). Così una ricerca/detection scritta sui campi CIM funziona su firewall, proxy ed endpoint senza riscriverla per ogni sourcetype, e abilita `tstats` accelerato sui datamodel.

## Collegamenti
- [[SIEM]]
- [[Log Analysis]]
- [[Detection di Attacchi]]
- [[Triage degli Alert]]
- [[Incident Response]]
- [[Windows Event Log]]
- [[Sysmon]] — sorgente endpoint per le ricerche
- [[MITRE ATT&CK]] — mappare le detection alle tecniche
- [[LetsDefend]]
- Attacchi rilevabili in SPL: [[Pass-the-Hash]] · [[Kerberoasting]] · [[Hydra]]

## Fonti
- [Splunk Docs – SPL Reference](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/WhatsInThisManual)
- [Splunk Docs – stats / eval / rex / transaction](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Stats)
- [Splunk Docs – Common Information Model (CIM)](https://docs.splunk.com/Documentation/CIM/latest/User/Overview)
- [Splunk Security Content (detections)](https://research.splunk.com/)
- [TryHackMe – Splunk: Basics](https://tryhackme.com/room/splunk101)
- [Splunk – Free Training Fundamentals 1](https://www.splunk.com/en_us/training/free-courses/splunk-fundamentals-1.html)
