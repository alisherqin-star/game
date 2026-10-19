"""Native pixel architecture shared by village props and the title courtyard."""
import math,random
from PIL import Image,ImageDraw,ImageChops
from pixel_nature import curve,soften

def cottage(style='elder'):
 im=Image.new('RGBA',(96,80));d=ImageDraw.Draw(im);rng=random.Random('cottage-'+style)
 colors={'elder':('#678357','#3e5e4d','#a0af73','#d6c7a4'),
         'guide':('#6c9ba1','#456b76','#afc5b4','#dbccb0'),
         'merchant':('#a96d7e','#744e65','#d3a4a1','#decaab')}
 roof,shade,light,wall=colors[style];edge='#49564a';wood='#82684f';gold='#e5bd79'
 def line(p,c,w=1):d.line(p,fill=c,width=w)
 def dot(x,y,c):d.point((x,y),fill=c)
 # Uneven stone footing and rounded plaster, with dark recesses at the eaves.
 d.rounded_rectangle((13,70,84,78),radius=3,fill='#677868')
 for x in range(16,81,12):d.rounded_rectangle((x,72,x+10,76),radius=2,fill='#a3aa87')
 d.rounded_rectangle((18,32,79,73),radius=5,fill=edge)
 d.rounded_rectangle((20,34,77,72),radius=4,fill=wall)
 d.rectangle((20,36,77,42),fill='#b4aa8b')
 for x,y in [(25,45),(64,64),(71,46),(36,67),(58,45)]:
  line([(x,y),(x+3,y)],'#c3b393')
 for x in (20,75):
  line([(x,41),(x-1,56),(x,72)],wood,2);line([(x+1,44),(x,54)],'#b89a70')
 # Short chimney, softened brick corners; the roof later occludes its base.
 d.rounded_rectangle((65,12,73,31),radius=2,fill='#8c8070')
 d.rounded_rectangle((63,11,74,15),radius=2,fill='#b4a78b')
 line([(66,18),(70,18)],'#c5b695');line([(69,23),(72,23)],'#b8aa8c')
 # Bowed, asymmetric roof; tile rows follow the slope rather than a rigid grid.
 outline=[(5,41),(12,35),(17,23),(28,13),(41,8),(52,10),(65,18),(74,29),(83,37),(92,41),(89,45),(72,44),(49,42),(29,44),(12,46)]
 d.polygon(soften(outline,2,True),fill=edge)
 roofpoints=[(9,40),(17,31),(22,21),(32,15),(43,11),(53,13),(64,21),(72,32),(87,40),(81,42),(63,39),(47,39),(28,41),(13,43)]
 d.polygon(soften(roofpoints,2,True),fill=roof)
 roofmask=Image.new('L',im.size);ImageDraw.Draw(roofmask).polygon(soften(roofpoints,2,True),fill=255)
 # Each shingle is a small curved fragment, with breaks and two hue families.
 tile=Image.new('RGBA',im.size);td=ImageDraw.Draw(tile)
 for y in (18,24,30,36,41):
  for x in range(-5,96,10):
   if rng.random()<.22:continue
   off=5 if (y//6)%2 else 0;xx=x+off
   yy=y+round(math.sin((xx-44)/40)*2)
   curve(td,[(xx,yy),(xx+4,yy+1),(xx+8,yy)],shade)
   if rng.random()<.5:td.line((xx+1,yy-1,xx+4,yy-1),fill=light)
 alpha=tile.getchannel('A');alpha=ImageChops.multiply(alpha,roofmask)
 tile.putalpha(alpha);im.alpha_composite(tile);d=ImageDraw.Draw(im)
 curve(d,[(9,42),(27,40),(48,40),(68,40),(87,42)],'#bba47a',2)
 curve(d,[(11,44),(29,43),(48,42),(69,43),(86,44)],wood)
 # One arched door and one bay window avoid the two-eyes/face facade effect.
 d.rounded_rectangle((46,47,61,74),radius=7,fill='#756751')
 d.rounded_rectangle((48,49,59,73),radius=5,fill='#8f7555')
 d.rectangle((48,59,59,73),fill='#8f7555')
 curve(d,[(50,53),(50,61),(51,71)],'#b89a70')
 line([(55,54),(55,70)],'#76614c');dot(57,63,gold)
 d.rounded_rectangle((25,47,40,60),radius=3,fill=wood)
 d.rounded_rectangle((27,49,38,58),radius=2,fill='#edc78a')
 line([(28,50),(35,50)],'#f5dfac');line([(32,49),(32,58)],'#9b805b')
 line([(27,54),(38,54)],'#a68a60')
 # Planter, climbing vine and warm hanging lantern are low-contrast details.
 d.rounded_rectangle((23,61,42,66),radius=2,fill='#9d795a')
 line([(24,61),(41,61)],'#cab18a')
 for x,y in [(26,59),(31,60),(36,59),(40,60)]:
  d.ellipse((x-2,y-2,x+2,y+1),fill='#7d9b63');dot(x,y-2,'#e3b7a9' if x%2 else '#e6ce92')
 curve(d,[(72,70),(70,59),(73,48),(75,41)],'#77956a')
 for x,y in [(71,62),(73,52),(73,45)]:
  d.ellipse((x-2,y-1,x+1,y+1),fill='#9bae7d')
 line([(64,46),(67,46),(67,49)],wood)
 d.rounded_rectangle((65,49,69,55),radius=1,fill='#8b7958')
 d.rectangle((66,50,68,53),fill='#f0d499');dot(67,50,'#fff0c2')
 d.rounded_rectangle((43,73,64,77),radius=2,fill='#c1b394')
 line([(46,74),(61,74)],'#e1ceb0')
 for x in (14,80):
  d.ellipse((x-5,69,x+4,76),fill='#6e8b60')
  d.ellipse((x-3,68,x+2,72),fill='#9eb078')
 # A role emblem is separate from window/door geometry.
 if style=='elder':
  d.polygon([(43,24),(47,20),(52,20),(49,25),(45,26)],fill='#c2ce90')
  line([(45,25),(49,22)],'#7b975c')
 elif style=='guide':
  d.polygon([(42,22),(47,24),(43,27)],fill='#c2d9d0')
  d.polygon([(48,24),(53,22),(52,27)],fill='#c2d9d0');dot(47,24,'#e9d8a4')
 else:
  # Compact berry awning over a serving hatch, with a satchel-shaped sign.
  d.rounded_rectangle((23,44,42,48),radius=2,fill='#a16a7c')
  for x in range(25,42,6):line([(x,45),(x+1,47)],'#e1b4af',2)
  d.rounded_rectangle((44,22,51,28),radius=1,fill='#d6b47f')
  d.arc((45,19,50,25),180,360,fill='#d6b47f');dot(48,25,'#8f6b57')
 return im

def title_board():
 im=Image.new('RGBA',(336,64));d=ImageDraw.Draw(im)
 d.rounded_rectangle((0,3,335,63),radius=12,fill='#495e4d')
 d.rounded_rectangle((2,1,333,59),radius=11,fill='#9d8560')
 d.rounded_rectangle((4,2,331,56),radius=9,fill='#d3bd91')
 d.rounded_rectangle((7,5,328,54),radius=8,fill='#e9d9b6')
 curve(d,[(14,8),(96,7),(181,9),(316,8)],'#f5e8c9')
 curve(d,[(14,51),(92,52),(202,50),(321,51)],'#c8b38b')
 for x,y in [(9,12),(320,13),(12,46),(321,44)]:
  d.ellipse((x-1,y-1,x+1,y+1),fill='#9a845f')
 # A few leaf clusters soften the board without interfering with the wordmark.
 for x,y,flip in [(2,4,1),(327,49,-1)]:
  curve(d,[(x,y+12),(x+flip*7,y+4),(x+flip*16,y)],'#6e8b5a')
  for dx,dy in [(3,5),(9,0),(10,7)]:
   d.ellipse((x+flip*dx-3,y+dy-2,x+flip*dx+3,y+dy+1),fill='#91aa6e')
 # Botanical crest balances the wordmark, using the same moss/cream palette.
 d.ellipse((282,10,320,48),fill='#d7cca8',outline='#b8ad86')
 curve(d,[(289,41),(285,31),(291,17)],'#8fa26e',2)
 curve(d,[(312,41),(316,31),(310,17)],'#8fa26e',2)
 for x,y in [(287,23),(288,33),(313,23),(313,34)]:
  d.ellipse((x-2,y-2,x+2,y),fill='#a4b580')
 d.polygon([(294,37),(292,19),(297,23),(301,32),(307,21),(311,19),(308,36),(301,42)],fill='#aa8a5f')
 d.polygon([(297,34),(300,36),(302,34),(306,35),(301,40)],fill='#f0dfbb')
 return im

if __name__=='__main__':
 from pathlib import Path
 root=Path(__file__).resolve().parents[1]
 for style in ('elder','guide','merchant'):cottage(style).save(root/'sprites/deco'/f'env_village_home_{style}.png')
 cottage('elder').save(root/'sprites/deco/env_village_cottage.png')
 title_board().save(root/'sprites/ui/env_village_title_board.png')
 print('Built three village homes and a matching title board.')
