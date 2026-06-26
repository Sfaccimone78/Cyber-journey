---
tipo: entita
tag: [crypto, tool, forensics]
fase: 1
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["CyberChef"]

---

# CyberChef

## Cos'è

**CyberChef** è un'applicazione web open-source sviluppata dal GCHQ (agenzia di intelligence britannica) che permette di eseguire centinaia di operazioni su dati — encoding, decoding, cifratura, hashing, compressione, analisi — attraverso un'interfaccia visuale **drag-and-drop**. Viene chiamata "il coltellino svizzero del cyber": non richiede installazione, funziona nel browser e supporta l'encatenamento di operazioni ("ricette"). Disponibile online su https://gchq.github.io/CyberChef/ o in locale.

## Uso tipico

```bash
# CyberChef ha interfaccia grafica, ma può essere usato anche da CLI
# con cyberchef-server o via Node.js (cyberchef-node)

# Installazione locale (opzionale, richiede Node.js)
npm install cyberchef

# Esempio di utilizzo via cyberchef-node
node -e "
const chef = require('cyberchef');
chef.bake({
  input: 'SGVsbG8gV29ybGQ=',
  recipe: [{ op: 'From Base64', args: ['A-Za-z0-9+/='] }]
}).then(r => console.log(r.value));
"
# Output: Hello World
```

**Operazioni tipiche nell'interfaccia web**:
- `From Base64` / `To Base64` — [[01. Base64|decodifica Base64]]
- `XOR` — applica [[03. XOR]] con una chiave
- `MD5`, `SHA-256` — calcola [[Funzioni di Hash|hash]]
- `AES Encrypt/Decrypt` — cifratura/decifratura AES
- `Magic` — tenta di identificare automaticamente il tipo di encoding e decodificarlo
- `Parse X.509 Certificate` — ispeziona [[Certificati Digitali e CA|certificati]]
- `URL Decode`, `HTML Entity Decode`, `From Hex`, `From Charcode`...

## Quando si usa

- **CTF**: strumento numero uno per decodificare rapidamente dati in formato sconosciuto. L'operazione "Magic" spesso identifica automaticamente codifiche nascoste.
- **Analisi malware e forensics**: decodificare payload offuscati in Base64, hex, o XOR trovati in script malevoli o traffico di rete.
- **Studio della crittografia**: visualizzare in tempo reale come cambiano i dati applicando [[Encoding vs Encryption|encoding o cifratura]] — ottimo per principianti.
- **Sviluppo**: testare rapidamente funzioni di hashing o cifratura senza scrivere codice.

## Note e trucchi

- La funzione **Magic** (la bacchetta magica) analizza l'input e suggerisce automaticamente come decodificarlo — punto di partenza perfetto quando non sai che encoding stai affrontando.
- Le **ricette** possono essere salvate e condivise come URL o file JSON — utile per team e CTF collaborativi.
- **Output immediato**: ogni modifica alla ricetta aggiorna l'output in tempo reale.
- Puoi caricare file binari (immagini, ZIP) oltre al testo.
- Per uso offline: scarica la release da GitHub, è un singolo file HTML che funziona senza server: https://github.com/gchq/CyberChef/releases
- Alternativa CLI potente: [[OpenSSL]] per operazioni crittografiche specifiche.

## Collegamenti

- [[01. Base64]] — operazione tra le più usate in CyberChef
- [[03. XOR]] — operazione XOR con chiave, comune nei CTF
- [[Encoding vs Encryption]] — CyberChef copre entrambe le categorie
- [[Funzioni di Hash]] — CyberChef calcola MD5, SHA-1, SHA-256 e altri
- [[OpenSSL]] — alternativa da riga di comando per operazioni crittografiche

## Fonti

1. GCHQ — CyberChef su GitHub: https://github.com/gchq/CyberChef
2. CyberChef — Istanza web ufficiale: https://gchq.github.io/CyberChef/
3. Wikipedia — CyberChef: https://en.wikipedia.org/wiki/CyberChef
