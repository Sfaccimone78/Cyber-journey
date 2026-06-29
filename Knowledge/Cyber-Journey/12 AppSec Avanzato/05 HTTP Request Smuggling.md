---
tipo: concetto
tag: [web, owasp, tool]
fase: 4
fonti: 4
aggiornato: 2026-06-28
stato: maturo
aliases: ["HTTP Request Smuggling", "Request Smuggling", "Desync Attacks"]
---

# HTTP Request Smuggling

> [!warning] Uso etico
> Il request smuggling avvelena la coda di richieste di **altri utenti**: è ad alto rischio di collaterali. Eseguirlo **solo** su lab dedicati (PortSwigger) o target in scope, con cautela. Mai su infrastruttura terza.

## In breve
Il **HTTP Request Smuggling** (o **desync attack**) sfrutta il disaccordo tra due server in catena — tipicamente un **front-end** (reverse proxy/CDN/load balancer) e un **back-end** — su *dove finisce una richiesta HTTP e dove inizia la successiva*. L'attaccante invia una richiesta ambigua: il front-end la interpreta in un modo, il back-end in un altro. La parte "smuggled" viene anteposta alla richiesta del **prossimo utente**, dirottandola. Ricerca fondante di **James Kettle** (PortSwigger, 2019).

## La radice: Content-Length vs Transfer-Encoding
Due modi di delimitare il body di una richiesta HTTP/1.1:
- **`Content-Length` (CL)**: lunghezza in byte.
- **`Transfer-Encoding: chunked` (TE)**: body in chunk, terminato da un chunk di dimensione `0`.

Se entrambi gli header sono presenti, la RFC dice di preferire TE — ma i server non concordano. Da qui le classi:

### CL.TE — front-end usa CL, back-end usa TE
```http
POST / HTTP/1.1
Host: vuln.lab
Content-Length: 6
Transfer-Encoding: chunked

0

G
```
Il front-end legge 6 byte (`0\r\n\r\nG`) e inoltra tutto. Il back-end vede `chunked`, si ferma al chunk `0`, e lascia `G` come inizio della **prossima** richiesta → la `G` si prepende alla richiesta della vittima (es. diventa `GET...`).

### TE.CL — front-end usa TE, back-end usa CL
```http
POST / HTTP/1.1
Host: vuln.lab
Content-Length: 4
Transfer-Encoding: chunked

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
...
0

```
Il front-end inoltra l'intero chunked; il back-end legge solo `Content-Length: 4` byte e considera il resto (`GPOST...`) come richiesta successiva smuggled.

### TE.TE — entrambi usano TE, ma uno è "ingannabile"
Si offusca uno dei due header `Transfer-Encoding` così che un solo server lo riconosca:
```http
Transfer-Encoding: chunked
Transfer-Encoding: x          ← uno dei due ignora questa riga
Transfer-Encoding:[tab]chunked
Transfer-Encoding : chunked   ← spazio prima dei due punti
```

## HTTP/2 desync (downgrade)
Con HTTP/2 il body è delimitato dalla struttura dei frame, non da CL/TE. Ma se il front-end "downgrada" a HTTP/1.1 verso il back-end, può reintrodurre l'ambiguità:
- **H2.CL / H2.TE**: si inietta un CL/TE nei pseudo-header o header HTTP/2 che il back-end onora dopo il downgrade.
- **CRLF injection** nei valori header HTTP/2 (es. nel valore di `foo`) per smuggling di header/request intere.

## Sfruttamento pratico (cosa ci fai)
- **Bypass di controlli di sicurezza del front-end** (es. accedere a `/admin` quando il proxy lo blocca).
- **Catturare richieste di altri utenti** (ruba cookie/CSRF token facendo loggare la loro request in un endpoint che riflette).
- **Response queue poisoning**: desincronizza la coda risposte → ogni utente riceve la risposta di un altro.
- **Web cache poisoning** combinato (vedi [[Web Cache Poisoning]]) e **request tunnelling**.

## Tooling
[[Burp Suite]] → estensione **HTTP Request Smuggler** (di James Kettle): rileva CL.TE/TE.CL/TE.TE/HTTP2 e genera prove di concetto. Disabilita l'aggiornamento automatico di Content-Length in Repeater per inviare richieste byte-esatte. `smuggler.py` come alternativa CLI.

## Impatto
Compromissione **trasversale**: dirottamento di sessioni di altri utenti, furto credenziali, bypass di WAF/auth, defacement via cache. Tra le vulnerabilità più severe e "rumorose".

## Come difendersi
1. **Usa HTTP/2 end-to-end** senza downgrade verso il back-end.
2. **Normalizza/rifiuta richieste ambigue**: il front-end deve respingere messaggi con sia CL sia TE, o con header duplicati/malformati.
3. **Stessa implementazione di parsing** front-end e back-end; configura il front-end perché normalizzi prima di inoltrare.
4. **Disabilita il riuso delle connessioni** back-end dove possibile (limita il poisoning della coda).
5. Tieni aggiornati proxy/CDN/server; testa con HTTP Request Smuggler in pre-produzione.

## Lab
- PortSwigger — HTTP request smuggling (lab CL.TE, TE.CL, TE.TE, "Bypass front-end security controls", "Capturing other users' requests", HTTP/2 H2.CL/H2.TE, request smuggling via CRLF): https://portswigger.net/web-security/request-smuggling
- PortSwigger — Advanced request smuggling: https://portswigger.net/web-security/request-smuggling/advanced
- James Kettle — "HTTP Desync Attacks: Request Smuggling Reborn": https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn
- James Kettle — "HTTP/2: The Sequel is Always Worse": https://portswigger.net/research/http2

## Domande
**D: Qual è la radice del request smuggling?**
R: Il disaccordo tra front-end e back-end su **dove finisce** una richiesta, tipicamente per
interpretazione diversa di `Content-Length` vs `Transfer-Encoding` (CL.TE / TE.CL / TE.TE).

**D: Cosa permette di ottenere?**
R: Bypass dei controlli del front-end, avvelenamento della cache, cattura delle richieste di altri
utenti (session/credential theft), e request hijacking.

**D: Come ci si difende?**
R: Normalizzare/rifiutare richieste ambigue (entrambe CL e TE), usare **HTTP/2 end-to-end** senza
downgrade, e idealmente lo stesso server per FE e BE.

## Collegamenti
- [[Web Cache Poisoning]]
- [[Race Condition Web]]
- [[Autenticazione e Gestione Sessioni]]
- [[Burp Suite]]
- [[OWASP Top 10]]

## Fonti
- PortSwigger — HTTP request smuggling: https://portswigger.net/web-security/request-smuggling
- James Kettle — HTTP Desync Attacks (PortSwigger Research): https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn
- James Kettle — HTTP/2: The Sequel is Always Worse: https://portswigger.net/research/http2
- defparam/smuggler: https://github.com/defparam/smuggler
