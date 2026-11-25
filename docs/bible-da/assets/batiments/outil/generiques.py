"""Bâtiments génériques réutilisables du centre de Béziers."""
from iso import S, rect, arch, NL, NR, NT, mix

WALLS = {'ocre': '#d8a466', 'sable': '#e5cfa2', 'saumon': '#df9f83', 'creme': '#eee0c1', 'paille': '#e8c47c',
         'terre': '#c98f62', 'rose': '#e8b9a3', 'gris': '#d8d1c2', 'pierre': '#ddcba5'}
SHUT = {'bleu': '#7d97ab', 'vert': '#86a890', 'vert-sombre': '#4f6b55', 'lavande': '#9ea3c9', 'bordeaux': '#8c4140',
        'brun': '#6e4c37', 'gris': '#a7aaa8', 'turquoise': '#5f9ea0', 'blanc': '#ece8de'}
TILES = {'a': '#c46a43', 'b': '#b85e3d', 'c': '#cd7b4e'}
AWN = {'rouge': ('#a8452f', '#f1e6d2'), 'vert': ('#3f6a52', '#efe6d2'), 'bleu': ('#2f5277', '#efe6d2'), 'ocre': ('#c58a2c', '#f3ead6'), 'bordeaux': ('#6e2b33', '#e9dcc8')}


