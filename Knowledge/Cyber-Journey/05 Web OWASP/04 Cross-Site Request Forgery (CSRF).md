---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 4
aggiornato: 2026-06-28
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

## Approfondimento sicurezza
**SameSite e i suoi limiti.** Dal 2020 i browser impostano `SameSite=Lax` di default sui cookie senza attributo esplicito: questo blocca l'invio cross-site su POST/iframe/AJAX ma **non** sui GET top-level (navigazione diretta). Quindi un'azione sensibile esposta via GET resta CSRF-able anche con Lax di default. `SameSite=Strict` chiude anche quel caso ma rompe i deep-link da siti esterni. Inoltre Lax ha una finestra di **120 secondi** (in Chrome) in cui i cookie nuovi vengono trattati come "None" per compatibilità: una nicchia sfruttabile.

**Bypass dei token (detection).** Pattern tipici: token non legato all'utente (riuso del proprio), token validato solo se presente (drop del parametro), token duplicato in un cookie e confrontato col body (**double-submit** debole se il sottodominio può settare il cookie), e token leakato via `Referer` verso domini terzi. Una difesa robusta è il pattern **synchronizer token** lato sessione o l'header custom (`X-CSRF-Token`) che CORS impedisce di forgiare cross-origin.

**Detection.** Lato server, log delle richieste state-changing con `Origin`/`Referer` esterni al dominio o assenti su endpoint sensibili → segnale. MITRE ATT&CK: il CSRF si colloca in **T1185** (Browser Session Hijacking) come tecnica di abuso della sessione autenticata.

## Lab
- **PortSwigger Web Academy** — [[PortSwigger Web Academy]]: percorso *CSRF* (token mancante/non validato, bypass via metodo, SameSite Lax bypass, Referer validation bypass). Lab gratuiti.
- **TryHackMe** — room *OWASP Top 10* (sezione CSRF) e *Cross-site Request Forgery*.
- **DVWA** — modulo CSRF (cambio password), livelli low→impossible per vedere l'introduzione progressiva del token.

## Domande
**D: Perché il CSRF funziona anche senza rubare il cookie?**
R: Perché sfrutta il fatto che il browser allega **automaticamente** i cookie di sessione a ogni richiesta verso quel dominio, anche se la richiesta parte da un sito attaccante. Non serve leggere il cookie: basta indurre il browser a inviare la richiesta voluta.

**D: Perché un XSS rende inutile ogni difesa CSRF?**
R: Con un XSS l'attaccante esegue JS nell'origine della vittima: può **leggere il token anti-CSRF dal DOM** e forgiare una richiesta perfettamente valida. Per questo l'XSS va chiuso prima: nessun token lo ferma.

**D: SameSite=Lax basta da solo come difesa?**
R: No. Lax non protegge le azioni esposte via **GET top-level** e ha finestre di compatibilità. Va combinato con token anti-CSRF e, idealmente, le azioni sensibili non devono mai cambiare stato via GET.

**D: Perché le API stateless con Bearer token in header sono immuni al CSRF classico?**
R: Perché il token non viene inviato automaticamente dal browser (non è un cookie): va aggiunto esplicitamente in un header via JS, cosa che la same-origin policy impedisce a un sito attaccante. Niente invio automatico, niente CSRF.

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
- PortSwigger — Bypassing SameSite cookie restrictions: https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions
