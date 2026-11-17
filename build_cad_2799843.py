#!/usr/bin/env python3
"""Deterministic concept architectural set, contest 2799843.
Python dependencies already on this workstation: ezdxf, PyMuPDF, matplotlib, Pillow.
Coordinates and DXF model space are millimetres; shared geometry drives PDF/SVG/DXF.
Run: python3 build_cad_2799843.py
"""
from pathlib import Path
from dataclasses import dataclass
from collections import Counter, OrderedDict
import json, math, html, zipfile, hashlib
import ezdxf
from ezdxf.enums import TextEntityAlignment
import fitz
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'exports'; OUT.mkdir(exist_ok=True)
QA=ROOT/'qa'; QA.mkdir(exist_ok=True)
DRAW=ROOT/'assets'/'cad'; DRAW.mkdir(exist_ok=True)
BLACK='#202426'; MID='#5b6265'; LIGHT='#e3e7e8'; FAINT='#f1f3f3'; GREEN='#dce4dd'
FONT=FontProperties(family='DejaVu Sans')
TYPES={
 'GD1':(5000,2600,0,'Sectional insulated steel','Garage'),
 'D1':(1400,2400,0,'Pivot / solid insulated leaf','Main entrance'),
 'D2':(1000,2400,0,'Solid-core acoustic hinged','Bedrooms / entertainment'),
 'D3':(800,2200,0,'Moisture-resistant hinged','WC / guest bath'),
 'D4':(800,2200,0,'10 mm toughened safety glass','Separate shower'),
 'D5':(900,2200,0,'Solid-core hinged','Pantry / storage'),
 'D6':(900,2200,0,'Self-closing service door*','Service / stair / kitchen exit'),
 'D7':(3000,2400,0,'3-panel aluminium slider / G1','Garden / terrace'),
 'D8':(1000,2400,0,'Insulated security hinged','Street pedestrian entrance'),
 'W1':(3600,2400,300,'Fixed + casement / G1','Living front'),
 'W2':(2400,1800,600,'Casement + fixed / G1','Guest bedroom'),
 'W3':(2400,1500,900,'Casement + fixed / G1','Dining'),
 'W4':(2400,1200,1200,'Awning + fixed / G1','Indoor kitchen'),
 'W5':(3000,1800,600,'Fixed + casement / G1','Entertainment'),
 'W6':(3000,2100,300,'Fixed + casement / G1','Master sleeping areas'),
 'W7':(1200,1200,1200,'Awning / G2 privacy','Walk-in closets'),
 'W8':(600,900,1500,'Awning / G2 privacy','Separate WC / guest bath'),
 'W9':(900,900,1500,'Awning / G2 privacy','Separate shower'),
 'W10':(1200,1200,1200,'Awning / G1','Street lobby / pantry'),
}
@dataclass
class Wall:
 id:str; axis:str; c:float; a:float; b:float; t:float=150
@dataclass
class Opening:
 level:int; wall:str; code:str; start:float; room:str; flip:int=1
OPEN=[]
WALLS={}
def op(l,w,c,s,r,flip=1): OPEN.append(Opening(l,w,c,s,r,flip))
def envelope(l,x1,y1,x2,y2):
 WALLS[l]=[Wall('F','h',y1+100,x1,x2,200),Wall('B','h',y2-100,x1,x2,200),Wall('L','v',x1+100,y1,y2,200),Wall('R','v',x2-100,y1,y2,200)]
def wa(l,id,axis,c,a,b,t=150): WALLS[l].append(Wall(id,axis,c,a,b,t))
# Baseline: front is y=0; x=0 is the left site boundary looking into the plot.
envelope(0,1000,0,11400,11400)
wa(0,'G','v',6800,200,11200); wa(0,'C','v',9600,4500,11200)
wa(0,'S','h',6600,1200,6800); wa(0,'E','v',4300,6600,11200)
wa(0,'ST','h',4500,6800,9600)
op(0,'F','GD1',1400,'Two-car garage'); op(0,'F','D8',10000,'Street lobby')
op(0,'F','W10',7300,'Street lobby');op(0,'G','D6',2300,'Garage to protected lobby',-1)
op(0,'S','D5',2000,'Rear storage / car repair');op(0,'S','D6',5000,'Electrical / IT / CCTV / NVR')
op(0,'ST','D6',7200,'Protected stair enclosure')
# Main floor.
envelope(1,1000,4500,17780,18500)
for c,id in [(6800,'A'),(11400,'BAY')]: wa(1,id,'v',c,4700,18300)
wa(1,'CORE','v',9600,4700,10000)
wa(1,'H1L','h',10000,1200,6800);wa(1,'H1R','h',10000,11400,17580)
wa(1,'H2L','h',11400,1200,6800);wa(1,'H2C','h',11400,6800,11400);wa(1,'H2R','h',11400,11400,17580)
wa(1,'SERV','h',14200,6800,11400);wa(1,'SPL','v',8700,11400,14200)
wa(1,'BATHV','v',15780,7300,10000);wa(1,'BATHH','h',7300,15780,17580)
op(1,'F','D1',9800,'Main entrance');op(1,'F','W1',2100,'Living');op(1,'F','W2',12300,'Guest suite')
op(1,'H1R','D2',11900,'Guest suite',-1);op(1,'H2R','D2',12000,'Entertainment')
op(1,'CORE','D6',4800,'Stair to main-floor hall')
op(1,'B','D6',5400,'Kitchen to rear garden')
op(1,'H2C','D3',7300,'Guest toilet');op(1,'H2C','D6',9600,'Laundry')
op(1,'A','D5',15900,'Pantry from kitchen');op(1,'BATHV','D3',8500,'Guest ensuite')
op(1,'B','D7',12600,'Entertainment to back garden');op(1,'B','W4',2300,'Indoor kitchen');op(1,'B','W10',8500,'Pantry')
op(1,'L','W3',11900,'Dining');op(1,'R','W5',13200,'Entertainment');op(1,'R','W8',8500,'Guest ensuite')
# Open passages between public zones are separately dimensioned, not door types.
PASSAGES={(1,'H1L'):[(4200,2000)],(1,'H2L'):[(4200,2000)],(1,'A'):[(10100,1100)],(1,'BAY'):[(10100,1100)]}
# Upper floor: two self-contained suites separated by the circulation core.
envelope(2,1000,4500,17780,18500)
wa(2,'A','v',6800,4700,18300);wa(2,'BAY','v',11400,4700,18300)
wa(2,'CORE','v',9600,4700,10000);wa(2,'TERR','h',11400,6800,11400)
for side,x0,x1,split,mid in [('A',1200,6800,3900,5350),('B',11400,17580,14580,12990)]:
 wa(2,side+'CL','v',split,13000,18300)
 wa(2,side+'CH','h',13000,x0,x1)
 vx0,vx1=(3900,6800) if side=='A' else (11400,14580)
 wa(2,side+'WET','h',15600,vx0,vx1);wa(2,side+'DIV','v',mid,15600,18300)
 op(2,side+'CH','D5',1800 if side=='A' else 15600,'Master '+side+' walk-in closet',-1)
 op(2,side+'WET','D3',4200 if side=='A' else 11700,'Master '+side+' separate WC')
 op(2,side+'WET','D4',5600 if side=='A' else 13300,'Master '+side+' separate shower')
 PASSAGES[(2,side+'CH')]=[(4800 if side=='A' else 11900,1800)]
op(2,'A','D2',10200,'Master A suite');op(2,'BAY','D2',10200,'Master B suite',-1);op(2,'TERR','D7',7500,'Shared roof terrace')
op(2,'CORE','D6',4800,'Stair to upper-floor hall')
op(2,'F','W6',2200,'Master A');op(2,'F','W6',12800,'Master B')
op(2,'L','W6',6500,'Master A side');op(2,'R','W6',6500,'Master B side')
op(2,'B','W7',2000,'Master A closet');op(2,'B','W8',4250,'Master A WC');op(2,'B','W9',5600,'Master A shower')
op(2,'B','W8',11750,'Master B WC');op(2,'B','W9',13250,'Master B shower');op(2,'B','W7',15600,'Master B closet')
# Rear middle is an open roof terrace. Back parapet is 1100 high, side privacy screens 1800.

