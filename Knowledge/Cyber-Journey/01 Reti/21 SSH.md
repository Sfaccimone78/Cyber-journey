---
tipo: entita
tag: [reti, linux]
fase: 1
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["SSH"]
---

# SSH

## Cos'è
**SSH** (Secure Shell, RFC 4251-4254) è il protocollo standard per l'accesso remoto **cifrato** a un sistema, tipicamente Linux/Unix. Gira sulla porta **22/TCP** e sostituisce protocolli in chiaro come Telnet e rlogin. Oltre alla shell remota, fornisce trasferimento file (SCP/SFTP), tunneling e port forwarding. È uno dei primi servizi che si incontrano in [[Enumerazione|enumerazione]] e CTF.

---

## Architettura: tre livelli SSH

SSH è definito da tre protocolli sovrapposti:

| Livello | Protocollo | Scopo |
|---|---|---|
| Trasporto | SSH-TRANS | negoziazione algoritmi, cifratura, integrità, autenticazione **host** |
| Autenticazione | SSH-AUTH | autenticazione **utente** (password, chiave, etc.) |
| Connessione | SSH-CONN | multiplexing di canali logici (shell, SCP, forwarding) |

---

## Handshake SSH passo per passo

```
Client                                  Server
  |--- TCP SYN → porta 22             --->|
  |<-- TCP SYN/ACK                    ---|
  |--- TCP ACK                        --->|
  |                                       |
  |--- SSH version string (SSH-2.0-...) ->|
  |<-- SSH version string             ---|
  |                                       |
  |--- SSH_MSG_KEXINIT (KEX, cipher,  --->|  ← negoziazione algoritmi
  |    MAC, compression supportati)       |
  |<-- SSH_MSG_KEXINIT                ---|
  |                                       |
  |=== Key Exchange (ECDH/DH) ==========>|  ← mai trasmessa la chiave
  |   entrambi derivano la stessa session key
  |                                       |
  |<-- SSH_MSG_NEWKEYS                ---|  ← da qui tutto cifrato
  |--- SSH_MSG_NEWKEYS                --->|
  |                                       |
  |--- SSH_MSG_SERVICE_REQUEST (auth) --->|
  |<-- SSH_MSG_SERVICE_ACCEPT         ---|
  |                                       |
  |--- SSH_MSG_USERAUTH_REQUEST       --->|  ← password o chiave pubblica
  |<-- SSH_MSG_USERAUTH_SUCCESS       ---|
  |                                       |
  |=== canale shell/SCP/port forward ====|
```

---

## Autenticazione host key

Alla **prima connessione**, SSH mostra il fingerprint della chiave pubblica del server:
```
The authenticity of host '10.10.10.5 (10.10.10.5)' can't be established.
ED25519 key fingerprint is SHA256:AAAA...
Are you sure you want to continue connecting (yes/no)?
```

- **Accettando**, la chiave viene salvata in `~/.ssh/known_hosts`.
- Alle connessioni successive, SSH confronta la chiave ricevuta con quella salvata.
- Se **cambia** (server reinstallato, ma anche MITM): `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` → blocca la connessione.
- Accettare alla cieca una host key sconosciuta espone a [[Man-in-the-Middle (MITM)|MITM]].

```bash
# Verificare il fingerprint del server (lato server)
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub

# Rimuovere una vecchia chiave da known_hosts (dopo reinstall legittimo)
ssh-keygen -R 10.10.10.5
```

---

## Autenticazione utente: password vs chiave pubblica

### Password
Il client invia la password **cifrata** nel canale SSH. Semplice ma soggetta a brute force e a keylogger. Disabilitarla in produzione.

### Chiave pubblica (consigliata)
Meccanismo challenge-response asimmetrico:
1. Il server ha la **chiave pubblica** dell'utente in `~/.ssh/authorized_keys`.
2. Il server invia una challenge cifrata con la chiave pubblica.
3. Il client decifra con la **chiave privata** (che non lascia mai il client) e risponde.
4. Nessun segreto viene trasmesso → immune a sniffing.

