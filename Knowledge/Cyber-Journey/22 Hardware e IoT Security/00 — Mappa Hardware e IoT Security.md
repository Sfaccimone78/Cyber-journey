---
tipo: sintesi
tag: [hardware, iot, moc]
fase: 3
aggiornato: 2026-07-01
stato: attivo
aliases: ["Hardware e IoT Security", "Mappa Hardware e IoT Security"]
---

# Hardware e IoT Security - Mappa

Area dedicata alla sicurezza dei **dispositivi fisici** e dell'**Internet of Things**: interfacce di
debug (UART, JTAG, SPI), estrazione ed analisi del **firmware**, e la superficie d'attacco tipica dei
dispositivi embedded, dove il confine tra software e hardware sparisce.

> [!info] Area in espansione
> Al momento contiene la nota introduttiva. Prossime note candidate: dump e analisi del firmware,
> attacchi a UART/JTAG/SPI, side-channel e fault injection, OWASP IoT Top 10 operativo.

## Percorso in ordine d'apprendimento

1. [[Hardware Hacking 101]] — interfacce di debug, estrazione firmware, toolkit di base
2. [[Analisi del Firmware]] — dump, entropia, binwalk, caccia ai segreti nel rootfs, emulazione QEMU/FirmAE

## Collegamenti trasversali
- [[Bluetooth, BLE e RFID-NFC]] — i protocolli radio dei dispositivi IoT
- [[Analisi Statica con Ghidra]] — reversing dei binari estratti dal firmware
- [[OWASP MASVS e MASTG]] — metodologia affine sul mondo mobile

## Navigazione
[[00 — Mappa OSINT e Social Engineering|21 OSINT e Social Engineering]] <- [[index|Indice]] -> [[00 — Mappa Laboratori e CTF|23 Laboratori e CTF]]
