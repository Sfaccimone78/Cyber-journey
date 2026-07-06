---
tipo: entita
tag: [linux]
fase: 1
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["sed"]

---

# sed

## In breve

**sed** (Stream EDitor) è un editor di testo non interattivo che legge l'input riga per riga, applica trasformazioni tramite un mini-linguaggio di comandi (basato su espressioni regolari), e scrive il risultato sullo stdout. A differenza di [[awk]], sed lavora su righe intere e su pattern di testo, non su colonne. Il suo punto di forza è la **sostituzione in massa** e la **trasformazione di flussi di testo** in pipeline.

Sintassi generale:
```bash
sed [opzioni] 'script' [file]
sed [opzioni] -e 'script1' -e 'script2' [file]
sed [opzioni] -f scriptfile [file]
```

---

## Opzioni principali

| Opzione | Significato |
|---------|-------------|
| `-n` | Sopprime l'output di default (stamp solo con `p`) |
| `-i[SUFFIX]` | In-place: modifica il file originale; con SUFFIX crea backup |
| `-e 'cmd'` | Aggiunge un comando allo script (per comandi multipli) |
| `-E` / `-r` | Abilita ERE (Extended Regular Expressions) |
| `-f file` | Legge lo script da file |
| `--sandbox` | Modalità sandbox: blocca comandi che leggono/scrivono file (GNU sed) |

---

## Indirizzi: selezionare le righe

Prima del comando puoi specificare un **indirizzo** che indica su quali righe applicarlo:

```bash
sed '3s/a/b/'          file   # solo riga 3
sed '5,10s/a/b/'       file   # righe da 5 a 10
sed '$s/a/b/'          file   # solo ultima riga
sed '/pattern/s/a/b/'  file   # righe che contengono "pattern"
sed '1,/stop/s/a/b/'   file   # dalla riga 1 fino alla prima che matcha "stop"
sed '/start/,/stop/d'  file   # cancella dal range start→stop
sed '2~3s/a/b/'        file   # prima con step: riga 2, poi 5, 8, 11… (GNU sed)
sed '/pattern/!s/a/b/' file   # righe che NON matchano "pattern"
```

---

## Comandi sed fondamentali

| Comando | Significato | Esempio |
|---------|-------------|---------|
| `s/re/repl/flags` | Sostituzione | `sed 's/foo/bar/'` |
| `d` | Cancella la riga | `sed '/^#/d'` |
| `p` | Stampa la riga (usato con `-n`) | `sed -n '5p'` |
| `q` | Esce dopo aver elaborato la riga corrente | `sed '10q'` (stampa prime 10 righe) |
| `a\testo` | Appende testo dopo la riga | `sed '/pattern/a\riga aggiunta'` |
| `i\testo` | Inserisce testo prima della riga | `sed '1i\# Header'` |
| `c\testo` | Sostituisce la riga con testo | `sed '/old line/c\nuova riga'` |
| `y/src/dst/` | Traslitterazione carattere per carattere | `sed 'y/abc/ABC/'` |
| `n` | Leggi la riga successiva nel pattern space | uso avanzato |
| `N` | Appende la riga successiva al pattern space | multi-riga |
| `=` | Stampa il numero di riga corrente | `sed -n '/error/='` |
| `r file` | Legge e inserisce il contenuto di un file | `sed '/tag/r fragment.html'` |
| `w file` | Scrive le righe matchate in un file | `sed -n '/FAIL/w fail.log'` |

---

## Il comando di sostituzione `s` in dettaglio

```bash
s/PATTERN/REPLACE/[flags]
```

**Flag della sostituzione:**

| Flag | Significato |
|------|-------------|
| `g` | Globale: sostituisce tutte le occorrenze sulla riga |
| `N` (numero) | Sostituisce solo la N-esima occorrenza |
| `i` / `I` | Case-insensitive (GNU sed) |
| `p` | Stampa la riga se ha avuto una sostituzione (usato con `-n`) |
| `w file` | Scrive la riga sostituita in un file |