```bash
# Generare coppia di chiavi (ED25519 = raccomandato nel 2026)
ssh-keygen -t ed25519 -C "commento_identità"

# Oppure RSA 4096 (compatibilità legacy)
ssh-keygen -t rsa -b 4096

# Copiare la chiave pubblica sul server
ssh-copy-id -i ~/.ssh/id_ed25519.pub utente@10.10.10.5

# Manuale: appendi a authorized_keys (se ssh-copy-id non disponibile)
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Connettersi specificando la chiave
ssh -i ~/.ssh/id_ed25519 utente@10.10.10.5
```

### Altre modalità
- **GSSAPI/Kerberos**: per ambienti Active Directory integrati.
- **Certificati SSH**: CA SSH firma le chiavi → niente `authorized_keys` distribuiti manualmente; usato in infrastrutture grandi.

---

## Uso tipico

```bash
# Connessione base
ssh utente@10.10.10.5

# Porta non standard
ssh -p 2222 utente@10.10.10.5

# Eseguire un comando remoto senza aprire una shell interattiva
ssh utente@10.10.10.5 "ls /etc/passwd"

# Trasferimento file (SCP)
scp file.txt utente@10.10.10.5:/tmp/
scp -r /directory/ utente@10.10.10.5:/tmp/dir/

# SFTP interattivo (rimpiazzo sicuro di ftp, NON richiede un server FTP, solo sshd)
sftp utente@10.10.10.5
sftp> get /remote/file ./local/

# rsync su SSH: preferibile per sincronizzazioni (trasferisce solo le differenze)
rsync -avz -e ssh /dir/ utente@10.10.10.5:/backup/

# X11 forwarding: esegui app grafiche remote sul display locale
ssh -X utente@10.10.10.5

# Modalità verbose (debug handshake)
ssh -vvv utente@10.10.10.5
```

---

## File di configurazione client: `~/.ssh/config`

Permette alias e opzioni per host, evitando comandi lunghi e ripetitivi:

```sshconfig
Host prod
    HostName 203.0.113.10
    User alice
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ServerAliveInterval 60
```

Poi basta `ssh prod`. Il server, invece, si configura in `/etc/ssh/sshd_config` (vedi Hardening).

---

## Port Forwarding: i tre tipi

Il port forwarding SSH crea **tunnel TCP** attraverso la connessione SSH cifrata. Fondamentale per il pivoting in post-exploitation.

```bash
# LOCAL (-L): porta locale → servizio interno raggiungibile dal server SSH
# Accede a un servizio interno (es. http su 80) attraverso il server
ssh -L 8080:192.168.1.100:80 utente@10.10.10.5
# → curl http://localhost:8080 raggiunge 192.168.1.100:80 tramite il bastion

# REMOTE (-R): esponi un servizio locale sul server SSH (reverse tunnel)
# Utile per raggiungere una macchina dietro NAT dall'esterno
ssh -R 9000:127.0.0.1:3000 utente@jump.server.com
# → dal jump server: curl http://localhost:9000 raggiunge il tuo servizio locale :3000

# DYNAMIC (-D): proxy SOCKS su porta locale (tunneling di qualsiasi TCP)
# Tutto il traffico può passare dal server SSH come proxy
ssh -D 1080 utente@10.10.10.5
# → configura il browser o proxychains per usare SOCKS5 su 127.0.0.1:1080

# Opzioni utili per tunnel stabili
ssh -N -f -L 8080:interno:80 utente@bastion   # -N: no shell, -f: background
```

Dettagli e uso offensivo in [[Port Forwarding]] e [[Pivoting]].

---

## ProxyJump e salti a cascata

```bash
# Raggiungi un host interno passando per un bastion (jump host)
ssh -J utente@bastion.com utente@192.168.1.50

# Catena di più hop
ssh -J user@hop1,user@hop2 user@target

# In ~/.ssh/config (equivalente permanente)
Host target-interno
    HostName 192.168.1.50
    User utente
    ProxyJump bastion.com
```

---

## Attacchi su SSH

### 1. Brute Force delle credenziali
Se l'autenticazione a password è attiva, attacchi dizionario sono banali:
```bash
# Hydra
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://10.10.10.5

# Medusa
medusa -h 10.10.10.5 -u admin -P rockyou.txt -M ssh

# Con nomi utente multipli
hydra -L users.txt -P passwords.txt ssh://10.10.10.5 -t 4
```

