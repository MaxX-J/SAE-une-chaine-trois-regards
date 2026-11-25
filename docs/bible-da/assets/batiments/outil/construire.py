"""Construit tous les assets SVG, le manifeste et les aperçus.
Usage : python3 construire.py <dossier_sortie>
"""
import json, os, sys
from iso import S, U, ZK
import generiques as G
import reperes as R
import vie as V
import scenes as SC

OUT = sys.argv[1]
MODES = (('jour', False), ('nuit', True))
manifest = {
    'version': 1,
    'projection': {'type': 'isometrique 2:1', 'px_par_metre': U, 'echelle_verticale': ZK,
                   'ancre': "Le point (0,0) du viewBox est le centre de l'emprise au sol.",
                   'axes': "x vers la droite et le bas de l'écran, y vers la gauche et le bas, z vers le haut",
                   'lumiere': 'de la gauche : face gauche éclairée, face droite à l\'ombre'},
    'generiques': [], 'reperes': [], 'vegetation': [], 'personnages': [], 'mobilier': [], 'incongrus': [],
    'variables_css_personnages': {'--haut': 'haut (couleur de l\'émotion)', '--bas': 'pantalon', '--peau': 'peau', '--cheveux': 'cheveux', '--objet': 'parapluie'},
    'couleurs_emotions': V.EMOTIONS, 'peaux': V.PEAUX, 'cheveux': V.CHEVEUX}


def emit(folder, aid, night, fn, bounds, title, meta):
    s = S(aid, night)
    s.cx, s.cy = (bounds[0] + bounds[2]) / 2, (bounds[1] + bounds[3]) / 2
    fn(s)
    os.makedirs(f'{OUT}/{folder}', exist_ok=True)
    open(f'{OUT}/{folder}/{aid}.svg', 'w').write(s.svg(title, meta=meta))
    return f'{folder}/{aid}.svg'


for name, (W, D) in G.FOOT.items():
    desc = (G.SIMPLE.get(name) or G.CUSTOM.get(name))[1]
    b = (-1, 0, 11, 13) if name == 'maison-maitre' else (0, 0, W, D)
    for i, v in enumerate(G.VARIANTS[name]):
        var = 'abc'[i]
        files = {}
        for mode, night in MODES:
            aid = f'{name}-{var}-{mode}'
            files[mode] = emit('generiques', aid, night, lambda s, n=name, v=v: G.draw(s, n, v), b, f'{desc} ({var}, {mode})',
                               {'id': name, 'variante': var, 'mode': mode, 'emprise_m': [b[2] - b[0], b[3] - b[1]]})
        manifest['generiques'].append({'id': name, 'variante': var, 'description': desc,
                                       'emprise_m': [b[2] - b[0], b[3] - b[1]], 'couleurs': v, 'fichiers': files})

for name, (fn, desc) in R.LANDMARKS.items():
    b = fn(S('tmp'))
    files = {}
    for mode, night in MODES:
        files[mode] = emit('reperes', f'{name}-{mode}', night, fn, b, f'{desc} ({mode})',
                           {'id': name, 'mode': mode, 'emprise_m': [b[2] - b[0], b[3] - b[1]]})
    manifest['reperes'].append({'id': name, 'description': desc, 'emprise_m': [round(b[2] - b[0], 1), round(b[3] - b[1], 1)], 'fichiers': files})

VEG = {'platane': lambda s: s.tree(0, 0, h=10, r=3.0, kind='platane'),
       'cypres': lambda s: s.tree(0, 0, h=11, r=1.3, kind='cypres'),
       'palmier': lambda s: s.tree(0, 0, h=9, r=1.7, kind='palmier'),
       'olivier': lambda s: s.tree(0, 0, h=5, r=1.8, kind='olivier'),
       'pin-parasol': lambda s: s.tree(0, 0, h=11, r=3.4, kind='pin'),
       'lampadaire': lambda s: s.lamppost(0, 0)}
for name, fn in VEG.items():
    files = {mode: emit('vegetation', f'{name}-{mode}', night, fn, (0, 0, 0, 0), f'{name} ({mode})', {'id': name, 'mode': mode})
             for mode, night in MODES}
    manifest['vegetation'].append({'id': name, 'fichiers': files})

