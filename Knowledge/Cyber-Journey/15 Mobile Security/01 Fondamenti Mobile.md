---
tipo: concetto
tag: [mobile]
fase: 3
fonti: 3
aggiornato: 2026-06-28
stato: maturo
aliases: ["Fondamenti Mobile"]
---

# Fondamenti Mobile

## In breve
La mobile security riguarda la protezione di applicazioni e dati su dispositivi Android e iOS, dove il modello di minaccia cambia rispetto al web: il dispositivo è fisicamente in mano all'utente (potenzialmente attaccante) e l'app gira in un ambiente parzialmente controllabile. Categoria: sicurezza applicativa client-side. Impatto: furto di credenziali, esfiltrazione di dati locali, abuso di API backend.

## Come funziona
Entrambe le piattaforme isolano le app con un **sandbox** a livello kernel: ogni app ha una UID dedicata (Android, basato su Linux) o un container (iOS, basato su Darwin/XNU). Android distribuisce APK/AAB con bytecode DEX eseguito su ART (Android Runtime, AOT/JIT); iOS distribuisce IPA con binari Mach-O nativi ARM compilati e firmati. Il modello di permessi è dichiarativo (`AndroidManifest.xml` / `Info.plist` + entitlements) e runtime (grant utente). Il rooting (Android) o jailbreak (iOS) rimuove le barriere del sandbox, permettendo lettura della memoria, hook runtime e accesso al filesystem completo: condizione abilitante per quasi tutto il pentest dinamico.

A basso livello la superficie d'attacco comprende: storage locale (SQLite, SharedPreferences, Keychain), IPC (Intent, deep link, URL scheme, Binder), traffico di rete verso le API, e il binario stesso (reverse engineering, tampering).

## Esempi
```bash
# Android: info sul dispositivo e pacchetti installati
adb devices -l
adb shell getprop ro.build.version.release
adb shell pm list packages -3        # solo app di terze parti
adb shell pm path com.example.app    # percorso dell'APK sul device

# Estrarre un APK dal device per analisi
adb shell pm path com.example.app
adb pull /data/app/com.example.app-1/base.apk .

# Ispezionare il manifest e i permessi
aapt dump badging base.apk | grep -E "package|permission"

# iOS: enumerare le app installate (device jailbroken via SSH)
ssh root@127.0.0.1 -p 2222 "ls /var/containers/Bundle/Application/"
frida-ps -Uai                        # app installate, anche su iOS non-jailbroken con app patchata
```

## Mitigazione e difesa
1. Non memorizzare segreti o dati sensibili sul dispositivo; se necessario usare Keystore/Keychain con protezione hardware (TEE/Secure Enclave).
2. Minimizzare i permessi richiesti nel manifest e usare permessi runtime con scope ridotto.
3. Applicare jailbreak/root detection e tamper detection (consapevoli che è defense-in-depth, non barriera assoluta).
4. Validare tutto lato server: il client mobile è untrusted per definizione.
5. Offuscare il codice (R8/ProGuard, obfuscation iOS) per alzare il costo del reverse engineering.

## Lab
- [[TryHackMe]] room "Android Hacking 101" e "Mobile" per fondamenti pratici.
- OWASP MASTG crackmes (Android UnCrackable L1-L4, iOS UnCrackable) per RE e bypass.
- DIVA (Damn Insecure and Vulnerable App) e InsecureBankv2 per Android.
- OWASP iGoat-Swift per iOS.
- [[HackTheBox]] challenge della categoria Mobile.

## Domande
**D:** Perché il dispositivo mobile è considerato un ambiente ostile nel modello di minaccia?
R: Perché è fisicamente in possesso dell'utente, che può rootare/jailbreakare, ispezionare storage e memoria e manipolare il runtime: tutto ciò che è sul client è ispezionabile.

**D:** Che differenza c'è tra il formato eseguibile di Android e iOS?
R: Android usa bytecode DEX eseguito da ART; iOS usa binari Mach-O nativi ARM firmati.

**D:** Cosa abilita root/jailbreak per il pentester?
R: Accesso completo al filesystem, lettura memoria, hooking runtime (Frida) e bypass del sandbox.

**D:** Dove si dichiarano permessi ed entitlement?
R: `AndroidManifest.xml` su Android, `Info.plist` ed entitlements sul binario firmato su iOS.

## Approfondimento livello esperto
Il sandboxing non protegge da un attaccante locale con privilegi root: su Android SELinux in modalità enforcing limita anche root, ma i custom ROM spesso lo allentano. Per OPSEC durante un assessment, usare emulatori (genymotion, Android Studio AVD con immagini Google APIs senza Play per evitare attestazioni SafetyNet/Play Integrity) o device dedicati mai loggati con account personali. La **Play Integrity API** e la **DeviceCheck/App Attest** di Apple introducono attestazione hardware-backed lato server: rilevano emulatori e root, e vanno aggirate a livello di risposta server o con moduli come Magisk DenyList + Zygisk. Il livello MASVS-L2 richiede protezioni resilienti (R) contro tampering e reversing: anti-debug, anti-hooking, integrity check del binario. Caso limite: app cross-platform (Flutter, React Native) cambiano la superficie — il codice Dart/JS bundle è spesso più facile da estrarre del nativo.

## Collegamenti
- [[Android Pentest]]
- [[iOS Pentest]]
- [[OWASP MASVS e MASTG]]
- [[Intercettazione traffico e API mobile]]
- [[Insecure Data Storage e Crypto su mobile]]
- [[OWASP Top 10]]
- [[Penetration Testing]]
- [[Reverse Engineering]]

## Fonti
- OWASP Mobile Application Security: https://mas.owasp.org/
- Android Application Fundamentals: https://developer.android.com/guide/components/fundamentals
- HackTricks Mobile Pentesting: https://book.hacktricks.xyz/mobile-pentesting