```bash
sed 's/foo/bar/'       # Prima occorrenza per riga
sed 's/foo/bar/g'      # Tutte le occorrenze
sed 's/foo/bar/2'      # Solo la seconda occorrenza
sed 's/foo/bar/gi'     # Tutte, case-insensitive (GNU)
sed -n 's/foo/bar/p'   # Stampa solo le righe modificate
```

**Delimitatore alternativo** (utile con path che contengono `/`):
```bash
sed 's|/usr/bin|/usr/local/bin|g' script.sh
sed 's!/old/path!/new/path!g'     script.sh
sed 's@https://old@https://new@g' urls.txt
```

**Riferimenti ai gruppi catturati:**
```bash
# BRE: gruppi con \( \), riferimento con \1
sed 's/\(root\):\(.*\):\(.*\)/\1 — UID:\3/' /etc/passwd

# ERE (-E): gruppi con ( ), riferimento con \1
sed -E 's/(root):(.*):([0-9]+)/\1 ha UID \3/' /etc/passwd

# & = l'intero match
sed 's/[0-9]\+/[&]/g' file.txt   # circonda ogni numero con []
```

---

## Uso in sicurezza e sysadmin

### Pulizia di file di configurazione

```bash
# Rimuovi commenti e righe vuote da sshd_config
sed '/^#/d; /^$/d' /etc/ssh/sshd_config

# Visualizza configurazione pulita (senza modificare il file)
sed '/^\s*#/d; /^\s*$/d' /etc/apache2/apache2.conf

# Disabilita PasswordAuthentication (in-place, con backup)
sed -i.bak 's/^PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
```

### Modifica di file di configurazione in automazione / pentest

```bash
# Cambia la porta SSH
sed -i 's/^#\?Port .*/Port 2222/' /etc/ssh/sshd_config

# Inietta una backdoor in .bashrc (post-exploitation)
sed -i '$a alias sudo="sudo -E env TERM=xterm"' /home/user/.bashrc

# Rimuovi una riga specifica dal sudoers (pericoloso — solo esempio)
sed -i '/^www-data/d' /etc/sudoers

# Sostituisci hash di password in file shadow (esempio CTF)
sed -i "s|root:.*:|root:$(python3 -c "import crypt; print(crypt.crypt('nuovapass','salt'))"):|" /etc/shadow

# Normalizza fine riga CRLF → LF (fix script Windows su Linux)
sed -i 's/\r$//' script.sh
```

### Parsing di log e output di tool

```bash
# Estrai solo le righe con errori, tra due timestamp
sed -n '/2026-06-22 14:00/,/2026-06-22 15:00/p' app.log | grep ERROR

# Rimuovi colori ANSI dall'output di tool (per parsing)
sed 's/\x1b\[[0-9;]*m//g' colored_output.txt

# Da output di nmap: estrai solo le righe con "open"
nmap -sV 192.168.1.0/24 | sed -n '/open/p'

# Anonimizza IP in un log per condivisione
sed -E 's/\b([0-9]{1,3}\.){3}[0-9]{1,3}\b/x.x.x.x/g' access.log

# Rimuovi righe duplicate consecutive (come uniq, ma senza sort)
sed '$!N; /^\(.*\)\n\1$/!P; D' file.txt

# Estrai sezione di un file di configurazione
sed -n '/\[Section\]/,/^\[/p' config.ini | sed '$d'
```

---

## Editing multi-riga

sed elabora una riga alla volta. Per pattern multi-riga si usa `N` (Next):

```bash
# Unisci ogni coppia di righe con una virgola
sed 'N; s/\n/,/' file.txt

# Elimina blocchi di righe vuote consecutive (lascia max 1)
sed '/^$/N;/^\n$/d' file.txt

# Cerca pattern che si estende su due righe
sed -n '/prima riga/{N; /seconda riga/p}' file.txt

# Sostituisci newline con spazio (variante)
sed ':a; N; $!ba; s/\n/ /g' file.txt
```

---

## `-i` in-place: uso sicuro

