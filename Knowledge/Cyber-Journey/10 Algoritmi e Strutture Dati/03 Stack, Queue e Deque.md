---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Stack, Queue e Deque", "Stack e Queue"]
---

# Stack, Queue e Deque

## Definizione
Tre interfacce (ADT) per aggiungere/rimuovere elementi solo agli **estremi** di una sequenza:
- **Stack** (pila): politica **LIFO** (Last-In First-Out). Operazioni `push(x)` e `pop()`.
- **Queue** (coda): politica **FIFO** (First-In First-Out). Operazioni `enqueue(x)` (`add`) e `dequeue()` (`remove`).
- **Deque** (double-ended queue): aggiunta/rimozione a **entrambi** gli estremi. [Fonte: ODS, sez. 1.2.1]

## Meccanismo
- **Stack** su array (ArrayStack) o lista: `push/pop` in coda all'array → O(1) ammortizzato.
- **Queue** su array circolare (ArrayQueue): due indici `head` e `len` che avanzano modulo la capacità, evitando lo shift → `add/remove` O(1) ammortizzato. [Fonte: ODS, sez. 2.3]
- **Deque** (ArrayDeque) su array circolare, oppure DualArrayDeque costruito da due stack contrapposti. [Fonte: ODS, sez. 2.4-2.5]

## Complessità
| Struttura | push/add | pop/remove | accesso interno |
|-----------|----------|------------|-----------------|
| Stack (array) | O(1) amm. | O(1) amm. | — |
| Queue (array circolare) | O(1) amm. | O(1) amm. | — |
| Deque (array circolare) | O(1) amm. agli estremi | O(1) amm. | O(n) |

## Esempio
- **Stack**: gestione delle chiamate ricorsive (call stack), valutazione di espressioni, undo/redo, [[BFS e DFS]] (DFS usa uno stack).
- **Queue**: scheduling round-robin, buffer di stampa, [[BFS e DFS]] (BFS usa una coda), gestione richieste in arrivo.

## Collegamenti
- Vedi anche: [[Array vs Linked List]], [[BFS e DFS]], [[Heap e Priority Queue]]
- Una **priority queue** [[Heap e Priority Queue]] generalizza la coda: esce l'elemento a priorità massima, non il più vecchio.
- Ponte sistemi: lo scheduling dei processi usa code → vedi [[Processi Linux]].

## Fonti
- [ODS, sez. 1.2.1 The Queue, Stack, and Deque Interfaces, p. 5]
- [ODS, cap. 2 Array-Based Lists, pp. 31-57]