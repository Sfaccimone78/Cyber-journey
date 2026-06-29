---
tipo: sintesi
tag: [devsecops, supply-chain, moc]
fase: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["DevSecOps e Supply Chain", "DevSecOps & Supply Chain", "Mappa DevSecOps e Supply Chain"]
---

# DevSecOps e Supply Chain - Mappa

Il software moderno non viene piu scritto: viene assemblato. Ogni build tira dentro centinaia di dipendenze transitive, gira su runner condivisi, viene firmata da pipeline automatiche e distribuita come container o pacchetto. La superficie d'attacco si sposta cosi dal codice applicativo alla **catena di produzione** stessa: chi compromette la pipeline o una dipendenza upstream colpisce a valle migliaia di vittime con un solo punto di ingresso. Questo filo conduttore parte dalla cultura e dai principi del DevSecOps (shift-left, security as code), entra nel cuore della CI/CD e dei suoi abusi (poisoned pipeline execution, runner self-hosted), copre gli strumenti di analisi automatica (SAST, DAST, SCA), affronta gli attacchi alla supply chain delle dipendenze (typosquatting, dependency confusion), introduce gli standard di integrita e provenienza (SBOM, SLSA, firma con cosign) e chiude con la gestione dei segreti e la sicurezza dell'Infrastructure as Code. L'obiettivo e ragionare come chi difende e come chi attacca l'intero ciclo di vita del software, non solo il prodotto finale.

## Percorso in ordine d'apprendimento

1. [[01 Fondamenti DevSecOps|Fondamenti DevSecOps]]
2. [[02 Sicurezza CI-CD Pipeline|Sicurezza CI-CD Pipeline]]
3. [[03 SAST, DAST e SCA|SAST, DAST e SCA]]
4. [[04 Supply Chain e Dependency Confusion|Supply Chain e Dependency Confusion]]
5. [[05 SBOM e SLSA|SBOM e SLSA]]
6. [[06 Secrets Management e IaC Security|Secrets Management e IaC Security]]

## Collegamenti trasversali

- [[Container Security (Docker)]] - la pipeline produce immagini: scansione, firma e immutabilita dei layer.
- [[Kubernetes Security (RBAC, escape)]] - il deploy finisce in cluster, dove RBAC e admission control filtrano cosa entra.
- [[Penetration Testing]] - il red teaming della supply chain estende la metodologia offensiva alla catena di build.

## Navigazione

[[00 — Mappa AI e LLM Security|18 AI e LLM Security]] <- [[index|Indice]] -> [[00 — Mappa GRC e Compliance|20 GRC e Compliance]]
