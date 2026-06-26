---
tipo: concetto
tag: [os]
fase: 0
fonti: 1
aggiornato: 2026-06-25
stato: maturo
aliases: ["Scheduling"]
---

# Scheduling: FIFO, SJF, STCF, Round Robin, MLFQ, CFS

## Definizione
Lo **scheduler** e la politica con cui l'OS decide *quale* processo ready eseguire e *per quanto*. Due metriche fondamentali in tensione: [Fonte: OSTEP, cap. 7]
- **Turnaround time** = (completamento - arrivo). Buono per job batch.
- **Response time** = (primo istante di esecuzione - arrivo). Buono per job interattivi.

*Crux: come sviluppare una politica di scheduling? Quali assunzioni, metriche, approcci?* [Fonte: OSTEP, cap. 7]

## Meccanismo: evoluzione delle politiche

| Politica | Idea | Pro | Contro |
|----------|------|-----|--------|
| **FIFO/FCFS** | first-come first-served | semplice | **convoy effect**: un job lungo davanti blocca i corti -> turnaround pessimo |
| **SJF** | esegui prima il job piu corto | ottimo turnaround (se non-preemptive, arrivi simultanei) | serve conoscere la durata |
| **STCF** | SJF **preemptive**: scegli il minor tempo residuo | turnaround ottimo | response time pessimo; serve l'oracolo |
| **Round Robin** | esegui ogni job per un **time slice** poi ruota | **ottimo response time**, equo | turnaround peggiore; slice corto -> overhead switch |

Tensione fondamentale: **STCF ottimizza il turnaround, RR il response time**. Non si puo avere il meglio di entrambi senza conoscere il futuro. [Fonte: OSTEP, cap. 7]

> Considerare l'**I/O**: quando un job si blocca su I/O, lo scheduler ne fa girare un altro (*overlap*), tenendo la CPU occupata. [Fonte: OSTEP, cap. 7]

## MLFQ (Multi-Level Feedback Queue)
Risolve il crux: schedulare **senza conoscenza** della durata. MLFQ *impara* dal comportamento osservato. [Fonte: OSTEP, cap. 8]

Regole:
1. Se priorita(A) > priorita(B), gira A.
2. Se uguali, A e B in **round robin**.
3. Un job entra alla **priorita massima**.
4. (Better accounting) Quando un job **esaurisce il quanto totale** a un livello (a prescindere da quante volte cede la CPU), scende di priorita.
5. **Priority boost**: ogni periodo S, riporta tutti i job al top.

Effetti: i job **interattivi** (cedono spesso per I/O) restano in alto -> ottimo response time; i job **CPU-bound** scendono -> ottimo throughput. Approssima SJF *senza* conoscere le durate. Il boost evita **starvation** e gestisce job che cambiano comportamento. La regola 4 difende dal **gaming**: senza, un processo che cede la CPU appena prima della fine del quanto resterebbe perennemente in alto. [Fonte: OSTEP, cap. 8]

## Proportional Share & CFS
- **Lottery scheduling**: ogni processo riceve dei **ticket**; lo scheduler estrae un ticket a caso -> probabilita di esecuzione proporzionale ai ticket. **Stride scheduling** e la variante deterministica. [Fonte: OSTEP, cap. 9]
- **CFS (Completely Fair Scheduler)** - scheduler di default di Linux. Usa il **virtual runtime (vruntime)**: ogni processo accumula vruntime mentre gira; lo scheduler elegge sempre quello col **vruntime minimo**, gestiti in un **red-black tree** (O(log n)). Parametri `sched_latency` e `min_granularity` bilanciano equita ed efficienza; il **nice** value modula il peso (velocita di accumulo del vruntime). [Fonte: OSTEP, cap. 9]

## Implicazioni
- Lo scheduler e dove **fairness vs efficienza** si scontrano concretamente.
- MLFQ e alla base di scheduler reali (Windows, vecchi Solaris/FreeBSD); CFS e il presente di Linux.
- Legato al [[Processi]] (context switch) e alla [[Concorrenza e Thread]] (scheduling non controllato -> race condition).

## Collegamenti
- Vedi anche: [[Processi]], [[Concorrenza e Thread]], [[Concetti dei Sistemi Operativi]]
- Cross-topic (linux): [[Processi Linux]]

## Fonti
- [OSTEP, cap. 7 "Scheduling: Introduction", p. 65-75]
- [OSTEP, cap. 8 "The Multi-Level Feedback Queue", p. 77-87]
- [OSTEP, cap. 9 "Scheduling: Proportional Share" (CFS), p. 89-101]
