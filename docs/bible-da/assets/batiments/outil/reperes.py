"""Repères de Béziers, dessinés sur mesure d'après photos.

Chaque fonction dessine dans la scène `s` et renvoie l'emprise au sol (x0, y0, x1, y1)
utilisée pour centrer l'asset.
"""
import math
from iso import S, rect, arch, circ, NL, NR, NT, mix, norm

STONE = '#d6c6a2'
TILE = '#c46a43'
IRON = '#2f2b2d'


def crenels(s, x0, y0, x1, y1, z, base, m=0.7, gap=0.55, h=0.8, t=0.45):
    items = []
    step = m + gap
    x = x0
    while x + m <= x1 + 1e-6:
        items.append((x, y0, x + m, y0 + t))
        items.append((x, y1 - t, x + m, y1))
        x += step
    y = y0 + t + gap
    while y + m <= y1 - t + 1e-6:
        items.append((x0, y, x0 + t, y + m))
        items.append((x1 - t, y, x1, y + m))
        y += step
    for a in sorted(items, key=lambda r: r[2] + r[3]):
        s.box(a[0], a[1], z, a[2], a[3], z + h, base, sw=0.3)


def cyl_pts(cx, cy, R, uz, z_only=False):
    """Coordonnées (s, z) le long d'un cylindre : s = longueur d'arc en mètres."""
    return [(cx + R * math.cos(u / R), cy + R * math.sin(u / R), z) for u, z in uz]


def ground(s, pts, colr, op=1.0, stroke=None):
    s.poly([(x, y, 0) for x, y in pts], s.col(colr, NT), stroke=stroke, op=op)


def paving(s, x0, y0, x1, y1, colr='#e4dccb', step=1.2):
    ground(s, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], colr)
    c = s.ink(s.col(colr, NT), 0.15)
    x = x0 + step
    while x < x1:
        s.line((x, y0, 0), (x, y1, 0), c, w=0.3, op=0.35)
        x += step
    y = y0 + step
    while y < y1:
        s.line((x0, y, 0), (x1, y, 0), c, w=0.3, op=0.35)
        y += step


# ======================================================================
def cathedrale(s):
    st = '#d3c29c'
    dk = '#3b3640'
    s.shadow(-1, 2, 19, 41, 34)
    paving(s, -3, 41, 21, 47, '#e2d8c3')
    # chevet polygonal (derrière)
    s.cyl(9, 3, 7.5, 0, 21, st, seg=8, rot=math.pi / 8, topc='#b9a888')
    s.cone(9, 3, 8.0, 21, 24.5, TILE, seg=8, rot=math.pi / 8)
    for th in (math.radians(22.5), math.radians(67.5), math.radians(112.5), math.radians(-22.5)):
        n = (math.cos(th), math.sin(th))
        if n[0] + n[1] < 0.05:
            continue
        r = 7.5 * math.cos(math.pi / 8) + 0.05
        cx, cy = 9 + r * math.cos(th), 3 + r * math.sin(th)
        tx, ty = -math.sin(th), math.cos(th)
        pts = [(cx + tx * u, cy + ty * u, z) for u, z in arch(-0.7, 0.7, 7, 17, pointed=True)]
        s.poly(pts, s.g('lit') if s.night else s.col('#3d4652', n + (0,)), sw=0.4)
    # clocher principal (côté -x, derrière la nef)
    tx0, ty0, tx1, ty1, TH = -8, 15, 0, 23, 44
    s.box(tx0, ty0, 0, tx1, ty1, TH, st)
    s.joints('L', ty1, tx0, tx1, 0, TH, step=0.7, op=0.15)
    for u in (tx0 + 2.2, tx1 - 2.2):
        s.window('L', ty1, u, 35.5, 1.3, 5.2, pointed=True, surround=st, sill=False, mull=False, lit=False)
        s.window('L', ty1, u, 27, 0.5, 2.6, pointed=True, surround=None, sill=False, mull=False, lit=False)
    s.band('L', ty1, tx0, tx1, 33.6, h=0.35, colr='#e2d6ba')
    s.band('L', ty1, tx0, tx1, 41.6, h=0.35, colr='#e2d6ba')
    corners = [(tx0, ty0), (tx1, ty0), (tx0, ty1), (tx1, ty1)]
    for cx, cy in corners[:2]:
        s.cyl(cx, cy, 1.0, TH - 3, TH + 1.6, st, seg=12, topc='#c9b893')
    crenels(s, tx0, ty0, tx1, ty1, TH, st)
    # campanile en fer
    mx, my = (tx0 + tx1) / 2, (ty0 + ty1) / 2
    ic = IRON if not s.night else '#0b0b14'
    top = (mx, my, TH + 6.5)
    for a, b in ((-1.4, -1.4), (1.4, -1.4), (1.4, 1.4), (-1.4, 1.4)):
        s.line((mx + a, my + b, TH), top, ic, w=0.7)
    s.line((mx - 1.4, my + 1.4, TH + 1.5), (mx + 1.4, my + 1.4, TH + 1.5), ic, w=0.5)
    s.line((mx + 1.4, my - 1.4, TH + 1.5), (mx + 1.4, my + 1.4, TH + 1.5), ic, w=0.5)
    s.circle_s((mx, my, TH + 3.2), 3.2, '#8a6a3a' if not s.night else '#4a3a2a', stroke=ic, sw=0.4)
    s.line(top, (mx, my, TH + 8.2), ic, w=0.5)
    for cx, cy in corners[2:]:
        s.cyl(cx, cy, 1.0, TH - 3, TH + 1.6, st, seg=12, topc='#c9b893')
    # nef
    NX0, NY0, NX1, NY1, NH = 0, 3, 18, 38, 22
    s.box(NX0, NY0, 0, NX1, NY1, NH, st, top=False)
    s.ao('R', NX1, NY0, NY1)
    s.joints('R', NX1, NY0, NY1, 0, NH, step=0.7, op=0.14)
    for k in range(6):
        y = NY0 + 0.6 + 1.3 + 2.15 + k * 5.6
        s.window('R', NX1, y, 9, 1.6, 9, pointed=True, surround=st, sill=False, mull=True)
    s.roof(NX0, NY0, NX1, NY1, NH, 'gable', pitch=0.22, ov=0.0, tile=TILE, wall=st, axis='y')
    for k in range(7):
        y = NY0 + 0.6 + k * 5.6
        s.box(NX1, y, 0, NX1 + 1.6, y + 1.3, NH - 2.5, st)
        s.poly([(NX1, y, NH - 2.5), (NX1 + 1.6, y, NH - 2.5), (NX1 + 1.6, y + 1.3, NH - 2.5), (NX1, y + 1.3, NH - 2.5)], s.col(st, NT))
    crenels(s, NX1 - 0.6, NY0, NX1, NY1, NH, st, t=0.6)
    s.genoise('R', NX1, NY0, NY1, NH)
    # façade ouest
    FY0, FY1 = 36, 41
    s.box(-1.5, FY0, 0, 4, FY1, 31, st)
    s.joints('L', FY1, -1.5, 4, 0, 31, step=0.7, op=0.16)
    s.window('L', FY1, 1.25, 23, 0.9, 4.2, pointed=True, surround=st, sill=False, mull=False, lit=False)
    s.window('L', FY1, 1.25, 10, 0.4, 2.4, surround=None, sill=False, mull=False, lit=False)
    crenels(s, -1.5, FY0, 4, FY1, 31, st)
    s.box(4, FY0 + 1, 0, 14, FY1, 26, st)
    s.joints('L', FY1, 4, 14, 0, 26, step=0.7, op=0.16)
    # mâchicoulis
    s.fpoly('L', FY1, rect(4, 14, 22.2, 23.2), s.col('#e2d6ba', NL), o=0.35)
    for k in range(12):
        u = 4.3 + k * 0.82
        s.fpoly('L', FY1, rect(u, u + 0.4, 21.6, 22.2), s.col('#cbb994', NL), o=0.3, sw=0.3)
    # rosace
    rc, rz, rr = 9, 15.5, 3.9
    s.fpoly('L', FY1, circ(rc, rz, rr + 0.55, 36), s.col('#e6dbc2', NL))
    s.fpoly('L', FY1, circ(rc, rz, rr, 36), s.g('rose') if s.night else s.col('#3e4658', NL), sw=0.4)
    tc = s.col('#e6dbc2', NL)
    for k in range(12):
        a = 2 * math.pi * k / 12
        s.fline('L', FY1, (rc + math.cos(a) * 0.9, rz + math.sin(a) * 0.9), (rc + math.cos(a) * rr, rz + math.sin(a) * rr), tc, w=0.8)
        s.fpoly('L', FY1, circ(rc + math.cos(a + 0.26) * rr * 0.72, rz + math.sin(a + 0.26) * rr * 0.72, 0.45, 12), 'none', stroke=tc, sw=0.5)
    s.fpoly('L', FY1, circ(rc, rz, 0.9, 16), tc)
    s.fpoly('L', FY1, circ(rc, rz, rr * 0.55, 30), 'none', stroke=tc, sw=0.6)
    # portail et gâble
    s.fpoly('L', FY1, [(6.0, 7.0), (12.0, 7.0), (9, 10.8)], s.col('#e2d6ba', NL))
    for i, w in enumerate((5.2, 4.4, 3.6)):
        c = mix('#cbb994', '#4a4048', i * 0.3)
        s.fpoly('L', FY1, arch(9 - w / 2, 9 + w / 2, 0, 3.6 + w * 0.95, pointed=True), s.col(c, NL), sw=0.35)
    s.fpoly('L', FY1, rect(7.3, 10.7, 0, 3.6), s.col('#5a3c2b', NL))
    s.fline('L', FY1, (9, 0), (9, 3.6), s.ink(s.col('#5a3c2b', NL)), w=0.5)
    for u in (5.0, 13.0):
        s.fpoly('L', FY1, rect(u - 0.35, u + 0.35, 2.2, 4.4), s.col('#e8decb', NL))
    crenels(s, 4, FY0 + 1, 14, FY1, 26, st)
    s.box(14, FY0, 0, 19.5, FY1, 31, st)
    s.joints('L', FY1, 14, 19.5, 0, 31, step=0.7, op=0.16)
    s.joints('R', 19.5, FY0, FY1, 0, 31, step=0.7, op=0.16)
    s.window('L', FY1, 16.75, 23, 0.9, 4.2, pointed=True, surround=st, sill=False, mull=False, lit=False)
    s.window('R', 19.5, 38.5, 20, 0.8, 3.6, pointed=True, surround=st, sill=False, mull=False, lit=False)
    crenels(s, 14, FY0, 19.5, FY1, 31, st)
    # échauguette d'angle
    s.cyl(19.5, FY1, 1.1, 27, 32.4, st, seg=14, topc='#c9b893')
    s.cone(19.5, FY1, 1.25, 32.4, 34.2, '#9b8a6c', seg=14)
    s.ground_glow((9, FY1 + 2, 0), 9 * 10, 30)
    s.lamppost(2, 45)
    s.lamppost(16, 45)
    s.tree(-2.5, 44, h=10, r=1.4, kind='cypres')
    s.tree(21, 43, h=11, r=1.5, kind='cypres')
    return (-8, 0, 21, 47)


