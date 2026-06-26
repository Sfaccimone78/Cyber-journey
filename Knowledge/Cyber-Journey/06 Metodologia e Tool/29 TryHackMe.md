---
tipo: entita
tag: [metodologia, tool]
fase: 1
fonti: 2
aggiornato: 2026-06-26
stato: maturo
aliases: ["TryHackMe"]
---

# TryHackMe

**TryHackMe** (THM) = piattaforma online per imparare cybersecurity in modo **pratico e guidato**,
con **room** tematiche che alternano teoria, dimostrazioni e domande a risposta (flag). I lab girano
in VM raggiungibili via [[VPN]] OpenVPN o tramite la **AttackBox** ([[Kali Linux]] in-browser, nessuna
installazione). Sito: https://tryhackme.com. È la rampa d'ingresso più dolce, ideale prima di
[[HackTheBox]].

> [!warning] Etica
> Le tecniche offensive imparate qui vanno usate **solo** dentro le room/scope della piattaforma o
> su sistemi tuoi. Vedi [[Penetration Testing]].

## Come è organizzata

| Elemento | Cosa è |
|----------|--------|
| **Room** | Modulo singolo su un tema (es. *Nmap*, *OWASP Top 10*). Free o Premium. |
| **Learning Path** | Sequenza curata di room verso un obiettivo (es. *Jr Penetration Tester*). |
| **Module** | Gruppo di room dentro un path. |
| **AttackBox** | Kali in-browser (tempo limitato nel piano free, illimitato in Premium). |
| **VPN** | Per attaccare le VM dalla tua Kali locale: scarichi il `.ovpn` e ti connetti. |

```bash
# Connettersi alla rete THM dalla propria Kali
sudo openvpn ~/Downloads/username.ovpn
# Verifica IP tun0 e raggiungibilità della target
ip a show tun0
ping 10.10.x.x
```

## Percorsi consigliati (per fase)

- **Fase 1 — basi**: *Pre Security*, *Complete Beginner*, *Introduction to Cyber Security*.
- **Fase 2 — offensivo**: *Jr Penetration Tester* (Nmap, Metasploit, web, privesc), *Offensive Pentesting*.
- **Fase 3 — difensivo**: *Cyber Defense*, *SOC Level 1* ([[SIEM]], [[Zeek]]/[[Suricata]], threat intel).
- **Room singole molto citate**: *Vulnversity*, *Basic Pentesting*, *Blue* (EternalBlue), *RootMe*,
  *Linux PrivEsc*, *Kenobi*, *OWASP Top 10*.

## Copertura

Copre tutto il tronco del piano: [[Reti|reti]], [[Privilege Escalation Linux|Linux]],
[[OWASP Top 10|web]], [[Active Directory|AD]], [[SIEM|blue team]], [[OSINT]], DFIR. Molte room
mappano esplicitamente le tecniche [[MITRE ATT&CK]].

## THM vs HackTheBox

| | TryHackMe | [[HackTheBox]] |
|---|-----------|-----------|
| Stile | Guidato, teoria + domande | Sfida, poco hand-holding |
| Curva | Dolce, per principianti | Più ripida |
| Forte su | Apprendimento strutturato | Enumerazione realistica, CTF |

## Lab

THM **è** la piattaforma di lab. Suggerito iniziare da *Pre Security* → *Jr Penetration Tester*,
poi consolidare su [[HackTheBox]] *Starting Point*.

## Collegamenti

- [[HackTheBox]] · [[Metodologia del Pentest]] · [[Penetration Testing]] · [[Kali Linux]]
- [[Certificazioni Cybersecurity]] · [[Percorsi di Carriera Pentester vs SOC]] · [[Metodologia CTF]]

## Fonti

- TryHackMe: https://tryhackme.com
- TryHackMe — Learning Paths: https://tryhackme.com/paths
