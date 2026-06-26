---
tipo: entita
tag: [reti, tool, blue-team]
fase: 1
fonti: 5
aggiornato: 2026-06-26
stato: maturo
aliases: ["Wireshark", "tshark", "Anatomia di un Pacchetto (Wireshark)"]
---

# Wireshark

> **Nota etica**: catturare traffico significa leggere comunicazioni altrui. Fallo **solo** sulla tua
> rete, in lab, CTF o pentest autorizzato. Lo sniffing di una rete di terzi (es. Wi-Fi pubblico) per
> raccogliere credenziali è intercettazione illecita, reato in quasi ogni giurisdizione.

## Cos'è
**Wireshark** è l'analizzatore di traffico (packet sniffer) open source più diffuso: cattura i
pacchetti su un'interfaccia e li **decodifica protocollo per protocollo**, mostrando l'intero stack
([[Modello OSI]]) di ogni pacchetto. È lo strumento per *vedere* davvero come funzionano [[TCP]],
[[ARP]], [[DNS]], [[HTTP e HTTPS|HTTP]] — ed è a **doppio uso**: l'attaccante lo usa per rubare
credenziali e mappare la rete, il difensore per la **network forensics** e la caccia agli attacchi nei
`.pcap`. `tshark` è la sua versione CLI (stessi filtri, scriptabile).

## Il prerequisito che tutti dimenticano: la POSIZIONE
Wireshark vede solo il traffico che **arriva alla tua scheda**. Su uno **switch** vedi solo il *tuo*
traffico (lo switch inoltra i frame solo alla porta giusta). Per vedere quello altrui servono:
- **Port mirroring / SPAN** o un **TAP** (difesa: posizione legittima sullo switch/router).
- Un [[Man-in-the-Middle (MITM)]] attivo — tipicamente [[ARP|ARP spoofing]] — per dirottare il
  traffico verso di te (attacco).
- In **Wi-Fi**: *monitor mode* + giusto canale per vedere il traffico radio altrui.

Senza una di queste, su una rete switchata cattureresti solo broadcast e il tuo traffico. È il primo
motivo per cui "non vedo niente di interessante".

## Capture filter vs Display filter (la distinzione chiave)
- **Capture filter** (sintassi **BPF**, *prima* della cattura): decide cosa salvare, non si cambia a
  posteriori. Es. `tcp port 80`, `host 10.0.0.5`. Riduce il volume su catture lunghe.
- **Display filter** (sintassi **Wireshark**, *dopo*): filtra ciò che già hai, reversibile. Es.
  `http.request.method == "POST"`. È quello che userai il 90% del tempo.
```text
# Capture (BPF)            # Display (Wireshark)
tcp port 443              tcp.port == 443
host 10.0.0.5             ip.addr == 10.0.0.5
not arp                   http or dns
```

## Display filter di base (la cassetta degli attrezzi)
```text
ip.addr == 192.168.1.10              # un host (sorgente O destinazione)
tcp.port == 445 && ip.addr==10.0.0.5 # combinazioni con && / || / !
tcp.flags.syn==1 && tcp.flags.ack==0 # solo SYN iniziali (nuove connessioni)
tcp.analysis.retransmission          # ritrasmissioni (rete o scan rumoroso)
http.request.method == "POST"        # invii dati / login
dns.flags.response == 0              # solo query DNS
frame contains "password"            # ricerca grezza di byte nel payload
tcp.stream eq 3                      # isola un'intera conversazione TCP per numero
```

---

# USO OFFENSIVO (attacco)

## 1. Furto di credenziali in chiaro
I protocolli legacy non cifrano: username e password viaggiano in chiaro. Wireshark li estrae con due
mosse — un display filter per trovarli, poi **Follow → TCP/HTTP Stream** (tasto destro) per leggere
l'intera conversazione ricostruita.
```text
ftp.request.command == "USER" || ftp.request.command == "PASS"   # FTP: user e pass espliciti
telnet                                                            # Telnet: tutto in chiaro, Follow Stream
http.authorization                                               # HTTP Basic Auth (Base64 → si decodifica)
http.request.method == "POST" && frame contains "pass"           # login web via POST
pop || imap || smtp                                              # mail legacy: AUTH in chiaro
```
`tshark` headless per estrarre solo i campi utili:
```bash
# Tutte le coppie user/pass FTP da un pcap
tshark -r cattura.pcap -Y 'ftp.request.command=="USER" || ftp.request.command=="PASS"' \
       -T fields -e ftp.request.arg
# Host + URI di ogni richiesta HTTP (mappa cosa visita la vittima)
tshark -r cattura.pcap -Y http.request -T fields -e http.host -e http.request.uri
```
> Difesa implicita: questo è **il** motivo per cui FTP/Telnet/HTTP vanno sostituiti con SFTP/SSH/HTTPS
> ([[TLS e SSL]]). Su HTTPS vedi solo metadati (SNI, dimensioni), non le credenziali.

