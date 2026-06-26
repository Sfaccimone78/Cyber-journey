---
tipo: concetto
tag: [blue-team]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Indicatori di Compromissione (IOC)"]

---

# Indicatori di Compromissione (IOC)

## In breve
Gli **Indicatori di Compromissione** (IOC, *Indicators of Compromise*) sono artefatti digitali che, se trovati in un sistema o nella rete, indicano che è avvenuta o è in corso una compromissione. Sono le "impronte digitali" lasciate da malware, attaccanti o campagne malevole.

## Come funziona
Gli IOC si dividono in categorie principali:

| Tipo | Esempio |
|------|---------|
| **Hash** | MD5/SHA256 di un file malware |
| **Indirizzo IP** | IP di un C2 (Command & Control) |
| **Dominio/URL** | `evil-update.ru/payload.exe` |
| **Chiave di registro** | `HKCU\Software\Malware\persist` |
| **Stringa nel log** | User-Agent anomalo in un log HTTP |
| **Nome file** | `svchost32.exe` nella cartella Desktop |

Gli IOC vengono distribuiti in formati standard come **STIX/TAXII** e consumati da [[SIEM]], firewall, EDR e piattaforme come [[VirusTotal]]. La loro utilità decade nel tempo: un hash cambia a ogni recompilazione del malware.

## Esempio pratico
Dopo un alert, un analista cerca nel [[SIEM]] [[Splunk]] l'hash SHA256 di un eseguibile sospetto:

```spl
index=endpoint file_hash="d41d8cd98f00b204e9800998ecf8427e"
| table host, file_path, user, _time
```

Se l'hash corrisponde a un malware noto (verificato su [[VirusTotal]]), si procede con l'isolamento dell'host e l'apertura di un caso di [[Incident Response]].

## Rilevanza per la sicurezza
Gli IOC sono lo strato più tattico della [[Threat Intelligence]]: permettono di automatizzare il blocco di minacce note e di accelerare il [[Triage degli Alert]]. Vanno però abbinati a indicatori comportamentali (TTP del [[MITRE ATT&CK]]) perché gli attaccanti esperti modificano facilmente hash e IP.

## Collegamenti
- [[Threat Intelligence]]
- [[VirusTotal]]
- [[Any.run]]
- [[Splunk]]
- [[SIEM]]
- [[Triage degli Alert]]
- [[Analisi Malware di Base]]
- [[MITRE ATT&CK]]

## Fonti
- [MITRE ATT&CK – Indicators of Compromise](https://attack.mitre.org/techniques/T1588/)
- [LetsDefend – IOC Analysis](https://letsdefend.io/blog/what-is-ioc/)
- [Splunk Docs – Threat Intelligence Framework](https://docs.splunk.com/Documentation/ESSOC/latest/user/Usetheappinvestigatethreats)
