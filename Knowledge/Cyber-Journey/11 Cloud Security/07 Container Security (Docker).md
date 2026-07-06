---
tipo: concetto
tag: [cloud, linux, tool]
fase: 3
fonti: 5
aggiornato: 2026-07-02
stato: maturo
aliases: ["Container Security (Docker)"]
---

# Container Security (Docker)

## In breve
Un **container** è un processo isolato dal resto del sistema tramite namespace (vista) e cgroups (risorse), più capabilities e seccomp/AppArmor per restringere le syscall. **Non è una VM**: condivide il kernel dell'host, quindi la sua sicurezza è in ultima analisi sicurezza del kernel condiviso e un **container escape** porta direttamente sull'host. I punti di rottura tipici sono `--privileged`, il socket `docker.sock` montato, capabilities pericolose (`CAP_SYS_ADMIN`) e mount sensibili.

## Definizione
Un **container** è un processo isolato dal resto del sistema tramite primitive del kernel Linux —
**namespace** (isolamento di vista: PID, NET, MNT, USER...) e **cgroups** (limiti di risorse) — più
**capabilities** e **seccomp/AppArmor** per restringere le syscall. **Non è una VM**: condivide il
kernel dell'host. Quindi la sicurezza del container è, in ultima analisi, sicurezza del kernel
condiviso: un **container escape** porta direttamente sull'host.

## Meccanismo: dove si rompe l'isolamento
- **Container privilegiato** (`--privileged`): rimuove quasi tutte le restrizioni → escape banale.
- **Socket Docker montato** (`/var/run/docker.sock`): chi lo raggiunge controlla il demone =
  controlla l'host (avvia un container che monta `/`).
- **Capabilities pericolose**: `CAP_SYS_ADMIN`, `CAP_SYS_PTRACE`, `CAP_DAC_READ_SEARCH`.
- **Mount sensibili**: host filesystem, `/proc`, dispositivi.
- **Immagini**: segreti hard-coded nei layer, base image con CVE, immagini non firmate.

## Esempio pratico — enumerazione ed escape
```bash
# Sono in un container? Indizi classici
cat /proc/1/cgroup        # presenza di "docker"/"kubepods"
ls -la /.dockerenv        # file sentinella
capsh --print             # capabilities correnti

# Escape 1: container privilegiato -> monto il disco dell'host
fdisk -l
mkdir /mnt/host && mount /dev/sda1 /mnt/host && chroot /mnt/host

# Escape 2: docker.sock montato dentro il container
docker -H unix:///var/run/docker.sock run -v /:/host -it alpine chroot /host sh

# Build sicura: utente non-root nell'immagine
# Dockerfile:
#   RUN adduser -D app && USER app
```

## Attacco / Difesa
| Vettore d'attacco | Contromisura difensiva |
|---|---|
| `--privileged` | Vietarlo; default no-new-privileges |
| `docker.sock` montato | Non montare mai il socket nei container; usare rootless/socket proxy |
| Capabilities eccessive | `--cap-drop=ALL` e aggiungere solo il minimo necessario |
| Container come root | `USER` non-root nel Dockerfile, **user namespace remap** |
| Immagini vulnerabili / con segreti | Scan (Trivy/Grype), distroless/minimal base, secret fuori dall'immagine |
| Syscall pericolose | Profili **seccomp** e **AppArmor**/SELinux attivi |

```bash
# Scansione vulnerabilità immagine
trivy image nginx:latest
# Esecuzione hardened
docker run --rm --cap-drop=ALL --security-opt=no-new-privileges \
  --read-only --user 1000:1000 myimage
```

## Lab
- **TryHackMe** — room *Intro to Containerisation*, *Docker Rodeo*
- **OWASP — Docker Security Cheat Sheet** — https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
- **Trivy** — https://github.com/aquasecurity/trivy / **Docker Bench** — https://github.com/docker/docker-bench-security
- **HackTricks — Docker Breakout / Privesc** — https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/docker-security/index.html

> [!warning] Etica
> Prova escape e abuso del socket Docker **solo** su host/container di tua proprietà o in lab. Un
> escape ti dà controllo dell'host: trattalo come un'azione altamente privilegiata.

## Domande
**D: Perché un container non è una sandbox di sicurezza come una VM?**
R: Condivide il **kernel** dell'host (isola solo via namespace/cgroups, non un hypervisor). Una
falla del kernel o una capability/mount eccessivi bypassano l'isolamento → escape sull'host. Per
isolamento forte servono microVM (Firecracker/Kata) o gVisor.

