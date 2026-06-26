---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Divide et Impera"]
---

# Divide et impera (Divide and Conquer)

## Definizione
**Divide et impera** è un paradigma in **tre fasi**: **Divide** il problema in sottoproblemi più piccoli **dello stesso tipo**, **Impera** (conquer) risolvendoli ricorsivamente, **Combina** le sottosoluzioni nella soluzione finale. Si applica quando i sottoproblemi sono **indipendenti** (se invece si sovrappongono, serve [[Programmazione Dinamica]]). [Fonte: Erickson, cap. Divide and Conquer]

## Meccanismo / pseudocodice (schema)
```
divide_conquer(P):
    if P è abbastanza piccolo: return soluzione_diretta(P)   # caso base
    dividi P in P1, P2, ..., Pa
    soluzioni = [divide_conquer(Pi) for Pi]                  # ricorsione
    return combina(soluzioni)                                # merge
```

## Analisi: il Master Theorem
Il costo si esprime con una **ricorrenza** T(n) = a·T(n/b) + f(n), dove *a* = numero di sottoproblemi, *n/b* = loro dimensione, *f(n)* = costo di divide+combina. Il **Master Theorem** dà la soluzione confrontando f(n) con n^(log_b a): [Fonte: Erickson, cap. Recurrences]
- se f(n) cresce **più lentamente** → T(n) = Θ(n^(log_b a)) (dominano le foglie),
- se **uguale** → T(n) = Θ(n^(log_b a) · log n),
- se **più velocemente** (regolarità) → T(n) = Θ(f(n)) (domina la radice).

Esempi: merge sort 2T(n/2)+O(n) → **Θ(n log n)**; binary search T(n/2)+O(1) → **Θ(log n)**; Karatsuba 3T(n/2)+O(n) → **Θ(n^1.585)**.

## Esempi canonici
- **[[Algoritmi di Ordinamento]]**: **Merge sort** (divide a metà, fonde) e **Quicksort** (partiziona sul pivot, ricorre).
- **[[Algoritmi di Ricerca]]**: **Binary search** (dimezza lo spazio) — il caso più semplice (un solo sottoproblema).
- **Moltiplicazione veloce**: **Karatsuba** (interi grandi), **Strassen** (matrici) battono l'algoritmo scolastico.
- **FFT** (trasformata di Fourier veloce) O(n log n).
- **Closest pair of points** nel piano, O(n log n).

## Complessità
Dipende dalla ricorrenza specifica (vedi Master Theorem sopra). Pattern tipico: dividere in due dà profondità O(log n); se ogni livello costa O(n) → O(n log n).

## Divide et impera vs Dynamic Programming
| | Divide et impera | DP |
|---|------------------|----|
| Sottoproblemi | **indipendenti** (no riuso) | **sovrapposti** (riuso con cache) |
| Esempio | merge sort, binary search | Fibonacci, knapsack |
| Tecnica | ricorsione pura | memoization / tabulation |

## Esempio
Merge sort su `[5,2,8,1]`: divide in `[5,2]` e `[8,1]`, ordina ricorsivamente in `[2,5]` e `[1,8]`, fonde in `[1,2,5,8]`. Tre livelli, O(n) di merge ciascuno → O(n log n), stabile e prevedibile.

## Collegamenti
- Vedi anche: [[Algoritmi di Ordinamento]] (merge & quick), [[Algoritmi di Ricerca]] (binary search), [[Programmazione Dinamica]] (D&I + sottoproblemi sovrapposti), [[Complessità Computazionale]] (ricorrenze, Master Theorem)

## Fonti
- [Erickson, cap. Divide and Conquer / Recurrences]