---
tipo: fonte
tag: [linux]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
url: http://linuxcommand.org
autore: William E. Shotts Jr.
aliases: ["The Linux Command Line", "TLCL"]
---

# Fonte - The Linux Command Line (W. Shotts)

## Panoramica

*The Linux Command Line* (TLCL), di **William E. Shotts Jr.** (LinuxCommand.org / No Starch Press, 5ª Internet Edition, 2019), è un'introduzione completa e progressiva all'uso della **shell bash** su sistemi Linux. Il libro parte da zero (cos'è una shell) e arriva fino allo scripting avanzato, coprendo ~38 capitoli in 4 parti. Il filo conduttore è la filosofia Unix: **"tutto è un file"**, strumenti piccoli e componibili tramite pipe, e l'idea che la CLI non è un residuo del passato ma lo strumento più potente e flessibile per controllare il sistema. [Fonte: TLCL, Introduzione]

## Audience

- Nuovi utenti Linux che migrano da Windows/macOS e vogliono capire *come funziona davvero* il sistema.
- Sviluppatori e aspiranti sysadmin che devono lavorare su server headless (senza GUI).
- Chiunque voglia automatizzare task ripetitivi con script bash.
- **Non** richiede conoscenze di programmazione pregresse; richiede solo un sistema Linux su cui sperimentare. [Fonte: TLCL, "Who Should Read This Book"]

## 5 Insight non ovvi

1. **La shell è sia interfaccia sia linguaggio.** Quasi tutto ciò che si fa interattivamente si può scrivere in uno script, e viceversa: imparare la CLI *è* imparare a programmare il sistema. [Fonte: TLCL, cap. 24]
2. **stdout e stderr sono flussi separati.** `cmd > file` cattura solo l'output normale; gli errori restano a schermo finché non li si redirige esplicitamente con `2>` o `&>`. Capire i file descriptor 0/1/2 è la chiave della redirezione. [Fonte: TLCL, cap. 6]
3. **L'operatore `>` distrugge file silenziosamente.** `ls > less` dentro `/usr/bin` sovrascrive il programma `less`. La redirezione va trattata con rispetto; preferire `>>` quando si vuole accodare. [Fonte: TLCL, cap. 6]
4. **`kill` non "uccide": invia segnali.** Il default è `TERM` (15), che un programma può intercettare per fare cleanup; `KILL` (9) è gestito dal kernel e non lascia scampo, va usato solo come ultima risorsa. [Fonte: TLCL, cap. 10]
5. **I permessi ottali mappano sul binario.** Ogni cifra ottale (0-7) = 3 bit rwx. Conoscere 7=rwx, 6=rw-, 5=r-x, 4=r-- basta per il 95% dei casi; `umask` *sottrae* bit dai permessi di default. [Fonte: TLCL, cap. 9]

## Mappa dei capitoli (1 riga per capitolo)

**Parte 1 — Learning the Shell**
1. What Is the Shell? — terminale, prompt, bash, history, primi comandi (`date`, `cal`, `df`, `free`). [[Shell e Bash]]
2. Navigation — albero del filesystem, `pwd`/`cd`/`ls`, path assoluti vs relativi. [[Filesystem Linux]]
3. Exploring the System — `ls -l`, `file`, `less`, tour della FHS, link simbolici/hard. [[Filesystem Linux]]
4. Manipulating Files — wildcard, `mkdir`/`cp`/`mv`/`rm`/`ln`, "playground".
5. Working with Commands — `type`/`which`/`help`/`man`/`apropos`/`info`, alias. [[Shell e Bash]]
6. Redirection — stdin/stdout/stderr, `>`/`>>`/`|`/`2>&1`, `cat`/`sort`/`uniq`/`grep`/`wc`/`tee`. [[Redirezione e Pipeline]]
7. Seeing the World as the Shell Sees It — espansioni (pathname, tilde, brace, parametri), quoting. [[Shell e Bash]]
8. Advanced Keyboard Tricks — editing readline, completion, history (`Ctrl-r`). [[Shell e Bash]]
9. Permissions — utenti/gruppi/world, rwx, `chmod` ottale/simbolico, `umask`, `su`/`sudo`/`chown`. [[Permessi dei File]]
10. Processes — `ps`/`top`, job control (`&`/`bg`/`fg`/`jobs`), segnali, `kill`/`killall`. [[Processi e Job Control]]

**Parte 2 — Configuration and the Environment**
11. The Environment — `printenv`/`set`/`export`, variabili shell vs ambiente, file di startup. [[Shell e Bash]]
12. A Gentle Introduction to vi — modi di vim, navigazione, editing, search-and-replace. [[Vim e Editor]]
13. Customizing the Prompt — anatomia di `PS1`, colori, escape.

**Parte 3 — Common Tasks and Essential Tools**
14. Package Management — `.deb` vs `.rpm`, `apt`/`dpkg`, `yum`/`dnf`/`rpm`, repository, dipendenze. [[Gestione Pacchetti]]
15. Storage Media — `mount`/`umount`, `fdisk`, `mkfs`, `fsck`, `dd`, immagini ISO.
16. Networking — `ping`/`traceroute`/`ip`/`netstat`, `ftp`/`wget`, `ssh`/`scp`/`sftp`, tunnel. [[Tool di Rete]] [[SSH]]
17. Searching for Files — `locate`, `find` (test/operatori/azioni), `xargs`.
18. Archiving and Backup — `gzip`/`bzip2`, `tar`/`zip`, `rsync`.
19. Regular Expressions — `grep`, metacaratteri, ancore, classi POSIX, BRE vs ERE, quantificatori.
20. Text Processing — `cat`/`sort`/`uniq`/`cut`/`paste`/`join`/`comm`/`diff`/`patch`/`tr`/`sed`.
21. Formatting Output — `nl`/`fold`/`fmt`/`pr`/`printf`, `groff`.
22. Printing — `pr`/`lpr`/`lp`/`lpstat`/`lpq`/`lprm`.
23. Compiling Programs — `make`, `./configure`, build di un programma C da sorgente.

**Parte 4 — Writing Shell Scripts**
24. Writing Your First Script — shebang `#!/bin/bash`, permessi eseguibili, `PATH`, `~/bin`. [[Scripting Bash]]
25. Starting a Project — variabili e costanti, here-documents (`<<`). [[Scripting Bash]]
26. Top-Down Design — funzioni shell, variabili locali, `declare`. [[Scripting Bash]]
27. Flow Control: if — exit status (`$?`), `test`/`[ ]`/`[[ ]]`/`(( ))`, operatori `&&`/`||`. [[Scripting Bash]]
28. Reading Keyboard Input — `read`, validazione, IFS, menu.
29. Flow Control: while/until — loop, `break`/`continue`, lettura file con loop. [[Scripting Bash]]
30. Troubleshooting — errori sintattici/logici, defensive programming, tracing (`set -x`). [[Scripting Bash]]
31. Flow Control: case — branching multiplo con pattern. [[Scripting Bash]]
32. Positional Parameters — `$1`..`$9`, `$#`, `$@`/`$*`, `shift`, `getopts`. [[Scripting Bash]]
33. Flow Control: for — forma tradizionale e forma C, iterazione su liste. [[Scripting Bash]]
34. Strings and Numbers — parameter expansion avanzata, aritmetica `(( ))`, `bc`.
35. Arrays — array indicizzati e associativi.
36. Exotica — group commands, subshell, process substitution, trap, async.

## Collegamenti
- [[index]]
- Pagina di sintesi del topic: [[Linux Essentials]]
- Concetti fondamentali: [[Shell e Bash]], [[Filesystem Linux]], [[Permessi dei File]], [[Processi e Job Control]], [[Redirezione e Pipeline]], [[Scripting Bash]]

## Fonti
- [TLCL — The Linux Command Line, W. Shotts, 5th Internet Edition, 2019] — interi capitoli 1-36.
- Sito di accompagnamento: <http://linuxcommand.org>
