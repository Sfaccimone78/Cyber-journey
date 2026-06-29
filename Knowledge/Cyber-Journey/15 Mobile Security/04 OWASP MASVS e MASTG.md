---
tipo: concetto
tag: [mobile]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["OWASP MASVS e MASTG"]
---

# OWASP MASVS e MASTG

## In breve
MASVS (Mobile Application Security Verification Standard) è lo standard OWASP che definisce i requisiti di sicurezza per app mobile; MASTG (Mobile Application Security Testing Guide) è la guida pratica con test, tecniche e tool per verificarli. Categoria: framework di verifica e metodologia. Impatto: fornisce un metro oggettivo e ripetibile per valutare e certificare la sicurezza di un'app.

## Come funziona
MASVS (versione moderna) è organizzato in categorie di controllo: **MASVS-STORAGE** (dati locali), **MASVS-CRYPTO** (crittografia), **MASVS-AUTH** (autenticazione), **MASVS-NETWORK** (comunicazioni), **MASVS-PLATFORM** (interazione con la piattaforma e IPC), **MASVS-CODE** (qualità e build), **MASVS-RESILIENCE** (resistenza a reversing e tampering), **MASVS-PRIVACY**. Definisce due livelli di verifica: **L1** (sicurezza standard, applicabile a tutte le app) e **L2** (difesa in profondità per app ad alto rischio, es. fintech, sanità). MASTG mappa ogni requisito a test concreti (statici e dinamici) e fornisce i crackme (UnCrackable) come palestra. Il MAS Checklist collega requisiti, livelli e test ID in un foglio operativo per l'assessment.

## Esempi
```bash
# Clonare i crackme ufficiali per esercitarsi
git clone https://github.com/OWASP/owasp-mastg.git
# i crackme sono in: owasp-mastg/Crackmes/

# Esempio: risolvere Android UnCrackable L1 (root detection)
adb install UnCrackable-Level1.apk
objection -g owasp.mstg.uncrackable1 explore
# dentro objection: bypass della root detection
android root disable
# poi invocare il check con il flag corretto

# Mappare un finding al requisito MASVS (esempio di annotazione report)
# MASVS-STORAGE-1  -> dati sensibili trovati in SharedPreferences in chiaro (FAIL, L1)
# MASVS-NETWORK-1  -> traffico in HTTPS con pinning assente (FAIL, L2)
# MASVS-RESILIENCE-1 -> root detection bypassabile con singolo hook (FAIL, L2)

# Tool che automatizza parte dei check MASTG
mobsf            # MobSF: analisi statica/dinamica con report mappato a MASVS
```

## Mitigazione e difesa
1. Adottare MASVS come requisito contrattuale/di progetto fin dal design (security by design).
2. Scegliere il livello corretto: L1 per app generiche, L2 + R per app che gestiscono dati critici.
3. Integrare i test MASTG nella pipeline CI/CD (es. MobSF, semgrep mobile rules).
4. Usare la MAS Checklist come gate di rilascio, tracciando ogni requisito a PASS/FAIL.
5. Ripetere la verifica a ogni release rilevante: la conformità non è statica.

## Lab
- OWASP MASTG Crackmes: Android UnCrackable L1-L4, iOS UnCrackable L1-L2.
- MobSF su DIVA, InsecureBankv2, iGoat per vedere il mapping automatico ai requisiti.
- [[TryHackMe]] room mobile per applicare i test MASTG in contesto guidato.
- [[HackTheBox]] challenge Mobile da risolvere annotando i requisiti violati.

## Domande
**D:** Qual è la differenza tra MASVS e MASTG?
R: MASVS definisce i requisiti (il "cosa"), MASTG fornisce i test e le tecniche per verificarli (il "come").

**D:** Cosa distingue il livello L1 dal L2?
R: L1 è la baseline per tutte le app; L2 aggiunge difesa in profondità per app ad alto rischio.

**D:** Cosa copre la categoria MASVS-RESILIENCE?
R: La resistenza dell'app a reverse engineering e tampering (anti-debug, anti-hooking, integrity check).

**D:** A cosa servono i crackme UnCrackable?
R: Sono app palestra ufficiali per esercitare bypass di root/jailbreak detection e anti-tamper.

## Approfondimento livello esperto
La categoria RESILIENCE (in MASVS L2 + R, ex MSTG-RESILIENCE) è la più sottile: richiede non un singolo controllo ma una strategia stratificata, perché qualunque check client-side è bypassabile da un attaccante con root e Frida. La metrica corretta non è "impossibile" ma "costoso": più layer indipendenti (root detection + integrity + anti-Frida + attestazione server) alzano il tempo necessario. Un assessment esperto documenta non solo il FAIL ma la catena di bypass usata (es. UnCrackable L4 richiede packing + native anti-tamper + obfuscation, da risolvere con frida-dexdump + patch di funzioni native). MASVS-PRIVACY (introdotto nelle versioni recenti) sposta il focus su minimizzazione dati e trasparenza, allineandosi a GDPR. OPSEC del tester: MobSF dynamic analysis gira su emulatore/device controllato; attenzione che alcune app rilevano MobSF stesso. La MAS Checklist va versionata col report perché i test ID cambiano tra versioni del MASTG.

## Collegamenti
- [[Fondamenti Mobile]]
- [[Android Pentest]]
- [[iOS Pentest]]
- [[Intercettazione traffico e API mobile]]
- [[Insecure Data Storage e Crypto su mobile]]
- [[OWASP Top 10]]
- [[Penetration Testing]]
- [[Reverse Engineering]]

## Fonti
- OWASP MASVS: https://mas.owasp.org/MASVS/
- OWASP MASTG: https://mas.owasp.org/MASTG/
- OWASP MAS Checklist: https://mas.owasp.org/checklists/
