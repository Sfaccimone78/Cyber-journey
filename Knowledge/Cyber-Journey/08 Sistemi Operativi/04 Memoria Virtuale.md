---
tipo: concetto
tag: [os]
fase: 0
fonti: 5
aggiornato: 2026-07-02
stato: maturo
aliases: ["Memoria Virtuale"]
---

# Memoria Virtuale: Paging, TLB, Page Fault

## In breve
La **memoria virtuale** dà a ogni processo l'illusione di uno spazio di indirizzi privato e contiguo, tradotto dall'MMU in memoria fisica a ogni accesso. Poggia su paging, page table (multi-livello), **TLB** come cache delle traduzioni e page fault/swap con politiche di rimpiazzo. È il fondamento dell'**isolamento** tra processi e la base delle difese di exploitation (ASLR, DEP/NX), oltre a essere bersaglio di attacchi micro-architetturali come Meltdown/Spectre e Rowhammer.

## Definizione
La **memoria virtuale** da a ogni processo l'illusione di uno **spazio di indirizzi** privato, grande e contiguo, che parte da 0 — mentre la memoria fisica e condivisa e frammentata. Obiettivi: **trasparenza** (il processo non sa di essere virtualizzato), **efficienza** (poco overhead di tempo/spazio), **protezione** (un processo non puo accedere alla memoria di un altro o del kernel). [Fonte: OSTEP, cap. 13]

Un indirizzo virtuale viene **tradotto** in indirizzo fisico dall'hardware (**MMU**) a ogni accesso. [Fonte: OSTEP, cap. 15]

## Meccanismo

### Dalla rilocazione al paging
- **Base & bounds**: il piu semplice — un registro base sommato all'indirizzo virtuale, un registro bounds per il controllo. Soffre di **frammentazione interna**.
- **Segmentazione**: base/bounds separati per code, heap, stack -> meno spreco, ma genera **frammentazione esterna**. [Fonte: OSTEP, cap. 16]
- **Paging**: divide lo spazio virtuale in **pagine** di dimensione fissa (tipicamente 4 KB) e la memoria fisica in **frame** della stessa dimensione. Niente frammentazione esterna; gestione flessibile. *Crux: virtualizzare la memoria con le pagine.* [Fonte: OSTEP, cap. 18]

### Page table
Struttura per-processo che mappa **numero di pagina virtuale (VPN) -> numero di frame fisico (PFN)**. Ogni **PTE** (page table entry) contiene il PFN e bit di controllo: **valid**, **present** (in RAM o su disco), **protection** (R/W/X), **dirty**, **accessed/reference**. Le page table lineari sono enormi -> si usano **page table multi-livello** (un albero: la directory indicizza tabelle di secondo livello, allocate solo se servono) o **inverted page table**. [Fonte: OSTEP, cap. 18, 20]

### TLB (Translation Lookaside Buffer)
Il paging "puro" e **troppo lento**: ogni accesso a memoria richiederebbe un accesso *extra* per leggere la PTE. La **TLB** e una **cache hardware** (nella MMU) delle traduzioni VPN->PFN piu recenti. [Fonte: OSTEP, cap. 19]
- **TLB hit**: traduzione immediata.
- **TLB miss**: si consulta la page table (in HW dalla MMU, o in SW dal kernel via trap), si popola la TLB, si riprova.
- Funziona grazie alla **localita spaziale e temporale**: accessi vicini cadono nella stessa pagina. *Crux: come accelerare la traduzione evitando l'accesso extra?* [Fonte: OSTEP, cap. 19]
- Problema sul **context switch**: le voci TLB del vecchio processo non sono valide per il nuovo -> o si **svuota (flush)** la TLB, o si usa un **ASID** (address space identifier) per distinguere i processi. [Fonte: OSTEP, cap. 19]

### Page fault e swap
La RAM puo non bastare: parte dello spazio virtuale risiede su **swap space** (disco). [Fonte: OSTEP, cap. 21]
- Se il bit **present** della PTE e 0, l'accesso genera un **page fault**: il kernel (page-fault handler) trova la pagina su disco, la carica in un frame libero, aggiorna la PTE, riprende l'istruzione.
- Se la RAM e **piena**, serve una **politica di rimpiazzo** che sceglie quale pagina **evict**. Ottimo teorico = **MIN/OPT** (evict la pagina usata piu lontano nel futuro, irrealizzabile). Politiche reali: **FIFO**, **Random**, **LRU**. LRU si approssima con l'algoritmo **clock** sfruttando il bit *reference*. **Belady's anomaly**: con FIFO, aumentare i frame puo *peggiorare* gli hit (contro-intuitivo). [Fonte: OSTEP, cap. 22]
- **Thrashing**: quando il working set supera la RAM, il sistema passa il tempo a fare paging -> crollo delle prestazioni. [Fonte: OSTEP, cap. 22]

