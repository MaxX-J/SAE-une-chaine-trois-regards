"""Personnages, mobilier, végétation de saison et éléments incongrus.

Les personnages sont des sprites dessinés à l'échelle de la carte (1,75 m ≈ 20 px).
Leurs couleurs passent par des variables CSS (--haut, --bas, --peau, --cheveux,
--objet) : le code peut les changer quand le SVG est inséré dans la page.
"""
import math
from iso import S, U, NL, NR, NT, mix, rect, SHADOW_TINT

EMOTIONS = {'joie': '#f2b134', 'tristesse': '#4f6fa8', 'colere': '#c8413a', 'peur': '#7a5aa0',
            'surprise': '#2fa3a0', 'degout': '#7e8f3a', 'neutre': '#9a948a'}
PEAUX = ['#f1c9a5', '#d9a47c', '#a86f4c', '#6f4630']
CHEVEUX = ['#2b211c', '#5a3a24', '#b88a4a', '#8c8c8c']


def P(x, y):
    return (x, y)


# Poses : coordonnées écran en px, origine aux pieds. y négatif = vers le haut.
# hip, neck, head ; jambes (hanche, genou, pied) ; bras (épaule, coude, main). Index 0 = côté gauche (devant).
def _base():
    return dict(lift=0, hip=(0, -9), neck=(0, -16), head=(0, -18.8),
                legs=[((-1.1, -9), (-1.2, -4.6), (-1.3, 0)), ((1.1, -9), (1.2, -4.6), (1.3, 0))],
                arms=[((-2.7, -15.4), (-3.3, -12.2), (-3.4, -9.3)), ((2.7, -15.4), (3.3, -12.2), (3.4, -9.3))])


def pose(name):
    p = _base()
    if name == 'marche':
        p['legs'] = [((-1, -9), (-2.1, -4.6), (-3.4, 0)), ((1, -9), (1.5, -4.5), (2.6, -0.2))]
        p['arms'] = [((-2.7, -15.4), (-2.2, -12.3), (-0.9, -9.7)), ((2.7, -15.4), (3.9, -12.4), (4.7, -9.9))]
    elif name == 'course':
        p.update(neck=(1.6, -15.6), head=(2.4, -18.2))
        p['legs'] = [((-0.9, -9), (-2.0, -4.6), (-4.8, -1.0)), ((0.9, -9), (3.4, -7.0), (2.6, -2.8))]
        p['arms'] = [((-1.2, -15.0), (-3.8, -13.2), (-2.8, -10.6)), ((4.0, -15.2), (5.0, -12.8), (6.6, -13.6))]
        p['lift'] = -1.2
    elif name == 'assis':
        p.update(hip=(0, -5.6), neck=(-0.3, -12.6), head=(-0.3, -15.4))
        p['legs'] = [((-1.1, -5.6), (2.0, -5.4), (2.2, 0)), ((1.1, -5.6), (3.6, -5.0), (3.8, 0.3))]
        p['arms'] = [((-3.0, -12.0), (-2.4, -9.0), (0.4, -7.2)), ((2.4, -12.0), (3.4, -9.0), (2.4, -6.8))]
    elif name == 'joie':
        p['lift'] = -2.2
        p['legs'] = [((-1.1, -9), (-1.8, -5.0), (-1.4, -0.8)), ((1.1, -9), (1.9, -5.0), (1.5, -0.8))]
        p['arms'] = [((-2.7, -15.6), (-4.4, -18.3), (-5.4, -21.4)), ((2.7, -15.6), (4.4, -18.3), (5.4, -21.4))]
    elif name == 'tristesse':
        p.update(neck=(0.4, -15.4), head=(1.0, -17.4))
        p['arms'] = [((-2.3, -14.6), (-2.6, -11.6), (-2.2, -8.8)), ((2.9, -14.6), (3.1, -11.6), (2.9, -8.8))]
    elif name == 'colere':
        p.update(neck=(0.8, -15.8), head=(1.3, -18.6))
        p['legs'] = [((-1.2, -9), (-2.2, -4.6), (-2.8, 0)), ((1.2, -9), (1.9, -4.6), (2.6, 0))]
        p['arms'] = [((-2.0, -15.4), (-4.8, -12.8), (-2.2, -10.0)), ((3.4, -15.4), (5.8, -12.8), (2.8, -10.0))]
    elif name == 'peur':
        p.update(hip=(-0.6, -6.6), neck=(0.6, -12.6), head=(1.2, -15.0))
        p['legs'] = [((-1.6, -6.6), (0.8, -3.8), (-1.6, 0)), ((0.4, -6.6), (2.6, -3.6), (1.2, 0))]
        p['arms'] = [((-1.8, -12.2), (-0.2, -10.2), (1.0, -14.4)), ((2.8, -12.2), (3.8, -10.2), (2.6, -14.6))]
    elif name == 'surprise':
        p.update(head=(0, -19.2))
        p['arms'] = [((-2.7, -15.6), (-4.6, -15.2), (-5.8, -17.6)), ((2.7, -15.6), (4.6, -15.2), (5.8, -17.6))]
        p['legs'] = [((-1.1, -9), (-1.9, -4.6), (-2.4, 0)), ((1.1, -9), (1.9, -4.6), (2.4, 0))]
    elif name == 'degout':
        p.update(neck=(-0.5, -16), head=(-1.3, -18.6))
        p['arms'] = [((-2.9, -15.4), (-3.2, -12.2), (-3.0, -9.3)), ((2.5, -15.4), (4.2, -14.4), (5.0, -17.0))]
    elif name == 'parapluie':
        p['arms'] = [((-2.7, -15.4), (-3.3, -12.2), (-3.4, -9.3)), ((2.7, -15.4), (3.6, -13.2), (2.2, -15.6))]
    return p


