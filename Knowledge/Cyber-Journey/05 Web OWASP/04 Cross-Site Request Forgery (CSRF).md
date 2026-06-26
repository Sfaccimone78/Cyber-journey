---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 3
aggiornato: 2026-06-21
stato: maturo
aliases: ["Cross-Site Request Forgery (CSRF)", "CSRF"]
---

# Cross-Site Request Forgery (CSRF)

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger Academy, DVWA, TryHackMe).

## In breve
Il **CSRF** inganna il browser della vittima per fargli inviare una richiesta **non voluta** a un'app dove è già autenticata. Il server la accetta come legittima perché il browser **allega in automatico il cookie di sessione**. L'attaccante non ruba il cookie e non vede la risposta: esegue un'**azione** per conto della vittima (cambio password, trasferimento, modifica email).

## Le tre condizioni necessarie
Un endpoint è CSRF-able solo se valgono **tutte e tre**:
1. **Azione rilevante** (cambia stato: modifica account, trasferimento…).
2. **Gestione sessione solo via cookie** inviato in automatico (no token in header).
3. **Parametri prevedibili**: l'attaccante può costruire la richiesta senza segreti.
Togli anche una sola → l'attacco cade. Le difese mirano esattamente a queste.

## Esempio pratico
GET (caso debole — azione sensibile via GET, già errore di design):
```html
<img src="https://banca.it/trasferisci?a=attaccante&importo=1000" width="0">
```
POST (auto-submit appena la vittima apre la pagina):
```html
<form action="https://banca.it/trasferisci" method="POST" id="f">
  <input type="hidden" name="destinatario" value="attaccante">
  <input type="hidden" name="importo" value="1000">
</form>
<script>document.getElementById('f').submit()</script>
```
[[Burp Suite]] genera il PoC: *Engagement tools → Generate CSRF PoC*.

## CSRF vs XSS (non confonderli)
| | CSRF | [[Cross-Site Scripting (XSS)]] |
|---|---|---|
| Dove gira il codice | sul sito **attaccante** | nel sito **vittima** |
| Cosa sfrutta | fiducia del sito nel browser | fiducia del browser nel sito |
| Vede la risposta? | **No** (blind, solo azione) | **Sì** (può leggere DOM/cookie) |

XSS **batte** ogni difesa CSRF: se c'è XSS sul sito, l'attaccante legge il token e forgia la richiesta valida. Prima si chiude l'XSS.

## Bypass comuni delle difese
- Token validato solo se presente → **rimuoverlo** dalla richiesta a volte passa.
- Token legato alla sessione ma non all'utente → riuso del proprio token.
- Validazione del **Referer** aggirabile (referer assente, o substring match debole `banca.it.evil.com`).
- `SameSite=Lax` non copre alcune richieste GET top-level → azioni GET restano esposte.

## Mitigazione (priorità)
1. **CSRF token** anti-forgery: casuale, legato alla sessione, validato server-side (difesa primaria).
2. **`SameSite=Strict/Lax`** sui cookie di sessione → il browser non li manda cross-site. Vedi [[Cookie e JWT]].
3. Verifica **Origin/Referer** come strato aggiuntivo.
4. Richiedere **ri-autenticazione** o conferma per azioni critiche.
5. **API stateless con Bearer token** in header (non cookie) → immuni al CSRF classico.

## Collegamenti
- [[OWASP Top 10]]
- [[Cross-Site Scripting (XSS)]]
- [[Clickjacking]] — UI redress: alternativa al CSRF quando i token bloccano la richiesta
- [[Cookie e JWT]]
- [[Autenticazione e Gestione Sessioni]]
- [[HTTP e HTTPS]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti
- PortSwigger — CSRF: https://portswigger.net/web-security/csrf
- OWASP — CSRF: https://owasp.org/www-community/attacks/csrf
- OWASP — CSRF Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
