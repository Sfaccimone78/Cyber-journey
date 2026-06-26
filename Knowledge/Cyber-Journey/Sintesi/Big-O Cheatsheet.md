---
tipo: sintesi
tag: [algoritmi, sintesi]
fase: 0
aggiornato: 2026-06-25
stato: attivo
aliases: ["Big-O Cheatsheet"]
---

# Big-O Cheatsheet

Sintesi rapida di complessità tempo/spazio. Convenzioni: *n* = numero elementi, complessità nel caso indicato. "amm." = amortizzato.

## Strutture dati × operazioni (tempo nel caso medio, peggiore se diverso)

| Struttura | Accesso/Index | Ricerca | Inserimento | Cancellazione | Spazio | Note |
|-----------|---------------|---------|-------------|---------------|--------|------|
| [[Array e Linked List]] — Array | **O(1)** | O(n) | O(n) | O(n) | O(n) | indicizzazione diretta |
| Array dinamico | O(1) | O(n) | O(1) amm. (O(n) worst) | O(n) | O(n) | resize raddoppiando |
| [[Array e Linked List]] — Linked list | O(n) | O(n) | **O(1)** (alla testa/nodo noto) | O(1) | O(n) | niente indice O(1) |
| [[Stack e Queue]] — Stack/Queue | — | — | **O(1)** | **O(1)** | O(n) | LIFO / FIFO |
| [[Hash Table]] | — | **O(1)** (O(n) worst) | O(1) | O(1) | O(n) | dipende da hash/load factor |
| [[Alberi Binari]] — BST bilanciato | O(log n) | O(log n) | O(log n) | O(log n) | O(n) | AVL / red-black |
| [[Alberi Binari]] — BST sbilanciato | O(n) worst | O(n) | O(n) | O(n) | O(n) | degenera a lista |
| [[Skip List]] | O(log n) atteso | O(log n) atteso | O(log n) atteso | O(log n) atteso | O(n) | randomizzata, O(n) worst raro |
| [[Heap e Priority Queue]] (binary heap) | find-min **O(1)** | O(n) | O(log n) | O(log n) (extract-min) | O(n) | build-heap O(n) |
| [[Trie]] | O(L) | O(L) | O(L) | O(L) | O(n·σ·L) | L=lung. chiave, σ=alfabeto |
| [[Grafi]] — Lista adiacenza | — | arco: O(deg) | O(1) | O(deg) | **O(V+E)** | grafi sparsi |
| [[Grafi]] — Matrice adiacenza | — | arco: **O(1)** | O(1) | O(1) | O(V²) | grafi densi |

## Algoritmi su grafi

| Algoritmo | Tempo | Spazio | Vincolo |
|-----------|-------|--------|---------|
| [[BFS e DFS]] BFS / DFS | O(V + E) | O(V) | — |
| [[Dijkstra]] (binary heap) | O((V+E) log V) | O(V) | pesi ≥ 0 |
| [[Bellman-Ford]] | O(V·E) | O(V) | rileva cicli negativi |
| Floyd-Warshall (all-pairs) | O(V³) | O(V²) | DP, pesi negativi ok |
| MST (Kruskal / Prim) | O(E log V) | O(V+E) | greedy |

## Sorting × complessità × stabilità × in-place

| Algoritmo | Best | Average | Worst | Spazio | Stabile | In-place |
|-----------|------|---------|-------|--------|:-------:|:--------:|
| Bubble sort | O(n) | O(n²) | O(n²) | O(1) | sì | sì |
| Insertion sort | O(n) | O(n²) | O(n²) | O(1) | sì | sì |
| Selection sort | O(n²) | O(n²) | O(n²) | O(1) | no | sì |
| **Merge sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | **sì** | no |
| **Quicksort** | O(n log n) | O(n log n) | **O(n²)** | O(log n) | no | sì |
| **Heapsort** | O(n log n) | O(n log n) | O(n log n) | O(1) | no | sì |
| Counting sort | O(n+k) | O(n+k) | O(n+k) | O(k) | sì | no |
| Radix sort | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | sì | no |
| Timsort (Python/Java) | O(n) | O(n log n) | O(n log n) | O(n) | sì | no |

> Limite inferiore dei comparison sort: **Ω(n log n)** → merge/heap sort sono **asintoticamente ottimali**. Counting/radix lo superano sfruttando chiavi intere limitate. Dettagli: [[Ordinamento (Sorting)]], [[Complessità Computazionale]].

## Ricerca

| Algoritmo | Best | Average | Worst | Requisito |
|-----------|------|---------|-------|-----------|
| [[Ricerca]] Linear search | O(1) | O(n) | O(n) | nessuno |
| [[Ricerca]] Binary search | O(1) | O(log n) | O(log n) | array **ordinato** |
| [[Ricerca]] Interpolation search | O(1) | O(log log n) | O(n) | ordinato + distribuzione uniforme |

## Collegamenti
- Vedi anche: [[Da problema ad algoritmo]] (quale scegliere), [[Complessità Computazionale]] (notazione O/Ω/Θ), e ogni concetto linkato in tabella.

## Fonti
- [Erickson, capp. Sorting / Shortest Paths / Asymptotic Analysis] → [[Algorithms (Jeff Erickson)]]
- [ODS, tabelle riepilogative capp. 2-13] → [[Open Data Structures (Pat Morin)]]
