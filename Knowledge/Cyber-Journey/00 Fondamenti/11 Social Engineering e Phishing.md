---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["Social Engineering e Phishing", "Social Engineering"]
---
# Social Engineering e Phishing

## In breve
Il **Social Engineering** è la manipolazione psicologica delle persone per indurle a compiere azioni o
rivelare informazioni. È il vettore che **aggira la tecnologia colpendo l'umano** — inutile cifrare il
disco se l'utente *consegna* la password a chi gliela chiede con il pretesto giusto. Per questo è
spesso il **primo anello** della [[La Cyber Kill Chain|Kill Chain]] (fase Delivery) e la parte umana
della [[Superficie di Attacco]].

Il **Phishing** ne è la forma più diffusa: messaggi ingannevoli che spingono a cliccare link, aprire
allegati o inserire credenziali su pagine fasulle.

## Perché funziona: le leve di Cialdini
L'attacco sfrutta scorciatoie cognitive (euristiche) che normalmente ci fanno risparmiare tempo:
- **Autorità** — finge di essere il capo, l'IT, la banca, l'Agenzia delle Entrate.
- **Urgenza / Paura** — "il tuo account sarà bloccato tra 24h": il panico spegne il pensiero critico.
- **Fiducia / Familiarità** — spoofing di mittenti noti, loghi corretti, tono interno.
- **Curiosità / Avidità** — "hai vinto", "fattura in allegato", "foto tue".
- **Riprova sociale / Reciprocità** — "tutti i colleghi l'hanno già fatto", piccolo favore prima della
  richiesta.

Il bersaglio di solito è **studiato prima** con [[OSINT]] (ruolo, colleghi, eventi recenti) per rendere
il pretesto credibile — è la fase Reconnaissance applicata alle persone.

> [!note] System 1 vs System 2 (Kahneman)
> Le leve di Cialdini funzionano perché colpiscono il **System 1** — il pensiero rapido, automatico e
> intuitivo — prima che il **System 2** — lento, analitico e critico — possa intervenire. Urgenza e
> paura servono proprio a impedire l'attivazione del System 2. Far "rallentare e verificare" la vittima
> è la contromisura cognitiva di base.

## Varianti comuni
|        Tecnica         |             Descrizione              |
| :--------------------: | :----------------------------------: |
|      **Phishing**      |      Email di massa ingannevoli      |
|   **Spear phishing**   |    Mirato a una persona specifica    |
|      **Whaling**       |          Mirato a dirigenti          |
| **Smishing / Vishing** |          via SMS / telefono          |
|     **Pretexting**     | Scenario inventato per ottenere dati |
|      **Baiting**       | USB "smarrita" lasciata di proposito |
| **Tailgating / piggybacking** | seguire fisicamente una persona autorizzata oltre una porta a badge |
|  **BEC** (Business Email Compromise) | dirottamento di pagamenti via email aziendale compromessa |
| **MFA fatiga / prompt bombing** | raffica di push per far approvare l'MFA per sfinimento |

## Anatomia di un'email di phishing — gli indizi
Apparente mittente Microsoft 365 che invita a "verificare l'account". Segnali di allarme:
- **Dominio look-alike** — `micros0ft-login.com`, sottodomini lunghi, TLD strani.
- **Discrepanza link↔testo** — il testo dice un URL, l'`href` ne punta un altro (passa il mouse sopra).
- **Urgenza + minaccia** di conseguenze.
- **Errori** o tono leggermente "off", richiesta inusuale di credenziali.
- **Allegato** inatteso (`.html`, `.iso`, `.zip` con dentro `.lnk`/macro).

## Phishing che batte l'MFA (lo stato dell'arte)
La sola password non basta più, ma nemmeno l'MFA è invincibile:
- **Reverse proxy / AiTM** (es. Evilginx) — l'attaccante si interpone, ruba **il cookie di sessione**
  dopo che la vittima ha superato l'MFA → bypassa il secondo fattore.