```bash
# SEMPRE fare un backup prima di modifiche in-place
sed -i.bak 's/old/new/g' file.txt   # crea file.txt.bak
# oppure
cp file.txt file.txt.bak && sed -i 's/old/new/g' file.txt

# Su macOS, -i richiede un suffisso obbligatorio (anche vuoto con '')
sed -i '' 's/old/new/g' file.txt  # macOS

# Verifica prima senza -i
sed 's/old/new/g' file.txt | diff - file.txt
```

> [!warning] `-i` senza backup può essere distruttivo. Soprattutto con pattern greedy o espressioni regolari errate, si può corrompere file di configurazione critici. Testa sempre prima senza `-i` e poi aggiungi il flag.

---

## Espressioni regolari in sed

### BRE (default)
```bash
sed 's/[0-9]\{3\}/NUM/'    # tre cifre (BRE: {} va escapato)
sed 's/\(word\)/[\1]/'     # gruppo catturato (BRE: () va escapato)
sed '/^.\{80\}/d'          # elimina righe più lunghe di 80 caratteri
```

### ERE (`sed -E`)
```bash
sed -E 's/[0-9]{3}/NUM/'        # tre cifre (ERE: {} senza escape)
sed -E 's/(word)/[\1]/'         # gruppo catturato (ERE: () senza escape)
sed -E 's/https?:\/\///'        # rimuovi http:// o https://
sed -E 's/(Failed|Invalid) (password|user)/LOGIN_ERROR/g'
```

---

## Pipeline avanzate con sed

```bash
# Pipeline classica: grep → sed → awk
grep "Failed password" /var/log/auth.log | \
  sed 's/.*from //' | \
  awk '{print $1}' | \
  sort | uniq -c | sort -rn

# Sostituire output di un comando prima di passarlo a un altro
curl -s https://example.com | sed 's/<[^>]*>//g'   # strip HTML tags

# Generare un file di configurazione dal template
sed "s/__HOST__/$TARGET_IP/g; s/__PORT__/$PORT/g" template.conf > target.conf

# Estrarre valori da JSON semplice (senza jq)
curl -s api/endpoint | sed -n 's/.*"token":"\([^"]*\)".*/\1/p'

# Sostituire password in file di config durante deployment
sed -i "s/DB_PASS=.*/DB_PASS=${NEW_PASS}/" /etc/app/config.env
```

---

## Confronto sed vs awk vs grep

| Operazione | Strumento ideale | Motivazione |
|------------|-----------------|-------------|
| Trova righe con pattern | [[grep]] | è il suo scopo principale |
| Sostituisci testo in righe | `sed` | `s///` è la sua forza |
| Filtra su colonna N | [[awk]] | accesso diretto a `$N` |
| Calcola somme/medie | [[awk]] | supporta aritmetica |
| Cancella righe con pattern | `sed '/p/d'` o `grep -v` | entrambi vanno bene |
| Estrai sezione (range) | `sed -n '/A/,/B/p'` o `awk '/A/,/B/'` | entrambi validi |
| Modifica file in-place | `sed -i` | grep/awk non hanno -i |
| Pattern multi-riga | `sed N;` o `awk` | awk è più leggibile |

---

## Casi limite e gotcha

