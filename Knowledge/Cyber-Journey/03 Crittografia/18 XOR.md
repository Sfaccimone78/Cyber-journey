---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["XOR", "03. XOR", "XOR e One-Time Pad"]
---

# XOR

## In breve
L'operatore **XOR** ($\oplus$) confronta due bit: restituisce `0` se sono uguali, `1` se sono diversi. In Python si usa `^`. È l'operazione alla base della [[Crittografia Simmetrica|cifratura simmetrica]] più elementare (cifrario XOR) e ricorre in quasi ogni sfida CTF di crittografia.

## Come funziona
```
  l  =  01101100  (ASCII 108)
 13  =  00001101
       ----------
XOR  =  01100001  = 'a'  (ASCII 97)
```

```python
string = "label"
key = 13

result = ""
for char in string:
    result += chr(ord(char) ^ key)
    # ord()  → carattere in intero ASCII
    # ^ key  → XOR con la chiave
    # chr()  → intero in carattere

print(result)
```

## Proprietà XOR
| Proprietà | Formula |
| :-: | :-: |
| **Commutativa** | $A \oplus B = B \oplus A$ |
| **Associativa** | $A \oplus (B \oplus C) = (A \oplus B) \oplus C$ |
| **Identità** | $A \oplus 0 = A$ |
| **Autoinversa** | $A \oplus A = 0$ |

> [!tip] Conseguenza chiave
> Grazie a **Associativa** + **Autoinversa** puoi **annullare** una variabile riapplicando XOR:
> $$A \oplus K \oplus K = A \oplus 0 = A$$
> È il principio del **cifrario XOR**: la stessa chiave cifra e decifra.

## Esempio pratico — XOR multiplo
Recuperare una flag combinata con più chiavi (CryptoHack):
```python
c1 = bytes.fromhex("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313")
r2 = bytes.fromhex("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1")
r3 = bytes.fromhex("04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf")

assert len(c1) == len(r2) == len(r3)   # stessa lunghezza obbligatoria
flag = bytearray()
for i in range(len(c1)):
    flag.append(c1[i] ^ r2[i] ^ r3[i])

print(flag.decode('utf-8'))
```

## Brute-force a 1 byte
Una chiave di 1 byte ha solo **256 valori** (`0x00`–`0xFF`): si provano tutti e si cerca il marcatore noto (`crypto`).
```python
c1 = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")

for key in range(256):
    decoded = "".join(chr(b ^ key) for b in c1)
    if "crypto" in decoded:
        print(f"[+] Chiave trovata: {key} (0x{key:02x})")
        print(f"    Flag: {decoded}")
        break
```

## Repeating-key XOR
Se il testo è cifrato con una chiave che si **ripete ciclicamente** e conosciamo l'inizio del plaintext (es. `crypto{`), facciamo lo XOR tra inizio del ciphertext e plaintext noto per **leakare** i primi byte della chiave. Indovinata la chiave, decifriamo tutto facendola ruotare con l'operatore modulo `%`.

```python
cypher = bytes.fromhex(
    "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526"
    "217f27342e175d0e077e263451150104"
)

# --- Fase 1: leak dei primi byte di chiave ---
known = b"crypto{"
key_leak = bytes(c ^ p for c, p in zip(cypher, known))
print(f"Leak parziale: {key_leak}")          # b'myXORke'

# --- Fase 2: decifratura con chiave intera ---
key = b"myXORkey"
flag = bytes(cypher[i] ^ key[i % len(key)] for i in range(len(cypher)))
print(f"Flag: {flag.decode('utf-8')}")
```

## One-Time Pad — segretezza perfetta (e perché è impraticabile)
Il **one-time pad (OTP)** è il cifrario XOR portato all'estremo: `C = P ⊕ K` con un **pad `K` veramente casuale, lungo quanto il messaggio e usato una sola volta**. Decifratura: `P = C ⊕ K`.

> [!tip] Perfect secrecy (Shannon)
> Se il pad è davvero casuale e mai riusato, l'OTP ha **segretezza perfetta**: vedendo `cᵢ = 1`, l'attaccante non può sapere se `pᵢ` era 0 o 1, perché `kᵢ` è ugualmente probabile. Non apprende **nulla** sul plaintext (tranne la sua lunghezza). È l'unico schema con sicurezza **informazionale-teorica**, non basata su difficoltà computazionale. [Fonte: Crypto101, cap. 5]

**Limiti pratici**: la chiave è grande quanto tutti i dati, va scambiata in anticipo e in modo sicuro, e serve casualità vera. *"Risolve il problema sbagliato"* → in pratica si usano block/stream cipher + key exchange.

### Riuso del pad = catastrofe (multi-time pad)
Riusare la stessa chiave su due messaggi annulla la sicurezza:
```
c₁ ⊕ c₂ = (p₁ ⊕ k) ⊕ (p₂ ⊕ k) = p₁ ⊕ p₂
```
La chiave sparisce e resta lo XOR dei due plaintext, che **fa trapelare moltissima informazione**. Si rompe con il **crib-dragging**: si "trascinano" sequenze probabili (`␣the␣`, `Content-Length:`) lungo i ciphertext; indovinato un pezzo in posizione `i`, si recupera `k = cᵢ ⊕ pᵢ` lì → si decifra *tutti* i messaggi in quella posizione. È **esattamente** ciò che accade con il riuso di nonce in CTR/GCM ([[Modi Operativi dei Block Cipher]], [[Stream Cipher]]) e con il riuso della chiave di un one-time MAC ([[MAC e HMAC]]). Vedi [[Attacchi Crittografici]].

> [!note] "OTP" commerciali
> Prodotti "snake oil" chiamano OTP costrutti dove il pad è generato da uno stream cipher deterministico: diventa sicuro *in pratica* ma **perde** la garanzia "unbreakable" — è uno stream cipher, non un vero one-time pad.

## Collegamenti
- [[Crittografia Simmetrica]] — il cifrario XOR è il caso più elementare di cifratura simmetrica
- [[Stream Cipher]] — un cifrario a flusso è un OTP col pad sostituito da un keystream pseudocasuale
- [[Modi Operativi dei Block Cipher]] — il riuso di nonce in CTR/GCM ripropone il multi-time pad
- [[Attacchi Crittografici]] — crib-dragging e riuso di chiave/nonce
- [[Base64]] — i ciphertext nelle sfide arrivano spesso in Base64 o hex
- [[Bytes e Long]] — manipolare i byte prima/dopo lo XOR
- [[AES]] — lo XOR è alla base delle modalità a blocchi (es. CBC)

## Fonti
- CryptoHack — XOR challenges: https://cryptohack.org/challenges/xor/
- Wikipedia — XOR cipher: https://en.wikipedia.org/wiki/XOR_cipher
- Crypto 101 (Laurens Van Houtven), cap. 5 "Exclusive or" (one-time pad, perfect secrecy, crib-dragging): https://crypto101.io/