- **MFA fatiga** — spam di richieste push finché la vittima approva per errore/stanchezza.
- Difesa robusta: **MFA phishing-resistant** (FIDO2/passkey, legate al dominio → non replicabili).

Strumenti di simulazione **autorizzata** (red team): **GoPhish** (campagne), **SET** (Social-Engineer
Toolkit), **Evilginx** (reverse proxy che ruba anche il token MFA).

## Caso reale — Twitter, luglio 2020
Gli attaccanti usarono **vishing** (telefonate) verso dipendenti Twitter per ottenere accesso a
strumenti interni e dirottare account verificati (Obama, Musk, Gates...) in una truffa Bitcoin.
Dimostra che la social engineering **bypassa controlli tecnici robusti colpendo le persone**: non
serviva alcun exploit software, solo manipolazione umana.

## Mitigazione — tecnica + umana (difesa a strati)
- **Formazione e simulazioni** periodiche (la consapevolezza è il controllo principale qui).
- **MFA phishing-resistant** ([[IAM e Zero Trust]]) per svalutare le credenziali rubate.
- **DMARC / DKIM / SPF** contro lo spoofing del mittente, filtri anti-spam, sandboxing allegati.
- **Procedure fuori banda** per richieste sensibili (doppio canale per i bonifici → blocca il BEC).
- **Cultura del "segnala senza colpa"**: un utente che segnala in fretta vale più di uno che nasconde
  l'errore per paura. Aggancio a [[Incident Response]].

## Lab
- **[[TryHackMe]]** → modulo *Phishing* del percorso *SOC Level 1* (room *Phishing Analysis Fundamentals*, *Phishing Emails 1-5*, *Phishing Analysis Tools*): analizza header, URL look-alike e allegati di email reali di esempio.
- **[[TryHackMe]]** → room *Intro to Cyber Threat Intelligence* / *OSINT*: pratica la fase di ricognizione sulle persone che precede lo spear phishing.
- **GoPhish in lab autorizzato**: monta una campagna di phishing simulata in una VM isolata (mai su terzi senza permesso) per capire tracking, landing page e metriche di click.

## Domande
1. **D:** Perché il social engineering è considerato il "primo anello" della Kill Chain? **R:** Perché aggira la tecnologia colpendo l'umano ed è tipicamente il vettore della fase Delivery: inutile cifrare il disco se l'utente consegna la password.
2. **D:** Quali leve psicologiche (Cialdini) sfrutta il phishing? **R:** Autorità, urgenza/paura, fiducia/familiarità, curiosità/avidità, riprova sociale/reciprocità.
3. **D:** Perché urgenza e paura sono così efficaci (System 1 vs System 2)? **R:** Colpiscono il System 1 (pensiero rapido e automatico) prima che il System 2 (lento e critico) possa intervenire; far "rallentare e verificare" è la contromisura cognitiva.
4. **D:** Come fa un attacco AiTM (es. Evilginx) a battere l'MFA? **R:** Con un reverse proxy si interpone e ruba il *cookie di sessione* dopo che la vittima ha superato l'MFA, bypassando il secondo fattore.
5. **D:** Qual è la difesa più robusta contro il phishing delle credenziali/MFA e perché? **R:** L'MFA phishing-resistant (FIDO2/passkey), perché è legata al dominio e non è replicabile su una pagina fasulla.

## Collegamenti
- [[La Cyber Kill Chain]] · [[Superficie di Attacco]] · [[OSINT]] · [[IAM e Zero Trust]] · [[Incident Response]]

## Fonti
- Robert Cialdini, *Influence* (principi di persuasione).
- Daniel Kahneman, *Thinking, Fast and Slow* (System 1 / System 2).
- Anderson, *Security Engineering*, cap. 3 (Psychology and Usability) — https://www.cl.cam.ac.uk/~rja14/book.html
- Verizon DBIR — peso del fattore umano nei breach · MITRE ATT&CK — Phishing (T1566).
