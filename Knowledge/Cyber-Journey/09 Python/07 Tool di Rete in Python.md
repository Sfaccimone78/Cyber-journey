---
tipo: concetto
tag: [tool]
fase: 1
fonti: 1
aggiornato: 2026-06-26
stato: stub
aliases: ["Tool di Rete in Python"]
---

# Tool di Rete in Python

> **Nota etica**: questi tool si usano **solo** su sistemi tuoi o in lab/CTF autorizzati
> (TryHackMe, HackTheBox, pwn.college). Usarli contro terzi è reato.

> [!info] Stub
> Pagina iniziale. Da espandere ingerendo i capitoli di rete di [[Fonte - Black Hat Python]].

Python come **moltiplicatore** quando sul target manca l'arsenale ma c'è l'interprete: si
ricostruiscono al volo i tool di rete essenziali con la sola standard library (`socket`,
`subprocess`, `threading`). Chiude l'area [[09 Python|Python]] dopo [[pwntools Base]].

## Mattoni

- **Netcat replacement** — un client/server TCP con [[Socket e Port Scanner|socket]] che gira
  comandi via `subprocess`, fa upload di file e apre una [[Reverse Shell e Bind Shell|shell]].
  Sostituto di `nc` quando non è installato.
- **Proxy TCP intercettante** — ascolta in locale, inoltra al target e stampa/edita il traffico
  nei due sensi (hex dump). Utile per capire protocolli proprietari e per il [[Man-in-the-Middle (MITM)|MITM]]
  applicativo in lab.
- **Tunnel / port forwarding** — inoltro di porte e tunnel SSH artigianali (con `paramiko`) per
  il [[Port Forwarding]] e il [[Lateral Movement]] quando i tool standard mancano.

## Concetti chiave

- `socket` per TCP/UDP grezzo; `threading` per gestire più connessioni.
- `subprocess.run(..., capture_output=True)` per eseguire comandi e rimandarne l'output.
- Differenza [[Reverse Shell e Bind Shell|bind vs reverse]] applicata al codice del listener.

## Collegamenti

- [[Socket e Port Scanner]] · [[Requests e HTTP]] · [[Automazione Offensiva]] · [[pwntools Base]]
- [[Reverse Shell e Bind Shell]] · [[Port Forwarding]] · [[Man-in-the-Middle (MITM)]]

## Fonti

- [[Fonte - Black Hat Python]]
