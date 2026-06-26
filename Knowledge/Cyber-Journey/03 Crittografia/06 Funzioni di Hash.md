---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 8
aggiornato: 2026-06-26
stato: maturo
aliases: ["Funzioni di Hash", "Funzioni Hash"]
---

# Funzioni di Hash

## In breve
Una **funzione di hash crittografica** trasforma un input di qualsiasi dimensione in un **digest** di lunghezza fissa, in modo **deterministico** e **a senso unico**: dall'hash non si risale all'input se non per forza bruta. È il mattone di integrità, firme digitali e archiviazione password.

## Le quattro proprietà che la rendono "crittografica"
- **Deterministica** — stesso input → stesso hash, sempre.
- **One-way (preimage resistance)** — dato `h`, è impraticabile trovare `m` con `hash(m)=h`.
- **Second preimage / collision resistance** — impraticabile trovare due input col **medesimo** hash.
- **Effetto valanga** — 1 bit cambiato nell'input → ~50% dei bit dell'hash cambiano.

> Non confondere con [[Encoding vs Encryption]]: l'hash **non** è reversibile (encryption sì) e **non** ha chiave (encoding nemmeno, ma l'encoding è reversibile). L'hash è a perdita d'informazione per costruzione.

## Algoritmi
| Algoritmo | Output | Stato |
|---|---|---|
| MD5 | 128 bit | **Rotto** (collisioni banali) — solo checksum non-sicurezza |
| SHA-1 | 160 bit | **Deprecato** (collisione SHAttered, 2017) |
| SHA-256 / SHA-512 | 256/512 bit | Sicuro, standard attuale |
| SHA-3 (Keccak) | variabile | Sicuro, costruzione diversa (sponge) |
| BLAKE2/3 | variabile | Sicuro e velocissimo |

Internamente processano il messaggio a blocchi con rotazioni di bit, [[XOR]] e addizioni modulari (costruzione Merkle–Damgård in MD5/SHA-2, sponge in SHA-3).

## L'attacco del compleanno (birthday)
La resistenza alle collisioni **non** è 2ⁿ ma **2^(n/2)**: per un hash a 128 bit servono ~2⁶⁴ tentativi per una collisione casuale, non 2¹²⁸. Per questo gli output moderni sono ≥256 bit.

## Hash ≠ hashing delle password
Le funzioni qui sopra sono **veloci** — ottimo per integrità, **pessimo** per le password (un attaccante prova miliardi di hash/s). Le password vogliono funzioni **lente e salate** (bcrypt, scrypt, Argon2): vedi [[Hashing delle Password e Salting]].

## Esempio pratico
```bash
sha256sum documento.pdf            # checksum integrità
openssl dgst -sha256 documento.pdf

# identificare un hash trovato
hashid '5f4dcc3b5aa765d61d8327deb882cf99'   # → MD5 (password "password")
```
```python
import hashlib
hashlib.sha256(b"ciao mondo").hexdigest()    # 64 hex
```

## Rilevanza per la sicurezza
- **Integrità**: pubblicare l'hash di un file accanto al download.
- **Firma digitale**: si firma l'**hash**, non il documento intero ([[Firma Digitale]]).
- **Cracking**: [[Hashcat]] e [[John the Ripper]] non "invertono" l'hash — ne calcolano milioni da wordlist e confrontano. Difesa = salt + funzione lenta.
- **Password leak**: un hash MD5/SHA1 senza salt si cracca in secondi con rainbow table.

---

# Strato esperto

## Costruzione Merkle–Damgård
MD5, SHA-1 e SHA-2 condividono lo stesso scheletro:
1. **Padding**: si appende un bit `1`, poi zeri, infine la **lunghezza del messaggio** in bit (Merkle–Damgård strengthening) per arrivare a un multiplo della dimensione di blocco (512 bit per MD5/SHA-1/SHA-256).
2. **Stato (IV)** iniziale fisso e pubblico.
3. Per ogni blocco: `stato = f(stato, blocco)` dove `f` è la **funzione di compressione** (round con [[XOR]], rotazioni, addizioni modulari).
4. L'**ultimo stato** è il digest.
```
H₀ = IV
Hᵢ = f(Hᵢ₋₁, blocco_i)
digest = Hₙ
```
> [!warning] Difetto strutturale
> Poiché il digest **è** lo stato interno finale, chi conosce `hash(m)` e `len(m)` può **continuare** il calcolo da quello stato → **length extension** (sotto). SHA-3 (sponge) e i costrutti HMAC non hanno questo problema.

### SHA-3 / Keccak (sponge)
Costruzione completamente diversa: una permutazione su uno stato grande, in due fasi (*absorb* / *squeeze*). Non espone lo stato come digest → **immune a length extension**. BLAKE2/3 usano un tree-hash veloce, anch'essi sicuri.

## Modello: le tre resistenze e i loro costi
| Proprietà | Cosa rompe | Costo brute force (hash a n bit) |
|---|---|---|
| Preimage | dato `h`, trova `m` | 2ⁿ |
| Second preimage | dato `m`, trova `m'≠m` con stesso hash | 2ⁿ |
| Collisione | trova **una qualsiasi** coppia | **2^(n/2)** (birthday) |

## Attacchi pratici passo-passo (CTF)

### 1. Collisione MD5 / SHA-1 (quando: due file devono avere lo stesso hash)
MD5 è rotto: si generano due input col **medesimo** MD5 in secondi (`fastcoll`, prefissi scelti con `hashclash`). SHA-1 cadde con **SHAttered** (2017, due PDF diversi, stesso SHA-1) e poi con collisioni a prefisso scelto (**SHA-1 is a Shambles**, 2020). Uso tipico in CTF: bypassare un controllo "carica due file diversi con lo stesso hash". Nel mondo reale una collisione MD5 fu usata per **forgiare un certificato CA** dal malware **Flame** (2012). [Fonte: Crypto101, cap. 10] Vedi [[Attacchi Crittografici]].

### 2. Length extension (quando: MAC fatto come `hash(secret ‖ message)` su MD5/SHA-1/SHA-256)
Conoscendo `hash(secret‖msg)` e `len(secret‖msg)`, **senza conoscere il secret** puoi calcolare `hash(secret‖msg‖padding‖estensione)` per un'estensione scelta → forgi un MAC valido.
```bash
# hashpump / hash_extender
hash_extender -d "user=guest" -s <hash_noto> -a "&admin=true" -l <len_secret> -f sha256
```
Difesa: **HMAC** (`hash(k⊕opad ‖ hash(k⊕ipad‖m))`) o SHA-3, non `hash(secret‖msg)`.

### 3. Birthday attack (quando: serve una collisione, non un preimage)
Per un hash troncato a `n` bit, ~`1.2·2^(n/2)` tentativi danno una collisione con probabilità ~50%. CTF tipico: hash troncato a 32–64 bit "per comodità" → collisione brute-forzabile.
```python
seen = {}
while True:
    x = random_input()
    h = trunc(hash(x), 32)
    if h in seen and seen[h] != x: break   # collisione trovata
    seen[h] = x
```

### 4. Identificazione e cracking
```bash
hashid '<hash>'            # indovina l'algoritmo
hashcat -m 0   hash.txt rockyou.txt   # MD5
hashcat -m 100 hash.txt rockyou.txt   # SHA-1
john --format=raw-sha256 hash.txt
```
[[Hashcat]] e [[John the Ripper]] non invertono nulla: calcolano milioni di hash da wordlist/regole e confrontano.

## Altri usi: Merkle tree e KDF
- **Merkle tree (hash tree)**: ogni nodo è identificato dall'hash del proprio contenuto + l'hash dei figli/genitore. Permette di verificare l'integrità di grandi strutture confrontando solo la radice. È il cuore di **Git**, **Bitcoin/blockchain**, **BitTorrent** e database come **Cassandra**. [Fonte: Crypto101, cap. 10]
- **KDF — alta vs bassa entropia**: per derivare chiavi da un input **ad alta entropia** (es. il segreto di [[Scambio di Chiavi Diffie-Hellman|Diffie-Hellman]]) si usa **HKDF** (basato su HMAC), che è *veloce*. Per le **password** (bassa entropia) serve invece una KDF *deliberatamente lenta* — bcrypt/scrypt/Argon2/PBKDF2 ([[Hashing delle Password e Salting]]). Non confondere i due casi: HKDF su una password resta brute-forzabile. [Fonte: Crypto101, cap. 13]

## Casi limite
- **Troncamento**: usare i primi 64 bit di SHA-256 dimezza la sicurezza alle collisioni a 2³² → fragile.
- **Hash di stringa vuota**: valore costante noto (`d41d8cd9...` per MD5) — utile per riconoscere "nessun input".
- **HMAC con chiave più lunga del blocco**: la chiave viene prima hashata, poi usata — bug comune se non gestito.
- **Salt non è segreto**: serve solo a impedire rainbow table/riuso, può stare in chiaro nel DB.

## Troubleshooting (errori comuni)
1. **MAC fatto come `md5(secret+msg)`** — vulnerabile a length extension. Causa: si è confuso "hash con chiave" con un vero MAC; usa HMAC.
2. **Stesso digest atteso ma valori diversi** — encoding diverso dell'input (UTF-8 vs UTF-16, newline `\r\n` vs `\n`): l'hash è byte-sensibile.
3. **MD5/SHA-1 ancora usati per sicurezza** — ok per checksum non-ostili, **mai** per firme/integrità contro un avversario.
4. **Password hashate con SHA-256 "perché è sicuro"** — sicuro ma **veloce**: serve bcrypt/Argon2 (vedi [[Hashing delle Password e Salting]]).
5. **Confronto di hash con `==` non costante** — può leakare via timing in contesti MAC; usa un confronto a tempo costante (`hmac.compare_digest`).

## Domande da colloquio / CTF
- *Perché una collisione costa 2^(n/2) e non 2ⁿ?* — paradosso del compleanno: il numero di **coppie** cresce quadraticamente, quindi basta ~√(spazio) tentativi.
- *Cos'è il length extension e cosa lo previene?* — sfrutta che il digest Merkle–Damgård è lo stato interno; HMAC e SHA-3 lo impediscono.
- *MD5 è "rotto" — significa che posso invertirlo?* — No: è rotto sulle **collisioni** (e quindi inadatto a firme), ma il preimage resta costoso. Il cracking password sfrutta la velocità + wordlist, non un'inversione.
- *Differenza tra hash e MAC?* — l'hash è senza chiave (chiunque lo ricalcola); il MAC usa una chiave segreta → garantisce **autenticità**, non solo integrità.

## Collegamenti
- [[Hashing delle Password e Salting]] — applicazione critica
- [[MAC e HMAC]] — autenticazione con chiave; HMAC neutralizza il length extension
- [[Attacchi Crittografici]] — collisioni, length extension, birthday
- [[Firma Digitale]]
- [[Encoding vs Encryption]]
- [[XOR]] — operazione interna agli algoritmi
- [[Hashcat]]
- [[John the Ripper]]

## Fonti
- Wikipedia — Cryptographic hash function: https://en.wikipedia.org/wiki/Cryptographic_hash_function
- NIST FIPS 180-4 — Secure Hash Standard: https://csrc.nist.gov/publications/detail/fips/180/4/final
- Cloudflare — Cryptographic hash function: https://www.cloudflare.com/learning/ssl/what-is-a-cryptographic-hash-function/
- CryptoHack — Hashing challenges: https://cryptohack.org/challenges/hashing/
- SHAttered — First SHA-1 collision: https://shattered.io/
- Wikipedia — Length extension attack: https://en.wikipedia.org/wiki/Length_extension_attack
- RFC 2104 — HMAC: https://datatracker.ietf.org/doc/html/rfc2104
- Crypto 101 (Laurens Van Houtven), capp. 10 "Hash functions" e 13 "Key derivation functions": https://crypto101.io/
