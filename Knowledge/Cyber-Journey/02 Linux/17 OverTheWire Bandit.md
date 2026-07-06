---
tipo: entita
tag: [linux, ctf, wargame]
fase: 1
fonti: 2
aggiornato: 2026-07-02
stato: maturo
aliases: ["OverTheWire Bandit"]

---

# OverTheWire Bandit

## In breve

**OverTheWire Bandit** è un wargame online gratuito e sempre disponibile (34 livelli via SSH) pensato per chi parte da zero con Linux e la sicurezza. È il punto d'ingresso classico prima di [[TryHackMe]] e [[HackTheBox]]: allena in modo incrementale comandi, pipe, codifiche, rete e le basi di [[Privilege Escalation Linux|privesc]] risolvendo un livello per trovare la password del successivo.

## Cos'è

**OverTheWire Bandit** è un wargame (CTF online sempre disponibile, gratuito, nessuna registrazione) progettato specificamente per chi inizia da zero con Linux e la sicurezza informatica. Ogni livello presenta un sistema a cui connettersi via SSH: si trovano la password del livello successivo sfruttando comandi Linux sempre più avanzati. A differenza dei CTF a tempo, Bandit è disponibile 24/7 e i livelli non cambiano — è un percorso di apprendimento permanente.

**URL ufficiale**: https://overthewire.org/wargames/bandit/

---

## Come funziona: struttura e connessione

```bash
# Connessione al livello 0 (punto di partenza assoluto)
ssh bandit0@bandit.labs.overthewire.org -p 2220
# password: bandit0

# Connessione ai livelli successivi (N = numero del livello)
ssh banditN@bandit.labs.overthewire.org -p 2220

# Con chiave SSH (alcuni livelli la richiedono)
ssh -i ./sshkey.private -p 2220 banditN@bandit.labs.overthewire.org
```

Ogni livello è un utente separato (`bandit0`, `bandit1`, … `bandit34`). La password per `banditN+1` si trova loggando come `banditN`. Le password sono **stabili** e vanno annotate: non c'è salvataggio tra sessioni.

---

## Mappa dei livelli e skill allenate

### Livelli 0–10: comandi base e navigazione