def _poly(pts):
    return 'M' + ' '.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'


def person(s, name, night=False):
    p = pose(name)
    ly = p['lift']

    def t(q):
        return (q[0], q[1] + ly)
    el = []
    # ombre au sol
    el.append(f'<ellipse cx="0.6" cy="0" rx="{4.2 if name != "joie" else 3.2}" ry="1.5" fill="#1b1730" opacity="{0.22 if not night else 0.35}"/>')
    if name == 'assis':
        # banc
        wood = '#8a5f3c'
        el.append(f'<path d="M-6 -5.3 L6 -1.3 L6 0.2 L-6 -3.8Z" fill="{wood}"/><path d="M-6 -5.3 L-6 -11 L-4.8 -10.6 L-4.8 -5Z" fill="{mix(wood, "#000000", 0.2)}"/><path d="M-4.8 -10.6 L6 -6.9 L6 -5.6 L-4.8 -9.3Z" fill="{wood}"/><path d="M-5 -3.6V0.4M5 -0.2V3" stroke="#2f2b2d" stroke-width="0.9"/>')
    legs, arms = p['legs'], p['arms']

    def limb(seg, var, w):
        a, b, c = (t(q) for q in seg)
        return f'M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}L{c[0]:.1f} {c[1]:.1f}', var, w
    # jambe arrière, bras arrière
    for i in (1, 0):
        d, v, w = limb(legs[i], 'var(--bas)', 2.1)
        el.append(f'<path d="{d}" fill="none" stroke="{v}" stroke-width="{w}"/>')
        if i == 1:
            el.append(f'<path d="{d}" fill="none" stroke="#000" stroke-opacity="0.18" stroke-width="{w}"/>')
        f = t(legs[i][2])
        el.append(f'<ellipse cx="{f[0] + 0.5:.1f}" cy="{f[1]:.1f}" rx="1.2" ry="0.8" fill="#2a2526"/>')
    d, v, w = limb(arms[1], 'var(--haut)', 1.7)
    el.append(f'<path d="{d}" fill="none" stroke="{v}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="#000" stroke-opacity="0.22" stroke-width="{w}"/>')
    h = t(arms[1][2])
    el.append(f'<circle cx="{h[0]:.1f}" cy="{h[1]:.1f}" r="0.85" fill="var(--peau)"/>')
    # torse
    hp, nk = t(p['hip']), t(p['neck'])
    dx, dy = nk[0] - hp[0], nk[1] - hp[1]
    L = math.hypot(dx, dy)
    px, py = -dy / L, dx / L
    tor = [(hp[0] - px * 2.2, hp[1] - py * 2.2 + 0.6), (hp[0] + px * 2.2, hp[1] + py * 2.2 + 0.6),
           (nk[0] + px * 2.8, nk[1] + py * 2.8), (nk[0] - px * 2.8, nk[1] - py * 2.8)]
    el.append(f'<path d="{_poly(tor)}" fill="var(--haut)"/>')
    half = [((tor[0][0] + tor[1][0]) / 2, (tor[0][1] + tor[1][1]) / 2), tor[1], tor[2], ((tor[2][0] + tor[3][0]) / 2, (tor[2][1] + tor[3][1]) / 2)]
    side = half if px < 0 else [tor[0], half[0], half[3], tor[3]]
    el.append(f'<path d="{_poly(side)}" fill="#000" opacity="0.16"/>')
    # tête
    hx, hy = t(p['head'])
    el.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="2.3" fill="var(--peau)"/>')
    el.append(f'<path d="M{hx:.1f} {hy - 2.3:.1f}A2.3 2.3 0 0 1 {hx:.1f} {hy + 2.3:.1f}Z" fill="#000" opacity="0.12"/>')
    el.append(f'<path d="M{hx - 2.45:.1f} {hy + 0.1:.1f}A2.45 2.45 0 0 1 {hx + 2.45:.1f} {hy + 0.1:.1f}Q{hx + 0.6:.1f} {hy - 1.1:.1f} {hx - 2.45:.1f} {hy + 0.1:.1f}Z" fill="var(--cheveux)"/>')
    # bras avant
    d, v, w = limb(arms[0], 'var(--haut)', 1.7)
    el.append(f'<path d="{d}" fill="none" stroke="{v}" stroke-width="{w}"/>')
    h = t(arms[0][2])
    el.append(f'<circle cx="{h[0]:.1f}" cy="{h[1]:.1f}" r="0.85" fill="var(--peau)"/>')
    if name == 'parapluie':
        hh = t(arms[1][2])
        el.append(f'<path d="M{hh[0]:.1f} {hh[1] + 1.5:.1f}V{hh[1] - 8:.1f}" stroke="#2a2526" stroke-width="0.6"/>')
        cx, cy = hh[0], hh[1] - 8
        el.append(f'<path d="M{cx - 7:.1f} {cy + 2.2:.1f}Q{cx:.1f} {cy - 6:.1f} {cx + 7:.1f} {cy + 2.2:.1f}Q{cx + 3.5:.1f} {cy + 0.8:.1f} {cx:.1f} {cy + 2.2:.1f}Q{cx - 3.5:.1f} {cy + 0.8:.1f} {cx - 7:.1f} {cy + 2.2:.1f}Z" fill="var(--objet)"/>')
        el.append(f'<path d="M{cx:.1f} {cy - 1.9:.1f}Q{cx + 4:.1f} {cy - 1:.1f} {cx + 7:.1f} {cy + 2.2:.1f}Q{cx + 3.5:.1f} {cy + 0.8:.1f} {cx:.1f} {cy + 2.2:.1f}Z" fill="#000" opacity="0.18"/>')
    if name == 'colere':
        el.append(f'<path d="M{hx + 2.6:.1f} {hy - 3.4:.1f}l1.4 -1.2M{hx + 3.4:.1f} {hy - 1.8:.1f}l1.8 -0.4M{hx + 1.4:.1f} {hy - 4.2:.1f}l0.6 -1.6" stroke="#c8413a" stroke-width="0.6"/>')
    if name == 'surprise':
        el.append(f'<path d="M{hx - 0.3:.1f} {hy - 5.6:.1f}v2.2M{hx - 0.3:.1f} {hy - 2.6:.1f}v0.2" stroke="#2fa3a0" stroke-width="0.8"/>')
    if name == 'tristesse':
        el.append(f'<path d="M{hx + 1.3:.1f} {hy + 0.6:.1f}q-0.5 1 0 1.4q0.5 -0.4 0 -1.4Z" fill="#7fb4e0"/>')
    s.pts += [(-8, -30), (8, 4)] if name in ('parapluie', 'joie') else [(-7, -24), (7, 4)]
    if name == 'parapluie':
        s.pts += [(-9, -32), (10, 4)]
    body = ''.join(el)
    if night:
        body = f'<g filter="url(#{s.k}n)">{body}</g>'
        s.defs.append(f'<filter id="{s.k}n"><feColorMatrix values="0.5 0.05 0.05 0 0 0.05 0.5 0.08 0 0 0.1 0.12 0.66 0 0.03 0 0 0 1 0"/></filter>')
    s.raw(body)


