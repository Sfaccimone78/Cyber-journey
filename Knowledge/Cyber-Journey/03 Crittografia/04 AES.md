---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 7
aggiornato: 2026-06-26
stato: maturo
aliases: ["AES", "Block Cipher e AES"]
---

# AES

## In breve

**AES** (Advanced Encryption Standard) è il principale algoritmo di [[Crittografia Simmetrica]] usato oggi in tutto il mondo. Adottato dal NIST nel 2001, cifra i dati a blocchi di 128 bit usando chiavi da 128, 192 o 256 bit. È usato in HTTPS, Wi-Fi (WPA2), file ZIP protetti, dischi cifrati e molto altro.

## Cos'è un block cipher (intuizione)

Un **cifrario a blocchi** è, formalmente, una **permutazione con chiave** (keyed permutation): mappa in modo biiettivo ogni possibile blocco su un altro blocco (la biiezione è necessaria per poter decifrare), e la chiave sceglie *quale* delle tantissime permutazioni usare. Con blocco di `n` bit esistono `(2ⁿ)!` permutazioni; una chiave di 128–256 bit ne seleziona "solo" `2¹²⁸–2²⁵⁶` — una frazione minuscola, ma troppo grande per il brute-force. Per un cifrario ideale, conoscere coppie (input, output) non dà alcuna informazione sulle altre: l'unico attacco è provare tutte le chiavi. [Fonte: Crypto101, cap. 6]

> AES nacque come **Rijndael** (dai crittografi belgi **Vincent Rijmen** e **Joan Daemen**) e fu scelto dal NIST tramite una **competizione pubblica e peer-reviewed** — il modello considerato preferibile per standardizzare la crittografia. [Fonte: Crypto101, cap. 6]

## Come funziona

AES è un **cifrario a blocchi**: prende 128 bit di plaintext e li trasforma in 128 bit di ciphertext usando una chiave. Il processo si chiama **round** e viene ripetuto più volte (10 round per AES-128, 14 per AES-256).

Ogni round applica quattro operazioni sulla **State Matrix** (una griglia 4x4 di byte):

1. **SubBytes** — sostituisce ogni byte con un valore da una tabella S-Box (aggiunge confusione).
2. **ShiftRows** — sposta le righe della matrice ciclicamente.
3. **MixColumns** — mescola le colonne con operazioni su campo finito.
4. **AddRoundKey** — fa [[03. XOR]] tra la matrice e la sottochiave del round.

**Modalità operative** (come gestire dati più grandi di 128 bit):
| Modalità | Note |
|----------|------|
| ECB | Insicura: blocchi identici producono ciphertext identici |
| CBC | Sicura se l'IV è random; standard per molte app |
| CTR | Trasforma AES in cifrario a flusso; parallelizzabile |
| GCM | Aggiunge autenticazione (AEAD); raccomandata oggi |

## Esempio pratico

```bash
# Cifrare con AES-256-GCM (modalità raccomandata) via OpenSSL
openssl enc -aes-256-gcm -salt -pbkdf2 \
  -in file.txt -out file.enc \
  -pass pass:"password_segreta"

# Decifrare
openssl enc -d -aes-256-gcm -pbkdf2 \
  -in file.enc -out file.txt \
  -pass pass:"password_segreta"
```

## Rilevanza per la sicurezza

- AES-128 e AES-256 non sono stati violati con attacchi pratici — la sicurezza dipende dalla **forza della chiave/password**.
- La modalità ECB è pericolosa: cifra ogni blocco indipendentemente, rivelando pattern nel plaintext (la famosa immagine del pinguino cifrata in ECB).
- Attacchi reali puntano alla debolezza della password, non all'algoritmo — usa [[Hashing delle Password e Salting]] per proteggere le chiavi derivate da password.
- [[Hashcat]] può attaccare file cifrati AES se la password è debole.

---

# Strato esperto

## Struttura interna nel dettaglio

### La S-box e il campo finito GF(2⁸)
AES vive nel **campo finito** GF(2⁸): ogni byte è un polinomio di grado <8 sul bit. La **S-box** (SubBytes) è la composizione di due passi:
1. **Inverso moltiplicativo** del byte in GF(2⁸) (con `00 → 00`) — non-linearità.
2. Una **trasformazione affine** sui bit — distrugge la struttura algebrica e rimuove i punti fissi.
È l'unico passo non-lineare: senza S-box, AES sarebbe interamente lineare e banale da rompere.

### MixColumns
Ogni colonna (4 byte) è moltiplicata per una matrice fissa in GF(2⁸) (coefficienti `02,03,01,01`). Garantisce **diffusione**: cambiare 1 byte d'input cambia tutti e 4 i byte d'output della colonna. Salta nell'ultimo round (per simmetria cifra/decifra).

