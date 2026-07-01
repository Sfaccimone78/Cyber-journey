---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 2
aggiornato: 2026-06-20
stato: maturo
aliases: ["Aritmetica Modulare", "CryptoHack - Mathematics (Modular Math)", "Modular Math", "Massimo Comune Divisore"]
---

## 1. Massimo Comune Divisore (GCD)

> [!info] Teoria
> Il **MCD** $\gcd(a,b)$ è il numero intero più grande che divide due interi positivi $a$ e $b$.
> - $a=12,\ b=8$ → divisori di $a$: $\{1,2,3,4,6,12\}$, divisori di $b$: $\{1,2,4,8\}$ → $\gcd=4$.
> - Due primi distinti (es. $11,17$) → $\gcd=1$.
> - Se $\gcd(a,b)=1$ → $a,b$ **coprimi**.

L'**algoritmo di Euclide** lo calcola in poche righe:

```python
def gcd(b, a):
    if b == 0:
        return a
    return gcd(a % b, b)

print(gcd(66528, 52920))
```

> [!success] Sfida
> $\gcd(66528, 52920)$ → **flag** dall'output.

---

## 2. Algoritmo di Euclide Esteso

> [!info] Teoria
> Trova interi $u,v$ tali che
> $$a \cdot u + b \cdot v = \gcd(a,b)$$
> Serve per calcolare l'**inverso modulare** dell'esponente pubblico in RSA.
>
> Se $a,b$ sono primi → $\gcd(a,b)=1$, quindi $a\cdot u + b\cdot v = 1$.

```python
def extended_gcd(a, b):
    u0, u1 = 1, 0    # coefficienti per u
    v0, v1 = 0, 1    # coefficienti per v
    while b != 0:
        quoz = a // b
        a, b = b, a % b
        u0, u1 = u1, u0 - quoz * u1
        v0, v1 = v1, v0 - quoz * v1
    return a, u0, v0   # gcd, u, v

p, q = 26513, 32321
gcd_val, u, v = extended_gcd(p, q)
print(f"GCD({p},{q}) = {gcd_val}")
print(f"u = {u}, v = {v}")
```

> [!success] Sfida
> $P=26513,\ Q=32321$ (primi) → $\gcd=1$. **Flag** = il più piccolo tra $u$ e $v$.

---

## 3. Aritmetica Modulare (Congruenze)

> [!info] Teoria
> Due interi sono **congruenti modulo $m$** se $a \equiv b \pmod m$, cioè dividendo $a$ per $m$ il resto è $b$.
> Se $m \mid a$ allora $a \equiv 0 \pmod m$.
> Intuizione: è "l'aritmetica dell'orologio" (modulo 12).

> [!success] Sfida
> - $11 \equiv x \pmod 6$ → $x = 5$
> - $8146798528947 \equiv y \pmod{17}$ → calcola $y$
> - **Flag** = il più piccolo tra $x$ e $y$.

```python
x = 11 % 6
y = 8146798528947 % 17
print(min(x, y))
```

---

## 4. Radici Quadrate Modulari (Residui Quadratici)

