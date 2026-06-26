---
tipo: concetto
tag:
  - fondamenti
fase: 0
fonti: 1
aggiornato: 2026-06-22
stato: maturo
aliases:
  - Cos'è la Sicurezza Informatica
---
# Cos'è la Sicurezza Informatica

La **sicurezza informatica** è l'insieme di pratiche, tecnologie e processi che proteggono sistemi,
reti e dati da accessi non autorizzati, alterazioni o interruzioni. Detta così sembra astratta; il
suo nucleo concreto è uno solo: **gestire il rischio** verso i tre pilastri della [[Triade CIA]]
(Riservatezza, Integrità, Disponibilità). Tutto il resto — tool, ruoli, certificazioni — sono mezzi
per questo fine.

## Perché esiste: l'economia dell'attacco
La sicurezza non è "rendere impossibile" l'attacco (impossibile), ma **renderlo più costoso del suo
guadagno**. L'attaccante ragiona in costi/benefici: tempo, competenze, rischio di essere scoperto vs
valore del bottino. Ogni controllo sposta quell'equazione. Per questo non esiste "sicuro al 100%":
esiste un livello di rischio *accettabile* per un dato contesto. Vedi
[[Vulnerabilità Exploit e Minaccia]] per la formula del rischio.

## Le tre grandi anime operative
- **Offensive Security (Red Team)** — *pensare da attaccante*. Penetration tester ed ethical hacker
  simulano attacchi **autorizzati** per trovare le falle prima dei criminali. Metodo in
  [[Metodologia del Pentest]].
- **Defensive Security (Blue Team)** — *difendere e rilevare*. Il SOC monitora, rileva e risponde agli
  attacchi reali tramite [[SIEM]], [[Log Analysis]], [[Incident Response]].
- **Governance, Risk & Compliance (GRC)** — *le regole*. Standard e leggi (GDPR, ISO 27001, NIST CSF)
  che definiscono cosa un'organizzazione *deve* fare. Trasforma la sicurezza da scelta tecnica a
  obbligo verificabile.

> Red e Blue non sono nemici: insieme formano il **Purple Team** — l'offensiva che alimenta la difesa.
> Vedi [[Pentester vs SOC]].

## I domini tecnici (dove si applica)
La stessa logica CIA si declina su superfici diverse, ognuna con tool e attacchi propri:
- **Network security** — protocolli, firewall, segmentazione (area [[Modello OSI|Reti]]).
- **Endpoint / OS security** — Linux e Windows hardening, EDR ([[EDR e XDR]]).
- **Application & Web security** — il codice e le sue falle ([[OWASP Top 10]]).
- **Identity & Access** — chi può fare cosa ([[IAM e Zero Trust]]).
- **Crittografia** — il livello matematico che rende possibile riservatezza e integrità
  ([[Encoding vs Encryption]]).
- **Cloud / OT / Mobile** — superfici moderne con modelli di responsabilità condivisa.

## Il principio che tiene tutto insieme
Sotto ogni dominio c'è la [[Triade CIA]] come griglia di valutazione, e sopra c'è la
[[Difesa in Profondità]] come strategia: nessun controllo singolo regge, servono strati. Imparare la
cybersecurity = imparare, per ogni tecnologia, *come funziona* → *come si rompe* → *come si difende*.

## Esempio
Una banca protegge i conti con: firewall e segmentazione (perimetro), cifratura dei dati
(riservatezza), backup giornalieri e ridondanza (disponibilità), firme sulle transazioni (integrità),
MFA (accesso), un SOC che monitora i log (rilevamento). Periodicamente ingaggia pentester per
*testare se queste difese reggono davvero* — chiudendo il ciclo offensiva→difesa.

## Collegamenti
- [[Triade CIA]] · [[Difesa in Profondità]] · [[Vulnerabilità Exploit e Minaccia]] · [[Pentester vs SOC]]
- Domini: [[Risk Management e Compliance]] · [[IAM e Zero Trust]] · [[OWASP Top 10]] · [[Metodologia del Pentest]]

## Fonti
- NIST Cybersecurity Framework (CSF) · ISO/IEC 27001.
- NIST SP 800-12 — An Introduction to Information Security.
