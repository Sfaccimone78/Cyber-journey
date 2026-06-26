---
tipo: entita
tag: [tool]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Nikto"]

---

# Nikto

## Cos'è

**Nikto** è uno scanner open source per server web. Analizza automaticamente un sito alla ricerca di configurazioni errate, file pericolosi, versioni obsolete di software, header HTTP mancanti e oltre 6700 vulnerabilità note. È uno strumento "noisy" — non cerca di essere silenzioso — ma è estremamente rapido per avere un quadro iniziale della sicurezza di un'applicazione web. Si usa nella fase di [[Enumerazione]].

> **Nota etica**: Nikto genera un numero elevato di richieste HTTP facilmente rilevabili nei log. Va usato ESCLUSIVAMENTE su applicazioni web di propria proprietà o per cui si ha autorizzazione scritta.

## Uso tipico

```bash
# Scansione base di un host sulla porta 80
nikto -h http://target.lab

# Scansione su HTTPS / porta personalizzata
nikto -h https://target.lab -p 443

# Scansione specificando solo IP e porta (Nikto aggiunge il percorso)
nikto -h 192.168.1.10 -p 8080

# Aggiungere autenticazione HTTP Basic
nikto -h http://target.lab -id admin:password

# Usare un proxy (es. Burp Suite per intercettare il traffico)
nikto -h http://target.lab -useproxy http://127.0.0.1:8080

# Salvare l'output in formato HTML
nikto -h http://target.lab -o report_nikto.html -Format html

# Salvare l'output in CSV per analisi successive
nikto -h http://target.lab -o report_nikto.csv -Format csv

# Limitare la scansione a specifici tipi di test (plugin)
nikto -h http://target.lab -Plugins "headers,cookies"

# Aggiornare il database delle vulnerabilità di Nikto
nikto -update
```

**Opzioni chiave:**

| Flag | Significato |
|---|---|
| `-h` | Host target (URL o IP) |
| `-p` | Porta (default: 80) |
| `-ssl` | Forza HTTPS |
| `-o` | File di output |
| `-Format` | Formato output: html, csv, txt, xml |
| `-id` | Credenziali HTTP Basic (`user:pass`) |
| `-useproxy` | Usa un proxy HTTP |
| `-Tuning` | Seleziona categorie di test (0-9) |

**Categorie di test (`-Tuning`):**

| Numero | Categoria |
|---|---|
| 0 | File upload |
| 1 | Interessante / sospetto |
| 2 | Misconfiguration / default file |
| 3 | Information disclosure |
| 4 | Injection (XSS/Script) |
| 6 | Denial of Service |
| 8 | Command injection |
| 9 | SQL Injection |

## Quando si usa

- Fase di [[Enumerazione]]: prima analisi automatica del server web per trovare "frutti bassi" (file di default, directory di test, header mancanti).
- Prima di un test manuale approfondito: Nikto dà un elenco iniziale di problemi da investigare.
- Verifica di configurazione: header di sicurezza mancanti (X-Frame-Options, Content-Security-Policy, HSTS).

## Note e trucchi

- Nikto è **molto rumoroso**: migliaia di richieste in pochi minuti. Non usarlo se l'obiettivo è la stealth.
- Non trova tutto: Nikto non sostituisce un test manuale o tool come [[ffuf]] e [[Gobuster]] per la discovery di contenuti.
- I risultati vanno **verificati manualmente**: molti sono falsi positivi. Ogni finding va confermato nel browser o con `curl`.
- Per aggiungere l'output di Nikto a [[Metasploit]]: Nikto supporta output XML che può essere importato.

## Collegamenti

- [[Enumerazione]]
- [[Gobuster]]
- [[ffuf]]
- [[HTTP e HTTPS]]
- [[OWASP Top 10]]
- [[Kali Linux]]

## Fonti

- Nikto — GitHub ufficiale: <https://github.com/sullo/nikto>
- Nikto documentazione: <https://cirt.net/Nikto2>
- HackTricks — Web Scanning: <https://book.hacktricks.xyz/network-services-pentesting/pentesting-web>