def facade(s, face, plane, u0, u1, spec, bays, rez):
    W = u1 - u0
    bw = W / bays
    centers = [u0 + bw * (i + 0.5) for i in range(bays)]
    rezh, fh, nf = spec['rezh'], spec['fh'], spec['nf']
    shut, sur = spec.get('shut'), spec.get('surround', '#efe5cf')
    w = min(bw * 0.46, 1.05)
    bal = spec.get('bal', {})
    # rez-de-chaussée
    i = 0
    while i < len(rez):
        kind = rez[i]
        c = centers[i]
        if kind == 'vitrine':
            j = i
            while j + 1 < len(rez) and rez[j + 1] == 'vitrine':
                j += 1
            a, b = centers[i] - bw / 2 + 0.35, centers[j] + bw / 2 - 0.35
            s.shop(face, plane, a, b, h=min(rezh - 0.5, 3.1), awn=spec.get('awn', AWN['rouge']) if spec.get('awn') is not False else None)
            i = j + 1
            continue
        if kind == 'porte':
            s.door(face, plane, c, 1.1, min(2.6, rezh - 0.6), colr=spec.get('doorc', '#5b3a2a'))
        elif kind == 'porte_arc':
            s.door(face, plane, c, 1.3, min(3.0, rezh - 0.3), colr=spec.get('doorc', '#5b3a2a'), arch_=True)
        elif kind == 'cochere':
            s.door(face, plane, c, 2.4, min(3.9, rezh - 0.2), colr=spec.get('doorc', '#4a3326'), arch_=True)
        elif kind == 'garage':
            n = s.fn(face)
            s.fpoly(face, plane, rect(c - 1.2, c + 1.2, 0, 2.4), s.col(sur, n))
            s.fpoly(face, plane, rect(c - 1.05, c + 1.05, 0, 2.25), s.col('#8a8e8c', n))
            for k in range(1, 9):
                s.fline(face, plane, (c - 1.05, 2.25 * k / 9), (c + 1.05, 2.25 * k / 9), s.ink(s.col('#8a8e8c', n), .3), w=.3, op=.6)
        elif kind == 'fenetre':
            s.window(face, plane, c, 1.0, w, 1.5, shut=shut, surround=sur)
        i += 1
    # étages
    for f in range(1, nf + 1):
        zf = rezh + (f - 1) * fh
        mode = bal.get(f)
        last = f == nf and spec.get('attique', False)
        for k, c in enumerate(centers):
            if spec.get('skip', {}).get((face, f, k)):
                continue
            if mode == 'filant' or mode == 'all' or (mode == 'center' and k == bays // 2):
                s.window(face, plane, c, zf + 0.08, w, min(2.25, fh - 0.75), shut=shut, surround=sur, bal=(mode != 'filant'), sill=False)
            elif last:
                s.window(face, plane, c, zf + 0.65, w * 0.9, 1.05, shut=None, surround=sur)
            else:
                s.window(face, plane, c, zf + 0.85, w, min(1.6, fh * 0.52), shut=shut, surround=sur)
        if mode == 'filant':
            s.balcony(face, plane, u0 + 0.3, u1 - 0.3, zf + 0.03)


def townhouse(s, spec):
    W, D = spec['W'], spec['D']
    rezh, fh, nf = spec['rezh'], spec['fh'], spec['nf']
    H = rezh + fh * nf
    wall = spec['wall']
    roof = spec.get('roof', 'hip')
    s.shadow(0, 0, W, D, H + 2)
    s.walls(0, 0, W, D, 0, H + (0.8 if roof == 'flat' else 0), wall)
    if spec.get('stone'):
        s.joints('L', D, 0, W, 0, H, step=0.55, op=0.16)
        s.joints('R', W, 0, D, 0, H, step=0.55, op=0.16)
        s.joints('L', D, 0, W, 0, rezh, step=0.45, op=0.3, vert=True)
        s.joints('R', W, 0, D, 0, rezh, step=0.45, op=0.3, vert=True)
    if spec.get('soubassement'):
        c = spec['soubassement']
        s.fpoly('L', D, rect(0, W, 0, 0.7), s.col(c, NL))
        s.fpoly('R', W, rect(0, D, 0, 0.7), s.col(c, NR))
    if spec.get('band', True):
        s.band('L', D, 0, W, rezh - 0.1, colr=spec.get('surround', '#efe5cf'))
        s.band('R', W, 0, D, rezh - 0.1, colr=spec.get('surround', '#efe5cf'))
    facade(s, 'L', D, 0, W, spec, spec['bL'], spec['rezL'])
    if spec['bR']:
        facade(s, 'R', W, 0, D, spec, spec['bR'], spec['rezR'])
    tile = spec.get('tile', TILES['a'])
    if roof in ('hip', 'gable'):
        if spec.get('genoise', True):
            s.genoise('L', D, -0.05, W + 0.05, H)
            if roof == 'hip' or spec.get('axis') == 'y':
                s.genoise('R', W, -0.05, D + 0.05, H)
        else:
            s.band('L', D, 0, W, H - 0.35, h=0.35, colr=spec.get('surround', '#efe5cf'))
            s.band('R', W, 0, D, H - 0.35, h=0.35, colr=spec.get('surround', '#efe5cf'))
        zr = s.roof(0, 0, W, D, H, roof, pitch=spec.get('pitch', 0.32), ov=0.35, tile=tile, wall=wall, axis=spec.get('axis'))
    elif roof == 'mansard':
        s.band('L', D, -0.1, W + 0.1, H - 0.45, h=0.45, colr='#eee6d4')
        s.band('R', W, -0.1, D + 0.1, H - 0.45, h=0.45, colr='#eee6d4')
        s.balcony('L', D, 0.2, W - 0.2, H - 0.45, dp=0.3, rail=0.7)
        bw = W / spec['bL']
        bwr = D / max(1, spec['bR'] or 1)
        s.mansard(0, 0, W, D, H, dormers_L=[bw * (i + 0.5) for i in range(spec['bL'])], dormers_R=[bwr * (i + 0.5) for i in range(spec['bR'] or 0)])
        zr = H + 3.6
    else:
        s.flat_roof(0, 0, W, D, H + 0.8)
        zr = H
    for k in range(spec.get('chim', 1)):
        cx = W * (0.25 + 0.5 * k)
        cy = D * 0.3
        if roof in ('hip', 'gable'):
            s.chimney(cx, cy, H + (D / 2 - D * 0.3) * spec.get('pitch', 0.32) + 0.2, colr=wall)
    return H


# --------------------------------------------------------------- catalogue
def maison_r2(v):
    return dict(W=8, D=9, rezh=3.4, fh=3.0, nf=2, roof='gable', axis='x', bL=3, rezL=['fenetre', 'porte', 'fenetre'],
                bR=2, rezR=['aveugle', 'fenetre'], bal={1: 'center'}, chim=1, **v)


def maison_r3(v):
    return dict(W=7, D=10, rezh=3.5, fh=3.0, nf=3, roof='hip', bL=2, rezL=['porte_arc', 'garage'], bR=3,
                rezR=['aveugle', 'fenetre', 'aveugle'], bal={1: 'all'}, chim=1, **v)


def maison_etroite(v):
    return dict(W=4.6, D=9, rezh=3.3, fh=2.9, nf=3, roof='gable', axis='x', bL=1, rezL=['porte'], bR=3,
                rezR=['aveugle', 'fenetre', 'aveugle'], bal={1: 'center'}, attique=True, chim=1, **v)


def immeuble_commerce(v):
    return dict(W=12, D=11, rezh=3.9, fh=3.1, nf=3, roof='hip', bL=4, rezL=['vitrine', 'vitrine', 'porte', 'vitrine'],
                bR=3, rezR=['vitrine', 'vitrine', 'aveugle'], bal={1: 'filant'}, chim=2, **v)


def immeuble_bourgeois(v):
    return dict(W=16, D=13, rezh=4.3, fh=3.3, nf=4, roof='mansard', bL=5,
                rezL=['vitrine', 'vitrine', 'cochere', 'vitrine', 'vitrine'], bR=4,
                rezR=['vitrine', 'vitrine', 'vitrine', 'aveugle'], bal={1: 'filant', 2: 'center', 4: 'filant'}, stone=True,
                genoise=False, chim=0, **v)


def maison_angle(v):
    return dict(W=10, D=10, rezh=3.6, fh=3.0, nf=2, roof='hip', bL=3, rezL=['vitrine', 'vitrine', 'porte'], bR=3,
                rezR=['porte', 'vitrine', 'vitrine'], bal={1: 'center'}, chim=1, **v)


def maison_faubourg(v):
    return dict(W=7, D=8, rezh=3.2, fh=2.9, nf=1, roof='gable', axis='x', bL=2, rezL=['porte', 'fenetre'], bR=2,
                rezR=['fenetre', 'aveugle'], chim=1, band=False, **v)


def maison_maitre(s, v):
    spec = dict(W=10, D=8, rezh=3.8, fh=3.4, nf=1, roof='hip', bL=3, rezL=['fenetre', 'porte_arc', 'fenetre'], bR=2,
                rezR=['fenetre', 'fenetre'], bal={1: 'center'}, chim=2, pitch=0.3, stone=False, **v)
    # jardin devant (côté +y) : muret, grille, palmier
    gy = 8 + 5
    s.shadow(0, 0, 10, 8, 9)
    s.poly([(-1, 8, 0), (11, 8, 0), (11, gy, 0), (-1, gy, 0)], s.col('#c9b98f', NT), stroke=None, op=0.55)
    s.tree(1.2, 10.6, h=8, r=1.6, kind='palmier')
    s.shadow = lambda *a, **k: None  # déjà faite
    townhouse(s, spec)
    del s.shadow
    s.tree(9.6, 9.5, h=4.5, r=1.6, kind='olivier')
    for x0, x1 in ((-1, 3.8), (6.2, 11)):
        s.box(x0, gy - 0.35, 0, x1, gy, 1.0, v['wall'], topc='#efe5cf')
        k = int((x1 - x0) / 0.25)
        for i in range(k + 1):
            x = x0 + (x1 - x0) * i / k
            s.line((x, gy - 0.15, 1.0), (x, gy - 0.15, 1.9), '#2f2b2d' if not s.night else '#0c0c14', w=0.35)
        s.line((x0, gy - 0.15, 1.9), (x1, gy - 0.15, 1.9), '#2f2b2d' if not s.night else '#0c0c14', w=0.6)
    for x in (3.8, 6.2):
        s.box(x - 0.25, gy - 0.5, 0, x + 0.25, gy, 2.4, '#efe5cf')
    s.box(11 - 0.35, 8, 0, 11, gy, 1.0, v['wall'], topc='#efe5cf')


def residence(s, v):
    W, D, rezh, fh, nf = 24, 12, 4.0, 2.9, 6
    H = rezh + fh * nf
    wall = v['wall']
    s.shadow(0, 0, W, D, H + 1)
    s.walls(0, 0, W, D, 0, H + 1.0, wall)
    # rez : verre et entrée
    s.shop('L', D, 0.6, 9.0, h=3.4, awn=None, frame='#575a5f')
    s.shop('L', D, 15.0, 23.4, h=3.4, awn=None, frame='#575a5f')
    s.door('L', D, 12, 2.0, 2.8, colr='#3c4449', surround='#c9c3b6')
    s.shop('R', W, 0.6, 11.4, h=3.4, awn=None, frame='#575a5f')
    for f in range(nf):
        zf = rezh + f * fh
        # loggias en bandes : face L
        for k in range(6):
            u = 2 + k * 4
            s.window('L', D, u, zf + 0.1, 2.2, 2.2, surround=None, sill=False, mull=True)
        s.fpoly('L', D, rect(0, W, zf - 0.25, zf + 0.05), s.col('#f4f1ea', NT), o=1.1, sw=0.3)
        s.fpoly('L', D, rect(0, W, zf - 0.25, zf + 0.05), s.col('#f4f1ea', NL), o=1.1, sw=0.3)
        s.fpoly('L', D, rect(0, W, zf + 0.05, zf + 1.05), s.col('#bcd0d6', NL), o=1.1, stroke=s.col('#9fb3ba', NL), sw=0.3, op=0.55)
        for k in range(4):
            s.window('R', W, 1.6 + k * 3, zf + 0.85, 1.2, 1.4, shut=v.get('shut'), surround=None)
    s.flat_roof(0, 0, W, D, H + 1.0, para=1.0, floor='#a9a39a')
    s.box(4, 3, H, 8, 6.5, H + 2.6, '#d9d3c7')
    s.box(15, 2.5, H, 17.5, 5, H + 1.6, '#cfc9bd')
    s.box(19, 6, H, 20.4, 7.2, H + 0.9, '#9aa0a4')


def chai(s, v):
    W, D, H = 22, 12, 6.5
    wall = v['wall']
    s.shadow(0, 0, W, D, H + 3)
    s.walls(0, 0, W, D, 0, H, wall)
    s.joints('L', D, 0, W, 0, H, step=0.5, op=0.18, vert=True)
    s.joints('R', W, 0, D, 0, H, step=0.5, op=0.18, vert=True)
    for k in range(4):
        u = 2.75 + k * 5.5
        s.door('L', D, u, 2.6, 4.2, colr=v.get('doorc', '#6b4b33'), arch_=True, surround='#e8dcc0')
    for k in range(5):
        x = k * 5.5
        s.box(x - 0.3, D, 0, x + 0.3, D + 0.45, H - 0.4, wall, topc='#e8dcc0')
    s.door('R', W, D / 2, 3.2, 4.6, colr=v.get('doorc', '#6b4b33'), arch_=True, surround='#e8dcc0')
    s.band('L', D, 0, W, H - 0.35, h=0.35, colr='#e8dcc0')
    s.roof(0, 0, W, D, H, 'gable', pitch=0.38, ov=0.45, tile=v.get('tile', TILES['a']), wall=wall, axis='x')
    n = NR
    zc = H + 2.0
    s.fpoly('R', W, [(D / 2 + 0.9 * __import__('math').cos(t / 10 * 6.283), zc + 0.9 * __import__('math').sin(t / 10 * 6.283)) for t in range(10)], s.col('#e8dcc0', n))
    s.fpoly('R', W, [(D / 2 + 0.6 * __import__('math').cos(t / 10 * 6.283), zc + 0.6 * __import__('math').sin(t / 10 * 6.283)) for t in range(10)], s.col('#3a3a42', n) if not s.night else s.g('lit'))
    # fûts
    for k in range(3):
        x = W + 1.2
        y = 2 + k * 1.3
        s.cyl(x, y, 0.5, 0, 1.0, '#8a5a36', seg=12, topc='#a06c42')


SIMPLE = {
    'maison-ville-r2': (maison_r2, 'Maison de ville R+2, toit à deux pans, génoise'),
    'maison-ville-r3': (maison_r3, 'Maison de ville R+3, toit à quatre pans, balcons'),
    'maison-etroite': (maison_etroite, 'Maison étroite d\'une travée, R+3 avec attique'),
    'immeuble-commerce': (immeuble_commerce, 'Immeuble avec commerces et stores bannes, balcon filant'),
    'immeuble-bourgeois': (immeuble_bourgeois, 'Immeuble bourgeois XIXe en pierre de taille, toit à la Mansart en zinc'),
    'maison-angle': (maison_angle, 'Maison d\'angle avec commerces sur deux rues'),
    'maison-faubourg': (maison_faubourg, 'Petite maison de faubourg R+1'),
}
CUSTOM = {
    'maison-maitre': (maison_maitre, 'Maison de maître avec jardin, grille et palmier'),
    'residence': (residence, 'Résidence des années 60-70, R+6, toit-terrasse'),
    'chai': (chai, 'Chai viticole en pierre, grandes portes cintrées'),
}

VARIANTS = {
    'maison-ville-r2': [dict(wall=WALLS['ocre'], shut=SHUT['bleu']), dict(wall=WALLS['saumon'], shut=SHUT['vert']), dict(wall=WALLS['creme'], shut=SHUT['bordeaux'], tile=TILES['b'])],
    'maison-ville-r3': [dict(wall=WALLS['saumon'], shut=SHUT['vert-sombre']), dict(wall=WALLS['paille'], shut=SHUT['lavande']), dict(wall=WALLS['gris'], shut=SHUT['brun'], tile=TILES['c'])],
    'maison-etroite': [dict(wall=WALLS['creme'], shut=SHUT['turquoise']), dict(wall=WALLS['rose'], shut=SHUT['gris']), dict(wall=WALLS['terre'], shut=SHUT['blanc'])],
    'immeuble-commerce': [dict(wall=WALLS['sable'], shut=SHUT['bleu'], awn=AWN['rouge']), dict(wall=WALLS['ocre'], shut=SHUT['vert'], awn=AWN['vert']), dict(wall=WALLS['rose'], shut=SHUT['gris'], awn=AWN['bleu'])],
    'immeuble-bourgeois': [dict(wall=WALLS['pierre'], shut=SHUT['gris'], awn=AWN['bordeaux']), dict(wall='#e4d6b8', shut=SHUT['blanc'], awn=AWN['vert']), dict(wall='#d6c29c', shut=SHUT['lavande'], awn=AWN['ocre'])],
    'maison-angle': [dict(wall=WALLS['paille'], shut=SHUT['bleu'], awn=AWN['ocre']), dict(wall=WALLS['saumon'], shut=SHUT['vert-sombre'], awn=AWN['rouge']), dict(wall=WALLS['sable'], shut=SHUT['bordeaux'], awn=AWN['vert'])],
    'maison-faubourg': [dict(wall=WALLS['terre'], shut=SHUT['vert']), dict(wall=WALLS['creme'], shut=SHUT['bleu']), dict(wall=WALLS['ocre'], shut=SHUT['brun'], tile=TILES['c'])],
    'maison-maitre': [dict(wall=WALLS['creme'], shut=SHUT['vert-sombre']), dict(wall=WALLS['rose'], shut=SHUT['gris']), dict(wall=WALLS['sable'], shut=SHUT['bleu'])],
    'residence': [dict(wall='#ece6da', shut=SHUT['blanc']), dict(wall='#e6d7bd', shut=SHUT['brun']), dict(wall='#dfe0dc', shut=SHUT['bleu'])],
    'chai': [dict(wall='#dac6a0'), dict(wall='#d2b98e', doorc='#4f6b55'), dict(wall='#e2d2b2', doorc='#7d4a3a')],
}

FOOT = {'maison-ville-r2': (8, 9), 'maison-ville-r3': (7, 10), 'maison-etroite': (4.6, 9), 'immeuble-commerce': (12, 11),
        'immeuble-bourgeois': (16, 13), 'maison-angle': (10, 10), 'maison-faubourg': (7, 8), 'maison-maitre': (12, 13),
        'residence': (24, 12), 'chai': (22, 12)}


def draw(s, name, v):
    if name in SIMPLE:
        townhouse(s, SIMPLE[name][0](dict(v)))
    else:
        CUSTOM[name][0](s, dict(v))
