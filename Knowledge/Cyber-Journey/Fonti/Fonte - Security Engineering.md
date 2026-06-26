---
tipo: fonte
tag: [metodologia, blue-team, crypto]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
url: https://www.cl.cam.ac.uk/~rja14/book.html
autore: Ross Anderson
aliases: ["Security Engineering", "Security Engineering (Ross Anderson)"]
---

# Fonte - Security Engineering — Ross Anderson (3a ed., capitoli gratuiti)

Sintesi dei capitoli letti: **1** (What is Security Engineering), **2** (Who is the Opponent), **3** (Psychology and Usability), **4** (Protocols), **5** (Cryptography), **21** (Network Attack and Defence).

> Nota: nella 3a edizione la psicologia è il **cap. 3** (non 2). Il cap. 2 è "Who is the Opponent" (modello di minaccia / attori). Adattato di conseguenza.

## Cap. 1 — Che cos'è la Security Engineering

Disciplina di costruire sistemi che restino **affidabili in presenza di malizia, errori e guasti ambientali**. Anderson la struttura su quattro pilastri:

- **Policy** — cosa significa "sicuro" per quel sistema (es. "solo utenti autorizzati leggono i dati").
- **Mechanism** — i mezzi tecnici che applicano la policy (cifratura, autenticazione, controllo accessi).
- **Assurance** — la fiducia che i meccanismi funzionino davvero (test, audit, metodi formali).
- **Incentives** — allineamento del comportamento umano agli obiettivi: chi ha l'incentivo a difendere/attaccare?

Distinzione chiave **safety vs security**: la safety assume guasti casuali; la security assume un **avversario intelligente** che sceglie attivamente il punto più debole. → vedi [[Threat Modeling]].
Tesi centrale: i sistemi falliscono per **disallineamento tra policy, meccanismo e incentivi**; l'anello debole è spesso umano/organizzativo, non tecnico. [Fonte: Anderson, cap. 1]

## Cap. 2 — Chi è l'avversario (threat model)

Senza un **modello di minaccia** chiaro (chi attacca, con quali risorse, quali asset, quali attacchi sono realistici) le misure diventano arbitrarie. Spettro di attori: criminalità organizzata, stati-nazione, insider, hacktivisti, script kiddie. Ogni attore ha capacità e motivazioni diverse → il modello determina cosa difendere. → [[Threat Modeling]]

## Cap. 3 — Psicologia e usabilità

La sicurezza fallisce sull'**essere umano** prima che sul codice.

- **Kahneman, System 1 vs System 2**: System 1 (veloce, intuitivo) gestisce le decisioni di routine — è ciò che il phishing sfrutta; System 2 (lento, analitico) è raramente attivato per "cliccare un link".
- **Bias sfruttati**: autorità (finto IT/CEO), urgenza, scarsità, riprova sociale, conferma. → [[Social Engineering]]
- **Perché si clicca**: sovraccarico cognitivo + *alert fatigue*, fiducia in cue di superficie (logo, dominio simile), pressione temporale.
- **Compliance budget**: gli utenti hanno una tolleranza limitata alle richieste di sicurezza; oltre la soglia trovano scorciatoie. Le password "forti" imposte vengono riusate o scritte su post-it.
- **Lezioni di design**: rendere l'azione sicura *quella di default*, ridurre il carico cognitivo, evitare l'abitudine agli avvisi, formare con phishing simulato. [Fonte: Anderson, cap. 3]

## Cap. 4 — Protocolli di sicurezza

> "If it's provably secure, it probably isn't." — Lars Knudsen, in epigrafe al capitolo.

I protocolli sono dove **crittografia e controllo accessi si incontrano**; specificano i passi con cui i principal stabiliscono fiducia. Valutarli richiede due domande: il modello di minaccia è realistico? Il protocollo lo affronta?

- **Notazione**: `T → G : T, {T, N}K` — T invia a G il nome T e il valore {T, N} cifrato con K.
- **Nonce e freshness**: un *nonce* (number used once: random, contatore o timestamp) garantisce che il messaggio sia fresco, non un **replay**. Esempio reale di fallimento: un contatore prepagato sudafricano accettava qualsiasi nonce diverso dall'ultimo → la serie `ABABAB...` ricaricava all'infinito.
- **Challenge-response**: l'immobilizzatore auto cifra una sfida casuale `N` con chiave condivisa. Tra 2005-2015 *tutti* i principali sistemi (DST 40-bit, Keeloq, Hitag2, Megamos) sono caduti per chiavi corte (export control USA), cifrari deboli, master key globali (BORA — break-once-run-anywhere) e bug di key diversification (XOR).
- **Man-in-the-middle**: la storia "MIG-in-the-middle" (IFF rilanciato in tempo reale). Versione moderna: il sito di phishing apre in parallelo una sessione con la banca, rilancia la sfida al token dell'utente e la risposta alla banca. → [[Attacchi di Rete]]
- **Reflection attack**: A rimanda la sfida di B verso B stesso (o il suo wingman) per ottenere una risposta valida. Difesa: includere i nomi dei due parti nello scambio (`{B, N}K`) e non accettare il rimbalzo della propria sfida.
- **Chosen-protocol / Mafia-in-the-middle**: riusare la stessa chiave in due applicazioni è pericoloso (es. "prova età" sul sito porno che rilancia una transazione bancaria da firmare). [Fonte: Anderson, cap. 4]

