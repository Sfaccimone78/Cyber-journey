---
tipo: concetto
tag: [hardware, iot, firmware]
fase: 3
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["Analisi del Firmware", "Firmware Analysis", "Firmware Reversing"]
---

# Analisi del Firmware

## In breve
Il **firmware** è il software che gira sui dispositivi embedded/IoT: bootloader, kernel, filesystem e applicazioni impacchettati in un'unica immagine. La sua analisi cerca segreti hardcoded (password, chiavi, certificati), vulnerabilità nei binari, backdoor e configurazioni deboli. È il passo che segue l'estrazione fisica (vedi [[Hardware Hacking 101]]) o il download dall'aggiornamento OTA. Impatto: da una singola immagine si possono ricavare credenziali valide per un'intera flotta di dispositivi identici.

## Come funziona
Il flusso segue la **OWASP Firmware Security Testing Methodology (FSTM)**:

1. **Ottenere il firmware**: dal sito del vendor (aggiornamenti), intercettando l'update, o estraendolo dalla flash via [[03 Interfacce di Debug (UART, JTAG, SWD)|interfacce di debug]] o desaldando il chip SPI/NAND e leggendolo con un programmatore.
2. **Riconoscere il formato**: `file firmware.bin` e soprattutto **entropia**. Alta entropia costante (≈8 bit/byte) = **cifrato o compresso**; entropia variabile = dati identificabili. `binwalk -E` traccia l'entropia.
3. **Carving/estrazione**: **binwalk** riconosce le firme (magic bytes) di header noti — bootloader (U-Boot), kernel Linux, filesystem (SquashFS, JFFS2, CramFS, UBIFS) — ed estrae il contenuto. `binwalk -e` esegue il carving ricorsivo.
4. **Analisi del filesystem estratto**: si esplora il rootfs come un normale Linux.
   - Credenziali: `/etc/passwd`, `/etc/shadow`, chiavi in `/etc/ssl`, `/etc/dropbear`.
   - Configurazioni e script di avvio (`/etc/init.d`, `rcS`).
   - Binari custom da fare in reverse (vedi [[Analisi Statica con Ghidra]]).
   - Segreti hardcoded: cerca `password`, `key`, `token`, `BEGIN RSA`, URL, API endpoint.
5. **Analisi dei binari**: architettura (spesso ARM/MIPS), librerie datate con CVE note, funzioni pericolose (`system`, `strcpy`), servizi di rete.
6. **Emulazione**: eseguire il firmware o singoli binari senza l'hardware con **QEMU** / **FirmAE** / **Firmadyne** per testare i servizi di rete a runtime (fuzzing, exploit) — cross-architettura tramite `qemu-user`.

Il concetto chiave è che il firmware è "un piccolo Linux (o RTOS) in scatola": una volta aperto il filesystem, valgono le stesse tecniche del pentest di un host.

## Esempi
Riconoscimento ed estrazione:
```bash
file firmware.bin
binwalk firmware.bin              # elenca le firme trovate
binwalk -E firmware.bin           # grafico di entropia (cifrato vs no)
binwalk -e firmware.bin           # estrazione (carving)
binwalk -Me firmware.bin          # estrazione ricorsiva "matryoshka"
```
Caccia ai segreti nel rootfs estratto:
```bash
cd _firmware.bin.extracted/squashfs-root
grep -rniE "password|passwd|api[_-]?key|secret|BEGIN RSA" . 2>/dev/null
cat etc/shadow etc/passwd
find . -name "*.pem" -o -name "*.key"
```
Identificazione ed emulazione di un binario:
```bash
file usr/sbin/httpd            # es. ELF 32-bit MIPS
qemu-mips-static -L . usr/sbin/httpd --help   # emulazione user-mode
```
Cracking di eventuali hash trovati con [[John the Ripper]] / [[Hashcat]]:
```bash
john --wordlist=rockyou.txt shadow.txt
```

## Mitigazione e difesa
Per chi progetta dispositivi, in ordine di efficacia:
1. **Niente segreti hardcoded**: nessuna password/chiave uguale su tutti i dispositivi; usare credenziali per-device e secure element per le chiavi.
2. **Secure boot + firmware firmato**: la CPU verifica la firma prima di eseguire, impedendo firmware modificato.
3. **Cifratura dell'immagine** a riposo e degli update, con anti-rollback (contatore di versione) per bloccare downgrade a versioni vulnerabili.
4. **Aggiornare le librerie**: eliminare componenti open source con CVE note (BusyBox, OpenSSL, kernel datati).
5. **Rimuovere debug e servizi non necessari** dal build di produzione (telnet, shell di root, tool di sviluppo).
6. **Update OTA sicuri**: canale TLS, verifica firma lato dispositivo, e distribuzione tempestiva delle patch.

## Lab
- **binwalk su un firmware reale**: scarica un aggiornamento dal sito di un vendor di router SOHO, esegui `binwalk -Me`, monta il rootfs e cerca credenziali/certificati. Documenta ogni finding.
- **[[HackTheBox]]** → traccia *IoT / firmware* delle challenge o percorso Hardware/embedded: pratica estrazione ed emulazione in ambiente legale.
- **OWASP IoTGoat / Damn Vulnerable Router Firmware (DVRF)**: firmware volutamente vulnerabili pensati per allenare estrazione, analisi ed emulazione end-to-end.
- **Emulazione con FirmAE/QEMU**: prendi un firmware Linux embedded ed emulane l'interfaccia web per testarla come un'app web normale.

## Domande
1. **D:** Cosa indica un'entropia costante prossima a 8 bit/byte su tutta l'immagine?  **R:** Che il firmware è probabilmente cifrato o compresso, quindi non direttamente estraibile con carving.
2. **D:** A cosa serve binwalk?  **R:** A riconoscere le firme (magic bytes) dei componenti nell'immagine ed estrarli (bootloader, kernel, filesystem) tramite carving.
3. **D:** Quali file cerchi per primi in un rootfs estratto e perché?  **R:** `/etc/passwd`, `/etc/shadow` e le chiavi in `/etc/ssl` o `/etc/dropbear`, perché contengono credenziali e materiale crittografico spesso hardcoded.
4. **D:** Perché si emula il firmware con QEMU?  **R:** Per eseguire binari/servizi di rete senza l'hardware fisico, permettendo test dinamici, fuzzing ed exploit cross-architettura.
5. **D:** Qual è la difesa più efficace contro l'esecuzione di firmware modificato?  **R:** Secure boot con firmware firmato: la verifica della firma prima dell'esecuzione blocca immagini alterate.

## Collegamenti
- [[Hardware Hacking 101]] — come si ottiene l'immagine dalla flash
- [[03 Interfacce di Debug (UART, JTAG, SWD)]]
- [[05 Attacchi ai Dispositivi IoT]]
- [[Analisi Statica con Ghidra]] — reversing dei binari estratti
- [[John the Ripper]] · [[Hashcat]] — cracking degli hash trovati

## Fonti
- OWASP Firmware Security Testing Methodology (FSTM): https://scriptingxss.gitbook.io/firmware-security-testing-methodology/
- binwalk (GitHub): https://github.com/ReFirmLabs/binwalk
- OWASP IoTGoat: https://github.com/OWASP/IoTGoat
- The Hardware Hacking Handbook (O'Flynn, van Woudenberg): https://nostarch.com/hardwarehacking
