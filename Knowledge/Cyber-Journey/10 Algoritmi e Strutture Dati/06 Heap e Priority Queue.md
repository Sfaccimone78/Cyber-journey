---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Heap e Priority Queue"]
---

# Heap e Priority Queue

## Definizione
Una **priority queue** (coda a priorità) è un ADT che mantiene un insieme di elementi con chiave/priorità e supporta: `add(x)` e `deleteMin()` (estrai l'elemento a priorità minima — o massima). L'implementazione standard è lo **heap binario**: un albero binario **quasi completo** che soddisfa la **heap property**: la chiave di ogni nodo è ≤ (min-heap) di quelle dei suoi figli. [Fonte: ODS, cap. 10]

## Meccanismo
- **Rappresentazione implicita**: lo heap binario si memorizza in un **array** senza puntatori. Per il nodo all'indice `i`: figli in `2i+1` e `2i+2`, padre in `(i−1)//2`. [Fonte: ODS, sez. 10.1]
- **add(x)**: inserisci in fondo all'array, poi *bubble-up* (scambia col padre finché la heap property è ripristinata) → O(log n).
- **deleteMin()**: rimuovi la radice, sposta l'ultimo elemento in cima, poi *trickle-down/sift-down* (scambia col figlio minore) → O(log n).
- **MeldableHeap**: variante randomizzata che supporta `merge(h1,h2)` di due heap in O(log n) atteso. [Fonte: ODS, sez. 10.2]
- **Heapify**: costruire uno heap da n elementi dati costa O(n) (non O(n log n)).

## Complessità
| Operazione | Heap binario |
|------------|--------------|
| findMin (peek) | O(1) |
| add | O(log n) |
| deleteMin | O(log n) |
| build (heapify) | O(n) |
| merge | O(n) [O(log n) per MeldableHeap] |

## Esempio
- **[[Algoritmo di Dijkstra]]** e **Prim**: estrazione ripetuta del nodo a distanza minima.
- **Heap-sort**: ordina inserendo tutto in uno heap ed estraendo (vedi [[Algoritmi di Ordinamento]]).
- Scheduling a priorità, simulazione a eventi discreti, top-k elementi, code di task in sistemi operativi.

## Collegamenti
- Vedi anche: [[Stack, Queue e Deque]] (la priority queue generalizza la coda), [[Algoritmi di Ordinamento]] (heap-sort), [[Algoritmo di Dijkstra]], [[Alberi Binari e BST]] (heap ordina per livello, BST per chiave)
- Ponte sistemi: gli scheduler a priorità dei sistemi operativi usano heap → [[Processi Linux]].

## Fonti
- [ODS, cap. 10 Heaps, pp. 203-214]
- CLRS — *Introduction to Algorithms*, cap. 6 "Heapsort" e §6.5 "Priority queues".
