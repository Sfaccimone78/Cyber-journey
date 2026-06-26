---
tipo: entita
tag: [windows]
fase: 2
fonti: 4
aggiornato: 2026-06-20
stato: maturo
aliases: ["SMB"]

---

# SMB

> Nota etica: le tecniche di sfruttamento di SMB sono spiegate a scopo difensivo. Usare solo in ambienti lab autorizzati.

## Cos'è

SMB (Server Message Block) è un protocollo di rete Windows per la condivisione di file, stampanti e risorse tra computer. Funziona sulla porta **445/TCP** (e storicamente sulla 139/TCP via NetBIOS). È il protocollo alla base delle share di rete Windows (`\\server\condivisione`) e dell'autenticazione NTLM/Kerberos in Active Directory.

È stato al centro di attacchi devastanti come **EternalBlue** (CVE-2017-0144, usato da WannaCry) e rimane un vettore primario per [[Pass-the-Hash]] e movimento laterale.

## Uso tipico

```bash
# Enumerare share SMB con credenziali (da Linux, con smbclient)
smbclient -L //192.168.1.10 -U 'DOMINIO\utente%password'

# Connettersi a una share specifica
smbclient //192.168.1.10/C$ -U 'DOMINIO\Administrator%Password123'

# Enumerare share con enum4linux
enum4linux -a 192.168.1.10

# Enumerare con CrackMapExec
crackmapexec smb 192.168.1.0/24 --shares -u utente -p password

# Montare share SMB su Linux
mount -t cifs //192.168.1.10/share /mnt/smb -o username=utente,password=pass
```

Versioni SMB e sicurezza:
- **SMBv1**: obsoleto e pericoloso (disabilitare sempre — EternalBlue lo sfrutta)
- **SMBv2/v3**: supporta firma digitale e cifratura; da preferire

## Quando si usa

- **Enumerazione**: trovare share accessibili, elencare utenti/policy con [[enum4linux]]
- **Movimento laterale**: accesso a share amministrative (`C$`, `ADMIN$`, `IPC$`) con [[Pass-the-Hash]]
- **Esecuzione remota**: tool come [[CrackMapExec]] e [[Impacket]] usano SMB per eseguire comandi

## Note e trucchi

- Le share `C$` e `ADMIN$` sono hidden shares amministrative presenti su ogni Windows; la `IPC$` serve per la comunicazione tra processi (usata da tool di enum).
- SMB Signing disabilitato consente attacchi di tipo **NTLM Relay** (un attaccante intercetta l'autenticazione e la redirige).
- Controllare se SMBv1 è attivo: `Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol`.
- Porta 445 non deve mai essere esposta direttamente su internet.

## Collegamenti

- [[Pass-the-Hash]]
- [[enum4linux]]
- [[CrackMapExec]]
- [[Impacket]]
- [[Active Directory]]
- [[Porte e Protocolli Comuni]]

## Fonti

- Microsoft Learn — SMB Overview: https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3
- MITRE ATT&CK T1021.002 — Remote Services: SMB/Windows Admin Shares: https://attack.mitre.org/techniques/T1021/002/
- HackTricks — SMB: https://book.hacktricks.xyz/network-services-pentesting/pentesting-smb
- TryHackMe — Network Services (SMB): https://tryhackme.com/room/networkservices