| Livelli | Tecnica / Concetto | Comandi chiave |
|---------|-------------------|----------------|
| 0 | Connessione SSH, lettura file | `ssh`, `cat`, `ls` |
| 1 | File con nome speciale (`-`) | `cat ./-`, `./` prefisso |
| 2 | Spazi nel nome del file | `cat "spaces in name"`, escape `\` |
| 3 | File nascosto (dotfile) | `ls -la` |
| 4 | Tipo di file: solo human-readable | `file ./-file*`, `cat` |
| 5 | Find per size, human-readable, non eseguibile | `find / -size 1033c ! -executable` |
| 6 | Find per owner e group specifici | `find / -user bandit7 -group bandit6 -size 33c 2>/dev/null` |
| 7 | Grep in file di testo grande | `grep "millionth" data.txt` |
| 8 | Riga presente una sola volta | `sort data.txt | uniq -u` |
| 9 | Stringhe leggibili in file binario | `strings data.txt | grep "==*"` |
| 10 | Decodifica base64 | `base64 -d data.txt` |

### Livelli 11–20: pipe, codifiche e rete

| Livelli | Tecnica / Concetto | Comandi chiave |
|---------|-------------------|----------------|
| 11 | ROT13 | `tr 'A-Za-z' 'N-ZA-Mn-za-m'` |
| 12 | File compresso più volte (gzip, bzip2, tar) | `xxd`, `file`, `gzip -d`, `bzip2 -d`, `tar -xf` |
| 13 | Chiave SSH privata per autenticazione | `ssh -i sshkey.private` |
| 14 | Connessione a porta locale, submit password | `nc localhost 30000` |
| 15 | Connessione SSL/TLS | `openssl s_client -connect localhost:30001` |
| 16 | Port scan locale + SSL su porta giusta | `nmap localhost -p 31000-32000`, `openssl s_client` |
| 17 | Differenza tra due file | `diff passwords.old passwords.new` |
| 18 | .bashrc malevolo: no shell interattiva | `ssh ... "cat readme"` (comando diretto) |
| 19 | Binario SUID di un altro utente | `./bandit20-do cat /etc/bandit_pass/bandit20` |
| 20 | Daemon TCP custom + SUID | `nc -lvnp PORT &` + `./suconnect PORT` |

### Livelli 21–34: scripting, cron, crittografia, git

| Livelli | Tecnica / Concetto | Comandi chiave |
|---------|-------------------|----------------|
| 21-23 | [[Cron e Job Pianificati]] e analisi script | `ls /etc/cron.d/`, `cat`, `bash` |
| 24 | Brute force password 4 cifre via nc | Script Bash/Python loop + `nc` |
| 25-26 | Shell ristretta, escape da `more` | `v` in more → vim → `:!/bin/bash` |
| 27-29 | Git: clone, log, branch, tag | `git clone`, `git log`, `git tag`, `git branch` |
| 30 | Git: stash | `git stash list`, `git stash show` |
| 31 | Git: push con file .gitignore | `git add -f`, `git push` |
| 32 | Uppercase shell: escape con `$0` | `$0` = nome shell corrente → `/bin/sh` |
| 33-34 | Meta-livelli / conclusione | — |

---

## Skill di cybersecurity allenate

### 1. SSH e autenticazione a chiave
Bandit introduce SSH fin dal livello 0 e progressivamente:
- Autenticazione con password.
- Autenticazione con chiave privata (`-i`).
- Comandi remoti senza shell interattiva (`ssh user@host "cmd"`).
- Port non standard (`-p 2220`).
- Configurazione `~/.ssh/config` per semplificare le connessioni.

### 2. Manipolazione di file e filesystem
- File con nomi speciali (iniziano con `-`, contengono spazi, sono nascosti).
- Identificazione tipo file con `file`.
- Ricerca avanzata con `find` (per size, owner, group, permission).
- Comprensione degli inode e dei [[Permessi Linux]].

### 3. Pipe e redirezione
Ogni livello usa pipeline:
```bash
sort data.txt | uniq -u              # livello 8
strings data.txt | grep "==*"       # livello 9
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'  # livello 11
```
È la palestra pratica migliore per [[Pipe e Redirezione]].

### 4. Codifiche e crittografia di base
- **Base64** (livello 10): encoding comune per payload, token, segreti.
- **ROT13** (livello 11): sostituzione monoalfabetica, `tr`.
- **Compressione multipla** (livello 12): gzip, bzip2, tar — come identificare il formato con `file`/`xxd`.
- **SSL/TLS** (livello 15-16): `openssl s_client` per connettersi a servizi cifrati.
- **Hashing** (livello 24 implicito): iterazione per brute force.

### 5. Connessioni di rete e netcat
- `nc localhost PORTA` per comunicare con servizi locali.
- Port scan locale con `nmap`.
- Scrittura di un daemon TCP minimale in Bash.
- Comunicazione bidirezionale con `nc`.

### 6. [[SUID e SGID]] e concetti di privilege escalation
- Livello 19-20: binario SUID che esegue comandi come altro utente.
- Comprensione pratica di come il bit SUID funziona prima di affrontare [[Privilege Escalation Linux]].

### 7. Cron e job pianificati
- Livelli 21-23: analisi di script eseguiti da cron, comprensione del timing e dell'ambiente di esecuzione.

### 8. Git per sicurezza
- Clonare repository, esplorare la history (`git log`), checkout di branch e tag, stash.
- Fondamentale per CTF con source code analysis e per OSINT su repository pubblici.

### 9. Shell escape (jailbreak)
- Livello 25-26: escape da shell ristretta tramite `more` → `vim` → `:!/bin/bash`.
- Livello 32: uppercase shell → `$0` come vettore di escape.
- Tecnica applicabile in contesti reali (restricted shell bypass).

---

## Perché Bandit è propedeutico

### Prima dei CTF avanzati
Bandit è il prerequisito pratico per:
- **TryHackMe** (Starting Point, rooms Linux): Bandit insegna la base prima di affrontare macchine virtuali.
- **HackTheBox** (Starting Point): richiede autonomia su Linux che Bandit costruisce sistematicamente.
- **PicoCTF**: molte challenge usano esattamente le tecniche dei livelli 10-25 di Bandit.

### Metodo di studio consigliato
1. **Prova da solo** almeno 15-20 minuti per livello.
2. **Leggi i suggerimenti** del sito ufficiale (elenco di comandi da studiare, no spoiler).
3. **Usa `man` e `--help`** per ogni comando nuovo: è l'abitudine più utile in assoluto.
4. **Tieni un diario** con password trovate + comando che le ha rivelate.
5. **Dopo aver risolto**, cerca writeup online per scoprire approcci alternativi.

> [!tip] Non cercare subito la soluzione
> Il valore di Bandit è nel **debugging autonomo**. Se si blocca su un livello, rilegi il testo del livello, controlla `man`, prova varianti del comando. La frustrazione produttiva è parte del metodo.

---

## Tecniche pratiche di esempio

### Livello 5 — `find` avanzato
```bash
# File: human-readable, 1033 byte, non eseguibile
find . -type f -size 1033c ! -executable -exec file {} \; | grep text
```

### Livello 12 — decompressione multipla
```bash
cp data.txt /tmp/workdir && cd /tmp/workdir
xxd data.txt | head        # vedi magic bytes
mv data.txt data.gz        # file identifica come gzip
gzip -d data.gz
file data                  # ora è bzip2
bzip2 -d data              # decomprimi
file data.out              # ora è tar
tar -xf data.out           # estrai
# ripeti finché non ottieni ASCII text
```

### Livello 16 — port scan locale + openssl
```bash
nmap -sV localhost -p 31000-32000   # trova la porta con SSL
openssl s_client -connect localhost:31790 -quiet
# invia la password di bandit16, ricevi chiave SSH privata per bandit17
```

### Livello 24 — brute force in Bash
```bash
for i in $(seq 0000 9999); do
  echo "PASSWORDCORRENTE $i"