def person_svg(name, night, haut, bas='#3b4252', peau=PEAUX[0], cheveux=CHEVEUX[1], objet='#c8413a'):
    aid = f'personne-{name}-{"nuit" if night else "jour"}'
    s = S(aid, night)
    person(s, name, night)
    svg = s.svg(f'Personnage : {name}', pad=1)
    style = f'--haut:{haut};--bas:{bas};--peau:{peau};--cheveux:{cheveux};--objet:{objet}'
    return svg.replace('<svg ', f'<svg style="{style}" ', 1)


# ======================================================================  mobilier
def poubelle_bac(s):
    g = '#3f6a4c'
    s.shadow(-0.35, -0.4, 0.35, 0.4, 1.1)
    s.box(-0.35, -0.4, 0, 0.35, 0.4, 1.0, g, top=False)
    s.box(-0.4, -0.48, 1.0, 0.4, 0.45, 1.1, mix(g, '#ffffff', 0.08))
    s.fline('L', 0.4, (-0.25, 0.85), (0.25, 0.85), s.ink(s.col(g, NL)), w=0.5)
    for x in (-0.22, 0.22):
        s.circle_s((x, 0.42, 0.1), 1.0, '#1f1d20')


def poubelle_rue(s):
    s.line((0, 0, 0), (0, 0, 0.6), '#2f2b2d', w=0.9)
    s.cyl(0, 0, 0.28, 0.4, 1.0, '#4a6455', seg=12, topc='#2b2a30')


