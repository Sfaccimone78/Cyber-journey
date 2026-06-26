---
tipo: concetto
tag: [linux]
fase: 1
fonti: 3
aggiornato: 2026-06-25
stato: maturo
aliases: ["Gestione Pacchetti"]
---

# Gestione Pacchetti

## In breve

Il **package management** è il metodo con cui Linux installa, aggiorna e rimuove software in modo controllato. Un **package file** è una raccolta compressa di file (eseguibili, dati, librerie) più **metadata**: descrizione, versione, dipendenze e script pre/post-installazione. I pacchetti risiedono in **repository** centrali firmati, mantenuti dal distributore — secondo Shotts è il fattore più importante nella qualità di una distribuzione.

Esistono due grandi famiglie storiche più una rolling-release:

| Famiglia | Formato | Distribuzioni | Low-level | High-level |
|----------|---------|---------------|-----------|------------|
| Debian | `.deb` | Debian, Ubuntu, Mint, Raspbian | `dpkg` | **`apt`** / apt-get / aptitude |
| Red Hat | `.rpm` | Fedora, RHEL, CentOS, Rocky | `rpm` | **`dnf`** / yum |
| Arch | `.pkg.tar.zst` | Arch, Manjaro, EndeavourOS | — | **`pacman`** |

---

## Come funziona

I package manager operano su **due livelli**:
- **Low-level** (`dpkg`, `rpm`): installano/rimuovono *un singolo file di pacchetto*, **senza** risolvere le dipendenze (se ne manca una, escono con errore).
- **High-level** (`apt`, `dnf`, `pacman`): interrogano i metadata dei repository, **risolvono le dipendenze** automaticamente e scaricano tutto il necessario.

Le **dipendenze** nascono perché i programmi condividono **librerie**: se un pacchetto richiede una libreria condivisa, ha una *dependency* e il gestore la installa insieme. I repository sono suddivisi per ciclo di vita (stable / testing / development) e possono includere **repository di terze parti** (per software con vincoli legali o esterno); aggiungere una terza parte richiede di registrarla manualmente e ne aumenta la superficie di fiducia.

### Tabella comparativa dei comandi

| Operazione | Debian/Ubuntu (apt) | RHEL/Fedora (dnf) | Arch (pacman) |
|-----------|---------------------|-------------------|---------------|
| Aggiorna indice | `apt update` | `dnf check-update` | `pacman -Sy` |
| Aggiorna sistema | `apt upgrade` | `dnf upgrade` | `pacman -Syu` |
| Cerca | `apt search <str>` | `dnf search <str>` | `pacman -Ss <str>` |
| Installa | `apt install <pkg>` | `dnf install <pkg>` | `pacman -S <pkg>` |
| Rimuovi | `apt remove <pkg>` | `dnf remove <pkg>` | `pacman -R <pkg>` |
| Rimuovi + config/orfani | `apt purge` / `autoremove` | `dnf remove` | `pacman -Rns` |
| Info pacchetto | `apt show <pkg>` | `dnf info <pkg>` | `pacman -Si <pkg>` |
| Lista installati | `apt list --installed` / `dpkg -l` | `dnf list installed` / `rpm -qa` | `pacman -Q` |
| File → pacchetto | `dpkg -S <file>` | `rpm -qf <file>` | `pacman -Qo <file>` |
| Installa file locale | `dpkg -i <file.deb>` | `rpm -i <file.rpm>` / `dnf install ./f.rpm` | `pacman -U <file>` |

> [!warning] Modello rolling di Arch
> `pacman -Syu` non distingue tra aggiornamenti di sicurezza e feature — scarica *tutto*. Questo lo rende poco adatto a server di produzione dove servono patch di sicurezza selettive.

---

## Esempio pratico

```bash
# Debian/Ubuntu — il pattern canonico: aggiorna indice POI aggiorna i pacchetti
sudo apt update && sudo apt upgrade -y
sudo apt install nginx
sudo apt purge nginx && sudo apt autoremove   # rimuove anche config e dipendenze orfane

# Fedora/RHEL
sudo dnf upgrade --refresh -y
sudo dnf install nginx

# Arch — un solo comando per sincronizzare e aggiornare tutto
sudo pacman -Syu
sudo pacman -S nginx

# Scoprire quale pacchetto ha installato un file (utile in audit)
dpkg -S /usr/bin/vim          # Debian
rpm -qf /usr/bin/vim          # Red Hat
```

---

## Comandi chiave

| Comando | Funzione |
|---------|----------|
| `apt` / `apt-get` | gestore high-level Debian (risoluzione dipendenze) |
| `dpkg` | low-level Debian (`-i` installa, `-l` lista, `-S` cerca file) |
| `dnf` / `yum` | gestore high-level Red Hat |
| `rpm` | low-level Red Hat (`-i/-U/-q/-qa/-qf`) |
| `pacman` | gestore Arch (`-S/-R/-Q/-Syu`) |
| `apt-cache` / `dnf search` | ricerca nei metadata |
| `unattended-upgrades` / `dnf-automatic` | patch di sicurezza automatiche |

---

## Rilevanza per la sicurezza

- **Aggiorna l'indice prima di installare** (`apt update` / `dnf check-update`): un indice locale obsoleto porta a versioni vecchie o a fallimenti di dipendenza.
- **Automatizza solo le patch di sicurezza**: su Ubuntu gli aggiornamenti di sicurezza arrivano da `<release>-security`; abilita **`unattended-upgrades`** (o `dnf-automatic` su Fedora/RHEL) limitato al canale security, così le vulnerabilità note si chiudono senza introdurre cambi di feature.
- **Verifica le firme GPG**: tutti i gestori nativi usano la **verifica crittografica della firma** dei repository — è la differenza tra un upgrade di routine e un incidente di supply-chain. Non disabilitare mai il controllo firma.
- **Preferisci i repository ufficiali della distro**; usa repo del vendor solo se necessario, **evita gli script `curl ... | sh`** da blog sconosciuti, e documenta ogni terza parte che aggiungi.
- **Riavvia dopo aggiornamenti di kernel, driver o librerie core**: il vecchio codice resta in memoria finché non si riavvia (`needrestart` / `dnf needs-restarting` aiutano a capire cosa).
- **Enumerazione (pentest)**: la versione di un pacchetto installato (`dpkg -l`, `rpm -qa`) rivela software vulnerabile a CVE note; `dpkg -S`/`rpm -qf` mappano un binario sospetto al pacchetto di origine.
- **AUR su Arch**: i pacchetti AUR sono build-script di utenti non vettati — leggi il `PKGBUILD` prima di compilare. Per **Flatpak/Snap/Nix** valgono cautele analoghe ma con sandboxing e verifica crittografica aggiuntiva.

---

## Collegamenti

- [[Filesystem Linux]]
- [[Permessi Linux]]
- [[Comandi Linux di Base]]
- [[Privilege Escalation Linux]]

## Fonti

- The Linux Command Line (W. Shotts), Cap. 14 "Package Management": https://linuxcommand.org/tlcl.php
- LinuxBlog.io — "Linux Package Managers Compared: APT, DNF, Pacman and Zypper" (2025)
- PatchMon — "The Complete Guide to Linux Patch Management" (2026)
