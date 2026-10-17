# 伊布及进化形态像素图生成器（28x26，按形状拼接 + 自动描边）
import json, math
W, H = 28, 26
def new(): return [['.']*W for _ in range(H)]
def ell(g, cx, cy, rx, ry, ch):
    for y in range(H):
        for x in range(W):
            if ((x+0.5-cx)/rx)**2 + ((y+0.5-cy)/ry)**2 <= 1: g[y][x] = ch
def poly(g, pts, ch):
    n = len(pts)
    for y in range(H):
        for x in range(W):
            px, py = x+0.5, y+0.5; inside = False
            for i in range(n):
                x1,y1 = pts[i]; x2,y2 = pts[(i+1)%n]
                if (y1 > py) != (y2 > py):
                    xi = x1 + (py-y1)*(x2-x1)/(y2-y1)
                    if px < xi: inside = not inside
            if inside: g[y][x] = ch
def rect(g, x0, y0, w, h, ch):
    for y in range(y0, y0+h):
        for x in range(x0, x0+w):
            if 0 <= x < W and 0 <= y < H: g[y][x] = ch
def put(g, x, y, ch):
    if 0 <= x < W and 0 <= y < H: g[y][x] = ch
def outline(g, protect=set()):
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' or g[y][x] in protect: continue
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x+dx, y+dy
                if nx<0 or ny<0 or nx>=W or ny>=H or g[ny][nx]=='.':
                    out[y][x] = 'o'; break
    return out
def edge(g, a, b):
    """在颜色 a 与 b 的交界处（a 一侧）画描边"""
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != a: continue
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x+dx, y+dy
                if 0<=nx<W and 0<=ny<H and g[ny][nx]==b: out[y][x]='o'; break
    return out

def part(g, fn, *a, **k):
    """在空白层上绘制部件、描边，再叠加到主图上"""
    layer = new(); fn(layer, *a, **k); layer = outline(layer)
    for y in range(H):
        for x in range(W):
            if layer[y][x] != '.': g[y][x] = layer[y][x]
def legs(g, walk, col='b'):
    # 后腿、前腿；walk 时错开
    if not walk:
        for x in (4, 9, 15, 20): rect(g, x, 20, 4, 6, col)
    else:
        rect(g, 2, 20, 4, 6, col); rect(g, 10, 20, 4, 5, col)
        rect(g, 14, 20, 4, 5, col); rect(g, 21, 20, 4, 6, col)

def head(g, col='b'):
    ell(g, 18.5, 12.5, 7.2, 6.3, col)
def eye(g, ecol='e'):
    ell(g, 21, 12.5, 2.1, 2.7, ecol)
    put(g, 20, 11, 'w'); put(g, 20, 12, 'w'); put(g, 22, 14, 'w')
    put(g, 25, 14, 'n'); put(g, 24, 14, 'n')
def body(g, col='b'):
    ell(g, 9.5, 18.5, 7.5, 4.8, col); rect(g, 12, 16, 12, 5, col)  # 胸部连接前腿，之后被颈毛/头盖住

def ears_big(g, col='b', inner='i'):
    poly(g, [(12,0),(9.5,10),(16,9)], col); poly(g, [(12,2),(10.8,8.5),(14.5,8)], inner)
    poly(g, [(21,0),(17.5,9),(24,10)], col); poly(g, [(21,2),(18.8,8),(22.5,8.5)], inner)
def ears_fin(g, col='l', inner='l'):   # 水伊布：宽鳍耳 + 颊鳍
    poly(g, [(9,2),(11,10),(17,9)], col); poly(g, [(20,1),(18,10),(25,9)], col)
    poly(g, [(23,11),(28,9),(27,15)], col)
def ears_spike(g, col='b', inner='i'):
    poly(g, [(12,0),(10,10),(15,9)], col); poly(g, [(21,0),(18,9),(24,10)], col)
    poly(g, [(16,2),(14,9),(18,8)], col)
def ears_leaf(g, col='L', inner='L'):
    poly(g, [(5,4),(10,10),(15,8),(8,3)], col); poly(g, [(26,3),(24,10),(18,9),(21,2)], col)
    put(g,6,5,'G'); put(g,7,6,'G'); put(g,8,7,'G'); put(g,9,8,'G')
    put(g,25,4,'G'); put(g,24,5,'G'); put(g,23,6,'G'); put(g,22,7,'G')
