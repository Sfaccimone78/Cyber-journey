---
tipo: entita
tag: [linux, tool, metodologia]
fase: 2
fonti: 0
aggiornato: 2026-06-26
stato: stub
aliases: ["GTFOBins"]
---

# GTFOBins

> [!info] Stub
> Risorsa di riferimento per la privilege escalation Unix. Da espandere.

**GTFOBins** (*Get The F*** Out Binaries*) = catalogo online di **binari Unix legittimi** che possono
essere abusati per bypassare restrizioni e fare [[Privilege Escalation Linux|privilege escalation]].
Sito: https://gtfobins.github.io.

## A cosa serve

Dato un binario (es. `vim`, `find`, `cp`, `tar`, `less`), GTFOBins elenca come sfruttarlo a seconda
del contesto:

- **`sudo`** — se è eseguibile via [[sudo]], spesso si ottiene una shell root (`sudo find . -exec /bin/sh \;`).
- **SUID** — se ha il bit [[SUID e SGID|SUID]], stessa idea con shell che mantiene l'uid privilegiato.
- **Capabilities** — abusi via [[Capabilities Linux]] (es. `cap_setuid`).
- Altri: lettura/scrittura file arbitrari, download, bind/reverse shell.

## Workflow tipico

1. Enumera con [[PEAS|linpeas]] / `sudo -l` / `find / -perm -4000`.
2. Cerca il binario su GTFOBins.
3. Applica la tecnica per la categoria giusta (`sudo`, `suid`, `capabilities`…).

Equivalente Windows-side: LOLBAS. Per editor specifici: [[Vim e Nano]].

## Collegamenti

- [[Privilege Escalation Linux]] · [[SUID e SGID]] · [[sudo]] · [[Capabilities Linux]] · [[PEAS]]
