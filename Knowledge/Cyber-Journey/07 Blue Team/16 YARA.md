---
tipo: entita
tag: [blue-team, tool]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["YARA"]
---

# YARA

## Cos'è
**YARA** è uno strumento per **identificare e classificare malware** tramite regole pattern-based. Una regola descrive stringhe, byte e condizioni che caratterizzano una famiglia di malware; YARA scansiona file, processi o dump di memoria cercando quei pattern. È lo standard de facto per condividere firme nell'[[Analisi Malware di Base|analisi malware]] e nella [[Threat Intelligence]].

## Anatomia di una regola
```yara
rule Esempio_Webshell_PHP
{
    meta:
        author = "blue-team"
        description = "Rileva webshell PHP che esegue comandi"
    strings:
        $a = "system($_GET" ascii
        $b = "eval(" ascii
        $c = /<\?php.{0,200}passthru/ nocase
    condition:
        $a or $b or $c
}
```

## Uso tipico
```bash
# Scansiona una cartella con un set di regole
yara -r regole.yar /var/www/

# Scansiona un processo in memoria (PID)
yara regole.yar 1337
```

## Quando si usa
- **Triage** di file sospetti raccolti durante l'[[Incident Response]].
- **Threat hunting** su larga scala (es. cercare un IOC noto su tutti gli endpoint).
- Integrato in sandbox come [[Any.run]] e in scanner come [[VirusTotal]] (YARA retrohunt).
- Per scrivere regole di rilevamento a partire da campioni analizzati.

## Note e trucchi
- Le condizioni possono combinare conteggi, offset e dimensioni del file (`filesize`).
- Regole troppo specifiche → si eludono facilmente; troppo generiche → falsi positivi. Bilanciare.
- Repository utili: **YARA-Rules**, le regole di Florian Roth (`signature-base`).

## Collegamenti
- [[Analisi Malware di Base]]
- [[Indicatori di Compromissione (IOC)]]
- [[Threat Intelligence]]
- [[VirusTotal]]
- [[Any.run]]
- [[Incident Response]]

## Fonti
- YARA Documentation: https://yara.readthedocs.io/
- YARA-Rules project: https://github.com/Yara-Rules/rules
- Florian Roth — signature-base: https://github.com/Neo23x0/signature-base
