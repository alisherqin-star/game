"""Native pixel assets for the 14 remaining regions. Pillow, fixed seeds, no resampling.

Only owns exp_* assets, expansion-scenes.json and expansion-overview.png.
The ImageGen concept is a separate reference; these PNGs are authored from code.
"""
from pathlib import Path
import hashlib
import json
import math
import random
from PIL import Image, ImageDraw, ImageFont
from pixel_nature import LOOKS, Painter, blend, curve, natural_background, refine_prop, terrain, groundcover
from pixel_craft import craft_prop

ROOT = Path(__file__).resolve().parents[1]
SPR = ROOT / 'sprites'
ART = ROOT / 'art'

# base, shade, highlight, rim, accent, light; backgrounds deliberately quieter.
THEMES = {
 'sewer': dict(name='地下水道', note='青苔砖拱、铜管和污水闸门；潮湿的村庄地下通道。', colors=['#455d54','#293d3c','#71816a','#a1ae78','#87b7a0','#d4dfab'], sky=['#152e31','#415a4d'], kind='brick', bg='arches', props=['sluice','pipe','wheel','grate','moss','bottle'], effect='drip'),
 'volcano': dict(name='火山洞', note='冷黑玄武岩衬托橙红熔流，烧焦的木梁与矿车留下探险痕迹。', colors=['#534443','#2b2933','#77605a','#a1846b','#ed7d43','#ffe4a0'], sky=['#251f32','#713c3b'], kind='basalt', bg='cavern', props=['basalt','charred','minecart','vent','ore','chain'], effect='flame'),
 'canopy': dict(name='森林高台', note='祖母绿树冠、悬空木棚与藤桥，明亮叶缘标示可行走的层次。', colors=['#65533d','#303c33','#8d7750','#91ad5c','#65ad7b','#d6df91'], sky=['#406e78','#b3cba1'], kind='root', bg='canopy', props=['treehouse','branch','fern','rope','flowers','basket'], effect='firefly'),
 'heartwood': dict(name='古树之心', note='中空巨树、环形年轮和琥珀树液，暖金光聚在树心祭台。', colors=['#69503e','#352f32','#92704a','#b49b60','#e4b766','#ffdf9b'], sky=['#242f2f','#6a6042'], kind='wood', bg='heartwood', props=['hearttree','root','sap','mushrooms','totem','vine'], effect='saplight'),
 'snow': dict(name='雪峰', note='覆雪冷杉、层叠雪山与登山营地；雪沿柔和，岩壁保持深色轮廓。', colors=['#677c94','#35475f','#9bafbd','#dce9e2','#8fc8d2','#f8f6df'], sky=['#638cae','#d8e5df'], kind='snow', bg='mountains', props=['fir','cairn','tent','sign','snowbush','fence'], effect='snowdust'),
 'ice': dict(name='冰窟', note='蓝青冰棱、冻结瀑布和霜花；深蓝裂隙区分前景冰面。', colors=['#426d8c','#26394f','#6aafc2','#b8e3de','#85d5e4','#edffed'], sky=['#172c49','#36637a'], kind='ice', bg='ice', props=['icefall','icecluster','icicle','frostflower','frozenarch','snowrock'], effect='icespark'),
 'sky': dict(name='天空遗迹', note='象牙石、失落拱门与浮岛，淡金纹样和青绿风化铜作点缀。', colors=['#9a9b89','#535f68','#c1bd9e','#e9dcad','#83c6bf','#fff2ca'], sky=['#6298b0','#e6dfbd'], kind='marble', bg='islands', props=['arch','column','sundial','urn','ivy','obelisk'], effect='mote'),
 'wind': dict(name='风之塔', note='细长塔身、风向旗与铜制风轮，开放窗洞露出高空云层。', colors=['#747986','#3d4b61','#a5a8ab','#d4c7a1','#cea373','#f4e2b4'], sky=['#6b8da9','#d9d1be'], kind='brick', bg='towers', props=['windmill','weathercock','pennant','bell','telescope','chain'], effect='ribbon'),
 'grave': dict(name='夜之墓地', note='蓝紫月雾、扭曲枯树、碑石和铁栅，灯火引导墓园小径。', colors=['#505267','#2b2e46','#79758b','#9995b3','#a9b5cd','#e4dcbe'], sky=['#202a48','#555970'], kind='soil', bg='graveyard', props=['dead_tree','tomb','mausoleum','ironfence','wilted','lantern'], effect='ghostflame'),
 'shadow': dict(name='影之祭坛', note='黑紫圣所、尖拱与蚀月石环；紫晶烛光集中在仪式中心。', colors=['#4a3e60','#231f38','#726085','#a58bb4','#c393d5','#ecd6ef'], sky=['#181b32','#473451'], kind='rune', bg='sanctum', props=['eclipse','gothicarch','candles','rune','banner','thorn'], effect='shadowflame'),
 'candy': dict(name='糖果花园', note='草莓奶油屋、香草门窗、心形饼干与蝴蝶结糖果，搭配柔和薄荷色花丛。', colors=['#d1a26d','#a47e83','#efd2a0','#f6bfd3','#a1d9ba','#fff2cd'], sky=['#9ba5ca','#f0d7cb'], kind='cake', bg='candy', props=['candyhouse','lollipop','candycane','cupcake','mintbush','wafer'], effect='sugar'),
 'abyss': dict(name='深渊海沟', note='深青海水、沉船肋骨与珊瑚，稀疏生物荧光照出遗迹轮廓。', colors=['#36586b','#152d44','#527d89','#80a8a4','#69c6bc','#c2f0d7'], sky=['#0b1e34','#174b5c'], kind='reef', bg='abyss', props=['shipwreck','coral','kelp','anemone','anchor','shell'], effect='jelly'),
 'core': dict(name='熔岩核心', note='暗红黑曜石、悬链与巨炉；比火山洞更工业化、光源更集中。', colors=['#56383c','#281f2c','#81504b','#b97653','#f49d4e','#fff0b4'], sky=['#201c2a','#683238'], kind='obsidian', bg='furnace', props=['furnace','crucible','chain','anvil','slag','pressurepipe'], effect='coreflame'),
 'altar': dict(name='进化祭坛', note='珠白石阶、八色元素宝石与天球仪，中央光环作为旅程终点。', colors=['#8b8a9c','#474761','#b5b3bd','#e1d9bc','#b9b0df','#fff3d3'], sky=['#333e66','#8b92ae'], kind='marble', bg='celestial', props=['portal','orrery','gemstand','obelisk','brazier','banner'], effect='prism'),
}

