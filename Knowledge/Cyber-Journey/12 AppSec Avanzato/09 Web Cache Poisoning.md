---
tipo: concetto
tag: [web, owasp, tool]
fase: 4
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["Web Cache Poisoning", "Cache Poisoning", "Cache Deception"]
---

# Web Cache Poisoning

> [!warning] Uso etico
> Avvelenare una cache colpisce **tutti** gli utenti che la condividono: è ad alto impatto e alto rischio collaterale. Eseguilo **solo** su lab dedicati o target in scope, e ripulisci/segnala. Mai su CDN di produzione terza.

## In breve
Il **Web Cache Poisoning** sfrutta le cache condivise (CDN, reverse proxy, cache applicative) per servire una **risposta malevola** a tutti gli utenti successivi. L'attaccante invia una richiesta che (1) influenza la risposta in modo dannoso tramite un input **non incluso nella cache key** (*unkeyed input*) e (2) viene **memorizzata** dalla cache. Ricerca di riferimento: **James Kettle**, "Practical Web Cache Poisoning" (PortSwigger, 2018) e "Web Cache Entanglement" (2020).

## Il concetto chiave: cache key vs unkeyed input
La cache decide se due richieste sono "la stessa" guardando la **cache key** (di solito metodo + host + path + query). Tutto ciò che la risposta usa ma che **non** fa parte della key è **unkeyed**: l'attaccante lo manipola, la cache serve la versione avvelenata a chi richiede la stessa key.
```text
Cache key:    GET /home?x=1   Host: site.com
Unkeyed:      header  X-Forwarded-Host, X-Forwarded-Scheme, X-Host, Cookie, ...
```

## 1. Poisoning via unkeyed header
Molte app riflettono header proxy nella risposta (es. costruzione di URL assoluti). Se l'header è unkeyed:
```http
GET / HTTP/1.1
Host: vuln.lab
X-Forwarded-Host: attacker.com
```
Se la risposta include `<script src="//attacker.com/resource">` (riflessione di X-Forwarded-Host) e viene cachata → **XSS persistente per tutti** finché la cache scade. Strumento per scoprire header unkeyed: **Param Miner** (estensione [[Burp Suite]], di James Kettle).

## 2. Identificare la cacheability
Header di risposta che indicano cache:
```text
X-Cache: hit | miss        Age: 120        Cache-Control: public, max-age=...
CF-Cache-Status: HIT       X-Cache-Hits: 3
```
Per testare senza danneggiare utenti reali: aggiungi un parametro "cache buster" unico (`?cb=12345`) così avveleni solo la *tua* key, poi verifichi il `X-Cache: hit` al secondo invio.

## 3. Cache key flaws (unkeyed query / fat GET)
- **Unkeyed query string**: se la query è esclusa dalla key, `?evil=...` influenza la risposta ma collide con `/`.
- **Unkeyed port / metodo**: alcune cache ignorano la porta o accettano body su GET ("fat GET").
- **Cache parameter cloaking**: parametri duplicati interpretati diversamente da cache e back-end.
```http
GET /?param=safe&excluded_param=<payload> HTTP/1.1   # se excluded_param è unkeyed ma usato dall'app
```

## 4. Web Cache Deception
Inverso del poisoning: si inganna la cache a **memorizzare contenuto dinamico privato** (es. la pagina account della vittima) rendendola accessibile all'attaccante.
```text
# La vittima visita un URL che sembra statico ma serve la sua pagina privata:
https://site.com/account/wallet.css   ← /account è dinamico; ".css" fa cachare la cache come statico
# poi l'attaccante richiede lo stesso URL e legge i dati cachati della vittima
```
Varianti moderne (2022, Omer Gil / "Cached and Confused"): delimitatori di path, normalizzazione divergente tra cache e origin.

## 5. Chaining con request smuggling
Combinato con [[HTTP Request Smuggling]]: si usa il desync per far cachare una risposta arbitraria su una URL popolare → poisoning persistente e mirato anche senza header unkeyed riflessi.

## Impatto
XSS/redirect/defacement **serviti a tutti** gli utenti della cache; furto di dati privati (deception); DoS (cachare una pagina di errore). Impatto di massa da una singola richiesta.

## Come difendersi
1. **Includi nella cache key** tutti gli input che influenzano la risposta (o **non riflettere** header come `X-Forwarded-Host` nel contenuto).
2. **Non cachare contenuto dinamico/personalizzato**; usa `Cache-Control: no-store/private` sulle risposte sensibili.
3. **Normalizza** path e query in modo coerente tra cache e origin (mitiga deception e cloaking).
4. Disabilita header non necessari e il supporto a metodi/parametri inattesi (fat GET).
5. Definisci esplicitamente cosa è cacheable (allow-list di estensioni/percorsi statici), non in base al solo suffisso URL.

## Lab
- PortSwigger — Web cache poisoning (lab: "via unkeyed header", "Web cache poisoning with multiple headers", "Targeted using an unknown header", "via unkeyed query string/param", "Cache key injection", "via fat GET", "via cache parameter cloaking"): https://portswigger.net/web-security/web-cache-poisoning
- PortSwigger — Web cache deception: https://portswigger.net/web-security/web-cache-deception
- James Kettle — "Practical Web Cache Poisoning": https://portswigger.net/research/practical-web-cache-poisoning
- James Kettle — "Web Cache Entanglement: Novel Pathways to Poisoning": https://portswigger.net/research/web-cache-entanglement

## Domande
**D: Differenza tra cache key e unkeyed input?**
R: La **cache key** identifica quale risposta servire dalla cache; un **input unkeyed** (es. un header
non incluso nella key) che però influenza la risposta permette di avvelenare la voce cacheata servita
a tutti gli utenti.

**D: Differenza tra cache poisoning e cache deception?**
R: Il **poisoning** inietta contenuto malevolo nella cache condivisa; la **deception** inganna la cache
a memorizzare contenuto **privato** di un utente (es. richiedendo `/account/profilo.css`) leggibile poi
da altri.

**D: Come ci si difende?**
R: Includere nella cache key **tutti** gli input che influenzano la risposta, normalizzare gli input,
e non cacheare contenuto dinamico/privato (header `Cache-Control` corretti).

## Collegamenti
- [[HTTP Request Smuggling]]
- [[Cross-Site Scripting (XSS)]]
- [[CORS Misconfiguration]]
- [[Burp Suite]]
- [[OWASP Top 10]]

## Fonti
- PortSwigger — Web cache poisoning: https://portswigger.net/web-security/web-cache-poisoning
- James Kettle — Practical Web Cache Poisoning (PortSwigger Research): https://portswigger.net/research/practical-web-cache-poisoning
- James Kettle — Web Cache Entanglement: https://portswigger.net/research/web-cache-entanglement
- Omer Gil — Web Cache Deception Attack: https://portswigger.net/web-security/web-cache-deception
