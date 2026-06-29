---
tipo: sintesi
tag: [ai, llm, moc]
fase: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["AI e LLM Security", "Mappa AI e LLM Security"]
---

# AI e LLM Security - Mappa

L'adozione massiva di modelli linguistici (LLM) e applicazioni generative ha introdotto una superficie d'attacco inedita: il confine tra dati e istruzioni collassa nel prompt, e l'LLM diventa un interprete fidato di input non fidati. Questa area parte dai fondamenti dell'architettura (tokenizzazione, system/user prompt, RAG, embeddings, agenti con tool-use) per capire dove e perche un modello puo essere manipolato. Si prosegue con la tassonomia di riferimento (OWASP Top 10 for LLM Applications), per poi approfondire le classi d'attacco principali: prompt injection diretta e indiretta, avvelenamento di dati e modelli, gestione insicura dell'output e rischi di supply chain del modello. Il filo conduttore e duplice: capire perche le difese deterministiche classiche non bastano contro un sistema probabilistico, e costruire una strategia di difesa a livelli (input/output filtering, isolamento dei privilegi, human-in-the-loop) validata da red teaming continuo.

## Percorso in ordine d'apprendimento

- [[01 Fondamenti AI e LLM Security|Fondamenti AI e LLM Security]]
- [[02 OWASP Top 10 for LLM Applications|OWASP Top 10 for LLM Applications]]
- [[03 Prompt Injection (direct e indirect)|Prompt Injection (direct e indirect)]]
- [[04 Data e Model Poisoning|Data e Model Poisoning]]
- [[05 Insecure Output e Supply Chain LLM|Insecure Output e Supply Chain LLM]]
- [[06 Difesa e Red Teaming LLM|Difesa e Red Teaming LLM]]

## Collegamenti trasversali

- [[OWASP Top 10]] - la tassonomia LLM eredita e specializza concetti come injection e broken access control.
- [[Penetration Testing]] - il red teaming LLM estende la metodologia di test offensivo ai sistemi generativi.
- [[Insecure Deserialization]] - rilevante per il caricamento insicuro di modelli serializzati (pickle/PyTorch) nella supply chain.

## Navigazione

[[00 — Mappa API e GraphQL Security|17 API e GraphQL Security]] <- [[index|Indice]] -> [[00 — Mappa DevSecOps e Supply Chain|19 DevSecOps e Supply Chain]]