STAGE_LAYOUTS={
 'sewer':[(160,192),(321,192),(81,192),(258,192),(42,192),(345,192)],
 'volcano':[(44,192),(301,192),(124,192),(247,192),(343,192),(205,0)],
 'canopy':[(74,192),(270,192),(130,192),(164,0),(337,192),(225,192)],
 'heartwood':[(200,192),(56,192),(285,192),(331,192),(100,192),(90,0)],
 'snow':[(64,192),(312,192),(158,192),(227,192),(351,192),(270,192)],
 'ice':[(70,192),(290,192),(186,0),(134,192),(221,192),(343,192)],
 'sky':[(200,192),(55,192),(113,192),(281,192),(334,192),(353,192)],
 'wind':[(113,192),(264,192),(311,0),(216,192),(340,192),(52,0)],
 'grave':[(47,192),(135,192),(275,192),(354,192),(185,192),(218,192)],
 'shadow':[(200,192),(65,192),(315,192),(118,192),(307,0),(361,192)],
 'candy':[(200,192),(58,192),(119,192),(274,192),(327,192),(364,192)],
 'abyss':[(129,192),(29,192),(352,192),(244,192),(301,192),(210,192)],
 'core':[(127,192),(224,192),(273,0),(331,192),(49,192),(286,192)],
 'altar':[(200,192),(64,192),(288,192),(340,192),(112,192),(312,16)],
}
SKIES={
 'sewer':['#263c49','#70816a'],'volcano':['#302539','#9b6751'],
 'canopy':['#508794','#c1c9a1'],'heartwood':['#304947','#94805b'],
 'snow':['#718fb5','#d4c5b6'],'ice':['#41395e','#6e9fa9'],
 'sky':['#649da9','#e5d2ad'],'wind':['#7489ab','#dcbf9e'],
 'grave':['#2c2d50','#7c6c86'],'shadow':['#292940','#75506a'],
 'candy':['#b9e4ed','#fff0da'],'abyss':['#26354e','#326e73'],
 'core':['#30243c','#855442'],'altar':['#4e537e','#b8aeb9'],
}
for key,sky in SKIES.items():THEMES[key]['sky']=sky

ASSETS = []
ANIMATIONS = []
SCENES = {}
im = d = None
P = None

def new(w, h, color=None):
 global im, d
 im = Image.new('RGBA', (w, h), color or (0, 0, 0, 0)); d = ImageDraw.Draw(im)

def rect(box, color): d.rectangle(tuple(map(int, box)), fill=color)
def line(points, color, width=1): d.line(points, fill=color, width=width)
def poly(points, color, edge=None):
 d.polygon(points, fill=color)
 if edge: d.line(points + [points[0]], fill=edge)
def ellipse(box, color, outline=None): d.ellipse(box, fill=color, outline=outline)

