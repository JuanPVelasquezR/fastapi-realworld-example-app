"""Markdown QA -> HTML (styled) -> PDF via headless Edge/Chrome.
Uso: python build_pdf.py "<entrada.md>" "<salida.pdf>"
"""
import re, subprocess, sys, pathlib, html
import markdown

here = pathlib.Path(__file__).parent
src = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2])
text = src.read_text(encoding="utf-8")

# --- limpieza de artefactos del markdown original ---

text = text.replace("\r\n", "\n")
def fix_analisis(text):
    text = re.sub(r"\$\s*ightarrow\$", "→", text)
    text = text.replace("\x0c", "/")
    pyr = (
        '<div class="pyrm"><div class="pyrm-shape"><div class="l1">36.6%</div><div class="l2">63.4%</div></div>'
        '<div class="pyrm-desc"><div class="d d1"><b>Capa superior · Manuales / Exploratorias</b><span>36.6% · 15 casos</span>'
        'Swagger UI, Postman, UX, mensajes y estados</div>'
        '<div class="d d2"><b>Base · Automatizadas de Integración</b><span>63.4% · 26 casos</span>'
        'pytest, PostgreSQL en Docker, pytest-cov (82.78% de cobertura)</div></div></div>')
    text = re.sub(r"\n`\n\s+/\s+/.*?-{5,}`\n", "\n\n" + pyr + "\n\n", text, flags=re.S)
    def mods(m):
        rows, cur = [], None
        for l in m.group(1).split("\n"):
            if not l.startswith("|"): continue
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if c[0]: cur = c; rows.append(cur)
            elif cur: cur[:] = [a + (" " + b if b else "") for a, b in zip(cur, c)]
        out = ["| Módulo | Casos | Bugs | Estado de madurez |", "|---|---|---|---|"]
        for r in rows[1:]:
            bugs = r[2]
            if bugs.startswith("BUG-02"): bugs = "BUG-02, BUG-03, BUG-04, BUG-07, BUG-08, BUG-09"
            cls = ("pass" if r[3].startswith(("Alta", "100%")) else "fail" if r[3].startswith(("Crítico", "Deficiente")) else "prog")
            head, _, tail = r[3].partition(",") if "," in r[3] else r[3].partition(":")
            sep = "," if "," in r[3] else ":"
            est = '<span class="badge %s">%s</span>%s' % (cls, head.strip(), (" " + tail.strip()) if tail else "")
            out.append("| **%s** | %s | %s | %s |" % (r[0], r[1], bugs if bugs != "Ninguno" else "—", est))
        return "\n" + "\n".join(out) + "\n"
    text = re.sub(r"\n`\n(\+-+\+-+.*?Módulo.*?)\n`\n", mods, text, flags=re.S)
    def risk(m):
        rows, cur, newrow = [], None, True
        for l in m.group(1).split("\n"):
            if l.startswith("+"): newrow = True; continue
            if not l.startswith("|"): continue
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) < 4: continue
            if c[0].startswith("MATRIZ") or c[0].startswith("Dimensi"): continue
            if cur is None or newrow: cur = [[x] if x else [] for x in c]; rows.append(cur); newrow = False
            else:
                for k in range(4):
                    if c[k]: cur[k].append(c[k])
        out = ['<div class="stlc-title" style="margin-top:6mm">MATRIZ DE RIESGO E IMPACTO EN EL NEGOCIO</div>', "",
               "| Dimensión de negocio | Defecto asociado | Nivel de riesgo | Impacto operativo / legal |", "|---|---|---|---|"]
        for r in rows:
            dim = " ".join(r[0]); bugs = "<br>".join(r[1])
            lvl = " ".join(r[2]).replace("**", "")
            cls = "fail" if lvl.startswith("CR") else "block" if "ALTO" in lvl else "prog" if lvl.startswith("MEDIO") else "pass"
            items, buf = [], None
            for x in r[3]:
                if x.startswith("- "): buf = x[2:]; items.append(buf)
                elif items: items[-1] += " " + x
            imp = "<ul>" + "".join("<li>%s</li>" % i for i in items) + "</ul>"
            out.append('| **%s** | %s | <span class="badge %s">%s</span> | %s |' % (dim, bugs, cls, lvl, imp))
        return "\n" + "\n".join(out) + "\n"
    text = re.sub(r"\n`\n(\+-+\+\n\|\s+MATRIZ.*?)\n`\n", risk, text, flags=re.S)
    return text
