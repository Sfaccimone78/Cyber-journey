# Fonti e Report Cybersecurity Ufficiali

Questa cartella raccoglie i documenti PDF originali scaricati dalle principali agenzie mondiali, pronti per essere letti direttamente da Obsidian (basta cliccarci sopra).

## Generali e Compliance
1. **NIST_CSF_2.0.pdf** (National Institute of Standards and Technology)
   - *Cybersecurity Framework 2.0* (aggiornato 2024). Il framework di riferimento per la gestione del rischio.
2. **CISA_Zero_Trust_Maturity_Model_v2.pdf** (CISA)
   - Modello ufficiale sull'architettura e implementazione Zero Trust.
3. **NIST_SP_800-53_Rev5.pdf**
   - L'elenco omnicomprensivo dei controlli di sicurezza tecnica ed organizzativa.

## Blue Team & Incident Response
4. **NIST_SP_800-61r2_Incident_Handling.pdf**
   - *Computer Security Incident Handling Guide*. La guida storica del NIST per i team di risposta agli incidenti. **Superata da r3** (vedi sotto) — tenuta come riferimento del modello classico a 4 fasi.
5. **NIST_SP_800-61r3_Incident_Response.pdf** — *aggiunto 2026-07-06*
   - *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile* (revisione 3, apr 2025). Ristruttura l'IR attorno al NIST CSF 2.0. Sostituisce r2.
   - Fonte: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf

## OSINT (Open Source Intelligence)
6. **Army_OSINT_ATP2_22_9.pdf**
   - *Open Source Intelligence Handbook (Dipartimento dell'Esercito USA)*. Uno dei manuali istituzionali più famosi per le metodologie di intelligence basata su fonti aperte, perfetto per strutturare indagini OSINT rigorose.

## Web Application Security — cartella `Web_OWASP/`
7. **Web_OWASP/OWASP_WSTG_v4.2.pdf** — *aggiunto 2026-07-06*
   - *OWASP Web Security Testing Guide v4.2*. La guida di riferimento per il testing di sicurezza delle applicazioni web (metodologia + test case per categoria).
   - Fonte: https://github.com/OWASP/wstg/releases/download/v4.2/wstg-v4.2.pdf
8. **Web_OWASP/OWASP_Top10_2025_Presentation.pdf** — *aggiunto 2026-07-06*
   - *OWASP Top 10:2025* (slide ufficiali di presentazione). Include le nuove categorie 2025 (Software Supply Chain Failures, Mishandling of Exceptional Conditions) e SSRF assorbito in Broken Access Control.
   - Documento completo (solo web): https://owasp.org/Top10/2025/
   - PDF slide: https://github.com/OWASP/Top10/tree/master/2025/Presentations

## AI e LLM Security — cartella `AI_LLM/`
9. **AI_LLM/OWASP_Top10_LLM_2025.pdf** — *aggiunto 2026-07-06*
   - *OWASP Top 10 for LLM Applications 2025*. Le 10 vulnerabilità principali delle applicazioni basate su LLM (Prompt Injection al #1, Sensitive Information Disclosure, Supply Chain, ecc.). Copre l'area `18 AI e LLM Security`.
   - Fonte: https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/

## Threat Intelligence — cartella `Threat_Intel/`
10. **Threat_Intel/ENISA_Threat_Landscape_2025.pdf** — *aggiunto 2026-07-06*
    - *ENISA Threat Landscape 2025* (v1.2, gen 2026). Analisi di 4.875 incidenti (lug 2024 – giu 2025): ransomware minaccia più impattante, phishing vettore d'intrusione dominante, crescente uso di AI da parte degli attaccanti.
    - Fonte: https://www.enisa.europa.eu/publications/enisa-threat-landscape-2025
