---
tipo: entita
tag: [blue-team, tool, sandbox]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Any.run"]

---

# Any.run

## Cos'è
**ANY.RUN** è una sandbox interattiva online per l'analisi dinamica del malware. A differenza di [[VirusTotal]] che esegue analisi automatiche, ANY.RUN permette di interagire in tempo reale con il file sospetto in un ambiente Windows virtuale — si possono cliccare bottoni, aprire documenti, seguire ogni azione del malware mentre avviene. È disponibile gratuitamente con alcune limitazioni.

## Uso tipico

1. Vai su https://app.any.run e carica un file o inserisci un URL.
2. Seleziona il sistema operativo (Windows 7/10/11), la versione di Office, la rete (attiva o simulata).
3. Avvia la sessione: si apre un desktop virtuale interattivo nel browser.
4. Osserva in tempo reale:
   - **Process tree**: gerarchia dei processi avviati (es. `winword.exe` → `cmd.exe` → `powershell.exe`)
   - **Network**: connessioni HTTP/DNS verso C2 server
   - **File system**: file creati, modificati, cancellati
   - **Registry**: chiavi create per la persistenza

Al termine, ANY.RUN genera un report con tutti gli [[Indicatori di Compromissione (IOC)]] estratti automaticamente.

## Quando si usa
- **[[Analisi Malware di Base]]**: analisi dinamica di un eseguibile, script, macro Office o PDF sospetto
- **[[Triage degli Alert]]**: verifica rapida del comportamento di un allegato email segnalato
- **Estrazione IOC**: ricavare IP, domini, hash e chiavi di registro da un malware per alimentare la [[Threat Intelligence]]
- **Formazione**: le sessioni pubbliche sono visibili a tutti — ottimo per studiare campagne reali

## Note e trucchi
- **Piano gratuito**: analisi pubbliche (visibili a tutti), massimo 3 minuti, file fino a 100 MB.
- **Piano Team**: analisi private, 10 minuti, funzioni avanzate (MITM, FakeNet).
- La funzione **"Suricata IDS"** integrata mostra alert di rete durante l'esecuzione.
- Cerca analisi pubbliche esistenti: https://app.any.run/submissions — spesso il malware è già stato analizzato da qualcun altro.
- Per collegare con [[MITRE ATT&CK Navigator]]: il report include i codici ATT&CK delle tecniche osservate.

## Collegamenti
- [[VirusTotal]]
- [[Analisi Malware di Base]]
- [[Indicatori di Compromissione (IOC)]]
- [[Threat Intelligence]]
- [[MITRE ATT&CK Navigator]]
- [[Triage degli Alert]]

## Fonti
- [ANY.RUN – Documentazione ufficiale](https://any.run/cybersecurity-blog/malware-analysis-with-any-run/)
- [TryHackMe – MAL: REMnux – The Redux](https://tryhackme.com/room/malremnuxv2)
- [LetsDefend – Dynamic Malware Analysis](https://letsdefend.io/blog/dynamic-malware-analysis/)
