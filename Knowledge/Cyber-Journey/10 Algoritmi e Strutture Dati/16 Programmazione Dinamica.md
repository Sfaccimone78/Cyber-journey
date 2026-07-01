---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Programmazione Dinamica"]
---

# Programmazione dinamica (Dynamic Programming)

## Definizione
La **programmazione dinamica** (DP) risolve problemi scomponendoli in **sottoproblemi sovrapposti** e riusando le soluzioni già calcolate, invece di ricalcolarle. Erickson la descrive come **"ricorsione intelligente"**: si parte da una formulazione ricorsiva corretta e si elimina la ricomputazione esponenziale. [Fonte: Erickson, cap. Dynamic Programming] Applicabile quando il problema ha:
1. **Sottostruttura ottima** — la soluzione ottima si compone di soluzioni ottime dei sottoproblemi.
2. **Sottoproblemi sovrapposti** — gli stessi sottoproblemi ricorrono molte volte (altrimenti basta [[Divide et Impera]]).

## Meccanismo: due approcci
### Memoization (top-down)
Ricorsione naturale + **cache** dei risultati. Si calcola solo ciò che serve (lazy).
```
memo = {}
def fib(n):
    if n <= 1: return n
    if n in memo: return memo[n]
    memo[n] = fib(n-1) + fib(n-2)
    return memo[n]
```

### Tabulation (bottom-up)
Si riempie una **tabella** dai casi base verso l'alto, in ordine di dipendenza. Spesso più efficiente (niente overhead di ricorsione) e permette ottimizzazione di spazio.
```
def fib(n):
    dp = [0, 1]
    for i in range(2, n+1):
        dp.append(dp[i-1] + dp[i-2])   # spesso riducibile a 2 variabili → O(1) spazio
    return dp[n]
```

| | Memoization | Tabulation |
|---|---|---|
| Direzione | top-down (ricorsivo) | bottom-up (iterativo) |
| Calcola | solo i sottoproblemi necessari | tutti (in ordine) |
| Rischio | stack overflow su ricorsione profonda | nessuno |
| Ottimizzazione spazio | difficile | facile (rolling array) |

## Procedura (ricetta di Erickson)
1. Definisci la **funzione ricorsiva** che esprime la soluzione (specifica cosa significano i parametri).
2. Verifica la **sottostruttura ottima** e scrivi la **ricorrenza** con i casi base.
3. Identifica i sottoproblemi → **stato** e numero di stati.
4. **Memoizza** o **tabula**; stabilisci l'**ordine di valutazione**.
5. Complessità = (numero di stati) × (costo per stato).

## Pattern classici
- **1-D**: Fibonacci, salita scale, cammino max in sequenza, *house robber*.
- **Knapsack** (0/1, illimitato): selezione con vincolo di capacità.
- **Sequenze**: LCS (longest common subsequence), edit distance (Levenshtein), LIS.
- **Su griglia**: cammini in matrice, *minimum path sum*.
- **Su intervalli/alberi**: matrix-chain multiplication, optimal BST.
- **Cammini minimi**: [[Algoritmo di Bellman-Ford]] e Floyd-Warshall sono DP su grafi.

## Complessità
Non c'è un'unica complessità: si misura come **#stati × lavoro/stato**.
- Fibonacci/scale: O(n) tempo, O(1)–O(n) spazio (vs O(2ⁿ) della ricorsione ingenua).
- Knapsack 0/1: O(n·W) (pseudo-polinomiale: dipende dal *valore* W, non dai bit). [Fonte: Erickson, cap. Dynamic Programming]
- LCS / edit distance: O(n·m).

## Esempio
**Edit distance** tra "kitten" e "sitting": `dp[i][j]` = minimo numero di operazioni (inserimento/cancellazione/sostituzione) per trasformare i primi *i* caratteri nei primi *j*. Riempiendo la tabella m×n si ottiene 3. Base di spell-checker e `diff`.

## Collegamenti
- Vedi anche: [[Divide et Impera]] (DP = D&I con sottoproblemi sovrapposti + cache), [[Algoritmi Greedy]] (greedy = DP quando la scelta locale è sempre ottima; spesso più semplice ma non sempre corretto), [[Algoritmo di Bellman-Ford]] (DP su grafi), [[Backtracking]] (DP memoizza ciò che il backtracking riesplora), [[Complessità Computazionale]] (pseudo-polinomialità)

## Fonti
- [Erickson, cap. Dynamic Programming]
- CLRS — *Introduction to Algorithms*, cap. 15 "Dynamic Programming".
