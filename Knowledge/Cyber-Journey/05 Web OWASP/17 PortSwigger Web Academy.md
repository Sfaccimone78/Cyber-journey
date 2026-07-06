---
tipo: entita
tag: [piattaforma, formazione, web]
fase: 1
fonti: 2
aggiornato: 2026-07-02
stato: maturo
aliases: ["PortSwigger Web Academy", "PortSwigger Labs"]

---

# PortSwigger Web Academy

## In breve

La **PortSwigger Web Security Academy** (portswigger.net/web-security) è la piattaforma di formazione gratuita creata da PortSwigger, l'azienda dietro [[Burp Suite]]. Offre teoria approfondita e **lab pratici interattivi** su tutte le principali vulnerabilità web, dalla [[SQL Injection]] al [[Server-Side Request Forgery (SSRF)]], passando per [[Cookie e JWT]], [[Cross-Site Scripting (XSS)]] e molte altre. È considerata la miglior risorsa gratuita per imparare il web hacking.

## Uso tipico

```
# Accesso alla piattaforma (account gratuito)
https://portswigger.net/web-security

# Struttura di ogni argomento:
# 1. Lettura teorica (Reading)
# 2. Lab pratici con ambienti vulnerabili reali
# 3. Community solutions per sbloccarsi

# Per i lab si usa Burp Suite Community (integrata nel browser via Burp's built-in browser)
# Oppure si configura il proprio browser con proxy 127.0.0.1:8080
```

Navigazione consigliata per un principiante:

| Ordine | Argomento | Difficoltà |
|--------|-----------|------------|
| 1 | SQL Injection | Apprentice |
| 2 | Authentication | Apprentice |
| 3 | Path Traversal | Apprentice |
| 4 | XSS | Apprentice → Practitioner |
| 5 | CSRF | Practitioner |
| 6 | SSRF | Practitioner |
| 7 | XXE | Practitioner |
| 8 | JWT Attacks | Practitioner |

I lab sono etichettati per **difficoltà**: **APPRENTICE** (basi, percorso guidato) → **PRACTITIONER** (scenari realistici, richiede metodo) → **EXPERT** (catene complesse, edge case, ricerca). Oltre alle vulnerabilità base, l'Academy copre argomenti **avanzati** spesso oggetto della ricerca PortSwigger: *HTTP request smuggling*, *web cache poisoning*, *prototype pollution*, *OAuth*, *GraphQL*.

## Burp Suite — edizioni e moduli
La piattaforma è strettamente legata a [[Burp Suite]], il proxy d'intercettazione di riferimento:

| Edizione | Note |
|----------|------|
| **Community** (free) | Proxy, Repeater, Decoder; Intruder **rallentato**. Sufficiente per imparare/CTF e per i lab dell'Academy. |
| **Professional** (a pagamento) | Intruder full-speed, **scanner** attivo, BApp store completo, salvataggio progetti. |
| **Enterprise** | Scanning automatizzato in CI/CD, scala aziendale. |

Moduli chiave: **Proxy** (intercetta), **Repeater** (test manuale), **Intruder** (fuzzing/brute), **Decoder/Comparer**, **Collaborator** (rilevamento *blind*/out-of-band → utile per [[Server-Side Request Forgery (SSRF)]]), **Extender/BApp** (estensioni come Autorize per l'access control).

## Quando si usa

- Come **risorsa principale** per apprendere le vulnerabilità web elencate nell'[[OWASP Top 10]]
- Per **praticare** con lab reali senza dover configurare ambienti vulnerabili locali
- Come **riferimento teorico** durante un CTF o un pentest (la documentazione è estremamente dettagliata)
- Per prepararsi a certificazioni web-oriented come eWPT, OSWE, BSCP (Burp Suite Certified Practitioner)
- La certificazione **BSCP** è rilasciata direttamente da PortSwigger ed è riconosciuta nel settore

## Note e trucchi

- Ogni argomento ha lab di tre livelli: **Apprentice** (base), **Practitioner** (medio), **Expert** (avanzato) — iniziare sempre da Apprentice
- I lab hanno un **timer**: l'ambiente si resetta dopo circa 20 minuti — se si resta bloccati, usare il pulsante "Access the lab" di nuovo
- La sezione **Community solutions** (link in ogni lab) mostra video e writeup di altri studenti: ottima per sbloccarsi senza spoilerare tutta la soluzione
- Usare il **Burp Suite Browser integrato** (in Proxy > Intercept) per evitare problemi di configurazione SSL
- Il percorso **"Learning paths"** raggruppa i lab per ordine logico di apprendimento
- Completare tutti i lab di un argomento sblocca un **badge** nel profilo pubblico

## Lab
Questa nota **è** la piattaforma di lab di riferimento della wiki: quasi tutte le altre note Web la citano nella loro sezione `## Lab`. Percorso di partenza consigliato (tutti lab reali, livello APPRENTICE salvo indicazione):
- **SQL injection** → *SQLi UNION attacks* e *Blind SQLi with conditional responses* (vedi [[SQL Injection]], [[sqlmap]]).
- **Authentication** → *Username enumeration via different responses* (vedi [[Autenticazione e Gestione Sessioni]]).
- **Path traversal** → *File path traversal, simple case* (vedi [[File Inclusion (LFI e RFI)]]).
- **Cross-site scripting** → *Reflected XSS into HTML context* → poi PRACTITIONER (vedi [[Cross-Site Scripting (XSS)]]).
- **SSRF / XXE / JWT** (PRACTITIONER) → catene più realistiche.
- Cosa esercitare: usare il **Burp's built-in browser** di [[Burp Suite]] (evita problemi SSL), seguire un **Learning path**, e completare l'intero set di un argomento per il badge. Obiettivo a lungo termine: la certificazione **BSCP**.

## Domande
1. **D:** Quali sono i tre livelli di difficoltà dei lab e cosa distinguono?  **R:** APPRENTICE (basi, percorso guidato), PRACTITIONER (scenari realistici, richiede metodo), EXPERT (catene complesse ed edge case da ricerca).
2. **D:** Che rapporto c'è tra la Web Security Academy e [[Burp Suite]]?  **R:** Entrambe sono di PortSwigger; i lab sono pensati per essere risolti con Burp (Community è sufficiente), tramite il proxy o il browser integrato.
3. **D:** Cosa offre l'Academy oltre alle vulnerabilità dell'[[OWASP Top 10]]?  **R:** Argomenti avanzati di ricerca PortSwigger: HTTP request smuggling, web cache poisoning, prototype pollution, OAuth, GraphQL.
4. **D:** Cos'è la certificazione BSCP?  **R:** Burp Suite Certified Practitioner, rilasciata da PortSwigger e riconosciuta nel settore, orientata al web hacking pratico.
5. **D:** A cosa servono le "Community solutions" e i "Learning paths"?  **R:** Le Community solutions offrono writeup/video per sbloccarsi; i Learning paths raggruppano i lab nell'ordine logico di apprendimento.

## Collegamenti

- [[Burp Suite]]
- [[OWASP Top 10]]
- [[SQL Injection]]
- [[Cross-Site Scripting (XSS)]]
- [[Autenticazione e Gestione Sessioni]]
- [[Cookie e JWT]]
- [[Server-Side Request Forgery (SSRF)]]

## Fonti

- PortSwigger Web Security Academy: https://portswigger.net/web-security
- Burp Suite Certified Practitioner: https://portswigger.net/web-security/certification
