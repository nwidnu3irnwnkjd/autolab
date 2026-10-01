"""Imágenes Open Graph 1200x630 en Python puro (zlib + struct), sin librerías. PNG de paleta (<120 KB).
og-<tema>.png: composición sin texto (el og:title ya lleva el texto) con la ilustración del tema.
quantize_png(): reduce un PNG RGB/RGBA existente (p. ej. og.png general) a paleta. Diseñador."""
import math, os, struct, zlib, hashlib

W, H = 1200, 630
NAVY = (27, 35, 64)


def hexc(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- PNG
def write_png(path, w, h, pix, pal):
    """pix: bytes de índices (w*h); pal: lista de (r,g,b)."""
    raw = bytearray()
    for y in range(h):
        raw.append(0); raw += pix[y * w:(y + 1) * w]
    def ch(t, d): c = struct.pack(">I", len(d)) + t + d; return c + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    nb = max(2, len(pal)); bits = 8
    png = b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, bits, 3, 0, 0, 0)) + \
        ch(b"PLTE", b"".join(bytes(c) for c in pal)) + ch(b"IDAT", zlib.compress(bytes(raw), 9)) + ch(b"IEND", b"")
    open(path, "wb").write(png)
    return len(png)


def read_png(path):
    d = open(path, "rb").read(); i = 8; idat = b""; ct = 0
    while i < len(d):
        n, t = struct.unpack(">I4s", d[i:i + 8]); b = d[i + 8:i + 8 + n]; i += 12 + n
        if t == b"IHDR": w, h, bd, ct, _, _, il = struct.unpack(">IIBBBBB", b)
        elif t == b"IDAT": idat += b
    assert bd == 8 and il == 0 and ct in (2, 6), "solo PNG 8 bits RGB/RGBA sin entrelazar"
    bpp = 3 if ct == 2 else 4; raw = zlib.decompress(idat); stride = w * bpp
    out = bytearray(); prev = bytearray(stride); p = 0
    for _ in range(h):
        f = raw[p]; line = bytearray(raw[p + 1:p + 1 + stride]); p += 1 + stride
        if f == 1:
            for k in range(bpp, stride): line[k] = (line[k] + line[k - bpp]) & 255
        elif f == 2:
            for k in range(stride): line[k] = (line[k] + prev[k]) & 255
        elif f == 3:
            for k in range(stride): line[k] = (line[k] + (((line[k - bpp] if k >= bpp else 0) + prev[k]) >> 1)) & 255
        elif f == 4:
            for k in range(stride):
                a = line[k - bpp] if k >= bpp else 0; b = prev[k]; c = prev[k - bpp] if k >= bpp else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                line[k] = (line[k] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        out += line; prev = line
    rgb = bytearray()
    for y in range(h):
        row = out[y * stride:(y + 1) * stride]
        rgb += row if bpp == 3 else b"".join(row[x:x + 3] for x in range(0, stride, 4))
    return w, h, bytes(rgb)


def quantize(w, h, rgb, ncol=96):
    """Cuantización por corte mediano sobre colores de 5 bits/canal y mapeo con caché."""
    cnt = {}
    for i in range(0, len(rgb), 3):
        k = (rgb[i] >> 3, rgb[i + 1] >> 3, rgb[i + 2] >> 3); cnt[k] = cnt.get(k, 0) + 1
    boxes = [list(cnt.items())]
    while len(boxes) < ncol:
        boxes.sort(key=lambda b: -max(max(c[0][a] for c in b) - min(c[0][a] for c in b) for a in range(3)) * (1 if len(b) > 1 else 0))
        b = boxes.pop(0)
        if len(b) < 2: boxes.append(b); break
        a = max(range(3), key=lambda a: max(c[0][a] for c in b) - min(c[0][a] for c in b))
        b.sort(key=lambda c: c[0][a]); tot = sum(c[1] for c in b); acc = 0
        for j, c in enumerate(b):
            acc += c[1]
            if acc >= tot / 2: break
        j = min(max(j, 0), len(b) - 2)
        boxes += [b[:j + 1], b[j + 1:]]
    pal = []
    for b in boxes:
        t = sum(c[1] for c in b)
        pal.append(tuple(min(255, int(sum(c[0][a] * c[1] for c in b) / t * 8 + 4)) for a in range(3)))
    cache = {}; out = bytearray(w * h)
    for n, i in enumerate(range(0, len(rgb), 3)):
        key = (rgb[i], rgb[i + 1], rgb[i + 2]); v = cache.get(key)
        if v is None:
            v = min(range(len(pal)), key=lambda j: (pal[j][0] - key[0]) ** 2 + (pal[j][1] - key[1]) ** 2 + (pal[j][2] - key[2]) ** 2)
            cache[key] = v
        out[n] = v
    return pal, bytes(out)


def quantize_png(src, dst, ncol=96):
    w, h, rgb = read_png(src); pal, pix = quantize(w, h, rgb, ncol)
    return write_png(dst, w, h, pix, pal)


# ---------------------------------------------------------------- Lienzo
class Canvas:
    def __init__(s, bg):
        s.p = bytearray(bytes(bg) * (W * H))

    def shape(s, x0, y0, x1, y1, sd, col, alpha=1.0):
        x0 = max(0, int(x0)); y0 = max(0, int(y0)); x1 = min(W, int(x1) + 1); y1 = min(H, int(y1) + 1)
        p = s.p; r, g, b = col
        for y in range(y0, y1):
            base = y * W * 3; fy = y + .5
            for x in range(x0, x1):
                a = .5 - sd(x + .5, fy)
                if a <= 0: continue
                if a > 1: a = 1
                a *= alpha; i = base + x * 3
                p[i] = int(p[i] + (r - p[i]) * a); p[i + 1] = int(p[i + 1] + (g - p[i + 1]) * a); p[i + 2] = int(p[i + 2] + (b - p[i + 2]) * a)

    def glow(s, cx, cy, rad, col, alpha):  # mancha suave radial
        p = s.p; r, g, b = col
        for y in range(max(0, int(cy - rad)), min(H, int(cy + rad))):
            base = y * W * 3
            for x in range(max(0, int(cx - rad)), min(W, int(cx + rad))):
                d = math.hypot(x - cx, y - cy) / rad
                if d >= 1: continue
                a = alpha * (1 - d) ** 2; i = base + x * 3
                p[i] = int(p[i] + (r - p[i]) * a); p[i + 1] = int(p[i + 1] + (g - p[i + 1]) * a); p[i + 2] = int(p[i + 2] + (b - p[i + 2]) * a)


def circle(c, cx, cy, r, col, alpha=1.0):
    c.shape(cx - r - 1, cy - r - 1, cx + r + 1, cy + r + 1, lambda x, y: math.hypot(x - cx, y - cy) - r, col, alpha)

def ring(c, cx, cy, r, w, col, alpha=1.0):
    c.shape(cx - r - w, cy - r - w, cx + r + w, cy + r + w, lambda x, y: abs(math.hypot(x - cx, y - cy) - r) - w / 2, col, alpha)

def ellipse(c, cx, cy, a, b, col, alpha=1.0):
    m = min(a, b)
    c.shape(cx - a - 1, cy - b - 1, cx + a + 1, cy + b + 1, lambda x, y: (math.hypot((x - cx) / a, (y - cy) / b) - 1) * m, col, alpha)

def rrect(c, x, y, w, h, r, col, alpha=1.0):
    cx, cy = x + w / 2, y + h / 2; hw, hh = w / 2 - r, h / 2 - r
    def sd(px, py):
        dx = abs(px - cx) - hw; dy = abs(py - cy) - hh
        return math.hypot(max(dx, 0), max(dy, 0)) + min(max(dx, dy), 0) - r
    c.shape(x - 1, y - 1, x + w + 1, y + h + 1, sd, col, alpha)

def capsule(c, x0, y0, x1, y1, w, col, alpha=1.0):
    dx, dy = x1 - x0, y1 - y0; L = dx * dx + dy * dy or 1
    def sd(px, py):
        t = max(0, min(1, ((px - x0) * dx + (py - y0) * dy) / L))
        return math.hypot(px - x0 - t * dx, py - y0 - t * dy) - w / 2
    c.shape(min(x0, x1) - w, min(y0, y1) - w, max(x0, x1) + w, max(y0, y1) + w, sd, col, alpha)

def poly(c, pts, col, alpha=1.0, edge=None, ew=0):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; n = len(pts)
    def inside(px, py):
        k = False
        for i in range(n):
            ax, ay = pts[i]; bx, by = pts[(i + 1) % n]
            if (ay > py) != (by > py) and px < (bx - ax) * (py - ay) / (by - ay) + ax: k = not k
        return k
    offs = [(-.25, -.25), (.25, -.25), (-.25, .25), (.25, .25)]
    def sd(px, py):  # cobertura por 4 muestras -> pseudo-distancia
        v = sum(inside(px + o[0], py + o[1]) for o in offs)
        return .5 - v / 4 * 1.0 if v not in (0, 4) else (-1 if v == 4 else 1)
    c.shape(min(xs) - 1, min(ys) - 1, max(xs) + 1, max(ys) + 1, sd, col, alpha)
    if edge:
        for i in range(n):
            capsule(c, pts[i][0], pts[i][1], pts[(i + 1) % n][0], pts[(i + 1) % n][1], ew, edge)


# ---------------------------------------------------------------- Ilustraciones (coords de 160x120 -> píxeles)
class T:
    def __init__(s, ox, oy, k): s.ox, s.oy, s.k = ox, oy, k
    def x(s, v): return s.ox + v * s.k
    def y(s, v): return s.oy + v * s.k
    def s(s, v): return v * s.k

def d_house(c, t, accent):
    ew = t.s(2.4)
    poly(c, [(t.x(80), t.y(14)), (t.x(122), t.y(50)), (t.x(38), t.y(50))], accent, edge=NAVY, ew=ew)
    rrect(c, t.x(46) - ew / 2, t.y(50) - ew / 2, t.s(68) + ew, t.s(52) + ew, t.s(3), NAVY)
    rrect(c, t.x(46), t.y(50), t.s(68), t.s(52), t.s(2), (255, 255, 255))
    rrect(c, t.x(70) - ew / 2, t.y(70) - ew / 2, t.s(20) + ew, t.s(32) + ew, t.s(3), NAVY)
    rrect(c, t.x(70), t.y(70), t.s(20), t.s(32), t.s(2), (240, 138, 75))
    circle(c, t.x(85), t.y(87), t.s(1.6), NAVY)
    rrect(c, t.x(98), t.y(58), t.s(10), t.s(10), t.s(1.5), (185, 199, 255))

def d_car(c, t, accent):
    ew = t.s(2.4)
    body = [(30, 70), (36, 52), (52, 44), (92, 44), (112, 56), (130, 60), (136, 72), (136, 82), (24, 82), (24, 74)]
    poly(c, [(t.x(a), t.y(b)) for a, b in body], accent, edge=NAVY, ew=ew)
    poly(c, [(t.x(a), t.y(b)) for a, b in [(42, 56), (54, 49), (70, 49), (70, 62), (40, 62)]], (214, 240, 244))
    poly(c, [(t.x(a), t.y(b)) for a, b in [(76, 49), (92, 49), (104, 62), (76, 62)]], (214, 240, 244))
    for cx in (50, 110):
        circle(c, t.x(cx), t.y(84), t.s(11), NAVY); circle(c, t.x(cx), t.y(84), t.s(7), (255, 255, 255)); circle(c, t.x(cx), t.y(84), t.s(2.2), NAVY)
    capsule(c, t.x(124), t.y(66), t.x(132), t.y(68), t.s(4), (255, 214, 102))

def d_doc(c, t, accent):
    ew = t.s(2.4)
    rrect(c, t.x(46) - ew / 2, t.y(14) - ew / 2, t.s(68) + ew, t.s(92) + ew, t.s(4), NAVY)
    rrect(c, t.x(46), t.y(14), t.s(68), t.s(92), t.s(3), (255, 255, 255))
    poly(c, [(t.x(96), t.y(14)), (t.x(114), t.y(32)), (t.x(96), t.y(32))], (185, 199, 255), edge=NAVY, ew=ew)
    for i, wd in enumerate((38, 30, 38)):
        rrect(c, t.x(56), t.y(42 + i * 11), t.s(wd), t.s(4), t.s(2), (200, 206, 224))
    circle(c, t.x(80), t.y(86), t.s(14), accent); circle(c, t.x(80), t.y(86), t.s(14), NAVY, 0)
    ring(c, t.x(80), t.y(86), t.s(14), t.s(2.4), NAVY)
    circle(c, t.x(74.5), t.y(80.5), t.s(2.4), (255, 255, 255)); circle(c, t.x(85.5), t.y(91.5), t.s(2.4), (255, 255, 255))
    capsule(c, t.x(86), t.y(79), t.x(74), t.y(93), t.s(2.6), (255, 255, 255))

def d_bolt(c, t, accent):
    ew = t.s(2.6)
    circle(c, t.x(80), t.y(60), t.s(44), (255, 255, 255)); ring(c, t.x(80), t.y(60), t.s(44), t.s(2.4), NAVY)
    pts = [(88, 14), (52, 66), (76, 66), (68, 106), (112, 50), (86, 50), (98, 14)]
    poly(c, [(t.x(a), t.y(b)) for a, b in pts], accent, edge=NAVY, ew=ew)

def d_coins(c, t, accent):
    ew = t.s(2.4)
    for i, cy in enumerate((90, 74, 58)):
        ellipse(c, t.x(58), t.y(cy + 4), t.s(30) + ew / 2, t.s(10) + ew / 2, NAVY)
        rrect(c, t.x(28), t.y(cy - 6), t.s(60), t.s(10), 0, accent)
        ellipse(c, t.x(58), t.y(cy + 4), t.s(30), t.s(10), accent)
        ellipse(c, t.x(58), t.y(cy - 6), t.s(30) + ew / 2, t.s(10) + ew / 2, NAVY)
        ellipse(c, t.x(58), t.y(cy - 6), t.s(30), t.s(10), tuple(min(255, v + 28) for v in accent))
    for (x0, hh) in ((98, 18), (112, 34), (126, 52)):
        rrect(c, t.x(x0) - ew / 2, t.y(100 - hh) - ew / 2, t.s(10) + ew, t.s(hh) + ew, t.s(3), NAVY)
        rrect(c, t.x(x0), t.y(100 - hh), t.s(10), t.s(hh), t.s(2), (20, 163, 148))
    poly(c, [(t.x(a), t.y(b)) for a, b in [(100, 36), (126, 20), (126, 28), (140, 18), (126, 8)]][:0] or [(0, 0), (1, 0), (0, 1)], NAVY, 0)

THEMES = {  # tema: (fondo, disco, acento, dibujo, brillo)
    "hipoteca": ("#f3f5fc", "#e1e8ff", "#2548f0", d_house),
    "coche": ("#f1f8f8", "#d9f0ee", "#11998e", d_car),
    "impuestos": ("#f7f3fc", "#ebe0f8", "#9b4dca", d_doc),
    "energia": ("#fcf8ef", "#fdebc4", "#f5b21a", d_bolt),
    "ahorro": ("#f1f8f4", "#d8f1e3", "#1faa6a", d_coins),
}


def logo(c, x, y, s):  # marca: cuadrado azul con tres barras
    rrect(c, x, y, s, s, s * .28, (37, 72, 240))
    for bx, by, bh, a in ((.22, .47, .31, .55), (.42, .31, .47, .8), (.62, .16, .62, 1.0)):
        rrect(c, x + s * bx, y + s * by, s * .16, s * bh, s * .08, (255, 255, 255), a)


def make(tema, path):
    bg, disc, acc, fn = THEMES[tema]
    bg, disc, acc = hexc(bg), hexc(disc), hexc(acc)
    c = Canvas(bg)
    c.glow(150, 120, 380, acc, .07); c.glow(1080, 560, 360, hexc("#f08a4b"), .06)
    circle(c, 600, 322, 262, disc)
    circle(c, 1010, 120, 46, disc, .8); circle(c, 190, 500, 62, disc, .8); circle(c, 130, 250, 22, acc, .25); circle(c, 1075, 470, 18, hexc("#f08a4b"), .6)
    ring(c, 600, 322, 292, 3, acc, .22)
    fn(c, T(600 - 80 * 3.7, 322 - 60 * 3.7, 3.7), acc)
    logo(c, 56, 52, 84)
    # puntos decorativos tipo «decisión»
    for i in range(7):
        circle(c, 880 + i * 38, 585, 5, acc, .25 + .1 * (i % 2))
    return emit(c, path)


def emit(c, path, ncol=200):
    pal, pix = quantize(W, H, bytes(c.p), ncol)
    return write_png(path, W, H, pix, pal)


def build_all(assets_dir, cache_dir):
    """Genera og-<tema>.png si faltan o si este módulo cambió. Devuelve lista de ficheros."""
    stamp = hashlib.sha1(open(__file__, "rb").read()).hexdigest()
    sp = os.path.join(cache_dir, "og.stamp"); os.makedirs(cache_dir, exist_ok=True)
    old = open(sp).read() if os.path.exists(sp) else ""
    out = []
    for t in THEMES:
        p = os.path.join(assets_dir, f"og-{t}.png")
        if old != stamp or not os.path.exists(p): make(t, p)
        out.append(p)
    open(sp, "w").write(stamp)
    return out


if __name__ == "__main__":
    import sys
    a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    for t in (sys.argv[1:] or THEMES): print(t, make(t, os.path.join(a, f"og-{t}.png")))
