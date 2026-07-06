---
tipo: sintesi
tag: [indice, moc]
aggiornato: 2026-06-23
stato: attivo
aliases: ["Home", "Homepage"]
---

# 🏡 Benvenuto nel tuo Cybersecurity Second Brain

> *"La sicurezza informatica non si impara memorizzando comandi, ma capendo come funzionano i sistemi reali."*

Sei all'inizio del tuo percorso. Questa Wiki è la tua centrale di controllo (Second Brain) per memorizzare, collegare e strutturare tutto ciò che studi. Non avere fretta: costruisci fondamenta solide prima di passare agli strumenti avanzati.

---

## 🟢 1. I FONDAMENTALI (Da dove iniziare)

Questi 5 pilastri costituiscono il tronco comune per qualsiasi ruolo futuro (Pentester o SOC Analyst). Studiali uno alla volta, seguendo l'ordine numerico delle mappe.

*   **[[00 — Mappa Fondamenti|🟢 Fondamenti di Sicurezza]]**
    *   La base teorica di tutto: la [[Triade CIA]], la [[Difesa in Profondità]] e la [[Vulnerabilità Exploit e Minaccia]].
*   **[[00 — Mappa Reti|🌐 Reti Informatiche]]**
    *   Come si scambiano dati i computer: il [[Modello TCP-IP]], gli indirizzi IP e gli strumenti di base come [[Ping e Traceroute]].
*   **[[00 — Mappa Linux|🐧 Linux e Terminale]]**
    *   Impara a muoverti nella riga di comando senza paura: comandi base, filesystem e permessi.
*   **[[00 — Mappa Windows e AD|🪟 Windows Base]]**
    *   *Nota per principianti:* Concentrati esclusivamente su filesystem, utenti locali e PowerShell. Metti in pausa la sezione "Active Directory" per il momento.
*   **[[00 — Mappa Crittografia|🔐 Crittografia di Base]]**
    *   Capire la differenza tra cifratura (AES/RSA) e Hashing, ed [[Encoding vs Encryption]].

---

## 🕸️ 2. APPLICAZIONE E STRUMENTI (Fase Successiva)

Accedi a queste aree solo dopo aver consolidato i Fondamentali qui sopra.

*   **[[00 — Mappa Web OWASP|🕸️ Sicurezza Web (OWASP)]]**
    *   Le 10 vulnerabilità web più comuni (es. [[SQL Injection]], [[Cross-Site Scripting (XSS)]]).
*   **[[00 — Mappa Metodologia e Tool|🎯 Metodologia e Strumenti]]**
    *   Il flusso di lavoro di un attacco e i tool basilari (es. scansione con [[Nmap]], connessioni con [[netcat]]).
    *   *Pianificazione futura:* Consulta la lista degli [[Strumenti da studiare in futuro]].
*   **[[00 — Mappa Python|🐍 Python per la Sicurezza]]**
    *   Impara a scrivere piccoli script di automazione per non fare tutto a mano.
*   **[[00 — Mappa Blue Team|🛡️ Blue Team (Difesa)]]**
    *   Come leggere i log e capire se un sistema è sotto attacco.

---

## 🧭 3. LE AREE AVANZATE E DI SPECIALIZZAZIONE (Mappa completa)

> ⚠️ **Prima i Fondamentali!** Le aree qui sotto sono avanzate: affrontale solo dopo aver consolidato i 5 pilastri della Sezione 1. Non è un percorso lineare — scegli il *track* più vicino ai tuoi obiettivi (Red Team, Blue Team, Cloud, GRC...) e non aver paura di saltare tra i binari.

### 🧮 Fondamenti CS (prerequisiti trasversali)

*I mattoni informatici che stanno sotto ogni specializzazione.*

*   **[[00 — Mappa Sistemi Operativi|🧩 Sistemi Operativi]]** — come funzionano davvero processi, memoria e kernel sotto il cofano.
*   **[[00 — Mappa Algoritmi e Strutture Dati|🧮 Algoritmi e Strutture Dati]]** — logica, complessità e strutture dati per ragionare (e scriptare) meglio.

