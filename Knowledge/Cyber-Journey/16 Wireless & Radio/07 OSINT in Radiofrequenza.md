---
tipo: concetto
tag: [hardware, osint, radio]
fase: 3
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["OSINT in Radiofrequenza"]
---

# OSINT in Radiofrequenza: Tracciamento dei Segnali con Software Defined Radio (SDR)

## In breve
L'**OSINT in radiofrequenza** intercetta e analizza in modo *passivo* i segnali wireless dello spettro elettromagnetico per raccogliere informazioni su aerei, navi, IoT e infrastrutture. La tecnologia **Software Defined Radio (SDR)** — un dongle economico come l'**RTL-SDR** (500 kHz–1.75 GHz) più software come GQRX/SDR# — ha reso accessibile catturare, visualizzare (FFT + waterfall) e decodificare protocolli di telemetria non cifrati: **ADS-B** (aerei, 1090 MHz), **AIS** (navi, VHF) e reti **POCSAG/FLEX** (cercapersone). Rimanere sulle bande pubbliche non cifrate è la chiave per operare nella legalità.

L'Open Source Intelligence (OSINT) in Radiofrequenza (RF) comporta l'intercettazione e l'analisi di segnali wireless trasmessi attraverso lo spettro elettromagnetico per raccogliere informazioni su navi, aerei, dispositivi IoT o infrastrutture. Storicamente, questo richiedeva ricevitori radio specializzati e costosi. Oggi, la tecnologia Software Defined Radio (SDR) consente agli investigatori di utilizzare dongle USB economici e software per catturare, visualizzare e decodificare un'ampia gamma di segnali radio.

## L'Hardware: RTL-SDR e Antenne

Lo strumento più popolare per l'OSINT RF è l'**RTL-SDR**, un dispositivo originariamente progettato per la ricezione televisiva DVB-T. È stato scoperto che il chip Realtek RTL2832U poteva emettere campioni I/Q grezzi, consentendogli di funzionare come un ricevitore software-defined a banda larga.

Un RTL-SDR copre tipicamente una gamma di frequenze da **500 kHz a 1.75 GHz**, che comprende la radio AM/FM standard, le onde corte, le bande VHF/UHF, le comunicazioni marittime e i transponder dell'aviazione.

Per catturare i segnali con successo, l'abbinamento dell'antenna alla frequenza bersaglio è cruciale. Ad esempio:
- **Antenne a Dipolo Telescopiche**: Buone per la scansione generale. La regolazione della lunghezza degli elementi consente la sintonizzazione su bande specifiche.
- **Antenne Yagi-Uda**: Altamente direzionali, utili per puntare segnali distanti o deboli.
- **Loop Attivi**: Migliori per le bande a bassa frequenza come le HF/Onde Corte.

## Nozioni Base sulle RF e Visualizzazione del Segnale

La comunicazione radio si basa sulla modulazione di un'onda portante ad alta frequenza con un segnale di informazione. I principali tipi di modulazione includono:
- **Modulazione di Ampiezza (AM)**: L'ampiezza dell'onda portante varia con il segnale.
- **Modulazione di Frequenza (FM)**: La frequenza dell'onda portante varia.
- **Modulazione Digitale (ASK, FSK, PSK)**: Impiega variazioni discrete di ampiezza, frequenza o fase per trasmettere dati binari (0 e 1).

