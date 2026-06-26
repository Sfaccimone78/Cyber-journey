---
tipo: sintesi
tag: [web, owasp, moc]
aggiornato: 2026-06-26
stato: maturo
---

# AppSec Avanzato - Mappa

Web hacking di **livello expert** (fase 3-4), oltre l'OWASP base coperto in [[00 — Mappa Web OWASP|05 Web OWASP]]. Qui stanno le classi di bug moderne: gadget chain, attacchi su token e federazione d'identità, desincronizzazione del protocollo HTTP, inquinamento di oggetti e cache, e le race condition lato server.

> [!warning] Uso etico
> Tutte le tecniche di quest'area vanno praticate **solo** su lab dedicati (PortSwigger Web Security Academy, HackTheBox, target con autorizzazione scritta / bug bounty in scope). Eseguirle contro sistemi terzi senza permesso è reato.

Percorso in ordine d'apprendimento (segui la numerazione):

[[Insecure Deserialization Avanzata (gadget chains)]] · [[Attacchi JWT]] · [[OAuth 2.0 e OpenID Connect Attacks]] · [[SAML e SSO Attacks]] · [[HTTP Request Smuggling]] · [[Prototype Pollution]] · [[Race Condition Web]] · [[GraphQL Security]] · [[Web Cache Poisoning]] · [[SSTI Avanzato e Sandbox Escape]]

## Mappa per temi
- **Oggetti & runtime**: [[Insecure Deserialization Avanzata (gadget chains)]] · [[Prototype Pollution]] · [[SSTI Avanzato e Sandbox Escape]]
- **Identità & token**: [[Attacchi JWT]] · [[OAuth 2.0 e OpenID Connect Attacks]] · [[SAML e SSO Attacks]]
- **Protocollo & infrastruttura**: [[HTTP Request Smuggling]] · [[Web Cache Poisoning]] · [[Race Condition Web]]
- **API moderne**: [[GraphQL Security]]

## Prerequisiti (area 05)
Padroneggia prima: [[OWASP Top 10]] · [[Server-Side Template Injection (SSTI)]] · [[Insecure Deserialization]] · [[Cookie e JWT]] · [[Autenticazione e Gestione Sessioni]] · [[Burp Suite]].

## Navigazione
[[00 — Mappa Cloud Security|11 Cloud Security]] <- [[index|Indice]] -> [[00 — Mappa Reverse Engineering e Exploit Dev|13 Reverse Engineering e Exploit Dev]]
