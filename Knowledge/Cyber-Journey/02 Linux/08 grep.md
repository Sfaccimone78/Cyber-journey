---
tipo: entita
tag: [linux]
fase: 1
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["grep"]

---

# grep

## In breve

**grep** (Global Regular Expression Print) è un comando Linux per cercare righe che corrispondono a un pattern di testo (o espressione regolare) all'interno di uno o più file, oppure nell'output di altri comandi tramite [[Pipe e Redirezione]]. È uno degli strumenti più usati nell'analisi di log, nell'[[Enumerazione]] di sistemi e nei CTF.

grep esiste in tre varianti: `grep` (BRE, Basic Regular Expressions), `egrep` / `grep -E` (ERE, Extended), `fgrep` / `grep -F` (stringhe fisse, no regex). Su GNU/Linux è quasi sempre GNU grep, che supporta anche PCRE con il flag `-P`.

---

## Flag principali

| Flag | Significato | Esempio |
|------|-------------|---------|
| `-i` | Case-insensitive | `grep -i "password" config.php` |
| `-r` / `-R` | Ricerca ricorsiva in directory | `grep -r "secret" /var/www/` |
| `-n` | Mostra il numero di riga | `grep -n "error" syslog` |
| `-v` | Inverti: righe che NON matchano | `grep -v "^#" sshd_config` |
| `-l` | Solo nomi dei file con match | `grep -rl "token" /etc/` |
| `-L` | Solo nomi dei file SENZA match | `grep -rL "AllowRoot" /etc/ssh/` |
| `-c` | Conta le righe che matchano | `grep -c "Failed" auth.log` |
| `-o` | Stampa solo la parte matchata | `grep -oE "\b[0-9]{1,3}(\.[0-9]{1,3}){3}\b" access.log` |
| `-E` | Regex estese (ERE) | `grep -E "root\|admin" /etc/passwd` |
| `-P` | PCRE (Perl-Compatible) | `grep -P "(?<=UID=)\d+" audit.log` |
| `-F` | Stringa fissa (no regex, più veloce) | `grep -F "404" access.log` |
| `-w` | Parola intera (word boundary) | `grep -w "root" /etc/passwd` |
| `-x` | Riga intera deve matchare | `grep -x "root:.*" /etc/passwd` |
| `-A N` | N righe **dopo** il match | `grep -A 3 "FAILED" auth.log` |
| `-B N` | N righe **prima** del match | `grep -B 2 "FAILED" auth.log` |
| `-C N` | N righe di contesto (prima e dopo) | `grep -C 2 "FAILED" auth.log` |
| `-m N` | Fermati dopo N match | `grep -m 5 "root" /etc/passwd` |
| `-a` | Tratta file binari come testo ASCII | `grep -a "flag{" chall.bin` |
| `-q` | Silenzioso (solo exit code) | `grep -q "root" /etc/passwd && echo trovato` |
| `-s` | Sopprimi errori (file non leggibili) | `grep -rs "pass" /etc/ 2>/dev/null` |
| `--color` | Evidenzia il match a colori | `grep --color "ERROR" app.log` |
| `-z` | Separatore NUL tra record (file 0-terminati) | `grep -z "pattern" nullterm_file` |

---

## Espressioni regolari: BRE vs ERE vs PCRE

### BRE (default `grep`)
```bash
# Metacaratteri base: . ^ $ * [ ] \
grep "^root"         /etc/passwd   # riga che inizia con "root"
grep "bash$"         /etc/passwd   # riga che finisce con "bash"
grep "ro\{2,4\}t"   file.txt      # root, roooot ecc. (BRE: le {} vanno escapate)
grep "[0-9]\{3\}"   file.txt      # tre cifre consecutive
```

### ERE (`grep -E` o `egrep`)
```bash
# Le {} e () non richiedono escape
grep -E "root|admin"             /etc/passwd   # alternativa
grep -E "^(root|daemon):"        /etc/passwd   # gruppo
grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" access.log  # IPv4 greedy
grep -E "(FAILED|Invalid|error)" /var/log/auth.log
```

### PCRE (`grep -P`)
```bash
# Lookahead, lookbehind, \d, \w, \s, quantificatori non-greedy
grep -P "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"  access.log   # IPv4 con \d
grep -P "(?<=password=)\S+"                      config.txt  # parola dopo "password="
grep -P "(?i)secret"                             file.txt    # case-insensitive inline
grep -P "Bearer\s+[A-Za-z0-9\-._~+/]+=*"        headers.txt # JWT/Bearer token
```

---

