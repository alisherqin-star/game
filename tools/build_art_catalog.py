"""Generate a self-contained review gallery + machine-readable asset manifest.
Does not embed into or change the game. Run after the three art generators.
"""
from pathlib import Path
import base64,json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; ART=ROOT/'art';ART.mkdir(exist_ok=True)
assets=[];data={}
for p in sorted((ROOT/'sprites').rglob('*.png')):
 if not p.stem.startswith(('forest_','biome_','env_')):continue
 im=Image.open(p);w,h=im.size; key=str(p.relative_to(ROOT/'sprites').with_suffix(''));raw=p.read_bytes()
 category=p.parent.name
 if 'forest_' in p.stem or any(n in p.stem for n in ['village','stump','bench','planter','fence','fern','berry','signpost']):region='forest'
 elif any(n in p.stem for n in ['shore','lake','reeds','pebbles','pier','mooring','canoe','lily','waterweed','river_stones']):region='lake'
 elif any(n in p.stem for n in ['cave','crystal','vine','stalag','stalact','mushroom','boulder']):region='cave'
 elif any(n in p.stem for n in ['tower','pillar','lamp','banner','gear','grate','coil','lever','torch']):region='tower'
 else:region='shared'
 ceiling=any(n in p.stem for n in ['stalactite','vine','banner','lamp'])
 anchor=[0,0] if category in ('tiles','backgrounds') else [w//2,0 if ceiling else h]
 asset={'id':key,'path':str(p.relative_to(ROOT)),'region':region,'category':category,'width':w,'height':h,'anchor':anchor,'anchorConvention':'pixel boundary, top-left origin','collision':'none; assign explicitly in level data','sha256':hashlib.sha256(raw).hexdigest()}
 if category=='tiles':asset['placement']='16px grid; variant chosen by stable tile-coordinate hash'
 if category=='backgrounds':asset.update({'repeat':'x','parallax':[.12,.23,.38][int(p.stem[-1])],'placement':'bottom aligned to camera viewport; render behind gameplay'})
 assets.append(asset);data[key]='data:image/png;base64,'+base64.b64encode(raw).decode()
animations=[{'id':'torch','frames':['deco/env_torch_'+str(i) for i in range(4)],'fps':8,'loop':True},{'id':'lily','frames':['deco/env_lily_'+str(i) for i in range(3)],'fps':3,'loop':True}]
for theme in ['lake','cave']:
 animations.append({'id':theme+'_surface','frames':['tiles/biome_'+theme+'_surface_'+str(i) for i in range(2)],'fps':4,'loop':True})
manifest={'version':1,'nativeTileSize':16,'filter':'nearest','coordinates':'x right, y down','alpha':'PNG RGBA, straight alpha','assets':assets,'animations':animations}
(ART/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
# Existing character is embedded only as a scale reference, never modified.
for name in ['eevee','vaporeon']:
 p=ROOT/'sprites/characters'/f'{name}.png';data['reference/'+name]='data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
template=(ART/'gallery-template.html').read_text()
(ART/'index.html').write_text(template.replace('/* MANIFEST */',json.dumps(manifest,ensure_ascii=False)).replace('/* DATA */',json.dumps(data)))
print(f'Built gallery and manifest: {len(assets)} scene assets, {len(animations)} animation groups.')
