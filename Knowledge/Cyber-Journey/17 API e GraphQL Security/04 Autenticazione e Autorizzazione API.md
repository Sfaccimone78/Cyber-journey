---
tipo: concetto
tag: [api]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Autenticazione e Autorizzazione API"]
---

# Autenticazione e Autorizzazione API

## In breve

L'autenticazione stabilisce chi è il chiamante, l'autorizzazione cosa può fare. Nelle API la prima si basa quasi sempre su token bearer (JWT, OAuth 2.0 access token, API key) trasmessi a ogni richiesta, dato che REST è stateless. Broken Authentication è API2 nell'OWASP API Security Top 10: comprende JWT mal validati, flussi OAuth deboli, refresh token mal gestiti, API key esposte e meccanismi di reset/OTP attaccabili. Questa nota approfondisce il lato API dei token e si collega ai fondamenti di [[Cookie e JWT]].

## Come funziona

**JWT** (JSON Web Token) è composto da header, payload e firma, separati da punti e codificati base64url. L'header dichiara l'algoritmo (`alg`), il payload contiene le claim (`sub`, `exp`, `role`), la firma garantisce integrità. Il server, ricevuto il token, ne verifica la firma e le claim. Gli attacchi tipici: algoritmo `none` accettato, confusione `RS256`/`HS256` (alg confusion), firma non verificata, `exp` ignorato, segreto HMAC debole bruteforzabile.

**OAuth 2.0** delega l'accesso tramite access token (e refresh token). Debolezze comuni: `redirect_uri` non validato, mancanza del parametro `state` (CSRF sul flusso), token nel fragment esposti, scope troppo ampi, mancata rotazione dei refresh token.

**API key**: stringhe statiche spesso hardcoded in app mobili o JS front-end, facilmente estraibili e prive di scadenza.

L'autorizzazione, separata, decide l'accesso a oggetti (vedi [[BOLA e BFLA]]) e funzioni. Un errore frequente è considerare l'autenticazione sufficiente: avere un token valido non implica il diritto sulla risorsa specifica.

## Esempi

Decodifica e analisi di un JWT con jwt_tool:

```bash
jwt_tool eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MiIsInJvbGUiOiJ1c2VyIn0.xxx
# Mostra header, claim e flag di sicurezza
```

Attacco algoritmo `none`:

```bash
jwt_tool $TOKEN -X a    # forza alg=none, rimuove la firma
```

Bruteforce del segreto HMAC (HS256) con jwt_tool e wordlist:

```bash
jwt_tool $TOKEN -C -d /usr/share/wordlists/rockyou.txt
# Se trovato: forgiatura di un token con role=admin
jwt_tool $TOKEN -S hs256 -p "secret-trovato" -T   # tamper del payload
```

Alg confusion RS256 -> HS256 (firma il token con la chiave pubblica come segreto HMAC):

```bash
jwt_tool $TOKEN -X k -pk public.pem
```

Replay manuale con token manomesso in curl:

```bash
curl -s "https://target.tld/api/v1/admin/stats" \
  -H "Authorization: Bearer $FORGED_TOKEN"
```

In Burp l'estensione **JWT Editor** consente di modificare claim, cambiare algoritmo e firmare con chiavi arbitrarie direttamente nel Repeater. Per testare l'assenza di `state` o redirect_uri deboli in OAuth si intercetta il flusso di autorizzazione e si manipolano i parametri.

## Mitigazione e difesa

- Verificare **sempre** la firma JWT e rifiutare esplicitamente `alg: none` e algoritmi non attesi (allowlist degli algoritmi).
- Usare segreti HMAC lunghi e casuali o, meglio, firma asimmetrica con chiavi gestite correttamente.
- Validare `exp`, `iss`, `aud` e usare token a vita breve con refresh ruotati.
- In OAuth: validazione stretta di `redirect_uri`, parametro `state` obbligatorio, scope minimi.
- Non incorporare API key statiche nei client; usare token a scadenza e rotazione.
- Tenere separati i controlli di autenticazione e autorizzazione, applicando deny-by-default sulle risorse.

## Lab

- [[PortSwigger Web Academy]] - laboratori JWT e OAuth authentication.
- [[TryHackMe]] - room su JWT e autenticazione API.
- [[HackTheBox]] - macchine con JWT e OAuth vulnerabili.
- crAPI - flussi di autenticazione e JWT da attaccare.
- VAmPI - endpoint con gestione token debole.
- OWASP juice-shop - sfide su JWT e gestione sessione.

## Domande

1. **Perché REST richiede un token a ogni richiesta?** Perché è stateless: il server non mantiene sessione, quindi ogni richiesta deve trasportare le credenziali (token, API key).
2. **Cos'è l'alg confusion?** Far validare al server un token firmato HS256 usando come segreto la chiave pubblica RSA, quando il server si aspetta RS256, ottenendo una firma forgiabile.
3. **Avere un JWT valido basta per l'autorizzazione?** No: l'autenticazione prova l'identità, ma l'accesso a ogni oggetto/funzione richiede un controllo di autorizzazione separato (vedi [[BOLA e BFLA]]).
4. **Perché le API key statiche nei client mobili sono rischiose?** Sono estraibili dal binario o dal traffico, non scadono e spesso hanno privilegi ampi.
5. **A cosa serve il parametro `state` in OAuth?** Protegge dal CSRF legando la richiesta di autorizzazione alla sessione del client.

## Approfondimento livello esperto

L'**alg confusion lato API** merita attenzione perché molte librerie JWT, nelle versioni datate, scelgono l'algoritmo di verifica dall'header del token invece di imporlo: passando un token con `alg: HS256` e firmandolo con la chiave pubblica RSA (pubblicamente nota, magari recuperata da `/jwks.json`) si ottiene un token valido. La difesa è imporre l'algoritmo server-side, mai derivarlo dall'header. Edge case correlati: (1) **kid injection** - il campo `kid` dell'header, se usato per caricare la chiave da filesystem o DB senza sanificazione, abilita path traversal o SQLi per puntare a una chiave controllata. (2) **JWKS spoofing** - se il server recupera le chiavi da un URL `jku`/`x5u` controllabile, si può fornire un set di chiavi proprio. (3) **token non revocabili** - i JWT stateless non si invalidano: un access token a vita lunga rubato resta valido fino a `exp`, quindi servono token brevi e una denylist per i casi critici. (4) **scope vs autorizzazione** - in OAuth uno scope ampio non sostituisce il controllo object-level: anche con scope corretto la BOLA resta possibile. Sul fronte detection/logging, vanno registrati e correlati i fallimenti di verifica firma, i cambi improvvisi di `alg`, e l'uso dello stesso token da IP/dispositivi diversi.

## Collegamenti

- [[Fondamenti API e REST Security]]
- [[OWASP API Security Top 10]]
- [[BOLA e BFLA]]
- [[Mass Assignment, SSRF e Rate Limiting API]]
- [[Cookie e JWT]]
- [[Broken Access Control e IDOR]]
- [[GraphQL Security]]
- [[Server-Side Request Forgery (SSRF)]]

## Fonti

- https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/
- https://portswigger.net/web-security/jwt
- https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens
