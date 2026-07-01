---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Algoritmi Greedy"]
---

# Algoritmi greedy (golosi)

## Definizione
Un algoritmo **greedy** costruisce la soluzione facendo, a ogni passo, la **scelta localmente ottima** (quella che sembra migliore ora) senza tornare indietro, sperando di raggiungere l'ottimo **globale**. È semplice e veloce, ma **corretto solo se** il problema gode della **proprietà della scelta greedy** (una scelta locale ottima fa parte di una soluzione globale ottima) e di **sottostruttura ottima**. Quando non vale, il greedy dà soluzioni subottime e serve [[Programmazione Dinamica]]. [Fonte: Erickson, cap. Greedy Algorithms]

> ⚠️ Dimostrare la correttezza è la parte difficile: tipicamente con argomento di **scambio** (exchange argument) — qualunque soluzione ottima può essere trasformata in quella greedy senza peggiorare.

## Meccanismo / pseudocodice (schema generale)
```
greedy(elementi):
    soluzione = ∅
    ordina/valuta gli elementi secondo un criterio greedy
    for e in elementi (in quell'ordine):
        if e è compatibile con soluzione:
            soluzione.add(e)        # scelta irrevocabile
    return soluzione
```

## Esempi canonici
- **Interval scheduling** (max attività compatibili): ordina per **tempo di fine** crescente, prendi sempre la prima che non si sovrappone. Ottimo. [Fonte: Erickson, cap. Greedy]
- **Codici di Huffman** (compressione): fonde ripetutamente i due simboli meno frequenti con un [[Heap e Priority Queue]] → codice prefisso ottimo.
- **MST**: **Kruskal** (arco più leggero che non crea ciclo, con union-find) e **Prim** (espande l'albero con l'arco minimo uscente). Entrambi greedy e ottimi su [[Grafi]].
- **[[Algoritmo di Dijkstra]]**: finalizza sempre il vertice con distanza provvisoria minima — greedy.
- **Coin change** con sistema **canonico** (es. €): prendi sempre la moneta più grande. ⚠️ Con sistemi non canonici il greedy **fallisce** → serve DP.

## Complessità
Tipicamente dominata dall'ordinamento o dalla struttura dati di supporto:
| Problema greedy | Complessità |
|------------------|-------------|
| Interval scheduling | O(n log n) (ordinamento) |
| Huffman | O(n log n) (priority queue) |
| Kruskal | O(E log V) (sort archi + union-find) |
| Prim (binary heap) | O(E log V) |
| Dijkstra (binary heap) | O((V+E) log V) |

## Greedy vs Dynamic Programming
| | Greedy | DP |
|---|--------|----|
| Scelte | una sola, irrevocabile per passo | esplora/combina più scelte |
| Velocità | più veloce | più lento ma sempre corretto (se applicabile) |
| Correttezza | solo se vale la proprietà greedy | sottostruttura ottima sovrapposta |
| Esempio | coin change canonico, MST | knapsack 0/1, coin change generico |

## Esempio
Sala conferenze, 5 talk con orari sovrapposti: ordinandoli per orario di fine e scegliendo sempre il prossimo compatibile si massimizza il numero di talk ospitati — risultato provatamente ottimo, in O(n log n).

## Collegamenti
- Vedi anche: [[Programmazione Dinamica]] (quando il greedy non basta), [[Algoritmo di Dijkstra]] (greedy su grafi), [[Grafi]] (MST), [[Heap e Priority Queue]] (supporto a Huffman/Prim), [[Divide et Impera]]

## Fonti
- [Erickson, cap. Greedy Algorithms / Minimum Spanning Trees]
- CLRS — *Introduction to Algorithms*, cap. 16 "Greedy Algorithms" (+ cap. 23 MST).
