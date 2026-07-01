---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Skip List"]
---

# Skip List

## Definizione
Una **skip list** è una struttura dati **randomizzata** che realizza l'interfaccia SSet (insieme ordinato) con operazioni in **O(log n) attese**, usando solo liste collegate con "scorciatoie" — senza la logica di rotazione/ribilanciamento dei BST. È l'alternativa probabilistica agli alberi bilanciati. [Fonte: ODS, cap. 4]

## Meccanismo
- Si costruisce una **gerarchia di liste collegate** L0, L1, L2, … La lista L0 contiene tutti gli elementi ordinati; ogni elemento di Li compare in Li+1 con probabilità 1/2 (lancio di moneta). [Fonte: ODS, sez. 4.1]
- Le liste superiori sono "express lane" sempre più rade: un elemento ha **altezza** pari al numero di teste consecutive ottenute.
- **search(x)**: si parte dalla lista più alta a sinistra e si scende: si avanza finché il prossimo nodo supererebbe x, poi si scende di un livello. Il cammino di ricerca ha lunghezza attesa O(log n). [Fonte: ODS, sez. 4.2]
- **add/remove**: trova la posizione, poi inserisce/rimuove il nodo a tutti i livelli della sua altezza casuale.

## Complessità
| Operazione | Skip list (atteso) | Peggiore |
|------------|--------------------|----------|
| find / add / remove | O(log n) | O(n) (raro, prob. esponenzialmente bassa) |
| spazio | O(n) atteso | — |

> Vantaggio pratico: codice molto più semplice di un red-black tree, ottime prestazioni medie, facile da rendere concorrente (usata in Redis per i sorted set, in alcuni filesystem e DB).

## Esempio
Sorted set di Redis (ZSET), indici in memoria, strutture concorrenti (`ConcurrentSkipListMap` in Java) dove la semplicità di locking conta più del bilanciamento garantito.

## Collegamenti
- Vedi anche: [[Array vs Linked List]] (la skip list parte da liste collegate), [[Alberi Binari e BST]] (stesso scopo, SSet, ma deterministico), [[Complessità Computazionale]] (analisi attesa/randomizzata)

## Fonti
- [ODS, cap. 4 Skiplists, pp. 83-97]
- Pugh, W. (1990) — "Skip Lists: A Probabilistic Alternative to Balanced Trees", CACM 33(6): https://doi.org/10.1145/78973.78977
