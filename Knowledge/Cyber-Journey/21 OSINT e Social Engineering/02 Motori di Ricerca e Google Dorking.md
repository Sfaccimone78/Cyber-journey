---
tipo: concetto
tag: [osint, recon, dorking]
fase: 3
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["Google Dorking", "Google Hacking", "Motori di Ricerca e Google Dorking", "Search Operators"]
---

# Motori di Ricerca e Google Dorking

## In breve
Il **Google Dorking** (o *Google Hacking*) è l'uso degli operatori di ricerca avanzati per trovare informazioni che sono pubbliche ma non pensate per essere trovate: file sensibili indicizzati, pannelli di login, elenchi di directory, credenziali in chiaro, dispositivi esposti. È una tecnica di [[OSINT]] **passiva** (non tocca il bersaglio) e a costo zero, quindi tipicamente il primo passo della ricognizione. L'impatto è alto: un singolo dork ben costruito può rivelare backup di database, chiavi API o configurazioni che l'organizzazione crede private.

## Come funziona
I motori di ricerca costruiscono un indice invertito del web crawlando i link. Gli **operatori di ricerca** filtrano quell'indice con precisione chirurgica. Su Google i principali sono:

| Operatore | Effetto | Esempio |
|-----------|---------|---------|
| `site:` | limita a un dominio | `site:example.com` |
| `filetype:` / `ext:` | limita a un'estensione | `filetype:pdf`, `ext:sql` |
| `intitle:` / `allintitle:` | parola nel `<title>` | `intitle:"index of"` |
| `inurl:` / `allinurl:` | parola nell'URL | `inurl:admin` |
| `intext:` / `allintext:` | parola nel corpo | `intext:"password"` |
| `cache:` | versione in cache | `cache:example.com` |
| `related:` | siti simili | `related:example.com` |
| `"..."` | corrispondenza esatta | `"internal use only"` |
| `-` | esclude un termine | `login -site:example.com` |
| `OR` / `\|` | alternativa logica | `filetype:pdf OR filetype:docx` |
| `*` | wildcard di parola | `"admin * panel"` |
| `..` | intervallo numerico | `salary 40000..60000` |

**Il paradosso di `robots.txt`**: il file `robots.txt` dice ai crawler cosa NON indicizzare, ma è pubblico e spesso elenca proprio i path sensibili (`/admin`, `/backup`, `/private`). Leggerlo è un dork manuale.

**Altri motori, altre forze**:
- **Bing** ha operatori unici come `ip:` (tutti i siti su un IP) e `feed:` (feed RSS).
- **DuckDuckGo** rispetta molti operatori Google ma con indice diverso: utile per confronto.
- **Yandex** è considerato il migliore per la ricerca inversa di **volti/immagini**.
- **Shodan** e **Censys** non indicizzano pagine ma **dispositivi e servizi** (banner, porte aperte, certificati): sono "motori di ricerca per Internet delle cose". Vedi anche [[04 OSINT su Domini e Infrastruttura]].

Il **Google Hacking Database (GHDB)** su Exploit-DB è il catalogo curato di dork pronti all'uso, categorizzati (file con password, pagine di login, messaggi d'errore, dispositivi online).

## Esempi
Ricognizione base di un'organizzazione:
```text
site:target.com filetype:pdf                # documenti pubblici
site:target.com -www                         # sottodomini indicizzati
site:target.com intitle:"index of"           # directory listing aperte
site:target.com ext:log OR ext:bak OR ext:sql  # log e backup
site:target.com inurl:(login OR admin OR dashboard)
```
Ricerca di segreti e configurazioni esposte (tipici del GHDB):
```text
intitle:"index of" "config.php"
filetype:env "DB_PASSWORD"
filetype:sql "INSERT INTO users"
inurl:wp-content intext:"define('DB_PASSWORD'"
```
Segreti nel codice sorgente (GitHub ha una propria sintassi di ricerca, non Google):
```text
# nella ricerca codice di GitHub
"target.com" AKIA path:.env          # possibili chiavi AWS
org:target-org "BEGIN RSA PRIVATE KEY"
```
Dispositivi esposti su Shodan (sintassi Shodan, non Google):
```text
org:"Target Inc"
http.title:"Login" port:8080
product:"MikroTik"
```

## Mitigazione e difesa
In ordine di efficacia:
1. **Non esporre** file sensibili: la difesa reale è che backup, `.env`, `.sql`, `.bak` non stiano su un web server pubblico.
2. **Autenticazione e autorizzazione** su ogni risorsa riservata: l'indicizzazione è irrilevante se serve login.
3. **Disabilitare il directory listing** (es. `Options -Indexes` in Apache) per eliminare le pagine `index of`.
4. **Meta tag `noindex`** e header `X-Robots-Tag: noindex`: dicono ai crawler di non indicizzare (ma non nascondono la risorsa).
5. **Google Search Console → Removals** per de-indicizzare in fretta contenuti già trapelati; poi rimuovere la risorsa alla fonte.
6. **Monitoraggio proattivo**: eseguire periodicamente i dork sulla propria organizzazione per scoprire esposizioni prima degli attaccanti.

`robots.txt` **non** è una misura di sicurezza: rende pubblici i path che elenca.

## Lab
- **Google Hacking Database (Exploit-DB GHDB)**: sfoglia le categorie e ricostruisci i dork; usali contro un dominio di tua proprietà per capire cosa risulta indicizzato.
- **[[TryHackMe]]** → cerca la room dedicata a *Google Dorking / OSINT* (categoria walkthrough introduttivi): pratica operatori e interpretazione dei risultati in un contesto guidato.
- **Esercizio autonomo**: scegli un dominio con bug-bounty pubblico e mappa in sola lettura sottodomini, documenti e pannelli con `site:` + `inurl:` + `filetype:`, annotando ogni finding.

## Domande
1. **D:** Perché `robots.txt` può aiutare l'attaccante invece di proteggere?  **R:** È pubblico ed elenca esplicitamente i path che il sito vuole tenere fuori dall'indice (es. `/admin`, `/backup`), fornendo una mappa dei percorsi sensibili.
2. **D:** Quale operatore useresti per trovare tutte le pagine PDF di un dominio?  **R:** `site:dominio filetype:pdf` (o `ext:pdf`).
3. **D:** Che differenza c'è tra Google e Shodan nella ricognizione?  **R:** Google indicizza pagine web (contenuti/testo), Shodan indicizza dispositivi e servizi esposti (banner, porte, certificati).
4. **D:** Il tag `noindex` mette al sicuro un file sensibile?  **R:** No: impedisce l'indicizzazione ma la risorsa resta raggiungibile da chiunque conosca l'URL; serve autenticazione o rimozione.
5. **D:** Qual è il modo più efficace per difendersi dal dorking?  **R:** Non esporre affatto i file sensibili e proteggere con autenticazione ogni risorsa riservata.

## Collegamenti
- [[OSINT]] — la ricognizione passiva nel pentest
- [[03 OSINT su Persone e Username]]
- [[04 OSINT su Domini e Infrastruttura]]
- [[05 Framework OSINT (Maltego, SpiderFoot, theHarvester)]]
- [[Social Engineering e Phishing]] — le info raccolte alimentano il pretexting

## Fonti
- Google — Refine web searches (operatori di ricerca): https://support.google.com/websearch/answer/2466433
- Exploit-DB — Google Hacking Database (GHDB): https://www.exploit-db.com/google-hacking-database
- OSINT Framework: https://osintframework.com/
- Bellingcat — Online Investigation Toolkit: https://www.bellingcat.com/
