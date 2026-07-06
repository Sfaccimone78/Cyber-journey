---
tipo: entita
tag: [crypto, tool, offensive]
fase: 1
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Hashcat"]

---

# Hashcat

## In breve

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

## Lab

- **[[TryHackMe]] → room *Crack the Hash* / *Hashcat***: fornisce set di hash di tipo diverso (MD5, SHA-1, NTLM, bcrypt) da identificare e crackare con la modalità e la wordlist giuste — palestra diretta per `-m` e `-a`.
- **[[HackTheBox]] → modulo *Password Attacks*** (o macchine con dump credenziali): estrai gli hash, identifica l'algoritmo con `hashcat --identify` e recuperali con `rockyou.txt` + regole (`-r best64.rule`).
- **Pratica locale con `rockyou.txt`**: genera un MD5 di una password comune, craccalo con `hashcat -m 0 -a 0`, poi ripeti su un hash bcrypt (`-m 3200`) e confronta la velocità in hash/s. Dimostra concretamente il legame con [[Hashing delle Password e Salting]].

## Domande

1. **D:** Cosa indicano i flag `-m` e `-a` in Hashcat? **R:** `-m` specifica il tipo di hash (es. 0 = MD5, 1000 = NTLM, 3200 = bcrypt); `-a` la modalità di attacco (0 = wordlist, 1 = combinato, 3 = brute-force/mask).
2. **D:** Perché Hashcat è così veloce? **R:** Sfrutta la GPU, provando miliardi di combinazioni al secondo su hash deboli come MD5.
3. **D:** A cosa serve un file di regole come `best64.rule`? **R:** Applica trasformazioni alle parole della wordlist (maiuscole, numeri in fondo, sostituzioni) per generare varianti realistiche senza brute-force cieco.
4. **D:** Cos'è il potfile di Hashcat? **R:** Il file `~/.hashcat/hashcat.potfile` dove salva gli hash già crackati, riutilizzandoli automaticamente nelle sessioni successive.
5. **D:** Perché bcrypt (`-m 3200`) è molto più lento da attaccare di MD5 (`-m 0`)? **R:** Bcrypt è una funzione deliberatamente lenta e salata, pensata per le password; MD5 è veloce e non progettato per resistere al cracking.

## Collegamenti

- [[Funzioni di Hash]] — cosa sono gli hash che Hashcat cerca di invertire
- [[Hashing delle Password e Salting]] — perché bcrypt/Argon2 rendono il cracking molto più lento
- [[John the Ripper]] — alternativa CPU-based per il cracking
- [[Encoding vs Encryption]] — l'hashing non è encryption, ma Hashcat non serve per cifratura

## Fonti

1. Hashcat — Sito ufficiale e wiki: https://hashcat.net/wiki/
2. Wikipedia — Hashcat: https://en.wikipedia.org/wiki/Hashcat
3. OWASP — Testing for Weak Cryptography: https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/
