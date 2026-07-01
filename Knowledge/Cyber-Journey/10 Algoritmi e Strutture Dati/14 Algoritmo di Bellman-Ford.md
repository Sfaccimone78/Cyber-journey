---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Algoritmo di Bellman-Ford", "Bellman-Ford"]
---

# Algoritmo di Bellman-Ford (cammini minimi con pesi negativi)

## Definizione
**Bellman-Ford** risolve il **single-source shortest path** anche quando il grafo ha **archi di peso negativo** (purché non esistano **cicli negativi** raggiungibili dalla sorgente — in quel caso il cammino minimo è −∞ e l'algoritmo lo **segnala**). È più lento di [[Algoritmo di Dijkstra]] ma più generale. È sostanzialmente [[Programmazione Dinamica]] sul numero di archi del cammino. [Fonte: Erickson, cap. Shortest Paths]

## Meccanismo / pseudocodice
Idea: un cammino minimo ha al più **V-1 archi**; quindi rilassando **tutti** gli archi V-1 volte le distanze convergono. Un (V-esimo) rilassamento che migliora ancora → c'è un ciclo negativo.
```
BellmanFord(G, s):
    for v in V: dist[v] = ∞; parent[v] = null
    dist[s] = 0
    repeat V-1 times:                       # V-1 passate
        for (u, v, w) in E:
            if dist[u] + w < dist[v]:       # RELAX
                dist[v] = dist[u] + w
                parent[v] = u
    # rilevamento ciclo negativo
    for (u, v, w) in E:
        if dist[u] + w < dist[v]:
            report "ciclo negativo raggiungibile"
```

## Complessità
| | |
|---|---|
| Tempo | **O(V · E)** |
| Spazio | O(V) |
| Best / Avg / Worst | tutti O(V·E) (deterministico; ottimizzabile con early-exit se una passata non cambia nulla) |

Confronto con Dijkstra: O(V·E) vs O((V+E) log V). Dijkstra vince su grafi con soli pesi non negativi; Bellman-Ford è obbligatorio con pesi negativi.

## Esempio
**Arbitraggio valutario**: nodi = valute, peso arco = −log(tasso di cambio). Un **ciclo negativo** indica un'opportunità di arbitraggio (sequenza di conversioni che produce profitto). Bellman-Ford lo rileva. In **routing**, l'algoritmo **distance-vector** (RIP) è una versione distribuita di Bellman-Ford: ogni router aggiorna le distanze dai vicini. [Fonte: Erickson, cap. Shortest Paths]

## Collegamenti
- Vedi anche: [[Algoritmo di Dijkstra]] (più veloce ma solo pesi ≥ 0), [[Programmazione Dinamica]] (Bellman-Ford è DP), [[Grafi]], [[BFS e DFS]]

## Fonti
- [Erickson, cap. Shortest Paths]
- CLRS — *Introduction to Algorithms*, §24.1 "The Bellman-Ford algorithm".
