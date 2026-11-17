from kit import *

BLK = '#17181a'; CHR = '#46484c'; WHT = '#f7f7f5'; GRY = '#a9abb0'; GL = '#c5d0d7'


class E:
    def __init__(self, ox, gy, s, mirror=None):
        self.ox, self.gy, self.s, self.mirror = ox, gy, s, mirror

    def x(self, m):
        return self.ox + ((self.mirror - m) if self.mirror else m) * self.s

    def z(self, z): return self.gy - z * self.s

    def r(self, x0, z0, x1, z1, fill, stroke=INK, sw=.8, extra=''):
        a, b = self.x(x0), self.x(x1)
        return rect(min(a, b), self.z(z1), abs(b - a), (z1 - z0) * self.s, fill, stroke, sw, extra)


DEFS = f'''<defs>
<pattern id="board" width="{0.6*26}" height="10" patternUnits="userSpaceOnUse"><rect width="{0.6*26}" height="10" fill="{CHR}"/><line x1="0" y1="0" x2="0" y2="10" stroke="#5b5d62" stroke-width=".8"/></pattern>
<pattern id="fins" width="5" height="10" patternUnits="userSpaceOnUse"><rect width="5" height="10" fill="{BLK}"/><line x1="0" y1="0" x2="0" y2="10" stroke="#34363a" stroke-width="1"/></pattern>
<pattern id="slat" width="10" height="4" patternUnits="userSpaceOnUse"><rect width="10" height="4" fill="{BLK}"/><line x1="0" y1="0" x2="10" y2="0" stroke="#3a3c40" stroke-width=".8"/></pattern>
<pattern id="soilE" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0,7 L7,0" stroke="{MID}" stroke-width=".5"/></pattern>
<pattern id="stone" width="14" height="7" patternUnits="userSpaceOnUse"><rect width="14" height="7" fill="#8f9297"/><path d="M0,0 H14 M0,3.5 H14 M7,0 V3.5 M0,3.5 V7" stroke="#76797e" stroke-width=".5"/></pattern>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#dfe7ec"/><stop offset="1" stop-color="#b3c1ca"/></linearGradient>
</defs>'''


def glass(e, x0, z0, x1, z1, mull=None, label=None):
    o = e.r(x0, z0, x1, z1, 'url(#glass)', BLK, 1.6)
    if mull:
        n = mull
        for i in range(1, n):
            xx = x0 + (x1 - x0) * i / n
            o += line(e.x(xx), e.z(z0), e.x(xx), e.z(z1), BLK, 1.1)
    # reflection streaks
    mx = (e.x(x0) + e.x(x1)) / 2
    o += line(e.x(x0) + 3, e.z(z0) - 4, e.x(x0) + 18, e.z(z1) + 4, '#fff', 1.2, None, 'opacity=".55"') if abs(e.x(x1) - e.x(x0)) > 30 else ''
    if label:
        o += tag(mx, (e.z(z0) + e.z(z1)) / 2, label, 6)
    return o


def levels(e, x_left, x_right, zs, ext_x):
    o = ''
    for z, lab in zs:
        y = e.z(z)
        o += line(x_left - 4, y, ext_x, y, ACC if z in (5.0,) else MID, .5, '7 3 1.5 3')
        o += f'<path d="M{f(x_left)},{f(y)} l-4,-6 h8 z" fill="{ACC if z==5.0 else INK}"/>'
        o += text(x_left - 7, y + 3, lab, 7.4, 'end', 700, ACC if z == 5.0 else INK, MONO, halo=True)
    return o


