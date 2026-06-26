---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Array vs Linked List", "Array e Linked List"]
---

# Array vs Linked List

## Definizione
Due modi fondamentali di realizzare una **sequenza lineare** (interfaccia `List`: `get(i)`, `set(i,x)`, `add(i,x)`, `remove(i)`):
- **Array** (ArrayList / ArrayStack in ODS): elementi in celle di memoria contigue, indirizzabili per indice.
- **Linked list**: nodi sparsi in memoria, ciascuno con un valore e uno o più puntatori al nodo successivo (singly) e/o precedente (doubly). [Fonte: ODS, cap. 2-3]

## Meccanismo
- **Array dinamico**: quando si riempie, si alloca un nuovo array di dimensione doppia e si copiano gli elementi. `add/remove` agli estremi costano O(1) **ammortizzato**; in mezzo richiedono lo shift di O(n) elementi. L'analisi ammortizzata mostra che una sequenza di m operazioni `add(i,x)`/`remove(i)` costa O(m + n) per il ridimensionamento. [Fonte: ODS, sez. 2.1.2]
- **Doubly-linked list (DLList)**: inserzione/cancellazione in O(1) **dato un puntatore al nodo**, ma `get(i)` richiede O(min{i, n−i}) per raggiungere la posizione (nessun accesso casuale). [Fonte: ODS, sez. 3.2]
- **SEList** (Space-Efficient List): lista di blocchi-array, riduce l'overhead dei puntatori bilanciando i due mondi. [Fonte: ODS, sez. 3.3]

## Complessità
| Operazione | Array dinamico | Doubly-linked list |
|------------|----------------|--------------------|
| `get(i)`/`set(i)` | O(1) | O(1 + min{i, n−i}) |
| `add/remove` agli estremi | O(1) ammortizzato | O(1) |
| `add(i)/remove(i)` interno | O(n) (shift) | O(1) col nodo, O(n) per trovarlo |
| spazio | compatto (1 ref/elem) | 2 puntatori/elem (overhead) |

## Esempio
Una pila di annullamenti (undo) cresce/decresce solo in cima → array dinamico (ArrayStack) è ideale. Una lista in cui si inseriscono di continuo elementi a metà avendo già il puntatore (es. cursore di un editor) → linked list.

## Collegamenti
- Vedi anche: [[Stack, Queue e Deque]], [[Skip List]], [[Complessità Computazionale]]
- Confronto: la [[Skip List|skiplist]] aggiunge accesso O(log n) a una struttura a liste.

## Fonti
- [ODS, cap. 2 Array-Based Lists, pp. 31-57]
- [ODS, cap. 3 Linked Lists, pp. 61-78]