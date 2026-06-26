---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 2
aggiornato: 2026-06-26
stato: maturo
aliases: ["Padding Oracle Attack", "Padding Oracle"]
---

# Padding Oracle Attack

## Definizione

Il **padding oracle attack** è un attacco **chosen-ciphertext** che permette di **decifrare interamente** un messaggio cifrato in **CBC** ([[Modi Operativi dei Block Cipher]]) — e anche di cifrarne di nuovi — **senza conoscere la chiave**. Sfrutta un solo bit di informazione: il sistema rivela se, dopo la decifratura, il **padding è valido o no**. [Fonte: Crypto101, cap. 7]

> È l'esempio canonico del principio *encryption is not authentication*: usare CBC senza un MAC che copra il ciphertext lascia aperto questo oracolo. La cura definitiva è l'**AEAD** ([[Authenticated Encryption (AEAD)]]).

## Intuizione

Il destinatario, ricevuto un ciphertext, lo decifra e **controlla il padding** (PKCS#7). Se è malformato, risponde con un errore (o impiega un tempo diverso, o chiude la connessione). Quel comportamento osservabile è l'**"oracolo"**: una funzione che, dato un ciphertext, dice "padding valido / non valido". Mallory non ha bisogno d'altro: con tante query mirate ricostruisce il plaintext byte per byte. **Un bit per query → l'intero messaggio.**

## La matematica

In CBC la decifratura del blocco `i` è:

```
P_i = D(k, C_i) ⊕ C_{i-1}
```

dove `D` è la decifratura del block cipher e `C_{i-1}` il ciphertext precedente (o l'IV). L'attaccante controlla `C_{i-1}` perché **lo invia lui**.

Per attaccare l'**ultimo byte** del blocco `P_i`, Mallory prende `C_{i-1}` e prova tutti i 256 valori di un byte `b` in posizione finale, mandando `(b‖…‖C_i)` all'oracolo. Sia `I_i = D(k, C_i)` (**intermediate**, ignoto ma fisso). Per ogni byte:

```
plaintext_byte = I_i[15] ⊕ b
```

Quando Mallory trova il `b` che produce **padding valido**, nel caso più probabile l'ultimo byte decifrato vale `0x01`:

```
0x01 = I_i[15] ⊕ b   ⟹   I_i[15] = b ⊕ 0x01
```

Ricavato `I_i[15]`, il byte reale del messaggio originale è:

```
P_i[15] = I_i[15] ⊕ C_{i-1}[15]   (con il C_{i-1} *vero*)
```

Poi si passa al penultimo byte forzando il padding a `0x02 0x02`, e così via. Costo: **~128 query in media per byte** (256/2), quindi lineare nella lunghezza del messaggio — banale rispetto a una ricerca esaustiva della chiave. [Fonte: Crypto101, cap. 7]

> Edge case: a volte il padding valido trovato non è `0x01` ma p.es. un `0x02 0x02` preesistente. Si rileva alterando il penultimo byte e verificando se l'oracolo cambia idea.

## Procedura (blocco da 16 byte)

Per recuperare l'ultimo byte:
1. `C'_{i-1} = 15 byte arbitrari ‖ b`, con `b = 0x00…0xFF`.
2. Invia `C'_{i-1} ‖ C_i`, osserva l'oracolo.
3. Al "valido": `I_i[15] = b ⊕ 0x01`, quindi `P_i[15] = I_i[15] ⊕ C_{i-1}[15]` (vero).
4. Per il byte 14: imposta il byte 15 di `C'_{i-1}` in modo che decifri a `0x02` (`C'_{i-1}[15] = I_i[15] ⊕ 0x02`), brute-forza il byte 14 cercando il padding `0x02 0x02`.
5. Ripeti fino a coprire il blocco; passa al blocco precedente. Tool: `padbuster`, script Cryptopals #17.

## Casi reali

- **POODLE** (2014): padding oracle su **SSL 3.0** (padding non deterministico, MAC-then-encrypt), sfruttato dopo downgrade. → [[TLS e SSL]]
- **Lucky13** (2013): padding oracle **via timing** in TLS — il tempo di calcolo del MAC dipende dal padding rimosso. → [[Attacchi Crittografici]]
- **Vaudenay (2002)**: il paper originale che introdusse l'attacco contro CBC/PKCS#7.
- **Bleichenbacher / ROBOT**: l'analogo padding oracle su **RSA PKCS#1 v1.5**. → [[RSA]]

## Mitigazioni

- **Usare AEAD** (AES-GCM, ChaCha20-Poly1305): il tag autentica il ciphertext → ogni manomissione è rifiutata **prima** di guardare il padding. → [[Authenticated Encryption (AEAD)]]
- Se proprio CBC: **Encrypt-then-MAC** sull'intero ciphertext (incluso IV); verifica del MAC **constant-time**; non rivelare *perché* la decifratura fallisce (stesso errore, stesso timing). → [[MAC e HMAC]]
- TLS 1.3 ha **rimosso del tutto CBC** proprio per chiudere questa classe. → [[TLS e SSL]]

## Collegamenti
- Modo vulnerabile: [[Modi Operativi dei Block Cipher]] (CBC, padding PKCS#7)
- Cura: [[Authenticated Encryption (AEAD)]] · [[MAC e HMAC]]
- Panoramica e timing variant: [[Attacchi Crittografici]]
- Protocollo colpito: [[TLS e SSL]] · analogo RSA: [[RSA]]
- [[00 — Mappa Crittografia|Mappa Crittografia]]

## Fonti
- Crypto 101 (Laurens Van Houtven), cap. 7 "CBC — Padding oracle attacks": https://crypto101.io/
- Serge Vaudenay — Security Flaws Induced by CBC Padding (2002): https://www.iacr.org/archive/eurocrypt2002/23320530/cbc02_e02d.pdf