os.makedirs(f'{OUT}/vie/personnages', exist_ok=True)
for name in V.POSTURES_ALLURE + [p for p in V.POSTURES_EMOTION if p != 'neutre']:
    pose = V.POSTURES_EMOTION.get(name, name)
    haut = V.EMOTIONS.get(name, V.EMOTIONS['neutre'] if name != 'parapluie' else '#4f6b55')
    files = {}
    for mode, night in MODES:
        f = f'vie/personnages/personne-{name}-{mode}.svg'
        open(f'{OUT}/{f}', 'w').write(V.person_svg(pose, night, haut))
        files[mode] = f
    manifest['personnages'].append({'id': name, 'type': 'emotion' if name in V.EMOTIONS else 'allure', 'fichiers': files})
for key, d in (('mobilier', V.MOBILIER), ('incongrus', V.INCONGRUS)):
    for name, fn in d.items():
        files = {mode: emit(f'vie/{key}', f'{name}-{mode}', night, fn, (0, 0, 0, 0), f'{name} ({mode})', {'id': name, 'mode': mode})
                 for mode, night in MODES}
        manifest[key].append({'id': name, 'fichiers': files})

json.dump(manifest, open(f'{OUT}/manifest.json', 'w'), ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- scène de démo
def scene(night):
    s = S(f'demo-{"nuit" if night else "jour"}', night)
    objs = []
    # rangée arrière
    x = 0
    back = [('maison-ville-r2', 0), ('maison-etroite', 1), ('immeuble-commerce', 0), ('maison-ville-r3', 2), ('maison-etroite', 0), ('maison-ville-r2', 1), ('maison-angle', 0)]
    for n, vi in back:
        W, D = G.FOOT[n]
        objs.append((x, 13 - D, n, vi, W, D))
        x += W
    # rangée avant
    x = 0
    front = [('immeuble-bourgeois', 0), ('maison-ville-r3', 0), ('maison-etroite', 2), ('immeuble-commerce', 1), ('maison-ville-r2', 2), ('maison-faubourg', 0)]
    for n, vi in front:
        W, D = G.FOOT[n]
        objs.append((x, 26, n, vi, W, D))
        x += W
    s.at(0, 0)
    ground = '#e7dfcd'
    s.poly([(-4, -2, 0), (66, -2, 0), (66, 42, 0), (-4, 42, 0)], s.col(ground), stroke=None)
    s.poly([(-4, 13, 0), (66, 13, 0), (66, 26, 0), (-4, 26, 0)], s.col('#cfc6b5'), stroke=None)
    for xx in range(-2, 66, 3):
        s.line((xx, 19.5, 0.01), (xx + 1.4, 19.5, 0.01), s.col('#f4f0e6'), w=0.8)
    items = [(ox + oy, 'b', (ox, oy, n, vi)) for ox, oy, n, vi, W, D in objs]
    for tx in (6, 20, 34, 48, 62):
        items.append((tx + 14.8 - 3, 't', (tx, 14.8)))
        items.append((tx + 3 + 24.3 - 6, 'l', (tx + 3, 24.3)))
    for _, k, d in sorted(items, key=lambda t: t[0]):
        if k == 'b':
            ox, oy, n, vi = d
            s.at(ox, oy)
            G.draw(s, n, G.VARIANTS[n][vi])
        elif k == 't':
            s.at(0, 0); s.tree(d[0], d[1], h=8.5, r=2.4, kind='platane')
        else:
            s.at(0, 0); s.lamppost(*d)
    return s.svg('Scène de démonstration : une rue de Béziers')


os.makedirs(f'{OUT}/apercu', exist_ok=True)
DEMOS = {'scene-joie': dict(night=False, emotion='joie', energie=0.8, tension=0.0, saison='printemps', seed=3),
         'scene-tristesse': dict(night=True, emotion='tristesse', energie=0.25, tension=0.3, saison='automne', pluie=True, seed=4),
         'scene-colere': dict(night=True, emotion='colere', energie=0.7, tension=1.0, saison='hiver', incongru='taureau', seed=5)}
for k, kw in DEMOS.items():
    open(f'{OUT}/apercu/{k}.svg', 'w').write(SC.rue(k, **kw))
for night in (False, True):
    open(f'{OUT}/apercu/scene-{"nuit" if night else "jour"}.svg', 'w').write(scene(night))
print('ok', sum(len(f) for _, _, f in os.walk(OUT)))
