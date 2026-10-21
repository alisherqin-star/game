"""Small identifying accessories over the unchanged original Eevee silhouette.

No player sprite or character palette is overwritten. All NPCs share foot anchor
(16, 28), so both facings and all accessories use the same baseline in game.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
IDENTITIES={
 'elder':('暖灰白与橡叶绿','#aab594','灰白毛＋金边眼镜＋橡叶拐杖'),
 'guide':('湖蓝','#49a9c9','斜蝴蝶结＋金铃铛'),
 'merchant':('莓红','#be627e','宽围巾＋皮挎包'),
 'healer':('奶白青绿','#59a98f','白头巾＋绿叶刺绣'),
 'explorer':('橘红','#c77847','护目镜＋橘色背包'),
 'gardener':('麦草金与陶粉','#c3927c','花草帽＋陶粉围裙'),
 'miner':('蜂蜜黄','#d8ad49','黄矿帽＋亮头灯'),
 'baker':('奶油粉','#d18fa6','蓬松厨帽＋粉领结'),
 'scholar':('葡萄紫','#9473bb','紫围巾＋随身书本'),
 'guard':('靛蓝','#5d7fae','蓝头带＋小盾徽'),
}
PROFILES={key:(role,IDENTITIES[key][2],IDENTITIES[key][1]) for key,role in {'elder': '村长奶奶', 'guide': '向导', 'merchant': '商人', 'healer': '医师', 'explorer': '探险家', 'gardener': '罗丝奶奶', 'miner': '矿工', 'baker': '糕点师', 'scholar': '学者', 'guard': '守卫'}.items()}

def make_sprite(style,base):
 # Only Penny ages: preserve the original player's silhouette and dark eyes.
 base=base.copy()
 if style=='elder':
  palette={(156,113,84):(199,199,189),(104,82,78):(144,149,143),
           (214,176,135):(225,217,198),(241,230,217):(245,235,217),
           (5,2,4):(66,62,58)}
  for y in range(base.height):
   for x in range(base.width):
    r,g,b,a=base.getpixel((x,y))
    if a:base.putpixel((x,y),(*palette.get((r,g,b),(r,g,b)),a))
 # Start clean: each role gets one colour mass and one distinct silhouette.
 im=Image.new('RGBA',(32,28));im.alpha_composite(base,(8,10));d=ImageDraw.Draw(im)
 color=IDENTITIES[style][1];edge='#685044';cream='#f0dfbd'
 def line(p,c,w=1):d.line(p,fill=c,width=w)
 def dot(x,y,c):d.point((x,y),fill=c)
 def collar(c):line([(16,22),(17,23),(19,24),(21,24),(22,23)],c,2)
 def cap(c,light):
  d.polygon([(14,13),(15,11),(17,11),(19,12),(20,14),(18,15),(16,14),(14,14)],fill=c)
  line([(14,14),(16,14),(18,15),(20,14)],light)
 def bow(x,y,c):
  d.polygon([(x-3,y-3),(x-1,y-2),(x,y),(x-3,y-1)],fill=c)
  d.polygon([(x,y),(x+3,y),(x+3,y+3),(x+1,y+2)],fill=c)
  dot(x,y,cream);dot(x-2,y-2,'#a7dbe2')
 if style=='elder':
  # A small shoulder shawl leaves the cream ruff and both ears exposed.
  d.polygon([(13,20),(14,19),(16,21),(17,23),(15,25),(13,24)],fill='#788971')
  line([(13,21),(14,23),(15,24),(16,23)],'#aeb89a')
  dot(15,22,'#d5c69b')
  # Tiny oak-leaf pin, not a second green hat like the gardener's old look.
  line([(14,13),(16,12),(17,13)],'#677b59')
  for x,y in [(14,11),(15,12),(16,10),(16,11),(17,12)]:dot(x,y,'#9bab7c')
  dot(16,12,'#d6d6a9')
  # Rims follow the two original eye positions on the oblique face.
  for pts in [[(18,18),(19,18),(20,19),(20,20),(19,21),(18,21),(17,20),(17,19)],
              [(23,16),(24,16),(25,17),(25,18),(24,19),(23,19),(22,18),(22,17)]]:
   for x,y in pts:dot(x,y,'#b59862')
  dot(18,18,'#e0c68c');dot(23,16,'#e0c68c')
  line([(20,19),(21,18),(22,18)],'#86704f')
  line([(15,17),(16,18),(17,19)],'#86704f')
  # Crooked wooden cane stands beside the face, not through it.
  line([(25,16),(25,15),(28,15),(29,16),(28,18),(28,27)],'#715e48')
  line([(26,15),(28,16)],'#c6a477');line([(28,19),(28,26)],'#b08d61')
  dot(27,27,'#715e48')
  # Oak-leaf emblem: three lobes and a visible central vein; plot clue.
  line([(29,18),(30,19)],'#715e48')
  d.polygon([(30,18),(31,19),(30,20),(31,21),(30,22),(31,23),(29,24),(28,23),(29,22),(28,21),(29,20),(29,19)],fill='#70835d')
  line([(30,19),(30,21),(29,23)],'#c6c795')
  # One pale paw rests on the shaft; the staff reaches the shared foot line.
  line([(25,24),(27,24)],'#e1d9c6');dot(26,25,'#a5a79d')
 elif style=='guide':
  bow(13,14,color);collar('#78c2d0')
  d.ellipse((19,24,21,26),fill='#d9b04e');dot(20,24,'#f8e7a4');dot(20,26,edge)
 elif style=='merchant':
  collar(color);line([(16,23),(16,25),(17,26)],'#a64d6b',2)
  line([(14,19),(15,21),(15,23)],'#bd986d')
  d.rounded_rectangle((12,22,16,26),radius=1,fill='#796044')
  d.polygon([(13,22),(16,22),(15,24),(13,24)],fill='#bb9362');dot(15,24,'#edce88')
 elif style=='healer':
  d.polygon([(14,12),(16,11),(18,12),(20,14),(18,15),(16,14),(14,14)],fill='#f1e4c8')
  line([(14,14),(16,15),(18,15)],'#baa990')
  line([(17,12),(18,13),(17,14)],color);dot(16,13,color)
  collar(color)
 elif style=='explorer':
  # Backpack sits behind the shoulder, unlike the merchant's low pouch.
  d.rounded_rectangle((11,18,15,24),radius=1,fill='#8b5a3e')
  d.rounded_rectangle((11,18,14,23),radius=1,fill=color)
  line([(12,19),(14,19)],'#e6b777');dot(13,22,'#f0ca91')
  line([(14,18),(15,19),(16,22)],'#b08e66')
  line([(13,14),(15,15),(18,14),(20,13)],'#9b744e')
  for x,y in [(14,14),(18,13)]:
   d.rectangle((x,y,x+2,y+2),fill=edge);line([(x,y),(x+1,y)],'#81bac0');dot(x+1,y+1,'#bedcd2')
 elif style=='gardener':
  cap('#c5ab75','#e5d19e')
  line([(13,14),(16,15),(19,15),(21,14)],'#b59865')
  line([(14,13),(16,13),(18,14),(20,13)],'#ad7c65')
  # Cream blossom and a small herb sprig distinguish Rose from Penny's oak pin.
  for x,y in [(15,11),(14,12),(16,12),(15,13)]:dot(x,y,'#f1dfb2')
  dot(15,12,'#cf9972');dot(13,12,'#7b9166')
  # A warm potter's-clay apron with a seed pocket; brown Eevee fur stays intact.
  d.polygon([(16,23),(18,24),(21,23),(21,26),(20,27),(17,26)],fill=color)
  line([(16,23),(18,24),(21,23)],'#e2c1a0')
  line([(18,25),(20,25),(20,26),(18,26)],'#a9715f')
  dot(19,25,'#e0b795');dot(17,24,'#cfaa8c')
 elif style=='miner':
  cap(color,'#f0cc77');dot(16,12,'#eac467')
  d.rectangle((19,12,21,14),fill='#7d6949');dot(20,12,'#fff1c6');dot(20,13,'#ffe49a')
  line([(16,22),(18,23)],'#869da2')
 elif style=='baker':
  for box in [(14,10,17,13),(16,8,19,13),(18,11,21,14)]:d.ellipse(box,fill='#eee1c4')
  line([(14,13),(16,14),(18,15),(20,14)],'#d9a7b1')
  bow(20,24,color)
 elif style=='scholar':
  collar(color);line([(17,24),(17,26)],'#795695',2)
  # A book replaces a second pair of glasses, making the silhouette unique.
  d.polygon([(12,22),(15,21),(16,25),(13,26)],fill='#645074')
  d.polygon([(13,22),(15,22),(15,24),(13,25)],fill='#b199d0')
  line([(13,25),(15,24)],'#e9dabe');dot(14,23,'#ebc983')
 elif style=='guard':
  line([(13,14),(15,14),(17,15),(19,14),(20,14)],color,2)
  dot(18,14,'#dfca91');collar('#8eadd0')
  d.polygon([(19,23),(22,23),(22,25),(20,27),(18,25)],fill='#c3a369')
  d.polygon([(19,24),(21,24),(21,25),(20,26),(19,25)],fill=color)
 # Protect expression and overlapping ear tips, even with bolder accessories.
 for x0,y0,x1,y1 in [(19,10,23,12),(12,12,14,13)]:
  for y in range(y0,y1+1):
   for x in range(x0,x1+1):
    c=base.getpixel((x-8,y-10))
    if c[3]:im.putpixel((x,y),c)
 for x,y in [(18,19),(18,20),(23,17),(23,18),(23,20)]:im.putpixel((x,y),base.getpixel((x-8,y-10)))
 return im


def main():
 base=Image.open(ROOT/'sprites/characters/eevee.png').convert('RGBA');out=ROOT/'sprites/npcs';out.mkdir(exist_ok=True)
 assets=[]
 for style,(role,trait,color) in PROFILES.items():
  im=make_sprite(style,base);path=out/(style+'.png');im.save(path)
  assets.append(dict(id='npcs/'+style,path=str(path.relative_to(ROOT)),role=role,trait=trait,
                     width=32,height=28,anchor=[16,28],accent=color,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 (ROOT/'art/npc-manifest.json').write_text(json.dumps(dict(version=4,variant='identity-B-story-grannies',fit='native oblique face; Penny warm grey fur; eye positions and shared foot anchor preserved',base='sprites/characters/eevee.png',assets=assets),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 fonts=['/System/Library/Fonts/Hiragino Sans GB.ttc','/System/Library/Fonts/STHeiti Medium.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc']
 font_path=next((p for p in fonts if Path(p).exists()),None)
 font=ImageFont.truetype(font_path,22) if font_path else ImageFont.load_default()
 small=ImageFont.truetype(font_path,17) if font_path else ImageFont.load_default()
 sheet=Image.new('RGB',(1200,1020),'#233a3e');g=ImageDraw.Draw(sheet)
 g.text((25,17),'剧本人物美术 · 村长奶奶与罗丝奶奶',font=font,fill='#f1e4c8')
 refs=[(base,'原版伊布 · 轮廓参考','主角图未改动'),
       (Image.open(out/'elder.png'),'村长奶奶','暖灰白毛 · 金边眼镜 · 橡叶拐杖'),
       (Image.open(out/'gardener.png'),'罗丝奶奶','棕毛 · 花草帽 · 陶粉围裙'),
       (Image.open(out/'guide.png'),'贝儿 · 风格参照','已确认外观保持不变')]
 for i,(im,title,desc) in enumerate(refs):
  x=i*300;g.rounded_rectangle((x+9,58,x+291,343),radius=12,fill='#d7d9c2')
  rgba=im.convert('RGBA');pic=rgba.resize((rgba.width*7,rgba.height*7),Image.Resampling.NEAREST)
  sheet.paste(pic,(x+(300-pic.width)//2,82+196-pic.height),pic)
  g.text((x+22,291),title,font=font,fill='#465a46');g.text((x+17,322),desc,font=small,fill='#6b6953')
 g.text((25,365),'左右朝向检查 · 共用脚底锚点，拐杖随人物镜像',font=small,fill='#c8d1b5')
 for i,(style,flip) in enumerate([('elder',False),('elder',True),('gardener',False),('gardener',True)]):
  x=i*300;g.rounded_rectangle((x+9,402,x+291,537),radius=9,fill='#49615a')
  im=Image.open(out/(style+'.png')).convert('RGBA')
  if flip:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  pic=im.resize((128,112),Image.Resampling.NEAREST);sheet.paste(pic,(x+86,411),pic)
  g.line((x+25,523,x+275,523),fill='#b2bd91')
 g.text((25,558),'村民合照 · 其余职业外观保持不变',font=font,fill='#e7dcca')
 for i,a in enumerate(assets):
  x=i%5*240;y=600+i//5*200;g.rounded_rectangle((x+7,y+8,x+232,y+192),radius=10,fill='#30494b')
  pic=Image.open(ROOT/a['path']).resize((128,112),Image.Resampling.NEAREST)
  sheet.paste(pic,(x+56,y+14),pic);g.text((x+16,y+135),a['role'],font=font,fill=a['accent'])
  # Longer story accessories use two short lines at a readable preview size.
  trait=a['trait'];parts=trait.split('＋')
  if len(parts)>2:trait='＋'.join(parts[:2])
  g.text((x+16,y+167),trait,font=small,fill='#e7dcca')
 sheet.save(ROOT/'docs/npc-lineup.png')
 print('Generated',len(assets),'NPC looks; player unchanged; Penny and Rose updated.')


if __name__=='__main__':main()
