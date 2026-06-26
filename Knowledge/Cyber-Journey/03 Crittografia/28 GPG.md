---
tipo: concetto
tag: [crypto]
fase: 1
fonti: 2
aggiornato: 2026-06-26
stato: maturo
aliases: ["GPG", "GnuPG", "OpenPGP", "PGP"]
---

# GPG

## Definizione
**GPG** (*GNU Privacy Guard*) è l'implementazione libera dello standard **OpenPGP** (RFC 4880/9580), nato da **PGP** (*Pretty Good Privacy*, Phil Zimmermann, 1991). Serve a **cifrare** e **firmare** dati — file, email, commit Git, pacchetti software — combinando primitive simmetriche e asimmetriche. È il punto in cui la teoria crittografica diventa tool quotidiano su Linux.

## Crittografia ibrida (il cuore)
Cifrare tutto in asimmetrico sarebbe lentissimo: GPG usa lo schema **ibrido** (come [[TLS e SSL]]):

1. Genera una **session key** simmetrica casuale (AES-256) → [[AES]].
2. Cifra il **messaggio** con quella (veloce, AEAD) → [[Authenticated Encryption (AEAD)]].
3. Cifra la **session key** con la **chiave pubblica** del destinatario → [[RSA]] o [[Crittografia a Curve Ellittiche (ECC)]].
4. Invia *(session key cifrata + messaggio cifrato)*. Solo chi ha la **chiave privata** recupera la session key e decifra.

> Insight: la confidenzialità si basa sull'asimmetrico solo per **trasportare una chiave** (come [[Scambio di Chiavi Diffie-Hellman]] nello spirito), non per cifrare i dati.

## I due usi fondamentali

| Operazione | Garantisce | Come |
|------------|-----------|------|
| **Encrypt** (chiave pubblica del destinatario) | **confidenzialità** | ibrido: solo il destinatario decifra |
| **Sign** (propria chiave privata) | **autenticità + integrità + non-ripudio** | hash del messaggio ([[Funzioni di Hash]]) cifrato con la privata; chiunque verifica con la pubblica |

Spesso combinati: **firma + cifra** (autentico *e* segreto). La firma è il duale asimmetrico del [[MAC e HMAC]] (che invece usa una chiave condivisa).

## Web of Trust vs PKI
GPG **non** usa le Certificate Authority gerarchiche di [[TLS e SSL]] (X.509/PKI). Adotta il **Web of Trust**: gli utenti **firmano** a vicenda le chiavi, costruendo fiducia decentralizzata e transitiva. Ogni chiave ha un **fingerprint** (hash della chiave pubblica) da verificare **fuori banda** prima di fidarsi. La **revoca** avviene con un *revocation certificate* da generare in anticipo.

## Comandi essenziali
```bash
gpg --full-generate-key                 # crea coppia (consigliato: ECC/Ed25519 o RSA 4096)
gpg --list-keys / --list-secret-keys    # elenca chiavi
gpg --fingerprint utente@mail           # mostra fingerprint da verificare
gpg --export -a utente@mail > pub.asc   # esporta chiave pubblica (ASCII armor)
gpg --import pub.asc                     # importa una chiave altrui

gpg -e -r dest@mail file.txt            # cifra per un destinatario  → file.txt.gpg
gpg -d file.txt.gpg                      # decifra (richiede la propria privata)
gpg -s file.txt                          # firma (binaria)
gpg --clear-sign nota.txt                # firma mantenendo il testo leggibile
gpg --verify file.sig                    # verifica una firma
```

## Dove si incontra nella pratica
- **Firma dei pacchetti**: apt/dnf/pacman verificano le firme GPG dei repository (difesa supply-chain).
- **Email cifrata** (PGP/MIME) e **firma dei commit Git**.
- **Cifrare credenziali/segreti** a riposo (es. il password manager `pass`).
- Sottostà alla fiducia crittografica anche di SSH (modello di chiavi affine).

## Limiti e alternative moderne
PGP è criticato per **UX complessa**, mancanza di *forward secrecy* e metadati esposti. Implementazioni moderne: **Sequoia-PGP**; per la sola cifratura file l'alternativa minimalista è **age**. Per la messaggistica si preferiscono protocolli con forward secrecy (Signal).

## Collegamenti
- [[TLS e SSL]] — altro schema ibrido, ma con PKI gerarchica
- [[RSA]] · [[Crittografia a Curve Ellittiche (ECC)]] — chiavi asimmetriche usate
- [[Scambio di Chiavi Diffie-Hellman]] — lo stesso spirito "trasporta una chiave"
- [[AES]] · [[Authenticated Encryption (AEAD)]] — cifratura della session key/dati
- [[Funzioni di Hash]] · [[MAC e HMAC]] — firme e integrità
- [[OpenSSL]] — l'altro coltellino svizzero crittografico da CLI
- [[00 — Mappa Crittografia|Mappa Crittografia]]

## Fonti
- GnuPG — Documentation: https://www.gnupg.org/documentation/
- Crypto 101 (Laurens Van Houtven), crittografia asimmetrica e ibrida: https://crypto101.io/
