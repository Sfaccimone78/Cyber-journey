---
tipo: concetto
tag: [wireless]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Attacchi WPA2 (handshake e PMKID)"]
---

# Attacchi WPA2 (handshake e PMKID)

## In breve
Contro WPA2-PSK esistono due vie per ottenere il materiale da attaccare offline: catturare il
**4-way handshake** (richiede un client che si autentica) oppure estrarre il **PMKID** direttamente
dall'AP (**clientless**, non serve alcun client). In entrambi i casi non si "rompe" AES: si esegue un
**attacco a dizionario/brute force offline** sulla passphrase. La robustezza dipende interamente da
quanto è forte la PSK.

## Come funziona
Il **4-way handshake** scambia quattro messaggi EAPOL per derivare la PTK senza trasmettere la PSK:

1. **AP -> STA**: invia l'**ANonce** (nonce dell'AP).
2. **STA -> AP**: invia lo **SNonce** + un **MIC** (Message Integrity Code) calcolato con la PTK.
3. **AP -> STA**: conferma e installa la GTK, con MIC.
4. **STA -> AP**: ack finale.

La **PTK** è derivata da: PMK + ANonce + SNonce + MAC dell'AP + MAC della STA. L'attaccante che
cattura ANonce, SNonce, i MAC e il MIC del messaggio 2 può, per ogni candidato di passphrase,
calcolare la PMK -> PTK -> MIC e confrontarlo con quello catturato. Quando i MIC coincidono, ha la
password. Per ottenere l'handshake rapidamente si forza un client a riconnettersi con un **deauth**.

Il **PMKID** è un campo opzionale che alcuni AP includono nel **primo messaggio EAPOL**: vale
`PMKID = HMAC-SHA1(PMK, "PMK Name" | MAC_AP | MAC_STA)`. Poiché dipende solo dalla PMK e dai MAC,
si può catturare interagendo direttamente con l'AP **senza alcun client connesso** (attacco di Steube
2018, alla base del formato hashcat **22000**).

## Esempi
Cattura del 4-way handshake + deauth mirato:

```bash
# Ascolta e salva la cattura sul canale dell'AP
sudo airodump-ng --bssid AA:BB:CC:DD:EE:FF -c 6 -w capture wlan0mon

# In un'altra shell: deauth di un client per forzare il re-handshake
sudo aireplay-ng --deauth 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
# airodump mostra "WPA handshake: AA:BB:CC:DD:EE:FF" in alto a destra quando catturato

# Crack con aircrack-ng (formato legacy 2500)
sudo aircrack-ng -w rockyou.txt -b AA:BB:CC:DD:EE:FF capture-01.cap
```

Attacco PMKID clientless con hcxdumptool + hashcat (-m 22000):

```bash
# Cattura PMKID/handshake nel formato pcapng moderno
sudo hcxdumptool -i wlan0mon -o dump.pcapng --enable_status=1

# Converte in formato hash 22000 per hashcat
hcxpcapngtool -o hash.22000 dump.pcapng

# Cracking GPU: 22000 copre sia PMKID sia EAPOL
hashcat -m 22000 hash.22000 rockyou.txt
# Esempio con regole/maschera
hashcat -m 22000 hash.22000 -a 3 '?d?d?d?d?d?d?d?d'
```

## Mitigazione e difesa
- **Passphrase lunghe e casuali**: l'unico fattore che rende l'attacco offline impraticabile.
- Disabilitare il roaming/802.11r non necessario e l'esposizione del **PMKID** dove possibile.
- **WPA3-SAE** elimina l'attacco offline: ogni guess richiede interazione attiva.
- Monitorare picchi di **deauth** (segnale tipico della fase di cattura handshake) tramite WIDS/WIPS.

## Lab
- [[TryHackMe]] — room dedicate alla cattura handshake e al cracking WPA2.
- [[HackTheBox]] — challenge con file .cap/.pcapng da analizzare.
- Lab: AP di test + `rockyou.txt`; provare sia la via handshake+deauth sia la via PMKID clientless.

## Domande
**D:** Serve sempre un client connesso per attaccare WPA2?
R: No: con il PMKID si interagisce direttamente con l'AP, senza alcun client (clientless).

**D:** Cosa si "rompe" davvero nell'attacco?
R: Non AES: si brute-forza offline la passphrase ricalcolando PTK/MIC (o il PMKID) per ogni candidato.

**D:** Perché si usa il deauth?
R: Per forzare un client a riconnettersi e quindi catturare un 4-way handshake fresco.

**D:** Cosa rappresenta `-m 22000` in hashcat?
R: Il formato unificato WPA-PBKDF2 che gestisce sia PMKID sia EAPOL handshake (sostituisce 2500/16800).

## Approfondimento livello esperto
Il **PMKID clientless attack** ha rivoluzionato gli assessment perché elimina la dipendenza dai client
e dal timing del deauth. Sul piano performance, hashcat sfrutta la GPU per PBKDF2-HMAC-SHA1 (4096
iterazioni): le passphrase deboli cadono in minuti, ma una PSK casuale di 20 caratteri è fuori
portata. La detection si concentra sui pattern di **association/EAPOL anomali** e sui deauth burst.
WPA3 chiude questa intera classe rendendo non utilizzabile il materiale offline; per questo gli
attacchi moderni puntano sulla **transition mode** o sull'**evil twin** per indurre downgrade.

## Collegamenti
- [[WEP, WPA, WPA2 e WPA3]] — perché WPA2 è vulnerabile e WPA3 no
- [[Fondamenti Wireless e 802.11]] — frame EAPOL e management
- [[Evil Twin e Rogue AP]] — alternativa quando la PSK è troppo forte
- [[Wireless Tooling (aircrack-ng, hashcat)]] — la catena di tool usata qui
- [[Penetration Testing]] — contesto metodologico
- [[Modello OSI]]

## Fonti
- https://hashcat.net/forum/thread-7717.html (PMKID clientless, Steube)
- https://hashcat.net/wiki/doku.php?id=cracking_wpawpa2
- https://www.aircrack-ng.org/doku.php?id=cracking_wpa
