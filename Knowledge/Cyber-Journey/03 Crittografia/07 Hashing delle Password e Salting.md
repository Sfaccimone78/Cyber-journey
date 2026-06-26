---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 4
aggiornato: 2026-06-20
stato: maturo
aliases: ["Hashing delle Password e Salting"]

---

# Hashing delle Password e Salting

## In breve

Quando un sito memorizza la tua password, non la salva in chiaro: la trasforma in un **hash** usando una [[Funzioni di Hash|funzione di hash]]. Così, anche se il database viene rubato, l'attaccante non vede le password. Il **salting** aggiunge un valore casuale unico prima di fare l'hash, rendendo molto più difficile craccare le password anche con tabelle precompilate.

## Come funziona

**Senza salt** — problema delle Rainbow Tables:

Se due utenti scelgono la stessa password, producono lo stesso hash. Un attaccante può precomputare una "rainbow table" con milioni di hash noti e trovare immediatamente la corrispondenza.

**Con salt** — soluzione moderna:

1. Al momento della registrazione, si genera un **salt** casuale (es. 16 byte) unico per ogni utente.
2. Si calcola `hash(password + salt)`.
3. Il database memorizza: `salt` + `hash`.
4. Al login, si recupera il salt, si ricalcola `hash(password_inserita + salt)` e si confronta.

**Algoritmi raccomandati** per l'hashing delle password (lenti per design):
| Algoritmo | Note |
|-----------|------|
| bcrypt | Standard consolidato, include il salt |
| Argon2 | Vincitore Password Hashing Competition 2015, raccomandato da OWASP |
| scrypt | Resistente ad attacchi hardware |
| PBKDF2 | Approvato NIST, usato in molti standard |

SHA-256 da solo non basta: è troppo veloce, facilitando gli attacchi brute-force.

## Esempio pratico

```bash
# Generare un hash bcrypt con OpenSSL (via Python in un one-liner)
python3 -c "import bcrypt; print(bcrypt.hashpw(b'password123', bcrypt.gensalt()))"
# b'$2b$12$exSalt...hashedOutput...'

# Verifica: Hashcat può tentare di craccare hash MD5 non salati
hashcat -m 0 -a 0 hash.txt wordlist.txt
# Con bcrypt (-m 3200) è enormemente più lento

# Esempio salt manuale con openssl (per capire il concetto)
SALT=$(openssl rand -hex 16)
echo -n "password123${SALT}" | openssl dgst -sha256
```

## Rilevanza per la sicurezza

- **Data breach**: quando un database viene esfiltrato, hashing + salting protegge gli utenti da una compromissione immediata delle password.
- **Credential stuffing**: password uniche e salt diversi limitano l'impatto.
- **Tool di attacco**: [[Hashcat]] e [[John the Ripper]] sono usati dai penetration tester per verificare la robustezza degli hash.
- **Errore comune**: usare MD5 o SHA-1 senza salt — ancora diffuso in sistemi legacy.

## Collegamenti

- [[Funzioni di Hash]] — il meccanismo base sottostante
- [[Hashcat]] — tool per craccare hash di password
- [[John the Ripper]] — alternativa per il cracking di hash
- [[Encoding vs Encryption]] — l'hashing non è né encoding né encryption
- [[CryptoHack - Mathematics (Modular Math)]] — fondamenti matematici della crittografia

## Fonti

1. OWASP — Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
2. Wikipedia — Bcrypt: https://en.wikipedia.org/wiki/Bcrypt
3. NIST — SP 800-63B (Digital Identity Guidelines): https://pages.nist.gov/800-63-3/sp800-63b.html
4. Cloudflare Learning — What is password hashing?: https://www.cloudflare.com/learning/ssl/what-is-hashing/
