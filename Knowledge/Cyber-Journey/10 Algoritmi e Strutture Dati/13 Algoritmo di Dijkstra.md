---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Algoritmo di Dijkstra", "Dijkstra"]
---

# Algoritmo di Dijkstra (cammini minimi, pesi non negativi)

## Definizione
L'algoritmo di **Dijkstra** risolve il problema **single-source shortest path** (cammini minimi da una sorgente *s* a tutti gli altri vertici) su grafi **pesati con pesi non negativi**. È un algoritmo [[Algoritmi Greedy|greedy]]: a ogni passo "finalizza" il vertice non ancora trattato con distanza provvisoria minima, certo che quella distanza non potrà più migliorare (proprio perché i pesi sono ≥ 0). [Fonte: Erickson, cap. Shortest Paths]

> ⚠️ Con **pesi negativi** Dijkstra è scorretto (un arco negativo successivo potrebbe accorciare un cammino già finalizzato) → serve [[Algoritmo di Bellman-Ford]].

## Meccanismo / pseudocodice
Mantiene `dist[]` (stima del cammino minimo) e una **coda di priorità** ([[Heap e Priority Queue]]) sui vertici, chiave = `dist`. Operazione centrale: **relax** di un arco (u→v).
```
Dijkstra(G, s):
    for v in V: dist[v] = ∞; parent[v] = null
    dist[s] = 0
    PQ = min-priority-queue(all V, key = dist)
    while PQ not empty:
        u = PQ.extract_min()           # vertice greedy: dist minima
        for (u, v, w) in edges(u):
            if dist[u] + w < dist[v]:  # RELAX
                dist[v] = dist[u] + w
                parent[v] = u
                PQ.decrease_key(v, dist[v])
```
`parent[]` ricostruisce il **shortest-path tree**. Ogni vertice viene estratto e finalizzato una sola volta.

## Complessità
Dipende dall'implementazione della priority queue:

| Priority queue | Complessità | Note |
|----------------|-------------|------|
| Array semplice | O(V²) | meglio per grafi **densi** |
| **Binary heap** | **O((V + E) log V)** | standard, grafi sparsi |
| Fibonacci heap | O(E + V log V) | ottimo teorico, decrease_key O(1) amortizzato |

Best = Avg = Worst (deterministico): la struttura del lavoro non dipende dai valori, solo da |V| e |E|.

## Esempio
**Navigatore stradale**: nodi = incroci, archi pesati = tempi di percorrenza (sempre ≥ 0) → Dijkstra dà il percorso più rapido. **Routing di rete**: il protocollo **OSPF** usa Dijkstra (SPF, Shortest Path First) per costruire le tabelle di instradamento da un grafo di link pesati per costo. [Fonte: Erickson, cap. Shortest Paths] Con pesi unitari, Dijkstra degenera in [[BFS e DFS]] (BFS).

## Collegamenti
- Vedi anche: [[Algoritmo di Bellman-Ford]] (gestisce pesi negativi), [[BFS e DFS]] (BFS = Dijkstra con pesi unitari), [[Algoritmi Greedy]] (Dijkstra è greedy), [[Heap e Priority Queue]] (struttura chiave), [[Grafi]]

## Fonti
- [Erickson, cap. Shortest Paths]