# 用法：python3 tools/extract/extract_sheet.py <拼贴图.png>
# 从 3x3 排列的伊布拼贴图中切出 9 只、还原为原始像素、生成闪光配色，输出 out/*.png、sheet_preview.png 和 sprites_b64.json
# （之后用 python3 tools/embed_sprites.py sprites_b64.json 写入 index.html）
import os, sys
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, os, json, base64, colorsys, io
from PIL import Image
from lib import *
im = load(sys.argv[1] if len(sys.argv) > 1 else 'sheet.png'); Hh = im.shape[0]
bg = np.array([201., 190., 230.])
is_bg = lambda c: np.sqrt(((c - bg) ** 2).sum()) < 16
mask = (np.sqrt(((im - bg) ** 2).sum(axis=2)) > 60) & (np.arange(Hh)[:, None] < 505)
comps = rows_sort(components(mask, 2000), 3)
names = ['vaporeon', 'jolteon', 'flareon', 'espeon', 'eevee', 'umbreon', 'leafeon', 'sylveon', 'glaceon']
gray = im.mean(axis=2)

def fit_grid2(sub, lo, hi):
    """纯度法：选使每格内部颜色最均匀的 (间距, 相位)。横纵共用间距。"""
    hh, ww = sub.shape
    def purity(axis, p, ph):
        n = ww if axis == 0 else hh
        cen = np.arange(ph + p / 2, n - 1, p)
        idx = np.round(cen).astype(int); idx = idx[(idx >= 1) & (idx < n - 1)]
        if len(idx) < 3: return 1e9
        if axis == 0: a, b, c = sub[:, idx - 1], sub[:, idx], sub[:, idx + 1]
        else: a, b, c = sub[idx - 1, :], sub[idx, :], sub[idx + 1, :]
        return (np.abs(a - b) + np.abs(c - b)).mean()
    best = (1e9, 0, (0, 0))
    for p in np.arange(lo, hi, 0.02):
        tot = 0; phs = []
        for axis in (0, 1):
            bb = min((purity(axis, p, ph), ph) for ph in np.arange(0, p, 0.2))
            tot += bb[0]; phs.append(bb[1])
        if tot < best[0]: best = (tot, p, tuple(phs))
    return [(best[1], best[2][0]), (best[1], best[2][1])]

def sample2(im, x0, y0, x1, y1, px, phx, py, phy):
    cols = []; cx = x0 + phx + px / 2
    while cx < x1: cols.append(cx); cx += px
    rows = []; cy = y0 + phy + py / 2
    while cy < y1: rows.append(cy); cy += py
    grid = []
    for cy in rows:
        row = []
        for cx in cols:
            rx, ry = px * 0.3, py * 0.3
            patch = im[int(round(cy - ry)):int(round(cy + ry)) + 1, int(round(cx - rx)):int(round(cx + rx)) + 1].reshape(-1, 3)
            d = np.sqrt(((patch - bg) ** 2).sum(axis=1))
            if (d < 16).mean() >= 0.45: row.append(None)
            else:
                fg = patch[d >= 16] if (d >= 16).any() else patch
                row.append(tuple(int(v) for v in np.median(fg, axis=0)))
        grid.append(row)
    return grid

def clean(g):
    h, w = len(g), len(g[0])
    for _ in range(2):
        out = [r[:] for r in g]
        for y in range(h):
            for x in range(w):
                if g[y][x] is None: continue
                nb = sum(1 for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= y+dy < h and 0 <= x+dx < w and g[y+dy][x+dx] is not None)
                near_bg = np.sqrt(((np.array(g[y][x]) - bg) ** 2).sum()) < 70
                if nb == 0 or (nb <= 2 and near_bg): out[y][x] = None
        g = out
    return crop_grid(g)

FIXED = dict(vaporeon=7.5, jolteon=7.9, flareon=7.7, espeon=7.8, eevee=7.3, umbreon=7.2, leafeon=8.4, sylveon=8.4, glaceon=8.5)
def best_phase(sub, p, axis):
    hh, ww = sub.shape; n = ww if axis == 0 else hh; best = (1e9, 0)
    for ph in np.arange(0, p, 0.2):
        cen = np.arange(ph + p / 2, n - 1, p); idx = np.round(cen).astype(int); idx = idx[(idx >= 1) & (idx < n - 1)]
        if axis == 0: a, b, c = sub[:, idx - 1], sub[:, idx], sub[:, idx + 1]
        else: a, b, c = sub[idx - 1, :], sub[idx, :], sub[idx + 1, :]
        sc = (np.abs(a - b) + np.abs(c - b)).mean()
        if sc < best[0]: best = (sc, ph)
    return best[1]
