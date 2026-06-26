---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["MAC e HMAC", "MAC", "HMAC", "Poly1305"]
---

# MAC e HMAC

## Definizione formale

Un **MAC** (Message Authentication Code) è una piccola informazione ("tag") usata per verificare **autenticità e integrità** di un messaggio. L'algoritmo prende un messaggio di lunghezza arbitraria e una **chiave segreta**, e produce il tag. Un algoritmo di verifica prende messaggio, chiave e tag e dice se è valido. [Fonte: Crypto101, cap. 11]

- È il corrispettivo **simmetrico** della firma digitale (asimmetrica → [[RSA]], [[Firma Digitale]]).
- **Sicurezza**: resistere alla **existential forgery** sotto chosen-message attack — l'attaccante, pur ottenendo tag per messaggi a scelta, non deve poter produrre un nuovo `(m, t)` valido.

## Perché serve la chiave segreta

Un **checksum o hash semplice** (CRC32, SHA-256) **non** autentica: chiunque può ricalcolarlo. Un attaccante che modifica un download ricalcola l'hash e nessuno se ne accorge. Solo chi ha la chiave segreta può produrre un MAC valido. [Fonte: Crypto101, cap. 11]

## Composizione MAC + cifratura

Tre modi di combinare MAC e ciphertext:

1. **Encrypt-and-MAC**: `C=E(P)`, `t=MAC(P)` — usato da SSH. *Problema*: tag uguali rivelano plaintext uguali (come ECB).
2. **MAC-then-Encrypt**: `t=MAC(P)`, `C=E(P‖t)` — usato (storicamente) da TLS. Richiede di decifrare prima di verificare.
3. **Encrypt-then-MAC**: `C=E(P)`, `t=MAC(C)` — usato da IPSec. **È l'unica scelta corretta.**

> **The Cryptographic Doom Principle** (Moxie Marlinspike): qualunque sistema che faccia *qualsiasi cosa* prima di verificare il MAC è condannato. [Fonte: Crypto101, cap. 11]

Solo encrypt-then-MAC ha sicurezza dimostrabile: si verifica il tag sul ciphertext *prima* di decifrare, scartando messaggi manipolati (e prevenendo i padding oracle → [[Padding Oracle Attack]]).

## Costruzioni insicure da evitare

- **Prefix-MAC** `t=H(k‖m)`: **insicuro** con hash Merkle–Damgård (MD5, SHA-1, SHA-2) per il **length extension attack** ([[Funzioni di Hash]]). Un attaccante forgia tag per `m‖padding‖m'`. (È invece *sicuro* con SHA-3/BLAKE2.)
- **Suffix-MAC** `t=H(m‖k)` e **sandwich-MAC** `t=H(k‖m‖k)`: meglio di prefix-MAC ma con problemi (suffix-MAC cade con una collisione sull'hash).

## HMAC

**HMAC** (Bellare, Canetti, Krawczyk, 1996) è lo standard per costruire un MAC da una hash crittografica:

```
HMAC(k, m) = H( (k⊕opad) ‖ H( (k⊕ipad) ‖ m ) )
```

con `ipad`=0x36 ripetuto e `opad`=0x5c ripetuto (un block-length ciascuno). [Fonte: Crypto101, cap. 11]

- **Doppio passaggio** nella hash, combinando la chiave prima di ognuno → immune al length extension.
- **Prova di sicurezza forte**: se la hash è una PRF, HMAC è una PRF; la hash **non** deve neppure essere collision-resistant. Per questo **HMAC-MD5** restava sicuro anche con MD5 rotto.
- I valori esatti di ipad/opad non contano, purché diversi.

## One-time MAC e Carter-Wegman

- **One-time MAC**: sicuro solo per *un* messaggio per chiave. Esempio: `t ≡ m·a + b (mod p)` con `a,b` casuali. Estendibile a messaggi multi-blocco con un polinomio (regola di Horner). **Velocissimo** e con prova information-theoretic. Ma **riuso della chiave = catastrofe**: con due tag si recuperano `a` e `b` con semplice algebra modulare (analogo al riuso del one-time pad → [[XOR]]).
- **Carter-Wegman MAC**: trasforma un one-time MAC in un MAC multi-uso sicuro mascherando il tag con una PRF su un nonce: `CW = F(k₁, n) ⊕ O(k₂, M)`. Il messaggio grande passa solo per il MAC veloce; la PRF lenta agisce solo sul nonce piccolo. **Poly1305-AES** è lo stato dell'arte. [Fonte: Crypto101, cap. 11]

## Esempio reale

- **HMAC-SHA256**: integrità in TLS, JWT, API signing (AWS SigV4).
- **Poly1305**: nell'AEAD **ChaCha20-Poly1305** (TLS 1.3, WireGuard). Vedi [[Authenticated Encryption (AEAD)]].
- **GMAC**: la componente di autenticazione di GCM.

## Collegamenti
- [[Authenticated Encryption (AEAD)]] · [[Funzioni di Hash]] · [[Padding Oracle Attack]] · [[Modi Operativi dei Block Cipher]]
- Firma (equivalente asimmetrico): [[RSA]] · [[Firma Digitale]]
- [[00 — Mappa Crittografia|Mappa Crittografia]]

## Fonti
- [Crypto101, cap. 11, "Message authentication codes", pp. 111–124]