# ======================================================================
def mairie(s):
    st = '#e3d4b2'
    W, D, H = 24, 14, 16.5
    paving(s, -3, D, W + 3, D + 8, '#e6ddca')
    s.shadow(0, 0, W, D, H + 10)
    s.walls(0, 0, W, D, 0, H, st)
    s.joints('L', D, 0, W, 4.5, H, step=0.55, op=0.15)
    s.joints('R', W, 0, D, 4.5, H, step=0.55, op=0.15)
    s.joints('L', D, 0, W, 0, 4.5, step=0.5, op=0.3, vert=True)
    s.joints('R', W, 0, D, 0, 4.5, step=0.5, op=0.3, vert=True)
    for face, plane, u1 in (('L', D, W), ('R', W, D)):
        s.band(face, plane, 0, u1, 4.4, h=0.3, colr='#efe6d2')
        s.band(face, plane, 0, u1, 9.0, h=0.2, colr='#efe6d2')
        s.band(face, plane, 0, u1, 12.9, h=0.2, colr='#efe6d2')
        s.band(face, plane, -0.15, u1 + 0.15, H - 0.6, h=0.6, colr='#efe6d2')
    bays = [1.7 + i * 3.43 for i in range(7)]
    for i, u in enumerate(bays):
        if i == 3:
            continue
        s.window('L', D, u, 0.9, 1.4, 2.8, arch_=True, surround='#efe6d2', sill=False)
        s.window('L', D, u, 5.4, 1.15, 2.6, arch_=True, surround='#efe6d2', shut=None)
        s.window('L', D, u, 9.9, 1.1, 2.1, surround='#efe6d2')
        s.window('L', D, u, 13.6, 1.0, 1.4, surround='#efe6d2')
    for u in (1.8, 5.2, 8.8, 12.2):
        s.window('R', W, u, 0.9, 1.3, 2.8, arch_=True, surround='#efe6d2', sill=False)
        s.window('R', W, u, 5.4, 1.1, 2.6, arch_=True, surround='#efe6d2')
        s.window('R', W, u, 9.9, 1.05, 2.1, surround='#efe6d2')
        s.window('R', W, u, 13.6, 0.95, 1.4, surround='#efe6d2')
    s.roof(0, 0, W, D, H, 'hip', pitch=0.3, ov=0.45, tile=TILE)
    # avant-corps central
    ax0, ax1 = 10.0, 14.0
    s.box(ax0, D, 0, ax1, D + 0.5, H + 0.4, st, topc='#efe6d2')
    pl = D + 0.5
    s.joints('L', pl, ax0, ax1, 0, H, step=0.55, op=0.2)
    s.door('L', pl, 12, 2.0, 4.0, colr='#4c3426', arch_=True, surround='#efe6d2')
    s.window('L', pl, 12, 5.1, 1.3, 3.1, arch_=True, surround='#efe6d2', bal=False, sill=False)
    s.balcony('L', pl, 10.4, 13.6, 5.0, dp=0.8)
    s.window('L', pl, 12, 9.9, 1.15, 2.3, surround='#efe6d2')
    s.window('L', pl, 12, 13.6, 1.0, 1.4, surround='#efe6d2')
    s.flag(10.3, pl + 0.8, 6.0, h=2.4, face='L')
    s.flag(13.7, pl + 0.8, 6.0, h=2.4, face='L')
    # tour de l'horloge
    tx0, tx1, ty0, ty1 = 10.2, 13.8, D - 3.0, D + 0.4
    TZ = H + 7.4
    s.box(tx0, ty0, H - 0.5, tx1, ty1, TZ, st, topc='#efe6d2')
    s.joints('L', ty1, tx0, tx1, H, TZ, step=0.55, op=0.2)
    s.band('L', ty1, tx0 - 0.1, tx1 + 0.1, H + 3.4, h=0.3, colr='#efe6d2')
    s.band('R', tx1, ty0, ty1, H + 3.4, h=0.3, colr='#efe6d2')
    # blason
    s.fpoly('L', ty1, arch(11.0, 13.0, H + 0.5, H + 3.0), s.col('#efe6d2', NL))
    s.fpoly('L', ty1, [(11.45, H + 2.5), (12.55, H + 2.5), (12.55, H + 1.5), (12, H + 0.9), (11.45, H + 1.5)], s.col('#b2453c', NL), sw=0.4)
    s.fpoly('L', ty1, [(11.45, H + 2.5), (12.55, H + 2.5), (12.55, H + 2.15), (11.45, H + 2.15)], s.col('#c9a54a', NL), stroke=None)
    # horloge
    cz = H + 5.4
    s.fpoly('L', ty1, circ(12, cz, 1.35, 28), s.col('#efe6d2', NL))
    s.fpoly('L', ty1, circ(12, cz, 1.1, 28), '#fff6dc' if s.night else s.col('#fbf7ee', NL), sw=0.4)
    if s.night:
        X, Y = s.P(*s.fp('L', ty1, 12, cz))
        s.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="22" fill="{s.g("glow")}"/>')
    hc = '#2a2526'
    s.fline('L', ty1, (12, cz), (12, cz + 0.8), hc, w=0.6)
    s.fline('L', ty1, (12, cz), (12.55, cz - 0.15), hc, w=0.6)
    s.fpoly('R', tx1, circ((ty0 + ty1) / 2, cz, 1.1, 24), s.col('#fbf7ee', NR), sw=0.4)
    # balustrade + pots à feu
    for face, plane, u0, u1 in (('L', ty1, tx0, tx1), ('R', tx1, ty0, ty1)):
        s.fpoly(face, plane, rect(u0, u1, TZ, TZ + 0.25), s.col('#efe6d2', s.fn(face)), sw=0.3)
        k = int((u1 - u0) / 0.3)
        for i in range(1, k):
            u = u0 + (u1 - u0) * i / k
            s.fline(face, plane, (u, TZ + 0.25), (u, TZ + 0.95), s.col('#dccdae', s.fn(face)), w=1.1)
        s.fpoly(face, plane, rect(u0, u1, TZ + 0.95, TZ + 1.2), s.col('#efe6d2', s.fn(face)), sw=0.3)
    for cx, cy in ((tx0, ty0), (tx1, ty0), (tx0, ty1), (tx1, ty1)):
        s.box(cx - 0.25, cy - 0.25, TZ, cx + 0.25, cy + 0.25, TZ + 1.5, '#efe6d2', sw=0.3)
        s.circle_s((cx, cy, TZ + 1.9), 2.6, s.col('#efe6d2', NL), stroke=s.ink(s.col('#efe6d2', NL)), sw=0.3)
    # campanile en fer forgé
    mx, my = (tx0 + tx1) / 2, (ty0 + ty1) / 2
    ic = IRON if not s.night else '#0b0b14'
    apex = (mx, my, TZ + 5.2)
    for a, b in ((-1.2, -1.2), (1.2, -1.2), (1.2, 1.2), (-1.2, 1.2)):
        s.pline([(mx + a, my + b, TZ + 1.2), (mx + a * 0.9, my + b * 0.9, TZ + 3.0), apex], ic, w=0.6)
    s.circle_s((mx, my, TZ + 2.6), 3.4, '#9a7b3e' if not s.night else '#5a4628', stroke=ic, sw=0.4)
    s.line(apex, (mx, my, TZ + 7.0), ic, w=0.5)
    s.line((mx, my, TZ + 6.4), (mx + 0.9, my, TZ + 6.4), ic, w=0.5)
    # place
    s.ground_glow((12, D + 3, 0), 120, 40)
    for x in (-1.5, W + 1.5):
        s.tree(x, D + 4, h=10, r=3.0, kind='platane')
    s.lamppost(5, D + 5.5)
    s.lamppost(19, D + 5.5)
    return (-3, 0, W + 3, D + 8)


