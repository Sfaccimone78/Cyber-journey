---
tipo: entita
tag: [blue-team, tool]
fase: 3
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["Suricata"]
---

# Suricata

**Suricata** = motore open-source **IDS/IPS** (e NSM) ad alte prestazioni, sviluppato da OISF.
Ispeziona il traffico e genera un **alert** quando un pacchetto/flusso combacia con una **regola**
(firma). Multi-thread, supporta accelerazione hardware e l'output strutturato **EVE JSON**.

| Modalità | Comportamento |
|----------|---------------|
| **IDS** | Solo rilevamento e alert (passivo, su SPAN/TAP). |
| **IPS** | Inline (NFQUEUE/AF_PACKET), può **droppare** il traffico malevolo. |
| **NSM** | Genera anche log di protocollo (HTTP, TLS, DNS) e fa estrazione file, come [[Zeek]]. |

## Anatomia di una regola

Le regole hanno la sintassi stile Snort: **action**, **header** (protocollo, IP/porte, direzione) e
**options** tra parentesi.

```text
action  proto  src_ip src_port -> dst_ip dst_port  (options)
```

```suricata
# Regola di esempio: rileva una richiesta HTTP con uno user-agent noto-malevolo
alert http $HOME_NET any -> $EXTERNAL_NET any ( \
    msg:"ET MALWARE Sospetto User-Agent C2"; \
    flow:established,to_server; \
    http.user_agent; content:"EvilBot/1.0"; \
    classtype:trojan-activity; \
    reference:url,attack.mitre.org/techniques/T1071/; \
    sid:1000001; rev:1; )
```

Campi chiave: `msg` (descrizione nell'alert), `content` (pattern da cercare, anche `|` hex `|`),
`flow` (stato/direzione), `sid` (id univoco — i custom partono da 1000000), `rev` (versione),
`classtype` e `reference` (spesso a una tecnica [[MITRE ATT&CK]]). I keyword `http.*`, `tls.sni`,
`dns.query` permettono il match a livello applicativo.

## Esempio pratico

```bash
# Test della sintassi delle regole senza avviare il motore
sudo suricata -T -c /etc/suricata/suricata.yaml -v

# Analisi offline di una cattura con un set di regole
sudo suricata -r capture.pcap -S local.rules -l ./output/

# Sniffing live su un'interfaccia (IDS)
sudo suricata -i eth0 -c /etc/suricata/suricata.yaml

# Aggiornare i feed di regole (Emerging Threats, ecc.) con suricata-update
sudo suricata-update

# Gli alert finiscono in eve.json: filtrarli con jq
cat output/eve.json | jq 'select(.event_type=="alert") | {sig:.alert.signature, src:.src_ip, dst:.dest_ip}'
```

**Feed di regole** comuni: **Emerging Threats Open** (gratuito), **ET Pro** e **Talos/Snort**
(a pagamento). L'output `eve.json` si invia tipicamente a un [[SIEM]] (Elastic/Splunk) per correlazione.

## Suricata vs Zeek

Suricata = **detection a firme** (riconosce ciò che è *già noto-cattivo*, e può bloccarlo inline).
[[Zeek]] = **visibilità/log** per hunting su comportamento. Sono complementari: Suricata risponde
"è passato qualcosa di malevolo noto?", Zeek "cosa è successo in generale?". Lo stack **Security
Onion** li integra entrambi. Vedi tabella di confronto in [[Zeek]].

## Lab

- **TryHackMe**: *Snort*, *Snort Challenge - The Basics*, *Snort Challenge - Live Attacks* (le regole
  Snort sono quasi identiche a quelle Suricata), percorso *SOC Level 1*.
- **Security Onion** — pratica Suricata + Zeek + Elastic su PCAP reali.
- **Malware-Traffic-Analysis.net** — esercizi: scrivi una regola che fanghi il C2 nel PCAP.

## Collegamenti

- [[Zeek]] · [[Wireshark]] · [[SIEM]] · [[Detection di Attacchi]] · [[Regole Sigma]]
- [[MITRE ATT&CK]] · [[Indicatori di Compromissione (IOC)]] · [[Threat Hunting]] · [[Log Analysis]]

## Fonti

- Documentazione ufficiale Suricata: https://docs.suricata.io
- Suricata Rules — formato: https://docs.suricata.io/en/latest/rules/intro.html
- Emerging Threats Open ruleset: https://rules.emergingthreats.net
