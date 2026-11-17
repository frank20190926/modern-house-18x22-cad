import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from kit import *
from elev import *

CSS = f'''*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1600px;height:1200px;overflow:hidden;background:{PAPER}}}
.sheet{{position:relative;width:1600px;height:1200px;overflow:hidden;background:{PAPER};font-family:{FONT};color:{INK}}}
.hdr{{position:absolute;left:0;top:0;width:1600px;height:92px;background:{INK};color:#fff;padding:14px 28px}}
.hdr .k{{font:600 11px {MONO};letter-spacing:.16em;color:#b9bbbf}}
.hdr h1{{font-size:28px;font-weight:800;margin-top:5px;letter-spacing:.01em}}
.hdr .r{{position:absolute;right:28px;top:16px;text-align:right;font:500 11px/1.55 {MONO};color:#cfd0d3}}
.hdr .p{{position:absolute;left:0;bottom:0;height:5px;width:1600px;background:linear-gradient(90deg,{INK} 0 33%,{CH} 33% 66%,#fff 66%)}}
svg.draw{{position:absolute;left:0;top:0}}
.hero{{position:absolute;left:28px;top:132px;width:742px;height:414px;border:1.4px solid {INK};background:url(assets/front-elevation-5m.jpg) center/cover}}
.hero .cap{{position:absolute;left:0;bottom:0;background:{INK};color:#fff;font:700 10px {MONO};padding:5px 10px;letter-spacing:.06em}}
.hero .cap2{{position:absolute;right:0;top:0;background:#fff;color:{INK};font:700 10px {MONO};padding:5px 10px;border-left:1.4px solid {INK};border-bottom:1.4px solid {INK}}}
.t{{position:absolute;font:800 13px {FONT};letter-spacing:.04em}}
.t small{{font:500 9.5px {MONO};color:#6b6e74;margin-left:8px;letter-spacing:.03em}}
.vr{{position:absolute;left:792px;top:100px;width:1.4px;height:1090px;background:{INK}}}
.key{{position:absolute;left:1418px;top:132px;width:160px;font:500 9px/1.5 {MONO};border:1px solid {INK};padding:8px 10px}}
.key b{{font-weight:800}}
.sw{{display:inline-block;width:11px;height:11px;border:1px solid {INK};vertical-align:-2px;margin-right:5px}}
.notes{{position:absolute;left:28px;top:1066px;width:742px;font:500 9.4px/1.55 {MONO};border-top:1px solid {INK};padding-top:6px}}
.legend{{position:absolute;left:28px;top:1138px;width:742px;height:48px;border:1.4px solid {INK};display:grid;grid-template-columns:1fr 1fr 1fr}}
.legend div{{padding:6px 10px;font:500 9px/1.45 {MONO}}} .legend div+div{{border-left:1px solid {INK}}}
'''


def main(out):
    d = [DEFS]
    # right column elevations
    d.append(front(910, 424, 24, False))
    d.append(front(910, 784, 24, True))
    d.append(side(880, 1090, 15, True))
    d.append(side(1236, 1090, 15, False))
    # section (left)
    d.append(section(86, 952, 29))
    svg = f'<svg class="draw" width="1600" height="1200" viewBox="0 0 1600 1200" xmlns="http://www.w3.org/2000/svg">{"".join(d)}</svg>'
    html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>DOC 01 — Elevations &amp; Section · Contest #2799843</title>
<style>{CSS}</style></head><body><div class="sheet">
<div class="hdr"><div class="k">DOC 01 / 03 · CONTEST #2799843 · TWO-STOREY MODERN CONTEMPORARY HOUSE</div>
<h1>FRONT, REAR &amp; SIDE ELEVATIONS + 5.00M SLOPE SECTION</h1>
<div class="r">BLACK / CHARCOAL GREY / CRISP WHITE CONTEMPORARY PALETTE<br>18.78m × 22.00m PLOT • +5.00m ELEVATION • 5.00m CUT-IN GARAGE<br>ALL DIMENSIONS IN METRES</div><div class="p"></div></div>
<div class="hero"><div class="cap">FRONT ELEVATION · PHOTOREAL — HOUSE PERCHED +5.00m ABOVE STREET</div><div class="cap2">HERO</div></div>
<div class="t" style="left:28px;top:560px">SECTION A–A — LONGITUDINAL THROUGH GARAGE, WORKSHOP &amp; NVR ROOM<small>cut x = 11.00m</small></div>
<div class="t" style="left:820px;top:104px">FRONT ELEVATION (SOUTH)<small>facade 16.78m · setbacks 1.00m L/R</small></div>
<div class="t" style="left:820px;top:478px">REAR ELEVATION (NORTH)<small>rear garden · outdoor kitchen pergola · panoramic sliders</small></div>
<div class="t" style="left:820px;top:846px">LEFT SIDE ELEVATION (WEST)<small>5.00m wall</small></div>
<div class="t" style="left:1176px;top:846px">RIGHT SIDE ELEVATION (EAST)<small>stepped planters</small></div>
<div class="vr"></div>
<div class="key"><b>MATERIAL KEY</b><br><span class="sw" style="background:{CH}"></span>Board-formed charcoal retaining wall<br><span class="sw" style="background:{INK}"></span>Black fins / aluminium frames<br><span class="sw" style="background:#fff"></span>Crisp white render &amp; parapet<br><span class="sw" style="background:#8f9297"></span>Grey stone cladding<br><span class="sw" style="background:{GL}"></span>Low-E glazing / glass balustrade<br><br><b>HEIGHTS</b><br>±0.00 street · +5.00 Level 1<br>+8.40 Level 2 · +11.80 parapet</div>
<div class="notes"><b>SECTION NOTES</b> · L0 clear 4.40m (slab 4.40–4.70, topping to +5.00) · L1 clear 3.00m (slab 8.00–8.40) · L2 clear 2.60m (roof slab 11.00–11.30, parapet to +11.80) · garage portal 5.20×2.40 in 5.00m board-formed retaining wall · weep holes + trench drain at portal · sump pump in NVR-side utility chase</div>
<div class="legend"><div><b>SECTION KEY</b><br>Garage 6.50×6.50 · rear workshop 6.50×4.20 · NVR room 3.40×2.80</div><div><b>VERTICAL CIRCULATION</b><br>Internal stair + lift core · exterior stepped stair 28 risers @178.6 = +5.00</div><div><b>SHEET 01 / 03</b> · 2026-11-08<br>Grey dashed = elements beyond cut plane</div></div>
{svg}
</div></body></html>'''
    open(out, 'w', encoding='utf-8').write(html)


if __name__ == '__main__':
    main(sys.argv[1])
