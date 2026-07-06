---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Crittografia Simmetrica"]

---

# Crittografia Simmetrica

## In breve

La **crittografia simmetrica** usa la **stessa chiave** sia per cifrare (nascondere) che per decifrare (recuperare) un messaggio. È come un lucchetto fisico: chi ha la chiave può sia chiudere che aprire. Veloce ed efficiente, viene usata per proteggere grandi quantità di dati.

## Come funziona

1. Il mittente e il destinatario si accordano su una **chiave segreta condivisa** (una sequenza di bit, es. 128 o 256 bit).
2. Il mittente usa la chiave + un **algoritmo di cifratura** (come [[AES]]) per trasformare il testo leggibile (**plaintext**) in testo cifrato (**ciphertext**).
3. Il destinatario usa la **stessa chiave** per invertire il processo e ottenere il plaintext originale.

Il problema principale è la **distribuzione della chiave**: come si consegna la chiave segreta in modo sicuro? Questo problema è risolto con la [[Crittografia Asimmetrica]] o lo [[Scambio di Chiavi Diffie-Hellman]].

## Esempio pratico

Cifrare un file con AES-256 usando [[OpenSSL]]:

```bash
# Cifrare
openssl enc -aes-256-cbc -salt -in segreto.txt -out segreto.enc -k "miasuperpassword"

# Decifrare (stessa chiave)
openssl enc -d -aes-256-cbc -in segreto.enc -out recuperato.txt -k "miasuperpassword"
```

## Rilevanza per la sicurezza

- È la base della protezione dei dati a riposo (hard disk cifrati, archivi ZIP protetti da password).
- In [[TLS e SSL]] viene usata per cifrare il traffico web dopo che le chiavi sono state scambiate.
- Un attaccante che riesce a ottenere la chiave simmetrica può decifrare **tutto il traffico** intercettato.
- Algoritmi obsoleti come DES (56 bit) sono stati violati; oggi si usa [[AES]] con chiavi da 128 o 256 bit.

## Lab

- **CryptoHack → sezione *Symmetric Ciphers*** (https://cryptohack.org): parti da *Keyed Permutations* e *Resisting Bruteforce* per capire perché una chiave a 128/256 bit non è forzabile, poi affronta le sfide sul funzionamento interno di un cifrario a blocchi. Ottimo per collegare teoria e pratica.
- **[[OpenSSL]] — pratica locale**: cifra e decifra un file con `openssl enc -aes-256-cbc -pbkdf2` (comando negli esempi) e verifica che, cambiando anche un solo carattere della password, la decifratura fallisce. Dimostra che la sicurezza dipende interamente dal segreto della chiave.
- **PicoCTF → categoria *Cryptography***: sfide che forniscono ciphertext + chiave (o password debole) da recuperare, per praticare il ciclo cifra/decifra simmetrico.

## Domande

1. **D:** Cosa distingue la crittografia simmetrica da quella asimmetrica? **R:** La simmetrica usa la **stessa** chiave per cifrare e decifrare; l'asimmetrica usa una coppia chiave pubblica/privata.
2. **D:** Qual è il problema principale della crittografia simmetrica? **R:** La **distribuzione sicura della chiave**: consegnare la chiave segreta al destinatario senza che venga intercettata.
3. **D:** Come si risolve in pratica il problema della distribuzione della chiave? **R:** Con la [[Crittografia Asimmetrica]] o con protocolli come lo [[Scambio di Chiavi Diffie-Hellman]].
4. **D:** Perché DES non è più considerato sicuro? **R:** Ha una chiave di soli 56 bit, forzabile con la potenza di calcolo moderna; oggi si usa [[AES]] con chiavi da 128 o 256 bit.
5. **D:** Cosa succede se un attaccante ottiene la chiave simmetrica? **R:** Può decifrare tutto il traffico o i dati cifrati con quella chiave.

## Collegamenti

- [[AES]] — l'algoritmo simmetrico standard moderno
- [[Crittografia Asimmetrica]] — alternativa che risolve il problema della distribuzione delle chiavi
- [[Scambio di Chiavi Diffie-Hellman]] — protocollo per accordarsi su una chiave simmetrica in modo sicuro
- [[TLS e SSL]] — usa la crittografia simmetrica per cifrare le sessioni web
- [[03. XOR]] — operazione di base usata internamente da molti cifrari

## Fonti

1. Wikipedia — Symmetric-key algorithm: https://en.wikipedia.org/wiki/Symmetric-key_algorithm
2. Cloudflare Learning — What is symmetric encryption?: https://www.cloudflare.com/learning/ssl/what-is-symmetric-encryption/
3. NIST — Recommendation for Block Cipher Modes: https://csrc.nist.gov/publications/detail/sp/800-38a/final
