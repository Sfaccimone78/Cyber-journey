---
tipo: concetto
tag: [wireless]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Evil Twin e Rogue AP"]
---

# Evil Twin e Rogue AP

## In breve
Quando la PSK è troppo forte per il cracking offline, l'attacco si sposta sull'**uomo nel mezzo a
livello 2**: si crea un AP fasullo che imita una rete legittima (**Evil Twin**) per indurre vittime e
client a connettersi, rubando credenziali tramite **captive portal** o intercettando il traffico. Un
**Rogue AP** è più in generale un AP non autorizzato collegato alla rete aziendale. Sono attacchi
attivi, rumorosi e ad alto impatto.

## Come funziona
L'**Evil Twin** sfrutta il fatto che i client si riconnettono automaticamente all'SSID memorizzato
con il segnale più forte. La sequenza tipica:

1. L'attaccante crea un AP (hostapd) con lo **stesso SSID** (ed eventualmente stesso BSSID) della
   rete target, su un canale con buon segnale.
2. Invia **deauth** ai client della rete legittima per scollegarli.
3. I client, riconnettendosi, scelgono l'AP fasullo se ha segnale migliore.
4. L'attaccante presenta un **captive portal** che simula una pagina di login del router/operatore e
   raccoglie la passphrase WPA2 o credenziali, oppure intercetta direttamente il traffico (DNS, HTTP).

Varianti:
- **KARMA**: l'AP risponde *a tutte* le probe request ("cerchi 'CasaMia'? eccomi"), sfruttando i
  client che trasmettono in chiaro la lista delle reti note (PNL, Preferred Network List).
- **Captive portal phishing**: pagina che chiede "reinserisci la password WiFi per aggiornamento
  firmware" — efficace contro utenti non tecnici.
- Per le reti **Enterprise (802.1X)**: un evil twin con RADIUS fasullo cattura gli hash MSCHAPv2.

## Esempi
Configurazione manuale di un AP con hostapd:

```bash
# /etc/hostapd/eviltwin.conf
cat > eviltwin.conf <<'EOF'
interface=wlan0
driver=nl80211
ssid=FreeCoffeeWiFi
hw_mode=g
channel=6
EOF

sudo hostapd eviltwin.conf
# In parallelo: dnsmasq per DHCP/DNS e un web server per il captive portal
```

Deauth della rete legittima per spingere i client sull'evil twin:

```bash
sudo aireplay-ng --deauth 0 -a AA:BB:CC:DD:EE:FF wlan0mon
```

Automazione completa con wifite (cattura handshake / PMKID / evil twin):

```bash
# wifite orchestra airmon, airodump, aireplay, hcxdumptool e il cracking
sudo wifite --kill
sudo wifite -i wlan0 --wpa
```

## Mitigazione e difesa
- **802.11w (PMF)** per impedire i deauth che innescano l'evil twin.
- Sui client enterprise: **validare il certificato del server RADIUS** (EAP-TLS) per non cadere nel
  RADIUS fasullo.
- **WIPS** che rilevano BSSID duplicati / SSID legittimi annunciati da MAC non autorizzati.
- Educazione utenti: un captive portal che chiede la password WiFi è quasi sempre un attacco.
- Disabilitare la connessione automatica a reti aperte note sui dispositivi (mitiga KARMA).

## Lab
- [[TryHackMe]] — room su evil twin e captive portal.
- [[HackTheBox]] — scenari di rogue AP.
- Lab isolato: due interfacce (una in monitor per deauth, una per hostapd) + un client di test
  dedicato; mai contro reti o utenti reali.

## Domande
**D:** Perché un client si connette all'evil twin?
R: Riconnessione automatica all'SSID noto con il segnale più forte; il deauth lo stacca dall'AP vero.

**D:** Cos'è KARMA?
R: Tecnica in cui l'AP risponde a tutte le probe request, sfruttando i client che annunciano la
propria lista di reti note.

**D:** L'evil twin funziona contro WPA3?
R: PMF blocca i deauth, ma la transition mode e l'ingegneria sociale (captive portal) restano vettori.

**D:** Come si difende una rete Enterprise dall'evil twin?
R: Imponendo la validazione del certificato del server RADIUS sui supplicant (EAP-TLS).

## Approfondimento livello esperto
L'evil twin con **captive portal** è oggi il vettore più affidabile contro reti WPA2 con PSK forte,
perché aggira completamente il cracking offline puntando sull'utente. Framework come `eaphammer`
automatizzano l'attacco enterprise (cattura MSCHAPv2 + relay), mentre tool come `wifiphisher` curano
il phishing del portale. Sul fronte difensivo, un **WIPS** correla potenza del segnale, BSSID e
fingerprint del beacon per individuare cloni; la **deauth detection** monitora rate anomali di
management frame. WPA3 + PMF + Enhanced Open (OWE) per le reti aperte alzano sensibilmente l'asticella.

## Collegamenti
- [[Attacchi WPA2 (handshake e PMKID)]] — alternativa quando la PSK è debole
- [[Fondamenti Wireless e 802.11]] — deauth e management frame
- [[WEP, WPA, WPA2 e WPA3]] — perché PMF/WPA3 mitigano questi attacchi
- [[Wireless Tooling (aircrack-ng, hashcat)]] — hostapd, wifite, aireplay
- [[Penetration Testing]] — fase di attacco attivo
- [[Modello OSI]]

## Fonti
- https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-wifi#evil-twin
- https://github.com/derv82/wifite2
- https://w1.fi/hostapd/