# ======================================================================
def polygone(s):
    white = '#efeae0'
    s.shadow(0, 0, 44, 14, 24)
    paving(s, -1, 14, 46, 24.5, '#e3dccd')
    # bloc A (arrière), en gradins
    A = (0, 0, 44, 14)
    s.walls(0, 0, 44, 14, 0, 20, white)
    s.shop('L', 14, 0.5, 20, h=4.2, awn=None, frame='#45484d')
    s.shop('L', 14, 24, 43.5, h=4.2, awn=None, frame='#45484d')
    s.shop('R', 44, 0.5, 13.5, h=4.2, awn=None, frame='#45484d')
    for f in range(5):
        z = 5 + f * 3
        for face, plane, u1 in (('L', 14, 44), ('R', 44, 14)):
            k = int(u1 / 3.2)
            for i in range(k):
                u = 1.6 + i * u1 / k
                s.window(face, plane, u, z + 0.35, 1.9, 2.1, surround=None, sill=False)
            s.fpoly(face, plane, rect(0, u1, z - 0.3, z + 0.05), s.col('#ffffff', s.fn(face)), o=0.9, sw=0.3)
            s.fpoly(face, plane, rect(0, u1, z + 0.05, z + 1.0), s.col('#a9c7d2', s.fn(face)), o=0.9, stroke=None, op=0.5)
    s.flat_roof(0, 0, 44, 14, 20, para=0.9, floor='#b9b2a6')
    s.box(0, 0, 20, 30, 9, 23.2, white)
    for i in range(9):
        s.window('L', 9, 1.7 + i * 3.3, 20.5, 2.0, 2.0, surround=None, sill=False)
    s.flat_roof(0, 0, 30, 9, 23.6, para=0.4, floor='#b9b2a6')
    # bois en façade (bardage)
    wood = '#b9895b'
    s.fpoly('L', 14, rect(20.5, 23.5, 4.4, 20), s.col(wood, NL))
    for i in range(1, 12):
        u = 20.5 + 3 * i / 12
        s.fline('L', 14, (u, 4.4), (u, 20), s.ink(s.col(wood, NL), 0.2), w=0.4)
    # rue piétonne : arbres + pergola
    for x in (5, 14, 30, 39):
        s.tree(x, 19, h=5.5, r=1.9, kind='olivier')
    cols = [(x, y) for x in range(2, 45, 6) for y in (14.6, 23.4)]
    for x, y in [c for c in cols if c[1] < 20]:
        s.box(x - 0.18, y - 0.18, 0, x + 0.18, y + 0.18, 12, '#f6f4ef', sw=0.25)
    zg = 12
    glass = '#bfe0ea' if not s.night else '#3d5a7a'
    s.poly([(1, 14.2, zg), (45, 14.2, zg), (45, 23.8, zg), (1, 23.8, zg)], glass, stroke=None, op=0.45)
    bc = s.col('#ffffff', NL)
    for x in range(1, 46, 2):
        s.line((x, 14.2, zg), (x, 23.8, zg), bc, w=0.7)
    for y in (14.6, 19, 23.4):
        s.box(1, y - 0.15, zg - 0.4, 45, y + 0.15, zg, '#f6f4ef', sw=0.25)
    for x, y in [c for c in cols if c[1] > 20]:
        s.box(x - 0.18, y - 0.18, 0, x + 0.18, y + 0.18, 12, '#f6f4ef', sw=0.25)
    # bloc B (avant, bas)
    s.shadow(0, 24.5, 34, 32, 8)
    s.walls(0, 24.5, 34, 32, 0, 7.5, '#e6e0d4')
    s.shop('L', 32, 0.5, 33.5, h=4.0, awn=None, frame='#3f4247')
    s.shop('R', 34, 25, 31.5, h=4.0, awn=None, frame='#3f4247')
    for i in range(1, 34 * 3):
        u = i / 3
        s.fline('L', 32, (u, 4.4), (u, 7.5), s.ink(s.col(wood, NL), 0.15), w=0.35)
    s.fpoly('L', 32, rect(0, 34, 4.4, 7.5), s.col(wood, NL), op=0.55, stroke=None)
    s.fpoly('R', 34, rect(24.5, 32, 4.4, 7.5), s.col(wood, NR), op=0.55, stroke=None)
    s.flat_roof(0, 24.5, 34, 32, 7.5, para=0.6, floor='#b9b2a6')
    for x, y in ((8, 28), (20, 27)):
        s.box(x, y, 6.9, x + 3, y + 2, 8.6, '#d4cec2')
    # rotonde avec écran
    cx, cy, R, H = 51, 18, 8.5, 21
    s.shadow(cx - R, cy - R, cx + R, cy + R, H)
    s.cyl(cx, cy, R, 0, H, '#f2efe8', seg=48, top=True, topc='#c9c3b8')
    for z in range(5, 21, 3):
        s.pline([s.cpt(cx, cy, R + 0.02, math.radians(a), z) for a in range(-44, 136, 4)], s.col('#c9cdd2', NL), w=0.5, op=0.7)
    band = [s.cpt(cx, cy, R + 0.05, math.radians(a), 8) for a in range(-30, 121, 5)] + [s.cpt(cx, cy, R + 0.05, math.radians(a), 17) for a in range(120, -31, -5)]
    s.poly(band, s.g('screen'), stroke=s.col('#2a2a30', NL), sw=0.5, op=1.0 if s.night else 0.92)
    if s.night:
        X, Y = s.P(cx + R * 0.7, cy + R * 0.7, 12)
        s.raw(f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="120" ry="70" fill="{s.g("glow")}"/>')
    glassb = [s.cpt(cx, cy, R + 0.05, math.radians(a), 0) for a in range(-44, 136, 5)] + [s.cpt(cx, cy, R + 0.05, math.radians(a), 4.2) for a in range(135, -45, -5)]
    s.poly(glassb, s.g('shop') if s.night else s.col('#56707f', NL), stroke=None)
    for a in range(-40, 136, 12):
        s.line(s.cpt(cx, cy, R + 0.06, math.radians(a), 0), s.cpt(cx, cy, R + 0.06, math.radians(a), 4.2), '#3f4247', w=0.6)
    s.tree(40, 33, h=8, r=1.6, kind='palmier')
    s.tree(60, 30, h=9, r=1.7, kind='palmier')
    return (0, 0, 60, 32)


# ======================================================================
def gare(s):
    st = '#e5cb9c'
    iron = '#56635e'
    # voies et marquise (derrière)
    ground(s, [(-4, -16), (64, -16), (64, -1), (-4, -1)], '#9d968c')
    rc = s.col('#6b6660', NT)
    for y in (-14, -12.6, -9.5, -8.1, -5, -3.6):
        s.line((-4, y, 0.05), (64, y, 0.05), rc, w=0.6)
    for y in (-15.2, -2.4):
        s.box(-2, y - 1.3, 0, 62, y + 1.3, 0.9, '#cfc6b5')
    zc = 7.5
    cols = [(x, y) for x in range(0, 61, 6) for y in (-15, -2.6)]
    for x, y in cols:
        s.line((x, y, 0.9), (x, y, zc), s.col(iron, NL), w=1.0)
    gl = '#c9e0e4' if not s.night else '#334a66'
    s.roof(-2, -16, 62, -1.5, zc, 'gable', pitch=0.22, ov=0.0, tile=gl, axis='x', wall=iron, mat='zinc')
    for x in range(-2, 63, 2):
        s.line((x, -1.5, zc), (x, -8.75, zc + 7.25 * 0.22), s.col(iron, NL), w=0.45)
    # bâtiment voyageurs
    W, D = 60, 12
    s.shadow(0, 0, W, D, 12)
    wings = [(0, 6, 8.5), (6, 22, 7.2), (22, 38, 11.8), (38, 54, 7.2), (54, 60, 8.5)]
    for x0, x1, h in wings:
        y0, y1 = (-0.6, D + 0.6) if (x1 - x0) <= 6 or h > 11 else (0, D)
        s.walls(x0, y0, x1, y1, 0, h, st)
        s.joints('L', y1, x0, x1, 0, h, step=0.5, op=0.16)
        if x1 == W:
            s.joints('R', x1, y0, y1, 0, h, step=0.5, op=0.16)
        s.band('L', y1, x0, x1, 0, h=0.6, colr='#d8bd8d')
        s.band('L', y1, x0 - 0.1, x1 + 0.1, h - 0.55, h=0.55, colr='#f0e2c4')
        if h > 11:
            n = 4
            for k in range(n):
                u = x0 + 2 + k * (x1 - x0 - 4) / (n - 1)
                s.window('L', y1, u, 0.2, 2.4, 5.2, arch_=True, surround='#f0e2c4', sill=False)
                s.window('L', y1, u, 7.0, 1.2, 2.6, arch_=True, surround='#f0e2c4')
            s.band('L', y1, x0, x1, 6.0, h=0.3, colr='#f0e2c4')
        else:
            n = int((x1 - x0) / 3.2)
            for k in range(n):
                u = x0 + (x1 - x0) * (k + 0.5) / n
                s.window('L', y1, u, 0.4, 1.7, 4.0 if h < 8 else 4.4, arch_=True, surround='#f0e2c4', sill=False)
        if x1 == W:
            for k in range(3):
                s.window('R', W, y0 + 2.5 + k * 4.3, 0.4, 1.6, 4.2, arch_=True, surround='#f0e2c4', sill=False)
        s.roof(x0, y0, x1, y1, h, 'hip', pitch=0.3, ov=0.35, tile=TILE)
    # fronton avec horloge
    pl = D + 0.6
    zb = 11.8
    s.fpoly('L', pl, arch(25.5, 34.5, zb, zb + 3.6, seg=16), s.col('#f0e2c4', NL))
    s.fpoly('L', pl, [(25.2, zb), (34.8, zb), (34.8, zb + 0.35), (25.2, zb + 0.35)], s.col('#e0c99c', NL))
    cz = zb + 1.6
    s.fpoly('L', pl, circ(30, cz, 1.2, 26), '#fff6dc' if s.night else s.col('#fbf7ee', NL), sw=0.4)
    s.fline('L', pl, (30, cz), (30, cz + 0.8), '#2a2526', w=0.6)
    s.fline('L', pl, (30, cz), (30.6, cz + 0.2), '#2a2526', w=0.6)
    if s.night:
        X, Y = s.P(*s.fp('L', pl, 30, cz))
        s.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="22" fill="{s.g("glow")}"/>')
    s.fpoly('L', pl, rect(29.7, 30.3, zb + 3.6, zb + 4.6), s.col('#f0e2c4', NL))
    s.ground_glow((30, D + 4, 0), 180, 50)
    paving(s, 0, D + 0.6, 60, D + 7, '#e3dccd')
    for x in (4, 18, 42, 56):
        s.tree(x, D + 5, h=9, r=2.6, kind='platane')
    s.lamppost(26, D + 5.5)
    s.lamppost(34, D + 5.5)
    return (-4, -16, 64, D + 7)


# ======================================================================
def cimetiere(s):
    W, D = 46, 38
    wall = '#d8c9a8'
    s.shadow(0, 0, W, D, 3)
    ground(s, [(0, 0), (W, 0), (W, D), (0, D)], '#ddd3bb')
    ground(s, [(21, 0.6), (25, 0.6), (25, D), (21, D)], '#cfc4a8')
    ground(s, [(0.6, 17), (W, 17), (W, 20), (0.6, 20)], '#cfc4a8')
    s.box(0, 0, 0, W, 0.6, 2.6, wall, topc='#ece2cc')
    s.box(0, 0.6, 0, 0.6, D, 2.6, wall, topc='#ece2cc')
    rng = s.rng
    items = []
    for y in [2.5 + 3.0 * i for i in range(12)]:
        if 16 < y < 20.5 or y > D - 2:
            continue
        for x in [2.2 + 2.3 * i for i in range(19)]:
            if 20 < x < 25.5 or x > W - 2:
                continue
            r = rng.random()
            if r < 0.1:
                items.append(('chapelle', x, y))
            elif r < 0.9:
                items.append(('tombe', x, y))
    for y in range(3, int(D), 4):
        if 16 < y < 21:
            continue
        items.append(('cypres', 20.3, y))
        items.append(('cypres', 25.7, y))
    for _ in range(9):
        items.append(('cypres', rng.uniform(2, W - 2), rng.uniform(2, D - 2)))
    for x, y in ((8, 6), (38, 30), (12, 30)):
        items.append(('pin', x, y))
    items.append(('statue', 23, 18.5))
    for kind, x, y in sorted(items, key=lambda t: t[1] + t[2]):
        if kind == 'tombe':
            m = rng.choice(['#efebe3', '#e6e1d6', '#d9d4ca', '#c9c4bb'])
            s.box(x - 0.5, y - 1.0, 0, x + 0.5, y + 1.0, 0.55, m, sw=0.3)
            if rng.random() < 0.6:
                s.box(x - 0.45, y - 1.0, 0.55, x + 0.45, y - 0.8, 1.6, m, sw=0.3)
            else:
                c = s.ink(s.col(m, NL), 0.5)
                s.line((x, y - 0.9, 0.55), (x, y - 0.9, 2.0), c, w=0.8)
                s.line((x - 0.35, y - 0.9, 1.6), (x + 0.35, y - 0.9, 1.6), c, w=0.8)
        elif kind == 'chapelle':
            m = rng.choice(['#e8e2d4', '#d9cdb3', '#c7bba3'])
            s.box(x - 1.0, y - 1.2, 0, x + 1.0, y + 1.2, 2.8, m, top=False, sw=0.35)
            s.door('L', y + 1.2, x, 0.8, 1.8, colr='#3c3a3f', surround=None)
            s.roof(x - 1.0, y - 1.2, x + 1.0, y + 1.2, 2.8, 'gable', pitch=0.7, ov=0.15, tile=mix(m, '#7a7468', 0.3), wall=m, axis='y', tex=False)
            X, Y = s.P(x, y + 1.25, 3.5)
            s.raw(f'<path d="M{X:.1f},{Y - 4:.1f}v6M{X - 2:.1f},{Y - 2:.1f}h4" stroke="{s.ink(s.col(m, NL), 0.4)}" stroke-width="0.6"/>')
        elif kind == 'cypres':
            s.tree(x, y, h=rng.uniform(9, 12), r=1.25, kind='cypres')
        elif kind == 'pin':
            s.tree(x, y, h=9, r=3.2, kind='pin')
        elif kind == 'statue':
            s.box(x - 0.6, y - 0.6, 0, x + 0.6, y + 0.6, 1.8, '#e8e2d4')
            s.cyl(x, y, 0.35, 1.8, 3.4, '#f1ede6', seg=10)
            s.circle_s((x, y, 3.8), 2.4, s.col('#f1ede6', NL))
    # murs avant + portail
    s.box(W - 0.6, 0.6, 0, W, D, 2.6, wall, topc='#ece2cc')
    s.box(0, D - 0.6, 0, 20.2, D, 2.6, wall, topc='#ece2cc')
    s.box(25.8, D - 0.6, 0, W - 0.6, D, 2.6, wall, topc='#ece2cc')
    for a in (20.0, 25.0):
        s.box(a, D - 0.9, 0, a + 1.0, D + 0.1, 5.2, '#e6dcc4', topc='#f0e8d6')
    pl = D + 0.1
    pts = [(20.0, 6.4), (26.0, 6.4), (26.0, 5.2), (25.0, 5.2)] + [(23 + 2 * math.cos(t * math.pi / 14), 3.6 + 2 * math.sin(t * math.pi / 14)) for t in range(0, 15)] + [(21.0, 5.2), (20.0, 5.2)]
    s.fpoly('L', pl, pts, s.col('#e6dcc4', NL))
    s.fpoly('L', pl, [(19.7, 6.4), (26.3, 6.4), (23, 7.9)], s.col('#efe6d2', NL))
    ic = IRON if not s.night else '#0b0b14'
    for k in range(17):
        u = 21.05 + k * 3.9 / 16
        s.fline('L', D - 0.3, (u, 0), (u, 3.6 + 2 * math.sqrt(max(0, 1 - ((u - 23) / 2) ** 2)) - 0.1), ic, w=0.35)
    s.lamppost(18.5, D + 2)
    s.lamppost(27.5, D + 2)
    return (0, 0, W, D)


# ======================================================================
def arenes(s):
    brick = '#b8603f'
    stone = '#e6d6b4'
    R, H = 24.0, 15.0
    if not s.night:
        pts = [(R * math.cos(t / 20 * 6.283), R * math.sin(t / 20 * 6.283)) for t in range(20)]
        pts += [(x + H * 0.42, y - H * 0.42) for x, y in pts]
        from iso import hull
        s.poly([(x, y, 0) for x, y in hull(pts)], '#2b2440', stroke=None, op=0.16)
    # gradins
    rings = 9
    r_out, r_in = R - 1.2, 12.5
    s.poly([s.cpt(0, 0, R, 2 * math.pi * i / 64, H) for i in range(64)], s.col(stone, NT), sw=0.4)
    for k in range(rings + 1):
        r = r_out - (r_out - r_in) * k / rings
        z = H - 0.4 - (H - 2.8) * k / rings
        c = '#cdbb9b' if k % 2 else '#bba985'
        s.poly([s.cpt(0, 0, r, 2 * math.pi * i / 64, z) for i in range(64)], s.col(c, NT), stroke=None)
        if k < rings:
            r2 = r_out - (r_out - r_in) * (k + 1) / rings
            z2 = H - 0.4 - (H - 2.8) * (k + 1) / rings
            for i in range(32):
                a = math.pi * 0.75 + math.pi * i / 32
                b = math.pi * 0.75 + math.pi * (i + 1) / 32
                n = (-math.cos((a + b) / 2), -math.sin((a + b) / 2), 0)
                s.poly([s.cpt(0, 0, r2, a, z2), s.cpt(0, 0, r2, b, z2), s.cpt(0, 0, r2, b, z), s.cpt(0, 0, r2, a, z)], s.col('#a8916f', n), stroke=None)
    # piste + barrière
    zb = 2.8
    s.poly([s.cpt(0, 0, r_in, 2 * math.pi * i / 64, 1.4) for i in range(64)], s.col('#e4c792', NT), stroke=None)
    for i in range(32):
        a = math.pi * 0.75 + math.pi * i / 32
        b = math.pi * 0.75 + math.pi * (i + 1) / 32
        n = (-math.cos((a + b) / 2), -math.sin((a + b) / 2), 0)
        s.poly([s.cpt(0, 0, r_in, a, 1.4), s.cpt(0, 0, r_in, b, 1.4), s.cpt(0, 0, r_in, b, zb), s.cpt(0, 0, r_in, a, zb)], s.col('#8e3a2c', n), stroke=None)
    s.poly([s.cpt(0, 0, r_in - 1.2, 2 * math.pi * i / 48, 1.42) for i in range(48)], 'none', stroke=s.col('#d1b27a', NT), sw=0.6)
    # mur extérieur
    s.cyl(0, 0, R, 0, H, brick, seg=64, top=False)
    for z0, z1 in ((0, 0.8), (6.6, 7.2), (H - 0.9, H)):
        band = [s.cpt(0, 0, R + 0.05, math.radians(a), z0) for a in range(-45, 136, 3)] + [s.cpt(0, 0, R + 0.05, math.radians(a), z1) for a in range(135, -46, -3)]
        s.poly(band, s.col(stone, NL), stroke=s.ink(s.col(stone, NL), 0.2), sw=0.3)
    nA = 44
    for i in range(nA):
        th = 2 * math.pi * i / nA
        if math.cos(th) + math.sin(th) < 0.12:
            continue
        if abs(th - math.pi / 2) < 0.2:
            continue
        n = (math.cos(th), math.sin(th), 0)
        u = th * R
        for z0, z1, w in ((0.8, 6.0, 2.4), (7.6, 13.4, 2.2)):
            s.poly(cyl_pts(0, 0, R + 0.06, arch(u - w / 2 - 0.35, u + w / 2 + 0.35, z0, z1 + 0.35)), s.col(stone, n), sw=0.3)
            lit = s.night and z0 < 1 and s.rng.random() < 0.5
            s.poly(cyl_pts(0, 0, R + 0.08, arch(u - w / 2, u + w / 2, z0, z1)), s.g('lit') if lit else s.col('#4a2c24', n), sw=0.3)
    # pavillon d'entrée rayé
    px0, px1, py0, py1, PH = -6.5, 6.5, R - 3.5, R + 1.8, 18.5
    s.box(px0, py0, 0, px1, py1, PH, stone, top=True)
    for face, plane, u0, u1 in (('L', py1, px0, px1), ('R', px1, py0, py1)):
        z = 1.0
        while z < PH - 1:
            s.fpoly(face, plane, rect(u0, u1, z, z + 0.55), s.col(brick, s.fn(face)), stroke=None)
            z += 1.1
    s.fpoly('L', py1, arch(-3.2, 3.2, 0, 8.6), s.col('#f0e4c9', NL))
    s.fpoly('L', py1, arch(-2.6, 2.6, 0, 8.0), s.g('lit') if s.night else s.col('#3d2a24', NL), sw=0.4)
    ic = IRON if not s.night else '#0b0b14'
    for k in range(13):
        u = -2.6 + k * 5.2 / 12
        s.fline('L', py1, (u, 0), (u, 5.6 + 2.4 * math.sqrt(max(0, 1 - (u / 2.6) ** 2)) - 0.2), ic, w=0.4)
    for u in (-4.6, 0, 4.6):
        s.window('L', py1, u, 10.5, 1.4, 3.4, arch_=True, surround='#f0e4c9', sill=False)
    s.window('R', px1, R - 0.85, 10.5, 1.4, 3.4, arch_=True, surround='#f0e4c9', sill=False)
    s.window('R', px1, R - 0.85, 2.5, 1.4, 3.4, arch_=True, surround='#f0e4c9', sill=False)
    s.band('L', py1, px0 - 0.1, px1 + 0.1, PH - 0.6, h=0.6, colr=stone)
    s.band('R', px1, py0, py1 + 0.1, PH - 0.6, h=0.6, colr=stone)
    crenels(s, px0, py0, px1, py1, PH, stone, m=0.6, gap=0.6, h=0.7)
    # tourelle centrale
    s.box(-2.6, R - 2.6, PH, 2.6, R + 1.2, PH + 5.5, stone)
    for face, plane, u in (('L', R + 1.2, 0), ('R', 2.6, R - 0.7)):
        s.window(face, plane, u, PH + 1.8, 1.1, 2.6, arch_=True, surround=stone, sill=False)
        z = PH + 0.6
        s.fpoly(face, plane, rect(u - 2.6 if face == 'L' else R - 2.6, u + 2.6 if face == 'L' else R + 1.2, z, z + 0.5), s.col(brick, s.fn(face)), stroke=None)
    s.roof(-2.6, R - 2.6, 2.6, R + 1.2, PH + 5.5, 'hip', pitch=0.5, ov=0.35, tile=TILE)
    s.flag(0, R - 0.7, PH + 7.6, h=2.6, face='L')
    s.ground_glow((0, R + 4, 0), 120, 40)
    for x in (-10, 10):
        s.tree(x, R + 4, h=8.5, r=1.7, kind='palmier')
    return (-R, -R, R, R + 2)


# ======================================================================
def halles(s):
    W, D = 36, 20
    brick, iron, louv = '#b8613f', '#55615f', '#efe6cf'
    s.shadow(0, 0, W, D, 13)
    s.walls(0, 0, W, D, 0, 1.4, brick)
    s.box(0, 0, 1.4, W, D, 8.2, louv, top=False)
    for face, plane, u1 in (('L', D, W), ('R', W, D)):
        n = s.fn(face)
        z = 1.7
        while z < 5.0:
            s.fline(face, plane, (0, z), (u1, z), s.ink(s.col(louv, n), 0.25), w=0.35, op=0.7)
            z += 0.22
        k = int(u1 / 3)
        for i in range(k):
            u = u1 * (i + 0.5) / k
            s.window(face, plane, u, 5.25, u1 / k - 0.7, 2.6, arch_=True, surround=None, sill=False)
        for i in range(k + 1):
            u = u1 * i / k
            s.box(*(((u - 0.15, plane, 1.4, u + 0.15, plane + 0.25, 8.2)) if face == 'L' else ((plane, u - 0.15, 1.4, plane + 0.25, u + 0.15, 8.2))), iron, top=False, sw=0.25)
        for z in (1.4, 5.0, 8.0):
            s.fpoly(face, plane, rect(0, u1, z, z + 0.2), s.col(iron, n), o=0.25, sw=0.25)
    zr = s.roof(0, 0, W, D, 8.2, 'hip', pitch=0.36, ov=0.5, tile='#8b98a5', mat='zinc')
    # lanterneau
    lx0, lx1, ly0, ly1 = 7, 29, 8.3, 11.7
    zl = zr - 0.6
    s.box(lx0, ly0, zl - 1, lx1, ly1, zl + 2.0, louv, top=False)
    for face, plane, u0, u1 in (('L', ly1, lx0, lx1), ('R', lx1, ly0, ly1)):
        n = s.fn(face)
        z = zl - 0.6
        while z < zl + 1.9:
            s.fline(face, plane, (u0, z), (u1, z), s.ink(s.col(louv, n), 0.25), w=0.35, op=0.7)
            z += 0.22
        u = u0
        while u <= u1:
            s.fline(face, plane, (u, zl - 1), (u, zl + 2), s.col(iron, n), w=0.6)
            u += 2.2
    s.roof(lx0, ly0, lx1, ly1, zl + 2.0, 'hip', pitch=0.4, ov=0.5, tile='#8b98a5', mat='zinc')
    # campanile horloge
    cx, cy = 18, 10
    zc = zl + 2.0 + 1.0
    s.box(cx - 1.1, cy - 1.1, zc - 1, cx + 1.1, cy + 1.1, zc + 2.6, louv)
    s.fpoly('L', cy + 1.1, circ(cx, zc + 1.3, 0.75, 20), '#fff6dc' if s.night else s.col('#fbf7ee', NL), sw=0.4)
    s.fpoly('R', cx + 1.1, circ(cy, zc + 1.3, 0.75, 20), s.col('#fbf7ee', NR), sw=0.4)
    s.cone(cx, cy, 1.6, zc + 2.6, zc + 4.4, '#7f8d9a', seg=4, rot=math.pi / 4)
    s.line((cx, cy, zc + 4.4), (cx, cy, zc + 5.6), IRON, w=0.5)
    # portail en pierre
    st = '#efe3c6'
    p0, p1 = 14, 22
    s.box(p0, D - 0.3, 0, p1, D + 0.9, 9.0, st, topc='#f5ecd8')
    pl = D + 0.9
    s.joints('L', pl, p0, p1, 0, 9, step=0.5, op=0.22, vert=True)
    s.fpoly('L', pl, arch(15.4, 20.6, 0, 7.4), s.col('#e2d3ae', NL))
    s.glass('L', pl, 18, 0, 4.4, 6.9, arch_=True, mull=True)
    s.fpoly('L', pl, arch(p0 - 0.2, p1 + 0.2, 9.0, 12.2, seg=16), s.col(st, NL))
    s.fpoly('L', pl, arch(16.6, 19.4, 9.4, 11.2), s.col('#e2d3ae', NL))
    s.fpoly('L', pl, rect(p0 - 0.3, p1 + 0.3, 8.6, 9.1), s.col('#f5ecd8', NL))
    for u in (p0 + 0.3, p1 - 0.3):
        s.fpoly('L', pl, rect(u - 0.3, u + 0.3, 9.1, 12.6), s.col(st, NL))
        s.circle_s(s.fp('L', pl, u, 12.9), 2.4, s.col(st, NL), stroke=s.ink(s.col(st, NL)), sw=0.3)
    s.ground_glow((18, D + 4, 0), 140, 40)
    paving(s, -1, D + 0.9, W + 1, D + 6, '#e3dccd')
    for x in (3, 33):
        s.tree(x, D + 4, h=9, r=2.6, kind='platane')
    return (-1, 0, W + 1, D + 6)


# ======================================================================
def pont_vieux(s):
    st = '#d4c09a'
    L, Wd, H = 62, 6, 10
    # rivière (coule selon y), berges
    ground(s, [(-8, -22), (70, -22), (70, 30), (-8, 30)], '#a9b98a')
    s.poly([(2, -22, 0), (58, -22, 0), (58, 30, 0), (2, 30, 0)], s.g('water'), stroke=None)
    for i in range(26):
        x = s.rng.uniform(4, 56)
        y = s.rng.uniform(-12, 20)
        s.line((x, y, 0), (x + 2.2, y, 0), '#ffffff' if not s.night else '#8fa6d0', w=0.5, op=0.35)
    for x0, x1 in ((-8, 2), (58, 70)):
        s.box(x0, -22, 0, x1, 30, 1.2, '#cdbf9d', topc='#b4b98d')
    # tablier et arches
    s.box(0, 0, 0, L, Wd, H, st, top=True, topc='#c9bb9c')
    s.joints('L', Wd, 0, L, 0, H, step=0.55, op=0.16)
    s.joints('R', L, 0, Wd, 0, H, step=0.55, op=0.16)
    span, pier = 5.6, 2.2
    u = 3.0
    piers = []
    while u + span < L - 2:
        s.fpoly('L', Wd, arch(u - 0.4, u + span + 0.4, 0, 0.9 * span + 0.4), s.col('#e3d6b8', NL))
        s.fpoly('L', Wd, arch(u, u + span, 0, 0.9 * span), s.col('#2f3a40', NL) if not s.night else '#0c1222', sw=0.4)
        s.fpoly('L', Wd, rect(u + 0.2, u + span - 0.2, 0, 0.6), s.g('water'), stroke=None, op=0.8)
        u += span
        piers.append(u + pier / 2)
        u += pier
    for p in piers[:-1]:
        b = [(p - pier / 2, Wd, 0), (p + pier / 2, Wd, 0), (p + pier / 2, Wd, 4.2), (p - pier / 2, Wd, 4.2)]
        tip = (p, Wd + 1.8)
        s.poly([(p, Wd + 1.8, 0), (p + pier / 2, Wd, 0), (p + pier / 2, Wd, 4.2), (p, Wd + 1.8, 4.2)], s.col(st, (1, 1, 0)))
        s.poly([(p - pier / 2, Wd, 0), (p, Wd + 1.8, 0), (p, Wd + 1.8, 4.2), (p - pier / 2, Wd, 4.2)], s.col(st, (-0.6, 1, 0)))
        s.poly([(p - pier / 2, Wd, 4.2), (p + pier / 2, Wd, 4.2), (p, Wd, 5.8), (p, Wd + 1.8, 4.2)], s.col('#bfae8b', (0, 0.6, 1)))
    # parapets
    s.box(0, 0, H, L, 0.5, H + 1.0, st, topc='#e3d6b8')
    s.poly([(0, 0.5, H + 0.01), (L, 0.5, H + 0.01), (L, Wd - 0.5, H + 0.01), (0, Wd - 0.5, H + 0.01)], s.col('#a8a090', NT), stroke=None)
    s.box(0, Wd - 0.5, H, L, Wd, H + 1.0, st, topc='#e3d6b8')
    s.band('L', Wd, 0, L, H - 0.3, h=0.3, colr='#e3d6b8')
    for x in (8, 30, 52):
        s.lamppost(x, Wd - 0.8)
    return (-8, -22, 70, 30)


# ======================================================================
def fonseranes(s):
    st = '#d6c6a2'
    water = '#6aa3b2' if not s.night else '#22385a'
    n, Lb, Dd, step = 8, 7.0, 9.0, 2.1
    top = n * step + 1.2
    # bief amont
    s.box(-10, 0, 0, 0, Dd, top, st, top=False)
    s.poly([(-10, 0, top), (0, 0, top), (0, Dd, top), (-10, Dd, top)], s.col('#e6dbc3', NT))
    s.poly([(-10, 1.6, top - 0.15), (0, 1.6, top - 0.15), (0, Dd - 1.6, top - 0.15), (-10, Dd - 1.6, top - 0.15)], water, stroke=None)
    # maison éclusière (derrière)
    s.shadow(14, -10, 21, -4, 7)
    s.walls(14, -10, 21, -4, 0, 6.2, '#e8d2a8')
    s.window('L', -4, 16, 0.9, 1.0, 1.5, shut='#86a890')
    s.door('L', -4, 19, 1.0, 2.3)
    s.window('L', -4, 16, 3.9, 1.0, 1.4, shut='#86a890')
    s.window('L', -4, 19, 3.9, 1.0, 1.4, shut='#86a890')
    s.window('R', 21, -7, 3.9, 1.0, 1.4, shut='#86a890')
    s.genoise('L', -4, 14, 21, 6.2)
    s.roof(14, -10, 21, -4, 6.2, 'hip', tile=TILE)
    for i in range(n):
        x0 = i * Lb
        x1 = x0 + Lb
        zt = (n - i) * step
        s.shadow(x0, 0, x1, Dd, 1.5)
        s.box(x0, 0, 0, x1, Dd, zt, st, top=False)
        s.joints('L', Dd, x0, x1, 0, zt, step=0.55, op=0.16)
        s.joints('R', x1, 0, Dd, 0, zt, step=0.55, op=0.16)
        s.poly([(x0, 0, zt), (x1, 0, zt), (x1, Dd, zt), (x0, Dd, zt)], s.col('#e6dbc3', NT))
        inner = [(x0 + 0.4, 1.6, zt), (x1 - 0.4, 1.6, zt), (x1 - 0.4, Dd - 1.6, zt), (x0 + 0.4, Dd - 1.6, zt)]
        k = s.clip(inner)
        zw = zt - 0.7
        s.poly([(x0 + 0.4, 1.6, zw - 2), (x1 - 0.4, 1.6, zw - 2), (x1 - 0.4, 1.6, zt), (x0 + 0.4, 1.6, zt)], s.col(st, NL), clip=k)
        s.poly([(x0 + 0.4, 1.6, zw - 2), (x0 + 0.4, Dd - 1.6, zw - 2), (x0 + 0.4, Dd - 1.6, zt), (x0 + 0.4, 1.6, zt)], s.col(st, NR), clip=k)
        s.poly([(x0 + 0.4, 1.6, zw), (x1 - 0.4, 1.6, zw), (x1 - 0.4, Dd - 1.6, zw), (x0 + 0.4, Dd - 1.6, zw)], water, clip=k, stroke=None)
        s.line((x0 + 1.5, 4, zw), (x0 + 3.5, 4, zw), '#ffffff', w=0.5, op=0.4, clip=k)
        # portes d'écluse (busquées)
        wd = '#4d3828' if not s.night else '#1a120d'
        gx = x0 + 0.6
        s.pline([(gx, 1.6, zt + 0.1), (gx + 0.9, Dd / 2, zt + 0.1), (gx, Dd - 1.6, zt + 0.1)], wd, w=1.4)
        s.pline([(gx, 1.6, zw), (gx + 0.9, Dd / 2, zw), (gx, Dd - 1.6, zw)], wd, w=0.6)
        # balanciers
        s.line((gx, Dd - 1.6, zt + 0.6), (gx - 1.8, Dd + 0.1, zt + 0.6), wd, w=1.2)
        s.line((gx, 1.6, zt + 0.6), (gx - 2.2, 0.2, zt + 0.6), wd, w=1.2)
        s.lamppost(x0 + 3.5, Dd - 0.5, h=3.2) if i % 3 == 1 else None
    # bief aval
    s.poly([(n * Lb, 1.6, 0.05), (n * Lb + 12, 1.6, 0.05), (n * Lb + 12, Dd - 1.6, 0.05), (n * Lb, Dd - 1.6, 0.05)], water, stroke=None)
    for i in (1, 4, 7):
        s.tree(i * Lb + 2, Dd + 3, h=(n - i) * step + 8, r=2.4, kind='platane') if False else None
    for x in (6, 20, 34, 48):
        s.tree(x, Dd + 3.5, h=8, r=2.3, kind='platane')
    return (-10, -10, n * Lb + 12, Dd + 4)


# ======================================================================
def allees(s):
    L, D = 64, 20
    ground(s, [(0, 0), (L, 0), (L, D), (0, D)], '#e6d9b8')
    ground(s, [(0, 7.5), (L, 7.5), (L, 12.5), (0, 12.5)], '#eadfc4')
    items = []
    for y in (2.5, 17.5):
        for x in range(4, L, 7):
            items.append(('platane', x, y))
    for y in (6.0, 14.0):
        for x in range(25, L, 7):
            items.append(('platane', x, y))
    items.append(('statue', 34, 10))
    items.append(('kiosque', 14, 10))
    for x in (24, 44, 54):
        items.append(('banc', x, 8.2))
        items.append(('lampe', x + 3, 12.2))
    for kind, x, y in sorted(items, key=lambda t: t[1] + t[2]):
        if kind == 'platane':
            s.tree(x, y, h=9.5, r=3.7, kind='platane')
        elif kind == 'banc':
            s.box(x, y, 0.4, x + 1.8, y + 0.5, 0.55, '#6b4b33', sw=0.3)
        elif kind == 'lampe':
            s.lamppost(x, y)
        elif kind == 'statue':
            s.box(x - 1.3, y - 1.3, 0, x + 1.3, y + 1.3, 0.6, '#e8e0cc')
            s.box(x - 0.9, y - 0.9, 0.6, x + 0.9, y + 0.9, 4.2, '#e6dcc4', topc='#efe8d8')
            br = '#4d5a52' if not s.night else '#1c2430'
            s.cyl(x, y, 0.45, 4.2, 6.6, br, seg=10)
            s.circle_s((x, y, 7.0), 2.8, s.col(br, NL))
            s.line((x + 0.3, y + 0.2, 6.2), (x + 0.9, y + 0.6, 5.2), s.col(br, NL), w=1.2)
        elif kind == 'kiosque':
            s.cyl(x, y, 3.2, 0, 0.9, '#e6dcc4', seg=8, rot=math.pi / 8, topc='#efe8d8')
            for i in range(8):
                a = math.pi / 8 + 2 * math.pi * i / 8
                p = s.cpt(x, y, 2.8, a, 0.9)
                s.line(p, (p[0], p[1], 4.4), '#3e5a4d' if not s.night else '#121a22', w=0.8)
            if s.night:
                X, Y = s.P(x, y, 3.0)
                s.raw(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="40" fill="{s.g("glow")}"/>')
            s.cone(x, y, 3.8, 4.4, 6.6, '#5f8a74', seg=8, rot=math.pi / 8)
            s.line((x, y, 6.6), (x, y, 7.6), IRON, w=0.6)
    return (0, 0, L, D)


LANDMARKS = {
    'cathedrale-saint-nazaire': (cathedrale, 'Cathédrale Saint-Nazaire : façade fortifiée, rosace, clocher carré crénelé avec campanile'),
    'hotel-de-ville': (mairie, 'Hôtel de ville (1746) : pierre de taille, avant-corps, tour de l\'horloge et campanile en fer'),
    'polygone': (polygone, 'Polygone : centre commercial à ciel ouvert, gradins blancs, pergola et rotonde à écran'),
    'gare': (gare, 'Gare : bâtiment voyageurs à arcades, pavillon central à horloge, marquise sur les voies'),
    'cimetiere-vieux': (cimetiere, 'Cimetière Vieux : enclos, portail cintré, tombes, chapelles et cyprès'),
    'arenes': (arenes, 'Arènes (1897) : mur de brique à deux rangs d\'arcades, pavillon d\'entrée rayé'),
    'halles': (halles, 'Halles (1891, style Baltard) : fer, persiennes, lanterneau et portail en pierre'),
    'pont-vieux': (pont_vieux, 'Pont-Vieux sur l\'Orb : arches en pierre et avant-becs'),
    'ecluses-fonseranes': (fonseranes, 'Écluses de Fonseranes : escalier de huit bassins sur le canal du Midi'),
    'allees-paul-riquet': (allees, 'Allées Paul-Riquet : platanes, statue de Riquet et kiosque'),
}
