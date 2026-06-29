---
tipo: concetto
tag: [devsecops]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["SAST, DAST e SCA"]
---

# SAST, DAST e SCA

## In breve
Sono le tre famiglie di analisi automatica della sicurezza applicativa integrate in pipeline. **SAST** (Static Application Security Testing) analizza il codice sorgente senza eseguirlo, cercando pattern vulnerabili e flussi di dati pericolosi. **DAST** (Dynamic) testa l'applicazione in esecuzione dall'esterno, come una scatola nera. **SCA** (Software Composition Analysis) inventaria le dipendenze di terze parti e le confronta con database di vulnerabilita note (CVE/GHSA). Sono complementari: SAST trova bug nel *tuo* codice, SCA nelle *altrui* librerie, DAST verifica il comportamento reale runtime.

## Come funziona
- **SAST**: costruisce un AST e un grafo di data-flow per fare **taint analysis** (tracciare input non fidati dalla source al sink). Veloce, copre tutto il codice, ma genera falsi positivi e non vede problemi runtime/config. Strumenti: Semgrep, CodeQL, SonarQube.
- **DAST**: invia richieste reali e osserva le risposte (fuzzing, injection probing). Trova problemi solo nelle parti raggiungibili e richiede un'app deployata; pochi falsi positivi ma copertura parziale. Strumenti: OWASP ZAP, Burp, Nuclei.
- **SCA**: parsa i lockfile (`package-lock.json`, `requirements.txt`, `go.sum`) per risolvere l'albero delle dipendenze, incluse quelle transitive, e cerca corrispondenze in advisory DB. Strumenti: Trivy, Grype, Snyk, Dependabot. Spesso genera anche l'**SBOM**.

## Esempi
SCA delle dipendenze e del filesystem con Trivy e Grype:

```bash
# Trivy: scansione progetto, fallisce su HIGH/CRITICAL
trivy fs --scanners vuln --severity HIGH,CRITICAL --exit-code 1 .

# Grype su un'immagine container, output tabellare
grype python:3.11-slim -o table --fail-on high

# Genera anche l'inventario (SBOM) con syft
syft dir:. -o cyclonedx-json > sbom.json
```

SAST con Semgrep e secret scanning con gitleaks/trufflehog:

```bash
# Semgrep con ruleset gestito + regola custom
semgrep --config "p/owasp-top-ten" --config ./rules/ --error .

# gitleaks: segreti nel working tree e nella history
gitleaks detect --source . --redact -v

# trufflehog: verifica anche se le chiavi trovate sono ancora valide
trufflehog git file://. --only-verified
```

Regola Semgrep custom (taint da request a os.system):

```yaml
rules:
  - id: py-command-injection
    languages: [python]
    severity: ERROR
    mode: taint
    pattern-sources: [{ pattern: "flask.request.args.get(...)" }]
    pattern-sinks: [{ pattern: "os.system(...)" }]
    message: "Input utente non sanificato passa a os.system (command injection)"
```

## Mitigazione e difesa
- Eseguire **SCA e secret scanning su ogni PR** (veloci), SAST completo su push, DAST in staging notturno.
- **Triage e baselining**: marcare i falsi positivi per evitare alert fatigue; bloccare solo su nuovi finding ad alta gravita.
- Combinare gitleaks (pattern) e trufflehog (verifica attiva) per ridurre rumore e confermare segreti vivi.
- Versionare le regole insieme al codice; mantenere un allowlist esplicito e revisionato.

## Lab
- [[TryHackMe]] - room su SAST/DAST e dependency scanning.
- OWASP Juice Shop o DVWA come bersaglio DAST con OWASP ZAP.
- Lab: aggiungere trivy + semgrep + gitleaks a un workflow GitHub Actions e analizzare i finding.

## Domande
1. **Differenza tra SAST e DAST?** SAST analizza il codice fermo (white-box), DAST l'app in esecuzione (black-box); coperture e falsi positivi opposti.
2. **Cosa copre l'SCA che SAST non vede?** Le vulnerabilita note nelle dipendenze di terze parti, incluse quelle transitive.
3. **Cos'e la taint analysis?** Il tracciamento di dati non fidati da una source a un sink sensibile per individuare injection.
4. **Perche affiancare trufflehog a gitleaks?** trufflehog verifica se i segreti trovati sono ancora validi, riducendo i falsi positivi azionabili.
5. **Perche non bloccare la build su ogni finding?** L'eccesso di falsi positivi genera alert fatigue e porta a ignorare gli alert reali.

## Approfondimento livello esperto
Lo scanning delle dipendenze ha un limite epistemico: l'advisory DB conosce solo le CVE *pubblicate*. Le vulnerabilita della supply chain piu gravi sono spesso **0-day di processo** (un pacchetto legittimo che diventa malevolo, vedi [[04 Supply Chain e Dependency Confusion|Supply Chain e Dependency Confusion]]) che nessun SCA segnala perche il pacchetto non e "vulnerabile", e *ostile*. Da qui l'importanza di **reachability analysis** (la dipendenza vulnerabile e effettivamente invocata?) per ridurre il rumore, e di tecniche come il **binary/source attestation**. CodeQL porta la taint analysis a livello di query database semantico, permettendo varianti hunting su intere codebase. La frontiera e l'integrazione tra SCA, SBOM (inventario) e provenienza SLSA: non basta sapere *cosa* contiene un artefatto, serve sapere *da dove viene* e firmarlo con sigstore/cosign per renderlo verificabile a valle.

## Collegamenti
- [[02 Sicurezza CI-CD Pipeline|Sicurezza CI-CD Pipeline]]
- [[04 Supply Chain e Dependency Confusion|Supply Chain e Dependency Confusion]]
- [[05 SBOM e SLSA|SBOM e SLSA]]
- [[Container Security (Docker)]]
- [[Kubernetes Security (RBAC, escape)]]

## Fonti
- https://owasp.org/www-community/Source_Code_Analysis_Tools
- https://semgrep.dev/docs/
- https://github.com/anchore/grype
