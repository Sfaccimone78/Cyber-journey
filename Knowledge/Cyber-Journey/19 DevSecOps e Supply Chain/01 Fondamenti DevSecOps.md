---
tipo: concetto
tag: [devsecops]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Fondamenti DevSecOps"]
---

# Fondamenti DevSecOps

## In breve
**DevSecOps** estende la cultura DevOps integrando la sicurezza come responsabilita condivisa lungo tutto il ciclo di vita del software, non come gate finale di un team separato. Il principio cardine e lo **shift-left**: anticipare i controlli di sicurezza il piu a sinistra possibile nella pipeline (IDE, commit, pull request) dove un difetto costa ordini di grandezza meno che in produzione. La sicurezza diventa **security as code**: policy, scansioni e controlli versionati e automatizzati come qualunque altro artefatto.

## Come funziona
Il modello tradizionale prevedeva un pentest a rilascio quasi pronto: feedback tardivo, costoso, spesso ignorato per non bloccare la release. DevSecOps ridistribuisce i controlli lungo l'intero flusso:

- **Plan**: threat modeling, requisiti di sicurezza, abuse cases.
- **Code**: linter di sicurezza nell'IDE, pre-commit hook, secret scanning.
- **Build/Test**: SAST, SCA sulle dipendenze, build riproducibili.
- **Release/Deploy**: firma artefatti, generazione SBOM, policy-as-code (OPA/Gatekeeper).
- **Operate/Monitor**: DAST, scansione runtime, detection, feedback verso il backlog.

Concetti chiave: **guardrail invece di gate** (la sicurezza guida senza bloccare arbitrariamente), **automazione** (il controllo umano non scala), **fail fast** (rompere la build presto e visibilmente) e **paved road** (percorsi pre-approvati e sicuri che gli sviluppatori scelgono perche comodi).

## Esempi
Pre-commit hook che blocca segreti e applica scansioni locali prima del push:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
  - repo: https://github.com/returntocorp/semgrep
    rev: v1.45.0
    hooks:
      - id: semgrep
        args: ["--config", "auto", "--error"]
```

Gate minimale in CI che fallisce su vulnerabilita critiche delle dipendenze:

```yaml
# .github/workflows/security.yml (estratto)
- name: Trivy filesystem scan
  run: trivy fs --severity HIGH,CRITICAL --exit-code 1 .
```

## Mitigazione e difesa
- Definire una **paved road**: template di pipeline e immagini base approvate centralmente.
- Differenziare **blocking vs non-blocking**: bloccare solo su finding ad alta confidenza e alta gravita per evitare alert fatigue.
- Misurare con metriche (MTTR delle vulnerabilita, coverage delle scansioni, percentuale di build firmate).
- Integrare la sicurezza nei rituali esistenti (PR review, retrospective) anziche in tool separati.

## Lab
- [[TryHackMe]] - percorso "DevSecOps" e room introduttive su CI/CD.
- Lab pratico: configurare pre-commit + un workflow GitHub Actions con trivy e gitleaks su un repo demo.
- OWASP DevSecOps Guideline come riferimento di maturita.

## Domande
1. **Cosa significa "shift-left"?** Anticipare i controlli di sicurezza nelle fasi iniziali (codice, PR) dove correggere costa meno.
2. **Differenza tra gate e guardrail?** Un gate blocca, un guardrail orienta verso scelte sicure mantenendo la velocita di rilascio.
3. **Perche l'automazione e centrale nel DevSecOps?** Il volume di build e dipendenze rende impossibile la revisione manuale; solo l'automazione scala.
4. **Cos'e la security as code?** Trattare policy e controlli come artefatti versionati, testabili e riproducibili.
5. **Cos'e una paved road?** Un percorso pre-approvato e sicuro che gli sviluppatori adottano perche e anche il piu comodo.

## Approfondimento livello esperto
La maturita DevSecOps si misura sulla **provenienza** e sulla **fiducia**: non basta scansionare, occorre poter dimostrare *come* un artefatto e stato prodotto. Qui DevSecOps converge con la supply chain security: framework come **SLSA** definiscono livelli di garanzia sulla build, mentre **sigstore/cosign** consentono firma e verifica keyless degli artefatti. Casi come **SolarWinds** (2020) hanno spostato l'attenzione del settore dalla sicurezza del codice alla sicurezza dell'ambiente di build: l'attaccante non modifico il sorgente, ma il processo di compilazione. Da qui la spinta normativa (Executive Order 14028 USA, linee guida CISA) verso SBOM obbligatori e attestazioni di provenienza. Il DevSecOps esperto progetta la pipeline come un sistema a fiducia minima: runner effimeri, segreti a vita breve, separazione tra build e deploy, e verifica crittografica di ogni transizione di stato.

## Collegamenti
- [[02 Sicurezza CI-CD Pipeline|Sicurezza CI-CD Pipeline]]
- [[03 SAST, DAST e SCA|SAST, DAST e SCA]]
- [[05 SBOM e SLSA|SBOM e SLSA]]
- [[Container Security (Docker)]]
- [[Kubernetes Security (RBAC, escape)]]

## Fonti
- https://owasp.org/www-project-devsecops-guideline/
- https://slsa.dev/spec/v1.0/
- https://www.cisa.gov/resources-tools/resources/securing-software-supply-chain-recommended-practices