def front(ox, gy, s=26, rear=False):
    e = E(ox, gy, s, PLOT_W if rear else None)
    o = [DEFS if False else '']
    W = PLOT_W
    # street / ground
    if not rear:
        o.append(rect(ox - 22, gy, W * s + 44, 12, 'url(#soilE)', None))
        o.append(line(ox - 22, gy, ox + W * s + 22, gy, INK, 1.6))
        # retaining wall
        o.append(e.r(0, 0, W, 5.0, 'url(#board)', INK, 1))
        o.append(e.r(-0.05, 5.0, W + .05, 5.14, WHT, INK, 1))
        # garage portal
        o.append(e.r(6.54, 0, 12.24, 2.95, '#26272a', INK, 1))
        o.append(e.r(6.79, 0, 11.99, 2.4, 'url(#slat)', INK, 1.2))
        o.append(e.r(6.79, 2.4, 11.99, 2.5, '#e8e8e8', None, 0))
        o.append(tag(e.x(9.39), e.z(1.2), 'GD-01', 7))
        o.append(text(e.x(9.39), e.z(2.7), '5200 × 2400 MOTORIZED', 5.8, 'middle', 700, '#e8e8e8', MONO))
        # pedestrian gate to stair
        o.append(e.r(1.2, 0, 2.3, 2.1, '#26272a', INK, 1))
        o.append(text(e.x(1.75), e.z(2.35), 'STAIR GATE', 5.2, 'middle', 700, WHT, MONO))
        # hedge + balustrade
        for a, b in ((0.3, 5.9), (12.4, 18.5)):
            o.append(f'<path d="M{f(e.x(a))},{f(e.z(5.14))} q4,-12 12,-8 q8,-10 20,-4 q10,-9 22,-2 L{f(e.x(b))},{f(e.z(5.14))} z" fill="#9b9ea3" opacity=".55"/>')
        o.append(e.r(0.15, 5.14, W - .15, 6.2, 'url(#glass)', INK, .5, 'opacity=".5"'))
    else:
        o.append(rect(ox - 22, e.z(5.0), W * s + 44, 5.0 * s, 'url(#soilE)', None, 0, 'opacity=".6"'))
        o.append(line(ox - 22, e.z(5.0), ox + W * s + 22, e.z(5.0), INK, 1.6))
        o.append(line(ox - 22, gy, ox + W * s + 22, gy, MID, .6, '8 3'))
        
    # --- L1 volume
    o.append(e.r(1.0, 5.0, 17.78, 8.4, WHT, INK, 1.2))
    if not rear:
        o.append(glass(e, 1.4, 5.1, 6.8, 7.5, 3, 'W-01'))
        o.append(glass(e, 7.25, 5.0, 7.85, 7.4, None))
        o.append(tag(e.x(7.55), e.z(7.75), 'W-02', 5.5))
        o.append(e.r(7.95, 5.0, 9.75, 7.4, BLK, INK, 1.4))
        o.append(line(e.x(8.85), e.z(5.0), e.x(8.85), e.z(7.4), '#55575b', .8))
        o.append(tag(e.x(8.85), e.z(6.2), 'D-01', 7))
        o.append(e.r(10.1, 5.0, 12.98, 8.4, 'url(#stone)', INK, 1))
        o.append(glass(e, 10.7, 6.7, 11.9, 7.3))
        o.append(tag(e.x(11.3), e.z(7.85), 'W-05', 5.5))
        o.append(e.r(12.98, 5.0, 17.78, 8.4, 'url(#fins)', INK, 1))
        o.append(text(e.x(15.38), e.z(6.7), 'ACOUSTIC THEATER · NO OPENINGS', 5.2, 'middle', 700, '#d0d0d0', MONO))
    else:
        # rear wall (north) mirrored
        o.append(glass(e, 1.2, 5.0, 5.2, 7.4, 4, 'D-02'))
        o.append(glass(e, 5.6, 5.0, 8.0, 7.4, 2, 'D-03'))
        o.append(glass(e, 8.3, 6.1, 9.5, 7.3, None))
        o.append(tag(e.x(8.9), e.z(7.75), 'W-03', 5.5))
        o.append(glass(e, 10.6, 5.0, 14.6, 7.4, 4, 'D-02'))
        o.append(e.r(15.2, 5.0, 17.78, 8.4, 'url(#stone)', INK, 1))
        # rear boundary wall + outdoor kitchen pergola
        o.append(e.r(0, 5.0, W, 6.1, '#e4e5e6', INK, 1))
        o.append(e.r(5.4, 5.0, 10.6, 5.95, '#1d1e20', INK, 1))
        o.append(e.r(5.4, 5.95, 10.6, 6.05, '#8b8e94', INK, .6))
        for px in (5.4, 10.5): o.append(e.r(px, 6.05, px + .1, 7.9, BLK, None, 0))
        o.append(e.r(5.3, 7.9, 10.7, 8.05, BLK, None, 0))
        for i in range(14): o.append(line(e.x(5.4 + i * 0.4), e.z(7.9), e.x(5.4 + i * 0.4), e.z(8.05), '#666', 1))
        o.append(text(e.x(8.0), e.z(5.45), 'OUTDOOR KITCHEN & BBQ 5200 × 2200', 5.4, 'middle', 700, WHT, MONO))
    # slab line L1/L2
    o.append(e.r(0.9, 8.1, 17.88, 8.4, WHT, INK, 1))
    # --- L2 volume
    o.append(e.r(1.0, 8.4, 17.78, 11.3, 'url(#fins)', INK, 1.2))
    if not rear:
        o.append(glass(e, 3.0, 8.5, 5.4, 10.9, 2, 'D-05'))
        o.append(glass(e, 13.38, 8.5, 15.78, 10.9, 2, 'D-05'))
        o.append(glass(e, 7.59, 8.5, 11.19, 10.9, 3, 'D-06'))
        o.append(e.r(0.9, 8.15, 17.88, 8.4, WHT, INK, 1))
        o.append(e.r(1.0, 8.4, 17.78, 9.5, GL, INK, .6, 'opacity=".35"'))
    else:
        o.append(glass(e, 7.89, 9.3, 10.89, 10.5, 3, 'W-08'))
        o.append(text(e.x(3.9), e.z(9.9), 'MASTER 1 SUITE', 5.4, 'middle', 700, '#cfcfcf', MONO))
        o.append(text(e.x(14.9), e.z(9.9), 'MASTER 2 SUITE', 5.4, 'middle', 700, '#cfcfcf', MONO))
    o.append(e.r(0.9, 11.0, 17.88, 11.3, WHT, INK, 1))
    o.append(e.r(0.9, 11.3, 17.88, 11.8, WHT, INK, 1.2))
    o.append(text(e.x(9.39), e.z(11.55) + 2, 'ROOF PARAPET +11.80', 5, 'middle', 700, INK, MONO))
    # dimension chains
    base = gy + 20
    L = e.x(0) if not rear else ox
    o.append(hdim(ox, ox + W * s, base + 18, '18.78m PLOT WIDTH', base + 4, 8, ACC, False, True))
    segs = [(0, 1.0, '1.00'), (1.0, 17.78, '16.78m FACADE WIDTH'), (17.78, 18.78, '1.00')]
    for a, b, lab in segs:
        o.append(hdim(ox + a * s, ox + b * s, base, lab, base - 12, 7, INK, False))
    zs = [(0, '±0.00'), (5.0, '+5.00'), (8.4, '+8.40'), (11.8, '+11.80')]
    xl = ox - 30
    lz = [(0, '±0.00 STREET'), (5.0, '+5.00 L1'), (8.4, '+8.40 L2'), (11.8, '+11.80 PARAPET')]
    for z, lab in lz:
        y = e.z(z)
        o.append(line(xl, y, ox + W * s + 6, y, ACC if z == 5.0 else MID, .45, '7 3 1.5 3'))
        o.append(f'<path d="M{f(xl)},{f(y)} l-4,-6 h8 z" fill="{ACC if z==5.0 else INK}"/>')
        o.append(text(xl - 7, y + 3, lab, 6.8, 'end', 700, ACC if z == 5.0 else INK, MONO, halo=True))
    xr = ox + W * s + 18
    for (a, b, lab) in [(0, 5.0, '5.00'), (5.0, 8.4, '3.40'), (8.4, 11.8, '3.40')]:
        o.append(vdim(xr, e.z(a), e.z(b), lab, xr - 10, 7, ACC if a == 0 else INK, False, a == 0))
    o.append(vdim(xr + 18, e.z(0), e.z(11.8), '11.80 TOTAL', xr + 8, 7.5, ACC, False, True))
    return ''.join(o)


