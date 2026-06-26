---
tipo: fonte
tag: [os]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
url: http://www.ostep.org
autore: Remzi e Andrea Arpaci-Dusseau
aliases: ["OSTEP", "Operating Systems: Three Easy Pieces"]
---

# Fonte - OSTEP: Operating Systems Three Easy Pieces

## Panoramica

*Operating Systems: Three Easy Pieces* (OSTEP) di Remzi e Andrea Arpaci-Dusseau (Univ. Wisconsin-Madison, v1.00) è un libro libero che organizza tutto il sapere sui sistemi operativi attorno a **tre idee fondamentali** ("easy pieces"), in omaggio ai *Six Easy Pieces* di Feynman. La tesi pedagogica: un OS fornisce **astrazioni** (virtualizza l'hardware), garantisce **performance** (overhead minimo) e offre **protezione/isolamento**. L'OS è il *"gestore delle risorse"* che virtualizza CPU, memoria e disco. [Fonte: OSTEP, cap. 2]

> Metodo didattico ricorrente: il **dialogo** Professore<->Studente e i riquadri **THE CRUX** che enunciano in una frase il problema centrale di ogni capitolo. [Fonte: OSTEP, cap. 1]

## Le 3 "Easy Pieces"

### 1. Virtualization (Virtualizzazione)
L'OS prende le risorse fisiche (un CPU, della memoria fisica) e crea per ogni processo l'**illusione** di possederne una copia privata e quasi infinita.
- **CPU virtuale**: time-sharing -> tanti processi su pochi core. *Crux: "come fornire l'illusione di tante CPU?"* [Fonte: OSTEP, cap. 4]
- **Memoria virtuale**: ogni processo vede uno spazio di indirizzi privato che parte da 0; meccanismi base/bounds -> segmentazione -> **paging** + **TLB**. *Crux: "virtualizzare la memoria con le pagine".* [Fonte: OSTEP, cap. 13-22]

### 2. Concurrency (Concorrenza)
Quando più thread condividono memoria, lo scheduling non controllato genera **race condition**. Servono primitive di sincronizzazione.
- **Lock/mutex**, **condition variables**, **semafori**. *Crux: "che supporto serve dall'hardware per costruire primitive di sincronizzazione?"* -> istruzioni atomiche (test-and-set, compare-and-swap). [Fonte: OSTEP, cap. 26-31]
- Bug classici: deadlock e non-deadlock (atomicity/order violation). [Fonte: OSTEP, cap. 32]

### 3. Persistence (Persistenza)
I dati devono sopravvivere a crash e spegnimenti -> gestione dispositivi I/O e file system.
- **Dispositivi I/O**: polling vs interrupt vs **DMA**; device driver come astrazione. [Fonte: OSTEP, cap. 36]
- **Dischi (HDD)**, **RAID**, **SSD flash**, **file system** (inode), **crash consistency** (FSCK, **journaling**, log-structured FS). [Fonte: OSTEP, cap. 37-45]

(Una quarta sezione breve tratta i **sistemi distribuiti**: comunicazione, RPC, NFS, AFS — cap. 48-50.)

## Mappa Capitoli -> Concetto

| Cap. | Argomento | Pagina wiki |
|------|-----------|-------------|
| 4-6 | Processo, API (fork/exec/wait), Limited Direct Execution, context switch | [[Processi]] |
| 7-10 | Scheduling: FIFO, SJF, STCF, Round Robin, MLFQ, multiprocessore | [[Scheduling]] |
| 9 | Proportional share, lottery, **CFS** Linux | [[Scheduling]] |
| 13-16 | Address space, address translation, segmentazione | [[Memoria Virtuale]] |
| 18-22 | **Paging**, **TLB**, page table multi-livello, page fault, swap, LRU | [[Memoria Virtuale]] |
| 26-32 | Thread, lock, condition variables, **semafori**, deadlock | [[Concorrenza e Thread]] |
| 36 | Dispositivi I/O, interrupt, **DMA** | [[I/O e Storage]] |
| 37-38 | HDD (geometria, seek), **RAID** 0/1/4/5 | [[I/O e Storage]] |
| 39-43 | File & directory, **inode**, FFS, **journaling**, LFS | [[Filesystem]] |
| 44 | **SSD flash**, FTL, wear leveling | [[I/O e Storage]] |

## 5 Insight Chiave (contro-intuitivi)

1. **L'OS è prevalentemente "fuori dai piedi".** Con la *Limited Direct Execution*, il codice utente gira direttamente sull'hardware a piena velocità; l'OS interviene solo su trap/interrupt. Non c'è un interprete che "esegue" i programmi. [Fonte: OSTEP, cap. 6]
2. **`fork()` è bizzarro ma potente.** Crea un duplicato esatto del processo che ritorna *due volte* (PID figlio al padre, 0 al figlio). La separazione fork/exec è ciò che permette alla shell di fare redirezione e pipe. [Fonte: OSTEP, cap. 5]
3. **Senza conoscenza del futuro non esiste lo scheduler ottimo.** SJF/STCF minimizzano il turnaround ma richiedono di conoscere la durata dei job; MLFQ *impara* dal comportamento passato e approssima SJF senza oracolo. [Fonte: OSTEP, cap. 7-8]
4. **Il paging "puro" è troppo lento.** Ogni accesso in memoria richiederebbe un accesso extra alla page table; la **TLB** (cache hardware delle traduzioni) rende la memoria virtuale praticabile — la località spaziale fa il resto. [Fonte: OSTEP, cap. 19]
5. **La consistenza dopo un crash è il problema difficile dei FS.** Aggiornare dati+inode+bitmap non è atomico: un crash a metà corrompe il FS. Il **journaling** (write-ahead logging) scrive prima l'intenzione nel log, poi applica — pagando un costo in scritture doppie. [Fonte: OSTEP, cap. 42]

## Collegamenti
- [[index]]
- Concetti OS: [[Processi]], [[Scheduling]], [[Memoria Virtuale]], [[Concorrenza e Thread]], [[Filesystem]], [[I/O e Storage]], [[Virtualizzazione]]
- Sintesi: [[I tre pezzi dell'OS]]
- Cross-topic (linux): [[Processi e Job Control]]
- Cross-topic (sicurezza): [[Privilege Escalation]]

## Fonti
- [OSTEP, Three Easy Pieces, cap. 1-2 (intro), cap. 4-51]
- <http://www.ostep.org>
