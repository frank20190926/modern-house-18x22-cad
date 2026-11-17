"""SVG drawing kit + shared building data for Contest #2799843 sheets."""
import math

INK = '#111214'; CH = '#3b3d41'; MID = '#8b8e94'; LT = '#d9dadc'; LT2 = '#eceded'
PAPER = '#fbfbf9'; ACC = '#d4380d'; GLASS = '#cfd9df'; WHITE = '#ffffff'
FONT = "'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SF Mono',Menlo,Consolas,'Courier New',monospace"

PLOT_W, PLOT_D = 18.78, 22.0
HX0, HX1, HY0, HY1 = 1.0, 17.78, 4.2, 18.0


def f(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return s if s not in ('-0', '') else '0'


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def line(x1, y1, x2, y2, c=INK, w=1, dash=None, extra=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="{w}"{d} {extra}/>'


def rect(x, y, w, h, fill='none', stroke=INK, sw=1, extra=''):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{fill}"{st} {extra}/>'


def poly(pts, fill='none', stroke=INK, sw=1, extra=''):
    p = ' '.join(f'{f(a)},{f(b)}' for a, b in pts)
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<polygon points="{p}" fill="{fill}"{st} {extra}/>'


def pline(pts, stroke=INK, sw=1, dash=None):
    p = ' '.join(f'{f(a)},{f(b)}' for a, b in pts)
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def circ(x, y, r, fill='none', stroke=INK, sw=1):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def text(x, y, s, size=9, anchor='middle', weight=400, fill=INK, fam=FONT, rot=None, halo=False, ls=0, extra=''):
    tr = f' transform="rotate({rot} {f(x)} {f(y)})"' if rot is not None else ''
    h = f' style="paint-order:stroke;stroke:{PAPER};stroke-width:2.6px;stroke-linejoin:round"' if halo else ''
    l = f' letter-spacing="{ls}"' if ls else ''
    return (f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
            f'fill="{fill}" font-family="{fam}"{tr}{h}{l} {extra}>{esc(s)}</text>')


def tag(x, y, s, size=6.5, fill=INK, tc=WHITE):
    w = len(s) * size * 0.62 + 5
    return (rect(x - w / 2, y - size * 0.8, w, size * 1.6, fill, None, 0, 'rx="1.5"') +
            text(x, y + size * 0.33, s, size, 'middle', 700, tc, MONO))


def tick(x, y):
    return line(x - 2.6, y + 2.6, x + 2.6, y - 2.6, INK, 1)


def hdim(x1, x2, y, label, ext=None, size=8, c=INK, up=True, bold=False):
    """horizontal dim line in pixel coords; ext = y of the measured feature for extension lines"""
    o = [line(x1, y, x2, y, c, 0.7), tick(x1, y), tick(x2, y)]
    if ext is not None:
        d = 2 if ext > y else -2
        o += [line(x1, y + (-d if True else 0) * 0, x1, ext, c, 0.35, None, 'opacity=".55"'),
              line(x2, y, x2, ext, c, 0.35, None, 'opacity=".55"')]
    ty = y - 2.6 if up else y + size + 1.4
    o.append(text((x1 + x2) / 2, ty, label, size, 'middle', 700 if bold else 500, c, MONO, halo=True))
    return ''.join(o)


def vdim(x, y1, y2, label, ext=None, size=8, c=INK, left=True, bold=False):
    o = [line(x, y1, x, y2, c, 0.7), tick(x, y1), tick(x, y2)]
    if ext is not None:
        o += [line(x, y1, ext, y1, c, 0.35, None, 'opacity=".55"'), line(x, y2, ext, y2, c, 0.35, None, 'opacity=".55"')]
    tx = x - 2.8 if left else x + size + 0.5
    o.append(text(tx, (y1 + y2) / 2, label, size, 'middle', 700 if bold else 500, c, MONO, rot=-90, halo=True))
    return ''.join(o)


class View:
    def __init__(self, ox, oy, s, H=PLOT_D):
        self.ox, self.oy, self.s, self.H = ox, oy, s, H

    def x(self, m): return self.ox + m * self.s
    def y(self, m): return self.oy + (self.H - m) * self.s
    def w(self, m): return m * self.s


def door_swing(v, hx, hy, ux, uy, nx, ny, ln, c=INK, leaf=True):
    """hinge (hx,hy) metres; u = unit along wall to closed end; n = unit normal for open leaf."""
    H = (v.x(hx), v.y(hy))
    C = (v.x(hx + ux * ln), v.y(hy + uy * ln))
    O = (v.x(hx + nx * ln), v.y(hy + ny * ln))
    cross = (C[0] - H[0]) * (O[1] - H[1]) - (C[1] - H[1]) * (O[0] - H[0])
    sw = 1 if cross > 0 else 0
    r = ln * v.s
    out = f'<path d="M{f(C[0])},{f(C[1])} A{f(r)},{f(r)} 0 0 {sw} {f(O[0])},{f(O[1])}" fill="none" stroke="{c}" stroke-width="0.6"/>'
    if leaf:
        out += line(H[0], H[1], O[0], O[1], c, 1.1)
    return out


# ---------------------------------------------------------------- building data
# rooms: (key, x0, y0, x1, y1, name, dimlabel, kind)
L0 = [
    ('garage', 6.14, 0.0, 12.64, 6.5, '2-CAR COVERED GARAGE', '6.50 × 6.50', 'park'),
    ('workshop', 10.1, 6.5, 16.6, 10.7, 'STORAGE & CAR REPAIR WORKSHOP', '6.50 × 4.20', 'serv'),
    ('elec', 10.1, 10.7, 13.5, 13.5, 'ELECTRICAL / IT / CCTV / NVR ROOM', '3.40 × 2.80', 'serv'),
    ('core', 7.2, 6.5, 10.1, 10.7, 'STAIR + LIFT CORE', '2.90 × 4.20', 'core'),
]
L1 = [
    ('living', 1.0, 4.2, 7.2, 9.6, 'LIVING ROOM', '6.20 × 5.40', 'open'),
    ('foyer', 7.2, 4.2, 10.1, 9.6, 'ENTRY FOYER + STAIR/LIFT', '2.90 × 5.40', 'core'),
    ('powder', 10.1, 4.2, 12.3, 6.0, 'GUEST POWDER', '2.20 × 1.80', 'wet'),
    ('store', 10.1, 6.0, 12.98, 8.4, 'STORE', '2.88 × 2.40', 'serv'),
    ('theatre', 12.98, 4.2, 17.78, 8.4, 'ACOUSTIC HOME THEATER', '4.80 × 4.20', 'bed'),
    ('laundry', 1.0, 10.4, 3.8, 12.8, 'LAUNDRY', '2.80 × 2.40', 'wet'),
    ('pantry', 5.4, 10.6, 7.8, 12.8, 'WALK-IN PANTRY', '2.40 × 2.20', 'serv'),
    ('ensuite', 10.38, 9.6, 13.18, 11.6, 'EN-SUITE BATH', '2.80 × 2.00', 'wet'),
    ('guest', 13.18, 9.6, 17.78, 13.8, 'GUEST BEDROOM SUITE 1', '4.60 × 4.20', 'bed'),
    ('dining', 1.0, 12.8, 5.4, 18.0, 'DINING ROOM', '5.20 × 4.40', 'open'),
    ('kitchen', 5.4, 12.8, 9.8, 18.0, 'INDOOR KITCHEN + ISLAND', '5.20 × 4.40', 'open'),
    ('lounge', 9.8, 13.8, 17.78, 18.0, 'FAMILY LOUNGE', '7.98 × 4.20', 'open'),
]
L1_OUT = [
    ('okitchen', 5.4, 19.8, 10.6, 22.0, 'OUTDOOR KITCHEN & BBQ', '5.20 × 2.20', 'out'),
]
L2 = [
    ('m1bed', 1.0, 4.2, 6.8, 9.0, 'MASTER SUITE 1 BEDROOM', '5.80 × 4.80', 'bed'),
    ('m1wc', 1.0, 9.0, 2.4, 10.8, 'WC', '1.40 × 1.80', 'wet'),
    ('m1sh', 2.4, 9.0, 4.0, 10.8, 'SHOWER', '1.60 × 1.80', 'wet'),
    ('m1van', 4.0, 9.0, 6.8, 10.8, 'DUAL VANITY', '2.80 × 1.80', 'wet'),
    ('m1wic', 1.0, 10.8, 4.4, 13.4, 'WALK-IN CLOSET', '3.40 × 2.60', 'serv'),
    ('m2bed', 11.98, 4.2, 17.78, 9.0, 'MASTER SUITE 2 BEDROOM', '5.80 × 4.80', 'bed'),
    ('m2wc', 16.38, 9.0, 17.78, 10.8, 'WC', '1.40 × 1.80', 'wet'),
    ('m2sh', 14.78, 9.0, 16.38, 10.8, 'SHOWER', '1.60 × 1.80', 'wet'),
    ('m2van', 11.98, 9.0, 14.78, 10.8, 'DUAL VANITY', '2.80 × 1.80', 'wet'),
    ('m2wic', 14.38, 10.8, 17.78, 13.4, 'WALK-IN CLOSET', '3.40 × 2.60', 'serv'),
    ('ulounge', 6.8, 4.2, 11.98, 8.2, 'UPPER LOUNGE', '5.18 × 4.00', 'open'),
    ('core2', 7.2, 8.2, 10.1, 10.8, 'STAIR + LIFT', '2.90 × 2.60', 'core'),
    ('study', 6.8, 10.8, 11.98, 15.0, 'STUDY GALLERY', '5.18 × 4.20', 'open'),
]
BALCONY = (1.0, 2.2, 17.78, 4.2)

FILL = {'open': '#ffffff', 'bed': '#ffffff', 'wet': '#e3e4e6', 'serv': '#d3d4d7', 'core': '#c8c9cd',
        'park': '#f1f1f1', 'out': '#f1f1f1'}


def area(r):
    return (r[3] - r[1]) * (r[4] - r[2])
