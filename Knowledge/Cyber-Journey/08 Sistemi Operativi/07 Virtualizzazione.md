---
tipo: concetto
tag: [os]
fase: 0
fonti: 5
aggiornato: 2026-07-02
stato: maturo
aliases: ["Virtualizzazione"]
---

# Virtualizzazione: VM, Container, Hypervisor tipo 1/2

## In breve
La **virtualizzazione** astrae una risorsa fisica per fornirne copie multiple, isolate e gestibili. Un **hypervisor** virtualizza l'intera macchina (più OS *guest* sullo stesso hardware, ognuno col proprio kernel); i **container** virtualizzano l'OS condividendo il kernel host (namespaces + cgroups). È il fondamento di cloud, isolamento e sandboxing, ma **sposta — non elimina** — il confine di sicurezza: VM escape, container escape e side-channel cross-VM restano superfici d'attacco.

## Definizione
La **virtualizzazione** crea un'astrazione di una risorsa fisica per fornirne copie multiple, isolate e gestibili. In OSTEP e il tema portante: l'OS *virtualizza* CPU e memoria per i processi. Estendendo l'idea un livello sopra, un **Virtual Machine Monitor (VMM)** / **hypervisor** virtualizza l'**intera macchina**, permettendo a piu sistemi operativi *guest* di girare sullo stesso hardware. [Fonte: OSTEP, cap. 2; intro VMM cap. 1]

> OSTEP usa per i processi le stesse tecniche che fondano le VM: **Limited Direct Execution** ed **address translation**. Una VM e "un processo che crede di essere un computer". [Fonte: OSTEP, cap. 6, 15]

## Meccanismo: come si virtualizza

### Trap-and-emulate (CPU)
Il principio (Popek & Goldberg) e analogo alla LDE dei processi: il guest gira **direttamente** sull'hardware in modalita non privilegiata; quando esegue un'**istruzione privilegiata** (I/O, modifica tabelle), questa **trappa** verso l'hypervisor, che la **emula** e restituisce il controllo. Stesso pattern del kernel che intercetta le system call dei processi. [Fonte: OSTEP, cap. 6 (analogia LDE)]
- Problema storico x86: alcune istruzioni "sensibili" non trappavano -> tecniche di **binary translation** (VMware) o **paravirtualizzazione** (Xen, il guest e modificato e chiama l'hypervisor via hypercall).
- Soluzione moderna: estensioni hardware **Intel VT-x / AMD-V** (root/non-root mode) -> trap-and-emulate efficiente.

### Memoria
Doppia traduzione: il guest mantiene le sue page table (virtuale guest -> fisico guest), l'hypervisor mappa fisico guest -> fisico host. Realizzata via **shadow page tables** o, in HW, **EPT/NPT (nested paging)**. Eredita i concetti di [[Memoria Virtuale]]. [Fonte: OSTEP, cap. 15 (address translation, base concettuale)]

### I/O
Il VMM intercetta gli accessi ai device (emulazione) o usa **paravirtualized drivers** (virtio) / **passthrough** (SR-IOV) per le prestazioni. Concetti da [[I/O e Storage]].

## Tassonomia degli hypervisor
> Nota: questa tassonomia e conoscenza generale di sistemi; OSTEP v1.00 non ha un capitolo dedicato agli hypervisor moderni, ma ne pone le basi (VMM, trap-and-emulate).

- **Hypervisor di Tipo 1 (bare-metal)**: gira **direttamente sull'hardware**, senza OS host sottostante. Massime prestazioni e isolamento. Esempi: **VMware ESXi, Xen, Microsoft Hyper-V, KVM** (KVM trasforma il kernel Linux stesso in hypervisor tipo 1).
- **Hypervisor di Tipo 2 (hosted)**: gira **come applicazione sopra un OS host**. Piu comodo per desktop/test. Esempi: **VMware Workstation/Player, VirtualBox, QEMU** (in user-mode), Parallels.

## Container vs VM
Differenza fondamentale nel **livello di astrazione**:
- **VM**: virtualizza l'**hardware**; ogni guest ha il **proprio kernel** e OS completo. Isolamento forte, overhead maggiore (boot di un OS intero, immagini grandi).
- **Container** (Docker, LXC, Podman): virtualizza l'**OS**; tutti i container **condividono il kernel host** ma hanno **filesystem, rete e process tree isolati**. Su Linux si basano su **namespaces** (isolamento: PID, net, mount, user...) + **cgroups** (limiti su CPU/memoria/IO) + capabilities/seccomp. Avvio in millisecondi, immagini leggere; isolamento piu debole di una VM (un'unica superficie kernel condivisa).

