---
tipo: concetto
tag: [web, owasp, tool]
fase: 3
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["Race Condition Web", "Race Conditions"]
---

# Race Condition Web

> [!warning] Uso etico
> Inviare raffiche concorrenti per sfruttare race condition **solo** su lab autorizzati o target in scope. Abusare di limiti/sconti/saldi su un sistema reale è frode.

## In breve
Una **race condition** web emerge quando l'applicazione esegue operazioni che dovrebbero essere atomiche ma non lo sono: in una piccola finestra temporale (**collision window**) tra il *check* e il *use* di uno stato, l'attaccante invia più richieste **in parallelo** che vengono processate prima che lo stato si aggiorni. Risultato: un controllo viene superato N volte invece di una. Ricerca moderna di riferimento: **James Kettle**, "Smashing the state machine" (PortSwigger, 2023), che ha generalizzato il problema oltre il classico TOCTOU.

## Il pattern TOCTOU (Time-Of-Check to Time-Of-Use)
```text
Richiesta 1: leggi saldo (100) → ok, scala 100 → saldo 0
Richiesta 2: leggi saldo (100) → ok, scala 100 → saldo 0     ← entrambe lette PRIMA dell'update
# Se arrivano insieme, entrambe vedono 100 → spendi 200 con 100.
```
Esempi: riscattare un **gift card/coupon** più volte, **applicare uno sconto** N volte, superare un **rate limit** di tentativi password/OTP, **registrare** lo stesso username, **prelevare** più del saldo, **votare/like** ripetutamente.

## Limit overrun — esempio carrello/coupon
```http
POST /coupon HTTP/1.1
Host: shop.lab
Cookie: session=...

code=PROMO20
```
Inviando 30 copie *simultanee* di questa richiesta, il coupon "monouso" viene applicato 30 volte perché il controllo "già usato?" gira prima che il primo commit lo segni come usato.

## Tecnica di invio: serve vero parallelismo
La chiave è far arrivare le richieste **nello stesso istante** lato server, neutralizzando il jitter di rete:
- **HTTP/1.1 — last-byte sync**: invii tutte le richieste tranne l'ultimo byte di ciascuna, poi rilasci gli ultimi byte insieme.
- **HTTP/2 — single-packet attack** (Kettle): impacchetti ~20-30 richieste in **un solo pacchetto TCP**, eliminando la latenza di rete come variabile. È il metodo moderno più affidabile.

In [[Burp Suite]]: **Repeater → "Send group in parallel (single-packet attack)"**. Estensione **Turbo Intruder** per raffiche programmatiche.
```python
# Turbo Intruder — schema single-packet attack
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint, concurrentConnections=1,
                           engine=Engine.BURP2)
    for i in range(30):
        engine.queue(target.req, gate='race1')   # accoda 30 richieste sullo stesso gate
    engine.openGate('race1')                       # le rilascia tutte insieme
```

## Varianti oltre TOCTOU ("multi-step" / hidden state)
- **Single-endpoint**: due richieste sullo stesso endpoint che collidono su stato condiviso.
- **Multi-endpoint**: richieste a endpoint *diversi* che toccano lo stesso record nella stessa finestra (es. cambia email mentre confermi un token).
- **Partial construction / time-sensitive**: sfruttare oggetti a metà creazione (es. token prevedibili generati nello stesso istante).
- **Rate-limit bypass**: la finestra annulla il conteggio dei tentativi → brute force di OTP/2FA.

## Impatto
Frode economica (sconti/saldi/withdraw), bypass di rate limit e 2FA, escalation di privilegi, corruzione di stato e dati. Spesso ad alto valore nei bug bounty (logica di business).

## Come difendersi
1. **Atomicità a livello di datastore**: transazioni con isolamento adeguato, `SELECT ... FOR UPDATE`, vincoli `UNIQUE`, contatori atomici.
2. **Lock pessimistici/ottimistici** sulla risorsa condivisa (es. lock per-utente o per-record durante l'operazione sensibile).
3. **Idempotenza**: chiavi di idempotenza per operazioni one-shot (coupon, pagamenti).
4. Evita di spezzare in più richieste operazioni che devono essere atomiche; riduci/elimina lo stato condiviso mutevole.
5. Non affidare l'unicità a un controllo applicativo "leggi-poi-scrivi" non transazionale.

## Lab
- PortSwigger — Race conditions (lab: "Limit overrun", "Bypassing rate limits via race conditions", "Multi-endpoint race conditions", "Single-endpoint race conditions", "Partial construction race conditions", "Time-sensitive attacks"): https://portswigger.net/web-security/race-conditions
- James Kettle — "Smashing the state machine: the true potential of web race conditions": https://portswigger.net/research/smashing-the-state-machine
- HackTricks — Race Condition: https://book.hacktricks.xyz/pentesting-web/race-condition

## Collegamenti
- [[HTTP Request Smuggling]]
- [[Autenticazione e Gestione Sessioni]]
- [[Broken Access Control e IDOR]]
- [[Burp Suite]]
- [[OWASP Top 10]]

## Fonti
- PortSwigger — Race conditions: https://portswigger.net/web-security/race-conditions
- James Kettle — Smashing the state machine (PortSwigger Research, 2023): https://portswigger.net/research/smashing-the-state-machine
- PortSwigger — Turbo Intruder: https://github.com/PortSwigger/turbo-intruder
- HackTricks — Race Condition: https://book.hacktricks.xyz/pentesting-web/race-condition
