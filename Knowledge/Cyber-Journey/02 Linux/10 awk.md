---
tipo: entita
tag: [linux]
fase: 1
fonti: 3
aggiornato: 2026-06-22
stato: maturo
aliases: ["awk"]

---

# awk

## Cos'è

**awk** è un linguaggio di scripting orientato al testo strutturato in colonne. Legge l'input riga per riga, divide ogni riga in **campi** (field) e applica blocchi di codice condizionati da pattern. Il nome deriva dai cognomi dei suoi creatori: **A**ho, **W**einberger, **K**ernighan (Bell Labs, 1977). Su Linux si usa quasi sempre GNU awk (`gawk`), chiamato semplicemente `awk`.

awk è preferibile a [[grep]] quando servono filtri su colonne specifiche e a [[sed]] quando si vuole calcolare, sommare o riformattare dati strutturati (log, CSV, output di comandi).

---

## Struttura di un programma awk

```
awk 'PATTERN { AZIONE }' file
```

- **PATTERN**: condizione opzionale. Se omessa, l'azione si applica a ogni riga.
- **AZIONE**: blocco di codice tra `{ }`. Può contenere print, calcoli, condizioni.
- Si possono concatenare più regole: `awk 'P1{A1} P2{A2}' file`

Blocchi speciali:
```bash
awk 'BEGIN { ... }     # eseguito PRIMA di leggere qualsiasi riga
     /pattern/ { ... } # eseguito per le righe che matchano il pattern
     END { ... }' file # eseguito DOPO aver letto l'ultimo record
```

---

## Variabili built-in fondamentali

| Variabile | Significato | Default |
|-----------|-------------|---------|
| `$0` | Intera riga (record corrente) | — |
| `$1`, `$2`… `$N` | Campo 1, 2… N | — |
| `$NF` | Ultimo campo della riga | — |
| `$(NF-1)` | Penultimo campo | — |
| `NR` | Numero di record (riga) letti finora | — |
| `NF` | Numero di campi nella riga corrente | — |
| `FS` | Field Separator (separatore input) | spazio/tab |
| `OFS` | Output Field Separator | spazio |
| `RS` | Record Separator | `\n` |
| `ORS` | Output Record Separator | `\n` |
| `FILENAME` | Nome del file in elaborazione | — |
| `FNR` | Numero di record nel file corrente (multi-file) | — |
| `SUBSEP` | Separatore per array multi-dimensionali | `\034` |

---

## Separatori: FS e OFS

```bash
# Separatore con -F (più comodo da riga di comando)
awk -F: '{print $1}' /etc/passwd       # usa ":" come FS
awk -F'\t' '{print $1, $3}' file.tsv  # tab come FS
awk -F'[;,]' '{print $2}' data.csv    # FS è regex: punto e virgola o virgola

# Imposta OFS per riformattare l'output
awk -F: 'BEGIN{OFS=","} {print $1,$3,$7}' /etc/passwd
# Output: root,0,/bin/bash — CSV di utente, UID, shell

# RS per file con record separati da riga vuota (es. blocchi di config)
awk 'BEGIN{RS=""; FS="\n"} {print $1}' blocchi.txt
```

---

## Pattern e filtri

```bash
# Filtra per stringa (regex)
awk '/FAILED/ {print}' /var/log/auth.log
awk '/^root/ {print $0}' /etc/passwd

# Filtra per condizione su campo
awk -F: '$3 == 0 {print $1}' /etc/passwd      # utenti con UID 0 (root)
awk -F: '$3 >= 1000 {print $1}' /etc/passwd   # utenti normali (UID >= 1000)
awk '$9 >= 400 {print $0}' access.log         # richieste con status >= 400

# Negazione
awk '!/^#/ {print}' /etc/ssh/sshd_config      # escludi commenti

# Range di righe (come sed)
awk 'NR>=5 && NR<=10 {print}' file.txt

# Intervallo pattern (dalla riga che matcha P1 alla riga che matcha P2)
awk '/BEGIN_SECTION/,/END_SECTION/ {print}' config.txt
```

---

## Stampa e formattazione

```bash
# print vs printf
awk '{print $1, $2}' file        # print: aggiunge OFS tra campi, ORS a fine riga
awk '{printf "%s\t%s\n", $1, $2}' file   # printf: controllo totale del formato

# Stampa solo alcune colonne di /etc/passwd
awk -F: '{print $1, $3, $7}' /etc/passwd       # utente, UID, shell
awk -F: 'BEGIN{OFS="\t"} {print $1,$3,$7}' /etc/passwd  # tab-separated

# Stampa con etichette
awk -F: '{print "User:", $1, "| UID:", $3, "| Shell:", $7}' /etc/passwd

# Stampa il numero di riga prima del contenuto
awk '{print NR": "$0}' file.txt

# Stampa solo l'ultimo campo di ogni riga
awk '{print $NF}' file.txt

# Stampa dalla colonna 3 in poi
awk '{for(i=3;i<=NF;i++) printf "%s ", $i; print ""}' file.txt
```

