---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 2
aggiornato: 2026-06-26
stato: maturo
aliases: ["Triade CIA"]
---
# Triade CIA

La **Triade CIA** non è uno slogan: è la **griglia di classificazione** con cui si decide *cosa* un
controllo di sicurezza sta proteggendo e *contro cosa*. Ogni vulnerabilità, ogni exploit, ogni difesa
si proietta su almeno uno dei tre assi — **C**onfidentiality (Riservatezza), **I**ntegrity (Integrità),
**A**vailability (Disponibilità). Sapere quale asse è in gioco guida la scelta del controllo giusto.

## Riservatezza — *chi può leggere il dato*
Garantire che l'informazione sia leggibile **solo** dai soggetti autorizzati. Si ottiene su due
livelli che lavorano insieme:

- **Crittografia** — rende il dato illeggibile a chi non ha la chiave. A *riposo* (disco cifrato,
  colonna DB cifrata) e in *transito* ([[TLS e SSL|TLS]]). Vedi [[Crittografia Simmetrica]] (velocità,
  stessa chiave) e [[Crittografia Asimmetrica]] (scambio chiave senza canale sicuro).
- **Controllo d'accesso** — decide *chi* ottiene la chiave / il permesso: autenticazione (chi sei) +
  autorizzazione (cosa puoi). È il dominio di [[IAM e Zero Trust]].

> La cifratura senza controllo d'accesso è inutile (chiunque abbia la chiave legge); il controllo
> d'accesso senza cifratura è aggirabile (basta leggere il disco a basso livello). Servono entrambi.

**Attacchi che la violano:** dump di un database ([[SQL Injection]]), sniffing di traffico in chiaro
([[Man-in-the-Middle (MITM)]]), furto credenziali ([[Pass-the-Hash]]), [[Cross-Site Scripting (XSS)]]
che ruba cookie di sessione.

## Integrità — *il dato è quello giusto e non è stato toccato*
Garantire che i dati non siano alterati da soggetti non autorizzati, e che un'alterazione sia
**rilevabile**. Il meccanismo chiave è il *fingerprint crittografico*:

- **Funzioni di hash** ([[Funzioni di Hash]]) — un bit cambiato → hash completamente diverso (effetto
  valanga). Confrontando l'hash atteso con quello calcolato si scopre la manomissione.
- **HMAC / firma digitale** ([[Firma Digitale]]) — aggiungono *autenticità*: non solo "il dato non è
  cambiato", ma "viene davvero da chi dice". Un hash semplice prova solo l'integrità, non l'origine
  (un attaccante può ricalcolare l'hash dopo aver modificato il dato — per questo serve una chiave).

**Attacchi che la violano:** alterazione di log per coprire tracce (vedi [[Log Analysis]]), modifica
di un bonifico in transito, [[Insecure Deserialization]], avvelenamento di un update software.

## Disponibilità — *il dato c'è quando serve*
Garantire che sistemi e dati siano raggiungibili. Si difende con **ridondanza** (più repliche, niente
single point of failure), **scalabilità** (assorbire i picchi), **backup** e **disaster recovery**
(ripristino dopo un disastro), e protezione anti-saturazione.

**Attacchi che la violano:** [[DoS e DDoS]] che satura banda/CPU, **ransomware** (cifra i dati e ne
nega la disponibilità — colpisce C *e* A), cancellazione distruttiva.

## I tre assi sono in tensione tra loro
Massimizzarne uno spesso erode gli altri — la sicurezza è un **bilanciamento**, non un massimo
assoluto:
- Cifratura aggressiva + backup off-line (↑C, ↑I) → ripristino più lento (↓A).
- Ridondanza geografica (↑A) → più copie del dato da proteggere (↓C: superficie più ampia).
- Controlli d'accesso rigidi (↑C) → attrito per gli utenti, che cercano scorciatoie (↓ sicurezza reale).

## Oltre la triade: AAA e l'esagono di Parker
Oltre ai tre pilastri, due estensioni ricorrenti:

- **Modello AAA + auditing** — spesso si aggiungono **Authentication** (chi sei),
  **Authorization** (cosa puoi), **Non-repudiation** (non puoi negare un'azione) e
  **Accountability/auditing** (tracciabilità di chi ha fatto cosa). È la base operativa del
  controllo d'accesso e del logging.
- **Parkerian Hexad** — modello esteso che aggiunge tre proprietà utili in incident response:
  **Autenticità** (l'origine è genuina), **Non ripudio** (chi ha agito non può negarlo — base legale
  delle firme digitali), **Possesso/Controllo** (un dato può essere rubato anche restando riservato:
  un backup cifrato sottratto viola il possesso, non la riservatezza).

> [!note] Ransomware "double extortion"
> Il ransomware moderno non si limita a cifrare i dati (colpisce **A**): prima li **esfiltra** e
> minaccia di pubblicarli (colpisce anche **C**). Questo "double extortion" è l'esempio canonico di
> attacco che viola più pilastri insieme.

## Esempio — home banking, mappato sui controlli
- **C**: TLS sul traffico, hashing+salting delle password ([[Hashing delle Password e Salting]]),
  RBAC sul conto → vedi solo il *tuo* saldo.
- **I**: firma/HMAC sulle transazioni → l'importo del bonifico non è alterabile in transito.
- **A**: cluster ridondato + anti-DDoS → servizio raggiungibile 24/7.

Un attacco può colpire un asse, due o tutti e tre insieme (il ransomware è l'esempio classico di
attacco doppio C+A).

## Collegamenti
- [[Cos'è la Sicurezza Informatica]] · [[Difesa in Profondità]] · [[Vulnerabilità Exploit e Minaccia]]
- Controlli per asse: [[Crittografia Simmetrica]] · [[Crittografia Asimmetrica]] · [[Funzioni di Hash]] · [[Firma Digitale]] · [[IAM e Zero Trust]]

## Fonti
- NIST SP 800-12 / 800-53 — definizioni di confidentiality, integrity, availability.
- Donn Parker, *Fighting Computer Crime* (Parkerian Hexad).
- Anderson, *Security Engineering* — https://www.cl.cam.ac.uk/~rja14/book.html