class Drawing:
 def __init__(self,name,bounds): self.name=name;self.bounds=bounds;self.items=[];self.dims=[]
 def line(self,x1,y1,x2,y2,layer='DETAIL',color=MID,width=15,dash=False): self.items.append(('line',(x1,y1,x2,y2),layer,color,width,dash))
 def poly(self,pts,layer='WALL',fill=None,color=BLACK,width=20,close=True): self.items.append(('poly',pts,layer,color,width,fill,close))
 def rect(self,x,y,w,h,layer='DETAIL',fill=None,color=MID,width=15): self.poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],layer,fill,color,width)
 def text(self,x,y,s,size=160,layer='TEXT',color=BLACK,align='center',rotation=0): size=max(size,170); self.items.append(('text',(x,y,str(s),size,align,rotation),layer,color))
 def circle(self,x,y,r,layer='FURN',color=MID,width=12):
  self.poly([(x+r*math.cos(a*math.pi/24),y+r*math.sin(a*math.pi/24)) for a in range(48)],layer,None,color,width)
 def arc(self,x,y,r,start,end,layer='DOOR'):
  self.poly([(x+r*math.cos(math.radians(start+(end-start)*i/24)),y+r*math.sin(math.radians(start+(end-start)*i/24))) for i in range(25)],layer,None,MID,12,False)
 def dim(self,a,b,offset,axis='h',label=None):
  # Native DXF DIMENSION + equivalent vector drafting representation.
  val=abs(b[0]-a[0]) if axis=='h' else abs(b[1]-a[1]);lab=label or f'{val:,.0f}'
  self.dims.append((a,b,offset,axis,lab))
  if axis=='h':
   for x,y in [a,b]: self.line(x,y,x,offset+90,'DIM',MID,9)
   self.line(a[0],offset,b[0],offset,'DIM',MID,9)
   for x in [a[0],b[0]]:self.line(x-65,offset-65,x+65,offset+65,'DIM',BLACK,16)
   self.text((a[0]+b[0])/2,offset+95,lab,220,'DIM')
  else:
   for x,y in [a,b]:self.line(x,y,offset-90,y,'DIM',MID,9)
   self.line(offset,a[1],offset,b[1],'DIM',MID,9)
   for y in [a[1],b[1]]:self.line(offset-65,y-65,offset+65,y+65,'DIM',BLACK,16)
   self.text(offset-115,(a[1]+b[1])/2,lab,220,'DIM',rotation=90)
 def room(self,x,y,title,sub='',size=170):
  self.text(x,y,title,max(size,190))
  if sub:self.text(x,y-270,sub,135,color=MID)

def getwall(o):return next(w for w in WALLS[o.level] if w.id==o.wall)
def draw_walls(d,l):
 for w in WALLS[l]:
  gaps=[(o.start,o.start+TYPES[o.code][0]) for o in OPEN if o.level==l and o.wall==w.id]+[(s,s+n) for s,n in PASSAGES.get((l,w.id),[])]
  p=w.a
  for a,b in sorted(gaps)+[(w.b,w.b)]:
   if a>p:
    if w.axis=='h':d.rect(p,w.c-w.t/2,a-p,w.t,'WALL',BLACK,BLACK,5)
    else:d.rect(w.c-w.t/2,p,w.t,a-p,'WALL',BLACK,BLACK,5)
   p=b
 for o in [o for o in OPEN if o.level==l]:
  w=getwall(o);a=o.start;b=a+TYPES[o.code][0];iswin=o.code.startswith('W');is_slide=o.code in ['GD1','D7']
  if w.axis=='h':
   if iswin or is_slide:
    for dy in [-50,0,50]:d.line(a,w.c+dy,b,w.c+dy,'WINDOW' if iswin else 'DOOR',BLACK,12)
    for x in [a,b,(a+b)/2]:d.line(x,w.c-90,x,w.c+90,'WINDOW',BLACK,12)
   else:
    d.line(a,w.c,a,w.c+o.flip*(b-a),'DOOR',BLACK,14);d.arc(a,w.c,b-a,0,90*o.flip)
   d.text((a+b)/2,w.c-310,o.code,145,'TAG')
  else:
   if iswin or is_slide:
    for dx in [-50,0,50]:d.line(w.c+dx,a,w.c+dx,b,'WINDOW' if iswin else 'DOOR',BLACK,12)
    for y in [a,b,(a+b)/2]:d.line(w.c-90,y,w.c+90,y,'WINDOW',BLACK,12)
   else:
    d.line(w.c,a,w.c-o.flip*(b-a),a,'DOOR',BLACK,14);d.arc(w.c,a,b-a,90,180 if o.flip>0 else 0)
   d.text(w.c+270,(a+b)/2,o.code,145,'TAG',rotation=90)

def bed(d,x,y,w=1800,h=2000):
 d.rect(x,y,w,h,'FURN',FAINT,width=12);d.rect(x+100,y+h-550,w/2-150,400,'FURN');d.rect(x+w/2+50,y+h-550,w/2-150,400,'FURN')
 d.line(x,y+500,x+w,y+500,'FURN');d.rect(x-450,y+h-500,350,450,'FURN');d.rect(x+w+100,y+h-500,350,450,'FURN')
def basin(d,x,y):d.rect(x-260,y-180,520,360,'FURN');d.circle(x,y,100)
def wc(d,x,y):d.rect(x-210,y,420,500,'FURN');d.circle(x,y,200)
def shower(d,x,y,w=1000,h=1100):d.rect(x,y,w,h,'FURN');d.line(x,y,x+w,y+h,'FURN');d.line(x+w,y,x,y+h,'FURN');d.circle(x+w/2,y+h/2,35)
def stairs(d,l):
 # 1200 clear flights, 150 centre well. 30 x 166.667 or 20 x 170 risers.
 x=6975;y=5900;n=15 if l==0 else 10;run=(n-1)*280
 for xx in [x,x+1350]:
  d.rect(xx,y,1200,run,'STAIR')
  for i in range(n):d.line(xx,y+i*280,xx+1200,y+i*280,'STAIR',MID,12)
  d.line(xx+600,y+250,xx+600,y+run-180,'STAIR',BLACK,18)
 d.poly([(x+480,y+run-400),(x+600,y+run-100),(x+720,y+run-400)],'STAIR',None,BLACK,18,False)
 d.rect(x,y+run,2550,1200,'STAIR')
 d.text(x+600,y-400,'UP' if l<2 else 'DN',180)
 d.text(x+1900,y-400,'30R' if l==0 else '20R',150)
 # Centre labels outside treads.
 d.text(10450,7600,'ENTRY / HALL',150,rotation=90)

def landscape(d):
 d.rect(0,0,18780,22000,'SITE',None,MID,20)
 for x in [1000,17780]:d.line(x,0,x,22000,'SETBACK',MID,10,True)
 d.rect(1200,1000,4900,2800,'GARDEN',GREEN,GREEN,8)
 d.rect(11900,1000,5600,2800,'GARDEN',GREEN,GREEN,8)
 d.text(3650,2400,'FRONT GARDEN',210);d.text(14500,2400,'FRONT GARDEN',210)
 d.text(9400,-1550,'FRONT STREET  /  +/-0.00 m',230)
 d.text(17200,21000,'BACK GARDEN',185,align='right')
 for x,y in [(1700,1700),(5600,3100),(16600,1700),(12300,3050),(16500,20400),(14300,20800)]:
  d.circle(x,y,400,'GARDEN','#88988b',15);d.circle(x,y,290,'GARDEN','#88988b',9)
 d.rect(1200,21100,5400,700,'FURN',LIGHT);d.rect(1700,21200,1000,500,'FURN');basin(d,5200,21450)
 d.rect(1000,19500,5800,2500,'CANOPY',None,MID,12)
 d.text(3900,20300,'OUTDOOR KITCHEN',185);d.text(3900,19980,'5,800 x 2,500 covered zone',140)
 d.text(9400,21750,'REAR BOUNDARY',150)