### 2. Furto di chiave privata
Una chiave privata (`~/.ssh/id_rsa`, `~/.ssh/id_ed25519`) trovata su un host compromesso permette accesso senza credenziali a tutti i server dove quella chiave è in `authorized_keys`. In CTF è uno dei movimenti laterali più comuni.

```bash
# Dopo aver trovato una chiave privata
chmod 600 id_rsa_trovata
ssh -i id_rsa_trovata utente@altro-target

# Se la chiave è protetta da passphrase, crackala
ssh2john id_rsa_trovata > hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

### 3. SSH Agent Hijacking
`ssh-agent` memorizza le chiavi private decifrate in memoria e le mette a disposizione tramite un socket Unix (`$SSH_AUTH_SOCK`). Un attaccante root può elencare e usare tutte le chiavi caricate dall'agente:

```bash
# Elenco delle chiavi caricate nell'agent
SSH_AUTH_SOCK=/tmp/ssh-XXXX/agent.NNN ssh-add -l

# Usare il socket dell'agent di un altro utente (richiede root)
SSH_AUTH_SOCK=/tmp/ssh-target/agent.NNN ssh utente@altro-host
```

**Difesa**: `ssh-add -c` (richiede conferma per ogni uso della chiave); timeout (`ssh-add -t 3600`); non fare forward dell'agente su host non fidati (`ForwardAgent no` in default).

### 4. Weaknesses nelle versioni vecchie
- CVE-2023-38408: agente SSH vulnerabile a RCE via PKCS#11.
- Algoritmi deprecati (DSA, RSA < 2048, MD5 HMAC): verifica con `nmap --script ssh2-enum-algos -p22 target`.

---

## Hardening (`/etc/ssh/sshd_config`)

```bash
# Disabilita login root
PermitRootLogin no

# Disabilita autenticazione a password (solo chiavi)
PasswordAuthentication no
ChallengeResponseAuthentication no

# Specifica gli utenti ammessi
AllowUsers deploy ops

# Timeout connessione inattiva
ClientAliveInterval 300
ClientAliveCountMax 2

# Limita protocollo (SSH2 only è il default, ma meglio esplicitare)
Protocol 2

# Disabilita agent e X11 forwarding se non necessario
AllowAgentForwarding no
X11Forwarding no

# Limita algoritmi (solo sicuri)
KexAlgorithms curve25519-sha256,ecdh-sha2-nistp521
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com

# Porta non standard (oscurity, non sicurezza reale, ma riduce log)
Port 2222

# Reloada dopo le modifiche
sudo systemctl reload sshd
```

> [!tip] Config in drop-in + test prima del reload (best practice 2026)
> Tieni le modifiche in **file separati sotto `/etc/ssh/sshd_config.d/`** (es. `99-hardening.conf`): sopravvivono agli aggiornamenti del pacchetto senza conflitti. **Verifica sempre la sintassi con `sshd -t` prima del reload**, e aggiungi `MaxAuthTries 3` per limitare i tentativi per connessione. Per un audit automatico della configurazione usa **`ssh-audit`** (`ssh-audit target`).

> [!warning] Ordine delle operazioni
> Verifica di poter entrare con la **chiave** (in una seconda sessione) **prima** di impostare `PasswordAuthentication no`, altrimenti rischi di chiuderti fuori dal server.

**Perché Ed25519 e non RSA**: chiavi a 256 bit compatte, generazione/verifica più rapide, implementazione semplice e minore superficie per attacchi side-channel. Ricorri a RSA (≥3072 bit) solo per requisiti di compatibilità legacy.

**fail2ban**: blocca IP dopo N tentativi falliti. Installato separatamente, fondamentale se la password auth è attiva.

```bash
# Stato fail2ban per SSH
sudo fail2ban-client status sshd

