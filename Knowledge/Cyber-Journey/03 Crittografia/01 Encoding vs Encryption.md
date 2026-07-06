---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Encoding vs Encryption"]

---

# Encoding vs Encryption

## In breve

**Encoding** e **Encryption** sono due operazioni completamente diverse, spesso confuse tra loro. L'encoding converte dati in un formato diverso per ragioni di **compatibilità** — chiunque può decodificarli. L'encryption li rende illeggibili senza la **chiave segreta**. Confonderli è un errore di sicurezza grave: usare Base64 per "nascondere" una password non la protegge affatto.

## Come funziona

| Proprietà | Encoding | Encryption | Hashing |
|-----------|----------|------------|---------|
| Scopo | Compatibilità/trasporto | Riservatezza | Integrità/verifica |
| Reversibile? | Sì, sempre | Sì, con la chiave | No (a senso unico) |
| Segreto? | No | Sì (la chiave) | No |
| Esempi | [[01. Base64]], URL encoding, UTF-8 | AES, RSA | SHA-256, MD5 |

**Encoding**: trasforma bit in un altro formato (es. binario → testo ASCII) usando uno schema pubblico e fisso. Non c'è segreto: chiunque conosce lo schema può invertire l'operazione.

**Encryption**: usa un algoritmo + una chiave segreta. Senza la chiave, i dati cifrati sono incomprensibili. Esistono due grandi categorie: [[Crittografia Simmetrica]] (stessa chiave per cifrare/decifrare) e [[Crittografia Asimmetrica]] (coppia chiave pubblica/privata).

**Hashing** (per completezza): trasformazione a senso unico. Non è né encoding né encryption — vedi [[Funzioni di Hash]].

## Esempio pratico

```bash
# ENCODING: Base64 — reversibile, nessun segreto
echo -n "password123" | base64
# cGFzc3dvcmQxMjM=

echo "cGFzc3dvcmQxMjM=" | base64 -d
# password123  ← chiunque può decodificarlo!

# ENCRYPTION: AES-256 — richiede la chiave
openssl enc -aes-256-cbc -pbkdf2 -in segreto.txt -out segreto.enc -k miachiave

openssl enc -aes-256-cbc -pbkdf2 -d -in segreto.enc -out segreto.txt -k miachiave
# Solo chi ha 'miachiave' può decifrare
```

## Rilevanza per la sicurezza

- **Bug comune**: sviluppatori che usano Base64 come "protezione" — non è sicurezza, è solo encoding.
- **CTF e analisi malware**: riconoscere encoding (Base64, hex, URL encoding) è fondamentale per decodificare payload e dati nascosti. Tool utile: [[CyberChef]].
- **HTTPS**: usa encryption (TLS), non encoding, per proteggere il traffico.

## Lab

- **CryptoHack → sezione *Introduction / General → Encoding*** (https://cryptohack.org): le sfide `ASCII`, `Hex`, `Base64`, `Bytes and Long` insegnano a riconoscere e convertire i vari encoding. Sono il punto di partenza ideale per non confondere trasformazione di formato e cifratura.
- **[[CyberChef]] — pratica libera**: incolla una stringa Base64 e usa la ricetta *From Base64* per verificare che nessuna chiave sia richiesta; poi confronta con *AES Encrypt/Decrypt* per toccare con mano la differenza (l'AES fallisce senza la chiave corretta, il Base64 no).
- **PicoCTF → categoria *Cryptography* (livello base)**: sfide come *Mod 26* e le challenge di decoding chiedono di riconoscere l'encoding prima di tentare la "decifratura" — esercizio classico sul distinguere i due concetti.

## Domande

1. **D:** Perché usare Base64 per "nascondere" una password è un errore di sicurezza? **R:** Perché Base64 è solo encoding: usa uno schema pubblico e reversibile senza segreto, quindi chiunque può decodificarlo con `base64 -d`. Non fornisce alcuna riservatezza.
2. **D:** Quale proprietà distingue l'encryption dall'encoding? **R:** L'encryption richiede una chiave segreta: senza di essa i dati sono incomprensibili. L'encoding non ha alcun segreto.
3. **D:** L'hashing è reversibile come l'encoding? **R:** No, l'hashing è una trasformazione a senso unico e non è né encoding né encryption; serve a integrità/verifica.
4. **D:** In un'analisi malware, perché è importante riconoscere Base64 o hex? **R:** Perché i payload sono spesso solo codificati (non cifrati): riconoscere l'encoding permette di decodificarli direttamente senza bisogno di alcuna chiave.
5. **D:** HTTPS protegge il traffico con encoding o encryption? **R:** Con encryption (TLS), non con encoding.

## Collegamenti

- [[01. Base64]] — esempio classico di encoding
- [[03. XOR]] — operazione base usata in alcuni schemi di encoding/cifratura debole
- [[Crittografia Simmetrica]] — encryption con chiave condivisa
- [[Crittografia Asimmetrica]] — encryption con chiave pubblica/privata
- [[Funzioni di Hash]] — la terza categoria, spesso confusa con le prime due
- [[CyberChef]] — tool per manipolare encoding in modo visuale

## Fonti

1. Cloudflare Learning — Encryption vs. Encoding: https://www.cloudflare.com/learning/ssl/what-is-encryption/
2. OWASP — Cryptographic Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
3. Wikipedia — Character encoding: https://en.wikipedia.org/wiki/Character_encoding
