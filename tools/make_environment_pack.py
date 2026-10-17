"""Build extra scene props and parallax layers. Pillow is the only build dependency.
Pixel coordinates are authored at native resolution: no resampling or AI assets.
Only writes env_* PNGs. Does not touch characters, world, UI or index.html.
"""
from pathlib import Path
import random
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]/'sprites'
for cat in ['deco','tiles','backgrounds']: (ROOT/cat).mkdir(exist_ok=True)
I=None; D=None
O='#253735';WOOD='#6b5140';LIGHT='#aa8359';DARK='#433e35';GREEN='#527a4b'
def new(w,h):
 global I,D
 I=Image.new('RGBA',(w,h));D=ImageDraw.Draw(I)
def rect(box,c):D.rectangle(box,fill=c)
def line(points,c,w=1):D.line(points,fill=c,width=w)
def poly(points,c,edge=None):
 D.polygon(points,fill=c)
 if edge:D.line(points+[points[0]],fill=edge,width=1)
def save(name,cat='deco'):I.save(ROOT/cat/('env_'+name+'.png'))
def plank(box):
 x,y,w,h=box;rect((x,y,x+w-1,y+h-1),WOOD);line((x,y,x+w-1,y),LIGHT);line((x,y+h-1,x+w-1,y+h-1),DARK)
 for xx in range(x+5,x+w,8):line((xx,y+1,xx,y+h-2),DARK)
