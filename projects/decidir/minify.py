"""Minificadores simples en Python puro (Diseñador). Conservadores: respetan strings, regex y plantillas.
css(src) / js(src) / html(src). El JS conserva los saltos de línea (seguro frente a ASI)."""
import re

_REGEX_PREV = set("(,=:[!&|?{};+-*%<>~^")
_REGEX_KW = ("return", "typeof", "case", "do", "else", "in", "of", "void", "delete", "throw", "new")


def css(src):
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == "/" and src[i + 1:i + 2] == "*":
            j = src.find("*/", i + 2); i = n if j < 0 else j + 2
            out.append(" ")
        elif c in "\"'":
            j = i + 1
            while j < n and src[j] != c:
                j += 2 if src[j] == "\\" else 1
            out.append(src[i:j + 1]); i = j + 1
        else:
            out.append(c); i += 1
    s = re.sub(r"\s+", " ", "".join(out))
    # los strings ya no se tocan por las expresiones de abajo salvo que contengan estos signos con espacios: se protegen
    parts = re.split(r"(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')", s)
    for k in range(0, len(parts), 2):
        p = parts[k]
        p = re.sub(r" ?([{};,>]) ?", r"\1", p)
        p = re.sub(r":\s", ":", p)
        p = p.replace(";}", "}")
        p = re.sub(r"\( ", "(", p); p = re.sub(r" \)", ")", p)
        parts[k] = p
    return "".join(parts).strip()


def js(src):
    """Quita comentarios y sangrías; colapsa espacios repetidos fuera de strings/regex; conserva saltos de línea."""
    out, i, n = [], 0, len(src)
    last = ""  # último carácter significativo emitido
    word = ""
    while i < n:
        c = src[i]
        nx = src[i + 1:i + 2]
        if c == "/" and nx == "/":
            while i < n and src[i] != "\n": i += 1
        elif c == "/" and nx == "*":
            j = src.find("*/", i + 2); i = n if j < 0 else j + 2
            out.append(" ")
        elif c in "\"'`":
            j = i + 1
            while j < n and src[j] != c:
                j += 2 if src[j] == "\\" else 1
            out.append(src[i:j + 1]); i = j + 1; last = c; word = ""
        elif c == "/":
            prev_word = "".join(out).rstrip()[-8:]
            is_re = (last == "" or last in _REGEX_PREV or any(re.search(r"(?<![\w$.])" + k + r"$", prev_word) for k in _REGEX_KW))
            if is_re:
                j = i + 1; cls = False
                while j < n and (src[j] != "/" or cls):
                    if src[j] == "\\": j += 1
                    elif src[j] == "[": cls = True
                    elif src[j] == "]": cls = False
                    j += 1
                j += 1
                while j < n and src[j].isalpha(): j += 1
                out.append(src[i:j]); i = j; last = "/"
            else:
                out.append(c); i += 1; last = c
        else:
            out.append(c); i += 1
            if not c.isspace(): last = c
    s = "".join(out)
    # fase 2: sangrías, líneas vacías, espacios repetidos y alrededor de puntuación segura (fuera de strings/regex es imposible
    # de distinguir tras la fase 1 sin tokenizar de nuevo, así que se hace por tokens)
    return _squeeze(s)


_TOK = re.compile(r"""("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'|`(?:[^`\\]|\\.)*`)""")


def _num(m):
    i, d = m.group(1), m.group(2).rstrip("0")
    return i if not d else ("" if i == "0" else i) + "." + d


