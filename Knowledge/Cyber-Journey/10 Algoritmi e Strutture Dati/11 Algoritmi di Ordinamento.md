---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Algoritmi di Ordinamento", "Ordinamento (Sorting)"]
---

# Algoritmi di ordinamento (sorting)

## Definizione
**Ordinare** = riordinare *n* elementi secondo una relazione d'ordine totale. I **comparison sort** (basati su confronti) hanno un limite inferiore dimostrato di **Ω(n log n)** confronti nel caso peggiore — nessun algoritmo basato su soli confronti può fare meglio. [Fonte: Erickson, cap. Sorting] Due proprietà chiave: **stabile** (preserva l'ordine relativo di elementi con chiave uguale) e **in-place** (usa O(1) o O(log n) memoria ausiliaria).

## Meccanismo / pseudocodice

### Insertion sort (incrementale)
Costruisce il prefisso ordinato inserendo un elemento alla volta nella posizione giusta.
```
for i in 1..n-1:
    key = A[i]; j = i-1
    while j >= 0 and A[j] > key: A[j+1] = A[j]; j -= 1
    A[j+1] = key
```
Ottimo su array **quasi ordinati** (O(n) best case). Stabile, in-place.

### Bubble sort
Scambi ripetuti di coppie adiacenti fuori ordine fino a stabilità. Didattico, lento. Stabile, in-place.

### Merge sort (divide et impera)
Divide a metà, ordina ricorsivamente, **fonde** (merge) le due metà ordinate.
```
mergesort(A):
    if len(A) <= 1: return A
    m = len(A)//2
    L = mergesort(A[:m]); R = mergesort(A[m:])
    return merge(L, R)        # fonde due liste ordinate in O(n)
```
**Sempre** O(n log n) (best=avg=worst). **Stabile**. **Non in-place** (O(n) extra). È il [[Divide et Impera]] per eccellenza.

### Quicksort (divide et impera)
Sceglie un **pivot**, **partiziona** (minori a sinistra, maggiori a destra), ricorre sulle due parti.
```
quicksort(A, lo, hi):
    if lo < hi:
        p = partition(A, lo, hi)   # pivot al posto finale
        quicksort(A, lo, p-1); quicksort(A, p+1, hi)
```
O(n log n) atteso, ma **O(n²)** se il pivot è sempre pessimo (array già ordinato + pivot=primo elemento). Mitigazione: pivot **casuale** o mediana-di-tre → peggiore improbabile. In-place, **non stabile**. In pratica il più veloce per via della **località di cache**.

### Heapsort
Costruisce un max-[[Heap e Priority Queue|heap]] (O(n)), poi estrae il massimo *n* volte.
```
build_max_heap(A)
for i in n-1..1: swap(A[0], A[i]); heap_size -= 1; sift_down(A, 0)
```
**Sempre** O(n log n). In-place, **non stabile**. Nessun caso peggiore quadratico (a differenza di quicksort).

### Sorting non a confronti (lineari)
**Counting sort** / **Radix sort** ordinano in **O(n + k)** / O(d·n) sfruttando la struttura delle chiavi (interi limitati), aggirando il limite Ω(n log n). Radix sort usa counting sort stabile cifra per cifra.

## Complessità (riepilogo)
| Algoritmo | Best | Average | Worst | Spazio | Stabile | In-place |
|-----------|------|---------|-------|--------|---------|----------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | sì | sì |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | sì | sì |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | no | sì |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | **sì** | no |
| Quick | O(n log n) | O(n log n) | **O(n²)** | O(log n) | no | sì |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | no | sì |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(k) | sì | no |
| Radix | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | sì | no |

## Quando usare cosa
- **Stabilità richiesta** (ordinamento multi-chiave): merge sort. `Timsort` (merge+insertion, in Python `sorted` e Java) è stabile e adattivo.
- **Memoria stretta / worst-case garantito**: heapsort.
- **Velocità media pura, dati in RAM**: quicksort (randomizzato).
- **Dati quasi ordinati / piccoli**: insertion sort.
- **Chiavi intere in range limitato**: counting/radix (lineare).

## Collegamenti
- Vedi anche: [[Divide et Impera]] (merge & quick), [[Heap e Priority Queue]] (heapsort), [[Complessità Computazionale]] (limite Ω(n log n)), [[Algoritmi di Ricerca]] (binary search richiede dati ordinati)

## Fonti
- [Erickson, cap. Sorting / Divide-and-Conquer]
- [ODS, sez. 11 Sorting Algorithms, pp. 219-238]