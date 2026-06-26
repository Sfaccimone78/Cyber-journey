---
tipo: entita
tag: [metodologia, tool]
fase: 2
fonti: 2
aggiornato: 2026-06-26
stato: maturo
aliases: ["HackTheBox", "HTB"]
---

# HackTheBox

**HackTheBox** (HTB) = piattaforma di hacking pratico orientata alla **sfida**: macchine vulnerabili
da compromettere end-to-end (foothold → [[Privilege Escalation Linux|privesc]] → root) con molto meno
hand-holding di [[TryHackMe]]. Allena l'enumerazione paziente e la metodologia reale. Sito:
https://hackthebox.com. Si gioca da [[Kali Linux]] connesso in [[VPN]].

> [!warning] Etica
> Attacca **solo** le macchine della piattaforma nello scope assegnato, e **non pubblicare writeup
> di box *active*** (regola HTB). Tutto fuori scope è illegale. Vedi [[Penetration Testing]].

## Componenti

| Componente | Cosa è |
|------------|--------|
| **Machines** | Box completi (active = a punti, retired = con writeup, richiedono VIP). Difficoltà Easy→Insane. |
| **Challenges** | Sfide atomiche: Web, Crypto, Reversing, Pwn, Forensics, OSINT, Hardware. |
| **Starting Point** | Percorso guidato per i primi passi (consigliato a chi arriva da THM). |
| **Pro Labs** | Ambienti enterprise multi-host (es. *Dante*, *Offshore* AD) per scenari realistici. |
| **HTB Academy** | Percorsi teorici modulari a punti *cubes*, con esami (es. **CPTS**, **CBBH**). |
| **Seasons** | Box competitivi a tema con classifica e badge. |

```bash
# 1. Connessione VPN
sudo openvpn ~/Downloads/lab_user.ovpn

# 2. Enumerazione iniziale di una box (IP dalla dashboard)
nmap -sC -sV -oA nmap/initial 10.10.10.10
# 3. Aggiungere l'hostname a /etc/hosts se la box usa virtual hosting
echo "10.10.10.10 box.htb" | sudo tee -a /etc/hosts
```

## Workflow tipico su una box

1. **Recon/Scan** — `nmap` completo, identificazione servizi e versioni ([[Scansione delle Porte]]).
2. **Enumerazione** — web (gobuster/ffuf), [[SMB]], DNS, servizi specifici ([[Enumerazione]]).
3. **Foothold** — exploit pubblico ([[ExploitDB]]/[[HackTricks]]) o misconfig → shell utente (user flag).
4. **Privilege Escalation** — [[PEAS|linpeas/winpeas]], [[GTFOBins]], kernel/servizi → root flag.
5. **Note** — documentare comandi e percorso (utile per OSCP/CPTS report).

Molte box mappano tecniche [[MITRE ATT&CK]]; le box AD allenano [[Kerberoasting]], [[BloodHound]], [[DCSync]].

## HTB vs TryHackMe

[[TryHackMe]] è guidato e didattico, ottimo per **imparare**; HTB è una palestra di **applicazione**
con enumerazione realistica. Percorso consigliato: THM *Jr Penetration Tester* → HTB *Starting Point*
→ box retired Easy/Medium → HTB Academy *CPTS* / preparazione **OSCP**.

## Lab

- **Starting Point** (tier 0-2): *Meow*, *Dancing*, *Appointment*, *Sequel*, *Crocodile*, *Responder*.
- **Box retired classici per imparare**: *Lame*, *Legacy*, *Blue*, *Jerry*, *Bashed*, *Netmon*, *Forest* (AD).
- **HTB Academy** — percorso *Penetration Tester* (esame CPTS), *Bug Bounty Hunter* (CBBH).

## Collegamenti

- [[TryHackMe]] · [[Metodologia del Pentest]] · [[Penetration Testing]] · [[Metodologia CTF]] · [[Kali Linux]]
- [[ExploitDB]] · [[HackTricks]] · [[PEAS]] · [[GTFOBins]] · [[Certificazioni Cybersecurity]] · [[MITRE ATT&CK]]

## Fonti

- HackTheBox: https://www.hackthebox.com
- HTB Academy: https://academy.hackthebox.com
