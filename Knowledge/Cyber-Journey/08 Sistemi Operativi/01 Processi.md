---
tipo: concetto
tag: [os]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Processi"]
---

# Processi: PCB, Context Switch, fork/exec

## Definizione
Un **processo** e l'astrazione di un programma in esecuzione: non il file su disco, ma l'istanza viva con il suo stato. Lo stato di un processo (*machine state*) comprende: lo **spazio di indirizzi** (memoria: code, heap, stack), i **registri** della CPU (in particolare il **Program Counter/PC** e lo **stack pointer**), e l'insieme dei **file aperti** (descrittori I/O). [Fonte: OSTEP, cap. 4]

L'OS virtualizza la CPU via **time-sharing**: alterna l'esecuzione di molti processi su pochi core, creando l'illusione di tante CPU virtuali. *Crux: come fornire l'illusione di un numero quasi infinito di CPU?* [Fonte: OSTEP, cap. 4]

## Meccanismo

### PCB (Process Control Block)
L'OS tiene per ogni processo una struttura C chiamata **PCB** (o *process descriptor*), che memorizza tutte le informazioni: stato, registri salvati, PID, spazio di indirizzi, file aperti. In xv6 si chiama `proc`. Quando un processo e fermo, i suoi registri vengono salvati nel *register context* del PCB; ripristinandoli l'OS riprende l'esecuzione. [Fonte: OSTEP, cap. 4]

### Stati del processo
- **Running**: in esecuzione su un core.
- **Ready**: pronto, in attesa che lo scheduler lo elegga.
- **Blocked**: in attesa di un evento (es. completamento I/O).
- Stati ausiliari: *initial* (in creazione) e **zombie** (terminato ma non ancora raccolto dal padre via `wait()`). [Fonte: OSTEP, cap. 4]

### Context switch
Il **context switch** e la procedura a basso livello con cui l'OS passa da un processo all'altro: salva i registri del processo corrente nel suo kernel stack/PCB e ripristina quelli del prossimo. Avviene durante una trap nel kernel (timer interrupt o syscall). E puro overhead, quindi va reso veloce. [Fonte: OSTEP, cap. 6]

### Limited Direct Execution (LDE)
Tecnica chiave: il programma utente gira **direttamente sull'hardware** a piena velocita (*direct execution*), ma in modo **limitato**:
- **Dual mode**: codice utente in *user mode* (privilegi ridotti); il kernel in *kernel mode*. Operazioni privilegiate (I/O, accesso hardware) richiedono una **system call** che esegue un'istruzione trap, salendo in kernel mode tramite la **trap table** configurata al boot.
- **Ritorno al controllo**: un **timer interrupt** periodico rida il controllo all'OS, che puo decidere di fare context switch (scheduling preemptive). [Fonte: OSTEP, cap. 6]

## Esempio: fork / exec / wait
Le API UNIX per creare processi:
- `fork()` crea un **duplicato** quasi esatto del processo chiamante. Ritorna **due volte**: il **PID del figlio** al padre, **0** al figlio. Padre e figlio hanno copie separate di address space, registri e PC. [Fonte: OSTEP, cap. 5]
- `wait()` / `waitpid()` sospende il padre finche un figlio non termina (raccogliendone lo stato, eliminando lo zombie). [Fonte: OSTEP, cap. 5]
- `exec()` **rimpiazza** l'immagine del processo corrente con un nuovo programma (carica nuovo code/data, re-inizializza heap/stack): non crea un nuovo processo, trasforma quello esistente. [Fonte: OSTEP, cap. 5]

> Perche separare fork ed exec? Tra i due, il figlio puo **modificare l'ambiente** (es. chiudere stdout e aprire un file -> redirezione `>`; collegare pipe). E esattamente cio che fa la **shell**. Questo e l'insight contro-intuitivo: l'apparente stranezza dell'API e la sua forza. [Fonte: OSTEP, cap. 5]

## Implicazioni
- Il context switch ha un **costo** (registri + invalidazione cache/TLB): troppi switch riducono il throughput.
- L'isolamento tra address space e la base della **sicurezza** dei processi; bug nei confini -> [[Privilege Escalation Linux]].
- Differenza processo/thread/goroutine: vedi [[Concetti dei Sistemi Operativi]].

## Collegamenti
- Vedi anche: [[Scheduling]], [[Concorrenza e Thread]], [[Memoria Virtuale]], [[Concetti dei Sistemi Operativi]]
- Cross-topic (linux): [[Processi Linux]], [[Strumenti di Rete]]
- Cross-topic (sicurezza): [[Privilege Escalation Linux]]

## Fonti
- [OSTEP, cap. 4 "The Abstraction: The Process", p. 25-33]
- [OSTEP, cap. 5 "Interlude: Process API", p. 37-45]
- [OSTEP, cap. 6 "Mechanism: Limited Direct Execution", p. 49-60]
