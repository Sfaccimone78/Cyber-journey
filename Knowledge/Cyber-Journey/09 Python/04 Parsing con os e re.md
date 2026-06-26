---
tipo: concetto
tag: [tool, linux]
fase: 1
fonti: 4
aggiornato: 2026-06-21
stato: maturo
aliases: ["Parsing con os e re"]
---

# Parsing con os e re

> **Nota etica**: cercare segreti nel filesystem è parte legittima della post-exploitation **solo** su
> sistemi autorizzati (TryHackMe, lab, CTF). Su una macchina non tua è accesso abusivo.

## In breve
Dopo aver ottenuto un accesso (vedi [[Post-Exploitation]]), il primo lavoro è **cercare**: password
nei file di config, chiavi private, token, flag. A mano è impossibile su un filesystem grande. Python
unisce due moduli della libreria standard: **`os`** (camminare la directory tree, leggere metadati) e
**`re`** (espressioni regolari, riconoscere *pattern* nel testo). È la versione programmabile di
`grep -r` (vedi [[grep]]) e `find` (vedi [[find]]), con in più logica e output strutturato.

## I due mattoni
- **`os.walk(radice)`** percorre **ricorsivamente** un albero di cartelle. A ogni passo restituisce la
  tripla `(cartella_corrente, sottocartelle, file)`. È il `find` di Python, ma in puro Python.
- **`re`** descrive *forme* di testo, non stringhe fisse. `password\s*=\s*\S+` non cerca la parola
  "password" ma il **pattern** "password, spazi opzionali, uguale, spazi, un valore". È la stessa
  potenza di [[grep]] `-E`, riusabile in logica.

## La regex compilata: perché `re.compile`
Se cerchi lo stesso pattern in 50.000 file, ricompilarlo ogni volta è spreco. `re.compile()` traduce
il pattern **una volta** in un automa riusabile. È la differenza tra leggere la ricetta ogni volta e
impararla a memoria.

## Script completo — secret hunter sul filesystem

```python
#!/usr/bin/env python3
# secret_hunter.py — cerca segreti (password, chiavi, token) in un albero di file. SOLO su sistemi autorizzati.

import os                           # walk del filesystem e metadati dei file
import re                           # espressioni regolari
import sys

# Pattern di interesse. re.IGNORECASE rende il match case-insensitive (Password == password).
# Ogni pattern ha un nome leggibile + la regex. Sono ESEMPI didattici, non esaustivi.
PATTERN = {
    "Password":     re.compile(r"(?i)password\s*[:=]\s*['\"]?(\S+)"),     # password = "..."
    "Chiave AWS":   re.compile(r"AKIA[0-9A-Z]{16}"),                       # access key AWS
    "Chiave priv.": re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
    "Token JWT":    re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
}

# Estensioni binarie da saltare: cercare testo in un .jpg è inutile e lento.
SALTA = {".jpg", ".png", ".gif", ".zip", ".gz", ".o", ".so", ".pyc", ".exe"}
MAX_BYTE = 2_000_000               # non leggere file enormi (> 2 MB): probabili dump/binari

def scansiona_file(percorso: str) -> None:
    """Apre un file di testo e applica tutti i pattern riga per riga."""
    try:
        # errors='ignore' evita crash su byte non-UTF8; leggiamo riga per riga per non saturare la RAM
        with open(percorso, "r", encoding="utf-8", errors="ignore") as f:
            for n, riga in enumerate(f, start=1):          # n = numero di riga (1-based)
                for nome, regex in PATTERN.items():
                    m = regex.search(riga)                 # cerca il pattern in QUESTA riga
                    if m:
                        # m.group(0) = tutto il match; lo tronchiamo per non stampare segreti interi
                        estratto = m.group(0)[:60]
                        print(f"  [{nome}] {percorso}:{n}  ->  {estratto}")
    except (OSError, PermissionError):    # file sparito o senza permessi: ignora e continua
        pass

def cammina(radice: str) -> None:
    """Percorre ricorsivamente la radice e scansiona ogni file testuale candidato."""
    for cartella, _sottocartelle, file in os.walk(radice):   # _ : variabile che non usiamo
        for nome_file in file:
            percorso = os.path.join(cartella, nome_file)     # ricostruisce il path completo (cross-OS)
            ext = os.path.splitext(nome_file)[1].lower()     # estensione, in minuscolo
            if ext in SALTA:
                continue
            try:
                if os.path.getsize(percorso) > MAX_BYTE:     # salta i file troppo grossi
                    continue
            except OSError:
                continue
            scansiona_file(percorso)

def main() -> None:
    radice = sys.argv[1] if len(sys.argv) > 1 else "."   # default: cartella corrente
    if not os.path.isdir(radice):
        print(f"[!] {radice} non è una cartella valida")
        sys.exit(1)
    print(f"[+] Caccia ai segreti in: {os.path.abspath(radice)}\n")
    cammina(radice)
    print("\n[+] Scansione completata.")

if __name__ == "__main__":
    main()
```

## La logica chiave
- **Pattern, non stringhe**: cercare `"password"` letterale perde `passwd`, `PASSWORD=`, `pwd:`. Una
  regex cattura la **forma** del segreto. È il salto concettuale rispetto a un `grep` ingenuo.
- **Lettura riga per riga**: `for riga in f` non carica il file intero in memoria — funziona su file
  da gigabyte. Caricare tutto con `f.read()` farebbe esplodere la RAM su un dump.
- **Filtrare prima di leggere**: saltare estensioni binarie e file enormi (`SALTA`, `MAX_BYTE`) è ciò
  che rende lo scan veloce. La maggior parte del tempo si risparmia *non* aprendo file inutili.
- **Robustezza**: `try/except OSError` ovunque. Su un filesystem reale incontri permessi negati, link
  rotti, file che spariscono: il tool deve assorbirli e proseguire.

## Gruppi di cattura
`m.group(0)` è l'intero match; `m.group(1)` è il primo gruppo `(...)` — nel pattern Password è **solo
il valore** dopo l'uguale. Usare i gruppi serve a estrarre la parte utile, non il rumore intorno.

## Esercizio progressivo
1. **Base**: aggiungi un pattern per gli indirizzi email e uno per le chiavi API generiche
   (`api[_-]?key`).
2. **Intermedio**: raccogli i risultati in una lista di dizionari e a fine scansione esporta un report
   JSON (`json.dump`), come farebbe un tool di [[Post-Exploitation]].
3. **Avanzato**: aggiungi `--exclude` per saltare cartelle (es. `node_modules`, `.git`) modificando
   *in-place* la lista `sottocartelle` dentro `os.walk` — è il trucco per **potare** l'albero e non
   discendere in rami inutili.

## Collegamenti
- [[grep]] — l'equivalente da shell di questo script
- [[find]] — `os.walk` è il suo gemello in Python
- [[Pipe e Redirezione]] — comporre tool testuali in shell
- [[Post-Exploitation]] — dove la caccia ai segreti entra in gioco
- [[Privilege Escalation Linux]] — config con password = vettore di escalation
- [[Automazione Offensiva]] — comporre questi mattoni in tool completi

## Fonti
- Python — os.walk: https://docs.python.org/3/library/os.html#os.walk
- Python — re (regex): https://docs.python.org/3/library/re.html
- Python — re HOWTO: https://docs.python.org/3/howto/regex.html
- OWASP — Secrets in code / TruffleHog (riferimento concettuale): https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password
