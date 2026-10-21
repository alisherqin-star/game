"""Transparent, limited-palette pixel title marks, generated at native resolution.

No external game logo or generated illustration is used. Oakbound capitals are
individually drawn; CJK lettering is rasterized to a hard pixel grid before inking.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];SIZE=(240,104)
FONTS=Path('/System/Library/Fonts/Supplemental')
GLYPHS={
'O':['..11111..','.11...11.','11.....11','11.....11','11.....11','11.....11','11.....11','11.....11','11.....11','.11...11.','..11111..'],
'A':['...111...','..11.11..','..11.11..','.11...11.','.11...11.','11.....11','111111111','11.....11','11.....11','11.....11','111...111'],
'K':['111...111','.11...11.','.11..11..','.11.11...','.1111....','.111.....','.1111....','.11.11...','.11..11..','.11...11.','111...111'],
'B':['1111111..','.11...11.','.11....11','.11....11','.11...11.','.111111..','.11...11.','.11....11','.11....11','.11...11.','1111111..'],
'U':['111...111','.11...11.','.11...11.','.11...11.','.11...11.','.11...11.','.11...11.','.11...11.','.11...11.','..11.11..','...111...'],
'N':['111....11','.111...11','.111...11','.1111..11','.11.11.11','.11.11.11','.11..1111','.11...111','.11...111','.11....11','111....11'],
'D':['111111...','.11..11..','.11...11.','.11....11','.11....11','.11....11','.11....11','.11....11','.11...11.','.11..11..','111111...']}

def font(size,cjk=False,italic=False):
 if cjk:return ImageFont.truetype('/System/Library/Fonts/Hiragino Sans GB.ttc',size,index=2)
 return ImageFont.truetype(str(FONTS/('Georgia Italic.ttf' if italic else 'Georgia Bold.ttf')),size)

def words_mask(lines,cjk=False):
 m=Image.new('L',SIZE);d=ImageDraw.Draw(m)
 for label,y,size,italic in lines:
  f=font(size,cjk,italic);box=d.textbbox((0,0),label,font=f);width=box[2]-box[0]
  d.text(((SIZE[0]-width)//2-box[0],y-box[1]),label,font=f,fill=255)
 return m.point(lambda x:255 if x>=145 else 0)

def ink(mask,solid=False):
 out=Image.new('RGBA',SIZE);edge=mask.filter(ImageFilter.MaxFilter(3 if solid else 5))
 out.paste('#334d40',(0,0),edge)
 shift=Image.new('L',SIZE);shift.paste(mask,(0,2));out.paste('#89764f',(0,0),shift)
 rows=Image.new('RGBA',SIZE);d=ImageDraw.Draw(rows)
 box=mask.getbbox() or (0,0,*SIZE);a,b=box[1],box[3]
 for y in range(SIZE[1]):
  t=(y-a)/max(1,b-a);c='#f5e7bd' if t<.38 else '#e5ce97' if t<.75 else '#c7ab72';d.line((0,y,SIZE[0],y),fill=c)
 out.paste(rows,(0,0),mask)
 shifted=Image.new('L',SIZE);shifted.paste(mask,(1,1));ridge=ImageChops.subtract(mask,shifted)
 if not solid:out.paste('#fff2ce',(0,0),ridge)
 return out

def decoration(out,secondary=False):
 d=ImageDraw.Draw(out)
 # One small acorn seal replaces the loose sprigs; the same mark anchors all languages.
 d.line((43,86,105,86),fill='#a29265');d.line((135,86,197,86),fill='#a29265')
 d.point((40,86),fill='#d5c28a');d.point((200,86),fill='#d5c28a')
 d.polygon([(112,83),(127,83),(126,91),(120,98),(114,92)],fill='#30483f')
 d.polygon([(114,85),(125,85),(124,91),(120,95),(116,91)],fill='#c1a16a')
 d.line((116,86,116,90),fill='#ebcf94')
 d.rectangle((112,81,127,85),fill='#6b7c50');d.line((113,81,126,81),fill='#b4b578')
 d.line((120,77,120,81),fill='#aeb27c')
 d.polygon([(120,78),(124,73),(131,72),(129,77),(124,80)],fill='#8f9c65')
 return out

def make(kind,lang):
 if kind=='oakbound' and lang=='en':
  mask=Image.new('L',SIZE);d=ImageDraw.Draw(mask);x=33
  for ch in 'OAKBOUND':
   for y,row in enumerate(GLYPHS[ch]):
    for col,value in enumerate(row):
     if value=='1':d.rectangle((x+col*2,34+y*3,x+col*2+1,36+y*3),fill=255)
   x+=22
  title=ink(mask,solid=True)
  sub=words_mask([("EEVEE'S ADVENTURE",12,12,False)])
 elif kind=='oakbound':
  label='橡树的约定' if lang=='zh' else 'オークの約束'
  mask=Image.new('L',SIZE);d=ImageDraw.Draw(mask)
  f=font(34,True) if lang=='zh' else ImageFont.truetype('/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc',32)
  box=d.textbbox((0,0),label,font=f);d.text(((240-(box[2]-box[0]))//2-box[0],33-box[1]),label,font=f,fill=255)
  title=ink(mask.point(lambda x:255 if x>=128 else 0),solid=True)
  sub=words_mask([('伊布冒险物语' if lang=='zh' else 'イーブイ冒険物語',11,13,False)],True)
 else:
  if lang=='en':title=ink(words_mask([('A PROMISE',26,21,False),('TO RETURN',49,18,False)]),solid=True)
  else:title=ink(words_mask([('归途的约定' if lang=='zh' else '帰り道の約束',34,32 if lang=='zh' else 29,False)],True),solid=True)
  sub=Image.new('L',SIZE)
 out=decoration(title)
 shadow=sub.filter(ImageFilter.MaxFilter(3));out.paste('#30483f',(0,0),shadow);out.paste('#e7dcb9',(0,0),sub)
 return out

def main():
 out=ROOT/'sprites/ui';out.mkdir(exist_ok=True);assets=[]
 for kind in ['homeward','oakbound']:
  for lang in ['zh','ja','en']:
   im=make(kind,lang);p=out/f'title_logo_{kind}_{lang}.png';im.save(p)
   assets.append(dict(id=f'ui/{p.stem}',path=str(p.relative_to(ROOT)),width=240,height=104,anchor=[120,52],language=lang,titleVariant=kind,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 (ROOT/'art/title-logo-manifest.json').write_text(json.dumps(dict(version=1,transparent=True,pixelEdges=True,assets=assets),ensure_ascii=False,indent=2)+'\n')
 sheet=Image.new('RGB',(1440,610),'#293f37');d=ImageDraw.Draw(sheet)
 f=font(24,True)
 for row,kind in enumerate(['oakbound','homeward']):
  d.text((28,row*300+12),'伊布冒险物语：橡树的约定 / Oakbound' if kind=='oakbound' else '旧名备选：归途的约定',font=f,fill='#e9dabc')
  for col,lang in enumerate(['zh','en','ja']):
   pic=make(kind,lang).resize((480,208),Image.Resampling.NEAREST);sheet.paste(pic,(col*480,row*300+62),pic)
   d.text((col*480+192,row*300+260),{'zh':'中文','en':'English','ja':'日本語'}[lang],font=font(17,True),fill='#a9bba0')
 sheet.save(ROOT/'docs/title-logo-options.png')
 sheet.crop((0,0,1440,300)).save(ROOT/'docs/title-logo-current.png')
 print('Built 6 transparent pixel title images and a comparison sheet.')
if __name__=='__main__':main()
