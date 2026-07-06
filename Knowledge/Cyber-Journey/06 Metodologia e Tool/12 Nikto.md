---
tipo: entita
tag: [tool]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Nikto"]

---

# Nikto

## In breve

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

## Lab

- **[[TryHackMe]] — "Nikto" e le room web del Jr Penetration Tester path**: fanno lanciare Nikto contro un server di test e interpretare i finding (file di default, header mancanti, software obsoleto).
- **[[HackTheBox]] — Starting Point con web server (es. *Markup*, *Included*)**: usa `nikto -h http://<ip>` come prima passata automatica per individuare i "frutti bassi" prima dell'analisi manuale.
- **[[PortSwigger Web Academy]] — categoria *Information disclosure*** (lab APPRENTICE): dopo che Nikto segnala header/file sospetti, verifica manualmente il finding con `curl` o nel browser, esercitando la conferma dei falsi positivi.

## Domande

1. **D:** Che tipo di problemi cerca Nikto su un server web?  **R:** Configurazioni errate, file pericolosi/di default, software obsoleto, header HTTP mancanti e oltre 6700 vulnerabilità note.
2. **D:** Perché Nikto non è adatto quando serve stealth?  **R:** Perché genera migliaia di richieste HTTP in pochi minuti, facilmente rilevabili nei log del server.
3. **D:** Perché i finding di Nikto vanno sempre verificati manualmente?  **R:** Perché produce molti falsi positivi; ogni risultato va confermato nel browser o con `curl`.
4. **D:** A cosa serve l'opzione `-Tuning`?  **R:** A selezionare le categorie di test da eseguire (es. injection, misconfiguration, information disclosure) invece di lanciarle tutte.
5. **D:** Come si fa passare il traffico di Nikto attraverso Burp Suite?  **R:** Con `-useproxy http://127.0.0.1:8080`, indirizzando le richieste al proxy in ascolto.

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