def leaves(cx,cy,r,seed):
 rng=random.Random(seed)
 for dx,dy,rr in [(-r//2,0,r//2),(r//2,0,r//2),(0,-r//3,r//2),(0,r//4,r//2)]:
  D.ellipse((cx+dx-rr,cy+dy-rr,cx+dx+rr,cy+dy+rr),fill='#294c3d')
  D.ellipse((cx+dx-rr+1,cy+dy-rr,cx+dx+rr-2,cy+dy+rr-4),fill='#527d4c')
 for _ in range(r*2):
  x,y=cx+rng.randrange(-r,r+1),cy+rng.randrange(-r,r+1)
  if 0<=x<I.width and 0<=y<I.height and I.getpixel((x,y))[:3]==(82,125,76):rect((x,y,x+2,y+1),'#91ac65')

# Village: a readable side-view house, split roof/door silhouettes, warm windows.
new(96,80)
rect((17,36,79,75),O);rect((19,37,77,73),'#b6aa80')
for y in (44,54,64):line((19,y,77,y),'#8d8b6b')
for x in (19,45,76):rect((x,36,x+2,74),WOOD);line((x,37,x,72),LIGHT)
rect((62,9,70,30),'#635d53');rect((61,9,71,12),'#a4997c')
poly([(4,39),(17,24),(47,5),(61,14),(91,39),(89,43),(7,43)],O)
poly([(8,37),(19,26),(47,9),(60,18),(86,37)],'#436344')
for y in range(17,38,5):
 inset=int((38-y)*1.05);line((10+inset,y,84-inset,y),'#73905a');line((11+inset,y+2,83-inset,y+2),'#36563f')
rect((12,39,85,43),WOOD);line((13,39,84,39),LIGHT)
rect((24,47,39,60),WOOD);rect((26,49,37,58),'#dfbb73');line((31,49,31,58),WOOD);line((26,53,37,53),WOOD)
rect((56,46,71,60),WOOD);rect((58,48,69,58),'#d3ad6e');line((63,48,63,58),WOOD)
rect((44,51,54,74),O);rect((46,53,52,74),'#755743');line((47,54,47,71),LIGHT);rect((51,63,51,64),'#e7c079')
rect((14,74,82,77),'#687568');line((14,74,82,74),'#a4ad85');save('village_cottage')
new(32,48);rect((13,6,16,47),WOOD);line((14,7,14,45),LIGHT);plank((3,6,25,10));plank((6,19,22,9));poly([(24,6),(30,11),(24,15)],WOOD);line((8,11,20,11),'#d6c391');line((10,23,21,23),'#d6c391');save('signpost')
new(32,32);D.ellipse((3,18,28,30),fill=O);rect((7,11,23,26),WOOD);D.ellipse((7,7,23,15),fill=LIGHT);D.ellipse((10,9,20,13),outline='#6f533b');line((15,9,15,12),DARK);line((9,16,9,25),LIGHT);poly([(8,24),(3,29),(10,27)],WOOD);poly([(22,23),(29,29),(21,27)],WOOD);save('stump')
new(32,32);plank((3,13,27,5));rect((7,18,10,31),DARK);rect((24,18,27,31),DARK);plank((4,3,25,6));rect((6,9,8,12),WOOD);rect((25,9,27,12),WOOD);save('bench')
new(32,32);rect((4,13,26,31),WOOD)
for x in (4,11,18,25):line((x,14,x,30),LIGHT)
rect((3,13,27,16),'#958064');rect((3,27,27,29),'#958064');rect((5,11,25,13),DARK);leaves(15,9,10,8);save('planter')
new(32,16)
for x in (2,15,28):rect((x,1,x+2,15),WOOD);line((x,1,x+2,1),LIGHT)
for y in (5,10):rect((0,y,31,y+2),WOOD);line((0,y,31,y),LIGHT)
save('fence')
# Large fern and berry shrub.
new(32,24)
for side in (-1,1):
 for k in range(4):
  x=15+side*(6+k*2);y=2+k*4;line([(15,23),(15+side*3,13),(x,y)],'#577e4a')
  for j in range(3):line((x-side*j,y+j*2,x-side*j+side*3,y+j*2),'#91ad62')
save('fern')
new(40,24);leaves(20,12,17,19)
for x,y in [(8,13),(17,5),(25,15),(31,9)]:rect((x,y,x+1,y+2),'#6f78a1');D.point((x,y),fill='#b5bbce')
save('berry_bush')
# Lake: repeating pier module, mooring post, canoe, lily and cattail silhouettes.
new(48,40);plank((0,7,48,7));rect((5,14,9,39),WOOD);line((5,15,5,38),LIGHT);rect((38,14,42,39),WOOD);line((38,15,38,38),LIGHT);line((8,32,39,16),DARK,2);save('pier')
new(16,32);rect((5,3,11,31),WOOD);line((6,4,6,30),LIGHT);D.ellipse((4,0,12,5),fill='#b6a07a');line((3,10,13,10),'#c3bc99',2);line((3,15,13,15),'#c3bc99',2);save('mooring_post')
new(64,24);poly([(1,6),(12,11),(52,11),(62,3),(56,19),(48,22),(13,22),(6,17)],O);poly([(4,8),(13,13),(51,13),(59,7),(54,17),(48,19),(13,19),(8,15)],WOOD);line((12,14,50,14),LIGHT);line((19,9,24,19),'#8b7051',2);line((45,1,24,20),'#c1a678',2);save('canoe')
for frame in range(3):
 new(32,16);D.ellipse((2,7,29,13),fill='#315d52');D.ellipse((3,6,28,11),fill='#69956b');poly([(17,7),(29,6),(22,11)],'#315d52')
 if frame!=1:
  for x,y in [(11,4),(14,2),(17,4)]:rect((x,y,x+2,y+3),'#d7b5b1')
  rect((14,5,16,7),'#edd6a5')
 else:rect((13,3,16,7),'#e3c4b5')
 save(f'lily_{frame}')
new(32,40)
for x,y in [(5,18),(12,6),(21,12),(27,2)]:
 line([(x,39),(x-2,y+7),(x+1,y)],'#4a7e72',2);line((x,37,x-1,y+10),'#79a793')
save('waterweed')
new(32,16);D.ellipse((3,8,28,14),fill='#516e6c')
for x,y in [(5,5),(12,2),(20,6)]:D.ellipse((x,y,x+8,y+7),fill='#90a59a');line((x+2,y+1,x+5,y+1),'#c1c7ac')
save('river_stones')
# Cave: outlined stalagmites, giant mineral cluster, bioluminescent mushrooms.
new(48,64)
for x,y,w in [(3,28,14),(16,3,17),(31,19,14)]:
 poly([(x,63),(x+1,y+8),(x+w//2,y),(x+w-1,y+8),(x+w-2,63)],'#2a4355',O)
 poly([(x+w//2,y+2),(x+w-2,y+8),(x+w-3,60),(x+w//2,61)],'#568f9d')
 line((x+w//2,y+4,x+w//2,57),'#a9d4ca')
 line((x+3,y+13,x+3,54),'#467c89')
save('crystal_cluster')
new(32,48);poly([(1,47),(8,21),(12,12),(16,33),(21,1),(27,14),(30,47)],'#314657',O);line([(9,24),(12,16),(14,34)],'#66818b');line([(22,5),(24,19),(24,40)],'#577480');save('stalagmite')
# Vertical flip is generated from authored geometry to match ceiling placement.
I=I.transpose(Image.Transpose.FLIP_TOP_BOTTOM);save('stalactite')
new(32,24)
for x,y,r in [(4,14,4),(14,4,6),(25,11,5)]:
 rect((x,y+3,x+1,23),'#4e777d');D.ellipse((x-r,y,x+r,y+5),fill='#294957');D.arc((x-r,y,x+r,y+5),180,355,fill='#8ac6bc');line((x-1,y+2,x+2,y+2),'#c1e1cc')
save('glow_mushrooms')
new(48,24);poly([(1,23),(4,14),(13,11),(17,6),(29,5),(36,11),(44,16),(46,23)],'#334d5a',O)
line([(5,15),(14,13),(18,8),(29,7)],'#6f9292');line([(28,9),(25,16),(31,20)],'#1b3345');save('boulder')
# Tower: machinery imagery only; Claude chooses any future mechanics.
new(32,32)
poly([(10,1),(21,1),(21,5),(26,6),(30,11),(27,14),(30,20),(25,25),(22,23),(20,30),(11,30),(11,26),(6,25),(1,20),(5,17),(2,11),(7,6),(10,8)],'#797580','#323344')
D.ellipse((7,7,24,24),fill='#454657');D.ellipse((10,10,21,21),fill='#a39888');D.ellipse((13,13,18,18),fill='#323344');line((12,10,19,10),'#d2bd93');save('gear')
new(32,48);rect((3,3,28,47),'#2d3042');rect((5,5,26,45),'#545468')
for x in (8,14,20):rect((x,7,x+2,42),'#30384b');line((x,7,x,42),'#93909a')
for y in (11,35):rect((4,y,27,y+3),'#8c7f74');D.point((6,y+1),fill='#e1c68d');D.point((25,y+1),fill='#e1c68d')
save('grate')
new(32,48);rect((13,15,18,43),'#535364');rect((7,42,25,47),'#77707d');line((7,42,25,42),'#b0a196')
for y in (14,20,26):rect((6,y,25,y+3),'#a28a69');line((8,y,23,y),'#d5bf84')
poly([(11,12),(15,4),(20,12),(17,17)],'#7da9ba');D.point((15,7),fill='#d4e4d5');save('coil')
new(32,32);rect((2,22,29,31),'#4a4759');line((4,22,27,22),'#999080');line((15,23,23,7),'#a6a1a2',3);rect((20,4,28,9),'#9b6a62');line((21,4,27,4),'#d5a382');save('lever')
for phase in range(4):
 new(16,32);rect((6,17,9,31),WOOD);rect((4,16,11,19),'#a18c65')
 drift=[0,1,0,-1][phase]
 poly([(4,15),(3,10),(6,7),(7+drift,1),(10,7),(12,11),(10,15)],'#b66d44')
 poly([(6,15),(5,11),(8+drift,5),(10,12),(9,15)],'#e8b972');rect((7,11,8,15),'#ffedb2');save(f'torch_{phase}')
# Seamless masonry/wood trim modules.
for name,color,edge,highlight in [('wood','#6b5140','#433e35','#b39162'),('stone','#545564','#333644','#989297')]:
 new(16,16);rect((0,0,15,15),color);line((0,0,15,0),highlight);line((0,15,15,15),edge)
 for x in (3,12):rect((x,3,x+1,4),highlight);rect((x,11,x+1,12),edge)
 save('trim_'+name,'tiles')

# Repeatable background strips. Every canopy crossing a border is wrapped.
# Layers can repeat horizontally at native width=384, with nearest filtering.
for theme in ['forest','lake','cave','tower']:
 for layer in range(3):
  new(384,224);rng=random.Random(400+layer)
  color={'forest':['#8da99c','#628a7e','#3d655e'],'lake':['#91b0ac','#6c9794','#4f7c7b'],'cave':['#182f42','#203d50','#2a4b5b'],'tower':['#252838','#303446','#404153']}[theme][layer]
  for i in range(6):
   cx=i*64+int(rng.randrange(-8,9));height=rng.randrange(35,85)
   for offset in (-384,0,384):
    x=cx+offset
    if theme in ('forest','lake'):
     base=148+layer*17
     if theme=='forest':
      rect((x+14,base-height,x+18,223),color)
      for tier in range(3):
       for row in range(8):
        w=3+row*4+tier*2;rect((x+16-w//2,base-height+tier*13+row*3,x+16+w//2,base-height+tier*13+row*3+2),color)
     else:
      for row in range(height//3):
       w=6+row*4;rect((x+16-w//2,base-height+row*3,x+16+w//2,base-height+row*3+2),color)
     rect((x,base,x+64,223),color)
    elif theme=='cave':
     poly([(x-12,0),(x+27,0),(x+16,height),(x+7,height+20)],color)
     poly([(x-15,224),(x+30,224),(x+15,224-height)],color)
    else:
     rect((x+6,0,x+47,223),color);rect((x+12,28,x+41,118),'#1e293b');rect((x+14,31,x+39,114),'#46566c')
     rect((x+26,31,x+28,114),color);rect((x+14,70,x+39,72),color);rect((x+4,123,x+49,127),'#555467')
  save(f'{theme}_layer_{layer}','backgrounds')
print('Generated environment props, animation frames and 12 repeatable parallax layers.')
