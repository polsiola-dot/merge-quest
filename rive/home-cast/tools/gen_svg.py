# Builds the home-screen cast (4 buddies) as an SVG whose groups are named and
# pivot-ready, for `rive svg` to convert into editable Rive shapes.
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
font = TTFont(os.path.join(HERE, '../../../fonts/lilita-one.woff2')); gs = font.getGlyphSet(); cmap = font.getBestCmap()
def glyph(ch):
    g = cmap[ord(ch)]; p = SVGPathPen(gs); gs[g].draw(p); return p.getCommands(), gs[g].width

def mix(a, b, t):
    return '#' + ''.join('%02x' % round(int(a[i:i+2], 16) * (1 - t) + int(b[i:i+2], 16) * t) for i in (1, 3, 5))

W, H = 400, 300
BUDDIES = [  # name, value, top, base, side, kind, left%, bottom%, width%, rot
    ('two', 2, '#6fc3ff', '#2f86e6', '#1c5fb8', 'curious', 4, 26, 24, -8),
    ('purple', 0, '#c48bff', '#8b45f0', '#5e22b8', 'cheer', 39, 24, 28, 0),
    ('four', 4, '#8af06a', '#3fbf2c', '#25861b', 'sleepy', 22, 4, 22, -4),
    ('eight', 8, '#ffb35c', '#ff8a1a', '#c45a00', 'determined', None, 10, 24, 7),
]
INK = '#5a0f22'
meta = {}

def pivot(name, px, py, inner):
    """group whose origin is (px,py) so rotation/scale pivot there"""
    return f'<g id="{name}" transform="translate({px} {py})"><g transform="translate({-px} {-py})">{inner}</g></g>'

def buddy(n, v, top, base, side, kind):
    eyes = [(21, 56), (79, 56)] if v else [(32, 44), (68, 44)]
    r = 10 if v else 12
    lidc = mix(top, base, (eyes[0][1] + 4) / 100)
    out = []
    gid = f'{n}_grad'
    out.append(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{base}"/></linearGradient></defs>')
    if kind == 'determined':
        out.append(pivot(f'{n}_aura', 50, 56, f'<circle cx="50" cy="56" r="66" fill="{top}" opacity="0.45"/>'))
    if kind == 'cheer':
        out.append(pivot(f'{n}_armL', 9, 47, pivot(f'{n}_armLs', 9, 47, f'<path d="M6 46 Q-12 30 -6 8" stroke="{base}" stroke-width="13" stroke-linecap="round" fill="none"/><circle cx="-6" cy="6" r="9" fill="{top}"/>')))
        out.append(pivot(f'{n}_armR', 91, 47, pivot(f'{n}_armRs', 91, 47, f'<path d="M94 46 Q112 30 106 8" stroke="{base}" stroke-width="13" stroke-linecap="round" fill="none"/><circle cx="106" cy="6" r="9" fill="{top}"/>')))
    out.append(f'<rect x="0" y="12" width="100" height="100" rx="22" fill="{side}"/>')
    out.append(f'<rect id="{n}_body" x="0" y="0" width="100" height="100" rx="22" fill="url(#{gid})"/>')
    out.append('<rect x="10" y="7" width="80" height="26" rx="13" fill="#ffffff" opacity="0.28"/>')
    if v:
        d, w = glyph(str(v)); s = 0.04; x0 = 50 - w * s / 2
        t = f'translate({x0:.2f} 47) scale({s} {-s})'
        out.append(f'<g transform="{t}"><path d="{d}" fill="{side}" stroke="{side}" stroke-width="175" stroke-linejoin="round"/><path d="{d}" fill="#ffffff"/></g>')
    for i, (x, y) in enumerate(eyes):
        inner_dir = -1 if i else 1
        T = y - 3 * r
        if kind == 'sleepy':
            shape = f'M{x-r-2} {T}H{x+r+2}V{y-r*.2}H{x-r-2}Z'; line = f'M{x-r-2} {y-r*.2}H{x+r+2}'
        elif kind == 'determined':
            yi, yo = y - r * .3, y - r * .95; xi, xo = x + inner_dir * (r + 2), x - inner_dir * (r + 2)
            shape = f'M{xo} {T}H{xi}V{yi}L{xo} {yo}Z'; line = f'M{xo} {yo}L{xi} {yi}'
        else:
            shape = f'M{x-r-2} {T}H{x+r+2}V{y-r-1}H{x-r-2}Z'; line = f'M{x-r-2} {y-r-1}H{x+r+2}'
        side_n = 'L' if i == 0 else 'R'
        out.append(f'<clipPath id="{n}_clip{i}"><circle cx="{x}" cy="{y}" r="{r+1}"/></clipPath>')
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff"/>')
        out.append(f'<g id="{n}_pup{side_n}"><g id="{n}_pup{side_n}s"><circle cx="{x+2}" cy="{y+2}" r="{6.5 if v else 8}" fill="#1d1340"/><circle cx="{x-1}" cy="{y-2}" r="2.6" fill="#ffffff"/></g></g>')
        out.append(f'<g clip-path="url(#{n}_clip{i})"><g id="{n}_lid{side_n}"><g id="{n}_lid{side_n}s"><path d="{shape}" fill="{lidc}"/><path d="{line}" stroke="{side}" stroke-width="3" stroke-linecap="round" fill="none"/></g></g></g>')
    by = 74 if v else 62
    for x in (16, 84):
        out.append(f'<ellipse cx="{x}" cy="{by}" rx="8" ry="5" fill="#ff6f9a" opacity="{0.8 if kind == "cheer" else 0.55}"/>')
    my = 72 if v else 64
    if kind == 'curious':
        out.append(f'<ellipse cx="50" cy="{my+4}" rx="5.5" ry="7" fill="#7a1530" stroke="{INK}" stroke-width="2"/><ellipse cx="50" cy="{my+8}" rx="3.5" ry="2.5" fill="#ff7a8a"/>')
    elif kind == 'sleepy':
        out.append(f'<g id="{n}_smile"><path d="M40 {my} Q50 {my+9} 60 {my}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round" fill="none"/></g>')
        out.append(pivot(f'{n}_yawn', 50, my + 5, f'<ellipse cx="50" cy="{my+5}" rx="9" ry="11" fill="#7a1530" stroke="{INK}" stroke-width="2"/><ellipse cx="50" cy="{my+11}" rx="6" ry="4" fill="#ff7a8a"/>'))
        d, w = glyph('z'); s = 0.04
        out.append(pivot(f'{n}_zz', 96, 0, f'<g transform="translate({96 - w*s/2:.2f} 6) scale({s} {-s})"><path d="{d}" fill="{side}" stroke="{side}" stroke-width="160" stroke-linejoin="round"/><path d="{d}" fill="#ffffff"/></g>'))
    elif kind == 'cheer':
        out.append(f'<path d="M34 {my-2} Q50 {my+24} 66 {my-2} Z" fill="#7a1530" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/><path d="M41 {my+8} Q50 {my+17} 59 {my+8}" fill="#ff7a8a"/>')
        for k, (sx, sy, ss) in enumerate([(-14, -14, 7), (112, -12, 6), (50, -18, 8)]):
            d = f'M{sx} {sy-ss}L{sx+ss*.3} {sy-ss*.3}L{sx+ss} {sy}L{sx+ss*.3} {sy+ss*.3}L{sx} {sy+ss}L{sx-ss*.3} {sy+ss*.3}L{sx-ss} {sy}L{sx-ss*.3} {sy-ss*.3}Z'
            out.append(pivot(f'{n}_spark{k}', sx, sy, f'<path d="{d}" fill="#fff6b0"/>'))
    else:
        out.append(f'<path d="M40 {my+4} Q53 {my+10} 61 {my-1}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round" fill="none"/>')
    return ''.join(out)

parts = []
# sky, sun glow and two hills, loosely like the home scene
parts.append(f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6cc6ff"/><stop offset="1" stop-color="#bfe8ff"/></linearGradient>'
             f'<radialGradient id="sun" cx="200" cy="130" r="170" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff6c4"/><stop offset="1" stop-color="#fff6c4" stop-opacity="0"/></radialGradient></defs>')
parts.append(f'<rect id="bg" x="0" y="0" width="{W}" height="{H}" fill="url(#sky)"/>')
parts.append(f'<circle cx="200" cy="130" r="170" fill="url(#sun)"/>')
parts.append(f'<ellipse cx="80" cy="330" rx="200" ry="90" fill="#5fcf4a"/><ellipse cx="340" cy="340" rx="200" ry="100" fill="#4dbb3a"/>')
for n, v, top, base, side, kind, lp, bp, wp, rot in BUDDIES:
    w = W * wp / 100; h = w * 150 / 140; s = w / 140
    left = W * lp / 100 if lp is not None else W - W * 4 / 100 - w
    bottom = H - H * bp / 100
    cx, cy = left + w / 2, bottom - h / 2
    # body space: viewBox (-20,-24) → body bottom-centre at (50,112)
    bx = left + (50 + 20) * s - cx; byy = bottom - h + (112 + 24) * s - cy
    inner = buddy(n, v, top, base, side, kind)
    parts.append(f'<g id="{n}" transform="translate({cx:.2f} {cy:.2f}) rotate({rot})">'
                 f'<g id="{n}_bob" transform="translate({bx:.2f} {byy:.2f}) scale({s:.4f})"><g id="{n}_act">'
                 f'<g transform="translate(-50 -112)">{inner}</g></g></g></g>')
Z = 2   # drawn at 2x so the artboard is 800x600
open(os.path.join(HERE, 'cast.svg'), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W*Z} {H*Z}" width="{W*Z}" height="{H*Z}"><g id="scene" transform="scale({Z})">' + ''.join(parts) + '</g></svg>')
print('ok')
