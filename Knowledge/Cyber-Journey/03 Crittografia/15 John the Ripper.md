---
tipo: entita
tag: [crypto, tool, offensive]
fase: 1
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["John the Ripper"]

---

# John the Ripper

## In breve

**John the Ripper** (spesso abbreviato in "John" o "JtR") è uno dei tool open-source più storici e usati per il **cracking di password e hash**. A differenza di [[Hashcat]] che predilige la GPU, John è ottimizzato per la **CPU** ed è particolarmente apprezzato per la sua capacità di **rilevare automaticamente** il tipo di hash e per i moduli `*2john` che estraggono hash da file protetti (ZIP, PDF, SSH key, KeePass...).

## Uso tipico

```bash
# Cracking base con wordlist — JtR rileva automaticamente il tipo di hash
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

# Specificare il formato esplicitamente
john hash.txt --format=bcrypt --wordlist=rockyou.txt

# Mostrare le password già crackate
john hash.txt --show

# Estrarre hash da file protetti (moduli *2john)
zip2john archivio.zip > hash_zip.txt
john hash_zip.txt --wordlist=rockyou.txt

pdf2john documento.pdf > hash_pdf.txt
john hash_pdf.txt --wordlist=rockyou.txt

ssh2john id_rsa_protetta > hash_ssh.txt
john hash_ssh.txt --wordlist=rockyou.txt

# Cracking del file /etc/shadow di Linux
unshadow /etc/passwd /etc/shadow > combined.txt
john combined.txt --wordlist=rockyou.txt
```

**Formati hash comuni** (`--format=`):
| Formato | Descrizione |
|---------|-------------|
| `md5crypt` | MD5 con salt (Linux vecchio) |
| `sha512crypt` | SHA-512 con salt (Linux moderno `/etc/shadow`) |
| `NT` | Hash NTLM di Windows |
| `bcrypt` | Bcrypt (password web) |
| `zip` | Archivi ZIP protetti |

## Quando si usa

- **CTF**: per craccare hash trovati nelle sfide, specialmente da file come `/etc/shadow` o archivi protetti.
- **Penetration testing**: dopo aver estratto hash da un sistema compromesso, per recuperare credenziali riutilizzabili.
- **Audit**: verificare che le password degli account rispettino le policy di complessità.
- I moduli `*2john` lo rendono insostituibile quando l'hash è "intrappolato" dentro un file — ZIP, PDF, chiavi SSH.

## Note e trucchi

- John salva il progresso automaticamente: puoi interrompere e riprendere con `john --restore`.
- La versione **Jumbo** (community patch, disponibile su GitHub) supporta molti più formati dell'originale — è quella che trovi su Kali Linux.
- Per vedere tutti i formati supportati: `john --list=formats`
- Premi `invio` durante l'esecuzione per vedere lo stato corrente.
- Per attacchi più veloci su GPU, usa [[Hashcat]]; John è preferibile quando hai bisogno dei moduli `*2john` o lavori senza GPU.
- Documentazione: https://www.openwall.com/john/doc/

## Lab

- **[[TryHackMe]] → room *John The Ripper (The Basics)***: percorso guidato che copre wordlist, formati, `unshadow` e i moduli `*2john` per estrarre hash da ZIP, RSA e altro — la palestra di riferimento per questo tool.
- **Pratica con i moduli `*2john`**: cifra un archivio ZIP con una password da `rockyou.txt`, estrai l'hash con `zip2john archivio.zip > hash.txt` e craccalo con `john hash.txt --wordlist=rockyou.txt`. Ripeti con `ssh2john` su una chiave privata protetta.
- **[[HackTheBox]] → macchine con `/etc/shadow` recuperabile**: usa `unshadow /etc/passwd /etc/shadow > combined.txt` e poi `john --format=sha512crypt` per recuperare credenziali riutilizzabili nel movimento laterale.

## Domande

1. **D:** Qual è la differenza principale tra John the Ripper e [[Hashcat]]? **R:** John è ottimizzato per la CPU e rileva automaticamente il tipo di hash; Hashcat sfrutta la GPU ed è spesso più veloce su hash semplici.
2. **D:** A cosa servono i moduli `*2john` (zip2john, ssh2john, pdf2john)? **R:** Estraggono l'hash "intrappolato" dentro un file protetto (ZIP, chiave SSH, PDF) in un formato che John può poi craccare.
3. **D:** Cosa fa `unshadow` e perché è necessario? **R:** Combina `/etc/passwd` e `/etc/shadow` in un unico file che John può elaborare per craccare le password degli utenti Linux.
4. **D:** Come si riprende una sessione di cracking interrotta? **R:** Con `john --restore`: John salva automaticamente il progresso.
5. **D:** Cos'è la versione *Jumbo* di John? **R:** Una community patch (su GitHub, inclusa in Kali) che aggiunge il supporto a molti più formati rispetto all'originale.

## Collegamenti

- [[Funzioni di Hash]] — cosa sono gli hash che John cerca di invertire
- [[Hashing delle Password e Salting]] — capire il salting spiega perché alcuni hash resistono meglio al cracking
- [[Hashcat]] — alternativa GPU-accelerata, spesso più veloce su hash semplici
- [[Permessi Linux]] — contesto per `/etc/shadow` e i permessi sui file di sistema

## Fonti

1. Openwall — John the Ripper official page: https://www.openwall.com/john/
2. Wikipedia — John the Ripper: https://en.wikipedia.org/wiki/John_the_Ripper
3. Kali Linux Tools — John documentation: https://www.kali.org/tools/john/
