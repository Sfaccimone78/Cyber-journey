---
tipo: concetto
tag: [reti]
fase: 1
fonti: 4
aggiornato: 2026-06-22
stato: maturo
aliases: ["VPN"]
---

# VPN

## In breve
Una **VPN** (Virtual Private Network) crea un **tunnel cifrato** tra due endpoint su una rete non fidata (Internet), garantendo **riservatezza** e **integrità** del traffico e facendo apparire i due lati come sulla stessa rete privata. Due usi distinti: **remote-access** (utente → rete aziendale) e **site-to-site** (sede ↔ sede). In pentest la VPN è sia un mezzo difensivo sia una **superficie d'attacco** (i concentratori VPN sono bersagli con CVE critiche) e uno strumento offensivo (pivot e anonimato parziale).

---

## Come funziona un tunnel VPN

```
Senza VPN:
  Tu → ISP → Internet → Server    (ISP/MITM vedono sorgente, destinazione e contenuto)

Con VPN (full tunnel):
  Tu → [ pacchetto originale incapsulato + cifrato ] → Gateway VPN → Internet → Server
         ↑ ISP vede solo "ti colleghi al gateway VPN su UDP/443"

Encapsulation:
  [ Ethernet | IP esterno | UDP/1194 | cifratura | IP interno | TCP | dati reali ]
```

Il meccanismo base è sempre lo stesso:
1. Negoziazione del canale di controllo (auth + scambio chiavi).
2. Derivazione delle chiavi simmetriche di sessione.
3. Incapsulamento dei pacchetti originali (IP-in-IP, tun/tap) dentro il tunnel cifrato.
4. Decapsulamento e inoltro all'altra estremità.

---

## Remote-access vs site-to-site
| Tipo | Chi si connette | Durata | Esempio |
|---|---|---|---|
| **Remote-access** | un client → gateway VPN | on-demand | smart working, lab TryHackMe/HTB (OpenVPN) |
| **Site-to-site** | gateway ↔ gateway tra reti | sempre attivo | filiale ↔ HQ, cloud hybrid |

---

## Protocolli a confronto
| Protocollo | Transport | Cifratura | Forward Secrecy | Note |
|---|---|---|---|---|
| **WireGuard** | UDP 51820 | ChaCha20-Poly1305, Curve25519, BLAKE2s | sì | ~4000 righe di codice, velocissimo, cripto fissa (no downgrade); relativa novità (2019) |
| **OpenVPN** | UDP/1194 o TCP/443 | TLS (OpenSSL) — configurabile | sì (con ECDHE) | maturo, flessibile; TCP/443 mimetizza il traffico come HTTPS |
| **IPsec/IKEv2** | UDP 500/4500 | AES-GCM, vari | sì | standard industriale, ottimo su mobile (MOBIKE per roaming); due fasi IKE |
| **L2TP/IPsec** | UDP 1701 + 500 | IPsec come sopra | parziale | obsolescente; L2TP da solo non cifra, dipende da IPsec |
| **PPTP** | TCP 1723 | MPPE (RC4) | no | **non usare**: rotto crittograficamente (MS-CHAPv2 broken) |

### IPsec/IKEv2 in dettaglio

IPsec opera in due modalità:
- **Transport mode**: cifra solo il payload IP (payload-to-payload).
- **Tunnel mode**: cifra l'intero pacchetto IP originale (usato nelle VPN).

IKE (Internet Key Exchange) ha due fasi:
1. **IKE Phase 1** (Main Mode / Aggressive Mode): autenticazione tra i peer e negoziazione di un canale sicuro (ISAKMP SA).
2. **IKE Phase 2** (Quick Mode): negoziazione dei parametri per il traffico dati (IPsec SA: AH e/o ESP).

NAT-T (NAT Traversal): incapsula ESP dentro UDP/4500 per attraversare il [[NAT]] (ESP non ha porte TCP/UDP → i NAT non sanno come gestirlo).

---

