"""Bring remaining gameplay tiles into the scene palette without changing geometry."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
from pixel_nature import terrain

ROOT=Path(__file__).resolve().parents[1]
STONE=['#777584','#494d65','#a3a4a3','#c3beb0','#8b929a','#e2d4b1']
WOOD=['#a08462','#655b51','#bba37d','#dfc698','#91a27f','#f1ddb2']

def main():
 assets=[]
 def save(name,im):
  path=ROOT/'sprites/tiles'/f'{name}.png';im.save(path)
  assets.append(dict(id='tiles/'+name,path=str(path.relative_to(ROOT)),region='shared',anchor=[0,0]))
 for name,kind,v in [('stone','brick',0),('rock','basalt',1),('brick','brick',2),('cracked','basalt',3)]:
  palette=['#927f7a','#655c68','#c0a592','#ddc3a3','#9c9b88','#f1d9b1'] if name=='brick' else STONE
  im=terrain('tower',palette,kind,v)[0]
  if name=='cracked':
   d=ImageDraw.Draw(im);d.line([(8,0),(6,4),(9,7),(6,11),(8,15)],fill='#45485b');d.line([(9,7),(13,8),(14,11)],fill='#45485b');d.line((7,3,9,5),fill='#b9b9b3')
  save(name,im)
 for name in ['platform','crate','door','spikes','fence_0','fence_1','shadow_0','shadow_1','lava_0','lava_1']:
  im=Image.new('RGBA',(16,16));d=ImageDraw.Draw(im)
  if name=='platform':
   d.rectangle((0,0,15,4),fill='#746653');d.line((0,0,15,0),fill='#d2bc91');d.rectangle((0,1,15,2),fill='#b89d76');d.line((1,3,7,3),fill='#9b835f');d.line((10,3,14,3),fill='#9b835f')
  elif name=='crate':
   im=terrain('heartwood',WOOD,'wood',1)[0];d=ImageDraw.Draw(im)
   d.rounded_rectangle((0,0,15,15),radius=1,outline='#64574b');d.rectangle((1,1,14,14),outline='#ceb38b')
   d.line((2,12,12,2),fill='#695c4b',width=3);d.line((3,13,13,3),fill='#bea27c',width=2)
   for x,y in [(2,2),(13,2),(2,13),(13,13)]:d.point((x,y),fill='#e2cba1')
  elif name=='door':
   d.rounded_rectangle((0,0,15,15),radius=2,fill='#646178',outline='#b3a78d');d.rectangle((3,1,12,14),fill='#80758a');d.line((4,3,11,3),fill='#a99aab')
   d.arc((6,5,10,10),180,360,fill='#e3c892');d.rectangle((6,8,10,11),fill='#d5b376');d.point((8,9),fill='#65546b')
  elif name=='spikes':
   for x,h in [(0,7),(5,10),(11,8)]:
    d.polygon([(x,15),(x+2,15-h),(min(15,x+5),15)],fill='#a2b3ba',outline='#536277');d.line((x+2,16-h,x+1,13),fill='#e0dbce')
   d.line((0,15,15,15),fill='#5f697d')
  elif name.startswith('fence'):
   f=int(name[-1]);d.rectangle((0,0,2,15),fill='#6e6b70');d.line((0,0,2,0),fill='#b8b9a6');d.line((0,7,2,7),fill='#e1be76')
   d.line([(8+f,0),(6+f,4),(10-f,7),(7+f,11),(9-f,15)],fill='#7bc9cd',width=3);d.line([(8+f,0),(6+f,4),(10-f,7),(7+f,11),(9-f,15)],fill='#f6e9b5');d.point((13-f,6+f),fill='#b5dfe0')
  elif name.startswith('shadow'):
   f=int(name[-1]);d.rounded_rectangle((0,0,15,15),radius=2,fill='#60546f');d.line([(1,4+f),(5,2),(10,5),(15,3+f)],fill='#8d769b');d.line([(0,12),(5,10-f),(10,13),(15,11)],fill='#443e5e');d.point((11,8+f),fill='#bf9cac');d.line([(6,6+f),(8,4+f),(10,6+f),(8,8+f),(6,6+f)],fill='#bba2cd');d.point((8,6+f),fill='#ded0df')
  else:
   f=int(name[-1]);d.rectangle((0,0,15,15),fill='#c76c50');d.polygon([(0,3+f),(4,1),(9,3),(15,1),(15,7),(10,9),(5,7),(0,10)],fill='#ef995b')
   d.line([(0,2+f),(4,0),(9,2),(15,0)],fill='#ffdc8e',width=2)
   d.arc((2+f,10,7+f,14),180,345,fill='#f0b77b');d.line((11-f,12,14-f,12),fill='#9e5e5a')
  save(name,im)
 (ROOT/'art/utility-manifest.json').write_text(json.dumps(dict(assets=assets),ensure_ascii=False,indent=2)+'\n')
 print('Unified',len(assets),'utility tiles; collision sizes remain 16×16.')

if __name__=='__main__':main()
