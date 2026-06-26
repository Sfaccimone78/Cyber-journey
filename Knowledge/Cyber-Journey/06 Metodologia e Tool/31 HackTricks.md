---
tipo: entita
tag: [metodologia, tool]
fase: 2
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["HackTricks"]
---

# HackTricks

**HackTricks** = wiki/cheat-sheet online enorme su tecniche di **pentesting, privilege escalation,
enumerazione e post-exploitation**, organizzata per scenario (Linux, Windows/AD, web, cloud, network,
mobile). Sito: https://book.hacktricks.xyz (libro principale) e https://cloud.hacktricks.xyz (cloud).
È la risorsa "guarda qui quando sei bloccato" più citata: ogni pagina ha **comandi pronti** per il
contesto specifico.

> [!warning] Etica
> Comandi e payload di HackTricks vanno usati **solo** in lab/CTF o in ingaggi autorizzati con scope
> firmato. Vedi [[Penetration Testing]].

## Come è strutturata

Navigazione per **scenario** e, dentro, per **porta/servizio** o **tecnica**:

- **Pentesting Methodology** — il flusso generale recon → exploit → privesc.
- **Linux/Windows Privilege Escalation** — checklist passo-passo (SUID, [[sudo]], capabilities, token,
  servizi mal configurati, kernel exploit).
- **Pentesting Network Services** — una pagina per porta: `21-ftp`, `139/445-smb`, `88-kerberos`,
  `3306-mysql`, `5985-winrm`… con enumerazione e attacchi.
- **Active Directory** — catena completa ([[Kerberoasting]], [[AS-REP Roasting]], [[DCSync]], [[BloodHound]]).
- **Web/Pentesting Web** — payload e bypass per le [[OWASP Top 10|vuln OWASP]] (SQLi, SSTI, XXE, file upload…).
- **Cloud** — AWS/GCP/Azure/Kubernetes (su cloud.hacktricks.xyz).

## Workflow operativo

Si usa **insieme** all'enumerazione, non da solo:

1. Trovi un servizio con [[Scansione delle Porte|nmap]] (es. porta 445/SMB su un host).
2. Apri la pagina HackTricks di quella porta → copi i comandi di enumerazione.
3. Se ottieni un foothold, vai alla pagina **PrivEsc** del SO target.

```bash
# Esempio: SMB trovato (porta 445). Comandi tipici dalla pagina HackTricks "139,445 - Pentesting SMB"
enum4linux -a 10.10.10.10
smbclient -L //10.10.10.10/ -N            # lista share senza credenziali
crackmapexec smb 10.10.10.10 --shares     # enum share/permessi
nxc smb 10.10.10.10 -u '' -p '' --users   # null session, enum utenti

# Privilege escalation Linux: la pagina rimanda a linpeas (vedi [[PEAS]]) e a [[GTFOBins]]
sudo -l
./linpeas.sh
```

## HackTricks vs ExploitDB

- **HackTricks** = *come* enumerare e sfruttare uno scenario (tecnica + comandi).
- **[[ExploitDB]]** = *quale* exploit/PoC esiste per un prodotto+versione specifico.

Tipicamente: HackTricks ti dice come enumerare → trovi la versione → ExploitDB/`searchsploit` ti dà il PoC.

## Lab

Si applica su qualsiasi box [[TryHackMe]]/[[HackTheBox]]: tienila aperta in un secondo monitor durante
le room *Jr Penetration Tester* e le box HTB Easy/Medium. Ottima da affiancare a *Linux PrivEsc* e
*Windows PrivEsc* (THM).

## Collegamenti

- [[Privilege Escalation Linux]] · [[Privilege Escalation Windows]] · [[PEAS]] · [[GTFOBins]]
- [[Metodologia del Pentest]] · [[Enumerazione]] · [[ExploitDB]] · [[Penetration Testing]]
- [[Active Directory]] · [[OWASP Top 10]] · [[SMB]] · [[Kerberos]]

## Fonti

- HackTricks (libro): https://book.hacktricks.xyz
- HackTricks Cloud: https://cloud.hacktricks.xyz
- Repository GitHub: https://github.com/HackTricks-wiki/hacktricks
