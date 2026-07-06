# Wiki di LLM — Cybersecurity (schema)

Questo file è lo **schema** della knowledge base. Dice all'agente LLM come è
strutturata la wiki, quali convenzioni seguire e quali workflow usare. Leggilo a ogni sessione
prima di toccare la wiki. Lo evolviamo insieme nel tempo.

> Modello di riferimento: **Wiki di LLM** (memex curato). La wiki è un artefatto **permanente** che
> si interpone tra l'utente e le fonti. La conoscenza si **compila una volta e si mantiene**, non
> si ricostruisce a ogni domanda. L'umano cura fonti e domande; l'LLM fa la contabilità.

---

## I tre strati

1. **`Fonti/`** — fonti grezze, la **verità immutabile**. Articoli, room TryHackMe, writeup, PDF,
   immagini, dati. L'LLM le **legge ma non le modifica mai**.
2. **Wiki** — Markdown generato dall'LLM: `Concetti/`, `Entita/`, `Sintesi/`, più gli appunti
   esistenti nella radice (vedi *Appunti dichiarati*). L'LLM gestisce interamente questo strato.
3. **Schema** — questo `WIKI_SCHEMA.md`. Configurazione che rende l'LLM un wiki-manager disciplinato.

---

## Regole d'oro

1. **Non modificare mai** i file in `Fonti/`. Solo lettura.
2. Ogni **ingestione** aggiorna SEMPRE `index.md` **e** `log.md`.
3. Ogni entità/concetto citato in una pagina va linkato con `[[wikilink]]`.
4. Una pagina = un'unità di conoscenza, in una **cartella d'area** con nome `NN <Titolo canonico>.md`
   (es. `06 Metodologia e Tool/09 Nmap.md`) e `aliases: ["<Titolo senza numero>"]` nel frontmatter.
5. Quando una nuova fonte **contraddice** una pagina esistente: NON sovrascrivere in silenzio.
   Segnala la contraddizione con un callout `> [!warning] Contraddizione` e cita entrambe le fonti.
6. Lingua: **italiano**.

---

## Struttura cartelle

La wiki è organizzata **per area** (non più per tipo). Ogni area è una cartella numerata; dentro,
le note hanno un **prefisso numerico** che dà l'ordine d'apprendimento. Concetti ed entità
**convivono** nella stessa cartella d'area — la distinzione resta nel frontmatter `tipo:`, non nelle
cartelle. Così studiare un tema = aprire una cartella e seguire i numeri.

```
Cyber-Journey/
├── WIKI_SCHEMA.md                # questo schema
├── index.md                 # catalogo + mappe per area + viste Dataview
├── log.md                   # registro cronologico
├── 00 Fondamenti/           # ogni area: una MOC "00 — Mappa <Area>.md" + note "NN <Titolo>.md"
├── 01 Reti/
├── 02 Linux/
├── 03 Crittografia/
├── 04 Windows e AD/
├── 05 Web OWASP/
├── 06 Metodologia e Tool/
├── 07 Blue Team/
├── 08 Sistemi Operativi/    # fondamenti CS: processi, scheduling, memoria, FS, I/O, virtualizz.
├── 09 Python/
├── 10 Algoritmi e Strutture Dati/  # fondamenti CS: strutture dati, grafi, sorting, DP, greedy
├── Fonti/                   # fonti grezze immutabili (+ assets/ per immagini)
├── Risorse/                 # indice risorse esterne (PDF, siti, piattaforme)
├── Sintesi/                 # overview generale, tabelle comparative, tesi in evoluzione
└── Template/                # template per nuove pagine + pagine esempio
```

> **Nota fusione (2026-06-26):** la vecchia wiki di ricerca `wiki/` (schema separato,
> topic-based) è stata **assorbita** in questa struttura area-based. Da lì arrivano le 2 aree
> trasversali **08 Sistemi Operativi** e **10 Algoritmi e Strutture Dati** più vari concetti
> teorici rifusi nelle aree esistenti. `wiki/` e il suo schema separato non esistono più: schema unico = questo file.