def _squeeze(s):
    # Protege strings/plantillas; los regex literales se protegen porque contienen caracteres que nunca estamos tocando salvo espacios
    # (los espacios dentro de un regex SÍ importan): detectarlos de nuevo es frágil, así que solo se tocan espacios entre palabras/puntuación segura
    lines = []
    for ln in s.split("\n"):
        ln = ln.strip()
        if ln: lines.append(ln)
    s = "\n".join(lines)
    parts = _TOK.split(s)
    for k in range(0, len(parts), 2):
        p = parts[k]
        if "/" in p and re.search(r"[=(,:!&|?]\s*/[^/*]", p):  # línea con regex literal: solo colapsar tabuladores
            parts[k] = p; continue
        p = re.sub(r"[ \t]{2,}", " ", p)
        p = re.sub(r"(?<=[\w)\]]) ([+\-/]) (?=[\w(.])", r"\1", p)  # a + b, a - b, a / b (no toca ++/--, ni signos unarios)
        p = re.sub(r" ?([{};,=:?<>*&|()\[\]]) ?", r"\1", p)
        p = re.sub(r"(?<![\w.$])(\d+)\.(\d+)(?![\w.$])", _num, p)  # 3.20 -> 3.2, 0.19 -> .19, 5.00 -> 5
        p = re.sub(r" !(?==)", "!", p)  # " !==" -> "!=="
        p = re.sub(r" ([+\-])=", r"\1=", p)  # " +=" -> "+="
        if k > 0: p = re.sub(r"^ \+ ", "+", p)  # "cadena" + x
        if k + 1 < len(parts): p = re.sub(r" \+ $", "+", p)  # x + "cadena"
        parts[k] = p
    return "".join(parts)


def html(src):
    """Quita sangrías y líneas vacías (conserva <pre>/<textarea>/<script>/<style> intactos)."""
    keep = re.compile(r"(<(pre|textarea|script|style)\b.*?</\2>)", re.S)
    parts = keep.split(src)
    out = []
    k = 0
    while k < len(parts):
        out.append(re.sub(r"\n\s*", "\n", parts[k]))
        if k + 2 < len(parts): out.append(parts[k + 1])
        k += 3
    return "".join(out)


# ---------------------------------------------------------------- Tree-shaking de CSS por tipo de página
def _blocks(s):
    """Divide CSS minificado en reglas de primer nivel."""
    out, i, n = [], 0, len(s)
    while i < n:
        j, d = i, 0
        while j < n:
            c = s[j]
            if c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0: break
            elif c == ";" and d == 0: break
            j += 1
        out.append(s[i:j + 1]); i = j + 1
    return out


def _split_sel(sel):
    parts, d, cur = [], 0, ""
    for ch in sel:
        if ch in "([": d += 1
        elif ch in ")]": d -= 1
        if ch == "," and d == 0: parts.append(cur); cur = ""
        else: cur += ch
    return parts + [cur]


def shake(css_min, pool, prefixes=()):
    """Elimina reglas cuyas clases/ids no aparecen en `pool` (set de palabras de HTML+JS de las páginas del tipo).
    Conserva @media/@supports (filtrando dentro), @font-face, :root y selectores sin clases/ids. Los @keyframes solo si se usan."""
    def known(t): return t in pool or any(t.startswith(p) for p in prefixes)
    def keep_sel(one):
        one = re.sub(r"\[[^\]]*\]", "", one)
        return all(known(t) for t in re.findall(r"[.#]([A-Za-z_][\w-]*)", one))
    def walk(blocks):
        out = []
        for b in blocks:
            if not b.endswith("}"): out.append(b); continue
            head, body = b.split("{", 1); body = body[:-1]
            if head.startswith(("@media", "@supports")):
                inner = "".join(walk(_blocks(body)))
                if inner: out.append(head + "{" + inner + "}")
            elif head.startswith("@"): out.append(b)
            else:
                sels = [x for x in _split_sel(head) if keep_sel(x)]
                if sels: out.append(",".join(sels) + "{" + body + "}")
        return out
    res = walk(_blocks(css_min))
    text = "".join(b for b in res if not b.startswith("@keyframes"))
    return "".join(b for b in res if not b.startswith("@keyframes") or re.match(r"@keyframes ([\w-]+)", b).group(1) in text)
