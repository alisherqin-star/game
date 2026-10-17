"""Check manifest integrity, deterministic IDs and animation compatibility."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'art/manifest.json').read_text()); assets={a['id']:a for a in m['assets']}
assert len(assets)==len(m['assets']), 'Duplicate resource id'
for a in assets.values():
 p=ROOT/a['path'];im=Image.open(p)
 assert im.mode=='RGBA',a['id']
 assert list(im.size)==[a['width'],a['height']],a['id']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256'],a['id']
 assert 0<=a['anchor'][0]<=im.width and 0<=a['anchor'][1]<=im.height,a['id']
 assert 'characters/' not in a['path'],a['id']
 if a['category']=='tiles':assert im.size==(16,16),a['id']
 if a['category']=='backgrounds':assert im.size==(384,224),a['id']
for a in m['animations']:
 frames=[assets[k] for k in a['frames']]
 assert len({(f['width'],f['height'],tuple(f['anchor'])) for f in frames})==1,a['id']
 assert a['fps']>0
print(f"Validated {len(assets)} images and {len(m['animations'])} animation groups.")
