# 进化相关素材：三颗进化石、苔藓岩 / 冰岩、太阳 / 月亮标记、缎带、迷路的小史莱姆。
# 用法：python3 tools/make_evolution_assets.py  → 写出 sprites/<类别>/<名字>.png，然后运行 tools/embed_assets.py。
# 小图是字符画（一个字母一个像素，'.' 透明）；两块巨石用固定种子程序生成，重复运行结果不变。
import os, random
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sprites')
ASSETS = {}
def A(name, pal, rows):
    w = len(rows[0]); assert all(len(r) == w for r in rows), (name, [len(r) for r in rows])
    ASSETS[name] = (rows, pal)

# ---------------- 进化石 14x14（原作：水之石蓝底水滴纹、雷之石黄绿底闪电纹、火之石橙底火焰纹） ----------------
A('items/water_stone', dict(o='#13234f', B='#3f7fe0', H='#a8d4ff', L='#d6f0ff', W='#ffffff', d='#24509e'), [
'.....oooo.....',
'...ooBBBBoo...',
'..oBHHBBBBBo..',
'.oBHHBBLBBBBo.',
'.oBHBBLLLBBBo.',
'oBBBBLLWLLBBBo',
'oBBBBLWLLLBBBo',
'oBBBBLLLLLBBBo',
'oBBBBBLLLBBBdo',
'.oBBBBBBBBBdo.',
'.odBBBBBBBddo.',
'..oddBBBBddo..',
'...ooddddoo...',
'.....oooo.....'])
A('items/thunder_stone', dict(o='#26360c', G='#9ad04a', H='#dcf29a', Y='#ffe94a', d='#5f8f22'), [
'.....oooo.....',
'...ooGGGGoo...',
'..oGHHGGGGGo..',
'.oGHHGGGYYGGo.',
'.oGHGGGYYGGGo.',
'oGGGGGYYGGGGGo',
'oGGGGYYYYYGGGo',
'oGGGGGGGYYGGGo',
'oGGGGGGYYGGGdo',
'.oGGGGYYGGGdo.',
'.odGGGYGGGddo.',
'..oddGGGGddo..',
'...ooddddoo...',
'.....oooo.....'])
A('items/fire_stone', dict(o='#4a1a08', R='#ee6a2a', H='#ffb070', Y='#ffd23c', W='#fff4c0', d='#b8401a'), [
'.....oooo.....',
'...ooRRRRoo...',
'..oRHHRRRRRo..',
'.oRHHRRYRRRRo.',
'.oRHRRRYRRRRo.',
'oRRRRRYYYRRRRo',
'oRRRRYYWYRRRRo',
'oRRRYYWWYYRRRo',
'oRRRYYWWYYRRdo',
'.oRRRYYYYRRdo.',
'.odRRRRRRRddo.',
'..oddRRRRddo..',
'...ooddddoo...',
'.....oooo.....'])

# ---------------- 背包里的条件图标 ----------------
A('items/sun_mark', dict(o='#8a4a08', S='#ffc83a', H='#fff4c0', d='#e89a1a', y='#ffe14a'), [
'.....yy.....',
'.y........y.',
'..y.oooo.y..',
'...oSSSSo...',
'..oSHHSSSo..',
'yyoSHSSSSoyy',
'yyoSSSSSSoyy',
'..oSSSSSdo..',
'...oSSSdo...',
'..y.oooo.y..',
'.y........y.',
'.....yy.....'])
A('items/moon_mark', dict(o='#2a2a50', M='#f5d442', H='#fff6b0'), [
'....oooo....',
'..ooMMMMoo..',
'.oMHMMoo....',
'.oMHMo......',
'oMHMo.......',
'oMMMo.......',
'oMMMo.......',
'oMMMo.......',
'.oMMMo......',
'.oMMMMoo....',
'..ooMMMMoo..',
'....oooo....'])
# 仙子伊布的缎带：粉色蝴蝶结 + 蓝色飘带
A('items/ribbon', dict(o='#6a1a3a', P='#f6a8c8', H='#ffffff', K='#e0608a', B='#7fc8f0'), [
'.ooo......ooo.',
'oPPPo....oPPPo',
'oPHPPo..oPPHPo',
'oPPPPPooPPPPPo',
'.oPPPPKKPPPPo.',
'..ooPPKKPPoo..',
'...oBBooBBo...',
'..oBBo..oBBo..',
'.oBBo....oBBo.',
'.ooo......ooo.'])

# ---------------- 古代石板 14x18（彩蛋：刻着进化线索的谜语） ----------------
A('props/tablet', dict(o='#22263a', S='#8f93a8', H='#c2c6d6', d='#5f6378', g='#7fe8ff', G='#c8f8ff', m='#4f8a3a'), [
'....oooooo....',
'..ooHHHHSSoo..',
'.oHHSSSSSSSdo.',
'.oHSSSSSSSSdo.',
'oHSSgGgSgGSSdo',
'oHSSSSSSSSSSdo',
'oHSgSSgGgSSSdo',
'oHSSSSSSSSSSdo',
'oHSSGgSSgSSSdo',
'oHSSSSSSSSSSdo',
'oHSgGgSSGgSSdo',
'oHSSSSSSSSSSdo',
'oHSSSgSSSSSSdo',
'oSSSSSSSSSSSdo',
'oSdSSSSSSSSddo',
'ommdddddddddmo',
'oommmmmmmmmmoo',
'.oooooooooooo.'])

