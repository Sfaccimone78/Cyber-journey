---
tipo: entita
tag: [crypto, tool, forensics]
fase: 1
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["CyberChef"]

---

# CyberChef

## In breve

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

## Lab

- **Pratica libera su https://gchq.github.io/CyberChef/**: incolla una stringa Base64 e costruisci una ricetta `From Base64`; poi concatena più livelli (es. `From Base64` → `From Hex` → `XOR`) su un payload multi-encoded per allenare l'occhio a riconoscere le codifiche annidate.
- **Usa la bacchetta *Magic*** su un input di formato ignoto: fai indovinare a CyberChef l'encoding e verifica il risultato. Esercizio ideale per i task di decoding di PicoCTF e dei CTF *forensics*.
- **CTF *forensics* / malware analysis**: prendi uno script offuscato (Base64 + XOR + gzip) e ricostruisci il payload originale con una singola ricetta, salvandola come URL condivisibile. Collega il flusso a [[Encoding vs Encryption]] e [[XOR]].

## Domande

1. **D:** Chi ha sviluppato CyberChef e come si usa? **R:** Il GCHQ (intelligence britannica); si usa nel browser tramite un'interfaccia drag-and-drop che concatena operazioni in "ricette".
2. **D:** A cosa serve l'operazione *Magic*? **R:** Analizza l'input e suggerisce automaticamente come decodificarlo, utile quando non si conosce il formato di partenza.
3. **D:** Perché CyberChef è prezioso in analisi malware/forensics? **R:** Permette di decodificare rapidamente payload offuscati in Base64, hex, XOR e simili, concatenando più passaggi senza scrivere codice.
4. **D:** Le ricette di CyberChef si possono condividere? **R:** Sì, come URL o file JSON, comode per team e CTF collaborativi.
5. **D:** CyberChef richiede una connessione o un server? **R:** No: può girare offline come singolo file HTML scaricabile da GitHub.

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
