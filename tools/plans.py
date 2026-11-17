from kit import *

SC = 23.5
OY = 196
OXS = [72, 592, 1112]
STAIR = dict(ax0=1.0, ax1=4.9, ay0=0.3, ay1=1.5, by0=1.7, by1=2.9, land=(4.9, 0.3, 6.1, 2.9))

HATCH_DEFS = f'''<defs>
<pattern id="soil" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0,7 L7,0" stroke="{MID}" stroke-width=".5"/><circle cx="2" cy="2" r=".6" fill="{MID}"/></pattern>
<pattern id="grass" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r=".55" fill="#9a9da2"/><circle cx="4.5" cy="4.5" r=".55" fill="#9a9da2"/></pattern>
<pattern id="roof" width="9" height="9" patternUnits="userSpaceOnUse"><path d="M0,9 L9,0" stroke="#b9bbbf" stroke-width=".4"/></pattern>
</defs>'''


def wall_gap(v, x, y, ln, orient, th=0.34):
    if orient == 'h':
        return rect(v.x(x), v.y(y) - th * v.s / 2, ln * v.s, th * v.s, WHITE, None, 0)
    return rect(v.x(x) - th * v.s / 2, v.y(y + ln), th * v.s, ln * v.s, WHITE, None, 0)


def win(v, x, y, ln, orient, label=None, lside=1):
    o = wall_gap(v, x, y, ln, orient, 0.3)
    if orient == 'h':
        for d in (-0.1, 0, 0.1):
            o += line(v.x(x), v.y(y) + d * v.s, v.x(x + ln), v.y(y) + d * v.s, INK, 0.6)
        if label: o += tag(v.x(x + ln / 2), v.y(y) + lside * 9, label)
    else:
        for d in (-0.1, 0, 0.1):
            o += line(v.x(x) + d * v.s, v.y(y), v.x(x) + d * v.s, v.y(y + ln), INK, 0.6)
        if label: o += tag(v.x(x) + lside * 11, v.y(y + ln / 2), label)
    return o


def door(v, x, y, ln, orient, hinge_first=True, normal=1, label=None, sliding=False):
    o = wall_gap(v, x, y, ln, orient)
    if sliding:
        if orient == 'h':
            o += line(v.x(x), v.y(y) - 1.5, v.x(x + ln * .6), v.y(y) - 1.5, INK, 1.2) + line(v.x(x + ln * .4), v.y(y) + 1.5, v.x(x + ln), v.y(y) + 1.5, INK, 1.2)
        else:
            o += line(v.x(x) - 1.5, v.y(y), v.x(x) - 1.5, v.y(y + ln * .6), INK, 1.2) + line(v.x(x) + 1.5, v.y(y + ln * .4), v.x(x) + 1.5, v.y(y + ln), INK, 1.2)
    else:
        if orient == 'h':
            hx = x if hinge_first else x + ln
            u = 1 if hinge_first else -1
            o += door_swing(v, hx, y, u, 0, 0, normal, ln)
        else:
            hy = y if hinge_first else y + ln
            u = 1 if hinge_first else -1
            o += door_swing(v, x, hy, 0, u, normal, 0, ln)
    if label:
        if orient == 'h': o += tag(v.x(x + ln / 2), v.y(y) - normal * (ln * v.s * .55 + 6), label)
        else: o += tag(v.x(x) + normal * (ln * v.s * .55 + 8), v.y(y + ln / 2), label)
    return o


def room_label(v, r, size=None):
    key, x0, y0, x1, y1, name, dim, kind = r
    w, h = (x1 - x0) * v.s, (y1 - y0) * v.s
    cx, cy = v.x((x0 + x1) / 2), v.y((y0 + y1) / 2)
    small = w < 70 or h < 50
    fs = size or (5.6 if small else 7)
    # wrap name
    words = name.split(' ')
    lines, cur = [], ''
    maxc = max(5, int(w / (fs * 0.62)))
    for wd in words:
        if len(cur) + len(wd) + 1 <= maxc or not cur:
            cur = (cur + ' ' + wd).strip()
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    lines = lines[:3]
    n = len(lines) + 1
    y = cy - (n - 1) * fs * 0.55
    o = ''
    for ln in lines:
        o += text(cx, y, ln, fs, 'middle', 700, INK, FONT, ls=0.2); y += fs * 1.15
    o += text(cx, y + 0.5, dim, fs - 0.4, 'middle', 600, ACC, MONO)
    return o


def furniture(v, key):
    o = ''
    P = lambda m: v.x(m)
    Q = lambda m: v.y(m)
    s = v.s
    def rr(x0, y0, x1, y1, fill=WHITE, st=MID, rx=1.5):
        return rect(P(x0), Q(y1), (x1 - x0) * s, (y1 - y0) * s, fill, st, 0.6, f'rx="{rx}"')
    if key == 'garage':
        for cx in (7.9, 10.9):
            o += rr(cx - 0.9, 0.9, cx + 0.9, 5.2, '#e9eaec', MID, 5)
            o += rr(cx - 0.75, 1.9, cx + 0.75, 3.6, '#d4d6d9', MID, 3)
        o += line(P(6.14), Q(0.0), P(12.64), Q(0.0), INK, 1)
    elif key == 'workshop':
        o += rr(11.0, 7.0, 13.0, 8.7, '#e9eaec', MID, 3) + rr(13.6, 7.0, 16.3, 7.5, '#d4d6d9', MID, 0) + rr(13.6, 10.0, 16.3, 10.5, '#d4d6d9', MID, 0)
    elif key == 'elec':
        for i in range(4):
            o += rr(10.3 + i * 0.7, 12.7, 10.9 + i * 0.7, 13.4, '#bfc1c5', INK, 0)
        o += rr(12.5, 10.9, 13.4, 11.5, WHITE, INK, 0) + text(P(12.95), Q(11.1), 'NVR', 5, 'middle', 700, INK, MONO)
    elif key == 'living':
        o += rr(1.6, 5.6, 4.6, 6.7, '#e9eaec', MID, 3) + rr(1.6, 6.9, 2.6, 8.4, '#e9eaec', MID, 3) + rr(3.0, 7.2, 4.6, 8.0, WHITE, MID, 0)
    elif key == 'dining':
        o += rr(2.0, 14.4, 4.4, 16.4, WHITE, INK, 1)
        for yy in (14.6, 15.6): o += rr(1.6, yy, 1.95, yy + .5) + rr(4.45, yy, 4.8, yy + .5)
    elif key == 'kitchen':
        o += rr(6.4, 14.6, 8.8, 16.0, '#dedfe1', INK, 0) + rr(5.5, 17.55, 9.7, 17.95, '#cfd0d3', INK, 0)
        o += circ(P(6.9), Q(15.3), 3, WHITE, INK, .6) + circ(P(7.6), Q(15.3), 3, WHITE, INK, .6)
    elif key == 'pantry':
        o += rr(5.5, 10.7, 5.8, 12.7, '#bfc1c5', MID, 0) + rr(7.4, 10.7, 7.7, 12.7, '#bfc1c5', MID, 0)
    elif key == 'theatre':
        o += rr(13.8, 7.2, 17.0, 8.1, '#d9dadc', INK, 2) + rr(13.7, 4.4, 17.1, 4.6, INK, INK, 0)
        for r_ in (5.4, 6.4):
            for i in range(3): o += rr(14.0 + i * 1.05, r_, 14.85 + i * 1.05, r_ + .7, '#bfc1c5', MID, 2)
    elif key == 'guest':
        o += rr(14.6, 11.4, 16.6, 13.5, WHITE, INK, 1) + rr(14.8, 12.9, 15.6, 13.4, '#e9eaec', MID, 2) + rr(15.6, 12.9, 16.4, 13.4, '#e9eaec', MID, 2)
    elif key == 'lounge':
        o += rr(10.6, 14.2, 13.6, 15.4, '#e9eaec', MID, 3) + rr(14.4, 14.6, 16.4, 16.4, WHITE, MID, 1)
    elif key == 'powder':
        o += rr(10.3, 4.4, 10.9, 5.1, WHITE, INK, 2) + rr(11.5, 5.4, 12.1, 5.9, WHITE, INK, 2)
    elif key in ('ensuite',):
        o += rr(10.5, 9.7, 11.1, 10.4, WHITE, INK, 2) + rr(12.0, 9.7, 13.0, 10.3, WHITE, INK, 2)
    elif key in ('m1bed', 'm2bed'):
        bx = 2.6 if key == 'm1bed' else 13.6
        o += rr(bx, 5.0, bx + 2.2, 7.4, WHITE, INK, 1) + rr(bx + .15, 6.7, bx + 1.0, 7.3, '#e9eaec', MID, 3) + rr(bx + 1.2, 6.7, bx + 2.05, 7.3, '#e9eaec', MID, 3)
    elif key in ('m1van', 'm2van'):
        bx = 4.2 if key == 'm1van' else 12.2
        for i in range(2): o += rect(P(bx + .4 + i * 1.1), Q(10.6), 0.8 * s, 0.4 * s, WHITE, INK, .7, 'rx="3"')
        o += rect(P(bx), Q(10.8), 2.4 * s, 0.1 * s, INK, None, 0)
    elif key in ('m1sh', 'm2sh'):
        bx = 2.4 if key == 'm1sh' else 14.78
        o += line(P(bx + .05), Q(9.05), P(bx + 1.55), Q(10.75), MID, .5) + line(P(bx + 1.55), Q(9.05), P(bx + .05), Q(10.75), MID, .5)
    elif key in ('m1wc', 'm2wc'):
        bx = 1.4 if key == 'm1wc' else 16.78
        o += rr(bx - .2, 9.2, bx + .2, 9.65, WHITE, INK, 2) + rr(bx - .22, 9.65, bx + .22, 10.1, WHITE, INK, 6)
    elif key in ('m1wic', 'm2wic'):
        bx = 1.2 if key == 'm1wic' else 14.58
        o += rr(bx, 12.9, bx + 3.0, 13.25, '#bfc1c5', MID, 0) + rr(bx, 10.9, bx + .3, 12.7, '#bfc1c5', MID, 0)
    elif key == 'ulounge':
        o += rr(7.4, 5.0, 11.2, 6.0, '#e9eaec', MID, 3) + rr(8.0, 6.8, 10.6, 7.5, WHITE, MID, 1)
    elif key == 'study':
        o += rr(7.0, 14.5, 11.8, 14.9, '#bfc1c5', MID, 0) + rr(7.4, 12.8, 9.6, 13.7, '#d4d6d9', INK, 0) + rr(7.0, 11.0, 7.3, 14.0, '#bfc1c5', MID, 0)
    elif key in ('core', 'core2'):
        x0 = 7.2; y0 = 6.5 if key == 'core' else 8.2; y1 = 10.7 if key == 'core' else 10.8
        o += rr(x0 + .15, y1 - 1.7, x0 + 1.5, y1 - .1, WHITE, INK, 0) + line(P(x0 + .15), Q(y1 - .1), P(x0 + 1.5), Q(y1 - 1.7), MID, .5) + line(P(x0 + 1.5), Q(y1 - .1), P(x0 + .15), Q(y1 - 1.7), MID, .5)
        yy = y1 - .15
        for i in range(10):
            o += line(P(x0 + 1.7), Q(yy - i * .18), P(x0 + 2.75), Q(yy - i * .18), MID, .5)
        o += text(P(x0 + .83), Q(y1 - 1.8), 'LIFT', 5, 'middle', 700, INK, MONO)
    return o


def ext_stair(v, level):
    """switchback exterior stepped stair, 28 risers @178.6"""
    S_ = STAIR
    o = ''
    n = 13
    tw = (S_['ax1'] - S_['ax0']) / n
    for i in range(n + 1):
        xa = S_['ax0'] + i * tw
        o += line(v.x(xa), v.y(S_['ay0']), v.x(xa), v.y(S_['ay1']), INK, .6)
        xb = S_['ax1'] - i * tw
        o += line(v.x(xb), v.y(S_['by0']), v.x(xb), v.y(S_['by1']), INK, .6)
    o += rect(v.x(S_['ax0']), v.y(S_['ay1']), (S_['ax1'] - S_['ax0']) * v.s, (S_['ay1'] - S_['ay0']) * v.s, 'none', INK, .9)
    o += rect(v.x(S_['ax0']), v.y(S_['by1']), (S_['ax1'] - S_['ax0']) * v.s, (S_['by1'] - S_['by0']) * v.s, 'none', INK, .9)
    lx0, ly0, lx1, ly1 = S_['land']
    o += rect(v.x(lx0), v.y(ly1), (lx1 - lx0) * v.s, (ly1 - ly0) * v.s, '#e9eaec', INK, .9)
    o += rect(v.x(0.1), v.y(4.1), 0.9 * v.s, 2.4 * v.s, '#e9eaec', INK, .9)  # top landing in west setback
    o += text(v.x(2.9), v.y(1.0) + 2.5, 'UP ▸ 14 R', 5.2, 'middle', 700, INK, MONO)
    o += text(v.x(3.0), v.y(2.3) + 2.5, '◂ UP 14 R', 5.2, 'middle', 700, INK, MONO)
    o += text(v.x(3.0), v.y(0.0) + 8.5 if level == 0 else v.y(3.55), 'EXT. STEPPED STAIR 28R @178.6 = +5.00' if level == 0 else 'STAIR ARRIVES +5.00 · PATH TO ENTRY', 5.2, 'middle', 700, ACC, MONO)
    return o


