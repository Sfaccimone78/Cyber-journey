---
tipo: concetto
tag: [reti]
fase: 2
fonti: 3
aggiornato: 2026-06-22
stato: maturo
aliases: ["Man-in-the-Middle (MITM)", "Man-in-the-Middle", "MITM"]
---

# Man-in-the-Middle (MITM)

> **Nota etica**: intercettare traffico altrui senza autorizzazione è reato penale. Ogni tecnica
> descritta è da praticare **esclusivamente in lab controllato, CTF o ambienti autorizzati**.
> MITRE ATT&CK: **T1557** (Adversary-in-the-Middle).

## In breve
In un attacco **Man-in-the-Middle** l'attaccante si interpone tra due parti che comunicano,
potendo **leggere, modificare o iniettare** traffico senza che le vittime se ne accorgano.
Viola riservatezza e integrità della [[Triade CIA]]. La tecnica più comune in LAN è l'**ARP
spoofing** (poisoning), ma esistono vettori a ogni livello dello stack.

---

## Tassonomia: on-path vs off-path

| Posizione | Descrizione | Esempio |
|---|---|---|
| **On-path** (vero MITM) | L'attaccante è *nel* percorso e vede/altera ogni pacchetto | ARP spoofing, rogue AP |
| **Off-path** | Non vede il traffico; deve *indovinare* o forzare deviazioni | Sequence prediction [[TCP]], cache poisoning [[DNS]] |

---

## Vettori per livello

| Livello ([[Modello OSI]]) | Vettore | Tool tipico |
|---|---|---|
| L2 | ARP spoofing / ARP poisoning | ettercap, bettercap |
| L2 | Rogue DHCP (DHCP starvation + server falso) | [[DHCP]], yersinia |
| L2 Wi-Fi | Rogue AP / Evil Twin | hostapd-wpe, wifiphisher |
| L2 Wi-Fi | KARMA attack (risponde a ogni SSID probe) | hostapd-wpe |
| L3 | ICMP redirect | — (vedi [[ICMP]]) |
| L3 | BGP hijacking (livello Internet, state-actor) | — |
| L7/Win | LLMNR / NBT-NS poisoning | [[Responder]] |
| L7/Win | DHCPv6 (mitm6) | mitm6 |
| L7 | DNS spoofing / cache poisoning | bettercap, dnschef |
| L7 | SSL stripping | sslstrip, bettercap |

---

## Meccanismi chiave

### 1. ARP Poisoning
[[ARP]] non ha autenticazione: ogni host accetta qualsiasi risposta ARP. L'attaccante invia
**gratuitous ARP** continuamente associando il proprio [[MAC Address]] all'[[Indirizzamento IP|IP]]
del gateway (verso la vittima) e all'IP della vittima (verso il gateway). Risultato:
tutto il traffico vittima↔gateway transita dal NIC dell'attaccante.

```
Vittima  ←→  Attaccante (inoltro attivo)  ←→  Gateway
```

Requisito critico: **IP forwarding abilitato** (`net.ipv4.ip_forward = 1`), altrimenti la vittima
perde connettività e l'attacco si svela immediatamente.

### 2. Rogue AP / Evil Twin
L'attaccante emette un SSID identico alla rete legittima con segnale più forte. I client
si connettono automaticamente. Il traffico transita tramite l'attaccante; se non c'è HTTPS,
le credenziali sono in chiaro. L'attacco KARMA estende il concetto rispondendo a *qualsiasi*
probe request dei dispositivi.

### 3. SSL Stripping
Tecnica ideata da Moxie Marlinspike (2009). L'attaccante, interposto tra client e server:
1. Il client chiede `http://sito.com`.
2. L'attaccante stabilisce una sessione HTTPS con il server (come proxy).
3. Risponde al client in **HTTP** (plain), downgrading la connessione.
4. Il client non vede il lucchetto; le credenziali viaggiano in chiaro verso l'attaccante.

Contromisura: **HSTS** (HTTP Strict Transport Security) forza il browser a usare sempre HTTPS
anche al primo collegamento (preload list). Vedi [[HTTP e HTTPS]] e [[TLS e SSL]].

### 4. LLMNR / NBT-NS Poisoning (ambienti Windows)
Quando un host Windows non trova un nome via [[DNS]], invia broadcast LLMNR o NBT-NS.
[[Responder]] risponde falsamente fingendo di essere il server cercato. La vittima invia
credenziali **NetNTLM** (challenge-response) che possono essere:
- **Craccate offline** con Hashcat/John.
- **Rilanciatel** via [[NTLM Relay]] verso altri host (attacco SMB relay → movimento laterale
  in [[Active Directory]]).