## Split tunnel vs full tunnel
| | Full Tunnel | Split Tunnel |
|---|---|---|
| Traffico che passa dal gateway | Tutto | Solo verso reti interne |
| Traffico Internet diretto | No (passa dalla VPN) | Sì (va diretto all'ISP) |
| Sicurezza / visibilità | Maggiore (azienda vede tutto) | Minore (comportamenti Internet privati) |
| Performance | Più carico sul gateway | Migliore per l'utente |
| Rischio | Nessun traffico "sfugge" | DNS leak, traffico malevolo non filtrato |

---

## Esempio pratico — lab HTB/THM
```bash
# Connetti alla VPN del lab (OpenVPN)
sudo openvpn --config lab.ovpn

# Controlla l'interfaccia tun0 e le rotte
ip addr show tun0
ip route

# Verifica che stai uscendo dal gateway VPN
curl ifconfig.me

# WireGuard
sudo wg-quick up wg0
sudo wg show            # stato tunnel, peer, handshake
sudo wg-quick down wg0

# Controllare leak DNS
cat /etc/resolv.conf    # deve puntare al DNS interno, non all'ISP
```

---

## VPN lato offensivo (uso in pentest)

### Pivot attraverso la VPN
Un client VPN compromesso (o credenziali VPN rubate) dà accesso diretto alla rete interna:
```
Attaccante → VPN aziendale (credenziali rubate) → rete interna → target
```
- Da lì: [[Lateral Movement]], [[Enumerazione]] della rete interna, accesso a servizi interni non esposti su Internet.
- Tecnica comune in attacchi APT: compromettere un laptop di un dipendente in smart working.

### VPN come proxy per anonimato (con limiti)
```bash
# Verifica IP uscita attraverso la VPN
curl ifconfig.me

# Proxychains su SOCKS5 (alternativa a VPN completa per pivoting)
proxychains nmap -sT -p 80,443 192.168.1.0/24
```

**Limiti dell'anonimato**:
- Il provider VPN vede *tutto* il tuo traffico → fiducia spostata, non eliminata.
- Un VPN provider no-log **non è verificabile** senza audit indipendenti.
- Correlazione temporale: se entri alle 14:00 e una connessione malevola parte alle 14:01 dall'exit node VPN, è correlabile.

### Concentratori VPN come bersaglio
I gateway VPN esposti su Internet hanno avuto CVE catastrofiche:
- **Fortinet FortiGate**: CVE-2018-13379 (path traversal → credenziali), CVE-2022-40684 (auth bypass RCE).
- **Pulse Secure**: CVE-2019-11510 (RCE pre-auth), sfruttata massivamente da APT.
- **Citrix ADC/Gateway**: CVE-2019-19781 (RCE), CVE-2023-3519 (RCE non autenticato).
- **Palo Alto GlobalProtect**: CVE-2024-3400 (RCE pre-auth, CVSS 10.0).

Patching del concentratore VPN è **priorità massima** — è esposto su Internet per definizione.

---

## Leak che rompono l'anonimato

| Tipo di leak | Meccanismo | Verifica | Difesa |
|---|---|---|---|
| **DNS leak** | Le query DNS escono fuori dal tunnel (all'ISP) | dnsleaktest.com | Configura DNS server interno nel profilo VPN |
| **WebRTC leak** | Il browser espone l'IP reale via WebRTC (peer-to-peer) | browserleaks.com/webrtc | Disabilita WebRTC in browser o usa estensione |
| **Kill switch assente** | Se il tunnel cade, il traffico esce in chiaro sull'ISP | Simula disconnessione VPN | `iptables` drop tutto il non-VPN; opzione integrata in WireGuard e OpenVPN |
| **IPv6 leak** | VPN gestisce solo IPv4; traffico IPv6 esce non cifrato | ipv6leak.com | Disabilita IPv6 o configura la VPN per gestirlo |

Verifica con [[Wireshark]] su tun0 e sull'interfaccia fisica in parallelo.

---

## Kill switch con iptables
```bash
# Blocca TUTTO il traffico tranne verso il gateway VPN e l'interfaccia tun0
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

# Permetti loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Permetti connessione al gateway VPN (es. UDP 1194)
iptables -A OUTPUT -d <VPN_SERVER_IP> -p udp --dport 1194 -j ACCEPT
iptables -A INPUT  -s <VPN_SERVER_IP> -p udp --sport 1194 -j ACCEPT

# Permetti tutto il traffico su tun0 (dentro il tunnel)
iptables -A INPUT  -i tun0 -j ACCEPT
iptables -A OUTPUT -o tun0 -j ACCEPT
```

In WireGuard il kill switch è configurabile nel peer con `PostUp`/`PreDown` o con `AllowedIPs = 0.0.0.0/0, ::/0`.

---

## VPN per il difensore
- **Zero Trust vs VPN**: il paradigma Zero Trust (ZTNA) supera la VPN tradizionale: anche all'interno del tunnel ogni richiesta è autenticata e autorizzata per risorsa specifica, non "chi è dentro la VPN può fare tutto". La VPN legacy concede fiducia implicita alla rete interna.
- **MFA sul concentratore**: protezione base contro credential stuffing (TOTP, hardware token).
- **Logging e anomaly detection**: orari di accesso insoliti, volume di dati insolito, accesso da geolocation impossibili → alerte nel [[SIEM]].
- **Split tunnel controllato**: anche in split tunnel, forzare il traffico DNS attraverso il gateway per avere visibilità.
- **Segmentazione post-VPN**: la VPN dà accesso alla rete interna, non a tutto. Firewall interni e VLAN separano i segmenti → anche se un attaccante entra via VPN, si muove in una zona limitata.

---

## Troubleshooting
| Sintomo | Causa probabile | Fix |
|---|---|---|
| `tun0` non appare | openvpn non in esecuzione o permessi | `sudo openvpn --config ...` o `sudo wg-quick up wg0` |
| Traffico non passa per il tunnel | rotte mancanti | `ip route add <rete_interna> via <gateway_tun>` |
| DNS leak rilevato | `/etc/resolv.conf` punta all'ISP | Aggiungi `dhcp-option DNS <IP_interno>` nel profilo ovpn |
| VPN connessa ma nessun accesso a internet | full tunnel senza gateway default del tunnel | Controlla `redirect-gateway def1` in ovpn |
| IKEv2 si disconnette al cambio rete | NAT-T non configurato o UDP bloccato | Abilita NAT-T; verifica UDP 500/4500 aperti |
| WireGuard: `handshake did not complete` | chiave pubblica peer errata o firewall UDP 51820 | Ricontrolla `[Peer] PublicKey` e `AllowedIPs` |

---

## Domande da esame / colloquio
1. **Differenza tra full tunnel e split tunnel?** Full: tutto il traffico passa dal gateway VPN (più sicuro e controllato, più carico). Split: solo il traffico verso la rete interna entra nel tunnel, il resto va diretto (performante, ma riduce visibilità e può causare DNS leak).
2. **Perché IPsec usa NAT-T?** Il protocollo ESP non ha porte TCP/UDP → i dispositivi NAT non sanno come gestire i pacchetti ESP (non riescono a tracciare la connessione nella tabella NAT). NAT-T incapsula ESP dentro UDP/4500 rendendo i pacchetti trattabili dai NAT.
3. **VPN = anonimato?** No. La fiducia si sposta dall'ISP al provider VPN. Il provider vede tutto il traffico. DNS leak, WebRTC leak, e assenza di kill switch possono esporre l'IP reale. Correlazione temporale può de-anonimizzare.
4. **Perché i concentratori VPN sono bersagli prioritari?** Sono esposti su Internet per definizione, gestiscono l'accesso all'intera rete interna, e le CVE su di essi (Fortinet, Pulse, Citrix) hanno CVSS altissimi con exploit pubblici. Comprometterli equivale a entrare in rete senza bussare.
5. **WireGuard vs OpenVPN: quando preferiresti uno o l'altro?** WireGuard: performance, semplicità, codice ridotto (superficie d'attacco minima), cripto moderna fissa. OpenVPN: flessibilità (configurabile su TCP/443 per bypassare firewall), ecosistema maturo, compatibilità con concentratori enterprise. WireGuard in scenari moderni; OpenVPN per compatibilità/enterprise.
6. **Come rileveresti un client VPN compromesso usato per pivoting?** Orari anomali, geolocation impossibile (VPN connessa da due paesi in parallelo), volume di traffico insolito, accesso a risorse insolite per quel ruolo → correlazione nel SIEM con IOC.

---

## Collegamenti
- [[NAT]] — NAT-T per IPsec · [[Crittografia Simmetrica]] · [[TLS e SSL]] — base di OpenVPN
- [[Scambio di Chiavi Diffie-Hellman]] — base del key exchange VPN
- [[Man-in-the-Middle (MITM)]] · [[Lateral Movement]] — pivot post-accesso
- [[Wireshark]] — verifica leak e traffico tunnel
- [[Port Forwarding]] · [[Pivoting]] — alternative VPN per pivoting
- [[SIEM]] — correlazione log VPN
- [[MITRE ATT&CK]] — T1133 External Remote Services, T1572 Protocol Tunneling

## Fonti
- Cloudflare — What is a VPN: https://www.cloudflare.com/learning/access-management/what-is-a-vpn/
- WireGuard — whitepaper: https://www.wireguard.com/papers/wireguard.pdf
- RFC 7296 — IKEv2: https://www.rfc-editor.org/rfc/rfc7296
- CISA — Vulnerabilità VPN: https://www.cisa.gov/news-events/cybersecurity-advisories