I software SDR (come **GQRX** su Linux/macOS o **SDR#** su Windows) elaborano campioni I/Q per visualizzare lo spettro radio. L'interfaccia tipicamente presenta due display principali:
1. **Analizzatore di Spettro FFT**: Mostra la forza del segnale (ampiezza) sull'asse verticale rispetto alla frequenza sull'asse orizzontale in tempo reale.
2. **Display Waterfall (Cascata)**: Traccia la frequenza nel tempo, dove l'intensità del colore rappresenta la potenza del segnale. Questo consente agli investigatori di vedere la durata, la larghezza di banda e la struttura di una trasmissione.

Ad esempio, una trasmissione FM standard a banda stretta appare come un blocco colorato solido che fluttua in larghezza con l'audio, mentre un segnale digitale a spostamento di frequenza (FSK) si presenta come due tracce parallele che si spostano avanti e indietro.

## Segnali OSINT RF Decodificabili

Diversi protocolli open-source trasmettono dati di telemetria non crittografati che possono essere intercettati per le indagini OSINT.

### 1. ADS-B (Tracciamento Aereo)
L'Automatic Dependent Surveillance-Broadcast (ADS-B) viene utilizzato da aerei commerciali e privati per trasmettere la loro posizione GPS, altitudine, velocità e numero di volo a **1090 MHz**. Collegando un RTL-SDR ed eseguendo strumenti come `dump1090`, un investigatore può mappare le posizioni degli aerei locali senza affidarsi a servizi web-based come Flightradar24, che potrebbero censurare i voli militari o privati.

```bash
dump1090 --interactive --net
```

### 2. AIS (Tracciamento Marittimo)
L'Automatic Identification System (AIS) è l'equivalente marittimo dell'ADS-B. Le navi trasmettono la loro identità, carico, velocità e rotta sui canali VHF 87B e 88B (**161.975 MHz** e **162.025 MHz**). L'intercettazione dei segnali AIS vicino alle coste fornisce i movimenti delle navi in tempo reale e può aiutare a tracciare le imbarcazioni che hanno disattivato il tracciamento satellitare.

### 3. Reti Cercapersone (POCSAG)
Le reti cercapersone (pager) sono ancora operative in molte aree per servizi di emergenza, sistemi industriali e messaggistica ospedaliera. Utilizzano comunemente i protocolli POCSAG o FLEX sulle bande VHF/UHF. Indirizzando l'audio da GQRX a un decodificatore come `multimon-ng`, gli investigatori possono catturare i messaggi cercapersone non crittografati:

```bash
rtl_fm -f 466.075M -s 22050 | multimon-ng -t raw -a POCSAG512 -a POCSAG1200 -f alpha -
```

## Considerazioni Legali ed Etiche

Mentre l'OSINT RF è passivo e non trasmette segnali (il che violerebbe le normative sulle radio come quelle della FCC o le leggi locali sulle licenze), la legalità dell'ascolto di certe bande varia. In alcune giurisdizioni, decrittografare o intercettare comunicazioni private (come reti cellulari o radio delle forze dell'ordine) è illegale. Gli investigatori dovrebbero concentrarsi sulle bande di telemetria pubbliche e non crittografate (ADS-B, AIS, satelliti meteorologici) per rimanere conformi alla legge.

## Lab
- **RTL-SDR + dump1090 (ADS-B)** — con un dongle RTL-SDR sintonizza 1090 MHz ed esegui `dump1090 --interactive --net`: mappa in locale i voli senza dipendere da servizi web. Guida di riferimento: https://www.rtl-sdr.com/adsb-aircraft-radar-with-rtl-sdr/.
- **WebSDR** — https://websdr.org/: ricevitori SDR pubblici accessibili dal browser, per esercitarsi a leggere spettro e waterfall e identificare modulazioni (AM/FM/FSK) **senza hardware**.
- **GQRX + multimon-ng (POCSAG)** — instrada l'audio demodulato a `multimon-ng` (`rtl_fm -f 466.075M -s 22050 | multimon-ng -t raw -a POCSAG512 -a POCSAG1200 -f alpha -`) per decodificare messaggi cercapersone non cifrati, ove legale.
- **Signal Identification Guide (sigidwiki)** — https://www.sigidwiki.com/: confronta un segnale sconosciuto catturato nel waterfall con la libreria di firme note.

> [!warning] Etica e legalità
> L'ascolto RF è passivo, ma **decrittare o intercettare comunicazioni private** (cellulari, radio
> delle forze dell'ordine) è illegale in molte giurisdizioni. Limitati alle bande di telemetria
> pubbliche e non cifrate (ADS-B, AIS, meteo). Vedi [[Sicurezza Operativa per le Indagini OSINT]].

## Domande
1. **D:** Cos'è un RTL-SDR e quale gamma di frequenze copre tipicamente?  **R:** Un dongle USB nato per la TV DVB-T (chip Realtek RTL2832U) che, emettendo campioni I/Q grezzi, funziona da ricevitore software-defined a banda larga, coprendo circa **500 kHz – 1.75 GHz** (AM/FM, HF, VHF/UHF, marittimo, aviazione).
2. **D:** A cosa servono il display FFT e il waterfall nei software SDR?  **R:** L'**FFT** mostra ampiezza (potenza) vs frequenza in tempo reale; il **waterfall** traccia la frequenza nel tempo con il colore = potenza, rivelando durata, larghezza di banda e struttura di una trasmissione.
3. **D:** Cosa sono ADS-B e AIS e su quali frequenze si trovano?  **R:** **ADS-B** è la telemetria degli aerei (posizione GPS, quota, volo) a **1090 MHz**; **AIS** è l'equivalente marittimo (identità, rotta, velocità) sui canali VHF 87B/88B (**161.975 / 162.025 MHz**).
4. **D:** Perché l'OSINT RF è considerato passivo e quali sono i limiti legali?  **R:** Perché **riceve** soltanto, senza trasmettere (evitando le violazioni FCC/licenze). Il limite è il *contenuto*: intercettare o decrittare comunicazioni private (cellulari, LE) è spesso illegale; restare su bande pubbliche non cifrate mantiene la conformità.
5. **D:** Perché la scelta dell'antenna conta e quali tipi si usano?  **R:** L'antenna va abbinata alla frequenza bersaglio: **dipolo telescopico** (scansione generale, regolabile), **Yagi-Uda** (direzionale, per segnali deboli/lontani), **loop attivo** (bande basse HF/onde corte).

## Collegamenti
- [[Fondamenti Wireless e 802.11]]
- [[Bluetooth, BLE e RFID-NFC]]
- [[OSINT]]
- [[Sicurezza Operativa per le Indagini OSINT]]

## Fonti
- RTL-SDR — Software Defined Radio: https://www.rtl-sdr.com/
- HackRF — documentation (Great Scott Gadgets): https://hackrf.readthedocs.io/
- Signal Identification Guide (sigidwiki): https://www.sigidwiki.com/
