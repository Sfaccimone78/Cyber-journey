---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Alberi Binari e BST", "Alberi Binari"]
---

# Alberi binari, BST e bilanciamento (AVL, Red-Black)

## Definizione
Un **albero binario** è una struttura in cui ogni nodo ha al più due figli (sinistro/destro). Un **Binary Search Tree (BST)** è un albero binario che mantiene la **proprietà di ordinamento**: per ogni nodo `v`, tutte le chiavi nel sottoalbero sinistro sono `< v.key` e quelle nel destro sono `> v.key`. Realizza l'interfaccia **SSet** (insieme ordinato: `find`, `add`, `remove`, più successore/predecessore). [Fonte: ODS, cap. 6]

## Meccanismo
- **Ricerca/inserzione/cancellazione**: si scende dalla radice confrontando la chiave, in tempo proporzionale all'**altezza** dell'albero. [Fonte: ODS, sez. 6.2]
- **Problema**: un BST non bilanciato può degenerare in una lista (altezza O(n)) se le chiavi arrivano ordinate. Serve il **bilanciamento** per garantire altezza O(log n).

### Strategie di bilanciamento
- **AVL tree**: per ogni nodo, le altezze dei due sottoalberi differiscono al più di 1; il riequilibrio avviene con **rotazioni** dopo ogni inserzione/cancellazione. Bilanciamento rigido → ricerche molto veloci. [Fonte: Erickson, cap. DP, esercizio AVL]
- **Red-Black tree**: nodi colorati rosso/nero con invarianti (radice nera, nessun rosso consecutivo, ugual numero di neri su ogni cammino radice-foglia). Garantisce altezza ≤ 2·log(n+1). ODS lo deriva come simulazione di un **2-4 tree** (left-leaning red-black). Bilanciamento più rilassato dell'AVL → meno rotazioni in inserimento. [Fonte: ODS, cap. 9]
- **Treap** (random BST): assegna priorità casuali e mantiene heap-order sulle priorità → altezza O(log n) **attesa** senza logica di rotazione complessa. [Fonte: ODS, cap. 7]
- **Scapegoat tree**: ricostruisce parzialmente sottoalberi quando si sbilanciano troppo → O(log n) ammortizzato. [Fonte: ODS, cap. 8]

## Complessità
| Operazione | BST non bilanciato | AVL / Red-Black | Treap (atteso) |
|------------|--------------------|-----------------|----------------|
| find / add / remove | O(n) peggiore | O(log n) garantito | O(log n) atteso |
| altezza | fino a n | O(log n) | O(log n) atteso |

> AVL vs Red-Black: AVL è più strettamente bilanciato (ricerche più rapide), Red-Black fa meno lavoro di ribilanciamento in scrittura. Red-Black è usato in `std::map` (C++), `TreeMap` (Java), scheduler del kernel Linux.

## Esempio
Mappa ordinata che richiede query di intervallo o "trova il più piccolo elemento ≥ x"; indici di database; tabelle dei processi ordinate. Per memoria esterna (disco), si usano i **B-tree** (generalizzazione multi-via). [Fonte: ODS, cap. 14]

## Collegamenti
- Vedi anche: [[Hash Table]] (USet non ordinato vs SSet ordinato), [[Heap e Priority Queue]] (heap = albero con ordine sui livelli, non sulle chiavi), [[Skip List]] (alternativa probabilistica all'SSet)
- Ponte sistemi/reti: i **B-tree** stanno alla base degli indici di filesystem e database → vedi [[Filesystem Linux]].

## Fonti
- [ODS, cap. 6 Binary Trees, pp. 127-140]
- [ODS, cap. 7 Random BST / cap. 8 Scapegoat / cap. 9 Red-Black Trees, pp. 145-198]
- [ODS, cap. 14 External Memory Searching (B-Trees), pp. 275-296]
- [Erickson, cap. Dynamic Programming, esercizi su AVL/Red-Black]