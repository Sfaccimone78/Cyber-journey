---
tipo: entita
tag: [tool, web, proxy]
fase: 2
fonti: 5
aggiornato: 2026-07-02
stato: maturo
aliases: ["Burp Suite"]

---

# Burp Suite

> **Nota etica**: Burp Suite va usato solo su applicazioni proprie o su ambienti autorizzati come [[PortSwigger Web Academy]]. Intercettare traffico senza autorizzazione è illegale.

## In breve

**Burp Suite** è la piattaforma di test per la sicurezza web più usata dai penetration tester. Sviluppata da PortSwigger, agisce come **proxy HTTP/S intercettante**: si posiziona tra il browser e il server, permettendo di ispezionare, modificare e riprodurre ogni richiesta e risposta. Esiste in versione Community (gratuita) e Professional (a pagamento).

## Uso tipico

```
Browser → Burp Proxy (127.0.0.1:8080) → Server target
```

Flusso di lavoro base:
```bash
# 1. Avviare Burp Suite
# 2. Configurare il browser per usare proxy 127.0.0.1:8080
# 3. Installare il certificato CA di Burp nel browser (https://burp/)
# 4. Navigare l'applicazione target con Intercept attivo
```

Funzionalità principali:

| Strumento | Cosa fa |
|-----------|---------|
| **Proxy** | Intercetta e modifica richieste/risposte in tempo reale |
| **Repeater** | Ripete e modifica singole richieste manualmente |
| **Intruder** | Automatizza attacchi a parametri (brute force, fuzzing) |
| **Scanner** | Scansione automatica vulnerabilità (solo Pro) |
| **Decoder** | Codifica/decodifica Base64, URL encoding, HTML entities |
| **Comparer** | Confronta due risposte per trovare differenze |
| **Spider/Crawler** | Mappa automaticamente i percorsi dell'applicazione |

Esempio: modificare una richiesta nel Repeater:
```http
GET /profilo?id=1 HTTP/1.1
Host: example.com
Cookie: session=abc123

→ Cambia id=1 in id=2 → Manda → Controlla se vedi dati altrui (IDOR)
```

## Quando si usa

Burp Suite è lo strumento centrale in quasi tutte le fasi del web pentesting:
- [[SQL Injection]], [[Cross-Site Scripting (XSS)]], [[Server-Side Request Forgery (SSRF)]]: analisi e modifica dei parametri
- [[Autenticazione e Gestione Sessioni]]: brute force login con Intruder, analisi dei cookie
- [[Cookie e JWT]]: ispezione e modifica dei token
- [[Cross-Site Request Forgery (CSRF)]]: generazione di PoC con Burp
- [[Vulnerabilita Upload File]]: bypass dei controlli modificando Content-Type e filename

## Note e trucchi

- **FoxyProxy** (estensione Firefox/Chrome) permette di switchare il proxy con un clic
- In Community, Intruder è **limitato in velocità** — per brute force veloci usare `ffuf` o `hydra`
- Usare **Match and Replace** nelle opzioni Proxy per modificare automaticamente header o parametri ricorrenti
- Il **Logger** (tab Logger++) registra tutto il traffico per analisi post-sessione
- Salvare lo **stato del progetto** (File > Save project) per riprendere il lavoro
- Estensioni utili (BApp Store): JWT Editor, ActiveScan++, Autorize (test per IDOR), Hackvertor

---

# Workflow professionale (livello esperto)

## Meccanismo interno — come Burp vede il traffico
Burp è un **proxy MITM TLS**: presenta al browser un certificato firmato dalla **CA di Burp** (installata in `http://burp/`), decifra, mostra il plaintext, ri-cifra verso il server. Tutto il traffico passa per il **flusso interno**: Proxy → (eventuale match/replace) → strumenti (Repeater/Intruder) condividono lo stesso motore HTTP. Concetti chiave:
- **Scope.** Definisce *cosa* Burp considera in-target. Imposta lo scope (Target → Scope, advanced control con regex su host) e attiva **"Show only in-scope items"** + Proxy → Options → "And URL is in target scope": evita di loggare CDN/telemetria e di toccare host fuori autorizzazione (OPSEC + legale).
- **Match and Replace** (Proxy → Options): regole automatiche su tutte le richieste/risposte — es. forzare `User-Agent`, iniettare un header, riscrivere `Content-Security-Policy` in risposta per testare senza CSP.
- **HTTP/2 vs /1.1.** Burp può inviare in entrambi: per request smuggling e header tampering a volte serve forzare la versione (Repeater → Inspector / "Change request method/protocol").

