---
tipo: concetto
tag: [tool]
fase: 1
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["Python per la Sicurezza"]
---

# Python per la Sicurezza

> **Nota etica**: gli strumenti costruiti in quest'area vanno usati **solo** su sistemi tuoi o con
> autorizzazione scritta (lab, TryHackMe, CTF, range autorizzati). Scansionare o attaccare host
> di terzi senza permesso è reato.

## In breve
Python è il **linguaggio franco** dell'offensive security: sintassi minima, libreria standard ricca
(socket, os, re, http, subprocess), e un ecosistema di pacchetti (`requests`, `pwntools`, `scapy`,
`impacket`) che coprono dalla rete al binary exploitation. La logica è sempre la stessa: **automatizzare
ciò che a mano sarebbe lento e ripetitivo** — provare 10.000 password, scansionare 65.535 porte,
parsare 4 GB di log. La CPU non si annoia e non sbaglia a copiare.

## Perché Python e non Bash
[[Bash Scripting]] è perfetto per incollare tool esistenti (`nmap | grep | cut`). Python serve quando
ti serve **stato e struttura**: gestire socket, parsare JSON, mantenere una sessione HTTP con cookie,
fare threading. Regola pratica: se devi *orchestrare comandi* usa Bash; se devi *costruire logica* usa Python.

## Setup: il virtualenv è obbligatorio
Mai installare pacchetti nel Python di sistema: rompi le dipendenze del SO. Si isola ogni progetto in
un **virtual environment** (venv) — una cartella con il suo interprete e i suoi pacchetti.

```bash
# 1. crea un ambiente isolato nella cartella .venv
python3 -m venv .venv

# 2. attivalo (Linux/macOS). Da ora 'python' e 'pip' puntano dentro .venv
source .venv/bin/activate
# Windows PowerShell:  .venv\Scripts\Activate.ps1

# 3. installa le librerie chiave SOLO in questo ambiente
pip install requests pwntools scapy

# 4. congela le versioni per riproducibilità
pip freeze > requirements.txt

# 5. disattiva quando hai finito
deactivate
```

## Script di esempio — verificatore d'ambiente
Uno script che controlla se le librerie chiave sono installate e stampa cosa manca. Logica: invece di
far esplodere lo script con un `ImportError` a runtime, **interroghiamo** l'ambiente in anticipo.

```python
#!/usr/bin/env python3
# verifica_setup.py — controlla che l'ambiente offensivo sia pronto

import importlib   # permette di importare moduli dal loro NOME (stringa), a runtime
import sys         # info sull'interprete: versione, eseguibile, path

# Librerie che ci aspettiamo di trovare. Chiave = nome import, valore = a cosa serve.
LIBRERIE = {
    "requests": "client HTTP ad alto livello (sessioni, header)",
    "pwn":      "pwntools: interazione con processi e servizi remoti",
    "scapy":    "forgia e sniffa pacchetti a basso livello",
    "bs4":      "BeautifulSoup: parsing HTML",
}

def controlla(nome: str) -> bool:
    """Prova a importare il modulo; True se esiste, False altrimenti."""
    try:
        importlib.import_module(nome)   # import dinamico: se fallisce solleva ImportError
        return True
    except ImportError:                 # catturiamo SOLO il caso 'non installato'
        return False

def main() -> None:
    # Verifica versione interprete: vogliamo Python 3.8+ (sys.version_info è una tupla)
    if sys.version_info < (3, 8):
        print(f"[!] Python troppo vecchio: {sys.version.split()[0]} — aggiorna a 3.8+")
        sys.exit(1)                      # exit code != 0 segnala fallimento agli script chiamanti

    print(f"[+] Interprete: {sys.executable}")
    print(f"[+] Versione:   {sys.version.split()[0]}\n")

    mancanti = []                        # accumuliamo i nomi non trovati
    for nome, scopo in LIBRERIE.items():
        ok = controlla(nome)
        stato = "OK " if ok else "MANCA"
        print(f"  [{stato}] {nome:<10} — {scopo}")
        if not ok:
            mancanti.append(nome)

    # Riepilogo finale: se manca qualcosa, suggerisci il comando di install
    if mancanti:
        # bs4 si installa come 'beautifulsoup4', pwn come 'pwntools': mappa i nomi pip
        pip_names = {"bs4": "beautifulsoup4", "pwn": "pwntools"}
        pacchetti = " ".join(pip_names.get(m, m) for m in mancanti)
        print(f"\n[!] Mancano {len(mancanti)} librerie. Installa con:\n    pip install {pacchetti}")
        sys.exit(1)
    print("\n[+] Ambiente pronto.")

if __name__ == "__main__":   # eseguito solo se lanciato direttamente, non se importato
    main()
```

## La logica chiave
- **Import dinamico** (`importlib`): controllare l'esistenza di un modulo *senza* dipenderci. È il
  pattern dei tool che si adattano a ciò che trovano installato sul sistema.
- **Exit code** (`sys.exit(1)`): in catena con [[Bash Scripting]], `0` = successo, `≠0` = errore.
  Permette `python verifica.py && ./exploit.py`.
- **`if __name__ == "__main__"`**: separa "libreria importabile" da "script eseguibile". Ogni tool
  serio lo usa per essere sia riusabile sia lanciabile.

## Esercizio progressivo
1. **Base**: estendi `LIBRERIE` con `impacket` e `paramiko` (SSH, vedi [[SSH]]).
2. **Intermedio**: aggiungi il controllo della versione *specifica* di una libreria
   (`importlib.metadata.version("requests")` e confronta con un minimo richiesto).
3. **Avanzato**: trasforma lo script in modo che, se `--fix` è passato come argomento (vedi `sys.argv`
   o il modulo `argparse`), installi automaticamente i pacchetti mancanti via
   `subprocess.run([sys.executable, "-m", "pip", "install", ...])`.

## Lab
- **TryHackMe** — *Python Basics*, *Python for Pentesters*. **Exercism** track Python per le basi.
- Ricrea il verificatore d'ambiente sopra in un virtualenv pulito; estendilo per leggere variabili
  sensibili da `os.environ`.

## Domande
**D: Perché un virtualenv è di fatto obbligatorio?**
R: Isola le dipendenze per progetto, evita conflitti di versione e di rompere il Python di sistema,
e rende l'ambiente riproducibile (`requirements.txt`).

**D: Quando conviene Python rispetto a Bash?**
R: Per logica complessa, parsing strutturato, gestione errori e librerie (requests, scapy, pwntools)
e portabilità. Bash resta migliore per glue di comandi e one-liner sul sistema.

**D: Cosa rende Python lo standard de-facto del tooling offensivo?**
R: Ecosistema ricco (requests, scapy, pwntools, impacket), prototipazione rapida e leggibilità: si
passa dall'idea allo script in pochi minuti.

## Collegamenti
- [[Socket e Port Scanner]] — primo uso concreto della rete in Python
- [[Requests e HTTP]] — livello applicativo
- [[Bash Scripting]] — quando preferire l'uno o l'altro
- [[Kali Linux]] — Python e le librerie offensive sono preinstallate
- [[SSH]] — automazione remota con `paramiko`

## Fonti
- Python — venv (ambienti virtuali): https://docs.python.org/3/library/venv.html
- Python — importlib: https://docs.python.org/3/library/importlib.html
- pip — Installing Packages: https://packaging.python.org/en/latest/tutorials/installing-packages/
- Real Python — Python Virtual Environments Primer: https://realpython.com/python-virtual-environments-a-primer/