if "MATRIZ DE RIESGO" in text: text = fix_analisis(text)
text = text.replace("\x07pp", "app").replace("\tests/", "tests/").replace("\test_report", "test_report")
text = re.sub(r"\t(ests/|est_report)", r"t\1", text)
lines = text.split("\n"); res = []; i = 0
while i < len(lines):
    if lines[i].strip() == "`":
        j = i + 1
        while j < len(lines) and lines[j].strip() != "`" and not lines[j].startswith("## "):
            j += 1
        if j < len(lines) and lines[j].strip() == "`":
            res.append("```"); res += lines[i+1:j]; res.append("```"); i = j + 1; continue
        i += 1; continue  # backtick huérfano
    res.append(lines[i]); i += 1
text = "\n".join(res).replace("$\\ge 95\\%$", "≥ 95%")
text = re.sub(r"^> ###\s+(.*)$", r"> ### \1", text, flags=re.M)

e = html.escape
def bullets(items):
    return "<ul>" + "".join(f"<li>{e(b)}</li>" for b in items) + "</ul>"

def parse_bullets(lines):
    out = []
    for l in lines:
        l = l.strip()
        if not l: continue
        if l.startswith("- "): out.append(l[2:].strip())
        elif out: out[-1] += " " + l
        else: out.append(l)
    return out

def pyramid(block):
    rows = [l.strip().strip("|").strip() if l.startswith("|") else l for l in block.split("\n")]
    secs, cur = [], None
    title = None
    for l in rows:
        if l.startswith("+") or not l.strip(): continue
        if title is None: title = l.strip(); continue
        if re.match(r"\d+\.\s", l): cur = [l, []]; secs.append(cur)
        elif cur is not None: cur[1].append(l)
    cols = ["#312E81", "#4338CA", "#0F766E", "#64748B"]
    h = f'<div class="pyr"><div class="pyr-title">{e(title)}</div>'
    for i, (hd, ls) in enumerate(secs):
        m = re.match(r"(\d+)\.\s*(.*)", hd)
        h += (f'<div class="tier" style="--c:{cols[i%4]};margin-left:{i*4}mm"><div class="tier-n">{m.group(1)}</div>'
              f'<div class="tier-b"><div class="tier-h">{e(m.group(2).rstrip(":"))}</div>{bullets(parse_bullets(ls))}</div></div>')
    return h + "</div>"

def stlc(block):
    rows, cur = [], None
    for l in block.split("\n"):
        if not l.startswith("|"): continue
        cells = [c for c in l.strip().strip("|").split("|")]
        if len(cells) < 2: continue
        c1, c2 = cells[0].strip(), cells[1].strip()
        if c1 and "FASES" not in c1 or (c1 and not c2 and "FASES" not in c1):
            cur = [c1, [c2]]; rows.append(cur)
        elif cur and not c1.startswith("FASES"):
            if c1: cur[0] += " " + c1
            cur[1].append(c2)
    h = ('<div class="stlc"><div class="stlc-title">FASES METODOLÓGICAS DEL STLC APLICADAS EN ESTE PROYECTO</div>')
    for c1, ls in rows:
        if c1.startswith("Fase del STLC"): continue
        m = re.match(r"(\d)\.\s*(.*?)\s*(\(.*\))?$", c1)
        if m: lab, name, sub = m.group(1), m.group(2), m.group(3) or ""
        else:
            lab, name, sub = "T", c1.split(":", 1)[-1].strip().replace("&", "&"), c1.split(":")[0]
            ls = [x if x.startswith("- ") else "- " + x for x in ls]
        items = [x.replace("(15 CP", "(15 CP)").replace("Registro de 9 defectos en GitHub Issues.", "Registro de 9 defectos en GitHub Issues.") for x in parse_bullets(ls)]
        h += (f'<div class="ph{" tr" if lab=="T" else ""}"><div class="ph-l"><span class="ph-n">{e(lab if lab!="T" else "↻")}</span>'
              f'<b>{e(name)}</b><i>{e(sub)}</i></div><div class="ph-r">{bullets(items)}</div></div>')
    return h + "</div>"

def esc_tags(line):
    if 'class="' in line: return line
    parts = re.split(r"(`[^`\n]*`)", line)
    for k in range(0, len(parts), 2):
        parts[k] = re.sub(r"<(/?)(?!br\b)([A-Za-z][^<>\n]*)>", r"&lt;\1\2&gt;", parts[k])
    return "".join(parts)
