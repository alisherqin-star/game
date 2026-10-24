"""First monster-state batch: native pixel grids, original-family palettes, left-facing.

Run this, build_art_catalog.py, then embed_assets.py. Does not edit game logic.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'sprites/enemies'
SLIME = {'o':'#4b3554', 'b':'#7d5aa5', 'h':'#a376d1', 's':'#71498e', 'w':'#f6ead0', 'p':'#424041'}
BAT = {'ink':'#3f3548', 'body':'#645681', 'light':'#8a78b2', 'shade':'#4f4360',
       'eye':'#f6ead0', 'coral':'#f26f68', 'mouth':'#302a3c'}
FROG = {'ink':'#426232', 'body':'#75bf5c', 'light':'#a4de81', 'shade':'#589443',
        'belly':'#e0e49f', 'eye':'#f6ead0', 'pupil':'#424041'}


def grid(rows, palette):
    w = len(rows[0])
    assert all(len(r) == w for r in rows), [(r, len(r)) for r in rows]
    im = Image.new('RGBA', (w, len(rows)))
    d = ImageDraw.Draw(im)
    for y, row in enumerate(rows):
        for x, key in enumerate(row):
            if key != '.':
                d.point((x, y), fill=palette[key])
    return im


def small_slime(frame):
    rows = [
        '....oooo....',
        '..oohhhhoo..',
        '.ohbbbbbbbo.',
        '.obbbbbbbbo.',
        'obbbbbbbbbbo',
        'obbbbbbbbbbo',
        'obbbbbbbbbbo',
        '.obbbbbbsso.',
        '.osssssssso.',
        '..oooooooo..',
    ] if frame == 0 else [
        '............',
        '...oooooo...',
        '.oohhhhhhoo.',
        'ohbbbbbbbbho',
        'obbbbbbbbbbo',
        'obbbbbbbbbbo',
        'obbbbbbbbbbo',
        'obbbbbbbbsso',
        '.osssssssso.',
        '..oooooooo..',
    ]
    im = grid(rows, SLIME)
    d = ImageDraw.Draw(im)
    y = 4 + frame
    # The face is biased toward the left; pupils stay on each eye's leading edge.
    for x in (2, 6):
        d.rectangle((x, y, x + 1, y + 1), fill=SLIME['w'])
        d.point((x, y + 1), fill=SLIME['p'])
    d.point((2, y - 1), fill=SLIME['o'])
    d.point((3, y), fill=SLIME['o'])
    d.point((6, y), fill=SLIME['o'])
    d.point((7, y - 1), fill=SLIME['o'])
    d.line((3, 7 + frame, 5, 7 + frame), fill=SLIME['o'])
    return im


def diving_bat(frame):
    im = Image.new('RGBA', (16, 12))
    d = ImageDraw.Draw(im)
    # Wings sweep behind the head (upper right), instead of the symmetric cruise pose.
    if frame == 0:
        d.polygon([(6, 7), (4, 4), (5, 1), (8, 4), (10, 6)], fill=BAT['ink'])
        d.polygon([(6, 5), (6, 3), (9, 6)], fill=BAT['body'])
        d.polygon([(7, 6), (8, 3), (12, 0), (12, 4), (15, 1), (14, 6), (10, 8)], fill=BAT['ink'])
        d.polygon([(8, 5), (11, 2), (11, 5), (14, 3), (13, 6), (10, 7)], fill=BAT['body'])
        d.line((10, 4, 11, 3), fill=BAT['light'])
    else:
        d.polygon([(6, 7), (5, 4), (7, 3), (10, 6)], fill=BAT['ink'])
        d.polygon([(7, 5), (7, 4), (9, 6)], fill=BAT['body'])
        d.polygon([(7, 6), (11, 3), (15, 3), (13, 5), (15, 6), (12, 8), (9, 9)], fill=BAT['ink'])
        d.polygon([(9, 6), (11, 4), (13, 4), (12, 6), (14, 6), (11, 7)], fill=BAT['body'])
        d.line((10, 5, 11, 4), fill=BAT['light'])
    # Both frames share the eye/mouth position so the attack remains readable in motion.
    d.polygon([(5, 4), (7, 3), (8, 5), (10, 6), (9, 9), (7, 11), (3, 11), (1, 9), (2, 7), (4, 6)], fill=BAT['ink'])
    d.polygon([(5, 6), (7, 5), (9, 6), (8, 9), (6, 10), (3, 10), (2, 9), (3, 8), (5, 7)], fill=BAT['body'])
    d.line((6, 5, 7, 6), fill=BAT['light'])
    d.point((3, 7), fill=BAT['eye']); d.point((4, 7), fill=BAT['coral'])
    d.point((6, 6), fill=BAT['eye']); d.point((7, 6), fill=BAT['coral'])
    d.rectangle((2, 8, 5, 10), fill=BAT['mouth'])
    d.point((2, 8), fill=BAT['eye']); d.point((5, 8), fill=BAT['eye'])
    d.line((3, 9, 4, 9), fill=BAT['coral'])
    return im


def landing_frog():
    im = Image.new('RGBA', (18, 10))
    d = ImageDraw.Draw(im)
    # Broad haunches and splayed feet preserve mass while the torso compresses.
    d.polygon([(3, 3), (14, 3), (17, 5), (17, 7), (15, 8), (17, 8),
               (17, 9), (12, 9), (11, 8), (5, 8), (4, 9), (0, 9),
               (0, 8), (2, 7), (1, 5), (2, 4)], fill=FROG['ink'])
    d.polygon([(3, 4), (13, 4), (16, 5), (16, 7), (13, 7), (11, 7),
               (5, 7), (3, 8), (1, 8), (3, 6), (2, 5)], fill=FROG['body'])
    d.line((13, 5, 15, 6), fill=FROG['shade'])
    d.rectangle((3, 6, 11, 7), fill=FROG['belly'])
    d.line((2, 8, 3, 8), fill=FROG['body'])
    d.line((13, 8, 16, 8), fill=FROG['body'])
    for x in (3, 9):
        d.polygon([(x, 0), (x + 2, 0), (x + 3, 2), (x + 3, 4), (x - 1, 4), (x - 1, 2)], fill=FROG['ink'])
        d.rectangle((x, 1, x + 1, 3), fill=FROG['eye'])
        d.point((x, 2), fill=FROG['pupil'])
        d.line((x, 4, x + 2, 4), fill=FROG['body'])
    d.point((3, 5), fill=FROG['light'])
    return im


def review():
    # Integer enlargement on contrasting backgrounds; native-sized strips below.
    groups = [
        ('Small slime: wild / left-facing', ['slime_small_0', 'slime_small_1'], ['slime_0']),
        ('Bat: cruise > dive', ['bat_dive_0', 'bat_dive_1'], ['bat_0', 'bat_1']),
        ('Frog: crouch > jump > landing', ['frog_land'], ['frog_0', 'frog_1']),
    ]
    out = Image.new('RGB', (960, 648), '#25343d')
    d = ImageDraw.Draw(out)
    f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 18)
    small = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 13)
    for row, (label, names, refs) in enumerate(groups):
        top = row * 216
        d.text((18, top + 10), label, font=f, fill='#e9dec1')
        for i, name in enumerate(refs + names):
            x = 18 + i * 188
            bg = '#d5d2b8' if i < len(refs) else '#53675c'
            d.rectangle((x, top + 40, x + 174, top + 181), fill=bg)
            pic = Image.open(OUT / (name + '.png')).convert('RGBA')
            big = pic.resize((pic.width * 7, pic.height * 7), Image.Resampling.NEAREST)
            out.paste(big, (x + (174 - big.width) // 2, top + 154 - big.height), big)
            out.paste(pic, (x + 146, top + 163), pic)
            d.text((x, top + 186), name + '  ' + str(pic.size), font=small, fill='#e9dec1')
    path = ROOT / 'docs/monster-batch1-review.png'
    out.save(path)


def main():
    frames = {'slime_small_0': small_slime(0), 'slime_small_1': small_slime(1),
              'bat_dive_0': diving_bat(0), 'bat_dive_1': diving_bat(1), 'frog_land': landing_frog()}
    manifest_path = ROOT / 'art/gameplay-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    ids = {'enemies/' + name for name in frames}
    manifest['assets'] = [a for a in manifest['assets'] if a['id'] not in ids]
    for name, im in frames.items():
        path = OUT / (name + '.png')
        im.save(path)
        manifest['assets'].append({'id': 'enemies/' + name, 'path': str(path.relative_to(ROOT)),
                                   'category': 'enemies', 'region': 'play',
                                   'anchor': [im.width // 2, im.height],
                                   'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    review()
    print('Built first batch: 5 native-grid, left-facing enemy state PNGs; catalog metadata registered.')


if __name__ == '__main__':
    main()
