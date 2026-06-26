---
tipo: concetto
tag: [fondamenti]
fase: 1
fonti: 0
aggiornato: 2026-06-23
stato: attivo
aliases: ["Glossario degli Acronimi", "Glossario"]
---

# Glossario degli Acronimi di Cybersecurity

La sicurezza informatica è piena di acronimi complessi che possono disorientare un principiante. Questa pagina raccoglie le sigle fondamentali citate in questa Wiki, traducendole e collegandole alle rispettive note teoriche.

---

## 🟢 Fondamenti e Sicurezza Generale
*   **MOC** (Map of Content): Mappa dei Contenuti. Nota riepilogativa usata su Obsidian per collegare logicamente pagine sullo stesso tema (es. [[00 — Mappa Fondamenti|Mappa Fondamenti]]).
*   **CIA** (Confidentiality, Integrity, Availability): Riservatezza, Integrità, Disponibilità. I tre pilastri fondamentali della sicurezza descritti nella [[Triade CIA]].
*   **CVE** (Common Vulnerabilities and Exposures): Un dizionario pubblico che cataloga e identifica in modo univoco le vulnerabilità di sicurezza note (es. [[CVE e CVSS]]).
*   **CVSS** (Common Vulnerability Scoring System): Metodo standardizzato per assegnare un punteggio numerico (da 0 a 10) che indica la gravità di una vulnerabilità.
*   **IAM** (Identity and Access Management): Gestione delle Identità e degli Accessi. Sistema per garantire che solo gli utenti autorizzati abbiano accesso alle giuste risorse (es. [[IAM e Zero Trust]]).
*   **MFA** (Multi-Factor Authentication): Autenticazione a più fattori. Richiede due o più prove di identità prima di concedere l'accesso.
*   **PoC** (Proof of Concept): Dimostrazione di fattibilità. Un piccolo codice o procedura che prova l'esistenza reale di una vulnerabilità.

---

## 🌐 Reti e Protocolli
*   **IP** (Internet Protocol): Protocollo Internet. Assegna gli indirizzi numerici univoci ai dispositivi in rete (es. [[Indirizzamento IP]]).
*   **MAC** (Media Access Control): Indirizzo fisico univoco cablato nella scheda di rete (es. [[MAC Address]]).
*   **ARP** (Address Resolution Protocol): Protocollo per tradurre un indirizzo IP logico nel corrispondente indirizzo MAC fisico (es. [[ARP]]).
*   **TCP** (Transmission Control Protocol): Protocollo di trasporto affidabile orientato alla connessione (es. [[TCP]]).
*   **UDP** (User Datagram Protocol): Protocollo di trasporto veloce ma non garantito (es. [[UDP]]).
*   **ICMP** (Internet Control Message Protocol): Protocollo per messaggi di controllo e diagnostica di rete, usato da [[Ping e Traceroute]] (es. [[ICMP]]).
*   **DNS** (Domain Name System): Il "rubricario" di Internet che traduce i nomi di dominio (es. google.com) in indirizzi IP (es. [[DNS]]).
*   **DHCP** (Dynamic Host Configuration Protocol): Configura automaticamente l'IP e i parametri di rete di un nuovo dispositivo (es. [[DHCP]]).
*   **NAT** (Network Address Translation): Consente a più dispositivi in una rete privata di condividere un unico IP pubblico (es. [[NAT]]).
*   **VPN** (Virtual Private Network): Crea un tunnel cifrato per navigare in sicurezza su reti non sicure (es. [[VPN]]).
*   **SSH** (Secure Shell): Protocollo per accedere a un computer remoto in modo cifrato via riga di comando (es. [[SSH]]).

---

## 🕸️ Web e Applicazioni
*   **OWASP** (Open Web Application Security Project): Organizzazione no-profit dedicata alla sicurezza del software (es. [[OWASP Top 10]]).
*   **SQLi** (SQL Injection): Iniezione di query SQL all'interno di input utente per manipolare un database (es. [[SQL Injection]]).
*   **XSS** (Cross-Site Scripting): Iniezione di script dannosi (generalmente JavaScript) all'interno di pagine web visualizzate da altri utenti (es. [[Cross-Site Scripting (XSS)]]).
*   **CSRF** (Cross-Site Request Forgery): Forza un utente autenticato a compiere azioni involontarie su un'applicazione web (es. [[Cross-Site Request Forgery (CSRF)]]).
*   **LFI/RFI** (Local / Remote File Inclusion): Costringe un'applicazione a caricare ed eseguire file locali o remoti non previsti (es. [[File Inclusion (LFI e RFI)]]).
*   **SSRF** (Server-Side Request Forgery): Costringe il server web a fare richieste HTTP verso risorse interne o esterne per conto dell'attaccante (es. [[Server-Side Request Forgery (SSRF)]]).
*   **JWT** (JSON Web Token): Standard per la trasmissione sicura di informazioni tra parti sotto forma di oggetto JSON, usato per la gestione delle sessioni (es. [[Cookie e JWT]]).

---

## 🛡️ Difesa e Monitoraggio (Blue Team)
*   **SIEM** (Security Information and Event Management): Software che raccoglie, analizza e correla i log di sicurezza provenienti da tutta la rete aziendale (es. [[SIEM]]).
*   **EDR / XDR** (Endpoint / Extended Detection and Response): Agenti di sicurezza installati sui dispositivi che monitorano comportamenti sospetti e bloccano minacce in tempo reale (es. [[EDR e XDR]]).
*   **IOC** (Indicator of Compromise): Indicatori di Compromissione. Tracce (hash di file, IP sospetti) che indicano che un sistema è stato violato (es. [[Indicatori di Compromissione (IOC)]]).
*   **WAF** (Web Application Firewall): Firewall specializzato nel filtrare e monitorare il traffico HTTP da e verso un'applicazione web.

---

## 🔗 Collegamenti
- [[00 — Mappa Fondamenti|Mappa Fondamenti]]
- [[index|Indice della Wiki]]
