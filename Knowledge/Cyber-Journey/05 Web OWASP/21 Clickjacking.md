---
tipo: concetto
tag: [web, owasp]
fase: 3
fonti: 3
aggiornato: 2026-06-20
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

## Collegamenti
- [[OWASP Top 10]]
- [[Cross-Site Request Forgery (CSRF)]]
- [[Cookie e JWT]]
- [[Security Misconfiguration]]
- [[HTTP e HTTPS]]

## Fonti
- PortSwigger — Clickjacking: https://portswigger.net/web-security/clickjacking
- OWASP — Clickjacking Defense Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html
- MDN — X-Frame-Options: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
