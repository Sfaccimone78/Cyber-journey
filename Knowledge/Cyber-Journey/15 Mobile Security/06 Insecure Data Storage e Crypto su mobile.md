---
tipo: concetto
tag: [mobile]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Insecure Data Storage e Crypto su mobile"]
---

# Insecure Data Storage e Crypto su mobile

## In breve
Insecure data storage è una delle vulnerabilità mobile più diffuse: l'app salva dati sensibili (credenziali, token, PII) sul device in modo non protetto, recuperabili da chi ha accesso fisico o root/jailbreak. Spesso si combina con uso scorretto della crittografia (chiavi hardcoded, algoritmi deboli). Categoria: MASVS-STORAGE e MASVS-CRYPTO. Impatto: furto di credenziali e dati, account takeover.

## Come funziona
Su Android i punti di storage a rischio sono SharedPreferences (XML in chiaro), database SQLite, file interni/esterni, cache, e log. Su iOS sono NSUserDefaults (plist), Keychain mal configurato, file in `Documents`/`Library` e cache. Il problema è che il sandbox protegge solo da altre app, non da un attaccante con root/jailbreak o da backup. Sul fronte crypto gli errori classici sono: chiavi simmetriche hardcoded nel binario, ECB mode (pattern leakabile), IV statici/prevedibili, uso di MD5/SHA1 per password invece di KDF (PBKDF2/scrypt/Argon2), e mancato uso di Keystore/Keychain hardware-backed. La chiave deve risiedere in Android Keystore (TEE/StrongBox) o iOS Keychain/Secure Enclave, dove il materiale crittografico non lascia l'hardware sicuro.

## Esempi
```bash
# Android: dumpare lo storage dell'app (root)
adb shell run-as com.example.app ls -la /data/data/com.example.app/
adb shell run-as com.example.app cat /data/data/com.example.app/shared_prefs/prefs.xml
adb shell run-as com.example.app cat /data/data/com.example.app/databases/app.db | strings

# Estrarre e leggere un DB SQLite
adb pull /data/data/com.example.app/databases/app.db .
sqlite3 app.db ".tables"
sqlite3 app.db "SELECT * FROM users;"

# objection: enumerare storage e segreti
objection -g com.example.app explore
android keystore list
ios keychain dump
ios nsuserdefaults get

# Cercare chiavi/crypto deboli nel codice decompilato
grep -rE "SecretKeySpec|AES/ECB|DES|MD5|\"-----BEGIN|password" base_out/
```

```javascript
// Frida: intercettare uso di cifratura per catturare chiavi/plaintext
Java.perform(function () {
  var Cipher = Java.use('javax.crypto.Cipher');
  Cipher.doFinal.overload('[B').implementation = function (data) {
    console.log('[+] Cipher.doFinal input: ' + Java.use('java.lang.String').$new(data));
    return this.doFinal(data);
  };
});
```

## Mitigazione e difesa
1. Non salvare dati sensibili sul device se evitabile; preferire token effimeri recuperati a runtime.
2. Usare Android Keystore (con StrongBox quando disponibile) e iOS Keychain/Secure Enclave per chiavi e segreti.
3. Cifrare i dati a riposo con AES-GCM (mai ECB), IV casuali per messaggio, e chiavi mai hardcoded.
4. Per le password usare KDF moderni (Argon2id, scrypt, PBKDF2 con iterazioni elevate), mai hash semplici.
5. Disabilitare backup dei dati sensibili (`android:allowBackup="false"`, exclusion list iOS) e ripulire cache/log.

## Lab
- DIVA (Insecure Data Storage parts 1-4) e InsecureBankv2 per Android.
- OWASP iGoat-Swift e DVIA-v2 per Keychain/plist su iOS.
- OWASP MASTG capitoli STORAGE e CRYPTO con i relativi test.
- [[TryHackMe]] room mobile su data storage; [[HackTheBox]] challenge con DB/segreti estraibili da APK.

## Domande
**D:** Perché SharedPreferences è un punto di rischio?
R: È un file XML in chiaro nel sandbox: protetto da altre app ma leggibile con root, backup o run-as in debug.

**D:** Qual è l'errore crypto dietro l'uso di AES/ECB?
R: ECB cifra blocchi identici allo stesso modo, leakando pattern del plaintext; va usato un mode autenticato come GCM con IV casuale.

**D:** Dove deve risiedere la chiave crittografica su mobile?
R: In Android Keystore (TEE/StrongBox) o iOS Keychain/Secure Enclave, così il materiale non lascia l'hardware sicuro.

**D:** Perché hashare le password con MD5/SHA1 è insufficiente?
R: Sono veloci e senza salt/work factor adeguati: vulnerabili a brute force e rainbow table; servono KDF come Argon2/scrypt/PBKDF2.

## Approfondimento livello esperto
Anche con Keystore, la chiave è usabile dal processo dell'app: un attaccante con Frida può hookare `Cipher.doFinal`/`Cipher.init` e catturare plaintext e (per chiavi software) il materiale, oppure invocare le API di decryption direttamente — il Keystore protegge l'estrazione della chiave, non l'uso da parte di un processo compromesso. Mitigazione forte: legare le operazioni a `setUserAuthenticationRequired(true)` con biometria e `setUnlockedDeviceRequired(true)`, e usare StrongBox per attestazione hardware. Su iOS, scegliere la classe Keychain corretta è critico: `kSecAttrAccessibleAlways` (deprecata) o `AfterFirstUnlock` espone i dati a estrazione da backup/lockscreen; preferire `WhenUnlockedThisDeviceOnly` + `SecAccessControl` biometrico. Per l'analisi forense, i dati cancellati possono persistere in WAL di SQLite (`-wal`, `-shm`) e in journal: controllarli sempre. OPSEC del tester: documentare il path esatto e la classe di protezione. MASVS-STORAGE-1/2 e MASVS-CRYPTO-1/2 (L1) coprono questi punti: la presenza di segreti recuperabili è un FAIL anche a livello base.

## Collegamenti
- [[Fondamenti Mobile]]
- [[Android Pentest]]
- [[iOS Pentest]]
- [[OWASP MASVS e MASTG]]
- [[Intercettazione traffico e API mobile]]
- [[Cookie e JWT]]
- [[OWASP Top 10]]
- [[Penetration Testing]]

## Fonti
- OWASP MASTG Data Storage Testing: https://mas.owasp.org/MASTG/
- Android Keystore System: https://developer.android.com/privacy-and-security/keystore
- HackTricks - Android Data Storage: https://book.hacktricks.xyz/mobile-pentesting/android-app-pentesting#insecure-data-storage
