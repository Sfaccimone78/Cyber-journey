---
tipo: lab
tag: [crypto, residui-quadratici, legendre, cryptohack, adriens-signs]
fase: 1
fonti: 1
aggiornato: 2026-06-23
stato: completato
aliases: ["Adrien's Signs", "Sfida CryptoHack - Adrien's Signs"]
---

# Sfida CryptoHack - Adrien's Signs

## 🎯 Obiettivo del Lab
Risolvere la sfida **Adrien's Signs** di CryptoHack decifrando la flag a partire da un ciphertext ottenuto manipolando i segni di potenze modulari generate casualmente.

## 💻 Ambiente & Setup
- **Piattaforma:** [CryptoHack](https://cryptohack.org/)
- **Argomenti chiave:** Residui Quadratici, Simbolo di Legendre, Criterio di Eulero, Aritmetica Modulare
- **File di riferimento:**
  - Codice sorgente: `source_734d7e14251f950935f83d228f8694ab.py`
  - Output cifrato: `output_80fc6398d2fd9f272186d0af510323f9.txt`

---

## 🔍 Analisi e Vulnerabilità

### Il Meccanismo di Cifratura
Analizzando `source_734d7e14251f950935f83d228f8694ab.py`, notiamo che la flag viene convertita in una sequenza di bit. Ogni bit $b$ viene cifrato come segue:
1. Si sceglie un esponente casuale $e$ nell'intervallo $[1, p]$.
2. Si calcola $n = a^e \pmod p$.
3. Se il bit $b$ è `'1'`, il valore aggiunto al ciphertext è $c = n$.
4. Se il bit $b$ è `'0'`, il valore aggiunto al ciphertext è $c = -n \pmod p$ (ovvero $p - n$).

I parametri pubblici sono:
- $a = 288260533169915$
- $p = 1007621497415251$

### La Debolezza (Residui Quadratici & Simbolo di Legendre)
La chiave per la decifratura risiede nel determinare se $c$ sia della forma $a^e$ o $-a^e \pmod p$.
Il **Simbolo di Legendre** $\left(\frac{x}{p}\right)$ è uno strumento fondamentale:
- $\left(\frac{x}{p}\right) = 1$ se $x$ è un residuo quadratico modulo $p$ (cioè $x \equiv y^2 \pmod p$).
- $\left(\frac{x}{p}\right) = -1$ se $x$ è un non-residuo quadratico modulo $p$.

Utilizziamo la proprietà moltiplicativa del simbolo di Legendre:
$$\left(\frac{-n}{p}\right) = \left(\frac{-1}{p}\right) \cdot \left(\frac{n}{p}\right)$$

1. **Analisi di $\left(\frac{-1}{p}\right)$**:
   Il valore di $\left(\frac{-1}{p}\right)$ dipende da $p \pmod 4$:
   $$p \equiv 1007621497415251 \equiv 3 \pmod 4$$
   Poiché $p \equiv 3 \pmod 4$, si ha:
   $$\left(\frac{-1}{p}\right) = -1$$

2. **Analisi di $\left(\frac{a}{p}\right)$**:
   Calcoliamo il simbolo di Legendre di $a$ usando il Criterio di Eulero ($a^{(p-1)/2} \pmod p$):
   $$a^{\frac{p-1}{2}} \equiv 288260533169915^{503810748707625} \equiv 1 \pmod p$$
   Quindi $\left(\frac{a}{p}\right) = 1$.

3. **Determinazione del Bit**:
   Poiché $n = a^e \pmod p$, il simbolo di Legendre di $n$ è:
   $$\left(\frac{n}{p}\right) = \left(\frac{a^e}{p}\right) = \left(\frac{a}{p}\right)^e = 1^e = 1$$
   Quindi, per qualsiasi esponente casuale $e$, $n$ è **sempre** un residuo quadratico modulo $p$.
   
   Ora verifichiamo il comportamento per i due possibili bit cifrati:
   - Se il bit è `'1'`:
     $$c = n \implies \left(\frac{c}{p}\right) = \left(\frac{n}{p}\right) = 1$$
   - Se il bit è `'0'`:
     $$c = -n \implies \left(\frac{c}{p}\right) = \left(\frac{-1}{p}\right) \cdot \left(\frac{n}{p}\right) = -1 \cdot 1 = -1 \pmod p$$

Grazie a questo, possiamo decifrare ciascun bit in modo deterministico calcolando semplicemente il simbolo di Legendre del valore del ciphertext.

---

## 🛠️ Script di Risoluzione (Python)

Il seguente script Python legge dinamicamente i dati da `output_80fc6398d2fd9f272186d0af510323f9.txt` e ricostruisce la flag:

```python
# Definizione dei parametri forniti
a = 288260533169915
p = 1007621497415251

# 1. Carica il ciphertext dal file di output
with open("output_80fc6398d2fd9f272186d0af510323f9.txt", "r") as f:
    ciphertext = eval(f.read().strip())

# 2. Decifra i bit usando il Criterio di Eulero per il Simbolo di Legendre
plaintext_bits = ""
for c in ciphertext:
    # Calcolo di c^((p-1)//2) mod p
    legendre = pow(c, (p - 1) // 2, p)
    
    if legendre == 1:
        plaintext_bits += "1"
    elif legendre == p - 1:  # Equivalente a -1 mod p
        plaintext_bits += "0"
    else:
        raise ValueError(f"Valore del simbolo di Legendre non valido riscontrato: {legendre}")

# 3. Raggruppa i bit in byte e decodifica la stringa
flag_bytes = bytearray()
for i in range(0, len(plaintext_bits), 8):
    byte_str = plaintext_bits[i:i+8]
    flag_bytes.append(int(byte_str, 2))

# 4. Stampa il risultato
print("Flag decifrata:", flag_bytes.decode('utf-8'))
```

---

## 🏆 Flag Recuperata

```text
crypto{p4tterns_1n_re5idu3s}
```

---

## 📝 Cosa ho imparato
- **Criterio di Eulero:** È un metodo efficiente $O(\log p)$ per calcolare il simbolo di Legendre ed esaminare la quadratic residuosity di un intero modulo un primo $p$.
- **Leaking di Informazione:** Se una cifratura dipende dal segno modulare di un elemento e il modulo soddisfa $p \equiv 3 \pmod 4$, la quadratic residuosity viene ribaltata per il segno negativo, permettendo la decifratura deterministica di singoli bit.
- **Importanza della Scelta del Modulo:** L'uso di operazioni condizionate sul segno modulare (come $-n \pmod p$) introduce seri problemi di leakage di canali laterali matematici (quadratic residuosity leakage).
