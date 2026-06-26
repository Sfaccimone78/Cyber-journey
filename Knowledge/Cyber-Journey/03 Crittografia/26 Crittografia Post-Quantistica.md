---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["Crittografia Post-Quantistica", "PQC", "Post-Quantum", "Crittografia Post-Quantum"]
---

# Crittografia Post-Quantistica

## Definizione

La **crittografia post-quantistica (PQC)** è l'insieme degli algoritmi a **chiave pubblica** progettati per resistere ad attacchi sia classici sia **quantistici**. Gira su computer classici (non è "crittografia quantistica"/QKD): cambia il **problema matematico** sottostante, scegliendone uno che **nemmeno un computer quantistico** sappia risolvere efficientemente.

## Perché Shor rompe RSA ed ECC

Tutta l'asimmetrica classica poggia su due problemi:
- **Fattorizzazione** di `N = p·q` → [[RSA]]
- **Logaritmo discreto** (classico ed ellittico) → [[Scambio di Chiavi Diffie-Hellman]], [[Crittografia a Curve Ellittiche (ECC)]]

> L'**algoritmo di Shor** (1994) risolve **entrambi** in **tempo polinomiale** su un computer quantistico sufficientemente grande e tollerante ai guasti. Non è un'ottimizzazione marginale: passa da sub-esponenziale a polinomiale, azzerando il vantaggio difensore/attaccante. RSA, DH, ECDH, ECDSA, EdDSA **cadono tutti insieme**. [Fonte: Crypto101, App. A]

Il simmetrico se la cava molto meglio. L'**algoritmo di Grover** dà solo uno **speedup quadratico** sulla ricerca di chiave: AES-128 scende a ~64 bit effettivi, ma **AES-256 resta sicuro** (~128 bit). Stesso per le hash: SHA-256 mantiene ~128 bit di resistenza alle collisioni. → [[AES]], [[Funzioni di Hash]]

| Primitivo | Minaccia quantistica | Mitigazione |
|-----------|----------------------|-------------|
| RSA / DH / ECC | **Shor** → rotti (polinomiale) | sostituire con PQC |
| AES-128 | Grover → ~64 bit | passare ad **AES-256** |
| SHA-256 | Grover (preimage), nessun impatto pratico sulle collisioni | OK; usare ≥256 bit |

> **"Harvest now, decrypt later"**: un avversario può **registrare oggi** traffico cifrato (RSA/ECDH) e decifrarlo **in futuro** quando avrà un quantum computer. Per questo la migrazione è urgente *anche prima* che la macchina esista, soprattutto per dati a lunga riservatezza.

## La matematica: i reticoli (lattice)

La famiglia più matura si basa su **problemi sui reticoli**:
- **LWE** (Learning With Errors): dato `A` e `b = A·s + e` con un piccolo **errore** `e`, recuperare il segreto `s` è difficile. L'errore "sporca" il sistema lineare rendendolo intrattabile.
- **Module-LWE / Ring-LWE**: varianti strutturate (su anelli di polinomi) → chiavi più piccole e operazioni più veloci, a costo di un'assunzione di sicurezza un po' più forte.
- **SIS** (Short Integer Solution): trovare una combinazione intera "corta" che annulli `A` — base per le firme.

Vantaggio: i migliori algoritmi noti (classici e quantistici) per LWE/SIS restano **esponenziali**; Shor **non** si applica perché non c'è una struttura di gruppo abeliano nascosto da sfruttare. [Fonte: Boneh-Shoup, cap. 17]

## Standard NIST (2024)

Nell'**agosto 2024** il NIST ha pubblicato i primi tre standard PQC finali:

| FIPS | Nome standard | Algoritmo origine | Tipo | Base |
|------|---------------|-------------------|------|------|
| **203** | **ML-KEM** | **CRYSTALS-Kyber** | KEM (scambio chiave) | Module-LWE |
| **204** | **ML-DSA** | **CRYSTALS-Dilithium** | Firma digitale | Module-LWE/SIS |
| **205** | **SLH-DSA** | **SPHINCS+** | Firma digitale | Hash-based (stateless) |

- **ML-KEM** (Module-Lattice **Key-Encapsulation Mechanism**): rimpiazza ECDH/RSA per **stabilire chiavi** in TLS, VPN, ecc. Un KEM incapsula una chiave simmetrica nella pubblica del destinatario. Livelli: ML-KEM-512/768/1024.
- **ML-DSA** (Module-Lattice **Digital Signature Algorithm**): firma generica, rimpiazzo primario di RSA/ECDSA.
- **SLH-DSA** (**Stateless Hash-based** DSA): firme basate **solo su funzioni hash** ([[Funzioni di Hash]]) → sicurezza basata su un'assunzione minimale e ben compresa, **diversificazione** rispetto ai reticoli se questi venissero indeboliti. Firme grandi e lente: riserva conservativa, non default.

> **FN-DSA** (da **Falcon**, firme lattice compatte) è atteso come **FIPS 206** (in finalizzazione). Inoltre nel 2025 NIST ha selezionato **HQC** (code-based) come **KEM di backup** non-lattice, per non mettere tutte le uova nel paniere dei reticoli.

## Vulnerabilità e rischi

- **Maturità**: schemi giovani rispetto a RSA (40+ anni di crittanalisi). *Attacks only get better* vale doppio qui → [[Attacchi Crittografici]].
- **Caduta di rami interi**: **SIKE/SIDH** (isogenie), un tempo candidato promettente, è stato **rotto classicamente** nel 2022 (attacco Castryck–Decru). Monito sul rischio di assunzioni nuove.
- **Implementazione**: chiavi/ciphertext **molto più grandi** (ML-KEM-768 ~1.1 KB di pubblica) e nuovi **side-channel** (timing/power sul campionamento gaussiano) → [[Attacchi Crittografici]].
- **Bug di transizione**: errori nella composizione ibrida o nel parsing dei nuovi formati.

## Migrazione ibrida (in pratica)

L'approccio adottato è **ibrido**: combinare un algoritmo classico **e** uno PQC, così la sessione è sicura se **almeno uno** regge.

- **X25519 + ML-KEM-768** ("X25519MLKEM768"): già in **TLS 1.3** (Chrome, Firefox, Cloudflare) e in OpenSSH (`sntrup761x25519`, poi varianti ML-KEM). → [[TLS e SSL]]
- **Signal** ha introdotto **PQXDH** (X25519 + Kyber) nel suo handshake.
- Settori a lunga riservatezza (governi, sanità, finanza) migrano per primi contro "harvest now, decrypt later".

## Collegamenti
- Problemi rotti da Shor: [[RSA]], [[Scambio di Chiavi Diffie-Hellman]], [[Crittografia a Curve Ellittiche (ECC)]]
- Simmetrico resiliente: [[AES]] (AES-256), [[Funzioni di Hash]]
- Dispiegamento: [[TLS e SSL]]
- Rischio crittanalisi: [[Attacchi Crittografici]]
- [[00 — Mappa Crittografia|Mappa Crittografia]]

## Fonti
- NIST FIPS 203 (ML-KEM): https://csrc.nist.gov/pubs/fips/203/final
- NIST FIPS 204 (ML-DSA): https://csrc.nist.gov/pubs/fips/204/final · FIPS 205 (SLH-DSA): https://csrc.nist.gov/pubs/fips/205/final
- Boneh & Shoup — A Graduate Course in Applied Cryptography, cap. 17 "Post-quantum cryptography from lattices": https://toc.cryptobook.us/
- Crypto 101 (Laurens Van Houtven), App. A (algoritmo di Shor): https://crypto101.io/
