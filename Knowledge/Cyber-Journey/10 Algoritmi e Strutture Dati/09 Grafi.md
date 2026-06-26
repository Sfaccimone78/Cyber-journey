---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Grafi"]
---

# Grafi: rappresentazione (lista vs matrice di adiacenza)

## Definizione
Un **grafo** G = (V, E) è un insieme di **vertici** V collegati da **archi** E. Può essere **orientato** (archi diretti u→v) o **non orientato**, **pesato** (ogni arco ha un costo) o non pesato. È il modello di ogni rete: strade, social network, dipendenze, circuiti. [Fonte: Erickson, cap. Basic Graph Algorithms; ODS, cap. 12]

## Meccanismo — due rappresentazioni
### Matrice di adiacenza (AdjacencyMatrix)
Matrice n×n booleana `A[i][j] = 1` se esiste l'arco i→j. [Fonte: ODS, sez. 12.1]
- Verifica esistenza arco in **O(1)**.
- Iterare sui vicini di un nodo costa **O(n)** anche se ha pochi archi.
- Spazio **O(n²)** indipendentemente dal numero di archi → inefficiente per grafi **sparsi**.

### Lista di adiacenza (AdjacencyLists)
Per ogni vertice, la lista dei suoi vicini. [Fonte: ODS, sez. 12.2]
- Iterare sui vicini di v costa O(deg(v)) → efficiente.
- Verifica esistenza arco i→j costa O(deg(i)).
- Spazio **O(n + m)** con m = |E| → ideale per grafi sparsi (la maggioranza dei casi reali).

## Complessità
| | Matrice | Lista |
|---|---------|-------|
| spazio | O(n²) | O(n + m) |
| arco esiste? | O(1) | O(deg(v)) |
| itera vicini di v | O(n) | O(deg(v)) |
| adatto a | grafi densi, query archi | grafi sparsi, traversate |

## Algoritmi correlati (panoramica)
- **Traversate**: [[BFS e DFS]] (BFS/DFS), basate sulla "whatever-first search" generica di Erickson.
- **Minimum Spanning Tree (MST)**: connetti tutti i nodi a costo minimo — **Borůvka**, **Jarník/Prim** (usa heap), **Kruskal** (usa union-find). [Fonte: Erickson, cap. Minimum Spanning Trees]
- **Cammini minimi**: [[Algoritmo di Dijkstra]] (pesi non negativi), [[Algoritmo di Bellman-Ford]] (pesi negativi), Floyd-Warshall (all-pairs).
- **Topological sort** e **componenti fortemente connesse** via DFS. [Fonte: Erickson, cap. Depth-First Search]

## Esempio
Rete stradale (nodi = incroci, archi pesati = tempi di percorrenza) → Dijkstra per il navigatore. Dipendenze tra task → topological sort. Social network → BFS per gradi di separazione.

## Collegamenti
- Vedi anche: [[BFS e DFS]], [[Algoritmo di Dijkstra]], [[Algoritmo di Bellman-Ford]], [[Algoritmi Greedy]] (MST è greedy)

## Fonti
- [ODS, cap. 12 Graphs, pp. 239-252]
- [Erickson, cap. Basic Graph Algorithms / Minimum Spanning Trees]