---
tipo: entita
tag: [crypto, tool, offensive]
fase: 1
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Hashcat"]

---

# Hashcat

## Cos'è

**Hashcat** è il tool open-source più veloce e diffuso per il **cracking di hash crittografici**. Dato un hash (es. di una password), tenta di trovare l'input originale tramite dizionari, regole, o forza bruta. Sfrutta la GPU per una velocità enorme: può provare miliardi di combinazioni al secondo su hash deboli come MD5.

## Uso tipico

```bash
# Sintassi base
hashcat -m <tipo_hash> -a <modalita_attacco> <file_hash> <wordlist>

# Cracking di un hash MD5 con wordlist (rockyou.txt)
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt

# Attacco con regole (aggiunge varianti: maiuscole, numeri in fondo...)
hashcat -m 0 -a 0 hash.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Brute-force su hash NTLM (Windows) — solo 6 caratteri alfanumerici
hashcat -m 1000 -a 3 hash.txt ?a?a?a?a?a?a

# Attacco combinato: due wordlist unite
hashcat -m 0 -a 1 hash.txt lista1.txt lista2.txt

# Identificare il tipo di hash (con hashid o --identify)
hashcat --identify hash.txt
```

**Tipi di hash comuni** (`-m`):
| Codice | Tipo |
|--------|------|
| 0 | MD5 |
| 100 | SHA-1 |
| 1400 | SHA-256 |
| 1000 | NTLM (Windows) |
| 1800 | sha512crypt (Linux /etc/shadow) |
| 3200 | bcrypt |
| 13400 | KeePass |

## Quando si usa

- **CTF**: quando si trovano hash da decifrare in sfide di crittografia o forensics.
- **Penetration testing**: dopo aver ottenuto il database delle password (o il file `/etc/shadow`), si tentano di recuperare le credenziali.
- **Audit di sicurezza**: verificare che le password degli utenti rispettino le policy aziendali.
- Concettualmente legato a [[Hashing delle Password e Salting]] — capire il salting spiega perché bcrypt (`-m 3200`) è ordini di grandezza più lento di MD5 (`-m 0`).

## Note e trucchi

- Hashcat mostra lo stato in tempo reale: premi `s` durante l'esecuzione per il riepilogo, `q` per uscire.
- Il file `hash.txt` deve contenere un hash per riga (senza spazi aggiuntivi).
- Se non hai una GPU potente, usa [[John the Ripper]] come alternativa CPU-friendly.
- La wordlist **rockyou.txt** (14 milioni di password reali da un breach del 2009) è il punto di partenza standard.
- Hash già crackati vengono salvati nel file `~/.hashcat/hashcat.potfile` — riutilizzati automaticamente nelle sessioni successive.
- Documentazione ufficiale: https://hashcat.net/wiki/

## Collegamenti

- [[Funzioni di Hash]] — cosa sono gli hash che Hashcat cerca di invertire
- [[Hashing delle Password e Salting]] — perché bcrypt/Argon2 rendono il cracking molto più lento
- [[John the Ripper]] — alternativa CPU-based per il cracking
- [[Encoding vs Encryption]] — l'hashing non è encryption, ma Hashcat non serve per cifratura

## Fonti

1. Hashcat — Sito ufficiale e wiki: https://hashcat.net/wiki/
2. Wikipedia — Hashcat: https://en.wikipedia.org/wiki/Hashcat
3. OWASP — Testing for Weak Cryptography: https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/