def side(ox, gy, s=15, west=True):
    """west: street(south) on the right; east: south on the left. y -> x."""
    D = PLOT_D
    mir = D if west else None
    e = E(ox, gy, s, mir)
    o = []
    yx = lambda m: e.x(m)
    ground5 = e.z(5.0)
    # street + soil
    sx0, sx1 = (e.x(0), e.x(-3)) if True else (0, 0)
    o.append(rect(min(e.x(-3), e.x(D)), gy, abs(e.x(D) - e.x(-3)), 10, 'url(#soilE)', None))
    o.append(line(min(e.x(-3), e.x(D)), gy, max(e.x(-3), e.x(D)), gy, INK, 1.6))
    # retaining wall + earth block (cut profile)
    xa, xb = sorted((e.x(0), e.x(D)))
    o.append(rect(xa, ground5, xb - xa, gy - ground5, 'url(#soilE)', INK, .8))
    wx = e.x(0) if not west else e.x(0) - 0.4 * s
    o.append(rect(min(e.x(0), e.x(0.4)), ground5, 0.4 * s, 5 * s, CHR, INK, 1))
    # stepped landscape beyond (stair silhouette 28 risers)
    pts = []
    for i in range(0, 15):
        yy = 0.3 + i * 0.28
        pts += [(e.x(yy), e.z(i * 5 / 14)), (e.x(yy + 0.28), e.z(i * 5 / 14))]
    o.append(pline(pts, GRY, 1, '3 2'))
    o.append(text(e.x(2.2), e.z(2.6), 'STEPPED STAIR + LANDSCAPE', 5, 'middle', 600, GRY, MONO, rot=-27 if not west else 27))
    # side boundary stepped planter wall
    o.append(rect(xa, e.z(5.6), xb - xa, 0.6 * s, '#d9dadc', INK, .8))
    for i, (ya, yb) in enumerate(((0.4, 4.2), (4.2, 11), (11, 22))):
        zz = 5.6 + 0.0
    o.append(text((xa + xb) / 2, e.z(5.25), 'STEPPED BLACK / GREY / WHITE PLANTER WALL', 5.2, 'middle', 700, INK, MONO))
    # house L1
    o.append(e.r(HY0, 5.0, HY1, 8.4, WHT, INK, 1.2))
    o.append(e.r(HY0 - 0.0, 8.4, HY1, 11.3, 'url(#fins)', INK, 1.2))
    o.append(e.r(HY0, 8.1, HY1, 8.4, WHT, INK, 1))
    # cantilever balcony
    o.append(e.r(2.2, 8.1, 4.2, 8.4, WHT, INK, 1))
    o.append(e.r(2.2, 8.4, 4.2, 9.5, GL, INK, .7, 'opacity=".6"'))
    o.append(e.r(2.2, 8.4, 2.25, 9.5, INK, None, 0))
    o.append(e.r(2.2, 8.4, 4.2, 9.5, 'none', INK, .6))
    o.append(e.r(2.2, 8.1, 4.2, 8.4, WHT, INK, 1))
    # roof
    o.append(e.r(HY0 - .1, 11.3, HY1 + .1, 11.8, WHT, INK, 1.2))
    # windows
    if west:
        g = [(10.9, 5.0 + 1.7, 12.1, 5.0 + 2.3, 'W-05'), (14.2, 5.9, 16.0, 7.4, 'W-10'),
             (5.5, 9.3, 7.5, 10.8, 'W-06'), (9.3, 10.1, 10.5, 10.7, 'W-05'), (11.2, 9.5, 12.7, 10.7, 'W-07')]
    else:
        g = [(10.6, 5.9, 12.4, 7.4, 'W-04'), (14.5, 5.9, 16.9, 7.4, 'W-09'),
             (5.5, 9.3, 7.5, 10.8, 'W-06'), (9.3, 10.1, 10.5, 10.7, 'W-05'), (11.2, 9.5, 12.7, 10.7, 'W-07')]
    for a, z0, b, z1, lab in g:
        o.append(glass(e, a, z0, b, z1))
        o.append(tag(e.x((a + b) / 2), e.z((z0 + z1) / 2), lab, 5))
    # stone pier at front
    o.append(e.r(HY0, 5.0, 5.0, 8.4, 'url(#stone)', INK, 1) if False else '')
    # dims
    base = gy + 20
    o.append(hdim(e.x(0) if not west else e.x(22), e.x(22) if not west else e.x(0), base + 14, '22.00m PLOT DEPTH', base + 2, 7.5, ACC, False, True))
    for a, b, lab in [(0, 4.2, '4.20'), (4.2, 18.0, '13.80 HOUSE'), (18.0, 22.0, '4.00')]:
        x1_, x2_ = sorted((e.x(a), e.x(b)))
        o.append(hdim(x1_, x2_, base, lab, base - 10, 6.5, INK, False))
    xr = (xb if not west else xa)
    for (a, b, lab) in [(0, 5, '5.00'), (5, 8.4, '3.40'), (8.4, 11.8, '3.40')]:
        xx = (max(e.x(0), e.x(D)) + 20) if not west else (min(e.x(0), e.x(D)) - 20)
        o.append(vdim(xx, e.z(a), e.z(b), lab, xx - (10 if not west else -10), 6.5, ACC if a == 0 else INK, west, a == 0))
    return ''.join(o)


