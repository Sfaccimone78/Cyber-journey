#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_index.py — Single source of truth per la sezione "Contenuto per area" di index.md.

Scansiona le cartelle d'area NN <Area>/ della wiki Cyber-Journey ed elenca, per ogni area,
le note reali sul disco (ordinate per numero), usando il "nome senza numero" (alias[0] del
frontmatter; fallback: nome-file completo). Rigenera la regione delimitata dai marker
<!-- AUTO-INDEX:START --> ... <!-- AUTO-INDEX:END --> e aggiorna il conteggio in testa.

Uso:
  python tools/gen_index.py            # --check: riporta la deriva, NON scrive
  python tools/gen_index.py --write    # rigenera la regione + il conteggio in index.md

Esci con codice 1 in --check se c'è deriva (utile in un hook/CI).
"""
import os, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(os.path.dirname(HERE), "Knowledge", "Cyber-Journey")
INDEX = os.path.join(ROOT, "index.md")

START = "<!-- AUTO-INDEX:START — generato da tools/gen_index.py; non modificare a mano -->"
END = "<!-- AUTO-INDEX:END -->"

# num_cartella -> (emoji, titolo mostrato, expert?)
AREAS = {
    "00": ("🟢", "Fondamenti", False),
    "01": ("🌐", "Reti", False),
    "02": ("🐧", "Linux", False),
    "03": ("🔐", "Crittografia", False),
    "04": ("🪟", "Windows e AD", False),
    "05": ("🕸️", "Web / OWASP", False),
    "06": ("🎯", "Metodologia e Tool", False),
    "07": ("🛡️", "Blue Team", False),
    "08": ("⚙️", "Sistemi Operativi", False),
    "09": ("🐍", "Python", False),
    "10": ("🧮", "Algoritmi e Strutture Dati", False),
    "11": ("☁️", "Cloud Security", True),
    "12": ("🧪", "AppSec Avanzato", True),
    "13": ("🔬", "Reverse Engineering e Exploit Dev", True),
    "14": ("🔎", "DFIR e Detection Engineering", True),
    "15": ("📱", "Mobile Security", True),
    "16": ("📶", "Wireless & Radio", True),
    "17": ("🔌", "API e GraphQL Security", True),
    "18": ("🤖", "AI e LLM Security", True),
    "19": ("🔁", "DevSecOps e Supply Chain", True),
    "20": ("📋", "GRC e Compliance", True),
    "21": ("🕵️", "OSINT e Social Engineering", True),
    "22": ("📟", "Hardware e IoT Security", True),
    "23": ("🚩", "Laboratori e CTF", True),
}


def read(p):
    for e in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            with open(p, encoding=e) as fh:
                return fh.read()
        except Exception:
            continue
    return ""


def get_aliases(text):
    """Estrae gli alias sia in forma inline (aliases: [..]) sia a blocco (aliases:\\n  - ..)."""
    m = re.search(r"(?m)^aliases?\s*:\s*\[(.*?)\]", text)
    if m:
        items = [(a or b).strip() for a, b in re.findall(r'"([^"]*)"|\'([^\']*)\'', m.group(1))]
        items = [i for i in items if i]
        if items:
            return items
        return [x.strip() for x in m.group(1).split(",") if x.strip()]
    m = re.search(r"(?m)^aliases?\s*:\s*$", text)
    if m:
        out, started = [], False
        for line in text[m.end():].splitlines():
            if re.match(r"^\s*-\s+", line):
                v = re.sub(r"^\s*-\s+", "", line).strip().strip("\"'")
                if v:
                    out.append(v)
                started = True
            elif line.strip() == "" and not started:
                continue  # salta la riga vuota subito dopo "aliases:"
            else:
                break
        return out
    return []


def first_alias(text):
    al = get_aliases(text)
    return al[0] if al else None


def build_resolvable():
    """Insieme (lowercase) di tutti i target risolvibili in Obsidian: nomi-file + alias."""
    res = set()
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            if not f.endswith(".md"):
                continue
            res.add(f[:-3].lower())
            for a in get_aliases(read(os.path.join(dp, f))):
                res.add(a.lower())
    return res


def scan():
    """area_num -> lista ordinata di (numero, display_name). Il display è sempre risolvibile."""
    resolvable = build_resolvable()
    result = {}
    for area_num, (emoji, title, expert) in AREAS.items():
        folder = None
        for d in os.listdir(ROOT):
            if d.startswith(area_num + " ") and os.path.isdir(os.path.join(ROOT, d)):
                folder = os.path.join(ROOT, d)
                break
        notes = []
        if folder:
            for f in os.listdir(folder):
                if not f.endswith(".md"):
                    continue
                base = f[:-3]
                if re.match(r"^00\s*[-—]", base):  # escludi le MOC
                    continue
                nm = re.match(r"^(\d+)", base)
                order = int(nm.group(1)) if nm else 9999
                alias = first_alias(read(os.path.join(folder, f)))
                strip = re.sub(r"^\d+\s+", "", base)  # nome senza prefisso NN
                # alias[0] = nome canonico curato (accenti inclusi); poi strip se risolve; infine nome-file
                if alias:
                    display = alias
                elif strip.lower() in resolvable:
                    display = strip
                else:
                    display = base
                notes.append((order, base, display))
        notes.sort(key=lambda x: (x[0], x[1]))
        result[area_num] = [(o, d) for (o, _b, d) in notes]
    return result


def render(data):
    basic, expert = [], []
    for area_num in sorted(AREAS):
        emoji, title, is_expert = AREAS[area_num]
        notes = data[area_num]
        header = f"### {emoji} {area_num} {title}"
        if notes:
            body = " · ".join(f"[[{d}]]" for _o, d in notes)
        else:
            body = "*(area in costruzione — vedi la Mappa)*"
        block = f"{header}\n{body}"
        (expert if is_expert else basic).append(block)
    out = "\n\n".join(basic)
    out += "\n\n---\n\n## 🚀 Aree avanzate (expert)\n\n"
    out += "> Livello fase 3-4. Vedi [[Analisi e Roadmap Expert]].\n\n"
    out += "\n\n".join(expert)
    return out


def total_notes(data):
    return sum(len(v) for v in data.values())


def apply_write(data):
    txt = read(INDEX)
    region = f"{START}\n{render(data)}\n{END}"

    if START in txt and END in txt:
        txt = re.sub(re.escape(START) + r".*?" + re.escape(END), region, txt, flags=re.S)
    else:
        # prima installazione: rimpiazza da "### <emoji> 00 Fondamenti" fino a prima di "## 🧭 Sintesi"
        m_start = re.search(r"(?m)^### .+ 00 Fondamenti\s*$", txt)
        m_end = txt.find("## 🧭 Sintesi")
        if not m_start or m_end == -1:
            print("ERRORE: ancore non trovate in index.md (### … 00 Fondamenti / ## 🧭 Sintesi).")
            return False
        # includi il '---' che precede la sezione Sintesi
        pre = txt.rfind("---", m_start.start(), m_end)
        cut_end = pre if pre != -1 else m_end
        txt = txt[: m_start.start()] + region + "\n\n---\n\n" + txt[m_end:]

    # aggiorna il conteggio in testa
    n = total_notes(data)
    a = len(AREAS)
    txt = re.sub(r"\*\*[~\d]+\s*pagine\*\* in \d+ aree",
                 f"**{n} pagine** in {a} aree", txt, count=1)

    with open(INDEX, "w", encoding="utf-8") as fh:
        fh.write(txt)
    print(f"index.md rigenerato: {n} note in {a} aree.")
    return True


def check(data):
    txt = read(INDEX)
    n = total_notes(data)
    print(f"Note totali sul disco: {n} in {len(AREAS)} aree")
    drift = False
    for area_num in sorted(AREAS):
        emoji, title, _ = AREAS[area_num]
        disk = [d for _o, d in data[area_num]]
        # cosa risulta linkato nell'index per quest'area (riga sotto l'header)
        m = re.search(r"(?m)^### .+ " + area_num + r" " + re.escape(title) + r"\s*$", txt)
        linked = set()
        if m:
            tail = txt[m.end(): m.end() + 4000]
            tail = tail.split("\n###", 1)[0].split("\n## ", 1)[0]
            linked = set(re.findall(r"\[\[([^\]|#]+)", tail))
        missing = [d for d in disk if d not in linked]
        if missing:
            drift = True
            print(f"  [{area_num} {title}] mancano da index.md: " + ", ".join(missing))
    if not drift:
        print("OK — nessuna deriva: ogni nota su disco è già in index.md.")
    return drift


if __name__ == "__main__":
    data = scan()
    if "--write" in sys.argv:
        ok = apply_write(data)
        sys.exit(0 if ok else 2)
    else:
        sys.exit(1 if check(data) else 0)