| | VM | Container |
|---|---|---|
| Virtualizza | hardware | OS (kernel condiviso) |
| Kernel | uno per guest | condiviso con l'host |
| Boot/overhead | secondi, pesante | ms, leggero |
| Isolamento | forte | piu debole (kernel comune) |
| Tecnologia Linux | KVM/QEMU, VT-x/EPT | namespaces + cgroups |

## Esempio
Un'app web in **Docker** impacchetta solo userland + dipendenze e condivide il kernel Linux host -> deploy rapido e denso. La stessa app in una **VM** porta con se un intero OS guest -> piu isolata ma piu pesante. Cloud moderni combinano i due (container *dentro* VM leggere, es. Firecracker/Kata) per avere densita **e** isolamento.

## Implicazioni
- I container condividono il kernel: una vulnerabilita kernel -> **container escape** -> rilevante per [[Privilege Escalation Linux]] e [[Attacchi di Rete]].
- L'isolamento si fonda su [[Memoria Virtuale]] (page table annidate) e [[Processi]] (namespaces/cgroups estendono l'astrazione del processo).

## Approfondimento sicurezza
La virtualizzazione sposta il confine di sicurezza, ma non lo elimina:
- **VM escape** — bug nell'emulazione device del VMM permettono di uscire dal guest verso l'host:
  **VENOM** (CVE-2015-3456, floppy controller QEMU), falle in VirtualBox/VMware. Più raro e prezioso
  del container escape perché rompe l'isolamento "forte".
- **Container escape** — kernel condiviso → privilegi/mount/socket eccessivi portano sull'host. È il
  tema di [[Container Security (Docker)]] e [[Kubernetes Security (RBAC, escape)]].
- **Cross-VM side channel** — cache/TLB condivise tra VM co-residenti abilitano leak (Flush+Reload,
  L1TF/Foreshadow su Intel). Mitigazioni: core scheduling, disabilitare hyperthreading per workload
  sensibili, microcode.
- **Hypervisor & supply chain** — compromettere il VMM = controllo di tutti i guest; nested virt e
  introspection (VMI) usate sia in difesa (sandbox malware) sia in attacco.
- **Difesa scelta dell'isolamento** — per multi-tenant non fidato preferire VM/microVM
  (Firecracker, Kata) ai soli container; defense-in-depth con seccomp/AppArmor anche dentro la VM.

## Lab
- Crea una VM con KVM/VirtualBox e un container Docker della stessa app; confronta boot time, footprint
  e isolamento.
- **TryHackMe** — *Intro to Containerisation*; per l'escape pratico vedi i lab di [[Container Security (Docker)]].
- Ispeziona i namespace di un container: `lsns`, `cat /proc/<pid>/ns/*`.

## Domande
**D: Differenza fondamentale tra VM e container?**
R: La VM virtualizza l'**hardware** e ogni guest ha il proprio kernel (isolamento forte, overhead
alto); il container virtualizza l'**OS** condividendo il kernel host (leggero, ms di avvio, isolamento
più debole via namespaces+cgroups).

**D: Cos'è trap-and-emulate e perché serviva la binary translation su x86?**
R: Il guest gira diretto in modalità non privilegiata; le istruzioni privilegiate trappano
all'hypervisor che le emula. Su x86 alcune istruzioni sensibili non trappavano → VMware usava binary
translation, Xen la paravirtualizzazione; VT-x/AMD-V hanno poi risolto in HW.

**D: Perché un container escape è più "probabile" di un VM escape?**
R: Il container condivide il kernel host: un bug kernel o una config permissiva (privileged, mount,
socket) basta. La VM ha un confine HW/hypervisor, più difficile da bucare (serve un bug nel VMM).

**D: Per workload multi-tenant non fidato, VM o container?**
R: VM o microVM (Firecracker/Kata) per l'isolamento forte; i container puri condividono il kernel →
superficie unica. Idealmente container *dentro* VM leggere.

## Collegamenti
- Vedi anche: [[Processi]], [[Memoria Virtuale]], [[I/O e Storage]], [[Concetti dei Sistemi Operativi]]
- Cross-topic (sicurezza): [[Privilege Escalation Linux]], [[Attacchi di Rete]], [[Container Security (Docker)]], [[Kubernetes Security (RBAC, escape)]]

## Fonti
- [OSTEP, cap. 2 "Introduction to Operating Systems" (virtualizzazione)]
- [OSTEP, cap. 6 "Limited Direct Execution" (trap-and-emulate, base dei VMM)]
- [OSTEP, cap. 15 "Address Translation" (base della memoria virtualizzata)]
- Tassonomia hypervisor/container: conoscenza generale di sistemi (non in OSTEP v1.00)
- VENOM (CVE-2015-3456) VM escape — CrowdStrike: https://www.crowdstrike.com/blog/venom-vulnerability-details/
