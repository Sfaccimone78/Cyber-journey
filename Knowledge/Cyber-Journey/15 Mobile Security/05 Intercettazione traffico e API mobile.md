---
tipo: concetto
tag: [mobile]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Intercettazione traffico e API mobile"]
---

# Intercettazione traffico e API mobile

## In breve
L'intercettazione del traffico mette un proxy MITM tra l'app e il backend per ispezionare e manipolare le chiamate API, il cuore della logica applicativa moderna. Categoria: analisi delle comunicazioni di rete (MASVS-NETWORK). Impatto: scoperta di endpoint nascosti, IDOR/BOLA, autenticazione debole, dati sensibili in transito e bypass di controlli client-side.

## Come funziona
Si configura un proxy (Burp Suite, mitmproxy, OWASP ZAP) come gateway del device e si installa la CA del proxy come trusted. Su Android 7+ le app non si fidano più delle CA utente per default (`network_security_config`): serve installare la CA come **system CA** (root) o modificare il config dell'app. Molte app implementano **certificate pinning**, che blocca il MITM anche con CA valida: va bypassato con Frida/objection hookando le funzioni di verifica. Una volta nel mezzo, si analizzano le API REST/GraphQL: parametri, header di auth (JWT, API key), e si testano vulnerabilità server-side come autorizzazione a livello di oggetto (BOLA/IDOR), mass assignment e SSRF. Il proxy permette anche il replay e la modifica al volo delle richieste.

## Esempi
```bash
# mitmproxy in ascolto, device punta a IP:8080
mitmproxy -p 8080
# poi sul device: Wi-Fi -> proxy manuale -> IP del PC : 8080
# visita http://mitm.it dal device per scaricare e installare la CA

# Installare la CA come system CA su Android rootato (Android < 14)
openssl x509 -inform PEM -subject_hash_old -in mitmproxy-ca-cert.pem | head -1
# rinomina cert in <hash>.0 e copia in /system/etc/security/cacerts
adb root && adb remount
adb push 9a5ba575.0 /system/etc/security/cacerts/
adb shell chmod 644 /system/etc/security/cacerts/9a5ba575.0
adb reboot

# Bypass cert pinning con objection (Frida)
objection -g com.example.app explore
android sslpinning disable        # Android
ios sslpinning disable            # iOS

# Burp: redirect del traffico via adb reverse (utile con emulatore)
adb reverse tcp:8080 tcp:8080
```

```javascript
// Frida: bypass pinning OkHttp universale (snippet)
Java.perform(function () {
  var CertPinner = Java.use('okhttp3.CertificatePinner');
  CertPinner.check.overload('java.lang.String', 'java.util.List').implementation = function (a, b) {
    console.log('[+] OkHttp pinning bypassato per: ' + a);
    return;
  };
});
```

## Mitigazione e difesa
1. Imporre TLS 1.2+ ovunque e implementare certificate pinning (preferibilmente public-key pinning) verificato correttamente.
2. Spostare ogni controllo di autorizzazione lato server: il client non deve essere l'unico gate (previene IDOR/BOLA).
3. Usare token a vita breve, scope minimo e binding del token al device/sessione.
4. Non esporre dati sensibili o endpoint di debug nelle risposte API; rimuovere verbose error.
5. Considerare attestazione (Play Integrity/App Attest) per ridurre traffico da client manomessi, validandola server-side.

## Lab
- PortSwigger Web Security Academy (API/access control) applicato al backend mobile.
- OWASP crAPI (Completely Ridiculous API) per BOLA/IDOR e mass assignment.
- InsecureBankv2 e DIVA per traffico in chiaro e pinning assente.
- [[TryHackMe]] room su Burp Suite e API; [[HackTheBox]] challenge web/API legate ad app mobile.

## Domande
**D:** Perché su Android 7+ non basta installare la CA come utente?
R: Dal default `network_security_config` le app non si fidano delle CA utente; serve installarla come system CA o modificare il config dell'app.

**D:** Cos'è il certificate pinning e perché blocca il MITM?
R: L'app accetta solo un certificato/chiave specifico del server; una CA valida ma diversa viene rifiutata, impedendo l'intercettazione finché non si bypassa il pin.

**D:** Cos'è BOLA/IDOR nel contesto API mobile?
R: Accesso a oggetti di altri utenti cambiando un identificatore nella richiesta, quando il server non verifica l'ownership.

**D:** A cosa serve `adb reverse tcp:8080 tcp:8080`?
R: A inoltrare la porta del device verso il proxy sul PC, utile per intercettare il traffico dell'emulatore senza configurare il Wi-Fi proxy.

## Approfondimento livello esperto
Quando `android sslpinning disable` fallisce significa pinning custom o native. Strategia: tracciare con `frida-trace -U -i "*SSL*" -i "*pinning*" com.example.app` per individuare le funzioni, poi hookare. Per pinning in BoringSSL (NDK, Flutter, React Native) si hooka `ssl_crypto_x509_session_verify_cert_chain` o si usa lo script di Frida CodeShare "frida-multiple-unpinning". App Flutter ignorano il proxy di sistema: serve impostare `dart:io HttpClient` proxy via Frida o usare `reFlutter` per ripatchare il bundle e disabilitare il pinning interno. Per evadere detection del proxy lato app (controllo di `http_proxy`, IP sospetti) si usa un MITM trasparente a livello di routing (iptables redirect verso mitmproxy in transparent mode) invece del proxy esplicito. OPSEC: cattura solo del traffico del target con SNI filtering per evitare rumore. Caso limite: gRPC/protobuf richiede decodifica con mitmproxy + plugin protobuf o estrazione del `.proto` dal binario. MASVS-NETWORK-2 (L2) richiede pinning, quindi la sua assenza è un FAIL su app ad alto rischio.

## Collegamenti
- [[Fondamenti Mobile]]
- [[Android Pentest]]
- [[iOS Pentest]]
- [[OWASP MASVS e MASTG]]
- [[Insecure Data Storage e Crypto su mobile]]
- [[Cookie e JWT]]
- [[Server-Side Request Forgery (SSRF)]]
- [[OWASP Top 10]]
- [[Penetration Testing]]

## Fonti
- OWASP MASTG Network Communication Testing: https://mas.owasp.org/MASTG/
- PortSwigger - Bypassing certificate pinning: https://portswigger.net/burp/documentation/desktop/mobile/config-android-device
- HackTricks - Certificate Pinning Bypass: https://book.hacktricks.xyz/mobile-pentesting/android-app-pentesting#bypass-ssl-pinning
