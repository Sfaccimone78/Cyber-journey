---
tipo: concetto
tag: [algoritmi]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Hash Table"]
---

# Hash Table (chaining vs open addressing)

## Definizione
Struttura che realizza l'interfaccia **USet** (insieme non ordinato: `add`, `remove`, `find`) in tempo **O(1) atteso**, mappando ogni chiave a un indice di un array tramite una **funzione hash** `h(x)`. Il problema centrale è gestire le **collisioni** (chiavi diverse, stesso indice). [Fonte: ODS, cap. 5]

## Meccanismo
Due strategie principali:

### Chaining (concatenazione) — ChainedHashTable
Ogni cella dell'array è una lista che contiene tutti gli elementi con quell'hash. `find(x)` scandisce la lista nella cella `h(x)`. Con n elementi e t celle, la lunghezza attesa di una lista è il **load factor** α = n/t; mantenendo α = O(1) (ridimensionando), le operazioni costano O(1) atteso. [Fonte: ODS, sez. 5.1]

### Open addressing (indirizzamento aperto) — LinearHashTable
Tutti gli elementi stanno nell'array stesso; in caso di collisione si **sonda** (probing) la cella successiva finché se ne trova una libera. ODS usa il **linear probing**: scansione `h(x), h(x)+1, ...` modulo la capacità. Richiede load factor basso (es. α ≤ 1/2) per restare efficiente; usa marcatori `del` per le cancellazioni. [Fonte: ODS, sez. 5.2]

### Hash codes
Per oggetti compositi/stringhe servono buoni hash code (es. hashing polinomiale). ODS analizza **multiplicative hashing** e **tabulation hashing**. [Fonte: ODS, sez. 5.3]

## Complessità
| Strategia | find/add/remove (atteso) | peggiore | spazio |
|-----------|--------------------------|----------|--------|
| Chaining | O(1) | O(n) (tutte collidono) | n + t |
| Open addressing (linear probing) | O(1) con α basso | O(n) | array di capacità ≥ 2n |

> Chaining tollera load factor alti e cancellazioni facili; open addressing ha migliore località di cache e nessun overhead di puntatori, ma degrada col clustering e richiede gestione attenta delle cancellazioni.

## Esempio
Dizionario/mappa di un linguaggio (Python `dict`), cache, deduplicazione, indici di database in memoria, tabella dei simboli di un compilatore.

## Collegamenti
- Vedi anche: [[Trie]] (alternativa ordinata su chiavi-interi/stringhe), [[Alberi Binari e BST]] (SSet ordinato vs USet non ordinato)
- Ponte crittografia: le funzioni hash crittografiche [[Funzioni di Hash]] hanno requisiti diversi (resistenza a collisioni/preimmagine), ma condividono l'idea di mappare input a un dominio fisso.
- Ponte sicurezza: i **collision attack** e gli **hash-flooding (algorithmic complexity attack)** sfruttano hash deboli per degradare una hash table a O(n).

## Fonti
- [ODS, cap. 5 Hash Tables, pp. 101-122]