---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Stream Cipher", "ChaCha20", "RC4", "Salsa20"]
---

# Stream Cipher (RC4, Salsa20, ChaCha20)

## Definizione formale

Uno **stream cipher** è un algoritmo simmetrico che cifra un flusso (stream) di bit di lunghezza arbitraria. Il tipo più comune è il **synchronous stream cipher**: da una chiave segreta produce un lungo **keystream** pseudocasuale, poi `C = P ⊕ keystream`. La decifratura è identica: `P = C ⊕ keystream`. [Fonte: Crypto101, cap. 7]

## Intuizione

È un **one-time pad** (vedi [[XOR]]) in cui il pad veramente casuale è sostituito da un keystream **pseudocasuale** derivato da una chiave corta. È ideale se l'unico attacco possibile è il brute-force della chiave; qualunque **bias** nell'output è un difetto. Due famiglie:
- **Native stream cipher** (RC4, Salsa20, ChaCha): progettati da zero come stream cipher.
- **Block cipher in un mode of operation** (CTR mode): produce un keystream da un block cipher. Vedi [[Modi Operativi dei Block Cipher]].

## RC4

Per anni lo stream cipher nativo più diffuso. Semplicissimo e veloce (~13.9 cicli/byte). Stato: array `S` di 256 byte (permutazione) + due indici `i, j`. Due fasi: **key scheduling** (mescola la chiave nello stato) e **pseudorandom generator** (produce i byte del keystream swappando elementi di `S`).

> **RC4 è rotto. Non usarlo.** [Fonte: Crypto101, cap. 7]

Vulnerabilità accumulate negli anni:
- I primi 3 byte della chiave correlati col primo byte del keystream (Roos).
- Il 2° byte del keystream è 2× più probabile che sia zero (Mantin-Shamir); forti bias nei primi byte (Fluhrer-Mantin-Shamir, FMS).
- **WEP** (Wi-Fi) fu devastato perché concatenava `k‖nonce` ingenuamente → recupero della chiave a lungo termine. TLS non era affetto perché combinava chiave e nonce in modo sicuro.
- Klein (2008): bastano decine di migliaia di messaggi. 2013 (Royal Holloway): single-byte bias nei primi 256 byte + double-byte bias ovunque → la goccia finale che ha imposto l'abbandono di RC4.

## Salsa20 e ChaCha20

Stream cipher moderni di **Dan Bernstein**, allo stato dell'arte. Varianti per numero di round: Salsa20/12, Salsa20/8; ChaCha8/12/20.

> Nessun attacco pratico noto contro Salsa20, ChaCha o le loro varianti raccomandate. [Fonte: Crypto101, cap. 7]

Proprietà notevoli:
- **Veloci**: Salsa20 full ~4 cicli/byte, /8 ~2 cicli/byte; ChaCha leggermente più veloce. Competitivo con AES anche senza hardware dedicato.
- **Seek nel keystream**: si può "saltare" a un punto qualsiasi senza calcolare i precedenti (come CTR mode) → letture random e parallelismo.
- **Constant-time**: design **ARX** (Add-Rotate-XOR). Nessun accesso a memoria segreto-dipendente (a differenza delle S-box di AES) → resistente a molti side-channel. Operazione core: `x ← x ⊕ (y ⊞ z) ≪ n` (addizione modulare, XOR, rotazione).
- Usano **nonce** per derivare keystream diversi dalla stessa chiave a lungo termine (RC4 non lo fa nativamente).

## Vulnerabilità note (comuni agli stream cipher)

- **Riuso di chiave/nonce** = attacco multi-time pad (vedi [[XOR]]). Per CTR mode il riuso del nonce ripete l'intero keystream.
- **Bit-flipping attack**: flippando un bit del ciphertext si flippa lo *stesso* bit del plaintext (più semplice che in CBC: colpisce solo quel bit, non scrambla il blocco). Dimostra ancora: *encryption is not authentication* → serve un MAC. Vedi [[MAC e HMAC]].

## Esempio reale

**ChaCha20-Poly1305** è l'AEAD preferito in TLS 1.3, OpenSSH, WireGuard, e su mobile dove manca l'accelerazione AES hardware. Vedi [[Authenticated Encryption (AEAD)]], [[TLS e SSL]].

## Collegamenti
- [[XOR]] · [[Modi Operativi dei Block Cipher]] · [[AES]] · [[Authenticated Encryption (AEAD)]]
- [[00 — Mappa Crittografia|Mappa Crittografia]]

## Fonti
- [Crypto101, cap. 7, "Stream ciphers", pp. 41–80]
- Menezes, van Oorschot, Vanstone — *Handbook of Applied Cryptography*, cap. 6 "Stream Ciphers" (PDF libero): https://cacr.uwaterloo.ca/hac/
