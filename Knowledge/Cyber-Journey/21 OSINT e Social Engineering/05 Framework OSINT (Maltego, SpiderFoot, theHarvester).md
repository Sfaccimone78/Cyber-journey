---
tipo: concetto
tag: [osint, recon, tool]
fase: 3
fonti: 4
aggiornato: 2026-07-02
stato: maturo
aliases: ["Framework OSINT", "Maltego", "SpiderFoot", "theHarvester", "OSINT Tooling"]
---

# Framework OSINT (Maltego, SpiderFoot, theHarvester)

## In breve
I **framework OSINT** automatizzano e correlano la raccolta di informazioni da molte fonti in un unico flusso, trasformando query manuali sparse in un grafo di relazioni. Tre strumenti coprono lo spettro: **theHarvester** (rapido, da riga di comando, per email/sottodomini/host), **SpiderFoot** (scanner automatizzato con centinaia di moduli e correlazioni), **Maltego** (analisi visuale a grafo con *transform* che espandono le entità). Impatto: riducono ore di ricerca a minuti e rendono evidenti collegamenti che sfuggirebbero a occhio.

## Come funziona
Il modello comune è **entità → trasformazione → nuove entità**: si parte da un seed (dominio, email, nome), uno strumento interroga fonti (DNS, CT, motori, breach, social) e restituisce nuovi dati collegati, che a loro volta diventano nuovi seed (pivoting automatizzato).

**theHarvester** — ricognizione da CLI, orientata a email, nomi, sottodomini, host e IP di un dominio. Interroga motori di ricerca e sorgenti passive (alcune richiedono API key). È il primo colpo veloce nella fase di *information gathering* (vedi [[04 OSINT su Domini e Infrastruttura]]).

**SpiderFoot** — automazione end-to-end. Ha oltre 200 moduli che partono da un target (dominio, IP, email, nome, telefono) e raccolgono/correlano automaticamente. Si usa da web UI o CLI, salva in database e produce grafi e report. Ideale per la copertura ampia; va poi validato a mano.

**Maltego** — piattaforma di *link analysis* visuale. L'analista trascina entità sul grafo ed esegue **transform** (interrogazioni a servizi tramite hub/API) che generano entità collegate. Eccelle nel mostrare **relazioni** (persona ↔ email ↔ dominio ↔ IP). Richiede la comprensione di transform e, per molte fonti, chiavi/abbonamenti. La community edition è limitata nel numero di risultati.

**Quando usare cosa**:
| Strumento | Interfaccia | Forza | Limite |
|-----------|-------------|-------|--------|
| **theHarvester** | CLI | veloce, mirato su dominio/email | copertura ristretta, dipende dalle fonti |
| **SpiderFoot** | Web/CLI | copertura ampia e automatica | molto rumore, da filtrare |
| **Maltego** | GUI a grafo | visualizza relazioni, pivoting guidato | curva di apprendimento, costi delle transform |

Nessuno sostituisce il ragionamento: gli strumenti raccolgono, l'analista **valida e correla**. L'OPSEC resta obbligatoria (usa questi tool dietro l'ambiente isolato di [[Sicurezza Operativa per le Indagini OSINT]]).

## Esempi
theHarvester su un dominio (fonti passive):
```bash
theHarvester -d example.com -b crtsh,bing,duckduckgo -l 500 -f report
# -b sorgenti, -l limite risultati, -f salva HTML/JSON
```
SpiderFoot in modalità server web locale, poi scansione dalla UI:
```bash
python3 sf.py -l 127.0.0.1:5001
# apri http://127.0.0.1:5001 → New Scan → target example.com
# scansione headless da CLI:
python3 sf.py -s example.com -t DOMAIN_NAME -o json > sf.json
```
Maltego (flusso tipico, GUI):
```text
1. Trascina un'entità "Domain" e imposta example.com
2. Esegui la transform "To DNS Name" / "To Email Address"
3. Espandi le nuove entità (IP, sottodomini) con altre transform
4. Il grafo evidenzia i nodi centrali (hub) e le relazioni
```

## Mitigazione e difesa
Dal punto di vista di chi difende (ridurre ciò che questi tool raccolgono):
1. **Minimizzare l'esposizione delle email** aziendali sul web (form al posto di indirizzi in chiaro) per ridurre la resa di theHarvester.
2. **Attack surface management**: eliminare sottodomini e host dimenticati che SpiderFoot/Maltego correlano.
3. **Igiene dei metadati e dei documenti** pubblici (autori, path interni negli EXIF/PDF).
4. **Monitoraggio del proprio grafo**: eseguire periodicamente questi tool contro la propria organizzazione per vedere cosa emerge e correggerlo.
5. **Threat intelligence**: alert su domini simili e credenziali trapelate correlate al brand.

## Lab
- **theHarvester su un dominio tuo o con bug-bounty pubblico**: confronta l'output con l'enumerazione manuale via crt.sh (vedi [[04 OSINT su Domini e Infrastruttura]]) per capire cosa aggiunge e cosa perde.
- **SpiderFoot in locale**: lancia una scansione su un target autorizzato e classifica i finding tra rumore e segnale; nota quanti falsi positivi vanno filtrati.
- **Maltego Community Edition**: ricostruisci il grafo di un dominio partendo da un'entità e usando le transform gratuite; osserva quali nodi diventano hub.
- **[[TryHackMe]]** → room del percorso *OSINT* che introducono theHarvester e la ricognizione automatizzata.

## Domande
1. **D:** Qual è il modello concettuale comune ai framework OSINT?  **R:** Entità → trasformazione → nuove entità: da un seed si generano dati collegati che diventano nuovi seed (pivoting automatizzato).
2. **D:** Per cosa è più indicato theHarvester?  **R:** Ricognizione rapida da CLI su email, sottodomini, host e IP di un dominio.
3. **D:** Qual è il punto di forza distintivo di Maltego?  **R:** La *link analysis* visuale: mostra graficamente le relazioni tra entità (persona, email, dominio, IP).
4. **D:** Perché l'output di SpiderFoot va sempre validato?  **R:** La copertura molto ampia produce anche molto rumore/falsi positivi che l'analista deve filtrare.
5. **D:** Gli strumenti OSINT sostituiscono l'analista?  **R:** No: automatizzano la raccolta, ma la correlazione, la validazione e il ragionamento restano compito umano.

## Collegamenti
- [[OSINT]]
- [[02 Motori di Ricerca e Google Dorking]]
- [[03 OSINT su Persone e Username]]
- [[04 OSINT su Domini e Infrastruttura]]
- [[Sicurezza Operativa per le Indagini OSINT]] — usali dietro l'ambiente isolato
- [[Nmap]] — validazione attiva dopo la fase passiva

## Fonti
- theHarvester (GitHub): https://github.com/laramies/theHarvester
- SpiderFoot (GitHub): https://github.com/smicallef/spiderfoot
- Maltego — documentazione ufficiale: https://docs.maltego.com/
- OSINT Framework: https://osintframework.com/