### Regole di posizionamento e naming
- **Nome file** = `NN <Nome canonico>.md` (es. `01 Modello OSI.md`). `NN` = posizione nell'ordine
  d'apprendimento dell'area. Inserire una pagina in mezzo → rinumerare le successive.
- **Alias obbligatorio**: nel frontmatter metti `aliases: ["<Nome senza numero>"]`. Così i wikilink
  scritti come `[[Modello OSI]]` (senza numero) risolvono sempre, anche se cambi la numerazione.
  **Linka sempre col nome senza numero** — più stabile.
- **Mappa d'area** (`00 — Mappa <Area>.md`, `tipo: sintesi`, tag `moc`): elenco ordinato delle note
  + navigazione ← prec / succ →. Aggiornala quando aggiungi/rinumeri pagine nell'area.
- Nuova pagina → scegli l'area giusta, dai il numero, aggiungi l'alias, aggiorna la Mappa d'area,
  `index.md` e `log.md`.

### Cosa va dove
- **Concetto** (`tipo: concetto`) = un'idea/tecnica/vulnerabilità (es. `SQL Injection`, `Subnetting`, `Kerberos`).
- **Entità** (`tipo: entita`) = una cosa nominabile e concreta (tool `Nmap`, piattaforma `TryHackMe`, protocollo
  `SMB`, `CVE-2021-41773`).
- **Sintesi** = output di valore che non deve sparire: confronti, mappe (MOC), la tesi corrente.
- **Fonte** = il materiale grezzo. Se la fonte è esterna (URL), crea una pagina riepilogo in
  `Fonti/` che la riassume e linka l'originale.

---

## Convenzioni di pagina

### Frontmatter standard (per Dataview)
```yaml
---
tipo: concetto      # concetto | entita | fonte | sintesi
tag: [web, owasp]   # da: reti, linux, windows, crypto, web, owasp, ad, tool, blue-team
fase: 2             # fase del piano: 1-4 (0 = trasversale)
fonti: 0            # numero di fonti che alimentano la pagina
aggiornato: 2026-06-20
stato: stub         # stub | attivo | maturo
aliases: ["Nome senza numero"]   # = titolo canonico senza prefisso NN; rende i wikilink stabili
---
```

### Wikilink e cross-reference
- Linka ogni concetto/entità citato: `... sfruttiamo [[SQL Injection]] tramite [[Burp Suite]] ...`.
- In fondo a ogni pagina, sezione `## Collegamenti` con i link correlati e le `## Fonti` citate.
- I link a fonti usano il nome pagina fonte: `[[Fonte - Titolo articolo]]`.

### Tag dominio (tronco comune del piano)
`reti` · `linux` · `windows` · `crypto` · `web` / `owasp` · `ad` (Active Directory) ·
`tool` · `blue-team` · `metodologia`

