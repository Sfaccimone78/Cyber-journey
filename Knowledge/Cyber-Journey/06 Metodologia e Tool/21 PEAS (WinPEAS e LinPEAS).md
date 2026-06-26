---
tipo: entita
tag: [tool]
fase: 2
fonti: 2
aggiornato: 2026-06-21
stato: maturo
aliases: ["PEAS", "WinPEAS", "LinPEAS", "PEASS-ng"]
---

# PEAS (WinPEAS e LinPEAS)

> **Nota etica**: solo lab autorizzati o engagement con permesso scritto.

## In breve
**PEASS-ng** è la suite di script di **enumerazione automatica per privilege escalation**: **LinPEAS** (Linux) e **WinPEAS** (Windows). Lanciati su una macchina dove hai già una shell utente, scansionano *centinaia* di possibili vettori e li **colorano per priorità**, così vedi subito cosa vale la pena approfondire. Sono il primo passo pratico della post-exploitation locale, complementari a [[Privilege Escalation Linux]] e [[Privilege Escalation Windows]].

## Uso
```bash
# LinPEAS — scarica ed esegui in memoria (no scrittura su disco)
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh
# oppure trasferisci e: ./linpeas.sh -a  (controlli completi)
```
```cmd
:: WinPEAS — versione exe o bat
winPEASx64.exe
.\winPEAS.bat
```

## Come leggere l'output (la parte che conta)
PEAS produce **tantissimo** testo: il valore è nel **codice colore**.
- **Rosso/giallo evidenziato** = molto probabilmente sfruttabile → guarda qui per primo.
- Sezioni chiave Linux: *SUID/SGID* ([[SUID e SGID]]), *capabilities* ([[Capabilities Linux]]), *sudo* ([[sudo]]), *cron* ([[Cron e Job Pianificati]]), *kernel/exploit suggeriti*, *credenziali in file*.
- Sezioni chiave Windows: *servizi* (unquoted/weak perms), *AlwaysInstallElevated*, *token privileges* (`SeImpersonate`), *credenziali salvate*, *AutoLogon*, *scheduled task*.

> [!tip] Non fidarti ciecamente
> PEAS **suggerisce**, non conferma. Un kernel exploit proposto può non compilare; un servizio "weak perms" può non essere riavviabile. Verifica sempre manualmente il vettore prima di bruciarlo.

## Note operative
- Pesantemente flaggato da AV/EDR (soprattutto WinPEAS): in ambienti monitorati preferisci controlli manuali mirati o [[PowerUp]].
- LinPEAS `-a` = tutti i check (più rumoroso/lento); senza flag = veloce.

## Detection
- Esecuzione di script di enum massiva (molte letture di `/etc`, query WMI/registro), download da github.
- MITRE: **T1082** (System Information Discovery), **T1083** (File and Directory Discovery).

## Collegamenti
- [[Privilege Escalation Linux]] · [[Privilege Escalation Windows]]
- [[Capabilities Linux]] · [[SUID e SGID]] · [[sudo]] · [[PowerUp]]
- [[Post-Exploitation]] · [[Enumerazione]]

## Fonti
- PEASS-ng — GitHub: https://github.com/peass-ng/PEASS-ng
- HackTricks (autori di PEAS) — Linux/Windows local privesc: https://book.hacktricks.xyz/
