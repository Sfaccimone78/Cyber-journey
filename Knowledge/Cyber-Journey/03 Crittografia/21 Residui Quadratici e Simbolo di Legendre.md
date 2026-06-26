---
tipo: concetto
tag: [crypto, matematica, residui-quadratici, legendre, cryptohack]
fase: 2
fonti: 1
aggiornato: 2026-06-23
stato: maturo
aliases: ["Residui Quadratici", "Quadratic Residues", "Simbolo di Legendre", "Tonelli-Shanks"]
---

# Residui Quadratici e Simbolo di Legendre

## 💡 In parole semplici
In aritmetica modulare, un numero $a$ è un **residuo quadratico** modulo $p$ se è un "quadrato perfetto" in quel sistema numerico. In altre parole, se è possibile trovare un intero $x$ tale che elevato al quadrato dia proprio $a$ (ovvero $x^2 \equiv a \pmod p$). Se tale numero non esiste, $a$ si dice **non-residuo quadratico**.

> [!TIP]
> **Esempio pratico in modulo 7:**
> - $1^2 = 1 \equiv 1 \pmod 7$
> - $2^2 = 4 \equiv 4 \pmod 7$
> - $3^2 = 9 \equiv 2 \pmod 7$
> - $4^2 = 16 \equiv 2 \pmod 7$
> - $5^2 = 25 \equiv 4 \pmod 7$
> - $6^2 = 36 \equiv 1 \pmod 7$
> 
> I **residui quadratici** modulo 7 sono $\{1, 2, 4\}$. I **non-residui** sono $\{3, 5, 6\}$.
> Notiamo che ciascun residuo ha esattamente **due radici quadrate** (es. per 2 le radici sono $3$ e $4 \equiv -3 \pmod 7$).

---

## 🔍 Come funziona (Teoria Matematica)

Sia $p$ un numero primo dispari. Un intero $a$ coprimo con $p$ si dice:
- **Residuo Quadratico (QR)** se esiste $x$ tale che $x^2 \equiv a \pmod p$.
- **Non-Residuo Quadratico (NQR)** se non esiste alcuna soluzione.

### Proprietà Fondamentali
1. **Cardinalità**: In $\mathbb{F}_p^*$ (il gruppo moltiplicativo degli interi modulo $p$), ci sono esattamente $\frac{p-1}{2}$ residui quadratici e $\frac{p-1}{2}$ non-residui quadratici.
2. **Mappatura 2-a-1**: Se $x$ è una radice quadrata di $a$, allora anche $-x \equiv p-x$ lo è. Non vi sono altre radici.

### Il Simbolo di Legendre
Il simbolo di Legendre è una funzione che indica se un numero è QR modulo un primo $p$:
$$\left(\frac{a}{p}\right) = \begin{cases} 
1 & \text{se } a \text{ è QR modulo } p \\ 
-1 & \text{se } a \text{ è NQR modulo } p \\ 
0 & \text{se } a \equiv 0 \pmod p 
\end{cases}$$

#### Proprietà Algebriche:
- **Moltiplicatività**: $\left(\frac{ab}{p}\right) = \left(\frac{a}{p}\right) \left(\frac{b}{p}\right)$.
- **Periodicità**: Se $a \equiv b \pmod p$, allora $\left(\frac{a}{p}\right) = \left(\frac{b}{p}\right)$.
- **Omomorfismo**: Comportamento analogo al prodotto dei segni (+ e -):
  - $\text{QR} \times \text{QR} = \text{QR} \implies (1) \times (1) = 1$
  - $\text{QR} \times \text{NQR} = \text{NQR} \implies (1) \times (-1) = -1$
  - $\text{NQR} \times \text{NQR} = \text{QR} \implies (-1) \times (-1) = 1$

### Criterio di Eulero
Il criterio di Eulero fornisce una formula esplicita per calcolare il simbolo di Legendre usando l'elevamento a potenza modulare:
$$\left(\frac{a}{p}\right) \equiv a^{\frac{p-1}{2}} \pmod p$$

---

## 🛠️ Algoritmi di Risoluzione (Calcolo delle Radici)

Dato $a$ che sappiamo essere un residuo quadratico ($\left(\frac{a}{p}\right) = 1$), come troviamo $x$ tale che $x^2 \equiv a \pmod p$?

### Caso 1: Quando $p \equiv 3 \pmod 4$ (Formula Diretta)
Se il primo soddisfa la congruenza $p \equiv 3 \pmod 4$ (ovvero $p = 4k + 3$), esiste una formula deterministica immediata:
$$x \equiv \pm a^{\frac{p+1}{4}} \pmod p$$

> [!NOTE]
> **Dimostrazione:**
> Vogliamo verificare che $x^2 \equiv a \pmod p$:
> $$x^2 \equiv \left(a^{\frac{p+1}{4}}\right)^2 \equiv a^{\frac{p+1}{2}} \equiv a \cdot a^{\frac{p-1}{2}} \pmod p$$
> Per il criterio di Eulero, sapendo che $a$ è QR, $a^{\frac{p-1}{2}} \equiv 1 \pmod p$. Dunque:
> $$x^2 \equiv a \cdot 1 \equiv a \pmod p \quad \blacksquare$$

### Caso 2: Quando $p \equiv 1 \pmod 4$ (Algoritmo di Tonelli-Shanks)
Nel caso in cui $p \equiv 1 \pmod 4$, non esiste una formula chiusa semplice. Si utilizza l'algoritmo di **Tonelli-Shanks**.

