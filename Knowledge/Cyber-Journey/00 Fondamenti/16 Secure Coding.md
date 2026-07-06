---
tipo: concetto
tag: [fondamenti, metodologia]
fase: 0
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Secure Coding"]
---
# Secure Coding

## In breve
Il **secure coding** è la metà difensiva del web hacking: scrivere software che **resiste** alle classi di attacco dell'[[OWASP Top 10]]. Principio guida: la sicurezza non è una *feature* aggiunta alla fine, ma una proprietà del **design** e di ogni riga di codice (*secure by design / by default*) → [[Insecure Design]], [[Threat Modeling]].

## Principi fondamentali
- **Least privilege**: ogni componente ha solo i permessi minimi necessari → [[Permessi Linux]], [[Broken Access Control e IDOR]].
- **Defense in depth**: più strati di controllo; se uno cade, gli altri reggono → [[Difesa in Profondità]].
- **Fail securely**: in caso di errore, **negare** l'accesso (default-deny), non aprirlo.
- **Secure defaults**: la configurazione di fabbrica è quella sicura → [[Security Misconfiguration]].
- **Don't trust input**: ogni dato esterno (utente, API, file, header) è ostile finché non validato.
- **Minimize attack surface**: meno endpoint/feature/dipendenze = meno bersagli → [[Superficie di Attacco]].

## Le contromisure mappate sulle vulnerabilità

| Vulnerabilità (OWASP) | Pratica di secure coding |
|-----------------------|--------------------------|
| **Injection** → [[SQL Injection]] | **Prepared statement / query parametrizzate**, ORM; mai concatenare input in query/comandi |
| **XSS** → [[Cross-Site Scripting (XSS)]] | **Output encoding** contestuale + **CSP**; framework con auto-escaping; evitare `innerHTML` |
| **Broken Access Control** → [[Broken Access Control e IDOR]] | Autorizzazione **server-side** su ogni richiesta; deny-by-default; no security-by-obscurity |
| **Cryptographic Failures** → [[Cryptographic Failures]] | Librerie note (no crypto fai-da-te), TLS ovunque, hashing password con **bcrypt/argon2** → [[Funzioni di Hash]] |
| **Broken Authentication** → [[Autenticazione e Gestione Sessioni]] | MFA, gestione sessioni sicura, rate-limit login, password policy sana |
| **SSRF** → [[Server-Side Request Forgery (SSRF)]] | Allow-list di destinazioni, blocco IP interni/metadata, no fetch di URL grezzi |
| **Vulnerable Components** → [[Componenti Vulnerabili]] | **SCA** + aggiornamenti, SBOM, rimuovere dipendenze inutili |
| **Security Logging Failures** → [[Logging e Monitoring Failures]] | Logging di eventi di sicurezza, niente segreti nei log, monitoraggio/alert |

## Validazione dell'input — la regola d'oro
**Allow-list > deny-list**: definisci cosa è *permesso* (tipo, lunghezza, formato, range), rifiuta tutto il resto. La deny-list è sempre aggirabile. Valida **lato server** (il client è sotto controllo dell'attaccante). [OWASP Input Validation Cheat Sheet]

```python
# MALE: input concatenato → SQL injection
cur.execute("SELECT * FROM users WHERE id = " + user_id)

# BENE: query parametrizzata → l'input non è mai "codice"
cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

## La sicurezza nel ciclo di vita (SSDLC)
La correzione costa meno **prima** è trovata. Integrare la sicurezza in ogni fase:
- **Design**: threat modeling, requisiti di sicurezza → [[Threat Modeling]]
- **Sviluppo**: linee guida secure coding, code review, gestione segreti (vault, no hardcoded)
- **Test**: **SAST** (analisi statica del codice), **DAST** (test dinamico runtime), **SCA** (dipendenze), fuzzing
- **Deploy/Run**: hardening, patch management, logging/monitoring, WAF come rete di sicurezza

## Gestione dei segreti
Mai credenziali/chiavi **hardcoded** nel codice o nel repo. Usare variabili d'ambiente o un **secrets manager**; ruotare le chiavi; `.gitignore` per i file sensibili → [[Cryptographic Failures]].

## Lab
- **[[PortSwigger Web Academy]]** → categorie *SQL injection* e *Cross-site scripting*: sfrutta la falla, poi ragiona sulla fix di secure coding (query parametrizzata, output encoding + CSP) che l'avrebbe impedita.
- **Semgrep** (SAST gratuito): esegui `semgrep --config auto` sul codice sorgente di un'app volutamente vulnerabile (es. OWASP Juice Shop o DVWA) e correggi le findings di injection/hardcoded secret.
- **OWASP Juice Shop** in locale: individua un endpoint vulnerabile, applica una contromisura server-side (deny-by-default sull'autorizzazione) e ri-testa.

## Domande
1. **D:** Perché nel secure coding si preferisce allow-list a deny-list per la validazione input? **R:** Perché la deny-list è sempre aggirabile; l'allow-list definisce esattamente cosa è permesso (tipo, lunghezza, formato, range) e rifiuta tutto il resto. La validazione va fatta lato server.
2. **D:** Cosa significa "fail securely"? **R:** In caso di errore il sistema deve *negare* l'accesso (default-deny), non aprirlo.
3. **D:** Qual è la contromisura di secure coding contro le injection SQL? **R:** Prepared statement / query parametrizzate (o ORM), senza mai concatenare l'input dell'utente nella query.
4. **D:** A cosa servono SAST, DAST e SCA nel SSDLC? **R:** SAST analizza staticamente il codice, DAST testa l'app a runtime, SCA controlla le dipendenze di terze parti; insieme spostano la scoperta dei difetti "a sinistra" dove costa meno.
5. **D:** Come vanno gestiti i segreti (chiavi, credenziali)? **R:** Mai hardcoded nel codice/repo: usare variabili d'ambiente o un secrets manager, ruotare le chiavi e mettere i file sensibili in `.gitignore`.

## Collegamenti
- [[Insecure Design]] · [[Threat Modeling]] · [[Security Misconfiguration]] · [[Difesa in Profondità]] · [[OWASP Top 10]]
- Crypto: [[Funzioni di Hash]] · [[TLS e SSL]] · Linux: [[Permessi Linux]]

## Fonti
- OWASP Proactive Controls — https://owasp.org/www-project-proactive-controls/
- OWASP Cheat Sheet Series — https://cheatsheetseries.owasp.org/
- Anderson, *Security Engineering* — https://www.cl.cam.ac.uk/~rja14/book.html