def section(ox, gy, s=29):
    """Longitudinal section A-A at x=11.0 ; y -> horizontal (south left)."""
    e = E(ox, gy, s)
    o = []
    Y = lambda m: e.x(m)
    Z = lambda m: e.z(m)
    P = lambda y0, y1, z0, z1, fill=INK: rect(Y(y0), Z(z1), (y1 - y0) * s, (z1 - z0) * s, fill, INK, .6)
    # soil mass
    o.append(rect(Y(0), Z(5.0), 22 * s, 5.5 * s, 'url(#soilE)', None))
    o.append(line(Y(-3.2), Z(0), Y(0), Z(0), INK, 1.6))
    o.append(text(Y(-1.6), Z(0) + 11, 'STREET', 6, 'middle', 700, MID, MONO))
    # L0 void rooms
    for a, b in ((0.4, 6.5), (6.5, 10.7), (10.7, 13.5)):
        o.append(rect(Y(a), Z(4.4), (b - a) * s, 4.4 * s, '#ffffff' if a < 10 else '#e3e4e6', None))
    o.append(P(0.4, 13.8, -0.4, 0))                   # foundation
    o.append(P(6.5, 6.7, 0, 4.4)); o.append(P(10.7, 10.9, 0, 4.4)); o.append(P(13.5, 13.8, 0, 4.4))
    o.append(P(0.4, 13.8, 4.4, 4.7))                  # L0 roof slab
    o.append(P(0.0, 0.4, 2.4, 5.0, CHR))              # retaining wall above portal header
    o.append(P(0.0, 0.4, 0, 2.4, BLK))                # garage door
    o.append(tag(Y(-0.7), Z(1.2), 'GD-01', 6))
    o.append(rect(Y(0.4), Z(5.0), 21.6 * s, 0, 'none', INK, 0))
    o.append(rect(Y(0.4), Z(4.95), 13.4 * s, 0.25 * s, '#cfd0d3', INK, .5))   # topping / planter
    # glass balustrade at crest
    o.append(rect(Y(0.0), Z(6.1), 0.1 * s, 1.1 * s, GL, INK, .6))
    # L1
    o.append(P(4.2, 4.5, 5.0, 8.0))                                           # front wall
    o.append(P(17.7, 18.0, 7.4, 8.0)); o.append(rect(Y(17.72), Z(7.4), 0.26 * s, 2.4 * s, GL, INK, .8))  # rear wall + sliding glass
    for yy in (6.0, 8.4, 9.6, 11.6, 13.8):
        o.append(P(yy - .06, yy + .06, 5.0, 8.0))
    o.append(P(4.2, 18.0, 8.0, 8.4))                                          # L1 ceiling / L2 floor slab
    # balcony cantilever
    o.append(P(2.2, 4.2, 8.1, 8.4)); o.append(rect(Y(2.2), Z(9.5), 0.08 * s, 1.1 * s, GL, INK, .6))
    # L2
    o.append(rect(Y(4.2), Z(10.9), 0.3 * s, 2.5 * s, GL, INK, .8))             # front sliding glass D-06
    o.append(P(4.2, 4.5, 10.9, 11.0))
    o.append(P(14.7, 15.0, 8.4, 11.0))                                        # study rear wall
    o.append(P(10.75, 10.85, 8.4, 11.0))
    o.append(P(4.2, 15.0, 11.0, 11.3))                                        # roof slab
    o.append(P(4.2, 4.45, 11.3, 11.8, WHT)); o.append(P(14.75, 15.0, 11.3, 11.8, WHT))
    o.append(P(4.2, 15.0, 11.3, 11.4, '#cfd0d3'))
    # green roof over rear L1
    o.append(rect(Y(15.0), Z(8.7), 3.0 * s, 0.3 * s, '#a7aaae', INK, .5, 'opacity=".7"'))
    o.append(P(17.8, 18.0, 8.4, 9.0))
    o.append(text(Y(16.4), Z(9.25), 'GREEN ROOF', 5.5, 'middle', 700, MID, MONO))
    # stair beyond
    pts = []
    for i in range(15):
        yy = 0.4 + i * 0.26
        pts += [(Y(yy), Z(i * 5 / 14)), (Y(yy + 0.26), Z(i * 5 / 14))]
    o.append(pline(pts, '#7a7d83', 1.1, '3 2'))
    o.append(text(Y(0.6), Z(3.6), 'EXT. STEPPED STAIR', 5, 'start', 700, '#7a7d83', MONO, rot=-38))
    cz = []
    for i in range(14):
        cz += [(Y(6.9 + i * 0.27), Z(i * 5 / 14)), (Y(6.9 + (i + 1) * 0.27), Z(i * 5 / 14))]
    o.append(pline(cz, '#7a7d83', 1, '3 2'))
    o.append(text(Y(8.5), Z(0.45), 'INTERNAL STAIR + LIFT (beyond)', 5, 'middle', 700, '#7a7d83', MONO))
    # outdoor kitchen beyond
    o.append(rect(Y(19.8), Z(5.95), 2.2 * s, 0.95 * s, '#d4d5d8', INK, .7))
    o.append(rect(Y(19.8), Z(7.9), 2.2 * s, 0.12 * s, BLK, None, 0))
    for px in (19.8, 21.9): o.append(rect(Y(px), Z(7.9), 0.1 * s, 1.9 * s, BLK, None, 0))
    o.append(text(Y(20.9), Z(8.3), 'OUTDOOR KITCHEN (beyond)', 4.8, 'middle', 700, MID, MONO))
    o.append(line(Y(0.4), Z(5.0), Y(22.0), Z(5.0), INK, 1.4))
    lab = lambda y, z, t, fs=6.4, c=INK, w=700: o.append(text(Y(y), Z(z), t, fs, 'middle', w, c, FONT))
    lab(3.5, 3.3, '2-CAR GARAGE', 7.4); lab(3.5, 2.75, '6.50 × 6.50', 6.2, ACC, 600)
    lab(8.6, 3.5, 'CAR REPAIR / STORAGE', 7); lab(8.6, 2.95, '6.50 × 4.20', 6.2, ACC, 600)
    o.append(rect(Y(7.4), Z(2.7), 3.0 * s, 0.1 * s, '#7a7d83', INK, .5)); lab(8.9, 2.4, 'MEZZANINE +2.70', 4.8, MID, 700)
    lab(12.1, 3.4, 'ELEC / IT /', 6); lab(12.1, 2.95, 'CCTV / NVR', 6); lab(12.1, 2.45, '3.40 × 2.80', 5.6, ACC, 600)
    lab(2.1, 5.6, 'FRONT GARDEN', 5.8, MID, 700)
    lab(5.1, 7.1, 'POWDER', 5); lab(7.2, 7.1, 'STORE', 5); lab(9.0, 7.1, 'HALL', 5); lab(10.6, 7.1, 'ENSUITE', 5); lab(12.7, 7.1, 'HALL', 5)
    lab(15.9, 6.5, 'FAMILY LOUNGE', 7); lab(15.9, 5.95, '7.98 × 4.20', 6, ACC, 600)
    lab(6.3, 9.9, 'UPPER LOUNGE', 6.6); lab(12.9, 9.9, 'STUDY GALLERY', 6.6)
    lab(3.2, 9.0, 'BALCONY', 5, INK, 700)
    lab(19.3, 5.5, 'BACK GARDEN', 6.2, MID, 700)
    lab(10.5, 4.4 + 0.0, '', 1)
    lab(7.0, 4.12, 'CLEAR 4.40 · SLAB 4.40–4.70 · TOPPING TO +5.00', 4.8, MID, 700)
    lab(10.9, 7.7 if False else 8.15, '', 1)
    xr = Y(22.0) + 10
    for z, t in ((0, '±0.00'), (5.0, '+5.00'), (8.4, '+8.40'), (11.8, '+11.80')):
        o.append(line(Y(-0.6), Z(z), xr + 4, Z(z), ACC if z == 5 else MID, .5, '7 3 1.5 3'))
        o.append(f'<path d="M{f(xr+6)},{f(Z(z))} l6,-4 v8 z" fill="{ACC if z==5 else INK}"/>')
        o.append(text(xr + 14, Z(z) + 3, t, 6.6, 'start', 700, ACC if z == 5 else INK, MONO))
    xl = Y(-3.0)
    for a, b, t in ((0, 5.0, '5.00'), (5.0, 8.4, '3.40'), (8.4, 11.8, '3.40')):
        o.append(vdim(xl, Z(a), Z(b), t, xl + 8, 7, ACC if a == 0 else INK, True, a == 0))
    o.append(vdim(xl - 18, Z(0), Z(11.8), '11.80', xl + 8, 7.5, ACC, True, True))
    by = Z(-0.4) + 20
    pts = [0, 4.2, 6.5, 10.7, 13.5, 18.0, 22.0]
    labs = ['4.20', '2.30', '4.20', '2.80', '4.50', '4.00']
    for i in range(6):
        o.append(hdim(Y(pts[i]), Y(pts[i + 1]), by, labs[i], by - 12, 6.8, INK, False))
    o.append(hdim(Y(0), Y(22), by + 16, '22.00m PLOT DEPTH (SOUTH → NORTH)', by + 3, 8, ACC, False, True))
    return ''.join(o)
