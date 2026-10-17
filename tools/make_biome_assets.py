"""Original code-authored pixel scenery; no character changes. Requires Pillow.
Run python3 tools/make_biome_assets.py then python3 tools/embed_assets.py.
"""
from pathlib import Path
import random
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]/'sprites'
def save(im,cat,name): im.save(ROOT/cat/('biome_'+name+'.png'))
for theme,colors in {'shore':['#657c74','#82968a','#4b6666','#a7b39a'], 'cave':['#293b52','#3b5267','#1c2c43','#58747b'], 'tower':['#494858','#656071','#333344','#8c8291']}.items():
 for v in range(4):
  rng=random.Random(312+v);im=Image.new('RGBA',(16,16),colors[0]);d=ImageDraw.Draw(im)
  if theme=='tower':
   for y in (0,8):
    d.line((0,y,15,y),fill=colors[2]);d.line((0,y+1,15,y+1),fill=colors[1])
    x=(v*3+(4 if y else 12))%16;d.line((x,y,x,y+7),fill=colors[2])
  else:
   for _ in range(14):
    x,y=rng.randrange(16),rng.randrange(16);d.rectangle((x,y,x+rng.randrange(1,5),y+1),fill=rng.choice(colors))
  d.point((3+v,4),fill=colors[3]);save(im,'tiles',f'{theme}_{v}')
# Reeds anchored on shoreline soil.
im=Image.new('RGBA',(24,32));d=ImageDraw.Draw(im)
for x,y in [(5,8),(12,3),(19,11)]:
 d.line((x,31,x,y),fill='#698961');d.line((x+1,30,x+1,y),fill='#a7b77e')
 d.rectangle((x-1,y,x+1,y+7),fill='#70503e');d.line((x,y,x,y+5),fill='#ae8956')
 d.line([(x,28),(x-4,20),(x-5,17)],fill='#52785d',width=1)
save(im,'deco','reeds')
im=Image.new('RGBA',(24,16));d=ImageDraw.Draw(im)
d.ellipse((0,5,22,14),fill='#304f55');d.ellipse((1,4,21,11),fill='#638776');d.line((3,7,17,7),fill='#a7b993');save(im,'deco','pebbles')
# Cave crystals, distinct decorative low-contrast outline.
for v in range(2):
 im=Image.new('RGBA',(24,32));d=ImageDraw.Draw(im)
 for x,y,h in [(3,16,12),(9,3,25),(16,11,17)]:
  d.polygon([(x,y+4),(x+3,y),(x+6,y+5),(x+5,31),(x+1,31)],fill='#34536a')
  d.polygon([(x+3,y+1),(x+5,y+5),(x+4,28),(x+3,30)],fill='#72c8c0' if not v else '#ab98cc')
  d.line((x+2,y+5,x+2,27),fill='#a9e0ca' if not v else '#d9c2ed')
 save(im,'deco',f'crystal_{v}')
im=Image.new('RGBA',(16,32));d=ImageDraw.Draw(im)
for x,y in [(2,2),(7,0),(12,4)]:
 d.line([(x,y),(x+1,14),(x-1,25),(x,31)],fill='#315960')
 for yy in range(y+4,28,7):d.line((x,yy,x+3,yy-2),fill='#4b847e')
save(im,'deco','vine')
# Tower ornaments: broken pillar, small brass lamp, hanging banner.
im=Image.new('RGBA',(24,48));d=ImageDraw.Draw(im)
d.rectangle((7,7,17,45),fill='#464657');d.rectangle((9,6,11,44),fill='#77717b');d.rectangle((14,8,15,44),fill='#302f41')
d.polygon([(5,9),(5,4),(11,4),(12,0),(16,3),(19,3),(19,9)],fill='#89818b')
d.rectangle((4,44,20,47),fill='#706c79');d.line((4,44,20,44),fill='#a69d9a');save(im,'deco','pillar')
im=Image.new('RGBA',(16,24));d=ImageDraw.Draw(im)
d.line((7,0,7,5),fill='#958267');d.rectangle((3,5,12,18),fill='#443d43');d.rectangle((5,7,10,16),fill='#e8bd75');d.rectangle((6,8,8,14),fill='#fff1b0');d.line((2,5,13,5),fill='#b59c71');d.line((3,18,12,18),fill='#b59c71');save(im,'deco','lamp')
im=Image.new('RGBA',(24,40));d=ImageDraw.Draw(im)
d.line((1,1,22,1),fill='#a9987b',width=2);d.polygon([(5,3),(18,3),(18,35),(12,31),(5,38)],fill='#514766');d.line((6,4,6,32),fill='#8a7795');d.polygon([(14,8),(9,18),(13,18),(10,27),(17,15),(13,15)],fill='#d1b47e');save(im,'deco','banner')

# Transparent water lets submerged scenery remain readable instead of covering it
# in a repeated dot texture. Surface highlights use the existing two-frame clock.
for theme,color in [('lake',(50,128,151,145)),('cave',(30,91,123,112))]:
 im=Image.new('RGBA',(16,16),color)
 save(im,'tiles',f'{theme}_water')
 for phase in range(2):
  surface=im.copy();d=ImageDraw.Draw(surface)
  d.line((0,0,15,0),fill=(144,209,204,220))
  d.line((2+phase*5,1,6+phase*5,1),fill=(216,239,216,230))
  save(surface,'tiles',f'{theme}_surface_{phase}')

print('Generated 26 regional scenery assets.')
