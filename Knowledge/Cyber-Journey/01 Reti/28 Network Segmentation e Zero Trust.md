---
tipo: concetto
tag: [reti, sysadmin, blue-team]
fase: 3
fonti: 3
aggiornato: 2026-06-29
stato: maturo
aliases: ["Network Segmentation e Zero Trust"]
---

# Network Segmentation & Zero Trust

La segmentazione di rete è la prima linea di difesa per contenere le violazioni. Una rete "piatta" permette a un attaccante di compromettere un dispositivo IoT e muoversi liberamente verso i server di database.

## 1. Concetti Chiave della Segmentazione
- **VLAN e Subnetting**: Dividere la rete fisica e logica in compartimenti isolati.
- **Micro-segmentazione**: Segmentazione a livello di host (spesso gestita via software o tramite hypervisor in ambienti virtualizzati), che limita le comunicazioni est-ovest anche all'interno della stessa VLAN.
- **DMZ (Demilitarized Zone)**: Isolare i servizi esposti su Internet dal resto della rete interna.

## 2. Verso la Zero Trust Architecture (ZTA)
Il modello Zero Trust assume che la rete sia già compromessa e che nessuna connessione (interna o esterna) sia affidabile di default.

- **Verifica Continua**: Autenticare e autorizzare rigorosamente ogni accesso in base all'identità, al contesto (dispositivo, posizione) e non in base all'indirizzo IP.
- **Least Privilege Access**: Consentire le comunicazioni solo sulle porte necessarie e solo tra gli host che ne hanno effettivamente bisogno (es. il Web Server può parlare col DB Server sulla porta 3306, ma nient'altro).
- **Isolamento dei Dispositivi non gestiti**: Stampanti, dispositivi IoT e BYOD (Bring Your Own Device) devono risiedere in VLAN separate senza accesso alla rete di produzione.

## 3. Best Practices Pratiche per Sysadmin
1. **Firewall Interni**: Non usare il firewall solo sul perimetro. Posizionare firewall tra segmenti critici (es. tra la rete degli utenti e la rete dei server).
2. **NAC (Network Access Control)**: Implementare soluzioni come 802.1X per garantire che solo i dispositivi autorizzati e conformi (es. con antivirus aggiornato) possano collegarsi alla rete cablata o Wi-Fi.
3. **Jump Server / Bastion Host**: Obbligare gli amministratori a passare attraverso un server di "salto" pesantemente monitorato e protetto per accedere ai segmenti critici (es. DMZ o management network).


## Collegamenti
- [[IAM e Zero Trust]]
- [[Firewall]]
- [[VPN]]
- [[Routing IP]]
- [[Active Directory]]

## Fonti
- NIST SP 800-207 — Zero Trust Architecture: https://csrc.nist.gov/pubs/sp/800/207/final
- CISA — Zero Trust Maturity Model: https://www.cisa.gov/zero-trust-maturity-model
- NIST SP 800-125B — Secure Virtual Network Configuration: https://csrc.nist.gov/pubs/sp/800/125/b/final
