"""Hand-authored material and silhouette revisions for constructed scene props.

All details are rasterized on the original pixel grid with the original anchors.
Wood, stone, copper, glass and cloth have separate palettes, not one biome tint.
"""
import math
from PIL import Image, ImageDraw
from pixel_nature import LOOKS, Painter, blend, curve, soften


CRAFT_KINDS={
 'sluice','pipe','pressurepipe','wheel','grate','bottle','basket','urn','crucible',
 'column','obelisk','gemstand','rune','totem','sign','fence','ironfence','wafer',
 'windmill','weathercock','bell','telescope','sundial','anvil','tomb','mausoleum',
 'eclipse','candles','lantern','brazier','candyhouse','lollipop','candycane','cupcake',
 'shipwreck','anchor','shell','furnace','portal','orrery','minecart','banner','pennant',
 'rope','chain','icicle',
 'gear','coil','lever','pier','canoe','crystal','hanginglamp','lavafall','coral_arch','willow',
}


class Craft:
 def __init__(self,size,theme):
  self.im=Image.new('RGBA',size);self.d=ImageDraw.Draw(self.im);self.w,self.h=size
  self.theme=theme;self.look=LOOKS[theme]
  self.ink='#283640';self.wood='#806247';self.woodlight='#b29668';self.wooddark='#51473b'
  self.stone=blend(self.look[1],'#89938f',.4);self.stonelight=blend(self.stone,'#e9d6ad',.4);self.stonedark=blend(self.stone,'#28394e',.47)
  self.copper='#97745a';self.gold='#c5ac79';self.metal='#536776';self.light=self.look[2]
  if theme=='candy':
   self.ink='#9b7380';self.wooddark='#a77c79';self.gold='#f5d59b'

 def box(self,b,face=None,r=2,edge=True):
  x,y,x1,y1=map(round,b)
  if x1<x or y1<y:return
  face=face or self.stone
  thin=x1-x<=3 or y1-y<=3
  self.d.rounded_rectangle((x,y,x1,y1),radius=r,fill=self.ink if edge and not thin else face)
  if edge and x1-x>3 and y1-y>3:self.d.rounded_rectangle((x+1,y+1,x1-1,y1-1),radius=max(0,r-1),fill=face)
  if y1-y>5: self.d.line((x+2,y+1,x1-2,y+1),fill=blend(face,'#ead9b0',.32))
  if y1-y>4:self.d.line((x+2,y1-1,x1-2,y1-1),fill=blend(face,'#253648',.28))

 def ellipse(self,b,color,edge=None):self.d.ellipse(tuple(map(round,b)),fill=color,outline=edge)

 def plank(self,b):
  self.box(b,self.wood,1);x,y,x1,y1=map(round,b)
  for yy in range(y+3,y1,5):curve(self.d,[(x+2,yy),(x+8,yy+1),(x1-2,yy)],self.wooddark)
  if x1-x>8:self.d.point((x+3,y+2),fill=self.gold);self.d.point((x1-3,y+2),fill=self.gold)

 def masonry(self,b):
  x,y,x1,y1=map(round,b)
  self.box(b,self.stonedark,3)
  for yy in range(y+1,y1,9):
   for xx in range(x-6 if ((yy-y)//9)%2 else x,x1,14):
    a=max(x+1,xx+1);z=min(x1-1,xx+13)
    if z>a:self.box((a,yy,z,min(yy+7,y1-1)),self.stone,2,False);self.d.line((a+1,yy+1,z-1,yy+1),fill=self.stonelight)

 def arch(self,b,door=False):
  x,y,x1,y1=map(round,b);ww=x1-x
  self.d.rounded_rectangle((x,y+ww//3,x1,y1),radius=3,fill=self.stonedark)
  self.ellipse((x,y,x1,y+ww),self.stonedark)
  self.d.rounded_rectangle((x+6,y+ww//3,x1-6,y1),radius=2,fill=self.ink)
  self.ellipse((x+6,y+6,x1-6,y+ww-6),self.ink)
  self.d.arc((x+1,y+1,x1-1,y+ww-1),180,350,fill=self.stonelight,width=2)
  for xx in (x,x1-5):
   self.box((xx,y+ww//2,xx+5,y1),self.stone,1)
   for yy in range(y+ww//2+6,y1,9):self.d.line((xx+1,yy,xx+4,yy),fill=self.stonedark)
  if door:
   self.d.rounded_rectangle((x+8,y+ww//2,x1-8,y1-1),radius=3,fill=self.wooddark)
   for xx in range(x+10,x1-7,5):self.d.line((xx,y+ww//2+1,xx,y1-3),fill=self.wood)
   self.box((x+8,y1-18,x1-8,y1-15),self.copper,1)

 def rivets(self,b):
  x,y,x1,y1=map(round,b)
  for xx in (x,x1):
   for yy in (y,y1):self.d.point((xx,yy),fill=self.gold);self.d.point((xx,yy+1),fill=self.ink)

 def feet(self,y=None):
  y=self.h-7 if y is None else y;self.box((3,y,self.w-4,self.h-1),self.stone,2)

 def foliage(self,b):
  Painter(self.im,['#344b43','#293f3c','#799267','#b1bc83','#567c59','#d4d6a0'],self.theme+str(b)).foliage(b,['#30483e','#4d7450','#74905b','#acb677'])

 def post(self,x,y,h):
  self.box((x-2,y,x+3,y+h),self.wood,2);self.d.line((x-1,y+2,x-1,y+h-2),fill=self.woodlight)

 def glass(self,b,color='#72b8b8'):
  self.box(b,blend(color,self.ink,.45),3)
  x,y,x1,y1=map(round,b);self.d.rounded_rectangle((x+2,y+2,x1-2,y1-2),radius=2,fill=color)
  self.d.line((x+3,y+3,x+3,y1-4),fill='#d2e6d4')
  if x1-x>9:self.d.line((x+4,y+3,x1-4,y+3),fill='#a5d5c8')


def craft_prop(theme,kind,size):
 if kind not in CRAFT_KINDS:return None
 c=Craft(size,theme);d=c.d;w,h=size
 if kind in ('lavafall','coral_arch','willow'):
  if kind=='lavafall':
   # A dark rock frame makes the warm flow read as a landscape, not a triangle.
   pen=Painter(c.im,['#514b60','#302c40','#8c7881','#bda08b','#de9b5f','#f2d39b'],theme+'fall')
   for b in [(0,-12,29,51),(w-31,-8,w+4,46),(1,38,21,103),(w-19,40,w+4,120),(0,h-43,27,h+3),(w-28,h-39,w,h+4)]:pen.rock(b)
   flow=soften([(25,-5),(40,-5),(38,32),(42,57),(39,85),(42,h-8),(33,h),(23,h-6),(26,92),(23,66),(27,35)],2,True)
   d.polygon(flow,fill='#c77b4b');curve(d,[(29,0),(30,37),(28,68),(32,103),(29,h-4)],'#edb56c',4)
   curve(d,[(36,0),(34,42),(37,78),(34,119),(37,h-2)],'#efc784',2)
   for yy in (13,43,81,116):d.line((28,yy,36,yy+1),fill='#ffe2a2')
   for x,y in [(10,h-5),(21,h-10),(46,h-8),(54,h-4)]:c.ellipse((x,y,x+4,y+3),'#cf9d68')
  elif kind=='willow':
   pen=Painter(c.im,['#71614a','#2c493f','#9a875f','#b7bd83','#668258','#c7cc9b'],theme+'willow')
   pen.bough([(w//2-12,h-1),(w//2-3,h-24),(w//2-5,h-51),(w//2+4,h-78)],9)
   for pts in [[(w//2-3,h-46),(23,h-68),(10,h-70)],[(w//2-2,h-60),(w-24,h-77),(w-10,h-70)]]:pen.bough(pts,4)
   for box in [(4,11,47,51),(26,3,74,47),(51,17,92,59),(13,29,57,68),(45,37,84,72)]:pen.foliage(box,['#2d5147','#4e7758','#79945f','#b4bf83'])
   for i,x in enumerate((11,20,32,60,71,82,88)):
    yy=35+i%3*8;end=77+(i%4)*4
    curve(d,[(x,yy),(x-3,yy+18),(x+2,end)],'#456e52',2)
    for y in range(yy+9,end,7):d.line((x-2,y,x+2,y+2),fill='#9aaf77')
   c.foliage((29,h-12,67,h-1))
  else:
   pen=Painter(c.im,['#627d8c','#263b50','#9b9ab4','#c9c4b9','#84b7aa','#d4dfcb'],theme+'coralarch')
   pen.rock((0,h-24,39,h+5));pen.rock((w-37,h-27,w+3,h+5))
   for i,x in enumerate((17,31,w-32,w-17)):
    curve(d,[(x,h-12),(x-4,h-41),(x+3,h-65),(x-5,h-87)],'#7e8da5',4)
    for yy in (h-35,h-52,h-69):
     for dx in (-10,10):curve(d,[(x,yy+7),(x+dx,yy+2),(x+dx+dx//3,yy-8)],'#ac9ab4',3);c.ellipse((x+dx-2,yy-8,x+dx+2,yy-4),'#c8b6c5')
   curve(d,[(24,h-70),(w//2,h-89),(w-25,h-72)],'#6d9e9c',5)
   for x,y in [(43,h-76),(56,h-83),(68,h-77)]:c.ellipse((x-2,y-2,x+2,y+2),'#b2d6c7')
 elif kind in ('sluice','mausoleum','furnace'):
  if kind=='sluice':
   c.masonry((6,14,w-7,h-1));c.arch((18,13,w-19,h-1))
   for x in range(26,w-24,6):c.box((x,32,x+2,h-2),c.metal,1)
   c.box((17,9,w-18,18),c.copper,2);c.rivets((20,11,w-21,15))
   c.post(w//2,0,14);c.ellipse((w//2-7,1,w//2+7,13),c.wooddark,c.gold);d.line((w//2-5,7,w//2+5,7),fill=c.gold)
   for x,y in [(9,18),(19,13),(w-18,22),(10,h-10),(w-20,h-8)]:c.foliage((x,y,x+11,y+7))
  elif kind=='mausoleum':
   c.masonry((10,29,w-11,h-1));c.arch((23,28,w-24,h-1),True)
   roof=soften([(3,30),(12,20),(w//2,5),(w-13,20),(w-4,30)],2)
   d.polygon(roof,fill=c.stonedark);curve(d,[(7,28),(23,17),(w//2,11),(w-22,18),(w-8,28)],c.stonelight,3)
   c.ellipse((w//2-6,17,w//2+6,28),c.metal,c.gold);d.line((w//2,19,w//2,25),fill=c.gold)
   for x in (13,w-18):c.box((x,35,x+5,h-6),c.stone,2)
   c.foliage((1,h-10,22,h-1));c.foliage((w-22,h-8,w-1,h-1))
  else:
   c.masonry((12,31,w-12,h-2));c.box((26,0,w-25,34),c.metal,4)
   for yy in (7,24):c.box((23,yy,w-22,yy+5),c.copper,2)
   c.arch((20,36,w-20,h-3));c.ellipse((27,48,w-27,h-8),'#a45139')
   c.ellipse((31,61,w-31,h-9),'#edba68');c.ellipse((35,73,w-34,h-10),'#ffe1a1')
   for x in range(27,w-24,7):c.box((x,54,x+2,h-5),c.metal,1)
   for yy in (33,h-9):c.box((8,yy,w-8,yy+5),c.copper,2);c.rivets((11,yy+2,w-11,yy+3))
   for x in (5,w-10):c.box((x,37,x+5,h-13),c.metal,2)
 elif kind in ('pipe','pressurepipe'):
  for x,yy in [(6,8),(27,0)]:
   c.box((x,yy,x+11,h-11),c.metal,5);d.line((x+3,yy+4,x+3,h-14),fill='#8ca29f')
   for y in (yy+6,h-20):c.box((x-2,y,x+13,y+5),c.copper,2);c.rivets((x,y+2,x+11,y+3))
  c.box((12,h-18,34,h-7),c.metal,5);d.line((16,h-16,31,h-16),fill='#91aba8')
  c.ellipse((16,15,29,28),c.ink,c.gold);c.ellipse((19,18,26,25),'#d8c9a3');d.line((23,22,24,19),fill=c.ink)
  if theme=='core':c.ellipse((9,4,15,6),'#d39b62')
 elif kind in ('wheel','grate','ironfence','fence','wafer','sign'):
  if kind=='wheel':
   c.post(w//2,20,h-20);c.ellipse((4,5,w-5,h-6),c.ink,c.copper);d.ellipse((7,8,w-8,h-9),outline=c.gold,width=3)
   for a in range(0,360,60):r=math.radians(a);curve(d,[(w/2,h/2),(w/2+math.cos(r)*10,h/2+math.sin(r)*10),(w/2+math.cos(r+.1)*17,h/2+math.sin(r+.1)*17)],c.copper,2)
   c.ellipse((w//2-4,h//2-4,w//2+4,h//2+4),c.metal,c.gold)
  elif kind=='grate':
   c.box((2,4,w-3,h-1),c.copper,4);c.box((5,7,w-6,h-4),c.ink,3)
   for x in range(8,w-6,5):c.box((x,8,x+2,h-5),c.metal,1)
   for yy in (15,h-14):c.box((3,yy,w-4,yy+3),c.copper,1);c.rivets((5,yy+1,w-6,yy+2))
  elif kind in ('fence','ironfence'):
   for x in range(4,w,10):
    if kind=='fence':c.post(x,13+(x%3),h-14-(x%3));c.box((x-2,12,x+3,17),c.woodlight,2)
    else:c.box((x-1,11,x+1,h-1),c.metal,1);c.ellipse((x-2,6,x+2,11),c.copper)
   for yy in (24,36):c.box((0,yy,w-1,yy+3),c.wood if kind=='fence' else c.metal,1)
   if kind=='fence':c.foliage((1,h-8,19,h-1))
  elif kind=='wafer':
   c.box((10,5,w-10,h-1),'#e1bc84',7)
   for yy in range(13,h-4,8):d.line((13,yy,w-13,yy),fill='#bb936d');d.line((13,yy+1,w-13,yy+1),fill='#ffe3ad')
   for x in range(17,w-13,8):d.line((x,9,x,h-4),fill='#caa579')
   c.ellipse((18,18,24,24),'#fff0d6');c.ellipse((24,18,30,24),'#fff0d6');d.polygon([(18,22),(30,22),(24,29)],fill='#fff0d6')
   c.ellipse((5,h-10,21,h-2),'#edc7a1');c.ellipse((26,h-8,41,h-1),'#d7b2df')
  else:
   c.post(w//2,17,h-18);c.plank((3,7,w-4,25));d.line((10,15,w-13,15),fill='#d1c393');curve(d,[(w-15,11),(w-10,15),(w-15,19)],'#d1c393');c.foliage((2,h-9,20,h-1))
 elif kind in ('column','obelisk','gemstand','totem','rune'):
  if kind=='column':
   c.box((14,9,w-15,h-6),c.stone,4);d.line((17,12,17,h-9),fill=c.stonelight);d.line((w-18,12,w-18,h-9),fill=c.stonedark)
   for x in range(21,w-16,4):d.line((x,12,x,h-10),fill=blend(c.stone,c.stonedark,.38))
   c.box((10,4,w-11,12),c.stonelight,3);c.box((8,h-7,w-9,h-1),c.stone,3);c.foliage((1,h-12,21,h-1))
  elif kind=='obelisk':
   pts=[(15,h-5),(17,10),(w//2+2,2),(w-15,13),(w-14,h-5)]
   d.polygon(soften(pts,1,True),fill=c.stone,outline=c.stonedark);curve(d,[(21,11),(21,26),(20,h-8)],c.stonelight,2);c.feet()
   for yy in (19,27,35):curve(d,[(25,yy-2),(29,yy),(25,yy+2)],'#81aaa3')
   c.foliage((6,h-10,21,h-1))
  elif kind=='gemstand':
   c.box((17,24,w-18,h-7),c.stone,3);c.feet();c.box((11,23,w-12,29),c.copper,3)
   d.polygon(soften([(17,17),(21,5),(28,8),(32,17),(26,23),(20,22)],1,True),fill='#77adae',outline=c.ink);curve(d,[(23,8),(21,15),(23,19)],'#d7e6cc',2)
  else:
   c.box((12,5,w-12,h-5),c.wood if kind=='totem' else c.stone,5);c.feet()
   for yy in (16,25,34):curve(d,[(20,yy-2),(26,yy),(22,yy+3),(29,yy+2)],'#b0bb91' if kind=='totem' else '#b99cc5')
   c.foliage((2,h-12,21,h-1))
 elif kind in ('bottle','basket','urn','crucible','shell'):
  if kind=='bottle':
   c.box((19,2,29,10),c.wood,2);c.glass((16,8,32,24));c.glass((10,18,38,h-2),'#6eaaa2');c.ellipse((15,30,33,41),'#9cae7d');d.line((17,31,29,31),fill='#d4d4a0');c.box((17,22,31,29),'#d1c5a1',2)
  elif kind=='basket':
   d.arc((9,8,39,37),180,360,fill=c.woodlight,width=3);c.box((7,25,41,h-1),c.wood,5)
   for yy in (30,36,42):d.line((10,yy,38,yy),fill=c.wooddark);d.line((11,yy+1,37,yy+1),fill=c.woodlight)
   for x in (14,23,32):d.line((x,27,x+2,h-3),fill=c.woodlight)
   c.foliage((12,17,34,28))
  elif kind=='shell':
   c.ellipse((6,13,42,h),'#b799a6',c.ink)
   for x in range(11,42,6):curve(d,[(24,h-2),(x,31),(x,21)],'#e0c3b6',2)
   c.ellipse((18,h-8,31,h-1),'#d4b9a8')
  else:
   d.polygon(soften([(4,19),(9,38),(16,46),(33,46),(40,37),(44,19)],2,True),fill=c.copper if kind=='crucible' else '#899d9b',outline=c.ink)
   c.ellipse((4,13,44,26),c.gold if kind=='crucible' else '#b5c1ae',c.ink);c.ellipse((9,17,39,23),c.ink)
   curve(d,[(12,27),(14,35),(18,40)],'#e2d3ac',2)
   if kind=='crucible':c.ellipse((10,18,38,22),'#e9a45e');d.line((17,19,30,19),fill='#ffe1a0')
 elif kind in ('windmill','weathercock','bell','telescope','sundial','anvil'):
  if kind=='windmill':
   d.polygon(soften([(23,h),(27,47),(34,35),(48,37),(54,48),(58,h)],1,True),fill=c.stone,outline=c.stonedark)
   for yy in range(58,h-3,8):d.line((28,yy,53,yy),fill=c.stonedark)
   c.arch((33,h-28,49,h-1),True);c.box((25,48,56,53),c.wood,3);cx,cy=41,35
  elif kind=='weathercock':c.post(24,15,h-16);cx,cy=24,15
  elif kind=='bell':
   for x in (7,39):c.post(x,5,h-6)
   c.plank((3,3,45,10));c.ellipse((16,14,32,27),c.copper,c.ink);d.polygon(soften([(16,21),(14,31),(9,36),(39,36),(34,31),(32,21)],1,True),fill=c.copper,outline=c.ink);curve(d,[(19,20),(18,26),(16,31)],c.gold,2);c.ellipse((21,35,27,42),c.gold);c.box((8,35,40,38),c.gold,2);c.foliage((0,h-9,20,h-1))
  elif kind=='telescope':
   for x in (10,24,38):curve(d,[(24,27),(x,44),(x,h-1)],c.woodlight,2)
   d.polygon(soften([(5,22),(34,7),(41,17),(12,34)],1,True),fill=c.copper,outline=c.ink);curve(d,[(9,23),(21,16),(34,10)],c.gold,2);c.ellipse((31,8,42,19),'#5d909b',c.gold);d.point((35,11),fill='#d7e9d2')
  elif kind=='sundial':
   c.box((18,24,30,h-6),c.stone,3);c.feet();c.ellipse((3,15,45,30),c.stone,c.ink);c.ellipse((6,15,42,25),c.stonelight)
   d.polygon(soften([(18,23),(28,5),(30,23)],1,True),fill=c.copper);curve(d,[(10,21),(24,25),(38,20)],c.gold)
  else:
   c.box((12,38,37,h-1),c.wood,3);d.polygon(soften([(2,17),(35,16),(46,21),(32,29),(30,37),(17,37),(17,28),(6,26)],1,True),fill=c.metal,outline=c.ink);curve(d,[(5,19),(22,18),(38,20)],'#a5b2aa',2);c.rivets((17,40,33,44))
  if kind in ('windmill','weathercock'):
   length=31 if kind=='windmill' else 20
   for a in range(0,360,90):
    r=math.radians(a+.15);ux,uy=math.cos(r),math.sin(r);vx,vy=-uy,ux
    pts=[(cx+ux*5,cy+uy*5),(cx+ux*length,cy+uy*length),(cx+ux*length+vx*7,cy+uy*length+vy*7),(cx+ux*9+vx*4,cy+uy*9+vy*4)]
    d.polygon(soften(pts,1,True),fill='#d5c49e',outline=c.wooddark);curve(d,[(cx+ux*7,cy+uy*7),(cx+ux*(length-2),cy+uy*(length-2))],c.woodlight)
   c.ellipse((cx-4,cy-4,cx+4,cy+4),c.copper,c.ink);d.point((cx-1,cy-1),fill=c.gold)
 elif kind in ('tomb','candles','lantern','brazier'):
  if kind=='tomb':
   c.box((10,8,38,h-5),c.stone,8);c.feet();c.ellipse((17,12,31,26),c.stonedark);d.line((24,15,24,23),fill=c.stonelight);d.line((20,19,28,19),fill=c.stonelight)
   for yy in (31,35):d.line((18,yy,30,yy),fill=c.stonedark)
   c.foliage((2,h-10,21,h-1))
  elif kind=='candles':
   for x,y in [(7,25),(20,12),(33,21)]:
    c.box((x,y,x+6,h-4),'#c9b6b0',2);d.line((x+2,y+3,x+2,y+8),fill='#e3cfc0');c.ellipse((x-1,y-7,x+6,y+1),'#dbae85');c.ellipse((x+1,y-5,x+4,y-1),'#f4deb0')
   c.box((3,h-5,44,h-1),c.copper,2)
  elif kind=='lantern':
   curve(d,[(15,h-1),(16,9),(20,3),(32,3),(37,8)],c.metal,3);c.box((27,11,43,34),c.copper,4);c.glass((30,15,40,30),'#dbba7b');c.box((25,10,45,14),c.gold,2);c.box((26,31,44,35),c.gold,2);d.line((35,15,35,30),fill=c.copper);c.foliage((3,h-10,24,h-1))
  else:
   c.box((18,27,30,h-5),c.stone,3);c.feet();c.ellipse((6,20,42,31),c.copper,c.ink);c.box((10,24,38,28),c.gold,2);d.polygon(soften([(15,22),(17,12),(24,3),(28,14),(34,22)],1,True),fill='#d9ae83');c.ellipse((20,15,29,24),'#f8deac')
 elif kind in ('candyhouse','lollipop','candycane','cupcake'):
  if kind=='candyhouse':
   c.box((15,44,w-16,h-4),'#ebbc83',8)
   for yy in (57,70,83):d.line((20,yy,w-21,yy),fill='#d5a47c')
   roof=soften([(5,46),(18,31),(43,18),(65,22),(82,34),(91,46)],2)
   d.polygon(roof,fill='#f1a1bd',outline='#be829b');curve(d,[(9,44),(25,30),(44,23),(64,27),(85,44)],'#ffe2e9',4)
   for x,y in [(15,44),(29,43),(43,44),(58,44),(73,45)]:c.ellipse((x-4,y,x+5,y+5),'#fff0d6')
   for x,y,color in [(28,33,'#fff1cc'),(38,29,'#f9d6df'),(59,32,'#b7dbc4'),(68,37,'#fff0cf')]:
    d.line((x,y,x+2,y),fill=color);d.point((x+1,y-1),fill=color)
   # Strawberry on the roof, and a heart plaque instead of a face-like facade.
   c.ellipse((43,10,53,21),'#e984a3');curve(d,[(44,11),(48,14),(53,10)],'#8fb68c',2)
   d.point((46,16),fill='#ffe8b7');d.point((50,17),fill='#ffe8b7')
   c.ellipse((44,45,49,50),'#dc87a4');c.ellipse((49,45,54,50),'#dc87a4');d.polygon([(44,48),(54,48),(49,54)],fill='#dc87a4')
   for x in (19,w-23):
    c.box((x,49,x+5,h-6),'#fff1d3',2)
    for yy in range(53,h-8,9):d.line((x+1,yy,x+4,yy+3),fill='#e9a4b8',width=2)
   c.box((30,63,46,h-5),'#dca1b3',7);d.line((33,72,33,87),fill='#f6c7d3');c.ellipse((40,77,43,80),'#fff0ba')
   c.box((55,60,75,76),'#fff3cf',5);d.rounded_rectangle((58,63,72,73),radius=3,fill='#b8dcd5');d.line((65,63,65,73),fill='#fff2d5')
   d.line((59,64,62,64),fill='#f6f4de');d.point((59,65),fill='#f6f4de')
   c.box((53,76,77,80),'#e3b888',2)
   for x in (58,66,73):c.ellipse((x-2,73,x+2,77),'#9ec8a1');c.ellipse((x-1,71,x+1,74),'#efabc0')
   c.ellipse((4,h-9,25,h-1),'#a3d8ac');c.ellipse((70,h-10,94,h-1),'#a9d9b3');c.box((3,h-4,w-4,h-1),'#e8c18d',2)
  elif kind=='lollipop':
   c.box((22,21,26,h-1),'#fff3d1',2);c.ellipse((5,1,42,38),'#cb95a9');c.ellipse((7,3,40,36),'#ffd1c3')
   pts=[]
   for i in range(85):a=i*.22;r=i*.16;pts.append((24+r*math.cos(a),20+r*math.sin(a)))
   curve(d,pts,'#e9a1b5',3);d.arc((10,6,36,32),195,290,fill='#fff3dc',width=2)
   d.polygon([(19,37),(24,39),(20,43),(18,41)],fill='#e7b4c6');d.polygon([(25,39),(30,37),(31,41),(27,43)],fill='#e7b4c6')
  elif kind=='candycane':
   d.arc((10,3,36,30),180,360,fill='#c49aaa',width=10);d.arc((11,4,35,29),180,360,fill='#fff4da',width=8);c.box((10,17,18,h-1),'#fff4da',3);c.box((29,17,36,27),'#fff4da',3)
   for yy in range(21,h,9):curve(d,[(11,yy),(14,yy+1),(17,yy+4)],'#edabc0',3)
   c.ellipse((16,5,22,9),'#edabc0');c.ellipse((29,8,34,14),'#edabc0')
   d.polygon([(8,29),(14,32),(9,36),(6,34)],fill='#a9d5be');d.polygon([(15,32),(21,29),(23,34),(18,36)],fill='#a9d5be')
  else:
   d.polygon(soften([(7,30),(40,30),(35,47),(13,47)],1,True),fill='#dfa04d',outline=c.ink)
   for x in (15,23,31):d.line((x,34,x+1,44),fill='#ffe176')
   for b in [(5,23,42,35),(10,16,38,29),(16,9,33,23)]:c.ellipse(b,'#f5b3cd','#c58da9')
   c.ellipse((22,4,29,11),'#e990a8');d.point((24,5),fill='#fff0c4');d.line((13,27,17,27),fill='#9dd4b3');d.line((28,19,31,19),fill='#ffe6a4')
   curve(d,[(23,4),(26,6),(29,3)],'#9ebf94',2)
 elif kind in ('portal','orrery','eclipse'):
  if kind=='portal':
   cx,cy=w//2,45
   for b,col,thick in [((10,2,w-10,88),c.stonedark,8),((13,5,w-13,85),c.stonelight,4),((21,13,w-21,77),c.copper,2)]:d.ellipse(b,outline=col,width=thick)
   colors=['#79b7c5','#dfc47a','#d59678','#8db68a','#b2d5d7','#b49cc5','#8e97b4','#d1a0b9']
   for i,col in enumerate(colors):
    a=i*math.pi/4-math.pi/2;x=cx+round(34*math.cos(a));y=cy+round(37*math.sin(a));c.ellipse((x-5,y-5,x+5,y+5),c.copper);c.ellipse((x-3,y-4,x+3,y+3),col);d.point((x-1,y-2),fill='#f4e5c3')
   c.box((29,84,w-29,h-8),c.stone,4);c.box((17,h-9,w-17,h-5),c.copper,3);c.box((10,h-5,w-10,h-1),c.stone,2)
   for x in (32,42,52,62):d.line((x,89,x,h-11),fill=c.stonedark)
  elif kind=='orrery':
   c.box((25,52,39,h-6),c.stone,3);c.feet();c.ellipse((23,20,41,42),'#92b7bf',c.gold)
   for b in [(4,7,60,53),(13,1,51,60),(1,20,63,41)]:d.ellipse(b,outline=c.copper,width=3);d.arc(b,180,300,fill=c.gold,width=1)
   for x,y,col in [(9,14,'#b4a0c6'),(50,42,'#d4b982'),(42,7,'#95baa7')]:c.ellipse((x-4,y-4,x+4,y+4),col,c.ink);d.point((x-1,y-2),fill='#f3dfb7')
  else:
   c.box((w//2-6,65,w//2+6,h-6),c.stone,3);c.feet()
   c.ellipse((6,3,w-6,73),c.stonedark);d.ellipse((9,6,w-9,70),outline=c.copper,width=3);d.ellipse((15,12,w-15,64),outline='#9c8eae',width=2);c.ellipse((24,22,w-22,56),'#c2acc4');c.ellipse((30,18,w-18,51),'#383950')
   for x in (11,w-15):c.box((x,65,x+4,h-9),c.metal,2)
 elif kind in ('shipwreck','minecart','anchor'):
  if kind=='shipwreck':
   hull=soften([(1,29),(14,39),(77,39),(94,19),(88,51),(71,63),(27,63),(9,54)],2,True)
   d.polygon(hull,fill=c.wooddark,outline=c.ink)
   for yy in (42,49,56):curve(d,[(13,yy),(39,yy+3),(72,yy+2),(88,yy-3)],c.wood,2)
   for x in (16,30,43,58,72,84):curve(d,[(x,38),(x+1,48),(x+5,58)],'#9a8b68',2)
   curve(d,[(47,52),(45,29),(42,4)],c.woodlight,4);curve(d,[(43,9),(57,16),(72,27)],'#b1b49a');d.polygon(soften([(45,11),(68,26),(53,23),(53,35),(47,31)],1,True),fill='#7f9d9a');c.foliage((65,49,94,64))
  elif kind=='minecart':
   for x in (11,36):c.ellipse((x-6,35,x+6,47),c.ink,c.copper);c.ellipse((x-2,39,x+2,43),c.gold)
   d.polygon(soften([(2,19),(46,19),(41,37),(8,37)],1,True),fill=c.metal,outline=c.ink);c.box((2,18,46,22),c.copper,2);c.rivets((10,26,38,31))
   for x,y in [(10,10),(21,6),(32,10)]:c.ellipse((x-5,y,x+9,y+12),'#5f5869','#303648');d.line((x-2,y+2,x+4,y+2),fill='#9a8985')
  else:
   d.ellipse((18,1,30,13),outline=c.copper,width=3);curve(d,[(24,11),(23,29),(24,43)],c.metal,5);curve(d,[(4,31),(11,41),(24,46),(37,41),(44,31)],c.copper,4);c.box((12,18,36,22),c.metal,2);d.line((24,13,24,35),fill='#a1aaa2')
 elif kind in ('gear','coil','lever','pier','canoe','crystal','hanginglamp'):
  if kind=='gear':
   cx,cy=w//2,h//2;rr=min(w,h)//2-5
   for a in range(0,360,45):
    r=math.radians(a);x=cx+round(math.cos(r)*rr);y=cy+round(math.sin(r)*rr)
    c.box((x-3,y-3,x+3,y+3),c.metal,2)
   c.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),c.metal,c.ink);d.ellipse((cx-rr+3,cy-rr+3,cx+rr-3,cy+rr-3),outline=c.copper,width=3)
   c.ellipse((cx-5,cy-5,cx+5,cy+5),c.ink,c.gold);d.arc((cx-rr+2,cy-rr+2,cx+rr-2,cy+rr-2),190,295,fill='#a7b2a4',width=1)
  elif kind=='coil':
   c.box((19,21,29,h-7),c.metal,3);c.feet()
   for yy in (21,29,37):c.ellipse((9,yy,39,yy+8),c.copper,c.ink);d.arc((11,yy+1,37,yy+6),180,350,fill=c.gold,width=2)
   c.glass((18,4,30,24),'#82b5c0');c.ellipse((21,7,26,12),'#dfecdb')
  elif kind=='lever':
   c.box((4,h-13,w-5,h-1),c.metal,4);c.rivets((8,h-9,w-9,h-5));c.ellipse((17,h-24,29,h-10),c.copper,c.ink)
   curve(d,[(24,h-15),(29,h-28),(35,9)],'#a9b0a2',3);c.box((29,4,42,12),'#a87c66',3);d.line((32,6,38,6),fill='#d5ad83')
  elif kind=='pier':
   for x in (8,w-10):c.post(x,12,h-13)
   curve(d,[(8,h-6),(w//2,25),(w-9,18)],c.wooddark,3)
   c.plank((0,5,w-1,15))
   for x in range(6,w,10):d.line((x,7,x+1,13),fill=c.wooddark)
   for x in (8,w-10):d.line((x-2,19,x+2,19),fill='#c3ba94')
  elif kind=='canoe':
   pts=soften([(1,5),(11,11),(w-15,11),(w-2,2),(w-7,h-8),(w-16,h-3),(15,h-3),(7,h-8)],2,True)
   d.polygon(pts,fill=c.wooddark,outline=c.ink);curve(d,[(4,7),(16,15),(w-17,15),(w-4,6)],c.woodlight,2)
   curve(d,[(13,16),(w//2,19),(w-14,16)],c.wood)
   curve(d,[(w//2-9,h-5),(w//2+5,8),(w-12,0)],'#bfa77e',2)
  elif kind=='crystal':
   colors=['#a294be','#c1a4ba','#8f9fb9'] if theme=='shadow' else ['#7fa9b5','#a496bb','#8dbcae']
   for i,(xx,yy,ww) in enumerate([(3,24,14),(16,3,17),(32,17,13)]):
    hh=h-yy;pts=soften([(xx,yy+9),(xx+ww*.45,yy),(xx+ww-1,yy+8),(xx+ww-2,h-2),(xx+2,h-1)],1,True)
    d.polygon(pts,fill=colors[i],outline='#35495b');curve(d,[(xx+ww*.43,yy+5),(xx+ww*.43,yy+21),(xx+ww*.35,h-6)],'#cad9d0',2)
    curve(d,[(xx+2,yy+14),(xx+3,h-8)],'#567a91')
  else:
   curve(d,[(w//2,0),(w//2-4,7),(w//2,12)],c.copper,2);c.box((10,12,w-10,h-7),c.copper,5);c.glass((14,16,w-14,h-11),'#d9bb80');c.box((8,10,w-8,15),c.gold,3);c.box((9,h-11,w-9,h-6),c.gold,2);d.line((w//2,16,w//2,h-12),fill=c.copper)
 elif kind in ('banner','pennant','chain','rope','icicle'):
  if kind in ('banner','pennant'):
   c.box((1,0,w-2,4),c.copper,2)
   cloth=soften([(5,5),(w-6,5),(w-5,h-9),(w//2,h-5),(5,h-1)],1,True)
   d.polygon(cloth,fill='#77627f' if theme!='wind' else '#ad8b77',outline=c.ink);curve(d,[(7,7),(8,22),(7,h-8)],'#b09aa6')
   curve(d,[(w//2,11),(w//2-4,20),(w//2+3,21),(w//2,31)],c.gold,2)
   for yy in (14,25):d.line((w-9,yy,w-8,yy+7),fill='#564e68')
  elif kind=='chain':
   for yy in range(0,h,7):d.ellipse((w//2-3,yy,w//2+3,yy+9),outline=c.metal,width=2);d.line((w//2-2,yy+1,w//2-2,yy+4),fill=c.gold)
  elif kind=='rope':
   for x in (7,w-8):curve(d,[(x,0),(x+1,h//2),(x,h-1)],c.woodlight,2)
   for yy in range(5,h,9):c.plank((6,yy,w-7,yy+3))
  else:
   for x,hh in [(2,h-7),(12,h-1),(24,h-17)]:
    pts=soften([(x,0),(x+7,0),(x+6,hh//2),(x+3,hh)],1,True);d.polygon(pts,fill='#92b7c3',outline='#48677e');curve(d,[(x+2,3),(x+3,hh//2),(x+3,hh-4)],'#d9e5dc')
 # Clustered wear is applied only after silhouette and material painting.
 Painter(c.im,[c.stone,c.stonedark,c.stonelight,c.gold,c.copper,c.light],theme+kind+'craft').grain(w*h//(38 if theme=='candy' else 19))
 return c.im
