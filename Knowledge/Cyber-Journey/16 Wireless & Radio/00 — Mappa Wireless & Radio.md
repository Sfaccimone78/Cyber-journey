---
tipo: sintesi
tag: [wireless, moc]
fase: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Wireless & Radio", "Mappa Wireless & Radio"]
---

# Wireless & Radio - Mappa

Area **avanzata/expert** (fase 3) dedicata alla sicurezza delle reti senza fili e dei protocolli
radio a corto raggio. Il filo conduttore parte dalla fisica del mezzo e dalla struttura dei frame
**802.11**, per capire *perché* il wireless è esposto: il canale è condiviso e i frame di management
viaggiano in chiaro. Da qui si sale lo stack di sicurezza (**WEP -> WPA -> WPA2 -> WPA3**), si
studiano gli attacchi pratici contro WPA/WPA2 (cattura dell'**handshake** e **PMKID**), si passa
alla manipolazione attiva del livello 2 (**Evil Twin** e **Rogue AP**), si formalizza il toolkit
(aircrack-ng, hashcat) e si chiude con i protocolli radio non-WiFi (**Bluetooth/BLE**, **RFID/NFC**)
che condividono lo stesso problema di fondo.

**Filo conduttore:** prima capisci *come è fatto un frame* ([[Fondamenti Wireless e 802.11]]), poi
*come si protegge* ([[WEP, WPA, WPA2 e WPA3]]); quindi *come si rompe* la PSK
([[Attacchi WPA2 (handshake e PMKID)]]) e *come si impersona* la rete
([[Evil Twin e Rogue AP]]); infine standardizzi gli strumenti
([[Wireless Tooling (aircrack-ng, hashcat)]]) ed estendi il discorso oltre il WiFi
([[Bluetooth, BLE e RFID-NFC]]).

## Percorso in ordine d'apprendimento

1. [[Fondamenti Wireless e 802.11]] — frame 802.11, banda 2.4/5 GHz, monitor mode, management frame
2. [[WEP, WPA, WPA2 e WPA3]] — evoluzione della cifratura, IV, TKIP, CCMP, SAE
3. [[Attacchi WPA2 (handshake e PMKID)]] — 4-way handshake, cattura EAPOL, PMKID clientless
4. [[Evil Twin e Rogue AP]] — AP fasullo, deauth, captive portal, KARMA
5. [[Wireless Tooling (aircrack-ng, hashcat)]] — suite aircrack-ng, hcxtools, hashcat -m 22000
6. [[Bluetooth, BLE e RFID-NFC]] — pairing, GATT, sniffing BLE, clonazione RFID/NFC

## Collegamenti trasversali
- [[Modello OSI]] — il wireless vive su L1/L2, ma gli attacchi risalgono tutto lo stack
- [[Penetration Testing]] — metodologia generale in cui inquadrare l'assessment WiFi

## Navigazione
[[00 — Mappa Mobile Security|15 Mobile Security]] <- [[index|Indice]] -> [[00 — Mappa API e GraphQL Security|17 API e GraphQL Security]]
