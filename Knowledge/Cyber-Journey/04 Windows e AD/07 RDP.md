---
tipo: entita
tag: [windows]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["RDP"]

---

# RDP

> Nota etica: gli attacchi RDP sono spiegati a scopo difensivo. Usare solo in ambienti lab autorizzati.

## Cos'è

RDP (Remote Desktop Protocol) è il protocollo Microsoft per il controllo remoto grafico di un computer Windows. Gira sulla porta **3389/TCP** (e opzionalmente UDP). Permette di vedere e interagire con il desktop del sistema remoto come se si fosse fisicamente presenti. È ampiamente usato per amministrazione remota ma è anche uno dei vettori di attacco più sfruttati: esposto su internet è spesso bersaglio di brute-force, spraying di credenziali e vulnerabilità critiche come **BlueKeep** (CVE-2019-0708).

## Uso tipico

```bash
# Connettersi con credenziali da Linux (con xfreerdp)
xfreerdp /u:Administrator /p:Password123 /v:192.168.1.10 /cert-ignore

# Connettersi passando l'hash NTLM (Pass-the-Hash via RDP con Restricted Admin Mode)
xfreerdp /u:Administrator /pth:8846f7eaee8fb117ad06bdd830b7586c /v:192.168.1.10

# Da Windows con mstsc
mstsc /v:192.168.1.10

# Scansione di host con RDP aperto
nmap -p 3389 --open 192.168.1.0/24
```

Con [[CrackMapExec]] per verificare credenziali RDP:
```bash
crackmapexec rdp 192.168.1.10 -u utenti.txt -p password.txt
```

## Quando si usa

- **Amministrazione legittima**: gestione remota di server e workstation Windows
- **Accesso iniziale (attacco)**: brute-force su porta 3389 esposta su internet, o credential stuffing
- **Movimento laterale**: dopo aver ottenuto credenziali valide, l'attaccante si sposta lateralmente aprendo sessioni RDP
- **Pass-the-Hash**: con Restricted Admin Mode abilitato, è possibile autenticarsi passando solo l'hash

## Note e trucchi

- Abilitare **Network Level Authentication (NLA)**: l'autenticazione avviene prima che la sessione grafica venga stabilita, riducendo la superficie di attacco.
- **Restricted Admin Mode**: disabilita il caching delle credenziali in memoria durante la sessione RDP (utile contro Pass-the-Hash), ma paradossalmente permette anche il PtH per connettersi.
- Event ID **4624** (Logon Type 10 = RemoteInteractive) nel [[Windows Event Log]] registra ogni accesso RDP.
- Cambiare la porta da 3389 non è sicurezza reale (security by obscurity): usare invece VPN o jump host.
- Tenere aggiornato Windows: BlueKeep e DejaBlue sono vulnerabilità critiche RDP senza autenticazione.

## Collegamenti

- [[Pass-the-Hash]]
- [[CrackMapExec]]
- [[Windows Event Log]]
- [[Active Directory]]
- [[Privilege Escalation Windows]]

## Fonti

- Microsoft Learn — Remote Desktop Protocol: https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/understanding-remote-desktop-protocol
- MITRE ATT&CK T1021.001 — Remote Services: Remote Desktop Protocol: https://attack.mitre.org/techniques/T1021/001/
- HackTricks — RDP Pentesting: https://book.hacktricks.xyz/network-services-pentesting/pentesting-rdp
