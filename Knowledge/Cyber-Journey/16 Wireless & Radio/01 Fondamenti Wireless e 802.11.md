---
tipo: concetto
tag: [wireless]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Fondamenti Wireless e 802.11"]
---

# Fondamenti Wireless e 802.11

## In breve
Il WiFi è definito dallo standard **IEEE 802.11**. A differenza di Ethernet, il mezzo è **condiviso
e broadcast**: chiunque sia nel raggio radio può ricevere i frame. La sicurezza non può quindi
basarsi sull'isolamento fisico, ma solo sulla crittografia del payload. Capire la struttura dei
**frame 802.11** e la differenza tra frame di management, control e data è il prerequisito di
qualsiasi attacco wireless.

## Come funziona
A basso livello una rete 802.11 lavora su **canali** nelle bande **2.4 GHz** (canali 1-13) e **5 GHz**.
Un client (STA) e un access point (AP) comunicano tramite tre famiglie di frame:

- **Management frame**: beacon (annuncio della rete + SSID), probe request/response, authentication,
  association, **deauthentication** e disassociation. Storicamente **non autenticati né cifrati**
  (prima di 802.11w), il che rende possibile l'iniezione di deauth.
- **Control frame**: RTS/CTS, ACK — regolano l'accesso al mezzo (CSMA/CA).
- **Data frame**: trasportano il payload effettivo, cifrato dal protocollo di sicurezza attivo.

Ogni frame ha un header con indirizzi MAC (fino a 4: sorgente, destinazione, BSSID), un campo
**Sequence Control** e flag (ToDS/FromDS). Il **BSSID** è il MAC dell'AP e identifica la cella.

Per catturare questo traffico la scheda deve entrare in **monitor mode**: riceve tutti i frame
dell'aria, non solo quelli destinati al proprio MAC (come fa il promiscuous mode su Ethernet).
Serve un chipset che supporti monitor mode e **packet injection** (es. Atheros AR9271, Realtek
RTL8812AU).

## Esempi
Attivare la monitor mode e mappare le reti vicine:

```bash
# Elenca le interfacce wireless e i processi che potrebbero interferire
sudo airmon-ng

# Termina NetworkManager/wpa_supplicant che disturbano la monitor mode
sudo airmon-ng check kill

# Porta wlan0 in monitor mode (diventa wlan0mon)
sudo airmon-ng start wlan0

# Scansione di tutte le reti e dei client associati
sudo airodump-ng wlan0mon

# Cambio manuale di canale e verifica modalità
sudo iw dev wlan0mon set channel 6
iw dev wlan0mon info
```

Filtrare su un singolo AP per vedere i client (STATION):

```bash
sudo airodump-ng --bssid AA:BB:CC:DD:EE:FF --channel 6 wlan0mon
```

## Mitigazione e difesa
- Abilitare **802.11w (Protected Management Frames, PMF)** per autenticare deauth/disassoc.
- Ridurre la potenza di trasmissione per contenere il raggio fisico fuori dal perimetro.
- Non nascondere l'SSID come misura di sicurezza: è ininfluente (il SSID compare nelle probe).
- Segmentare la rete WiFi (VLAN/SSID guest isolati) rispetto alla rete interna.

## Lab
- [[TryHackMe]] — percorsi introduttivi su 802.11 e cattura traffico.
- [[HackTheBox]] — challenge di analisi pcap wireless.
- Lab casalingo: scheda USB compatibile in **monitor mode** + un AP di test dedicato; mai operare su
  reti di terzi senza autorizzazione scritta.

## Domande
**D:** Perché un attaccante può iniettare deauth senza conoscere la password?
R: I management frame (prima di 802.11w) non sono autenticati: l'AP/STA accettano un deauth con il
BSSID/MAC corretto, banale da forgiare.

**D:** Che differenza c'è tra monitor mode e promiscuous mode?
R: Il promiscuous mode (Ethernet) cattura i frame del proprio segmento; la monitor mode cattura
*tutti* i frame radio dell'aria, anche di reti a cui non si è associati.

**D:** A cosa serve il BSSID?
R: È il MAC dell'AP e identifica univocamente la cella su cui filtrare la cattura.

**D:** Nascondere l'SSID protegge la rete?
R: No: il client lo trasmette nelle probe request, quindi è facilmente recuperabile.

## Approfondimento livello esperto
La scelta del chipset è critica: senza supporto a injection non si possono fare deauth né attacchi
attivi. Strumenti come `mdk4` sfruttano i management frame per beacon flooding e deauth massivi.
A livello di detection, un **WIDS** identifica anomalie nella sequenza dei management frame e nei
rate di deauth. L'introduzione del **PMF obbligatorio in WPA3** chiude definitivamente la classe di
attacchi basati su deauth forgiati, spostando il fronte sugli attacchi al handshake SAE.

## Collegamenti
- [[WEP, WPA, WPA2 e WPA3]] — i protocolli che cifrano i data frame
- [[Attacchi WPA2 (handshake e PMKID)]] — sfrutta la cattura dei frame EAPOL
- [[Wireless Tooling (aircrack-ng, hashcat)]] — la suite per cattura e injection
- [[Modello OSI]] — 802.11 occupa L1/L2
- [[Penetration Testing]] — inquadramento metodologico

## Fonti
- https://www.aircrack-ng.org/doku.php?id=airmon-ng
- https://standards.ieee.org/ieee/802.11/7028/
- https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-wifi
