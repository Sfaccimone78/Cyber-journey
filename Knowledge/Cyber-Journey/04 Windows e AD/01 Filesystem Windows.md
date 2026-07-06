---
tipo: concetto
tag: [windows]
fase: 1
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Filesystem Windows"]

---

# Filesystem Windows

## In breve
Il filesystem di Windows è la struttura con cui il sistema operativo organizza file e cartelle sul disco. La variante più usata oggi si chiama **NTFS** (New Technology File System) e offre permessi dettagliati, journaling (registro delle operazioni) e supporto a file molto grandi.

## Come funziona
Windows organizza tutto a partire da **lettere di unità** (C:, D:, ecc.). L'unità principale è quasi sempre `C:\`. Da lì si ramificano le cartelle di sistema:

| Percorso | Contenuto |
|---|---|
| `C:\Windows\` | File del sistema operativo |
| `C:\Windows\System32\` | Eseguibili e DLL di sistema (64-bit) |
| `C:\Windows\SysWOW64\` | Eseguibili 32-bit su sistemi 64-bit |
| `C:\Users\<nome>\` | Cartella personale di ogni utente |
| `C:\Program Files\` | Programmi installati (64-bit) |
| `C:\Program Files (x86)\` | Programmi installati (32-bit) |
| `C:\Temp\` o `%TEMP%` | File temporanei |

NTFS supporta i **permessi ACL** (Access Control List): ogni file ha una lista di chi può leggerlo, scriverlo o eseguirlo — vedi [[Utenti e Permessi Windows]].

Esiste anche il concetto di **Alternate Data Streams (ADS)**: un file può nascondere dati extra dentro flussi alternativi (`file.txt:nascosto`), tecnica usata da malware per sfuggire ai controlli.

## Esempio pratico
Un attaccante scarica un file sospetto e lo nasconde in un ADS:

```cmd
echo MalwarePayload > innocente.txt:hidden_stream
dir /r innocente.txt
```

Con `dir /r` si vedono tutti gli stream. Lo strumento **Sysinternals Streams** può rilevarli e rimuoverli.

## Mitigazione e difesa
- Abilitare la **registrazione degli accessi ai file** tramite [[Windows Event Log]] (Event ID 4663).
- Monitorare scritture in `System32` e `Temp` da processi non di sistema.
- Usare strumenti AV/EDR che analizzano gli Alternate Data Streams.
- Limitare i permessi di scrittura nelle cartelle di sistema tramite [[Utenti e Permessi Windows]].

## Approfondimento sicurezza
- **Alternate Data Streams (ADS)**: MITRE **T1564.004** (Hide Artifacts: NTFS File Attributes). Sysmon **Event ID 15** (FileCreateStreamHash) registra la creazione di stream alternativi — segnale ad alta fedeltà di payload nascosto in `file.txt:stream`.
- **Mark-of-the-Web (MotW)**: i file scaricati ricevono lo stream `Zone.Identifier`; la sua rimozione manuale (`Unblock-File` o stream cancellato) su un eseguibile è un segnale di evasione.
- Scritture in `C:\Windows\System32` / `%TEMP%` da processi non di sistema: Sysmon **Event ID 11** (FileCreate); abbinare l'audit NTFS **Event ID 4663** (accesso a oggetto) tramite SACL.

```yaml
title: Creazione di Alternate Data Stream sospetto
logsource: { product: windows, category: file_stream_creation }   # Sysmon EID 15
detection:
  selection:
    TargetFilename|contains: ':'
  filter:
    TargetFilename|endswith: ':Zone.Identifier'
  condition: selection and not filter
level: medium
```

## Lab
- **TryHackMe** — *Windows Fundamentals 1/2/3* (struttura del filesystem, System32, NTFS).
- **TryHackMe** — *Alternate Data Streams* / room di Windows forensics (`MFT`, recupero file).
- **HackTheBox** Academy — *Windows Fundamentals* (NTFS, permessi, ADS).
- Esercizio locale: creare un ADS con `echo payload > file.txt:hidden`, rilevarlo con `dir /r` e `Get-Item file.txt -Stream *`, poi rimuoverlo con Sysinternals `streams.exe -d`.

## Domande
**D: Cos'è un Alternate Data Stream (ADS) e perché interessa la sicurezza?**
R: È un flusso di dati aggiuntivo che NTFS permette di legare a un file (`file.txt:stream`), invisibile in Esplora risorse e a `dir` semplice. I malware lo usano per nascondere payload; si rileva con `dir /r`, `Get-Item -Stream *` o Sysinternals Streams.

**D: A cosa serve lo stream `Zone.Identifier`?**
R: È il Mark-of-the-Web: Windows lo aggiunge ai file scaricati da Internet per attivare i controlli SmartScreen/Protected View. Rimuoverlo (`Unblock-File`) elimina questi controlli ed è un segnale di tentata evasione.

**D: Differenza tra `C:\Windows\System32` e `C:\Windows\SysWOW64`?**
R: Su un Windows a 64 bit, `System32` contiene i binari/DLL a 64 bit, `SysWOW64` quelli a 32 bit (WoW64 = Windows-on-Windows). Il nome è storicamente fuorviante.

**D: Perché NTFS è preferito a FAT32 in contesti enterprise?**
R: NTFS supporta ACL granulari (DACL/SACL), journaling, cifratura (EFS), file > 4 GB, hard link e auditing degli accessi — tutte funzioni assenti in FAT32.

## Collegamenti
- [[Utenti e Permessi Windows]]
- [[Registro di Sistema Windows]]
- [[Windows Event Log]]
- [[Privilege Escalation Windows]]
- [[PowerShell]]

## Fonti
- Microsoft Learn – NTFS overview: https://learn.microsoft.com/en-us/windows-server/storage/file-server/ntfs-overview
- HackTricks – Windows File System: https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation
- Microsoft Learn – Alternate Data Streams: https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-fscc/a82e9105-2405-4e37-b2c3-28c773902d85
