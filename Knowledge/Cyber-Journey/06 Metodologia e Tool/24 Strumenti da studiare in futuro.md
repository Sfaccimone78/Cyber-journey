---
tipo: concetto
tag: [tool, metodologia]
fase: 1
fonti: 0
aggiornato: 2026-06-23
stato: attivo
aliases: ["Strumenti da studiare in futuro"]
---

# Strumenti da studiare in futuro

Questa nota funge da "parcheggio" per tutti gli strumenti di sicurezza avanzati identificati durante i controlli della Wiki. Essendo al momento focalizzato sui fondamenti IT e sulla sicurezza di base, questi strumenti sono temporaneamente in pausa e verranno approfonditi solo quando le basi saranno consolidate.

---

## 🧭 Lista degli Strumenti in Pausa

### 🎯 Pentesting e Offensiva Avanzata
*   **`chisel`**: Un tool veloce e leggero per creare tunnel TCP/UDP. Molto usato per il [[Pivoting]] (accesso a reti interne).
*   **`proxychains`**: Permette di forzare le connessioni TCP di qualsiasi programma attraverso server proxy. Indispensabile in accoppiata con chisel.
*   **`socat`**: Una utility di rete simile a Netcat ma molto più potente. Utilizzata per il reindirizzamento del traffico e per stabilire shell interattive stabili.
*   **`searchsploit`**: Tool a riga di comando per cercare exploit nel database locale di Exploit-DB.
*   **`xp_cmdshell`**: Un modulo di Microsoft SQL Server che consente di eseguire comandi del sistema operativo dal database.
*   **`smbclient`**: Un client per connettersi e interagire con le condivisioni di rete [[SMB]].

### 📡 OSINT e Ricognizione Esterna
*   **`Shodan`**: Un motore di ricerca per dispositivi connessi a Internet (router, server, telecamere). Fondamentale per scoprire servizi esposti.
*   **`theHarvester`**: Tool per raccogliere email, sottodomini, host, nomi di dipendenti, porte aperte e banner da diverse fonti pubbliche.

### 🛡️ Blue Team, IDS/IPS e Analisi di Rete
*   **`Suricata`**: Un motore di rilevamento delle intrusioni (IDS), prevenzione (IPS) e monitoraggio della sicurezza di rete in tempo reale.
*   **`tcpdump`**: Analizzatore di pacchetti a riga di comando. È il fratello testuale di [[Wireshark]] per intercettare il traffico direttamente dal terminale.

### 🤖 Command & Control (C2)
*   **`Cobalt Strike`**: Una suite di emulazione delle minacce e attacco commerciale, famosissima sia tra i Red Team che tra i criminali informatici.
*   **`Sliver`**: Un framework C2 open-source e cross-platform basato su Go, usato come alternativa gratuita a Cobalt Strike.

### 🪟 Strumenti Active Directory Avanzati
*(Questi strumenti sono già documentati nella Wiki nell'area `04 Windows e AD` ma sono messi in pausa per lo studio futuro)*
*   [[Mimikatz]] (estrazione credenziali in memoria)
*   [[Responder]] (LLMNR/NBT-NS poisoning)
*   [[BloodHound]] (mappatura visuale delle relazioni AD)
*   [[NetExec]] e [[CrackMapExec]] (automazione e attacco su reti locali)
*   [[bloodyAD]] (manipolazione oggetti AD tramite protocollo LDAP)
*   [[Impacket]] (suite di script Python per protocolli di rete)

---

## 🔗 Collegamenti
- [[00 — Mappa Metodologia e Tool|Mappa Metodologia e Tool]]
- [[index|Indice della Wiki]]
- [[Piano_cybersecurity|Piano di Studio]]