#### Implementazione Python dell'algoritmo di Tonelli-Shanks:
```python
def tonelli_shanks(a, p):
    # Verifica preliminare se a è effettivamente un residuo quadratico
    if pow(a, (p - 1) // 2, p) != 1:
        return None  # Non ha radici quadrate modulo p

    # 1. Scrivere p - 1 come Q * 2^S con Q dispari
    s = 0
    q = p - 1
    while q % 2 == 0:
        s += 1
        q //= 2
        
    if s == 1:
        return pow(a, (p + 1) // 4, p)

    # 2. Trovare un non-residuo quadratico z modulo p
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1

    # 3. Inizializzazione delle variabili
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)

    # 4. Ciclo di raffinamento
    while t != 1:
        # Trova il più piccolo i (0 < i < m) tale che t^(2^i) = 1
        t2i = t
        i = 0
        for i in range(1, m):
            t2i = pow(t2i, 2, p)
            if t2i == 1:
                break
        
        # Aggiornamento delle variabili
        b = pow(c, 2 ** (m - i - 1), p)
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p
        
    return r  # Restituisce una delle due radici: r e p-r
```

---

## 🎯 Come risolvere le sfide di CryptoHack

CryptoHack include diverse sfide nella sezione **Mathematics** basate su questa teoria. Ecco la metodologia per ciascuna classe di problemi:

### 1. Trovare la radice quadrata modulare (Sfida "Modular Square Root")
- **Problema:** Ti viene fornito un intero $a$ e un grande primo $p$ e ti viene chiesto di trovare $x$ tale che $x^2 \equiv a \pmod p$.
- **Risoluzione:**
  1. Controlla la forma di $p$: calcola `p % 4`.
  2. Se `p % 4 == 3`, usa la formula veloce: `pow(a, (p + 1) // 4, p)`.
  3. Se `p % 4 == 1`, implementa o importa l'algoritmo di **Tonelli-Shanks** per estrarre la radice.
  4. La sfida solitamente richiede di inserire la radice più piccola tra $x$ e $p-x$.

### 2. Filtrare residui quadratici (Sfida "Legendre Symbol")
- **Problema:** Ti vengono dati un primo $p$ e una lista di interi. Devi individuare quale tra questi è un residuo quadratico modulo $p$.
- **Risoluzione:**
  - Itera sulla lista ed applica il **Criterio di Eulero** calcolando `pow(x, (p - 1) // 2, p)`.
  - Il residuo quadratico restituirà `1`. I non-residui restituiranno `p - 1` (cioè $-1$).

### 3. Leakage del segno modulare (Sfida "Adrien's Signs")
- **Problema:** Il sistema cifra i bit di una flag generando $c = a^e \pmod p$ per il bit `1` e $c = -a^e \pmod p$ per il bit `0`. Vengono forniti $a$, $p$ e il ciphertext.
- **Vulnerabilità:**
  1. Il primo $p$ soddisfa $p \equiv 3 \pmod 4$, quindi $\left(\frac{-1}{p}\right) = -1$.
  2. La base $a$ è un residuo quadratico, quindi $\left(\frac{a}{p}\right) = 1 \implies \left(\frac{a^e}{p}\right) = 1$ per qualunque esponente $e$.
  3. Di conseguenza:
     - Se il bit cifrato è `1` $\implies \left(\frac{c}{p}\right) = 1$.
     - Se il bit cifrato è `0` $\implies \left(\frac{c}{p}\right) = \left(\frac{-1}{p}\right) \left(\frac{a^e}{p}\right) = -1 \cdot 1 = -1 \equiv p-1 \pmod p$.
- **Risoluzione:** 
  Per ciascun numero $c$ del ciphertext, calcola `pow(c, (p - 1) // 2, p)`. Se fa `1` il bit è `1`, se fa `p-1` il bit è `0`.
  *(Vedi la nota di walkthrough dedicata: [[Sfida CryptoHack - Adrien's Signs]])*

---

## ❓ Domande Frequenti e Dubbi

### Che cosa succede se il modulo $N$ è composto ($N = p \cdot q$)?
Se il modulo $N$ è il prodotto di due numeri primi sconosciuti (come in RSA), trovare le radici quadrate di un residuo quadratico modulo $N$ è un **problema computazionalmente difficile**.
In effetti, è matematicamente dimostrato che **estrarre radici quadrate modulo $N$ composto è equivalente a fattorizzare $N$**. 
- Se conosci $p$ e $q$, puoi calcolare le radici modulo $p$ e modulo $q$ (tramite Tonelli-Shanks) e poi combinarle usando il **Teorema Cinese del Resto (CRT)**. Questo produrrà $4$ radici quadrate distinte modulo $N$.
- Se non conosci i fattori, non esiste alcun algoritmo noto efficiente. Questa asimmetria è la base di sicurezza del cifrario a botola di **Rabin**.

---

## 🔗 Collegamenti
- [[19 Aritmetica Modulare|19 Aritmetica Modulare]] (Basi di congruenze modulari e GCD)
- [[05 RSA|05 RSA]] (Applicazioni del calcolo modulare in crittografia asimmetrica)
- [[Sfida CryptoHack - Adrien's Signs]] (Walkthrough pratico della sfida correlata)

## 📚 Fonti
- **CryptoHack Mathematics**: [Challenges - Maths](https://cryptohack.org/challenges/maths/)
- **Wikipedia**: [Quadratic Residue (Residui Quadratici)](https://en.wikipedia.org/wiki/Quadratic_residue)
