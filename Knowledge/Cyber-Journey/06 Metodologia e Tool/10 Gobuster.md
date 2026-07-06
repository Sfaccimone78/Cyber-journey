---
tipo: entita
tag: [tool]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Gobuster"]

---

# Gobuster

## In breve

**Gobuster** è un tool open source scritto in Go per il **brute-force di directory e file web**, sottodomini DNS e virtual host. Dato un URL e una wordlist, tenta ogni parola della lista come path e riporta le risorse che restituiscono risposte HTTP valide (tipicamente codici 200, 301, 302). È uno strumento fondamentale per la fase di [[Enumerazione]] web.

> **Nota etica**: Gobuster va usato solo su applicazioni web di cui si ha autorizzazione. L'uso su siti altrui è illegale e facilmente rilevabile dai log del server.

## Uso tipico

```bash
# Directory busting — modalità dir
gobuster dir -u http://target.lab -w /usr/share/wordlists/dirb/common.txt

# Aggiungere estensioni da cercare (es. .php, .txt, .bak)
gobuster dir -u http://target.lab -w /usr/share/wordlists/dirb/common.txt -x php,txt,bak

# Specificare il codice di stato da mostrare (default: 200,301,302,403)
gobuster dir -u http://target.lab -w /usr/share/wordlists/dirb/common.txt -s 200,301

# Aumentare i thread per velocità (default: 10)
gobuster dir -u http://target.lab -w /usr/share/wordlists/dirb/common.txt -t 50

# Enumerazione sottodomini DNS — modalità dns
gobuster dns -d example.com -w /usr/share/wordlists/dnsmap.txt

# Enumerazione virtual host — modalità vhost
gobuster vhost -u http://10.10.10.5 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Salvare l'output su file
gobuster dir -u http://target.lab -w /usr/share/wordlists/dirb/common.txt -o risultati_gobuster.txt
```

**Flag chiave (modalità dir):**

| Flag | Significato |
|---|---|
| `-u` | URL target |
| `-w` | Percorso della wordlist |
| `-x` | Estensioni da aggiungere a ogni parola |
| `-t` | Numero di thread paralleli |
| `-s` | Codici di stato HTTP da mostrare |
| `-o` | File di output |
| `--no-error` | Non mostrare errori (output più pulito) |

## Quando si usa

- Fase di [[Enumerazione]]: per scoprire directory nascoste (`/admin`, `/backup`, `/api`), file dimenticati (`.env`, `config.php`, `backup.zip`).
- Ricerca di pannelli di amministrazione non linkati.
- Enumerazione di sottodomini in alternativa a `dig` o `dnsrecon`.
- Virtual host discovery quando più siti girano sullo stesso IP.

## Note e trucchi

- La qualità dei risultati dipende quasi interamente dalla **wordlist**: SecLists (disponibile su [[Kali Linux]] in `/usr/share/seclists/`) è la raccolta più completa. Per web: `Discovery/Web-Content/directory-list-2.3-medium.txt`.
- Se Gobuster è troppo rumoroso, considerare [[ffuf]] che offre più opzioni di filtro output.
- Con `-x php,html,txt` il numero di richieste moltiplica: una wordlist di 2000 parole con 3 estensioni fa 8000 richieste. Regolare i thread di conseguenza.
- L'errore `invalid certificate` su HTTPS si bypassa con il flag `-k` (skip TLS verification).

## Lab

- **[[TryHackMe]] — "Content Discovery"**: allena il directory/file busting e la vhost discovery esattamente con l'approccio di Gobuster (URL + wordlist), confrontandolo con altri tool.
- **[[PortSwigger Web Academy]] — categoria *Information disclosure*** e i lab su file/percorsi nascosti: pratica il *perché* si cercano directory dimenticate (backup, config, endpoint admin).
- **[[HackTheBox]] — Starting Point con servizi web**: usa `gobuster dir -u ... -w directory-list-2.3-medium.txt -x php,txt,bak` per trovare l'endpoint che apre la macchina.

## Domande

1. **D:** A cosa serve Gobuster e in quale fase del pentest si usa?  **R:** Al brute-force di directory/file web, sottodomini DNS e virtual host; si usa nella fase di enumerazione.
2. **D:** Da cosa dipende soprattutto la qualità dei risultati?  **R:** Dalla wordlist scelta (es. SecLists), che determina quali path vengono tentati.
3. **D:** Cosa fa il flag `-x` e che effetto ha sul numero di richieste?  **R:** Aggiunge estensioni (es. `php,txt,bak`) a ogni parola, moltiplicando le richieste per il numero di estensioni.
4. **D:** Come si gestisce un certificato TLS non valido su un target HTTPS?  **R:** Con il flag `-k` (salta la verifica del certificato).
5. **D:** Perché a volte si preferisce [[ffuf]] a Gobuster?  **R:** Perché ffuf offre più opzioni di filtro dell'output (per size, codice, parole), utile quando Gobuster è troppo rumoroso.

## Collegamenti

- [[Enumerazione]]
- [[ffuf]]
- [[Nikto]]
- [[HTTP e HTTPS]]
- [[Kali Linux]]
- [[Ricognizione (Recon)]]

## Fonti

- Gobuster — GitHub ufficiale: <https://github.com/OJ/gobuster>
- HackTricks — Web Fuzzing: <https://book.hacktricks.xyz/generic-methodologies-and-resources/web-api-pentesting>
- TryHackMe — Content Discovery: <https://tryhackme.com/room/contentdiscovery>
