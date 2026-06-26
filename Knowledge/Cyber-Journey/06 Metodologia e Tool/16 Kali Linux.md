---
tipo: entita
tag: [tool]
fase: 2
fonti: 3
aggiornato: 2026-06-20
stato: maturo
aliases: ["Kali Linux"]

---

# Kali Linux

## Cos'è

**Kali Linux** è una distribuzione Linux basata su Debian, mantenuta da Offensive Security, progettata specificamente per il penetration testing e la sicurezza informatica offensiva. Viene fornita con oltre 600 tool preinstallati per [[Ricognizione (Recon)]], [[Scansione delle Porte]], [[Enumerazione]], [[Exploitation]], [[Post-Exploitation]], analisi forense, cracking di password e wireless security. È lo standard de facto nel settore del pentesting.

> **Nota etica**: Kali Linux è uno strumento professionale. I tool in essa contenuti vanno usati solo su sistemi autorizzati: lab personali, CTF, o pentest con contratto. L'uso su sistemi altrui è illegale.

## Uso tipico

```bash
# Aggiornare il sistema e i tool
sudo apt update && sudo apt upgrade -y

# Installare un tool non presente di default
sudo apt install tool-name

# Trovare tool per categoria con kali-tools
apt search kali-tools-

# Installare un meta-pacchetto (set di tool per categoria)
sudo apt install kali-tools-web          # tool per web application testing
sudo apt install kali-tools-passwords    # tool per password cracking
sudo apt install kali-tools-wireless     # tool per wireless

# Wordlists — percorso principale
ls /usr/share/wordlists/
gunzip /usr/share/wordlists/rockyou.txt.gz   # decomprimere rockyou

# SecLists — raccolta estesa di wordlist
sudo apt install seclists
ls /usr/share/seclists/

# Avviare i servizi di database per Metasploit
sudo systemctl start postgresql
sudo msfdb init

# Verificare la versione di Kali
cat /etc/os-release

# Tool comuni preinstallati e dove trovarli
which nmap gobuster ffuf nikto hydra nc msfconsole
```

**Tool principali inclusi per categoria:**

| Categoria | Tool inclusi |
|---|---|
| Scansione rete | [[Nmap]], masscan, netdiscover |
| Web | [[Gobuster]], [[ffuf]], [[Nikto]], Burp Suite, sqlmap |
| Exploitation | [[Metasploit]], searchsploit (Exploit-DB offline) |
| Password | [[Hydra]], John the Ripper, Hashcat |
| Rete | [[netcat]], Wireshark, tcpdump |
| Post-exploitation | LinPEAS, WinPEAS, enum4linux |
| Forense | Autopsy, Volatility |

## Quando si usa

- Come **sistema operativo principale** o su VM per fare pentest e CTF.
- Su **macchina virtuale** (VirtualBox, VMware) per isolare il lab da rete domestica.
- Come **bootable live USB** per pentest fisici senza lasciare tracce sul sistema host.
- Su **WSL2** (Windows Subsystem for Linux) per avere i tool Kali su Windows.
- Su **cloud** (AWS, DigitalOcean) come attack box remota.

## Note e trucchi

- **Non usare Kali come OS quotidiano**: non è ottimizzata per uso desktop. È pensata per sessioni di testing.
- Il percorso `/usr/share/wordlists/` contiene le wordlist più usate. SecLists (da installare) in `/usr/share/seclists/` è molto più completa.
- `searchsploit termine` permette di cercare exploit nel database Exploit-DB locale, senza connessione internet.
- Il tool **kali-tweaks** (`sudo kali-tweaks`) permette di configurare shell, desktop e installare pacchetti aggiuntivi in modo guidato.
- Versione **Kali NetHunter**: porta Kali su dispositivi Android per test mobile e wireless.
- Per aggiornare solo i tool di sicurezza senza toccare il sistema: `sudo apt upgrade kali-linux-default`.

## Mitigazione e difesa

Non applicabile direttamente — Kali è un tool offensivo. Dal punto di vista difensivo, la presenza di Kali o dei suoi tool su sistemi aziendali non autorizzati è un segnale di allarme da monitorare.

## Collegamenti

- [[Metodologia del Pentest]]
- [[Nmap]]
- [[Metasploit]]
- [[Gobuster]]
- [[ffuf]]
- [[Nikto]]
- [[Hydra]]
- [[netcat]]
- [[Ricognizione (Recon)]]
- [[Filesystem Linux]]

## Fonti

- Kali Linux — documentazione ufficiale: <https://www.kali.org/docs/>
- Kali Tools — lista completa dei tool: <https://www.kali.org/tools/>
- Offensive Security — Kali overview: <https://www.offsec.com/kali-linux/>
