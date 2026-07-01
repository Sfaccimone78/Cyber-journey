---
tipo: concetto
tag: [hardware, iot]
fase: 3
fonti: 3
aggiornato: 2026-06-29
stato: maturo
aliases: ["Hardware Hacking 101"]
---

# Hardware Hacking 101: Interfacciamento con JTAG e UART per l'Estrazione del Firmware

L'analisi della sicurezza hardware richiede spesso l'estrazione del firmware del dispositivo per analizzarlo in cerca di vulnerabilità, segreti hardcoded o per fare reverse engineering dei suoi protocolli proprietari. Durante l'auditing di hardware IoT ed embedded, le due interfacce fisiche più comuni e accessibili sono UART (Universal Asynchronous Receiver-Transmitter) e JTAG (Joint Test Action Group). Questa guida descrive in dettaglio la metodologia per identificare le configurazioni dei pin (pinout), utilizzare le apparecchiature diagnostiche ed estrarre il firmware dalle schede bersaglio.

## UART: La Console Hardware

UART è un protocollo di comunicazione seriale che consente la trasmissione asincrona di dati tra dispositivi. Nei sistemi embedded, UART è frequentemente utilizzato per esporre una console seriale (come una shell Linux o una console del bootloader come U-Boot) agli sviluppatori per il debug.

### Identificazione della Configurazione dei Pin (Pinout)
Un'interfaccia UART standard richiede quattro pin:
- **TX (Transmit)**: Il pin tramite cui il dispositivo invia i dati seriali.
- **RX (Receive)**: Il pin tramite cui il dispositivo riceve i dati seriali.
- **GND (Ground/Massa)**: Il riferimento di massa comune.
- **VCC (Power/Alimentazione)**: Il pin di alimentazione (solitamente 3.3V o 5V). **Attenzione**: Non collegare mai il VCC del tuo debugger direttamente al VCC della scheda target se la scheda è già alimentata, in quanto ciò può distruggere il chip.

Per identificare questi pin su una scheda a circuito non etichettata:
1. **Trovare GND**: Impostare il multimetro in modalità continuità e toccare un piano di massa noto (come uno schermo o l'involucro dell'USB) con una sonda e i pin dell'header target con l'altra. Un segnale acustico (beep) indica il pin di massa.
2. **Trovare VCC**: Accendere il dispositivo e misurare la tensione dei pin rimanenti rispetto a GND. Il pin VCC mostrerà una tensione costante di 3.3V o 5V.
3. **Trovare TX**: Durante l'avvio del dispositivo, misurare la tensione dei pin rimanenti. Il pin TX fluttuerà rapidamente mentre il dispositivo emette i log di boot, facendo oscillare la lettura del multimetro tra 0V e 3.3V.
4. **Trovare RX**: Il pin RX tipicamente rimarrà a una tensione elevata e stabile (3.3V) o scenderà a 0V e non fluttuerà durante l'avvio.

### Interfacciamento con un Bus Pirate o un Adattatore USB-UART
Una volta identificati, collegare il TX della scheda all'RX dell'adattatore (es. un Bus Pirate o un adattatore FTDI), l'RX della scheda al TX dell'adattatore, e GND a GND. Utilizzare un emulatore di terminale come screen o Minicom per connettersi:

```bash
screen /dev/ttyUSB0 115200
```

Se il baud rate è sconosciuto, è possibile utilizzare strumenti automatizzati o analizzatori logici per misurare l'ampiezza dell'impulso più piccolo nel segnale per determinare la velocità di comunicazione (ad es. 9600, 57600, 115200).

## JTAG: Lo Standard di Debugging

JTAG è un'interfaccia standard del settore utilizzata per testare circuiti integrati ed eseguire il debug di sistemi embedded. A differenza di UART, che si affida a un sistema operativo in esecuzione o a un bootloader per esporre una console, JTAG consente un accesso diretto e a basso livello ai registri della CPU e alla memoria flash.

### Identificazione della Configurazione dei Pin (Pinout)
Un'interfaccia JTAG standard richiede almeno 4 (spesso 5) segnali:
- **TCK (Test Clock)**: Sincronizza le operazioni interne della state machine.
- **TMS (Test Mode Select)**: Controlla le transizioni della state machine JTAG.
- **TDI (Test Data In)**: Inserisce i dati nel chip.
- **TDO (Test Data Out)**: Trasmette i dati in uscita dal chip.
- **TRST (Test Reset)**: Resetta il controller JTAG (opzionale).

Se i pin JTAG non sono etichettati, è possibile utilizzare scanner hardware specializzati come il **JTAGulator** per automatizzare la scoperta del pinout ciclando attraverso le combinazioni e verificando le risposte al boundary-scan.

### Interfacciamento con OpenOCD
OpenOCD (Open On-Chip Debugger) è lo strumento software standard utilizzato per fare da ponte tra il debugger hardware (come un Jlink o un Bus Pirate) e l'interfaccia JTAG del chip bersaglio. Un comando OpenOCD di esempio per connettersi a un target ARM Cortex-M potrebbe apparire così:

```bash
openocd -f interface/ftdi/jtag-lock-pick_arm.cfg -f target/stm32f4x.cfg
```

Una volta connesso, OpenOCD apre un server telnet locale (solitamente sulla porta 4444) attraverso il quale è possibile inviare istruzioni dirette a riga di comando per fermare la CPU ed estrarre il dump della memoria:

```telnet
telnet localhost 4444
> halt
> flash banks
> dump_image firmware_dump.bin 0x08000000 0x100000
```

Questo estrae `0x100000` byte di memoria flash iniziando dall'indirizzo di base `0x08000000` in un file binario sulla macchina host.

## Mitigazioni Difensive

Per proteggere i sistemi embedded dall'estrazione tramite JTAG e UART:
1. **Disabilitare le Interfacce di Debug in Produzione**: Scollegare fisicamente i pad JTAG/UART rimuovendo i resistori da zero ohm o tagliando le tracce sul PCB.
2. **Abilitare la Protezione in Lettura (RDP)**: I moderni microcontrollori consentono agli sviluppatori di impostare dei fuse (RDP Livello 1 o 2) che bloccano permanentemente l'interfaccia JTAG, impedendo la lettura della memoria flash.
3. **Offuscare le Tracce di Debug**: Nascondere vie e pad di debug sotto componenti BGA o strati interni del PCB.


## Collegamenti
- [[Bluetooth, BLE e RFID-NFC]]
- [[Analisi Statica con Ghidra]]
- [[Assembly x86-64 Essenziale]]
- [[OWASP MASVS e MASTG]]

## Fonti
- OWASP — Internet of Things (IoT Top 10): https://owasp.org/www-project-internet-of-things/
- The Hardware Hacking Handbook (O'Flynn, van Woudenberg): https://nostarch.com/hardwarehacking
- OWASP Firmware Security Testing Methodology (FSTM): https://scriptingxss.gitbook.io/firmware-security-testing-methodology/