def despeckle(g):
    from collections import Counter
    h, w = len(g), len(g[0]); cnt = Counter(v for r in g for v in r if v); total = sum(cnt.values())
    for _ in range(2):
        out = [r[:] for r in g]
        for y in range(h):
            for x in range(w):
                v = g[y][x]
                if v is None: continue
                nb = [g[y+dy][x+dx] for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= y+dy < h and 0 <= x+dx < w and g[y+dy][x+dx] is not None]
                if len(nb) >= 3:
                    c, n = Counter(nb).most_common(1)[0]
                    if n >= 3 and c != v and cnt[v] < total * 0.03: out[y][x] = c
        g = out
    return g
grids = {}
for c, name in zip(comps, names):
    x0, x1, y0, y1 = c['x0'] - 3, c['x1'] + 3, c['y0'] - 3, c['y1'] + 3
    p = FIXED[name]; sub = gray[y0:y1, x0:x1]
    phx, phy = best_phase(sub, p, 0), best_phase(sub, p, 1); px = py = p
    g = clean(crop_grid(sample2(im, x0, y0, x1, y1, px, phx, py, phy)))
    pal = merge_palette([v for r in g for v in r if v], 34, 3)
    g = [[(snap(v, pal) if v else None) for v in r] for r in g]
    g = despeckle(g)
    grids[name] = g
    print(name, 'pitch', round(px, 2), round(py, 2), 'size', len(g[0]), 'x', len(g), 'colors', len(pal))

# ---------- 闪光配色：按色相区间做色调映射 ----------
def hsl(c):
    h, l, s = colorsys.rgb_to_hls(c[0]/255, c[1]/255, c[2]/255); return h*360, s, l
def rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360)/360, max(0, min(1, l)), max(0, min(1, s))); return (int(r*255), int(g*255), int(b*255))
def in_hue(h, lo, hi): return (lo <= h <= hi) if lo <= hi else (h >= lo or h <= hi)
SHINY = {
  'eevee':    [((15, 50, 0.25, 1), lambda h,s,l: (38, s*0.35, min(0.9, l+0.14)))],                 # 银白
  'vaporeon': [((170, 225, 0.25, 1), lambda h,s,l: (300, s*0.9, l+0.03))],                        # 紫粉
  'jolteon':  [((35, 70, 0.3, 1), lambda h,s,l: (78, s, l))],                                     # 黄绿
  'flareon':  [((0, 40, 0.4, 1), lambda h,s,l: (46, s, min(0.85, l+0.12)))],                       # 金黄
  'espeon':   [((250, 330, 0.15, 1), lambda h,s,l: (140, s*0.8, l))],                              # 薄荷绿
  'umbreon':  [((35, 70, 0.4, 1), lambda h,s,l: (210, s, l))],                                    # 蓝环
  'leafeon':  [((60, 160, 0.3, 1), lambda h,s,l: (h+25, min(1, s*1.2), min(0.85, l+0.06))), ((20, 60, 0.2, 1), lambda h,s,l: (h+10, s, min(0.9, l+0.05)))],
  'glaceon':  [((170, 230, 0.2, 1), lambda h,s,l: (165, min(1, s*1.1), l))],                      # 青绿
  'sylveon':  [((305, 20, 0.2, 1), lambda h,s,l: (205, s, l)), ((185, 240, 0.2, 1), lambda h,s,l: (335, s, l))],  # 粉蓝互换
}
def shinify(name, g):
    out = []
    for r in g:
        row = []
        for v in r:
            if v is None: row.append(None); continue
            h, s, l = hsl(v); nv = v
            if l > 0.12 and l < 0.97:
                for (lo, hi, smin, smax), fn in SHINY[name]:
                    if in_hue(h, lo, hi) and smin <= s <= smax:
                        nh, ns, nl = fn(h, s, l); nv = rgb(nh, ns, nl); break
            row.append(nv)
        out.append(row)
    return out
shiny = {n: shinify(n, g) for n, g in grids.items()}

os.makedirs('out', exist_ok=True)
sheet = Image.new('RGBA', (9 * 150, 300), (201, 190, 230, 255)); data = {}
for i, name in enumerate(names):
    for kind, g in (('normal', grids[name]), ('shiny', shiny[name])):
        img = to_image(g, None, flip=True); img.save(f'out/{name}_{kind}.png')
        big = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
        sheet.paste(big, (i * 150 + 5, 5 + (0 if kind == 'normal' else 150)), big)
        buf = io.BytesIO(); img.save(buf, 'PNG'); data.setdefault(name, {})[kind] = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
sheet.save('sheet_preview.png')
json.dump(data, open('sprites_b64.json', 'w'))
print('total b64 bytes', sum(len(v[k]) for v in data.values() for k in v))
