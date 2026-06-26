---
tipo: concetto
tag: [linux]
fase: 1
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Vim e Nano", "Vim", "nano", "Vim e Editor"]
---

# Vim e Nano

## In breve

Modificare file di testo (config, script, log) dalla CLI è un'attività quotidiana, e su un server **headless** o via [[SSH]] non c'è una GUI. I due editor da terminale fondamentali sono **Vim** (potente, modale) e **nano** (semplice, immediato).

**Perché imparare Vim**: (1) è **quasi sempre presente** — lo standard **POSIX** richiede `vi`, mentre nano non è universale; è un salvavita su server remoti o sistemi con GUI rotta. (2) È **leggero e veloce**, progettato per non staccare mai le mani dalla tastiera. Nato nel 1976 da Bill Joy, oggi le distro spediscono **Vim** ("vi improved" di Bram Moolenaar), di solito collegato all'alias `vi`.

---

## Vim è modale — il concetto chiave

A differenza di ogni editor "normale", in Vim i tasti fanno cose diverse a seconda della **modalità**:

| Modalità | Come entrarci | A cosa serve |
|----------|---------------|--------------|
| **Normal** (comandi) | `Esc` | navigare e impartire comandi (modalità di default) |
| **Insert** (inserimento) | `i` `a` `o` | digitare testo come in un editor normale |
| **Visual** (selezione) | `v` `V` `Ctrl-v` | selezionare testo (caratteri/righe/blocchi) |
| **Command-line** (ex) | `:` | comandi su riga: salva, esci, cerca-sostituisci |

> [!tip] Regola di sopravvivenza
> Se sei "perso", premi **`Esc` due volte** per tornare in Normal mode. Da lì: `:q` esce, `:q!` esce **scartando** le modifiche, `:wq` (o `ZZ`) salva ed esce.

### Comandi essenziali (Normal mode)

```
Movimento:   h j k l   (←↓↑→)   w/b parola avanti/indietro   0/$ inizio/fine riga
             gg / G    inizio / fine file        :42  vai alla riga 42
Inserimento: i  prima del cursore     a  dopo      o  nuova riga sotto      A  fine riga
Modifica:    x  cancella carattere    dd  cancella riga    dw  cancella parola
             yy  copia riga (yank)     p  incolla     u  undo     Ctrl-r  redo
             cw  cambia parola         r  sostituisci 1 carattere    .  ripeti ultimo comando
```

I comandi si **compongono** con conteggi e movimenti (operatore + moto): `3dd` cancella 3 righe, `d$` cancella fino a fine riga, `2yw` copia 2 parole. È questa "grammatica" a rendere Vim potente.

### Ricerca e sostituzione

```
/testo      cerca in avanti (n = prossimo, N = precedente)
?testo      cerca all'indietro
:%s/vecchio/nuovo/g     sostituisce in tutto il file (g = tutte le occorrenze per riga)
:%s/vecchio/nuovo/gc    ...chiedendo conferma a ogni occorrenza (c)
```

Vim incorpora il line editor **ex**, da cui i comandi `:`.

---

## nano — l'alternativa semplice

`nano file` apre un editor immediato, non modale: si digita e basta. I comandi sono in fondo allo schermo, con `^` = `Ctrl`:

```
^O  salva (WriteOut)     ^X  esci      ^W  cerca      ^K  taglia riga    ^U  incolla
^G  aiuto                ^_  vai a riga            ^\  cerca-e-sostituisci
```

Ideale per modifiche rapide e per chi inizia; spesso è l'editor di default di `git`/`crontab` su Ubuntu.

---

## Esempio pratico

```bash
# Modificare una config di sistema con Vim
sudo vi /etc/ssh/sshd_config
#   /PermitRootLogin   ← cerca la riga
#   cw  poi digita 'no'  Esc   ← cambia la parola
#   :wq                  ← salva ed esci

# Modifica rapida con nano (più semplice)
nano ~/.bashrc
#   ...scrivi...  Ctrl-O  Invio (salva)  Ctrl-X (esci)

# Configurare Vim moderno (disattiva compatibilità vi)
echo "set nocompatible" >> ~/.vimrc
```

---

## Comandi chiave

| Comando | Funzione |
|---------|----------|
| `vi` / `vim file` | apre Vim (Normal mode) |
| `Esc` → `:w` `:q` `:wq` `:q!` | salva / esci / salva+esci / esci scartando |
| `i a o` · `Esc` | entra in Insert · torna in Normal |
| `dd yy p` · `u` `Ctrl-r` | cancella/copia riga, incolla · undo/redo |
| `/pat` `n` · `:%s/a/b/g` | cerca · sostituisci globale |
| `nano file` | editor semplice non modale |
| `^O ^X ^W ^K` (nano) | salva / esci / cerca / taglia |
| `vimtutor` | tutorial interattivo di Vim (30 min) |

---

## Best Practice e note di sicurezza

- **Impara almeno il minimo di Vim** anche se preferisci nano: su un server remoto o in un container minimale potresti trovare *solo* `vi` (POSIX lo garantisce, nano no). Saper entrare/uscire e fare una modifica base è una competenza di sopravvivenza.
- **Usa `vimtutor`** per le basi (30 minuti guidati) prima di buttarti nella configurazione: la curva ripida di Vim è soprattutto all'inizio.
- **Per modifiche rapide e occasionali, nano basta** e riduce gli errori; tieni Vim per editing intensivo dove la composizione dei comandi paga.
- Personalizza con un **`~/.vimrc`** essenziale (`set number`, `syntax on`, `set expandtab tabstop=4`, `set nocompatible`) anziché plugin pesanti.
- Verifica **quale editor usa `git`/`sudoers`**: `git config --global core.editor "vim"` (o `nano`) evita sorprese; `visudo` rispetta `$EDITOR`.
- **Privilege escalation (pentest)**: molti editor sono in [GTFOBins](https://gtfobins.github.io). Se `vi`/`vim`/`nano` è eseguibile via `sudo` o è SUID, si ottiene una shell: in Vim `:!sh` o `:set shell=/bin/sh` poi `:shell`; in nano `^R^X` (read/execute command). Vedi [[SUID e SGID]] e [[Privilege Escalation Linux]].
- Alternative moderne (Neovim, Helix, micro) offrono UX migliori, ma la portabilità di `vi`/`nano` resta imbattuta su sistemi non controllati da te.

---

## Collegamenti

- [[Comandi Linux di Base]]
- [[SSH]]
- [[Bash Scripting]]
- [[Permessi Linux]]
- [[SUID e SGID]]
- [[Privilege Escalation Linux]]

## Fonti

- The Linux Command Line (W. Shotts), Cap. 12 "A Gentle Introduction to vi": https://linuxcommand.org/tlcl.php
- vimtutor; man nano; https://www.vim.org
