---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Trie"]
---

# Trie (albero di prefissi)

## Definizione
Un **trie** (o **albero di prefissi**, da re*trie*val) è una struttura dati ad albero per memorizzare un insieme di **stringhe**, dove ogni nodo rappresenta un **prefisso** comune e ogni arco è etichettato con un carattere. La chiave non è memorizzata in un singolo nodo: è data dal **cammino** dalla radice al nodo. Tutte le stringhe che condividono un prefisso condividono il cammino iniziale. [Fonte: Erickson, cap. Backtracking / String Algorithms]

## Meccanismo
- La **radice** rappresenta la stringa vuota. Un nodo a profondità *d* rappresenta un prefisso di lunghezza *d*.
- Ogni nodo ha fino a **σ figli** (σ = dimensione dell'alfabeto: 26 per lettere, 256 per byte). I figli sono indicizzati per carattere (array di σ puntatori, o mappa hash per alfabeti grandi/sparsi).
- Un flag booleano `isEndOfWord` marca i nodi che terminano una parola effettivamente inserita (distinguendo "ca" prefisso da "ca" parola).

```
search(word):
    node = root
    for c in word:
        if node.child[c] == null: return false
        node = node.child[c]
    return node.isEndOfWord

insert(word):
    node = root
    for c in word:
        if node.child[c] == null: node.child[c] = new Node()
        node = node.child[c]
    node.isEndOfWord = true

startsWith(prefix):           # ricerca per prefisso — il punto di forza
    node = root
    for c in prefix:
        if node.child[c] == null: return false
        node = node.child[c]
    return true                # esiste almeno una parola con questo prefisso
```

## Complessità
Con *L* = lunghezza della stringa, σ = dimensione alfabeto, *n* = numero di chiavi:

| Operazione | Tempo | Note |
|------------|-------|------|
| search / insert / delete | **O(L)** | indipendente da *n*: dipende solo dalla lunghezza della chiave |
| startsWith (prefisso) | O(L) | best/avg/worst tutti O(L) |
| spazio | O(n · L · σ) peggiore | con array di figli; ridotto con mappe o **compressed trie** (Patricia/radix tree) |

> Vantaggio chiave: a differenza di una [[Hash Table]] (O(L) per hashing + niente ordine), il trie supporta **autocompletamento** e ricerca per prefisso, ed è **ordinato** (visita DFS in ordine lessicografico). Svantaggio: consumo di memoria. Il **radix tree** comprime catene di nodi a figlio unico per mitigarlo.

## Esempio
Autocompletamento di una barra di ricerca, controllo ortografico, instradamento IP **longest-prefix match** (tabelle di routing usano radix trie), filtri di parole, indici di stringhe (suffix tree). Inserendo `cat`, `car`, `card`: la radice → `c` → `a` si dirama in `t` (fine) e `r` (fine), e da `r` prosegue in `d` (fine).

## Collegamenti
- Vedi anche: [[Hash Table]] (alternativa per lookup esatto, ma senza prefissi/ordine), [[Alberi Binari e BST]] (anch'esso ad albero, ma chiave per-nodo e confronto binario), [[Backtracking]] (la visita di un trie è un DFS strutturato)

## Fonti
- [Erickson, cap. String Algorithms / Backtracking]
- [ODS, cap. 13 BinaryTrie / XFastTrie / YFastTrie, pp. 253-270]