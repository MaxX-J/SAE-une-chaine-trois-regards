"""Scènes de démonstration : la même rue, animée selon des valeurs d'exemple."""
import functools, math, random
from iso import S
import generiques as G
import vie as V

ROWS_BACK = [('immeuble-bourgeois', 0), ('maison-etroite', 1), ('immeuble-commerce', 0), ('maison-ville-r3', 2), ('maison-ville-r2', 1)]
ROWS_FRONT = [('immeuble-bourgeois', 0), ('maison-ville-r3', 0), ('maison-etroite', 2), ('immeuble-commerce', 1), ('maison-ville-r2', 2), ('maison-faubourg', 0)]


def _behind(a, b):
    return a[2] <= b[0] + 1e-6 or a[3] <= b[1] + 1e-6


def _cmp(a, b):
    A, B = a[0], b[0]
    if _behind(A, B) and not _behind(B, A):
        return -1
    if _behind(B, A) and not _behind(A, B):
        return 1
    return (A[0] + A[1] + A[2] + A[3]) - (B[0] + B[1] + B[2] + B[3])


def rue(aid, night=False, emotion='neutre', energie=0.5, tension=0.0, saison='ete', pluie=False, incongru=None, seed=1):
    rng = random.Random(seed)
    s = S(aid, night, seed)
    items = []

    def add(box, fn):
        items.append((box, fn))
    x = 0
    for n, vi in ROWS_BACK:
        W, D = G.FOOT[n]
        add((x, 13 - D, x + W, 13), (lambda n=n, vi=vi, ox=x, oy=13 - D: (s.at(ox, oy), G.draw(s, n, G.VARIANTS[n][vi]))))
        x += W

    def pt(px, py, fn, r=0.3):
        add((px - r, py - r, px + r, py + r), lambda: (s.at(px, py), fn()))
    # arbres et lampadaires
    for tx in (4, 16, 28, 40):
        pt(tx, 29.5, lambda: V.platane_saison(s, saison), r=0.5)
    for tx in (10, 22, 34):
        lamp = 'gresille' if tension >= 0.75 and rng.random() < 0.7 else ('eteint' if tension >= 0.5 and rng.random() < 0.4 else None)
        if lamp and night:
            pt(tx, 15.2, lambda m=lamp: V.lampadaire_variant(s, m))
        else:
            pt(tx, 15.2, lambda: s.lamppost(0, 0))
    # décor selon l'émotion et la tension
    if emotion == 'joie':
        for xx in (7, 31):
            pt(xx, 17.5, lambda: V.terrasse(s), r=1.2)
        pt(20, 25, lambda: V.pigeons(s), r=1)
        pt(44, 18, lambda: V.arbuste(s, 'laurier'))
        pt(44, 22, lambda: V.arbuste(s, 'laurier'))
    if tension >= 0.5:
        for xx in (5, 26, 38):
            pt(xx, 15.4, lambda: V.poubelle_debordante(s), r=0.6)
    else:
        pt(26, 15.4, lambda: V.poubelle_bac(s), r=0.5)
    pt(13, 27, lambda: V.banc(s), r=1)
    if saison == 'automne':
        for xx in (6, 18, 33):
            pt(xx, 27.5, lambda: V.feuilles(s), r=0.1)
    if pluie:
        for xx, yy in ((12, 20), (24, 23), (37, 26)):
            pt(xx, yy, lambda: V.flaque(s), r=0.1)
    # personnages : nombre selon l'énergie, posture selon l'émotion
    n = 3 + int(energie * 16)
    pose_emo = V.POSTURES_EMOTION[emotion]
    for i in range(n):
        px, py = rng.uniform(1, 44), rng.uniform(16.5, 28)
        r = rng.random()
        if pluie and r < 0.6:
            ps = 'parapluie'
        elif r < 0.4:
            ps = pose_emo
        else:
            ps = 'course' if energie > 0.7 and rng.random() < 0.5 else ('marche' if energie > 0.3 else rng.choice(['debout', 'assis']))
        haut = V.EMOTIONS[emotion] if rng.random() < 0.6 else rng.choice(['#9a948a', '#5b6b7a', '#c9b79a', '#3f4a5a'])

        def draw(ps=ps, haut=haut, flip=rng.random() < 0.5):
            X, Y = s.P(0, 0, 0)
            sub = S(s.aid, night)
            V.person(sub, ps, night)
            style = f'--haut:{haut};--bas:{rng.choice(["#3b4252", "#5a4a3a", "#2f3a4f"])};--peau:{rng.choice(V.PEAUX)};--cheveux:{rng.choice(V.CHEVEUX)};--objet:{rng.choice(["#c8413a", "#2f5277", "#f2b134"])}'
            tr = f'translate({X:.1f} {Y:.1f})' + (' scale(-1 1)' if flip else '')
            s.defs.extend(d for d in sub.defs if d not in s.defs)
            s.raw(f'<g transform="{tr}" style="{style}">{"".join(sub.el)}</g>')
        pt(px, py, draw, r=0.2)
    if incongru:
        pt(21, 21, lambda: V.INCONGRUS[incongru](s), r=1.2)
    s.at(0, 0)
    ground = '#e7dfcd'
    s.poly([(-2, -1, 0), (48, -1, 0), (48, 32, 0), (-2, 32, 0)], s.col(ground), stroke=None)
    s.poly([(-2, 13, 0), (48, 13, 0), (48, 15.8, 0), (-2, 15.8, 0)], s.col('#d6cdbb'), stroke=None)
    for it in sorted(items, key=functools.cmp_to_key(_cmp)):
        it[1]()
    s.at(0, 0)
    if pluie:
        X0, Y0 = s.P(-4, 42, 0)
        X1, Y1 = s.P(68, -2, 0)
        d = []
        for _ in range(260):
            x, y = rng.uniform(-330, 480), rng.uniform(-260, 280)
            d.append(f'M{x:.0f} {y:.0f}l-3 9')
        s.raw(f'<path d="{"".join(d)}" stroke="{"#c9d6e6" if not night else "#8fa6d0"}" stroke-width="0.6" opacity="0.55"/>')
    if not night and pluie:
        s.raw('<rect x="-500" y="-400" width="1400" height="900" fill="#5a6a80" opacity="0.12"/>')
    return s.svg('Scène de démonstration')
