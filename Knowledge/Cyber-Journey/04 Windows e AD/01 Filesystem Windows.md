---
tipo: concetto
tag: [windows]
fase: 1
fonti: 3
aggiornato: 2026-06-20
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
