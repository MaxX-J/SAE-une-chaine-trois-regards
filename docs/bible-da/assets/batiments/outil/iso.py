"""Moteur de dessin isométrique minimal (SVG) pour les assets de Béziers.

Repère du monde, en mètres :
  x : vers la droite et le bas de l'écran
  y : vers la gauche et le bas de l'écran
  z : vers le haut
Projection 2:1 (dimétrique) : un mètre au sol = U px en largeur.
Les faces visibles d'une boîte sont +x (face « R », à droite) et +y (face « L », à gauche).
La lumière vient de la gauche (côté +y, -x) : face L éclairée, face R à l'ombre.
"""
import math
import random

U = 10.0          # px par mètre (largeur au sol)
ZK = 1.12         # échelle verticale
LIGHT = (-0.35, 0.55, 0.76)
NIGHT_BASE = '#1c2140'
SHADOW_TINT = '#2b2440'

NL, NR, NT = (0, 1, 0), (1, 0, 0), (0, 0, 1)


def hx(c):
    c = c.lstrip('#')
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def rgb(v):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(x)))) for x in v)


def mix(a, b, t):
    A, B = hx(a), hx(b)
    return rgb([A[i] + (B[i] - A[i]) * t for i in range(3)])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(v):
    l = math.sqrt(dot(v, v)) or 1.0
    return [x / l for x in v]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scl(a, k):
    return tuple(x * k for x in a)


LN = norm(LIGHT)


def rect(u0, u1, z0, z1):
    return [(u0, z0), (u1, z0), (u1, z1), (u0, z1)]


def arch(u0, u1, z0, z1, seg=12, pointed=False):
    """Baie cintrée (plein cintre) ou ogivale, en coordonnées de face (u, z)."""
    w = u1 - u0
    c = (u0 + u1) / 2
    if pointed:
        zs = z1 - w * 0.866
        pts = [(u0, z0), (u1, z0), (u1, zs)]
        for i in range(1, seg + 1):
            t = math.radians(60 * i / seg)
            pts.append((u0 + w * math.cos(t), zs + w * math.sin(t)))
        for i in range(1, seg + 1):
            t = math.radians(120 + 60 * i / seg)
            pts.append((u1 + w * math.cos(t), zs + w * math.sin(t)))
        return pts
    r = w / 2
    zs = max(z0, z1 - r)
    pts = [(u0, z0), (u1, z0), (u1, zs)]
    for i in range(1, seg):
        t = math.pi * i / seg
        pts.append((c + r * math.cos(t), zs + r * math.sin(t)))
    pts.append((u0, zs))
    return pts


def circ(cu, cz, r, seg=28):
    return [(cu + r * math.cos(2 * math.pi * i / seg), cz + r * math.sin(2 * math.pi * i / seg)) for i in range(seg)]


def hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


