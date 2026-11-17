import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from kit import *
from elev import DEFS, BLK, WHT, GL

BF = 'Black thermally-broken aluminium (RAL 9005)'
# tag, name, location, level, W, H, sill, frame, glazing, qty, op
DOORS = [
    ('GD-01', 'Motorized sectional garage door', 'Street-level garage portal', 'L0', 5200, 2400, 0, 'Black alu sandwich panel, RAL 9005', 'Insulated 40mm PU panel + 2 vision slits', 1, 'garage'),
    ('D-01', 'Pivot entry door', 'Entry foyer (front)', 'L1', 1800, 2400, 0, 'Black alu pivot, central axis', '10.76 laminated + sidelight W-02', 1, 'pivot'),
    ('D-02', '4-panel lift-slide', 'Dining + Family Lounge to Back Garden', 'L1', 4000, 2400, 0, BF, '6+12Ar+6 Low-E DGU', 2, 'lift4'),
    ('D-03', '2-panel slider', 'Kitchen to Outdoor Kitchen', 'L1', 2400, 2400, 0, BF, '6+12Ar+6 Low-E DGU', 1, 'slide2'),
    ('D-04', 'Acoustic double-leaf', 'Home Theater', 'L1', 1500, 2100, 0, 'Black steel-skin acoustic leaf', 'Solid core 48dB Rw, no glass', 1, 'double'),
    ('D-05', '2-panel balcony slider', 'Master 1 / Master 2 to front balcony', 'L2', 2400, 2400, 0, BF, '8+12Ar+8 Low-E laminated', 2, 'slide2'),
    ('D-06', '3-panel balcony slider', 'Upper Lounge to front balcony', 'L2', 3600, 2400, 0, BF, '8+12Ar+8 Low-E laminated', 1, 'slide3'),
    ('D-07', 'Interior flush swing / pocket', 'Bedrooms, baths, WC, shower, WIC, laundry', 'L1/L2', 900, 2100, 0, 'Black alu frame, white flush leaf', 'Solid / opaque', 14, 'swing'),
    ('D-08', 'Fire-rated steel service door', 'Garage, workshop, NVR room, core', 'L0', 900, 2100, 0, 'Black powder-coat steel, 60 min', 'Solid, panic-free latch', 4, 'steel'),
]
WINS = [
    ('W-01', 'Fixed + vent picture window', 'Living Room (front)', 'L1', 5400, 2400, 100, BF, '8+12Ar+8 Low-E laminated', 1, 'fix3'),
    ('W-02', 'Fixed sidelight', 'Entry Foyer', 'L1', 600, 2400, 0, BF, '10.76 laminated', 1, 'fix'),
    ('W-03', 'Casement window', 'Kitchen (rear)', 'L1', 1200, 1200, 1100, BF, '6+12Ar+6 Low-E DGU', 1, 'case'),
    ('W-04', 'Sliding window', 'Guest Bedroom (east)', 'L1', 1800, 1500, 900, BF, '6+12Ar+6 Low-E DGU', 1, 'slidew'),
    ('W-05', 'High-level louvre', 'Powder, Laundry, Master 1 & 2 WC', 'L1/L2', 1200, 600, 1700, BF, '6mm acid-etched privacy', 4, 'louvre'),
    ('W-06', 'Casement window', 'Master 1 / Master 2 bedroom (side)', 'L2', 2000, 1500, 900, BF, '6+12Ar+6 Low-E DGU', 2, 'case2'),
    ('W-07', 'Sliding window', 'Master WIC (side)', 'L2', 1500, 1200, 1100, BF, '6+12Ar+6 Low-E frosted', 2, 'slidew'),
    ('W-08', 'Fixed ribbon window', 'Study Gallery (rear)', 'L2', 3000, 1200, 900, BF, '8+12Ar+8 Low-E laminated', 1, 'fix3'),
    ('W-09', 'Sliding window', 'Family Lounge (east)', 'L1', 2400, 1500, 900, BF, '6+12Ar+6 Low-E DGU', 1, 'slidew'),
    ('W-10', 'Sliding window', 'Dining Room (west)', 'L1', 1800, 1500, 900, BF, '6+12Ar+6 Low-E DGU', 1, 'slidew'),
]
CAMS = [
    ('C1', 'Garage portal / street frontage', 'Bullet 4MP IR', 'Vehicle + plate, street approach'),
    ('C2', 'Garage interior', 'Dome 4MP', '2 parking bays, door motion'),
    ('C3', 'Workshop', 'Dome 4MP', 'Tool bench + loft storage'),
    ('C4', 'Exterior stepped stair', 'Bullet 4MP IR', 'Stair flights + gate'),
    ('C5', 'Front garden + entry D-01', 'Turret 4MP', 'Entry door, face capture'),
    ('C6', 'West side passage (1.00m)', 'Bullet 4MP IR', 'Setback strip, 1.00m wide'),
    ('C7', 'East side passage (1.00m)', 'Bullet 4MP IR', 'Setback strip, 1.00m wide'),
    ('C8', 'Back garden + outdoor kitchen', 'Bullet 4MP IR', 'Rear boundary, pergola'),
    ('C9', 'Front balcony (L2)', 'Dome 4MP', 'Balcony + street view'),
    ('C10', 'Foyer / core lobby', 'Dome 4MP', 'Internal stair + lift'),
]
SC = 0.05  # px per mm
CSS = f'''*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1600px;height:1200px;overflow:hidden;background:{PAPER}}}
.sheet{{position:relative;width:1600px;height:1200px;overflow:hidden;background:{PAPER};font-family:{FONT};color:{INK}}}
.hdr{{position:absolute;left:0;top:0;width:1600px;height:92px;background:{INK};color:#fff;padding:14px 28px}}
.hdr .k{{font:600 11px {MONO};letter-spacing:.16em;color:#b9bbbf}}
.hdr h1{{font-size:27px;font-weight:800;margin-top:5px}}
.hdr .r{{position:absolute;right:28px;top:16px;text-align:right;font:500 11px/1.55 {MONO};color:#cfd0d3}}
.hdr .p{{position:absolute;left:0;bottom:0;height:5px;width:1600px;background:linear-gradient(90deg,{INK} 0 33%,{CH} 33% 66%,#fff 66%)}}
svg.draw{{position:absolute;left:0;top:0}}
.t{{position:absolute;left:28px;font:800 13px {FONT};letter-spacing:.05em}}
.t small{{font:500 9.5px {MONO};color:#6b6e74;margin-left:8px}}
.tb{{position:absolute;left:28px;top:668px;width:1040px}}
table{{border-collapse:collapse;width:100%;font:500 8.6px {MONO}}}
th{{background:{INK};color:#fff;text-align:left;padding:3px 5px;font-weight:700;white-space:nowrap}}
td{{padding:3.4px 5px;border-bottom:.5px solid {LT};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:330px}}
td.n,th.n{{text-align:right}}
tr.sub td{{background:{LT2};font-weight:800;letter-spacing:.06em}}
tr.tot td{{font-weight:800;border-top:1.2px solid {INK}}}
td.tg{{font-weight:800}}
.rp{{position:absolute;left:1092px;top:668px;width:480px}}
.rp h3{{font:800 12px {FONT};letter-spacing:.05em;margin:0 0 4px}}
.rp table{{font-size:8.4px}}
.rp ul{{margin:6px 0 0 14px;font:500 8.8px/1.5 {MONO}}}
.foot{{position:absolute;left:28px;right:28px;bottom:14px;height:56px;border:1.4px solid {INK};display:grid;grid-template-columns:1.2fr 1.6fr 1fr}}
.foot div{{padding:6px 12px;font:500 9.4px/1.5 {MONO}}} .foot div+div{{border-left:1px solid {INK}}}
'''