### Standard Nota Esperto (requisito per `stato: maturo`)
Lo scopo della wiki è uniforme **profondità da esperto**, non solo ampiezza. Una nota può essere
`stato: maturo` **solo se** contiene tutte queste sezioni (nell'ordine). Sotto questa soglia →
`stato: attivo`. Nota-modello di riferimento: **`05 Web OWASP/02 SQL Injection.md`**. Template da
usare per le nuove: **`Template/template-concetto-pentest.md`**.

1. **In breve** — 2-3 frasi: cos'è, categoria, impatto, dove si colloca.
2. **Come funziona / Meccanismo** — il processo + il "perché" a basso livello (pacchetti, memoria,
   parsing, flusso auth).
3. **Esempi / Walkthrough** — comandi e flag **reali**, copia-incollabili; non un solo esempio.
4. **Mitigazione e difesa** — in ordine di efficacia.
5. **`## Lab`** — almeno un lab concreto agganciato ([[PortSwigger Web Academy]], [[TryHackMe]],
   [[HackTheBox]], CTF, pwn.college…). Nessuna tecnica senza pratica.
6. **`## Domande`** — 3-5 Q&A secche (auto-test / ripasso / colloquio).
7. **Approfondimento livello esperto** — la parte che alza la nota: evasion/OPSEC, casi limite,
   detection engineering (Event ID, Sigma, SPL/KQL, MITRE ATT&CK), troubleshooting.
8. **`## Collegamenti`** — wikilink correlati.
9. **`## Fonti`** — **≥2 fonti reali e verificabili** (PortSwigger, HackTricks, MITRE, RFC, paper,
   vendor docs). `fonti:` nel frontmatter = conteggio reale.

> Quando aggiorni una nota allo standard: aggiorna `fonti:`, `aggiornato:`, `stato:` e la MOC d'area.

---

## Appunti dichiarati (esistenti, già nella wiki)

Questi file esistono già e **contano come concept page**. Non spostarli, non riscriverli senza
motivo. Alla prima ingestione che li tocca, aggiungi frontmatter e cross-link:
- Radice: `01. Base64.md`, `02. Bytes-Long.md`, `03. XOR.md`,
  `CryptoHack - Mathematics (Modular Math).md` → tag `crypto`, fase 1.
- `Crittografia/` → tag `crypto`.
- `Network/` (`1. Rete Informatica...`, `2. Hardware di Rete.md`) → tag `reti`, fase 1.

---

## Workflow

### 1. Ingest (acquisire una fonte)
Trigger utente: *"ingerisci questa fonte"* dopo aver messo un file in `Fonti/`.
1. **Leggi** la fonte in `Fonti/`.
2. **Discuti** con l'utente i punti chiave (cosa enfatizzare).
3. Scrivi/aggiorna la **pagina fonte** in `Fonti/` se serve un riepilogo (per fonti esterne/URL).
   *(I file grezzi originali restano intoccati.)*
4. **Crea/aggiorna** le pagine `Concetti/` ed `Entita/` interessate. Una fonte può toccare 10-15
   pagine. Incrementa `fonti:` e aggiorna `aggiornato:`.
5. **Cross-linka** tutto. Segnala contraddizioni (regola d'oro 5).
6. **Aggiorna `index.md`** (aggiungi/aggiorna le righe delle pagine toccate).
7. **Appendi a `log.md`** una voce ingest.

Default: una fonte alla volta, con l'utente coinvolto. Più fonti insieme = meno supervisione.

### 2. Query (interrogare la wiki)
1. Leggi `index.md` per trovare le pagine pertinenti.
2. Apri e leggi quelle pagine.
3. Sintetizza la risposta con **citazioni** `[[fonte]]`.
4. Se la risposta ha valore duraturo (un confronto, un'analisi, una connessione scoperta),
   **offri di salvarla** come pagina in `Sintesi/`. Poi aggiorna `index.md` + `log.md`.

Formati di risposta possibili: pagina Markdown, tabella comparativa, presentazione (Marp),
grafico (matplotlib), immagine. Scegli in base alla domanda.

### 3. Lint (controllo di integrità — periodico)
Trigger utente: *"fai il lint della wiki"*. Cerca e riporta:
- **Contraddizioni** tra pagine.
- Affermazioni **obsolete** superate da fonti più recenti.
- Pagine **orfane** (nessun backlink in entrata).
- Concetti importanti **citati ma senza pagina** dedicata.
- **Cross-link mancanti**.
- **Lacune** colmabili con ricerca web.
Suggerisci nuove domande da approfondire e nuove fonti. Logga l'evento come `lint`.

**Gate automatico (Definition of Done):** `tools/check_notes.py` verifica che ogni nota
`stato: maturo` (tipo `concetto`/`entita`) non sia un'isola: ≥1 `[[wikilink]]`, sezione
`## Collegamenti`, `## Fonti` con ≥2 voci, e presenza nella Mappa d'area. Gira come **hook
pre-commit** (`tools/githooks/pre-commit`) sui file in stage. Installazione una-tantum per clone:
`git config core.hooksPath tools/githooks`. Report completo del vault: `python tools/check_notes.py`
(`--strict` tratta anche gli avvisi come errori). Se una nota non è ancora pronta → `stato: attivo`.
I heading `## Collegamenti` e `## Fonti` sono riconosciuti anche con decorazione emoji
(es. `## 🔗 Collegamenti`, `## 📚 Fonti`); evita invece refusi con spazio dentro la parola
(`## Collegamen ti` non è un heading valido).

---

## index.md e log.md

- **`index.md`** è orientato ai *contenuti*: catalogo di ogni pagina con link, breve riassunto e
  metadati, organizzato per categoria. Aggiornalo a ogni ingestione. Leggilo per primo in query.
  Contiene anche blocchi Dataview che si auto-popolano dal frontmatter.
  - **La sezione "Contenuto per area" è generata**: la regione tra i marker
    `<!-- AUTO-INDEX:START -->` e `<!-- AUTO-INDEX:END -->` è prodotta da **`tools/gen_index.py`**
    (scansiona le cartelle d'area, elenca le note reali via alias). Non modificarla a mano.
    Dopo aver aggiunto/rinominato/spostato note: esegui `python tools/gen_index.py` (verifica la deriva,
    esce ≠0 se ce n'è) e `python tools/gen_index.py --write` (rigenera regione + conteggio in testa).
- **`log.md`** è orientato agli *eventi*: cronologia append-only. Ogni voce inizia con prefisso
  coerente per essere grep-abile:
  ```
  ## [YYYY-MM-DD] <tipo> | <titolo>
  ```
  Tipi: `ingest` · `query` · `lint` · `init`.
  `grep "^## \[" log.md | tail -5` → ultime 5 voci.

---

## Gestione immagini (opzionale)

Le immagini scaricate vanno in `Fonti/assets/`. Gli LLM non leggono nativamente il Markdown con
immagini incorporate in un'unica passata: **leggi prima il testo**, poi visualizza separatamente
le immagini rilevanti da `Fonti/assets/` per contesto aggiuntivo.

---

## Tooling futuro (non ora)

A ~100 fonti, `index.md` + la ricerca globale di Obsidian bastano. Se la wiki cresce molto,
valuta **qmd** (ricerca locale ibrida BM25/vettoriale su Markdown, CLI + server MCP) o un piccolo
script di ricerca custom. Aggiorna questo schema quando lo introduci.

---

## Plugin Obsidian disponibili
`dataview` (query frontmatter) · `templater` (template in `Template/`) · `excalidraw` (diagrammi) ·
`editing-toolbar`. Graph view = miglior modo per vedere hub, orfani e struttura.

---

## Vocabolario canonico e validazione

Riferimento per il gate `tools/check_notes.py`. Serve a tenere il frontmatter e gli heading
allineati allo schema, così Dataview e le mappe d'area restano affidabili.

### Valori ammessi nel frontmatter
- **`tipo:`** → uno tra **`concetto`** · **`entita`** · **`fonte`** · **`sintesi`**.
- **`stato:`** → uno tra **`stub`** · **`attivo`** · **`maturo`**.

Ogni nota non-MOC / non-template con frontmatter è validata: un valore fuori da questi insiemi è un
**ERRORE** (`TIPO-OFFSCHEMA` / `STATO-OFFSCHEMA`), a prescindere dallo `stato`. Il controllo scatta
di default, non solo sulle note `maturo` (evita stati/tipi improvvisati tipo `lab`/`completato`).

### Heading canonici e alias accettati
Nel verificare le sezioni minime, il gate riconosce come equivalenti:

| Heading canonico | Alias accettato |
|------------------|-----------------|
| `## In breve`    | `## Panoramica` |
| `## Lab`         | `## Esercizi`   |
| `## Domande`     | — (nessun alias) |

Usare la variante alias **non** fa scattare l'avviso di "sezione assente".

### Flag `--dod` (Definition of Done stretta, opt-in)
`python tools/check_notes.py --dod` promuove ad **ERRORE** ciò che di default resta AVVISO su una
nota `maturo`: sezioni `## In breve` / `## Lab` / `## Domande` mancanti e mismatch tra `fonti:` nel
frontmatter e il conteggio reale delle voci in `## Fonti`. **Senza** `--dod` il comportamento è
invariato (restano avvisi non bloccanti), così l'hook pre-commit resta verde durante l'arricchimento
in corso. Usa `--dod` per audit periodici della qualità, non nel gate di commit.
