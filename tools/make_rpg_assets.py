# RPG 系统的小图标：材料（树果、电光石）和罗丝奶奶的料理（蘑菇汤、噼啪糖）。
# 用法：python3 tools/make_rpg_assets.py  → 写出 sprites/items/<名字>.png，然后运行 tools/embed_assets.py。
# 字符画，一个字母一个像素，'.' 透明。以后美术重画时直接替换同名 PNG 即可。
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sprites')
ASSETS = {}
def A(name, pal, rows):
    w = len(rows[0]); assert all(len(r) == w for r in rows), (name, [len(r) for r in rows])
    ASSETS[name] = (rows, pal)

# 树果：一对红色的小果子，和点心用的蓝莓区分开
A('items/mat_berry', dict(o='#4a1020', R='#e8406a', H='#ffb0c4', d='#a82848', g='#3f8a2e', G='#7fd060', s='#6a4a20'), [
'.......gg..',
'......gGGg.',
'.....s.s...',
'....s...s..',
'..ooo..ooo.',
'.oRHRooRHRo',
'.oRRRooRRRo',
'.oRRdooRRdo',
'..ooo..ooo.'])
# 电光石：黄色的小晶石，中间一道白光
A('items/mat_spark', dict(o='#3a3010', Y='#ffd83a', H='#fff6b0', W='#ffffff', d='#c89a1a'), [
'....oo....',
'...oYWo...',
'..oYYHYo..',
'.oYYHYYdo.',
'oYYYHYYYdo',
'oYYYYYYddo',
'.oYYYYddo.',
'..oYYddo..',
'...oddo...',
'....oo....'])
# 蘑菇汤：冒热气的碗，汤里漂着红蘑菇
A('items/dish_soup', dict(o='#3a2010', S='#e0a050', M='#c84a3a', m='#f0e0c0', B='#e8e0d0', H='#ffffff', d='#b0a090', s='#e8f0ff'), [
'...s..s.....',
'....s..s....',
'..oooooooo..',
'.oSMSSmSSSo.',
'oBBBBBBBBBBo',
'oBHBBBBBBBdo',
'.oBBBBBBBdo.',
'..oBBBBBdo..',
'...oooooo...'])
# 噼啪糖：粉色糖纸包着的黄色糖块
A('items/dish_candy', dict(o='#3a2a10', P='#ff9ac8', Y='#ffd84a', H='#fff6b0', W='#ffffff'), [
'.o........o.',
'oPo.oooo.oPo',
'oPPoYYWYoPPo',
'.oPYYYYHYPo.',
'.oPYHYYYYPo.',
'oPPoYYYYoPPo',
'oPo.oooo.oPo',
'.o........o.'])

def render(rows, pal):
    w, h = len(rows[0]), len(rows)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            ch = rows[y][x]
            if ch in '. ': continue
            c = pal[ch]; img.putpixel((x, y), (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 255))
    return img

if __name__ == '__main__':
    for name, (rows, pal) in ASSETS.items():
        p = os.path.join(ROOT, name + '.png'); os.makedirs(os.path.dirname(p), exist_ok=True)
        render(rows, pal).save(p)
    print('wrote', len(ASSETS), 'rpg assets')