---

## Calcoli e aggregazioni

```bash
# Somma di una colonna (es. quinta colonna di ls -l = dimensione file)
ls -l | awk '{sum += $5} END {print "Totale bytes:", sum}'

# Conta le righe che matchano un pattern
awk '/FAILED/ {count++} END {print count, "tentativi falliti"}' /var/log/auth.log

# Media di una colonna
awk '{sum += $3; n++} END {print "Media:", sum/n}' data.txt

# Valore massimo e minimo
awk 'BEGIN{max=0} {if($1>max) max=$1} END{print "Max:", max}' data.txt

# Frequenza: conta quante volte appare ogni valore in una colonna
awk '{count[$1]++} END {for(ip in count) print count[ip], ip}' access.log | sort -rn
```

---

## Uso in sicurezza: /etc/passwd e utenti

```bash
# Utenti con UID 0 (root equivalenti)
awk -F: '$3 == 0 {print "ATTENZIONE: utente root:", $1}' /etc/passwd

# Utenti con shell di login (non /bin/false o /usr/sbin/nologin)
awk -F: '$7 !~ /false|nologin/ {print $1, $7}' /etc/passwd

# Utenti con home directory esistente
awk -F: '$6 != "" && $6 != "/nonexistent" {print $1, $6}' /etc/passwd

# Formato CSV: utente, UID, GID, shell
awk -F: 'BEGIN{OFS=","} {print $1,$3,$4,$7}' /etc/passwd

# Confronta /etc/passwd e /etc/shadow per trovare utenti senza hash
awk -F: '{print $1}' /etc/passwd | while read u; do
  grep -q "^$u:" /etc/shadow || echo "Utente senza shadow: $u"
done
```

---

## Uso in Log Analysis

```bash
# Apache/Nginx access.log: conta richieste per IP
awk '{print $1}' /var/log/apache2/access.log | sort | uniq -c | sort -rn | head -10

# Filtra solo le richieste con status 4xx o 5xx
awk '$9 ~ /^[45]/ {print $1, $9, $7}' access.log

# Estrai URL delle richieste POST
awk '$6 == "\"POST" {print $7}' access.log | sort | uniq -c | sort -rn

# Calcola il traffico totale per IP (somma bytes, campo 10)
awk '{bytes[$1] += $10} END {for(ip in bytes) print bytes[ip], ip}' access.log | sort -rn

# auth.log: IP con più tentativi SSH falliti
awk '/Failed password/ {print $(NF-3)}' /var/log/auth.log | sort | uniq -c | sort -rn

# Estrai timestamp e IP da log SSH
awk '/Failed password/ {print $1, $2, $3, $(NF-3)}' /var/log/auth.log

# Filtra log per intervallo orario (es. 02:00-04:00)
awk -F'[: ]' '$4 >= 2 && $4 <= 4 {print $0}' /var/log/auth.log

# Parsing di output nmap -oG
awk '/open/ {print $2, $5}' scan.gnmap
```

---

## Uso avanzato: array, funzioni, multi-file

```bash
# Array associativo: mappa IP → numero tentativi
awk '/Failed password/ {
  match($0, /from ([0-9.]+)/, arr)
  count[arr[1]]++
} END {
  for (ip in count)
    if (count[ip] > 10) print count[ip], ip, "- possibile brute force"
}' /var/log/auth.log

# Join di due file per campo comune (simile a SQL JOIN)
# file1: utenti con UID; file2: UID con privilegi
awk -F: 'NR==FNR {priv[$3]=$0; next} $3 in priv {print $1, "ha privilegio:", priv[$3]}' \
    privs.txt /etc/passwd

# Funzione definita dall'utente
awk 'function upper(s) {return toupper(s)} {print upper($1)}' file.txt

# Elaborazione multi-file: stampa il nome del file prima di ogni sezione
awk 'FNR==1 {print "=== File:", FILENAME, "==="} {print}' file1.log file2.log

# Contare righe uniche in una colonna senza sort | uniq
awk '!seen[$1]++ {print}' file.txt   # stampa la prima occorrenza di ogni valore $1
```

---

## One-liner utili per pentest e CTF

