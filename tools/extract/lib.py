import numpy as np
from PIL import Image
from collections import deque

def load(path):
    return np.array(Image.open(path).convert('RGB')).astype(float)

def components(mask, min_pts=300, dilate=2):
    Hh, Ww = mask.shape
    dil = mask.copy()
    for _ in range(dilate):
        d2 = dil.copy(); d2[1:] |= dil[:-1]; d2[:-1] |= dil[1:]; d2[:, 1:] |= dil[:, :-1]; d2[:, :-1] |= dil[:, 1:]; dil = d2
    lab = np.zeros((Hh, Ww), int); comps = []
    for y0 in range(Hh):
        for x0 in range(Ww):
            if dil[y0, x0] and lab[y0, x0] == 0:
                cid = len(comps) + 1; lab[y0, x0] = cid; q = deque([(y0, x0)]); pts = 0; ys = [y0, y0]; xs = [x0, x0]
                while q:
                    y, x = q.popleft(); pts += 1
                    ys[0] = min(ys[0], y); ys[1] = max(ys[1], y); xs[0] = min(xs[0], x); xs[1] = max(xs[1], x)
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = y+dy, x+dx
                        if 0 <= ny < Hh and 0 <= nx < Ww and dil[ny, nx] and lab[ny, nx] == 0: lab[ny, nx] = cid; q.append((ny, nx))
                comps.append(dict(n=pts, y0=ys[0], y1=ys[1], x0=xs[0], x1=xs[1]))
    return [c for c in comps if c['n'] >= min_pts]

def rows_sort(comps, n_rows):
    comps = sorted(comps, key=lambda c: (c['y0'] + c['y1']) / 2)
    # 按 y 中心聚成 n_rows 行（相邻间距最大的地方切开）
    ys = [(c['y0'] + c['y1']) / 2 for c in comps]
    gaps = sorted(range(1, len(ys)), key=lambda i: ys[i] - ys[i-1], reverse=True)[:n_rows-1]
    cuts = sorted(gaps); rows = []; start = 0
    for ccut in cuts + [len(comps)]:
        rows.append(sorted(comps[start:ccut], key=lambda c: (c['x0'] + c['x1']) / 2)); start = ccut
    return [c for r in rows for c in r]

def fit_grid(gray_sub, pitch_range, step=0.02):
    """联合搜索 (间距, 相位)，使格线落在梯度最大处。返回 (pitch, phase) 两个方向。"""
    res = []
    for axis in (1, 0):
        prof = np.abs(np.diff(gray_sub, axis=axis)).sum(axis=1 - axis)
        n = len(prof); best = (-1, 0, 0)
        for p in np.arange(pitch_range[0], pitch_range[1], step):
            k = np.arange(0, int(n / p) + 1)
            for ph in np.arange(0, p, 0.25):
                pos = np.round(ph + k * p).astype(int); pos = pos[(pos >= 0) & (pos < n)]
                s = prof[pos].mean()
                if s > best[0]: best = (s, p, ph)
        res.append((best[1], best[2]))
    return res  # [(px, phx), (py, phy)]

def sample(im, x0, y0, x1, y1, px, phx, py, phy, is_bg):
    cols = []; cx = x0 + phx + px / 2
    while cx < x1: cols.append(cx); cx += px
    rows = []; cy = y0 + phy + py / 2
    while cy < y1: rows.append(cy); cy += py
    grid = []
    for cy in rows:
        row = []
        for cx in cols:
            xi, yi = int(round(cx)), int(round(cy))
            patch = im[max(0, yi-1):yi+2, max(0, xi-1):xi+2].reshape(-1, 3)
            col = np.median(patch, axis=0)
            row.append(None if is_bg(col) else tuple(int(v) for v in col))
        grid.append(row)
    return grid

def crop_grid(grid):
    ys = [y for y, r in enumerate(grid) if any(v for v in r)]
    xs = [x for x in range(len(grid[0])) if any(r[x] for r in grid)]
    return [r[xs[0]:xs[-1]+1] for r in grid[ys[0]:ys[-1]+1]]

def merge_palette(colors, thr=26, min_n=2):
    pal = []
    for col in colors:
        for p in pal:
            if np.sqrt(sum((a - b) ** 2 for a, b in zip(col, p['c']))) < thr: p['n'] += 1; p['sum'] = [s + v for s, v in zip(p['sum'], col)]; break
        else: pal.append(dict(c=col, n=1, sum=list(col)))
    return [tuple(int(v / p['n']) for v in p['sum']) for p in pal if p['n'] >= min_n]

def snap(col, pal):
    return min(pal, key=lambda p: sum((a - b) ** 2 for a, b in zip(col, p)))

def to_image(grid, pal=None, flip=True):
    h, w = len(grid), len(grid[0])
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            if c: img.putpixel((w - 1 - x if flip else x, y), (snap(c, pal) if pal else c) + (255,))
    return img
