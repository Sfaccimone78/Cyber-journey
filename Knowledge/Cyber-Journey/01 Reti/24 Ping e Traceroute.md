---
tipo: entita
tag: [reti, tool]
fase: 1
fonti: 0
aggiornato: 2026-06-23
stato: attivo
aliases: ["Ping e Traceroute"]
---

# Ping e Traceroute

Questi sono i due strumenti a riga di comando più importanti e basilari per diagnosticare problemi di rete, testare la raggiungibilità di un host e analizzare il percorso dei pacchetti IP su Internet.

---

## 📡 1. Ping (Packet Internet Groper)

### In poche parole
`ping` controlla se una macchina remota è accesa e raggiungibile sulla rete. È l'equivalente digitale del bussare alla porta di qualcuno per vedere se risponde "Sì, sono qui!".

### Come funziona internamente
Ping utilizza il protocollo [[ICMP]] (Internet Control Message Protocol).
1. Il tuo computer invia un pacchetto **ICMP Echo Request** (Tipo 8) all'indirizzo IP di destinazione.
2. Se la macchina di destinazione è attiva e configurata per rispondere, risponde con un pacchetto **ICMP Echo Reply** (Tipo 0).

### Esempi di utilizzo pratico
Esegui questi comandi nel tuo terminale (Linux, macOS o Windows cmd):

*   **Verificare se internet funziona (es. interrogando il server DNS di Google):**
    ```bash
    ping 8.8.8.8
    ```
*   **Verificare se una macchina locale risponde (es. il tuo router):**
    ```bash
    ping 192.168.1.1
    ```
*   **Interpretare l'output:**
    *   `64 bytes from...`: La destinazione ha risposto.
    *   `time=12ms`: Tempo impiegato dal pacchetto per andare e tornare (latenza o Round Trip Time - RTT).
    *   `TTL=64` (o 128/255): Time To Live, indica quanti passaggi di router il pacchetto può fare ancora prima di essere scartato.
    *   `Request timed out` (Richiesta scaduta): La macchina è spenta, l'IP non esiste o un firewall blocca i pacchetti ICMP.

---

## 🗺️ 2. Traceroute (o Tracert su Windows)

### In poche parole
`traceroute` mostra l'esatto percorso (la "strada") che i tuoi dati fanno per raggiungere una destinazione su Internet, elencando ogni singolo router che i pacchetti attraversano.

### Come funziona internamente
Traceroute fa un trucco intelligente modificando il campo **TTL** (Time To Live) dei pacchetti IP:
1. Invia il primo pacchetto con **TTL = 1**. Il primo router riceve il pacchetto, decrementa il TTL a 0, scarta il pacchetto e risponde con un errore: `ICMP Time Exceeded`. Traceroute segna l'indirizzo IP di questo primo router.
2. Invia un secondo pacchetto con **TTL = 2**. Questo supera il primo router e scade al secondo, rivelando la sua identità.
3. Continua incrementando il TTL (+1 alla volta) finché il pacchetto non raggiunge la destinazione finale.

### Esempi di utilizzo pratico
*   **Tracciare la strada per raggiungere un sito su Linux/macOS:**
    ```bash
    traceroute google.com
    ```
*   **Tracciare la strada su Windows (usa il protocollo ICMP di default):**
    ```cmd
    tracert google.com
    ```

---

## 🧠 Collegamenti con la teoria
- [[ICMP]] (il protocollo fondamentale usato da ping e traceroute)
- [[Indirizzamento IP]] (per capire gli indirizzi dei router elencati)
- [[Modello TCP-IP]] (per capire come viaggiano i pacchetti)

## 📚 Fonti
- RFC 792 (specifiche del protocollo ICMP)
- Manuale d'uso dei comandi Linux `man ping` e `man traceroute`.
