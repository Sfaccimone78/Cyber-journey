---
tipo: sintesi
tag: [algoritmi, sintesi]
fase: 0
aggiornato: 2026-06-25
stato: attivo
aliases: ["Da problema ad algoritmo"]
---

# Da problema ad algoritmo (mappa decisionale)

Mappa "tipo di problema → tecnica/struttura dati consigliata". Punto di partenza per scegliere l'approccio prima di scrivere codice.

## Cammini e grafi

| Problema | Soluzione | Perché |
|----------|-----------|--------|
| Cammino minimo, grafo **non pesato** | [[BFS e DFS]] (BFS) | BFS esplora per livelli = distanza in archi |
| Cammino minimo, **pesi ≥ 0** | [[Dijkstra]] | greedy con priority queue |
| Cammino minimo, **pesi negativi** / rileva ciclo negativo | [[Bellman-Ford]] | rilassa tutti gli archi V-1 volte |
| Cammini minimi **tra tutte le coppie** | Floyd-Warshall | DP O(V³) |
| Connettere tutti i nodi a costo minimo | MST (Kruskal/Prim) — [[Algoritmi Greedy]] | sottostruttura greedy |
| Ordinare task con dipendenze | Topological sort (DFS) | ordine post-visita invertito su DAG |
| Rilevare cicli / componenti connesse | [[BFS e DFS]] (DFS) | back edge / visita |
| Raggiungibilità, flood fill | [[BFS e DFS]] | visita da sorgente |

## Ricerca e ordinamento

| Problema | Soluzione | Perché |
|----------|-----------|--------|
| Cercare in dati **ordinati** | [[Ricerca]] binary search O(log n) | dimezza lo spazio |
| Cercare in dati non ordinati | linear search, o [[Hash Table]] se molte query | hash → O(1) lookup |
| Ordinare, serve **stabilità** | merge sort / Timsort | preserva ordine chiavi uguali |
| Ordinare, **memoria stretta** | heapsort | in-place, O(n log n) garantito |
| Ordinare **interi in range limitato** | counting / radix sort | lineare, aggira Ω(n log n) |
| K-esimo elemento / mediana | Quickselect O(n) avg, o [[Heap e Priority Queue]] | partizione / heap di dimensione k |
| Top-K elementi da uno stream | min-heap di dimensione k | O(n log k) |

## Strutture per accesso e associazioni

| Esigenza | Struttura | Perché |
|----------|-----------|--------|
| Lookup chiave→valore O(1) | [[Hash Table]] | hashing |
| Mantenere ordine + range query | BST bilanciato / [[Skip List]] | O(log n) ordinato |
| Min/Max ripetuto (scheduling) | [[Heap e Priority Queue]] | extract-min O(log n) |
| LIFO / undo / parsing | stack ([[Stack e Queue]]) | ultimo-in-primo-out |
| FIFO / buffer / BFS | queue ([[Stack e Queue]]) | primo-in-primo-out |
| **Prefissi / autocomplete / longest-prefix** | [[Trie]] | cammino = prefisso, [[IP Routing]] |

## Tecniche di progettazione

| Indizio nel problema | Tecnica | Riferimento |
|----------------------|---------|-------------|
| Scomponibile a metà, sottoproblemi **indipendenti** | Divide et impera | [[Divide et Impera]] |
| Sottoproblemi **sovrapposti** + sottostruttura ottima | Programmazione dinamica | [[Programmazione Dinamica]] |
| Ottimizzazione, scelta locale ottima è globale | Greedy | [[Algoritmi Greedy]] |
| **Interval scheduling** (max attività compatibili) | Greedy (ordina per fine) | [[Algoritmi Greedy]], [[Scheduling]] |
| Esplorare tutte le configurazioni con vincoli (N-regine, Sudoku, subset) | Backtracking | [[Backtracking]] |
| Knapsack, edit distance, LCS, subset-sum | Programmazione dinamica | [[Programmazione Dinamica]] |
| Coin change (sistema canonico) | Greedy; altrimenti DP | [[Algoritmi Greedy]] / [[Programmazione Dinamica]] |

## Sicurezza / crittografia (ponte)

| Problema | Strumento | Riferimento |
|----------|-----------|-------------|
| Integrità / fingerprint dati | funzione hash | [[Funzioni Hash]], [[Algoritmi Crittografici]] |
| Cifratura asimmetrica / firma | RSA (durezza fattorizzazione) | [[RSA]], [[Complessità Computazionale]] |
| Perché un cifrario "regge" | intrattabilità computazionale (P vs NP) | [[Complessità Computazionale]] |
| Timing / collision attack | sfruttano complessità e probabilità collisioni | [[Attacchi Crittografici]] |

## Collegamenti
- Vedi anche: [[Big-O Cheatsheet]] (i costi delle opzioni), e ogni concetto referenziato.

## Fonti
- [Erickson, panoramica trasversale: Recursion / DP / Greedy / Graphs] → [[Algorithms (Jeff Erickson)]]
- [ODS, scelta della struttura dati per interfaccia, capp. 1-13] → [[Open Data Structures (Pat Morin)]]
