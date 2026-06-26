---
tipo: concetto
tag: [os]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["I/O e Storage"]
---

# I/O e Storage: DMA, RAID, SSD vs HDD

## Definizione
Un OS deve comunicare con i **dispositivi I/O** (dischi, rete, tastiera) in modo efficiente e device-neutral. Un dispositivo canonico espone tre registri: **status**, **command**, **data**. Il protocollo base e: il CPU fa polling dello status (attesa "not busy"), scrive i dati e il comando, attende il completamento. *Crux: come comunicare con i dispositivi e ridurre l'overhead del CPU?* [Fonte: OSTEP, cap. 36]

## Meccanismo: ridurre l'overhead del CPU

### Polling -> Interrupt
Il **polling** spreca cicli CPU in busy-wait. Con gli **interrupt**, il CPU lancia la richiesta, mette il processo a dormire e fa altro; quando il device finisce, solleva un **interrupt** -> il kernel esegue l'handler e risveglia il processo. *Crux: evitare i costi del polling.* (Per device velocissimi a volte il polling resta migliore, perche l'overhead dell'interrupt supera l'attesa.) [Fonte: OSTEP, cap. 36]

### PIO -> DMA
Con **PIO** (programmed I/O) il CPU copia i dati byte/word a mano -> spreco. Il **DMA (Direct Memory Access)** e un motore hardware che trasferisce dati tra dispositivo e memoria **senza coinvolgere il CPU**: il CPU programma il DMA (sorgente, destinazione, lunghezza) e viene interrotto solo a trasferimento finito. *Crux: abbassare l'overhead del PIO.* [Fonte: OSTEP, cap. 36]

### Comunicazione e device driver
Due metodi per parlare coi registri del device: **istruzioni I/O esplicite** (in/out, port-mapped) o **memory-mapped I/O** (registri mappati nello spazio di indirizzi). L'astrazione del **device driver** isola i dettagli del dispositivo dal resto dell'OS -> *device-neutral*. [Fonte: OSTEP, cap. 36]

## HDD (Hard Disk Drive)
Geometria: **piatti** rotanti, **tracce** concentriche, **settori** (512 byte / 4 KB). Il tempo di I/O ha 3 componenti: **seek time** (spostare la testina sulla traccia), **rotational delay** (attendere il settore sotto la testina), **transfer time**. Il seek e il rotational dominano -> gli accessi **sequenziali** sono molto piu veloci dei **random**. Esempi di specs reali (cap. 37): SCSI 15.000 RPM / seek medio 4 ms / ~125 MB/s vs SATA 7.200 RPM / seek 9 ms / ~105 MB/s. Algoritmi di **disk scheduling** (SSTF, SCAN/elevator, C-SCAN) minimizzano i seek. [Fonte: OSTEP, cap. 37]

## SSD (Solid State Drive, flash)
Niente parti mobili: celle **NAND flash**. Proprieta peculiari: [Fonte: OSTEP, cap. 44]
- Si legge/scrive a livello di **pagina**, ma si puo **cancellare solo a livello di blocco** (gruppo di pagine) — e l'erase e lento.
- Una pagina va **cancellata prima di essere riscritta** (no overwrite in-place).
- Le celle si **usurano** (numero limitato di cicli P/E).
- L'**FTL (Flash Translation Layer)** mappa indirizzi logici -> pagine fisiche, tipicamente **log-structured** (scrive sequenzialmente su pagine fresche), con **garbage collection** e **wear leveling** (distribuisce l'usura uniformemente). [Fonte: OSTEP, cap. 44]

### SSD vs HDD
| | HDD | SSD |
|---|---|---|
| Accesso random | lento (seek+rotazione, ms) | **velocissimo** (us, no parti mobili) |
| Sequenziale | buono | ottimo |
| Costo/GB | basso | piu alto |
| Usura | meccanica | celle limitate (P/E cycles) |
| Asimmetria R/W | minima | **scrittura piu costosa** (erase-before-write) |

L'**asimmetria lettura/scrittura** e la necessita di GC/wear-leveling sono ciò che rende l'SSD contro-intuitivo rispetto a un disco "ideale". [Fonte: OSTEP, cap. 44]

## RAID (Redundant Array of Inexpensive Disks)
Combina piu dischi in un unico volume logico per **capacita**, **performance** e **affidabilita**, in modo trasparente al FS. Si valuta su 3 assi: capacita, affidabilita (quanti guasti tollera), prestazioni. [Fonte: OSTEP, cap. 38]

| Livello | Tecnica | Capacita (N dischi) | Tollera guasti | Note |
|---------|---------|---------------------|----------------|------|
| **RAID-0** | striping | N (100%) | **0** | massima banda e capacita, nessuna ridondanza |
| **RAID-1** | mirroring | N/2 | 1 (per coppia) | ogni dato duplicato; letture veloci, costo capacita |
| **RAID-4** | parita dedicata | N-1 | 1 | un disco di parita -> **bottleneck** in scrittura (small-write problem) |
| **RAID-5** | parita **rotante** | N-1 | 1 | parita distribuita su tutti i dischi -> elimina il bottleneck di RAID-4 |

Il **small-write problem** (RAID-4/5): aggiornare un blocco richiede leggere vecchio dato+parita, ricalcolare, riscrivere entrambi (additive/subtractive parity). [Fonte: OSTEP, cap. 38]

## Implicazioni
- La gerarchia di prestazioni (registri > cache > RAM > SSD > HDD > rete) guida ogni decisione di caching/buffering nel FS [[Filesystem]] e nello swap [[Memoria Virtuale]].
- RAID non e un backup: protegge dai guasti hardware, non da cancellazioni/ransomware -> rilevante per la sicurezza.

## Collegamenti
- Vedi anche: [[Filesystem]], [[Memoria Virtuale]], [[Processi]]
- Cross-topic (linux): [[Processi Linux]]

## Fonti
- [OSTEP, cap. 36 "I/O Devices" (DMA, interrupt), p. 419-431]
- [OSTEP, cap. 37 "Hard Disk Drives", p. 433-447]
- [OSTEP, cap. 38 "RAID", p. 449-465]
- [OSTEP, cap. 44 "Flash-based SSDs", p. 563-583]