def ears_diamond(g, col='D', inner='D'):
    poly(g, [(12,0),(9,5),(12,10),(15,5)], col); poly(g, [(21,0),(18,5),(21,10),(24,5)], col)
    poly(g, [(12,2),(10.5,5),(12,8),(13.5,5)], 'b'); poly(g, [(21,2),(19.5,5),(21,8),(22.5,5)], 'b')

def tail_bushy(g, col='b', tip='l'):
    ell(g, 5, 12, 5.2, 4.3, col); ell(g, 3.5, 9.5, 3.2, 2.6, tip)
    put(g, 1, 7, tip); put(g, 3, 7, tip); put(g, 5, 7, tip)
def tail_fish(g, col='b', fin='D'):
    poly(g, [(5,16),(1,8),(3,8),(7,14)], col); poly(g, [(0,6),(3,9),(1,10),(3,13),(0,14),(5,10)], fin)
def tail_spike(g, col='b', tip='w'):
    poly(g, [(6,17),(2,10),(6,11),(5,14),(9,16)], tip); poly(g, [(2,12),(5,13),(4,15)], tip)
def tail_leaf(g, col='L'):
    poly(g, [(6,16),(0,9),(3,8),(8,14)], col); poly(g, [(0,7),(5,8),(3,12),(0,10)], col)
    put(g,2,9,'G'); put(g,3,10,'G'); put(g,4,11,'G')
def tail_fork(g, col='b'):
    poly(g, [(5,17),(3,9),(5,9),(7,16)], col); poly(g, [(3,10),(1,6),(3,7),(5,10)], col); poly(g, [(4,10),(6,6),(7,8),(5,11)], col)
def tail_thin(g, col='b', ring='x'):
    poly(g, [(5,17),(1,8),(4,8),(7,16)], col)
    put(g,3,11,ring); put(g,4,11,ring); put(g,3,12,ring); put(g,4,12,ring); put(g,5,12,ring)

def ruff_fluffy(g, col='l'):
    ell(g, 16, 19, 7.5, 4.2, col)
    for cx in (10, 13, 16, 19, 22): ell(g, cx, 21.5, 1.8, 1.8, col)
def ruff_spiky(g, col='w'):
    poly(g, [(8,16),(10,24),(13,17),(15,25),(18,17),(21,25),(24,17),(25,22),(25,16)], col)
def ruff_fin(g, col='l'):
    poly(g, [(11,16),(14,21),(16,17),(19,22),(22,17),(24,20),(24,16)], col)

PALS = {
 'eevee':   dict(o='#3a2010', b='#c98a46', d='#9a5f2b', l='#f6e8c8', i='#5c3a22', e='#2b1a10', w='#ffffff', n='#2b1a10'),
 'vaporeon':dict(o='#1b4a66', b='#5fc3e6', d='#3b93b8', l='#f6efc8', i='#f6efc8', e='#1b1a2a', w='#ffffff', n='#1b4a66', D='#2a6f99'),
 'jolteon': dict(o='#5a4a0a', b='#f5d33f', d='#c9a327', l='#ffffff', i='#8a6a10', e='#2b1a10', w='#ffffff', n='#2b1a10'),
 'flareon': dict(o='#5a2208', b='#ee6a2a', d='#b84a16', l='#f8e6a4', i='#f8e6a4', e='#2b1a10', w='#ffffff', n='#2b1a10'),
 'leafeon': dict(o='#3f5a1e', b='#efe3b8', d='#c4b07a', l='#efe3b8', i='#7cc043', e='#2b1a10', w='#ffffff', n='#4a3a20', L='#7cc043', G='#3f8a2a'),
 'glaceon': dict(o='#1e4a70', b='#a8dcf3', d='#6fb3d9', l='#a8dcf3', i='#2f6a9c', e='#1b1a2a', w='#ffffff', n='#1e4a70', D='#2f6a9c'),
 'espeon':  dict(o='#4a2a5e', b='#cfa3e3', d='#a070bf', l='#cfa3e3', i='#b283cf', e='#2b1a10', w='#ffffff', n='#4a2a5e', x='#e8323f'),
 'umbreon': dict(o='#0c0c12', b='#34343f', d='#22222a', l='#34343f', i='#22222a', e='#e8323f', w='#ffe08a', n='#0c0c12', x='#f5d442'),
 'sylveon': dict(o='#6a3250', b='#f6c4d8', d='#d892b0', l='#ffffff', i='#7fb0e6', e='#2b1a10', w='#ffffff', n='#6a3250', x='#7fb0e6', p='#ff6b9a'),
}

