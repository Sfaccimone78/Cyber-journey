---
tipo: entita
tag: [tool]
fase: 2
fonti: 7
aggiornato: 2026-07-02
stato: maturo
aliases: ["Nmap"]
---

# Nmap

## In breve
**Nmap** (Network Mapper) è lo scanner di rete open source di riferimento: scopre host attivi, porte aperte, servizi e versioni, OS, e con gli script **NSE** esegue enumerazione e controlli di vulnerabilità. Preinstallato su [[Kali Linux]], è il primo strumento della [[Scansione delle Porte]] e dell'[[Enumerazione]].

> **Nota etica**: solo su sistemi autorizzati. Scansionare host altrui senza permesso è reato in molte giurisdizioni.

## Metodologia in 5 fasi
1. **Host discovery** — chi è vivo? `nmap -sn 10.10.10.0/24` (ping sweep).
2. **Port scan** — quali porte aperte? `-sS`/`-sT`, `-p-` per tutte.
3. **Service/version** — cosa gira e che versione? `-sV`.
4. **NSE + OS** — approfondimento: `-sC`, script mirati, `-O`.
5. **Documentazione** — `-oA` per salvare e riusare.

## Tipi di scansione (e perché)
| Flag | Scan | Note |
|---|---|---|
| `-sS` | SYN / half-open | invia SYN, non completa l'handshake → più **stealth** e veloce; richiede **root** (raw socket) |
| `-sT` | TCP connect | handshake completo via OS; **no root**, ma più rumoroso e loggato |
| `-sU` | UDP | lento (no handshake, si basa su timeout/ICMP) ma scopre DNS, SNMP, DHCP |
| `-sA` | ACK | mappa regole firewall (filtered vs unfiltered) |
| `-sn` | ping scan | solo host discovery, nessuna porta |

