---
tipo: concetto
tag: [devsecops]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["SBOM e SLSA"]
---

# SBOM e SLSA

## In breve
Sono i due pilastri della **trasparenza e integrita** della supply chain. Un **SBOM** (Software Bill of Materials) e l'inventario formale e leggibile a macchina di tutti i componenti di un artefatto: dipendenze, versioni, licenze, hash. **SLSA** (Supply-chain Levels for Software Artifacts) e un framework di garanzie sul *processo* di build, organizzato in livelli crescenti di rigore, che culmina nella **provenance**: un'attestazione firmata che lega l'artefatto al sorgente esatto e all'ambiente che lo ha prodotto. SBOM risponde a "cosa c'e dentro?", SLSA a "come e stato fatto e posso fidarmi?".

## Come funziona
**SBOM** segue due formati standard: **CycloneDX** (OWASP) e **SPDX** (Linux Foundation). Viene generato automaticamente in build (es. con syft) e consumato per: matching continuo con nuove CVE, audit di licenze, risposta rapida agli incidenti ("uso quella libreria vulnerabile?").

**SLSA v1.0** definisce **build levels**:
- **L0**: nessuna garanzia.
- **L1**: provenance esiste (la build e documentata e l'origine dichiarata).
- **L2**: build su servizio ospitato con provenance **firmata**.
- **L3**: build **isolata e non falsificabile** (hardened), provenance non manipolabile dal processo di build stesso.

La **provenance** e un documento (in-toto attestation) che descrive builder, sorgente, parametri e digest dell'output, firmato crittograficamente. La verifica a valle confronta il digest dell'artefatto con quello attestato e valida la firma.

## Esempi
Generazione SBOM con syft e scansione dell'SBOM con grype:

```bash
# SBOM in formato CycloneDX e SPDX
syft myapp:1.0 -o cyclonedx-json=sbom.cdx.json
syft myapp:1.0 -o spdx-json=sbom.spdx.json

# Scansiona l'SBOM contro le CVE note (non l'immagine intera)
grype sbom:./sbom.cdx.json --fail-on critical
```

Firma keyless di un'immagine e verifica con cosign (sigstore):

```bash
# Firma keyless: identita via OIDC, niente chiavi da gestire
COSIGN_EXPERIMENTAL=1 cosign sign registry.io/myapp@sha256:abc...

# Verifica firma + identita del firmatario
cosign verify registry.io/myapp@sha256:abc... \
  --certificate-identity-regexp '.*@azienda\.it' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com

# Allega e firma l'SBOM come attestazione dell'immagine
cosign attest --predicate sbom.cdx.json --type cyclonedx registry.io/myapp@sha256:abc...
```

Generazione provenance SLSA in GitHub Actions (estratto):

```yaml
jobs:
  provenance:
    permissions:
      id-token: write   # OIDC per firma keyless
      contents: read
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v2.0.0
    with:
      base64-subjects: ${{ needs.build.outputs.digest }}
```

## Mitigazione e difesa
- **Generare SBOM a ogni build** e archiviarlo come artefatto per il monitoraggio continuo delle CVE.
- **Firmare gli artefatti** (immagini, binari) con cosign e firma keyless via OIDC: nessuna chiave da custodire.
- Imporre la **verifica della firma e della provenance al deploy** (admission controller in Kubernetes, es. Kyverno/policy-controller).
- Puntare almeno a **SLSA L2/L3**: build isolata, provenance firmata e non falsificabile.
- Conservare le attestazioni in un registry trasparente (Rekor) per audit immutabile.

## Lab
- [[TryHackMe]] - room su supply chain integrity e signing.
- Lab: generare un SBOM con syft, firmarlo e verificarlo con cosign su un'immagine demo.
- Esercizio: configurare un admission controller che rifiuta immagini non firmate (deliberately vulnerable cluster).

## Domande
1. **Differenza tra SBOM e SLSA?** SBOM elenca *cosa* contiene un artefatto; SLSA garantisce *come* e stato prodotto e la sua provenienza.
2. **Cosa distingue SLSA L1 da L3?** L1 ha provenance dichiarata; L3 richiede build isolata e provenance non falsificabile dal processo stesso.
3. **Cos'e la provenance?** Un'attestazione firmata che lega artefatto, sorgente, builder e parametri di build, verificabile a valle.
4. **Cosa rende "keyless" la firma sigstore?** L'identita deriva da un certificato OIDC effimero invece che da una chiave privata persistente.
5. **A cosa serve Rekor?** A un log trasparente e immutabile delle firme/attestazioni, per audit verificabile.

## Approfondimento livello esperto
La forza di **sigstore** sta nell'eliminare il problema piu fragile della firma tradizionale: la gestione delle chiavi a lungo termine. Con la firma **keyless**, Fulcio emette un certificato X.509 a vita brevissima legato a un'identita OIDC (es. il workflow GitHub Actions), si firma, e la prova viene registrata nel log trasparente **Rekor**; la chiave privata non sopravvive alla sessione. Questo, combinato con SLSA L3, mira a chiudere proprio i gap sfruttati da **SolarWinds** (build environment compromesso) e **xz** (release divergente dal sorgente): se la provenance attesta digest e ambiente in modo non falsificabile, un artefatto manomesso o costruito altrove fallisce la verifica al deploy. La frontiera operativa e l'**enforcement a livello di cluster**: un admission controller che, prima di schedulare un pod, verifica firma cosign e politica di provenance, integrando cosi DevSecOps con la sicurezza runtime di [[Kubernetes Security (RBAC, escape)|Kubernetes]].

## Collegamenti
- [[04 Supply Chain e Dependency Confusion|Supply Chain e Dependency Confusion]]
- [[03 SAST, DAST e SCA|SAST, DAST e SCA]]
- [[02 Sicurezza CI-CD Pipeline|Sicurezza CI-CD Pipeline]]
- [[Container Security (Docker)]]
- [[Kubernetes Security (RBAC, escape)]]

## Fonti
- https://slsa.dev/spec/v1.0/levels
- https://www.sigstore.dev/
- https://cyclonedx.org/
