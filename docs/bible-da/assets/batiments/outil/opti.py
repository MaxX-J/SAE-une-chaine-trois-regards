"""Allège un SVG produit par iso.py, sans changer son rendu.

- fusionne les traits consécutifs de même style en un seul <path> ;
- fusionne les polygones consécutifs de même remplissage (sans contour ni opacité) ;
- raccourcit nombres et couleurs, met les styles communs sur la racine ;
- retire les dégradés inutilisés.
"""
import re

NUM = re.compile(r'(?<![\w#.])(-?)0\.(\d)')
LINE = re.compile(r'<line x1="([^"]+)" y1="([^"]+)" x2="([^"]+)" y2="([^"]+)"([^>]*)/>')
POLY = re.compile(r'<polygon points="([^"]+)"([^>]*)/>')
PLINE = re.compile(r'<polyline points="([^"]+)"([^>]*)/>')


def _num(s):
    s = re.sub(r'(\d+)\.0(?!\d)', r'\1', s)
    return NUM.sub(r'\1.\2', s)


def _pts(p):
    out = []
    for xy in p.split(' '):
        x, y = xy.split(',')
        out.append(f'{x} {y}' if not y.startswith('-') else f'{x}{y}')
    return ' '.join(out)


def _hex(m):
    c = m.group(1).lower()
    if c[0] == c[1] and c[2] == c[3] and c[4] == c[5]:
        return '#' + c[0] + c[2] + c[4]
    return '#' + c


def optimise(svg):
    head, body = svg.split('</defs>', 1)
    body = body.replace(' stroke-linejoin="round"', '').replace(' stroke-linecap="round"', '')
    tokens = re.findall(r'<[^>]+/>|<[^>]+>[^<]*</[^>]+>|<[^>]+>|[^<]+', body)
    out = []
    pend_key, pend_d = None, []

    def flush():
        nonlocal pend_key, pend_d
        if pend_key is None:
            return
        kind, rest = pend_key
        if kind == 'l':
            out.append(f'<path d="{"".join(pend_d)}" fill="none"{rest}/>')
        else:
            out.append(f'<path d="{"".join(pend_d)}"{rest}/>')
        pend_key, pend_d = None, []

    for t in tokens:
        m = LINE.fullmatch(t)
        if m:
            key = ('l', m.group(5))
            if key != pend_key:
                flush()
                pend_key = key
            pend_d.append(f'M{m.group(1)} {m.group(2)}L{m.group(3)} {m.group(4)}')
            continue
        m = POLY.fullmatch(t)
        if m and 'stroke=' not in m.group(2) and 'opacity' not in m.group(2):
            key = ('p', m.group(2))
            if key != pend_key:
                flush()
                pend_key = key
            pend_d.append(f'M{_pts(m.group(1))}Z')
            continue
        flush()
        m = POLY.fullmatch(t)
        if m:
            t = f'<path d="M{_pts(m.group(1))}Z"{m.group(2)}/>'
        m = PLINE.fullmatch(t)
        if m:
            t = f'<path d="M{_pts(m.group(1))}"{m.group(2)}/>'
        out.append(t)
    flush()
    body = ''.join(out)
    # dégradés inutilisés
    used = set(re.findall(r'url\(#([^)]+)\)', body))
    used |= set(re.findall(r'url\(#([^)]+)\)', head.split('<defs>', 1)[1]))

    def keep(m):
        return m.group(0) if m.group(1) in used else ''
    head = re.sub(r'<(?:linear|radial)Gradient id="([^"]+)".*?</(?:linear|radial)Gradient>', keep, head)
    head = re.sub(r'<clipPath id="([^"]+)">.*?</clipPath>', keep, head)
    head = head.replace('<svg ', '<svg stroke-linejoin="round" stroke-linecap="round" ', 1)
    head = head.replace('<defs></defs>', '')
    s = head + ('</defs>' if '<defs>' in head else '') + body
    s = re.sub(r'#([0-9a-fA-F]{6})(?![0-9a-fA-F])', _hex, s)
    # nombres (hors métadonnées et identifiants)
    parts = re.split(r'(<metadata>.*?</metadata>|<title>.*?</title>|id="[^"]*"|url\(#[^)]*\))', s)
    s = ''.join(p if i % 2 else _num(p) for i, p in enumerate(parts))
    s = s.replace(' stroke-linecap="butt"', ' stroke-linecap="butt"')
    return s
