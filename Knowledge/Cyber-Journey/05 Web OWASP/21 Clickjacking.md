---
tipo: concetto
tag: [web, owasp]
fase: 3
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Clickjacking"]
---

# Clickjacking

> **Nota etica**: dimostrare solo su pagine di test o con autorizzazione.

## In breve
Il **Clickjacking** (UI redress) inganna l'utente facendogli cliccare su elementi di un sito legittimo **nascosto** in un iframe trasparente sopra una pagina-esca. L'utente crede di interagire con la pagina visibile, ma in realtà compie azioni sul sito target (es. cambiare email, autorizzare un pagamento, attivare la webcam).

## Come funziona
L'attaccante incorpora il sito vittima in un `<iframe>` reso invisibile (`opacity:0`) e lo posiziona sopra un pulsante-esca. Quando l'utente clicca l'esca, il clic "passa" all'iframe sottostante, dove è autenticato con i suoi cookie.

## Esempio pratico
```html
<style>
  iframe { position:absolute; top:0; left:0; width:500px; height:500px;
           opacity:0.0001; z-index:2; }
  button { position:absolute; top:300px; left:80px; z-index:1; }
</style>
<button>Vinci un premio!</button>
<iframe src="https://banca.example/trasferisci?to=attacker&amount=1000"></iframe>
```
Il clic su "Vinci un premio!" colpisce in realtà il bottone di conferma trasferimento nell'iframe.

## Mitigazione e difesa
- Header **`Content-Security-Policy: frame-ancestors 'self'`** (standard moderno).
- Header legacy **`X-Frame-Options: DENY`** o `SAMEORIGIN`.
- Cookie di sessione con `SameSite` (vedi [[Cookie e JWT]]) per limitare l'invio cross-site.
- Azioni sensibili protette da re-autenticazione/conferma esplicita.

## Lab
- [[PortSwigger Web Academy]] → categoria **Clickjacking**. Percorso dal livello APPRENTICE:
  - *Basic clickjacking with CSRF token protection* — sovrapporre un iframe trasparente a un'esca.
  - *Clickjacking with form input data prefilled from a URL parameter*.
  - *Exploiting clickjacking vulnerability to trigger DOM-based XSS* e *Multistep clickjacking* (PRACTITIONER).
- Cosa esercitare: costruire la pagina-esca con l'`<iframe>` a bassa opacità (come l'esempio), allineare l'esca al pulsante target, e verificare la difesa con l'header `Content-Security-Policy: frame-ancestors`.

## Domande
1. **D:** In cosa consiste il clickjacking (UI redress)?  **R:** Incorporare il sito vittima in un iframe trasparente sopra una pagina-esca, così che il clic dell'utente sull'esca colpisca in realtà un elemento del sito target dove è autenticato.
2. **D:** Qual è l'header moderno che previene il clickjacking e cosa fa?  **R:** `Content-Security-Policy: frame-ancestors 'self'`: dichiara quali origini possono incorporare la pagina in un frame; con `'self'` solo l'origine stessa.
3. **D:** Che rapporto c'è tra clickjacking e X-Frame-Options?  **R:** `X-Frame-Options: DENY/SAMEORIGIN` è la difesa **legacy** con lo stesso scopo, oggi superata da `frame-ancestors` di CSP ma ancora utile per browser vecchi.
4. **D:** Perché `SameSite` sui cookie aiuta contro il clickjacking?  **R:** Limita l'invio del cookie di sessione nelle richieste cross-site incorniciate, riducendo l'efficacia dell'azione compiuta a insaputa dell'utente.
5. **D:** Perché rendere l'iframe quasi invisibile (`opacity` bassa) invece di nasconderlo del tutto?  **R:** Deve restare cliccabile e ricevere il clic; con `opacity:0.0001` è invisibile all'occhio ma ancora presente e interattivo nel layout.

## Collegamenti
- [[OWASP Top 10]]
- [[Cross-Site Request Forgery (CSRF)]]
- [[Cookie e JWT]]
- [[Security Misconfiguration]]
- [[HTTP e HTTPS]]
- [[PortSwigger Web Academy]]

## Fonti
- PortSwigger — Clickjacking: https://portswigger.net/web-security/clickjacking
- OWASP — Clickjacking Defense Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html
- MDN — X-Frame-Options: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