> [!note] Nota di Approfondimento
> Per una spiegazione approfondita dei concetti matematici, algoritmi risolutivi completi (come l'algoritmo di **Tonelli-Shanks**) e walkthrough di sfide CryptoHack, consulta la nota dedicata: [[21 Residui Quadratici e Simbolo di Legendre|Residui Quadratici e Simbolo di Legendre]].

> [!info] Teoria
> $a$ è una **radice quadrata** di $n$ modulo $P$ se $a^2 \equiv n \pmod P$. Se esiste, $n$ è un **residuo quadratico (QR)**, altrimenti **non-residuo (NQR)**.
> - In $\mathbb{F}_p^*$ esattamente **metà** dei numeri sono QR.
> - Se $a$ è radice, anche $-a \equiv P-a$ lo è → ogni QR ha **due radici**.

### Mappatura "2-a-1"
$$a^2 \equiv (P-a)^2 \pmod P$$
I numeri si accoppiano e collassano sullo stesso residuo. Con 28 elementi $(1..28)$ → $28/2 = 14$ destinazioni → 14 QR, 14 NQR.

> [!note] Perché è importante in crittografia
> - $P$ primo → formule veloci (Eulero, Tonelli-Shanks).
> - $N = p\cdot q$ composto → trovare la radice è **equivalente a fattorizzare** $N$ (problema difficile). Base di **funzioni a botola** (RSA, Rabin, ZK proofs).

### Esempio (P=29, candidati [14, 6, 11])
$8^2 = 64 \equiv 6 \pmod{29}$ → QR è **6**. Radici: $8$ e $29-8=21$.

> [!success] Sfida
> **Flag** = la radice più piccola = **8**.

```python
p = 29
candidati = [14, 6, 11]
for a in range(1, p):
    if (a * a) % p in candidati:
        r1, r2 = a, p - a
        print(f"QR: {(a*a)%p}, radici: {r1} e {r2}, flag: {min(r1, r2)}")
        break
```

---

## 5. Simbolo di Legendre & Criterio di Eulero

> [!info] Teoria — filtro veloce QR/NQR
> $$a^{\frac{p-1}{2}} \equiv \begin{cases} 1 \pmod p & a \text{ è QR} \\ -1 \equiv p-1 \pmod p & a \text{ è NQR} \\ 0 \pmod p & p \mid a \end{cases}$$
> Regola dei segni: $\text{NQR} \times \text{NQR} = \text{QR}$ (come $(-1)\times(-1)=+1$).

> [!tip] Formula radice per $p \equiv 3 \pmod 4$
> Se $a$ è QR:
> $$r \equiv \pm\, a^{\frac{p+1}{4}} \pmod p$$
> **Dimostrazione:** $r^2 \equiv a^{\frac{p+1}{2}} \equiv a \cdot a^{\frac{p-1}{2}} \equiv a \cdot 1 \equiv a \pmod p$ (per Eulero). Radici: $r$ e $p-r$.

```python
#!/usr/bin/env python3
p = 3        # sostituisci col primo della sfida
ints = []    # lista degli interi candidati

target_a = None
for a in ints:
    if pow(a, (p - 1) // 2, p) == 1:   # criterio di Eulero
        target_a = a
        print(f"[+] QR trovato: {target_a}")
        break

if target_a is None:
    print("[-] Nessun QR trovato.")
    exit()

r1 = pow(target_a, (p + 1) // 4, p)    # formula p = 3 mod 4
r2 = p - r1
print(f"Radici: {r1}, {r2}")
print(f"[!] FLAG (la maggiore): {max(r1, r2)}")
```

---

## 6. Tonelli-Shanks

> [!info] Teoria
> Algoritmo generale per risolvere $r^2 \equiv a \pmod p$ quando $p \equiv 1 \pmod 4$ (caso non coperto dalla formula semplice). Nome da un italiano del XIX secolo, riscoperto da Daniel Shanks negli anni '70.
> - **Non funziona su moduli composti** → equivalente alla fattorizzazione (difficile).
> - Uso principale: trovare coordinate su curve ellittiche.

```python
#!/usr/bin/env python3
def tonelli_shanks(a, p):
    if pow(a, (p - 1) // 2, p) != 1:      # esiste la radice?
        return None

    # Passo 1: p-1 = Q * 2^S
    s, q = 0, p - 1
    while q % 2 == 0:
        s += 1
        q //= 2
    if s == 1:                            # caso semplice p = 3 mod 4
        return pow(a, (p + 1) // 4, p)

    # Passo 2: trova un non-residuo z
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1

    # Passo 3: init
    m, c = s, pow(z, q, p)
    t, r = pow(a, q, p), pow(a, (q + 1) // 2, p)

    # Passo 4: raffinamento
    while t != 1:
        t2i, i = t, 0
        for i in range(1, m):
            t2i = pow(t2i, 2, p)
            if t2i == 1:
                break
        b = pow(c, 2 ** (m - i - 1), p)
        m, c = i, pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p
    return r

# Dati sfida (a, p a 2048 bit)
a = 8479994658316772151941616510097127087554541274812435112009425778595495359700244470400642403747058566807127814165396640215844192327900454116257979487432016769329970767046735091249898678088061634796559556704959846424131820416048436501387617211770124292793308079214153179977624440438616958575058361193975686620046439877308339989295604537867493683872778843921771307305602776398786978353866231661453376056771972069776398999013769588936194859344941268223184197231368887060609212875507518936172060702209557124430477137421847130682601666968691651447236917018634902407704797328509461854842432015009878011354022108661461024768
p = 30531851861994333252675935111487950694414332763909083514133769861350960895076504687261369815735742549428789138300843082086550059082835141454526618160634109969195486322015775943030060449557090064811940139431735209185996454739163555910726493597222646855506445602953689527405362207926990442391705014604777038685880527537489845359101552442292804398472642356609304810680731556542002301547846635101455995732584071355903010856718680732337369128498655255277003643669031694516851390505923416710601212618443109844041514942401969629158975457079026906304328749039997262960301209158175920051890620947063936347307238412281568760161

r1 = tonelli_shanks(a, p)
if r1 is not None:
    r2 = p - r1
    print(f"[!] FLAG (la più piccola): {min(r1, r2)}")
else:
    print("Non è un residuo quadratico!")
```

> [!success] Sfida
> File: `output.txt`. **Flag** = la radice più piccola tra $r$ e $p-r$.

---

## 7. Teorema Cinese del Resto (CRT)

> [!info] Teoria
> Dati interi $a_i$ e moduli **coprimi a coppie** $n_i$ (cioè $\gcd(n_i, n_j)=1$):
> $$x \equiv a_1 \pmod{n_1},\quad x \equiv a_2 \pmod{n_2},\ \dots$$
> Esiste un'unica soluzione $x \equiv a \pmod N$ con $N = n_1 \cdot n_2 \cdots n_k$.
> Uso in crypto: spezzare un problema con interi enormi in problemi piccoli.

### Sfida — risoluzione per sostituzione
Sistema (parti dal modulo più grande):
1. $x \equiv 5 \pmod{17}$
2. $x \equiv 3 \pmod{11}$
3. $x \equiv 2 \pmod 5$

$N = 5 \cdot 11 \cdot 17 = 935$.

- **Passo 1:** $x = 17k + 5$
- **Passo 2:** $17k + 5 \equiv 3 \pmod{11} \Rightarrow 6k \equiv 9 \pmod{11}$. Inverso di $6$ è $2$ → $k \equiv 18 \equiv 7 \pmod{11}$ → $k = 11m + 7$
- **Passo 3:** $x = 187m + 124$
- **Passo 4:** $187m + 124 \equiv 2 \pmod 5 \Rightarrow 2m \equiv 3 \pmod 5$. Inverso di $2$ è $3$ → $m \equiv 9 \equiv 4 \pmod 5$ → $m = 5n + 4$
- **Passo 5:** $x = 935n + 872 \Rightarrow x \equiv 872 \pmod{935}$

> [!success] Sfida
> **Flag:** `872`

```python
#!/usr/bin/env python3
rimasugli = [2, 3, 5]   # resti a_i
moduli = [5, 11, 17]    # moduli n_i

def inverso_modulare(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def crt(rim, mod):
    N = 1
    for n in mod:
        N *= n
    x = 0
    for a_i, n_i in zip(rim, mod):
        Ni = N // n_i
        x += a_i * Ni * inverso_modulare(Ni, n_i)
    return x % N

print(f"Flag: {crt(rimasugli, moduli)}")
```

---

## Collegamenti
- [[Residui Quadratici e Simbolo di Legendre]] — radici quadrate modulari, simbolo di Legendre, Tonelli-Shanks
- [[05 RSA|RSA]] — inverso modulare (Euclide esteso) e CRT sono il cuore di RSA
- [[Sfida CryptoHack - Adrien's Signs]] — applicazione pratica del simbolo di Legendre

## Fonti
- CryptoHack — Mathematics (Modular Math): https://cryptohack.org/challenges/maths/
- Menezes, van Oorschot, Vanstone — *Handbook of Applied Cryptography*, cap. 2 §2.4 "Number theory" (PDF libero): https://cacr.uwaterloo.ca/hac/
