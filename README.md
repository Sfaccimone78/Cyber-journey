# 🛡️ Cyber Journey — Knowledge Base di Cybersecurity

Wiki di **cybersecurity** in italiano: un *second brain* in Markdown
(compatibile [Obsidian](https://obsidian.md)), costruito come knowledge base
permanente invece di ricostruire la conoscenza a ogni domanda.

> **Modello**: la conoscenza si **compila una volta e si mantiene**. Le fonti grezze restano
> immutabili; le pagine wiki sintetizzano, collegano e restano aggiornate. Vedi lo
> [schema della wiki](Knowledge/Cyber-Journey/WIKI_SCHEMA.md).

📊 **~280 pagine** · 11 aree tematiche · interamente cross-linkata con `[[wikilink]]`.

> 🎯 **Punto di partenza:** il [**Piano di Studio**](Knowledge/Cyber-Journey/Sintesi/Piano_cybersecurity.md)
> (percorso 15 mesi verso Junior Pentester / SOC Analyst L1, con tronco comune e biforcazione).

---

## 📂 Struttura

Tutta la wiki vive in [`Knowledge/Cyber-Journey/`](Knowledge/Cyber-Journey). È organizzata
**per area**: ogni cartella è numerata e contiene una mappa (`00 — Mappa <Area>.md`) più note
con prefisso numerico che dà l'ordine d'apprendimento.

| # | Area | Contenuto |
|---|------|-----------|
| 00 | [Fondamenti](Knowledge/Cyber-Journey/00%20Fondamenti) | Triade CIA, kill chain, threat modeling, carriere, certificazioni |
| 01 | [Reti](Knowledge/Cyber-Journey/01%20Reti) | OSI/TCP-IP, indirizzamento, protocolli, Wireshark, attacchi di rete |
| 02 | [Linux](Knowledge/Cyber-Journey/02%20Linux) | CLI, permessi, processi, scripting, privilege escalation |
| 03 | [Crittografia](Knowledge/Cyber-Journey/03%20Crittografia) | Simmetrica/asimmetrica, hash, TLS, RSA, ECC, post-quantum |
| 04 | [Windows e AD](Knowledge/Cyber-Journey/04%20Windows%20e%20AD) | Active Directory, Kerberos, NTLM, lateral movement, attacchi AD |
| 05 | [Web OWASP](Knowledge/Cyber-Journey/05%20Web%20OWASP) | OWASP Top 10, SQLi, XSS, SSRF, Burp Suite, PortSwigger |
| 06 | [Metodologia e Tool](Knowledge/Cyber-Journey/06%20Metodologia%20e%20Tool) | Fasi del pentest, Nmap, Metasploit, reporting, piattaforme |
| 07 | [Blue Team](Knowledge/Cyber-Journey/07%20Blue%20Team) | SIEM, detection, IR, MITRE ATT&CK, YARA/Sigma, Zeek/Suricata |
| 08 | [Sistemi Operativi](Knowledge/Cyber-Journey/08%20Sistemi%20Operativi) | Processi, scheduling, memoria virtuale, filesystem, virtualizzazione |
| 09 | [Python](Knowledge/Cyber-Journey/09%20Python) | Python per la sicurezza, socket, scripting offensivo |
| 10 | [Algoritmi e Strutture Dati](Knowledge/Cyber-Journey/10%20Algoritmi%20e%20Strutture%20Dati) | Strutture dati, grafi, sorting, DP, complessità |

### Cartelle trasversali

- **[`Fonti/`](Knowledge/Cyber-Journey/Fonti)** — fonti grezze (riassunti di articoli, libri, room). Verità immutabile, mai modificate.
- **[`Risorse/`](Knowledge/Cyber-Journey/Risorse)** — indice di risorse esterne e PDF di riferimento.
- **[`Sintesi/`](Knowledge/Cyber-Journey/Sintesi)** — overview, tabelle comparative, mappe (MOC), roadmap.
- **[`Template/`](Knowledge/Cyber-Journey/Template)** — template per nuove pagine.

---

## 🧭 Come si naviga

- **In Obsidian** (consigliato): apri `Knowledge/Cyber-Journey/` come vault. Usa la *graph view*
  per vedere hub e collegamenti, e [`index.md`](Knowledge/Cyber-Journey/index.md) come catalogo.
- **Su GitHub**: parti da una mappa d'area (`00 — Mappa <Area>.md`) e segui i link, oppure
  dall'[indice](Knowledge/Cyber-Journey/index.md).

## 🔧 Come si mantiene

Ogni pagina ha un frontmatter YAML (`tipo`, `tag`, `stato`, `aliases`, …) per le query
[Dataview](https://github.com/blacksmithgu/obsidian-dataview). Il workflow di
**ingest** (acquisire una fonte) e **lint** (controllo integrità: link rotti, orfani,
contraddizioni) è descritto nello [schema della wiki](Knowledge/Cyber-Journey/WIKI_SCHEMA.md). La cronologia
degli eventi è in [`log.md`](Knowledge/Cyber-Journey/log.md).

---

## ⚠️ Nota etica

Tecniche, payload e tool documentati qui sono a scopo **didattico** e per **lab/CTF autorizzati**
(TryHackMe, HackTheBox, PortSwigger) o ingaggi con autorizzazione scritta. Usarli contro sistemi
di terzi senza consenso è illegale.

---

*Lingua: italiano · Repository pubblico.*
