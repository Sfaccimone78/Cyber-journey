---
tipo: entita
tag: [blue-team, tool, threat-intel]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["VirusTotal"]

---

# VirusTotal

## Cos'è
**VirusTotal** è un servizio online gratuito (di proprietà di Google) che analizza file, URL, indirizzi IP e hash con oltre 70 motori antivirus e strumenti di sicurezza simultaneamente. Restituisce in pochi secondi un responso aggregato su se un artefatto è malevolo, neutro o sospetto. È lo strumento di primo controllo per qualsiasi analista SOC o ricercatore di sicurezza.

## Uso tipico

Tramite interfaccia web (https://www.virustotal.com):
1. Carica un file sospetto oppure incolla un hash, un IP o un URL.
2. VirusTotal lo confronta con i database di oltre 70 vendor (Kaspersky, CrowdStrike, ESET, ecc.).
3. Mostra il **detection ratio** (es. `42/72`), i nomi dati al malware da ciascun vendor, e metadati come data di prima comparsa.

Tramite API (per automazione):

```bash
curl --request GET \
  --url "https://www.virustotal.com/api/v3/files/{sha256_hash}" \
  --header "x-apikey: TUO_API_KEY"
```

L'API gratuita permette 4 richieste/minuto e 500/giorno.

## Quando si usa
- **[[Analisi Malware di Base]]**: primo controllo su un file sospetto prima di eseguirlo in sandbox
- **[[Triage degli Alert]]**: verifica rapida di un hash o IP trovato nei log [[Splunk]]
- **[[Indicatori di Compromissione (IOC)]]**: conferma se un IOC è già noto alla comunità
- **Ricerca [[Threat Intelligence]]**: sezione "Relations" mostra IP, domini e file correlati

## Note e trucchi
- **Non caricare documenti sensibili**: tutto ciò che carichi è visibile ad altri utenti premium. Per file riservati, usa solo l'hash.
- La scheda **"Behavior"** mostra (se disponibile) il comportamento dinamico analizzato in sandbox — simile ad [[Any.run]].
- La scheda **"Community"** contiene commenti di ricercatori: spesso rivelano il contesto di una campagna.
- Hash utile da calcolare in PowerShell: `Get-FileHash file.exe -Algorithm SHA256`

## Collegamenti
- [[Any.run]]
- [[Analisi Malware di Base]]
- [[Indicatori di Compromissione (IOC)]]
- [[Threat Intelligence]]
- [[Triage degli Alert]]
- [[Splunk]]

## Fonti
- [VirusTotal – Documentazione ufficiale](https://docs.virustotal.com/docs/how-it-works)
- [TryHackMe – Threat Intelligence Tools](https://tryhackme.com/room/threatinteltools)
- [LetsDefend – VirusTotal for SOC Analysts](https://letsdefend.io/blog/virustotal-for-soc-analysts/)
