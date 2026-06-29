---
tipo: concetto
tag: [wireless]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["WEP, WPA, WPA2 e WPA3"]
---

# WEP, WPA, WPA2 e WPA3

## In breve
La sicurezza WiFi è una storia di rattoppi successivi. **WEP** (1997) è rotto in modo catastrofico,
**WPA** (2003) è una toppa temporanea su hardware WEP, **WPA2** (2004) è lo standard de facto per
quindici anni ma vulnerabile ad attacchi offline sulla PSK, **WPA3** (2018) introduce **SAE** per
chiudere gli attacchi a dizionario offline. Conoscere le differenze spiega *quale attacco* è
applicabile a *quale rete*.

## Come funziona
- **WEP**: usa RC4 con un **IV (Initialization Vector) di soli 24 bit** concatenato alla chiave. Gli
  IV si ripetono rapidamente; raccogliendo abbastanza pacchetti con IV deboli (attacco FMS/PTW) la
  chiave si recupera in minuti. Da considerare equivalente a rete aperta.
- **WPA (TKIP)**: introduce **TKIP** con chiave per-pacchetto e MIC (Michael), girando ancora su RC4.
  Mitiga WEP ma TKIP ha debolezze proprie (Beck-Tews). Deprecato.
- **WPA2 (CCMP/AES)**: usa **AES-CCMP**, robusto sul piano crittografico. Il punto debole non è la
  cifratura ma il **4-way handshake**: chi cattura l'handshake può fare **brute force/dizionario
  offline** sulla PSK senza più toccare la rete.
- **WPA3-Personal (SAE)**: sostituisce la PSK handshake con **SAE (Simultaneous Authentication of
  Equals)**, una variante di Dragonfly basata su PAKE. Fornisce **forward secrecy** e rende
  l'attacco a dizionario offline **non più possibile**: ogni tentativo richiede un'interazione
  attiva con l'AP. Impone inoltre **PMF** obbligatorio.

A livello di chiavi: dalla **PSK** (o da SAE) si deriva la **PMK** (Pairwise Master Key); dal 4-way
handshake si deriva la **PTK** (Pairwise Transient Key) usata per cifrare il traffico unicast, e la
**GTK** per il traffico broadcast/multicast.

## Esempi
Identificare il protocollo in uso (colonna ENC/CIPHER/AUTH di airodump):

```bash
sudo airodump-ng wlan0mon
# ENC: WEP / WPA / WPA2 / WPA3
# CIPHER: WEP, TKIP, CCMP
# AUTH: PSK (pre-shared) o SAE (WPA3) o MGT (802.1X/enterprise)
```

Cracking storico WEP (solo per laboratorio didattico):

```bash
# Cattura traffico con IV; aireplay-ng accelera generando traffico ARP
sudo airodump-ng --bssid AA:BB:CC:DD:EE:FF -c 6 -w wep wlan0mon
sudo aireplay-ng -3 -b AA:BB:CC:DD:EE:FF wlan0mon
sudo aircrack-ng wep-01.cap
```

## Mitigazione e difesa
- Disabilitare WEP e WPA/TKIP: usare **solo WPA2-CCMP** o, meglio, **WPA3** / modalità di transizione
  WPA3-WPA2 con PMF.
- Passphrase **lunghe e casuali** (>=16 caratteri non da dizionario): contro WPA2 è l'unica difesa
  reale dato l'attacco offline.
- In ambienti aziendali preferire **WPA2/WPA3-Enterprise (802.1X/EAP-TLS)** con certificati invece
  della PSK condivisa.

## Lab
- [[TryHackMe]] — moduli sui protocolli WiFi e sul cracking WPA2.
- [[HackTheBox]] — challenge su handshake e analisi cifratura.
- Lab: AP di test configurabile su WEP/WPA2/WPA3 + scheda in monitor mode per confrontare gli ENC.

## Domande
**D:** Perché WEP è considerato insicuro a prescindere dalla password?
R: L'IV di 24 bit si ripete; con abbastanza pacchetti (PTW/FMS) la chiave si recupera a prescindere
dalla sua lunghezza.

**D:** WPA2-CCMP è crittograficamente rotto?
R: No, AES-CCMP è solido. La debolezza è il 4-way handshake catturabile e attaccabile offline.

**D:** Cosa cambia con SAE in WPA3?
R: SAE è un PAKE che impedisce l'attacco a dizionario offline e fornisce forward secrecy: ogni
guess richiede un handshake attivo.

**D:** Differenza tra PMK e PTK?
R: La PMK deriva dalla PSK/SAE; la PTK deriva dalla PMK + nonce durante il 4-way handshake e cifra il
traffico della sessione.

## Approfondimento livello esperto
WPA3 non è esente da falle: la ricerca **Dragonblood** (Vanhoef & Ronen, 2019) ha mostrato attacchi
side-channel (cache e timing) sulla derivazione della password in SAE e downgrade verso la modalità
di transizione WPA2. La **transition mode** resta un rischio: un attaccante può forzare un client a
usare WPA2 e poi attaccare l'handshake. In enterprise, EAP mal configurato (es. assenza di
validazione del certificato server) apre ad attacchi tipo **evil twin RADIUS** con cattura delle
credenziali MSCHAPv2.

## Collegamenti
- [[Fondamenti Wireless e 802.11]] — il livello su cui poggiano questi protocolli
- [[Attacchi WPA2 (handshake e PMKID)]] — l'attacco pratico contro WPA2-PSK
- [[Wireless Tooling (aircrack-ng, hashcat)]] — gli strumenti di cracking
- [[Modello OSI]] — cifratura a livello data link
- [[Penetration Testing]] — contesto metodologico

## Fonti
- https://www.wi-fi.org/discover-wi-fi/security
- https://wpa3.mathyvanhoef.com/ (Dragonblood)
- https://www.aircrack-ng.org/doku.php?id=cracking_wpa
