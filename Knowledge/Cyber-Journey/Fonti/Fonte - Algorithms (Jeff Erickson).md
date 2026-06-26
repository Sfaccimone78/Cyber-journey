---
tipo: fonte
tag: [algoritmi]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
url: https://jeffe.cs.illinois.edu/teaching/algorithms/
autore: Jeff Erickson
aliases: ["Algorithms (Jeff Erickson)"]
---

# Fonte - Algorithms (Jeff Erickson)

## Panoramica
*Algorithms* di Jeff Erickson (University of Illinois Urbana-Champaign) è un manuale gratuito (Creative Commons) nato da appunti per corsi di teoria degli algoritmi di livello junior. È un libro di **progettazione di algoritmi**: insegna a progettare, dimostrare corretti e analizzare algoritmi, più che a catalogarli. [Fonte: Erickson, Preface]

## Approccio
- **Centrato sui paradigmi di progettazione**, non sulle strutture dati. I capitoli sono organizzati per tecnica: ricorsione → backtracking → programmazione dinamica → greedy → algoritmi su grafi.
- **Rigore matematico**: ogni algoritmo è accompagnato dalla derivazione di una ricorrenza di costo e da una prova di correttezza (induzione strutturale). Esempio tipico: per Subset Sum deriva `T(n) ≤ 2·T(n−1) + O(1)` da cui `T(n) = O(2ⁿ)`, riconducendolo alla ricorrenza della Torre di Hanoi. [Fonte: Erickson, cap. Dynamic Programming]
- **Filosofia "Smart Recursion"**: la programmazione dinamica è presentata come backtracking + memoization, non come tecnica separata. Il mantra è "prima la ricorsione corretta, poi la tabella".
- **Avvertenza ricorrente**: *"Greed is Stupid"* — gli algoritmi greedy raramente sono corretti e vanno sempre dimostrati con argomenti di scambio (exchange argument). [Fonte: Erickson, cap. Greedy Algorithms]

## Audience
Studenti che **hanno già** un corso di strutture dati e uno di matematica discreta. Presuppone familiarità con: notazione asintotica, induzione, alberi/grafi come oggetti astratti, BST bilanciati, hash table, heap binari. Non è un primo libro di strutture dati. [Fonte: Erickson, Prerequisites]

## Contenuti principali (per capitolo)
| Capitolo | Concetti chiave | Pagina wiki |
|----------|-----------------|-------------|
| Recursion | divide-et-impera, Mergesort, Quicksort, selezione lineare, moltiplicazione veloce (Karatsuba) | [[Divide et Impera]], [[Ordinamento (Sorting)]] |
| Backtracking | N-Queens, Subset Sum, game trees, text segmentation, LIS | [[Backtracking]] |
| Dynamic Programming | edit distance, Optimal BST, DP su alberi, Fibonacci | [[Programmazione Dinamica]] |
| Greedy Algorithms | scheduling, codici di Huffman, stable matching (Gale-Shapley) | [[Algoritmi Greedy]] |
| Basic Graph Algorithms | rappresentazioni, whatever-first search, flood fill | [[Grafi]], [[BFS e DFS]] |
| Depth-First Search | preorder/postorder, topological sort, componenti fortemente connesse | [[BFS e DFS]] |
| Minimum Spanning Trees | Borůvka, Jarník/Prim, Kruskal | [[Grafi]] |
| Shortest Paths | BFS (non pesati), Dijkstra, Bellman-Ford, DAG | [[Dijkstra]], [[Bellman-Ford]] |
| All-Pairs Shortest Paths | Floyd-Warshall, Johnson | [[Dijkstra]] |
| NP-Hardness | riduzioni, P vs NP, intrattabilità | [[Complessità Computazionale]] |

## Concetti unici vs sovrapposti con ODS
- **Unici di Erickson**: paradigmi di design (backtracking, DP, greedy, divide-et-impera) con prove formali; algoritmi su grafi pesati (Dijkstra, Bellman-Ford, MST, Floyd-Warshall); teoria NP-hardness; selezione lineare; moltiplicazione veloce.
- **Sovrapposti con [[Open Data Structures (Pat Morin)]]**: sorting (Merge/Quick/Heap, lower bound Ω(n log n)), BFS/DFS, rappresentazioni di grafi, ordinamento per confronto vs per chiave.
- **Demarcazione**: Erickson assume le strutture dati come "scatole nere" già note (ADT) e si concentra su *cosa farci*; ODS apre le scatole e mostra *come sono costruite*.

## Collegamenti
- [[index]]
- Vedi anche: [[Open Data Structures (Pat Morin)]], [[Da problema ad algoritmo]], [[Complessità Computazionale]]

## Fonti
- [Erickson, Preface, About This Book, pp. i–vii]
- [Erickson, Table of Contents, p. ix–xii]
- [Erickson, cap. Dynamic Programming / Greedy Algorithms / Shortest Paths]
- Sito ufficiale: <https://jeffe.cs.illinois.edu/teaching/algorithms/>
