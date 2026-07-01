#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_notes.py — Gate "Definition of Done" anti-islands per la wiki Cyber-Journey.

Verifica che ogni nota con `stato: maturo` non sia un'isola e rispetti il minimo
dello Standard Nota Esperto (WIKI_SCHEMA.md). Pensato per girare come hook pre-commit.

ERRORI (bloccano il commit) su una nota `maturo`:
  - WIKILINK : nessun [[wikilink]] nel corpo (era il sintomo del dump-merge).
  - COLLEG   : manca la sezione `## Collegamenti`.
  - FONTI    : manca `## Fonti` oppure ha < 2 voci fonte.
  - IN-MOC   : la nota non è linkata dalla Mappa (MOC) della sua area.

AVVISI (non bloccano): sezioni In breve / Lab / Domande assenti; `fonti:` != conteggio reale.

Uso:
  python tools/check_notes.py             # report su tutto il vault
  python tools/check_notes.py --staged    # solo i .md in stage (hook pre-commit)
  python tools/check_notes.py --strict     # tratta anche gli AVVISI come errori
Esce ≠0 se c'è almeno un ERRORE (o un AVVISO in --strict).
"""
import os, re, sys, io, subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ROOT = os.path.join(REPO, "Knowledge", "Cyber-Journey")


def read(p):
    for e in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            with open(p, encoding=e) as fh:
                return fh.read()
        except Exception:
            continue
    return ""


def get_aliases(text):
    m = re.search(r"(?m)^aliases?\s*:\s*\[(.*?)\]", text)
    if m:
        items = [(a or b).strip() for a, b in re.findall(r'"([^"]*)"|\'([^\']*)\'', m.group(1))]
        items = [i for i in items if i]
        return items or [x.strip() for x in m.group(1).split(",") if x.strip()]
    m = re.search(r"(?m)^aliases?\s*:\s*$", text)
    if m:
        out, started = [], False
        for line in text[m.end():].splitlines():
            if re.match(r"^\s*-\s+", line):
                out.append(re.sub(r"^\s*-\s+", "", line).strip().strip("\"'"))
                started = True
            elif line.strip() == "" and not started:
                continue
            else:
                break
        return [x for x in out if x]
    return []


def frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def body(text):
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.S)
    return text[m.end():] if m else text


def strip_code(t):
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    return re.sub(r"`[^`]*`", "", t)


def area_moc_links(area_dir):
    """Insieme (lowercase) dei target [[..]] presenti in TUTTE le mappe 00— dell'area."""
    links = set()
    for f in os.listdir(area_dir):
        if re.match(r"^00\s*[-—]", f) and f.endswith(".md"):
            txt = read(os.path.join(area_dir, f))
            for m in re.findall(r"\[\[([^\]]+?)\]\]", txt):
                links.add(m.split("|")[0].split("#")[0].strip().lower())
    return links


def fonti_count(text):
    # heading tollerante: accetta '## Fonti', '## 📚 Fonti', '## Fonti primarie'…
    m = re.search(r"(?mi)^#{2,}[^\n]*\bFonti\b", text)
    if not m:
        return 0
    tail = text[m.end():]
    tail = re.split(r"(?m)^##+\s", tail, maxsplit=1)[0]
    n = 0
    for ln in tail.splitlines():
        if re.match(r"^\s*(?:[-*]|\d+[.)])\s+\S", ln) or "http" in ln:
            n += 1
    return n


def check_note(path):
    """Ritorna (errors, warnings) per una nota. Salta MOC/template/non-maturo."""
    name = os.path.basename(path)
    if re.match(r"^00\s*[-—]", name) or "template" in path.lower():
        return [], []
    txt = read(path)
    fm = frontmatter(txt)
    st = re.search(r"(?m)^stato\s*:\s*(\w+)", fm)
    if not st or st.group(1) != "maturo":
        return [], []
    # il gate vale solo per le note-contenuto (concetto/entita); sintesi/fonte/MOC esclusi
    tp = re.search(r"(?m)^tipo\s*:\s*(\w+)", fm)
    if not tp or tp.group(1) not in ("concetto", "entita"):
        return [], []

    b = body(txt)
    bc = strip_code(b)
    errors, warns = [], []

    if not re.search(r"\[\[[^\]]+\]\]", bc):
        errors.append("WIKILINK: nessun [[link]] nel corpo")
    # heading tollerante: accetta '## Collegamenti', '## 🔗 Collegamenti', '## Collegamenti con la teoria'…
    if not re.search(r"(?mi)^#{2,}[^\n]*\bCollegamenti\b", b):
        errors.append("COLLEG: manca '## Collegamenti'")
    fc = fonti_count(b)
    if fc < 2:
        errors.append(f"FONTI: '## Fonti' con {fc} voci (min 2)")

    # presenza in MOC d'area
    area_dir = os.path.dirname(path)
    if re.match(r"^\d\d ", os.path.basename(area_dir)):
        moc = area_moc_links(area_dir)
        names = set(a.lower() for a in get_aliases(txt))
        names.add(name[:-3].lower())
        names.add(re.sub(r"^\d+\s+", "", name[:-3]).lower())
        if moc and not (names & moc):
            errors.append("IN-MOC: non linkata dalla Mappa d'area")

    # avvisi (non bloccanti)
    for sec in ("In breve", "Lab", "Domande"):
        if not re.search(r"(?mi)^##+\s*" + re.escape(sec) + r"\b", b):
            warns.append(f"sezione '## {sec}' assente")
    mf = re.search(r"(?m)^fonti\s*:\s*(\d+)", fm)
    if mf and fc and int(mf.group(1)) != fc:
        warns.append(f"frontmatter fonti:{mf.group(1)} != {fc} voci reali")

    return errors, warns


def staged_files():
    out = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                         cwd=REPO, capture_output=True, text=True).stdout
    files = []
    for line in out.splitlines():
        line = line.strip()
        if line.endswith(".md") and line.startswith("Knowledge/Cyber-Journey/"):
            files.append(os.path.join(REPO, line))
    return files


def all_notes():
    files = []
    for dp, dn, fn in os.walk(ROOT):
        if "Template" in dp:
            continue
        for f in fn:
            if f.endswith(".md"):
                files.append(os.path.join(dp, f))
    return files


if __name__ == "__main__":
    strict = "--strict" in sys.argv
    targets = staged_files() if "--staged" in sys.argv else all_notes()
    n_err = n_warn = n_bad = 0
    for p in sorted(targets):
        if not os.path.exists(p):
            continue
        errs, warns = check_note(p)
        if errs or (warns and strict):
            n_bad += 1
            rel = os.path.relpath(p, ROOT)
            print(f"\n✗ {rel}")
            for e in errs:
                print(f"    ERRORE  {e}"); n_err += 1
            for w in warns:
                print(f"    avviso  {w}"); n_warn += 1
        elif warns:
            n_warn += len(warns)
    scope = "staged" if "--staged" in sys.argv else "vault"
    print(f"\n[{scope}] note con problemi: {n_bad} · errori: {n_err} · avvisi: {n_warn}")
    fail = n_err > 0 or (strict and n_warn > 0)
    if fail:
        print("GATE: FALLITO — sistema le note sopra o abbassa stato a 'attivo'.")
    else:
        print("GATE: OK.")
    sys.exit(1 if fail else 0)
