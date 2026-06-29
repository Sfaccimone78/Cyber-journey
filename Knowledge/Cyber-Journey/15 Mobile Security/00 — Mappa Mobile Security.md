---
tipo: sintesi
tag: [mobile, moc]
fase: 3
fonti: 0
aggiornato: 2026-06-28
stato: maturo
aliases: ["Mobile Security", "Mappa Mobile Security"]
---

# Mobile Security - Mappa

Area **avanzata/expert** (fase 3-4) dedicata alla sicurezza delle applicazioni mobili **Android** e
**iOS**. Il filo conduttore parte dall'architettura delle due piattaforme (sandbox, permessi,
firma del codice), passa al pentest pratico di APK e IPA con strumentazione dinamica
(**Frida**/**Objection**), formalizza il metodo con [[OWASP MASVS e MASTG]], e chiude con i due
problemi più ricorrenti sul campo: l'**intercettazione del traffico** verso le API e l'**insecure
data storage**.

**Filo conduttore:** prima capisci *come è isolata un'app* ([[Fondamenti Mobile]]), poi smonti il
client su [[Android Pentest]] e [[iOS Pentest]]; standardizzi le verifiche con
[[OWASP MASVS e MASTG]]; infine attacchi i due lati esposti — il **canale** verso il backend
([[Intercettazione traffico e API mobile]]) e i **dati a riposo** sul device
([[Insecure Data Storage e Crypto su mobile]]).

## Percorso in ordine d'apprendimento

1. [[Fondamenti Mobile]] — architettura Android/iOS, sandbox, modello permessi, code signing
2. [[Android Pentest]] — APK, `adb`, smali/baksmali, Frida/Objection, rooting
3. [[iOS Pentest]] — IPA, jailbreak, Keychain, strumentazione dinamica
4. [[OWASP MASVS e MASTG]] — standard di verifica e metodologia di test
5. [[Intercettazione traffico e API mobile]] — Burp, proxy, bypass del certificate pinning
6. [[Insecure Data Storage e Crypto su mobile]] — storage locale, Keychain/Keystore, crypto errata

## Collegamenti trasversali
- [[OWASP Top 10]] — il web Top 10 a confronto col MASVS
- [[API & GraphQL Security]] — il backend che le app mobili consumano
- [[Penetration Testing]] — metodologia generale
- [[Cookie e JWT]] — token e sessioni usati anche dai client mobili
- [[Reverse Engineering]] — la base teorica del reversing di binari mobili

## Navigazione
[[00 — Mappa DFIR e Detection Engineering|14 DFIR e Detection Engineering]] <- [[index|Indice]] -> [[00 — Mappa Wireless & Radio|16 Wireless & Radio]]
