---
tipo: concetto
tag: [web, owasp, crypto]
fase: 4
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["SAML e SSO Attacks", "SAML Attacks", "SSO Attacks"]
---

# SAML e SSO Attacks

> [!warning] Uso etico
> Manomettere asserzioni SAML e tentare bypass di firma **solo** su lab autorizzati o target in scope. Forgiare l'identità di un altro utente su un IdP/SP reale è accesso abusivo.

## In breve
**SAML** (Security Assertion Markup Language) è lo standard XML per il **Single Sign-On** enterprise. Tre attori: **IdP** (Identity Provider, autentica), **SP** (Service Provider, eroga il servizio), **utente** (browser). L'IdP emette un'**asserzione XML firmata** che attesta l'identità; l'SP la verifica e crea la sessione. Alternativa "enterprise" all'OIDC visto in [[OAuth 2.0 e OpenID Connect Attacks]]; condivide il tema "fidarsi di un token d'identità" con gli [[Attacchi JWT]]. Quasi tutti gli attacchi colpiscono la **verifica della firma XML**, notoriamente fragile.

## Flusso SP-initiated (SAML 2.0 Web Browser SSO)
```text
1. Utente → SP (risorsa protetta)
2. SP → browser: AuthnRequest, redirect all'IdP
3. Utente si autentica sull'IdP
4. IdP → browser: SAMLResponse (asserzione FIRMATA) in un form POST
5. browser → SP/ACS (Assertion Consumer Service): l'SP verifica la firma e logga l'utente
```
La `SAMLResponse` è base64 (a volte deflate+base64 nel binding Redirect). Decodificarla rivela l'XML con `<saml:Assertion>`, `<saml:Subject><saml:NameID>` e `<ds:Signature>`.

## 1. XML Signature Wrapping (XSW)
L'attacco classico. La verifica della firma e l'elaborazione dell'asserzione guardano **nodi diversi** dell'albero XML. Si inserisce un'asserzione malevola (non firmata) tenendo l'originale firmata in una posizione che soddisfa il verificatore ma viene ignorata dal processore.
```xml
<samlp:Response>
  <saml:Assertion ID="evil">            <!-- asserzione attaccante: NameID=administrator -->
    <saml:Subject><saml:NameID>administrator</saml:NameID></saml:Subject>
  </saml:Assertion>
  <saml:Assertion ID="orig">            <!-- asserzione legittima firmata, "nascosta" -->
    <ds:Signature>...firma valida su 'orig'...</ds:Signature>
    <saml:Subject><saml:NameID>guest</saml:NameID></saml:Subject>
  </saml:Assertion>
</samlp:Response>
```
Esistono ~8 varianti XSW (spostare la firma dentro/fuori, duplicare ID, usare `Object`, ecc.). **SAML Raider** (estensione [[Burp Suite]]) le automatizza.

## 2. Firma assente / non richiesta
Se l'SP non *impone* che l'asserzione sia firmata, si rimuove `<ds:Signature>` e si edita liberamente il `NameID`. Variante: firmare la `Response` ma non l'`Assertion` (o viceversa) — manomettere quella non protetta.

## 3. XML Comment injection (truncation)
Alcuni parser XML restituiscono solo il testo *prima* di un commento. Inserendo un commento nel `NameID` si confonde l'SP sull'identità:
```xml
<saml:NameID>admin<!---->@evil.com</saml:NameID>   <!-- l'SP può leggere "admin" -->
```

## 4. XXE nel parsing della SAMLResponse
La SAMLResponse è XML controllato dall'attaccante: se il parser dell'SP non disabilita le entità esterne → [[XML External Entity (XXE)]] (file read, SSRF).
```xml
<!DOCTYPE x [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<samlp:Response>...&xxe;...</samlp:Response>
```

## 5. Replay e Recipient/Audience non validati
- **Replay**: riusare una `SAMLResponse` valida se `NotOnOrAfter`/`OneTimeUse` non sono enforced.
- **Audience/Recipient confusion**: un'asserzione emessa per l'SP-A accettata dall'SP-B se `<AudienceRestriction>`/`Destination` non sono verificati.

## 6. Key confusion / certificato fornito dall'attaccante
Se l'SP accetta il certificato dichiarato nel `<KeyInfo>` della Response invece di una chiave pinnata, l'attaccante allega il *proprio* certificato e firma l'asserzione con la propria chiave privata.

## Tooling
**SAML Raider** (Burp) — decodifica, edit, XSW automatizzate, gestione certificati e self-sign. Estensione "SAML Encoder/Decoder". `xmlsec` per verifiche manuali.

## Impatto
Bypass completo dell'autenticazione SSO → impersonificazione di qualsiasi utente (incluso admin) su tutti gli SP federati, accesso a interi ecosistemi enterprise da un singolo difetto di verifica.

## Come difendersi
1. **Verifica la firma sull'elemento giusto** e processa **solo** ciò che è coperto dalla firma (riferimento per ID, no wrapping). Usa librerie SAML aggiornate e mature, non parsing fatto a mano.
2. **Imponi** che l'asserzione (non solo la Response) sia firmata; rifiuta asserzioni non firmate.
3. **Disabilita le entità esterne** nel parser XML (anti-XXE).
4. Valida `Recipient`/`Destination`, `Audience`, `NotBefore`/`NotOnOrAfter`, `InResponseTo`; impedisci replay (one-time use).
5. **Pinna i certificati IdP**; non fidarti del `<KeyInfo>` fornito nel messaggio.
6. Normalizza/blocca i commenti XML nei valori identità (mitiga il truncation).

## Lab
- PortSwigger — non ha un percorso SAML dedicato; usa i lab [[XML External Entity (XXE)]] e [[Attacchi JWT|JWT]] per le primitive correlate: https://portswigger.net/web-security/xxe
- HackTricks — SAML attacks (XSW, dettagli varianti): https://book.hacktricks.xyz/pentesting-web/saml-attacks
- PortSwigger Research — "On Breaking SAML: Be Whoever You Want to Be" (paper fondante XSW): https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/somorovsky
- HackTheBox: macchine/sfide enterprise con SSO SAML (es. scenari Active Directory federati).

## Collegamenti
- [[OAuth 2.0 e OpenID Connect Attacks]]
- [[Attacchi JWT]]
- [[XML External Entity (XXE)]]
- [[Autenticazione e Gestione Sessioni]]
- [[Burp Suite]]

## Fonti
- HackTricks — SAML Attacks: https://book.hacktricks.xyz/pentesting-web/saml-attacks
- Somorovsky et al. — "On Breaking SAML: Be Whoever You Want to Be" (USENIX Security 2012): https://www.usenix.org/system/files/conference/usenixsecurity12/sec12-final91.pdf
- OWASP — SAML Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html
- PortSwigger — SAML Raider (BApp Store): https://portswigger.net/bappstore/c61cfa893bb14db4b01775554f7b802e
