---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Backtracking"]
---

# Backtracking (ricerca con ritorno)

## Definizione
Il **backtracking** è una tecnica di **ricerca esaustiva incrementale**: costruisce una soluzione **un pezzo alla volta** e, appena un candidato parziale viola un vincolo (non potrà mai completarsi in una soluzione valida), **abbandona quel ramo** (backtrack) e torna alla scelta precedente. È una [[BFS e DFS|DFS]] sull'**albero delle decisioni**, con **potatura** (pruning) dei rami senza speranza. [Fonte: Erickson, cap. Backtracking]

## Meccanismo / pseudocodice (schema)
```
backtrack(soluzione_parziale):
    if è_completa(soluzione_parziale):
        registra / return soluzione
        return
    for scelta in scelte_possibili(soluzione_parziale):
        if è_valida(scelta):                  # pruning: scarta subito i rami morti
            soluzione_parziale.add(scelta)
            backtrack(soluzione_parziale)     # esplora in profondità
            soluzione_parziale.remove(scelta) # BACKTRACK: annulla la scelta
```
La riga di `remove` (annullamento) è ciò che distingue il backtracking dalla semplice ricorsione: lo stato viene **ripristinato** per provare alternative.

## Esempi canonici
- **N-regine**: posiziona regine riga per riga; se una colonna/diagonale è attaccata, backtrack.
- **Sudoku solver**: prova le cifre 1-9 in una cella; se nessuna è valida, torna indietro.
- **Permutazioni / combinazioni / subset**: genera tutte le configurazioni.
- **Subset sum / partizione**: includi o escludi ogni elemento.
- **Cammini in labirinto**, colorazione di grafi, parsing.

## Complessità
Nel **caso peggiore** è **esponenziale** (esplora tutto l'albero): O(bᵈ) con *b* ramificazione e *d* profondità — es. permutazioni O(n!), subset O(2ⁿ). Il **pruning** non cambia la classe worst-case ma in pratica taglia enormi porzioni di spazio, rendendo trattabili istanze reali. Quando i sottoproblemi si **sovrappongono**, memoizzarli trasforma il backtracking in [[Programmazione Dinamica]] (riduzione da esponenziale a polinomiale).

| | |
|---|---|
| Best | O(d) (trova subito / pota presto) |
| Worst | O(bᵈ) esponenziale (es. O(n!), O(2ⁿ)) |
| Spazio | O(d) (profondità ricorsione) |

> Branch and bound estende il backtracking con un **limite (bound)** sul valore ottenibile, per potare rami non solo invalidi ma anche **non ottimali** (usato per problemi NP-hard come TSP).

## Esempio
Sudoku: si sceglie la prima cella vuota, si prova `1`; se è coerente con riga/colonna/blocco si passa alla cella successiva, altrimenti `2`, ecc. Se tutte le cifre falliscono, si torna alla cella precedente e si cambia la sua cifra. La potatura per vincoli rende il solver praticamente istantaneo nonostante lo spazio teorico enorme.

## Collegamenti
- Vedi anche: [[BFS e DFS]] (backtracking = DFS sull'albero delle scelte), [[Programmazione Dinamica]] (memoizza i sottoproblemi che il backtracking riesplora), [[Trie]] (la sua visita è un DFS strutturato), [[Complessità Computazionale]] (spazi esponenziali, NP)

## Fonti
- [Erickson, cap. Backtracking]