done | nc localhost 30002 | grep -v "Wrong"
```

### Livello 26 — escape da shell ristretta
```bash
# bandit26 usa /usr/bin/showtext come shell (mostra testo + exit)
# Trick: rimpicciolisci il terminale finché more si ferma
# In more premi 'v' (apre vim)
# In vim: :set shell=/bin/bash → :shell
```

---

## Dopo Bandit: percorso consigliato

```
OverTheWire Bandit (0-34)
    ↓
OverTheWire Natas (web: XSS, SQLi base, PHP)   ← stessa piattaforma
OverTheWire Leviathan (Linux intermedio)        ← stessa piattaforma
    ↓
TryHackMe – Pre-Security / Jr Penetration Tester paths
    ↓
HackTheBox – Starting Point (macchine reali)
```

---

## Sicurezza: perché studiare Bandit è difensivo oltre che offensivo

Le tecniche di Bandit sono **esattamente** quelle usate dagli attaccanti in post-exploitation:
- Trovare file nascosti e con permessi speciali → [[Enumerazione]].
- Leggere `/etc/passwd`, file di configurazione, chiavi SSH.
- Decodificare dati base64 o compressi trovati in un sistema.
- Sfuggire a shell ristrette (hardened user → pivot).

Chi difende un sistema deve sapere cosa cerca un attaccante — Bandit lo insegna sistematicamente dal punto di vista del "trovatore".

---

## Casi limite e troubleshooting

1. **Connessione SSH rifiutata** → Il server può avere picchi di traffico. Riprova dopo qualche minuto. Controlla di usare la porta `2220` (non la standard 22).
2. **Password non funziona al livello successivo** → Bandit resetta periodicamente le password. Se una password salvata non funziona, ri-risolvi il livello precedente per ottenere quella aggiornata.
3. **Shell che esce subito** → Livello 18: `.bashrc` modificato fa uscire immediatamente. Usa `ssh bandit18@... -p 2220 "cat readme"` per eseguire il comando senza avviare la shell interattiva.
4. **`more` non si ferma** → Allarga il terminale: `more` impagina solo se il testo non entra nello schermo. Per il livello 26, **rimpicciolisci** il terminale finché `more` si ferma e aspetta input.
5. **Script di brute force (livello 24) troppo lento** → Usa `printf` invece di `echo` + aggiungi un sleep minimo se il server limita la velocità. Alternativa: Python con socket per maggiore velocità.

---

## Domande da esame / colloquio

> **D: Cos'è OverTheWire Bandit e a che livello è indicato?**
> È un wargame online gratuito e sempre disponibile, pensato per principianti assoluti di Linux e sicurezza. Insegna tramite pratica diretta: ogni livello richiede l'uso di comandi Linux reali per trovare la password del livello successivo. È il primo passo consigliato prima di TryHackMe o HackTheBox.

> **D: Quale skill fondamentale di pentest si allena fin dai primissimi livelli di Bandit?**
> L'uso di `find` con parametri avanzati (size, owner, permission, tipo), la combinazione di comandi in pipeline e la lettura della documentazione via `man`. Sono esattamente le tecniche usate nella fase di enumerazione post-foothold su un target Linux reale.

> **D: Come si affronta il livello 12 di Bandit (file compresso multiple volte)?**
> Si usa `xxd` per leggere i magic bytes e identificare il formato, poi `file` dopo ogni decompressione. Si ciclano `gzip -d`, `bzip2 -d`, `tar -xf` fino a ottenere un file ASCII leggibile. Insegna a riconoscere i formati binari senza fare affidamento sull'estensione.

> **D: Cosa insegna il livello 25-26 di Bandit in termini di sicurezza?**
> Insegna lo **shell escape da shell ristretta**: quando un utente è forzato a usare `more` come shell, premere `v` apre `vim`; da vim si può impostare `:set shell=/bin/bash` e poi `:shell` per ottenere una bash completa. Tecnica applicabile in contesti reali di restricted shell bypass.

---

## Lab

Bandit **è** il lab: praticalo direttamente su `overthewire.org/wargames/bandit/` con questo piano.

- **Sessione 1 — livelli 0-10**: connessione SSH (`-p 2220`), lettura file con nomi ostili, `find` per size/owner/permessi, `grep`, `sort | uniq -u`, `strings`, `base64 -d`. Obiettivo: fluidità coi [[Comandi Linux di Base]] e le [[Pipe e Redirezione]].
- **Sessione 2 — livelli 11-20**: `tr` (ROT13), decompressione multipla (`file`/`xxd` → gzip/bzip2/tar), chiavi SSH, `nc`/`openssl s_client`, `nmap` locale, e i primi [[SUID e SGID]] (livelli 19-20).
- **Sessione 3 — livelli 21-34**: [[Cron e Job Pianificati]] (21-23), brute force in [[Bash Scripting|Bash]] (24), shell escape da `more`/uppercase shell (25-26, 32), Git per la security (27-31).
- **Metodo**: prova ≥15 min da solo, usa `man`/`--help`, tieni un diario password+comando, e solo dopo leggi i writeup per approcci alternativi.
- **Dopo Bandit**: prosegui su [[OverTheWire Bandit|OverTheWire]] Natas/Leviathan, poi [[TryHackMe]] (Pre-Security / Jr Penetration Tester) e [[HackTheBox]] Starting Point.

## Collegamenti

- [[Comandi Linux di Base]]
- [[Pipe e Redirezione]]
- [[grep]]
- [[find]]
- [[Bash Scripting]]
- [[SUID e SGID]]
- [[Cron e Job Pianificati]]
- [[Permessi Linux]]
- [[Enumerazione]]
- [[Privilege Escalation Linux]]

## Fonti

- Sito ufficiale OverTheWire Bandit: https://overthewire.org/wargames/bandit/
- OverTheWire – come funziona (intro): https://overthewire.org/wargames/
