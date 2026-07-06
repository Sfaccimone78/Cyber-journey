---
tipo: concetto
tag: [fondamenti]
fase: 0
fonti: 3
aggiornato: 2026-07-02
stato: maturo
aliases: ["IAM e Zero Trust"]
---

# IAM e Zero Trust

## In breve
L'**IAM** (Identity and Access Management) è l'insieme di processi e tecnologie che gestiscono **chi può accedere a cosa**. Lo **Zero Trust** è il modello architetturale moderno che ne porta i principi all'estremo: *"never trust, always verify"* — nessun utente o dispositivo è fidato per default, nemmeno dentro la rete aziendale.

## I pilastri dell'IAM (le "4 A")
- **Identificazione**: dichiarare chi sei (username).
- **Autenticazione**: provarlo (password, **MFA**, biometria, chiavi).
- **Autorizzazione**: cosa puoi fare (RBAC, [[Permessi Linux|permessi]]).
- **Accounting/Audit**: tracciare cosa hai fatto (log).

### Fattori di autenticazione (MFA)
- **Qualcosa che sai** (password, PIN)
- **Qualcosa che hai** (token, app TOTP, security key FIDO2)
- **Qualcosa che sei** (impronta, volto)

L'**MFA** combina almeno due fattori ed è la singola contromisura più efficace contro il furto di credenziali da [[Social Engineering e Phishing|phishing]].

## Principi Zero Trust
- **Verifica esplicita** di ogni richiesta (identità, dispositivo, contesto).
- **Least privilege**: accesso minimo necessario (vedi [[Difesa in Profondità]]).
- **Assume breach**: progetta come se l'attaccante fosse già dentro → micro-segmentazione, limitare il [[Lateral Movement|movimento laterale]].

## Esempio pratico
In un modello Zero Trust, un dipendente che accede a un'app SaaS non è autorizzato solo perché è "in ufficio": il sistema verifica identità + MFA, **postura del dispositivo** (patch, antivirus), posizione e rischio della sessione, concedendo accesso solo a quella specifica risorsa. Strumenti: Okta/Entra ID (IdP), SSO + Conditional Access.

## Perché conta
La maggior parte delle violazioni gravi sfrutta **credenziali valide** (vedi [[Pass-the-Hash]], [[NTLM]]). IAM forte + MFA + Zero Trust riducono drasticamente l'impatto del furto di identità e contengono la propagazione di un attacco.

## Lab
- **[[TryHackMe]]** → room *Active Directory Basics* e *Windows Fundamentals*: osserva come identità, gruppi e RBAC governano "chi può accedere a cosa".
- **MFA hands-on**: configura un TOTP (Google Authenticator/Authy) su un account di test e poi una security key FIDO2, notando perché la seconda è phishing-resistant.
- **Entra ID free tier**: crea un tenant Microsoft Entra ID di prova e imposta una regola di *Conditional Access* (es. richiedi MFA da fuori rete) per toccare con mano la "verifica esplicita" di Zero Trust.

## Domande
1. **D:** Cosa significa lo slogan Zero Trust "never trust, always verify"? **R:** Nessun utente o dispositivo è fidato per default, nemmeno dentro la rete aziendale: ogni richiesta va verificata esplicitamente.
2. **D:** Quali sono le "4 A" dell'IAM? **R:** Identificazione (chi sei), Autenticazione (provarlo), Autorizzazione (cosa puoi fare), Accounting/Audit (tracciare cosa hai fatto).
3. **D:** Quali sono i tre fattori di autenticazione? **R:** Qualcosa che sai (password/PIN), qualcosa che hai (token/TOTP/FIDO2), qualcosa che sei (biometria).
4. **D:** Quali sono i tre principi cardine di Zero Trust? **R:** Verifica esplicita di ogni richiesta, least privilege e assume breach (micro-segmentazione per limitare il movimento laterale).
5. **D:** Perché IAM forte e MFA contano tanto? **R:** Perché la maggior parte delle violazioni gravi sfrutta credenziali valide; MFA e Zero Trust riducono l'impatto del furto di identità e contengono la propagazione.

## Collegamenti
- [[Difesa in Profondità]]
- [[Social Engineering e Phishing]]
- [[Autenticazione e Gestione Sessioni]]
- [[Lateral Movement]]
- [[Triade CIA]]
- [[Active Directory]]

## Fonti
- NIST SP 800-207 — Zero Trust Architecture: https://csrc.nist.gov/publications/detail/sp/800-207/final
- CISA — Zero Trust Maturity Model: https://www.cisa.gov/zero-trust-maturity-model
- Microsoft — What is Zero Trust?: https://learn.microsoft.com/en-us/security/zero-trust/zero-trust-overview