# Sblocca un IP
sudo fail2ban-client set sshd unbanip 10.10.10.5
```

---

## SSH per il difensore
- **Audit chiavi autorizzate**: `find / -name authorized_keys 2>/dev/null` — cercare chiavi sconosciute.
- **Log di autenticazione**: `/var/log/auth.log` (Debian/Ubuntu), `/var/log/secure` (RHEL). Cerca `Failed password`, `Invalid user`, `Accepted publickey`.
- **Monitoraggio**: alert su tentativi multipli falliti (brute force) + accessi da IP anomali. Integra con [[SIEM]].
- **Rotazione chiavi**: revocare le chiavi di utenti che lasciano il team → rimuovere da ogni `authorized_keys`.
- **MITRE ATT&CK**: T1021.004 (Remote Services: SSH), T1110.001 (Brute Force), T1552.004 (Private Keys).

---

## Troubleshooting
| Sintomo | Causa probabile | Fix |
|---|---|---|
| `Connection refused` | sshd non in ascolto / firewall | `nmap -p22 target`; controlla `systemctl status sshd` |
| `Permission denied (publickey)` | chiave non in `authorized_keys` o permessi errati | `chmod 700 ~/.ssh; chmod 600 authorized_keys` |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` | chiave host cambiata (reinstall o MITM) | Verifica il fingerprint out-of-band, poi `ssh-keygen -R host` |
| Connessione lenta all'inizio | DNS reverse lookup lento | `UseDNS no` in `sshd_config` |
| `Too many authentication failures` | troppi tentativi con agent con molte chiavi | `ssh -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 ...` |
| Port forwarding non funziona | `GatewayPorts no` (default) | `GatewayPorts yes` per forward su interfacce non-loopback |

---

## Domande da esame / colloquio
1. **Differenza tra autenticazione a password e a chiave pubblica in SSH?** La password è trasmessa (cifrata) al server → vulnerabile a brute force e key-logging lato server. Con la chiave pubblica, la privata non lascia mai il client: il server sfida il client e verifica che risponda correttamente con la chiave privata associata. Zero segreto trasmesso.
2. **Cosa succede se la host key del server cambia?** SSH emette un warning e rifiuta la connessione (se `StrictHostKeyChecking yes`). Indica reinstall legittimo *oppure* MITM in corso. Bisogna verificare il fingerprint out-of-band prima di ri-accettare.
3. **Differenza tra `-L`, `-R`, `-D` in SSH?** `-L local:` → porta locale verso servizio remoto (forward locale). `-R remote:` → porta remota verso servizio locale (reverse/remote forward). `-D porta` → proxy SOCKS dinamico: tutto il traffico rediretto attraverso il server SSH.
4. **Cos'è l'SSH agent hijacking e come si previene?** Root può usare il socket dell'agente di altri utenti (`$SSH_AUTH_SOCK`) per accedere alle chiavi in memoria. Prevenzione: no `ForwardAgent` su host non fidati, `ssh-add -c` per conferma manuale, timeout breve sulle chiavi.
5. **Come hardeni un server SSH in produzione?** `PermitRootLogin no`, `PasswordAuthentication no`, `AllowUsers` lista, timeout di inattività, algoritmi moderni (Ed25519, ChaCha20-Poly1305), fail2ban, porta non standard come deterrente.

---

## Collegamenti
- [[Porte e Protocolli Comuni]] · [[TCP]] · [[Three-Way Handshake TCP]]
- [[Crittografia Asimmetrica]] · [[Scambio di Chiavi Diffie-Hellman]]
- [[Man-in-the-Middle (MITM)]]
- [[Hydra]] — brute force SSH
- [[Lateral Movement]] · [[Port Forwarding]] · [[Pivoting]]
- [[Enumerazione]] · [[Scansione delle Porte]]
- [[Privilege Escalation Linux]] — chiavi SSH trovate in post-exploitation
- [[SIEM]] — correlazione log auth
- [[MITRE ATT&CK]]

## Fonti
- OpenSSH Manual: https://www.openssh.com/manual.html
- HackTricks — Pentesting SSH (port 22): https://book.hacktricks.xyz/network-services-pentesting/pentesting-ssh
- Arch Wiki — SSH keys: https://wiki.archlinux.org/title/SSH_keys
- TLCL — cap. 16 "Networking" (scp/sftp/rsync, tunneling, X11); ssh-audit.com — Hardening Guides; Linuxize — "SSH Hardening Best Practices" (~/.ssh/config, sshd_config.d, Ed25519 — ricerca 2025-2026)
