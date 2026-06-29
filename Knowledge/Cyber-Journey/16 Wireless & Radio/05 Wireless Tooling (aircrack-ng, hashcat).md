---
tipo: concetto
tag: [wireless]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Wireless Tooling (aircrack-ng, hashcat)"]
---

# Wireless Tooling (aircrack-ng, hashcat)

## In breve
Un assessment WiFi si appoggia a una catena di strumenti specializzati: la **suite aircrack-ng** per
cattura e injection a livello 802.11, **hcxtools** per la cattura/conversione moderna (PMKID +
formato 22000), **hashcat** per il cracking accelerato su GPU, e orchestratori come **wifite** che
automatizzano l'intero flusso. Conoscerne ruoli e formati evita di perdere catture inutilizzabili.

## Come funziona
Il flusso logico è: **monitor mode -> ricognizione -> cattura -> conversione -> cracking**.

- **airmon-ng**: gestisce la monitor mode e termina i processi interferenti.
- **airodump-ng**: ricognizione (lista AP/client) e cattura su file `.cap`.
- **aireplay-ng**: injection — deauth, fake auth, replay ARP (storico per WEP).
- **aircrack-ng**: cracking CPU di WEP e WPA/WPA2 (formato legacy 2500 da `.cap`).
- **hcxdumptool**: cattura moderna in `.pcapng`, ottiene PMReKID anche clientless.
- **hcxpcapngtool**: converte il `.pcapng` nel formato hash **22000** per hashcat.
- **hashcat**: cracking su GPU; `-m 22000` (WPA-PBKDF2, copre PMKID + EAPOL), `-m 2500` (legacy).
- **wifite**: wrapper che richiama automaticamente la catena sopra.

Il punto chiave dei formati: hashcat ha unificato in **22000** sia il PMKID (vecchio 16800) sia
l'handshake EAPOL (vecchio 2500). aircrack-ng lavora invece direttamente sul `.cap`.

## Esempi
Catena completa con la suite aircrack-ng:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo airodump-ng --bssid AA:BB:CC:DD:EE:FF -c 6 -w cap wlan0mon
sudo aireplay-ng --deauth 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
sudo aircrack-ng -w rockyou.txt cap-01.cap
```

Catena moderna con hashcat (-m 22000):

```bash
sudo hcxdumptool -i wlan0mon -o dump.pcapng --enable_status=1
hcxpcapngtool -o hash.22000 dump.pcapng

# Dizionario
hashcat -m 22000 hash.22000 rockyou.txt
# Maschera (es. 8 cifre, tipico default router)
hashcat -m 22000 hash.22000 -a 3 ?d?d?d?d?d?d?d?d
# Dizionario + regole
hashcat -m 22000 hash.22000 rockyou.txt -r rules/best64.rule
# Mostra risultati già crackati
hashcat -m 22000 hash.22000 --show
```

Tutto automatico:

```bash
sudo wifite -i wlan0 --kill --wpa --dict rockyou.txt
```

## Mitigazione e difesa
- Dal lato difensivo gli stessi strumenti servono per **audit autorizzati**: verificare la robustezza
  delle proprie PSK eseguendo il cracking interno è una buona pratica.
- Politiche di passphrase forti rendono inutile il cracking, indipendentemente dalla GPU disponibile.
- Logging e WIDS per individuare l'uso di questi tool (deauth burst, hcxdumptool probe).

## Lab
- [[TryHackMe]] — room "Wifi Hacking 101" e simili per la suite aircrack-ng.
- [[HackTheBox]] — challenge con file di cattura da convertire e crackare.
- Lab: scheda in monitor mode + GPU (anche cloud) per hashcat; dataset `rockyou.txt` per i test.

## Domande
**D:** Qual è la differenza tra `-m 2500` e `-m 22000`?
R: 2500 è il formato legacy EAPOL; 22000 è quello unificato che gestisce sia PMKID sia handshake.

**D:** Perché convertire il `.pcapng` con hcxpcapngtool?
R: hashcat non legge direttamente il pcapng: serve il formato hash 22000.

**D:** aircrack-ng usa la GPU?
R: No, è CPU-bound; per performance reali su WPA2 si usa hashcat su GPU.

**D:** Cosa fa wifite?
R: Orchestra airmon/airodump/aireplay/hcxdumptool e il cracking, automatizzando il flusso.

## Approfondimento livello esperto
La scelta tra dizionario, regole e maschera determina la copertura: contro le PSK di default dei
router (spesso pattern noti, es. 8-10 cifre o MAC-based) le **maschere** sono molto più efficienti di
un dizionario. hashcat sfrutta PBKDF2-HMAC-SHA1 a 4096 iterazioni, quindi anche su GPU potenti le
passphrase casuali lunghe restano fuori portata: il vero limite è l'entropia della password, non lo
strumento. In contesti enterprise si affiancano `eaphammer` (evil twin RADIUS) e `hostapd-wpe` per
la cattura di credenziali 802.1X. Per le catture sul campo, `hcxdumptool` con filtri sui BSSID
riduce il rumore e il rischio di colpire reti fuori scope.

## Collegamenti
- [[Attacchi WPA2 (handshake e PMKID)]] — l'uso primario di questi tool
- [[Evil Twin e Rogue AP]] — hostapd e wifite per attacchi attivi
- [[Fondamenti Wireless e 802.11]] — monitor mode e injection
- [[WEP, WPA, WPA2 e WPA3]] — formati e protocolli da attaccare
- [[Penetration Testing]] — fase di exploitation
- [[Modello OSI]]

## Fonti
- https://hashcat.net/wiki/doku.php?id=hashcat
- https://www.aircrack-ng.org/doku.php?id=getting_started
- https://github.com/ZerBea/hcxtools
