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

## 🛠️ 3. I TUOI STRUMENTI PER LO STUDIO

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