## Esempio
Accesso a `array[i]` in un loop: il primo elemento di ogni pagina causa un TLB miss, i successivi (stessa pagina) sono hit. Con pagine da 4 KB e int da 4 byte -> ~1 miss ogni 1024 accessi: l'hit rate alto (~99%+) rende il paging praticabile. [Fonte: OSTEP, cap. 19]

## Implicazioni
- La memoria virtuale e il fondamento dell'**isolamento** tra processi (sicurezza) e dell'**overcommit** (illusione di piu RAM del fisico).
- TLB e cache sono **canali laterali** sfruttabili da attacchi (timing, Meltdown/Spectre): cross-link a [[Attacchi di Rete]] e alla sicurezza.
- Legame stretto con [[I/O e Storage]] (lo swap usa il disco) e [[Processi]] (ogni processo ha la sua page table).

## Approfondimento sicurezza
La memoria virtuale è il fondamento dell'isolamento — e quindi un bersaglio:
- **ASLR** randomizza la posizione di stack/heap/librerie nello spazio virtuale per rendere non
  predicibili gli indirizzi: difesa centrale contro l'exploitation. Dettagli e bypass in
  [[Bypass Protezioni (ASLR, DEP, Stack Canary, PIE)]]. **DEP/NX** usa il bit di protezione delle PTE
  (`X`) per rendere lo stack non eseguibile.
- **Attacchi micro-architetturali** — **Meltdown/Spectre** sfruttano l'esecuzione speculativa per
  leggere memoria oltre i confini di protezione; **Rowhammer** induce bit-flip in DRAM per corrompere
  page table e ottenere privesc. La TLB/cache sono **canali laterali** di timing.
- **Page table & `/proc/<pid>/maps`** — leggere la mappa di un processo rivela basi randomizzate
  (utile dopo un leak per bypassare ASLR). `mprotect` per rendere eseguibile memoria (shellcode JIT).
- **Difesa** — KASLR, KPTI (isolamento page table kernel/user post-Meltdown), `mmap_min_addr`
  (contro null-deref), W^X.

## Lab
- Osserva ASLR: esegui due volte un binario PIE e confronta `/proc/self/maps` (gli indirizzi cambiano).
  Disabilita con `setarch -R` o `echo 0 > /proc/sys/kernel/randomize_va_space` (solo in lab).
- **pwn.college** — moduli *Memory Errors / ASLR*.
- Misura un TLB miss: loop su array grande vs piccolo, confronta i tempi (`perf stat -e dTLB-load-misses`).

## Domande
**D: Perché si usa il paging invece della segmentazione pura?**
R: Pagine a dimensione fissa eliminano la frammentazione esterna e semplificano l'allocazione; la
segmentazione la genera. Il costo (tabelle grandi) si gestisce con page table multi-livello.

**D: Cos'è la TLB e perché è necessaria?**
R: Cache hardware delle traduzioni VPN→PFN. Senza, ogni accesso a memoria richiederebbe un accesso
extra alla page table. Sfrutta la località per avere hit rate molto alto.

**D: Cosa succede durante un page fault?**
R: Il bit present è 0 → trap al kernel, che carica la pagina (da swap/file) in un frame, aggiorna la
PTE e riprende l'istruzione. Se la RAM è piena, prima fa evict secondo la politica di rimpiazzo.

**D: Come si lega la memoria virtuale alla sicurezza dell'exploitation?**
R: Fornisce isolamento e le protezioni ASLR/DEP (via randomizzazione e bit PTE); attacchi come
Meltdown/Spectre/Rowhammer e leak da `/proc/maps` mirano proprio a bucare o aggirare questo strato.

## Collegamenti
- Vedi anche: [[Processi]], [[I/O e Storage]], [[Filesystem]], [[Concetti dei Sistemi Operativi]]
- Cross-topic (sicurezza): [[Privilege Escalation Linux]], [[Bypass Protezioni (ASLR, DEP, Stack Canary, PIE)]], [[Stack Buffer Overflow]]

## Fonti
- [OSTEP, cap. 13 "The Abstraction: Address Spaces", p. 121-127]
- [OSTEP, cap. 15-16 "Address Translation / Segmentation", p. 141-163]
- [OSTEP, cap. 18-20 "Paging / TLB / Smaller Tables", p. 185-227]
- [OSTEP, cap. 21-22 "Beyond Physical Memory: Mechanisms & Policies", p. 231-257]
- Meltdown/Spectre — https://meltdownattack.com/ ; Rowhammer (Google P0): https://googleprojectzero.blogspot.com/2015/03/exploiting-dram-rowhammer-bug-to-gain.html
