---
tipo: concetto
tag: [os]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Concorrenza e Thread"]
---

# Concorrenza e Thread: Mutex, Semafori, Deadlock

## Definizione
Un **thread** e un flusso di esecuzione indipendente *dentro* un processo: ogni thread ha **PC e registri e stack propri**, ma **condivide** address space (code, heap, dati globali) e file aperti con gli altri thread del processo. La condivisione e la fonte sia della potenza sia dei pericoli. [Fonte: OSTEP, cap. 26]

Si usano i thread per **parallelismo** (sfruttare piu core) e per **sovrapporre I/O e calcolo** (evitare di bloccare l'intero processo). [Fonte: OSTEP, cap. 26]

## Il problema

### Race condition e sezione critica
Operazioni apparentemente atomiche come `counter++` sono in realta 3 istruzioni (load, add, store). Con scheduling non controllato, due thread possono interlacciarsi e perdere aggiornamenti -> **race condition**. Il codice che accede a dati condivisi e una **sezione critica** e va eseguito in **mutua esclusione**. *Crux: che supporto serve dall'hardware/OS per costruire primitive di sincronizzazione?* [Fonte: OSTEP, cap. 26]

## Meccanismi

### Lock / Mutex
Garantisce che **un solo thread** entri nella sezione critica (`lock()` ... `unlock()`). Costruzione: [Fonte: OSTEP, cap. 28]
- **Disabilitare interrupt**: funziona solo su monoprocessore, pericoloso.
- **Istruzioni atomiche hardware**: **test-and-set**, **compare-and-swap (CAS)**, **load-linked/store-conditional**, **fetch-and-add** (ticket lock). Sono il cuore di ogni lock corretto.
- **Spin lock**: il thread gira in busy-wait finche il lock e libero -> spreca CPU. Meglio **cedere (yield)** o **dormire** in coda (park/unpark) per evitare lo spin prolungato. Un **two-phase lock** prima spinna brevemente, poi dorme. [Fonte: OSTEP, cap. 28]

### Condition Variables (CV)
Permettono a un thread di **attendere** (`wait`) che una condizione diventi vera, e a un altro di **segnalare** (`signal`/`broadcast`). `wait()` rilascia atomicamente il lock e mette il thread a dormire; al risveglio lo riacquisisce. **Regola d'oro: controllare la condizione in un `while`, mai in un `if`** (risvegli spuri / Mesa semantics). Usate nel problema **produttore/consumatore** (bounded buffer). [Fonte: OSTEP, cap. 30]

### Semafori
Oggetto con un valore intero e due operazioni atomiche: **`sem_wait()`** (decrementa; se < 0 blocca) e **`sem_post()`** (incrementa; sveglia un attesa). [Fonte: OSTEP, cap. 31]
- Inizializzato a **1** -> **semaforo binario** = lock/mutex.
- Inizializzato a **0** -> usato per **ordinamento** (un thread aspetta che un altro segnali).
- Inizializzato a **N** -> consente N accessi concorrenti (es. slot di un buffer).
- Problemi classici risolti: **produttore/consumatore**, **reader-writer lock**, **dining philosophers** (5 filosofi, 5 forchette). [Fonte: OSTEP, cap. 31]

## Bug di concorrenza
Studio empirico (cap. 32): [Fonte: OSTEP, cap. 32]
- **Non-deadlock** (~la maggioranza):
  - **Atomicity violation**: una sequenza che si assume atomica viene interrotta. Fix: lock.
  - **Order violation**: si assume un ordine tra accessi che non e garantito. Fix: condition variable.
- **Deadlock**: due+ thread si bloccano a vicenda. Richiede **4 condizioni simultanee** (Coffman): **mutua esclusione**, **hold-and-wait**, **no preemption**, **attesa circolare**.
  - Prevenzione: rompere una condizione. La piu pratica: imporre un **ordine totale di acquisizione dei lock** (rompe l'attesa circolare). Altri: lock atomici globali (rompe hold-and-wait), trylock+backoff (no preemption -> rilascia e riprova), evitamento alla Banker, oppure **detect & recover**. [Fonte: OSTEP, cap. 32]

## Esempio: deadlock da ordine di lock
Thread1 prende `L1` poi `L2`; Thread2 prende `L2` poi `L1`. Se entrambi acquisiscono il primo lock e poi attendono il secondo -> deadlock. Soluzione: **tutti** acquisiscono sempre prima `L1` poi `L2`. [Fonte: OSTEP, cap. 32]

## Implicazioni
- La concorrenza e la fonte numero uno di bug **non deterministici** (Heisenbug).
- Race condition sono anche **vulnerabilita di sicurezza** (TOCTOU, time-of-check/time-of-use) -> cross-link a [[Privilege Escalation Linux]].
- Differenze thread vs processo vs goroutine vs coroutine: vedi [[Concetti dei Sistemi Operativi]].

## Collegamenti
- Vedi anche: [[Processi]], [[Scheduling]], [[Concetti dei Sistemi Operativi]]
- Cross-topic (sicurezza): [[Privilege Escalation Linux]]

## Fonti
- [OSTEP, cap. 26 "Concurrency: An Introduction", p. 287-299]
- [OSTEP, cap. 27-28 "Thread API / Locks", p. 303-335]
- [OSTEP, cap. 30-31 "Condition Variables / Semaphores", p. 351-383]
- [OSTEP, cap. 32 "Common Concurrency Problems", p. 385-399]