## Repeater — caso reale: enumerare un IDOR
Repeater serve a **iterare manualmente** una singola richiesta. Workflow:
1. Intercetti `GET /api/invoice?id=1031`, **Ctrl+R** la manda a Repeater.
2. Cambi `id` a mano (`1030`, `1032`...) e osservi se vedi fatture altrui → **IDOR**.
3. Usi i **tab multipli** per confrontare richieste autenticata vs non; **Inspector** per editare header/cookie in modo strutturato.
4. Trovato il pattern, lo passi a Intruder per spazzare tutti gli `id`.
> Repeater è anche il posto per raffinare payload [[SQL Injection]]/[[Cross-Site Scripting (XSS)]] un colpo alla volta prima di automatizzare.

## Intruder — i 4 tipi di attacco
Marca i punti d'iniezione con `§...§`. La scelta del tipo dipende da quanti punti e da come combinare i payload:

| Tipo | Posizioni | Payload set | Caso reale |
|---|---|---|---|
| **Sniper** | 1+ ma **un §  alla volta** | 1 lista | fuzzing di un singolo parametro (un payload SQLi/XSS per volta su ogni campo a turno) |
| **Battering ram** | molti §, **stesso** valore in tutti | 1 lista | stesso payload in più posizioni simultanee (es. token uguale in header e body) |
| **Pitchfork** | N posizioni, **N liste in parallelo** | N liste (avanzano insieme) | **credential stuffing**: lista user e lista pass abbinate riga-per-riga |
| **Cluster bomb** | N posizioni, **prodotto cartesiano** | N liste (tutte le combo) | **brute force** user×pass (ogni user con ogni pass) |

Per ogni attacco: definisci **Grep-Match** (stringhe in risposta che indicano successo, es. "Welcome") e **Grep-Extract** (estrai un valore, es. un token CSRF), ordina i risultati per **status/length** per spottare l'anomalia.
> [!warning] Intruder in Community è throttled
> In Burp Community l'Intruder è rallentato artificialmente. Per brute force seri usa `ffuf`/`hydra`, o Burp Pro. Intruder Community resta ottimo per logica/PoC, non per volume.

## Sequencer — caso reale: qualità dei token di sessione
Sequencer **analizza la casualità** di token (session ID, anti-CSRF, password-reset). Workflow:
1. Trovi una risposta che emette un token (`Set-Cookie: session=...`), la mandi a Sequencer (Live capture).
2. Burp raccoglie centinaia/migliaia di campioni rieseguendo la richiesta.
3. Analisi: entropia bit-per-bit, test FIPS. Bassa entropia → token **predicibili** → session hijacking / reset token bruteforzabile.

## Comparer — caso reale: blind boolean SQLi
Comparer evidenzia **differenze byte/word** tra due risposte. Casi:
- **Blind SQLi**: confronta la risposta di `AND 1=1` (vero) vs `AND 1=2` (falso) → vedi la differenza minima che distingue vero/falso.
- **Autorizzazione**: confronta la pagina vista da admin vs user per spottare campi nascosti.
- **Userenum**: "username valido" vs "non valido" che differiscono di poche parole.

