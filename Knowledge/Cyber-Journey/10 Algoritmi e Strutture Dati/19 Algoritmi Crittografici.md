---
tipo: concetto
tag: [algoritmi, crypto]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Algoritmi Crittografici"]
---

# Algoritmi crittografici (ponte algoritmi ↔ crittografia)

## Definizione
Pagina-ponte che inquadra i primitivi crittografici come **algoritmi**: ne mostra meccanica computazionale, costo e il fondamento di sicurezza (la **durezza computazionale** — vedi [[Complessità Computazionale]]). Per la trattazione crittografica completa rimanda a [[RSA]], [[AES]], [[Funzioni di Hash]]. [Fonte: Crypto101; Erickson, cap. Number-Theoretic Algorithms]

## RSA — generazione delle chiavi (key gen)
Algoritmo basato sulla teoria dei numeri; sicurezza = **presunta intrattabilità della fattorizzazione** di n. [Fonte: Crypto101, cap. RSA]
```
1. genera due primi grandi p, q (test di primalità Miller-Rabin, probabilistico)
2. n = p·q                         # modulo pubblico
3. φ(n) = (p-1)(q-1)               # toziente di Eulero
4. scegli e con gcd(e, φ(n)) = 1   # esponente pubblico (spesso 65537)
5. d = e⁻¹ mod φ(n)                # inverso → Euclide esteso
→ chiave pubblica (e, n), chiave privata (d, n)
```
Algoritmi numerici sottostanti e costo:
- **Esponenziazione modulare** (cifratura `c = mᵉ mod n`): **square-and-multiply**, O(log e) moltiplicazioni — un [[Divide et Impera]] sull'esponente.
- **GCD / inverso modulare**: **algoritmo di Euclide (esteso)**, O(log n).
- **Test di primalità**: **Miller-Rabin** randomizzato, O(k·log³n).
- La **rottura** richiede di fattorizzare n: nessun algoritmo classico polinomiale noto (sub-esponenziale: GNFS) → vedi [[Complessità Computazionale]] (P vs NP) e Shor su computer quantistici.

## AES — internals
**Cifrario a blocchi** (128 bit), rete di **sostituzione-permutazione** su 10/12/14 round (chiavi 128/192/256). [Fonte: Crypto101, cap. Block ciphers] Ogni round applica:
1. **SubBytes** — sostituzione non lineare via **S-box** (basata sull'inverso in GF(2⁸)); confusione.
2. **ShiftRows** — permutazione: shift ciclico delle righe dello stato.
3. **MixColumns** — diffusione: moltiplicazione di colonne in GF(2⁸).
4. **AddRoundKey** — XOR con la sottochiave del round (**key schedule** espande la chiave).
È un algoritmo a **tempo costante** per progetto (gli AES-NI hardware evitano lookup data-dependent) per resistere agli attacchi di tipo **timing/cache**.

## Hash — costruzione
Una **funzione hash** comprime input arbitrario in un digest fisso, processandolo a blocchi. [Fonte: Crypto101, cap. Hash functions]
- **Merkle-Damgård** (MD5, SHA-1, SHA-2): itera una **funzione di compressione** blocco dopo blocco, con padding finale; stato → digest.
- **Sponge** (SHA-3/Keccak): assorbe i blocchi in uno stato grande (absorb) poi ne "spreme" l'output (squeeze).
- Costo: **O(L)** lineare nella lunghezza del messaggio.
- Sicurezza = **resistenza a preimmagine e collisioni**: trovare una collisione costa ~2^(b/2) per il **paradosso del compleanno** (probabilità/[[Complessità Computazionale]]) → motivo per cui SHA-256 usa digest a 256 bit.

## Complessità (riepilogo)
| Primitiva / operazione | Costo |
|------------------------|-------|
| Esponenziazione modulare (RSA) | O(log e) moltiplicazioni |
| Euclide esteso (inverso/GCD) | O(log n) |
| Miller-Rabin (primalità) | O(k·log³n) |
| AES cifratura blocco | O(1) per blocco (round fissi), O(L) sul messaggio |
| Hash (SHA-2/3) | O(L) |
| Attacco collisione (birthday) | ~O(2^(b/2)) |

## Esempio
TLS in una connessione HTTPS combina i tre: **RSA**/ECDHE per lo scambio chiavi (numerico), **AES** per cifrare il flusso (SP-network), **SHA-256** per integrità/HMAC. Ognuno è un algoritmo la cui sicurezza dipende da un problema computazionalmente duro.

## Collegamenti
- Vedi anche: [[RSA]], [[AES]], [[Funzioni di Hash]] (trattazione crittografica), [[Complessità Computazionale]] (durezza = sicurezza, P vs NP), [[Divide et Impera]] (square-and-multiply)

## Fonti
- [Crypto101, capp. RSA / Block ciphers / Hash functions]
- [Erickson, cap. Number-Theoretic Algorithms / Randomized Algorithms]