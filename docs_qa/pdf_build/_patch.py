p = 'docs_qa/pdf_build/build_pdf.py'
s = open(p, encoding='utf-8').read()
old_start = s.index("            if len(c) < 4: continue")
old_end = s.index("        out = ['<div class=\"stlc-title\"")
new_loop = '''            if len(c) < 4: continue
            if c[0].startswith("MATRIZ") or c[0].startswith("Dimensi"): continue
            if cur is None or newrow: cur = [[x] if x else [] for x in c]; rows.append(cur); newrow = False
            else:
                for k in range(4):
                    if c[k]: cur[k].append(c[k])
'''
# rebuild risk loop header to track separators
s = s[:old_start] + new_loop + s[old_end:]
s = s.replace('''        rows, cur = [], None
        for l in m.group(1).split("\\n"):
            if not l.startswith("|"): continue
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) < 4: continue
            if c[0].startswith("MATRIZ")''', '''        rows, cur, newrow = [], None, True
        for l in m.group(1).split("\\n"):
            if l.startswith("+"): newrow = True; continue
            if not l.startswith("|"): continue
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) < 4: continue
            if c[0].startswith("MATRIZ")''', 1)
s = s.replace('''    parts = re.split(r"(`[^`\\n]*`)", line)''', '''    if 'class="' in line: return line
    parts = re.split(r"(`[^`\\n]*`)", line)''', 1)
# list fixes before markdown
s = s.replace('body = markdown.markdown(text,', '''_o = text.split("\\n"); _n = []
for _i, _l in enumerate(_o):
    if re.match(r"^ {2,3}([-*]|\\d+\\.) ", _l): _l = "    " + _l.lstrip()
    if re.match(r"^\\s*([-*]|\\d+\\.) ", _l) and _n and _n[-1].strip() and not re.match(r"^\\s*([-*]|\\d+\\.) ", _n[-1]) and not _n[-1].startswith("|"):
        _n.append("")
    _n.append(_l)
text = "\\n".join(_n)
body = markdown.markdown(text,''', 1)
open(p, 'w', encoding='utf-8').write(s)