## Cap. 5 — Crittografia

> "Cryptography is where security engineering meets mathematics ... surprisingly hard to do right."

- **Storia → intuizione**: Caesar (chiave fissa), Vigenère (stream cipher a chiave ripetuta, rotto da Kasiski via pattern), Playfair (block cipher a digrammi). One-time pad = **segretezza perfetta** (Shannon: tante chiavi quanti plaintext) ma **nessuna integrità**.
- **Confusione e diffusione**: in un buon block cipher cambiare 1 bit di input deve cambiare ~metà dei bit di output (diffusione).
- **Modelli di sicurezza**: perfect secrecy → concrete security (t,ε)-secure → standard model (indistinguibilità/semantic security) → **random oracle model** (l'"elfo con i dadi e la pergamena").
- **Primitive come oracoli casuali**:
  - *Random function* = **hash**: one-wayness; resistenza a preimage (~2^(n-1) tentativi) e a **collisione** (~2^(n/2) per il **teorema del compleanno** → servono ≥256 bit, SHA-2/SHA-3; MD5 e SHA-1 rotti).
  - *Random generator* = **stream cipher**: input corto → keystream lungo; mai riusare il keystream (two-time pad → Venona); usare seed/IV.
  - *Random permutation* = **block cipher** (DES 64-bit, AES 128-bit), `C = {M}K`. Attacchi: known/chosen plaintext, chosen ciphertext, related-key; obiettivo forgery o key-recovery. Attacchi "certificazionali" vs sfruttabili.
- **ECB è insicuro**: stesso blocco → stesso ciphertext (cut-and-paste di transazioni); le API (es. CAPI) spingono ECB come default → serve un *mode* (CBC/CTR) che leghi i blocchi.
- **MAC / universal hash**: `A = k1*M + k2 mod p` autentica con sicurezza ideale se la chiave è unica per messaggio.
- **Asimmetrica**: trapdoor one-way permutation; cifratura a chiave pubblica (analogia: cassetta postale), **firma digitale** (sign con chiave privata, verify con pubblica; firmare l'**hash** del messaggio — donde la necessità di hash collision-free, vedi truffa "Rubber Fetish vol.7 → mutuo $75k"). [Fonte: Anderson, cap. 5]

→ Vedi [[Cryptographic Failures]], [[Funzioni Hash]], [[TLS/SSL]], [[Padding Oracle]].

## Cap. 21 — Attacco e difesa di rete

- **Perimetro vs zero-trust**: dal modello "intranet fidata dietro firewall" verso il **deperimetrismo** (Google BeyondCorp: controlli sui singoli utenti/dispositivi, non sulla rete; NIST zero-trust). Caso opposto: ICS/SCADA (Modbus/DNP3 senza crittografia) → **ri-perimetrizzazione** sull'unica connessione esterna.
- **DoS/DDoS**: SYN flood (fix: SYN cookie), **SYN reflection** e **amplification** (smurf/ICMP, NTP, DNS, DNSSEC come amplificatore). Botnet IoT — **Mirai** (CCTV con password di default) dal 2016.
- **Routing/Naming**: hijack **BGP** (Pakistan→YouTube 2008; China Telecom 100k rotte 2010), mitigazione RPKI. **DNS**: pharming, drive-by pharming; difesa **DNSSEC** (firme sui record), tensione con DoH.
- **Email**: SMTP non autenticato → SPF, DKIM, DMARC, ARC; MTA-STS contro downgrade.
- **Malware (tassonomia di Anderson)**: *Trojan* (malizioso quando eseguito), *worm* (si replica in rete), *virus* (si aggancia ad altro codice), *RAT*, *rootkit* (root + stealth), PUS. Storia: Morris worm 1988, "Love Bug" 2000, flash worm (Code Red, Slammer), WannaCry/NotPetya (EternalBlue su SMB). Struttura: dropper + payload; polimorfismo per eludere gli scanner. → [[Malware]]
- **Difese**: firewall (packet filter / circuit gateway / application proxy), IDS/IPS, VPN/IPsec, threat intelligence, SOAR, DLP. L'antivirus da solo è sempre meno efficace ("live off the land"). [Fonte: Anderson, cap. 21]

→ Vedi [[Attacchi di Rete]], [[TCP]], [[DNS]].

## Collegamenti
- [[index]]
- Vedi anche: [[Triade CIA]], [[Threat Modeling]], [[Cryptographic Failures]], [[Malware]], [[Attacchi di Rete]], [[OWASP Top 10]], [[Matrice Attacco-Difesa]]

## Fonti
- [Anderson, *Security Engineering* 3rd ed., capp. 1-5, 21 — <https://www.cl.cam.ac.uk/~rja14/book.html>]
