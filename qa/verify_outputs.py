"""Geometry connectivity, vector output, and byte-repeatability checks."""
from pathlib import Path
import importlib.util, sys, collections, subprocess, hashlib, json
import fitz
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('house_builder',ROOT/'build_cad_2799843.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)

def connected(level):
 # Test architectural circulation through actual wall openings, with windows closed.
 step=50
 boxes=[]
 for w in m.WALLS[level]:
  gaps=[(o.start,o.start+m.TYPES[o.code][0]) for o in m.OPEN if o.level==level and o.wall==w.id and not o.code.startswith('W')]
  gaps += [(s,s+n) for s,n in m.PASSAGES.get((level,w.id),[])]
  cur=w.a
  for a,b in sorted(gaps)+[(w.b,w.b)]:
   if a>cur:
    boxes.append((cur,w.c-w.t/2,a,w.c+w.t/2) if w.axis=='h' else (w.c-w.t/2,cur,w.c+w.t/2,a))
   cur=b
 bounds=(1000,0,11400,11400) if level==0 else (1000,4500,17780,18500)
 x0,y0,x1,y1=bounds
 def grid(x,y):return (round((x-x0)/step),round((y-y0)/step))
 maxx,maxy=grid(x1,y1)
 blocked=set()
 for a,b,c,d in boxes:
  ia,ib=grid(a-step,b-step);ic,id=grid(c+step,d+step)
  for i in range(max(0,ia),min(maxx,ic)+1):
   for j in range(max(0,ib),min(maxy,id)+1):
    x=x0+i*step;y=y0+j*step
    if a<=x<=c and b<=y<=d:blocked.add((i,j))
 start=grid(10500,1500 if level==0 else 7000)
 seen={start};q=collections.deque([start])
 while q:
  i,j=q.popleft()
  for ij in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
   if 0<=ij[0]<=maxx and 0<=ij[1]<=maxy and ij not in blocked and ij not in seen:seen.add(ij);q.append(ij)
 anchors={0:{'garage':(4000,3000),'repair':(2500,8500),'electrical':(5500,8500),'stair landing':(8000,5200)},
  1:{'stair landing':(8000,5200),'living':(4000,8000),'dining':(4000,12500),'kitchen':(4000,16000),'pantry':(9000,16000),'laundry':(10000,13000),'guest WC':(7800,13000),'guest bedroom':(14000,8000),'guest ensuite':(16500,8500),'entertainment':(14000,15000)},
  2:{'stair landing':(8000,5200),'master A':(4000,9000),'master B':(14000,9000),'closet A':(2500,15000),'closet B':(16000,15000),'vanity A':(5600,14000),'vanity B':(12500,14000),'WC A':(4600,16500),'shower A':(6000,16500),'WC B':(12200,16500),'shower B':(13800,16500),'terrace':(9000,15000)}}[level]
 unreachable=[name for name,p in anchors.items() if grid(*p) not in seen]
 assert not unreachable,(level,unreachable)
 return list(anchors)

circulation={f'L{l}':connected(l) for l in range(3)}
files=list((ROOT/'exports').glob('*'))+list(ROOT.glob('board*-codex.html'))+list((ROOT/'assets/cad').glob('*.svg'))
def digest():return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file()}
a=digest();subprocess.run([sys.executable,str(ROOT/'build_cad_2799843.py')],cwd=ROOT,check=True,capture_output=True);b=digest()
assert a==b, [p for p in a if a[p]!=b[p]]
# The drawing PDF must contain vector geometry and searchable annotations, not raster pages.
doc=fitz.open(ROOT/'exports/Modern_House_18.78x22m_Full_Drawing_Set.pdf')
assert all(not p.get_images() for p in doc)
clip=[]
for i,p in enumerate(doc):
 for b in p.get_text('dict')['blocks']:
  for ln in b.get('lines',[]):
   for span in ln['spans']:
    r=fitz.Rect(span['bbox'])
    if not p.rect.contains(r):clip.append((i+1,span['text']))
assert not clip,clip
report={'circulation_reachable_rooms':circulation,'rebuild_sha256_identical':True,'hashed_artifacts':len(a),'pdf_raster_images':0,'pdf_text_outside_page':0,'sha256':a}
(ROOT/'qa/verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='sha256'},indent=2))
