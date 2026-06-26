---
tipo: sintesi
tag: [os, sintesi]
fase: 0
aggiornato: 2026-06-25
stato: attivo
aliases: ["I tre pezzi dell'OS", "La vita di un programma"]
---

# Synthesis — I tre pezzi dell'OS: la vita di un programma dal lancio all'exit

Sintesi cross-source gemella di [[Lo stack di rete]]: invece di seguire un pacchetto, **segue un programma** da quando lo lanci (`./app`) fino all'`exit()`, attraversando i **tre pezzi** dell'OS — *virtualizzazione, concorrenza, persistenza*. Raccorda [[Processi]], [[Scheduling]], [[Memoria Virtuale]], [[Concorrenza e Thread]], [[Filesystem]], [[I/O e Storage]], [[Virtualizzazione]] e [[OSTEP]].

## 1. Il lancio (fork + exec)

Quando la shell lancia un programma, fa **due syscall** distinte. [Fonte: OSTEP, cap. 5]

1. **`fork()`** — duplica il processo chiamante: nasce un figlio con una **copia** dello spazio di indirizzi (in pratica *copy-on-write*). `fork()` ritorna **due volte**: il PID del figlio al padre, `0` al figlio.
2. **`exec()`** — il figlio **sostituisce** la propria immagine con il binario su disco: l'OS legge l'eseguibile dal [[Filesystem]], imposta code/data/heap/stack e salta all'entry point.

Lo iato tra fork ed exec è ciò che permette alla shell di fare **redirezione e pipe** (chiude/riapre i file descriptor *tra* i due passi) → [[Redirezione e Pipeline]]. Il padre poi fa **`wait()`** per raccogliere l'exit status del figlio.

## 2. Pezzo 1 — Virtualizzazione della CPU

Il processo ora è una **entità schedulabile**. L'OS mantiene per ognuno un **PCB** (process control block) con registri salvati, stato, PID, page table → [[Processi]].

- **Limited Direct Execution**: il codice utente gira **direttamente** sull'hardware a piena velocità; l'OS riprende il controllo solo su **trap/syscall** o **interrupt del timer**. Non c'è interprete. [Fonte: OSTEP, cap. 6]
- Al **timer interrupt** scatta il **context switch**: salva i registri del processo uscente nel suo kernel stack, carica quelli dell'entrante → lo **scheduler** decide chi gira → [[Scheduling]].
- Lo scheduler reale (Linux **CFS**) approssima *"il job più corto / meno servito prima"* senza oracolo, come fa **MLFQ** imparando dal comportamento passato. [Fonte: OSTEP, cap. 7-9]

> Insight: dal punto di vista del processo, **possiede la CPU**. È un'illusione mantenuta a colpi di context switch migliaia di volte al secondo (time-sharing).

## 3. Pezzo 1bis — Virtualizzazione della Memoria

Ogni processo vede uno **spazio di indirizzi privato** che parte da 0 (code, heap ↑, stack ↓), anche se in RAM è sparpagliato altrove → [[Memoria Virtuale]].

- La traduzione **virtuale→fisica** avviene a granularità di **pagina** tramite la **page table** (multi-livello).
- Ogni accesso in memoria richiederebbe un accesso *extra* alla page table: la **TLB** (cache hardware delle traduzioni) lo evita, e la **località spaziale** fa il resto. [Fonte: OSTEP, cap. 19]
- Un **page fault** porta dentro la pagina mancante (da disco/swap); se la RAM è piena, una politica di rimpiazzo (approx-**LRU**) sceglie la vittima → ponte con [[I/O e Storage]].

L'isolamento degli address space è anche una **frontiera di sicurezza**: bug/exploit cercano di romperlo (buffer overflow, info leak) → [[Privilege Escalation]], [[Malware]].

## 4. Pezzo 2 — Concorrenza

Il programma crea più **thread** che condividono lo stesso spazio di indirizzi → [[Concorrenza e Thread]].

