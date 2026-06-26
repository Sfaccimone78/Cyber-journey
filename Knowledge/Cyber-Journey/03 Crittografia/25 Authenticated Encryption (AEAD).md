---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Authenticated Encryption (AEAD)", "AEAD", "Authenticated Encryption", "GCM"]
---

# Authenticated Encryption (AEAD)

## Definizione formale

L'**authenticated encryption** fornisce contemporaneamente **riservatezza** (privacy) e **integrità/autenticità** in un'unica primitiva. **AEAD** (Authenticated Encryption with Associated Data) è la variante che autentica anche **metadati in chiaro** ("associated data") insieme al contenuto cifrato. [Fonte: Crypto101, cap. 11]

## Intuizione

Molti messaggi hanno due parti:
- **Contenuto**: da cifrare *e* autenticare.
- **Metadati**: spesso devono restare in chiaro (es. il destinatario di un'email, che i server di routing devono leggere) ma vanno comunque **autenticati**, così un attaccante non può alterarli mantenendo il messaggio valido.

Un AEAD lega crittograficamente l'intero `(ciphertext + associated data)` in un unico tag. Togliendo la scelta su *come* comporre cifratura e MAC all'application developer, gli si impedisce di fare la scelta sbagliata (vedi Doom Principle in [[MAC e HMAC]]).

> Motivazione: *unauthenticated encryption is virtually never what you want.* Gli attacchi padding oracle e bit-flipping mostrano che senza autenticazione un attaccante attivo può modificare — e talvolta decifrare — i messaggi. [Fonte: Crypto101, cap. 9, 11]

## OCB mode

Uno dei primi modi AEAD. Strutturalmente simile a ECB ma sicuro grazie agli **offset `Δᵢ`** unici per blocco.
- **Veloce**: ~1 operazione di block cipher per blocco + 1 per il tag finale; parallelizzabile.
- Tag costruito da un **checksum** `X` (XOR di tutti i blocchi di plaintext) + tag separato `tₐ` per gli associated data.
- Padding integrato (nessun blocco sprecato).
- **Poco usato** perché **coperto da brevetto** (anche se con licenze gratuite per open source). [Fonte: Crypto101, cap. 11]

## GCM mode (Galois/Counter Mode)

Il modo AEAD **più diffuso**. RFC NIST. Combina:
- **CTR mode** per la cifratura (vedi [[Modi Operativi dei Block Cipher]]),
- un **MAC Carter-Wegman** su campo di Galois per l'autenticazione (la sola parte MAC = **GMAC**).

[Fonte: Crypto101, cap. 11]

> ⚠️ **Nonce reuse in GCM è catastrofico**: ripete il keystream CTR (multi-time pad) *e* permette il recupero della chiave di autenticazione GMAC. Il nonce deve essere unico per ogni cifratura sotto la stessa chiave.

## AEAD moderni (oltre Crypto101)

- **AES-GCM**: standard de facto in TLS 1.2/1.3, IPSec, con accelerazione hardware (AES-NI + PCLMULQDQ).
- **ChaCha20-Poly1305**: AEAD basato sullo stream cipher ChaCha20 ([[Stream Cipher]]) + MAC Poly1305 ([[MAC e HMAC]]). Preferito dove manca l'accelerazione AES (mobile), in TLS 1.3, OpenSSH, WireGuard.
- **AES-GCM-SIV** / **XChaCha20-Poly1305**: varianti "nonce-misuse resistant" o con nonce esteso (192 bit) che mitigano il rischio di riuso del nonce.

## Vulnerabilità note

- **Nonce reuse** (vedi sopra) — il principale piede di porto degli AEAD.
- Tag **troncati** troppo corti riducono la sicurezza di autenticazione.
- AEAD usati correttamente eliminano padding oracle, bit-flipping e manipolazione attiva: rifiutano qualunque ciphertext alterato *prima* di decifrare.

## Esempio reale

In **TLS 1.3** sono ammessi **solo** cipher suite AEAD (AES-GCM, AES-CCM, ChaCha20-Poly1305): i vecchi schemi MAC-then-Encrypt con CBC (vulnerabili a Lucky13/padding oracle) sono stati rimossi. Vedi [[TLS e SSL]].

## Collegamenti
- [[MAC e HMAC]] · [[Modi Operativi dei Block Cipher]] · [[Stream Cipher]] · [[Padding Oracle Attack]] · [[TLS e SSL]]
- [[00 — Mappa Crittografia|Mappa Crittografia]]

## Fonti
- [Crypto101, cap. 11, "Authenticated encryption modes" (AEAD/OCB/GCM), pp. 124–129]
