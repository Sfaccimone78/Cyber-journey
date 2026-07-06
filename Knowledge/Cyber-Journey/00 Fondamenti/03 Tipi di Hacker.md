---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 2
aggiornato: 2026-07-02
stato: maturo
aliases: ["Tipi di Hacker"]

---
# Tipi di Hacker

## In breve
Il termine **hacker** non significa automaticamente "criminale". Indica una persona con competenze tecniche avanzate. La distinzione avviene tramite il colore del "cappello" (white/black/grey hat) e il ruolo nel team di sicurezza (red/blue/purple).

## Hat

|     Tipo      |                                                            Descrizione                                                             |
| :-----------: | :--------------------------------------------------------------------------------------------------------------------------------: |
| **White Hat** |   **Hacker etico**: <br>Attacca sistemi con il permesso del proprietario per trovare falle. <br>È un lavoro legale e richiesto.    |
| **Black Hat** |        **Hacker malintenzionato:** <br>Attacca sistemi senza permesso per scopi criminali (furto, estorsione, sabotaggio).         |
| **Grey Hat**  | **Via di mezzo**: <br>Viola sistemi senza permesso, ma senza intento criminale. <br>Rimane illegale nella maggior parte dei paesi. |

**Team di sicurezza aziendale**

- **Red Team**: simula attacchi reali contro l'organizzazione. Pensa come un attaccante. Usa le stesse tecniche dei black hat, ma con autorizzazione. Segue spesso la [[La Cyber Kill Chain|Kill Chain]].
- **Blue Team**: difende attivamente l'organizzazione. Monitora reti, risponde agli incidenti, gestisce i [[CVE e CVSS|CVE]]. Lavora nei [[Percorsi di Carriera Pentester vs SOC|SOC (Security Operations Center)]].
- **Purple Team**: non è un team separato, ma una modalità collaborativa in cui red e blue lavorano insieme per massimizzare l'apprendimento da ogni esercizio.

## Esempio

Una banca assume un red team esterno per tentare di bucare la rete interna durante tre settimane. Il blue team interno cerca di rilevare e bloccare gli attacchi. Alla fine, entrambi i team si riuniscono (modalità purple) per discutere cosa ha funzionato e cosa no.

## Perché conta

Capire i ruoli ti aiuta a orientarti nella scelta del [[Percorsi di Carriera Pentester vs SOC|percorso di carriera]]: preferisci attaccare (red) o difendere (blue)? Entrambe le strade richiedono competenze tecniche solide, ma mentalità differenti.

## Lab
- **[[TryHackMe]]** → room *Careers in Cyber* e *Red Team Fundamentals* / *Security Operations*: confronta mentalità e attività di red vs blue team descritte qui.
- **[[TryHackMe]]** → percorso *Jr Penetration Tester* (lato red) oppure *SOC Level 1* (lato blue): scegline uno e nota quali tecniche e tool cambiano tra offensiva e difesa.
- Esercizio: leggi un report di penetration test pubblico e classifica ogni azione come tipica di white hat, e ogni contromisura come attività di blue team.

## Domande
1. **D:** Il termine "hacker" implica di per sé un criminale? **R:** No: indica una persona con competenze tecniche avanzate; la distinzione la fa il "cappello" (white/black/grey) e il contesto di autorizzazione.
2. **D:** Qual è la differenza legale tra white hat e grey hat? **R:** Il white hat attacca con permesso del proprietario (legale); il grey hat viola i sistemi senza permesso ma senza intento criminale, restando comunque illegale nella maggior parte dei paesi.
3. **D:** Cosa distingue un red team da un black hat, visto che usano le stesse tecniche? **R:** L'autorizzazione: il red team opera con mandato dell'organizzazione, il black hat no.
4. **D:** Cos'è il Purple Team? **R:** Non un team separato, ma una modalità collaborativa in cui red e blue lavorano insieme per massimizzare l'apprendimento da ogni esercizio.
5. **D:** Di cosa si occupa principalmente il blue team? **R:** Difende attivamente l'organizzazione: monitora le reti, risponde agli incidenti e gestisce/prioritizza i CVE, tipicamente in un SOC.

## Collegamenti
- [[La Cyber Kill Chain]] — il red team ne segue le fasi per simulare un attacco reale
- [[Percorsi di Carriera Pentester vs SOC]] — red (offensive) vs blue (SOC/difesa)
- [[CVE e CVSS]] — il blue team gestisce e prioritizza le vulnerabilità note
- [[Cos'è la Sicurezza Informatica]] — inquadramento generale della disciplina

## Fonti
- NIST SP 800-115 — Technical Guide to Information Security Testing and Assessment: https://csrc.nist.gov/pubs/sp/800/115/final
- MITRE ATT&CK — framework di tattiche per red/blue/purple teaming: https://attack.mitre.org/