def frame_svg(item, x, base, kind):
    tg, nm, loc, lv, W, H, sill, frame, glz, qty, op = item
    w, h, sl = W * SC, H * SC, sill * SC
    y0 = base - sl - h
    o = [f'<g>']
    isdoor = kind == 'door'
    # wall opening context
    o.append(line(x - 14, base, x + w + 14, base, INK, 1.6))
    o.append(rect(x, y0, w, h, '#26272a' if op in ('garage', 'pivot', 'steel', 'double') else 'url(#glass)', None))
    dark = op in ('garage', 'pivot', 'steel', 'double')
    # leaves
    if op == 'garage':
        for i in range(1, 8): o.append(line(x, y0 + h * i / 8, x + w, y0 + h * i / 8, '#4a4c50', .8))
        o.append(f'<path d="M{f(x+w/2)},{f(y0+h*0.75)} v-{f(h*0.5)} m-5,7 l5,-7 l5,7" stroke="{ACC}" fill="none" stroke-width="1.2"/>')
        for i in range(3): o.append(rect(x + w * (0.12 + i * 0.3), y0 + h * 0.17, w * 0.2, 4, '#c8d2d8', None))
    elif op == 'pivot':
        o.append(line(x + w / 2, y0, x + w / 2, y0 + h, '#7a7d83', .8, '4 3'))
        o.append(f'<path d="M{f(x+w*0.25)},{f(y0+h*0.45)} a{f(w*0.25)},{f(w*0.25)} 0 0 1 {f(w*0.5)},0" stroke="{ACC}" fill="none" stroke-width="1.1"/>')
        o.append(rect(x + w * 0.44, y0 + h * 0.5, 2, h * 0.14, '#bdbfc3', None))
    elif op == 'steel':
        o.append(rect(x + 3, y0 + 3, w - 6, h - 6, 'none', '#55575b', .8)); o.append(circ(x + w - 7, y0 + h * 0.5, 1.8, '#bdbfc3', None, 0))
        o.append(text(x + w / 2, y0 + h * 0.3, 'EI60', 5, 'middle', 700, '#d0d0d0', MONO))
    elif op == 'double':
        o.append(line(x + w / 2, y0, x + w / 2, y0 + h, '#7a7d83', 1))
        o.append(text(x + w / 2, y0 + h * 0.35, '48 dB', 5, 'middle', 700, '#d0d0d0', MONO))
    elif op in ('swing',):
        o.append(rect(x, y0, w, h, WHT, None))
        o.append(f'<path d="M{f(x+w)},{f(y0)} L{f(x)},{f(y0+h/2)} L{f(x+w)},{f(y0+h)}" fill="none" stroke="{INK}" stroke-width=".7" stroke-dasharray="3 2"/>')
        o.append(circ(x + w - 5, y0 + h * 0.5, 1.6, INK, None, 0))
    elif op in ('lift4', 'slide2', 'slide3', 'slidew'):
        n = {'lift4': 4, 'slide2': 2, 'slide3': 3, 'slidew': 2}[op]
        for i in range(1, n): o.append(line(x + w * i / n, y0, x + w * i / n, y0 + h, BLK, 2))
        pw = w / n
        o.append(f'<path d="M{f(x+pw*0.2)},{f(y0+h*0.5)} h{f(pw*0.6)} m-5,-3 l5,3 l-5,3" fill="none" stroke="{ACC}" stroke-width="1.1"/>')
        if n > 2: o.append(f'<path d="M{f(x+w-pw*0.8)},{f(y0+h*0.5)} h{f(pw*0.6)} m5,-3 l-5,3 l5,3" fill="none" stroke="{ACC}" stroke-width="1.1"/>')
    elif op in ('case', 'case2'):
        n = 2 if op == 'case2' else 1
        pw = w / n
        for i in range(n):
            xx = x + i * pw
            o.append(f'<path d="M{f(xx+pw)},{f(y0)} L{f(xx)},{f(y0+h/2)} L{f(xx+pw)},{f(y0+h)}" fill="none" stroke="{INK}" stroke-width=".7" stroke-dasharray="3 2"/>')
            if i: o.append(line(xx, y0, xx, y0 + h, BLK, 2))
    elif op == 'louvre':
        for i in range(1, 6): o.append(line(x, y0 + h * i / 6, x + w, y0 + h * i / 6, '#7d8187', .8))
    elif op in ('fix3', 'fix'):
        n = 3 if op == 'fix3' else 1
        for i in range(1, n): o.append(line(x + w * i / n, y0, x + w * i / n, y0 + h, BLK, 2))
        o.append(line(x + 4, y0 + h - 5, x + 18, y0 + 5, '#fff', 1.2, None, 'opacity=".6"'))
        if op == 'fix3' and W > 5000:
            o.append(f'<path d="M{f(x+w*2/3)},{f(y0)} L{f(x+w)},{f(y0+h*0.5)} L{f(x+w*2/3)},{f(y0+h)}" fill="none" stroke="{INK}" stroke-width=".7" stroke-dasharray="3 2"/>')
    o.append(rect(x, y0, w, h, 'none', BLK, 3.2))
    # dims
    o.append(hdim(x, x + w, base + 14, f'{W}', base + 3, 7.4, INK, False, True))
    xr = x + w + 11
    o.append(vdim(xr, y0, y0 + h, f'{H}', x + w + 2, 7.4, INK, False, True))
    if sill:
        o.append(vdim(x - 9, y0 + h, base, f'{sill}', x - 2, 6.6, ACC, True))
        o.append(f'<text x="{f(x+w/2)}" y="{f(base-3)}" font-size="5.6" text-anchor="middle" fill="{ACC}" font-family="{MONO}" font-weight="700">SILL {sill}</text>')
    # tag + qty
    cx = x + w / 2
    o.append(tag(cx, y0 - 18, tg, 9))
    o.append(text(cx, y0 - 7, f'×{qty}', 7.4, 'middle', 700, ACC, MONO))
    o.append('</g>')
    return ''.join(o)


