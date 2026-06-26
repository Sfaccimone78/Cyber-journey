---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 2
aggiornato: 2026-06-20
stato: maturo
aliases: ["Bytes e Long"]
---

# Bytes e Long

## In breve
Algoritmi come **[[RSA]]** operano su **interi enormi**, ma i dati reali sono **sequenze di byte**. Saper convertire tra le due rappresentazioni è un passo base di ogni sfida crittografica.

## Come funziona
Ogni sequenza di byte è interpretabile come un intero in **Big-Endian**:

$$\text{long} = b_0 \times 256^{n-1} + b_1 \times 256^{n-2} + \ldots + b_{n-1} \times 256^0$$

dove $b_i$ è il valore del byte alla posizione $i$ e $n$ è la lunghezza totale.

> [!example] Esempio
> Il byte `0x41` (carattere `A`) ha valore intero `65`.
> La stringa `b"AB"` → `0x4142` → intero `16706`.

## Esempio pratico
```python
from Crypto.Util.number import bytes_to_long, long_to_bytes

# bytes → long
message = b"crypto{learning_to_convert_bytes}"
number = bytes_to_long(message)
# number è un intero molto grande

# long → bytes
restored = long_to_bytes(number)
print(restored.decode('utf-8'))  # riottieni la stringa originale
```

> [!warning] Attenzione alla lunghezza
> `long_to_bytes` inferisce la lunghezza minima necessaria.
> Se devi produrre output di lunghezza fissa (es. modulo RSA a 2048 bit = 256 byte), usa `long_to_bytes(n, 256)`.

## Collegamenti
- [[RSA]] — opera su interi: serve convertire i byte del messaggio in `long`
- [[Aritmetica Modulare]] — la matematica che gira su questi interi
- [[Base64]] — un'altra rappresentazione dei dati binari
- [[Encoding vs Encryption]] — conversione di rappresentazione, non cifratura

## Fonti
- CryptoHack — General challenges: https://cryptohack.org/challenges/general/
- PyCryptodome — `Crypto.Util.number`: https://pycryptodome.readthedocs.io/en/latest/src/util/util.html