**D: Trovi `/var/run/docker.sock` montato in un container. Impatto?**
R: Game over: il socket parla col demone Docker (root sull'host). Avvio un container che monta `/`
dell'host e faccio `chroot` → controllo totale. È equivalente a root sull'host, non "solo" sul container.

**D: `--cap-drop=ALL` rende il container sicuro?**
R: Riduce molto la superficie ma non basta da solo: restano mount sensibili, socket, kernel
condiviso. Va combinato con `no-new-privileges`, seccomp/AppArmor, user namespace remap, `--read-only`,
utente non-root.

**D: Come capisci a runtime se sei dentro un container e se puoi evadere?**
R: `cat /proc/1/cgroup` (stringhe `docker`/`kubepods`), `/.dockerenv`, `capsh --print` per le
capability, `mount`/`fdisk -l` per dischi host montati, presenza di `docker.sock`. `CAP_SYS_ADMIN` o
`--privileged` = escape probabile.

## Approfondimento livello esperto

### Anatomia dell'escape `--privileged` (perché funziona)
Un container privilegiato gira con **tutte le capability**, **senza seccomp/AppArmor** e con accesso
ai **device** dell'host (`/dev`). Da qui i due classici:
- **Mount del disco host**: `fdisk -l` mostra `/dev/sda*` (visibili perché device non filtrati) →
  `mount /dev/sda1 /mnt/host && chroot /mnt/host` = filesystem host scrivibile.
- **release_agent / cgroup-v1 escape**: si crea un cgroup, si imposta `notify_on_release` e un
  `release_agent` che punta a uno script nel container; alla "release" il kernel lo esegue **come
  root sull'host**. È la tecnica storica di `--privileged` senza bisogno di device.

### Capability pericolose (mappa rapida)
| Capability | Abuso |
|---|---|
| `CAP_SYS_ADMIN` | mount, namespace, cgroup → la più potente, vicina a root |
| `CAP_SYS_PTRACE` | ptrace di processi host (se PID host condiviso) → injection |
| `CAP_SYS_MODULE` | carica kernel module → codice in ring 0 = escape diretto |
| `CAP_DAC_READ_SEARCH` | bypass permessi lettura → `shocker`/open_by_handle_at → leggi file host |
| `CAP_NET_RAW` | sniffing/spoofing sulla rete del container |

### Detection engineering
- **Runtime sensor** (Falco) — regole su: shell spawn in container (`spawned process in container`),
  scrittura in path sensibili, lettura `/etc/shadow`, uso di `mount`/`nsenter`, accesso a
  `docker.sock`. Falco aggancia syscall via eBPF.
- **MITRE ATT&CK**: **T1610** Deploy Container · **T1611** Escape to Host · **T1613** Container &
  Resource Discovery · **T1552.007** Container API credentials.
- **Audit host**: `auditd` su `mount`, `unshare`, `setns`; alert su container con `Privileged:true`
  (query a Docker/K8s API). In K8s, **admission controller** (OPA/Gatekeeper, Pod Security Standards)
  che blocca `privileged`, `hostPID`, `hostPath`, capability extra **prima** dello scheduling.

### Hardening — supply chain dell'immagine
Oltre al runtime: **firma** (cosign/Sigstore) + **provenance** (SLSA), **scan** in CI (Trivy/Grype)
con gate sui CVE critici, base **distroless**/minimal (meno binari = meno GTFO-style), **niente
segreti nei layer** (controlla con `dive`/`docker history` — i layer sono pubblici), `HEALTHCHECK` e
`USER` non-root nel Dockerfile. A runtime: rootless Docker / Podman per togliere il demone-root.

## Collegamenti
- [[Kubernetes Security (RBAC, escape)]]
- [[Privilege Escalation Linux]]
- [[Fondamenti Cloud e Shared Responsibility]]
- [[Logging e Detection Cloud (CloudTrail)]]

## Fonti
- Docker — Security documentation: https://docs.docker.com/engine/security/
- OWASP — Docker Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
- HackTricks — Docker Breakout: https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/docker-security/index.html
- Falco — Container runtime security rules: https://falco.org/docs/
- MITRE ATT&CK — Containers matrix (T1610/T1611/T1613): https://attack.mitre.org/matrices/enterprise/containers/