## 2. Session hijacking — rubare cookie e token
Sul traffico HTTP in chiaro, i **cookie di sessione** viaggiano in ogni richiesta. Catturato il cookie,
l'attaccante lo reinietta nel proprio browser e diventa la vittima senza password.
```text
http.cookie                          # cookie nelle richieste
http.set_cookie                      # cookie emessi dal server (login)
http contains "Authorization: Bearer" # token JWT/OAuth in chiaro
```
Mitigazione lato server: flag **`Secure`** (solo HTTPS) e **`HttpOnly`** sui cookie (vedi
[[Cookie e JWT]]); senza HTTPS il furto è banale.

## 3. Estrazione di file e malware dal pcap
`File → Export Objects → HTTP` (o SMB, FTP-DATA, TFTP) tira fuori **ogni file trasferito**: immagini,
documenti, eseguibili. Offensivo (esfiltri ciò che la vittima ha scaricato) e difensivo (recuperi il
sample di malware da analizzare — vedi [[Analisi Malware di Base]]).
```bash
# Estrai tutti gli oggetti HTTP da CLI
tshark -r cattura.pcap --export-objects http,./oggetti_estratti/
```

## 4. Wi-Fi: catturare l'handshake WPA2 per il cracking
Wireshark non "buca" il Wi-Fi, ma cattura il **4-way handshake EAPOL** che contiene il materiale per
crackare offline la PSK. In *monitor mode* sul canale giusto, filtra l'handshake:
```text
eapol                                # i 4 messaggi del 4-way handshake WPA/WPA2
wlan.fc.type_subtype == 0x08         # beacon (mappa gli SSID presenti)
```
Poi converti e cracka **fuori** da Wireshark (è solo cattura):
```bash
hcxpcapngtool -o hash.22000 cattura.pcapng   # estrai l'hash in formato hashcat
hashcat -m 22000 hash.22000 wordlist.txt     # cracking offline → vedi [[Hashcat]]
```

## 5. Recon passivo
Senza inviare un solo pacchetto (a differenza di [[Nmap]], che è **attivo** e rumoroso), Wireshark
**ascolta** e ricostruisce: host attivi, OS (TTL, fingerprint), servizi annunciati, nomi NetBIOS/mDNS,
SSID. `Statistics → Conversations` e `→ Protocol Hierarchy` danno la mappa della rete in silenzio.

---

# USO DIFENSIVO (network forensics & threat hunting)

## Workflow di triage di un pcap (incident response)
Aprire un `.pcap` sospetto e procedere dall'alto verso il dettaglio:
1. **`Statistics → Capture File Properties`**: durata, dimensione, intervallo temporale (inquadra l'evento).
2. **`Statistics → Protocol Hierarchy`**: che protocolli dominano? Tanto DNS o TLS verso un solo host = sospetto.
3. **`Statistics → Conversations`** (tab TCP/IP): ordina per **byte** → chi trasferisce di più (esfiltrazione?);
   per **durata** → connessioni lunghissime (C2/reverse shell).
4. **`Expert Information`**: Wireshark segnala da solo retransmission, reset, malformazioni.
5. **`Follow Stream`** sui flussi sospetti → contenuto reale (comandi shell, beacon, payload).
6. **`Export Objects`** → estrai i file trasferiti, hashali, cercali su [[VirusTotal]].

## Rilevare una scansione di porte (firma di Nmap)
Un [[Nmap]] SYN scan = **molti SYN da un IP verso molte porte, senza completare l'handshake** (tanti
RST o nessun dato). In Wireshark:
```text
tcp.flags.syn==1 && tcp.flags.ack==0           # raffica di SYN iniziali...
tcp.flags.reset==1                             # ...seguiti da molti RST = porte chiuse sondate
```
Poi `Statistics → Conversations`: un IP sorgente con **centinaia di conversazioni** verso porte diverse
del/dei target in pochi secondi = scan. Le scansioni FIN/NULL/Xmas si vedono come pacchetti con flag
anomale: `tcp.flags == 0x000` (NULL), `tcp.flags.fin==1 && tcp.flags.ack==0` (FIN).

