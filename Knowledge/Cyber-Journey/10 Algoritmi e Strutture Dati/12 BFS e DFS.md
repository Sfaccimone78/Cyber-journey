---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["BFS e DFS"]
---

# BFS e DFS (visite di grafi)

## Definizione
**BFS** (Breadth-First Search, ricerca in ampiezza) e **DFS** (Depth-First Search, ricerca in profondità) sono le due strategie fondamentali per **visitare** sistematicamente tutti i vertici raggiungibili di un [[Grafi|grafo]]. Erickson le presenta come istanze della stessa **"whatever-first search"** generica: cambia solo la struttura usata per la frontiera dei nodi da esplorare — **coda** (FIFO) per BFS, **pila** (LIFO) per DFS. [Fonte: Erickson, cap. Basic Graph Algorithms]

## Meccanismo / pseudocodice

### BFS — usa una coda ([[Stack, Queue e Deque]])
Esplora per **livelli**: prima tutti i vicini a distanza 1, poi 2, ecc. Su grafi **non pesati** calcola il **cammino minimo** (minor numero di archi) dalla sorgente.
```
BFS(G, s):
    for v in V: dist[v] = ∞; parent[v] = null
    dist[s] = 0; Q = queue([s])
    while Q not empty:
        u = Q.dequeue()
        for w in neighbors(u):
            if dist[w] == ∞:               # non ancora visitato
                dist[w] = dist[u] + 1
                parent[w] = u
                Q.enqueue(w)
```

### DFS — usa una pila (o ricorsione)
Va il più in profondità possibile prima di tornare indietro (**backtrack**).
```
DFS(G, u):
    mark u as visited
    pre[u] = clock++          # tempo di scoperta
    for w in neighbors(u):
        if w not visited: parent[w] = u; DFS(G, w)
    post[u] = clock++         # tempo di completamento
```
I tempi **pre/post** classificano gli archi (tree/back/forward/cross) e abilitano gli algoritmi derivati.

## Complessità
Entrambe visitano ogni vertice e ogni arco una volta:

| | Tempo (lista adiacenza) | Tempo (matrice) | Spazio |
|---|---|---|---|
| BFS | **O(V + E)** | O(V²) | O(V) (coda) |
| DFS | **O(V + E)** | O(V²) | O(V) (pila/stack ricorsione) |

Best = Avg = Worst = Θ(V + E): la visita tocca tutto il grafo raggiungibile.

## Applicazioni
**BFS:**
- Cammino minimo in grafi **non pesati** (← caso base di [[Algoritmo di Dijkstra]] con pesi unitari).
- Gradi di separazione, web crawling per livelli, broadcast in reti.
- Test di **bipartizione** (2-coloring).

**DFS:**
- **Ordinamento topologico** (topological sort) di un DAG → ordine post-visita invertito. [Fonte: Erickson, cap. Depth-First Search]
- **Componenti fortemente connesse** (Tarjan, Kosaraju).
- Rilevamento di **cicli** (back edge).
- Attraversamento di alberi, generazione di labirinti, [[Backtracking]] (DFS sullo spazio delle soluzioni).

## Esempio
Social network: BFS da "Alice" trova in quanti passi minimi raggiunge "Bob" (gradi di separazione). Sistema di build: DFS sul grafo di dipendenze produce l'ordine di compilazione (topological sort) e rileva dipendenze circolari (back edge).

## Collegamenti
- Vedi anche: [[Grafi]] (rappresentazione), [[Stack, Queue e Deque]] (coda↔BFS, pila↔DFS), [[Algoritmo di Dijkstra]] (BFS pesato con priority queue), [[Backtracking]] (DFS guidato), [[Trie]] (visita DFS = ordine lessicografico)

## Fonti
- [Erickson, cap. Basic Graph Algorithms / Depth-First Search]
- [ODS, cap. 12 Graphs (BFS/DFS), pp. 245-250]