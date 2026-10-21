"""Title A/B built from the game's pixel assets; no generated illustration.

384x224 native pixels, integer sprite scales and hard-edged colour clusters.
Two independent compositions: village departure and a lakeside picnic overlook.
"""
from pathlib import Path
import random,math,json,hashlib
from PIL import Image,ImageDraw,ImageFont
from pixel_nature import blend,curve,soften
ROOT=Path(__file__).resolve().parents[1];W,H=384,224

def ancient_oak():
 """Independently authored landmark, not a scaled forest-tree sprite.

 Three registered layers: far foliage, ancient wood and near foliage.
 All outlines and texture clusters are rasterized at the game's native scale.
 """
 rng=random.Random(308);layers={k:Image.new('RGBA',(W,H)) for k in ('back','wood','front')}
 wood=layers['wood'];d=ImageDraw.Draw(wood)
 edge='#354b42';shade='#555d4c';bark='#80775e';light='#a39773';gold='#b7ae80'
 # Upright, weight-bearing limbs rise into the crown rather than sprawling sideways.
 branches=[([(65,114),(54,77),(32,48),(8,24),(-12,10)],29),
           ([(73,105),(91,65),(123,37),(160,17),(199,-7)],31),
           ([(72,83),(70,48),(82,18),(96,-12)],27),
           ([(116,43),(155,37),(189,25),(220,7),(243,-10)],17),
           ([(37,53),(12,63),(-12,68)],14)]
 def tapered(pts,w,col,offset=0,extra=0):
  line=soften(pts,3)
  for i,(a,b) in enumerate(zip(line,line[1:])):
   ww=max(1,round(w*(1-.70*i/max(1,len(line)-2)))+extra)
   d.line([(a[0],a[1]+offset),(b[0],b[1]+offset)],fill=col,width=ww)
 for pts,w in branches:
  tapered(pts,w,edge,extra=3);tapered(pts,w,shade,-1)
  tapered(pts,w-6,bark,-2);tapered(pts,max(2,w//6),light,-w//5)
 # A broad, near-vertical bole and short buttresses give the oak a calm, solemn mass.
 trunk=[(15,206),(32,194),(40,176),(43,152),(42,125),(44,99),
        (43,78),(49,59),(66,46),(83,51),(96,67),(97,91),
        (93,119),(96,145),(100,167),(109,184),(126,195),(141,201),
        (122,204),(105,199),(94,187),(99,202),(113,210),(96,211),
        (79,197),(72,184),(66,194),(60,205),(46,211),(32,212),(43,198)]
 d.polygon(soften(trunk,2,True),fill=edge)
 inner=[(25,205),(40,190),(46,171),(49,147),(48,122),(50,98),
        (49,79),(54,63),(67,52),(80,57),(90,70),(91,92),
        (87,117),(89,143),(94,166),(104,186),(123,199),
        (105,194),(90,180),(90,198),(99,205),(84,194),(74,177),
        (65,183),(58,200),(45,207),(49,193)]
 d.polygon(soften(inner,2,True),fill=bark)
 # Long, restrained bark planes replace the yellow stripes and eye-like knot.
 for pts in [
  [(56,71),(63,57),(67,59),(61,83),(62,107),(58,132),(59,157),(53,180),(43,197),(48,174),(51,151),(51,125),(55,99)],
  [(76,66),(82,70),(80,98),(78,123),(83,148),(84,166),(79,157),(73,132),(73,108)]]:
  d.polygon(soften(pts,2,True),fill=light)
 d.polygon(soften([(85,65),(91,78),(86,110),(85,139),(91,166),(101,186),(90,179),(81,155),(79,131),(81,104)],2,True),fill=shade)
 # Short roots settle into the earth; tapered ends no longer read as long tentacles.
 for pts,w in [([(55,173),(43,189),(25,199),(9,202)],8),
               ([(89,174),(103,188),(119,196),(135,200)],8),
               ([(73,184),(82,198),(95,207),(109,211)],7),
               ([(56,181),(51,196),(41,208)],7)]:
  curve(d,pts,edge,w+2);curve(d,[(x,y-1) for x,y in pts],bark,w)
  curve(d,[(x,y-2) for x,y in pts],light,1)
 # Quiet vertical fissures preserve the sense of age without a face or busy scratches.
 for pts in [[(63,83),(61,104),(65,120)],[(72,104),(70,130),(74,148)],
             [(55,137),(54,157),(49,177)],[(86,91),(82,113),(85,130)],
             [(65,154),(68,172),(64,184)],[(91,152),(92,168),(99,182)]]:
  curve(d,pts,shade,1)
 # A few slender, clipped grain marks keep the broad planes tactile at native scale.
 for _ in range(25):
  xx=rng.randrange(48,92);yy=rng.randrange(77,178)
  if wood.getpixel((xx,yy))[:3] not in [(128,119,94),(163,151,115)]:continue
  length=rng.randrange(4,12)
  curve(d,[(xx,yy),(xx-1,yy+length//2),(xx,yy+length)],shade if xx%3 else gold,1)
 # A worn oak-leaf seal, carved rather than painted onto the bark.
 d.line((68,128,68,144),fill=shade,width=2)
 d.polygon([(68,128),(72,131),(70,133),(73,136),(70,137),(71,140),(68,143),(65,140),(66,137),(63,136),(66,133),(65,131)],fill=shade)
 d.line((68,131,68,140),fill=gold);d.line((66,134,68,136),fill=gold);d.point((70,137),fill=gold)
 # Moss is confined to the buttress hollows; it never washes across the bole.
 for pts in [[(44,169),(40,184),(31,194)],[(99,177),(108,188),(119,194)],[(53,196),(46,205)]]:
  curve(d,pts,'#5d7755',3);curve(d,[(x-1,y-1) for x,y in pts],'#8b9a67',1)

 # Rebuild the lower bole and roots as one continuous silhouette, with no stacked tubes.
 d.rectangle((0,160,W,H),fill=(0,0,0,0))
 root=[(43,157),(96,157),(98,173),(105,185),(119,195),(132,201),
       (119,204),(103,198),(88,185),(89,199),(103,212),(88,210),
       (74,197),(69,185),(59,201),(43,213),(31,215),(40,200),
       (48,183),(34,193),(19,204),(4,206),(21,193),(36,179)]
 d.polygon(soften(root,1,True),fill=edge)
 innerroot=[(46,160),(93,160),(95,175),(102,187),(119,199),(105,195),
            (85,178),(83,197),(94,207),(78,193),(70,176),(57,198),
            (38,211),(47,194),(55,174),(33,190),(14,201),(29,189),(41,178)]
 d.polygon(soften(innerroot,1,True),fill=bark)
 # Each raised rib continues from a trunk plane, then narrows into buried wood.
 for pts in [[(51,157),(58,157),(57,174),(47,192),(35,207),(42,193),(49,175)],
             [(75,157),(80,158),(80,179),(87,195),(95,206),(82,197),(74,180)],
             [(89,160),(93,161),(96,178),(108,190),(120,199),(105,192),(92,178)]]:
  d.polygon(soften(pts,1,True),fill=light)
 for pts in [[(61,165),(65,176),(58,191)],[(84,169),(88,182),(100,195)],[(43,182),(34,193),(23,199)]]:
  curve(d,pts,shade,2)
 # Broad, weathered bark plates and a healed seam convey age at readable scale.
 for x,y,w,h in [(50,91,7,19),(72,81,8,23),(57,121,6,18),(82,114,5,22),(69,148,6,17)]:
  d.polygon([(x,y),(x+w-2,y-2),(x+w,y+5),(x+w-1,y+h),(x+2,y+h+2),(x,y+h-4)],fill=bark)
  d.line([(x,y+1),(x-1,y+h//2),(x+2,y+h)],fill=shade)
  d.line((x+2,y+h,x+w-1,y+h-1),fill=light)
 curve(d,[(69,65),(65,79),(67,96),(74,111)],shade,2)
 curve(d,[(71,66),(68,81),(70,95),(76,107)],light,1)
 # Broken lichen colonies follow shaded hollows, never stripe the entire tree.
 for x,y in [(43,170),(42,179),(34,192),(94,176),(105,191),(45,203)]:
  d.polygon([(x-2,y),(x,y-2),(x+3,y),(x+2,y+3),(x-1,y+4)],fill='#607752')
  d.line((x,y,x+1,y-1),fill='#91a16b')

 def leaf_mass(layer,points,base,lit,highlight,seed):
  target=layers[layer];g=ImageDraw.Draw(target);r=random.Random(seed)
  mask=Image.new('1',(W,H));md=ImageDraw.Draw(mask);md.polygon(soften(points,2,True),fill=1)
  g.polygon(soften(points,2,True),fill=base)
  # Unequal linked terraces replace stacked circular canopy blobs.
  for j in range(15):
   x=r.randrange(max(0,min(p[0] for p in points)),max(1,min(W,max(p[0] for p in points))))
   y=r.randrange(max(0,min(p[1] for p in points)),max(1,min(H,max(p[1] for p in points))))
   if not mask.getpixel((x,y)):continue
   patch=[(x,y),(x+4,y-3),(x+10,y-2),(x+17,y-4),(x+21,y-1),(x+27,y+1),(x+22,y+5),(x+14,y+6),(x+7,y+5),(x+2,y+3)]
   # Draw on a clipped temporary layer so silhouettes remain deliberately stepped.
   tile=Image.new('RGBA',(W,H));td=ImageDraw.Draw(tile);td.polygon(patch,fill=lit)
   tile.putalpha(Image.composite(tile.getchannel('A'),Image.new('L',(W,H)),mask));target.alpha_composite(tile)
  g=ImageDraw.Draw(target)
  for j in range(18):
   x=r.randrange(max(0,min(p[0] for p in points)),max(1,min(W,max(p[0] for p in points))))
   y=r.randrange(max(0,min(p[1] for p in points)),max(1,min(H,max(p[1] for p in points))))
   if not mask.getpixel((x,y)):continue
   for dx,dy in [(0,0),(1,0),(2,-1),(3,-1),(4,0),(2,1)]:
    xx,yy=x+dx,y+dy
    if 0<=xx<W and 0<=yy<H and mask.getpixel((xx,yy)):g.point((xx,yy),fill=highlight if j%3 else lit)

 leaf_mass('back',[(-10,-10),(74,-10),(104,3),(142,-8),(171,3),(207,-6),(243,0),(273,-8),(311,3),(350,-4),(395,1),(395,19),(366,26),(347,19),(321,33),(297,27),(271,42),(245,32),(218,43),(192,37),(161,54),(136,45),(111,63),(88,55),(61,72),(29,62),(-10,78)],'#354f43','#4d6850','#71885b',9)
 leaf_mass('front',[(-10,-9),(30,-9),(55,0),(84,-7),(105,5),(137,1),(155,13),(145,31),(120,34),(113,52),(91,49),(85,66),(63,62),(50,82),(24,74),(9,91),(-10,85)],'#3c5c43','#597948','#8c9e5d',12)
 leaf_mass('front',[(108,-9),(171,-9),(197,3),(232,-7),(248,4),(243,21),(220,22),(208,33),(182,29),(163,40),(147,30),(128,34),(118,17)],'#405e46','#657b50','#93a169',17)
 leaf_mass('front',[(257,-8),(307,-8),(333,1),(360,-5),(390,0),(390,15),(372,21),(351,16),(335,28),(314,23),(304,36),(288,29),(271,31),(270,15)],'#3e5b45','#617b50','#92a167',21)
 leaf_mass('front',[(102,44),(119,40),(128,46),(142,45),(148,54),(139,60),(144,65),(134,70),(123,66),(117,75),(105,69),(108,61),(98,57)],'#426144','#69814c','#9ca866',28)
 # A few recognisably lobed oak leaves hang beyond the crown's edge.
 g=ImageDraw.Draw(layers['front'])
 for x,y in [(19,92),(90,68),(114,56),(158,46),(212,38),(272,36),(319,32),(362,23)]:
  g.line((x,y-7,x+1,y-2),fill='#61794a')
  g.polygon([(x+1,y-3),(x+3,y-2),(x+2,y),(x+4,y+1),(x+2,y+3),(x+2,y+5),(x,y+6),(x-2,y+4),(x-1,y+2),(x-3,y),(x-1,y-1)],fill='#91a15e')
  g.line((x+1,y-2,x,y+4),fill='#c0bd7e')
 # Sparse hanging lichen suggests centuries of undisturbed growth.
 for x,y,n in [(12,79,12),(101,56,9),(149,34,10),(185,27,7)]:
  g.line((x,y,x,y+n),fill='#58785b');g.line((x+1,y+2,x+1,y+n-2),fill='#84966c')
  for yy in range(y+3,y+n,4):g.point((x-1,yy),fill='#a2ac7a')
 # Separate ending-only flower layer. The normal title never displays it.
 bloom=Image.new('RGBA',(W,H));g=ImageDraw.Draw(bloom);r=random.Random(1095)
 for _ in range(210):
  x,y=r.randrange(2,W-4),r.randrange(3,77)
  if not layers['front'].getpixel((x,y))[3] or r.random()<.3:continue
  g.line((x,y-1,x,y+2),fill='#eadac0');g.line((x-1,y,x+2,y),fill='#f6ebd2')
  g.point((x,y),fill='#cbb581');g.point((x+1,y-1),fill='#fff1d8')
 layers['blossom']=bloom
 return layers

OAK=ancient_oak()

def make_departure():
 night=False
 rng=random.Random(701);im=Image.new('RGB',(W,H));d=ImageDraw.Draw(im)
 top,bottom=('#3c536d','#80979b') if night else ('#a6bfb8','#edd4aa')
 # Broad quiet colour bands leave room for the logo; no simulated photographic glow.
 for y in range(H):d.line((0,y,W,y),fill=blend(top,bottom,round(min(1,y/148)*24)/24))
 def polygon(points,c):d.polygon(points,fill=c)
 def sprite(name,x,y,scale=1,flip=False,night_tint=False,far=False):
  pic=Image.open(ROOT/'sprites'/name).convert('RGBA')
  if flip:pic=pic.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if night_tint or far:
   for py in range(pic.height):
    for px in range(pic.width):
     r,g,b,a=pic.getpixel((px,py))
     if a:
      if night_tint:r,g,b=blend((r,g,b),'#48616b',.30)
      if far:r,g,b=blend((r,g,b),'#91a59a' if not night else '#5a7b85',.30)
      pic.putpixel((px,py),(r,g,b,a))
  if scale!=1:pic=pic.resize((round(pic.width*scale),round(pic.height*scale)),Image.Resampling.NEAREST)
  im.paste(pic,(x,y),pic)
 def actor(name,cx,ground,flip=False,on_cloth=False):
  # Exact 2x replication retains every original face pixel and palette entry.
  source=Image.open(ROOT/'sprites'/name).convert('RGBA')
  source=source.crop(source.getbbox())
  if flip:source=source.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  pic=source.resize((source.width*2,source.height*2),Image.Resampling.NEAREST)
  w,h=pic.size;x=cx-w//2;y=ground-h
  # Contact shadows touch the feet; their colour belongs to the receiving surface.
  shadow=('#766f67' if night else '#998b71') if on_cloth else ('#4e6650' if night else '#64794e')
  d.ellipse((cx-w//4-2,ground-1,cx+w//4,ground+2),fill=shadow)
  im.paste(pic,(x,y),pic)
  return (x,y,w,h)
 # Cloud banks use the existing pixel cloud silhouettes.
 if night:
  for x,y in [(183,18),(211,35),(267,13),(310,37),(359,12),(334,73),(223,70),(379,53)]:
   d.point((x,y),fill='#e0d8b1')
  d.line((287,30,289,30),fill='#d9d6b1');d.line((288,29,288,31),fill='#d9d6b1')
  d.ellipse((347,23,361,37),fill='#ddd8b4');d.ellipse((343,20,357,34),fill='#495f75')
 else:
  sprite('deco/cloud_small.png',170,37,far=True)
  sprite('deco/cloud_small.png',286,60,far=True)
  # The sun is only a cream disc behind the far trees, never an HDR flare.
  d.ellipse((350,37,365,52),fill='#efddac')
 # Distant wooded slopes, lake and tiny native village roofs.
 polygon([(0,128),(24,116),(54,120),(88,109),(121,117),(148,111),(177,118),(210,108),(244,116),(276,109),(311,117),(347,106),(384,116),(384,178),(0,178)],'#6d8b89' if night else '#8ca99b')
 polygon([(0,149),(23,139),(66,147),(99,134),(143,142),(178,132),(214,138),(249,130),(293,141),(342,128),(384,137),(384,184),(0,184)],'#54797c' if night else '#779888')
 # One continuous rolling meadow replaces the disconnected lake/platform shelves.
 # Paint terrain before buildings, so feet and foundations stay on their own plane.
 meadow='#6d8462' if night else '#9cab79'
 polygon(soften([(105,151),(141,146),(181,137),(217,140),(247,139),(278,146),(315,145),(353,140),(384,143),(384,224),(0,224),(0,159),(57,150)],2,True),meadow)
 # A narrow stream winds behind the village; its banks share the meadow contour.
 water=soften([(384,148),(355,151),(336,157),(326,166),(338,175),(369,184),(384,191),(384,205),(354,193),(324,180),(313,168),(320,157),(341,149),(367,145)],2,True)
 polygon(water,'#607d80' if night else '#91b2aa')
 for x,y,w in [(351,153,10),(330,161,7),(329,171,8),(351,183,12),(373,194,7)]:
  d.line((x,y,x+w,y),fill='#8fa6a0' if night else '#c8d0b0')
 # Gentle foreground folds overlap instead of meeting in hard cut seams.
 polygon(soften([(-10,183),(30,177),(69,182),(112,185),(151,177),(186,174),(219,180),(251,176),(279,180),(310,190),(342,195),(384,201),(395,230),(-10,230)],3,True),'#566f54' if night else '#819565')
 # A far hamlet has a connected lane, orchard and shared grassy foundations.
 curve(d,[(178,157),(197,151),(220,149),(243,147),(264,152)],'#819078' if night else '#b4b58b',3)
 sprite('deco/env_village_home_elder.png',186,104,.5,night_tint=night,far=True)
 sprite('deco/env_village_home_merchant.png',237,108,.5,night_tint=night,far=True)
 d.rectangle((274,109,282,139),fill='#718887' if night else '#8a9d93')
 d.polygon([(272,109),(274,105),(276,105),(276,100),(280,100),(280,105),(283,106),(285,109)],fill='#607b7d' if night else '#7b908a')
 d.line((275,112,275,136),fill='#92a4a0' if night else '#b3b9a1')
 for yy in (114,125):d.rectangle((278,yy,279,yy+4),fill='#c7bb8c' if night else '#667d78')
 # Ground shadow and a curving doorstep lane tie the near home into the clearing.
 d.ellipse((275,153,349,174),fill='#5a7357' if night else '#74875c')
 sprite('deco/env_village_home_guide.png',272,93,night_tint=night,far=True)
 sprite('deco/forest_tree_1.png',340,73,night_tint=night,far=True)
 # Low bushes overlap the foundations rather than leaving pasted rectangular bases.
 for x,y in [(190,144),(218,147),(247,146),(279,161),(338,162),(358,170)]:
  col='#647d5c' if night else '#8e9f69'
  d.polygon([(x-5,y),(x-4,y-3),(x-1,y-4),(x+1,y-2),(x+4,y-3),(x+6,y),(x+4,y+2),(x-3,y+2)],fill=col)
  d.line((x-3,y-2,x,y-3),fill='#82956c' if night else '#b1ba82')
 # A cover has a foreground, not a horizontal cutaway of a platform level.
 # Broken tufts frame the same native-pixel clearing without exposing tiled dirt.
 for x in list(range(0,105,3))+list(range(170,W,3)):
  yy=219+round(math.sin(x*.11)*2);h=2+(x*7)%5
  d.line((x,yy,x-1,yy-h),fill='#4e674f' if night else '#5e7c50')
  if x%2:d.point((x-1,yy-h),fill='#71875b' if night else '#a0ad6e')
 # Hand placed leaf/grass clusters keep the central clearing open.
 for x,y in [(8,184),(28,199),(62,203),(86,215),(183,207),(202,189),(259,211),(284,194),(325,207),(365,188),(380,216)]:
  col='#7c9166' if night else '#a3b278';d.line((x,y,x+3,y),fill=col);d.line((x+1,y-1,x+2,y-1),fill=col)
 # A continuous S-shaped lane narrows toward the cottage door, without detached forks.
 route=[(143,230,44),(151,211,36),(178,195,28),(215,185,20),(253,179,14),(287,171,9),(306,162,6)]
 for _ in range(3):
  sm=[route[0]]
  for a,b in zip(route,route[1:]):
   sm.extend([tuple(.75*u+.25*v for u,v in zip(a,b)),tuple(.25*u+.75*v for u,v in zip(a,b))])
  sm.append(route[-1]);route=sm
 left=[];right=[]
 for i,(x,y,w) in enumerate(route):
  a=route[max(0,i-1)];b=route[min(len(route)-1,i+1)];dx=b[0]-a[0];dy=b[1]-a[1];length=max(.1,math.hypot(dx,dy))
  nx=-dy/length;ny=dx/length
  left.append((round(x+nx*w/2),round(y+ny*w/2)));right.append((round(x-nx*w/2),round(y-ny*w/2)))
 road=left+right[::-1];polygon(road,'#c1ac83')
 # Fine edge chips and broad worn centres follow the same curve.
 for i in range(6,len(route)-4,8):
  x,y,w=route[i];x=round(x);y=round(y)
  d.line((x-2,y,x+3,y-1),fill='#d7c198')
 for side in [left,right]:
  for i,(x,y) in enumerate(side):
   if i%8==0 and 173<y<223:
    d.line((x-1,y,x+1,y-1),fill='#829562');d.point((x,y-2),fill='#9caa6e')
 # Small patches follow the slope instead of a uniform dotted texture.
 for x,y in [(19,186),(38,213),(205,207),(229,195),(267,210),(305,201),(370,218)]:
  polygon([(x-10,y),(x-7,y-2),(x+3,y-3),(x+12,y),(x+6,y+2),(x-5,y+2)],'#607953' if night else '#8fa269')
 # Cottage garden shares the slope and path palette: low edging, herbs, warm flowers.
 for j in range(11):
  x=259+j*3;y=166+round(math.sin(j*.5)*2)
  d.line((x,y,x+2,y),fill='#8c9580' if night else '#bbb594')
  if j%2==0:
   d.line((x+1,y-1,x+1,y-5),fill='#567654' if night else '#6d8954')
   d.point((x,y-4),fill='#a7a481' if night else '#debb83')
   d.point((x+2,y-5),fill='#b4a89a' if night else '#deb2a4')
 # Low masonry bridge, diagonally crossing the stream between two actual banks.
 polygon([(320,177),(340,167),(351,172),(330,184)],'#4e6d6e' if night else '#6e9188')
 stone='#86917e' if night else '#aaa68a';lit='#a9ad91' if night else '#d2c5a1';seam='#5b7267' if night else '#7d876e'
 polygon([(314,174),(341,161),(350,167),(324,181)],stone)
 polygon([(324,181),(350,167),(350,173),(344,177),(340,175),(334,179),(332,184),(324,188)],seam)
 polygon([(325,181),(349,168),(349,171),(343,174),(339,173),(333,177),(330,183),(325,185)],stone)
 # Raised far curb and worn paving courses share a single vanishing direction.
 d.line([(314,174),(341,161),(350,167)],fill=lit,width=2)
 d.line((324,181,350,167),fill=lit)
 for x,y in [(320,171),(326,168),(333,165),(339,163)]:d.line((x,y,x+8,y+6),fill=seam)
 d.line((318,177,345,164),fill=seam)
 for x,y in [(315,176),(324,184),(349,171)]:
  d.line((x,y,x+3,y-1),fill='#66815a' if night else '#83955d',width=2)
 # Shared tree shade follows the footprint, under roots and props rather than over them.
 polygon(soften([(18,184),(39,172),(77,170),(107,180),(131,197),(115,209),(70,214),(26,207),(6,198)],2,True),'#526b50' if night else '#6d8153')
 # Familiar village materials are staged in depth, at their native pixel scale.
 sprite('deco/env_village_home_elder.png',-8,88,night_tint=night)
 # Village joinery: thick rails, capped posts, one diagonal brace and grass at the feet.
 fence_dark='#59634f' if night else '#706447';fence_mid='#8a8970' if night else '#ac9064';fence_lit='#aeab88' if night else '#d1b17d'
 d.polygon([(174,168),(239,168),(235,171),(171,171)],fill='#586f50' if night else '#748755')
 for j,xx in enumerate(range(181,236,7)):
  top=153+(j%3==1)
  d.polygon([(xx,top+1),(xx+1,top),(xx+3,top+1),(xx+3,168),(xx,168)],fill=fence_mid)
  d.line((xx,top+2,xx,167),fill=fence_lit)
  d.point((xx+2,161),fill=fence_dark)
 for yy in [155,162]:
  d.polygon([(174,yy),(238,yy+1),(238,yy+4),(174,yy+3)],fill=fence_dark)
  d.line((175,yy,237,yy+1),fill=fence_lit)
  d.line((175,yy+1,237,yy+2),fill=fence_mid)
 for j,xx in enumerate([175,205,237]):
  top=150+(j%2);base=169
  d.polygon([(xx-2,top+2),(xx,top),(xx+3,top+2),(xx+3,base),(xx-2,base)],fill=fence_dark)
  d.rectangle((xx-1,top+3,xx+1,base-1),fill=fence_mid)
  d.line((xx-1,top+3,xx-1,base-1),fill=fence_lit)
  d.line((xx-2,top+2,xx+3,top+2),fill=fence_lit)
  for yy in [157,164]:d.point((xx+1,yy),fill='#4c5948')
  d.line((xx-3,base,xx-1,base-3),fill='#6a8554');d.line((xx+3,base,xx+4,base-2),fill='#91a569')
 sprite('deco/env_bench.png',79,143,night_tint=night)
 # A short washing line beside the back cottage and two residents give the village life.
 d.line((155,130,155,145),fill='#7c785a');d.line((182,130,182,143),fill='#7c785a')
 curve(d,[(155,132),(168,134),(182,132)],'#d2c198',1)
 for x,y,c in [(159,133,'#d4bd9a'),(169,134,'#839c95'),(176,133,'#c2a39a')]:
  d.rectangle((x,y,x+4,y+6),fill=c);d.point((x+1,y-1),fill='#837759')
 def resident(name,cx,base,flip=False):
  pic=Image.open(ROOT/'sprites/npcs'/name).convert('RGBA');pic=pic.crop(pic.getbbox())
  if flip:pic=pic.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  d.ellipse((cx-7,base-1,cx+7,base+2),fill='#748455')
  im.paste(pic,(cx-pic.width//2,base-pic.height),pic)
 resident('merchant.png',211,182)
 resident('gardener.png',265,180,True)
 # A pair of produce boxes and a watering can explain what the residents are doing.
 for x,y in [(223,180),(231,177)]:
  d.rectangle((x,y-5,x+7,y),fill='#9b825a');d.line((x,y-4,x+7,y-4),fill='#c9ad76')
  for xx in [x+2,x+5]:d.point((xx,y-6),fill='#b9b76d')
 d.rectangle((276,176,280,179),fill='#879b8d');d.line((280,176,283,174),fill='#aeb9a1')
 for x,y in [(250,179),(256,177),(284,178)]:
  d.line((x,y,x,y-4),fill='#687f4d');d.line((x-1,y-5,x+1,y-5),fill='#dfbd8f')
 # The landmark is made of independent native-pixel layers, never scaled.
 for key in ('back','wood','front'):
  pic=OAK[key].copy()
  if night:
   for yy in range(H):
    for xx in range(W):
     r,g,b,a=pic.getpixel((xx,yy))
     if a:pic.putpixel((xx,yy),(*blend((r,g,b),'#48616b',.24),a))
  im.paste(pic,(0,0),pic)
 if night:
  # Tiny registered points of cool light; no blur, halo or change of silhouette.
  d=ImageDraw.Draw(im)
  for xx,yy in [(68,132),(68,136),(67,140),(54,173),(96,181)]:
   d.point((xx,yy),fill='#a6c4a7')
 d=ImageDraw.Draw(im)
 # Soil rises over root ends; sparse blades finish the ground/root/grass depth order.
 ground='#566f54' if night else '#819565'
 for pts in [[(5,202),(15,200),(24,203),(20,207),(3,207)],[(32,211),(44,208),(53,212),(48,216),(28,216)],[(111,201),(126,199),(135,202),(137,207),(119,207)]]:
  polygon(pts,ground)
 for x,y in [(17,203),(37,211),(47,210),(118,202),(126,202)]:
  d.line((x,y+1,x-1,y-3),fill='#617b51' if night else '#6d8852')
  d.line((x,y,x+2,y-2),fill='#899c65')
 d=ImageDraw.Draw(im)
 d.line((114,163,115,184),fill='#74674e',width=2)
 d.polygon([(104,160),(122,159),(125,161),(121,166),(104,166)],fill='#b59c70')
 d.line((106,161,120,161),fill='#d0b889')
 # Tiny oak-leaf carving repeats Penny's cane, with no written spoiler.
 d.line((112,162,115,164),fill='#6c8056');d.point((115,162),fill='#81975e')
 sprite('deco/env_stump.png',-8,168,night_tint=night)
 sprite('deco/env_fern.png',5,173,night_tint=night)
 sprite('deco/env_berry_bush.png',-17,199,night_tint=night)
 sprite('deco/env_river_stones.png',327,197,night_tint=night)
 sprite('deco/env_fern.png',354,193,night_tint=night)
 # Sparse native flowers act as framing, not a carpet of decorative noise.
 for x,y in [(28,189),(68,212),(184,190),(204,217),(365,207)]:
  d.line((x,y,x,y-4),fill='#627d54');d.line((x-1,y-5,x+1,y-5),fill='#c8ad9b' if night else '#e3baa0');d.point((x,y-6),fill='#e8d5a4')
 # Repeated long-grain shapes on the left avoid the former solid, empty lawn.
 for x,y in [(2,215),(35,221),(74,219),(174,218),(308,220),(344,218)]:sprite('deco/forest_plant_1.png',x,y-11,night_tint=night)
 d=ImageDraw.Draw(im)
 # The elder stands on a flat patch beside the roots, with the feet below all wood.
 d.ellipse((58,211,103,220),fill='#788b59')
 actor('npcs/elder.png',80,216)
 actor('npcs/guide.png',132,188)
 actor('characters/eevee.png',176,200)
 # Fallen leaves and a small trail of stepping stones lead toward the open village.
 for x,y in [(108,200),(127,192),(187,207)]:
  d.line((x,y,x+2,y-1),fill='#c4ad77')
 for x,y in [(65,216),(94,216),(116,188),(159,200)]:
  d.line((x,y+1,x-1,y-2),fill='#80945c');d.point((x+1,y-1),fill='#a1ac6c')
 return im

def make_lakeside():
 """A separate lakeside overlook: no road or village clearing beneath the picnic."""
 im=Image.new('RGB',(W,H));d=ImageDraw.Draw(im);rng=random.Random(4206)
 def poly(pts,c):d.polygon(pts,fill=c)
 def sprite(name,x,y,scale=1,flip=False):
  p=Image.open(ROOT/'sprites'/name).convert('RGBA')
  if flip:p=p.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if scale!=1:p=p.resize((p.width*scale,p.height*scale),Image.Resampling.NEAREST)
  im.paste(p,(x,y),p)
 for y in range(H):d.line((0,y,W,y),fill=blend('#253f58','#728e94',round(min(1,y/140)*18)/18))
 # Clear sky on the right is reserved for the title; the moon belongs to the lake view.
 for x,y in [(17,29),(56,17),(93,31),(147,16),(173,40),(204,19),(247,12),(288,17),(339,20),(368,47),(214,82),(27,82)]:
  d.point((x,y),fill='#b5c5b3')
 d.ellipse((188,24,206,42),fill='#e6dfbb');d.ellipse((183,21,200,38),fill='#334c63')
 # Layered wooded ridgelines, with no repeated foreground village houses.
 poly([(0,112),(30,100),(55,107),(89,92),(117,101),(147,98),(176,112),(213,102),(243,113),(280,102),(315,107),(353,94),(384,104),(384,153),(0,153)],'#456878')
 poly([(0,132),(39,118),(78,123),(118,115),(163,125),(203,120),(246,131),(283,123),(322,128),(360,117),(384,124),(384,156),(0,156)],'#3c6270')
 # The lake fills the middle distance; reflections are horizontal, sparse and stepped.
 d.rectangle((0,136,W,H),fill='#547e87')
 for y in range(136,H):
  d.line((0,y,W,y),fill=blend('#547e87','#355d70',round((y-136)/88*12)/12))
 for i in range(52):
  x=rng.randrange(W);y=rng.randrange(139,195);length=rng.randrange(3,13)
  d.line((x,y,x+length,y),fill='#73969b' if i%3 else '#436e7c')
 for y,w in [(141,10),(146,15),(152,9),(158,21),(164,17)]:
  d.line((197-w//2,y,197+w//2,y),fill='#b0b7a2')
 # Larger geometry is rasterized directly, retaining one-pixel bark and leaf edges.
 def T(p):return (round(98+(p[0]-95)*1.35),round(143+(p[1]-143)*1.25))
 def tree_poly(pts,c):poly([T(p) for p in pts],c)
 def tree_line(pts,fill,width=1):
  if isinstance(pts[0],(int,float)):pts=[pts[:2],pts[2:]]
  d.line([T(p) for p in pts],fill=fill,width=max(1,round(width*1.25)))
 def tree_point(p,fill):d.point(T(p),fill=fill)
 def tree_curve(pts,c,width=1):curve(d,[T(p) for p in pts],c,max(1,round(width*1.25)))
 # The ancient oak is now seen across the water, complete in silhouette and immense.
 tree_poly([(33,137),(58,129),(82,126),(111,126),(139,133),(152,139),(134,144),(64,145),(30,142)],'#2f5358')
 tree_poly([(45,137),(65,131),(112,130),(138,137),(127,139),(56,140)],'#718773')
 tree_poly([(72,137),(83,121),(87,95),(89,73),(100,68),(109,84),(106,111),(113,130),(129,137),(110,136),(100,125),(93,137)],'#536861')
 for pts in [[(96,101),(75,78),(56,67)],[(98,96),(118,69),(139,60)],[(98,85),(97,57),(104,41)]]:
  tree_curve(pts,'#536861',7);tree_curve([(x+1,y-1) for x,y in pts],'#7d8d79',2)
 # Broad oak boughs remain visible through deliberately placed gaps in the crown.
 for pts in [[(95,101),(81,84),(55,76)],[(100,96),(119,81),(145,74)],[(96,87),(94,65),(83,52)]]:
  tree_curve(pts,'#405e56',6);tree_curve([(x+1,y-1) for x,y in pts],'#798a70',1)
 # The old bole has a split plane, weathered plates and heavy supporting roots.
 tree_poly([(88,94),(94,83),(96,109),(92,126),(81,136),(76,137),(88,119)],'#7b8a73')
 tree_poly([(102,88),(107,94),(105,117),(111,133),(122,137),(112,137),(100,123)],'#3a574f')
 for pts in [[(96,96),(94,109),(96,119)],[(102,106),(101,121),(106,132)]]:tree_curve(pts,'#a0aa86',1)
 # Asymmetric stepped foliage and overlapping shoulders, rather than an umbrella disc.
 masses=[
  ([(26,75),(31,65),(42,62),(44,54),(57,53),(65,43),(79,44),(87,35),(101,36),(110,32),(123,40),(135,39),(140,49),(153,51),(154,61),(163,66),(160,77),(148,79),(142,86),(126,84),(120,90),(106,85),(93,89),(82,85),(70,91),(57,85),(44,87),(40,80),(30,82)],'#2e534d'),
  ([(34,66),(45,59),(57,59),(65,49),(80,50),(88,42),(104,42),(111,38),(125,44),(126,54),(119,62),(105,62),(95,70),(81,66),(70,75),(56,72),(46,76),(36,72)],'#496d57'),
  ([(67,49),(80,44),(90,39),(104,40),(111,38),(121,43),(113,48),(99,48),(90,54),(77,53)],'#768b66'),
  ([(110,69),(124,60),(139,59),(148,64),(155,69),(149,76),(139,75),(133,81),(118,78),(108,81)],'#52775b'),
  ([(42,77),(52,73),(63,76),(70,80),(65,86),(52,83),(43,85)],'#3e644f')]
 for pts,c in masses:tree_poly(pts,c)
 for x,y in [(42,65),(56,61),(72,54),(89,46),(105,43),(120,70),(138,66),(81,78),(55,79),(128,77)]:
  tree_line([(x,y),(x+2,y-1),(x+5,y-1),(x+7,y)],fill='#8a9c71')
  tree_line((x+1,y+2,x+4,y+2),fill='#69855d')
 for x,y in [(45,68),(56,56),(70,61),(83,53),(97,47),(112,55),(126,65),(143,70),(68,78),(97,73),(122,80)]:
  tree_poly([(x-4,y),(x-2,y-3),(x+4,y-3),(x+8,y),(x+4,y+3),(x-2,y+2)],'#5b7b5b')
  tree_line([(x-2,y-2),(x+3,y-2),(x+5,y-1)],fill='#92a274')
 # Hanging tips and the old healed split distinguish the guardian tree at this distance.
 for x,y in [(48,84),(74,88),(125,86),(145,79)]:
  tree_line((x,y,x,y+5),fill='#617e62');tree_point((x+1,y+4),fill='#9aa67c')
 # Small roots and their broken reflection make the remote tree feel grounded.
 tree_line((95,92,94,119),fill='#98a087');tree_line((100,111,104,130),fill='#80927c')
 for y,w in [(147,36),(151,26),(155,18),(159,13)]:tree_line((95-w//2,y,95+w//2,y),fill='#41676b')
 # Near grassy terrace occupies only the bottom-left; there is deliberately no path.
 poly([(0,169),(30,164),(55,168),(83,165),(113,169),(140,169),(164,175),(187,183),(206,196),(214,224),(0,224)],'#314f48')
 poly([(0,167),(29,162),(56,166),(82,162),(112,167),(139,166),(163,172),(183,180),(202,192),(208,224),(0,224)],'#60774f')
 poly([(0,196),(34,189),(70,194),(113,190),(149,198),(185,196),(206,210),(208,224),(0,224)],'#526c4b')
 # Bank stones and reeds separate the resting place from the water.
 for x,y in [(10,169),(34,168),(173,181),(194,194),(207,212)]:
  poly([(x-4,y),(x-2,y-3),(x+3,y-2),(x+5,y+1),(x+1,y+3)],'#718579')
  d.line((x-2,y-2,x+2,y-2),fill='#95a18a')
 for x,y in [(18,169),(41,167),(177,181),(190,188),(211,218)]:
  d.line((x,y+4,x-1,y-6),fill='#8c9c6a');d.line((x+2,y+3,x+3,y-4),fill='#798f64')
 # Near-bank foliage is drawn at a different scale from the remote island foliage.
 for x,y in [(8,180),(17,212),(188,194),(200,216)]:
  poly([(x-5,y),(x-3,y-4),(x,y-2),(x+3,y-5),(x+5,y),(x+2,y+2)],'#3f6049')
  d.line((x-3,y-2,x,y),fill='#7c9762');d.line((x+3,y-3,x+1,y),fill='#9aaa75')
 for x,y in [(7,195),(18,216),(188,185),(199,211)]:
  d.line((x,y,x,y-5),fill='#849963');d.line((x-1,y-5,x+1,y-5),fill='#c4c6a2');d.point((x,y-6),fill='#d7d1ae')
 # A few pads and bank reflections break the empty water without covering the menu.
 for x,y in [(220,210),(228,212),(214,199),(243,218)]:
  poly([(x-3,y),(x-1,y-2),(x+3,y-1),(x+4,y),(x+1,y+1)],'#547a6a')
  d.line((x-2,y+3,x+4,y+3),fill='#345d6b')
 # Warm woven cloth on a level patch, well inside the grassy shoreline.
 poly([(48,184),(132,181),(164,207),(54,216)],'#3d5545')
 poly([(45,181),(132,179),(163,205),(53,213)],'#a18c91')
 d.line([(45,181),(132,179),(163,205)],fill='#c9b2a3')
 d.line([(49,185),(133,183),(157,203),(56,209),(49,185)],fill='#766f7a')
 for j in range(6):d.line((52+j,187+j*4,137+j*4,184+j*3),fill='#af9898')
 for x,y in [(59,213),(75,212),(91,210),(107,209),(123,208),(139,206)]:d.line((x,y,x,y+2),fill='#c9b3a5')
 def actor(name,cx,base,flip=False):
  p=Image.open(ROOT/'sprites'/name).convert('RGBA');p=p.crop(p.getbbox())
  if flip:p=p.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  p=p.resize((p.width*2,p.height*2),Image.Resampling.NEAREST)
  d.ellipse((cx-10,base-1,cx+9,base+2),fill='#746c70')
  im.paste(p,(cx-p.width//2,base-p.height),p)
 actor('npcs/elder.png',38,193)
 actor('npcs/guide.png',84,188)
 actor('characters/eevee.png',126,202,flip=True)
 # Empty cushion is part of the gathering, with a small untouched cup.
 poly([(73,198),(89,197),(95,205),(76,207)],'#c8b692')
 d.line((77,199,88,199),fill='#e3cfaa');d.rectangle((83,192,86,196),fill='#ded2b2')
 # Basket on grass beside the blanket; lantern marks its outside corner.
 bx,by=175,209
 d.ellipse((bx-7,by-1,bx+7,by+2),fill='#405b46')
 d.arc((bx-5,by-15,bx+4,by-6),180,360,fill='#786747',width=2)
 poly([(bx-7,by-9),(bx+6,by-9),(bx+5,by),(bx-5,by)],'#806c4e')
 d.rectangle((bx-4,by-7,bx+4,by-1),fill='#b29969')
 for yy in [by-6,by-3]:d.line((bx-5,yy,bx+5,yy),fill='#d1b780')
 for xx in [bx-3,bx,bx+3]:d.line((xx,by-7,xx+1,by-1),fill='#8c7951')
 d.rectangle((25,197,31,205),fill='#72674d');d.rectangle((27,199,29,203),fill='#e4bf7b');d.point((28,200),fill='#fff0bc')
 for x,y in [(6,213),(22,221),(44,217),(185,215),(199,221)]:
  d.line((x,y,x-1,y-5),fill='#91a46c');d.line((x,y,x+3,y-3),fill='#798e59')
 return im

def main():
 out=ROOT/'sprites/backgrounds';out.mkdir(exist_ok=True)
 assets=[]
 for key,layer in OAK.items():
  path=ROOT/'sprites/deco'/('title_oak_'+key+'.png');layer.save(path)
  assets.append(dict(id='deco/title_oak_'+key,path=str(path.relative_to(ROOT)),category='deco',
                     region='forest',width=W,height=H,anchor=[72,202],layer=key,
                     sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 (ROOT/'art/title-oak-manifest.json').write_text(json.dumps(dict(version=1,nativeScale=1,renderOrder=['back','wood','front'],endingOnlyLayer='blossom',assets=assets),ensure_ascii=False,indent=2)+'\n')
 a,b=make_departure(),make_lakeside();a.save(out/'title_departure.png');b.save(out/'title_picnic.png')
 ending=a.convert('RGBA');ending.alpha_composite(OAK['blossom']);ending.save(ROOT/'docs/title-oak-blossom.png')
 sheet=Image.new('RGB',(1536,516),'#263e40');g=ImageDraw.Draw(sheet)
 font=ImageFont.truetype('/System/Library/Fonts/Hiragino Sans GB.ttc',24)
 for i,(pic,label) in enumerate([(a,'A · 晨光村口 · 启程'),(b,'B · 湖畔草坪 · 星夜野餐')]):
  sheet.paste(pic.resize((768,448),Image.Resampling.NEAREST),(i*768,52));g.text((i*768+24,14),label,font=font,fill='#e7dbc0')
 sheet.save(ROOT/'docs/title-covers-ab.png')
 # A/B presentation with the active title brand, kept reproducible with the covers.
 import re
 brand=re.search(r"const TITLE_BRAND = '([^']+)'",(ROOT/'index.html').read_text()).group(1)
 logo=Image.open(ROOT/('sprites/ui/title_logo_'+brand+'_zh.png')).convert('RGBA').resize((160,69),Image.Resampling.NEAREST)
 for i,pic in enumerate((a,b)):
  panel=pic.convert('RGBA');panel.alpha_composite(logo,(208,22))
  sheet.paste(panel.convert('RGB').resize((768,448),Image.Resampling.NEAREST),(i*768,52))
 sheet.save(ROOT/'docs/title-screen-polished.png')
 # Enlargements are always nearest-neighbour, for review of the actual source pixels.
 regions=[(a,(18,155,203,219),'村口启程'),(b,(16,158,197,220),'湖畔野餐'),(a,(302,154,360,190),'石桥'),(a,(169,145,247,174),'围栏')]
 height=sum((box[3]-box[1])*4+48 for _,box,_ in regions)
 detail=Image.new('RGB',(800,height),'#263e40');dd=ImageDraw.Draw(detail);y=0
 for src,box,label in regions:
  dd.text((16,y+5),label,font=font,fill='#e9ddba')
  crop=src.crop(box).resize(((box[2]-box[0])*4,(box[3]-box[1])*4),Image.Resampling.NEAREST)
  detail.paste(crop,(16,y+35));y+=crop.height+48
 detail.save(ROOT/'docs/title-details-review.png')
 fade=Image.new('RGB',(1056,192),'#263e40')
 for i,src in enumerate((a,Image.new('RGB',(W,H),'#243d43'),b)):
  fade.paste(src.crop((24,148,200,212)).resize((352,128),Image.Resampling.NEAREST),(i*352,32))
 fade.save(ROOT/'docs/title-character-fade-check.png')

 print('Built distinct village-departure and lakeside-picnic covers.')
if __name__=='__main__':main()