### Key schedule
La chiave si espande in `Nr+1` round key (44 word per AES-128) tramite `RotWord`, `SubWord` (riusa la S-box) e costanti `Rcon`. Round key deboli/correlate furono alla base degli attacchi related-key teorici su AES-192/256 (Biryukov–Khovratovich, 2009) — irrilevanti in pratica perché richiedono chiavi scelte in relazione nota.

### Round, in sintesi
| Versione | Chiave | Round (Nr) |
|---|---|---|
| AES-128 | 128 bit | 10 |
| AES-192 | 192 bit | 12 |
| AES-256 | 256 bit | 14 |
Il primo `AddRoundKey` precede il round 1; l'ultimo round omette `MixColumns`.

## Predecessori: DES e 3DES
Prima di AES lo standard era **DES** (1977), oggi **insicuro**: la chiave è di soli **56 bit** (l'input è 64 bit ma 8 sono di parità), brute-forzabile in meno di un giorno su hardware moderno. **Da non usare in nuovi sistemi.**

**3DES** lo estende cifrando tre volte: `C = E(k₁, D(k₂, E(k₃, P)))` (lo schema encrypt-decrypt-encrypt dà retrocompatibilità con DES quando `k₁=k₂=k₃`). Ha chiavi da 168 bit ma **sicurezza effettiva solo ~112 bit**, ed è **lento** (fino a ~134 cicli/byte, un ordine di grandezza più di AES, ~12.6 cicli/byte). Scelta scadente per nuovi sistemi, ma ancora presente nel settore finanziario. [Fonte: Crypto101, cap. 6]

## Modi operativi — quando ogni modo è sicuro
| Modo | Tipo | IV/Nonce | Parallelo | Autenticato | Sicuro se… |
|---|---|---|---|---|---|
| ECB | block | nessuno | sì | no | **mai** (rivela pattern) |
| CBC | block | IV random/imprevedibile | solo decifra | no | IV random + MAC esterno + no padding oracle |
| CTR | stream | nonce **unico** | sì | no | nonce mai riusato con la stessa chiave |
| GCM | stream+MAC | nonce **unico** (96 bit) | sì | **sì** (AEAD) | nonce mai riusato; tag verificato |

> [!tip] Regola pratica
> Se devi scegliere oggi: **AES-256-GCM** (o ChaCha20-Poly1305). CBC e CTR da soli non autenticano → un attaccante può manomettere il ciphertext. "Encrypt-then-MAC" o, meglio, un AEAD.

## Attacchi pratici passo-passo (CTF)

### 1. ECB pattern / detection (quando: blocchi ripetuti nel ciphertext)
ECB cifra ogni blocco di 16 byte indipendentemente → **blocchi di plaintext identici producono blocchi di ciphertext identici**. Rilevamento: spezza il ciphertext in chunk da 16 byte e cerca duplicati.
```python
blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
is_ecb = len(blocks) != len(set(blocks))   # duplicati ⇒ probabile ECB
```
**ECB byte-at-a-time (oracle)**: se controlli un prefisso che viene cifrato + un segreto sconosciuto, allinei il segreto sui confini di blocco e lo recuperi un byte alla volta (CryptoHack/Cryptopals classico).

### 2. CBC bit-flipping (quando: hai accesso al ciphertext e l'IV/blocco precedente)
In CBC `Pᵢ = Dec(Cᵢ) ⊕ Cᵢ₋₁`. Modificando un byte di `Cᵢ₋₁` (o dell'IV per il primo blocco) flippi **lo stesso byte** di `Pᵢ` — a costo di rendere spazzatura `Pᵢ₋₁`. Classico per trasformare `;admin=false` → `;admin=true ` senza conoscere la chiave.
```python
# voglio P[i][j] = target: nuovo C_prev[j] = C_prev[j] ⊕ P_attuale[j] ⊕ target
```

### 3. Padding oracle (quando: il server distingue "padding valido" da "padding non valido")
Con PKCS#7 + CBC, se il server rivela se il padding decifrato è valido, recuperi `Dec(Cᵢ)` byte per byte manipolando `Cᵢ₋₁` finché l'ultimo byte di plaintext è `0x01`, poi `0x02 0x02`, ecc. Da lì `Pᵢ = Dec(Cᵢ) ⊕ Cᵢ₋₁`. Decifra **e** cifra plaintext arbitrari senza la chiave. Tool: `padbuster`, script Cryptopals #17.

### 4. IV / nonce reuse
- **CTR/GCM con nonce riusato**: due ciphertext sotto lo stesso (chiave, nonce) → `C₁ ⊕ C₂ = P₁ ⊕ P₂` (vedi [[XOR]]), si attacca come un many-time pad.
- **GCM nonce reuse** è peggio: oltre a esporre i plaintext, permette di **recuperare la chiave di autenticazione H** e quindi **forgiare tag** validi (attacco "forbidden", Joux). Per questo GCM esige nonce univoci (o random a 96 bit con limite di messaggi).
- **CBC con IV prevedibile** (es. IV = ultimo blocco precedente, come in TLS 1.0) → abilita **BEAST**.

## Casi limite
- **Plaintext multiplo esatto di 16 byte** con PKCS#7 → si aggiunge un **blocco intero** di padding `10 10 ... 10`, altrimenti la rimozione è ambigua.
- **AES-NI**: le CPU moderne hanno istruzioni hardware → AES è velocissimo e (importante) **costante nel tempo**, mentre le S-box software via lookup-table possono leakare via cache-timing.
- **GCM oltre ~2³² blocchi** con la stessa chiave → degrado di sicurezza; ruotare la chiave.

## Troubleshooting (errori comuni)
1. **"Padding is incorrect" in decifra** — chiave/IV sbagliati, oppure modo diverso da quello di cifratura. Non sempre è il padding: spesso è la chiave.
2. **IV riusato per "comodità"** (IV fisso/zero in CBC o CTR) — distrugge la segretezza semantica; usa IV random e trasmettilo in chiaro col ciphertext.
3. **GCM senza verificare il tag** — decifrare e usare il plaintext prima di controllare il tag annulla l'autenticazione (e riapre il padding-oracle equivalente).
4. **Nonce GCM derivato da contatore che riparte da 0** dopo un riavvio → reuse catastrofico.
5. **ECB perché "più semplice"** — qualsiasi struttura ripetitiva nel plaintext (header, JSON, immagini) trapela. È quasi sempre un bug, non una scelta.

## Domande da colloquio / CTF
- *Perché ECB è insicuro anche se AES è robusto?* — AES protegge il singolo blocco, ma ECB non nasconde l'**uguaglianza tra blocchi**: il pattern del plaintext resta visibile.
- *CBC vs CTR: differenza pratica?* — CBC è un block mode con padding e dipendenza seriale (non parallelizza in cifra); CTR trasforma AES in stream (XOR con keystream), parallelo e senza padding, ma richiede nonce unici e nessuna autenticazione intrinseca.
- *Perché GCM è raccomandato?* — è **AEAD**: cifra e autentica in un colpo, rilevando manomissioni; evita la trappola "cifrato ma non autenticato" di CBC/CTR.
- *Cosa rende possibile il CBC bit-flipping?* — la relazione `Pᵢ = Dec(Cᵢ) ⊕ Cᵢ₋₁`: il plaintext dipende linearmente dal ciphertext precedente, quindi modifiche controllate al ciphertext si riflettono nel plaintext.

## Collegamenti

- [[Crittografia Simmetrica]] — AES è il principale algoritmo simmetrico
- [[Modi Operativi dei Block Cipher]] — ECB/CBC/CTR/GCM in dettaglio
- [[Stream Cipher]] — alternativa (CTR trasforma AES in cifrario a flusso)
- [[Padding Oracle Attack]] — attacco su CBC + PKCS#7
- [[Authenticated Encryption (AEAD)]] — GCM e ChaCha20-Poly1305
- [[TLS e SSL]] — usa AES-GCM per cifrare il traffico web
- [[03. XOR]] · [[XOR]] — operazione AddRoundKey e analisi del nonce reuse
- [[OpenSSL]] — tool per usare AES da riga di comando
- [[Encoding vs Encryption]] — AES è cifratura vera, non semplice encoding
- [[Hashcat]] — cracking di file/archivi AES con password debole

## Fonti

1. Wikipedia — Advanced Encryption Standard: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
2. NIST — FIPS 197, Advanced Encryption Standard: https://csrc.nist.gov/publications/detail/fips/197/final
3. Cloudflare Learning — What is AES?: https://www.cloudflare.com/learning/ssl/what-is-aes-encryption/
4. NIST SP 800-38A/D — Block Cipher Modes (ECB/CBC/CTR e GCM): https://csrc.nist.gov/publications/detail/sp/800/38d/final
5. The Cryptopals Crypto Challenges (ECB detection, CBC bit-flip, padding oracle): https://cryptopals.com/
6. Joux — Authentication Failures in NIST GCM (nonce reuse): https://csrc.nist.gov/csrc/media/projects/block-cipher-techniques/documents/bcm/comments/800-38-series-drafts/gcm/joux_comments.pdf
7. Crypto 101 (Laurens Van Houtven), cap. 6 "Block ciphers" (keyed permutation, Rijndael, DES/3DES): https://crypto101.io/