def plan(l):
 d=Drawing('L'+str(l),(-1900,-2200,20800,23800))
 if l==1:landscape(d)
 else:
  d.rect(0,0,18780,22000,'SITE',None,MID,16)
  for x in [1000,17780]:d.line(x,0,x,22000,'SETBACK',MID,9,True)
  d.text(9400,-1550,'FRONT STREET  /  +/-0.00 m',230)
 if l==0:
  d.rect(1200,200,5400,6200,'ZONE',FAINT,FAINT)
  for x in [1450,4150]:
   d.rect(x,700,2350,5300,'BAY',None,MID,12)
   d.rect(x+280,1100,1800,4400,'FURN',LIGHT,MID,16)
   d.rect(x+400,1800,1560,950,'FURN');d.rect(x+400,4300,1560,650,'FURN')
  d.room(3900,6200,'2-CAR COVERED GARAGE','5,525 x 6,325 clear',200)
  d.room(2700,9200,'STORAGE / REPAIR','3,025 x 4,525 clear')
  d.rect(1400,10400,2300,600,'FURN',LIGHT);d.text(2500,10700,'WORKBENCH',140)
  d.room(5500,9700,'ELECTRICAL / IT','2,350 x 4,525 clear',150)
  d.text(5500,9050,'CCTV / NVR / UPS',150)
  d.rect(4700,10400,600,600,'FURN',LIGHT);d.rect(5700,10400,600,600,'FURN',LIGHT)
  d.text(5500,8200,'FRONT DUCTS',140)
  d.room(8150,2700,'STREET LOBBY','Protected access',150)
  d.text(14500,8000,'UNEXCAVATED GROUND',220)
  d.text(14500,7500,'Main house / garden above',170,color=MID)
  d.text(9400,20000,'PLOT BOUNDARY ABOVE',220,color=MID)
  stairs(d,0)
 elif l==1:
  d.room(3900,7900,'LIVING','5,525 x 5,225 clear',220)
  d.rect(1600,5400,900,2200,'FURN',LIGHT);d.rect(2600,5400,2300,900,'FURN',LIGHT);d.rect(3000,6700,1200,650,'FURN')
  d.room(3900,14200,'DINING','5,525 x 3,225 zone',210)
  d.rect(2500,12000,2400,1000,'FURN',LIGHT)
  for xx in [2700,3500,4300]:
   for yy in [11500,13100]:d.rect(xx,yy,400,400,'FURN')
  d.room(3900,17000,'ISLAND KITCHEN','5,525 x 3,600 zone',195)
  d.rect(1400,17600,3600,650,'FURN',LIGHT);d.rect(1400,15800,650,1800,'FURN',LIGHT)
  d.rect(3150,15500,2400,900,'FURN',LIGHT);d.text(4350,15850,'2,400 x 900',160);basin(d,4300,17900)
  d.room(7800,12550,'GUEST WC','1,750 x 2,650',135);wc(d,7600,13200);basin(d,8200,13800)
  d.room(10000,13300,'LAUNDRY','2,550 x 2,650',135)
  d.rect(9000,11600,600,650,'FURN');d.rect(9700,11600,600,650,'FURN');basin(d,10800,13700)
  d.room(9100,16300,'PANTRY ROOM','4,450 x 4,025 clear',180)
  d.rect(7100,17100,600,1000,'FURN',LIGHT);d.rect(10600,14800,600,3300,'FURN',LIGHT)
  d.room(13600,9100,'GUEST SUITE','4,230 x 5,225 sleeping zone',175);bed(d,13000,6100,1600)
  d.rect(16000,4800,1350,600,'FURN',LIGHT);d.text(16600,6200,'ROBE',145)
  d.text(16600,9500,'ENSUITE',140);wc(d,16200,7700);shower(d,16400,8600,950,1100);basin(d,17200,7700)
  d.room(14600,15600,'ENTERTAINMENT','6,105 x 6,825 clear',215)
  d.rect(12000,12500,850,2300,'FURN',LIGHT);d.rect(12900,12500,2800,850,'FURN',LIGHT);d.rect(16700,12800,350,2600,'FURN',BLACK)
  d.text(9400,10600,'1,250 CLEAR CROSS HALL',140)
  stairs(d,1)
 else:
  for x,title in [(3900,'MASTER A'),(14500,'MASTER B')]:
   d.room(x,9500,title,('5,525' if title=='MASTER A' else '6,105')+' x 6,300 sleeping zone',220);bed(d,x-900,6200)
   d.text(x,11500,'PRIVATE DRESSING LOBBY',160)
  d.room(2500,14900,'WALK-IN','2,625 x 5,225',165);d.rect(1400,13500,600,4500,'FURN',LIGHT);d.rect(3100,13500,600,4500,'FURN',LIGHT)
  d.room(16200,14900,'WALK-IN','2,925 x 5,225',165);d.rect(14900,13500,600,4500,'FURN',LIGHT);d.rect(16800,13500,600,4500,'FURN',LIGHT)
  for x,tx in [(4000,5650),(13800,12300)]:
   d.rect(x,13200,600,1350,'FURN',LIGHT);basin(d,x+300,13525);basin(d,x+300,14225)
   d.text(tx,14000,'2 BASINS',160)
  for x,w in [(3975,1300),(11475,1440)]:
   wc(d,x+w/2,17400);d.room(x+w/2,16900,'WC',f'{w:,} x 2,625',125)
  for x,w in [(5425,1300),(13065,1440)]:
   shower(d,x+80,17100,w-160,1000);d.room(x+w/2,16900,'SHOWER',f'{w:,} x 2,625',125)
  d.rect(6900,11600,4400,6700,'TERRACE',FAINT,FAINT)
  d.room(9100,15000,'ROOF TERRACE','Open sky / +8.40 m',180)
  d.text(9100,14200,'1,100 rear guard / solid side walls',120)
  stairs(d,2)
 draw_walls(d,l)
 # Overall and chained dimensions. Millimetres; house outside faces are fixed.
 d.dim((0,22000),(18780,22000),23400)
 for a,b in [(0,1000),(1000,17780),(17780,18780)]:d.dim((a,22000),(b,22000),22650)
 d.dim((0,0),(0,22000),-1500,'v')
 if l:
  for a,b in [(0,4500),(4500,18500),(18500,22000)]:d.dim((18780,a),(18780,b),19900,'v')
  for a,b in [(1000,6800),(6800,11400),(11400,17780)]:d.dim((a,4500),(b,4500),4000)
  for a,b in [(4500,10000),(10000,11400),(11400,18500)]:d.dim((1000,a),(1000,b),-550,'v')
  chain=[1000,6800,8700,11400,17780] if l==1 else [1000,3900,5350,6800,11400,12990,14580,17780]
  for a,b in zip(chain,chain[1:]):d.dim((a,18500),(b,18500),19000)
  ychain=[4500,7300,10000,11400,14200,18500] if l==1 else [4500,10000,11400,13000,15600,18500]
  for a,b in zip(ychain,ychain[1:]):d.dim((17780,a),(17780,b),20500,'v')
 else:
  for a,b in [(1000,6800),(6800,9600),(9600,11400)]:d.dim((a,0),(b,0),-650)
  for a,b in [(0,6600),(6600,11400)]:d.dim((1000,a),(1000,b),-550,'v')
  d.dim((1000,11400),(11400,11400),12800)
  for a,b in [(1000,4300),(4300,6800)]:d.dim((a,11400),(b,11400),12000)
  d.dim((11400,0),(11400,11400),12400,'v')
 # A-A cut marker through garage and rear site.
 if l==1:
  d.line(3500,-400,3500,22400,'SECTION',MID,10,True);d.text(3500,-700,'A',200);d.text(3500,22400,'A',200)
 return d

LEVELS={0:0,1:5000,2:8400}
def glazing(d,x,z,w,h,code):
 d.rect(x,z,w,h,'GLAZING',LIGHT,BLACK,20)
 for xx in [x+65,x+w-65,x+w/2]:d.line(xx,z,xx,z+h,'MULLION',BLACK,25)
 d.line(x+100,z+100,x+w-100,z+h-100,'GLAZING',MID,9)
 d.text(x+w/2,z+h+150,code,140,'TAG')