def row(items, base, kind, x0=36, x1=1564):
    total = sum(i[4] for i in items) * SC
    gap = (x1 - x0 - total) / (len(items) - 1)
    x = x0; out = ''
    for it in items:
        out += frame_svg(it, x, base, kind)
        x += it[4] * SC + gap
    return out


def trs(items, label):
    r = f'<tr class="sub"><td colspan="9">{label}</td></tr>'
    for it in items:
        tg, nm, loc, lv, W, H, sill, frame, glz, qty, op = it
        r += (f'<tr><td class="tg">{tg}</td><td>{esc(loc)} — {esc(nm)}</td><td>{lv}</td><td class="n">{W} × {H}</td>'
              f'<td class="n">{sill}</td><td>{esc(frame)}</td><td>{esc(glz)}</td><td class="n">{qty}</td></tr>')
    return r


def main(out):
    d = [DEFS]
    d.append(row(DOORS, 300, 'door'))
    d.append(row(WINS, 586, 'win', 60, 1540))
    # section rules
    d.append(line(28, 392, 1572, 392, INK, 1.2))
    dq = sum(i[9] for i in DOORS); wq = sum(i[9] for i in WINS)
    tab = (f'<table><tr><th>TAG</th><th>LOCATION / DESCRIPTION</th><th>LEVEL</th><th class="n">W × H (mm)</th><th class="n">SILL (mm)</th><th>FRAME FINISH</th><th>GLAZING SPEC</th><th class="n">QTY</th></tr>'
           + trs(DOORS, 'DOORS') + trs(WINS, 'WINDOWS')
           + f'<tr class="tot"><td colspan="7">TOTAL OPENINGS — {dq} DOORS + {wq} WINDOWS</td><td class="n">{dq + wq}</td></tr></table>')
    cam = ''.join(f'<tr><td class="tg">{a}</td><td>{b}</td><td>{c}</td><td>{d_}</td></tr>' for a, b, c, d_ in CAMS)
    rp = f'''<h3>LOW-VOLTAGE CCTV / NVR CAMERA COVERAGE MATRIX</h3>
<table><tr><th>ID</th><th>COVERAGE ZONE</th><th>CAMERA</th><th>VIEW</th></tr>{cam}</table>
<ul><li>NVR: 16-ch PoE 4K, 2×6TB HDD, 1500VA UPS — in Electrical/IT/CCTV/NVR Room 3.40×2.80 (L0)</li>
<li>Cat6A home-runs to patch panel; 10 cameras + 6 spare PoE ports; Wi-Fi 6 AP ×3 (L0/L1/L2)</li></ul>
<h3 style="margin-top:10px">DRAINAGE SUMMARY</h3>
<ul style="margin-top:2px"><li>5.00m retaining wall: 100mm weep holes @1.50m c/c + gravel filter + perimeter French drain</li>
<li>Garage portal: 5.20m stainless trench drain → oil interceptor → sump pump → street kerb</li>
<li>Front garden / terrace +5.00: 1:100 falls to channel drains, 110mm outlets ×3</li>
<li>Roofs (L2 + green roof): internal 110mm downpipes ×4, overflow scuppers 50mm</li>
<li>Back garden: 1:80 fall to rear catch-pit; outdoor kitchen grease trap</li></ul>'''
    html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>DOC 03 — Doors &amp; Windows Schedule · Contest #2799843</title>
