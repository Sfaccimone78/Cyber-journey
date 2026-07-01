---
tipo: concetto
tag: [osint, opsec]
fase: 3
fonti: 3
aggiornato: 2026-06-29
stato: maturo
aliases: ["Sicurezza Operativa per le Indagini OSINT"]
---

# Sicurezza Operativa (OpSec) per le Indagini OSINT: Costruire Sock Puppet Resilienti

Le indagini Open Source Intelligence (OSINT) richiedono la raccolta di informazioni da database pubblici, piattaforme social, forum e siti del dark web. Durante queste attività, mantenere un'assoluta Sicurezza Operativa (OpSec) è critico. Se un investigatore accede agli account o ai siti web bersaglio utilizzando il proprio indirizzo IP personale, account connessi o configurazioni del browser identificabili, rischia di esporre la propria identità. Questo processo di esposizione è noto come "attribuzione". Per prevenire l'attribuzione, gli investigatori costruiscono ambienti isolati e identità virtuali, comunemente chiamati "sock puppet".

## Il Modello di Minaccia Principale nell'OSINT

Un modello di minaccia definisce i rischi e gli avversari che un investigatore affronta. Nell'OSINT, le minacce principali sono:
1. **Allerta del Bersaglio**: Il soggetto dell'indagine riceve una notifica (es. "Qualcuno ha visualizzato il tuo profilo su LinkedIn") ed elimina le prove o va offline.
2. **Reverse OSINT**: Un threat actor sofisticato monitora i log del proprio server, estrae l'indirizzo IP, l'impronta digitale del browser (fingerprint) o l'email dell'investigatore, ed esegue un'indagine sull'investigatore stesso.
3. **Contaminazione Incrociata**: Collegare accidentalmente un account personale (loggato sullo stesso browser) alle attività di indagine.

Mitigare queste minacce richiede la separazione delle attività di indagine dalla vita personale a ogni livello: rete, browser, macchina e identità.

## Anonimizzazione e Routing di Rete

L'indirizzo IP dell'investigatore è l'identificatore più diretto. L'uso di una semplice connessione internet domestica o aziendale espone la posizione e i dettagli dell'ISP.

- **Virtual Private Networks (VPN)**: Una misura di sicurezza di base che cifra il traffico e nasconde l'IP dell'host. Tuttavia, gli IP delle VPN commerciali sono ben noti e spesso bloccati dalle piattaforme social o dai provider cloud.
- **Rete Tor**: Eccellente per l'anonimizzazione, ma soffre di velocità lente e CAPTCHA frequenti. Inoltre, alcuni siti bersaglio bloccano completamente i nodi di uscita Tor.
- **Proxy Residenziali**: Questi instradano il traffico attraverso connessioni internet domestiche (appartenenti agli ISP standard), facendo apparire l'investigatore come un residente locale legittimo piuttosto che un investigatore che utilizza una VPN da datacenter.
- **Prevenzione dei Leak**: Assicurarsi che WebRTC sia disabilitato e che le query DNS siano instradate attraverso l'interfaccia VPN/Tor per prevenire i "DNS leak", che rivelano il vero ISP dell'investigatore anche quando una VPN è attiva.

## Sconfiggere il Browser Fingerprinting

Le piattaforme moderne non si basano esclusivamente sugli indirizzi IP per tracciare gli utenti; utilizzano il **Browser Fingerprinting**. Questa tecnica aggrega le configurazioni di sistema univoche per identificare un'istanza del browser:
- **Stringa User-Agent**: Versione del browser, OS, lingua.
- **Canvas Fingerprinting**: Come il browser esegue il rendering della grafica HTML5 Canvas, che varia in base a GPU, driver e font.
- **Fingerprint WebGL e Audio**: Comportamento dell'elaborazione audio e dettagli del rendering 3D.
- **Risoluzione dello Schermo e Elenco dei Font**: I font di sistema esatti installati.

Per contrastare il fingerprinting, l'uso di profili browser standard è insufficiente. Gli investigatori utilizzano:
1. **Browser Anti-Detect**: Software come Multilogin, Linken Sphere o profili specializzati in Brave che alterano dinamicamente canvas, WebGL e gli identificatori hardware, presentando un'impronta unica e coerente per ogni sock puppet.
2. **Blocco WebRTC**: Estensioni o configurazioni per disabilitare WebRTC, che può far trapelare l'indirizzo IP locale sottostante dietro a un proxy.

## Costruire Sock Puppet Resilienti

Un sock puppet è una falsa persona online. Crearne uno in grado di eludere i moderni sistemi di rilevamento delle frodi richiede una pianificazione meticolosa.

### 1. Generazione della Persona e del Background
Sviluppare una persona coesa e noiosa. Generare un nome realistico, un indirizzo e un'occupazione. Evitare di generare volti IA "perfetti" che mostrano artefatti (come orecchini asimmetrici o sfondi sfocati), poiché le piattaforme moderne utilizzano algoritmi di rilevamento per segnalarli. L'uso di foto stock o avatar stilizzati e non ovvi è spesso più sicuro.

### 2. Verifica Telefonica ed Email
La maggior parte delle piattaforme richiede la verifica via SMS durante la registrazione.
- Evitare l'uso di numeri VoIP virtuali gratuiti (come Google Voice), poiché le piattaforme principali li segnalano e li rifiutano automaticamente.
- Utilizzare schede SIM usa e getta (burner) o servizi di hosting SIM a pagamento che utilizzano reti cellulari reali.
- Registrare un'email sicura (come ProtonMail o Tuta) utilizzando il numero burner, e usare quell'email per registrarsi sulle piattaforme bersaglio.

### 3. Attività e Manutenzione della Persona
Stabilire una cronologia di base. Un account nuovo di zecca con zero amici, nessun post e ricerche immediate di bersagli sensibili verrà segnalato e sospeso. Lasciare invecchiare l'account, iscriversi a gruppi generici, seguire notiziari e stabilire una cronologia di navigazione naturale prima di iniziare la raccolta attiva di intelligence.

## Isolamento del Sistema Operativo

Mai eseguire i sock puppet direttamente su un sistema operativo principale. Utilizzare macchine virtuali (VM) o distribuzioni specializzate:
- **Tails OS**: Un sistema operativo live che instrada tutto il traffico tramite Tor e non lascia traccia sul computer locale una volta spento.
- **Whonix**: Un OS basato su Debian incentrato sulla sicurezza, composto da due VM: un gateway (che instrada tutto il traffico tramite Tor) e una workstation (dove l'utente esegue il browser). Questa architettura impedisce ai malware o agli exploit del browser di scoprire il vero indirizzo IP esterno.
- **Qubes OS**: Un OS orientato alla sicurezza che utilizza la virtualizzazione Xen per isolare le applicazioni in separate "AppVM".


## Collegamenti
- [[OSINT]]
- [[Social Engineering e Phishing]]
- [[VPN]]
- [[OSINT in Radiofrequenza]]

## Fonti
- Michael Bazzell — IntelTechniques / OSINT Techniques: https://inteltechniques.com/
- Bellingcat — Online Investigation Toolkit: https://www.bellingcat.com/
- US Army ATP 2-22.9 — Open-Source Intelligence: https://irp.fas.org/doddir/army/atp2-22-9.pdf
