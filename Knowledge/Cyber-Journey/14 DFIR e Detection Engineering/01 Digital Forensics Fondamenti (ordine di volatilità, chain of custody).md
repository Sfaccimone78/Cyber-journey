---
tipo: concetto
tag: [blue-team, metodologia]
fase: 3
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["Digital Forensics Fondamenti", "Ordine di Volatilità", "Chain of Custody"]
---

# Digital Forensics Fondamenti (ordine di volatilità, chain of custody)

## In breve
La **digital forensics** è la disciplina che acquisisce, preserva, analizza e presenta prove
digitali in modo **difendibile** (anche in tribunale). Il principio cardine: le prove vanno
raccolte **dal dato più volatile al meno volatile** e ogni manipolazione deve preservare
l'**integrità** (hash) e la **catena di custodia**. Sbagliare l'ordine o non documentare
distrugge il valore probatorio: è la differenza tra un'investigazione e una contaminazione.

## Principi fondanti
- **Locard's Exchange Principle**: ogni interazione lascia tracce. Un attaccante che tocca un
  sistema lascia artefatti; l'analista che tocca il sistema *altera* artefatti.
- **Ordine di volatilità (RFC 3227)**: raccogli prima ciò che sparisce per primo.
- **Integrità**: ogni acquisizione produce un **hash crittografico** (SHA-256) calcolato prima
  e dopo; se coincidono, la prova non è stata alterata. Vedi [[Hashing delle Password e Salting]]
  per il concetto di hash.
- **Riproducibilità**: un secondo analista deve poter ripetere l'analisi e ottenere lo stesso
  risultato. Si lavora sempre su **copie** (immagini forensi), mai sull'originale.
- **Write blocker**: hardware/software che impedisce scritture sul supporto originale durante
  l'acquisizione del disco.

## Ordine di volatilità (RFC 3227)
Dal più volatile al meno volatile — l'ordine è vincolante:

```text
1. Registri CPU, cache              (microsecondi)
2. RAM: processi, connessioni,      ← Memory Forensics: NON spegnere l'host!
   sessioni, chiavi, malware fileless
3. Stato di rete: ARP, tabelle di
   routing, socket aperti
4. Processi in esecuzione, /tmp
5. Disco: file system, slack space
6. Log remoti e telemetria
7. Configurazioni fisiche, topologia
8. Supporti di archivio, backup, nastri
```

> [!warning] Errore classico
> **Spegnere o riavviare un host compromesso prima di dumpare la RAM** perde malware fileless,
> chiavi di cifratura in chiaro e connessioni C2 attive — prove spesso irrecuperabili dal disco.
> Nel [[Incident Response]] il containment breve isola l'host **mantenendolo acceso**.

## Chain of custody (catena di custodia)
Documento che traccia *chi* ha avuto *cosa*, *quando*, *dove* e *perché*, dal sequestro alla
presentazione. Ogni passaggio di mano è firmato. Una catena rotta = prova inammissibile.

| Campo | Esempio |
|---|---|
| Identificativo prova | EVID-2026-0042 |
| Descrizione | HDD Seagate 1TB S/N XYZ da HOST-12 |
| Acquisito da / quando | M. Rossi, 2026-06-26 14:32 CET |
| Hash acquisizione | SHA-256: 3f5a...c91 |
| Metodo | dd via write blocker Tableau T35u |
| Trasferimenti | → laboratorio (firmato), → analista (firmato) |

## Esempio pratico — acquisizione disco verificata
```bash
# Acquisizione bit-a-bit in formato forense (Expert Witness/E01) con hashing integrato
ewfacquire /dev/sdb \
  -t /evidence/HOST-12_disk \
  -d sha256 -c best -S 2GiB

# Alternativa raw con dd e verifica hash manuale
sudo dd if=/dev/sdb of=/evidence/host12.raw bs=4M conv=noerror,sync status=progress
sha256sum /dev/sdb /evidence/host12.raw   # i due hash DEVONO coincidere

# Verifica integrità di un'immagine E01 in qualsiasi momento
ewfverify /evidence/HOST-12_disk.E01
```

> [!caution] Etica e legalità
> La forensics si esegue **solo** su sistemi di propria competenza o con autorizzazione scritta
> (mandato, incarico aziendale, consenso). Acquisire o analizzare dispositivi altrui senza titolo
> è reato. La gestione di dati personali rientra nel **GDPR**: minimizza, cifra le immagini,
> limita l'accesso. Vedi anche notifica violazione entro 72h.

## Checklist di prima risposta (first responder)
- [ ] Fotografa lo stato (schermo, cavi, periferiche) prima di toccare.
- [ ] Sistema acceso? → **dump RAM** prima di tutto (vedi [[Memory Forensics con Volatility]]).
- [ ] Non spegnere "pulito": rischi shutdown script che cancellano tracce. Valuta pull-the-plug.
- [ ] Acquisisci il disco con **write blocker** + hash SHA-256.
- [ ] Compila la chain of custody **subito**, per ogni reperto.
- [ ] Lavora solo su copie verificate; conserva l'originale in cassaforte.

## Lab
- **TryHackMe** — *Digital Forensics Fundamentals*, *DFIR: An Introduction*, percorso *SOC Level 1/2*.
- **CyberDefenders** — challenge *Packet Detective*, *DumpMe* (catena completa acquisizione→analisi).
- **BlueTeamLabs.online** — investigations introduttive con gestione delle prove.

## Collegamenti
- [[Incident Response]]
- [[Memory Forensics con Volatility]]
- [[Disk Forensics e Timeline Analysis]]
- [[Windows Forensics (artefatti)]]
- [[Indicatori di Compromissione (IOC)]]
- [[Hashing delle Password e Salting]]

## Fonti
- RFC 3227 — Guidelines for Evidence Collection and Archiving: https://www.rfc-editor.org/rfc/rfc3227
- NIST SP 800-86 — Guide to Integrating Forensic Techniques into IR: https://csrc.nist.gov/pubs/sp/800/86/final
- SANS — Digital Forensics & Incident Response: https://www.sans.org/cyber-security-courses/?focus-area=digital-forensics-incident-response
- SWGDE Best Practices for Digital Evidence Collection: https://www.swgde.org/
