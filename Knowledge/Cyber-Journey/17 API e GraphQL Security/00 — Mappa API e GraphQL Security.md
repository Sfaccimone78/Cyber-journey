---
tipo: sintesi
tag: [api, web, moc]
fase: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["API e GraphQL Security", "API & GraphQL Security", "Mappa API e GraphQL Security"]
---

# API e GraphQL Security - Mappa

Le API sono ormai la superficie d'attacco dominante delle applicazioni moderne: ogni app mobile, SPA o microservizio espone endpoint REST o GraphQL che parlano JSON e spesso replicano logiche di business sensibili senza la protezione di una UI. A differenza del web tradizionale, qui mancano i confini visivi: un'API si fida dell'`id` che riceve, del campo che il client invia, del token che presenta. Questo filo conduttore parte dai fondamenti di REST e dal modello di minaccia OWASP API Security Top 10, attraversa le vulnerabilità di autorizzazione che dominano la classifica (BOLA e BFLA), approfondisce autenticazione e gestione dei token, passa per mass assignment, SSRF e rate limiting, e chiude con il toolchain offensivo per testare API reali. L'obiettivo è ragionare come chi disegna e come chi attacca un contratto API.

## Percorso in ordine d'apprendimento

1. [[Fondamenti API e REST Security]]
2. [[OWASP API Security Top 10]]
3. [[BOLA e BFLA]]
4. [[Autenticazione e Autorizzazione API]]
5. [[Mass Assignment, SSRF e Rate Limiting API]]
6. [[API Testing e Tooling]]

## Collegamenti trasversali

- [[OWASP Top 10]]
- [[Broken Access Control e IDOR]]
- [[GraphQL Security]]
- [[Cookie e JWT]]
- [[Server-Side Request Forgery (SSRF)]]
- [[Penetration Testing]]

## Navigazione

[[00 — Mappa Wireless & Radio|16 Wireless & Radio]] <- [[index|Indice]] -> [[00 — Mappa AI e LLM Security|18 AI e LLM Security]]
