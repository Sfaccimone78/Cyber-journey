---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 8
aggiornato: 2026-06-26
stato: maturo
aliases: ["RSA"]
---

# RSA

## In breve
**RSA** (Rivest–Shamir–Adleman, 1977) è l'algoritmo di [[Crittografia Asimmetrica]] più noto. La sicurezza poggia sulla difficoltà di **fattorizzare** `n = p × q` quando `p` e `q` sono primi molto grandi: conosci `n` ed `e` (pubblici) ma senza `p`,`q` non ricavi `d` (privato). Usato per scambio chiavi, firma e autenticazione in [[TLS e SSL]] e [[Certificati Digitali e CA]].

## Generazione delle chiavi
1. Scegli due primi grandi `p`, `q`.
2. `n = p × q` (il **modulo**, parte pubblica).
3. `φ(n) = (p-1)(q-1)` (toziente di Eulero).
4. Scegli `e` con `MCD(e, φ(n)) = 1` (tipico `65537`).
5. `d = e⁻¹ mod φ(n)` (**inverso modulare**, vedi [[Aritmetica Modulare]]).

- **Chiave pubblica** `(e, n)` · **Chiave privata** `(d, n)`.
- **Cifra** `c = mᵉ mod n` · **Decifra** `m = cᵈ mod n`.
- **Firma** (inverso dei ruoli): firmi con `d`, chiunque verifica con `e`.

```python
p, q = 61, 53
n   = p * q            # 3233
phi = (p-1)*(q-1)      # 3120
e   = 17
d   = pow(e, -1, phi)  # 2753  (inverso modulare, Python 3.8+)

m  = 65
c  = pow(m, e, n)      # cifra  → 2790
m2 = pow(c, d, n)      # decifra → 65 ✓
```

## Perché è lento, e come si usa davvero
RSA è **molto più lento** del cifrario simmetrico e cifra al massimo ~modulo byte. Quindi nella pratica è **ibrido**: RSA cifra (o firma) solo una **chiave di sessione** [[AES]], che poi cifra i dati veri. È lo schema di [[TLS e SSL]].

## Attacchi (perché "RSA raw" è pericoloso)
| Condizione | Attacco |
|---|---|
| `e` piccolo (es. 3) + niente padding + `m` piccolo | **Cube root / Håstad** — `m = ∛c` se `mᵉ < n` |
| Stesso `m` a destinatari diversi con `e=3` | **Håstad broadcast** (CRT) |
| `d` piccolo | **Wiener** (frazioni continue) |
| `p` e `q` troppo vicini | **Fermat factorization** |
| `n` condiviso / GCD comune tra chiavi | `gcd(n1,n2)` rivela un fattore |
| Errori di tempo/oracolo sul padding | **Bleichenbacher** (padding oracle) |

Difesa: **mai RSA testuale**. Usa sempre padding: **OAEP** per cifrare, **PSS** per firmare. Chiavi **≥ 2048 bit** (meglio 3072/4096). RC: i computer quantistici (algoritmo di **Shor**) romperebbero RSA → ricerca su crittografia **post-quantistica**.

## In CTF
Vedi spesso `n`, `e`, `c` e devi recuperare `m`. Workflow tipico: fattorizza `n` (FactorDB, Fermat, Pollard rho), ricostruisci `φ` e `d`, decifra. Tool: `RsaCtfTool`, FactorDB. Le sfide di **CryptoHack** sezione RSA coprono ogni variante.

---

# Strato esperto

## Meccanismo interno — la matematica che fa funzionare RSA

### Perché `m = cᵈ mod n` riporta al messaggio
La correttezza di RSA è un corollario del **teorema di Eulero** (vedi [[Aritmetica Modulare]]): se `MCD(m,n)=1` allora `m^φ(n) ≡ 1 (mod n)`. Per costruzione `e·d ≡ 1 (mod φ(n))`, cioè `e·d = 1 + k·φ(n)`. Quindi:
```
cᵈ = (mᵉ)ᵈ = m^(e·d) = m^(1 + k·φ(n)) = m · (m^φ(n))ᵏ ≡ m · 1ᵏ ≡ m (mod n)
```
Il caso `MCD(m,n)≠1` (cioè `m` multiplo di `p` o `q`) si chiude con il **teorema cinese del resto** (CRT): l'identità vale comunque modulo `p` e modulo `q`, quindi modulo `n`.