def build(form, walk):
    g = new(); P = lambda fn, *a, **k: part(g, fn, *a, **k)
    if form == 'eevee':
        P(tail_bushy); P(lambda g: (body(g), legs(g, walk))); P(ruff_fluffy); P(head); P(ears_big); eye(g)
    elif form == 'vaporeon':
        P(tail_fish); P(lambda g: (body(g), legs(g, walk))); P(ruff_fin); P(head); P(ears_fin); eye(g)
        for x in range(5, 13): put(g, x, 14 - (x%2), 'D')
    elif form == 'jolteon':
        P(tail_spike); P(lambda g: (body(g), poly(g, [(3,15),(5,11),(7,14),(9,10),(11,14),(13,11),(15,15)], 'b'), legs(g, walk))); P(ruff_spiky); P(head); P(ears_spike); eye(g)
    elif form == 'flareon':
        P(tail_bushy, 'l', 'l'); P(lambda g: (body(g), legs(g, walk))); P(ruff_fluffy); P(head); P(ears_big); P(lambda g: ell(g, 17, 6.5, 3.2, 1.8, 'l')); eye(g)
    elif form == 'leafeon':
        P(tail_leaf); P(lambda g: (body(g), legs(g, walk, 'd'))); P(head); P(ears_leaf); P(lambda g: poly(g, [(16,6),(18,1),(20,6)], 'L')); eye(g)
    elif form == 'glaceon':
        P(tail_fish, 'b', 'D'); P(lambda g: (body(g), legs(g, walk))); P(head); P(ears_diamond); P(lambda g: (rect(g, 10, 10, 2, 4, 'D'), rect(g, 25, 10, 2, 4, 'D'))); eye(g)
    elif form == 'espeon':
        P(tail_fork); P(lambda g: (body(g), legs(g, walk))); P(head); P(ears_big); eye(g)
        for x, y in ((19,8),(20,8),(19,9),(20,9),(18,8),(21,8)): put(g, x, y, 'x')
    elif form == 'umbreon':
        P(tail_thin); P(lambda g: (body(g), legs(g, walk))); P(head); P(ears_big, 'b', 'b'); eye(g)
        rect(g, 11, 3, 3, 2, 'x'); rect(g, 20, 3, 3, 2, 'x'); ell(g, 18.5, 8.5, 2, 1.3, 'x')
        rect(g, 5, 23, 2, 1, 'x'); rect(g, 21, 23, 2, 1, 'x'); ell(g, 9, 17, 2.2, 1.5, 'x')
    elif form == 'sylveon':
        P(tail_bushy, 'b', 'l'); P(lambda g: (body(g), legs(g, walk))); P(ruff_fluffy, 'l'); P(head); P(ears_big, 'b', 'i'); eye(g)
        rect(g, 10, 4, 3, 2, 'x'); rect(g, 19, 4, 3, 2, 'x'); ell(g, 13, 18, 1.8, 1.4, 'p')
        for x, y in [(12,19),(11,20),(10,21),(9,22),(8,23),(7,24),(14,19),(13,20),(12,21),(11,22),(10,23)]: put(g, x, y, 'x')
    return [''.join(r) for r in g]

# 用法：python3 tools/gen_sprites.py  —— 重新生成 9 种伊布的像素图并写入 index.html
import os
out = {}
for f in PALS:
    out[f] = {'pal': PALS[f], 'frames': [build(f, 0), build(f, 1)]}
html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
html = open(html_path, encoding='utf-8').read()
begin, end = '/* SPRITE_DATA_BEGIN */', '/* SPRITE_DATA_END */'
i, j = html.index(begin) + len(begin), html.index(end)
html = html[:i] + '\nconst SPRITE_DATA = ' + json.dumps(out, separators=(',', ':')) + ';\n' + html[j:]
open(html_path, 'w', encoding='utf-8').write(html)
print('sprites written into index.html')