def plan(level, idx):
    v = View(OXS[idx], OY, SC)
    ox, oy = v.ox, v.oy
    W, D = PLOT_W * SC, PLOT_D * SC
    o = [f'<g id="plan{level}">']
    # plot + setback
    o.append(rect(ox, oy, W, D, PAPER, None))
    # zone fills
    if level == 0:
        o.append(rect(ox, oy, W, D, 'url(#soil)', None))
    elif level == 1:
        o.append(rect(ox, oy + v.w(PLOT_D - 4.2), W, v.w(4.2), 'url(#grass)', None))
        o.append(rect(ox, oy, W, v.w(4.0), 'url(#grass)', None))
    else:
        o.append(rect(ox, oy, W, D, 'url(#roof)', None, 0, 'opacity=".55"'))
        o.append(rect(v.x(HX0), v.y(HY1), v.w(HX1 - HX0), v.w(HY1 - HY0), '#f4f4f2', None))
    o.append(rect(ox, oy, W, D, 'none', MID, 1.1, 'stroke-dasharray="6 3"'))
    for sx in (1.0, PLOT_W - 1.0):
        o.append(line(v.x(sx), oy, v.x(sx), oy + D, MID, .6, '2 3'))
    # retaining wall / street
    if level < 2:
        o.append(rect(ox - 8, v.y(0) - 1, W + 16, 7, CH, None))
        o.append(text(ox + W / 2, v.y(0) + 16, 'STREET LEVEL ±0.00m  ·  5.00m RETAINING WALL FACE' if level == 1 else 'STREET ±0.00m  ·  EMBANKMENT +5.00m BEHIND (SOIL HATCH)', 6.2, 'middle', 700, MID, MONO))
    rooms = {0: L0, 1: L1, 2: L2}[level]
    # wall hatch of L1 footprint under L2
    if level == 0:
        for r in rooms:
            o.append(rect(v.x(r[1]), v.y(r[4]), v.w(r[3] - r[1]), v.w(r[4] - r[2]), FILL[r[7]], INK, 4.2))
        o.append(ext_stair(v, 0))
    else:
        for r in rooms:
            o.append(rect(v.x(r[1]), v.y(r[4]), v.w(r[3] - r[1]), v.w(r[4] - r[2]), FILL[r[7]], INK, 2))
        if level == 1:
            o.append(ext_stair(v, 1))
            # front path + garden notes
            o.append(rect(v.x(2.2), v.y(4.0), v.w(8.6), v.w(1.0), '#e3e4e6', MID, .5))
            o.append(text(v.x(9.39), v.y(2.0), 'FRONT GARDEN  18.78 × 4.20', 7.5, 'middle', 700, INK, FONT, halo=True))
            o.append(text(v.x(9.39), v.y(1.2), '(+5.00m terrace over garage roof slab)', 5.6, 'middle', 600, MID, MONO, halo=True))
            o.append(text(v.x(9.39), v.y(20.9) - 22 if False else v.y(19.0), 'BACK GARDEN  18.78 × 4.00', 7.5, 'middle', 700, INK, FONT, halo=True))
            # outdoor kitchen pergola
            r = L1_OUT[0]
            o.append(rect(v.x(r[1]), v.y(r[4]), v.w(r[3] - r[1]), v.w(r[4] - r[2]), '#f1f1f1', INK, 1.4, 'stroke-dasharray="4 2"'))
            o.append(rect(v.x(5.4), v.y(22.0), v.w(5.2), v.w(0.6), '#bfc1c5', INK, .8))
            o.append(circ(v.x(6.4), v.y(21.5), 4, WHITE, INK, .7) + circ(v.x(7.3), v.y(21.5), 4, WHITE, INK, .7) + rect(v.x(8.4), v.y(21.7), v.w(1.4), v.w(.4), '#7a7d83', INK, .6))
            o.append(room_label(v, (r[0], r[1], r[2] + .2, r[3], r[4] - .6, r[5], r[6], r[7]), 6.2))
        if level == 2:
            # balcony
            b = BALCONY
            o.append(rect(v.x(b[0]), v.y(b[3]), v.w(b[2] - b[0]), v.w(b[3] - b[1]), '#ececec', INK, 1.2))
            o.append(rect(v.x(b[0]) + 1.5, v.y(b[1]) - 3, v.w(b[2] - b[0]) - 3, 2.4, GLASS, INK, .5))
            o.append(text(v.x(9.39), v.y(3.2) + 2, 'FRONT CANTILEVERED GLASS BALCONY  16.78 × 2.00', 6.6, 'middle', 700, INK, FONT))
            o.append(text(v.x(3.9), v.y(16.4), 'GREEN ROOF (non-trafficable)', 5.8, 'middle', 700, MID, MONO))
            o.append(text(v.x(14.9), v.y(16.4), 'GREEN ROOF (non-trafficable)', 5.8, 'middle', 700, MID, MONO))
            o.append(text(v.x(9.39), v.y(16.8), 'ROOF TERRACE / PV ARRAY', 5.8, 'middle', 700, MID, MONO))
            o.append(text(v.x(9.39), v.y(20.0), 'BACK GARDEN (+5.00m) — BELOW', 6, 'middle', 700, MID, MONO))
            o.append(text(v.x(9.39), v.y(1.0), 'FRONT GARDEN (+5.00m) — BELOW', 6, 'middle', 700, MID, MONO))
    # furniture + labels
    for r in rooms:
        o.append(furniture(v, r[0]))
    for r in rooms:
        if r[0] in ('m1van', 'm2van', 'm1wc', 'm2wc', 'm1sh', 'm2sh'):
            nm = {'van': 'VANITY', 'wc': 'WC', 'sh': 'SHOWER'}[r[0][2:]]
            cx, cy = v.x((r[1] + r[3]) / 2), v.y((r[2] + r[4]) / 2)
            o.append(text(cx, cy - 1, nm, 5.2, 'middle', 700, INK, FONT) + text(cx, cy + 6.5, r[6], 4.6, 'middle', 600, ACC, MONO))
            if r[0] in ('m1van', 'm2van'):
                cxm = 3.9 if r[0] == 'm1van' else 14.88
                o.append(text(v.x(cxm), v.y(8.75), 'SEPARATE ENCLOSED WC 1.40×1.80', 4.6, 'middle', 700, INK, MONO))
                o.append(text(v.x(cxm), v.y(8.4), 'SEPARATE ENCLOSED SHOWER 1.60×1.80', 4.6, 'middle', 700, INK, MONO))
                o.append(text(v.x(3.9 if r[0] == 'm1van' else 14.88), v.y(8.05), 'DUAL VANITY 2.80m · 2 WASHBASINS', 4.6, 'middle', 700, ACC, MONO))
        elif r[0] in ('living', 'dining', 'kitchen', 'theatre', 'guest', 'lounge', 'garage', 'workshop', 'ulounge', 'study', 'm1bed', 'm2bed'):
            # push label to a free band
            dy = {'living': 1.3, 'dining': -.6, 'kitchen': -1.4, 'theatre': 1.3, 'guest': 0.6, 'lounge': -.3, 'garage': -1.0,
                  'workshop': -.3, 'ulounge': -0.7, 'study': -1.2, 'm1bed': 0.9, 'm2bed': 0.9}.get(r[0], 0)
            rr_ = list(r); rr_[2] += dy; rr_[4] += dy
            o.append(room_label(v, tuple(rr_), 6.6))
        else:
            o.append(room_label(v, r))
    # exterior walls
    if level == 1:
        o.append(rect(v.x(HX0), v.y(HY1), v.w(HX1 - HX0), v.w(HY1 - HY0), 'none', INK, 7))
    if level == 2:
        o.append(rect(v.x(HX0), v.y(15.0), v.w(HX1 - HX0), v.w(15.0 - HY0), 'none', INK, 7))
        o.append(rect(v.x(HX0), v.y(13.4), v.w(5.8), v.w(1.0), 'none', INK, 0))
        o.append(line(v.x(1.0), v.y(13.4), v.x(1.0), v.y(15.0), INK, 7))
        o.append(line(v.x(6.8), v.y(13.4), v.x(6.8), v.y(15.0), INK, 7))
        o.append(line(v.x(HX1), v.y(13.4), v.x(HX1), v.y(15.0), INK, 7))
        o.append(line(v.x(11.98), v.y(13.4), v.x(11.98), v.y(15.0), INK, 7))
    # openings
    if level == 0:
        o.append(wall_gap(v, 6.79, 0.0, 5.2, 'h', .5))
        o.append(rect(v.x(6.79), v.y(0) - 3, v.w(5.2), 6, INK, None))
        o.append(tag(v.x(9.39), v.y(0) - 12, 'GD-01  5200×2400'))
        o.append(door(v, 7.2, 6.5, 0.9, 'h', True, -1, 'D-08'))
        o.append(door(v, 10.1, 7.2, 0.9, 'v', True, 1, 'D-08'))
        o.append(door(v, 11.2, 10.7, 0.9, 'h', True, 1, 'D-08'))
        o.append(door(v, 12.0, 6.5, 0.9, 'h', True, -1, 'D-08'))
    elif level == 1:
        o.append(win(v, 1.4, 4.2, 5.4, 'h', 'W-01'))
        o.append(win(v, 7.25, 4.2, 0.6, 'h', 'W-02'))
        o.append(door(v, 7.95, 4.2, 1.8, 'h', True, 1, 'D-01'))
        o.append(win(v, 10.7, 4.2, 1.2, 'h', 'W-05'))
        o.append(door(v, 1.2, 18.0, 4.0, 'h', True, 1, 'D-02', True))
        o.append(door(v, 5.6, 18.0, 2.4, 'h', True, 1, 'D-03', True))
        o.append(win(v, 8.3, 18.0, 1.2, 'h', 'W-03'))
        o.append(door(v, 10.6, 18.0, 4.0, 'h', True, 1, 'D-02', True))
        o.append(win(v, 17.78, 14.5, 2.4, 'v', 'W-09', 1))
        o.append(win(v, 17.78, 10.6, 1.8, 'v', 'W-04', 1))
        o.append(win(v, 1.0, 14.2, 1.8, 'v', 'W-10', -1))
        o.append(win(v, 1.0, 10.9, 1.2, 'v', 'W-05', -1))
        o.append(door(v, 12.98, 5.0, 1.5, 'v', True, -1, 'D-04'))
        for key, dx, dy, dl, ori, hf, nm in [('guest', 14.0, 9.6, 0.9, 'h', True, 1), ('ensuite', 10.8, 9.6, 0.8, 'h', True, 1),
                                          ('laundry', 2.0, 10.4, 0.9, 'h', True, 1), ('pantry', 6.0, 12.8, 0.9, 'h', True, -1), ('powder', 10.1, 4.9, 0.8, 'v', True, 1)]:
            o.append(door(v, dx, dy, dl, ori, hf, nm, 'D-07'))
        o.append(door(v, 11.0, 6.0, 0.9, 'h', True, 1, 'D-07'))
    else:
        b = BALCONY
        o.append(door(v, 3.0, 4.2, 2.4, 'h', True, 1, 'D-05', True))
        o.append(door(v, 13.38, 4.2, 2.4, 'h', True, 1, 'D-05', True))
        o.append(door(v, 7.59, 4.2, 3.6, 'h', True, 1, 'D-06', True))
        o.append(win(v, 1.0, 5.5, 2.0, 'v', 'W-06', -1))
        o.append(win(v, 17.78, 5.5, 2.0, 'v', 'W-06', 1))
        o.append(win(v, 1.0, 9.3, 1.2, 'v', 'W-05', -1))
        o.append(win(v, 17.78, 9.3, 1.2, 'v', 'W-05', 1))
        o.append(win(v, 1.0, 11.2, 1.5, 'v', 'W-07', -1))
        o.append(win(v, 17.78, 11.2, 1.5, 'v', 'W-07', 1))
        o.append(win(v, 7.89, 15.0, 3.0, 'h', 'W-08', -1))
        for dx, dy, dl, ori, nm, hf in [(5.0, 9.0, 0.9, 'h', 1, True), (5.2, 10.8, 0.9, 'h', -1, True), (3.0, 9.0, 0.7, 'h', 1, True), (1.5, 9.0, 0.7, 'h', 1, True),
                                         (15.2, 9.0, 0.9, 'h', 1, False), (13.0, 10.8, 0.9, 'h', -1, True), (15.4, 9.0, 0.7, 'h', 1, False), (16.7, 9.0, 0.7, 'h', 1, False)]:
            o.append(door(v, dx, dy, dl, ori, hf, nm, None))
    # dimension chains
    top = oy - 8
    o.append(hdim(v.x(0), v.x(PLOT_W), top - 20, '18.78m  PLOT WIDTH', top, 8, ACC, True, True))
    o.append(hdim(v.x(0), v.x(1.0), top - 2, '1.00m', top + 8, 6.5))
    o.append(hdim(v.x(1.0), v.x(PLOT_W - 1.0), top - 2, '16.78m BUILDING', top + 8, 7))
    o.append(hdim(v.x(PLOT_W - 1.0), v.x(PLOT_W), top - 2, '1.00m', top + 8, 6.5))
    lx = ox - 10
    o.append(vdim(lx - 24, v.y(0), v.y(22), '22.00m PLOT DEPTH', lx + 8, 8, ACC, True, True))
    chain = {0: [(0, 6.5, '6.50'), (6.5, 10.7, '4.20'), (10.7, 13.5, '2.80'), (13.5, 22, '8.50')],
             1: [(0, 4.2, '4.20 FRONT'), (4.2, 18.0, '13.80 HOUSE'), (18.0, 22, '4.00 BACK')],
             2: [(0, 2.2, '2.20'), (2.2, 4.2, '2.00 BALC.'), (4.2, 18.0, '13.80 HOUSE'), (18, 22, '4.00')]}[level]
    for a, b, lab in chain:
        o.append(vdim(lx - 2, v.y(a), v.y(b), lab, lx + 8, 6.4))
    bot = {0: [(0, 1.0, '1.00'), (1.0, 6.14, '5.14'), (6.14, 12.64, '6.50 GARAGE'), (12.64, 17.78, '5.14'), (17.78, 18.78, '1.00')],
           1: [(0, 1.0, '1.00'), (1.0, 7.2, '6.20'), (7.2, 10.1, '2.90'), (10.1, 12.98, '2.88'), (12.98, 17.78, '4.80'), (17.78, 18.78, '1.00')],
           2: [(0, 1.0, '1.00'), (1.0, 6.8, '5.80'), (6.8, 11.98, '5.18'), (11.98, 17.78, '5.80'), (17.78, 18.78, '1.00')]}[level]
    by = oy + D + 22
    for a, b, lab in bot:
        o.append(hdim(v.x(a), v.x(b), by, lab, by - 12, 6.4, INK, False))
    o.append(hdim(v.x(0), v.x(PLOT_W), by + 14, '18.78m', by + 2, 8, ACC, False, True))
    # section mark on L0
    if level == 0:
        o.append(line(v.x(11.0), v.y(-0.8), v.x(11.0), v.y(16.5), ACC, 1, '8 3 2 3'))
        o.append(tag(v.x(11.0), v.y(-0.8) + 8, 'A', 8, ACC) + tag(v.x(11.0), v.y(16.5) - 6, 'A', 8, ACC))
    # north arrow
    ax_, ay_ = ox + W - 12, oy - 70 if False else oy + 14
    if level == 2:
        pass
    o.append('</g>')
    return ''.join(o)


def area_table(level):
    rooms = {0: L0, 1: L1 + L1_OUT, 2: L2}[level]
    rows = ''.join(f'<tr><td>{esc(r[5].title() if False else r[5])}</td><td class="n">{r[6]}</td><td class="n">{area(r):.1f}</td></tr>' for r in rooms)
    return rows
