---
tipo: concetto
tag: [metodologia]
fase: 2
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["OSINT"]

---

# OSINT

## In breve

**OSINT** (Open Source INTelligence) è la raccolta e l'analisi di informazioni provenienti da fonti *pubblicamente accessibili*: siti web, social network, registri DNS, database di breach, motori di ricerca. Non richiede accesso autorizzato ai sistemi target ed è spesso il primo passo nella fase di [[Ricognizione (Recon)]].

## Come funziona

L'OSINT sfrutta le informazioni che organizzazioni e individui lasciano involontariamente in chiaro. Le principali categorie di fonti:

### Infrastruttura e dominio
- **WHOIS**: chi ha registrato un dominio, quando scade, email del registrante
- **DNS**: record A, MX, TXT, CNAME — rivelano sotto-domini, provider email, CDN usati
- **Certificate Transparency Logs**: tutti i certificati SSL emessi per un dominio (e i suoi sotto-domini)
- **Shodan / Censys**: motori di ricerca per dispositivi esposti su Internet (IP, porte, banner)

### Informazioni sulle persone
- **LinkedIn**: ruoli, tecnologie usate, dipendenti (utile per attacchi di social engineering)
- **Google Dorking**: query avanzate su Google per trovare file esposti, pannelli di login, backup
- **HaveIBeenPwned**: verifica se un'email è presente in data breach pubblici

### Codice e documenti
- **GitHub**: credenziali e chiavi API accidentalmente committate in repository pubblici
- **Metadata di documenti**: file PDF/Office pubblicati sul sito aziendale possono contenere nomi utente, percorsi di rete, versioni software

## Esempio pratico

```bash
# WHOIS di un dominio
whois example.com

# Ricerca sottodomini con certificate transparency
# (usa il sito crt.sh)
curl -s "https://crt.sh/?q=%.example.com&output=json" | jq '.[].name_value' | sort -u

# DNS lookup completo
dig any example.com +noall +answer

# Google Dorking — trovare file di configurazione esposti
# Query da browser: site:example.com filetype:env OR filetype:conf OR filetype:bak

# Ricerca su Shodan (richiede account gratuito)
# Ricerca host: shodan search "apache 2.4 example.com"

# theHarvester — raccoglie email, host, IP da fonti pubbliche
theHarvester -d example.com -b all
```

## Note

> L'OSINT è legale quando si usano fonti pubbliche senza autenticazione a sistemi altrui. Raccogliere dati personali in modo massiccio può comunque violare il GDPR in Europa.

- **Mantenere la distanza**: durante OSINT passivo non interagire direttamente con i sistemi target (non mandare richieste al loro server). Usa strumenti che interrogano database terzi.
- **theHarvester**, **Maltego** e **Recon-ng** sono framework OSINT completi disponibili su [[Kali Linux]].
- I **Google Dork** più utili: `site:`, `filetype:`, `inurl:`, `intitle:`, `"parola esatta"`.
- Shodan è spesso chiamato "il motore di ricerca degli hacker" — mostra banner di servizi, versioni, certificati di miliardi di host.

## Mitigazione e difesa

- Usare WHOIS privacy per nascondere i dati del registrante.
- Controllare regolarmente i propri repository GitHub con tool come `git-secrets` o `truffleHog`.
- Rimuovere i metadata dai documenti prima di pubblicarli (`exiftool -all= file.pdf`).
- Monitorare HaveIBeenPwned per le email aziendali.
- Eseguire periodicamente OSINT sulla propria organizzazione per scoprire esposizioni involontarie.

## Lab

- **[[TryHackMe]] — "OhSINT" e "Sakura Room"**: due room interamente OSINT. In *OhSINT* parti da una singola immagine ed estrai metadata, geolocalizzazione e account collegati; *Sakura Room* è un'indagine OSINT più ampia su un attore reale.
- **[[TryHackMe]] — "Google Dorking"**: pratica gli operatori di ricerca avanzata per trovare risorse esposte.
- **theHarvester su [[Kali Linux]]**: esegui `theHarvester -d <dominio-di-tua-proprietà> -b all` e confronta i risultati con quanto trovi manualmente su `crt.sh` e Shodan, per capire quante fonti aggrega uno strumento automatico.

## Domande

1. **D:** Cosa significa OSINT e su quali fonti si basa?  **R:** Open Source INTelligence: raccolta e analisi di informazioni da fonti pubblicamente accessibili (siti, social, DNS, breach, motori di ricerca).
2. **D:** A cosa servono i Certificate Transparency Logs in fase OSINT?  **R:** A scoprire tutti i certificati SSL emessi per un dominio e quindi anche sotto-domini altrimenti nascosti.
3. **D:** Perché GitHub è una fonte OSINT preziosa?  **R:** Perché sviluppatori committano accidentalmente credenziali e chiavi API in repository pubblici.
4. **D:** Come si rimuovono i metadata da un documento prima di pubblicarlo?  **R:** Con `exiftool -all= file.pdf`.
5. **D:** Quando l'OSINT può comunque violare la legge nonostante usi fonti pubbliche?  **R:** Quando la raccolta massiva di dati personali viola il GDPR in Europa.

## Collegamenti

- [[Ricognizione (Recon)]]
- [[Metodologia del Pentest]]
- [[DNS]]
- [[HTTP e HTTPS]]
- [[Enumerazione]]
- [[Kali Linux]]

## Fonti

- OSINT Framework (raccolta di fonti categorizzate): <https://osintframework.com/>
- HaveIBeenPwned: <https://haveibeenpwned.com/>
- Certificate Transparency — crt.sh: <https://crt.sh/>
- theHarvester — GitHub ufficiale: <https://github.com/laramies/theHarvester>