## Burp Collaborator — OOB / OAST
Collaborator è un **server esterno** (DNS + HTTP + SMTP) controllato da Burp che cattura interazioni *out-of-band*. Essenziale quando non c'è feedback in-band:
- **SSRF, blind [[SQL Injection]], blind [[Command Injection]], blind XXE**: inietti un sottodominio Collaborator; se ricevi una hit DNS/HTTP → la vuln esiste anche senza output diretto.
- "Insert Collaborator payload" genera un dominio unico `xxx.oastify.com`; "Poll now" mostra le interazioni ricevute (con timestamp, IP sorgente, tipo).
- In Community **non c'è** il Collaborator ufficiale: usa alternative come `interactsh` (OAST self-hosted) o un proprio listener DNS/HTTP.

## Macro e sessioni autenticate
Per testare aree autenticate senza far scadere la sessione, configura **Session Handling Rules** (Settings → Sessions):
- **Macro**: registra una sequenza (es. login → estrai token) che Burp **riesegue** quando la sessione scade, reiniettando il cookie/CSRF token aggiornato nelle richieste di Scanner/Intruder.
- Caso tipico: form con **token anti-CSRF per-richiesta**. La macro fa un GET della pagina, estrae il token fresco con una regola, e lo sostituisce nel POST successivo — così Intruder/Scanner non vengono respinti con "invalid token".
- **Cookie jar** condiviso mantiene i cookie tra strumenti.

## Estensioni essenziali (BApp Store)
| Estensione | A cosa serve |
|---|---|
| **Autorize** | test automatico di autorizzazione/IDOR: ripete ogni richiesta con la sessione di un utente a privilegi minori e segnala dove l'accesso *non* viene bloccato |
| **JWT Editor** | decodifica/firma/altera JWT (none-alg, key-confusion, brute del segreto HS256) |
| **ActiveScan++** | estende lo scanner attivo con check aggiuntivi |
| **Hackvertor** | encoding/transform inline nei payload con tag `<@base64>...` |
| **Logger++** | log completo e ricercabile di tutto il traffico, post-analisi |
| **Param Miner** | scopre header/parametri nascosti (cache poisoning, hidden params) |
| **Turbo Intruder** | attacchi ad altissima velocità/concorrenza (race condition, scripting Python) |
| **Collaborator Everywhere** | inietta payload OAST in tutte le richieste passive per scoprire SSRF/OOB |

## OPSEC e limiti
- **Scope rigoroso**: senza scope rischi di scansionare host non autorizzati (Scanner attivo invia payload reali). Definisci sempre lo scope e disabilita lo scan fuori scope.
- Lo **Scanner attivo** è invasivo (può creare record, inviare email, triggerare azioni): non lanciarlo su produzione senza permesso esplicito.
- Il certificato CA di Burp installato **abbassa la sicurezza** della macchina di test: usalo solo su una VM dedicata, rimuovilo dopo.
- Collaborator/OAST rivela un dominio: nei test usa l'infrastruttura concordata col cliente.

## Detection engineering (lato blue team — riconoscere Burp)
**Sorgenti:** access/WAF log. Indicatori: header `User-Agent` di default lasciati, **scanner attivo** = molte richieste quasi identiche con payload (`'`, `<script>`, `../`) in rapida sequenza dallo stesso IP, parametri Collaborator (`*.oastify.com`, `*.burpcollaborator.net`).
```spl
index=web
| stats count, dc(uri_query) as distinct_payloads,
        values(http_user_agent) as ua by src_ip
| where count > 200 AND distinct_payloads > 100
```
**Regola Sigma:**
```yaml
title: Scansione web automatizzata / payload OAST (Burp Collaborator)
logsource: { category: webserver }
detection:
  sel:
    cs-uri-query|contains:
      - 'oastify.com'
      - 'burpcollaborator.net'
  condition: sel
level: medium
```
**MITRE ATT&CK:** uso di Burp come tool ricade in **T1190** (exploit web app) e **T1595.002** (Active Scanning: Vulnerability Scanning) nella fase di reconnaissance.

