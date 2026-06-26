---
tipo: fonte
tag: [algoritmi]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
url: https://opendatastructures.org/
autore: Pat Morin
aliases: ["Open Data Structures (Pat Morin)", "Open Data Structures"]
---

# Fonte - Open Data Structures (Pat Morin)

## Panoramica
*Open Data Structures* di Pat Morin (Carleton University) è un manuale introduttivo gratuito (Creative Commons, sorgenti su GitHub) dedicato interamente alle **strutture dati**. Obiettivo dichiarato: liberare gli studenti dal dover pagare un libro di strutture dati. [Fonte: ODS, "Why This Book?"]

## Approccio
- **Centrato sulle interfacce (ADT) e sull'implementazione concreta**. Ogni capitolo introduce un'interfaccia (Stack/Queue/Deque, List, USet, SSet) e poi mostra strutture che la realizzano con diversi compromessi.
- **Analisi rigorosa di tempo e spazio** per ogni operazione, con forte uso di **analisi ammortizzata** (es. crescita/restringimento degli array, SEList) e **analisi attesa/randomizzata** (Skiplist, Treap, MeldableHeap). [Fonte: ODS, sez. 1.5, cap. 2-3]
- **Pseudocodice + Python**: implementazioni reali e testabili, non solo schemi.
- **Motivazione applicativa concreta**: l'introduzione lega ogni struttura a un problema quotidiano (aprire un file → filesystem; rubrica → ricerca; login → lookup utenti; ricerca web → indici). [Fonte: ODS, cap. 1]

## Audience
Studenti del primo corso di strutture dati. Richiede solo basi di programmazione e matematica elementare (logaritmi, fattoriali, notazione asintotica, probabilità di base, spiegate nel cap. 1). È esplicitamente il prerequisito che Erickson dà per scontato. [Fonte: ODS, cap. 1.3]

## Contenuti principali (per capitolo)
| Capitolo | Strutture | Interfaccia | Pagina wiki |
|----------|-----------|-------------|-------------|
| 2 Array-Based Lists | ArrayStack, ArrayQueue, ArrayDeque, DualArrayDeque, RootishArrayStack | List/Deque | [[Array e Linked List]], [[Stack e Queue]] |
| 3 Linked Lists | SLList, DLList, SEList | List/Deque | [[Array e Linked List]] |
| 4 Skiplists | SkiplistSSet, SkiplistList | SSet/List | [[Skip List]] |
| 5 Hash Tables | ChainedHashTable, LinearHashTable, hash codes | USet | [[Hash Table]] |
| 6 Binary Trees | BinaryTree, BinarySearchTree | SSet | [[Alberi Binari]] |
| 7 Random BST | random BST, Treap | SSet | [[Alberi Binari]] |
| 8 Scapegoat Trees | ScapegoatTree (ricostruzione parziale) | SSet | [[Alberi Binari]] |
| 9 Red-Black Trees | 2-4 trees, RedBlackTree | SSet | [[Alberi Binari]] |
| 10 Heaps | BinaryHeap (implicito), MeldableHeap | priority queue | [[Heap e Priority Queue]] |
| 11 Sorting | Merge-sort, Quicksort, Heap-sort, Counting/Radix sort, lower bound | — | [[Ordinamento (Sorting)]] |
| 12 Graphs | AdjacencyMatrix, AdjacencyLists, BFS, DFS | grafo | [[Grafi]], [[BFS e DFS]] |
| 13 Data Structures for Integers | BinaryTrie, XFastTrie, YFastTrie | SSet su interi | [[Trie]] |
| 14 External Memory | Block Store, B-Trees | SSet su disco | [[Alberi Binari]] |

## Interfacce (ADT) — la spina dorsale del libro
- **Queue / Stack / Deque**: aggiunta/rimozione agli estremi (FIFO, LIFO, entrambi). [Fonte: ODS, sez. 1.2.1]
- **List**: sequenza lineare con accesso per indice `get(i)/set(i)`, `add(i,x)`, `remove(i)`. [Fonte: ODS, sez. 1.2.2]
- **USet** (Unordered Set): insieme senza ordine, `add/remove/find` — realizzato da hash table. [Fonte: ODS, sez. 1.2.3]
- **SSet** (Sorted Set): insieme ordinato, supporta `find(x)` come successore/predecessore — realizzato da BST bilanciati, skiplist, trie. [Fonte: ODS, sez. 1.2.4]

## Concetti unici vs sovrapposti con Erickson
- **Unici di ODS**: implementazione interna di array dinamici, liste, skiplist, hash table (chaining e linear probing), alberi bilanciati (red-black, scapegoat, treap), heap, trie su interi (X/Y-fast), B-tree per memoria esterna; analisi ammortizzata e randomizzata.
- **Sovrapposti con [[Algorithms (Jeff Erickson)]]**: algoritmi di sorting, BFS/DFS, rappresentazione di grafi (lista vs matrice).
- **Demarcazione**: ODS costruisce le strutture; Erickson le usa.

## Collegamenti
- [[index]]
- Vedi anche: [[Algorithms (Jeff Erickson)]], [[Big-O Cheatsheet]], [[Complessità Computazionale]]

## Fonti
- [ODS, cap. 1 Introduction, pp. 1-29]
- [ODS, "Why This Book?", pp. xi-xii]
- [ODS, Table of Contents]
- Sito ufficiale: <https://opendatastructures.org/>
