---
tipo: entita
tag: [tool, web, proxy, scanner]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["OWASP ZAP"]

---

# OWASP ZAP

> **Nota etica**: OWASP ZAP va usato solo su applicazioni proprie o su ambienti autorizzati. Scansionare sistemi senza permesso è illegale.

## Cos'è

**OWASP ZAP (Zed Attack Proxy)** è uno scanner di sicurezza web **open source e gratuito** mantenuto da OWASP. Come [[Burp Suite]], agisce da proxy intercettante tra browser e server, ma è orientato all'automazione e alla scansione attiva. È lo strumento ideale per chi inizia (interfaccia più guidata) e per l'integrazione in pipeline CI/CD.

## Uso tipico

```bash
# Avvio da riga di comando (headless) con spider + scan attivo
zap.sh -daemon -port 8080 -host 127.0.0.1 \
  -config api.key=mysecretkey

# Avvio della GUI (modalità interattiva)
zap.sh

# Spider automatico di un target (via API ZAP)
curl "http://localhost:8080/JSON/spider/action/scan/?apikey=mysecretkey&url=http://target.com"

# Avvio scansione attiva
curl "http://localhost:8080/JSON/ascan/action/scan/?apikey=mysecretkey&url=http://target.com"
```

Modalità operative principali:

| Modalità | Descrizione |
|----------|-------------|
| **Standard** | GUI completa, uso manuale + automatico |
| **Headless/Daemon** | Senza GUI, controllato via API REST o CLI |
| **Desktop** | Integrazione con browser via browser extension ZAP |

Flusso base nella GUI:
1. Aprire ZAP → configurare browser con proxy `127.0.0.1:8080`
2. Navigare il sito target (ZAP registra le richieste in "Sites")
3. Tasto destro su un sito → **Active Scan** per avviare la scansione automatica
4. Controllare la tab **Alerts** per i risultati classificati per gravità

## Quando si usa

- **Scansione automatica veloce** di applicazioni web: ZAP trova vulnerabilità comuni ([[SQL Injection]], [[Cross-Site Scripting (XSS)]], [[Security Misconfiguration]], header mancanti) senza configurazione avanzata
- **Integrazione CI/CD**: con Docker e l'API REST, ZAP può essere inserito in pipeline GitHub Actions / Jenkins per test di sicurezza automatici ad ogni deploy
- **DAST (Dynamic Application Security Testing)**: test della sicurezza dell'applicazione in esecuzione
- Come alternativa gratuita a [[Burp Suite]] Professional per la scansione attiva

```bash
# Esempio Docker per scan rapido (ZAP Full Scan)
docker run -t ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py \
  -t https://example.com -r report.html
```

## Note e trucchi

- Gli **add-on** (Marketplace ZAP) estendono le funzionalità: FuzzDB, Retire.js (dipendenze JS vulnerabili), Script Console
- La **Forced Browse** scansiona directory nascoste usando wordlist (simile a `gobuster`)
- Lo **Spider AJAX** gestisce applicazioni Single Page Application (React, Angular) che il classico spider non riesce a esplorare
- I falsi positivi sono più frequenti rispetto a [[Burp Suite]] Pro — verificare manualmente le alert critiche
- ZAP salva le sessioni come file `.session` riapribli in seguito

## Collegamenti

- [[Burp Suite]]
- [[OWASP Top 10]]
- [[Security Misconfiguration]]
- [[SQL Injection]]
- [[Cross-Site Scripting (XSS)]]
- [[PortSwigger Web Academy]]

## Fonti

- OWASP ZAP Official Site: https://www.zaproxy.org/
- OWASP ZAP Getting Started: https://www.zaproxy.org/getting-started/
- HackTricks ZAP: https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/owasp-zap