def poubelle_debordante(s):
    poubelle_bac(s)
    for x, y, r, c in ((0.6, 0.3, 0.32, '#2b2a30'), (0.45, 0.85, 0.28, '#3a3a40'), (-0.2, 0.75, 0.26, '#d9d2c3')):
        X, Y = s.P(x, y, r * 0.8)
        s.raw(f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="{r * U:.1f}" ry="{r * U * 0.8:.1f}" fill="{s.col(c, NL)}" stroke="{s.ink(s.col(c, NL))}" stroke-width="0.3"/>')
        s.pts += [(X - r * U, Y - r * U), (X + r * U, Y + r * U)]
    X, Y = s.P(-0.05, -0.05, 1.25)
    s.raw(f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="3" ry="2" fill="{s.col("#2b2a30", NL)}"/>')


def banc(s):
    wood, iron = '#8a5f3c', '#2f2b2d' if not s.night else '#101018'
    s.shadow(-1.0, -0.3, 1.0, 0.3, 0.8)
    for x in (-0.8, 0.8):
        s.line((x, 0.2, 0), (x, 0.2, 0.45), iron, w=0.8)
        s.line((x, -0.2, 0), (x, -0.2, 0.9), iron, w=0.8)
    for i, y in enumerate((-0.25, -0.05, 0.15)):
        s.box(-1.0, y, 0.42, 1.0, y + 0.14, 0.48, wood, sw=0.25)
    for z in (0.6, 0.78):
        s.box(-1.0, -0.3, z, 1.0, -0.22, z + 0.1, wood, sw=0.25)


def arbuste(s, kind='rond'):
    base = {'rond': '#6f8f4e', 'laurier': '#5f7f4a', 'buis': '#5d7b45'}[kind]
    if kind == 'buis':
        s.shadow(-0.5, -0.5, 0.5, 0.5, 0.9)
        s.box(-0.55, -0.55, 0, 0.55, 0.55, 0.3, '#b57a52')
        s.box(-0.5, -0.5, 0.3, 0.5, 0.5, 1.1, base)
        return
    X, Y = s.P(0, 0, 0.55)
    R = 0.8 * U
    if not s.night:
        s.raw(f'<ellipse cx="{X + 5:.1f}" cy="{Y + 6:.1f}" rx="{R * 1.2:.1f}" ry="{R * 0.45:.1f}" fill="{SHADOW_TINT}" opacity="0.15"/>')
    dk, lt = s.col(base, NR), s.col(base, NL)
    for dx, dy, k in ((0, 0, 1), (-0.5, 0.15, 0.7), (0.5, 0.2, 0.7), (0, -0.35, 0.65)):
        s.raw(f'<circle cx="{X + dx * R:.1f}" cy="{Y + dy * R:.1f}" r="{k * R * 0.7:.1f}" fill="{dk}"/>')
    s.raw(f'<circle cx="{X - R * 0.2:.1f}" cy="{Y - R * 0.2:.1f}" r="{R * 0.5:.1f}" fill="{lt}"/>')
    if kind == 'laurier':
        rng = s.rng
        for _ in range(14):
            a, r = rng.uniform(0, 6.28), rng.uniform(0, R * 0.8)
            s.raw(f'<circle cx="{X + math.cos(a) * r:.1f}" cy="{Y + math.sin(a) * r * 0.8:.1f}" r="0.9" fill="{s.col("#e7799a", NL)}"/>')
    s.pts += [(X - R, Y - R), (X + R * 1.5, Y + R)]


def jardiniere(s):
    s.shadow(-1, -0.4, 1, 0.4, 0.8)
    s.box(-1, -0.4, 0, 1, 0.4, 0.5, '#c0805a')
    rng = s.rng
    for i in range(7):
        x = -0.85 + i * 0.28
        X, Y = s.P(x, 0, 0.6)
        c = s.col(rng.choice(['#6f8f4e', '#7f9f55', '#5f7f4a']), NL)
        s.raw(f'<circle cx="{X:.1f}" cy="{Y - 1:.1f}" r="2.4" fill="{c}"/>')
        if rng.random() < 0.5:
            s.raw(f'<circle cx="{X + 0.6:.1f}" cy="{Y - 2.4:.1f}" r="0.8" fill="{s.col(rng.choice(["#e7799a", "#f2c14e", "#f4f1ea"]), NL)}"/>')
    s.pts += [s.P(-1, 0, 1.2), s.P(1, 0, 1.2)]


def potelets(s):
    c = '#3e4a44' if not s.night else '#141a20'
    for x in (-1.2, 0, 1.2):
        s.cyl(x, 0, 0.09, 0, 0.85, c, seg=8)
        s.cyl(x, 0, 0.12, 0.85, 0.95, mix(c, '#c9a54a', 0.5), seg=8)


def panneau(s):
    s.line((0, 0, 0), (0, 0, 2.4), '#8e9398', w=0.8)
    X, Y = s.P(0, 0.05, 2.6)
    s.raw(f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="3.6" ry="4.2" fill="{s.col("#f4f1ea", NL)}" stroke="{s.col("#c8413a", NL)}" stroke-width="1.2"/>')
    s.pts += [(X - 5, Y - 5)]


def feu(s):
    s.line((0, 0, 0), (0, 0, 2.6), '#2f2b2d', w=0.9)
    s.box(-0.12, 0.0, 2.3, 0.12, 0.3, 3.2, '#2f2b2d', sw=0.3)
    on = 2 if s.night else 0
    for i, (c, z) in enumerate((('#e0473f', 3.0), ('#f2b134', 2.75), ('#42b36b', 2.5))):
        X, Y = s.P(0, 0.3, z)
        lit = i == 2
        col = c if lit else mix(c, '#222222', 0.65)
        if lit and s.night:
            s.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="7" fill="{s.g("glow")}"/>')
        s.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="0.9" fill="{col}"/>')


def lampadaire_variant(s, mode):
    c = '#2b2a30' if not s.night else '#0d0e18'
    h = 4.5
    s.line((0, 0, 0), (0, 0, h), c, w=0.9)
    s.line((0, 0, h), (0.6, 0, h), c, w=0.8)
    X, Y = s.P(0.6, 0, h - 0.2)
    X0, Y0 = s.P(0.6, 0, 0)
    s.pts += [(X - 16, Y - 16), (X0 + 32, Y0 + 16), (X0 - 32, Y0)]
    if mode == 'eteint':
        s.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="1.3" fill="#4a4a55" stroke="{c}" stroke-width="0.4"/>')
        return
    anim = ''
    if mode == 'gresille':
        anim = f' class="{s.k}g"'
        # variation lente (pas d'éclair), coupée si le visiteur demande moins de mouvement
        s.raw(f'<style>@keyframes {s.k}g{{0%,100%{{opacity:1}}40%{{opacity:.4}}55%{{opacity:.55}}70%{{opacity:.35}}}}.{s.k}g{{animation:{s.k}g 5s ease-in-out infinite}}@media (prefers-reduced-motion:reduce){{.{s.k}g{{animation:none}}}}</style>')
    s.raw(f'<g{anim}><ellipse cx="{X0:.1f}" cy="{Y0:.1f}" rx="32" ry="16" fill="{s.g("pool")}"/><circle cx="{X:.1f}" cy="{Y:.1f}" r="16" fill="{s.g("glow")}"/><circle cx="{X:.1f}" cy="{Y:.1f}" r="1.6" fill="#fff4d0"/></g>')


def fontaine(s):
    st = '#d6c6a2'
    s.shadow(-1.2, -1.2, 1.2, 1.2, 0.6)
    s.cyl(0, 0, 1.3, 0, 0.5, st, seg=20, topc='#e6dbc3')
    s.poly([s.cpt(0, 0, 1.1, 2 * math.pi * i / 20, 0.5) for i in range(20)], s.g('water'), stroke=None)
    s.cyl(0, 0, 0.18, 0.5, 1.4, st, seg=10)
    s.cyl(0, 0, 0.45, 1.4, 1.55, st, seg=14, topc='#e6dbc3')
    X, Y = s.P(0, 0, 1.6)
    s.raw(f'<path d="M{X:.1f} {Y:.1f}q-3 -4 -5 3M{X:.1f} {Y:.1f}q3 -4 5 3" fill="none" stroke="#bfe3ec" stroke-width="0.7"/>')


def velo(s):
    c = '#2f2b2d' if not s.night else '#101018'
    f = '#c8413a'
    A, B = s.P(-0.5, 0, 0.33), s.P(0.5, 0, 0.33)
    s.pts += [(A[0] - 4, A[1] - 4), (B[0] + 4, B[1] + 4), (A[0] - 4, A[1] + 4)]
    for X, Y in (A, B):
        s.raw(f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="3.6" ry="3.9" fill="none" stroke="{c}" stroke-width="0.6"/>')
    s.pline([(-0.5, 0, 0.33), (-0.1, 0, 0.75), (0.35, 0, 0.75), (0.5, 0, 0.33)], s.col(f, NL), w=0.7)
    s.line((-0.1, 0, 0.75), (0, 0, 0.33), s.col(f, NL), w=0.7)
    s.line((-0.15, 0, 0.9), (-0.05, 0, 0.9), c, w=1.0)
    s.line((0.35, 0, 0.75), (0.32, 0, 0.98), c, w=0.6)


def terrasse(s):
    for x, y in ((-0.7, -0.5), (0.8, 0.6)):
        s.cyl(x, y, 0.32, 0.7, 0.75, '#e9e2d4', seg=12)
        s.line((x, y, 0), (x, y, 0.7), '#2f2b2d', w=0.6)
        for dx in (-0.45, 0.45):
            s.box(x + dx - 0.15, y - 0.15, 0.42, x + dx + 0.15, y + 0.15, 0.47, '#4f6b55', sw=0.2)
    s.line((0, 0, 0), (0, 0, 2.2), '#6b4b33', w=0.6)
    X, Y = s.P(0, 0, 2.3)
    s.pts += [(X - 23, Y - 6), (X + 23, Y + 7)]
    s.raw(f'<path d="M{X - 22:.1f} {Y + 6:.1f}Q{X:.1f} {Y - 10:.1f} {X + 22:.1f} {Y + 6:.1f}Q{X:.1f} {Y + 2:.1f} {X - 22:.1f} {Y + 6:.1f}Z" fill="{s.col("#f1e6d2", NL)}" stroke="{s.col("#a8452f", NL)}" stroke-width="0.8"/>')


def flaque(s):
    pts = [(math.cos(a) * (1.2 + 0.25 * math.sin(3 * a)), math.sin(a) * (0.8 + 0.2 * math.cos(2 * a)), 0) for a in [i / 16 * 6.283 for i in range(16)]]
    s.poly(pts, s.g('water'), stroke=None, op=0.75)
    s.line((-0.5, -0.1, 0), (0.1, -0.1, 0), '#ffffff', w=0.5, op=0.5)


def feuilles(s):
    rng = s.rng
    for _ in range(26):
        x, y = rng.uniform(-1.5, 1.5), rng.uniform(-1, 1)
        X, Y = s.P(x, y, 0)
        c = s.col(rng.choice(['#c9772f', '#d99a3a', '#a8552c', '#e0b04a']), NT)
        s.raw(f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="1.2" ry="0.6" fill="{c}" transform="rotate({rng.randint(0, 180)} {X:.1f} {Y:.1f})"/>')
    s.pts += [s.P(-1.5, -1, 0), s.P(1.5, 1, 0), s.P(1.5, -1, 0), s.P(-1.5, 1, 0)]


def pigeons(s):
    rng = s.rng
    for _ in range(5):
        x, y = rng.uniform(-1, 1), rng.uniform(-0.7, 0.7)
        X, Y = s.P(x, y, 0)
        g = s.col('#8b8f9a', NL)
        d = rng.choice((-1, 1))
        s.raw(f'<ellipse cx="{X:.1f}" cy="{Y - 1.2:.1f}" rx="1.6" ry="1.0" fill="{g}"/><circle cx="{X + 1.4 * d:.1f}" cy="{Y - 2.3:.1f}" r="0.6" fill="{s.col("#6d7180", NL)}"/><path d="M{X - 1.4 * d:.1f} {Y - 1.3:.1f}l{-1 * d} -0.4" stroke="{s.col("#5a5e6a", NL)}" stroke-width="0.6"/>')
    s.pts += [s.P(-1, -0.7, 0.5), s.P(1, 0.7, 0), s.P(1, -0.7, 0), s.P(-1, 0.7, 0)]


def chat(s):
    X, Y = s.P(0, 0, 0)
    c = s.col('#e0974a', NL)
    s.pts += [(X - 5, Y - 7), (X + 5, Y + 1)]
    s.raw(f'<ellipse cx="{X + 0.8:.1f}" cy="{Y + 0.2:.1f}" rx="3" ry="0.9" fill="#1b1730" opacity="0.2"/><path d="M{X - 2:.1f} {Y:.1f}q0 -3.2 2 -3.4q2.2 0 2.2 3.4Z" fill="{c}"/><circle cx="{X - 1.2:.1f}" cy="{Y - 4.3:.1f}" r="1.5" fill="{c}"/><path d="M{X - 2.5:.1f} {Y - 5:.1f}l0.2 -1.6l1 1.1M{X - 0.8:.1f} {Y - 5.5:.1f}l0.6 -1.4l0.4 1.5" fill="{c}"/><path d="M{X + 2.1:.1f} {Y - 0.4:.1f}q2.2 -0.4 1.8 -3" fill="none" stroke="{c}" stroke-width="0.8"/>')


# ----------------------------------------------------------------- incongrus
def piano(s):
    k = '#1c1a1f' if not s.night else '#08070b'
    s.shadow(-1, -0.7, 1, 0.7, 1.0)
    for x, y in ((-0.8, -0.5), (0.8, -0.4), (-0.6, 0.5)):
        s.line((x, y, 0), (x, y, 0.65), k, w=0.9)
    pts = [(-1.0, -0.7), (0.9, -0.55), (1.3, -0.1), (0.6, 0.35), (-0.2, 0.55), (-1.0, 0.65)]
    s.poly([(x, y, 0.65) for x, y in pts], mix(k, '#555566', 0.25))
    s.poly([(x, y, 1.0) for x, y in pts], mix(k, '#777788', 0.3))
    s.poly([(-1.0, 0.65, 0.65), (-0.2, 0.55, 0.65), (-0.2, 0.55, 1.0), (-1.0, 0.65, 1.0)], k)
    s.poly([(-1.0, -0.7, 1.0), (0.9, -0.55, 1.0), (0.9, -0.55, 2.0)], mix(k, '#555566', 0.2))
    s.poly([(-1.05, 0.65, 0.95), (-1.05, -0.7, 0.95), (-1.25, -0.7, 0.9), (-1.25, 0.65, 0.9)], '#f4f1ea', stroke=None)
    for i in range(10):
        y = -0.65 + i * 0.13
        s.line((-1.2, y, 0.93), (-1.12, y, 0.93), k, w=0.4)


def baignoire(s):
    w = '#f4f1ea'
    s.shadow(-1.0, -0.45, 1.0, 0.45, 0.7)
    for x, y in ((-0.8, -0.35), (0.8, -0.35), (-0.8, 0.35), (0.8, 0.35)):
        s.line((x, y, 0), (x, y, 0.2), '#c9a54a', w=1.2)
    pts = [(math.cos(a) * 1.0, math.sin(a) * 0.45) for a in [i / 24 * 6.283 for i in range(24)]]
    vis = [(x, y) for x, y in pts]
    s.poly([(x, y, 0.2) for x, y in vis] , s.col(w, NL))
    s.poly([(x, y, 0.75) for x, y in vis], s.col(w, NT))
    s.poly([(x * 0.85, y * 0.75, 0.74) for x, y in vis], s.g('water'), stroke=None)
    for i in range(8):
        a = i / 8 * 6.283
        X, Y = s.P(math.cos(a) * 0.4, math.sin(a) * 0.2, 0.8)
        s.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="1.4" fill="#ffffff" opacity="0.9"/>')


def taureau(s):
    k = s.col('#2a2224', NL) if not s.night else '#3a3550'
    X, Y = s.P(0, 0, 0)
    s.pts += [(X - 16, Y - 22), (X + 16, Y + 3)]
    s.raw(f'<ellipse cx="{X + 2:.1f}" cy="{Y + 0.5:.1f}" rx="13" ry="3" fill="#1b1730" opacity="{0.18 if not s.night else 0.3}"/>')
    s.raw(f'<path d="M{X - 10:.1f} {Y - 9:.1f}C{X - 11:.1f} {Y - 15:.1f} {X - 4:.1f} {Y - 17:.1f} {X + 2:.1f} {Y - 16:.1f}C{X + 7:.1f} {Y - 15.5:.1f} {X + 10:.1f} {Y - 13:.1f} {X + 9:.1f} {Y - 8:.1f}L{X + 8:.1f} {Y:.1f}H{X + 6.6:.1f}L{X + 6:.1f} {Y - 6:.1f}L{X - 3:.1f} {Y - 6.5:.1f}L{X - 4:.1f} {Y:.1f}H{X - 5.4:.1f}L{X - 6:.1f} {Y - 6.5:.1f}C{X - 8:.1f} {Y - 7:.1f} {X - 9.5:.1f} {Y - 7.5:.1f} {X - 10:.1f} {Y - 9:.1f}Z" fill="{k}"/>')
    s.raw(f'<path d="M{X - 9:.1f} {Y - 14:.1f}C{X - 13:.1f} {Y - 15:.1f} {X - 16:.1f} {Y - 12:.1f} {X - 15:.1f} {Y - 8.5:.1f}C{X - 14:.1f} {Y - 6.5:.1f} {X - 11:.1f} {Y - 7:.1f} {X - 9.5:.1f} {Y - 9:.1f}Z" fill="{k}"/>')
    hc = s.col('#efe6d2', NL)
    s.raw(f'<path d="M{X - 13.5:.1f} {Y - 13.8:.1f}q-1.5 -3.5 1 -6q-0.4 3 1.2 5.4ZM{X - 10.8:.1f} {Y - 14.6:.1f}q0.6 -3.8 3.4 -5q-1.6 2.6 -1.9 5.2Z" fill="{hc}"/>')
    s.raw(f'<path d="M{X + 9:.1f} {Y - 13:.1f}q4 1 3 6" fill="none" stroke="{k}" stroke-width="0.8"/>')


def poisson(s):
    X, Y = s.P(0, 0, 5)
    X0, Y0 = s.P(0, 0, 0)
    s.pts += [(X - 20, Y - 12), (X + 20, Y0 + 3)]
    c = s.col('#e8784a', NL)
    s.raw(f'<ellipse cx="{X0:.1f}" cy="{Y0:.1f}" rx="9" ry="2.4" fill="#1b1730" opacity="0.15"/>')
    s.raw(f'<path d="M{X - 13:.1f} {Y:.1f}C{X - 8:.1f} {Y - 9:.1f} {X + 7:.1f} {Y - 9:.1f} {X + 11:.1f} {Y:.1f}C{X + 7:.1f} {Y + 8:.1f} {X - 8:.1f} {Y + 8:.1f} {X - 13:.1f} {Y:.1f}Z" fill="{c}"/>')
    s.raw(f'<path d="M{X + 10:.1f} {Y:.1f}l7 -6l-1.5 6l1.5 6Z" fill="{s.col("#d4603a", NL)}"/>')
    s.raw(f'<path d="M{X - 4:.1f} {Y - 6:.1f}q3 -5 7 -1Z" fill="{s.col("#d4603a", NL)}"/>')
    s.raw(f'<circle cx="{X - 7.5:.1f}" cy="{Y - 1.5:.1f}" r="1.6" fill="#fff"/><circle cx="{X - 7.8:.1f}" cy="{Y - 1.5:.1f}" r="0.8" fill="#1b1730"/>')
    for i in range(3):
        s.raw(f'<path d="M{X - 1 + i * 3.5:.1f} {Y - 4:.1f}q2 4 0 8" fill="none" stroke="{s.col("#f6b27a", NL)}" stroke-width="0.7"/>')


# ------------------------------------------------------------- arbres de saison
SAISONS = {'printemps': ('#9cc46a', '#f2b8c6'), 'ete': ('#7f9f55', None), 'automne': ('#d4893a', '#b85a2e'), 'hiver': (None, None)}


def platane_saison(s, saison):
    green, accent = SAISONS[saison]
    h, r = 10, 3.0
    if saison == 'hiver':
        trunk = s.col('#a3957c', NL)
        X0, Y0 = s.P(0, 0, 0)
        if not s.night:
            s.raw(f'<ellipse cx="{X0 + 24:.1f}" cy="{Y0:.1f}" rx="30" ry="9" fill="{SHADOW_TINT}" opacity="0.1"/>')
        s.line((0, 0, 0), (0, 0, h * 0.55), trunk, w=2.0)
        X, Y = s.P(0, 0, h * 0.55)
        s.pts += [(X - 30, Y - 50), (X + 30, Y0 + 10)]
        br = []
        for a, L in ((-0.9, 26), (-0.4, 32), (0.1, 30), (0.6, 28), (1.0, 22), (-1.2, 18)):
            ex, ey = X + math.sin(a) * L, Y - math.cos(a) * L
            br.append(f'M{X:.1f} {Y:.1f}Q{X + math.sin(a) * L * 0.3:.1f} {Y - L * 0.6:.1f} {ex:.1f} {ey:.1f}')
            for b in (-0.5, 0.5):
                br.append(f'M{X + math.sin(a) * L * 0.6:.1f} {Y - math.cos(a) * L * 0.6:.1f}l{math.sin(a + b) * 9:.1f} {-math.cos(a + b) * 9:.1f}')
        s.raw(f'<path d="{"".join(br)}" fill="none" stroke="{trunk}" stroke-width="0.9"/>')
        return
    s.tree(0, 0, h=h, r=r, kind='platane') if saison == 'ete' else None
    if saison != 'ete':
        s.line((0, 0, 0), (0, 0, h * 0.55), s.col('#9a8a70', NL), w=2.0)
        X, Y = s.P(0, 0, h * 0.72)
        R = r * U
        s.pts += [(X - R * 1.3, Y - R * 1.2), (X + R * 1.3, Y + R)]
        if not s.night:
            X0, Y0 = s.P(0, 0, 0)
            s.raw(f'<ellipse cx="{X0 + R * 0.8:.1f}" cy="{Y0:.1f}" rx="{R * 1.2:.1f}" ry="{R * 0.5:.1f}" fill="{SHADOW_TINT}" opacity="0.15"/>')
        dark, base, hi = s.col(green, NR), s.col(green, NL), s.col(green, NT)
        blobs = [(0, 0, 1.0), (-0.45, 0.15, 0.7), (0.45, 0.2, 0.72), (0.05, -0.35, 0.7), (-0.2, 0.35, 0.6), (0.3, -0.15, 0.6)]
        k = 0.85 if saison == 'automne' else 1.0
        for dx, dy, kk in blobs:
            s.raw(f'<circle cx="{X + dx * R:.1f}" cy="{Y + dy * R * 0.8:.1f}" r="{kk * R * 0.72 * k:.1f}" fill="{dark}"/>')
        for dx, dy, kk in blobs[:4]:
            s.raw(f'<circle cx="{X + dx * R - R * 0.12:.1f}" cy="{Y + dy * R * 0.8 - R * 0.1:.1f}" r="{kk * R * 0.55 * k:.1f}" fill="{base}"/>')
        s.raw(f'<circle cx="{X - R * 0.28:.1f}" cy="{Y - R * 0.3:.1f}" r="{R * 0.3 * k:.1f}" fill="{hi}" opacity="0.8"/>')
        rng = s.rng
        for _ in range(22):
            a, rr = rng.uniform(0, 6.28), rng.uniform(0, R * 0.85)
            s.raw(f'<circle cx="{X + math.cos(a) * rr:.1f}" cy="{Y + math.sin(a) * rr * 0.8:.1f}" r="1.1" fill="{s.col(accent, NL)}"/>')


MOBILIER = {
    'poubelle-bac': poubelle_bac, 'poubelle-rue': poubelle_rue, 'poubelle-debordante': poubelle_debordante,
    'banc': banc, 'arbuste': lambda s: arbuste(s, 'rond'), 'laurier-rose': lambda s: arbuste(s, 'laurier'),
    'buis-taille': lambda s: arbuste(s, 'buis'), 'jardiniere': jardiniere, 'potelets': potelets,
    'panneau': panneau, 'feu-tricolore': feu, 'fontaine': fontaine, 'velo': velo, 'terrasse-cafe': terrasse,
    'lampadaire-eteint': lambda s: lampadaire_variant(s, 'eteint'),
    'lampadaire-gresille': lambda s: lampadaire_variant(s, 'gresille'),
    'flaque': flaque, 'feuilles-mortes': feuilles, 'pigeons': pigeons, 'chat': chat,
    'platane-printemps': lambda s: platane_saison(s, 'printemps'), 'platane-ete': lambda s: platane_saison(s, 'ete'),
    'platane-automne': lambda s: platane_saison(s, 'automne'), 'platane-hiver': lambda s: platane_saison(s, 'hiver'),
}
INCONGRUS = {'piano': piano, 'baignoire': baignoire, 'taureau': taureau, 'poisson-volant': poisson}
POSTURES_ALLURE = ['debout', 'marche', 'course', 'assis', 'parapluie']
POSTURES_EMOTION = {'joie': 'joie', 'tristesse': 'tristesse', 'colere': 'colere', 'peur': 'peur',
                    'surprise': 'surprise', 'degout': 'degout', 'neutre': 'debout'}
