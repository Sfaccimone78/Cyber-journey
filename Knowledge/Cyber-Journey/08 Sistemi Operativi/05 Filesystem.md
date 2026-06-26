---
tipo: concetto
tag: [os]
fase: 0
fonti: 2
aggiornato: 2026-06-25
stato: maturo
aliases: ["Filesystem"]
---

# File System: inode, Journaling, ext4, NTFS

## Definizione
Un **file system** organizza i dati su un dispositivo a blocchi in due astrazioni: il **file** (sequenza lineare di byte con un nome) e la **directory** (contenitore che mappa nomi -> riferimenti a file/sottodirectory, formando un albero). Internamente ogni file e identificato da un numero: l'**inode number**. *Crux: come costruire un file system semplice — quali strutture su disco, cosa tracciano, come si accedono?* [Fonte: OSTEP, cap. 39-40]

## Meccanismo

### Layout su disco (very simple file system, vsfs)
Il disco e diviso in blocchi (es. 4 KB) organizzati in regioni: [Fonte: OSTEP, cap. 40]
- **Superblock**: metadati globali del FS (dimensioni, numero di inode/blocchi, magic number).
- **Inode bitmap** e **data bitmap**: tracciano inode e blocchi dati liberi/occupati.
- **Inode table**: array di inode.
- **Data region**: i blocchi di dati veri e propri.

### Inode
L'**inode** (index node) e la struttura di metadati per-file: tipo, dimensione, permessi/proprietario, timestamp, **conteggio dei link**, e i **puntatori ai blocchi dati**. Per supportare file grandi usa uno schema a **puntatori indiretti**: alcuni puntatori diretti + un **puntatore indiretto singolo** (punta a un blocco di puntatori) + **doppio** + **triplo** indiretto (multi-level index). I file piccoli usano solo i diretti -> efficiente; i grandi crescono via indiretti. [Fonte: OSTEP, cap. 40]

### Directory e hard/soft link
Una directory e un file speciale che contiene coppie `(nome, inode number)`. [Fonte: OSTEP, cap. 39]
- **Hard link**: piu nomi puntano allo **stesso inode** -> incrementano il *link count*; il file esiste finche il count > 0. Non attraversano FS diversi.
- **Symbolic (soft) link**: file separato che contiene il **path** di un altro -> puo puntare fuori dal FS, ma si rompe se il target sparisce (dangling). [Fonte: OSTEP, cap. 39]

### FFS — località
Il file system originale UNIX aveva **prestazioni pessime** (blocchi sparsi sul disco). La **Fast File System (FFS)** introduce i **cylinder group** (block group): raggruppa inode e dati correlati vicini sul disco per ridurre i seek; politiche di allocazione che mettono i file di una directory nello stesso gruppo; gestione dei file grandi come eccezione. *Crux: organizzare le strutture su disco per migliorare le prestazioni.* ext2/ext3/ext4 ne ereditano l'impostazione a block group. [Fonte: OSTEP, cap. 41]

### Crash consistency: FSCK e Journaling
Aggiornare un file tocca **3 strutture** (data block, inode, bitmap): non e atomico. Un crash a meta lascia il FS **inconsistente**. *Crux: come aggiornare il disco in modo da sopravvivere ai crash?* [Fonte: OSTEP, cap. 42]
- **FSCK** (file system checker): dopo un crash scandisce *tutto* il FS e ripara le incoerenze (es. inode con link count errato, blocchi allocati ma non referenziati). **Lento** (proporzionale alla dimensione del disco, non al lavoro perso).
- **Journaling (write-ahead logging)** — usato da **ext3/ext4, NTFS, XFS**: prima di modificare le strutture finali, scrive l'intenzione in un **log/journal**. Sequenza: scrivi nel journal il *transaction begin* + i blocchi -> scrivi il *commit* -> poi **checkpoint** (applica alle posizioni finali). Dopo un crash basta **rieseguire (replay)** il log: recovery proporzionale alla dimensione del log, non del disco.
  - **Ordered/metadata journaling**: per ridurre il costo, si journala solo i **metadati** (dati scritti prima, in-place) -> meno doppia scrittura mantenendo la consistenza. E la modalita di default di ext4. [Fonte: OSTEP, cap. 42]
- **LFS (Log-structured File System)**: scrive **tutto sequenzialmente** in un log (ottimo per la banda di scrittura dei dischi); usa una **inode map** e un **checkpoint region** per ritrovare gli inode; richiede **garbage collection** dei segmenti vecchi. Idea ripresa dagli SSD (FTL log-structured). [Fonte: OSTEP, cap. 43]

## Esempio: aprire e leggere /foo/bar
Per leggere `/foo/bar`: leggi l'inode della root -> leggi i suoi dati per trovare `foo` -> leggi l'inode di `foo` -> trova `bar` -> leggi l'inode di `bar` -> leggi i blocchi dati. Sono **molti** accessi I/O sparsi: per questo servono **caching** dei blocchi e località (FFS). [Fonte: OSTEP, cap. 40-41]

## Confronto ext4 vs NTFS (sintesi)
| | ext4 (Linux) | NTFS (Windows) |
|---|---|---|
| Metadati file | **inode** in inode table | record nella **MFT** (Master File Table) |
| Consistenza | **journaling** (ordered, default) | **journaling** ($LogFile) |
| Allocazione | block group (eredita FFS), extents | extents, cluster |
| Extra | extents, delayed allocation | ACL, stream alternati (ADS), compressione |

## Implicazioni
- Gli **stream alternati (ADS)** di NTFS e i permessi/ACL sono rilevanti per la **sicurezza** (occultamento dati, escalation).
- Il *link count* e gli hard link sono spesso sfruttati in attacchi di tipo **symlink/TOCTOU** -> [[Privilege Escalation Linux]].
- Lo storage sottostante (HDD/SSD/RAID) e in [[I/O e Storage]].

## Collegamenti
- Vedi anche: [[I/O e Storage]], [[Memoria Virtuale]], [[Processi]]
- Cross-topic (linux): [[Processi Linux]]
- Cross-topic (sicurezza): [[Privilege Escalation Linux]]

## Fonti
- [OSTEP, cap. 39 "Interlude: Files and Directories", p. 467-491]
- [OSTEP, cap. 40 "File System Implementation" (inode), p. 493-509]
- [OSTEP, cap. 41 "Locality and The Fast File System", p. 511-523]
- [OSTEP, cap. 42 "Crash Consistency: FSCK and Journaling", p. 525-543]
- [OSTEP, cap. 43 "Log-structured File Systems", p. 547-560]
- [The Systems Approach — https://book.systemsapproach.org/]
