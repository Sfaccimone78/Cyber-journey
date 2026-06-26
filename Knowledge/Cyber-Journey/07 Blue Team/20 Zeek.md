---
tipo: entita
tag: [blue-team, tool]
fase: 3
fonti: 3
aggiornato: 2026-06-26
stato: maturo
aliases: ["Zeek"]
---

# Zeek

**Zeek** (ex *Bro*) = framework open-source di **Network Security Monitoring** (NSM). Non è un IDS a
firme: osserva il traffico e produce **log strutturati ad alto livello** (connessioni, DNS, HTTP,
TLS, file trasferiti), su cui poi si fa detection, correlazione e [[Threat Hunting|threat hunting]].
È la "scatola nera" della rete: anche se non scatta nessun alert, hai un registro ricco di ciò che è
successo.

## Architettura e idea chiave

- **Event-driven**: un *event engine* trasforma i pacchetti in eventi semantici
  (`connection_established`, `dns_request`, `http_request`); un *policy script layer* in **linguaggio
  Zeek** reagisce a quegli eventi.
- **Output = decine di log** (uno per protocollo), in TSV o **JSON**, ideali da inviare a un [[SIEM]].
- Forte su **visibilità e contesto**; complementare alle firme di [[Suricata]].

| Log | Contenuto |
|-----|-----------|
| `conn.log` | Ogni connessione: IP/porte, durata, byte, stato. Il log fondamentale. |
| `dns.log` | Query e risposte DNS (utile per C2/DGA, [[Indicatori di Compromissione (IOC)|IOC]]). |
| `http.log` | Richieste HTTP: host, URI, user-agent, status. |
| `ssl.log` | Handshake TLS: SNI, certificati, versione (rileva self-signed/JA3 sospetti). |
| `files.log` | File trasferiti, con hash MD5/SHA1 (incrocia con [[VirusTotal]]). |
| `notice.log` | Avvisi generati dagli script (la cosa più simile a un "alert"). |
| `x509.log`, `smtp.log`, `ftp.log`, `weird.log` | Altri protocolli e anomalie. |

## Esempio pratico

```bash
# Analisi offline di una cattura (genera i log Zeek nella dir corrente)
zeek -r capture.pcap
ls
# conn.log dns.log http.log ssl.log files.log ...

# Sniffing live su un'interfaccia (deployment NSM)
sudo zeek -i eth0

# Interrogare i log con zeek-cut (estrae colonne dal formato TSV)
cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p proto service duration
# Top destinazioni per byte trasferiti
cat conn.log | zeek-cut id.resp_h orig_bytes | sort | uniq -c | sort -rn | head
```

### Script Zeek di detection

Si estende Zeek con script `.zeek`. Esempio: segnalare connessioni verso una porta sospetta.

```zeek
# detect-telnet.zeek — alza un notice su traffico Telnet (porta 23) in chiaro
@load base/protocols/conn

redef enum Notice::Type += { Telnet_Detected };

event connection_established(c: connection)
    {
    if ( c$id$resp_p == 23/tcp )
        NOTICE([$note=Telnet_Detected,
                $conn=c,
                $msg=fmt("Connessione Telnet in chiaro verso %s", c$id$resp_h)]);
    }
```

Zeek ships con framework utili: **Intelligence Framework** (incrocia il traffico con feed di IOC),
**File Analysis**, **SumStats**. Distribuzione gestita su larga scala con **ZeekControl**.

## Zeek vs Suricata

| | Zeek | [[Suricata]] |
|---|------|----------|
| Modello | Behavioral / log-centric (NSM) | Signature-based IDS/IPS |
| Output | Log ricchi per hunting | Alert su match di regole |
| Domanda a cui risponde | "Cosa è successo sulla rete?" | "È passato qualcosa di noto-cattivo?" |
| Uso tipico | Visibilità, threat hunting, forensics | Detection/blocco di minacce note |

Spesso si usano **insieme** (es. nello stack **Security Onion**), inviando entrambi a un [[SIEM]].

## Lab

- **TryHackMe**: *Zeek*, *Zeek Exercises*, *Snort* (per confronto), percorso *SOC Level 1* (Network
  Security & Traffic Analysis).
- **Security Onion** — distro NSM che integra Zeek + Suricata + Elastic; ottima per esercitarsi.
- **Malware-Traffic-Analysis.net** — PCAP reali su cui far girare `zeek -r`.

## Collegamenti

- [[Suricata]] · [[Wireshark]] · [[SIEM]] · [[Log Analysis]] · [[Detection di Attacchi]]
- [[Threat Intelligence]] · [[Indicatori di Compromissione (IOC)]] · [[VirusTotal]] · [[Threat Hunting]]

## Fonti

- Documentazione ufficiale Zeek: https://docs.zeek.org
- Zeek log reference: https://docs.zeek.org/en/master/logs/index.html
- Security Onion docs: https://docs.securityonion.net
