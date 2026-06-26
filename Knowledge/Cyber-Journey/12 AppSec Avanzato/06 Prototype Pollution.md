---
tipo: concetto
tag: [web, owasp]
fase: 3
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["Prototype Pollution"]
---

# Prototype Pollution

> [!warning] Uso etico
> Sfruttare prototype pollution per XSS/RCE **solo** su lab autorizzati o target in scope. Una pollution che arriva a RCE su un server Node è compromissione totale: trattala come tale.

## In breve
**Prototype Pollution** è una vulnerabilità specifica di **JavaScript**. Sfrutta il modello a prototipi del linguaggio: ogni oggetto eredita proprietà da `Object.prototype`. Se l'attaccante riesce a **scrivere su `Object.prototype`** (tramite chiavi come `__proto__`, `constructor.prototype`), inietta proprietà che diventano visibili a **tutti** gli oggetti dell'applicazione. Da lì: bypass logici, [[Cross-Site Scripting (XSS)]] (client-side) o **RCE** (server-side Node.js).

## Perché succede: merge ricorsivo non sicuro
Funzioni che fondono input utente in un oggetto senza filtrare le chiavi speciali:
```javascript
function merge(target, source) {
  for (let key in source) {
    if (typeof source[key] === 'object')
      merge(target[key], source[key]);     // ricorre dentro __proto__ → scrive sul prototipo
    else
      target[key] = source[key];
  }
}
// input attaccante (JSON):
merge({}, JSON.parse('{"__proto__":{"isAdmin":true}}'));
({}).isAdmin;   // → true  (TUTTI gli oggetti ora "sono admin")
```

## Client-side (DOM prototype pollution → XSS)
La sorgente è di solito la **query string/hash** parsata in modo ingenuo; la sink è un gadget che legge una proprietà non impostata e la usa in modo pericoloso.
```text
# Sorgente: ?__proto__[hello]=world  oppure  #__proto__[hello]=world
https://vuln.lab/?__proto__[innerHTML]=<img src=x onerror=alert(1)>
# Gadget tipici: librerie che fanno  el[config.transport_url]  o  $.extend / lodash merge
```
Burp DOM Invader (in [[Burp Suite]]) individua sorgenti e gadget automaticamente.

## Server-side (Node.js → da DoS a RCE)
Polluting `Object.prototype` lato server può alterare opzioni passate a funzioni interne. Gadget noti portano a RCE tramite `child_process`:
```text
# se l'app spawna processi, si inietta NODE_OPTIONS / shell
{"__proto__":{"NODE_OPTIONS":"--require /proc/self/environ","env":{...}}}
# gadget classico: pollutare "shell" o gli argv di child_process.spawn/exec
{"constructor":{"prototype":{"argv0":"node","shell":"/bin/sh"}}}
```
Anche template engine (Handlebars, EJS, Pug) hanno gadget che trasformano la pollution in [[SSTI Avanzato e Sandbox Escape|SSTI/RCE]].

## Vettori d'ingresso comuni
- Body JSON fuso con `Object.assign`/lodash `merge`/`_.set`/`$.extend(true,...)`.
- Query string parser (`qs`, parsing custom di `?a[b]=c`).
- Funzioni di "deep clone"/"deep merge" fatte a mano.

## Le tre chiavi magiche
```text
__proto__
constructor.prototype        (es. obj.constructor.prototype.x)
constructor[prototype][x]    (forma annidata, bypassa filtri su "__proto__")
```

## Varianti e bypass
- **Filtro su `__proto__`**: usare `constructor.prototype`.
- **`Object.freeze(Object.prototype)`** bypassato puntando ad altri prototipi (`Array.prototype`, prototipi di classi specifiche).
- **Pollution persistente** server-side che condiziona richieste successive di altri utenti.

## Impatto
- **Client**: DOM XSS, bypass di sanitizzazione, manomissione logica.
- **Server**: privilege escalation logica (es. `isAdmin:true`), DoS, e nei casi peggiori **RCE** sul server Node.

## Come difendersi
1. **Filtra le chiavi** `__proto__`, `constructor`, `prototype` negli input e nei merge.
2. Usa **`Object.create(null)`** per oggetti "map" senza prototipo, o **`Map`** invece di oggetti plain.
3. **`Object.freeze(Object.prototype)`** come hardening (non risolve tutto).
4. Valida l'input con **schema** (es. JSON Schema) e librerie di merge sicure aggiornate.
5. Evita deep-merge fatti a mano; preferisci librerie patchate (lodash ≥ 4.17.21).

## Lab
- PortSwigger — Prototype pollution (lab client-side via browser API, via flawed sanitization, via Object.defineProperty; server-side via JSON input, scanning for properties, RCE via child_process): https://portswigger.net/web-security/prototype-pollution
- PortSwigger — Server-side prototype pollution: https://portswigger.net/web-security/prototype-pollution/server-side
- HackTricks — Prototype Pollution: https://book.hacktricks.xyz/pentesting-web/deserialization/nodejs-proto-prototype-pollution

## Collegamenti
- [[Cross-Site Scripting (XSS)]]
- [[SSTI Avanzato e Sandbox Escape]]
- [[Insecure Deserialization Avanzata (gadget chains)]]
- [[Burp Suite]]
- [[OWASP Top 10]]

## Fonti
- PortSwigger — Prototype pollution: https://portswigger.net/web-security/prototype-pollution
- Gareth Heyes (PortSwigger) — "Server-side prototype pollution: Black-box detection without the DoS": https://portswigger.net/research/server-side-prototype-pollution
- OWASP — Prototype Pollution Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html
- HackTricks — NodeJS Prototype Pollution: https://book.hacktricks.xyz/pentesting-web/deserialization/nodejs-proto-prototype-pollution