## Uso in sicurezza: enumerazione e ricerca di credenziali

```bash
# Ricerca ricorsiva di stringhe sensibili (prima cosa su un target)
grep -r "password" / 2>/dev/null
grep -r "secret\|token\|api_key\|passwd\|credential" /var/www/ 2>/dev/null

# Trovare file .env o .config con credenziali
grep -rl "DB_PASSWORD\|SECRET_KEY" / 2>/dev/null

# Estrarre solo i valori dopo "password=" (output pulito)
grep -oP "(?<=password=)\S+" /var/www/html/config.php

# Cercare chiavi private SSH nei file
grep -r "BEGIN RSA PRIVATE KEY\|BEGIN OPENSSH PRIVATE KEY" / 2>/dev/null

# Cercare hash in file shadow/passwd
grep -v "*\|!" /etc/shadow 2>/dev/null   # utenti con hash reale (no lock)

# Utenti con shell di login (per pivoting)
grep -E "/bin/(ba)?sh$" /etc/passwd
```

---

## Uso in Log Analysis

```bash
# Tentativi di login SSH falliti
grep "Failed password" /var/log/auth.log

# Mostra IP attaccante + contesto (3 righe)
grep -C 3 "Failed password" /var/log/auth.log

# Conta gli attacchi per IP (poi si passa ad awk per aggregare)
grep -oP "from \K\S+" /var/log/auth.log | sort | uniq -c | sort -rn

# Richieste HTTP con codice 404/500
grep -E " (404|500) " /var/log/apache2/access.log

# Estrai solo gli IP che hanno generato 401 (Unauthorized)
grep " 401 " access.log | grep -oE "^[0-9.]+"

# Log con sudo: chi ha elevato i privilegi
grep "sudo" /var/log/auth.log | grep -v "pam_unix"

# Cercare errori in log di più servizi contemporaneamente
grep -rh "ERROR\|CRITICAL" /var/log/{apache2,nginx,mysql}/ 2>/dev/null
```

---

## CTF e analisi di file

```bash
# Trovare flag in tutti i file di una directory
grep -r "HTB{" .
grep -r "flag{" . 2>/dev/null

# Cercare in file binari (dump di memoria, immagini, eseguibili)
grep -a "flag{\|password\|secret" dump.bin

# Estrazione di email da un file di testo
grep -oE "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" emails.txt

# Estrazione di URL
grep -oP "https?://\S+" file.txt

# Estrarre indirizzi IPv4 da un log
grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" access.log | sort -u
```

---

## Pipeline avanzate

```bash
# Da output nmap grepping: host con porta 22 aperta (formato -oG)
grep "22/open" scan.gnmap | grep -oP "\d+\.\d+\.\d+\.\d+"

# Filtrare l'output di ps per processi sospetti
ps aux | grep -E "(nc|ncat|python|perl|ruby) .*(-e|-c|/dev/tcp)"

# Cercare configurazioni con PasswordAuthentication abilitato
grep -rn "^PasswordAuthentication yes" /etc/ssh/

# Trovare file PHP con exec/shell_exec/system (webshell hunting)
grep -rl "shell_exec\|exec\|system\|passthru" /var/www/ 2>/dev/null

# Combinare con find per cercare solo in file .log modificati di recente
find /var/log -name "*.log" -mmin -60 -exec grep -l "error" {} \;
```

---

## Casi limite e gotcha

- **File binari**: per default grep avverte "binary file matches" e non stampa il contenuto. Usa `-a` per forzare il trattamento come testo, `--binary-files=text` come alternativa.
- **Newline nei pattern**: grep per default matcha riga per riga. Per pattern multi-riga usa `grep -P` con lookahead o `pcregrep -M`, oppure `awk`/`sed`.
- **Caratteri speciali nel pattern**: `.`, `*`, `[`, `]`, `\`, `^`, `$` sono metacaratteri. Per cercarli letteralmente: escapa con `\` o usa `-F` (stringa fissa).
- **`grep -r` vs `grep -R`**: `-R` segue i symlink; `-r` no. Importante su sistemi con link a `/proc` o `/sys` per evitare loop infiniti.
- **Performance**: su file grandi, `-F` (stringa fissa) è molto più veloce di una regex. Evita `.*` iniziale nei pattern ERE perché forza un backtracking esteso.
- **`2>/dev/null`**: sempre aggiungerlo in ricerche su `/` per sopprimere i "Permission denied" che inquinano l'output.
- **Codifica**: su file UTF-8 con caratteri accentati, imposta `LC_ALL=C` per matching byte-level: `LC_ALL=C grep "pattern" file`.

---

## Strato esperto: tecniche avanzate

```bash
# grep con AND (grep non supporta AND nativo — usa pipe o lookahead PCRE)
grep "admin" /etc/passwd | grep "bash"          # AND con pipe
grep -P "(?=.*admin)(?=.*bash)" /etc/passwd     # AND con lookahead PCRE

