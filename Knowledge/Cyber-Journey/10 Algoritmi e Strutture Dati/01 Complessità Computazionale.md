---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-07-02
stato: maturo
aliases: ["Complessità Computazionale"]
---

# Complessità Computazionale (O, Ω, Θ, P vs NP)

## In breve

La **complessità computazionale** descrive come tempo e spazio richiesti da un algoritmo crescono con la dimensione dell'input *n*, in modo **asintotico** (ignorando costanti e termini minori). È il linguaggio con cui si confrontano algoritmi indipendentemente dall'hardware, tramite le notazioni **O/Ω/Θ**, e la cornice teorica delle classi **P vs NP** su cui poggia la sicurezza della crittografia asimmetrica.

## Definizione
La **complessità computazionale** misura quanto **tempo** (numero di operazioni) e **spazio** (memoria) un algoritmo richiede in funzione della dimensione dell'input *n*, in modo **asintotico** — ignorando costanti e termini di ordine inferiore, per confrontare algoritmi indipendentemente dall'hardware. [Fonte: Erickson, cap. Asymptotic Analysis / ODS, cap. 1]

## Notazione asintotica
Date due funzioni f(n), g(n) ≥ 0:

| Notazione | Significato | Intuizione |
|-----------|-------------|------------|
| **O(g)** | f cresce **al più** come g | limite **superiore** (worst case) — ∃ c,n₀: f(n) ≤ c·g(n) ∀n≥n₀ |
| **Ω(g)** | f cresce **almeno** come g | limite **inferiore** (best case / lower bound del problema) |
| **Θ(g)** | f cresce **esattamente** come g | limite **stretto**: f = O(g) **e** f = Ω(g) |
| o(g) / ω(g) | strettamente minore / maggiore | limiti non stretti |

> Distinzione chiave: **caso peggiore/medio/migliore** (proprietà di un *algoritmo* su input variabili) ≠ **O/Ω/Θ** (relazioni tra *funzioni*). Si può dire "il caso migliore di insertion sort è Θ(n)". Dire "O(n²) nel caso peggiore" significa: il tempo nel caso peggiore è limitato superiormente da n².

## Gerarchia delle classi di crescita
Dal più veloce al più lento:
```
O(1) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)
costante  log    radice  lineare  linearitm.  quadr.  cubico  esponenz. fattoriale
```
- **Polinomiale** (nᵏ): trattabile, "efficiente".
- **Esponenziale** (2ⁿ, n!): intrattabile oltre input piccoli (forza bruta, alcuni [[Backtracking]]).

## P vs NP
La grande questione aperta dell'informatica teorica. [Fonte: Erickson, cap. NP-Hardness]

| Classe | Definizione |
|--------|-------------|
| **P** | Problemi **risolvibili** in tempo polinomiale da una macchina deterministica. |
| **NP** | Problemi la cui soluzione è **verificabile** in tempo polinomiale (Nondeterministic Polynomial). |
| **NP-completi** | I più difficili in NP: se uno si risolve in P, **tutti** quelli in NP si risolvono (SAT, clique, ciclo hamiltoniano, knapsack, TSP decisionale). Riduzioni polinomiali li collegano. |
| **NP-hard** | Almeno difficili quanto NP-completi, non necessariamente in NP. |

- Ovviamente **P ⊆ NP** (se risolvi, verifichi). Se **P = NP?** è il problema aperto: nessuno sa se i problemi facili-da-verificare siano anche facili-da-risolvere. Si congettura **P ≠ NP**.
- **Rilevanza crittografica**: la sicurezza pratica di [[RSA]] poggia sulla **presunta** difficoltà (non in P note) della **fattorizzazione**, e di Diffie-Hellman sul **logaritmo discreto**. Se P=NP (o emergesse un algoritmo polinomiale), gran parte della crittografia asimmetrica crollerebbe.

## Esempio
Ricerca in array ordinato: lineare O(n) vs [[Algoritmi di Ricerca|ricerca]] binaria O(log n) — per n = 1 miliardo, ~30 confronti contro 1 miliardo. Il limite **Ω(n log n)** degli [[Algoritmi di Ordinamento|ordinamenti]] a confronti dimostra che merge/heap sort sono **ottimali** (non migliorabili asintoticamente con soli confronti).

## Lab

Non esiste un "problema" isolato sulla complessità: si allena **analizzando** ogni soluzione che scrivi. Pattern consigliato: risolvi in forza bruta, calcola O(tempo)/O(spazio), poi ottimizza e riconfronta.

- **LeetCode #1 *Two Sum***: brute force O(n²) → hash map O(n) tempo / O(n) spazio. Classico esempio di trade-off tempo-memoria.
- **LeetCode #217 *Contains Duplicate***: ordina + scorri O(n log n) vs set O(n); confronta anche lo spazio.
- **LeetCode #53 *Maximum Subarray***: O(n²) ingenuo vs Kadane O(n) — mostra come un'idea algoritmica abbatte una classe di crescita.
- **NeetCode.io – roadmap "Big-O / Arrays & Hashing"**: per ogni problema, dichiara la complessità *prima* di sottomettere e verifica con l'analisi ufficiale.

## Domande

1. **D:** Qual è la differenza tra O, Ω e Θ?  **R:** `O(g)` è un limite **superiore** (f cresce al più come g), `Ω(g)` un limite **inferiore** (f cresce almeno come g), `Θ(g)` un limite **stretto** (f è sia O(g) sia Ω(g), cresce esattamente come g).
2. **D:** "Caso peggiore" e "O grande" sono sinonimi?  **R:** No. Caso peggiore/medio/migliore sono proprietà di un *algoritmo* su input variabili; O/Ω/Θ sono relazioni tra *funzioni*. Si può dire "il caso migliore di insertion sort è Θ(n)": si applica una notazione asintotica stretta a uno specifico caso.
3. **D:** Perché merge sort e heap sort sono considerati ottimali tra gli ordinamenti a confronti?  **R:** Perché raggiungono O(n log n) e il lower bound dimostrato per l'ordinamento basato su confronti è **Ω(n log n)**: nessun algoritmo a soli confronti può fare asintoticamente meglio.
4. **D:** Che relazione c'è tra P e NP e perché è rilevante per la crittografia?  **R:** P ⊆ NP (se risolvi in tempo polinomiale, verifichi anche). Si congettura P ≠ NP. La sicurezza pratica di [[RSA]] e Diffie-Hellman poggia sulla presunta difficoltà (non nota in P) di fattorizzazione e logaritmo discreto: se P=NP crollerebbe.
5. **D:** Perché una complessità esponenziale come O(2ⁿ) è "intrattabile"?  **R:** Perché il numero di operazioni raddoppia a ogni incremento di *n*: già per input moderati il tempo esplode oltre ogni risorsa pratica, a differenza delle polinomiali (nᵏ) considerate efficienti.

## Collegamenti
- Vedi anche: [[Algoritmi di Ordinamento]] (lower bound Ω(n log n)), [[Algoritmi di Ricerca]], [[Programmazione Dinamica]] (pseudo-polinomialità), [[Backtracking]] (esplora spazi esponenziali), [[RSA]] e [[Funzioni di Hash]] (sicurezza = durezza computazionale), [[Algoritmi Crittografici]]

## Fonti
- [Erickson, cap. Asymptotic Analysis / NP-Hardness]
- [ODS, cap. 1.3 The Need for Efficiency, pp. 6-10]
