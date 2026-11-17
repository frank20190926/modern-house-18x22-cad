import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from kit import *
from plans import *

CSS = f'''*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1600px;height:1200px;overflow:hidden;background:{PAPER}}}
.sheet{{position:relative;width:1600px;height:1200px;overflow:hidden;background:{PAPER};font-family:{FONT};color:{INK}}}
.hdr{{position:absolute;left:0;top:0;width:1600px;height:92px;background:{INK};color:#fff;padding:14px 28px}}
.hdr .k{{font:600 11px {MONO};letter-spacing:.16em;color:#b9bbbf}}
.hdr h1{{font-size:30px;font-weight:800;letter-spacing:.01em;margin-top:5px}}
.hdr .r{{position:absolute;right:28px;top:16px;text-align:right;font:500 11px/1.55 {MONO};color:#cfd0d3}}
.hdr .p{{position:absolute;left:0;bottom:0;height:5px;width:1600px;background:linear-gradient(90deg,{INK} 0 33%,{CH} 33% 66%,#fff 66%)}}
svg.draw{{position:absolute;left:0;top:0}}
.pt{{position:absolute;top:108px;font:800 14px {FONT};letter-spacing:.04em;width:500px}}
.pt small{{display:block;font:500 10px {MONO};color:#6b6e74;letter-spacing:.04em;margin-top:2px}}
.tbl{{position:absolute;top:790px;width:490px}}
table{{border-collapse:collapse;width:100%;font:500 9.4px {MONO}}}
th{{background:{INK};color:#fff;text-align:left;padding:3px 5px;font-weight:700}}
td{{padding:2.4px 5px;border-bottom:.5px solid {LT}}}
td.n,th.n{{text-align:right;white-space:nowrap}}
tr.tot td{{font-weight:800;border-top:1.2px solid {INK}}}
.foot{{position:absolute;left:28px;right:28px;bottom:16px;height:92px;border:1.4px solid {INK};display:grid;grid-template-columns:1.25fr 1.45fr 1fr}}
.foot div{{padding:8px 12px;font:500 10px/1.5 {MONO}}}
.foot div+div{{border-left:1px solid {INK}}}
.foot b{{font-weight:800}}
'''


def tbl(level, idx, title, sub):
    rooms = {0: L0, 1: L1 + L1_OUT, 2: L2}[level]
    tot = sum(area(r) for r in rooms)
    rows = ''.join(f'<tr><td>{esc(r[5])}</td><td class="n">{r[6]}</td><td class="n">{area(r):.1f}</td></tr>' for r in rooms)
    rows += f'<tr class="tot"><td>TOTAL LISTED ROOM AREA</td><td class="n"></td><td class="n">{tot:.1f} m²</td></tr>'
    left = OXS[idx] - 50
    return f'<div class="tbl" style="left:{left}px"><table><tr><th>ROOM</th><th class="n">W × D (m)</th><th class="n">m²</th></tr>{rows}</table></div>'


def main(out):
    draws = HATCH_DEFS + ''.join(plan(l, i) for i, l in enumerate((0, 1, 2)))
    titles = [('PLAN A: LEVEL 0 — STREET-LEVEL SUBTERRANEAN BASE (±0.00m)', 'Cut into 5.00m front embankment · clear height 4.40m · slab top +5.00m'),
              ('PLAN B: LEVEL 1 — MAIN GROUND FLOOR (+5.00m)', 'Front garden 4.20m · house 13.80m · back garden 4.00m · clear 3.00m'),
              ('PLAN C: LEVEL 2 — UPPER FLOOR (+8.40m)', 'Two master suites · front cantilevered glass balcony · clear 2.60m')]
    pts = ''.join(f'<div class="pt" style="left:{OXS[i] - 50}px">{t}<small>{s}</small></div>' for i, (t, s) in enumerate(titles))
    tbls = ''.join(tbl(l, i, *titles[i]) for i, l in enumerate((0, 1, 2)))
    html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>DOC 02 — Floor Plans · Contest #2799843</title>
<style>{CSS}</style></head><body><div class="sheet">
<div class="hdr"><div class="k">DOC 02 / 03 · CONTEST #2799843 · TWO-STOREY MODERN CONTEMPORARY HOUSE</div>
<h1>FLOOR PLANS WITH FULL MEASUREMENTS — LEVEL 0, LEVEL 1 &amp; LEVEL 2</h1>
<div class="r">BLACK / CHARCOAL GREY / CRISP WHITE<br>PLOT 18.78m × 22.00m · SETBACKS 1.00m L/R · +5.00m ELEVATION<br>ALL DIMENSIONS IN METRES · NORTH ↑ · STREET AT BOTTOM</div><div class="p"></div></div>
<svg class="draw" width="1600" height="1200" viewBox="0 0 1600 1200" xmlns="http://www.w3.org/2000/svg">{draws}</svg>
{pts}{tbls}
<div class="foot">
<div><b>LEGEND</b><br>▬ 300mm external wall · thin line 120mm partition<br>Tags: GD garage door · D door · W window (see DOC 03)<br>Red = overall / key dimensions · A–A = section line (DOC 01)</div>
<div><b>KEY COMPLIANCE</b><br>Master 1 &amp; 2: separate enclosed WC 1.40×1.80, separate enclosed shower 1.60×1.80, dual vanity 2.80m with 2 washbasins<br>Garage 6.50×6.50 · workshop 6.50×4.20 · electrical/IT/CCTV/NVR room 3.40×2.80</div>
<div><b>SHEET 02 / 03</b><br>Scale ≈ 1:100 on 1600×1200 sheet<br>Issue date 2026-11-08<br>Net floor areas are room-internal W×D</div></div>
</div></body></html>'''
    open(out, 'w', encoding='utf-8').write(html)


if __name__ == '__main__':
    main(sys.argv[1])
