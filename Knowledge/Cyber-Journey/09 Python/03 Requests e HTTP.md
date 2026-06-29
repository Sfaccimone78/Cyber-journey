---
tipo: concetto
tag: [tool, web]
fase: 1
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["Requests e HTTP"]
---

# Requests e HTTP

> **Nota etica**: automatizzare richieste HTTP verso un'app significa generare traffico e potenzialmente
> alterarne lo stato. Fallo **solo** su target autorizzati ([[PortSwigger Web Academy]], lab, CTF).

## In breve
`requests` è la libreria HTTP di Python: nasconde socket, parsing dello status line e degli header, e
ti dà oggetti puliti. Per la sicurezza è il livello su cui si costruisce **quasi tutto il web hacking
automatizzato**: provare endpoint, fuzzare parametri, mantenere sessioni autenticate, parsare risposte.
È il [[Requests e HTTP|requests]] che sta dietro a un fuzzer o a un bruteforcer come quelli in
[[Automazione Offensiva]]. Vale la teoria di [[HTTP e HTTPS]]: metodo, header, status code, body.

## Il concetto chiave: la Session
Una **request singola** è stateless. Ma un'app web è **stateful**: dopo il login ti dà un cookie di
sessione (vedi [[Cookie e JWT]]) che devi reinviare a ogni richiesta. Una `requests.Session()` fa
esattamente questo: **conserva cookie, header e connessione** tra chiamate. Senza Session dovresti
copiare il cookie a mano ogni volta; con Session, una volta loggato resti loggato.