### ⚔️ Offensive avanzato

*Dal trovare bug al costruire exploit veri e propri.*

*   **[[00 — Mappa AppSec Avanzato|🐞 AppSec Avanzato]]** — vulnerabilità applicative oltre la OWASP Top 10.
*   **[[00 — Mappa Reverse Engineering e Exploit Dev|🔬 Reverse Engineering & Exploit Dev]]** — smontare binari e sviluppare exploit partendo da zero.
*   **[[00 — Mappa API e GraphQL Security|🔌 API e GraphQL Security]]** — attaccare e mettere in sicurezza API REST e GraphQL.

### 🛡️ Difesa & Forensics

*Rilevare, investigare e rispondere agli incidenti.*

*   **[[00 — Mappa DFIR e Detection Engineering|🔎 DFIR e Detection Engineering]]** — digital forensics, incident response e scrittura di regole di detection. *(Prosegue naturalmente dal [[00 — Mappa Blue Team|🛡️ Blue Team]] della Sezione 2.)*

### ☁️ Cloud & DevSecOps

*Sicurezza dove ormai gira tutto: cloud e pipeline.*

*   **[[00 — Mappa Cloud Security|☁️ Cloud Security]]** — mettere in sicurezza AWS, Azure e GCP.
*   **[[00 — Mappa DevSecOps e Supply Chain|♾️ DevSecOps e Supply Chain]]** — integrare la sicurezza nelle pipeline CI/CD e proteggere la catena di fornitura.

### 📡 Specializzazioni

*Percorsi verticali per chi vuole un dominio di nicchia.*

*   **[[00 — Mappa Mobile Security|📱 Mobile Security]]** — sicurezza di app e dispositivi Android/iOS.
*   **[[00 — Mappa Wireless & Radio|📶 Wireless & Radio]]** — Wi-Fi, Bluetooth e segnali radio (SDR).
*   **[[00 — Mappa AI e LLM Security|🤖 AI e LLM Security]]** — attacchi e difese su modelli di machine learning e LLM.
*   **[[00 — Mappa OSINT e Social Engineering|🕵️ OSINT e Social Engineering]]** — raccolta di informazioni da fonti aperte e fattore umano.
*   **[[00 — Mappa Hardware e IoT Security|🔧 Hardware e IoT Security]]** — dispositivi fisici, firmware e Internet of Things.

### 📋 Governance

*La cybersecurity vista da processi, rischio e norme.*

*   **[[00 — Mappa GRC e Compliance|📋 GRC e Compliance]]** — governance, gestione del rischio e conformità (ISO, NIST, GDPR).

### 🚩 Pratica

*Il ponte tra teoria e mani sulla tastiera.*

*   **[[00 — Mappa Laboratori e CTF|🚩 Laboratori e CTF]]** — ambienti di pratica, macchine vulnerabili e Capture The Flag per allenarti sul serio.

---

## 🛠️ 4. I TUOI STRUMENTI PER LO STUDIO

*   **I tuoi Template per nuove note (nella cartella `Template/`):**
    *   Usa `template-teoria-base.md` per riassumere nuovi concetti teorici usando parole semplici ed analogie.
    *   Usa `template-lab-base.md` per registrare i tuoi primi laboratori pratici (es. i livelli di OverTheWire Bandit).
*   **Il tuo piano personalizzato:**
    *   Consulta il [[Piano_cybersecurity|Piano di Studio Fondamentali v3]] per guidare la tua routine di studio quotidiana.

---

## 🕒 Pagine Modificate di Recente (Dataview)

*(Richiede il plugin Dataview attivo su Obsidian per autocompilarsi)*

```dataview
LIST
WHERE tipo = "concetto" OR tipo = "entita"
SORT file.mtime DESC
LIMIT 7
```

## ⚠️ Note da Revisionare (Più vecchie di 1 anno)

```dataview
LIST
WHERE (tipo = "concetto" OR tipo = "entita") AND file.mtime < date(today) - dur(1 year)
SORT file.mtime ASC
```
