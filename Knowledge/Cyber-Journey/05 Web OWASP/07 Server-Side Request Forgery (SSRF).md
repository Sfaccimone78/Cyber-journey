---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Server-Side Request Forgery (SSRF)", "SSRF"]
---

# Server-Side Request Forgery (SSRF)

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger Academy, DVWA, TryHackMe).

## In breve
La **SSRF** costringe il **server** a fare richieste verso destinazioni scelte dall'attaccante — incluse risorse **interne** irraggiungibili da fuori. Il server è un proxy fidato dentro la rete: SSRF lo trasforma in un piede dentro il perimetro. Categoria propria **A10** dell'[[OWASP Top 10]] 2021.

> [!note] Numerazione OWASP 2025
> Nella bozza **OWASP Top 10:2025** la SSRF è stata **assorbita in A01 Broken Access Control** (è di fatto un bypass dei confini di accesso). Resta comunque un concetto distinto e ad alto impatto. Vedi [[Broken Access Control e IDOR]].

## Perché è grave
Il server di solito può raggiungere ciò che tu non puoi: `localhost`, pannelli admin interni, altri microservizi, e soprattutto gli **endpoint di metadati cloud** che custodiscono credenziali. Una SSRF su cloud spesso → **takeover dell'account cloud**.

## Bersagli tipici
```
http://localhost/admin              servizi solo-interni
http://127.0.0.1:6379/              Redis/DB non esposti
http://169.254.169.254/latest/meta-data/   metadati AWS (IMDSv1)
http://metadata.google.internal/   metadati GCP
file:///etc/passwd                 lettura file (se segue lo schema file://)
gopher://127.0.0.1:6379/_...       smuggling verso servizi non-HTTP (Redis, SMTP)
dict://, ftp://                    altri schemi abusabili
```

## Esempio pratico — furto credenziali cloud (AWS IMDSv1)
```http
POST /api/fetch-image  {"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}
→ risponde "ec2-role"
POST /api/fetch-image  {"url": ".../iam/security-credentials/ec2-role"}
→ AccessKeyId / SecretAccessKey / Token   → accesso diretto all'infra AWS
```

## SSRF cieca e bypass dei filtri
- **Blind SSRF**: nessuna risposta in pagina → conferma con **OAST** (Burp Collaborator): l'URL punta a un tuo dominio, vedi arrivare la richiesta DNS/HTTP.
- **Bypass blacklist di `127.0.0.1` / `localhost`**:
  - notazioni alternative: `127.1`, `0.0.0.0`, `0x7f000001`, `2130706433` (decimale)
  - IPv6: `[::1]`, `[::ffff:127.0.0.1]`
  - **DNS rebinding**: dominio che risolve prima a IP pubblico (passa il check) poi a `127.0.0.1` (alla fetch)
  - redirect aperto: l'URL allowlisted fa `302` verso quello interno.

## Mitigazione (priorità)
1. **Allowlist** di domini/IP di destinazione (molto meglio della blacklist).
2. **Bloccare reti private** (RFC 1918: 10/8, 172.16/12, 192.168/16), loopback, link-local `169.254/16`.
3. **Validare dopo la risoluzione DNS** e ri-validare dopo ogni redirect (anti-rebinding); disabilitare schemi non-HTTP.
4. Su cloud: **IMDSv2** (richiede token, blocca SSRF semplici), ruoli IAM minimi.
5. Non restituire la risposta grezza al client; **network egress filtering**: il server applicativo non deve poter raggiungere il metadata endpoint né reti interne sensibili.
6. Bloccare schemi non-HTTP(S) (`file`, `gopher`, `dict`).

## CVE / casi reali
- **Capital One (2019)** — SSRF su un WAF mal configurato che ha letto le credenziali IAM dal metadata endpoint AWS → **100M record** esfiltrati. Caso di studio canonico di SSRF + misconfig cloud → [[Security Misconfiguration]].
- **CVE-2021-26855 "ProxyLogon"** (Microsoft Exchange) — SSRF pre-auth usata come primo anello di una catena che porta a RCE; sfruttata massivamente in the wild.

## Lab
- [[PortSwigger Web Academy]] → categoria **SSRF**. Percorso consigliato dal livello APPRENTICE:
  - *Basic SSRF against the local server* — fetch di `http://localhost/admin` per raggiungere un pannello solo-interno.
  - *SSRF against another back-end system* — enumerare l'IP interno (es. `192.168.0.X`) per trovare un servizio admin.
  - *SSRF with blacklist-based input filter bypass* — praticare le notazioni alternative di `127.0.0.1` (`127.1`, encoding, doppio URL-encode).
  - *Blind SSRF with out-of-band detection* — confermare una SSRF cieca con **Burp Collaborator** (canale DNS/HTTP).
- Cosa esercitare: usare [[Burp Suite]] Repeater per manipolare il parametro `url`, e Collaborator per la variante blind.

## Domande
1. **D:** Perché una SSRF su un'istanza cloud è particolarmente grave?  **R:** Il server può raggiungere l'endpoint di metadati (`169.254.169.254`) e leggerne le credenziali IAM, portando spesso al takeover dell'account cloud (caso Capital One 2019).
2. **D:** Come si conferma una SSRF **cieca**, senza output in pagina?  **R:** Con tecniche OAST: si punta l'URL a un dominio controllato (Burp Collaborator) e si osserva l'arrivo della richiesta DNS/HTTP.
3. **D:** Perché l'allowlist è preferibile alla blacklist per mitigare la SSRF?  **R:** La blacklist di `localhost`/`127.0.0.1` si aggira con notazioni alternative (`127.1`, `0x7f000001`, IPv6, DNS rebinding); un'allowlist di destinazioni ammesse chiude tutte queste varianti.
4. **D:** Cos'è il DNS rebinding e perché batte la validazione dell'URL?  **R:** Un dominio che risolve prima a un IP pubblico (supera il check) e poi a `127.0.0.1` al momento della fetch: la validazione avviene prima della risoluzione effettiva usata dalla richiesta.
5. **D:** Come mitiga IMDSv2 la SSRF verso i metadati AWS?  **R:** Richiede un token ottenuto con una richiesta PUT preventiva e header specifici, che una SSRF semplice basata su GET non può fornire.

## Collegamenti
- [[OWASP Top 10]]
- [[HTTP e HTTPS]]
- [[Ricognizione (Recon)]]
- [[Security Misconfiguration]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti
- PortSwigger — SSRF: https://portswigger.net/web-security/ssrf
- OWASP — A10 SSRF: https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/
- OWASP — SSRF Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