## Status code = il linguaggio del fuzzing
Il valore di una risposta sta nel suo **status code** e nella **lunghezza del body**:
- `200` → la risorsa esiste / la richiesta è valida.
- `301/302` → redirect (spesso "login richiesto").
- `403` → esiste ma vietato (interessante: c'è qualcosa).
- `404` → non esiste.
Un dir-fuzzer come [[ffuf]] o [[Gobuster]] non fa altro che provare migliaia di path e **filtrare per
status/lunghezza**. Lo stesso principio guida lo script qui sotto.

## Script completo — client HTTP con sessione, login e sonda di endpoint

```python
#!/usr/bin/env python3
# http_probe.py — login + enumerazione di endpoint via sessione. SOLO su target autorizzati.

import sys
import requests                     # client HTTP ad alto livello

# Header realistico: alcune app bloccano l'User-Agent di default di requests (anti-bot).
HEADERS = {"User-Agent": "Mozilla/5.0 (compatibile; lab-scanner)"}
TIMEOUT = 5                         # secondi: oltre, la richiesta è considerata persa

def login(sess: requests.Session, base: str, user: str, pwd: str) -> bool:
    """Esegue il login POST e ritorna True se la sessione risulta autenticata."""
    url = f"{base}/login"
    # POST con dati form. La Session salva AUTOMATICAMENTE i cookie di risposta (set-cookie).
    r = sess.post(url, data={"username": user, "password": pwd},
                  timeout=TIMEOUT, allow_redirects=False)  # non seguiamo il redirect: ci basta lo status
    # Euristica: login riuscito di solito risponde 302 (redirect alla dashboard) o setta un cookie sessione
    autenticato = r.status_code == 302 or "session" in sess.cookies
    print(f"[{'+' if autenticato else '-'}] Login {user}:{pwd} -> HTTP {r.status_code}")
    return autenticato

def sonda(sess: requests.Session, base: str, percorsi: list[str]) -> None:
    """Prova una lista di path e riporta quelli 'interessanti' (non-404)."""
    for p in percorsi:
        url = f"{base}/{p}"
        try:
            r = sess.get(url, timeout=TIMEOUT, allow_redirects=False)
        except requests.RequestException as e:   # cattura timeout, DNS, connessione rifiutata...
            print(f"  [!] {p}: errore di rete ({e.__class__.__name__})")
            continue
        # Filtriamo via i 404: tutto il resto merita uno sguardo. len(r.content) distingue pagine diverse.
        if r.status_code != 404:
            print(f"  [{r.status_code}] /{p:<15} ({len(r.content)} byte)")

def main() -> None:
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <http://host:porta>")
        sys.exit(1)
    base = sys.argv[1].rstrip("/")  # togli slash finale per non avere // nei path

    # UNA sola Session per tutto: header condivisi + cookie persistenti tra login e sonde
    with requests.Session() as sess:
        sess.headers.update(HEADERS)       # applica l'User-Agent a ogni richiesta della sessione

        # 1) prova un login (credenziali di lab note)
        loggato = login(sess, base, "admin", "admin")

        # 2) enumera endpoint comuni. Da loggati possiamo vedere aree protette.
        comuni = ["admin", "dashboard", "api/users", "config", "backup.zip", "robots.txt"]
        print(f"\n[+] Sondaggio endpoint ({'autenticato' if loggato else 'anonimo'}):")
        sonda(sess, base, comuni)

if __name__ == "__main__":
    main()
```

## La logica chiave
- **Session = stato**: il salto di qualità è capire che il login non "ritorna un token da gestire a
  mano" — la Session lo conserva per te. Tutto ciò che segue eredita l'autenticazione.
- **`allow_redirects=False`**: per il fuzzing vuoi vedere il `302` *grezzo*, non finire dove ti manda
  il server. Seguire i redirect nasconde l'informazione che cerchi.
- **`try/except requests.RequestException`**: una richiesta su mille fallirà (timeout, reset). Lo
  script non deve morire: cattura, logga, continua. È la differenza tra un tool e uno script fragile.
- **Filtrare, non collezionare**: il valore è scartare i 404. Stesso identico principio di [[ffuf]]
  (`-fc`, `-fs`) e [[Gobuster]].

## Parsing della risposta
Per estrarre dati (link, token CSRF, versioni) dal body si usa BeautifulSoup (`bs4`):
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, "html.parser")
token = soup.find("input", {"name": "csrf"})["value"]   # estrai il token CSRF prima del POST
```
Per le API JSON basta `r.json()` → ottieni un `dict` Python pronto da navigare.

## Esercizio progressivo
1. **Base**: leggi la lista di path da un file wordlist (una per riga) invece che hardcoded.
2. **Intermedio**: prima del login fai un `GET /login`, estrai il **token CSRF** con BeautifulSoup
   (vedi [[Cross-Site Request Forgery (CSRF)]]) e includilo nel POST.
3. **Avanzato**: trasforma `sonda` in multithread con `ThreadPoolExecutor` (come in
   [[Socket e Port Scanner]]) e aggiungi un filtro `--filter-size` per nascondere le risposte di una
   data lunghezza (tipica pagina "non trovato" custom).

## Lab
- **PortSwigger Web Academy** — automatizza un lab (es. brute di password o enumerazione) con `requests`.
- Scrivi un mini dir-buster con una wordlist che classifica per status code; confrontalo con [[ffuf]]/[[Gobuster]].

## Domande
**D: A cosa serve `requests.Session()`?**
R: Persiste cookie, header e connessione (keep-alive) tra richieste → permette login e poi navigazione
autenticata senza ripassare i cookie a mano.

**D: Come si sfruttano gli status code nel fuzzing/dir-busting?**
R: Si distinguono 200/301-302/403/404 per dedurre esistenza e accessibilità delle risorse; 403 spesso
indica una risorsa che esiste ma è protetta.

**D: Perché a volte si imposta `allow_redirects=False`?**
R: Per osservare il vero comportamento (es. il 302 di un login riuscito) invece di seguire la catena e
vederne solo la pagina finale.

## Collegamenti
- [[HTTP e HTTPS]] — la teoria del protocollo
- [[Cookie e JWT]] — cosa conserva la Session
- [[Cross-Site Request Forgery (CSRF)]] — il token da estrarre prima dei POST
- [[ffuf]] / [[Gobuster]] — fuzzer industriali con la stessa logica
- [[Automazione Offensiva]] — qui si compone in un tool completo
- [[Burp Suite]] — l'alternativa GUI per ispezionare le richieste

## Fonti
- Requests — documentazione ufficiale: https://requests.readthedocs.io/en/latest/
- Requests — Sessions e cookie: https://requests.readthedocs.io/en/latest/user/advanced/#session-objects
- MDN — HTTP response status codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- Beautiful Soup — documentazione: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