# Cerca in più file e mostra il nome del file (-H, default con più file)
grep -H "root" /etc/passwd /etc/shadow 2>/dev/null

# Numerare le occorrenze (non le righe) con -o | nl
grep -o "Failed" /var/log/auth.log | nl

# Estrai blocchi tra due pattern (simile a sed, ma con PCRE multi-riga)
# Alternativa: usa awk '/START/,/END/'
grep -Pzo "(?s)-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----" file.pem

# Ricerca in archivi compressi senza decomprimere
zgrep "pattern" /var/log/syslog.2.gz
bzgrep "pattern" file.bz2

# ripgrep (rg) — alternativa ultra-veloce, stessa sintassi di base
rg "pattern" /var/www/ --type php
```

---

## Lab

- **OverTheWire — Bandit** (livelli 5-12): filtraggio di contenuti e ricerca di pattern in molti file.
- **TryHackMe — Linux Fundamentals Part 2**: uso di `grep` per analisi file e log.
- **TryHackMe — Splunk / Intro to Logs**: parte di triage testuale dove `grep` su access/auth log individua attacchi.

## Domande da esame/colloquio

> **D: Qual è la differenza tra `grep -E` e `grep -P`?**
> `-E` abilita ERE (Extended Regular Expressions): supporta `+`, `?`, `|`, `()` senza escape, ma non lookahead/lookbehind. `-P` abilita PCRE (Perl-Compatible): aggiunge `\d`, `\w`, `\s`, lookahead `(?=...)`, lookbehind `(?<=...)`, quantificatori non-greedy `*?`. PCRE è più potente ma non disponibile su tutti i sistemi (es. macOS grep non supporta `-P`, serve `grep -E` o installare `ggrep`).

> **D: Come estrai solo la parte del testo che matcha il pattern, senza stampare l'intera riga?**
> Con il flag `-o` (only-matching). Esempio: `grep -oE "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" access.log` estrae solo gli IPv4. Combinato con `-P` e lookbehind si possono estrarre valori dopo un prefisso noto senza includerlo.

> **D: Come cerchi AND tra due pattern con grep?**
> grep non supporta AND nativamente. Le opzioni sono: doppia pipe (`grep "A" file | grep "B"`), o PCRE con lookahead positivo (`grep -P "(?=.*A)(?=.*B)" file`). Per OR si usa `-E` con `|`: `grep -E "A|B" file`.

> **D: Perché in una ricerca su tutto il filesystem aggiungi sempre `2>/dev/null`?**
> I file in `/proc`, `/sys`, device files e directory senza permesso di lettura generano centinaia di messaggi "Permission denied" sullo stderr che si mischiano all'output utile. Redirigendo stderr a `/dev/null` si ottiene solo l'output rilevante. In alternativa si può usare `-s` (suppress errors), ma `2>/dev/null` è più universale.

> **D: Come usi grep per trovare webshell in un server web compromesso?**
> Cerchi le funzioni PHP di esecuzione comandi: `grep -rl "shell_exec\|exec\|system\|passthru\|eval.*base64" /var/www/ 2>/dev/null`. Poi esamini i file trovati per capire se il codice è legittimo o iniettato. Puoi anche cercare pattern obfuscati: `grep -r "base64_decode" /var/www/`.

> **D: Qual è la differenza tra `-r` e `-R` in grep ricorsivo?**
> `-r` non segue i symlink; `-R` li segue. Su sistemi con `/proc` linkato o con directory come `/dev`, usare `-R` può causare loop o letture interminabili. Per ricerche sicure su filesystem di produzione, preferire `-r` con `2>/dev/null`.

---

## Collegamenti

- [[Pipe e Redirezione]]
- [[find]]
- [[awk]]
- [[sed]]
- [[Log Analysis]]
- [[Enumerazione]]
- [[Bash Scripting]]
- [[Privilege Escalation Linux]]
- [[Comandi Linux di Base]]

## Fonti

- Man page grep: https://man7.org/linux/man-pages/man1/grep.1.html
- The Linux Command Line – Searching for Text: https://linuxcommand.org/tlcl.php
- OverTheWire Bandit (livelli con grep): https://overthewire.org/wargames/bandit/