`-sS` e `-sT` danno lo stesso risultato sulle porte: la differenza è **come** sondano. Su un target che blocca il ping, aggiungi **`-Pn`** (tratta l'host come up, salta la discovery) — errore tipico è "nessuna porta aperta" solo perché l'ICMP è filtrato.

## Uso tipico
```bash
# Discovery di rete
nmap -sn 10.10.10.0/24

# Scan veloce iniziale (top 1000) con versioni + script default
nmap -sC -sV 10.10.10.5

# TUTTE le porte TCP, poi -sV mirato sulle aperte (workflow CTF)
nmap -p- --min-rate 5000 10.10.10.5            # trova le aperte in fretta
nmap -p22,80,445 -sC -sV 10.10.10.5            # approfondisci solo quelle

# UDP top 20
sudo nmap -sU --top-ports 20 10.10.10.5

# Aggressiva (OS + version + script default + traceroute)
nmap -A -T4 10.10.10.5

# Salva in tutti i formati (per report / import)
nmap -sC -sV -oA scan_iniziale 10.10.10.5
```

## NSE — gli script che fanno il lavoro vero
Stanno in `/usr/share/nmap/scripts/`. Categorie: `default` (`-sC`), `discovery`, `auth`, `vuln`, `safe`, `exploit`, `brute`.
```bash
# Enumerazione SMB (utenti, share, OS)
nmap --script smb-enum-shares,smb-enum-users,smb-os-discovery -p445 10.10.10.5

# HTTP: directory, titolo, metodi, header
nmap --script http-enum,http-title,http-methods -p80,443 10.10.10.5

# FTP anonimo
nmap --script ftp-anon -p21 10.10.10.5

# Check vulnerabilità note (ms17-010 EternalBlue, ecc.)
nmap --script vuln -p- 10.10.10.5
```

## Tuning e evasione (lab autorizzati)
- **Timing**: `-T0`..`-T5` (0 lentissimo/evasivo, 4 default aggressivo CTF, 5 può perdere porte). Controllo fine: `--min-rate`, `--max-retries`.
- **`-sV --version-intensity 0..9`**: più alto = più probe, più preciso, più lento.
- **Evasione IDS/firewall**: `-f` (frammenta), `--mtu`, `-D RND:10` (decoy), `--source-port 53`, `--data-length`. Da usare solo con autorizzazione.

## Output e integrazione
- `-oA nome` → `nome.nmap` (umano), `nome.gnmap` (grepable), `nome.xml`.
- Import in [[Metasploit]]: `db_import nome.xml` in `msfconsole`.
- Per scan iniziali ultra-rapidi molti usano **RustScan** (trova le porte) e poi passano la lista a Nmap `-sV -sC`.

## Errori comuni
- Dimenticare `-p-`: la scan default copre solo 1000 porte → servizi su porte alte (es. 8080, 31337) sfuggono.
- Non usare `-Pn` su host che bloccano il ping → falsi "host down".
- Lanciare `-sU -p-` (UDP su 65535 porte): impiega ore. Limita con `--top-ports`.

---

## MECCANISMO INTERNO — ogni scan type a livello pacchetto

Tutto si fonda sul [[Three-Way Handshake TCP]] (SYN → SYN/ACK → ACK) e sull'interpretazione delle **flag TCP** (SYN, ACK, RST, FIN, PSH, URG). Nmap manda pacchetti malformati o parziali e **deduce** lo stato della porta dalla risposta (o dalla sua assenza).

| Scan | Cosa manda | Porta APERTA risponde | Porta CHIUSA risponde | Filtrata (firewall) |
|---|---|---|---|---|
| **`-sS` SYN** | `SYN` | `SYN/ACK` (Nmap manda `RST`, non completa) | `RST` | nessuna risposta / ICMP unreachable |
| **`-sT` Connect** | handshake completo via syscall `connect()` | handshake completo poi chiude | `RST` | timeout |
| **`-sA` ACK** | `ACK` | `RST` (**unfiltered**) | `RST` (**unfiltered**) | nessuna risposta = **filtered** |
| **`-sF` FIN** | `FIN` | **nessuna risposta** (open\|filtered) | `RST` | nessuna risposta |
| **`-sN` NULL** | nessuna flag | **nessuna risposta** | `RST` | nessuna risposta |
| **`-sX` Xmas** | `FIN+PSH+URG` | **nessuna risposta** | `RST` | nessuna risposta |

> [!info] La logica dietro FIN/NULL/Xmas
> Lo standard RFC 793 dice: se arriva un segmento senza `SYN/RST/ACK` a una porta **chiusa**, rispondi `RST`; a una porta **aperta**, **ignora**. Nmap sfrutta questa regola: silenzio = aperta-o-filtrata, `RST` = chiusa. Funziona solo su stack conformi all'RFC: **Windows, Cisco, BSD recenti rispondono SEMPRE `RST`** → tutte le porte appaiono "chiuse" e lo scan è inutile. Utile solo contro Linux/Unix e per superare firewall stateless che filtrano solo i `SYN` entranti.

- **`-sA` (ACK) non trova porte aperte** — non è il suo scopo. Mappa il firewall: distingue `filtered` (stateful, droppa) da `unfiltered` (lascia passare). È diagnostica di rete, non di servizio.
- **`-sU` (UDP)**: niente handshake. Porta chiusa → `ICMP port unreachable` (type 3 code 3); porta aperta → di solito **silenzio** (open\|filtered). Da qui la lentezza: Nmap deve attendere i timeout e l'ICMP è rate-limited dal kernel Linux (1/s) → uno scan UDP `-p-` può durare giorni.
- **`-sV` (version)**: dopo aver trovato la porta aperta, apre una connessione completa e invia **probe** dal file `nmap-service-probes`, confrontando le risposte (banner) con migliaia di signature. `--version-intensity 0-9` regola quante probe inviare.

## NSE — anatomia di uno script

Gli script sono in **Lua**, vivono in `/usr/share/nmap/scripts/`, indicizzati in `script.db`. Ogni script dichiara:
```lua
description = "..."           -- cosa fa
categories = {"vuln","safe"}  -- in quali categorie rientra
portrule = function(host, port)            -- QUANDO girare (es. port.number==445)
  return port.number == 445 and port.protocol == "tcp"
end
action = function(host, port)              -- COSA fare quando portrule è true
  -- invia richieste, parsa risposte, ritorna output
end
```
Categorie chiave: `safe` (non invasivi), `intrusive` (possono crashare il servizio), `vuln` (test CVE), `exploit` (tentano sfruttamento), `brute` (password guessing), `auth`, `discovery`, `default` (= `-sC`).
```bash
nmap --script "smb-vuln-*" -p445 10.10.10.5      # wildcard per famiglia
nmap --script "vuln and safe" 10.10.10.5         # espressione booleana tra categorie
nmap --script http-enum --script-args http-enum.basepath=/api/ -p80 10.10.10.5  # argomenti
nmap --script-updatedb                           # rigenera script.db dopo aver aggiunto script
```
> [!warning] `--script vuln` e `--script exploit` sono RUMOROSI e a volte distruttivi
> Categoria `intrusive`/`exploit` può mandare in crash servizi fragili (vecchi SMB, stampanti, SCADA/ICS). In produzione o su asset delicati limitati a `safe`. `--script vuln` genera traffico anomalo che un IDS segnala immediatamente.

## CASI LIMITE E VARIANTI
- **Host che bloccano ICMP** → `-Pn` (salta la discovery, tratta tutto come up). Senza, Nmap dichiara l'host "down" e non scansiona nulla.
- **`-sS` senza root** → Nmap ripiega automaticamente su `-sT` (Connect) perché i raw socket richiedono privilegi.
- **`--reason`** → mostra *perché* Nmap ha classificato così la porta (`syn-ack`, `reset`, `no-response`): essenziale per il debug.
- **`-6`** per target IPv6; molti firewall sono configurati solo per IPv4 → percorso d'attacco trascurato.
- **`--top-ports N`** usa la frequenza statistica del file `nmap-services`, non le prime N porte numeriche.

## WALKTHROUGH END-TO-END — una /24
```bash
# 1. Chi è vivo? (ping sweep, niente port scan) — salva solo gli IP up
nmap -sn 10.10.10.0/24 -oG - | awk '/Up$/{print $2}' > live.txt

# 2. Scan SYN veloce di TUTTE le porte sugli host vivi
nmap -sS -p- --min-rate 2000 -iL live.txt -oA 02_fullports

# 3. Estrai coppie host:porta aperte e approfondisci SOLO quelle (version + script default)
nmap -sC -sV -p22,80,445 10.10.10.5 -oA 03_deep_10.10.10.5

# 4. UDP mirato (i servizi UDP più ghiotti: SNMP, DNS, TFTP, IKE)
sudo nmap -sU --top-ports 50 -iL live.txt -oA 04_udp

# 5. Vuln scan mirato dove ha senso (es. SMB esposto)
nmap --script "smb-vuln-*" -p445 10.10.10.5 -oA 05_smbvuln
```
Principio: **discovery larga e veloce → enumerazione profonda e mirata**. Mai `-A -p-` sull'intera /24 al primo colpo: spreca ore e satura l'IDS.

## EVASION / OPSEC (solo lab autorizzati)
| Tecnica | Flag | Limite reale |
|---|---|---|
| Timing lento | `-T0`/`-T1`, `--scan-delay 5s` | `-T0` può richiedere **giorni** per una /24; pratico solo per poche porte |
| Frammentazione | `-f` (frammenti da 8 byte), `--mtu 16` | IDS moderni e firewall **riassemblano** i frammenti → spesso inefficace |
| Decoy | `-D RND:10` o `-D ip1,ip2,ME,ip3` | nasconde la sorgente reale tra esche, ma `-sV`/NSE usano comunque il tuo IP reale; decoy down possono causare SYN-flood |
| Spoofing porta sorgente | `--source-port 53` / `-g 53` | supera firewall che fidano del traffico "da DNS"; inefficace su firewall stateful |
| Lunghezza dati casuale | `--data-length 25` | altera la dimensione del pacchetto per eludere signature basate sulla size |
| Spoof IP sorgente | `-S <ip>` | non ricevi le risposte (cieco) salvo che controlli quel segmento |

> [!warning] L'evasione moderna è in gran parte teatro
> Contro un NGFW/IDS aggiornato (Suricata, Palo Alto) frammentazione e decoy sono per lo più neutralizzati. Il vero stealth è **andare piano e mimetizzarsi nel traffico legittimo** (`-T1`, poche porte, source-port 443). In esame/CTF l'evasione conta poco; in un red team reale serve calibrarla con il cliente.

## DETECTION ENGINEERING — come appare in IDS/log
- **SYN scan (`-sS`)**: molti SYN verso porte diverse senza ACK finale → tante connessioni half-open. Suricata: `ET SCAN Nmap Scripting Engine User-Agent`, `ET SCAN Potential SYN scan`. Firewall log: raffica di SYN da un solo IP su molte porte in pochi secondi.
- **Connect scan (`-sT`)**: handshake completi che si chiudono subito → compaiono nei log applicativi (Apache `access.log`, auth.log) come connessioni immediate. Più loggato del SYN.
- **NSE `http-*`**: User-Agent di default contiene `Nmap Scripting Engine` → firma banale per un WAF.
- **MITRE ATT&CK**: `T1046` Network Service Discovery, `T1595.001` Active Scanning: Scanning IP Blocks, `T1018` Remote System Discovery.
- Pattern rilevatore generico: *N connessioni a >M porte distinte dallo stesso IP entro T secondi* (port-scan detection di Snort/Suricata, `sfportscan`).

## NMAP PER IL DIFENSORE (blue team)
Nmap non è solo offensivo: il difensore lo usa per **conoscere la propria superficie d'attacco** prima
che lo faccia un attaccante (vedi [[Superficie di Attacco]]).
- **Asset inventory / audit**: scansiona le tue reti per scoprire host e servizi *non previsti*
  (shadow IT, porte aperte per errore, servizi di gestione esposti). `nmap -sV -p- 10.0.0.0/24 -oA audit`.
- **Caccia ai servizi rogue**: confronta lo stato attuale con una baseline. **`ndiff`** mostra cosa è
  cambiato fra due scansioni → una porta nuova = possibile backdoor o misconfigurazione.
  ```bash
  nmap -sV -oX oggi.xml 10.0.0.0/24
  ndiff ieri.xml oggi.xml          # evidenzia host/porte/servizi comparsi o spariti
  ```
- **Verifica patch/hardening**: dopo una remediation, ri-scansiona per confermare che la porta sia
  chiusa o il servizio aggiornato (`-sV` mostra la nuova versione).
- **Monitoraggio schedulato**: uno scan `ndiff` periodico (cron) è un rilevatore di cambiamenti
  low-cost; le differenze vanno al [[SIEM]] come evento.
- **Attenzione**: scansionare la *propria* produzione può comunque far scattare l'IDS o stressare
  servizi fragili → coordina con il SOC e usa `safe` per gli script (vedi warning su `--script vuln`).

> Specularmente, **rilevare** uno scan Nmap fatto da un attaccante è coperto sotto
> *Detection engineering* qui sopra, e l'analisi del pcap dello scan in [[Wireshark]].

## TROUBLESHOOTING (5 errori + causa)
1. **"All 1000 ports filtered" / host "down"** → l'host droppa ICMP. Causa: discovery fallita. Fix: `-Pn`.
2. **Scan lentissimo su UDP** → ICMP rate-limit del kernel + timeout. Fix: `--top-ports`, `--max-retries 1`, non fare `-sU -p-`.
3. **Tutte le porte "chiuse" con `-sF/-sN/-sX`** → target è Windows/Cisco (non RFC-compliant). Fix: usa `-sS`/`-sT`.
4. **`-sS` dà gli stessi risultati di `-sT` ma "You requested a scan type which requires root"** → manca `sudo`; Nmap è ripiegato su Connect silenziosamente. Fix: `sudo`.
5. **Servizio noto non rilevato / versione sbagliata** → `-sV` con intensità bassa o servizio su porta non standard. Fix: `-sV --version-intensity 9`, `--allports`, e verifica con `-p-`.

## DOMANDE DA COLLOQUIO
1. **Differenza tra `-sS` e `-sT`, e perché uno richiede root?** `-sS` costruisce pacchetti SYN grezzi (raw socket → privilegi root) e non completa l'handshake (half-open, più stealth). `-sT` usa la syscall `connect()` dell'OS (no privilegi) ma completa il three-way handshake, risultando più lento e più loggato.
2. **Perché FIN/NULL/Xmas non funzionano contro Windows?** Si basano sul comportamento RFC 793 (porta chiusa → `RST`, aperta → silenzio). Lo stack Windows risponde `RST` a *qualsiasi* probe verso porte chiuse e aperte, rendendo indistinguibili gli stati.
3. **A cosa serve `-sA` se non trova porte aperte?** A mappare il firewall: distingue porte `filtered` (nessuna risposta = firewall stateful) da `unfiltered` (`RST`). È ricognizione delle regole, non dei servizi.
4. **Come renderesti uno scan più silenzioso e quanto è efficace?** Rallentando (`-T1`, `--scan-delay`), riducendo le porte, usando `--source-port 443`. Frammentazione e decoy contro IDS moderni sono per lo più inefficaci (riassemblaggio); il fattore vero è il volume/velocità del traffico.

## Lab
- **[[TryHackMe]] — "Nmap" (furthernmap)**: la room di riferimento per allenare tutti i tipi di scansione, `-sV`, NSE e l'interpretazione degli stati porta; ripercorre esattamente i flag di questa nota.
- **[[TryHackMe]] — "Nmap Live Host Discovery"**: dedicata alla fase 1 (host discovery) con ARP/ICMP/`-sn` e all'uso di `-Pn`.
- **[[HackTheBox]] — Starting Point**: applica il workflow "discovery larga → enum profonda mirata" (`-p-` per trovare le porte, poi `-sC -sV` sulle aperte) su macchine reali.

## Collegamenti
- [[Scansione delle Porte]]
- [[Enumerazione]]
- [[Ricognizione (Recon)]]
- [[Metasploit]]
- [[Kali Linux]]
- [[Porte e Protocolli Comuni]]
- [[Three-Way Handshake TCP]] — base del SYN scan `-sS`
- [[Wireshark]] — vedere/rilevare uno scan a livello pacchetto; recon **passivo** vs attivo
- [[Superficie di Attacco]] — ciò che lo scan misura, lato difensore
- [[MITRE ATT&CK]]

## Fonti
- Nmap Reference Guide (ufficiale): https://nmap.org/book/man.html
- Nmap NSE Documentation: https://nmap.org/nsedoc/
- Nmap — Firewall/IDS Evasion and Spoofing: https://nmap.org/book/man-bypass-firewalls-ids.html
- Nmap — Port Scanning Techniques: https://nmap.org/book/man-port-scanning-techniques.html
- HackTricks — Nmap cheatsheet: https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/nmap-cheatsheet-nmap-scanning
- TryHackMe — Nmap: https://tryhackme.com/room/furthernmap
- MITRE ATT&CK — Network Service Discovery (T1046): https://attack.mitre.org/techniques/T1046/