- **BRE vs ERE**: i metacaratteri `+`, `?`, `|`, `(`, `)`, `{`, `}` in BRE (default) richiedono il backslash: `\+`, `\?` ecc. Con `-E` non serve. Molti errori nascono da questa confusione.
- **`&` nella sostituzione**: `&` rappresenta l'intero match. Per scrivere un `&` letterale nella stringa di replace, escapalo: `\&`.
- **macOS sed vs GNU sed**: su macOS, `sed` è BSD sed e si comporta diversamente. `-i` richiede un argomento (anche `''`); `-E` non è accettato (usa `-E` — in realtà su macOS recenti va bene). Per script portabili, usa `gsed` (GNU sed installabile con Homebrew).
- **Spazi nel comando `a`, `i`, `c`**: la sintassi tradizionale richiede `a\` seguito da newline e poi il testo. GNU sed accetta anche `a testo` sulla stessa riga, ma non è portabile.
- **Pattern con `/`**: se il pattern contiene `/`, o lo escapi con `\/` o cambi delimitatore: `sed 's|/old|/new|g'`.
- **`-i` e `set -e`**: in script con `set -e`, un `sed -i` che non trova nessun match su alcuni sistemi può restituire exit code non zero. Usa `|| true` se il mancato match è accettabile.
- **Newline nel replace**: per inserire un newline nel testo di sostituzione, in BRE usa `\n`; in alcuni sed antichi serve un backslash seguito da newline letterale.

---

## Lab

- **HackerRank — Linux Shell → Text Processing / "Sed"**: sfide (`sed-1` … `sed-5`) su sostituzione con e senza `g`, N-esima occorrenza, gruppi catturati `\(...\)`/`\1` e indirizzi di riga — copre esattamente il comando `s///` e i suoi flag.
- **OverTheWire — Bandit** (livelli di manipolazione testo): usa `sed` per ripulire l'output e isolare la stringa utile prima di passarla al comando successivo in pipeline.
- **Lab pratico locale**: prendi un `sshd_config` o un `.env` e allena i casi reali della nota — `sed '/^#/d; /^$/d'` per ripulire i commenti, `sed -i.bak 's/^PasswordAuthentication yes/PasswordAuthentication no/'` per l'hardening (sempre con backup `.bak`).

## Domande da esame/colloquio

> **D: Qual è la differenza tra `sed 's/foo/bar/'` e `sed 's/foo/bar/g'`?**
> Senza flag, `s` sostituisce solo la **prima occorrenza** del pattern su ciascuna riga. Con `g` (global) sostituisce **tutte** le occorrenze sulla riga. Esempio: `echo "foo foo foo" | sed 's/foo/bar/'` → `bar foo foo`; con `/g` → `bar bar bar`.

> **D: Come modifichi un file in-place preservando un backup?**
> `sed -i.bak 's/old/new/g' file.txt`. GNU sed crea `file.txt.bak` con il contenuto originale e modifica `file.txt`. Su macOS (BSD sed) la sintassi è la stessa ma il suffisso è obbligatorio anche se vuoto: `sed -i '' 's/old/new/'`.

> **D: Come cancelli tutte le righe vuote e i commenti da un file di configurazione?**
> `sed '/^\s*#/d; /^\s*$/d' file.conf`. Il primo comando cancella le righe che iniziano con `#` (eventualmente preceduto da spazi); il secondo cancella le righe vuote o con soli spazi. I due comandi possono essere concatenati con `;` oppure dati separatamente con `-e`.

> **D: Come estrai le righe dalla 10 alla 20 di un file di log senza head/tail?**
> `sed -n '10,20p' file.log`. Il flag `-n` sopprime l'output di default; `p` stampa le righe nell'intervallo specificato. Alternativa con pattern: `sed -n '/timestamp_start/,/timestamp_end/p' file.log`.

> **D: Come usi sed per rimuovere i codici colore ANSI dall'output di un tool?**
> `sed 's/\x1b\[[0-9;]*m//g'`. Questo pattern matcha le sequenze di escape ANSI (`ESC[...m`) usate per i colori nel terminale. Utile quando si salva l'output di tool come `nmap`, `linpeas`, `gobuster` su file e si vuole parsare il testo senza artefatti.

> **D: Come sostituisci un pattern che contiene slash senza fare escaping?**
> Cambiando il delimitatore del comando `s`. Il carattere immediatamente dopo `s` diventa il delimitatore: `sed 's|/usr/bin|/usr/local/bin|g'` oppure `sed 's@/usr@/opt@g'`. Qualunque carattere non speciale può fungere da delimitatore.

---

## Collegamenti

- [[awk]]
- [[grep]]
- [[Pipe e Redirezione]]
- [[Bash Scripting]]
- [[Log Analysis]]
- [[Comandi Linux di Base]]
- [[Permessi Linux]]

## Fonti

- Man page sed: https://man7.org/linux/man-pages/man1/sed.1.html
- GNU sed manual: https://www.gnu.org/software/sed/manual/sed.html
- The Linux Command Line – sed: https://linuxcommand.org/tlcl.php
