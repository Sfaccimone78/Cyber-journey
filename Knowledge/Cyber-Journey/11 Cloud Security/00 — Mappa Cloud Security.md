---
tipo: sintesi
tag: [cloud, moc]
fase: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["Mappa Cloud Security"]
---

# Cloud Security - Mappa

Area **avanzata/expert** (fase 3-4) che copre il gap cloud. Il filo conduttore va dalla teoria del
modello di responsabilità condivisa fino allo sfruttamento concreto di misconfigurazioni cloud,
container e Kubernetes, chiudendo con il rilevamento.

**Filo conduttore:** prima capisci *chi è responsabile di cosa* ([[Fondamenti Cloud e Shared Responsibility]]),
poi il cuore di ogni cloud — l'identità ([[IAM Cloud (utenti, ruoli, policy)]]) — declinata sui due
provider dominanti ([[AWS Sicurezza (S3, EC2, IAM, STS)]], [[Azure e Entra ID Sicurezza]]). Da lì
entri in offensiva: l'innesco classico è la [[SSRF e Metadata Service (IMDS)]] che ruba credenziali,
che alimenta la [[Privilege Escalation in Cloud]]. Scendi poi nel piano di esecuzione moderno —
[[Container Security (Docker)]] e [[Kubernetes Security (RBAC, escape)]] — e infine ribalti la
prospettiva sul blue team con [[Logging e Detection Cloud (CloudTrail)]].

## Percorso in ordine d'apprendimento

1. [[Fondamenti Cloud e Shared Responsibility]] — modelli di servizio, shared responsibility, attack surface
2. [[IAM Cloud (utenti, ruoli, policy)]] — identità, ruoli, policy, principio del minimo privilegio
3. [[AWS Sicurezza (S3, EC2, IAM, STS)]] — i servizi chiave AWS e i loro abusi
4. [[Azure e Entra ID Sicurezza]] — Azure RBAC, Entra ID, Managed Identity
5. [[SSRF e Metadata Service (IMDS)]] — l'attacco che ruba credenziali alla macchina
6. [[Privilege Escalation in Cloud]] — da accesso minimo a controllo totale
7. [[Container Security (Docker)]] — immagini, namespace, capabilities, escape
8. [[Kubernetes Security (RBAC, escape)]] — RBAC, pod escape, lateral movement
9. [[Logging e Detection Cloud (CloudTrail)]] — telemetria, detection, threat hunting cloud

## Collegamenti trasversali
- [[IAM e Zero Trust]] — fondamento teorico dell'identità
- [[Server-Side Request Forgery (SSRF)]] — la vulnerabilità web che innesca l'attacco cloud
- [[Penetration Testing]] — metodologia generale
- [[MITRE ATT&CK]] — la matrice Cloud mappa queste tecniche

## Navigazione
[[00 — Mappa Algoritmi e Strutture Dati|10 Algoritmi e Strutture Dati]] <- [[index|Indice]]