```bash
# Estrai solo gli IP da output di nmap -sV
nmap -sV 192.168.1.0/24 | awk '/Nmap scan report/ {print $NF}'

# Da gobuster output: estrai solo i path con status 200
gobuster dir -u http://target -w wordlist.txt | awk '$2 == "(Status:" && $3 == "200)" {print $1}'

# Parsing di /etc/shadow: utenti con hash (non bloccati)
awk -F: '$2 !~ /^[*!]/ && $2 != "" {print $1, $2}' /etc/shadow 2>/dev/null

# Estrai IP da output di ifconfig/ip a
ip a | awk '/inet / && !/127.0.0.1/ {print $2}'

# Parsare output di ss per porte in ascolto
ss -tlnp | awk 'NR>1 {print $4}' | awk -F: '{print $NF}' | sort -n

# Da linee di log strutturate JSON-like: estrai valori
awk -F'"' '/"ip"/ {for(i=1;i<=NF;i++) if($i=="ip") print $(i+2)}' access_json.log
```

---

## Casi limite e gotcha

- **Spazi nel FS**: FS=` ` (default) ha un comportamento speciale — gestisce multipli spazi/tab come separatore singolo e ignora gli spazi iniziali. Se usi `FS=" "` esplicitamente si comporta diversamente da `FS=/[ \t]+/`.
- **Numeri come stringhe**: awk fa confronti numerici se entrambi i lati sembrano numeri, stringa altrimenti. `$3 == "0"` e `$3 == 0` si comportano diversamente su campo con valore `"0"` vs `"00"`.
- **Array non ordinati**: gli array associativi in awk non hanno ordine garantito nel ciclo `for(k in arr)`. Per output ordinato pipe verso `sort`.
- **`print` vs `printf`**: `print` aggiunge ORS (default `\n`) automaticamente; `printf` no. Mescolarli può dare output con righe doppie o mancanti.
- **Regex nel pattern vs nella condizione**: `/regex/ {print}` matcha sull'intera riga `$0`; `$3 ~ /regex/ {print}` matcha solo sul campo 3.
- **Campi numerici con virgola**: se i numeri usano la virgola come decimale (locale europea), awk potrebbe non riconoscerli come numeri. Imposta `LC_ALL=C` o sostituisci con `gsub(/,/, ".", $3)`.
- **OFMT e CONVFMT**: awk usa `OFMT="%.6g"` per la rappresentazione dei float in output e `CONVFMT` per le conversioni interne. Se hai bisogno di precisione esplicita, usa `printf "%.2f"`.

---

## Domande da esame/colloquio

> **D: Qual è la differenza tra NR e FNR?**
> `NR` è il numero totale di record letti dall'inizio dell'esecuzione (cresce attraverso più file). `FNR` è il numero di record nel file corrente (si azzera all'inizio di ogni file). Usato tipicamente nel pattern `NR==FNR` per identificare il primo file in un'operazione di join: `awk 'NR==FNR {a[$1]=$2; next} $1 in a {print}' file1 file2`.

> **D: Come si fa un join tra due file con awk?**
> Si usa il pattern `NR==FNR` per caricare il primo file in un array associativo, poi per il secondo file si controlla se il campo chiave è nell'array: `awk 'NR==FNR {map[$1]=$2; next} $1 in map {print $0, map[$1]}' file1 file2`.

> **D: Come conti le righe che matchano un pattern senza usare grep | wc -l?**
> `awk '/pattern/ {count++} END {print count}' file`. Più efficiente perché è una singola passata senza pipe.

> **D: Come estrai IP con più di 100 tentativi di login falliti da auth.log?**
> `awk '/Failed password/ {ip[$(NF-3)]++} END {for(i in ip) if(ip[i]>100) print ip[i], i}' /var/log/auth.log | sort -rn`. Prima si accumula il conteggio per IP in un array associativo, poi nel blocco END si filtra per soglia.

> **D: Differenza tra awk e sed per elaborare un log?**
> `sed` è ottimale per trasformazioni su righe intere o sostituzioni con regex (s///). `awk` è ottimale quando si lavora con colonne strutturate: somme, conteggi, filtri su campo N, join. In pipeline si usano spesso insieme: `grep "Failed" auth.log | awk '{print $11}' | sort | uniq -c`.

> **D: Come stampi solo le righe uniche di una colonna senza sort | uniq?**
> `awk '!seen[$1]++' file.txt`. L'espressione `!seen[$1]++` è falsa (quindi la riga non viene stampata) se `seen[$1]` era già > 0; altrimenti è vera e incrementa il contatore. Questo preserva l'ordine di prima apparizione, a differenza di `sort | uniq`.

---

## Collegamenti

- [[sed]]
- [[grep]]
- [[Pipe e Redirezione]]
- [[Bash Scripting]]
- [[Log Analysis]]
- [[Comandi Linux di Base]]
- [[Enumerazione]]
- [[Privilege Escalation Linux]]

## Fonti

- Man page awk (gawk): https://man7.org/linux/man-pages/man1/gawk.1.html
- The GNU Awk User's Guide: https://www.gnu.org/software/gawk/manual/gawk.html
- The Linux Command Line – awk: https://linuxcommand.org/tlcl.php