## Troubleshooting (5 errori comuni)
1. **HTTPS non intercetta / errore certificato** → CA di Burp non installata o non trusted nel browser. Scaricala da `http://burp/` (con proxy attivo) e importala nello store dei certificati attendibili.
2. **Niente traffico nel Proxy** → il browser non punta a `127.0.0.1:8080`, oppure usa DoH/proxy di sistema che salta Burp. Usa il **Burp's embedded browser** (preconfigurato) o FoxyProxy.
3. **Intruder lentissimo** → throttling di Community. Riduci il payload set per il PoC, o passa a `ffuf`/Turbo Intruder/Burp Pro.
4. **Sessione scade durante Intruder/Scanner** → manca una Session Handling Rule con macro che rinnova cookie/CSRF token. Configura la macro di login + estrazione token.
5. **Collaborator non riceve interazioni** → in Community non esiste; egress filtering blocca DNS/HTTP in uscita dal target; o il payload non raggiunge un sink OOB. Verifica con un test SSRF noto e considera `interactsh`.

## Domande da colloquio
**D: Quando useresti Cluster bomb invece di Pitchfork in Intruder?**
R: Pitchfork abbina le liste riga-per-riga (combo già accoppiate, es. credential stuffing user:pass noti). Cluster bomb fa il prodotto cartesiano di tutte le combinazioni (brute force di ogni user con ogni password): più richieste ma copertura totale.

**D: A cosa serve Burp Collaborator e quando è indispensabile?**
R: Cattura interazioni out-of-band (DNS/HTTP/SMTP) verso un dominio controllato da Burp. È indispensabile per vulnerabilità **blind** senza feedback in-band: SSRF cieca, blind SQLi/command injection, XXE OOB — la hit verso il Collaborator conferma l'esecuzione.

**D: Come testi una funzione protetta da token anti-CSRF per-richiesta con Intruder?**
R: Con una Session Handling Rule + macro: Burp fa un GET preliminare, estrae il token fresco con una regola, e lo sostituisce nel parametro/header del POST a ogni iterazione. Senza macro ogni richiesta verrebbe respinta per token non valido.

**D: Perché lo Scanner attivo non va lanciato a cuor leggero in produzione?**
R: Invia payload reali (injection, fuzz) che possono creare/cancellare record, inviare email, triggerare azioni o causare DoS. Va usato solo in scope autorizzato, idealmente in staging, con il cliente avvisato.

## Lab
- [[PortSwigger Web Academy]] è il terreno di pratica nativo di Burp (stesso autore): ogni categoria di lab si risolve intercettando e modificando le richieste con Burp.
  - *Percorso "Apprentice"*: risolvi i primi lab di **SQL injection** e **XSS** usando **Repeater** (un payload alla volta) e **Intruder** (Sniper) per il fuzzing.
  - *Authentication*: pratica il brute force con **Intruder** (attacchi *Pitchfork*/*Cluster bomb*) sui lab di login.
  - *SSRF/blind*: usa **Burp Collaborator** sui lab di SSRF cieca e blind [[SQL Injection]].
  - *Access control*: installa **Autorize** e rigioca i lab IDOR con una seconda sessione.
- TryHackMe → room *Burp Suite: The Basics* / *Burp Suite: Repeater/Intruder* per il setup guidato (proxy, CA, Intercept).
- Cosa esercitare: configurare proxy + CA, definire lo **Scope**, e completare un flusso Proxy → Repeater → Intruder su un lab reale.

## Collegamenti

- [[SQL Injection]]
- [[Cross-Site Scripting (XSS)]]
- [[Command Injection]] — Collaborator per il blind OOB
- [[Server-Side Request Forgery (SSRF)]] — Collaborator indispensabile per la SSRF cieca
- [[Autenticazione e Gestione Sessioni]]
- [[Cookie e JWT]]
- [[PortSwigger Web Academy]]
- [[OWASP ZAP]]

## Fonti

- PortSwigger Burp Suite Documentation: https://portswigger.net/burp/documentation
- PortSwigger Web Security Academy (labs Burp): https://portswigger.net/web-security
- HackTricks Burp Suite: https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/burp-suite
- PortSwigger — Burp Collaborator: https://portswigger.net/burp/documentation/collaborator
- PortSwigger — Session handling rules e macro: https://portswigger.net/burp/documentation/desktop/settings/sessions