### 5. DHCPv6 / mitm6
Nei segmenti di rete con IPv6 abilitato (default in Windows anche se non usato), mitm6
risponde alle richieste DHCPv6 assegnandosi come DNS default. Riesce così a forzare
autenticazioni NTLM/Kerberos verso sistemi controllati dall'attaccante.

---

## Walkthrough in lab (ARP + intercettazione HTTPS)

> Ambiente: Kali Linux + VM vittima sulla stessa subnet `/24`. Tutto autorizzato.

```bash
# 1. Abilita IP forwarding per non interrompere la connettività della vittima
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# 2a. ARP spoofing con ettercap (modalità testo, arp remote)
sudo ettercap -T -M arp:remote /192.168.1.100// /192.168.1.1//

# 2b. Alternativa con bettercap (più moderno, modulare)
sudo bettercap -iface eth0
# dentro bettercap REPL:
#   set arp.spoof.targets 192.168.1.100
#   arp.spoof on
#   net.sniff on

# 3. Sniff del traffico catturato (in parallelo)
sudo wireshark -i eth0 -f "host 192.168.1.100"

# 4. SSL stripping con bettercap
#   https.proxy on            # bettercap fa da proxy HTTPS
#   set https.proxy.sslstrip true
#   # oppure
sudo sslstrip -l 8080
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

# 5. Cattura credenziali HTTP in chiaro tramite Wireshark o tcpdump
sudo tcpdump -i eth0 -A -s 0 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) \
  - ((tcp[12]&0xf0)>>2)) != 0)' | grep -Ei "pass|user|login"
```

Analisi successiva con [[Wireshark]]: filtrare `http.request.method == "POST"` per trovare
credenziali in form HTML.

### Intercettare con mitmproxy
mitmproxy (non ha pagina dedicata nella wiki) è un proxy interattivo TLS-aware:
```bash
# Avvia in modalità trasparente
mitmproxy --mode transparent --showhost

# La vittima deve avere la CA di mitmproxy installata per HTTPS; altrimenti solo HTTP
```

---

## Tabella difese per vettore

| Vettore | Difesa tecnica | Livello |
|---|---|---|
| ARP spoofing | Dynamic ARP Inspection (DAI) + DHCP snooping sugli switch managed | Switch L2 |
| ARP spoofing | ARP statico per gateway (su host critici) | Host |
| Rogue AP / Evil Twin | 802.1X (autenticazione port-based), EAP-TLS, WIDS | Wi-Fi |
| SSL stripping | HSTS + HSTS Preload; [[Certificati Digitali e CA]] pinning | Applicativo |
| LLMNR/NBT-NS | Disabilitare LLMNR e NBT-NS via GPO (Windows) | Active Directory |
| DHCPv6 / mitm6 | Disabilitare IPv6 se non usato; DHCPv6 Guard sui switch | Rete |
| BGP hijacking | RPKI (Resource Public Key Infrastructure), BGP community filtering | ISP/backbone |
| Generico | Cifratura end-to-end ([[TLS e SSL]]) + certificate pinning mobile | Applicativo |
| Monitoraggio | Rilevare cambio MAC↔IP anomalo nelle ARP table; alert su [[SIEM]] | Blue Team |
| Segmentazione | VLAN + [[Subnetting]] riduce il blast radius di un MITM L2 | Rete |

---

## Rilevamento (lato Blue Team)

**Indicatori di ARP spoofing:**
- Un [[MAC Address]] risponde per più IP (`arp -a` mostra duplicati di MAC).
- Traffico da/verso un host con MAC insolito; alert da tool come `arpwatch` o XDR.
- Latenza anomala (hop extra introdotto dall'attaccante).

**Indicatori di rogue AP:**
- SSID duplicato con BSSID diverso → WIDS alert.
- Client che si disassociano improvvisamente e si riassociano.

**Indicatori di LLMNR/NBT-NS abuse:**
- Log eventi Windows 4625 (failed logon) verso IP insoliti.
- Traffico LLMNR (UDP 5355) o NBT-NS (UDP 137) con risposte da IP non autorizzati.
- [[Responder]] lascia tracce nei log SMB e nei log di rete se il SOC monitora.

---

## MITRE ATT&CK

| Tecnica | ID | Descrizione |
|---|---|---|
| Adversary-in-the-Middle | T1557 | Intercettazione on-path generico |
| ARP Cache Poisoning | T1557.002 | Sub-tecnica ARP |
| LLMNR/NBT-NS Poisoning | T1557.001 | Sub-tecnica Windows |
| Network Sniffing | T1040 | Cattura passiva del traffico |
| SSL Stripping (downgrade) | T1600 | Indebolimento crittografico |

---

## Casi limite e varianti avanzate

- **HTTPS con HSTS Preload**: lo stripping fallisce; il browser si rifiuta di caricare il sito in HTTP.
- **Certificate Pinning**: app mobile con pin del certificato rifiuta la CA dell'attaccante (mitmproxy
  diventa inutile senza bypass del pin via Frida/Objection).
- **VPN**: tutto il traffico verso il server VPN è cifrato; il MITM vede solo pacchetti cifrati.
  Vedi [[VPN]].
- **Reti commutate (switch) vs hub**: in una rete switched lo sniff passivo non funziona; serve ARP
  poisoning o port mirroring (accesso fisico).
- **IPv6 SLAAC**: anche senza DHCPv6, un router advertisement falso può reindirizzare il traffico.

---

## Domande da esame / colloquio

**Q1: Perché abilitare IP forwarding prima di un ARP spoofing?**
A: Senza forwarding il traffico della vittima arriva all'attaccante ma non viene inoltrato al gateway:
la vittima perde Internet e l'attacco si svela. Con forwarding l'attaccante è un router trasparente.

**Q2: Come funziona SSL stripping e perché HSTS lo neutralizza?**
A: SSL stripping downgrade la connessione HTTPS a HTTP tra client e attaccante, pur mantenendo HTTPS
verso il server. HSTS impone al browser (via header o preload list) di usare ALWAYS HTTPS verso quel
dominio: la prima risposta HTTP viene rifiutata, impedendo il downgrade.

**Q3: Quale differenza tra ARP spoofing e ARP poisoning?**
A: I termini sono spesso usati come sinonimi. Tecnicamente, "spoofing" indica l'invio di risposte
ARP false; "poisoning" descrive il risultato (la cache ARP dell'host contiene associazioni false).
In pratica sono la stessa tecnica.

**Q4: Come si difende un'azienda da LLMNR/NBT-NS poisoning?**
A: Disabilitare LLMNR (via GPO: Computer Config → Admin Templates → Network → DNS Client → Turn off
multicast name resolution = Enabled) e NBT-NS (scheda di rete → proprietà TCP/IPv4 → Avanzate → WINS
→ Disable NetBIOS over TCP/IP). Come compensating control: SMB signing obbligatorio blocca il relay
anche se le credenziali vengono catturate.

**Q5: Cosa distingue un Evil Twin da un Rogue AP?**
A: Un Rogue AP è qualsiasi access point non autorizzato sulla rete. Un Evil Twin è un Rogue AP che
clona deliberatamente l'SSID (e talvolta il BSSID) di una rete legittima per ingannare i client e
posizionarsi come MITM. L'Evil Twin è un sottoinsieme malevolo del concetto di Rogue AP.

**Q6: Che cos'è il BGP hijacking e perché è pericoloso?**
A: Il Border Gateway Protocol instrada il traffico tra AS (autonomous systems) Internet. Un attore
malevolo annuncia prefissi IP non propri, deviando il traffico globale verso sé stesso. Esempi reali:
Pakistan Telecom vs YouTube (2008), Rostelecom (2020). Difficile da difendere senza RPKI.

---

## Strumenti di riferimento

| Tool | Funzione | Note |
|---|---|---|
| **bettercap** | ARP spoof, sniff, SSL strip, proxy | Più moderno di ettercap; REPL interattivo |
| **ettercap** | ARP spoof, plugin MITM | Classico, GUI disponibile |
| **mitmproxy** | Proxy TLS interattivo / script | Ottimo per analisi HTTP/HTTPS |
| **Responder** | LLMNR/NBT-NS/WPAD poisoning | Vedi [[Responder]] |
| **mitm6** | DHCPv6 MITM + DNS spoofing | Usato con [[NTLM Relay]] |
| **sslstrip** | SSL stripping (legacy) | Superato da bettercap |
| **arpwatch** | Rilevamento cambio MAC/IP | Difesa/monitoraggio |
| **Wireshark** | Analisi pacchetti catturati | Vedi [[Wireshark]] |

---

## Collegamenti
- [[ARP]] · [[MAC Address]] · [[Indirizzamento IP]] · [[DHCP]] · [[ICMP]]
- [[Wireshark]] · [[TLS e SSL]] · [[Certificati Digitali e CA]] · [[HTTP e HTTPS]]
- [[DNS]] · [[TCP]] · [[UDP]] · [[VPN]] · [[Subnetting]] · [[Modello OSI]]
- [[Responder]] · [[NTLM Relay]] · [[Active Directory]] — catena Windows
- [[Triade CIA]] · [[SIEM]] · [[Detection di Attacchi]] · [[MITRE ATT&CK]]

## Fonti
- OWASP — Man-in-the-middle attack: https://owasp.org/www-community/attacks/Manipulator-in-the-middle_attack
- HackTricks — Spoofing LLMNR/NBT-NS/ARP: https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/spoofing-llmnr-nbt-ns-mdns-dns-and-wpad-and-relay-attacks
- Cloudflare — What is a MITM attack?: https://www.cloudflare.com/learning/security/threats/man-in-the-middle-attack/
