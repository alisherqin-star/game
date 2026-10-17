"""Reproducible pixel art for the forest visual prototype (Pillow only).
Writes only forest_* assets; existing character art remains available as fallback.
Run this script, then tools/embed_assets.py. No downloaded art is used.
"""
from pathlib import Path
import random
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[1] / 'sprites'

def save(im, category, name):
    path = ROOT / category / ('forest_' + name + '.png')
    path.parent.mkdir(exist_ok=True)
    im.save(path)

# Clustered soil, pebbles and an irregular turf edge; variants have fixed seeds.
for variant in range(4):
    rng = random.Random(71 + variant)
    soil = Image.new('RGBA', (16, 16), '#624a3c')
    d = ImageDraw.Draw(soil)
    for _ in range(18):
        x, y = rng.randrange(16), rng.randrange(16)
        color = rng.choice(['#735443', '#805f49', '#513e36', '#927052'])
        d.rectangle((x, y, x + rng.randrange(1, 4), y + 1), fill=color)
    d.line((2, 7, 5, 7), fill='#a08360')
    d.point((12, 12), fill='#b0946a')
    save(soil, 'tiles', f'dirt_{variant}')
    turf = soil.copy(); d = ImageDraw.Draw(turf)
    for x in range(16):
        deep = 4 + rng.randrange(3)
        d.line((x, 0, x, deep), fill='#315341')
        d.line((x, 0, x, deep - 2), fill='#50834b')
        d.line((x, 0, x, 1), fill='#8cb866')
        if x % 3: d.point((x, 0), fill='#c0d98b')
    save(turf, 'tiles', f'grass_{variant}')

# Three irregular canopy trees, 80x112. Fine clusters sit on darker leaf masses.
for variant in range(3):
    rng = random.Random(140 + variant)
    im = Image.new('RGBA', (80, 112)); d = ImageDraw.Draw(im)
    d.polygon([(32,111),(35,71),(32,52),(38,47),(43,68),(45,105),(53,111)],fill='#283e36')
    d.polygon([(36,108),(38,65),(35,53),(39,53),(41,79),(41,108)],fill='#69563f')
    d.line([(39,84),(23,64),(17,63)],fill='#514b38',width=3)
    d.line([(41,73),(56,54),(62,53)],fill='#514b38',width=3)
    d.line((39,88,39,105),fill='#98815a',width=2)
    clusters=[(9,29,37,59),(23,10,53,44),(43,22,71,53),(18,36,59,68),(2,43,29,67),(49,42,77,66)]
    for x0,y0,x1,y1 in clusters:
        d.ellipse((x0,y0,x1,y1),fill='#264a3c')
        d.ellipse((x0+1,y0+1,x1-2,y1-6),fill='#37694a')
        d.ellipse((x0+3,y0+1,x1-6,y1-12),fill='#528551')
    for _ in range(115):
        x,y=rng.randrange(5,75),rng.randrange(12,66)
        if im.getpixel((x,y))[:3] in [(55,105,74),(82,133,81)]:
            d.rectangle((x,y,x+2,y+1),fill=rng.choice(['#729b5a','#8ead67','#456e49']))
    save(im,'deco',f'tree_{variant}')

for variant in range(4):
    im=Image.new('RGBA',(16,16)); d=ImageDraw.Draw(im)
    if variant < 2:
        for x,h in [(2,4),(5,8),(8,5),(11,9),(13,3)]:
            d.line((x,15,x-2,15-h),fill='#3e7046')
            d.point((x-2,15-h),fill='#a9bf73')
        if variant == 1:
            for x,y in [(4,7),(10,4)]:
                d.rectangle((x-1,y,x+1,y+2),fill='#d7b78d'); d.point((x,y+1),fill='#ffe6a8')
    else:
        for x,y in [(4,10),(10,7)]:
            d.rectangle((x,y,x+1,15),fill='#c4b294')
            d.rectangle((x-2,y-2,x+3,y),fill='#985f58' if variant==2 else '#77a19a')
            d.line((x-1,y-3,x+2,y-3),fill='#d4a38a' if variant==2 else '#b6dbbd')
            d.point((x,y-2),fill='#f3dcb4')
    save(im,'deco',f'plant_{variant}')

print('Forest environment assets generated. Run python3 tools/embed_assets.py next.')