### CRT per decifrare/firmare 3–4× più veloce
In pratica il software **non** calcola `cᵈ mod n` direttamente. Precalcola `dp = d mod (p-1)`, `dq = d mod (q-1)`, `qinv = q⁻¹ mod p`, poi:
```python
m1 = pow(c, dp, p)
m2 = pow(c, dq, q)
h  = (qinv * (m1 - m2)) % p
m  = m2 + h * q          # ricomposizione CRT
```
> [!danger] Fault attack (Bellcore)
> Se durante una firma RSA-CRT avviene un **glitch** in uno solo dei due rami (es. `m1` corrotto), l'attaccante che vede la firma errata `s'` e il messaggio recupera un fattore con `p = gcd(s'ᵉ − m, n)`. È la ragione per cui le smartcard verificano la firma prima di emetterla.

### φ(n) vs λ(n)
Molte implementazioni usano la **funzione di Carmichael** `λ(n) = lcm(p-1, q-1)` al posto di `φ(n)` per ottenere il `d` minimo (PKCS#1 lo prevede). Per gli attacchi è indifferente: chi conosce `p,q` conosce entrambe.

## Attacchi pratici passo-passo (CTF)

### 1. Small `e` / cube root (quando: `e=3`, niente padding, `m` corto)
Se `mᵉ < n` allora `c = mᵉ` su interi (nessuna riduzione modulare) e basta la radice e-esima esatta:
```python
from gmpy2 import iroot
m, exact = iroot(c, 3)     # ∛c
```
Se `m³` ha "wrappato" poche volte, prova `iroot(c + k*n, 3)` per `k = 0,1,2,...`.

### 2. Håstad broadcast (quando: stesso `m`, `e` destinatari con `e=3` e moduli `nᵢ` coprimi)
Hai `c₁,c₂,c₃` con `cᵢ = m³ mod nᵢ`. Con CRT ricostruisci `M = m³ mod (n₁n₂n₃)`; poiché `m³ < n₁n₂n₃`, `M = m³` su interi → radice cubica.
```python
from sympy.ntheory.modular import crt
M, _ = crt([n1,n2,n3], [c1,c2,c3])
m, _ = iroot(M, 3)
```

### 3. Common modulus (quando: stesso `n`, stesso `m`, due `e₁,e₂` con `gcd(e₁,e₂)=1`)
Hai `c₁=m^e₁`, `c₂=m^e₂`. Con Bézout `a·e₁ + b·e₂ = 1`, allora `c₁ᵃ · c₂ᵇ ≡ m (mod n)` (uno dei due esponenti è negativo → usa l'inverso del ciphertext).
```python
g, a, b = gmpy2.gcdext(e1, e2)
m = (pow(c1, a, n) * pow(gmpy2.invert(c2, n), -b, n)) % n  # se b<0
```

### 4. Wiener (quando: `d` piccolo, `d < n^0.25 / 3`)
Espandi `e/n` in **frazione continua**; uno dei convergenti `k/d` rivela `d`. Verifica ogni candidato controllando che `(e·d − 1)/k = φ` sia intero e che il polinomio `x² − (n−φ+1)x + n` abbia radici intere (`p,q`). Tool pronto: `RsaCtfTool --attack wiener` o lo script `wiener_attack.py`.

### 5. Fattori vicini — Fermat (quando: `|p − q|` piccolo)
`n = a² − b² = (a−b)(a+b)`. Parti da `a = ⌈√n⌉`, incrementa finché `a²−n` è un quadrato perfetto `b²`; allora `p=a−b`, `q=a+b`.
```python
a = isqrt(n) + 1
while not is_square(a*a - n): a += 1
b = isqrt(a*a - n); p, q = a-b, a+b
```

### 6. Fattori condivisi / GCD batch (quando: molte chiavi generate con RNG debole)
Se due moduli condividono un primo, `gcd(n₁, n₂) = p` lo rivela istantaneamente — fu il caso del paper *"Mining your Ps and Qs"* (2012). In CTF: dato un pacchetto di chiavi, calcola i GCD a coppie (o usa l'algoritmo batch-GCD).

### 7. Padding oracle (Bleichenbacher, PKCS#1 v1.5)
Se il server rivela (anche via timing/errore distinto) se un ciphertext si decifra in un blocco **PKCS#1 v1.5 valido** (inizia con `00 02`), si recupera `m` adattivamente moltiplicando `c` per `sᵉ` e restringendo l'intervallo. È un **oracle**, non una rottura di RSA: la difesa è OAEP + risposte indistinguibili.

## Padding: textbook vs OAEP
- **Textbook (raw)** — deterministico (lo stesso `m` dà sempre lo stesso `c` → distinguibile, malleabile: `(m₁m₂)ᵉ = c₁c₂`). Mai in produzione.
- **PKCS#1 v1.5** — aggiunge randomness ma è vulnerabile a Bleichenbacher.
- **OAEP** — padding randomizzato con due hash (mask generation function): rende RSA semanticamente sicuro. Per le **firme** l'analogo è **PSS** (non usare PKCS#1 v1.5 firma se evitabile).

## Casi limite
- `e` non coprimo con `φ(n)` → `d` non esiste: scegli un altro `e`.
- `p == q` → `n` è un quadrato, `φ(n) = p(p−1)`, fattorizzazione banale (`√n`).
- `m = 0, 1, n−1` → punti fissi: `c = m` (messaggi "non cifrati").
- **`e = 1`** → cifratura nulla (`m¹ ≡ m`): il ciphertext **è** il plaintext. Sembra assurdo ma è stato un bug reale e di lunga durata in **Salt** (gestione configurazioni). [Fonte: Crypto101, cap. 9]
- Multi-prime RSA (`n = p·q·r`) → la decifra CRT scala, ma se un fattore è piccolo cade subito.

> [!note] Quanto è lento RSA davvero
> Decifrare 256 byte con RSA-2048 costa ~11 megacicli contro ~3 kilocicli di un cifrario simmetrico: **~4000× più lento**. È la ragione strutturale per cui RSA cifra solo una chiave di sessione, mai i dati (schema ibrido). [Fonte: Crypto101, cap. 9]

## Troubleshooting (errori comuni)
1. **`pow(e,-1,phi)` lancia ValueError** — `e` non è invertibile: `MCD(e,φ)≠1`. Causa: `e` condivide un fattore con `p-1` o `q-1`.
2. **Decifra restituisce spazzatura** — hai usato `φ` sbagliato (es. `(p-1)(q-1)` quando il testo usava `λ`), oppure `c` non era ridotto mod `n`.
3. **`int.from_bytes` del plaintext > n** — il messaggio è più lungo del modulo: va spezzato o (correttamente) si cifra solo una chiave di sessione.
4. **Cube root fallisce** — `m³ ≥ n`: l'attacco small-e richiede `mᵉ < n`; prova i `k·n` o un altro vettore.
5. **Firma PKCS#1 v1.5 "verifica" testo arbitrario** — implementazione che non controlla il padding fino in fondo (Bleichenbacher '06, "BERserk"): bug classico nelle CTF di crypto-firma.

## Domande da colloquio / CTF
- *Perché `e=65537` e non `e=3`?* — 65537 è primo (sempre coprimo con `φ` di buoni primi) ed è `2¹⁶+1` (solo 2 bit a 1 → esponenziazione veloce), evitando le trappole di `e` troppo piccolo senza padding.
- *Conoscere `φ(n)` equivale a fattorizzare `n`?* — Sì: da `n` e `φ=n-(p+q)+1` ricavi `p+q`, e con `p·q=n` risolvi l'equazione di secondo grado → `p,q`.
- *Perché RSA testuale è malleabile e perché è un problema?* — `Enc(m₁)·Enc(m₂) = Enc(m₁·m₂)`: un attaccante manipola il ciphertext senza la chiave (es. cambia un voto/importo). OAEP rompe questa omomorfia.
- *Cosa rompe RSA su un computer quantistico?* — L'algoritmo di **Shor** fattorizza in tempo polinomiale → migrazione alla crittografia post-quantistica (es. ML-KEM/Kyber).

## Collegamenti
- [[Crittografia Asimmetrica]] — RSA è l'implementazione più nota
- [[Aritmetica Modulare]] — base matematica
- [[Firma Digitale]]
- [[Certificati Digitali e CA]]
- [[OpenSSL]]
- [[Scambio di Chiavi Diffie-Hellman]] — alternativa moderna per lo scambio chiavi
- [[TLS e SSL]]

## Fonti
- Wikipedia — RSA (cryptosystem): https://en.wikipedia.org/wiki/RSA_(cryptosystem)
- NIST FIPS 186-5 — Digital Signature Standard: https://csrc.nist.gov/publications/detail/fips/186/5/final
- Cloudflare — Asymmetric encryption: https://www.cloudflare.com/learning/ssl/what-is-asymmetric-encryption/
- CryptoHack — RSA challenges: https://cryptohack.org/challenges/rsa/
- Dan Boneh — Twenty Years of Attacks on the RSA Cryptosystem: https://crypto.stanford.edu/~dabo/abstracts/RSAattack-survey.html
- Heninger et al. — Mining Your Ps and Qs (shared factors): https://factorable.net/
- RFC 8017 — PKCS#1 v2.2 (RSAES-OAEP / RSASSA-PSS): https://datatracker.ietf.org/doc/html/rfc8017
- Crypto 101 (Laurens Van Houtven), cap. 9 "Public-key encryption" / RSA / OAEP: https://crypto101.io/
