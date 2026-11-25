import json, sys
B = sys.argv[1]; m = json.load(open(f'{B}/manifest.json'))
def page(mode):
    bg, fg, card = ('#f3efe6', '#2b2440', '#fbf8f2') if mode == 'jour' else ('#141831', '#e8e4f5', '#1c2142')
    h = [f'<html><head><meta charset="utf-8"><style>body{{margin:0;background:{bg};color:{fg};font:15px/1.3 system-ui,sans-serif;padding:28px}}h1{{font-size:30px;margin:0 0 4px}}h2{{font-size:20px;margin:28px 0 12px}}.g{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}}.r{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.c{{background:{card};border-radius:10px;padding:10px;display:flex;flex-direction:column;align-items:center}}.c img{{width:100%;height:230px;object-fit:contain}}.r .c img{{height:400px}}.c b{{margin-top:6px;font-size:14px}}.c span{{opacity:.65;font-size:12px;text-align:center}}</style></head><body>',
         f'<h1>Béziers en relief : assets de bâtiments ({mode})</h1><div style="opacity:.7">Isométrie 2:1, 10 px par mètre, lumière à gauche. Brouillon pour la bible DA.</div>',
         '<h2>Repères sur mesure</h2><div class="r">']
    for r in m['reperes']:
        h.append(f'<div class="c"><img src="{r["fichiers"][mode]}"><b>{r["id"]}</b><span>{r["description"]}</span></div>')
    h.append('</div><h2>Bâtiments génériques (variante a)</h2><div class="g">')
    for g in m['generiques']:
        if g['variante'] == 'a':
            h.append(f'<div class="c"><img src="{g["fichiers"][mode]}"><b>{g["id"]}</b><span>{g["description"]}</span></div>')
    h.append('</div><h2>Végétation et mobilier</h2><div class="g" style="grid-template-columns:repeat(6,1fr)">')
    for v in m['vegetation']:
        h.append(f'<div class="c"><img src="{v["fichiers"][mode]}" style="height:140px"><b>{v["id"]}</b></div>')
    h.append('</div></body></html>')
    open(f'{B}/planche-{mode}.html', 'w').write(''.join(h))
def variantes():
    h = ['<html><head><meta charset="utf-8"><style>body{margin:0;background:#f3efe6;color:#2b2440;font:15px system-ui;padding:28px}.g{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.c{background:#fbf8f2;border-radius:10px;padding:8px;text-align:center}.c img{width:100%;height:200px;object-fit:contain}</style></head><body><h1>Les trois teintes de chaque bâtiment générique</h1><div class="g">']
    for g in m['generiques']:
        h.append(f'<div class="c"><img src="{g["fichiers"]["jour"]}"><div>{g["id"]} · {g["variante"]}</div></div>')
    h.append('</div></body></html>')
    open(f'{B}/planche-variantes.html', 'w').write(''.join(h))
page('jour'); page('nuit'); variantes()
def vie(mode):
    bg, fg, card = ('#f3efe6', '#2b2440', '#fbf8f2') if mode == 'jour' else ('#141831', '#e8e4f5', '#1c2142')
    css = f'body{{margin:0;background:{bg};color:{fg};font:15px/1.3 system-ui,sans-serif;padding:28px}}h1{{font-size:30px;margin:0 0 4px}}h2{{font-size:20px;margin:26px 0 12px}}.g{{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}}.c{{background:{card};border-radius:10px;padding:10px;display:flex;flex-direction:column;align-items:center}}.c img{{width:100%;height:150px;object-fit:contain}}.p img{{height:120px}}.c b{{margin-top:6px;font-size:13px}}.c i{{display:inline-block;width:12px;height:12px;border-radius:6px;margin-right:4px;vertical-align:-1px}}'
    h = [f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>',
         f'<h1>La vie de la carte : gens, mobilier, incongrus ({mode})</h1><div style="opacity:.7">Même isométrie que les bâtiments. Les vêtements des personnages se recolorent en CSS (couleur de l\'émotion).</div>',
         '<h2>Personnages : allures et émotions</h2><div class="g p">']
    for p in m['personnages']:
        col = m['couleurs_emotions'].get(p['id'])
        dot = f'<i style="background:{col}"></i>' if col else ''
        h.append(f'<div class="c"><img src="{p["fichiers"][mode]}"><b>{dot}{p["id"]}</b></div>')
    h.append('</div><h2>Mobilier, végétation de saison</h2><div class="g">')
    for v in m['mobilier']:
        h.append(f'<div class="c"><img src="{v["fichiers"][mode]}"><b>{v["id"]}</b></div>')
    h.append('</div><h2>Éléments incongrus (absurdité)</h2><div class="g">')
    for v in m['incongrus']:
        h.append(f'<div class="c"><img src="{v["fichiers"][mode]}"><b>{v["id"]}</b></div>')
    h.append('</div></body></html>')
    open(f'{B}/planche-vie-{mode}.html', 'w').write(''.join(h))
vie('jour'); vie('nuit')
for sc in ('joie', 'tristesse', 'colere'):
    open(f'{B}/scene-{sc}.html', 'w').write(f'<html><body style="margin:0;background:#e9e3d6"><img src="apercu/scene-{sc}.svg" style="width:100%;display:block"></body></html>')
