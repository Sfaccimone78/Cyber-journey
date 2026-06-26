---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 1
aggiornato: 2026-06-22
stato: maturo
aliases: ["Superficie di Attacco"]
---
# Superficie di Attacco

La **superficie di attacco** è l'insieme di **tutti i punti** attraverso cui un attaccante può tentare
di entrare o estrarre dati. È una proprietà *misurabile* e *riducibile*: meno punti esposti → meno
opportunità. Per il pentester la fase di [[Ricognizione (Recon)]] serve esattamente a **mapparla**;
per il difensore, a **restringerla**.

## Superficie ≠ vettore
Distinzione operativa fondamentale:
- **Superficie di attacco** = tutti i punti esposti (le *porte* dell'edificio).
- **Vettore di attacco** = il percorso specifico usato in un attacco (la *porta da cui sono entrato*).
- **Attack vector ≠ attack surface ≠ exploit**: la superficie è il "dove possibile", il vettore è il
  "come effettivo", l'[[Vulnerabilità Exploit e Minaccia|exploit]] è lo strumento che attiva il difetto.

## Le tre dimensioni
1. **Digitale (rete/software)** — tutto ciò che è raggiungibile o eseguibile:
   - **Porte e servizi** esposti — ogni servizio in ascolto è un ingresso (22/SSH, 80-443/HTTP,
     445/[[SMB]], 3389/[[RDP]]). Si enumerano con [[Nmap]] (vedi [[Scansione delle Porte]]).
   - **Applicazioni web** — endpoint, form, API, parametri, upload ([[Vulnerabilita Upload File]]),
     cookie/sessioni. Spesso la superficie più ricca e mutevole.
   - **Dipendenze e terze parti** — librerie con [[CVE e CVSS|CVE]] noti, SaaS collegati, supply chain.
2. **Fisica** — porte USB, accesso ai server, badge, console non bloccate.
3. **Umana / sociale** — le persone manipolabili: la superficie sfruttata dal
   [[Social Engineering e Phishing]]. Spesso la più facile da bucare.

## Misurare e gestire (ASM)
"Non puoi proteggere ciò che non sai di avere." La disciplina si chiama **Attack Surface Management**:

1. **Discovery** — inventario continuo di asset, sottodomini, IP, certificati, servizi. Strumenti
   esterni (EASM): Shodan, Censys, [[OSINT]]; interni: scansioni di rete.
2. **Classificazione** — quali asset sono critici / esposti / dimenticati (*shadow IT*, server di test
   lasciati online — la causa di moltissime compromissioni reali).
3. **Monitoraggio** — la superficie **cambia di continuo** (nuovo deploy, porta aperta per debug e mai
   richiusa, certificato scaduto). Lo snapshot di ieri non vale oggi.

## Ridurre la superficie — principi concreti
- **Minimizzazione** — disattiva servizi/porte/feature non necessari (il principio del *minimo
  necessario* applicato all'esposizione).
- **Minimo privilegio** — meno permessi attivi = meno da rubare/abusare ([[IAM e Zero Trust]]).
- **Segmentazione** — isolare le reti limita *quanto in profondità* un attaccante arriva dopo essere
  entrato (vedi [[Difesa in Profondità]], [[Pivoting]]).
- **Patch & hardening** — chiudere i difetti sui punti che *devono* restare esposti.
- **Chiudere lo shadow IT** — il server dimenticato è superficie che non stai nemmeno difendendo.

## Esempio — letto come un attaccante
Un'azienda espone: FTP anonimo (porta 21), un WordPress di staging senza MFA su un sottodominio
dimenticato, e dipendenti con password riusate. `nmap` rivela le porte; un sottodominio
(`staging.azienda.com`) emerge da certificate transparency; il WordPress di test diventa il **vettore**;
le credenziali riusate permettono il [[Lateral Movement|movimento laterale]]. Ogni elemento è un pezzo
di superficie che *non serviva* essere lì.

## Collegamenti
- [[Ricognizione (Recon)]] · [[OSINT]] · [[Scansione delle Porte]] · [[Nmap]]
- Riduzione: [[Difesa in Profondità]] · [[IAM e Zero Trust]] · [[CVE e CVSS]] · [[Social Engineering e Phishing]]

## Fonti
- OWASP — Attack Surface Analysis Cheat Sheet.
- NIST SP 800-53 / Gartner — Attack Surface Management (ASM/EASM).