def emit(theme, name, cat='deco', top=False):
 # Sparse two-pixel clusters break up large flat fills while preserving silhouettes.
 # Texturing stays inside a single painted face, so outlines and alpha stay exact.
 if cat=='deco' and not name.rsplit('_',1)[-1].isdigit():
  rng=random.Random(f'{theme}/{name}/texture');source=im.copy()
  for _ in range(im.width*im.height//(42 if theme=='candy' else 17)):
   x=rng.randrange(1,im.width-2);y=rng.randrange(1,im.height-1);c=source.getpixel((x,y))
   if c[3]!=255 or any(source.getpixel((x+dx,y+dy))!=c for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]):continue
   change=rng.choice([-12,-8,9,14]);color=tuple(max(0,min(255,v+change)) for v in c[:3])+(255,)
   d.line((x,y,x+1,y),fill=color)
 key=f'{cat}/exp_{theme}_{name}'; path=SPR/(key+'.png'); path.parent.mkdir(exist_ok=True)
 im.save(path)
 ASSETS.append(dict(id=key, region=theme, category=cat, anchor=[0,0] if cat!='deco' else [im.width//2,0 if top else im.height]))
 return key

def stone(box, colors=None):
 c=colors or P; x,y,x1,y1=box
 rect(box,c[0]);line((x,y,x1,y),c[2]);line((x,y,x,y1),c[2]);line((x,y1,x1,y1),c[1]);line((x1,y,x1,y1),c[1])

def gem(x,y,w,h,col=None):
 c=col or P[4]
 poly([(x,y+h//4),(x+w//2,y),(x+w-1,y+h//4),(x+w-2,y+h-1),(x+2,y+h-1)],c,P[1])
 poly([(x+w//2,y+2),(x+w-2,y+h//4),(x+w-3,y+h-3),(x+w//2,y+h-2)],P[2])
 line((x+w//2,y+3,x+w//2,y+h-4),P[5])

def leaf(x,y,w,h,c=None):
 color=c or P[4]
 # A canopy cluster, not a flat polygon: three overlapping leaf lobes.
 for box in [(x,y+h//3,x+w*2//3,y+h),(x+w//3,y+h//4,x+w,y+h),(x+w//5,y,x+w*4//5,y+h*4//5)]:
  ellipse(box,color,P[1])
 line((x+w//3,y+2,x+w//2+2,y+2),P[3]);line((x+2,y+h//2,x+5,y+h//2),P[2]);d.point((x+w-3,y+h//2),fill=P[3])

def masonry(x,y,w,h,step=12):
 for yy in range(y,y+h,8):
  for xx in range(x-step//2 if (yy-y)//8%2 else x,x+w,step):
   stone((max(x,xx),yy,min(x+w-1,xx+step-1),min(y+h-1,yy+7)))

def arch(x,y,w,h,gothic=False):
 # A truly transparent opening: draw stones around it, never a flat opaque cutout.
 for xx in (x,x+w-10):masonry(xx,y+18,10,h-18)
 points=[(x+5,y+21),(x+8,y+10),(x+w//2,y if gothic else y+3),(x+w-8,y+10),(x+w-5,y+21)]
 line(points,P[1],11);line(points,P[2],7);line(points,P[3],1)
 for a in range(0,181,30):
  rad=math.radians(a);cx=x+w//2+int((w/2-5)*math.cos(rad));cy=y+22-int(17*math.sin(rad))
  line((cx,cy,cx,cy+4),P[1])
 for xx in (x-2,x+w-12):stone((xx,y+h-7,xx+13,y+h-1))

def pillar(x,y,w,h):
 stone((x+3,y+6,x+w-4,y+h-6))
 for xx in range(x+5,x+w-4,4):line((xx,y+8,xx,y+h-8),P[1])
 stone((x,y,x+w-1,y+6));stone((x-2,y+h-6,x+w+1,y+h-1))

def chain(x,y,h):
 for yy in range(y,y+h,7):
  d.ellipse((x-2,yy,x+2,yy+8),outline=P[2]);line((x-1,yy+1,x-1,yy+4),P[3])

def branch(points,w=6):
 line(points,P[1],w+2);line(points,P[0],w);line([(x-1,y-1) for x,y in points],P[2],max(1,w//3))

def sprite(theme, kind):
 global P, im, d
 P=THEMES[theme]['colors']; top=kind in ('chain','rope','vine','icicle','banner','pennant')
 sizes={'sluice':(80,80),'treehouse':(96,112),'hearttree':(96,128),'fir':(64,96),'icefall':(64,112),'frozenarch':(80,80),'arch':(80,80),'windmill':(80,112),'dead_tree':(80,96),'mausoleum':(80,80),'eclipse':(80,96),'gothicarch':(64,96),'candyhouse':(96,96),'shipwreck':(96,64),'furnace':(80,96),'portal':(96,112),'orrery':(64,80)}
 w,h=sizes.get(kind,(32,48) if top else (48,48));new(w,h)
 if kind in ('arch','frozenarch','gothicarch'):
  arch(8,4,w-16,h-4,kind=='gothicarch')
  if kind=='frozenarch':
   for x in (15,27,43,57):poly([(x,16),(x+6,16),(x+2,34)],P[4]);line((x+1,17,x+2,28),P[5])
 elif kind in ('column','obelisk','totem','gemstand','rune'):
  if kind=='column':pillar(13,4,22,44)
  elif kind=='obelisk':
   poly([(14,44),(16,9),(24,0),(32,9),(34,44)],P[0],P[1]);poly([(24,2),(31,10),(32,42),(24,42)],P[2]);stone((9,42,39,47))
  elif kind=='gemstand':stone((8,39,40,47));pillar(16,24,16,20);gem(17,3,14,24)
  else:stone((13,5,34,44));stone((8,42,39,47))
  if kind not in ('gemstand','column'):
   for y in (15,23,31):line([(21,y-2),(26,y),(21,y+2)],P[4]);d.point((28,y),fill=P[3])
 elif kind in ('sluice','mausoleum'):
  masonry(8,20,64,60);arch(20,15,40,65,kind=='mausoleum')
  if kind=='sluice':
   for x in range(27,55,6):stone((x,35,x+2,77))
   rect((15,6,64,17),P[1]);stone((16,7,63,12));line((39,11,39,28),P[3],2)
   for x in range(11,69,13):leaf(x,15,8,11)
  else:
   poly([(4,23),(40,2),(75,23)],P[0],P[1]);line([(8,21),(40,6),(71,21)],P[3]);rect((36,9,43,19),P[1]);line((40,10,40,17),P[3]);line((37,13,43,13),P[3])
 elif kind in ('pipe','pressurepipe'):
  for x in (8,27):stone((x,5,x+10,39));stone((x-2,9,x+12,14));stone((x-2,31,x+12,36))
  stone((14,29,33,39));rect((11,0,15,4),P[1]);rect((30,0,34,4),P[1])
  for x in (8,27):line((x+3,16,x+3,29),P[3]);d.point((x,11),fill=P[5])
 elif kind=='wheel':
  stone((20,20,27,47));ellipse((3,4,44,45),P[1]);d.ellipse((6,7,41,42),outline=P[2],width=4)
  for a in range(0,360,45):
   r=math.radians(a);line((24,25,24+int(16*math.cos(r)),25+int(16*math.sin(r))),P[3],2)
  ellipse((20,21,28,29),P[2]);d.point((22,23),fill=P[5])
 elif kind=='grate':
  stone((3,5,44,47));rect((7,9,40,43),P[1])
  for x in range(10,40,6):rect((x,9,x+2,43),P[2]);line((x,9,x,42),P[3])
  for y in (14,35):stone((4,y,43,y+3))
 elif kind in ('moss','fern','mintbush','snowbush','flowers','wilted','frostflower','coral','kelp','thorn','ivy','mushrooms'):
  rng=random.Random(kind)
  for i in range(5):
   x=5+i*8;y=8+rng.randrange(15)
   if kind in ('mushrooms',):
    line((x,46,x,y+8),P[2],2);ellipse((x-5,y,x+7,y+9),P[1]);ellipse((x-4,y,x+6,y+5),P[4]);line((x-2,y+2,x+3,y+2),P[5])
   elif kind in ('mintbush','snowbush','moss'):
    leaf(x-5,y+8,16,25,P[2] if kind=='snowbush' else P[4])
    if kind=='snowbush':poly([(x-5,y+15),(x,y+5),(x+10,y+14),(x+7,y+18),(x+2,y+15)],P[3])
   else:
    pts=[(x,47),(x-2,y+15),(x+2,y)];line(pts,P[2],2);line([(xx-1,yy) for xx,yy in pts],P[4])
    for yy in range(y+5,41,8):
     if kind in ('coral','thorn'):line([(x,yy+7),(x-5,yy+2),(x-5,yy-3)],P[4],2);line((x,yy+4,x+5,yy),P[4],2)
     else:leaf(x-6,yy,7,4,P[2]);leaf(x,yy+3,8,4,P[4])
    if kind in ('flowers','frostflower','wilted'):
     for dx,dy in [(-3,0),(3,0),(0,-3),(0,3)]:rect((x+dx,y+dy,x+dx+2,y+dy+2),P[3])
     rect((x,y,x+2,y+2),P[5])
 elif kind in ('bottle','urn','basket','crucible'):
  if kind=='bottle':stone((19,2,28,7));poly([(19,8),(28,8),(28,18),(35,24),(35,45),(13,45),(13,24),(19,18)],P[2],P[1]);rect((16,29,32,42),P[4]);line((17,25,17,39),P[5])
  elif kind=='basket':
   d.arc((10,7,37,36),180,360,fill=P[3],width=3);stone((8,25,40,47))
   for y in range(28,46,5):line((9,y,39,y),P[1])
   for x in range(12,40,6):line((x,27,x,45),P[2])
  else:
   poly([(5,18),(42,18),(37,43),(30,47),(17,47),(10,42)],P[0],P[1]);ellipse((4,12,43,24),P[2]);ellipse((8,15,39,21),P[1]);line((13,25,17,40),P[3],2)
   if kind=='crucible':ellipse((9,17,38,21),P[4]);line((14,18,32,18),P[5])
 elif kind in ('basalt','ore','icecluster','snowrock','slag','sap','cairn'):
  if kind in ('basalt','ore','icecluster','sap'):
   for x,y,ww,hh in [(3,22,14,26),(17,3,16,45),(32,17,13,31)]:gem(x,y,ww,hh,P[4] if kind in ('ore','icecluster','sap') else P[0])
  elif kind=='cairn':
   for x,y,ww in [(6,36,37),(12,23,27),(17,12,17),(21,4,10)]:ellipse((x,y,x+ww,y+10),P[0],P[1]);line((x+3,y+2,x+ww-3,y+2),P[3])
  else:
   poly([(2,46),(8,26),(18,20),(30,24),(43,36),(46,47)],P[0],P[1]);line([(8,28),(18,23),(29,27)],P[3],2)
   if kind=='snowrock':poly([(7,30),(15,20),(28,22),(36,29),(31,33),(22,29),(16,33)],P[3])
   else:line([(12,35),(23,31),(21,40),(31,44)],P[4]);d.point((24,33),fill=P[5])
 elif kind in ('charred','dead_tree','root','branch'):
  ground=h-1;branch([(w//2,ground),(w//2-3,ground-20),(w//2+2,ground-39),(w//2-6,4)],8)
  for dx,dy in [(-1,20),(1,31),(-1,45),(1,58)]:
   if dy>h-6:continue
   branch([(w//2,ground-dy//2),(w//2+dx*15,ground-dy),(w//2+dx*24,max(3,ground-dy-10))],3)
  for dx in (-1,1):branch([(w//2,ground-12),(w//2+dx*12,ground-3),(w//2+dx*21,ground)],5)
  if kind=='branch':
   for x,y in [(0,9),(25,4),(6,22)]:leaf(x,y,18,12)
  if kind=='charred':line((w//2+1,16,w//2+1,31),P[4]);d.point((w//2+1,20),fill=P[5])
 elif kind in ('chain','rope','vine','icicle','pennant','banner'):
  if kind=='chain':chain(16,0,48)
  elif kind=='rope':
   for x in (8,24):line((x,0,x,47),P[2],2)
   for y in range(4,48,8):line((7,y,25,y),P[3],2)
  elif kind=='vine':
   for x in (6,18,25):
    line([(x,0),(x+2,18),(x-2,36),(x,47)],P[2]);
    for y in range(3,40,9):leaf(x-3,y,8,5)
  elif kind=='icicle':
   for x,y,ww in [(1,0,9),(10,0,12),(23,0,8)]:
    poly([(x,y),(x+ww,y),(x+ww//2,47-x//2)],P[2],P[1]);line((x+ww//2,y+2,x+ww//2,36-x//2),P[5])
  else:
   line((1,2,30,2),P[3],2)
   poly([(6,4),(26,4),(26,42),(16,37),(6,47)],P[0],P[1]);line((8,5,8,38),P[2])
   if kind=='pennant':line([(12,14),(21,19),(12,24),(20,29)],P[4],2)
   else:poly([(16,11),(22,22),(16,33),(11,22)],P[4]);d.point((16,17),fill=P[5])
 elif kind=='treehouse':
  branch([(63,111),(59,69),(64,26),(56,3)],12)
  for x,y in [(3,10),(19,0),(45,6),(65,17)]:leaf(x,y,29,28)
  stone((19,61,71,92));poly([(12,62),(43,37),(78,62)],P[1]);poly([(17,59),(43,41),(71,59)],P[4]);line((20,57,66,57),P[3])
  rect((48,70,61,91),P[1]);stone((26,69,39,81));rect((28,71,37,78),P[5]);line((32,71,32,78),P[1]);stone((13,92,79,97))
  for x in (20,69):line((x,98,x,111),P[2],2)
 elif kind=='hearttree':
  poly([(2,127),(18,92),(14,34),(25,0),(69,0),(79,31),(75,88),(94,127)],P[0],P[1])
  for x in (23,31,65,73):line([(x,4),(x-3,42),(x+2,81),(x-3,118)],P[2],2)
  ellipse((28,25,69,105),P[1]);ellipse((34,36,63,88),P[2]);gem(39,42,19,38)
  for x in (2,10,69,79):branch([(47,106),(x+8,118),(x,127)],7)
  for x,y in [(5,0),(34,-8),(61,3)]:leaf(x,y,31,25,P[2])
 elif kind=='fir':
  stone((29,39,35,95))
  for y,ww in [(4,22),(23,36),(43,50),(62,62)]:
   poly([(32,y),(32+ww//2,y+22),(32+ww//2-4,y+25),(32-ww//2,y+25)],P[0],P[1]);poly([(32,y),(32+ww//2-3,y+18),(38,y+16),(31,y+19),(24,y+15),(32-ww//2+4,y+20)],P[3]);line((30,y+4,25,y+12),P[5])
 elif kind=='icefall':
  for x in range(5,60,8):
   stone((x,0,x+6,111));line([(x+1,1),(x+2,39),(x,64),(x+2,108)],P[4],2)
   for y in (20+x%7,59+x%11,85):line((x,y,x+5,y-4),P[5])
  for x in (0,19,39):gem(x,87,23,25)
 elif kind in ('tent','sign','fence','ironfence'):
  if kind=='tent':
   poly([(1,46),(23,7),(46,46)],P[2],P[1]);poly([(23,9),(32,46),(14,46)],P[1]);line((23,7,1,46),P[3],2);line((23,7,46,46),P[3],2)
  elif kind=='sign':stone((21,15,25,47));stone((2,8,44,23));line((8,15,31,15),P[1]);line([(30,11),(35,15),(30,19)],P[1])
  else:
   for x in range(4,48,10):
    stone((x,13,x+2,47));poly([(x-2,15),(x+1,8),(x+4,15)],P[2])
   for y in (24,37):stone((0,y,47,y+2))
 elif kind in ('windmill','weathercock'):
  if kind=='windmill':
   masonry(27,40,26,72);poly([(23,42),(40,26),(57,42)],P[3],P[1]);rect((36,87,44,111),P[1]);cx,cy=40,34
  else:stone((21,17,25,47));cx,cy=24,15
  for a in range(0,360,90):
   rad=math.radians(a);dx,dy=math.cos(rad),math.sin(rad);sx,sy=-dy,dx;length=32 if kind=='windmill' else 21
   points=[(int(cx+dx*5),int(cy+dy*5)),(int(cx+dx*length),int(cy+dy*length)),(int(cx+dx*length+sx*6),int(cy+dy*length+sy*6)),(int(cx+dx*10+sx*3),int(cy+dy*10+sy*3))]
   poly(points,P[2],P[1]);line(points[:2],P[3])
  ellipse((cx-3,cy-3,cx+3,cy+3),P[4])
 elif kind in ('bell','lantern','brazier','candles'):
  if kind=='bell':
   arch(4,3,40,45);poly([(17,14),(30,14),(31,31),(37,36),(10,36),(16,31)],P[2],P[1]);line((19,16,19,30),P[3]);ellipse((21,35,27,41),P[4])
  elif kind=='lantern':
   stone((21,3,24,47));line((22,4,38,4),P[3],2);rect((29,11,43,31),P[1]);rect((32,14,40,28),P[4]);rect((34,16,37,25),P[5]);line((35,5,35,11),P[3])
  elif kind=='brazier':
   pillar(17,25,14,23);poly([(7,19),(41,19),(34,28),(15,28)],P[2],P[1]);gem(16,2,17,21)
  else:
   for x,y in [(8,23),(20,9),(32,18)]:stone((x,y,x+5,46));poly([(x,y-2),(x+2,y-9),(x+5,y-2)],P[4]);d.point((x+2,y-4),fill=P[5])
 elif kind in ('telescope','sundial','anvil'):
  if kind=='telescope':
   line((23,29,12,47),P[2],2);line((23,29,35,47),P[2],2);line((23,29,23,46),P[3]);poly([(6,24),(36,7),(43,18),(12,34)],P[0],P[1]);line((8,25,36,10),P[3],2);line((36,8,42,17),P[4],3)
  elif kind=='sundial':pillar(17,22,14,26);ellipse((3,13,44,28),P[2],P[1]);poly([(16,21),(27,3),(28,21)],P[3],P[1]);line((9,23,38,23),P[4])
  else:poly([(2,17),(38,17),(45,21),(35,27),(29,27),(28,38),(37,43),(37,47),(11,47),(11,42),(18,37),(18,27),(5,25)],P[2],P[1]);line((4,18,38,18),P[3]);line((20,28,20,37),P[0])
 elif kind=='tomb':
  ellipse((10,4,38,30),P[0],P[1]);stone((10,18,38,43));stone((5,42,43,47));line((24,12,24,30),P[3],2);line((17,19,31,19),P[3],2);line((17,35,30,35),P[1])
 elif kind=='eclipse':
  pillar(32,65,16,31);ellipse((6,3,74,71),P[1]);d.ellipse((8,5,72,69),outline=P[3],width=3);d.ellipse((14,11,66,63),outline=P[2],width=2);ellipse((24,21,58,55),P[4]);ellipse((29,18,61,50),P[1]);stone((16,86,64,95))
 elif kind=='candyhouse':
  stone((16,42,80,91));poly([(4,45),(48,9),(91,45)],P[1]);poly([(9,42),(48,14),(86,42)],P[4]);line([(10,43),(19,48),(27,43),(35,48),(43,43),(51,48),(59,43),(67,48),(76,43),(84,47)],P[3],4)
  for x in (26,62):ellipse((x-6,54,x+8,68),P[1]);ellipse((x-4,56,x+6,66),P[5]);line((x+1,56,x+1,66),P[0])
  stone((42,65,55,91));rect((44,68,53,90),P[1]);stone((10,91,86,95))
  for x in (18,75):
   line((x,46,x,90),P[3],4)
   for y in range(50,90,9):line((x-1,y,x+1,y+3),P[4],2)
 elif kind=='lollipop':
  line((24,20,24,47),P[3],3);ellipse((5,1,42,38),P[1]);ellipse((7,3,40,36),P[3]);
  pts=[]
  for i in range(70):
   a=i*.22;r=i*.2;pts.append((int(24+r*math.cos(a)),int(20+r*math.sin(a))))
  line(pts,P[4],3)
 elif kind=='candycane':
  d.arc((10,3,36,30),180,360,fill=P[1],width=9);d.arc((11,4,35,29),180,360,fill=P[3],width=7);line((14,17,14,47),P[3],7);line((32,17,32,25),P[3],7)
  for y in range(21,47,9):line((11,y,17,y+4),P[4],3)
 elif kind=='cupcake':
  poly([(8,30),(39,30),(35,47),(12,47)],P[0],P[1]);
  for x in range(13,36,5):line((x,32,x+1,44),P[2])
  for box in [(5,21,42,34),(10,13,38,27),(17,7,32,20)]:ellipse(box,P[3],P[1])
  ellipse((22,2,28,9),P[4]);line((13,23,16,23),P[4]);line((29,18,32,18),P[0])
 elif kind=='wafer':
  stone((11,4,37,47));
  for x in range(14,37,7):line((x,7,x,45),P[1])
  for y in range(10,46,7):line((13,y,35,y),P[2])
 elif kind=='shipwreck':
  poly([(1,29),(16,39),(80,39),(94,18),(88,53),(70,63),(26,63),(9,54)],P[0],P[1])
  for y in (42,49,56):line((16,y,82,y),P[2])
  for x in range(15,87,13):line((x,38,x+4,57),P[1],2)
  branch([(47,51),(42,6)],4);line((43,11,69,29),P[3]);poly([(45,13),(67,29),(49,25),(51,36),(46,32)],P[2]);line((11,33,88,33),P[2])
 elif kind=='anchor':
  d.ellipse((18,1,30,13),outline=P[2],width=3);line((24,12,24,40),P[2],4);line((13,20,35,20),P[3],3);line([(4,31),(9,40),(24,46),(39,40),(44,31)],P[2],4);poly([(2,27),(13,33),(5,37)],P[3]);poly([(46,27),(35,33),(43,37)],P[3])
 elif kind in ('anemone','shell'):
  if kind=='shell':
   ellipse((6,14,42,47),P[0],P[1]);
   for x in range(10,42,6):line((24,46,x,19+abs(24-x)//3),P[3],2)
  else:
   ellipse((7,36,41,47),P[0],P[1]);
   for x in range(9,42,5):line([(24,42),(x,28),(x-3,17),(x,9)],P[4],2);d.point((x,9),fill=P[5])
 elif kind=='furnace':
  masonry(10,25,60,71);masonry(27,0,27,27);arch(18,32,44,64);ellipse((25,50,55,88),P[4]);ellipse((31,63,49,88),P[5]);
  for x in range(25,56,7):stone((x,50,x+2,94))
  for y in (28,90):stone((7,y,73,y+4));
  chain(8,0,62);chain(72,0,62)
 elif kind=='portal':
  ellipse((10,1,86,87),P[1]);d.ellipse((13,4,83,84),outline=P[2],width=6);d.ellipse((21,12,75,76),outline=P[3],width=2)
  # Transparent center; the eight evolution colors belong to the pedestal design.
  d.ellipse((26,17,70,71),fill=(0,0,0,0))
  colors=['#75bada','#eed16e','#e79c70','#80b886','#acdce4','#b79ace','#8a8aaf','#dda0c2']
  for i,c in enumerate(colors):
   a=i*math.pi/4-math.pi/2;x=48+int(33*math.cos(a));y=44+int(35*math.sin(a));gem(x-4,y-6,9,13,c)
  pillar(30,83,36,24);stone((12,105,84,111))
 elif kind=='orrery':
  pillar(25,51,14,29)
  for box in [(5,7,59,52),(13,0,51,60),(1,19,63,40)]:d.ellipse(box,outline=P[3],width=2)
  gem(25,20,15,24);ellipse((9,12,17,20),P[4]);ellipse((48,40,56,48),P[5])
 elif kind=='minecart':
  for x in (10,35):ellipse((x-6,35,x+6,47),P[1]);ellipse((x-3,38,x+3,44),P[2])
  poly([(2,19),(46,19),(41,37),(8,37)],P[0],P[1]);line((4,21,44,21),P[3],2)
  for x in (12,25,38):line((x,23,x-1,34),P[1]);gem(x-7,9,11,12,P[0])
 elif kind=='vent':
  poly([(2,47),(9,27),(18,23),(31,23),(40,30),(47,47)],P[0],P[1]);ellipse((12,23,35,32),P[1]);ellipse((16,26,31,30),P[4]);line((18,28,28,28),P[5])
 else:raise ValueError(kind)
 im=craft_prop(theme,kind,im.size) or refine_prop(im,theme,kind,P);d=ImageDraw.Draw(im)
 return emit(theme,kind,top=top)

def tiles(theme, cfg):
 global im,d,P
 P=cfg['colors']
 for v in range(4):
  fill,top,wall=terrain(theme,P,cfg['kind'],v)
  for name,picture in [('fill',fill),('top',top),('wall',wall)]:
   im=picture;d=ImageDraw.Draw(im);emit(theme,f'{name}_{v}','tiles')
 new(16,16)
 d.rounded_rectangle((0,0,15,5),radius=2,fill=P[0]);line((0,1,15,1),blend(P[2],LOOKS[theme][2],.2))
 for x in (4,11):curve(d,[(x,4),(x+1,6),(x-1,8)],P[1])
 emit(theme,'platform','tiles')
 for v in range(3):
  im=groundcover(theme,P,v);d=ImageDraw.Draw(im);emit(theme,f'groundcover_{v}')


def liquids(theme,cfg):
 colors={'sewer':(54,101,83,145),'volcano':(188,70,35,255),'core':(208,76,40,255),'abyss':(18,76,95,72)}
 if theme not in colors:return None
 color=colors[theme];new(16,16,color)
 if theme in ('volcano','core'):
  for y in (5,12):line((2,y,10,y),cfg['colors'][4]);line((10,y+1,15,y+1),cfg['colors'][0])
 body=emit(theme,'liquid','tiles');frames=[]
 for phase in range(2):
  new(16,16,color);line((0,0,15,0),cfg['colors'][4]);line((2+phase*5,1,6+phase*5,1),cfg['colors'][5]);line((9-phase*4,5,13-phase*4,5),cfg['colors'][4]);frames.append(emit(theme,f'liquid_surface_{phase}','tiles'))
 a=dict(id=f'exp_{theme}_liquid',frames=frames,fps=4,loop=True);ANIMATIONS.append(a)
 return dict(body=body,animation=a['id'],x=176,y=200,w=48,h=24,overlay=theme=='abyss')

def mix(a,b,t):
 aa=tuple(bytes.fromhex(a[1:]));bb=tuple(bytes.fromhex(b[1:]));return tuple(round(x*(1-t)+y*t) for x,y in zip(aa,bb))+(255,)

def backgrounds(theme,cfg):
 global im,d,P
 P=cfg['colors']
 for layer in range(3):
  im=natural_background(theme,cfg['sky'],P,layer,cfg['bg']);d=ImageDraw.Draw(im)
  emit(theme,f'layer_{layer}','backgrounds')


def effect(theme,cfg):
 global P
 P=cfg['colors'];kind=cfg['effect'];frames=[]
 for frame in range(4):
  new(32,32)
  if theme=='candy':
   for i,(x,base_y,color) in enumerate([(7,13,'#e9aac4'),(23,23,'#b3d7c7')]):
    y=base_y-(frame+i)%4
    rect((x-2,y,x-1,y+1),color);rect((x+1,y,x+2,y+1),color)
    poly([(x-2,y+1),(x+2,y+1),(x,y+4)],color)
   x,y=16,7+(frame%2);line((x-1,y,x+1,y),'#fff1c3');line((x,y-1,x,y+1),'#fff1c3')
  elif kind in ('flame','coreflame','ghostflame','shadowflame'):
   shift=[0,2,0,-2][frame];poly([(7,29),(4,22),(9,13),(13+shift,2),(19,13),(24,9),(23,23),(20,29)],P[2]);poly([(10,28),(8,23),(14+shift,10),(18,19),(20,24),(17,28)],P[4]);poly([(13,27),(13,22),(16,17),(18,25),(16,28)],P[5])
  elif kind=='jelly':
   y=3+frame%2;ellipse((5,y,27,y+14),P[2],P[1]);d.arc((6,y+1,26,y+13),180,355,fill=P[4],width=2)
   for x in (10,16,22):line([(x,y+13),(x+frame%3-1,y+21),(x-2,y+28)],P[4]);d.point((x,y+8),fill=P[5])
  elif kind=='ribbon':
   line([(0,11),(8,8+frame),(17,14),(25,13-frame),(31,10)],P[3],2);line([(1,18),(11,20-frame),(20,17),(30,18)],P[4])
  elif kind=='drip':
   yy=frame*7;poly([(16,yy),(13,yy+5),(16,yy+7),(19,yy+5)],P[4]);d.point((15,yy+4),fill=P[5]);
   if frame==3:d.arc((5,24,27,31),0,180,fill=P[3])
  else:
   for i in range(5):
    x=4+(i*13+frame*3)%24;y=3+(i*9-frame*4)%25
    line((x-1,y,x+1,y),P[4]);line((x,y-1,x,y+1),P[4]);d.point((x,y),fill=P[5] if (i+frame)%2 else P[3])
  frames.append(emit(theme,f'{kind}_{frame}'))
 ANIMATIONS.append(dict(id='exp_'+theme+'_'+kind,frames=frames,fps=6 if 'flame' in kind else 4,loop=True))

def compose(theme,cfg,liquid):
 global im,d
 new(384,224)
 for yy in range(224):line((0,yy,383,yy),mix(*cfg['sky'],yy/223))
 for l in range(3):im.alpha_composite(Image.open(SPR/f'backgrounds/exp_{theme}_layer_{l}.png'))
 layout=[]
 # The six unique silhouettes are arranged at different heights, not on a single shelf.
 positions=STAGE_LAYOUTS[theme]
 for n,(kind,(x,y)) in enumerate(zip(cfg['props'],positions)):
  asset=next(a for a in ASSETS if a['id']==f'deco/exp_{theme}_{kind}')
  layout.append(dict(id=asset['id'],x=x,y=y))
  pic=Image.open(SPR/(asset['id']+'.png'));im.alpha_composite(pic,(x-asset['anchor'][0],y-asset['anchor'][1]))
 landmark={'volcano':('lavafall',220),'abyss':('coral_arch',291)}.get(theme)
 if landmark:
  kind,x=landmark;key=f'deco/exp_{theme}_{kind}';pic=Image.open(SPR/(key+'.png'))
  im.alpha_composite(pic,(x-pic.width//2,192-pic.height))
  layout.append(dict(id=key,x=x,y=192))
 # Uneven, low clusters settle the props into the ground rather than a bare ruler.
 for i,x in enumerate((8,35,89,129,163,247,301,352,377)):
  key=f'deco/exp_{theme}_groundcover_{(i*7)%3}'
  layout.append(dict(id=key,x=x,y=192))
  im.alpha_composite(Image.open(SPR/(key+'.png')),(x-8,176))
 platforms=[]
 for p in platforms:
  for x in range(p['x'],p['x']+p['w']*16,16):im.alpha_composite(Image.open(SPR/f'tiles/exp_{theme}_platform.png'),(x,p['y']))
 for y in range(192,224,16):
  for x in range(0,384,16):
   if liquid and not liquid['overlay'] and liquid['x']<=x<liquid['x']+liquid['w']:continue
   variant=((x//16)*7+y//16)%4;k='top' if y==192 else 'fill';im.alpha_composite(Image.open(SPR/f'tiles/exp_{theme}_{k}_{variant}.png'),(x,y))
 fx=dict(id=ANIMATIONS[-1]['frames'][0],x=180,y=188);pic=Image.open(SPR/(fx['id']+'.png'));im.alpha_composite(pic,(164,156))
 player_x={'volcano':83,'canopy':159,'heartwood':133,'wind':174,'grave':95,'sky':149,'core':183,'altar':143,'candy':151,'abyss':185}.get(theme,111)
 char=Image.open(SPR/'characters/eevee.png');im.alpha_composite(char,(player_x-char.width//2,192-char.height))
 if liquid:
  anim=next(a for a in ANIMATIONS if a['id']==liquid['animation'])
  for y in range(0 if liquid['overlay'] else liquid['y'],224,16):
   for x in range(0 if liquid['overlay'] else liquid['x'],384 if liquid['overlay'] else liquid['x']+liquid['w'],16):
    key=liquid['body'] if liquid['overlay'] or y>liquid['y'] else anim['frames'][0]
    im.alpha_composite(Image.open(SPR/(key+'.png')),(x,y))
 SCENES[theme]=dict(name=cfg['name'],description=cfg['note'],sky=cfg['sky'],palette=cfg['colors'],ground=192,props=layout,platforms=platforms,effect=dict(animation=ANIMATIONS[-1]['id'],x=180,y=188),background=f'backgrounds/exp_{theme}_layer_',surface=f'tiles/exp_{theme}_top_',fill=f'tiles/exp_{theme}_fill_',platform=f'tiles/exp_{theme}_platform')
 SCENES[theme]['atmosphere']=dict(zip(('distance','material','light','mist'),LOOKS[theme]))
 SCENES[theme]['playerX']=player_x
 if liquid:SCENES[theme]['liquid']=liquid
 return im.copy()

def main():
 panels=[]
 for theme,cfg in THEMES.items():
  tiles(theme,cfg);liquid=liquids(theme,cfg);backgrounds(theme,cfg)
  for prop in cfg['props']:sprite(theme,prop)
  extra={'volcano':('lavafall',(64,144)),'abyss':('coral_arch',(112,96))}.get(theme)
  if extra:
   global im,d
   im=craft_prop(theme,extra[0],extra[1]);d=ImageDraw.Draw(im);emit(theme,extra[0])
  effect(theme,cfg);panels.append((cfg['name'],compose(theme,cfg,liquid)))
 ART.mkdir(exist_ok=True)
 (ART/'expansion-scenes.json').write_text(json.dumps(dict(version=1,regions=SCENES,assets=ASSETS,animations=ANIMATIONS),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 font_paths=['/System/Library/Fonts/PingFang.ttc','/System/Library/Fonts/Hiragino Sans GB.ttc','/System/Library/Fonts/STHeiti Medium.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc']
 font_path=next((p for p in font_paths if Path(p).exists()),None)
 font=ImageFont.truetype(font_path,18) if font_path else ImageFont.load_default()
 sheet=Image.new('RGB',(1536,7*486),'#14282e');g=ImageDraw.Draw(sheet)
 for i,(name,pic) in enumerate(panels):
  x=(i%2)*768;y=(i//2)*486;g.text((x+16,y+7),f'{i+1:02d}  {name}',font=font,fill='#e5dbba');sheet.paste(pic.resize((768,448),Image.Resampling.NEAREST),(x,y+38))
 sheet.save(ART/'expansion-overview.png')
 print(f'Generated {len(ASSETS)} native PNGs, {len(ANIMATIONS)} animations, {len(SCENES)} region compositions.')

if __name__=='__main__':main()
