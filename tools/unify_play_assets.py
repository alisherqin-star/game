"""Unify gameplay props/items/enemies at native size; never touch player/NPC looks."""
from pathlib import Path
import colorsys,hashlib,json,shutil
from PIL import Image,ImageDraw,ImageFont
from pixel_nature import Painter,curve

ROOT=Path(__file__).resolve().parents[1]
SOURCES=ROOT/'art/gameplay-style-source'

def polish(name,im):
 im=im.convert('RGBA');out=im.copy()
 # A small common cream component unifies highlights without losing danger hues.
 for y in range(im.height):
  for x in range(im.width):
   r,g,b,a=im.getpixel((x,y))
   if not a:continue
   h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255)
   if max(r,g,b)<48:col=(66,64,65)
   elif l>.91:col=(246,234,208)
   else:
    col=tuple(round(c*.78+t*.22) for c,t in zip((r,g,b),(194,185,155)))
   # Tiny original pupils retain their contrast.
   if 'enemies/' in name and max(r,g,b)<30 and (r,g,b)!=(26,26,42):col=(29,32,31)
   out.putpixel((x,y),(*col,a))
 d=ImageDraw.Draw(out)
 if name in ('props/moss_rock','props/ice_rock'):
  out=Image.new('RGBA',im.size);d=ImageDraw.Draw(out)
  ice='ice_' in name
  pal=['#8aa6ac','#536b78','#b4d0cf','#e1e4ce','#b7c7d5','#f2e9d7'] if ice else ['#8c9981','#526a58','#b5bd92','#d7d4ab','#8eb084','#e9d9b0']
  Painter(out,pal,name).rock((1,3,31,24));d=ImageDraw.Draw(out)
  if ice:
   d.polygon([(5,10),(13,5),(24,8),(27,14),(20,12),(13,15),(8,13)],fill='#b6d5d3')
   curve(d,[(8,8),(12,11),(12,17)],'#e1e9d9');curve(d,[(25,10),(20,14),(22,20)],'#6e96a6')
  else:
   d.polygon([(4,10),(8,5),(16,4),(22,7),(28,10),(24,13),(17,11),(11,14),(7,11)],fill='#83a574')
   for x,y in [(7,7),(12,5),(18,7),(23,9),(13,11)]:d.line((x,y,x+2,y),fill='#b5c58a')
   d.point((8,8),fill='#e9c5aa');d.point((20,8),fill='#e5d391')
 elif name.startswith('props/chest_'):
  opened=name.endswith('_1');out=Image.new('RGBA',im.size);d=ImageDraw.Draw(out)
  d.rounded_rectangle((0,3,15,12),radius=2,fill='#6f5847');d.rounded_rectangle((1,4,14,11),radius=1,fill='#ad8c62')
  d.rounded_rectangle((0,0 if opened else 2,15,4 if opened else 7),radius=2,fill='#bfa175',outline='#79664e')
  if opened:d.rectangle((2,4,13,6),fill='#4e5147')
  for x in (3,12):d.line((x,4 if opened else 3,x,11),fill='#d6ba7e')
  d.rectangle((7,7,9,9),fill='#e7ce92');d.point((8,8),fill='#8b7656')
 elif name=='props/tablet':
  out=Image.new('RGBA',im.size);d=ImageDraw.Draw(out)
  d.rounded_rectangle((1,0,12,17),radius=4,fill='#667c78');d.rounded_rectangle((2,1,11,16),radius=3,fill='#acb7a0')
  d.line((4,3,9,3),fill='#d9d8bb');curve(d,[(4,6),(7,5),(9,7),(6,9),(7,12)],'#778d81')
  d.line((4,14,9,14),fill='#889c87')
 elif name=='tiles/gate':
  out=Image.new('RGBA',im.size);d=ImageDraw.Draw(out)
  for x in (1,7,13):
   d.rectangle((x,0,x+1,15),fill='#63737e');d.line((x,1,x,14),fill='#a6b5ad')
  for y in (1,11):
   d.rectangle((0,y,15,y+2),fill='#7c817b');d.line((1,y,14,y),fill='#c5b58c')
   for x in (2,8,14):d.point((x,y+1),fill='#e0c28c')
 elif name.startswith('props/lever_'):
  out=Image.new('RGBA',im.size);d=ImageDraw.Draw(out)
  d.rounded_rectangle((0,7,11,10),radius=2,fill='#63747a');d.line((2,7,9,7),fill='#afbaa7')
  right=name.endswith('_1');tip=8 if right else 2
  curve(d,[(6,8),(6,5),(tip,2)],'#c5af81',2)
  d.rounded_rectangle((tip-1,0,tip+2,3),radius=1,fill='#94b391' if right else '#bd8791')
  d.point((tip,0),fill='#e0d4af')
 return out

def main():
 paths=[*sorted((ROOT/'sprites/props').glob('*.png')),*sorted((ROOT/'sprites/items').glob('*.png')),
        *sorted((ROOT/'sprites/enemies').glob('*.png')),*sorted((ROOT/'sprites/npcs').glob('baby_slime_*.png')),
        ROOT/'sprites/tiles/gate.png']
 assets=[]
 for p in paths:
  key=str(p.relative_to(ROOT/'sprites').with_suffix(''));src=SOURCES/(key+'.png');src.parent.mkdir(parents=True,exist_ok=True)
  if not src.exists():shutil.copy2(p,src)
  before=Image.open(src).convert('RGBA');after=polish(key,before);assert before.size==after.size
  after.save(p)
  assets.append(dict(id=key,path=str(p.relative_to(ROOT)),category='enemies' if key.startswith('npcs/') else p.parent.name,region='play',anchor=[0,0] if p.parent.name=='tiles' else [after.width//2,after.height],sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 (ROOT/'art/gameplay-manifest.json').write_text(json.dumps({'assets':assets},ensure_ascii=False,indent=2)+'\n')
 font=ImageFont.truetype('/System/Library/Fonts/Hiragino Sans GB.ttc',18)
 sheet=Image.new('RGB',(1440,((len(paths)+7)//8)*145+48),'#263d40');d=ImageDraw.Draw(sheet)
 d.text((18,12),'冒险素材统一 · 每格左为原版，右为新版（同倍率）',font=font,fill='#e9d9b5')
 for i,p in enumerate(paths):
  x=i%8*180;y=i//8*145+46;key=str(p.relative_to(ROOT/'sprites').with_suffix(''))
  for k,pic in enumerate([Image.open(SOURCES/(key+'.png')),Image.open(p)]):
   scale=min(4,72//max(pic.size));pic=pic.resize((pic.width*scale,pic.height*scale),Image.Resampling.NEAREST)
   sheet.paste(pic,(x+10+k*86+(70-pic.width)//2,y+8+(88-pic.height)//2),pic)
  d.text((x+5,y+108),p.stem,font=font,fill='#b7c5af')
 (ROOT/'docs').mkdir(exist_ok=True);sheet.save(ROOT/'docs/gameplay-assets-unified.png')
 print('Unified',len(paths),'assets; character and NPC identity sprites untouched.')

if __name__=='__main__':main()
