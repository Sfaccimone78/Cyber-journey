---
tipo: concetto
tag: [wireless]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Bluetooth, BLE e RFID-NFC"]
---

# Bluetooth, BLE e RFID-NFC

## In breve
Oltre al WiFi, l'aria è piena di altri protocolli radio a corto raggio: **Bluetooth Classic**,
**Bluetooth Low Energy (BLE)** usato da IoT/wearable/smart lock, e **RFID/NFC** per badge, carte e
pagamenti. Condividono lo stesso problema di fondo del WiFi — mezzo broadcast — ma con superfici
d'attacco proprie: pairing deboli, advertising in chiaro, tag clonabili. Sono sempre più rilevanti
negli assessment IoT/fisici.

## Come funziona
- **Bluetooth Classic**: opera a 2.4 GHz con frequency hopping. Il **pairing** stabilisce una link
  key; metodi legacy (PIN corti) sono brute-forzabili. Storici attacchi: BlueBorne (RCE su stack),
  KNOB (downgrade dell'entropia della chiave).
- **BLE**: pensato per basso consumo. Un dispositivo trasmette **advertising packet** (broadcast, in
  chiaro) su 3 canali; un central si connette e naviga il **GATT** (servizi e caratteristiche). La
  sicurezza dipende dal metodo di pairing: **Just Works** (nessuna autenticazione, vulnerabile a
  MITM), **Passkey**, **Numeric Comparison**, **OOB**. Molti device IoT usano Just Works.
- **RFID/NFC**: tag passivi alimentati dal campo del lettore. **LF 125 kHz** (badge EM4100, banali da
  clonare) e **HF 13.56 MHz** (MIFARE Classic, NFC). MIFARE Classic usa il cifrario proprietario
  **Crypto1**, rotto: le chiavi si recuperano con attacchi tipo nested/darkside. NFC è RFID HF con
  stack applicativo (pagamenti, smartphone).

## Esempi
Scansione e enumerazione BLE su Linux (BlueZ + bettercap):

```bash
# Scoperta dispositivi BLE
sudo hcitool lescan
sudo bluetoothctl
# [bluetooth]# scan on

# bettercap: enumerazione e dump del GATT
sudo bettercap
> ble.recon on
> ble.show
> ble.enum <MAC>
```

Sniffing BLE con strumenti dedicati e gattacker/nRF:

```bash
# Con un dongle nRF52 + Wireshark plugin per sniffare advertising/connessioni
# (Nordic nRF Sniffer) oppure con Ubertooth per Bluetooth Classic
ubertooth-btle -f   # follow connessioni BLE
```

Clonazione RFID/NFC con Proxmark3:

```bash
# Identifica il tag
pm3 --> hf search        # tag HF (MIFARE/NFC)
pm3 --> lf search        # tag LF (EM4100, badge 125 kHz)

# Attacco alle chiavi MIFARE Classic e dump
pm3 --> hf mf autopwn
pm3 --> hf mf dump
```

## Mitigazione e difesa
- BLE: usare pairing **LE Secure Connections** (numeric comparison/passkey), non Just Works; cifrare
  i dati applicativi a livello GATT.
- Bluetooth: tenere aggiornato lo stack (mitigazione BlueBorne/KNOB), disabilitare la visibilità
  quando non serve.
- RFID/NFC: abbandonare LF EM4100 e MIFARE Classic; usare **MIFARE DESFire EV2/EV3** o smart card con
  crittografia forte e autenticazione mutua.
- Limitare il raggio fisico e proteggere i badge in custodie schermanti dove serve.

## Lab
- [[TryHackMe]] — moduli introduttivi su IoT/BLE.
- [[HackTheBox]] — challenge hardware/IoT con dump di firmware e traffico BLE.
- Lab: Proxmark3 per RFID/NFC, dongle nRF52/Ubertooth per BLE, smart lock o wearable di test.

## Domande
**D:** Perché molti device BLE sono vulnerabili a MITM?
R: Usano il pairing **Just Works**, privo di autenticazione, che non protegge dall'uomo nel mezzo.

**D:** MIFARE Classic è sicuro?
R: No: il cifrario Crypto1 è rotto, le chiavi si recuperano e il tag si clona (Proxmark autopwn).

**D:** Cosa sono gli advertising packet BLE?
R: Pacchetti broadcast (spesso in chiaro) con cui un device si annuncia prima della connessione.

**D:** Differenza tra RFID LF e HF?
R: LF 125 kHz (EM4100, clonazione triviale) vs HF 13.56 MHz (MIFARE/NFC, più funzioni ma anche
vulnerabilità note).

## Approfondimento livello esperto
Negli assessment IoT il vettore BLE è centrale: spesso le smart lock e i wearable espongono
caratteristiche GATT scrivibili senza autenticazione, permettendo replay di comandi catturati. KNOB
ha mostrato come negoziare entropia della chiave a 1 byte rendendo il brute force banale; LE Secure
Connections (BT 4.2+) mitiga. Sul fronte RFID, oltre a Crypto1, anche alcuni MIFARE Plus configurati
in compatibilità restano deboli; Proxmark3 con `hf mf autopwn` combina nested/darkside/hardnested. La
detection è difficile per la natura passiva dei tag: la difesa è quasi interamente progettuale
(scelta del chip e del protocollo). NFC relay attack (pagamenti, accessi) resta un'area di ricerca
attiva.

## Collegamenti
- [[Fondamenti Wireless e 802.11]] — stesso principio di mezzo broadcast
- [[Wireless Tooling (aircrack-ng, hashcat)]] — strumentazione radio affine
- [[Evil Twin e Rogue AP]] — MITM su radio applicato qui al BLE
- [[Penetration Testing]] — assessment IoT/fisico
- [[Modello OSI]]

## Fonti
- https://book.hacktricks.xyz/todo/radio-hacking/pentesting-ble-bluetooth-low-energy
- https://www.bluetooth.com/specifications/specs/core-specification/
- https://github.com/RfidResearchGroup/proxmark3
