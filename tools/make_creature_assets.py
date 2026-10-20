# 第二批敌人和机关的图：草原的刺猬、雷电塔的电球炮台、湖泊的跳鱼；拉杆和闸门。
# 用法：python3 tools/make_creature_assets.py  → 写出 sprites/<类别>/<名字>.png，然后运行 tools/embed_assets.py。
# 字符画，一个字母一个像素，'.' 透明；和其他敌人一样默认朝左，游戏里朝右时自动翻转。
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sprites')
ASSETS = {}
def A(name, pal, rows):
    w = len(rows[0]); assert all(len(r) == w for r in rows), (name, [len(r) for r in rows])
    ASSETS[name] = (rows, pal)

# 刺猬：棕色的刺、米色的脸；隔一会儿缩成刺球，这时踩不得
HEDGE = dict(o='#2a1a10', S='#6e4226', s='#a06a3a', F='#f0d8b0', e='#1a1010', N='#3a2020', f='#5a3a20')
A('enemies/hedgehog_0', HEDGE, [
'.....o.o.o.o....',
'....oSoSoSoSo...',
'...oSsSsSsSsSo..',
'..oSsSsSsSsSsSo.',
'.oFFoSsSsSsSsSo.',
'oFeFFoSsSsSsSSo.',
'NFFFFFoSsSsSsSo.',
'oFFFFFFoooooooo.',
'.oFFFFFFFFFFFo..',
'..ofo.....ofo...'])
A('enemies/hedgehog_1', HEDGE, [
'.....o.o.o.o....',
'....oSoSoSoSo...',
'...oSsSsSsSsSo..',
'..oSsSsSsSsSsSo.',
'.oFFoSsSsSsSsSo.',
'oFeFFoSsSsSsSSo.',
'NFFFFFoSsSsSsSo.',
'oFFFFFFoooooooo.',
'.oFFFFFFFFFFFo..',
'...ofo...ofo....'])
A('enemies/hedgehog_ball', HEDGE, [
'....o.o.o.o...',
'...oSoSoSoSo..',
'..oSsSsSsSsSo.',
'.oSsSsSsSsSsSo',
'oSsSsSsSsSsSso',
'.oSsSsSsSsSsSo',
'oSsSsSsSsSsSso',
'.oSsSsSsSsSsSo',
'..oSsSsSsSsSo.',
'...oSoSoSoSo..',
'....o.o.o.o...'])
# 电球炮台：铁皮箱子顶上一圈线圈，炮口朝左；蓄电时线圈发白
TUR = dict(o='#1a1a2a', G='#5a6a8a', g='#7a8aaa', C='#3a3a4a', Y='#e8c83a', W='#fff6b0', d='#3a4258')
A('enemies/turret_0', TUR, [
'......oooo......',
'.....oYYYo......',
'......oYo.......',
'....oooooooo....',
'...oGgGgGgGGo...',
'ooooGgGgGgGgGo..',
'oCCCoGgGgGgGGo..',
'ooooGgGgGgGgGo..',
'...oGGGGGGGGGo..',
'...oddddddddo...',
'..oddddddddddo..',
'..oooooooooooo..'])
A('enemies/turret_1', dict(TUR, Y='#ffffff', C='#e8c83a'), [
'.....oWWWWo.....',
'.....oYWYYo.....',
'......oYo.......',
'....oooooooo....',
'...oGgGgGgGGo...',
'ooooGgGgGgGgGo..',
'oCCCoGgGgGgGGo..',
'ooooGgGgGgGgGo..',
'...oGGGGGGGGGo..',
'...oddddddddo...',
'..oddddddddddo..',
'..oooooooooooo..'])
# 跳鱼：蓝色的小鱼，平时在水面下游，伊布靠近就跳出来
FISH = dict(o='#10203a', B='#3a8ad8', H='#8ac8ff', d='#24609e', k='#0a0a14', W='#ffffff', F='#ff8a6a')
A('enemies/fish_0', FISH, [
'.......oo.......',
'......oBBo..oo..',
'...ooBBBBBooFo..',
'..oBBHBBBBBoFFo.',
'.oWkBBBBBBBBFFo.',
'.oBBBBBBBBBBoFo.',
'..odBBBdBBdo.oo.',
'...oooooooo.....'])
A('enemies/fish_1', FISH, [
'.......oo.......',
'......oBBo......',
'...ooBBBBBo..oo.',
'..oBBHBBBBBooFo.',
'.oWkBBBBBBBBFFo.',
'.oBBBBBBBBBBFFo.',
'..odBBBdBBdooFo.',
'...oooooooo..oo.'])

# ---------------- 机关 ----------------
# 闸门（关卡字符 J）：铁栅栏，拉下同一间房里的拉杆就打开
A('tiles/gate', dict(o='#1a1a24', G='#6a7088', g='#9aa2bc', d='#3a3e50'), [
'oooooooooooooooo',
'oGgGoGgGoGgGoGgo',
'oGdGoGdGoGdGoGdo',
'oGdGoGdGoGdGoGdo',
'oGdGoGdGoGdGoGdo',
'oooooooooooooooo',
'oGgGoGgGoGgGoGgo',
'oGdGoGdGoGdGoGdo',
'oGdGoGdGoGdGoGdo',
'oGdGoGdGoGdGoGdo',
'oGdGoGdGoGdGoGdo',
'oooooooooooooooo',
'oGgGoGgGoGgGoGgo',
'oGdGoGdGoGdGoGdo',
'oGdGoGdGoGdGoGdo',
'oooooooooooooooo'])
# 拉杆（关卡字符 l）：碰一下就拉下来
LEV = dict(o='#1a1a24', B='#5a5a70', b='#8a8aa0', R='#e04a4a', r='#ff8a8a', W='#c8a070')
A('props/lever_0', LEV, [
'..oo........',
'.oRro.......',
'.oRRo.......',
'..ooW.......',
'....oW......',
'.....oW.....',
'......oW....',
'..oooooooo..',
'.obbbbbbbbo.',
'oBBBBBBBBBBo',
'oooooooooooo'])
A('props/lever_1', LEV, [
'........oo..',
'.......orRo.',
'.......oRRo.',
'.......Woo..',
'......Wo....',
'.....Wo.....',
'....Wo......',
'..oooooooo..',
'.obbbbbbbbo.',
'oBBBBBBBBBBo',
'oooooooooooo'])

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
    print('wrote', len(ASSETS), 'creature and mechanism assets')