## Rilevare ARP poisoning / MITM
Il sintomo è **due IP che rispondono con lo stesso MAC**, o reply ARP non sollecitate (gratuite):
```text
arp.duplicate-address-detected       # Wireshark rileva l'IP duplicato
arp.opcode == 2                      # reply ARP: troppe e non richieste = spoofing
```
È l'attacco che spesso *precede* lo sniffing: chi avvelena l'ARP si mette in mezzo ([[Man-in-the-Middle (MITM)]]).

## Rilevare reverse shell e C2 beaconing
- **Reverse shell**: connessione **in uscita** verso un IP esterno su porta alta, long-lived, con
  pacchetti PSH piccoli e interattivi. `Follow TCP Stream` mostra il prompt di shell o i comandi.
- **C2 beaconing**: connessioni **regolari** a intervalli fissi (es. ogni 60s) verso lo stesso host —
  pattern "battito". In `Statistics → Conversations` o `→ IO Graph` la regolarità è visibile a occhio.
  Il malware moderno usa TLS: identificalo col **fingerprint JA3** (hash del ClientHello) anche senza
  decifrare.
```text
tcp.flags.push==1 && tcp.len < 100   # tante piccole PSH = sessione interattiva (shell)
tls.handshake.type == 1              # ClientHello → base del fingerprint JA3
```

## Rilevare esfiltrazione e DNS tunneling
- **Esfiltrazione bulk**: `Statistics → Conversations` ordinato per byte in uscita → un upload anomalo.
- **DNS tunneling** (dati incapsulati in query DNS): tantissime query verso un dominio, sottodomini
  lunghi e casuali, record TXT/NULL:
```text
dns.qry.type == 16                   # record TXT (vettore tipico di tunneling)
dns && frame.len > 200               # query/risposte DNS anomalamente grandi
dns.flags.response == 0              # volume di query verso un solo dominio (con Statistics → DNS)
```

## Estrazione di IOC per il report / SIEM
Dal pcap si ricavano **Indicatori di Compromissione** ([[Indicatori di Compromissione (IOC)]]) da
girare al [[SIEM]]: IP/domini contattati, URI, hash dei file estratti, JA3. `tshark` li tira fuori in
forma lista:
```bash
tshark -r evento.pcap -Y dns.flags.response==0 -T fields -e dns.qry.name | sort -u   # domini contattati
tshark -r evento.pcap -Y http.request -T fields -e ip.dst -e http.host | sort -u     # host HTTP
```

## TLS: si può decifrare?
HTTPS è cifrato, ma in lab lo decodifichi se hai il materiale di chiave: imposta la variabile
**`SSLKEYLOGFILE`** (browser/curl la scrivono) e caricala in *Preferences → TLS → (Pre)-Master-Secret
log* → Wireshark mostra l'HTTP in chiaro. Senza chiavi vedi solo metadati (SNI, certificati, dimensioni,
JA3). Per la difesa, **JA3/SNI** bastano spesso a riconoscere il malware senza decifrare.

## Walkthrough end-to-end — "pcap sospetto" in CTF/IR
```text
1. Statistics → Protocol Hierarchy   → noto un 12% di DNS: troppo. Sospetto tunneling.
2. dns.qry.type == 16                → centinaia di TXT verso  x.attacker.com con sottodomini base32.
3. Statistics → Conversations (TCP)  → una connessione a 185.x.x.x:4444 lunga 14 min, in uscita.
4. tcp.stream eq <n> → Follow Stream → vedo un prompt "$ " e comandi: è una reverse shell.
5. File → Export Objects → HTTP      → estraggo update.exe; hash → VirusTotal = malware noto.
6. Compilo gli IOC: 185.x.x.x, x.attacker.com, hash di update.exe → li mando al [[SIEM]].
```

## tshark / tcpdump (CLI per cattura headless e automazione)
```bash
sudo tcpdump -i eth0 -w cattura.pcap 'tcp port 80'   # cattura senza GUI (BPF), per server/sensori
sudo tshark -i eth0 -Y "http.request" -T fields -e http.host -e http.request.uri
tshark -r cattura.pcap -q -z conv,tcp                # report conversazioni TCP da CLI
wireshark cattura.pcap                                # analizzi con calma nella GUI
```
Per il rilevamento **continuo** a livello rete, Wireshark cede il passo a [[Zeek]]/[[Suricata]] (sensori
che girano 24/7 e generano log/alert); Wireshark resta lo strumento di **analisi puntuale** e deep-dive.

## Casi limite e troubleshooting
| Sintomo | Causa | Fix |
|---|---|---|
| "Non vedo traffico altrui" | rete switchata, niente mirror/MITM | SPAN/TAP, o ARP spoof in lab; in Wi-Fi monitor mode |
| Cattura enorme e illeggibile | nessun capture filter | filtra prima (`tcp port 443`) o lavora a display filter + `tcp.stream` |
| HTTPS tutto cifrato | manca il materiale di chiave | `SSLKEYLOGFILE` in lab; altrimenti usa SNI/JA3/metadati |
| Permessi negati alla cattura | utente non nel gruppo | `sudo usermod -aG wireshark $USER` e ri-login |
| Pacchetti "malformed" ovunque | offload/checksum della NIC | disattiva *checksum offload* o ignora i checksum errati nelle Preferences |
| Wi-Fi: vedo solo i miei pacchetti | manca monitor mode / canale | abilita monitor mode, fissa il canale del target |

## Domande da colloquio
1. **Capture filter vs display filter?** Il capture filter (BPF) decide *cosa salvare* prima della
   cattura ed è irreversibile; il display filter (sintassi Wireshark) filtra *a posteriori* ciò che hai
   già, reversibile.
2. **Perché su uno switch non vedi il traffico altrui e come ci si mette in mezzo?** Lo switch inoltra i
   frame solo alla porta di destinazione. Servono port mirroring/TAP (legittimo) o un MITM via ARP
   spoofing (offensivo); in Wi-Fi, monitor mode.
3. **Come riconosci una reverse shell in un pcap?** Connessione in uscita verso IP esterno su porta alta,
   long-lived, piccoli pacchetti PSH interattivi; `Follow TCP Stream` mostra prompt e comandi.
4. **Come spotti un DNS tunneling?** Volume anomalo di query verso un solo dominio, sottodomini lunghi e
   casuali, record TXT/NULL; in Protocol Hierarchy il DNS pesa troppo.
5. **Puoi leggere HTTPS in Wireshark?** Solo con il materiale di chiave (`SSLKEYLOGFILE`) in lab; in
   produzione vedi solo metadati — ma SNI e fingerprint JA3 spesso bastano a identificare il malware.

## Collegamenti
- [[TCP]] · [[UDP]] · [[ICMP]] · [[ARP]] · [[DNS]] · [[HTTP e HTTPS]]
- [[Three-Way Handshake TCP]] · [[Modello OSI]] · [[Man-in-the-Middle (MITM)]]
- [[Nmap]] — recon **attivo**, l'opposto dell'ascolto passivo di Wireshark
- [[TLS e SSL]] · [[Cookie e JWT]] — perché le credenziali in chiaro si rubano
- [[Incident Response]] · [[Log Analysis]] · [[Indicatori di Compromissione (IOC)]] · [[SIEM]]
- [[Analisi Malware di Base]] · [[VirusTotal]] · [[Hashcat]] — dove finiscono i file/hash estratti

## Fonti
- Wireshark — User's Guide: <https://www.wireshark.org/docs/wsug_html_chunked/>
- Wireshark — Display Filter Reference: <https://www.wireshark.org/docs/dfref/>
- Chris Sanders — *Practical Packet Analysis* (No Starch)
- Wireshark — Statistics & Follow Stream: <https://www.wireshark.org/docs/wsug_html_chunked/ChStatistics.html>
- Peterson & Davie — *Computer Networks: A Systems Approach* (incapsulamento e header dei protocolli, letti layer per layer nel dissector): <https://book.systemsapproach.org/>
