---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Modi Operativi dei Block Cipher", "Modi Operativi", "ECB", "CBC", "CTR"]
---

# Modi Operativi dei Block Cipher (ECB/CBC/CTR/GCM)

## Definizione

Un **mode of operation** è una configurazione che permette a un block cipher (che cifra un solo blocco, vedi [[AES]]) di cifrare stream/messaggi di lunghezza arbitraria. Il sistema composto si comporta come uno stream cipher; il modo è indipendente dallo specifico cifrario. [Fonte: Crypto101, cap. 7]

## ECB — Electronic Code Book

Il modo più semplice (e **insicuro**): si divide il messaggio in blocchi e si cifra ciascuno indipendentemente.

> Difetto fatale: blocchi di plaintext identici → blocchi di ciphertext identici. [Fonte: Crypto101, cap. 7]

- **Image leak**: cifrando un'immagine bitmap in ECB, la **macrostruttura resta visibile** (il famoso "pinguino Tux" cifrato). Anche con block size enormi e irrealistici il problema persiste.
- **Encryption oracle attack**: se un oracolo cifra `A‖S` con `A` controllato dall'attaccante e `S` segreto, l'attaccante recupera `S` byte per byte in `256·b` tentativi (allineando un byte incognito alla volta al confine del blocco), invece di `256^b`. **Mai usare ECB.**

## CBC — Cipher Block Chaining

Ogni blocco di plaintext è XORato col **blocco di ciphertext precedente** prima di essere cifrato. Per il primo blocco si usa un **IV** (initialization vector).

- L'**IV deve essere imprevedibile** (idealmente casuale) ma **non segreto** (si invia in chiaro col ciphertext).
- Non intrinsecamente insicuro come ECB, ma fragile:
  - **IV prevedibili** → attacco a confronto: Mallory costruisce `P_M = IV_M ⊕ IV_A ⊕ G` per testare se il record di Alice è `G`. (BEAST in TLS 1.0 usava il ciphertext precedente come IV → prevedibile.)
  - **Chiave usata come IV** → un chosen-ciphertext attack recupera la chiave modificando un solo messaggio.
  - **Bit-flipping**: flippando bit nel ciphertext del blocco `i`, si flippano gli stessi bit nel plaintext del blocco `i+1` (mentre il blocco `i` diventa spazzatura). Permette di iniettare `;admin=1;` in un cookie.
  - **Padding oracle** (vedi [[Padding Oracle Attack]]): decifra l'intero messaggio sfruttando il leak "padding valido/non valido".
- Richiede **padding** (vedi sotto).

## CTR — Counter Mode

Concatena un **nonce** con un **contatore** (incrementato per blocco, zero-padded a block size), cifra il risultato col block cipher e usa l'output come keystream: `Cᵢ = Pᵢ ⊕ E(k, N‖i)`. È un **synchronous stream cipher** prodotto da un block cipher.

- Cifratura = decifratura (entrambe producono keystream e XORano).
- A differenza dell'IV di CBC, il **nonce di CTR può essere prevedibile** (senza la chiave l'output del cifrario è imprevedibile), ma **non deve mai essere riusato** (riuso → keystream ripetuto → multi-time pad).
- Parallelizzabile e con seek nel keystream.

## Padding (per CBC/ECB)

I messaggi devono essere multipli del block size. Lo schema più comune è **PKCS#5/PKCS#7**: si riempie con `N` byte di valore `N`. Se il plaintext è già multiplo, si aggiunge un blocco intero di padding. Padding errato → il destinatario rifiuta il messaggio (questo "leak" abilita il padding oracle). [Fonte: Crypto101, cap. 7]

## GCM — Galois/Counter Mode (AEAD)

**GCM** è un modo **autenticato** (AEAD): combina CTR mode con un **MAC Carter-Wegman** su campo di Galois. Fornisce cifratura + autenticazione + dati associati in chiaro autenticati. Il solo MAC si chiama **GMAC**. È il modo AEAD più diffuso (TLS, IPSec). Dettagli in [[Authenticated Encryption (AEAD)]]. [Fonte: Crypto101, cap. 11]

## Vulnerabilità note — riepilogo

| Modo | Problema principale |
|------|---------------------|
| ECB | Pattern leak, encryption oracle → **mai usare** |
| CBC | IV prevedibili, key-as-IV, bit-flipping, **padding oracle** |
| CTR | Riuso nonce = catastrofe (multi-time pad) |
| GCM | Riuso nonce rompe l'autenticazione; corretto se nonce unici |

Tutti i modi **non autenticati** (ECB/CBC/CTR puri) sono vulnerabili a manipolazione attiva: *encryption is not authentication*. Preferire sempre AEAD (GCM, ChaCha20-Poly1305).

## Collegamenti
- [[AES]] · [[Stream Cipher]] · [[Padding Oracle Attack]] · [[Authenticated Encryption (AEAD)]] · [[MAC e HMAC]]
- [[00 — Mappa Crittografia|Mappa Crittografia]]

## Fonti
- [Crypto101, cap. 7, "Stream ciphers" (ECB/CBC/CTR/padding), pp. 41–80]
- [Crypto101, cap. 11, "GCM mode", pp. 128–129]