- Lo scheduling non controllato su dati condivisi genera **race condition**; serve **mutua esclusione**.
- Primitive: **lock/mutex**, **condition variables**, **semafori**, costruite su istruzioni atomiche hardware (**test-and-set**, **compare-and-swap**). [Fonte: OSTEP, cap. 28-31]
- Bug classici: **deadlock** (le 4 condizioni di Coffman: mutua esclusione, hold-and-wait, no-preemption, attesa circolare) e non-deadlock (atomicity/order violation). [Fonte: OSTEP, cap. 32]

> Insight: la concorrenza è "facile" finché non c'è **stato condiviso mutabile**. Il prezzo della performance multi-core è la disciplina di sincronizzazione.

## 5. Pezzo 3 — Persistenza

Il programma salva dati che devono **sopravvivere a crash e spegnimenti** → [[Filesystem]], [[I/O e Storage]].

- Una `write()` attraversa lo stack: file → **inode** → blocchi dati → bitmap → **buffer cache** → device driver → disco. L'I/O usa **interrupt** e **DMA** per non bruciare CPU nell'attesa. [Fonte: OSTEP, cap. 36]
- Aggiornare dati+inode+bitmap **non è atomico**: un crash a metà corrompe il FS. Il **journaling** (write-ahead logging) scrive prima l'intenzione nel log, poi applica — pagando scritture doppie. [Fonte: OSTEP, cap. 42]
- Sotto: **HDD** (geometria/seek), **RAID** (0/1/5), **SSD** flash con FTL e wear leveling → [[I/O e Storage]].

## 6. L'uscita

`exit()` libera le risorse (memoria, file descriptor); il processo diventa **zombie** finché il padre non fa `wait()` e ne raccoglie lo status. Se il padre muore prima, il processo viene **adottato da init/systemd** → [[Processi e Job Control]] (linux).

## 7. Schema: dove vive ogni pezzo

```
 [ Programma utente ]                    ← gira in user mode (LDE)
   | syscall / trap / interrupt
 [ KERNEL ]
   ├─ Virtualizzazione CPU   → scheduler, context switch   [[Scheduling]]
   ├─ Virtualizzazione MEM   → page table, TLB, page fault  [[Memoria Virtuale]]
   ├─ Concorrenza            → lock, semafori, CV           [[Concorrenza e Thread]]
   └─ Persistenza            → FS, inode, journaling, I/O   [[Filesystem]]
 [ HARDWARE ]  CPU · RAM · disco/SSD · timer · DMA
```

## 8. I tre pezzi a colpo d'occhio

| Pezzo | Problema (CRUX) | Meccanismi | Pagina |
|-------|-----------------|------------|--------|
| **Virtualizzazione** | dare a ogni processo l'illusione di CPU+memoria proprie | time-sharing, LDE, paging, TLB | [[Processi]], [[Memoria Virtuale]] |
| **Concorrenza** | coordinare thread su stato condiviso | atomiche, lock, semafori, CV | [[Concorrenza e Thread]] |
| **Persistenza** | far sopravvivere i dati ai crash | inode, journaling, DMA, RAID | [[Filesystem]], [[I/O e Storage]] |

## Collegamenti
- Concetti OS: [[Processi]], [[Scheduling]], [[Memoria Virtuale]], [[Concorrenza e Thread]], [[Filesystem]], [[I/O e Storage]], [[Virtualizzazione]]
- Sintesi gemella (reti): [[Lo stack di rete]]
- Riassunto fonte: [[OSTEP]]
- Cross-topic (linux): [[Processi e Job Control]], [[Redirezione e Pipeline]]
- Cross-topic (sicurezza): [[Privilege Escalation]], [[Malware]]
- Cross-topic (algoritmi): [[Scheduling]] ↔ code/heap, [[Hash Table]] (page table come mappa)

## Fonti
- [OSTEP, *Three Easy Pieces* — cap. 4-6 (processi/LDE), 7-10 (scheduling), 13-22 (memoria virtuale), 26-32 (concorrenza), 36-45 (persistenza)] → [[OSTEP]]
- <http://www.ostep.org>
