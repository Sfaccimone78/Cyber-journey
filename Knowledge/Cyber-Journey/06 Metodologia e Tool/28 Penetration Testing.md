---
tipo: concetto
tag: [metodologia]
fase: 1
fonti: 0
aggiornato: 2026-06-26
stato: stub
aliases: ["Penetration Testing"]
---

# Penetration Testing

> [!info] Stub
> Pagina ombrello (cos'è). Per il **come** operativo segui [[Metodologia del Pentest]] e le fasi
> numerate dell'area [[06 — Mappa Metodologia e Tool|Metodologia e Tool]].

**Penetration Testing** (pentest) = simulazione **autorizzata** di un attacco reale per trovare e
sfruttare vulnerabilità prima che lo faccia un avversario. Output = un [[Reporting Pentest|report]]
con rischi e rimedi. È il lato offensivo del [[Percorsi di Carriera Pentester vs SOC|Pentester]].

> [!warning] Etica e legge
> Si esegue **solo** con autorizzazione scritta (scope/rules of engagement) o su lab/CTF
> ([[TryHackMe]], [[HackTheBox]]). Senza autorizzazione è reato.

## Livelli di conoscenza

- **Black box** — nessuna info iniziale, simula l'attaccante esterno.
- **Grey box** — info parziali (es. credenziali utente base).
- **White box** — accesso completo a codice/architettura.

## vs concetti vicini

- **Vulnerability Assessment** — *trova* le vulnerabilità ma non le sfrutta.
- **Red Team** — operazione goal-oriented e stealth, valuta anche la *detection* del blue team.
- **Pentest** — sta in mezzo: trova **e** sfrutta, con scope definito.

## Fasi (sintesi)

[[Ricognizione (Recon)]] -> [[Scansione delle Porte]] -> [[Enumerazione]] ->
[[Exploitation]] -> [[Post-Exploitation]] -> [[Reporting Pentest]].
Dettaglio in [[Metodologia del Pentest]].

## Collegamenti

- [[Metodologia del Pentest]] · [[Metodologia CTF]] · [[Kali Linux]]
- [[Percorsi di Carriera Pentester vs SOC]] · [[Reporting Pentest]]