class S:
    """Une scène SVG (un asset)."""

    def __init__(self, aid, night=False, seed=0):
        self.aid = aid
        import hashlib
        self.k = 'b' + hashlib.md5(aid.encode()).hexdigest()[:4]
        self.night = night
        self.rng = random.Random(f'{aid}|{seed}')
        self.el = []
        self.defs = []
        self.pts = []
        self.n = 0
        self.ox = self.oy = 0.0
        self.cx = self.cy = 0.0

    # ---------- repère ----------
    def at(self, ox, oy):
        self.ox, self.oy = ox, oy
        return self

    def P(self, x, y, z):
        x += self.ox - self.cx
        y += self.oy - self.cy
        X = (x - y) * U
        Y = (x + y) * U / 2 - z * U * ZK
        self.pts.append((X, Y))
        return X, Y

    def uid(self, p='c'):
        self.n += 1
        return f'{self.k}{p}{self.n}'

    def g(self, name):
        return f'url(#{self.k}{name})'

    # ---------- couleurs ----------
    def col(self, base, n=NT):
        d = max(0.0, dot(norm(n), LN))
        if not self.night:
            f = 0.78 + 0.42 * d
            if f >= 1:
                return mix(base, '#fff8ec', (f - 1) * 1.6)
            return mix(base, SHADOW_TINT, (1 - f) * 1.2)
        b = mix(base, NIGHT_BASE, 0.58)
        f = 0.84 + 0.24 * d
        if f >= 1:
            return mix(b, '#8d99c9', (f - 1) * 1.3)
        return mix(b, '#0a0d1b', (1 - f) * 1.5)

    def ink(self, c, k=0.38):
        return mix(c, '#140f1e', k)

    # ---------- primitives ----------
    def _pts(self, pts3):
        return ' '.join('%.1f,%.1f' % self.P(*p) for p in pts3)

    def poly(self, pts3, fill, stroke='auto', sw=0.45, op=None, clip=None, extra=''):
        d = self._pts(pts3)
        if stroke == 'auto':
            stroke = self.ink(fill) if fill.startswith('#') else None
        st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ''
        o = f' opacity="{op:.2f}"' if op is not None else ''
        c = f' clip-path="url(#{clip})"' if clip else ''
        self.el.append(f'<polygon points="{d}" fill="{fill}"{st}{o}{c}{extra}/>')

    def line(self, a, b, colr, w=0.5, op=None, dash=None, clip=None, cap='round'):
        (x1, y1), (x2, y2) = self.P(*a), self.P(*b)
        o = f' opacity="{op:.2f}"' if op is not None else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        c = f' clip-path="url(#{clip})"' if clip else ''
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{colr}" stroke-width="{w}" stroke-linecap="{cap}"{o}{d}{c}/>')

    def pline(self, pts3, colr, w=0.5, op=None, fill='none'):
        o = f' opacity="{op:.2f}"' if op is not None else ''
        self.el.append(f'<polyline points="{self._pts(pts3)}" fill="{fill}" stroke="{colr}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{o}/>')

    def clip(self, pts3):
        i = self.uid('k')
        self.defs.append(f'<clipPath id="{i}"><polygon points="{self._pts(pts3)}"/></clipPath>')
        return i

    def ellipse_s(self, p3, rx, ry, fill, op=None):
        X, Y = self.P(*p3)
        o = f' opacity="{op:.2f}"' if op is not None else ''
        self.el.append(f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}"{o}/>')

    def circle_s(self, p3, r, fill, stroke=None, sw=0.5, op=None, dx=0, dy=0):
        X, Y = self.P(*p3)
        o = f' opacity="{op:.2f}"' if op is not None else ''
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        self.el.append(f'<circle cx="{X + dx:.1f}" cy="{Y + dy:.1f}" r="{r:.1f}" fill="{fill}"{st}{o}/>')

    def raw(self, txt):
        self.el.append(txt)

    # ---------- faces ----------
    @staticmethod
    def fp(face, plane, u, z, o=0.0):
        return (u, plane + o, z) if face == 'L' else (plane + o, u, z)

    @staticmethod
    def fn(face):
        return NL if face == 'L' else NR

    def fpoly(self, face, plane, uz, fill, o=0.0, **kw):
        self.poly([self.fp(face, plane, u, z, o) for u, z in uz], fill, **kw)

    def fline(self, face, plane, a, b, colr, o=0.0, **kw):
        self.line(self.fp(face, plane, a[0], a[1], o), self.fp(face, plane, b[0], b[1], o), colr, **kw)

    # ---------- volumes ----------
    def box(self, x0, y0, z0, x1, y1, z1, base, top=True, topc=None, sw=0.45):
        self.poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], self.col(base, NR), sw=sw)
        self.poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], self.col(base, NL), sw=sw)
        if top:
            self.poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], self.col(topc or base, NT), sw=sw)

    def shadow(self, x0, y0, x1, y1, h, k=0.26):
        if self.night:
            return
        c = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        o = [(x + h * k, y - h * k) for x, y in c]
        hl = hull(c + o)
        self.poly([(x, y, 0) for x, y in hl], SHADOW_TINT, stroke=None, op=0.16)

    def ao(self, face, plane, u0, u1, z0=0.0, h=2.4):
        self.fpoly(face, plane, rect(u0, u1, z0, z0 + h), self.g('ao'), stroke=None)

    def walls(self, x0, y0, x1, y1, z0, z1, base):
        self.box(x0, y0, z0, x1, y1, z1, base, top=False)
        self.ao('R', x1, y0, y1, z0)
        self.ao('L', y1, x0, x1, z0)

    def ground_glow(self, p3, rx, ry=None, op=0.55):
        if self.night:
            self.ellipse_s(p3, rx, ry or rx * 0.5, self.g('pool'), op=op)

    # ---------- cylindres et prismes ----------
    def cpt(self, cx, cy, r, th, z):
        return (cx + r * math.cos(th), cy + r * math.sin(th), z)

    def cyl(self, cx, cy, r, z0, z1, base, seg=32, top=True, topc=None, rot=0.0, sw=0.4, side=True):
        segs = []
        for i in range(seg):
            a, b = rot + 2 * math.pi * i / seg, rot + 2 * math.pi * (i + 1) / seg
            m = (a + b) / 2
            n = (math.cos(m), math.sin(m), 0)
            if n[0] + n[1] > -1e-6:
                segs.append((math.cos(m) + math.sin(m), a, b, n))
        if side:
            for _, a, b, n in sorted(segs):
                c = self.col(base, n)
                self.poly([self.cpt(cx, cy, r, a, z0), self.cpt(cx, cy, r, b, z0), self.cpt(cx, cy, r, b, z1), self.cpt(cx, cy, r, a, z1)], c, stroke=c if seg > 12 else 'auto', sw=sw if seg <= 12 else 0.3)
        if top:
            self.poly([self.cpt(cx, cy, r, rot + 2 * math.pi * i / seg, z1) for i in range(seg)], self.col(topc or base, NT), sw=sw)

    def cone(self, cx, cy, r, z0, z1, base, seg=24, rot=0.0):
        tris = []
        for i in range(seg):
            a, b = rot + 2 * math.pi * i / seg, rot + 2 * math.pi * (i + 1) / seg
            m = (a + b) / 2
            h = z1 - z0
            n = norm((math.cos(m) * h, math.sin(m) * h, r))
            tris.append((math.cos(m) + math.sin(m), a, b, n))
        for _, a, b, n in sorted(tris):
            c = self.col(base, n)
            self.poly([self.cpt(cx, cy, r, a, z0), self.cpt(cx, cy, r, b, z0), (cx, cy, z1)], c, stroke=c if seg > 12 else 'auto', sw=0.3)

    # ---------- toits ----------
    def _pan(self, pts, base, eave, up, step=0.34, courses=4, tex=True, kind='tuile'):
        n = cross(sub(pts[1], pts[0]), sub(pts[-1], pts[0]))
        if n[2] < 0:
            n = scl(n, -1)
        c = self.col(base, n)
        self.poly(pts, c, sw=0.45)
        if not tex:
            return
        k = self.clip(pts)
        a, b = eave
        L = math.dist(a[:2], b[:2])
        cnt = max(1, int(L / step))
        lc = self.ink(c, 0.32 if kind == 'tuile' else 0.18)
        for i in range(1, cnt):
            p = add(a, scl(sub(b, a), i / cnt))
            self.line(p, add(p, up), lc, w=0.55 if kind == 'tuile' else 0.35, op=0.55 if kind == 'tuile' else 0.6, clip=k)
        if kind == 'tuile':
            for j in range(1, courses + 1):
                f = j / (courses + 1)
                self.line(add(a, scl(up, f)), add(b, scl(up, f)), lc, w=0.35, op=0.35, clip=k)

    def roof(self, x0, y0, x1, y1, ze, kind='hip', pitch=0.32, ov=0.4, tile='#c46a43', wall=None, axis=None, hipk=1.0, tex=True, mat='tuile'):
        X0, Y0, X1, Y1 = x0 - ov, y0 - ov, x1 + ov, y1 + ov
        if axis is None:
            axis = 'x' if (x1 - x0) >= (y1 - y0) else 'y'
        ridge_c = mix(tile, '#f4d9b8', 0.25) if mat == 'tuile' else mix(tile, '#ffffff', 0.25)
        if self.night:
            ridge_c = mix(self.col(tile, NT), '#c9a48a', 0.25)
        st = 0.34 if mat == 'tuile' else 0.55
        if axis == 'x':
            half = (Y1 - Y0) / 2
            cy = (Y0 + Y1) / 2
            rise = half * pitch
            zr = ze + rise
            hh = half * hipk if kind == 'hip' else 0.0
            A, B = (X0 + hh, cy, zr), (X1 - hh, cy, zr)
            self._pan([(X0, Y0, ze), (X1, Y0, ze), B, A], tile, ((X0, Y0, ze), (X1, Y0, ze)), (0, half, rise), st, tex=tex, kind=mat)
            if kind == 'hip':
                self._pan([(X0, Y0, ze), (X0, Y1, ze), A], tile, ((X0, Y0, ze), (X0, Y1, ze)), (hh, 0, rise), st, tex=tex, kind=mat)
                self._pan([(X1, Y0, ze), (X1, Y1, ze), B], tile, ((X1, Y0, ze), (X1, Y1, ze)), (-hh, 0, rise), st, tex=tex, kind=mat)
            else:
                w = wall or '#d9b07a'
                zw = ze + (half - ov) * pitch
                self.poly([(x1, y0, ze), (x1, y1, ze), (x1, cy, zw)], self.col(w, NR))
            self._pan([(X0, Y1, ze), (X1, Y1, ze), B, A], tile, ((X0, Y1, ze), (X1, Y1, ze)), (0, -half, rise), st, tex=tex, kind=mat)
            self.line(A, B, ridge_c, w=1.3)
            if kind == 'hip':
                for p, q in (((X0, Y1, ze), A), ((X1, Y1, ze), B), ((X1, Y0, ze), B)):
                    self.line(p, q, ridge_c, w=1.0)
            else:
                self.line((X1, Y0, ze), B, ridge_c, w=0.9)
                self.line((X1, Y1, ze), B, ridge_c, w=0.9)
        else:
            half = (X1 - X0) / 2
            cx = (X0 + X1) / 2
            rise = half * pitch
            zr = ze + rise
            hh = half * hipk if kind == 'hip' else 0.0
            A, B = (cx, Y0 + hh, zr), (cx, Y1 - hh, zr)
            self._pan([(X0, Y0, ze), (X0, Y1, ze), B, A], tile, ((X0, Y0, ze), (X0, Y1, ze)), (half, 0, rise), st, tex=tex, kind=mat)
            if kind == 'hip':
                self._pan([(X0, Y0, ze), (X1, Y0, ze), A], tile, ((X0, Y0, ze), (X1, Y0, ze)), (0, hh, rise), st, tex=tex, kind=mat)
                self._pan([(X0, Y1, ze), (X1, Y1, ze), B], tile, ((X0, Y1, ze), (X1, Y1, ze)), (0, -hh, rise), st, tex=tex, kind=mat)
            else:
                w = wall or '#d9b07a'
                zw = ze + (half - ov) * pitch
                self.poly([(x0, y1, ze), (x1, y1, ze), (cx, y1, zw)], self.col(w, NL))
            self._pan([(X1, Y0, ze), (X1, Y1, ze), B, A], tile, ((X1, Y0, ze), (X1, Y1, ze)), (-half, 0, rise), st, tex=tex, kind=mat)
            self.line(A, B, ridge_c, w=1.3)
            if kind == 'hip':
                for p, q in (((X1, Y1, ze), B), ((X0, Y1, ze), B), ((X1, Y0, ze), A)):
                    self.line(p, q, ridge_c, w=1.0)
            else:
                self.line((X0, Y1, ze), B, ridge_c, w=0.9)
                self.line((X1, Y1, ze), B, ridge_c, w=0.9)
        return zr

    def flat_roof(self, x0, y0, x1, y1, ztop, para=0.8, t=0.3, floor='#bdb6aa', coping='#e9e2d4'):
        """Toit-terrasse : les murs montent jusqu'à ztop (haut de l'acrotère)."""
        zf = ztop - para
        inner = [(x0 + t, y0 + t, ztop), (x1 - t, y0 + t, ztop), (x1 - t, y1 - t, ztop), (x0 + t, y1 - t, ztop)]
        k = self.clip(inner)
        cop = self.col(coping, NT)
        self.poly([(x0, y0, ztop), (x1, y0, ztop), (x1, y1, ztop), (x0, y1, ztop)], cop)
        # l'intérieur de l'acrotère, découpé par l'ouverture
        self.poly([(x0 + t, y0 + t, zf), (x1 - t, y0 + t, zf), (x1 - t, y1 - t, zf), (x0 + t, y1 - t, zf)], self.col(floor, NT), clip=k, stroke=None)
        self.poly([(x0 + t, y0 + t, zf), (x1 - t, y0 + t, zf), (x1 - t, y0 + t, ztop), (x0 + t, y0 + t, ztop)], self.col(floor, NL), clip=k)
        self.poly([(x0 + t, y0 + t, zf), (x0 + t, y1 - t, zf), (x0 + t, y1 - t, ztop), (x0 + t, y0 + t, ztop)], self.col(floor, NR), clip=k)
        return zf

    def mansard(self, x0, y0, x1, y1, ze, h1=3.0, inset=1.0, zinc='#6e7c8f', dormers_L=(), dormers_R=(), stone='#e6dcc6'):
        ov = 0.2
        X0, Y0, X1, Y1 = x0 - ov, y0 - ov, x1 + ov, y1 + ov
        a0, b0, a1, b1 = x0 + inset, y0 + inset, x1 - inset, y1 - inset
        zt = ze + h1
        self._pan([(X0, Y0, ze), (X1, Y0, ze), (a1, b0, zt), (a0, b0, zt)], zinc, ((X0, Y0, ze), (X1, Y0, ze)), (0, inset, h1), 0.6, tex=False, kind='zinc')
        self._pan([(X0, Y0, ze), (X0, Y1, ze), (a0, b1, zt), (a0, b0, zt)], zinc, ((X0, Y0, ze), (X0, Y1, ze)), (inset, 0, h1), 0.6, tex=False, kind='zinc')
        self._pan([(X1, Y0, ze), (X1, Y1, ze), (a1, b1, zt), (a1, b0, zt)], zinc, ((X1, Y0, ze), (X1, Y1, ze)), (-inset - ov, 0, h1), 0.6, kind='zinc')
        self._pan([(X0, Y1, ze), (X1, Y1, ze), (a1, b1, zt), (a0, b1, zt)], zinc, ((X0, Y1, ze), (X1, Y1, ze)), (0, -inset - ov, h1), 0.6, kind='zinc')
        light = mix(zinc, '#ffffff', 0.18)
        self.roof(a0, b0, a1, b1, zt, 'hip', pitch=0.18, ov=0.0, tile=light, mat='zinc')
        # brisis : ligne claire
        for p, q in (((a0, b1, zt), (a1, b1, zt)), ((a1, b0, zt), (a1, b1, zt))):
            self.line(p, q, mix(zinc, '#ffffff', 0.45), w=0.8)
        for u in dormers_L:
            self.dormer('L', y1 - inset * 0.45, u, ze + 0.25, stone)
        for u in dormers_R:
            self.dormer('R', x1 - inset * 0.45, u, ze + 0.25, stone)

    def dormer(self, face, plane, u, z, stone, w=0.85, h=1.45):
        n = self.fn(face)
        self.fpoly(face, plane, rect(u - w / 2 - 0.18, u + w / 2 + 0.18, z, z + h + 0.15), self.col(stone, n))
        self.fpoly(face, plane, [(u - w / 2 - 0.3, z + h + 0.15), (u + w / 2 + 0.3, z + h + 0.15), (u, z + h + 0.75)], self.col(stone, n))
        self.glass(face, plane, u, z + 0.12, w - 0.1, h - 0.25, arch_=True)

    # ---------- baies ----------
    def glass(self, face, plane, u, z, w, h, arch_=False, pointed=False, lit=None, mull=True, o=0.0):
        n = self.fn(face)
        shp = arch(u - w / 2, u + w / 2, z, z + h, pointed=pointed) if (arch_ or pointed) else rect(u - w / 2, u + w / 2, z, z + h)
        if lit is None:
            lit = self.rng.random() < 0.58
        if self.night:
            fill = self.g('lit') if lit else self.col('#2b3550', n)
        else:
            fill = self.col('#4b6272', n)
        self.fpoly(face, plane, shp, fill, o=o, stroke=self.col('#2b2626', n), sw=0.35)
        if not self.night:
            self.fpoly(face, plane, [(u - w / 2, z + h * 0.35), (u - w / 2 + w * 0.45, z + h * 0.95), (u - w / 2 + w * 0.7, z + h * 0.95), (u - w / 2 + w * 0.2, z + h * 0.35)], '#ffffff', o=o, stroke=None, op=0.13)
        if mull:
            mc = self.col('#e8e0d0', n) if not (self.night and lit) else '#7a4a22'
            self.fline(face, plane, (u, z), (u, z + h * (0.92 if not arch_ else 0.8)), mc, o=o, w=0.45, op=0.8)
            self.fline(face, plane, (u - w / 2, z + h * 0.62), (u + w / 2, z + h * 0.62), mc, o=o, w=0.35, op=0.7)
        return lit

    def window(self, face, plane, u, z, w, h, shut=None, arch_=False, pointed=False, lit=None, surround='#efe5cf', sill=True, bal=False, mull=True, e=0.14, iron='#2f2b2d'):
        n = self.fn(face)
        if lit is None:
            lit = self.rng.random() < 0.58
        if self.night and lit:
            X, Y = self.P(*self.fp(face, plane, u, z + h / 2))
            self.raw(f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="{w * U * 1.5:.1f}" ry="{h * U * 0.95:.1f}" fill="{self.g("glow")}"/>')
        shp = (lambda a, b, c, d: arch(a, b, c, d, pointed=pointed)) if (arch_ or pointed) else rect
        if surround:
            self.fpoly(face, plane, shp(u - w / 2 - e, u + w / 2 + e, z - e * 0.5, z + h + e), self.col(surround, n), sw=0.35)
        self.glass(face, plane, u, z, w, h, arch_=arch_, pointed=pointed, lit=lit, mull=mull)
        if shut:
            zt = z + h - (w / 2 if arch_ else 0)
            sc = self.col(shut, n)
            dk = self.ink(sc, 0.35)
            for side in (-1, 1):
                ua = u + side * (w / 2 + e)
                ub = ua + side * (w / 2 + 0.03)
                lo, hi = min(ua, ub), max(ua, ub)
                self.fpoly(face, plane, rect(lo, hi, z, zt), sc, sw=0.35)
                k = max(3, int((zt - z) / 0.16))
                for j in range(1, k):
                    zz = z + (zt - z) * j / k
                    self.fline(face, plane, (lo + 0.05, zz), (hi - 0.05, zz), dk, w=0.3, op=0.55)
        if sill:
            self.fpoly(face, plane, rect(u - w / 2 - e - 0.08, u + w / 2 + e + 0.08, z - e * 0.5 - 0.12, z - e * 0.5), self.col(surround or '#efe5cf', NT), sw=0.3)
        if bal:
            self.balcony(face, plane, u - w / 2 - 0.4, u + w / 2 + 0.4, z - 0.05, iron=iron)
        return lit

    def balcony(self, face, plane, u0, u1, z, dp=0.65, slab='#e7ddca', iron='#2f2b2d', rail=1.0):
        n = self.fn(face)
        fp = self.fp
        self.poly([fp(face, plane, u0, z), fp(face, plane, u1, z), fp(face, plane, u1, z, dp), fp(face, plane, u0, z, dp)], self.col(slab, NT), sw=0.3)
        self.fpoly(face, plane, rect(u0, u1, z - 0.16, z), self.col(slab, n), o=dp, sw=0.3)
        ic = iron if not self.night else '#0c0c14'
        self.fline(face, plane, (u0, z + rail), (u1, z + rail), ic, o=dp, w=0.7)
        self.line(fp(face, plane, u0, z + rail), fp(face, plane, u0, z + rail, dp), ic, w=0.6)
        self.line(fp(face, plane, u1, z + rail), fp(face, plane, u1, z + rail, dp), ic, w=0.6)
        k = int((u1 - u0) / 0.13)
        for i in range(k + 1):
            uu = u0 + (u1 - u0) * i / k
            self.fline(face, plane, (uu, z), (uu, z + rail), ic, o=dp, w=0.28, op=0.85)
        self.fline(face, plane, (u0, z + rail * 0.18), (u1, z + rail * 0.18), ic, o=dp, w=0.4)

    def door(self, face, plane, u, w=1.2, h=2.5, colr='#5b3a2a', arch_=False, z=0.0, surround='#e9dfc9', lit=None):
        n = self.fn(face)
        e = 0.18
        shp = arch if arch_ else rect
        if surround:
            self.fpoly(face, plane, shp(u - w / 2 - e, u + w / 2 + e, z, z + h + e), self.col(surround, n), sw=0.35)
        self.fpoly(face, plane, shp(u - w / 2, u + w / 2, z, z + h), self.col(colr, n), sw=0.35)
        if arch_:
            zs = z + h - w / 2
            self.fpoly(face, plane, arch(u - w / 2 + 0.08, u + w / 2 - 0.08, zs, z + h - 0.08), self.g('lit') if self.night else self.col('#4b6272', n), stroke=None)
            self.fline(face, plane, (u - w / 2, zs), (u + w / 2, zs), self.ink(self.col(colr, n)), w=0.5)
        dk = self.ink(self.col(colr, n), 0.3)
        self.fline(face, plane, (u, z + 0.05), (u, z + h - (w / 2 if arch_ else 0.05)), dk, w=0.4)
        top = z + h - (w / 2 if arch_ else 0)
        for uu in (u - w / 4, u + w / 4):
            self.fpoly(face, plane, rect(uu - w * 0.15, uu + w * 0.15, z + 0.3, top - 0.35), 'none', stroke=dk, sw=0.3)
        if self.night:
            self.lamp_wall(face, plane, u + w / 2 + 0.45, z + h * 0.8)

    def lamp_wall(self, face, plane, u, z):
        X, Y = self.P(*self.fp(face, plane, u, z, 0.2))
        self.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="7" fill="{self.g("glow")}"/>')
        self.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="1.1" fill="#fff1c9"/>')

    def shop(self, face, plane, u0, u1, h=3.0, awn=('#a8452f', '#f1e6d2'), frame='#3a3431', z=0.0, lit=True):
        n = self.fn(face)
        fc = self.col(frame, n)
        if self.night:
            X, Y = self.P(*self.fp(face, plane, (u0 + u1) / 2, z + 0.2))
            self.raw(f'<ellipse cx="{X:.1f}" cy="{Y + 6:.1f}" rx="{(u1 - u0) * U * 1.1:.1f}" ry="{(u1 - u0) * U * 0.45:.1f}" fill="{self.g("pool")}"/>')
        self.fpoly(face, plane, rect(u0, u1, z, z + h), fc)
        gfill = self.g('shop') if self.night else self.col('#56707f', n)
        self.fpoly(face, plane, rect(u0 + 0.2, u1 - 0.2, z + 0.35, z + h - 0.55), gfill, stroke=None)
        if not self.night:
            self.fpoly(face, plane, [(u0 + 0.3, z + 0.5), (u0 + 0.9, z + h - 0.6), (u0 + 1.4, z + h - 0.6), (u0 + 0.8, z + 0.5)], '#ffffff', stroke=None, op=0.14)
        k = max(1, int((u1 - u0) / 1.3))
        for i in range(1, k):
            uu = u0 + (u1 - u0) * i / k
            self.fline(face, plane, (uu, z + 0.35), (uu, z + h - 0.55), fc, w=0.6)
        if awn:
            zt, out, drop = z + h - 0.15, 1.0, 0.75
            stripes = max(4, int((u1 - u0) / 0.5))
            for i in range(stripes):
                a = u0 - 0.1 + (u1 - u0 + 0.2) * i / stripes
                b = u0 - 0.1 + (u1 - u0 + 0.2) * (i + 1) / stripes
                c = awn[i % 2]
                nn = norm((0, out, drop)) if face == 'L' else norm((out, 0, drop))
                self.poly([self.fp(face, plane, a, zt), self.fp(face, plane, b, zt), self.fp(face, plane, b, zt - drop, out), self.fp(face, plane, a, zt - drop, out)], self.col(c, nn), stroke=None)
                self.fpoly(face, plane, rect(a, b, zt - drop - 0.28, zt - drop), self.col(c, n), o=out, stroke=None)
            self.fline(face, plane, (u0 - 0.1, zt - drop - 0.28), (u1 + 0.1, zt - drop - 0.28), self.ink(self.col(awn[0], n)), o=out, w=0.4)

    # ---------- décors de façade ----------
    def band(self, face, plane, u0, u1, z, h=0.22, colr='#efe5cf'):
        n = self.fn(face)
        self.fpoly(face, plane, rect(u0, u1, z, z + h), self.col(colr, n), sw=0.3)
        self.fline(face, plane, (u0, z - 0.04), (u1, z - 0.04), SHADOW_TINT, w=0.6, op=0.22)

    def genoise(self, face, plane, u0, u1, z, tile='#b9643f', mortar='#efe3cc'):
        n = self.fn(face)
        self.fpoly(face, plane, rect(u0, u1, z - 0.5, z), self.col(mortar, n), sw=0.3)
        tc = self.col(tile, n)
        self.fline(face, plane, (u0 + 0.05, z - 0.13), (u1, z - 0.13), tc, w=1.5, dash='1.6 1.1', cap='butt')
        self.fline(face, plane, (u0 + 0.3, z - 0.36), (u1, z - 0.36), tc, w=1.3, dash='1.6 1.1', cap='butt')

    def joints(self, face, plane, u0, u1, z0, z1, step=0.5, colr=None, op=0.22, vert=False):
        c = colr or SHADOW_TINT
        z = z0 + step
        row = 0
        while z < z1 - 0.05:
            self.fline(face, plane, (u0, z), (u1, z), c, w=0.35, op=op)
            if vert:
                off = 0.6 if row % 2 else 0
                uu = u0 + off + 0.3
                while uu < u1:
                    self.fline(face, plane, (uu, z - step), (uu, z), c, w=0.3, op=op * 0.8)
                    uu += 1.2
            z += step
            row += 1

    def chimney(self, x, y, z, h=1.4, w=0.6, colr='#d9b07a'):
        self.box(x, y, z - 0.6, x + w, y + w, z + h, colr)
        self.box(x - 0.08, y - 0.08, z + h, x + w + 0.08, y + w + 0.08, z + h + 0.18, '#c46a43')

    # ---------- végétation et mobilier ----------
    def tree(self, x, y, h=9.0, r=3.0, kind='platane'):
        night = self.night
        if kind == 'cypres':
            if not night:
                X0, Y0 = self.P(x, y, 0)
                self.raw(f'<ellipse cx="{X0 + r * U * 0.9:.1f}" cy="{Y0:.1f}" rx="{r * U * 1.1:.1f}" ry="{r * U * 0.35:.1f}" fill="{SHADOW_TINT}" opacity="0.15"/>')
            X0, Y0 = self.P(x, y, 0.4)
            X1, Y1 = self.P(x, y, h)
            w = r * U * 0.55
            self.pts += [(X0 - w * 1.3, Y0), (X0 + r * U * 2, Y0)]
            base = self.col('#3d5a3c', NL)
            dark = self.col('#3d5a3c', NR)
            mid = (Y0 + Y1) / 2
            self.raw(f'<path d="M{X0:.1f},{Y0:.1f} C{X0 - w * 1.2:.1f},{Y0 - 2:.1f} {X0 - w:.1f},{mid:.1f} {X1:.1f},{Y1:.1f} C{X0 + w:.1f},{mid:.1f} {X0 + w * 1.2:.1f},{Y0 - 2:.1f} {X0:.1f},{Y0:.1f}Z" fill="{dark}" stroke="{self.ink(dark)}" stroke-width="0.4"/>')
            self.raw(f'<path d="M{X0:.1f},{Y0:.1f} C{X0 - w * 1.2:.1f},{Y0 - 2:.1f} {X0 - w:.1f},{mid:.1f} {X1:.1f},{Y1:.1f} C{X0 - w * 0.2:.1f},{mid:.1f} {X0 - w * 0.1:.1f},{Y0 - 2:.1f} {X0:.1f},{Y0:.1f}Z" fill="{base}"/>')
            return
        green = {'platane': '#7f9f55', 'olivier': '#97a383', 'pin': '#5d7a48'}[kind] if kind != 'palmier' else '#6f9152'
        if not night:
            X0, Y0 = self.P(x, y, 0)
            self.raw(f'<ellipse cx="{X0 + r * U * 0.8:.1f}" cy="{Y0:.1f}" rx="{r * U * 1.2:.1f}" ry="{r * U * 0.5:.1f}" fill="{SHADOW_TINT}" opacity="0.15"/>')
        trunk = self.col('#9a8a70' if kind == 'platane' else '#6d5a46', NL)
        if kind == 'palmier':
            pts = [(x + 0.15 * math.sin(i / 3), y, h * i / 6) for i in range(7)]
            self.pline(pts, self.col('#8a7356', NL), w=2.2)
            X, Y = self.P(*pts[-1])
            self.pts += [(X - r * U * 1.3, Y - r * U), (X + r * U * 1.3, Y + r * U)]
            lc = self.col(green, NL)
            dc = self.col(green, NR)
            for i in range(9):
                a = 2 * math.pi * i / 9 + 0.3
                L = r * U * 1.2
                ex, ey = X + math.cos(a) * L, Y + math.sin(a) * L * 0.55 + 6
                mx, my = X + math.cos(a) * L * 0.5, Y + math.sin(a) * L * 0.3 - 5
                c = lc if math.cos(a) < 0.2 else dc
                self.raw(f'<path d="M{X:.1f},{Y:.1f} Q{mx:.1f},{my - 3:.1f} {ex:.1f},{ey:.1f} Q{mx:.1f},{my + 2:.1f} {X:.1f},{Y:.1f}Z" fill="{c}" stroke="{self.ink(c)}" stroke-width="0.3"/>')
            return
        self.line((x, y, 0), (x, y, h * 0.55), trunk, w=2.0 if kind == 'platane' else 1.6)
        X, Y = self.P(x, y, h * 0.72)
        R = r * U
        self.pts += [(X - R * 1.3, Y - R * 1.2), (X + R * 1.3, Y + R * 1.0), (X + R * 2.2, Y)]
        base = self.col(green, NL)
        dark = self.col(green, NR)
        hi = self.col(green, NT)
        blobs = [(0, 0, 1.0), (-0.45, 0.15, 0.7), (0.45, 0.2, 0.72), (0.05, -0.35, 0.7), (-0.2, 0.35, 0.6), (0.3, -0.15, 0.6)]
        if kind == 'pin':
            X, Y = self.P(x, y, h * 0.9)
            self.line((x, y, h * 0.5), (x, y, h * 0.88), trunk, w=1.6)
            for dx, dy, k in blobs:
                self.raw(f'<ellipse cx="{X + dx * R * 1.1:.1f}" cy="{Y + dy * R * 0.35:.1f}" rx="{k * R * 0.8:.1f}" ry="{k * R * 0.38:.1f}" fill="{dark}" stroke="{self.ink(dark, 0.25)}" stroke-width="0.4"/>')
            for dx, dy, k in blobs[:4]:
                self.raw(f'<ellipse cx="{X + dx * R - R * 0.15:.1f}" cy="{Y + dy * R * 0.35 - R * 0.12:.1f}" rx="{k * R * 0.6:.1f}" ry="{k * R * 0.26:.1f}" fill="{base}"/>')
            return
        for dx, dy, k in blobs:
            self.raw(f'<circle cx="{X + dx * R:.1f}" cy="{Y + dy * R * 0.8:.1f}" r="{k * R * 0.72:.1f}" fill="{dark}" stroke="{self.ink(dark, 0.25)}" stroke-width="0.4"/>')
        for dx, dy, k in blobs[:4]:
            self.raw(f'<circle cx="{X + dx * R - R * 0.12:.1f}" cy="{Y + dy * R * 0.8 - R * 0.1:.1f}" r="{k * R * 0.55:.1f}" fill="{base}"/>')
        self.raw(f'<circle cx="{X - R * 0.28:.1f}" cy="{Y - R * 0.3:.1f}" r="{R * 0.3:.1f}" fill="{hi}" opacity="0.8"/>')

    def lamppost(self, x, y, h=4.5):
        c = '#2b2a30' if not self.night else '#0d0e18'
        self.line((x, y, 0), (x, y, h), c, w=0.9)
        self.line((x, y, h), (x + 0.6, y, h), c, w=0.8)
        X, Y = self.P(x + 0.6, y, h - 0.2)
        if self.night:
            self.pts += [(X - 1.6 * U, Y - 1.6 * U), (X + 3.2 * U, Y + 6 * U)]
            X0, Y0 = self.P(x + 0.6, y, 0)
            self.raw(f'<ellipse cx="{X0:.1f}" cy="{Y0:.1f}" rx="{3.2 * U:.1f}" ry="{1.6 * U:.1f}" fill="{self.g("pool")}"/>')
            self.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{1.6 * U:.1f}" fill="{self.g("glow")}"/>')
            self.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="1.6" fill="#fff4d0"/>')
        else:
            self.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="1.3" fill="#e9e2cf" stroke="{c}" stroke-width="0.4"/>')

    def flag(self, x, y, z, h=2.2, face='L'):
        c = '#2b2a30'
        self.line((x, y, z), (x, y, z + h), c, w=0.5)
        w = 1.2
        cols = ['#2b4ea2', '#f4f1ea', '#d0333a']
        for i, cc in enumerate(cols):
            a, b = w * i / 3, w * (i + 1) / 3
            pts = [(x + a, y, z + h), (x + b, y, z + h - 0.05), (x + b, y, z + h - 0.75), (x + a, y, z + h - 0.7)] if face == 'R' else [(x, y + a, z + h), (x, y + b, z + h - 0.05), (x, y + b, z + h - 0.75), (x, y + a, z + h - 0.7)]
            self.poly(pts, self.col(cc, NL), stroke=None)

    # ---------- sortie ----------
    def svg(self, title='', pad=8, meta=None):
        xs = [p[0] for p in self.pts] or [0]
        ys = [p[1] for p in self.pts] or [0]
        x0, x1, y0, y1 = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
        night = self.night
        a = self.k
        defs = [
            f'<linearGradient id="{a}ao" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SHADOW_TINT}" stop-opacity="0"/><stop offset="1" stop-color="{SHADOW_TINT}" stop-opacity="{0.28 if not night else 0.45}"/></linearGradient>',
            f'<linearGradient id="{a}lit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe7a8"/><stop offset="1" stop-color="#ffa957"/></linearGradient>',
            f'<linearGradient id="{a}shop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0c4"/><stop offset="1" stop-color="#ffb867"/></linearGradient>',
            f'<radialGradient id="{a}glow"><stop offset="0" stop-color="#ffc977" stop-opacity="0.55"/><stop offset="1" stop-color="#ffb357" stop-opacity="0"/></radialGradient>',
            f'<radialGradient id="{a}pool"><stop offset="0" stop-color="#ffcf86" stop-opacity="0.5"/><stop offset="1" stop-color="#ffb357" stop-opacity="0"/></radialGradient>',
            f'<linearGradient id="{a}water" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{"#7fb1bd" if not night else "#1f3450"}"/><stop offset="1" stop-color="{"#4f8c9e" if not night else "#152540"}"/></linearGradient>',
            f'<radialGradient id="{a}rose"><stop offset="0" stop-color="#ffe2a0"/><stop offset="0.45" stop-color="#e0705a"/><stop offset="1" stop-color="#4a5fb0"/></radialGradient>',
            f'<linearGradient id="{a}screen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e2557a"/><stop offset="0.5" stop-color="#f19a4a"/><stop offset="1" stop-color="#5a7fe0"/></linearGradient>',
        ]
        m = ''
        if meta:
            import json
            m = f'<metadata>{json.dumps(meta, ensure_ascii=False)}</metadata>'
        from opti import optimise
        return optimise(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}" width="{x1 - x0:.0f}" height="{y1 - y0:.0f}" data-ancre="0,0" data-px-par-metre="{U:g}">'
                f'<title>{title}</title>{m}<defs>{"".join(defs)}{"".join(self.defs)}</defs>'
                f'{"".join(self.el)}</svg>')
