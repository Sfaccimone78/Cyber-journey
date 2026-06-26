---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Algoritmi di Ricerca", "Ricerca"]
---

# Algoritmi di ricerca (linear, binary, interpolation)

## Definizione
**Cercare** = determinare se (e dove) un valore *x* è presente in una collezione. La scelta dell'algoritmo dipende dalla struttura: dati **non ordinati** → ricerca lineare; dati **ordinati** → ricerca binaria (o interpolazione). [Fonte: Erickson, cap. Searching / ODS, cap. 1]

## Meccanismo / pseudocodice

### Linear search (ricerca sequenziale)
Scorre ogni elemento. Unico metodo possibile su dati **non ordinati**.
```
for i in 0..n-1:
    if A[i] == x: return i
return -1
```

### Binary search (ricerca binaria — divide et impera)
Su array **ordinato**: confronta col mezzo, scarta metà collezione a ogni passo.
```
lo, hi = 0, n-1
while lo <= hi:
    mid = (lo + hi) // 2
    if A[mid] == x: return mid
    elif A[mid] < x: lo = mid + 1
    else: hi = mid - 1
return -1
```
È [[Divide et Impera]]: dimezza lo spazio → O(log n). Variante chiave: **lower_bound** (primo elemento ≥ x) per inserimenti ordinati.

### Interpolation search
Su array ordinato **uniformemente distribuito**: invece del centro, stima la posizione probabile interpolando il valore (come si cerca su un elenco telefonico).
```
pos = lo + (x - A[lo]) * (hi - lo) // (A[hi] - A[lo])
```
O(log log n) medio su dati uniformi, ma degrada a **O(n)** su distribuzioni sbilanciate.

## Complessità
| Algoritmo | Best | Average | Worst | Requisito |
|-----------|------|---------|-------|-----------|
| Linear | O(1) | O(n) | O(n) | nessuno |
| **Binary** | O(1) | O(log n) | O(log n) | array **ordinato** |
| Interpolation | O(1) | **O(log log n)** | O(n) | ordinato + distribuzione uniforme |

> Per molte ricerche ripetute conviene una struttura dedicata: [[Hash Table]] (O(1) lookup, niente ordine) o BST/[[Skip List]] (O(log n) ordinato).

## Esempio
Dizionario ordinato di 1.000.000 parole: binary search trova qualsiasi parola in ≤20 confronti, contro ~500.000 medi della lineare. La binary search è anche il pattern del **binary search on the answer** (cercare il minimo/massimo valore che soddisfa un predicato monotòno).

## Collegamenti
- Vedi anche: [[Divide et Impera]] (binary search ne è l'esempio minimale), [[Algoritmi di Ordinamento]] (binary search presuppone dati ordinati), [[Hash Table]] e [[Alberi Binari e BST]] (alternative per ricerche frequenti), [[Complessità Computazionale]] (O(log n) vs O(n))

## Fonti
- [Erickson, cap. Searching / Divide-and-Conquer]
- [ODS, cap. 1 (ricerca in SSet/USet), pp. 6-13]