def elevation(which):
 front=which=='Front';back=which=='Rear';side=which in ['Left','Right']
 extent=22000 if side else 18780
 d=Drawing(which,(-1500,-1600,extent+3500,13300))
 if side:
  d.rect(0,0,11400,5000,'RETAIN',MID,BLACK,30)
  d.rect(4500,5000,14000,3400,'FACADE',FAINT,BLACK,35)
  d.rect(4500,8400,14000,3400,'FACADE',FAINT,BLACK,35)
  d.rect(4500,8000,14000,400,'FACADE',BLACK,BLACK,20)
  for l in [1,2]:
   for o in [o for o in OPEN if o.level==l and o.wall==('L' if which=='Left' else 'R')]:
    w,h,s,*_=TYPES[o.code];glazing(d,o.start,LEVELS[l]+s,w,h,o.code)
  d.line(11400,5000,22000,5000,'GROUND',BLACK,50)
  d.rect(19500,5000,2500,2400,'CANOPY',None,MID,15)
  d.dim((4500,11800),(18500,11800),12600)
  d.text(6600,1800,'CUT-IN BASEMENT',210,color='#ffffff')
 else:
  if front:d.rect(0,0,18780,5000,'RETAIN',MID,BLACK,30)
  else:d.line(0,5000,18780,5000,'GROUND',BLACK,50)
  d.rect(1000,5000,16780,3400,'FACADE',FAINT,BLACK,35)
  if front:
   d.rect(1000,8400,5800,3400,'FACADE','#ffffff',BLACK,35)
   d.rect(6800,8400,10980,3400,'FACADE',MID,BLACK,35)
  else:
   for xx,ww in [(1000,5800),(11400,6380)]:d.rect(xx,8400,ww,3400,'FACADE',FAINT,BLACK,35)
   d.rect(6800,8400,4600,1100,'GUARD',LIGHT,BLACK,20)
   d.text(9100,10000,'OPEN TERRACE',145)
  d.rect(1000,8100,16780,300,'FACADE',BLACK,BLACK,20)
  for l in ([0,1,2] if front else [1,2]):
   for o in [o for o in OPEN if o.level==l and o.wall==('F' if front else 'B')]:
    w,h,s,*_=TYPES[o.code]
    if o.code=='GD1':
     d.rect(o.start,0,w,h,'DOOR',BLACK,BLACK,25)
     for z in range(250,h,250):d.line(o.start,z,o.start+w,z,'DETAIL',MID,12)
     d.text(o.start+w/2,h+160,'GD1  5,000 x 2,600',150,color='#ffffff')
    else:glazing(d,o.start,LEVELS[l]+s,w,h,o.code)
  if front:
   # 1100 garden-edge balustrade over the 5 m retaining edge.
   d.rect(0,5000,18780,1100,'GUARD',None,MID,18)
   for x in range(0,18780,1500):d.line(x,5000,x,6100,'GUARD',MID,12)
   d.text(14300,2200,'CHARCOAL RETAINING FACE',200,color='#ffffff')
  else:
   d.rect(1000,5000,5800,900,'OUTDOOR_KITCHEN',LIGHT,BLACK,20)
   d.line(1000,7400,6800,7400,'CANOPY',BLACK,40)
   for x in [1000,6800]:d.line(x,5000,x,7400,'CANOPY',MID,25)
  d.dim((1000,11800),(17780,11800),12600)
 for z,lab in [(0,'+0.00 STREET'),(5000,'+5.00 L1'),(8400,'+8.40 L2'),(11800,'+11.80 PARAPET')]:
  d.line(-500,z,extent+500,z,'DATUM',MID,9,True)
  d.text(extent+650,z+80,lab,170,'DATUM',align='left')
 d.dim((extent,0),(extent,5000),extent+2300,'v')
 for a,b in [(5000,8400),(8400,11800)]:d.dim((extent,a),(extent,b),extent+2300,'v')
 d.text(extent/2,-1100,'BLACK METAL   /   CHARCOAL CLADDING   /   CRISP WHITE RENDER',185)
 if which in ['Rear','Left']:
  # Conventional view toward the named facade, with readable mirrored annotations.
  flipped=[]
  for it in d.items:
   kind,a,lay,col,*extra=it
   if kind=='text':
    x,y,s,size,align,rot=a;a=(extent-x,y,s,size,{'left':'right','right':'left'}.get(align,align),rot)
   elif kind=='line':
    x,y,xx,yy=a;a=(extent-x,y,extent-xx,yy)
   else:a=[(extent-x,y) for x,y in a]
   flipped.append((kind,a,lay,col,*extra))
  d.items=flipped
  d.dims=[((extent-a[0],a[1]),(extent-b[0],b[1]),extent-off if ax=='v' else off,ax,lab) for a,b,off,ax,lab in d.dims]
  x0,y0,x1,y1=d.bounds;d.bounds=(extent-x1,y0,extent-x0,y1)
 return d

def section():
 d=Drawing('Section A-A',(-1800,-2200,25000,13500))
 # y-site coordinates horizontally. Section crosses left garage, store and main living wing.
 d.poly([(11400,0),(22000,0),(22000,5000),(11400,5000)],'EARTH','#e2e5e3',MID,15)
 for x in range(11700,22000,550):d.line(x,0,min(x+2500,22000),min(2500,22000-x),'EARTH',MID,9)
 d.rect(0,-250,11400,250,'SLAB',BLACK,BLACK)
 d.rect(0,4250,4500,250,'SLAB',BLACK,BLACK)
 d.rect(0,4500,4500,500,'SOIL',GREEN,MID)
 d.rect(4500,4750,14000,250,'SLAB',BLACK,BLACK)
 d.rect(4500,8150,14000,250,'SLAB',BLACK,BLACK)
 d.rect(4500,11200,14000,250,'SLAB',BLACK,BLACK)
 for x in [4500,18300]:d.rect(x,5000,200,6800,'WALL',BLACK,BLACK)
 d.rect(0,2600,300,1650,'RETAIN',MID,BLACK)
 d.rect(11100,0,300,4750,'RETAIN',MID,BLACK)
 d.line(0,5000,4500,5000,'GROUND',BLACK,25);d.line(18500,5000,22000,5000,'GROUND',BLACK,25)
 d.rect(4500,11450,14000,350,'PARAPET',FAINT,BLACK)
 d.line(0,0,-1300,0,'STREET',BLACK,35)
 d.line(200,0,200,2600,'DOOR',BLACK,15)
 d.rect(6600,0,150,4250,'PARTITION',None,MID,18)
 d.room(3300,1800,'GARAGE','Street entry +/-0.00',230)
 d.room(8750,1800,'STORAGE / REPAIR','Back of garage',200)
 d.room(9000,6500,'LEVEL 1 / LIVING + DINING','FFL +5.00 m',220)
 d.room(10000,9600,'LEVEL 2 / MASTER A','FFL +8.40 m',220)
 d.text(2100,5350,'FRONT GARDEN',180);d.text(20400,5350,'BACK GARDEN',180)
 d.text(15800,2600,'RETAINED GROUND',210)
 # Drainage/waterproofing concept with separated legible callouts.
 d.line(11500,300,11500,4650,'DRAIN',MID,22);d.circle(11600,300,100,'DRAIN')
 d.line(11600,600,14200,1200,'LEADER',MID,12)
 d.text(14400,1250,'Drain + waterproofing to engineer design',155,align='left')
 d.text(3000,-1250,'Portal clear height 2,600',170)
 d.text(9000,-1250,'Retaining / slab thicknesses diagrammatic',160)
 for z,label in [(0,'+0.00'),(5000,'+5.00'),(8400,'+8.40'),(11800,'+11.80')]:
  d.line(-900,z,23100,z,'DATUM',MID,9,True);d.text(23300,z,label,180,align='left')
 d.dim((0,0),(0,5000),-1000,'v','5,000 LEVEL DIFFERENCE')
 d.dim((22000,5000),(22000,8400),22500,'v');d.dim((22000,8400),(22000,11800),22500,'v')
 for a,b in [(0,4500),(4500,18500),(18500,22000)]:d.dim((a,11800),(b,11800),12800)
 return d

PLANS=[plan(i) for i in range(3)]
ELEV=[elevation(w) for w in ['Front','Rear','Left','Right']]
SEC=section()
COUNTS=Counter(o.code for o in OPEN)
def schedule_drawing(codes,name):
 cols=5 if len(codes)>9 else 5
 rows=math.ceil(len(codes)/cols);cellw=6700;cellh=5700
 d=Drawing(name,(0,0,cols*cellw,rows*cellh))
 for i,c in enumerate(codes):
  w,h,s,spec,room=TYPES[c];x=(i%cols)*cellw+800;y=(rows-1-i//cols)*cellh+1700
  # Common elevation scale across every opening.
  xx=x+(5000-w)/2
  if c.startswith('W') or c in ['D4','D7']:
   glazing(d,xx,y,w,h,c)
  else:
   d.rect(xx,y,w,h,'DOOR',FAINT,BLACK,20)
   d.rect(xx+50,y+50,w-100,h-100,'DOOR',None,MID,15)
   d.text(xx+w/2,y+h+150,c,240,'TAG')
  if c=='GD1':
   for z in range(250,h,250):d.line(xx,y+z,xx+w,y+z,'DETAIL',MID,12)
  elif c.startswith('D') and c!='D7':
   d.poly([(xx,y),(xx+w,y+h/2),(xx,y+h)],'DOOR',None,MID,12,False)
   d.circle(xx+w-100,y+1050,35,'DOOR')
  d.dim((xx,y),(xx+w,y),y-330)
  d.dim((xx+w,y),(xx+w,y+h),xx+w+330,'v')
  d.text(x+2500,y-750,f'{c}   {w:,} x {h:,}   SILL {s:,}',270)
  d.text(x+2500,y-1100,room,165)
  d.text(x+2500,y-1400,f'QTY {COUNTS[c]}   '+spec,135)
 return d
DOORS=schedule_drawing([x for x in TYPES if x.startswith('D') or x=='GD1'],'Doors')
WINDOWS=schedule_drawing([x for x in TYPES if x.startswith('W')],'Windows')

# SVG text is outlined, so the presentation has no live-font dependency.
PATHCACHE={}
def outline(s,size):
 key=(s,size)
 if key in PATHCACHE:return PATHCACHE[key]
 p=TextPath((0,0),s,size=size,prop=FONT);parts=[];cur=(0,0);start=(0,0)
 for pts,code in p.iter_segments(curves=True,simplify=False):
  if code==1:
   parts.append(f'M{pts[0]:.3f},{pts[1]:.3f}');cur=start=(pts[0],pts[1])
  elif code==2:
   parts.append(f'L{pts[0]:.3f},{pts[1]:.3f}');cur=(pts[0],pts[1])
  elif code==3:
   qx,qy,ex,ey=pts
   c1=(cur[0]+2*(qx-cur[0])/3,cur[1]+2*(qy-cur[1])/3)
   c2=(ex+2*(qx-ex)/3,ey+2*(qy-ey)/3)
   parts.append(f'C{c1[0]:.3f},{c1[1]:.3f} {c2[0]:.3f},{c2[1]:.3f} {ex:.3f},{ey:.3f}');cur=(ex,ey)
  elif code==4:
   parts.append(f'C{pts[0]:.3f},{pts[1]:.3f} {pts[2]:.3f},{pts[3]:.3f} {pts[4]:.3f},{pts[5]:.3f}');cur=(pts[4],pts[5])
  elif code==79:parts.append('Z');cur=start
 width=p.get_extents().width if s.strip() else 0
 PATHCACHE[key]=(' '.join(parts),width);return PATHCACHE[key]
def svg(d):
 x0,y0,x1,y1=d.bounds;sy=y0+y1
 out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1-x0} {y1-y0}" role="img" aria-label="{html.escape(d.name)}">']
 for it in d.items:
  kind,a,lay,col,*extra=it
  if kind=='text':
   x,y,s,size,align,rot=a;p,w=outline(s,size);dx=-w/2 if align=='center' else -w if align=='right' else 0
   out.append(f'<path fill="{col}" d="{p}" transform="translate({x},{sy-y}) rotate({-rot}) scale(1,-1) translate({dx},0)"/>')
  elif kind=='line':
   x,y,xx,yy=a;width,dash=extra
   out.append(f'<path d="M{x},{sy-y} L{xx},{sy-yy}" fill="none" stroke="{col}" stroke-width="{width}"'+(' stroke-dasharray="140 90"' if dash else '')+'/>')
  else:
   width,fill,closed=extra;pts=' '.join(f'{x},{sy-y}' for x,y in a)
   tag='polygon' if closed else 'polyline'
   out.append(f'<{tag} points="{pts}" fill="{fill or "none"}" stroke="{col}" stroke-width="{width}"/>')
 out.append('</svg>');return '\n'.join(out)
