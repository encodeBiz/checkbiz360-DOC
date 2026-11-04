#!/usr/bin/env python3
"""Convierte contrato-de-encargo-del-tratamiento.publicado.md en el módulo TS que sirve la
página /legal/encargo-del-tratamiento del panel, y su traducción al inglés
(contrato-de-encargo-del-tratamiento.publicado.en.md) en contrato.en.html.ts. Solo entiende el
markdown que usa ese texto: títulos, párrafos, listas (a), -, 1.), tablas, citas y
negrita/cursiva/código.

    python3 generar-contrato-html.py <ruta del repo del panel>
"""
import html, json, pathlib, re, sys

AQUI = pathlib.Path(__file__)
PANEL = pathlib.Path(sys.argv[1]) / "src/app/(legal)/legal/encargo-del-tratamiento"
# (markdown de origen, módulo TS de destino, nombre de la constante). El inglés es una
# traducción del español y se regenera con él.
DOCUMENTOS = [
    (AQUI.with_name("contrato-de-encargo-del-tratamiento.publicado.md"), PANEL / "contrato.html.ts", "CONTRATO_HTML"),
    (AQUI.with_name("contrato-de-encargo-del-tratamiento.publicado.en.md"), PANEL / "contrato.en.html.ts", "CONTRATO_HTML_EN"),
]
ITEM = re.compile(r"^([a-z]\) |- |\d+\. )")

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", s)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)

def convertir(t):
    out, para, lines, i = [], [], t.split("\n"), 0
    def flush():
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para.clear()
    while i < len(lines):
        l = lines[i]
        if l.startswith("# "): flush(); out.append(f"<h1>{inline(l[2:])}</h1>"); i += 1
        elif l.startswith("## "): flush(); out.append(f"<h2>{inline(l[3:])}</h2>"); i += 1
        elif l.strip() == "---": flush(); out.append("<hr />"); i += 1
        elif l.startswith("|"):
            flush(); rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(set(c) <= set("-: ") for c in r)]
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table>")
        elif l.startswith(">"):
            flush(); q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(lines[i][1:].strip()); i += 1
            out.append("<blockquote>" + "".join(f"<p>{inline(p.replace(chr(10), ' '))}</p>" for p in "\n".join(q).split("\n\n") if p.strip()) + "</blockquote>")
        elif ITEM.match(l):
            flush(); items, kind = [], ("a" if re.match(r"^[a-z]\) ", l) else "ul" if l.startswith("- ") else "ol")
            def mismo_tipo(s):
                m = ITEM.match(s)
                return bool(m) and (("a" if re.match(r"^[a-z]\) ", s) else "ul" if s.startswith("- ") else "ol") == kind)
            while i < len(lines):
                if not lines[i].strip():
                    # Los apartados van separados por una línea en blanco: si lo que sigue es otro
                    # apartado del mismo tipo, la lista continúa.
                    j = i
                    while j < len(lines) and not lines[j].strip(): j += 1
                    if j < len(lines) and mismo_tipo(lines[j]): i = j; continue
                    break
                m = ITEM.match(lines[i])
                if m: items.append(lines[i][m.end():].strip())
                else: items[-1] += " " + lines[i].strip()   # línea de continuación, con o sin sangría
                i += 1
            tag, attr = ("ol", ' type="a"') if kind == "a" else (kind, "")
            out.append(f"<{tag}{attr}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
        elif l.strip() == "": flush(); i += 1
        else: para.append(l.strip()); i += 1
    flush()
    return "\n".join(out)

for src, dest, nombre in DOCUMENTOS:
    h = convertir(src.read_text())
    dest.write_text(f"// Generado desde DOCS/ingenieria/proteccion-de-datos/{src.name}\n"
                    "// con generar-contrato-html.py. No editar a mano: se regenera desde el markdown.\n"
                    f"export const {nombre} = " + json.dumps(h, ensure_ascii=False) + ";\n")
    print("generado:", dest, len(h), "chars")
