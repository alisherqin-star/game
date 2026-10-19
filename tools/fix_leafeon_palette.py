"""Correct only Leafeon's muddy body colours; preserve alpha and leaf/eye pixels."""
from pathlib import Path
from PIL import Image
from extract.make_shiny import shinify

ROOT=Path(__file__).resolve().parents[1]
# Explicit colour replacements avoid touching the dark outline or green leaves.
BODY={
 (208,170,132):(244,224,180),
 (172,148,127):(221,199,157),
 (155,125,103):(201,175,133),
 (130,98,83):(174,144,107),
 (91,90,81):(185,166,133),
}

def main():
 path=ROOT/'sprites/characters/leafeon.png'
 im=Image.open(path).convert('RGBA');out=im.copy();changed=0
 for y in range(im.height):
  for x in range(im.width):
   r,g,b,a=im.getpixel((x,y))
   if a and (r,g,b) in BODY:
    out.putpixel((x,y),(*BODY[(r,g,b)],a));changed+=1
 out.save(path)
 shinify('leafeon',out).save(path.with_name('leafeon_shiny.png'))
 print('Corrected',changed,'body pixels; regenerated only Leafeon shiny.')

if __name__=='__main__':main()
