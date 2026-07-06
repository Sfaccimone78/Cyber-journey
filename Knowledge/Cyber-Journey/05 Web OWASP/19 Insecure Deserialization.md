---
tipo: concetto
tag: [web, owasp]
fase: 3
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Insecure Deserialization", "Deserializzazione Insicura"]
---

# Insecure Deserialization

> **Nota etica**: praticare solo su lab autorizzati (PortSwigger, CTF).

## In breve
La **deserializzazione insicura** avviene quando l'app ricostruisce oggetti da dati serializzati **controllati dall'utente** senza validarli. Va dalla manomissione di stato (privilege escalation) all'**RCE** tramite *gadget chain*. Categoria **A08 Software & Data Integrity Failures** dell'[[OWASP Top 10]].

## Serializzazione e magic methods
Serializzare = oggetto → stringa/byte trasportabile; deserializzare = il contrario. Il pericolo: alcuni linguaggi, durante la deserializzazione, invocano **automaticamente** metodi dell'oggetto:
| Linguaggio | API a rischio | Magic method |
|---|---|---|
| PHP | `unserialize()` | `__wakeup`, `__destruct` |
| Java | `ObjectInputStream.readObject` | `readObject` |
| Python | `pickle.loads` | `__reduce__` |
| .NET | `BinaryFormatter` | callback vari |
| Ruby | `Marshal.load` | — |

Se l'input serializzato torna dal client (cookie, parametro, token) → l'attaccante controlla lo stato **e** può innescare quei metodi.

## Esempio — tampering di stato (PHP)
```text
O:4:"User":2:{s:4:"name";s:5:"guest";s:7:"isAdmin";b:0;}   ← originale nel cookie
O:4:"User":2:{s:4:"name";s:5:"guest";s:7:"isAdmin";b:1;}   ← b:0 → b:1 = admin
```

## Esempio — RCE (Python pickle)
```python
import pickle, os
class Exploit:
    def __reduce__(self):
        return (os.system, ("id",))      # eseguito da pickle.loads() sul server
pickle.dumps(Exploit())
```

## Gadget chain (il caso RCE serio)
In Java/.NET raramente l'app ha un metodo che esegue comandi. Si concatenano **gadget** — classi già presenti nelle librerie (Commons-Collections, ecc.) — che, deserializzate in sequenza, finiscono per eseguire codice. **ysoserial** (Java) e **ysoserial.net** generano questi payload pronti. Log4Shell e molti RCE enterprise nascono qui.

## Come si individua
Riconoscere i formati nei dati che tornano dal client:
```
PHP:    O:4:"User":...           Java (base64): rO0AB...   (0xAC 0xED)
Python pickle: \x80\x04...        .NET: AAEAAAD/////
```
Modificarli con [[Burp Suite]]; estensione **Java Deserialization Scanner**.

## Mitigazione (priorità)
1. **Non deserializzare dati non fidati.** Se serve scambio dati, usa **JSON/formati puri** con parser che non istanziano classi arbitrarie.
2. **Integrità**: firma/HMAC sui dati serializzati → rileva la manomissione.
3. **Allow-list** delle classi deserializzabili; evitare `pickle`/`BinaryFormatter` su input esterni.
4. Monitorare gadget noti; aggiornare le librerie.

## Lab
- [[PortSwigger Web Academy]] → categoria **Insecure deserialization**. Percorso dal livello APPRENTICE:
  - *Modifying serialized objects* — tampering di stato PHP (`isAdmin` come nell'esempio sopra).
  - *Modifying serialized data types* e *Using application functionality to exploit insecure deserialization*.
  - *Arbitrary object injection in PHP* e *Exploiting Java deserialization with Apache Commons* (PRACTITIONER) — introduce le **gadget chain** e `ysoserial`.
- Cosa esercitare: riconoscere i formati serializzati (`O:4:"User"`, base64 `rO0AB...`), manometterli con [[Burp Suite]] (estensione *Java Deserialization Scanner*) e generare payload RCE con **ysoserial**.

## Domande
1. **D:** Perché la deserializzazione di dati non fidati può portare a RCE e non solo a tampering?  **R:** Molti linguaggi invocano automaticamente **magic method** durante la deserializzazione (`__wakeup`/`__destruct`, `readObject`, `__reduce__`); concatenando classi già presenti (gadget chain) si arriva a eseguire comandi.
2. **D:** Cos'è una gadget chain e a cosa serve ysoserial?  **R:** È una sequenza di classi di libreria che, deserializzate in ordine, finiscono per eseguire codice; ysoserial (Java) genera automaticamente questi payload per librerie note come Commons-Collections.
3. **D:** Come si riconosce un oggetto Java serializzato in transito?  **R:** Dai magic bytes `0xAC 0xED`, che in base64 iniziano con `rO0AB`.
4. **D:** Qual è la mitigazione primaria?  **R:** Non deserializzare dati non fidati: usare formati dati puri (JSON) con parser che non istanziano classi arbitrarie; in subordine, firma/HMAC per l'integrità e allow-list delle classi.
5. **D:** In che modo un semplice tampering PHP può dare privilege escalation senza RCE?  **R:** Modificando un attributo nell'oggetto serializzato nel cookie (es. `isAdmin;b:0` → `b:1`) si altera lo stato che l'app ricostruisce fidandosi del dato client.

## Collegamenti
- [[OWASP Top 10]]
- [[Cookie e JWT]]
- [[Command Injection]]
- [[Reverse Shell e Bind Shell]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti
- PortSwigger — Insecure deserialization: https://portswigger.net/web-security/deserialization
- OWASP — Deserialization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html
- OWASP — A08:2021: https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/