# ---------------- 迷路的小史莱姆 12x10，两帧（比敌人史莱姆小、颜色更浅、腮红） ----------------
P_BABY = dict(o='#3a1a5a', B='#c9a3ff', H='#ece0ff', d='#9a73d8', w='#ffffff', e='#1a1020', m='#7a3a9a', t='#ff9ac0')
A('npcs/baby_slime_0', P_BABY, [
'....oooo....',
'..ooHHHHoo..',
'.oHHBBBBHHo.',
'.oBwwBBwwBo.',
'oBBweBBweBBo',
'oBBwwBBwwBBo',
'oBtBBmmBBtBo',
'oBBBBBBBBBBo',
'.oddBBBBddo.',
'..oooooooo..'])
A('npcs/baby_slime_1', P_BABY, [
'............',
'...oooooo...',
'.ooHHHHHHoo.',
'oHBwwBBwwBHo',
'oBBweBBweBBo',
'oBBwwBBwwBBo',
'oBtBBmmBBtBo',
'oBBBBBBBBBBo',
'oddBBBBBBddo',
'.oooooooooo.'])

# ---------------- 巨石 32x24（程序生成） ----------------
def boulder(seed, stone, moss, frost):
    """椭圆巨石 + 顶部覆盖物。stone/moss 是 (暗, 中, 亮) 三色；frost=True 时覆盖物画成冰棱。"""
    rnd = random.Random(seed)
    W, H = 32, 24
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cx, cy, rx, ry = 15.5, 14.0, 15.0, 10.0
    inside = lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0 and y <= H - 1
    hexc = lambda c: (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 255)
    outline = hexc('#1c2420' if not frost else '#1a2c40')
    # 覆盖物下沿：每列一个高度，起伏平滑
    edge, h = [], 14.0
    for x in range(W):
        h += rnd.uniform(-1.4, 1.4); h = max(11.5, min(16.0, h)); edge.append(h)
    for y in range(H):
        for x in range(W):
            if not inside(x, y): continue
            border = not (inside(x - 1, y) and inside(x + 1, y) and inside(x, y - 1) and inside(x, y + 1))
            if border: img.putpixel((x, y), outline); continue
            shade = (x - cx) / rx * 0.6 + (y - cy) / ry * 0.8          # 左上亮、右下暗
            top = y < edge[x] or (frost and y < edge[x] + (2 if x % 5 == 2 else 0))   # 冰棱往下挂
            pal = moss if top else stone
            k = 2 if shade < -0.45 else (0 if shade > 0.35 else 1)
            if rnd.random() < 0.10: k = max(0, k - 1)                    # 斑点纹理
            img.putpixel((x, y), hexc(pal[k]))
    # 覆盖物下沿的垂挂（苔藓垂须 / 冰柱）
    for x in range(3, W - 3, 3):
        y0 = int(edge[x])
        for d in range(rnd.randint(1, 3)):
            if inside(x, y0 + d) and img.getpixel((x, y0 + d))[3]: img.putpixel((x, y0 + d), hexc(moss[0 if not frost else 2]))
    # 覆盖物在石面下半部再点缀几块（苔斑 / 霜斑）
    for _ in range(6):
        bx, by = rnd.randint(5, W - 7), rnd.randint(int(cy) + 2, H - 4)
        for dx in range(rnd.randint(2, 4)):
            for dy in range(rnd.randint(1, 2)):
                x, y = bx + dx, by + dy
                if inside(x, y) and img.getpixel((x, y)) != outline and img.getpixel((x, y))[3]: img.putpixel((x, y), hexc(moss[1]))
    # 高光点
    for _ in range(5):
        x, y = rnd.randint(6, 14), rnd.randint(6, 12)
        if inside(x, y) and img.getpixel((x, y)) != outline: img.putpixel((x, y), hexc('#ffffff' if frost else moss[2]))
    return img

EXTRA = {
    'props/moss_rock': boulder(7, stone=('#5c615a', '#80867c', '#a9aea2'), moss=('#2f7a28', '#4fa53a', '#8fd65a'), frost=False),
    'props/ice_rock':  boulder(11, stone=('#4f7896', '#7fb0cf', '#b8dcf0'), moss=('#8cc8ea', '#c8ecff', '#ffffff'), frost=True),
}

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
    out = {name: render(rows, pal) for name, (rows, pal) in ASSETS.items()}
    out.update(EXTRA)
    for name, img in out.items():
        p = os.path.join(ROOT, name + '.png'); os.makedirs(os.path.dirname(p), exist_ok=True)
        img.save(p)
    print('wrote', len(out), 'evolution assets')