<style>{CSS}</style></head><body><div class="sheet">
<div class="hdr"><div class="k">DOC 03 / 03 · CONTEST #2799843 · TWO-STOREY MODERN CONTEMPORARY HOUSE</div>
<h1>DOORS &amp; WINDOWS MEASUREMENT SCHEDULE + MEP / CCTV MATRIX</h1>
<div class="r">BLACK THERMALLY-BROKEN ALUMINIUM FRAMES · ALL SIZES IN mm<br>OPENING ARROWS: RED = SLIDE / LIFT · DASHED V = SWING (APEX AT HINGE)<br>SILL = FINISHED FLOOR TO FRAME BOTTOM</div><div class="p"></div></div>
<div class="t" style="top:102px">DOORS — GD-01, D-01 … D-08<small>measured elevations, scale 1 : 20 on sheet · tag · quantity</small></div>
<div class="t" style="top:402px">WINDOWS — W-01 … W-10<small>width × height · sill height · opening type</small></div>
<svg class="draw" width="1600" height="1200" viewBox="0 0 1600 1200" xmlns="http://www.w3.org/2000/svg">{"".join(d)}</svg>
<div class="tb">{tab}</div>
<div class="rp">{rp}</div>
<div class="foot"><div><b>SHEET 03 / 03</b> · 2026-11-08<br>Plot 18.78m × 22.00m · +5.00m elevation</div>
<div><b>NOTES</b> Tags cross-reference DOC 02 plans (D / W / GD tags) · all glazing U ≤ 1.6 W/m²K · safety glass to all openings below 800mm · garage door 5.20 × 2.40 within 5.60m portal in retaining wall</div>
<div><b>PALETTE</b> Black · Charcoal grey · Crisp white</div></div>
</div></body></html>'''
    open(out, 'w', encoding='utf-8').write(html)


if __name__ == '__main__':
    main(sys.argv[1])