text = "\n".join(esc_tags(l) for l in text.split("\n"))
def chips(m):
    key, rest = m.group(1), m.group(2)
    sel = [x.strip() for ok, x in re.findall(r"\[(x| )\]\s+(.+?)(?=\s{2,}\[|\s*\|?\s*$)", rest) if ok == "x"]
    cls = {"Pasó": "pass", "Falló": "fail", "Bloqueado": "block", "No ejecutado": "prog"}
    out = " ".join('<span class="badge %s">%s</span>' % (cls.get(x, "chip") if key == "Estado" else "chip", x) for x in sel) or "—"
    return "| **%s** | %s |" % (key, out)
text = re.sub(r"^\| \*\*(Estado|Prioridad|Tipo de prueba|Modo|Técnica aplicada)\*\* \|(.*)$", chips, text, flags=re.M)
store = []
def swap(m):
    b = m.group(1)
    if "PIRÁMIDE" in b: store.append(pyramid(b))
    elif "FASES METODOL" in b: store.append(stlc(b))
    else: return m.group(0)
    return f"\n\nQAWIDGET{len(store)-1}X\n\n"
text = re.sub(r"```\n(.*?)\n```", swap, text, flags=re.S)
_o = text.split("\n"); _n = []
for _i, _l in enumerate(_o):
    if re.match(r"^ {2,3}([-*]|\d+\.) ", _l): _l = "    " + _l.lstrip()
    if re.match(r"^\s*([-*]|\d+\.) ", _l) and _n and _n[-1].strip() and not re.match(r"^\s*([-*]|\d+\.) ", _n[-1]) and not _n[-1].startswith("|"):
        _n.append("")
    _n.append(_l)
text = "\n".join(_n)
body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
for i, w in enumerate(store):
    body = body.replace(f"<p>QAWIDGET{i}X</p>", w)

# --- badges QA ---
def badge(cls, label): return f'<span class="badge {cls}">{label}</span>'
body = re.sub(r"<strong>Pasó</strong>", badge("pass", "PASS"), body)
body = re.sub(r"<strong>Falló</strong>", badge("fail", "FAIL"), body)
body = body.replace("[x] Sí", badge("pass", "✔ SÍ")).replace("[x]", badge("pass", "✔"))
body = re.sub(r"\[ \] No", badge("block", "NO"), body)
body = body.replace("[ ]", "☐")
body = re.sub(r"(?:✅)\s*(<strong>)?", lambda m: badge("pass", "✔") + " " + (m.group(1) or ""), body)
body = body.replace("🚨", badge("fail", "!"))
# severidades / probabilidad
for w, c in [("Crítica", "fail"), ("Alta", "block"), ("Media", "prog"), ("Baja", "pass")]:
    body = re.sub(rf"<td>{w}</td>", f"<td>{badge(c, w)}</td>", body)
# IDs de bugs y casos
body = re.sub(r"\bBUG-\d+\b(?![^<]*</code>)", lambda m: f'<span class="bug">{m.group(0)}</span>', body)
body = re.sub(r"(?<![\w/])(\d{2}/\d{2}/\d{4})(?![\w/])", r'<span style="white-space:nowrap">\1</span>', body)
# tablas anchas: clase para ID de casos
body = re.sub(r"<strong>(CP-[A-Z]+-[A-Z]-\d+)</strong>", r'<code class="cp">\1</code>', body)
# bloques ASCII (fences) -> tarjeta de diagrama
body = body.replace("<pre><code>", '<pre class="diagram"><code>')
# título del documento
i1 = body.find("<table>"); i2 = body.find("<h2>")
if 0 <= i1 < i2: body = body.replace("<table>", '<table class="cover">', 1)
body = re.sub(r"<h1>(?:<strong>)?(.*?)(?:</strong>)?</h1>", r'<div class="eyebrow">QA · STLC · ISTQB</div><h1>\1</h1>', body, count=1)

css = (here / "qa_style.css").read_text(encoding="utf-8")
doc = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Plan de Pruebas</title><style>{css}</style></head><body>{body}</body></html>'
htmlf = here / (src.stem.replace(" ", "_") + ".html"); htmlf.write_text(doc, encoding="utf-8")

browser = next((p for p in [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
] if pathlib.Path(p).exists()), None)
if not browser: sys.exit("No se encontró Edge/Chrome")
subprocess.run([browser, "--headless", "--disable-gpu", "--no-sandbox", f"--user-data-dir={(here / '.profile').resolve()}", "--no-pdf-header-footer",
                f"--print-to-pdf={out.resolve()}", htmlf.resolve().as_uri()], check=True, timeout=120)
print("PDF:", out)
