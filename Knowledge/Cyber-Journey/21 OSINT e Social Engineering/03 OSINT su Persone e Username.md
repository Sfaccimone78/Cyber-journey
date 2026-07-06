---
tipo: concetto
tag: [osint, recon, persone]
fase: 3
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["OSINT su Persone", "OSINT su Username", "Sockpuppet Search", "People OSINT"]
---

# OSINT su Persone e Username

## In breve
L'OSINT su persone raccoglie e correla informazioni pubbliche su un individuo: nomi, email, username, numeri di telefono, foto, profili social e luoghi. È il cuore della ricognizione [[OSINT]] a supporto del [[Social Engineering e Phishing|social engineering]], delle indagini e del bug bounty. Il concetto chiave è la **correlazione tra identità**: le persone riusano lo stesso username, la stessa email e le stesse foto su piattaforme diverse, creando un filo che collega account apparentemente separati. Impatto: da un singolo dato (un'email o un nickname) si può ricostruire un intero profilo digitale.

## Come funziona
Il processo è iterativo — ogni dato trovato diventa un nuovo punto di partenza (**pivoting**):

1. **Seed (dato iniziale)**: nome reale, email, username o numero di telefono.
2. **Enumerazione username**: lo stesso *handle* riappare su decine di piattaforme. Strumenti come **Sherlock**, **Maigret** o **WhatsMyName** interrogano centinaia di siti verificando dove quell'username esiste.
3. **Correlazione email**:
   - **Breach data**: verificare se l'email compare in data breach noti (es. *Have I Been Pwned* indica *dove*, non le password).
   - **Enumerazione account**: molte piattaforme rivelano se un'email è registrata tramite la funzione "recupero password" o "registrati" (account enumeration).
   - **Formato aziendale**: dedurre lo schema `nome.cognome@azienda.com` da un solo esempio per generare altre email valide.
4. **Telefono**: reverse lookup, app di rubrica condivisa, verifica su servizi di messaggistica.
5. **Immagini**: la **reverse image search** (Yandex, Google Lens, TinEye, PimEyes per i volti) trova dove una foto è stata pubblicata altrove — utile per smascherare foto profilo riciclate.
6. **Metadati (EXIF)**: le foto pubblicate possono contenere modello di fotocamera, data/ora e persino coordinate GPS (geolocalizzazione).
7. **Social**: relazioni, luoghi, orari, abitudini ricavati da post, tag e check-in.

L'OPSEC dell'investigatore è prerequisito, non optional: vedi [[Sicurezza Operativa per le Indagini OSINT]] (sock puppet, isolamento, prevenzione dell'attribuzione).

## Esempi
Enumerazione di un username su molte piattaforme:
```bash
# Sherlock — cerca "jdoe" su centinaia di siti
python3 sherlock.py jdoe

# Maigret — report ricco con estrazione di dati collegati
maigret jdoe --html
```
Verifica di un'email in breach noti (via API di Have I Been Pwned):
```bash
curl -s -H "hibp-api-key: $HIBP_KEY" \
  "https://haveibeenpwned.com/api/v3/breachedaccount/target@example.com"
```
Estrazione di metadati EXIF da un'immagine scaricata:
```bash
exiftool foto.jpg | grep -iE "GPS|Date|Model|Software"
```
Deduzione di email aziendali da un pattern noto (`n.cognome@azienda.com`):
```bash
# genera candidati da una lista di nomi cognomi
awk '{print substr($1,1,1)"."$2"@azienda.com"}' persone.txt
```

## Mitigazione e difesa
Per ridurre la propria superficie OSINT (utile per chi difende dirigenti o sé stesso):
1. **Igiene degli username**: non riusare lo stesso handle su account sensibili e su quelli pubblici — spezza la correlazione.
2. **Email separate** per registrazioni ad alto rischio; alias usa-e-getta per servizi minori.
3. **Rimuovere/limitare i metadati**: la maggior parte dei social spoglia l'EXIF, ma non tutti i canali (email, file su cloud) lo fanno.
4. **Impostazioni privacy** restrittive su liste amici, tag, check-in di posizione.
5. **Data-broker opt-out**: richiedere la rimozione dai siti aggregatori di dati personali.
6. **Monitorare i breach** (HIBP) e ruotare le credenziali riutilizzate; abilitare l'**MFA** (autenticazione a più fattori) ovunque.

## Lab
- **[[TryHackMe]]** → percorso *OSINT* (room introduttive su ricerca di persone e username): pratica l'enumerazione di handle e la correlazione tra profili in ambiente guidato.
- **OSINT CTF pubblici / Trace Labs Search Party**: sfide legali su target fittizi o persone scomparse (con autorizzazione) che allenano il pivoting reale.
- **Esercizio etico su te stesso**: parti dal tuo username preferito ed esegui `sherlock`/`maigret`; verifica con reverse image search dove appaiono le tue foto profilo. Osserva quanta correlazione emerge.

## Domande
1. **D:** Cos'è il "pivoting" nell'OSINT su persone?  **R:** Usare ogni dato trovato (email, username, foto) come nuovo punto di partenza per scoprire altre informazioni collegate.
2. **D:** Perché il riuso dello stesso username è un rischio?  **R:** Permette di correlare account su piattaforme diverse riconducendoli alla stessa persona.
3. **D:** A cosa serve la reverse image search in un'indagine?  **R:** A trovare dove una stessa immagine (es. foto profilo) è stata pubblicata altrove, smascherando identità false o collegando profili.
4. **D:** Che informazione può nascondersi nei metadati EXIF di una foto?  **R:** Modello di fotocamera, data/ora e talvolta le coordinate GPS del luogo dello scatto.
5. **D:** Have I Been Pwned rivela le password trapelate?  **R:** No: indica in quali breach compare un'email/account, non le password in chiaro.

## Collegamenti
- [[Sicurezza Operativa per le Indagini OSINT]] — prerequisito OPSEC
- [[02 Motori di Ricerca e Google Dorking]]
- [[04 OSINT su Domini e Infrastruttura]]
- [[Social Engineering e Phishing]] — dove finiscono i dati raccolti
- [[OSINT]]

## Fonti
- Michael Bazzell — IntelTechniques / OSINT Techniques: https://inteltechniques.com/
- Bellingcat — Online Investigation Toolkit: https://www.bellingcat.com/
- Sherlock Project (GitHub): https://github.com/sherlock-project/sherlock
- Have I Been Pwned — API v3: https://haveibeenpwned.com/API/v3
