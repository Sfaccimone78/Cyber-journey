---
tipo: entita
tag: [tool]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["ffuf"]

---

# ffuf

## Cos'è

**ffuf** (Fuzz Faster U Fool) è un web fuzzer scritto in Go, molto veloce e flessibile. A differenza di [[Gobuster]], ffuf permette di posizionare la parola da testare *ovunque* nell'URL, negli header o nel body della richiesta usando il placeholder `FUZZ`. Eccelle nel fuzzing di parametri, valori di cookie, header HTTP e sottodomini, oltre alla classica enumerazione di directory.

> **Nota etica**: ffuf va usato solo su applicazioni web di cui si ha autorizzazione esplicita. L'uso non autorizzato è illegale e visibile nei log.

## Uso tipico

```bash
# Directory busting base — FUZZ nel path
ffuf -u http://target.lab/FUZZ -w /usr/share/wordlists/dirb/common.txt

# Ricerca file con estensioni specifiche
ffuf -u http://target.lab/FUZZ -w /usr/share/wordlists/dirb/common.txt -e .php,.txt,.bak

# Fuzzing di un parametro GET — FUZZ nel valore
ffuf -u "http://target.lab/page.php?id=FUZZ" -w /usr/share/seclists/Fuzzing/1-4_digit_numbers.txt

# Fuzzing sottodomini — FUZZ nell'host header
ffuf -u http://FUZZ.target.lab/ -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host: FUZZ.target.lab"

# Fuzzing POST — FUZZ nel body (es. brute-force login)
ffuf -u http://target.lab/login -X POST -d "username=admin&password=FUZZ" \
     -w /usr/share/wordlists/rockyou.txt -H "Content-Type: application/x-www-form-urlencoded"

# Filtrare per codice HTTP (es. escludere 404)
ffuf -u http://target.lab/FUZZ -w wordlist.txt -fc 404

# Filtrare per dimensione risposta (es. escludere risposte da 0 byte)
ffuf -u http://target.lab/FUZZ -w wordlist.txt -fs 0

# Limitare la velocità per non sovraccaricare il server
ffuf -u http://target.lab/FUZZ -w wordlist.txt -rate 50

# Output in formato JSON per analisi successive
ffuf -u http://target.lab/FUZZ -w wordlist.txt -o risultati.json -of json
```

**Flag chiave:**

| Flag | Significato |
|---|---|
| `-u` | URL con `FUZZ` come placeholder |
| `-w` | Wordlist (può usare `-w lista:KEYWORD` per più wordlist) |
| `-e` | Estensioni da aggiungere |
| `-H` | Header HTTP aggiuntivo |
| `-X` | Metodo HTTP (GET, POST, PUT…) |
| `-d` | Dati del body (richieste POST) |
| `-fc` | Filtra per codice HTTP (esclude) |
| `-fs` | Filtra per dimensione risposta (esclude) |
| `-mc` | Mostra solo questi codici HTTP |
| `-rate` | Richieste al secondo |
| `-t` | Thread paralleli (default: 40) |

## Quando si usa

- Fase di [[Enumerazione]]: directory busting, ricerca file nascosti, fuzzing parametri.
- Quando si ha bisogno di fuzzing avanzato (parametri, cookie, header) dove [[Gobuster]] è limitato.
- Brute-force di form di login (con filtri per distinguere successo/fallimento).
- Discovery di sottodomini e virtual host.

## Note e trucchi

- Il placeholder `FUZZ` può apparire in qualsiasi parte della richiesta: URL, header, body. Con più wordlist si usa `W1` e `W2` come keyword.
- Per evitare di sovraccaricare il server target (e rendersi meno visibili), usare `-rate 50` o `-t 20`.
- La modalità **interattiva** (tasto `p` durante l'esecuzione) mette in pausa il fuzzing senza terminarlo.
- Combinare con [[Gobuster]] nella pratica: Gobuster per la prima passata veloce, ffuf per fuzzing parametri e filtri fini.

## Collegamenti

- [[Gobuster]]
- [[Enumerazione]]
- [[Nikto]]
- [[HTTP e HTTPS]]
- [[SQL Injection]]
- [[Cross-Site Scripting (XSS)]]
- [[Kali Linux]]

## Fonti

- ffuf — GitHub ufficiale: <https://github.com/ffuf/ffuf>
- HackTricks — Fuzzing: <https://book.hacktricks.xyz/generic-methodologies-and-resources/web-api-pentesting>
- TryHackMe — Ffuf room: <https://tryhackme.com/room/ffuf>