for d in PLANS+ELEV+[SEC,DOORS,WINDOWS]:(DRAW/(d.name.replace(' ','_')+'.svg')).write_text(svg(d))

# Native AutoCAD R2010 entities and rendered associative-free dimensions.
def rgb(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))
def make_dxf():
 ezdxf.options.write_fixed_meta_data_for_testing=True
 doc=ezdxf.new('R2010',setup=True);doc.units=4
 doc.header['$INSUNITS']=4;doc.header['$MEASUREMENT']=1;doc.header['$LUNITS']=2;doc.header['$LUPREC']=0
 doc.header['$TDCREATE']=2461353.5;doc.header['$TDUPDATE']=2461353.5
 doc.header['$FINGERPRINTGUID']='{27998430-0000-4000-8000-000000000001}'
 doc.header['$VERSIONGUID']='{27998430-0000-4000-8000-000000000002}'
 m=doc.modelspace()
 origins={}
 groups=PLANS+ELEV+[SEC,DOORS,WINDOWS]
 for idx,d in enumerate(groups):
  ox=(idx%3)*45000;oy=-(idx//3)*35000;origins[d.name]=[ox,oy]
  prefix=d.name.replace(' ','_').replace('-','_').upper()
  for it in d.items:
   kind,a,lay,col,*extra=it
   if lay=='DIM':continue
   ln=prefix+'_'+lay
   if ln not in doc.layers:doc.layers.new(ln,dxfattribs={'color':7,'lineweight':25 if lay=='WALL' else 13})
   # Plotting uses layer lineweights; all text remains editable.
   att={'layer':ln,'true_color':ezdxf.colors.rgb2int(rgb(col))}
   if kind=='line':
    x,y,xx,yy=a;m.add_line((x+ox,y+oy),(xx+ox,yy+oy),dxfattribs=att)
   elif kind=='poly':
    width,fill,closed=extra;pts=[(x+ox,y+oy) for x,y in a]
    m.add_lwpolyline(pts,close=closed,dxfattribs=att)
    if fill:
     h=m.add_hatch(color=7,dxfattribs={'layer':ln,'true_color':ezdxf.colors.rgb2int(rgb(fill))});h.paths.add_polyline_path(pts,is_closed=True)
   else:
    x,y,s,size,align,rot=a
    ent=m.add_text(s,dxfattribs={**att,'height':size,'rotation':rot,'style':'OpenSans'})
    ent.set_placement((x+ox,y+oy),align={'center':TextEntityAlignment.BOTTOM_CENTER,'left':TextEntityAlignment.LEFT,'right':TextEntityAlignment.RIGHT}[align])
  ln=prefix+'_DIM'
  if ln not in doc.layers:doc.layers.new(ln,dxfattribs={'color':7,'lineweight':13})
  for a,b,offset,axis,lab in d.dims:
   p1=(a[0]+ox,a[1]+oy);p2=(b[0]+ox,b[1]+oy)
   base=(ox,offset+oy) if axis=='h' else (offset+ox,oy)
   dm=m.add_linear_dim(base=base,p1=p1,p2=p2,angle=0 if axis=='h' else 90,text=lab,dimstyle='EZDXF',override={'dimtxt':220,'dimasz':90,'dimgap':50,'dimexo':40,'dimexe':80,'dimtad':1,'dimclrd':7,'dimclre':7,'dimclrt':7},dxfattribs={'layer':ln});dm.render()
  m.add_text(d.name.upper()+' / mm / CONCEPT DESIGN',dxfattribs={'height':320,'layer':ln}).set_placement((ox+d.bounds[0],oy+d.bounds[3]+700))
 # Machine-readable schedule with real text and cell lines, in model space.
 ox,oy=0,-145000
 cols=[0,1800,4200,6500,8700,10300,22500,33000]
 rows=[['TYPE','WIDTH','HEIGHT','SILL','QTY','CONSTRUCTION / GLAZING','ROOM / USE']]+[[c,str(v[0]),str(v[1]),str(v[2]),str(COUNTS[c]),v[3],v[4]] for c,v in TYPES.items()]
 doc.layers.new('SCHEDULE',dxfattribs={'color':7})
 for r,row in enumerate(rows):
  for j,s in enumerate(row):m.add_text(s,dxfattribs={'height':175,'layer':'SCHEDULE'}).set_placement((ox+cols[j]+100,oy-r*650))
  m.add_line((ox,oy-r*650-150),(ox+cols[-1],oy-r*650-150),dxfattribs={'layer':'SCHEDULE'})
 # Opening setting-out table shared with PDF: every installed instance.
 sox=40000;soy=-145000
 for i,o in enumerate(OPEN):
  w=getwall(o);x=o.start if w.axis=='h' else w.c;y=w.c if w.axis=='h' else o.start
  row=f'{i+1:02}  L{o.level}  {o.code}  {w.axis.upper()}  X={x:.0f}  Y={y:.0f}  {o.room}'
  m.add_text(row,dxfattribs={'height':175,'layer':'SCHEDULE'}).set_placement((sox,soy-i*400))
 note=['18,780 x 22,000 plot. Units mm. Site origin left-front corner.',
       'L0 +/-0.00 / L1 +5.00 / L2 +8.40 / parapet +11.80 m.',
       'External walls 200 / internal walls 150. Structural elements indicative.',
       'A-A cut at site X=3,500. Elevations are viewed from their named side.',
       'Front/right use increasing site axes; rear/left are mirrored orthographic views.',
       'Opening table gives lower start coordinate and wall centreline.',
       'Dimensions are proposed design sizes, not survey or fabrication sizes.',
       'G1: 6T / 12Ar / 6T low-E double glazing; G2: obscure inner pane.',
       'Verify wind, energy, safety, egress and local fire-rating requirements.',
       'CONCEPT ONLY. Local architect / engineer to verify before construction.']
 for i,s in enumerate(note):m.add_text(s,dxfattribs={'height':200,'layer':'SCHEDULE'}).set_placement((0,-160000-i*500))
 doc.set_modelspace_vport(80000,center=(40000,-65000))
 doc.classes.add_required_classes(doc.dxfversion)
 doc.classes.classes=OrderedDict(sorted(doc.classes.classes.items()))
 path=OUT/'Modern_House_18.78x22m_Full_CAD.dxf';doc.saveas(path)
 return path,origins

# Vector PDF engine: the same geometry, with searchable native PDF text.
PT=72/25.4
PAGE=(594*PT,420*PT)
def fcolor(c):return tuple(x/255 for x in rgb(c))
def pdftext(p,x,y,s,size=10,col=BLACK,bold=False,align='left'):
 font='hebo' if bold else 'helv';w=fitz.get_text_length(s,fontname=font,fontsize=size)
 if align=='center':x-=w/2
 elif align=='right':x-=w
 p.insert_text((x,y),s,fontname=font,fontsize=size,color=fcolor(col))
def pdfdrawing(p,d,box,scale=None):
 x0,y0,x1,y1=d.bounds;bx,by,bw,bh=box
 sc=scale if scale else min(bw/(x1-x0),bh/(y1-y0))
 ox=bx+(bw-(x1-x0)*sc)/2-x0*sc;oy=by+(bh-(y1-y0)*sc)/2+y1*sc
 def point(x,y):return fitz.Point(ox+x*sc,oy-y*sc)
 for it in d.items:
  kind,a,lay,col,*extra=it
  if kind=='text':
   x,y,s,size,align,rot=a;pt=point(x,y);sz=size*sc
   w=fitz.get_text_length(s,fontname='helv',fontsize=sz)
   shift=w/2 if align=='center' else w if align=='right' else 0
   if rot==0:pt.x-=shift
   else:pt.y+=shift
   p.insert_text(pt,s,fontsize=sz,fontname='helv',color=fcolor(col),rotate=rot)
  elif kind=='line':
   x,y,xx,yy=a;width,dash=extra
   p.draw_line(point(x,y),point(xx,yy),color=fcolor(col),width=max(.15,width*sc),dashes='[4 3] 0' if dash else None)
  else:
   width,fill,closed=extra
   p.draw_polyline([point(x,y) for x,y in a],color=fcolor(col),fill=fcolor(fill) if fill else None,width=max(.15,width*sc),closePath=closed)
 return sc

def titlepage(doc,num,title,sub):
 p=doc.new_page(width=PAGE[0],height=PAGE[1]);w,h=PAGE
 p.draw_rect(fitz.Rect(28,28,w-28,h-28),color=fcolor(BLACK),width=.8)
 pdftext(p,48,65,'18.78 / 22',21,bold=True);pdftext(p,238,65,title,23,bold=True)
 pdftext(p,238,87,sub,10,col=MID)
 p.draw_line((48,105),(w-48,105),color=fcolor(BLACK),width=.7)
 p.draw_line((48,h-74),(w-48,h-74),color=fcolor(BLACK),width=.7)
 pdftext(p,48,h-52,'2799843  /  TWO STOREY MODERN CONTEMPORARY HOUSE',10,bold=True)
 pdftext(p,48,h-37,'CONCEPT DESIGN  /  Dimensions in mm unless noted  /  08 NOV 2026',8,col=MID)
 pdftext(p,w-48,h-51,f'A{num:02}  /  A2 LANDSCAPE',12,bold=True,align='right')
 pdftext(p,w-48,h-37,'Verify survey, structure and statutory requirements before construction',8,col=MID,align='right')
 return p

def notes(p,x,y,lines,size=11,leading=23):
 for s in lines:pdftext(p,x,y,s,size);y+=leading

def table(p,x,y,width,headers,rows,colwidths,rowh=29,fs=10):
 xs=[x]
 for c in colwidths:xs.append(xs[-1]+width*c)
 p.draw_rect(fitz.Rect(x,y,x+width,y+rowh),color=None,fill=fcolor(BLACK))
 for j,h in enumerate(headers):pdftext(p,xs[j]+8,y+rowh*.66,h,fs,col='#ffffff',bold=True)
 for i,row in enumerate(rows):
  yy=y+(i+1)*rowh
  if i%2==0:p.draw_rect(fitz.Rect(x,yy,x+width,yy+rowh),color=None,fill=fcolor(FAINT))
  for j,s in enumerate(row):pdftext(p,xs[j]+8,yy+rowh*.66,str(s),fs)
  p.draw_line((x,yy+rowh),(x+width,yy+rowh),color=fcolor(LIGHT),width=.4)

def make_pdf():
 doc=fitz.open()
 for l,d in enumerate(PLANS):
  p=titlepage(doc,l+1,['Street garage + infrastructure','Main floor + gardens','Twin master suites'][l],f'LEVEL {l}   /   FFL {LEVELS[l]/1000:+.2f} m   /   Plan 1:75 at A2, print at 100%')
  pdfdrawing(p,d,(50,115,900,985),PT/75)
  x=1020
  if l==0:
   lines=['01  TWO-CAR GARAGE','5,525 x 6,325 clear between finished wall faces.','Two indicative parking bays. 5,000 x 2,600 door.','Street access is level at the front boundary.','','02  BACK-OF-GARAGE SERVICE ROOMS','Storage / car repair: 3,025 x 4,525 clear.','Electrical / IT / CCTV / NVR: 2,350 x 4,525.','Service rooms enter from the garage.','Front duct routes for below-ground ventilation.','','03  PROTECTED PEDESTRIAN ROUTE','Separate D8 street entrance and internal lobby.','Garage separation and D6 fire rating to local code.','Stair L0-L1: 30 risers @ 166.667 = 5,000.','Two flights, 15 risers each, 14 goings @ 280.','1,200 clear flights / 1,200 minimum landings.','Exact rise per step = 5,000 / 30 mm.','','BASEMENT OUTSIDE FOOTPRINT','10,400 x 11,400 = 118.56 m2.','Retaining walls and excavation require engineering.']
  elif l==1:
   lines=['01  SITE + SETBACKS','18,780 x 22,000 = 413.16 m2.','1,000 clear to both side boundaries.','House outside footprint: 16,780 x 14,000.','Front garden zone 4,500 deep, rear 3,500.','','02  FAMILY + SOCIAL','Living / dining / island kitchen form an open route.','Dedicated entertainment room faces rear garden.','1,250 clear cross hall links the three bays.','Guest suite has its own combined WC + shower.','','03  SERVICES + OUTDOOR COOKING','Enclosed pantry entered directly from kitchen.','Dedicated laundry and common guest WC.','Rear outdoor kitchen: counter, sink and grill.','Canopy at rear boundary, no enclosed side setback.','','04  VERTICAL CIRCULATION','Stair L1-L2: 20 risers @ 170 = 3,400.','Two flights, 10 risers each, 9 goings @ 280.','1,200 clear flights / 1,200 minimum landings.','Laundry / guest WC exhaust via vertical ducts.','Garden edges receive 1,100 high guards.']
  else:
   lines=['01  TWO COMPLETE PRIVATE SUITES','Each suite enters from the shared central hall.','Sleeping room, dressing lobby and rear wet zone','remain inside the individual suite.','','02  MASTER A','Sleeping zone: 5,525 wide, furniture drawn to scale.','Walk-in closet: 2,625 x 5,225 clear.','Separate WC: 1,300 x 2,625 clear.','Separate shower: 1,300 x 2,625 clear.','Two washbasins in dedicated vanity area.','','03  MASTER B','Sleeping zone: 6,105 wide, furniture drawn to scale.','Walk-in closet: 2,925 x 5,225 clear.','Separate WC: 1,440 x 2,625 clear.','Separate shower: 1,440 x 2,625 clear.','Two washbasins in dedicated vanity area.','','04  SHARED REAR ROOF TERRACE','Open to sky, accessed from the common landing.','1,100 rear guard; full-height suite walls at sides.','Provide drainage, overflow and waterproofing.']
  notes(p,x,160,lines,11,25)
  # Measured scale bar for plan sheets.
  sx=1030;sy=955
  for i in range(5):p.draw_rect(fitz.Rect(sx+i*1000*PT/75,sy,sx+(i+1)*1000*PT/75,sy+7),color=fcolor(BLACK),fill=fcolor(BLACK) if i%2==0 else None,width=.5)
  pdftext(p,sx,sy+25,'0',9);pdftext(p,sx+5000*PT/75,sy+25,'5 m',9,align='right')
  pdftext(p,x,1015,'Dimension chains: external faces / internal wall centrelines.',9,col=MID)
  pdftext(p,x,1033,'Room sizes: clear wall faces. External walls 200, partitions 150.',9,col=MID)
 for n,pair in enumerate([ELEV[:2],ELEV[2:]]):
  p=titlepage(doc,n+4,['Front + rear elevations','Left + right elevations'][n],'Elevation scale 1:100 at A2  /  Heights in metres relative to front street datum')
  for j,d in enumerate(pair):
   pdfdrawing(p,d,(70,135+j*460,1000,430),PT/100)
   pdftext(p,80,150+j*460,d.name.upper()+' ELEVATION',13,bold=True)
  notes(p,1170,190,['MATERIAL PALETTE','','M01  Crisp white mineral render','M02  Charcoal rainscreen / concrete','M03  Black powder-coated aluminium','M04  Clear / privacy low-E glazing','','DATUM STRATEGY','','+11.80  Main roof parapet','+8.40    Upper finished floor','+5.00    Main finished floor','+0.00    Street garage finished floor','','GARAGE IN THE RETAINING FACE','','5.00 m level change integrated at front.','Garage is excavated into the raised site.','Main pedestrian access uses D8 + stair.','','PROJECTION NOTE','','Each view looks toward its named facade.','Rear and left views mirror the site axes.','Opening register uses the common site origin','shown on the plans.','','The supplied perspective is atmospheric.','Dimensioned orthographic views govern.'],11,25)
 p=titlepage(doc,6,'5.00 m cut-in garage section','SECTION A-A at site X = 3,500 mm  /  1:100 at A2  /  Building and terrain relationship')
 pdfdrawing(p,SEC,(65,135,1500,575),PT/100)
 notes(p,75,770,['SECTION KEY','Garage floor at +/-0.00. Main floor +5.00. Upper floor +8.40. Roof parapet +11.80.',
 'Front garden over garage: indicative 500 landscape build-up over slab. Garage clear soffit shown at +4.25.',
 'House slabs shown 250 thick for coordination only. Floor-to-floor height 3,400, indicative upper clear height 2,800.',
 'Retaining elements, foundations and lintels are diagrammatic. No reinforcement, bearing capacity or wall sizing is certified.',
 'Provide rear-wall waterproofing, drained cavity, subsoil drain and a maintainable positive discharge route.',
 'Set street threshold, trench drain and drainage discharge from measured road levels and flood requirements.',
 'Stair dimensions and access are documented on A01-A03. The A-A cut does not pass through the stair core.'],12,30)
 for num,d,codes in [(7,DOORS,[c for c in TYPES if not c.startswith('W')]),(8,WINDOWS,[c for c in TYPES if c.startswith('W')])]:
  p=titlepage(doc,num,'Door elevations + schedule' if num==7 else 'Window elevations + schedule','Nominal opening dimensions in mm  /  Sill measured from corresponding finished floor  /  Elevations NTS')
  pdfdrawing(p,d,(55,125,1570,510))
  rows=[[c,str(TYPES[c][0]),str(TYPES[c][1]),str(TYPES[c][2]),str(COUNTS[c]),TYPES[c][3],TYPES[c][4]] for c in codes]
  table(p,60,665,1560,['TYPE','WIDTH','HEIGHT','SILL','QTY','CONSTRUCTION / GLAZING','ROOM / USE'],rows,[.06,.06,.06,.06,.04,.37,.35],29,11)
  pdftext(p,65,1035,'G1: 6 mm toughened / 12 mm argon / 6 mm toughened low-E IGU. G2: G1 with obscure inner pane. Black aluminium frames.',10)
  pdftext(p,65,1056,'* D6 rating, frames, hardware and closers to local fire strategy. Confirm wind, safety, energy and fabrication allowances before ordering.',10)
 # Every opening placement, useful for reproducing the drawing without measuring a PDF.
 for chunk in range(math.ceil(len(OPEN)/27)):
  p=titlepage(doc,9+chunk,'Opening setting-out register',f'INSTANCE REGISTER {chunk+1}  /  Origin X=0, Y=0 at left-front site corner  /  Coordinates in mm')
  rows=[]
  for idx,o in list(enumerate(OPEN))[chunk*27:(chunk+1)*27]:
   w=getwall(o);x=o.start if w.axis=='h' else w.c;y=w.c if w.axis=='h' else o.start
   rows.append([f'{idx+1:02}',f'L{o.level}',o.code,'X' if w.axis=='h' else 'Y',f'{x:,.0f}',f'{y:,.0f}',f'{TYPES[o.code][0]:,}',o.room])
  table(p,60,140,1560,['NO.','LEVEL','TYPE','RUN AXIS','START X','START Y','WIDTH','ROOM / CONNECTION'],rows,[.045,.05,.055,.08,.09,.09,.08,.51],29,11)
  notes(p,65,1010,['Start X/Y identifies the low-coordinate jamb on the wall centreline. Width extends in the positive run-axis direction.',
                     'Opening heights/sills and construction are defined by type on A07-A08. All instances are represented in plan and schedule.'],10,22)
 p=titlepage(doc,11,'Design basis + requirement register','Source: Residential House Design Requirements.pdf, 13 pages  /  Employer brief + requested level strategy')
 req=[('Plot + clearances','18,780 x 22,000. 1,000 each side. Main house 16,780 wide.','A01-A03'),('5 m elevated site','Garage excavated into retaining face, street-level vehicle access.','A01, A04-A06'),('Two-car covered parking','2 bays, GD1 5,000 x 2,600. Rear repair/store and electrical room.','A01, A07'),('Living + dining + entertainment','Dedicated entertainment room. Public rooms linked by cross hall.','A02'),('Indoor kitchen + pantry','Island, worktops and enclosed pantry directly accessible.','A02'),('Outdoor kitchen + laundry','Rear-boundary cooking counter with sink. Separate laundry.','A02'),('Guest suite + common WC','Guest ensuite with combined WC/shower. Separate common WC.','A02'),('Front + back gardens','Front planted terrace and 3,500 deep rear outdoor zone.','A02, A06'),('Two masters','Two separate suites, each closet + WC + shower + 2 washbasins.','A03'),('All four elevations + section','Front/rear/left/right, four datum levels and 5 m section.','A04-A06'),('Doors + windows','GD1 plus D1-D8, W1-W10. Every instance has a coordinate.','A07-A10'),('CAD + PDF','R2010 DXF in mm. A2 vector PDF and ZIP with both files.','Package')]
 table(p,60,145,1560,['REQUIREMENT','PROPOSED RESPONSE','SHEETS'],req,[.22,.66,.12],36,11)
 notes(p,70,680,['DESIGN BASIS AND LIMITS',
  'The 18.78 x 22 m site and 1 m side spaces come from brief pages 1-2. Site photos on pages 10-12 show a raised roadside corner.',
  'Front orientation is diagrammatic. North, road boundary survey, rear/side terrain, solar orientation and jurisdiction are not supplied.',
  'A level +5.00 main terrace is assumed across the site. No driveway slope, existing contour or geotechnical condition is inferred.',
  'Room sizes, openings, floor heights, wall/slab thicknesses and canopy are design proposals. Survey and local approvals remain necessary.',
  'Repair room is light domestic storage/tool work only. Vehicle workshop use needs a separate fire, exhaust and use-class review.',
  'Structural design, egress/accessibility, retaining stability, foundations, drainage and MEP design are outside this concept drawing set.',
  'Door/window tags use GD1 for the garage plus D1-D8 and W1-W10, retaining both requested numbering scopes.',
  'All plan geometry and opening counts are generated from one data model. The supplied photorealistic image is a concept reference.'],11,31)
 doc.set_metadata({'title':'Modern House 18.78 x 22 m - Full Drawing Set','author':'Project Design Studio','subject':'Contest 2799843 - Concept architectural drawings','creationDate':'D:20261108000000Z','modDate':'D:20261108000000Z'})
 path=OUT/'Modern_House_18.78x22m_Full_Drawing_Set.pdf';doc.save(path,garbage=4,deflate=True,no_new_id=True);doc.close();return path

# Fixed 1600 x 1200 editorial boards, rendered entirely from the shared model.
CSS='''*{box-sizing:border-box}html,body{margin:0;width:1600px;height:1200px;overflow:hidden;background:#fff;color:#202426;font-family:Arial,Helvetica,sans-serif}body{padding:40px 48px}header{height:100px;border-top:5px solid #202426;display:flex;align-items:center;justify-content:space-between}h1{font-size:38px;letter-spacing:-1.2px;margin:0;font-weight:500}header p{font-size:13px;line-height:1.7;margin:0;text-align:right;letter-spacing:.7px}.num{font-size:62px;font-weight:700;letter-spacing:-4px;margin-right:22px}.title{display:flex;align-items:center}h2{font-size:17px;letter-spacing:.2px;margin:0 0 6px}p{font-size:14px;line-height:1.5}small{font-size:12px;color:#5b6265}footer{position:absolute;bottom:32px;left:48px;right:48px;border-top:1px solid #202426;display:flex;justify-content:space-between;padding-top:14px;font-size:11px;letter-spacing:.5px}img.cad{width:100%;height:100%;object-fit:contain}.label{font-size:12px;text-transform:uppercase;letter-spacing:1px}.datum{font-variant-numeric:tabular-nums}.swatch{display:inline-block;width:15px;height:15px;margin-right:7px;vertical-align:middle}.sheet1{height:970px;display:grid;grid-template-columns:970px 510px;gap:24px}.hero{height:650px;position:relative;overflow:hidden;background:#dbe0e0}.hero img{width:100%;height:100%;object-fit:cover}.hero-caption{position:absolute;bottom:0;left:0;right:0;padding:18px 22px;background:rgba(255,255,255,.92);display:flex;justify-content:space-between}.hero-caption strong{font-size:25px;font-weight:500}.section{height:300px;margin-top:18px;border-top:1px solid #aab0b2;padding-top:12px}.section .drawing{height:225px}.orthos{display:grid;grid-template-rows:repeat(4,222px);gap:10px}.ortho{border-bottom:1px solid #d4d9da;padding:5px 0}.ortho .drawing{height:196px}.plans{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;height:780px}.plan{padding-top:18px;border-top:1px solid #202426}.plan .drawing{height:670px}.plan h2{font-size:23px;font-weight:500}.plan .tag{font-size:12px;letter-spacing:1px;color:#5b6265}.metrics{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid #202426;padding-top:18px;gap:22px;margin-top:20px}.metrics strong{font-size:30px;font-weight:500;display:block}.metrics p{margin:8px 0 0;font-size:13px}.sched-grid{height:465px;display:grid;grid-template-columns:1fr 1fr;gap:28px}.sched-grid .drawing{height:402px}.tables{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:8px}table{border-collapse:collapse;width:100%;font-size:11px}th{text-align:left;background:#202426;color:white;padding:9px 6px;font-size:10px;letter-spacing:.4px}td{padding:7px 6px;border-bottom:1px solid #d5dadd;line-height:1.2}tr:nth-child(even){background:#f1f3f3}.notes{display:grid;grid-template-columns:1fr 1fr;gap:28px;border-top:1px solid #202426;margin-top:20px;padding-top:10px}.notes p{font-size:12px;margin:0}.accent{color:#5b6265}'''
def image_tag(d):return '<img class="cad" src="assets/cad/'+d.name.replace(' ','_')+'.svg" alt="'+html.escape(d.name)+' dimensioned CAD drawing">'
def header(num,title,right):return f'<header><div class="title"><span class="num">{num:02}</span><h1>{title}</h1></div><p>18.78 × 22.00 m<br>{right}</p></header>'
def footer(n):return f'<footer><span>2799843 / MODERN CONTEMPORARY RESIDENCE</span><span>CONCEPT DESIGN · ALL DIMENSIONS IN mm · ORTHOGRAPHIC DRAWINGS GOVERN</span><span>SHEET {n:02} / 03</span></footer>'
def writeboard(n,body):
 (ROOT/f'board{n}-codex.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1600, initial-scale=1"><title>Modern House / Sheet '+str(n)+'</title><style>'+CSS+'</style></head><body>'+body+footer(n)+'</body></html>')
def board_table(codes):
 s='<table><thead><tr><th>TYPE / QTY</th><th>W × H / SILL</th><th>ROOM / CONSTRUCTION</th></tr></thead><tbody>'
 for c in codes:
  w,h,si,sp,r=TYPES[c];s+=f'<tr><td><b>{c}</b> / {COUNTS[c]}</td><td>{w:,} × {h:,} / {si:,}</td><td>{r}<br><span class="accent">{sp}</span></td></tr>'
 return s+'</tbody></table>'
def makeboards():
 body=header(1,'A house above the street','ELEVATIONS + 5.00 m CUT-IN SECTION')
 body+='<main class="sheet1"><div><div class="hero"><div style="position:absolute;top:18px;left:18px;z-index:1;background:rgba(255,255,255,.93);padding:12px 16px;font-size:12px;line-height:1.8">+11.80 m / ROOF PARAPET<br>+8.40 m / TWIN MASTERS<br>+5.00 m / MAIN FLOOR<br>±0.00 m / STREET GARAGE</div><img src="assets/front-elevation-5m.jpg" alt="Supplied concept perspective of the modern house above a cut-in garage"><div class="hero-caption"><strong>5.00 m. One integrated arrival.</strong><span class="label">Supplied concept perspective<br>Atmosphere + material reference</span></div></div><div class="section"><h2>A—A / The garage within the retaining face</h2><div class="drawing">'+image_tag(SEC)+'</div><small>Level access at street. Main garden +5.00 m. Structure and drainage to engineer design.</small></div></div><div><div class="orthos">'
 for d in ELEV:body+='<div class="ortho"><h2>'+d.name+' elevation</h2><div class="drawing">'+image_tag(d)+'</div></div>'
 body+='</div><p style="font-size:12px;margin-top:14px"><span class="swatch" style="background:#202426"></span>Black metal &nbsp; <span class="swatch" style="background:#5b6265"></span>Charcoal &nbsp; <span class="swatch" style="background:#fff;border:1px solid #bbb"></span>Crisp white</p></div></main>'
 writeboard(1,body)
 body=header(2,'Three levels. Every room resolved.','FULL MEASUREMENT FLOOR PLANS')+'<main><div class="plans">'
 for l,d in enumerate(PLANS):
  body+='<section class="plan"><div class="tag">LEVEL '+str(l)+' / '+f'{LEVELS[l]/1000:+.2f}'+' m</div><h2>'+['Street garage','Main ground floor','Twin master suites'][l]+'</h2><div class="drawing">'+image_tag(d)+'</div><small>'+['Two covered bays · Rear storage / repair · Electrical / IT / CCTV / NVR','Living · Dining · Entertainment · Island kitchen · Pantry · Laundry · Guest suite','Each suite: walk-in closet · Separate WC · Separate shower · Two washbasins'][l]+'</small></section>'
 body+='</div><div class="metrics"><div><strong>413.16 m²</strong><p>18.78 × 22.00 m plot<br>1.00 m clear on both sides</p></div><div><strong>16.78 m</strong><p>Maximum house width<br>14.00 m main building depth</p></div><div><strong>+5.00 / +8.40</strong><p>Main / upper finished-floor levels<br>30 + 20 stair risers</p></div><div><strong>Front + back</strong><p>Planted front terrace and rear garden<br>Outdoor kitchen at rear boundary</p></div></div></main>'
 writeboard(2,body)
 body=header(3,'Openings, precisely specified.','DOOR + WINDOW ELEVATIONS AND SCHEDULE')
 body+='<main><div class="sched-grid"><section><h2>GD1 + D1–D8 / Door types</h2><div class="drawing">'+image_tag(DOORS)+'</div></section><section><h2>W1–W10 / Window types</h2><div class="drawing">'+image_tag(WINDOWS)+'</div></section></div><div class="tables">'
 body+=board_table([c for c in TYPES if not c.startswith('W')])+board_table([c for c in TYPES if c.startswith('W')])+'</div>'
 body+='<div class="notes"><p><b>G1</b> 6 mm toughened / 12 mm argon / 6 mm toughened low-E IGU.<br><b>G2</b> G1 with obscure inner pane. Black powder-coated aluminium frames.</p><p>Sill heights from each finished floor. Dimensions are nominal design openings.<br>D8 and W10 retain the extended brief scope. D6 fire rating / hardware to local code.</p></div></main>'
 writeboard(3,body)

def validate(dxf,pdf):
 errors=[]
 for l,walls in WALLS.items():
  for w in walls:
   oo=sorted([o for o in OPEN if o.level==l and o.wall==w.id],key=lambda o:o.start)
   end=w.a
   for o in oo:
    if o.start<end-1:errors.append(f'overlap L{l} {w.id} {o.code}')
    if o.start+TYPES[o.code][0]>w.b:errors.append(f'out of wall {o}')
    end=o.start+TYPES[o.code][0]
 assert not errors,errors
 assert abs(18.78*22-413.16)<1e-6
 assert 1000+16780+1000==18780
 assert all(COUNTS[c]>0 for c in TYPES)
 doc=ezdxf.readfile(dxf);audit=doc.audit();assert not audit.has_errors
 assert doc.dxfversion=='AC1024' and doc.header['$INSUNITS']==4
 dims=len(doc.modelspace().query('DIMENSION'));assert dims>75
 pd=fitz.open(pdf);assert len(pd)==11
 text='\n'.join(p.get_text() for p in pd)
 assert all(c in text for c in TYPES)
 vectors=sum(len(p.get_drawings()) for p in pd);assert vectors>1000
 report={'dxf_version':doc.dxfversion,'units':'millimetres','dxf_audit_errors':len(audit.errors),'native_dimensions':dims,'entity_count':len(doc.modelspace()),'pdf_pages':len(pd),'pdf_vector_paths':vectors,'opening_instances':len(OPEN),'opening_type_counts':dict(COUNTS),'geometry_checks':'passed','construction_status':'concept design, not engineered / permit set'}
 (QA/'validation.json').write_text(json.dumps(report,indent=2));return report

def main():
 dxf,origins=make_dxf();pdf=make_pdf();makeboards();report=validate(dxf,pdf)
 # Fixed ZIP metadata and stable PDF/DXF metadata provide repeatable builds.
 zpath=OUT/'Modern_House_18.78x22m_CAD_Package.zip'
 with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in [dxf,pdf]:
   info=zipfile.ZipInfo(p.name,date_time=(2026,11,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,p.read_bytes())
 (QA/'model-register.json').write_text(json.dumps({'types':TYPES,'openings':[vars(o) for o in OPEN],'drawing_origins_mm':origins},indent=2))
 print(json.dumps(report,indent=2));print('Built',dxf.name,pdf.name,zpath.name)
if __name__=='__main__':main()
